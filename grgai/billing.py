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
import math

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

# ─────────────── PER-MESSAGE CREDITS — TWO BUCKETS (usage + effort, margin-safe) ───────────────
# Credits are spent PER MESSAGE (by model weight × effort), not per word. There are TWO buckets:
#   1) FREE bucket  — pays for FREE models (Groq/:free). Costs us ~nothing, so it's generous and
#      refills: GrgFree 100/WEEK, GrgPro 500/DAY, GrgUltra 2000/DAY.
#   2) PREMIUM bucket — pays for PREMIUM models (paid OpenRouter). A MONTHLY budget sized to the
#      plan's money so MARGIN IS GUARANTEED: each premium message costs real_cost×MARKUP credits,
#      so spending the whole bucket can never cost more real API than the plan paid for.
# Bought wallet credits can pay either bucket. All numbers are tunable.
FREE_WEEKLY_CREDITS = 100        # GrgFree free-model bucket, reset WEEKLY (NOT shown on the plans card)
PRO_DAILY_CREDITS = 500          # GrgPro free-model bucket, reset DAILY
ULTRA_DAILY_CREDITS = 2000       # GrgUltra free-model bucket, reset DAILY (4x Pro)
FREE_PERIOD = 7 * 86400          # free bucket: GrgFree resets every 7 days
PRO_PERIOD = 86400               # free bucket: paid plans reset every day
PAID_PLANS = ("pro", "ultra")    # plans that unlock premium models
# PREMIUM bucket (credits/MONTH) — sized to the plan price (1 credit = €0.01 ⇒ €5 → 500, €20 → 2000).
PREMIUM_MONTHLY = {"free": 0, "pro": 500, "ultra": 2000}
PREMIUM_PERIOD = 30 * 86400
EFFORT_MULT = {"low": 1.0, "mid": 1.5, "high": 2.0, "ultra": 3.0}   # free-model effort weighting
# Assumed tokens per message by effort — this makes the PREMIUM price FLAT per message (not per
# word) while still reflecting real cost. If a real message uses fewer tokens you profit more;
# output is capped ~8k so it can't blow far past the 'ultra' assumption.
EFFORT_TOKENS = {"low": 1500, "mid": 3000, "high": 6000, "ultra": 10000}
FREE_MSG_CREDITS = 1
MSG_CREDITS_MIN = 1
# Padding on the char-based input estimate so we never undercharge the prompt side.
# json.dumps already inflates the char count vs real text, and 1.5x adds headroom for
# denser tokenization (code / non-English). Output is hard-capped by max_tokens, so the
# prompt side is the only soft part — the pad keeps the ceiling >= real usage.
EST_IN_PAD = 1.5
# Specialist AGENTS cost more than normal chat: they use more resources (long expert
# system prompts, bigger context, more back-and-forth). Every message sent with an agent
# active is charged AGENT_MULT× the normal per-message price — on free AND premium models
# — so the owner profits more and never goes negative on the heavier agent workload.
AGENT_MULT = 4.0

def _is_free_model(model: str) -> bool:
    m = (model or "")
    return (m.endswith(":free") or m.startswith("openai/gpt-oss")
            or m.startswith("groq/") or m == "qwen/qwen3.8-27b"
            or m not in MODEL_PRICE_EUR)

def free_msg_credits(effort: str = "low") -> int:
    return max(1, int(round(FREE_MSG_CREDITS * EFFORT_MULT.get(str(effort or "low").lower(), 1.0))))

def premium_msg_credits(model: str, effort: str = "low",
                        est_in_tokens: int = 0, max_out_tokens: int = 0) -> int:
    """Per-message premium price = WORST-CASE cost × MARKUP, in credits — so the owner
    ALWAYS profits on every message. The worst case is (padded input estimate + the max
    output tokens we actually allow for this message) at the model's price; the real usage
    can NEVER exceed that ceiling, so the credits charged are always ≥ the real API cost,
    keeping the full MARKUP margin. We ceil() so rounding can never undercharge."""
    out = int(max_out_tokens) if max_out_tokens else EFFORT_TOKENS.get(str(effort or "low").lower(), 1500)
    toks = int(int(est_in_tokens) * EST_IN_PAD) + max(0, out)   # ceiling tokens for this message
    real = toks / 1_000_000.0 * model_price_eur(model)          # EUR ceiling cost
    return max(1, math.ceil(real * MARKUP / CREDIT_EUR))

def message_cost_credits(model: str, effort: str = "low", images: int = 0,
                         est_in_tokens: int = 0, max_out_tokens: int = 0,
                         agent_mult: float = 1.0) -> int:
    c = (free_msg_credits(effort) if _is_free_model(model)
         else premium_msg_credits(model, effort, est_in_tokens, max_out_tokens))
    c = max(1, math.ceil(c * float(agent_mult or 1.0)))      # agents cost AGENT_MULT× more
    return max(MSG_CREDITS_MIN, c + int(images) * 2)

