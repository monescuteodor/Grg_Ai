"""
lemonsqueezy_handler.py — Lemon Squeezy (Merchant of Record) payments for Grg AI.

Mirrors stripe_handler: hosted checkout for one-time credit top-ups and for
Pro/Ultra subscriptions, plus a signed webhook that credits the SAME pay-as-you-go
wallet / grants the SAME plan buckets as Stripe (billing.credit_topup_once /
billing.grant_plan). Lets us accept card payments WITHOUT our own company — LS is
the merchant of record and handles VAT. Activated by filling the LS_* vars in .env.
"""
import os
import json
import hmac
import hashlib
import httpx
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# ─── CONFIG (from .env) ───
LS_API_KEY        = os.environ.get("LS_API_KEY", "")
LS_STORE_ID       = os.environ.get("LS_STORE_ID", "")
LS_WEBHOOK_SECRET = os.environ.get("LS_WEBHOOK_SECRET", "")
# Variant IDs created in the LS dashboard:
LS_VARIANT_TOPUP        = os.environ.get("LS_VARIANT_TOPUP", "")         # a "custom price" one-time product
LS_VARIANT_PRO          = os.environ.get("LS_VARIANT_PRO", "")           # €5/mo subscription
LS_VARIANT_PRO_YEARLY   = os.environ.get("LS_VARIANT_PRO_YEARLY", "")
LS_VARIANT_ULTRA        = os.environ.get("LS_VARIANT_ULTRA", "")         # €20/mo subscription
LS_VARIANT_ULTRA_YEARLY = os.environ.get("LS_VARIANT_ULTRA_YEARLY", "")
FRONTEND_URL      = os.environ.get("FRONTEND_URL", "https://grg-ai.com")

LS_API = "https://api.lemonsqueezy.com/v1/checkouts"
_HEADERS = {
    "Authorization": f"Bearer {LS_API_KEY}",
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json",
}

TOPUP_MIN_EUR = 1
TOPUP_MAX_EUR = 500


def ls_enabled() -> bool:
    return bool(LS_API_KEY and LS_STORE_ID)


def _variant_for(kind: str, plan: str, interval: str) -> str:
    if kind == "topup":
        return LS_VARIANT_TOPUP
    yearly = (interval == "yearly")
    if plan == "ultra":
        return LS_VARIANT_ULTRA_YEARLY if yearly else LS_VARIANT_ULTRA
    return LS_VARIANT_PRO_YEARLY if yearly else LS_VARIANT_PRO


async def create_ls_checkout(request: Request):
    """POST /api/ls/checkout — returns a Lemon Squeezy hosted checkout URL.
    body: { uid, email, kind: "topup"|"subscription", plan?, interval?, eur? }"""
    if not ls_enabled():
        return JSONResponse({"error": "Lemon Squeezy not configured on server (.env)"}, status_code=503)
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    uid   = body.get("uid")
    email = body.get("email")
    kind  = body.get("kind", "subscription")
    plan  = body.get("plan", "pro")
    interval = body.get("interval", "monthly")
    if plan not in ("pro", "ultra"):
        plan = "pro"
    if not uid:
        return JSONResponse({"error": "uid required"}, status_code=400)

    variant = _variant_for(kind, plan, interval)
    if not variant:
        return JSONResponse({"error": f"variant not configured for {kind}/{plan}/{interval}"}, status_code=400)

    # Custom data comes back verbatim in the webhook (meta.custom_data) — keep values as strings.
    custom = {"firebase_uid": str(uid)}
    attrs = {
        "checkout_data": {"custom": custom},
        "product_options": {"redirect_url": f"{FRONTEND_URL}?pay=success"},
    }
    if email:
        attrs["checkout_data"]["email"] = email

    if kind == "topup":
        try:
            eur = round(float(body.get("eur", 0)), 2)
        except (TypeError, ValueError):
            eur = 0
        if eur < TOPUP_MIN_EUR or eur > TOPUP_MAX_EUR:
            return JSONResponse({"error": f"Amount must be between €{TOPUP_MIN_EUR} and €{TOPUP_MAX_EUR}"}, status_code=400)
        custom["kind"] = "topup"
        custom["eur"] = ("%g" % eur)
        attrs["custom_price"] = int(round(eur * 100))   # cents, store currency
        attrs["product_options"]["redirect_url"] = f"{FRONTEND_URL}?topup=success"
    else:
        custom["plan"] = plan

    payload = {
        "data": {
            "type": "checkouts",
            "attributes": attrs,
            "relationships": {
                "store":   {"data": {"type": "stores",   "id": str(LS_STORE_ID)}},
                "variant": {"data": {"type": "variants", "id": str(variant)}},
            },
        }
    }
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(20.0, connect=10.0)) as client:
            r = await client.post(LS_API, headers=_HEADERS, json=payload)
        if r.status_code not in (200, 201):
            print(f"[LS checkout {r.status_code}] {r.text[:300]}")
            return JSONResponse({"error": f"Lemon Squeezy error {r.status_code}"}, status_code=400)
        url = r.json()["data"]["attributes"]["url"]
        return JSONResponse({"url": url})
    except Exception as e:  # noqa: BLE001
        print(f"[LS checkout ERROR] {e}")
        return JSONResponse({"error": "Could not create checkout"}, status_code=500)


