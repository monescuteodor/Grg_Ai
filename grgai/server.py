"""
server.py — Grg AI Web Server (Pi version)
FastAPI + Stripe + Firebase + nHash + streaming LLM proxy (Groq / OpenRouter)
"""

import os
import re
import time
import json
import asyncio
import secrets
import collections
from html import unescape as _html_unescape
from urllib.parse import unquote as _url_unquote
from io import BytesIO
from urllib.parse import quote
from pathlib import Path
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse, Response, RedirectResponse
from fastapi.staticfiles import StaticFiles

try:
    from PIL import Image as _PILImage
    _PIL_OK = True
except Exception:  # noqa: BLE001
    _PIL_OK = False


# ─── ENV LOADING (no external deps) ───
def _load_env():
    """Load KEY=VALUE lines from a local .env file into os.environ."""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        val = val.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), val)


_load_env()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# provider -> (upstream url, api key, extra headers)
_PROVIDERS = {
    "groq": (
        "https://api.groq.com/openai/v1/chat/completions",
        lambda: GROQ_API_KEY,
        {},
    ),
    "openrouter": (
        "https://openrouter.ai/api/v1/chat/completions",
        lambda: OPENROUTER_API_KEY,
        {"HTTP-Referer": "https://grg-ai.com", "X-Title": "Grg AI"},
    ),
}

SYSTEM_PROMPT = (
    "You are Grg AI, an expert programming assistant created by Monescu Teodor. "
    "You are especially strong at writing, explaining, debugging and reviewing code. "
    "Give correct, production-quality answers. Prefer fenced code blocks with a language tag. "
    "When you produce a runnable web snippet (HTML/CSS/JS), make it self-contained so it can be previewed directly. "
    "IMAGES: whenever a website/app/page you generate needs a photo, use a REAL photo via "
    "'https://grg-ai.com/img?q=<comma,separated,keywords>' (optionally add &w=1600&h=900 for size, and &i=2 / &i=3 to pick a different photo when you need several distinct ones). "
    "For example a hero for a Paris page: <img src=\"https://grg-ai.com/img?q=paris,eiffel+tower,city&w=1600&h=900\">. "
    "NEVER use placeholder services or fake/broken image URLs — always use the /img endpoint so real, relevant photos show up. "
    "Explain briefly, avoid filler, and when unsure say so instead of inventing facts."
)

# Only these models may be proxied (protects the API keys from being used for
# arbitrary/expensive models by anyone hitting /api/chat directly).
ALLOWED_MODELS = {
    # Groq (free)
    "openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b", "groq/compound",
    # OpenAI
    "openai/gpt-5.6", "openai/gpt-5.5", "openai/gpt-5.2", "openai/gpt-5.1-codex", "openai/gpt-4o",
    # Anthropic (Claude)
    "anthropic/claude-sonnet-5", "anthropic/claude-opus-4.8", "anthropic/claude-opus-4.6",
    "anthropic/claude-fable", "anthropic/claude-haiku-4.5",
    # Meta
    "meta-llama/llama-4-maverick", "meta-llama/llama-4-scout",
    # Qwen
    "qwen/qwen3-coder", "qwen/qwen3-max", "qwen/qwen3-vl", "qwen/qwen3.8-27b:free",
    # DeepSeek
    "deepseek/deepseek-v4", "deepseek/deepseek-v4-flash-0731:free", "deepseek/deepseek-v4-pro", "deepseek/deepseek-r1",
    # Google
    "google/gemini-3.1-pro-preview", "google/gemini-2.5-pro", "google/gemini-3-flash-preview", "google/gemma-4-31b-it:free",
    # Nvidia
    "nvidia/nemotron-3-ultra-550b-a55b:free", "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3.5-lightning:free",
    # xAI
    "x-ai/grok-4", "x-ai/grok-4.1", "x-ai/grok-4.6",
    # Moonshot
    "moonshotai/kimi-k2.7-code", "moonshotai/kimi-k2.6", "moonshotai/kimi-k3",
    # Mistral
    "mistralai/codestral-2508", "mistralai/mistral-large-2", "mistralai/mistral-large",
    # GLM (z-ai)
    "z-ai/glm-5.3", "z-ai/glm-5.2:free",
    # Code / other free
    "poolside/laguna-s-2.1:free", "inclusionai/ling-3.0-flash-vl:free",
    "google/gemini-3.1-pro-preview", "google/gemini-3-flash-preview",
    "qwen/qwen3-coder", "deepseek/deepseek-r1", "openai/gpt-5.1-codex", "openai/gpt-5.2",
}

from stripe_handler import (
    create_checkout_session,
    stripe_webhook,
    get_subscription_status,
    record_message,
    create_portal_session,
    create_topup_session,
    confirm_topup,
)
try:
    from billing import get_account, premium_allowed, charge_usage
    _BILLING_OK = True
except Exception as _e:  # noqa: BLE001
    print(f"[billing] not available: {_e}")
    _BILLING_OK = False
try:
    import docgen
    _DOCGEN_OK = True
except Exception as _e:  # noqa: BLE001
    print(f"[docgen] not available: {_e}")
    _DOCGEN_OK = False
from nhash_handler import (
    create_nhash_order,
    check_nhash_order,
    nhash_info,
)

app = FastAPI(title="Grg AI")
STATIC_DIR = Path(__file__).parent / "static"

# ─── RATE LIMITING (per-IP sliding window) ───────────────────────────────────
# Protects the scarce free-tier tokens (Groq ~8k TPM) and the Pi itself from a
# single client hammering the expensive endpoints. In-memory is fine: one uvicorn
# process on the Pi. Keyed on the real client IP (Cloudflare → CF-Connecting-IP).
_RL_HITS = collections.defaultdict(collections.deque)  # key -> deque[timestamps]
# path-prefix -> (max_requests, window_seconds)
_RL_RULES = {
    "/api/chat":          (30, 60),
    "/api/agent":         (30, 60),   # also covers /api/agent/stream
    "/api/doc/generate":  (12, 60),
    "/api/image":         (20, 60),
    "/api/images/search": (45, 60),
    "/api/web/search":    (45, 60),
    "/api/share":         (12, 60),
    "/api/publish":       (12, 60),
}
_RL_DAY = (800, 86400)  # per-IP daily cap across chat + agent (abuse ceiling)

def _client_ip(request):
    return (request.headers.get("cf-connecting-ip")
            or (request.headers.get("x-forwarded-for") or "").split(",")[0].strip()
            or (request.client.host if request.client else "?"))

def _rl_hit(key, limit, window, now):
    """Return (allowed, retry_after_seconds). Appends the hit when allowed."""
    dq = _RL_HITS[key]
    cutoff = now - window
    while dq and dq[0] < cutoff:
        dq.popleft()
    if len(dq) >= limit:
        return False, int(window - (now - dq[0])) + 1
    dq.append(now)
    return True, 0

@app.middleware("http")
async def rate_limit(request, call_next):
    path = request.url.path
    for pref, (limit, window) in _RL_RULES.items():
        if path.startswith(pref):
            ip = _client_ip(request)
            now = time.time()
            ok, retry = _rl_hit(f"{ip}|{pref}", limit, window, now)
            if ok and pref in ("/api/chat", "/api/agent"):
                ok, retry = _rl_hit(f"{ip}|day", _RL_DAY[0], _RL_DAY[1], now)
            if not ok:
                return JSONResponse(
                    {"error": f"You're going a bit fast — please wait {retry}s and try again."},
                    status_code=429, headers={"Retry-After": str(retry)})
            # Opportunistic cleanup so the table can't grow unbounded.
            if len(_RL_HITS) > 6000:
                for k in [k for k, v in list(_RL_HITS.items()) if not v]:
                    _RL_HITS.pop(k, None)
            break
    return await call_next(request)

@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/privacy")
async def privacy():
    return FileResponse(STATIC_DIR / "privacy.html")

@app.get("/terms")
async def terms():
    return FileResponse(STATIC_DIR / "terms.html")

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/health")
async def health():
    return {"status": "ok"}

# ─── SHARE A CONVERSATION (public read-only link) ────────────────────────────
_SHARE_DIR = Path(__file__).parent / "shares"
try:
    _SHARE_DIR.mkdir(exist_ok=True)
except Exception as _e:  # noqa: BLE001
    print(f"[share] cannot create dir: {_e}")
