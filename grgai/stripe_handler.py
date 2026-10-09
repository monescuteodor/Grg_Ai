"""
stripe_handler.py — Stripe Subscription Handler for Grg AI
Handles checkout, webhooks, and subscription status.
"""

import os
import json
import time
import stripe
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# ─── CONFIG ─── (secrets read from .env; literals kept only as test-mode fallback)
STRIPE_SECRET_KEY      = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET  = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_ID        = os.environ.get("STRIPE_PRICE_ID", "")
STRIPE_PRICE_ID_YEARLY = os.environ.get("STRIPE_PRICE_ID_YEARLY", "")
# GrgUltra (€20/mo, €200/yr) — set in .env; the yearly one must be a price with a YEARLY interval.
STRIPE_PRICE_ID_ULTRA        = os.environ.get("STRIPE_PRICE_ID_ULTRA", "")
STRIPE_PRICE_ID_ULTRA_YEARLY = os.environ.get("STRIPE_PRICE_ID_ULTRA_YEARLY", "")
FRONTEND_URL           = os.environ.get("FRONTEND_URL", "https://grg-ai.com")

def _price_for(plan: str, interval: str) -> str:
    """Pick the Stripe price for a plan (pro/ultra) + interval (monthly/yearly)."""
    yearly = (interval == "yearly")
    if plan == "ultra":
        return STRIPE_PRICE_ID_ULTRA_YEARLY if yearly else STRIPE_PRICE_ID_ULTRA
    return STRIPE_PRICE_ID_YEARLY if yearly else STRIPE_PRICE_ID

stripe.api_key = STRIPE_SECRET_KEY

# ─── FIREBASE ADMIN (pentru a salva subscription în Firestore) ───
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-service-account.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    FIREBASE_AVAILABLE = True
except Exception as e:
    print(f"[Stripe] Firebase Admin not available: {e}")
    FIREBASE_AVAILABLE = False
    db = None


# ─── HELPERS ───

def _get_user_ref(uid: str):
    if not FIREBASE_AVAILABLE or not db:
        return None
    return db.collection("users").document(uid)


def _set_subscription(uid: str, status: str, stripe_customer_id: str = None,
                       stripe_subscription_id: str = None, plan: str = "free"):
    ref = _get_user_ref(uid)
    if not ref:
        return
    data = {
        "plan": plan,
        "subscription_status": status,
        "updated_at": firestore.SERVER_TIMESTAMP,
    }
    if stripe_customer_id:
        data["stripe_customer_id"] = stripe_customer_id
    if stripe_subscription_id:
        data["stripe_subscription_id"] = stripe_subscription_id
    ref.set(data, merge=True)


# ─── RATE LIMITING (50 msg/zi pentru Free) ───

DAILY_LIMIT_FREE = 50

def check_rate_limit(uid: str) -> dict:
    """
    Verifică dacă userul a depășit limita zilnică.
    Returnează: { allowed: bool, used: int, limit: int, reset_at: int }
    """
    if not FIREBASE_AVAILABLE or not db:
        return {"allowed": True, "used": 0, "limit": DAILY_LIMIT_FREE, "reset_at": 0}

    ref = _get_user_ref(uid)
    doc = ref.get()
    data = doc.to_dict() if doc.exists else {}

    plan = data.get("plan", "free")
    if plan == "pro":
        return {"allowed": True, "used": 0, "limit": -1, "reset_at": 0, "plan": "pro"}

    now = time.time()
    first_msg_at = data.get("daily_first_msg_at", 0)
    daily_count  = data.get("daily_msg_count", 0)

    # Reset dacă au trecut 24h de la primul mesaj
    if now - first_msg_at > 86400:
        first_msg_at = 0
        daily_count  = 0

    allowed = daily_count < DAILY_LIMIT_FREE
    reset_at = int(first_msg_at + 86400) if first_msg_at else 0

    return {
        "allowed": allowed,
        "used": daily_count,
        "limit": DAILY_LIMIT_FREE,
        "reset_at": reset_at,
        "plan": "free"
    }


def increment_message_count(uid: str):
    """Incrementează contorul zilnic de mesaje."""
    if not FIREBASE_AVAILABLE or not db:
        return
    ref = _get_user_ref(uid)
    doc = ref.get()
    data = doc.to_dict() if doc.exists else {}

    now = time.time()
    first_msg_at = data.get("daily_first_msg_at", 0)
    daily_count  = data.get("daily_msg_count", 0)

    # Reset dacă au trecut 24h
    if now - first_msg_at > 86400:
        first_msg_at = now
        daily_count  = 0

    if first_msg_at == 0:
        first_msg_at = now

    ref.set({
        "daily_msg_count":   daily_count + 1,
        "daily_first_msg_at": first_msg_at,
    }, merge=True)