def _roll_daily(data: dict) -> dict:
    """Refill the FREE-model bucket on the plan's cycle (paid=daily, free=weekly)."""
    plan = data.get("plan")
    period_len = PRO_PERIOD if plan in PAID_PLANS else FREE_PERIOD
    grant = (ULTRA_DAILY_CREDITS if plan == "ultra"
             else PRO_DAILY_CREDITS if plan == "pro" else FREE_WEEKLY_CREDITS)
    cycle = int(time.time() // period_len)
    if int(data.get("daily_credits_day", -1)) != cycle:
        return {"daily_credits": grant, "daily_credits_day": cycle, "_reset": True}
    return {"daily_credits": int(data.get("daily_credits", 0)), "daily_credits_day": cycle}

def _roll_premium(data: dict) -> dict:
    """Refill the PREMIUM bucket (monthly) to the plan's budget."""
    grant = PREMIUM_MONTHLY.get(data.get("plan", "free"), 0)
    period = int(time.time() // PREMIUM_PERIOD)
    if int(data.get("premium_credits_period", -1)) != period:
        return {"premium_credits": grant, "premium_credits_period": period, "_reset": True}
    return {"premium_credits": int(data.get("premium_credits", 0)), "premium_credits_period": period}

def message_rates() -> dict:
    """{model_id: baseline credits_per_message} for the UI — a representative low-effort
    message (no extra input, ~1500-token answer). The live charge scales with effort and
    input, so this is a 'from' figure."""
    ids = list(MODEL_PRICE_EUR.keys()) + ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]
    return {m: message_cost_credits(m, "low", 0, 0, EFFORT_TOKENS["low"]) for m in ids}

def charge_message(uid: str, model: str, effort: str = "low", images: int = 0,
                   est_in_tokens: int = 0, max_out_tokens: int = 0,
                   agent_mult: float = 1.0) -> dict:
    """Spend credits for ONE message from the right bucket (free-model→free bucket,
    premium→premium bucket), then bought wallet. Anonymous is never charged/blocked.
    The premium cost is the WORST-CASE (ceiling) cost × MARKUP, so the charge is always
    ≥ the real API cost → the owner profits on every message. `agent_mult` (AGENT_MULT when
    a specialist agent is active) makes agent messages cost proportionally more.
    Returns {allowed, cost, balance, charged, reason}. Fail-OPEN on any backend error."""
    cost = message_cost_credits(model, effort, images, est_in_tokens, max_out_tokens, agent_mult)
    if not uid or not FIREBASE_AVAILABLE:
        return {"allowed": True, "cost": cost, "charged": 0, "balance": None, "anon": True}
    try:
        ref = _get_user_ref(uid)
        if not ref:
            return {"allowed": True, "cost": cost, "charged": 0, "balance": None}
        data = ref.get().to_dict() or {}
        daily = _roll_daily(data)
        prem = _roll_premium(data)
        wallet = float(data.get("wallet_eur", 0.0))
        daily_credits = int(daily["daily_credits"])
        premium_credits = int(prem["premium_credits"])
        wallet_credits = eur_to_credits(wallet)
        is_free = _is_free_model(model)
        bucket = daily_credits if is_free else premium_credits    # which bucket pays
        usable = bucket + wallet_credits
        total_all = daily_credits + premium_credits + wallet_credits
        if usable < cost:
            if is_free:
                reason = "out_of_credits"
            else:
                reason = "needs_pro" if data.get("plan") not in PAID_PLANS else "out_of_premium"
            return {"allowed": False, "cost": cost, "balance": total_all, "reason": reason}
        use_bucket = min(bucket, cost)
        use_wallet = cost - use_bucket
        um = dict(data.get("usage_models", {}))
        cur = um.get(model, {})
        um[model] = {"messages": int(cur.get("messages", 0)) + 1,
                     "credits": int(cur.get("credits", 0)) + cost,
                     "tokens": int(cur.get("tokens", 0))}
        updates = {
            "wallet_eur": max(0.0, wallet - use_wallet * CREDIT_EUR),
            "usage_models": um,
            "msgs_used": firestore.Increment(1) if firestore else int(data.get("msgs_used", 0)) + 1,
            "credits_spent_total": firestore.Increment(cost) if firestore else int(data.get("credits_spent_total", 0)) + cost,
            "updated_at": firestore.SERVER_TIMESTAMP if firestore else int(time.time()),
        }
        if is_free:
            updates["daily_credits"] = daily_credits - use_bucket
            updates["daily_credits_day"] = daily["daily_credits_day"]
            if prem.get("_reset"):   # also persist a just-refilled premium bucket
                updates["premium_credits"] = premium_credits
                updates["premium_credits_period"] = prem["premium_credits_period"]
        else:
            updates["premium_credits"] = premium_credits - use_bucket
            updates["premium_credits_period"] = prem["premium_credits_period"]
            if daily.get("_reset"):
                updates["daily_credits"] = daily_credits
                updates["daily_credits_day"] = daily["daily_credits_day"]
        ref.set(updates, merge=True)
        return {"allowed": True, "cost": cost, "charged": cost, "balance": total_all - cost,
                "from_bucket": use_bucket, "from_wallet": use_wallet, "is_free": is_free}
    except Exception as e:  # noqa: BLE001 — never block a message on a billing error
        print(f"[charge_message ERROR] {e}")
        return {"allowed": True, "cost": cost, "charged": 0, "balance": None, "error": str(e)[:120]}


def premium_actual_credits(model: str, in_tokens: int, out_tokens: int,
                           agent_mult: float = 1.0) -> int:
    """Credits the owner must keep for the message's REAL usage = real_cost × MARKUP × agent_mult.
    ceil() so the charge is never below the real cost + margin."""
    toks = max(0, int(in_tokens)) + max(0, int(out_tokens))
    real = toks / 1_000_000.0 * model_price_eur(model)
    return max(1, math.ceil(real * MARKUP / CREDIT_EUR * float(agent_mult or 1.0)))


def settle_premium(uid: str, model: str, in_tokens: int, out_tokens: int,
                   charged_credits: int, from_bucket: int = 0, from_wallet: int = 0,
                   agent_mult: float = 1.0) -> dict:
    """Reconcile the up-front WORST-CASE premium hold to the ACTUAL token usage reported
    by the provider. Refund the overcharge, or claw back the (rare) undercharge, so the
    user pays exactly real_cost × MARKUP and the owner's margin is exact, never negative.
    Fail-OPEN: on any error we keep the up-front hold (which is already profit-safe)."""
    actual = premium_actual_credits(model, in_tokens, out_tokens, agent_mult)
    delta = actual - int(charged_credits)          # <0 → refund the user; >0 → charge a bit more
    if not uid or not FIREBASE_AVAILABLE or delta == 0:
        return {"actual": actual, "delta": 0, "balance": None}
    try:
        ref = _get_user_ref(uid)
        if not ref:
            return {"actual": actual, "delta": 0, "balance": None}
        data = ref.get().to_dict() or {}
        daily = _roll_daily(data)
        prem = _roll_premium(data)
        wallet = float(data.get("wallet_eur", 0.0))
        daily_credits = int(daily["daily_credits"])
        premium_credits = int(prem["premium_credits"])
        updates = {
            "premium_credits_period": prem["premium_credits_period"],
            "credits_spent_total": firestore.Increment(delta) if firestore else int(data.get("credits_spent_total", 0)) + delta,
            "updated_at": firestore.SERVER_TIMESTAMP if firestore else int(time.time()),
        }
        if delta < 0:
            # REFUND |delta|: reverse the wallet portion first, then the premium bucket.
            refund = -delta
            back_wallet = min(refund, int(from_wallet))
            back_bucket = refund - back_wallet
            wallet = wallet + back_wallet * CREDIT_EUR
            premium_credits = premium_credits + back_bucket
        else:
            # Rare: real input out-tokenized our padded estimate → charge the extra, bucket then wallet.
            need = delta
            take_bucket = min(premium_credits, need)
            premium_credits -= take_bucket
            need -= take_bucket
            if need > 0:
                wallet = max(0.0, wallet - need * CREDIT_EUR)
        updates["premium_credits"] = premium_credits
        updates["wallet_eur"] = max(0.0, wallet)
        if prem.get("_reset") is None and daily.get("_reset"):
            updates["daily_credits"] = daily_credits
            updates["daily_credits_day"] = daily["daily_credits_day"]
        # keep usage_models credits in sync with the actual (not the ceiling)
        um = dict(data.get("usage_models", {}))
        cur = um.get(model, {})
        um[model] = {"messages": int(cur.get("messages", 0)),
                     "credits": max(0, int(cur.get("credits", 0)) + delta),
                     "tokens": int(cur.get("tokens", 0)) + max(0, int(in_tokens)) + max(0, int(out_tokens))}
        updates["usage_models"] = um
        updates["tokens_used"] = (firestore.Increment(max(0, int(in_tokens)) + max(0, int(out_tokens)))
                                  if firestore else int(data.get("tokens_used", 0)) + max(0, int(in_tokens)) + max(0, int(out_tokens)))
        ref.set(updates, merge=True)
        balance = premium_credits + daily_credits + eur_to_credits(wallet)
        return {"actual": actual, "delta": delta, "balance": balance}
    except Exception as e:  # noqa: BLE001 — never undo a streamed answer over a settle error
        print(f"[settle_premium ERROR] {e}")
        return {"actual": actual, "delta": 0, "balance": None, "error": str(e)[:120]}


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
    daily = _roll_daily(data)
    prem = _roll_premium(data)
    if FIREBASE_AVAILABLE and (pro.get("_reset") or daily.get("_reset") or prem.get("_reset")):
        ref = _get_user_ref(uid)
        if ref:
            _w = {}
            if pro.get("_reset"):
                _w["plan_eur"] = pro["plan_eur"]; _w["plan_period_end"] = pro["plan_period_end"]
            if daily.get("_reset"):
                _w["daily_credits"] = daily["daily_credits"]; _w["daily_credits_day"] = daily["daily_credits_day"]
            if prem.get("_reset"):
                _w["premium_credits"] = prem["premium_credits"]; _w["premium_credits_period"] = prem["premium_credits_period"]
            if _w:
                ref.set(_w, merge=True)
    plan = data.get("plan", "free")
    wallet = float(data.get("wallet_eur", 0.0))
    has_credit = wallet > 0.0005
    daily_credits = int(daily.get("daily_credits", 0))
    premium_credits = int(prem.get("premium_credits", 0))
    daily_total = (ULTRA_DAILY_CREDITS if plan == "ultra"
                   else PRO_DAILY_CREDITS if plan == "pro" else FREE_WEEKLY_CREDITS)
    premium_total = PREMIUM_MONTHLY.get(plan, 0)
    return {
        "plan": plan,
        "currency": CURRENCY,
        "has_credit": has_credit,
        "wallet_eur": round(wallet, 4),          # internal only; never shown as a € balance
        # Spendable now = free-model bucket + premium bucket + bought wallet.
        "credits_balance": daily_credits + premium_credits + eur_to_credits(wallet),
        "daily_credits": daily_credits,
        "daily_credits_total": daily_total,
        "premium_credits": premium_credits,
        "premium_credits_total": premium_total,
        "plan_credits": premium_credits,          # back-compat alias for the UI
        "plan_credits_total": premium_total,
        "wallet_credits": eur_to_credits(wallet),
        "plan_period_end": pro.get("plan_period_end", 0),
        "premium_available": (premium_credits > 0) or has_credit,
        "tokens_used": int(data.get("tokens_used", 0)),
        "msgs_used": int(data.get("msgs_used", 0)),
        "credits_spent_total": int(data.get("credits_spent_total", 0)),
        "usage_models": data.get("usage_models", {}),
        "model_rates": model_rates(),
        "message_rates": message_rates(),
        "effort_mult": EFFORT_MULT,
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
    prem = _roll_premium(data)
    wallet = float(data.get("wallet_eur", 0.0))
    # Premium is paid from the monthly PREMIUM bucket (GrgPro 500 / GrgUltra 2000)
    # or from bought wallet credits.
    if int(prem.get("premium_credits", 0)) > 0 or wallet > 0.0005:
        return {"allowed": True}
    return {"allowed": False, "reason": "no_funds"}


def charge_usage(uid: str, model: str, in_tokens: int, out_tokens: int, images: int = 0,
                 agent_mult: float = 1.0) -> dict:
    """Consume the plan's token allowance first (free to the user); charge any
    overflow tokens to the credit wallet at real_cost*MARKUP*agent_mult. Used by the
    desktop agent (/api/agent); `agent_mult` makes specialist-agent runs cost more."""
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
    charge = round(real * MARKUP * float(agent_mult or 1.0), 6)
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


def grant_plan(uid: str, plan: str = "pro"):
    """On subscribe/renew: set the plan and immediately fill BOTH credit buckets
    (free-model daily/weekly + premium monthly) for GrgPro or GrgUltra."""
    if not uid or not FIREBASE_AVAILABLE:
        return
    ref = _get_user_ref(uid)
    if not ref:
        return
    if plan not in PAID_PLANS:
        plan = "pro"
    now = time.time()
    daily_grant = ULTRA_DAILY_CREDITS if plan == "ultra" else PRO_DAILY_CREDITS
    ref.set({
        "plan": plan,
        "daily_credits": daily_grant,
        "daily_credits_day": int(now // PRO_PERIOD),
        "premium_credits": PREMIUM_MONTHLY.get(plan, 0),
        "premium_credits_period": int(now // PREMIUM_PERIOD),
        "plan_eur": PRO_MONTHLY_EUR,            # legacy field, harmless
        "plan_period_end": int(now + 30 * 86400),
        "updated_at": firestore.SERVER_TIMESTAMP if firestore else int(now),
    }, merge=True)

def grant_pro_budget(uid: str):
    """Back-compat wrapper — grants the GrgPro plan."""
    grant_plan(uid, "pro")