_SHARE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{6,24}$")

@app.post("/api/share")
async def share_create(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    turns = body.get("turns") or []
    if not isinstance(turns, list) or not turns:
        return JSONResponse({"error": "Nothing to share"}, status_code=400)
    clean = []
    for t in turns[:300]:
        if not isinstance(t, dict):
            continue
        clean.append({
            "user": str(t.get("user") or "")[:20000],
            "assistant": str(t.get("assistant") or "")[:80000],
            "image": (str(t.get("image") or "")[:4000] if t.get("image") else ""),
        })
    if not clean:
        return JSONResponse({"error": "Nothing to share"}, status_code=400)
    doc = {
        "title": str(body.get("title") or "Shared chat")[:200],
        "model": str(body.get("model") or "")[:80],
        "ts": int(time.time()),
        "turns": clean,
    }
    raw = json.dumps(doc, ensure_ascii=False)
    if len(raw.encode("utf-8")) > 1_400_000:
        return JSONResponse({"error": "This conversation is too large to share."}, status_code=413)
    sid = secrets.token_urlsafe(6)
    for _ in range(5):
        if not (_SHARE_DIR / f"{sid}.json").exists():
            break
        sid = secrets.token_urlsafe(6)
    try:
        (_SHARE_DIR / f"{sid}.json").write_text(raw, encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"error": f"Could not save share: {e}"}, status_code=500)
    return {"id": sid, "url": f"/s/{sid}"}

@app.get("/api/share/{share_id}")
async def share_get(share_id: str):
    if not _SHARE_ID_RE.match(share_id or ""):
        return JSONResponse({"error": "Not found"}, status_code=404)
    f = _SHARE_DIR / f"{share_id}.json"
    if not f.exists():
        return JSONResponse({"error": "Not found"}, status_code=404)
    try:
        return JSONResponse(json.loads(f.read_text(encoding="utf-8")))
    except Exception:
        return JSONResponse({"error": "This shared chat is unavailable."}, status_code=500)

@app.get("/s/{share_id}")
async def share_view(share_id: str):
    # Read-only viewer page; it fetches /api/share/{id} client-side.
    return FileResponse(STATIC_DIR / "share.html")

# ─── PUBLISH A GENERATED PAGE TO A REAL PUBLIC URL ───────────────────────────
# Hosts the HTML a user generated (from the preview) at /p/<id>. Served with a
# `Content-Security-Policy: sandbox` header so the page runs in an OPAQUE origin:
# it can still run its own JS and load CDNs (React/Tailwind), but it CANNOT read
# grg-ai.com cookies/localStorage (Firebase tokens) — safe multi-tenant hosting.
_PUB_DIR = Path(__file__).parent / "published"
try:
    _PUB_DIR.mkdir(exist_ok=True)
except Exception as _e:  # noqa: BLE001
    print(f"[publish] cannot create dir: {_e}")

@app.post("/api/publish")
async def publish_create(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    html = str(body.get("html") or "")
    if not html.strip():
        return JSONResponse({"error": "Nothing to publish"}, status_code=400)
    if len(html.encode("utf-8")) > 3_000_000:
        return JSONResponse({"error": "This page is too large to publish (max 3 MB)."}, status_code=413)
    sid = secrets.token_urlsafe(6)
    for _ in range(5):
        if not (_PUB_DIR / f"{sid}.html").exists():
            break
        sid = secrets.token_urlsafe(6)
    try:
        (_PUB_DIR / f"{sid}.html").write_text(html, encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"error": f"Could not publish: {e}"}, status_code=500)
    return {"id": sid, "url": f"/p/{sid}"}

@app.get("/p/{page_id}")
async def publish_view(page_id: str):
    if not _SHARE_ID_RE.match(page_id or ""):
        return JSONResponse({"error": "Not found"}, status_code=404)
    f = _PUB_DIR / f"{page_id}.html"
    if not f.exists():
        return Response("<!doctype html><meta charset=utf-8><title>Not found</title>"
                        "<body style='font-family:system-ui;background:#0e0e16;color:#e7e7ef;"
                        "text-align:center;padding:80px'><h2>This page was not found.</h2>"
                        "<p><a style='color:#8b5cf6' href='/'>Open Grg AI</a></p>",
                        media_type="text/html", status_code=404)
    try:
        html = f.read_text(encoding="utf-8")
    except Exception:
        return JSONResponse({"error": "unavailable"}, status_code=500)
    return Response(html, media_type="text/html", headers={
        # Opaque-origin sandbox: scripts/forms/popups OK, no same-origin access.
        "Content-Security-Policy": "sandbox allow-scripts allow-forms allow-popups allow-modals allow-downloads allow-popups-to-escape-sandbox",
        "X-Robots-Tag": "noindex, nofollow",
    })

# ─── STRIPE & SUBSCRIPTION ───
@app.post("/api/create-checkout")
async def checkout(request: Request):
    return await create_checkout_session(request)

@app.post("/api/webhook")
async def webhook(request: Request):
    return await stripe_webhook(request)

@app.get("/api/subscription")
async def subscription(request: Request):
    return await get_subscription_status(request)

@app.post("/api/record-message")
async def record_msg(request: Request):
    return await record_message(request)

@app.post("/api/create-portal")
async def portal(request: Request):
    return await create_portal_session(request)

@app.post("/api/create-topup")
async def topup(request: Request):
    return await create_topup_session(request)

@app.post("/api/topup-confirm")
async def topup_confirm(request: Request):
    return await confirm_topup(request)

@app.get("/api/account")
async def account(request: Request):
    uid = request.query_params.get("uid")
    if not uid:
        return JSONResponse({"error": "uid required"}, status_code=400)
    defaults = {"plan": "free", "premium_available": False, "has_credit": False,
                "credits_balance": 0, "plan_credits": 0, "plan_credits_total": 500,
                "wallet_credits": 0, "tokens_used": 0, "usage_models": {}, "model_rates": {},
                "credit_eur": 0.01, "currency": "eur",
                "daily_used": 0, "daily_limit": 50, "topup_packs": [5, 10, 20], "markup": 1.34}
    if not _BILLING_OK:
        return JSONResponse(defaults)
    try:
        return JSONResponse(get_account(uid))
    except Exception as e:  # noqa: BLE001
        print(f"[account ERROR] {e}")
        return JSONResponse(defaults)

# ─── nHASH PAYMENTS ───
@app.post("/api/nhash/create-order")
async def nhash_create(request: Request):
    return await create_nhash_order(request)

@app.post("/api/nhash/check-order")
async def nhash_check(request: Request):
    return await check_nhash_order(request)

@app.get("/api/nhash/info")
async def nhash_info_route(request: Request):
    return await nhash_info(request)

# ─── LLM CHAT PROXY (streaming, keys stay server-side) ───
# ─── Web search (DuckDuckGo, no API key / no account) — for live hardware data ───
_DDG_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://duckduckgo.com/",
}

def _ddg_clean(s):
    return _html_unescape(re.sub(r"<[^>]+>", "", s or "")).strip()

def _ddg_deurl(u):
    m = re.search(r"uddg=([^&]+)", u or "")
    if m:
        return _url_unquote(m.group(1))
    return ("https:" + u) if u.startswith("//") else u

