"""
billing.py — Pay-as-you-go credit + premium-model metering for Grg AI.

Model:
  * Free models (Groq / OpenRouter ':free') stay free — no wallet needed.
  * Premium models (paid OpenRouter) are usable ONLY when the user has funds:
      - an active Grg-Pro subscription with monthly premium budget left, OR
      - a prepaid pay-as-you-go wallet balance.
  * Every premium call deducts (real_api_cost * MARKUP) so a profit margin is
    always kept: the user can never consume more real API than they paid.

Display uses CREDITS (1 credit = €0.01); euros are never shown to the user.
Firestore fields on users/{uid}:
  wallet_eur       float  — prepaid pay-as-you-go balance (EUR, internal)
  plan_eur         float  — remaining monthly Pro allowance as a charge-budget (EUR)
  plan_period_end  int    — unix ts when the allowance resets
  tokens_used      int    — lifetime premium tokens consumed
  usage_models     map    — per-model {tokens, credits} breakdown
  spent_eur        float  — lifetime spend (plan + wallet)
"""

import os
import time

from stripe_handler import _get_user_ref, FIREBASE_AVAILABLE, check_rate_limit
try:
    from stripe_handler import db as _db
except Exception:  # noqa: BLE001
    _db = None

try:
    from firebase_admin import firestore
except Exception:  # noqa: BLE001
    firestore = None

# ─────────────── TUNABLE ECONOMICS (safe to change) ───────────────
# Two independent ways to use premium models (the user picks either):
#   1) a PLAN (Grg-Pro): a fixed monthly TOKEN allowance — usage, not money.
#   2) CREDITS (pay-as-you-go): a prepaid € wallet, charged real_cost*MARKUP.
# A Pro user spends the plan allowance first; when it runs out, premium falls
# back to their credits (if any). A user with no plan uses credits only.
MARKUP = 1.34                    # 25% profit margin: EVERY charge = real_cost * MARKUP,
                                 # so profit is guaranteed on every model (plan OR credits).
TOPUP_PACKS_EUR = [5, 10, 20]
CREDIT_EUR = 0.01                # 1 credit = €0.01 of the user's balance (display unit, no € shown)
PRO_MONTHLY_EUR = 5.0            # Grg-Pro monthly allowance as a charge-budget (= 500 credits)
CURRENCY = "eur"

# € per 1,000,000 tokens (blended 35% input / 65% output — the real usage weighting).
# Sourced from live OpenRouter pricing 2026-09-22 (USD figures used directly as EUR,
# which leaves a small FX buffer on top of the 25% MARKUP margin). These are raw costs;
# the margin is added via MARKUP at charge time.
MODEL_PRICE_EUR = {
    # OpenAI
    "openai/gpt-5.6": 8.5,
    "openai/gpt-5.5": 21.0,
    "openai/gpt-5.2": 9.7,
    "openai/gpt-5.1-codex": 7.0,
    "openai/gpt-4o": 7.4,
    # Anthropic
    "anthropic/claude-opus-4.6": 18.0,
    "anthropic/claude-opus-4.8": 18.0,
    "anthropic/claude-sonnet-5": 7.2,
    "anthropic/claude-fable": 3.6,
    # Google
    "google/gemini-3.1-pro-preview": 8.5,
    "google/gemini-3.1-pro": 8.5,
    "google/gemini-2.5-pro": 7.0,
    # DeepSeek
    "deepseek/deepseek-v4": 1.0,
    "deepseek/deepseek-v4-pro": 1.5,
    "deepseek/deepseek-r1": 1.9,
    # Meta
    "meta-llama/llama-4-scout": 0.25,
    "meta-llama/llama-4-maverick": 0.5,
    # xAI
    "x-ai/grok-4": 4.0,
    "x-ai/grok-4.1": 4.6,
    "x-ai/grok-4.6": 4.6,
    # Mistral
    "mistralai/mistral-large-2": 4.6,
    "mistralai/codestral-2508": 0.7,
    # Moonshot
    "moonshotai/kimi-k3": 10.8,
    "moonshotai/kimi-k2.6": 2.9,
    "moonshotai/kimi-k2.7-code": 2.4,
    # Qwen (Alibaba)
    "qwen/qwen3-max": 2.8,
    "qwen/qwen3-coder": 0.75,
    "qwen/qwen3-vl": 1.3,
    # GLM
    "z-ai/glm-5.3": 1.6,
}
MODEL_PRICE_DEFAULT = 6.0
# Flat € per image for premium image models (charged * MARKUP).
IMAGE_PRICE_EUR = 0.04


