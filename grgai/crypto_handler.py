"""
crypto_handler.py — Solana USDC payments (Solana Pay) for Grg AI.

Non-custodial, no processor, no KYC: customers pay USDC on Solana straight to the
owner's wallet (SOL_ADDRESS). Each order gets a unique Solana Pay `reference`
pubkey, so the exact payment is found on-chain (getSignaturesForAddress) and
credits the SAME wallet / plan buckets as Stripe (billing.credit_topup_once /
grant_plan). Pending orders live in Firestore. Activated by SOL_ADDRESS in .env.
"""
import os
import time
import uuid
import secrets
import httpx
from urllib.parse import quote
from fastapi import Request
from fastapi.responses import JSONResponse

SOL_ADDRESS = os.environ.get("SOL_ADDRESS", "")
USDC_MINT   = os.environ.get("USDC_MINT", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")  # USDC on Solana
SOL_RPC     = os.environ.get("SOL_RPC", "https://api.mainnet-beta.solana.com")
HELIUS_API_KEY = os.environ.get("HELIUS_API_KEY", "")
if HELIUS_API_KEY:
    SOL_RPC = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://grg-ai.com")

TOPUP_MIN_EUR = 1
TOPUP_MAX_EUR = 500
PLAN_EUR = {"pro": 5.0, "ultra": 20.0}
ORDER_TTL = 1800  # 30 min window to pay

try:
    from stripe_handler import db as _db, FIREBASE_AVAILABLE as _FB
except Exception as _e:  # noqa: BLE001
    print(f"[crypto] Firebase not available: {_e}")
    _db, _FB = None, False

# ─── base58 (for the random Solana Pay reference pubkey) ───
_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def _b58encode(b: bytes) -> str:
    n = int.from_bytes(b, "big")
    out = ""
    while n > 0:
        n, r = divmod(n, 58)
        out = _B58[r] + out
    pad = 0
    for x in b:
        if x == 0:
            pad += 1
        else:
            break
    return ("1" * pad) + out


def crypto_enabled() -> bool:
    return bool(SOL_ADDRESS and _FB and _db)


def _order_doc(order_id: str):
    return _db.collection("crypto_orders").document(order_id) if (_FB and _db) else None


async def _eur_to_usdc(eur: float) -> float:
    """USDC (USD-pegged) needed for this many EUR, +1% buffer so we never under-collect."""
    rate_usdc_per_eur = 1.09  # fallback (~1 EUR = 1.09 USD)
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(6.0, connect=4.0)) as c:
            r = await c.get("https://api.coingecko.com/api/v3/simple/price",
                            params={"ids": "usd-coin", "vs_currencies": "eur"})
            usdc_in_eur = float(r.json()["usd-coin"]["eur"])
            if usdc_in_eur > 0:
                rate_usdc_per_eur = 1.0 / usdc_in_eur
    except Exception:  # noqa: BLE001
        pass
    return eur * rate_usdc_per_eur * 1.01


async def create_crypto_checkout(request: Request):
    """POST /api/crypto/checkout — body {uid, kind:"topup"|"subscription", plan?, eur?} → Solana Pay order."""
    if not crypto_enabled():
        return JSONResponse({"error": "Crypto not configured on server"}, status_code=503)
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    uid  = body.get("uid")
    kind = body.get("kind", "topup")
    plan = body.get("plan", "pro")
    if plan not in ("pro", "ultra"):
        plan = "pro"
    if not uid:
        return JSONResponse({"error": "uid required"}, status_code=400)

    if kind == "topup":
        try:
            eur = round(float(body.get("eur", 0)), 2)
        except (TypeError, ValueError):
            eur = 0
        if eur < TOPUP_MIN_EUR or eur > TOPUP_MAX_EUR:
            return JSONResponse({"error": f"Amount must be between €{TOPUP_MIN_EUR} and €{TOPUP_MAX_EUR}"}, status_code=400)
    else:
        eur = PLAN_EUR.get(plan, 5.0)

    usdc = round(await _eur_to_usdc(eur), 6)
    reference = _b58encode(secrets.token_bytes(32))
    order_id = uuid.uuid4().hex

    _order_doc(order_id).set({
        "uid": uid, "kind": kind, "plan": plan, "eur": eur,
        "usdc": usdc, "reference": reference, "status": "pending",
        "created_at": time.time(),
    })

    msg = f"Grg AI — credit €{('%g' % eur)}" if kind == "topup" else f"Grg {plan.capitalize()} (30 zile)"
    pay_url = (f"solana:{SOL_ADDRESS}?amount={usdc}&spl-token={USDC_MINT}"
               f"&reference={reference}&label={quote('Grg AI')}&message={quote(msg)}")
    return JSONResponse({
        "order_id": order_id, "address": SOL_ADDRESS, "amount_usdc": usdc,
        "reference": reference, "solana_url": pay_url, "eur": eur,
        "kind": kind, "plan": plan, "network": "Solana", "token": "USDC",
    })