async def _web_search(query, n=5):
    """Return [{title,url,snippet}] from DuckDuckGo. No key, no account. Retries on rate-limit."""
    q = (query or "").strip()[:220]
    if not q:
        return []
    async with httpx.AsyncClient(timeout=httpx.Timeout(14.0, connect=8.0), follow_redirects=True) as client:
        for endpoint in ("https://html.duckduckgo.com/html/", "https://lite.duckduckgo.com/lite/"):
            for attempt in range(2):
                try:
                    r = await client.post(endpoint, data={"q": q}, headers=_DDG_HEADERS)
                    hh = r.text
                    if r.status_code != 200:
                        await asyncio.sleep(1.2 * (attempt + 1))
                        continue
                    if "result__a" in hh:
                        titles = re.findall(r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', hh, re.S)
                        snips = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', hh, re.S)
                    else:  # lite endpoint
                        titles = []
                        for m in re.finditer(r'<a\b([^>]*class="result-link"[^>]*)>(.*?)</a>', hh, re.S):
                            hm = re.search(r'href="([^"]+)"', m.group(1))
                            if hm:
                                titles.append((hm.group(1), m.group(2)))
                        snips = re.findall(r'class="result-snippet"[^>]*>(.*?)</td>', hh, re.S)
                    out = []
                    for k, (u, t) in enumerate(titles[:n]):
                        title = _ddg_clean(t)
                        if title:
                            out.append({"title": title, "url": _ddg_deurl(u),
                                        "snippet": _ddg_clean(snips[k]) if k < len(snips) else ""})
                    if out:
                        return out
                    await asyncio.sleep(1.0)
                except Exception:  # noqa: BLE001
                    await asyncio.sleep(1.0)
    return []


# ─── Real-image search (keyless: Openverse + Wikimedia Commons, Picsum fallback) ───
_IMG_HEADERS = {"User-Agent": "GrgAI/1.0 (+https://grg-ai.com; real-image lookup)"}
_IMG_CACHE = {}   # query(lower) -> {"ts": float, "items": [...]}
_IMG_TTL = 3600.0
_IMG_BAD_EXT = (".svg", ".pdf", ".ogg", ".ogv", ".webm", ".gif", ".tif", ".tiff")

async def _image_search(query, n=6):
    """Return [{url,thumb,title,credit,license,source,link}] of REAL photos. No key/account."""
    q = (query or "").strip()[:120]
    if not q:
        return []
    now = time.time()
    c = _IMG_CACHE.get(q.lower())
    if c and (now - c["ts"] < _IMG_TTL) and c["items"]:
        return c["items"][:n]
    items = []
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(12.0, connect=6.0), follow_redirects=True) as client:
            # 1) Openverse — query-based, CC-licensed real photos
            try:
                r = await client.get("https://api.openverse.org/v1/images/",
                                      params={"q": q, "page_size": max(n, 6), "mature": "false"},
                                      headers=_IMG_HEADERS)
                if r.status_code == 200:
                    for x in (r.json().get("results") or []):
                        u = x.get("url") or ""
                        if u.startswith("http") and not u.lower().endswith(_IMG_BAD_EXT):
                            items.append({"url": u, "thumb": x.get("thumbnail") or u,
                                          "title": (x.get("title") or "")[:120], "credit": x.get("creator") or "",
                                          "license": x.get("license") or "", "source": "openverse",
                                          "link": x.get("foreign_landing_url") or u})
            except Exception:  # noqa: BLE001
                pass
            # 2) Wikimedia Commons — great for places/landmarks
            if len(items) < n:
                try:
                    r = await client.get("https://commons.wikimedia.org/w/api.php",
                                          params={"action": "query", "generator": "search", "gsrsearch": q,
                                                  "gsrnamespace": 6, "gsrlimit": max(n, 6), "prop": "imageinfo",
                                                  "iiprop": "url", "iiurlwidth": 1600, "format": "json"},
                                          headers=_IMG_HEADERS)
                    if r.status_code == 200:
                        pages = ((r.json().get("query") or {}).get("pages") or {})
                        for v in pages.values():
                            ii = (v.get("imageinfo") or [{}])[0]
                            u = ii.get("thumburl") or ii.get("url") or ""
                            if u.startswith("http") and not u.lower().endswith(_IMG_BAD_EXT):
                                items.append({"url": u, "thumb": u,
                                              "title": (v.get("title") or "").replace("File:", "")[:120],
                                              "credit": "Wikimedia Commons", "license": "see source",
                                              "source": "wikimedia", "link": u})
                except Exception:  # noqa: BLE001
                    pass
    except Exception:  # noqa: BLE001
        pass
    # de-dup by url, keep order
    seen, uniq = set(), []
    for it in items:
        if it["url"] not in seen:
            seen.add(it["url"]); uniq.append(it)
    if uniq:
        _IMG_CACHE[q.lower()] = {"ts": now, "items": uniq}
    return uniq[:n]


@app.get("/img")
async def img_redirect(q: str = "", w: int = 1600, h: int = 900, i: int = 0):
    """Redirect to a REAL photo for the query — models embed <img src='/img?q=...'>."""
    items = await _image_search(q, 8)
    if items:
        idx = max(0, int(i or 0)) % len(items)
        return RedirectResponse(items[idx]["url"], status_code=302)
    # deterministic real-photo fallback (always works, sized)
    seed = re.sub(r"[^a-z0-9]+", "-", (q or "grg").lower()).strip("-")[:40] or "grg"
    ww = max(64, min(int(w or 1600), 2400)); hh = max(64, min(int(h or 900), 2400))
    return RedirectResponse(f"https://picsum.photos/seed/{seed}/{ww}/{hh}", status_code=302)


@app.get("/api/images/search")
async def api_image_search(q: str = "", n: int = 6):
    """JSON list of real photos (url + attribution) for the query."""
    return {"query": q, "images": await _image_search(q, max(1, min(int(n or 6), 12)))}


@app.get("/api/web/search")
async def api_web_search(q: str = "", n: int = 5):
    """Public web-search endpoint (DuckDuckGo, no key) used by Grg Code's web_search tool."""
    try:
        res = await _web_search(q, max(1, min(int(n or 5), 8)))
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"query": q, "results": [], "error": str(e)})
    return {"query": q, "results": res}


# ─── Live model availability (which AIs actually work right now) ───
_AVAIL_CACHE = {"ts": 0.0, "data": None}

async def _get_availability(force=False):
    """Which providers/models are usable right now (cached ~3 min)."""
    now = time.time()
    if not force and _AVAIL_CACHE["data"] and now - _AVAIL_CACHE["ts"] < 180:
        return _AVAIL_CACHE["data"]
    groq_ids, premium_ok, credit_remaining = [], False, 0.0
    free_remaining, free_limit = None, None
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=6.0)) as client:
            if GROQ_API_KEY:
                try:
                    r = await client.get("https://api.groq.com/openai/v1/models",
                                         headers={"Authorization": f"Bearer {GROQ_API_KEY}"})
                    if r.status_code == 200:
                        groq_ids = [m.get("id") for m in r.json().get("data", []) if m.get("id")]
                except Exception:  # noqa: BLE001
                    pass
            if OPENROUTER_API_KEY:
                try:
                    r = await client.get("https://openrouter.ai/api/v1/credits",
                                         headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"})
                    if r.status_code == 200:
                        d = r.json().get("data", {}) or {}
                        credit_remaining = float(d.get("total_credits", 0)) - float(d.get("total_usage", 0))
                        premium_ok = credit_remaining > 0.001
                except Exception:  # noqa: BLE001
                    pass
                try:
                    r = await client.get("https://openrouter.ai/api/v1/key",
                                         headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"})
                    if r.status_code == 200:
                        fr = (r.json().get("data", {}) or {}).get("free_model_daily_requests") or {}
                        free_remaining, free_limit = fr.get("remaining"), fr.get("limit")
                except Exception:  # noqa: BLE001
                    pass
    except Exception:  # noqa: BLE001
        pass
    data = {"groq": groq_ids, "premium_ok": premium_ok,
            "credit_remaining": round(credit_remaining, 4),
            "free_remaining": free_remaining, "free_limit": free_limit, "ts": int(now)}
    _AVAIL_CACHE["ts"], _AVAIL_CACHE["data"] = now, data
    return data

@app.get("/api/models/status")
async def models_status():
    return JSONResponse(await _get_availability())

@app.post("/api/doc/generate")
async def doc_generate(request: Request):
    """Render a JSON spec into a real .pptx/.xlsx/.docx and return it for download."""
    if not _DOCGEN_OK:
        return JSONResponse({"error": "Document generation is not available on the server."}, status_code=503)
    try:
        spec = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    try:
        data, mime, fname = docgen.generate(spec)
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"error": f"Could not generate document: {str(e)[:200]}"}, status_code=400)
    from urllib.parse import quote
    return Response(content=data, media_type=mime,
                    headers={"Content-Disposition": "attachment; filename=\"%s\"; filename*=UTF-8''%s" % (fname, quote(fname))})