def model_price_eur(model: str) -> float:
    """€ per 1M tokens for a model (blended)."""
    return MODEL_PRICE_EUR.get(model, MODEL_PRICE_DEFAULT)


def eur_to_credits(eur: float) -> int:
    return int(round(float(eur) / CREDIT_EUR))


def model_credits_per_mtok(model: str) -> int:
    """Credits a model consumes per 1,000,000 tokens (real cost * MARKUP, in credits).
    Pricier models cost more credits → you can use them less, and vice-versa."""
    return int(round(model_price_eur(model) * MARKUP / CREDIT_EUR))


def model_rates():
    """{model_id: credits_per_1M_tokens} for every priced premium model."""
    return {m: model_credits_per_mtok(m) for m in MODEL_PRICE_EUR}


def _user_data(uid: str) -> dict:
    if not FIREBASE_AVAILABLE:
        return {}
    ref = _get_user_ref(uid)
    if not ref:
        return {}
    doc = ref.get()
    return doc.to_dict() if doc.exists else {}


def _roll_pro_period(data: dict) -> dict:
    """Refill the monthly Pro allowance (a charge-budget in EUR) if the period elapsed."""
    if data.get("plan") != "pro":
        return {"plan_eur": 0.0, "plan_period_end": 0}
    now = time.time()
    end = data.get("plan_period_end", 0) or 0
    if now > end or "plan_eur" not in data:
        return {"plan_eur": PRO_MONTHLY_EUR,
                "plan_period_end": int(now + 30 * 86400), "_reset": True}
    return {"plan_eur": float(data.get("plan_eur", 0.0)), "plan_period_end": end}


def get_account(uid: str) -> dict:
    """Full account snapshot for the Settings page."""
    rate = check_rate_limit(uid)
    data = _user_data(uid)
    pro = _roll_pro_period(data)
    if pro.get("_reset") and FIREBASE_AVAILABLE:
        ref = _get_user_ref(uid)
        if ref:
            ref.set({"plan_eur": pro["plan_eur"],
                     "plan_period_end": pro["plan_period_end"]}, merge=True)
    plan = data.get("plan", "free")
    wallet = float(data.get("wallet_eur", 0.0))
    plan_eur = float(pro.get("plan_eur", 0.0)) if plan == "pro" else 0.0
    has_credit = wallet > 0.0005
    return {
        "plan": plan,
        "currency": CURRENCY,
        "has_credit": has_credit,
        "wallet_eur": round(wallet, 4),          # internal only; never shown as a € balance
        "credits_balance": eur_to_credits(plan_eur + wallet),
        "plan_credits": eur_to_credits(plan_eur),
        "plan_credits_total": eur_to_credits(PRO_MONTHLY_EUR),
        "wallet_credits": eur_to_credits(wallet),
        "plan_period_end": pro.get("plan_period_end", 0),
        "premium_available": (plan_eur > 0.0005) or has_credit,
        "tokens_used": int(data.get("tokens_used", 0)),
        "usage_models": data.get("usage_models", {}),
        "model_rates": model_rates(),
        "credit_eur": CREDIT_EUR,
        "email": data.get("email"),
        "daily_used": rate.get("used", 0),
        "daily_limit": rate.get("limit", 0),
        "topup_packs": TOPUP_PACKS_EUR,
        "markup": MARKUP,
    }


def premium_allowed(uid: str) -> dict:
    """Whether the user can currently use premium models (plan allowance or credits)."""
    if not uid:
        return {"allowed": False, "reason": "sign_in"}
    data = _user_data(uid)
    pro = _roll_pro_period(data)
    plan = data.get("plan", "free")
    plan_eur = float(pro.get("plan_eur", 0.0)) if plan == "pro" else 0.0
    wallet = float(data.get("wallet_eur", 0.0))
    if plan_eur > 0.0005 or wallet > 0.0005:
        return {"allowed": True}
    return {"allowed": False, "reason": "no_funds"}


