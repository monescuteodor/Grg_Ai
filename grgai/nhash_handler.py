"""
nhash_handler.py — Pay for Grg Pro with nHash (CoreHash).

Receive-only, on-chain payment verification. The ARM Pi can't run the AES-NI node, so this polls
the nHash explorer on the x86 node (192.168.50.220) to confirm payments. Each order is assigned a
unique EXACT amount to one merchant address; a confirmed transaction of that exact amount, newer
than the order, activates Grg Pro through the same Firestore write Stripe uses. No wallet keys and
no secrets live here — it only watches a public address.

Config below is safe to edit (merchant address, prices). Restart the service after changing it:
    sudo systemctl restart grgai.service
"""

import time
import json
import secrets
import urllib.request
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# ─── CONFIG (safe to edit) ─────────────────────────────────────────────────
MERCHANT_ADDRESS = "a3cb24487a4f6728fb64d05ef813dcf00931c0238352225356db859b34f344a7"
EXPLORER   = "http://192.168.50.220:8080"     # nHash explorer/API (the x86 node)
POOL_ADDR  = "192.168.50.220:9350"            # where friends point nhash-miner to earn nHash
COIN       = 100_000_000                       # base units in 1 nHash
PRICE_NHASH = {                                # price per interval, in whole nHash
    "monthly": 150,
    "yearly":  1500,
}
ORDER_TTL  = 3600      # seconds an order stays payable
CONF_SLACK = 300       # accept a payment timestamped up to this many seconds before the order
# ───────────────────────────────────────────────────────────────────────────

# Reuse the Firebase app that stripe_handler already initialised.
try:
    import firebase_admin  # noqa: F401
    from firebase_admin import firestore
    _db = firestore.client()
except Exception as e:  # pragma: no cover
    print(f"[nHash] Firebase not available: {e}")
    _db = None


def _orders():
    return _db.collection("nhash_orders") if _db else None


def _activate_pro(uid: str):
    """Grant Grg Pro — mirrors stripe_handler._set_subscription(active, pro)."""
    if not _db:
        return
    _db.collection("users").document(uid).set({
        "plan": "pro",
        "subscription_status": "active",
        "updated_at": firestore.SERVER_TIMESTAMP,
        "pro_via": "nhash",
    }, merge=True)


def _get_json(url: str, timeout: int = 8):
    req = urllib.request.Request(url, headers={"User-Agent": "grgai-nhash"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


async def nhash_info(request: Request):
    """GET /api/nhash/info — live network stats (proxied from the LAN explorer, which browsers
    can't reach directly) plus the mining pool address and prices, for the nHash section."""
    chain = {}
    try:
        chain = _get_json(f"{EXPLORER}/api/info")
    except Exception as e:
        print(f"[nHash] info proxy failed: {e}")
    return JSONResponse({
        "chain": chain,
        "pool": POOL_ADDR,
        "explorer": EXPLORER,
        "coin": COIN,
        "price": dict(PRICE_NHASH),
    })


def _amount_in_use(amount: int) -> bool:
    """True if a still-pending order already claims this exact amount (avoid collisions)."""
    col = _orders()
    if not col:
        return False
    now = int(time.time())
    try:
        for d in col.stream():
            o = d.to_dict()
            if o.get("status") == "pending" and int(o.get("amount", -1)) == amount \
               and now <= int(o.get("expires_at", 0)):
                return True
    except Exception as e:
        print(f"[nHash] amount-in-use scan failed: {e}")
    return False


async def create_nhash_order(request: Request):
    """POST /api/nhash/create-order  {uid, interval} -> {order_id, address, amount, ...}."""
    body = await request.json()
    uid = body.get("uid")
    interval = body.get("interval", "monthly")
    if not uid:
        raise HTTPException(status_code=400, detail="uid required")
    if interval not in PRICE_NHASH:
        interval = "monthly"
    if not _orders():
        return JSONResponse({"error": "payments unavailable"}, status_code=503)

    base = PRICE_NHASH[interval] * COIN
    # Unique exact amount = base + a small sub-unit nonce (0.00000001 .. 0.00100000 nHash),
    # so concurrent orders to the same address never collide and each payment maps to one order.
    amount = base
    for _ in range(60):
        nonce = secrets.randbelow(100_000) + 1
        if not _amount_in_use(base + nonce):
            amount = base + nonce
            break

    now = int(time.time())
    order_id = secrets.token_hex(12)
    _orders().document(order_id).set({
        "uid": uid,
        "interval": interval,
        "amount": amount,
        "address": MERCHANT_ADDRESS,
        "status": "pending",
        "created_at": now,
        "expires_at": now + ORDER_TTL,
        "txid": None,
    })
    return JSONResponse({
        "order_id": order_id,
        "address": MERCHANT_ADDRESS,
        "amount": amount,
        "amount_nhash": amount / COIN,
        "interval": interval,
        "expires_at": now + ORDER_TTL,
    })


def _find_payment(order: dict):
    """Return the txid of a confirmed payment of the exact amount to the merchant, newer than
    the order — or None. Uses the explorer's per-address history (confirmed txs only)."""
    try:
        data = _get_json(f"{EXPLORER}/api/addrtxs?a={order['address']}")
    except Exception as e:
        print(f"[nHash] explorer unreachable: {e}")
        return None
    want = int(order["amount"])
    floor = int(order["created_at"]) - CONF_SLACK
    for tx in data.get("txs", []):
        if int(tx.get("received", 0)) != want:
            continue
        if int(tx.get("time", 0)) < floor:
            continue
        return tx.get("txid")
    return None


async def check_nhash_order(request: Request):
    """POST /api/nhash/check-order {order_id} -> {status: pending|paid|expired|unknown}."""
    order_id = request.query_params.get("order_id")
    if not order_id:
        try:
            body = await request.json()
        except Exception:
            body = {}
        order_id = body.get("order_id")
    if not order_id:
        raise HTTPException(status_code=400, detail="order_id required")

    col = _orders()
    if not col:
        return JSONResponse({"status": "error", "detail": "payments unavailable"}, status_code=503)
    ref = col.document(order_id)
    snap = ref.get()
    if not snap.exists:
        return JSONResponse({"status": "unknown"})
    order = snap.to_dict()

    if order.get("status") == "paid":
        return JSONResponse({"status": "paid", "txid": order.get("txid")})
    if int(time.time()) > int(order.get("expires_at", 0)):
        ref.set({"status": "expired"}, merge=True)
        return JSONResponse({"status": "expired"})

    txid = _find_payment(order)
    if txid:
        ref.set({"status": "paid", "txid": txid}, merge=True)
        _activate_pro(order["uid"])
        print(f"[nHash] order {order_id} PAID by {order['uid']} — tx {txid}")
        return JSONResponse({"status": "paid", "txid": txid})
    return JSONResponse({"status": "pending"})