# ─── AutoGrg: smart router — classify the task, pick the best model, inject expertise ───
AUTO_HARDWARE_BRIEF = (
    "You are Grg's HARDWARE EXPERT — precise, current PC/component advice.\n"
    "- Know CPUs (Intel Core/Core Ultra, AMD Ryzen), GPUs (Nvidia RTX/GTX, AMD Radeon RX, Intel Arc), "
    "motherboards (sockets LGA1700/1851, AM5/AM4; chipsets Z/B/X), RAM (DDR4/DDR5, speeds, dual-channel), "
    "storage (NVMe Gen4/5, SATA), PSUs (80+ rating, wattage + ~30% headroom), cooling (air vs AIO, TDP).\n"
    "- Compatibility: CPU socket ↔ board, RAM type ↔ platform, PSU wattage ≥ draw + headroom, GPU length/power connectors, case clearance.\n"
    "- Value: judge price/performance for the user's goal (gaming 1080p/1440p/4K, editing, streaming, workstation, budget vs high-end) and their region.\n"
    "- PRICES & STORES: LIVE web search results may be provided below. If present, base prices/availability/stores ONLY on them and CITE the links; never invent prices, stock or listings. If no results are given, give typical price TIERS and reputable retailers to check, and say prices should be verified.\n"
    "- Verify key specs against official maker data (Intel ARK, AMD, Nvidia); if unsure of an exact number, say so.\n"
    "- Answer with: a clear pick, a short why, alternatives at nearby price tiers, compatibility caveats, and any bottleneck/PSU/thermal warnings."
)
AUTO_APPBUILD_BRIEF = (
    "You are Grg's APP, WEBSITE, MOBILE & DOCUMENT BUILDING EXPERT — production-quality output.\n"
    "- Web default stack: Next.js (App Router) or Vite+React, TypeScript, TailwindCSS, shadcn/ui; Supabase/Prisma for data+auth; deploy Vercel/Netlify. Server Components by default, 'use client' only for interactivity, mutate via Server Actions, keep secrets server-side.\n"
    "- MOBILE (iOS + Android): default to React Native + Expo (expo-router, EAS build/submit) for one cross-platform codebase; Flutter as an alternative; native = SwiftUI (iOS) / Jetpack Compose (Android). Cover navigation, state (Zustand/TanStack Query), native permissions, and store submission (App Store / Play).\n"
    "- EMBEDDED / MICROCONTROLLERS: program any MCU. Families: AVR (Arduino Uno/Nano, 5V), ESP32/ESP8266 (WiFi+BLE, 3.3V), RP2040 (Pico), STM32, nRF52 (BLE), SAMD/Teensy; Raspberry Pi is a Linux SBC not an MCU. Languages: C/C++ (Arduino framework or vendor SDK), MicroPython/CircuitPython (Python on-chip), Rust (embedded-hal/Embassy). Toolchains: arduino-cli (`compile`/`upload` with an FQBN like arduino:avr:uno or esp32:esp32:esp32), PlatformIO (`pio run`/`pio run -t upload`), ESP-IDF, Pico SDK, STM32Cube, Zephyr. Structure sketches as setup()/loop(); NON-blocking timing with millis() not delay(); use pinMode/digitalWrite/analogRead/analogWrite, Serial, interrupts; buses I2C(Wire)/SPI/UART; PWM for motors/LEDs. WiFi/IoT on ESP32: WebServer/ESPAsyncWebServer, HTTPClient, MQTT (PubSubClient), BLE, deep sleep, OTA. Watch VOLTAGE (3.3V vs 5V), floating inputs (pull-ups), and power. Give a complete sketch + the exact build/flash commands.\n"
    "- ROBOTICS: never drive a motor from a logic pin — use a driver + separate motor supply + COMMON GROUND. DC motors -> H-bridge (L298N/TB6612/DRV8833), speed via PWM (ESP32: LEDC), direction via 2 pins; steppers -> A4988/DRV8825/TMC2209 (STEP/DIR, AccelStepper); BLDC -> ESC driven like a servo. Servos -> Servo/ESP32Servo (50Hz, 1-2ms = 0-180deg), separate 5-6V supply, PCA9685 for many. Close loops with PID: out = Kp*e + Ki*integral(e) + Kd*de/dt, with anti-windup (clamp integral), derivative-on-measurement, and a FIXED sample time; tune Kp then Kd then Ki. Differential drive = motor mixing: L=throttle+steer, R=throttle-steer, steer from a PID on the line/heading error. Feedback from quadrature encoders (interrupts) or an IMU (MPU6050). ARM KINEMATICS/IK: for a 2-link planar arm use the analytic law-of-cosines solution (cos(theta2)=(r^2-L1^2-L2^2)/(2*L1*L2), clamp to [-1,1]; theta1=atan2(y,x)-atan2(L2*sin(theta2),L1+L2*cos(theta2))); for a 3-DOF arm rotate the base with atan2(y,x) then solve the 2-link IK in the vertical plane; check reachability |L1-L2|<=reach<=L1+L2; map angles to servo microseconds with per-joint offset/direction/limits; for many DOF use CCD/FABRIK or a Jacobian, and ikpy/PyBullet/ROS2-MoveIt off the microcontroller.\n"
    "- ROS 2 (real robots): nodes talk over DDS via topics (pub/sub, e.g. /cmd_vel=geometry_msgs/Twist, /scan, /image_raw), services, actions; QoS must match. Python=rclpy, C++=rclcpp; build with colcon in a workspace (ament_python: package.xml+setup.py, console_scripts entry point), source install/setup.bash, run with ros2 run/launch; debug with ros2 topic echo/hz, rqt_graph, rviz2, ros2 bag. Ecosystem: TF2 (frames), URDF (model), Nav2 (navigation), MoveIt2 (arm planning+IK), ros2_control (motors), Gazebo (sim), micro-ROS (ROS2 on ESP32/STM32). Distros: Humble/Jazzy on Ubuntu.\n"
    "- COMPUTER VISION on robots (Python + OpenCV): capture (webcam / Picamera2 on Pi / Jetson), then color tracking (HSV inRange + contours), edges/Hough (line following), ArUco/AprilTag for ID+6-DoF pose, camera calibration; deep learning with YOLO (ultralytics) or OpenCV-DNN/TFLite/TensorRT on the edge; depth via stereo/RealSense. VISUAL SERVOING: turn the pixel/pose error into motor commands with a PID (center a target = PID on horizontal error -> steer; approach = PID on box size -> forward). In ROS 2 convert images with cv_bridge and publish /cmd_vel. Keep the loop fast (downscale, detect every N frames) and handle 'target lost'.\n"
    "- DOCUMENTS: to DELIVER a real downloadable file (PowerPoint/Excel/Word), output a fenced code block tagged grgdoc containing ONLY JSON — Grg renders it to a file with a Download button. Schemas: "
    "pptx = {\"type\":\"pptx\",\"filename\":\"name\",\"title\":\"Deck Title\",\"subtitle\":\"opt\",\"slides\":[{\"title\":\"Slide\",\"bullets\":[\"point\",\"point\"],\"notes\":\"opt\"}]}; "
    "xlsx = {\"type\":\"xlsx\",\"filename\":\"name\",\"sheets\":[{\"name\":\"Sheet1\",\"headers\":[\"A\",\"B\"],\"rows\":[[\"x\",1],[\"y\",2]]}]}; "
    "docx = {\"type\":\"docx\",\"filename\":\"name\",\"title\":\"Doc Title\",\"sections\":[{\"heading\":\"H\",\"level\":1,\"paragraphs\":[\"text\"],\"bullets\":[\"b1\"]}]}. "
    "Write a brief sentence, then the grgdoc block with rich, real content. Only emit grgdoc when the user actually wants a file.\n"
    "- UI/UX: mobile-first responsive, one type + spacing scale, dark mode via CSS tokens, accessible (semantic HTML, labels, focus rings), one clear primary action per view.\n"
    "- IMAGES: use REAL photos, never broken placeholders. In web/HTML use 'https://grg-ai.com/img?q=<comma,keywords>&w=1600&h=900' (add &i=2/&i=3 for distinct photos) — e.g. a hero for a restaurant in Rome: <img src=\"https://grg-ai.com/img?q=rome,italian+restaurant,pasta&w=1600&h=900\">.\n"
    "- Give runnable, self-contained code with correct file paths + install commands; reusable components; explain key decisions briefly."
)
_HW_RE = re.compile(r"(?i)\b(cpu|gpu|procesor|procesoare|plac[ai][ăa]? video|graphics card|rtx|gtx|radeon|arc a[0-9]|ryzen|core i[3579]|core ultra|geforce|nvidia|motherboard|plac[ăa] de baz[ăa]|chipset|ddr4|ddr5|nvme|psu|socket|am5|am4|lga1[0-9]{3}|cooler|tdp|benchmark|pc build|build a pc|config(ura[țt]ie)? (pc|gaming))\b")
_APP_RE = re.compile(r"(?i)(build (me )?(an?|a) (app|application|website|site|landing|dashboard)|create (an?|a) (app|website|site)|creeaz[ăa].*(app|site|aplica|website)|construie[sșşt]te.*(app|site|aplica|website)|landing page|next\.?js app|react app|website nou|aplica[țt]ie|react native|expo app|flutter|swiftui|jetpack compose|ios app|android app|mobile app|\.pptx|\.xlsx|\.docx|powerpoint|prezentare|slide deck|spreadsheet|excel|word document|document word|arduino|esp32|esp8266|microcontroll?er|microcontroler|micro-?controller|raspberry pi pico|rp2040|platformio|micropython|circuitpython|\bstm32\b|nrf52|firmware|\.ino\b|embedded|robot|robotic[ăa]?|\bservo\b|stepper|line follower|h-?bridge|l298n|tb6612|drv88[0-9]{2}|a4988|drv8825|pca9685|pid controller|balancing robot|differential drive|inverse kinematics|forward kinematics|kinematic[ăa]?|robot arm|bra[țt] robotic|ikpy|fabrik|jacobian|dh parameter|\bik\b|[0-9]-?dof|degrees of freedom|ros ?2|\brclpy\b|\brclcpp\b|colcon|rviz|nav2|moveit|micro-?ros|cv_bridge|opencv|computer vision|viziune computer|visual servoing|aruco|apriltag|\byolo\b|object detection|detec[țt]ie de obiecte)")
_CODE_RE = re.compile(r"(?i)(```|\breact\b|next\.?js|\bvite\b|tailwind|typescript|javascript|python|\bapi\b|function|component|deploy|supabase|prisma|\bcss\b|\bhtml\b|\bbug\b|error|refactor|database|\bsql\b|endpoint)")
_RESEARCH_RE = re.compile(r"(?i)(latest|current price|in stock|disponibil|caut[ăa] pe web|search the web|cele mai (noi|recente)|news about|știri)")