def charge_usage(uid: str, model: str, in_tokens: int, out_tokens: int, images: int = 0) -> dict:
    """Consume the plan's token allowance first (free to the user); charge any
    overflow tokens to the credit wallet at real_cost*MARKUP."""
    if not uid or not FIREBASE_AVAILABLE:
        return {"tokens": 0, "charged_eur": 0.0}
    ref = _get_user_ref(uid)
    if not ref:
        return {"tokens": 0, "charged_eur": 0.0}
    tokens = max(0, int(in_tokens)) + max(0, int(out_tokens))
    if tokens <= 0 and not images:
        return {"tokens": 0, "charged_eur": 0.0}

    data = ref.get().to_dict() or {}
    pro = _roll_pro_period(data)
    plan = data.get("plan", "free")
    plan_eur = float(pro.get("plan_eur", 0.0)) if plan == "pro" else 0.0
    wallet = float(data.get("wallet_eur", 0.0))

    # Full cost of the call, with the 25% margin baked in (guaranteed profit).
    real = tokens / 1_000_000.0 * model_price_eur(model)
    if images:
        real += images * IMAGE_PRICE_EUR
    charge = round(real * MARKUP, 6)
    # Spend the plan allowance first, then the pay-as-you-go wallet.
    from_plan = min(plan_eur, charge)
    from_wallet = min(wallet, charge - from_plan)
    spent = from_plan + from_wallet
    credits_spent = eur_to_credits(spent)

    # Per-model breakdown: tokens used + credits it consumed (adaptive per model rate).
    um = dict(data.get("usage_models", {}))
    cur = um.get(model, {"tokens": 0, "credits": 0})
    um[model] = {"tokens": int(cur.get("tokens", 0)) + tokens,
                 "credits": int(cur.get("credits", 0)) + credits_spent}
    updates = {
        "plan_eur": max(0.0, plan_eur - from_plan),
        "plan_period_end": pro.get("plan_period_end", 0),
        "wallet_eur": max(0.0, wallet - from_wallet),
        "spent_eur": firestore.Increment(spent) if firestore else round(float(data.get("spent_eur", 0.0)) + spent, 6),
        "tokens_used": firestore.Increment(tokens) if firestore else int(data.get("tokens_used", 0)) + tokens,
        "usage_models": um,
        "updated_at": firestore.SERVER_TIMESTAMP if firestore else int(time.time()),
    }
    ref.set(updates, merge=True)
    return {"tokens": tokens, "credits": credits_spent,
            "from_plan_eur": round(from_plan, 6), "from_wallet_eur": round(from_wallet, 6)}


def add_wallet_credit(uid: str, eur: float):
    """Credit a completed Stripe top-up to the wallet (non-idempotent)."""
    if not uid or not FIREBASE_AVAILABLE:
        return
    ref = _get_user_ref(uid)
    if not ref:
        return
    inc = firestore.Increment(float(eur)) if firestore else float(eur)
    ref.set({"wallet_eur": inc,
             "updated_at": firestore.SERVER_TIMESTAMP if firestore else int(time.time())}, merge=True)


def credit_topup_once(uid: str, session_id: str, eur: float) -> bool:
    """Credit a top-up to the wallet EXACTLY once per Stripe session.
    Both the webhook and the success-return confirm call this; the per-session
    marker doc makes it idempotent so a payment is never double-credited.
    Returns True if it credited now, False if already credited."""
    if not uid or not eur or not FIREBASE_AVAILABLE:
        return False
    eur = float(eur)
    if _db is not None and session_id:
        marker = _db.collection("users").document(uid).collection("topups").document(str(session_id))
        try:
            marker.create({"eur": eur, "at": firestore.SERVER_TIMESTAMP if firestore else int(time.time())})
        except Exception:  # AlreadyExists → already credited
            return False
    ref = _get_user_ref(uid)
    if not ref:
        return False
    inc = firestore.Increment(eur) if firestore else eur
    ref.set({"wallet_eur": inc,
             "updated_at": firestore.SERVER_TIMESTAMP if firestore else int(time.time())}, merge=True)
    return True


def grant_pro_budget(uid: str):
    """Give a Pro user their monthly allowance (charge-budget, on activation/renewal)."""
    if not uid or not FIREBASE_AVAILABLE:
        return
    ref = _get_user_ref(uid)
    if not ref:
        return
    ref.set({"plan_eur": PRO_MONTHLY_EUR,
             "plan_period_end": int(time.time() + 30 * 86400)}, merge=True)