async def _rpc(method: str, params: list):
    async with httpx.AsyncClient(timeout=httpx.Timeout(12.0, connect=6.0)) as c:
        r = await c.post(SOL_RPC, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
        return r.json()


def _tx_pays_us(tx: dict, want_usdc: float) -> bool:
    """Confirm the tx actually moved >= want_usdc USDC into our wallet (not just carried the reference)."""
    if not tx:
        return False
    try:
        meta = tx.get("meta") or {}
        pre = {b["accountIndex"]: b for b in (meta.get("preTokenBalances") or [])}
        for b in (meta.get("postTokenBalances") or []):
            if b.get("mint") != USDC_MINT or b.get("owner") != SOL_ADDRESS:
                continue
            post_amt = float((b.get("uiTokenAmount") or {}).get("uiAmount") or 0)
            pre_amt = float(((pre.get(b["accountIndex"]) or {}).get("uiTokenAmount") or {}).get("uiAmount") or 0)
            if post_amt - pre_amt >= want_usdc - 1e-6:
                return True
    except Exception:  # noqa: BLE001
        pass
    return False


async def _verify_payment(reference: str, want_usdc: float) -> bool:
    try:
        res = await _rpc("getSignaturesForAddress", [reference, {"limit": 10}])
        for s in (res.get("result") or []):
            if s.get("err") is not None:
                continue
            sig = s.get("signature")
            tx = await _rpc("getTransaction", [sig, {"encoding": "jsonParsed",
                            "maxSupportedTransactionVersion": 0, "commitment": "confirmed"}])
            if _tx_pays_us(tx.get("result"), want_usdc):
                return True
        return False
    except Exception as e:  # noqa: BLE001
        print(f"[crypto verify ERROR] {e}")
        return False


async def check_crypto_status(request: Request):
    """POST /api/crypto/status — body {order_id} → {status: pending|paid|expired|unknown}. Credits on first confirm."""
    if not (_FB and _db):
        return JSONResponse({"status": "error"}, status_code=503)
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    order_id = body.get("order_id")
    if not order_id:
        return JSONResponse({"error": "order_id required"}, status_code=400)
    doc_ref = _order_doc(order_id)
    doc = doc_ref.get()
    if not doc.exists:
        return JSONResponse({"status": "unknown"})
    o = doc.to_dict()
    if o.get("status") == "paid":
        return JSONResponse({"status": "paid"})
    if time.time() - float(o.get("created_at", 0)) > ORDER_TTL:
        return JSONResponse({"status": "expired"})

    if await _verify_payment(o["reference"], float(o["usdc"])):
        uid, kind, plan, eur = o["uid"], o.get("kind"), o.get("plan", "pro"), float(o["eur"])
        try:
            if kind == "topup":
                from billing import credit_topup_once
                credit_topup_once(uid, f"sol_{order_id}", eur)
            else:
                from billing import grant_plan
                grant_plan(uid, plan)
                from stripe_handler import _set_subscription
                _set_subscription(uid, "active", plan=plan)
            print(f"[crypto] order {order_id} PAID ({kind} {plan} €{eur}) for {uid}")
        except Exception as e:  # noqa: BLE001
            print(f"[crypto credit ERROR] {e}")
        doc_ref.set({"status": "paid", "paid_at": time.time()}, merge=True)
        return JSONResponse({"status": "paid"})
    return JSONResponse({"status": "pending"})