def _auto_classify(messages):
    text = ""
    for m in reversed(messages):
        if (m or {}).get("role") == "user":
            text = str(m.get("content") or "")[:1200]
            break
    if _HW_RE.search(text):
        return "hardware"
    if _APP_RE.search(text):
        return "app_build"
    if _RESEARCH_RE.search(text):
        return "research"
    if _CODE_RE.search(text):
        return "code"
    return "general"

_AUTO_BRIEF = {"hardware": AUTO_HARDWARE_BRIEF, "app_build": AUTO_APPBUILD_BRIEF}
# When the user has funds (Pro plan or credits), AutoGrg may pick premium models per task.
_AUTO_PREMIUM = {
    "code":      ("openrouter", "openai/gpt-5.1-codex",     "GPT-5.1 Codex"),
    "app_build": ("openrouter", "anthropic/claude-sonnet-5", "Claude Sonnet 5"),
    "hardware":  ("openrouter", "anthropic/claude-sonnet-5", "Claude Sonnet 5"),
    "research":  ("openrouter", "anthropic/claude-sonnet-5", "Claude Sonnet 5"),
    "general":   ("openrouter", "anthropic/claude-sonnet-5", "Claude Sonnet 5"),
}

def _auto_route(category, funded=False):
    """Funds-aware routing:
      - funded (Pro plan OR credits) → the best PREMIUM model for the task (charged, with margin);
      - otherwise → the best FREE Groq model (always works, no charge).
    (Groq's web-capable 'compound' is gone from this account, so hardware is knowledge-based
     until a search API is wired.)"""
    brief = _AUTO_BRIEF.get(category)
    label = category.replace("_", "-").title()
    if funded:
        pr, mdl, name = _AUTO_PREMIUM.get(category, _AUTO_PREMIUM["general"])
        return (pr, mdl, f"AutoGrg · {label} → {name}", brief)
    return ("groq", "openai/gpt-oss-120b", f"AutoGrg · {label}", brief)


# ─── Skill/knowledge retrieval for the WEBSITE (same docs Grg Code ships) ───
# The full skill .md files live next to server.py in ./knowledge/. When a chat
# question matches a skill, inject that whole doc so the site has Grg Code's depth.
_KB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge")
_KB_CACHE = {"docs": None, "ts": 0.0}
# Curated keywords per doc for good recall (plus the filename tokens, added below).
_KB_KW = {
    "arduino": ["arduino", ".ino", "avr", "atmega", "arduino-cli", "sketch", " uno", " nano"],
    "esp32-iot": ["esp32", "esp8266", "espressif", "wifi", "mqtt", " ble", "iot", "esphome", "nodemcu"],
    "microcontrollers": ["microcontroll", "micro-controller", "microcontroler", "stm32", "rp2040", "raspberry pi pico", " pico", "micropython", "circuitpython", "nrf52", "embedded", "firmware", "platformio", "teensy", " samd"],
    "robotics": ["robot", "robotic", " motor", " servo", "stepper", "h-bridge", "hbridge", "l298n", "tb6612", "drv88", "a4988", "encoder", "bldc", " esc ", "differential drive"],
    "pid-control": [" pid", "kp ", "ki ", "kd ", "control loop", "setpoint", "anti-windup", "windup", "ziegler", "pid tuning"],
    "kinematics-ik": ["kinematic", "inverse kinematics", "forward kinematics", " dof", "fabrik", "jacobian", "robot arm", "braț robotic", "dh parameter"],
    "ros2": ["ros2", "ros 2", "rclpy", "rclcpp", "colcon", "nav2", "moveit", "rviz", "cmd_vel", "micro-ros", "microros", " tf2", "urdf", "rosbag"],
    "robot-vision": ["opencv", "computer vision", "viziune computer", "visual servoing", "aruco", "apriltag", " yolo", "object detection", "cv_bridge", "picamera", "image processing"],
    "nextjs": ["next.js", "nextjs", "app router", "server component"],
    "react-vite": ["react", " vite", " jsx", "single-page"],
    "tailwind-shadcn": ["tailwind", "shadcn"],
    "supabase-prisma": ["supabase", "prisma"],
    "databases": ["database", " sql", "postgres", "mysql", "mongodb", "drizzle", "redis", "sqlite", "orm "],
    "auth-and-payments": ["auth", "authentication", "login", " jwt", "oauth", "stripe", "payment", "checkout", "subscription", "password"],
    "testing-qa": ["testing", "unit test", "vitest", " jest", "pytest", "playwright", " tdd", "e2e"],
    "devops-cicd": ["docker", "ci/cd", "github actions", "deploy", "kubernetes", "pipeline", "dockerfile"],
    "mobile-ios-android": ["react native", " expo", "flutter", "swiftui", "jetpack compose", "mobile app", " ios ", "android app"],
    "ios-native": ["swiftui", "ios native", "xcode", "app store"],
    "android-native": ["jetpack compose", "android native", "kotlin", "play store"],
    "browser-extensions": ["chrome extension", "browser extension", "manifest v3", "content script"],
    "cli-tools": [" cli", "command line", "commander", "typer", "argparse"],
    "ai-llm-apps": [" llm", " rag ", "embeddings", "vector db", "tool calling", "function calling", "chatbot", "openai api", "anthropic"],
    "games": [" game", "phaser", "godot", " unity", "canvas game", "game loop"],
    "security-performance": ["security", "owasp", " xss", " csrf", "sql injection", "performance", "lighthouse", "accessibility", "a11y"],
    "debugging": ["debug", "stack trace", "breakpoint", "traceback", "reproduce the bug"],
    "desktop-cross-platform": ["electron", " tauri", "desktop app"],
    "windows-apps": ["winui", ".net maui", " wpf ", "windows app", "winforms"],
    "macos-apps": ["appkit", "macos app", "notariz"],
    "linux-apps": [" gtk", " qt ", "flatpak", "appimage", "pyqt", "pyside"],
    "backend-apis": ["fastapi", "express", "rest api", "backend api", "endpoint"],
    "office-docs": [".pptx", ".xlsx", ".docx", "powerpoint", " excel", "word document", "spreadsheet"],
    "agent-playbook": [],
    "ui-ux": ["ui/ux", "design system", "figma"],
    "boilerplates": [],
}
def _kb_docs():
    now = time.time()
    if _KB_CACHE["docs"] is not None and now - _KB_CACHE["ts"] < 300:
        return _KB_CACHE["docs"]
    docs = {}
    try:
        for f in os.listdir(_KB_DIR):
            if f.lower().endswith(".md"):
                try:
                    with open(os.path.join(_KB_DIR, f), encoding="utf-8") as fh:
                        docs[f[:-3]] = fh.read()
                except Exception:  # noqa: BLE001
                    pass
    except Exception:  # noqa: BLE001
        pass
    _KB_CACHE["docs"] = docs; _KB_CACHE["ts"] = now
    return docs