def _verify_signature(body: bytes, signature: str) -> bool:
    if not LS_WEBHOOK_SECRET or not signature:
        return False
    digest = hmac.new(LS_WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
    try:
        return hmac.compare_digest(digest, signature)
    except Exception:  # noqa: BLE001
        return False


async def ls_webhook(request: Request):
    """POST /api/ls/webhook — Lemon Squeezy events (HMAC-SHA256 signed via X-Signature)."""
    body = await request.body()
    sig = request.headers.get("X-Signature", "")
    if not _verify_signature(body, sig):
        raise HTTPException(status_code=400, detail="Invalid signature")

    try:
        event = json.loads(body)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    meta = event.get("meta") or {}
    event_name = meta.get("event_name") or request.headers.get("X-Event-Name", "")
    custom = meta.get("custom_data") or {}
    uid = custom.get("firebase_uid")
    data = event.get("data") or {}
    obj_id = data.get("id")

    try:
        if event_name == "order_created":
            # One-time top-up → credit the pay-as-you-go wallet (idempotent per order id).
            if uid and custom.get("kind") == "topup":
                try:
                    eur = float(custom.get("eur") or 0)
                    from billing import credit_topup_once
                    ok = credit_topup_once(uid, f"ls_{obj_id}", eur)
                    print(f"[LS] Topup €{eur} for {uid} credited={ok}")
                except Exception as e:  # noqa: BLE001
                    print(f"[LS topup credit ERROR] {e}")

        elif event_name in ("subscription_created", "subscription_resumed",
                            "subscription_payment_success", "subscription_updated"):
            if uid:
                plan = custom.get("plan") or "pro"
                if plan not in ("pro", "ultra"):
                    plan = "pro"
                # Only (re)grant on active statuses.
                status = ((data.get("attributes") or {}).get("status")) or "active"
                if status in ("active", "on_trial", "paid") or event_name == "subscription_payment_success":
                    try:
                        from billing import grant_plan
                        grant_plan(uid, plan)
                        from stripe_handler import _set_subscription
                        _set_subscription(uid, "active", plan=plan)
                        print(f"[LS] {plan} active for {uid} ({event_name})")
                    except Exception as e:  # noqa: BLE001
                        print(f"[LS plan grant ERROR] {e}")

        elif event_name in ("subscription_cancelled", "subscription_expired", "subscription_paused"):
            if uid:
                try:
                    from stripe_handler import _set_subscription
                    _set_subscription(uid, "canceled", plan="free")
                    print(f"[LS] subscription ended for {uid} ({event_name})")
                except Exception as e:  # noqa: BLE001
                    print(f"[LS cancel ERROR] {e}")

    except Exception as e:  # noqa: BLE001
        print(f"[LS webhook ERROR] {e}")

    return JSONResponse({"status": "ok"})