# ─── ROUTES ───

async def create_checkout_session(request: Request):
    """POST /api/create-checkout — creează Stripe Checkout session."""
    body = await request.json()
    uid      = body.get("uid")
    email    = body.get("email")
    interval = body.get("interval", "monthly")  # "monthly" or "yearly"
    plan     = body.get("plan", "pro")           # "pro" or "ultra"
    if plan not in ("pro", "ultra"):
        plan = "pro"

    if not uid or not email:
        raise HTTPException(status_code=400, detail="uid and email required")

    price_id = _price_for(plan, interval)
    if not price_id:
        raise HTTPException(status_code=400, detail=f"{plan} {interval} price not configured")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            customer_email=email,
            metadata={"firebase_uid": uid, "plan": plan},
            subscription_data={"metadata": {"firebase_uid": uid, "plan": plan}},
            success_url=f"{FRONTEND_URL}?upgrade=success",
            cancel_url=f"{FRONTEND_URL}?upgrade=cancelled",
        )
        return JSONResponse({"url": session.url})
    except stripe.error.StripeError as e:
        print(f"[Stripe ERROR] {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[Checkout ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))


TOPUP_MIN_EUR = 1
TOPUP_MAX_EUR = 500

async def create_topup_session(request: Request):
    """POST /api/create-topup — one-time Stripe Checkout that credits the wallet (pay-as-you-go).
    Accepts a preset or a custom amount between TOPUP_MIN_EUR and TOPUP_MAX_EUR."""
    body = await request.json()
    uid    = body.get("uid")
    email  = body.get("email")
    try:
        eur = round(float(body.get("eur", 0)), 2)
    except (TypeError, ValueError):
        eur = 0
    if not uid or not email:
        raise HTTPException(status_code=400, detail="uid and email required")
    if eur < TOPUP_MIN_EUR or eur > TOPUP_MAX_EUR:
        raise HTTPException(status_code=400, detail=f"Amount must be between €{TOPUP_MIN_EUR} and €{TOPUP_MAX_EUR}")

    amt_label = ("%g" % eur)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "unit_amount": int(round(eur * 100)),
                    "product_data": {"name": f"Grg AI credit — €{amt_label}"},
                },
                "quantity": 1,
            }],
            customer_email=email,
            metadata={"firebase_uid": uid, "kind": "topup", "eur": amt_label},
            success_url=f"{FRONTEND_URL}?topup=success&session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}?topup=cancelled",
        )
        return JSONResponse({"url": session.url})
    except stripe.error.StripeError as e:
        print(f"[Stripe topup ERROR] {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[Topup ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def confirm_topup(request: Request):
    """POST /api/topup-confirm — verify a completed Checkout session and credit the wallet.
    Reliable path that doesn't depend on the webhook; idempotent per session."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    session_id = body.get("session_id")
    if not session_id:
        return JSONResponse({"error": "session_id required"}, status_code=400)
    try:
        s = stripe.checkout.Session.retrieve(session_id)
        meta = s["metadata"] or {}
        uid = meta["firebase_uid"] if "firebase_uid" in meta else None
        kind = meta["kind"] if "kind" in meta else None
        eur = float(meta["eur"]) if "eur" in meta else 0
        paid = s["payment_status"] == "paid"
        if kind == "topup" and paid and uid and eur > 0:
            from billing import credit_topup_once
            credited = credit_topup_once(uid, session_id, eur)
            return JSONResponse({"ok": True, "credited": credited, "eur": eur})
        return JSONResponse({"ok": False, "paid": paid})
    except stripe.error.StripeError as e:
        return JSONResponse({"error": str(e)[:200]}, status_code=400)
    except Exception as e:  # noqa: BLE001
        print(f"[Topup confirm ERROR] {e}")
        return JSONResponse({"error": "Could not confirm the payment."}, status_code=500)


async def create_portal_session(request: Request):
    """POST /api/create-portal — deschide Stripe Customer Portal pentru manage/cancel."""
    try:
        body = await request.json()
        uid = body.get("uid")
        if not uid:
            raise HTTPException(status_code=400, detail="uid required")

        # Găsim customer_id din Firestore
        ref = _get_user_ref(uid)
        if not ref:
            raise HTTPException(status_code=400, detail="Firebase not available")

        doc = ref.get()
        data = doc.to_dict() if doc.exists else {}
        customer_id = data.get("stripe_customer_id")

        if not customer_id:
            raise HTTPException(status_code=400, detail="No subscription found")

        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=FRONTEND_URL,
        )
        return JSONResponse({"url": session.url})
    except stripe.error.StripeError as e:
        print(f"[Portal ERROR] {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        print(f"[Portal ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def stripe_webhook(request: Request):
    """POST /api/webhook — ascultă events Stripe."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        event_type = event["type"]
        data = event["data"]["object"]

        def get_field(obj, field, default=None):
            try:
                val = obj[field]
                return val if val is not None else default
            except (KeyError, TypeError):
                return default

        def get_metadata_uid(obj):
            try:
                meta = obj["metadata"]
                return meta["firebase_uid"] if meta else None
            except (KeyError, TypeError):
                return None

        def meta_field(obj, key):
            # metadata is a StripeObject, not a dict — read via indexing, not .get()
            try:
                m = obj["metadata"]
                return m[key] if (m and key in m) else None
            except (KeyError, TypeError):
                return None

        if event_type == "checkout.session.completed":
            uid = get_metadata_uid(data)
            kind = meta_field(data, "kind")
            # One-time top-up → credit the pay-as-you-go wallet (idempotent per session).
            if uid and kind == "topup":
                try:
                    from billing import credit_topup_once
                    eur = float(meta_field(data, "eur") or 0)
                    session_id = get_field(data, "id")
                    ok = credit_topup_once(uid, session_id, eur)
                    print(f"[Stripe] Topup €{eur} for {uid} credited={ok}")
                except Exception as e:  # noqa: BLE001
                    print(f"[Stripe topup credit ERROR] {e}")
            else:
                customer_id = get_field(data, "customer")
                subscription_id = get_field(data, "subscription")
                plan = meta_field(data, "plan") or "pro"
                if plan not in ("pro", "ultra"):
                    plan = "pro"
                if uid:
                    _set_subscription(uid, "active", customer_id, subscription_id, plan=plan)
                    try:
                        from billing import grant_plan
                        grant_plan(uid, plan)
                    except Exception as e:  # noqa: BLE001
                        print(f"[Stripe plan budget ERROR] {e}")
                    print(f"[Stripe] {plan} activated for {uid}")

        elif event_type == "invoice.paid":
            subscription_id = get_field(data, "subscription")
            if subscription_id:
                sub = stripe.Subscription.retrieve(subscription_id)
                uid = get_metadata_uid(sub)
                plan = meta_field(sub, "plan") or "pro"
                if plan not in ("pro", "ultra"):
                    plan = "pro"
                if uid:
                    _set_subscription(uid, "active", plan=plan)
                    try:
                        from billing import grant_plan
                        grant_plan(uid, plan)  # refill both buckets on renewal
                    except Exception as e:  # noqa: BLE001
                        print(f"[Stripe plan renew ERROR] {e}")

        elif event_type == "invoice.payment_failed":
            subscription_id = get_field(data, "subscription")
            if subscription_id:
                sub = stripe.Subscription.retrieve(subscription_id)
                uid = get_metadata_uid(sub)
                if uid:
                    _set_subscription(uid, "past_due", plan="free")
                    print(f"[Stripe] Payment failed for {uid}")

        elif event_type in ("customer.subscription.deleted", "customer.subscription.canceled"):
            uid = get_metadata_uid(data)
            if uid:
                _set_subscription(uid, "canceled", plan="free")
                print(f"[Stripe] Canceled for {uid}")

    except Exception as e:
        print(f"[Webhook ERROR] {e}")

    return JSONResponse({"status": "ok"})


async def get_subscription_status(request: Request):
    """GET /api/subscription?uid=... — returnează planul și limita userului."""
    uid = request.query_params.get("uid")
    if not uid:
        raise HTTPException(status_code=400, detail="uid required")

    rate = check_rate_limit(uid)
    return JSONResponse(rate)


async def record_message(request: Request):
    """POST /api/record-message — înregistrează un mesaj trimis."""
    try:
        body = await request.json()
        uid = body.get("uid")
        if uid:
            limit_check = check_rate_limit(uid)
            if not limit_check["allowed"]:
                return JSONResponse({"error": "limit_exceeded", "reset_at": limit_check["reset_at"]}, status_code=429)
            increment_message_count(uid)
        return JSONResponse({"ok": True})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