def _kb_match(text, cap=4800):
    """Return the single most relevant skill doc's content for the query, or ''."""
    q = (text or "").lower()
    if not q.strip():
        return ""
    words = set(re.findall(r"[a-z0-9]+", q))
    docs = _kb_docs()
    if not docs:
        return ""

    def hit(kw):
        kw = kw.strip().lower()
        if not kw:
            return False
        if re.search(r"[^a-z0-9]", kw):          # phrase / has a symbol -> substring (specific enough)
            return kw in q
        if len(kw) >= 4:                          # real word -> exact or prefix (matches inflections)
            return any(w == kw or w.startswith(kw) for w in words)
        return kw in words                        # short token (cli, pid, uno) -> exact word only

    best, best_score = None, 0
    for name in docs:
        curated = set(_KB_KW.get(name, []))
        tokens = {t for t in re.split(r"[-_]", name) if len(t) > 2} - curated
        score = 2 * sum(1 for kw in curated if hit(kw)) + sum(1 for kw in tokens if hit(kw))
        if score > best_score:
            best, best_score = name, score
    if best and best_score >= 1:
        return docs[best][:cap]
    return ""


@app.post("/api/chat")
async def chat(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    provider = (body.get("provider") or "groq").lower()
    model = body.get("model")
    messages = body.get("messages") or []
    temperature = body.get("temperature", 0.7)
    max_tokens = body.get("max_tokens", 2048)

    # AutoGrg: classify the task, then route to the best model the user can afford
    # (premium if they have a Pro plan or credits; free otherwise) + inject expertise.
    routed = None
    if model == "auto" or provider == "auto":
        _cat = _auto_classify(messages)
        _avail = await _get_availability()
        # Premium only when the user has funds AND OpenRouter actually has credit right now.
        _funded = bool(_BILLING_OK and premium_allowed(body.get("uid")).get("allowed") and _avail.get("premium_ok"))
        provider, model, _label, _brief = _auto_route(_cat, _funded)
        # If the chosen FREE model isn't live on Groq now, fall back to one that is.
        if provider == "groq" and _avail.get("groq") and model not in _avail["groq"]:
            for _alt in ("openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"):
                if _alt in _avail["groq"]:
                    model = _alt
                    break
        routed = {"model": _label, "category": _cat, "premium": _funded}
        _inject = [_brief] if _brief else []
        # Live web (DuckDuckGo, no key) for hardware/research so answers use real, current data.
        if _cat in ("hardware", "research"):
            _q = ""
            for _m in reversed(messages):
                if (_m or {}).get("role") == "user":
                    _q = str(_m.get("content") or ""); break
            _results = await _web_search(_q, 5)
            if _results:
                _ctx = ("LIVE web search results for the user's question (today) — use these and CITE the links; "
                        "do NOT invent prices, stores or stock:\n" + "\n".join(
                            f"[{_i+1}] {_r['title']}\n{_r['url']}\n{_r['snippet']}" for _i, _r in enumerate(_results)))
                _inject.append(_ctx)
                routed["web"] = True
        if _inject:
            messages = [{"role": "system", "content": _s} for _s in _inject] + list(messages)

    # Deep skill retrieval (works for ANY model): if the question matches a skill,
    # inject that full doc so the site has the same depth as Grg Code.
    try:
        _qtext = ""
        for _m in reversed(messages):
            if (_m or {}).get("role") == "user":
                _qtext = str(_m.get("content") or ""); break
        _kb = _kb_match(_qtext)
        if _kb:
            messages = [{"role": "system", "content": "Reference knowledge for this task — follow it and give complete, runnable answers:\n\n" + _kb}] + list(messages)
    except Exception:  # noqa: BLE001
        pass

    if provider not in _PROVIDERS:
        return JSONResponse({"error": f"Unknown provider '{provider}'"}, status_code=400)
    if not model:
        return JSONResponse({"error": "Missing 'model'"}, status_code=400)
    if model not in ALLOWED_MODELS:
        return JSONResponse({"error": f"Model '{model}' is not enabled"}, status_code=403)
    if not isinstance(messages, list) or not messages:
        return JSONResponse({"error": "Missing 'messages'"}, status_code=400)

    url, key_fn, extra_headers = _PROVIDERS[provider]
    api_key = key_fn()
    if not api_key:
        return JSONResponse(
            {"error": f"{provider} API key not configured on server (.env)"},
            status_code=503,
        )

    # Premium models (paid OpenRouter, not ':free') need funds: Pro budget or wallet.
    uid = body.get("uid")
    is_premium = provider == "openrouter" and not str(model).endswith(":free")

    def _err_stream(msg):
        async def g():
            yield "data: " + json.dumps({"error": msg}) + "\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(g(), media_type="text/event-stream",
                                 headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

    if is_premium and _BILLING_OK:
        gate = premium_allowed(uid)
        if not gate.get("allowed"):
            if gate.get("reason") == "sign_in":
                return _err_stream("Sign in to use premium models.")
            return _err_stream("Out of credit — top up in Settings to use premium models, or pick a free Grg model.")

    # Prepend the Grg system persona if the client didn't send one.
    if not any((m or {}).get("role") == "system" for m in messages):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    headers.update(extra_headers)
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True,
    }
    # Ask the provider to report exact token usage so we charge precisely (money at stake).
    if is_premium:
        payload["stream_options"] = {"include_usage": True}

    est_in_tokens = (len(json.dumps(messages)) // 4) if is_premium else 0

    async def event_stream():
        out_chars = 0
        real_usage = None
        if routed:
            yield "data: " + json.dumps({"routed": routed}) + "\n\n"
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(180.0, connect=15.0)) as client:
                async with client.stream("POST", url, headers=headers, json=payload) as resp:
                    if resp.status_code != 200:
                        detail = (await resp.aread()).decode("utf-8", "ignore")[:300]
                        yield "data: " + json.dumps(
                            {"error": f"{provider} {resp.status_code}: {detail}"}
                        ) + "\n\n"
                        return
                    async for line in resp.aiter_lines():
                        if not line:
                            continue
                        line = line.strip()
                        if not line.startswith("data:"):
                            continue
                        data = line[5:].strip()
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                        except Exception:
                            continue
                        # Exact usage arrives in a final chunk (often with empty choices).
                        if is_premium and isinstance(chunk.get("usage"), dict):
                            real_usage = chunk["usage"]
                        try:
                            delta = chunk["choices"][0]["delta"]
                        except (KeyError, IndexError, TypeError):
                            delta = None
                        if delta:
                            # Reasoning / chain-of-thought tokens (gpt-oss, deepseek-r1, etc.)
                            rc = delta.get("reasoning")
                            if rc is None:
                                rc = delta.get("reasoning_content")
                            if rc:
                                yield "data: " + json.dumps({"reasoning": rc}) + "\n\n"
                            content = delta.get("content")
                            if content:
                                out_chars += len(content)
                                yield "data: " + json.dumps({"token": content}) + "\n\n"
            # Meter premium usage with the profit margin. Prefer the provider's EXACT
            # token counts; fall back to a char/4 estimate only if usage wasn't reported.
            if is_premium and _BILLING_OK and uid:
                try:
                    if real_usage:
                        in_tok = int(real_usage.get("prompt_tokens", 0))
                        out_tok = int(real_usage.get("completion_tokens", 0))
                    else:
                        in_tok, out_tok = est_in_tokens, out_chars // 4
                    charge_usage(uid, model, in_tok, out_tok)
                except Exception as ce:  # noqa: BLE001
                    print(f"[billing charge ERROR] {ce}")
            yield "data: [DONE]\n\n"
        except httpx.TimeoutException:
            yield "data: " + json.dumps({"error": "Upstream timed out"}) + "\n\n"
        except Exception as e:  # noqa: BLE001
            yield "data: " + json.dumps({"error": f"Proxy error: {e}"}) + "\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ─── IMAGE PROXY (Pollinations) — fetch server-side and crop the watermark off ───
@app.get("/api/image")
async def image(request: Request):
    prompt = (request.query_params.get("prompt") or "").strip()[:800]
    if not prompt:
        return JSONResponse({"error": "missing prompt"}, status_code=400)
    seed = request.query_params.get("seed", "")

    def _clampi(name, default, lo, hi):
        try:
            return max(lo, min(hi, int(request.query_params.get(name, default))))
        except Exception:
            return default

    out_w = _clampi("w", 1024, 256, 1536)
    out_h = _clampi("h", 1024, 256, 1536)
    band = 80                       # extra rows to hide the watermark strip, then crop away
    url = (
        f"https://image.pollinations.ai/prompt/{quote(prompt, safe='')}"
        f"?width={out_w}&height={out_h + band}&nologo=true&private=true&referrer=grg-ai.com&model=flux"
    )
    if seed:
        url += f"&seed={seed}"

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(90.0, connect=15.0), follow_redirects=True) as client:
            r = await client.get(url, headers={"Referer": "https://grg-ai.com/"})
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"error": f"image upstream error: {e}"}, status_code=502)
    if r.status_code != 200 or not r.content:
        return JSONResponse({"error": f"image upstream {r.status_code}"}, status_code=502)

    data = r.content
    headers = {"Cache-Control": "public, max-age=86400"}

    if _PIL_OK:
        try:
            img = _PILImage.open(BytesIO(data)).convert("RGB")
            w, h = img.size
            keep_h = max(1, int(round(h * out_h / (out_h + band))))  # drop the bottom watermark band
            img = img.crop((0, 0, w, keep_h))
            out = BytesIO()
            img.save(out, format="JPEG", quality=90)
            return Response(content=out.getvalue(), media_type="image/jpeg", headers=headers)
        except Exception:  # noqa: BLE001
            pass  # fall back to raw bytes if decode/crop fails

    return Response(content=data, media_type=r.headers.get("content-type", "image/jpeg"), headers=headers)


# ─── AGENT ENDPOINT (tool-calling, for the Grg Code desktop app) ───
# Models that run through Groq (fast, free, real tool-calling).
GROQ_AGENT_MODELS = {"openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b", "groq/compound", "groq/compound-mini"}

def _route_agent_model(model):
    """Return (provider, url, api_key, extra_headers, use_tools) for a model."""
    if model in GROQ_AGENT_MODELS or model.startswith("openai/gpt-oss"):
        return ("groq", "https://api.groq.com/openai/v1/chat/completions", GROQ_API_KEY, {}, True)
    # OpenRouter: paid models support tool-calling; ':free' ones generally do not.
    extra = {"HTTP-Referer": "https://grg-ai.com", "X-Title": "Grg Code"}
    return ("openrouter", "https://openrouter.ai/api/v1/chat/completions", OPENROUTER_API_KEY, extra, not model.endswith(":free"))

# Groq's free tier caps a request at ~8000 tokens/minute, and it counts
# max_tokens toward that budget. Keep input + max_tokens comfortably under it.
TPM_BUDGET = 7600

def _tok_est(obj):
    """Rough token estimate (~4 chars/token) from the JSON size."""
    try:
        return len(json.dumps(obj)) // 4
    except Exception:  # noqa: BLE001
        return 0

def _dyn_max_tokens(messages, tools, want):
    est_in = _tok_est(messages) + (_tok_est(tools) if tools else 0) + 200
    return max(512, min(want, 3072, TPM_BUDGET - est_in))

def _trim_messages(messages, keep_tail):
    """Drop the oldest turns to shrink an over-limit request, preserving a
    leading system message and never starting the tail on an orphan tool reply."""
    head = messages[:1] if (messages and messages[0].get("role") == "system") else []
    rest = messages[len(head):]
    tail = rest[-keep_tail:] if len(rest) > keep_tail else rest[:]
    while tail and tail[0].get("role") == "tool":
        tail = tail[1:]
    return head + tail

@app.post("/api/agent")
async def agent(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    model = body.get("model") or "openai/gpt-oss-120b"
    # AutoGrg for the agent: classify the task, then route to the best model the user can
    # afford (premium tool-capable model when funded; free Groq gpt-oss-120b otherwise).
    if model == "auto" or model == "grg-auto":
        _cat = _auto_classify(body.get("messages") or [])
        _avail = await _get_availability()
        _funded = bool(_BILLING_OK and premium_allowed(body.get("uid")).get("allowed") and _avail.get("premium_ok"))
        _pr, _mdl, _label, _brief = _auto_route(_cat, _funded)
        # The agent needs tool-calling: only keep the premium pick if it's not a ':free' model
        # (those don't support tools); otherwise fall back to the free Groq agent model.
        model = _mdl if (_mdl in ALLOWED_MODELS and not str(_mdl).endswith(":free")) else "openai/gpt-oss-120b"
    if model not in ALLOWED_MODELS and model not in GROQ_AGENT_MODELS:
        model = "openai/gpt-oss-120b"
    messages = body.get("messages") or []
    tools = body.get("tools")
    if not isinstance(messages, list) or not messages:
        return JSONResponse({"error": "Missing 'messages'"}, status_code=400)

    provider, url, api_key, extra_headers, use_tools = _route_agent_model(model)
    if not api_key:
        return JSONResponse({"error": f"{provider} key not configured on server"}, status_code=503)

    payload = {
        "model": model,
        "messages": messages,
        "temperature": body.get("temperature", 0.3),
        "max_tokens": _dyn_max_tokens(messages, tools if use_tools else None, body.get("max_tokens", 2048)),
    }
    if tools and use_tools:
        payload["tools"] = tools
        payload["tool_choice"] = body.get("tool_choice", "auto")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    headers.update(extra_headers)
    last_err = ""
    # Always respond 200 with an {error} field on failure so the client shows a clear message
    # (a raw 502 gets replaced by Cloudflare's gateway page). Retry on rate-limit / transient errors.
    for attempt in range(3):
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(170.0, connect=15.0)) as client:
                r = await client.post(url, headers=headers, json=payload)
            if r.status_code == 200:
                d = r.json()
                choice = d["choices"][0]
                return JSONResponse({"message": choice["message"], "finish_reason": choice.get("finish_reason"), "usage": d.get("usage")})
            # parse a helpful upstream message
            try:
                emsg = r.json().get("error", {}).get("message", "")[:220]
            except Exception:
                emsg = r.text[:220]
            last_err = f"{r.status_code} {emsg}".strip()
            if r.status_code in (429, 500, 502, 503) and attempt < 2:
                await asyncio.sleep(1.5 * (attempt + 1))
                continue
            if r.status_code == 429:
                hint = " — rate-limited, wait a few seconds or switch to a smaller model."
            elif r.status_code == 402:
                hint = " — this premium model needs OpenRouter credits. Add credits or pick a free Grg model."
            elif r.status_code == 404 and "tool" in emsg.lower():
                hint = " — this free model can't use tools; pick a Grg model (gpt-oss) for the agent."
            else:
                hint = ""
            return JSONResponse({"error": f"Model error {last_err}{hint}"})
        except httpx.TimeoutException:
            last_err = "timed out"
            if attempt < 2:
                await asyncio.sleep(1.0)
                continue
            return JSONResponse({"error": "The model took too long — try again or use a smaller model."})
        except Exception as e:  # noqa: BLE001
            last_err = str(e)[:200]
            if attempt < 2:
                await asyncio.sleep(1.0)
                continue
            return JSONResponse({"error": f"Connection error: {last_err}"})
    return JSONResponse({"error": f"Model busy: {last_err}"})


# ─── STREAMING AGENT (SSE): streams content tokens live + assembles tool_calls ───
@app.post("/api/agent/stream")
async def agent_stream(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    model = body.get("model") or "openai/gpt-oss-120b"
    # AutoGrg for the agent: classify the task, then route to the best model the user can
    # afford (premium tool-capable model when funded; free Groq gpt-oss-120b otherwise).
    if model == "auto" or model == "grg-auto":
        _cat = _auto_classify(body.get("messages") or [])
        _avail = await _get_availability()
        _funded = bool(_BILLING_OK and premium_allowed(body.get("uid")).get("allowed") and _avail.get("premium_ok"))
        _pr, _mdl, _label, _brief = _auto_route(_cat, _funded)
        # The agent needs tool-calling: only keep the premium pick if it's not a ':free' model
        # (those don't support tools); otherwise fall back to the free Groq agent model.
        model = _mdl if (_mdl in ALLOWED_MODELS and not str(_mdl).endswith(":free")) else "openai/gpt-oss-120b"
    if model not in ALLOWED_MODELS and model not in GROQ_AGENT_MODELS:
        model = "openai/gpt-oss-120b"
    messages = body.get("messages") or []
    tools = body.get("tools")
    if not isinstance(messages, list) or not messages:
        return JSONResponse({"error": "Missing 'messages'"}, status_code=400)

    provider, url, api_key, extra_headers, use_tools = _route_agent_model(model)
    if not api_key:
        return JSONResponse({"error": f"{provider} key not configured"}, status_code=503)

    # Premium (paid OpenRouter) models need funds; free Grg/Groq models are free.
    uid = body.get("uid")
    is_premium = provider == "openrouter" and not str(model).endswith(":free")

    def sse(obj):
        return "data: " + json.dumps(obj) + "\n\n"

    if is_premium and _BILLING_OK:
        gate = premium_allowed(uid)
        if not gate.get("allowed"):
            msg = ("Sign in to use premium models." if gate.get("reason") == "sign_in"
                   else "Out of credit — top up in Grg Code to use premium models, or pick a free Grg model.")
            async def _blocked():
                yield sse({"error": msg})
                yield "data: [DONE]\n\n"
            return StreamingResponse(_blocked(), media_type="text/event-stream",
                                     headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

    payload = {"model": model, "messages": messages,
               "temperature": body.get("temperature", 0.3),
               "max_tokens": _dyn_max_tokens(messages, tools if use_tools else None, body.get("max_tokens", 2048)),
               "stream": True}
    if is_premium:
        payload["stream_options"] = {"include_usage": True}  # exact token counts for metering
    if tools and use_tools:
        payload["tools"] = tools
        payload["tool_choice"] = body.get("tool_choice", "auto")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    headers.update(extra_headers)

    async def gen():
        import re as _re
        tool_acc = {}
        real_usage = None
        used_model = model
        # On the big free Groq model, fall back to a smaller (higher-limit) one
        # automatically if the rate limit keeps blocking us.
        candidates = [model]
        if model == "openai/gpt-oss-120b":
            candidates.append("openai/gpt-oss-20b")
        last_err = ""
        try:
            for ci, cur in enumerate(candidates):
                pr, purl, pkey, pextra, puse = _route_agent_model(cur)
                p2 = dict(payload)
                p2["model"] = cur
                if not (tools and puse):
                    p2.pop("tools", None)
                    p2.pop("tool_choice", None)
                h2 = {"Authorization": f"Bearer {pkey}", "Content-Type": "application/json"}
                h2.update(pextra)
                if ci > 0:
                    yield sse({"notice": f"Switching to a smaller model ({cur.split('/')[-1]}) to get past the rate limit…"})
                success = False
                for attempt in range(3):
                    async with httpx.AsyncClient(timeout=httpx.Timeout(180.0, connect=15.0)) as client:
                        async with client.stream("POST", purl, headers=h2, json=p2) as r:
                            if r.status_code == 200:
                                async for line in r.aiter_lines():
                                    line = line.strip()
                                    if not line.startswith("data:"):
                                        continue
                                    data = line[5:].strip()
                                    if data == "[DONE]":
                                        break
                                    try:
                                        chunk = json.loads(data)
                                    except ValueError:
                                        continue
                                    if is_premium and isinstance(chunk.get("usage"), dict):
                                        real_usage = chunk["usage"]
                                    try:
                                        delta = chunk["choices"][0]["delta"]
                                    except (KeyError, IndexError, TypeError):
                                        continue
                                    rc = delta.get("reasoning") or delta.get("reasoning_content")
                                    if rc:
                                        yield sse({"reasoning": rc})
                                    c = delta.get("content")
                                    if c:
                                        yield sse({"token": c})
                                    for tc in (delta.get("tool_calls") or []):
                                        idx = tc.get("index", 0)
                                        acc = tool_acc.setdefault(idx, {"id": "", "name": "", "arguments": ""})
                                        if tc.get("id"):
                                            acc["id"] = tc["id"]
                                        fn = tc.get("function") or {}
                                        if fn.get("name"):
                                            acc["name"] = fn["name"]
                                        if fn.get("arguments"):
                                            acc["arguments"] += fn["arguments"]
                                success = True
                                used_model = cur
                            else:
                                detail = (await r.aread()).decode("utf-8", "ignore")[:260]
                                last_err = f"{r.status_code} {detail}".strip()
                                if r.status_code == 413 and attempt < 2:
                                    # Request bigger than the per-minute budget. Shrink the
                                    # reply room first, then trim the oldest context, and retry.
                                    cur_max = p2.get("max_tokens", 2048)
                                    if cur_max > 1024:
                                        p2["max_tokens"] = 1024
                                    else:
                                        p2["messages"] = _trim_messages(p2["messages"], 6)
                                        p2["max_tokens"] = min(cur_max, 1024)
                                    yield sse({"notice": "Request too large — trimming context and retrying…"})
                                    continue
                                if r.status_code in (429, 500, 502, 503) and attempt < 2:
                                    m = _re.search(r"try again in ([\d.]+)s", detail)
                                    wait = min(22.0, float(m.group(1)) + 0.5) if m else 2.0 * (attempt + 1)
                                    if r.status_code == 429:
                                        yield sse({"notice": f"Rate limit reached — retrying in {int(wait) + 1}s…"})
                                    await asyncio.sleep(wait)
                                    continue  # retry the same model
                                break  # non-retryable, or attempts exhausted → next candidate
                    if success:
                        break
                if success:
                    break
            else:
                hint = ""
                low = last_err.lower()
                if last_err.startswith("429"):
                    hint = " — the free tier limit was exceeded; wait a minute or add OpenRouter credits for a bigger model."
                elif last_err.startswith("413"):
                    hint = " — the request is too big for the free tier; try /compact or a fresh session, or add OpenRouter credits."
                elif last_err.startswith("402"):
                    hint = " — this premium model needs OpenRouter credits."
                elif last_err.startswith("404") and "tool" in low:
                    hint = " — this free model can't use tools; pick a Grg model."
                yield sse({"error": f"Model error {last_err}{hint}"})
                return
            # Meter premium usage (exact provider token counts) with the profit margin.
            if is_premium and _BILLING_OK and uid and real_usage:
                try:
                    charge_usage(uid, used_model,
                                 int(real_usage.get("prompt_tokens", 0)),
                                 int(real_usage.get("completion_tokens", 0)))
                except Exception as ce:  # noqa: BLE001
                    print(f"[agent billing charge ERROR] {ce}")
            if tool_acc:
                calls = [{"id": v["id"] or f"call_{k}", "type": "function",
                          "function": {"name": v["name"], "arguments": v["arguments"]}}
                         for k, v in sorted(tool_acc.items())]
                yield sse({"tool_calls": calls})
            yield "data: [DONE]\n\n"
        except httpx.TimeoutException:
            yield sse({"error": "The model took too long — try again or use a smaller model."})
        except Exception as e:  # noqa: BLE001
            yield sse({"error": f"Connection error: {str(e)[:200]}"})

    return StreamingResponse(gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.on_event("startup")
async def startup():
    print("\n" + "=" * 50)
    print("   GRG AI — Starting up (Pi mode)...")
    print(f"   Groq key:       {'LOADED' if GROQ_API_KEY else 'MISSING'}")
    print(f"   OpenRouter key: {'LOADED' if OPENROUTER_API_KEY else 'MISSING'}")
    print("   Streaming chat proxy: ENABLED")
    print(f"   Image proxy (crop):   {'ENABLED (Pillow)' if _PIL_OK else 'RAW (no Pillow)'}")
    print("   nHash payments: ENABLED")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
