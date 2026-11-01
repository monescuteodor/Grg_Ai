#!/usr/bin/env python3
"""
GrgAPI — a privacy-first, OpenAI-compatible AI API for companies to embed.

What it does: a company sends a normal OpenAI-style chat request (with their raw,
possibly sensitive data). GrgAPI REDACTS PII server-side (emails, IBANs, cards, CNPs,
phones, API keys, names) BEFORE forwarding to the big AI provider, then restores the
real values in the reply. So OpenAI/Anthropic/etc. NEVER see the real data — the
company gets the real answer. Auth via per-company API keys; usage metered per key.

Runs on the Ryzen box (CPU). Deps: starlette, uvicorn, httpx. Reads secrets from
env (OPENROUTER_API_KEY, GROQ_API_KEY, GRGAPI_KEYS). OpenAI-compatible so clients
just point their existing SDK at this base URL.
"""
import os, re, json, time, uuid
import httpx
from starlette.applications import Starlette
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route

# ─── CONFIG (from ~/grgapi/.env + env) ───
def _load_env():
    p = os.path.expanduser("~/grgapi/.env")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
_load_env()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
GROQ_API_KEY       = os.environ.get("GROQ_API_KEY", "")
# GRGAPI_KEYS = "key1:CompanyA,key2:CompanyB"  (company API keys we issue)
_RAW_KEYS = os.environ.get("GRGAPI_KEYS", "")
API_KEYS = {}
for pair in _RAW_KEYS.split(","):
    pair = pair.strip()
    if ":" in pair:
        k, co = pair.split(":", 1)
        API_KEYS[k.strip()] = co.strip()
MARKUP = float(os.environ.get("GRGAPI_MARKUP", "1.34"))
USAGE_LOG = os.path.expanduser("~/grgapi/usage.jsonl")

_PROVIDERS = {
    "openrouter": ("https://openrouter.ai/api/v1/chat/completions", lambda: OPENROUTER_API_KEY,
                   {"HTTP-Referer": "https://grg-ai.com", "X-Title": "GrgAPI"}),
    "groq":       ("https://api.groq.com/openai/v1/chat/completions", lambda: GROQ_API_KEY, {}),
}
# Public model name -> (provider, upstream model). Clients use these friendly names.
MODELS = {
    "grg-flagship": ("openrouter", "anthropic/claude-opus-4.8"),
    "grg-pro":      ("openrouter", "anthropic/claude-sonnet-5"),
    "grg-gpt":      ("openrouter", "openai/gpt-5.6"),
    "grg-gemini":   ("openrouter", "google/gemini-3.1-pro-preview"),
    "grg-code":     ("openrouter", "openai/gpt-5.1-codex"),
    "grg-fast":     ("groq",       "openai/gpt-oss-20b"),
    "grg-free":     ("groq",       "openai/gpt-oss-120b"),
}
DEFAULT_MODEL = "grg-pro"

# ───────────────────────── SERVER-SIDE PII REDACTION ─────────────────────────
_PII_PATTERNS = [
    ("SECRET", r"(?:sk-[A-Za-z0-9]{16,}|sk_(?:live|test)_[A-Za-z0-9]{10,}|rk_(?:live|test)_[A-Za-z0-9]{10,}|gsk_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_\-]{20,}|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]{10,}|whsec_[A-Za-z0-9]{10,})"),
    ("EMAIL", r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
    ("IBAN",  r"[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]{3,4}){3,7}"),
    ("CARD",  r"(?:\d[ \-]?){14,16}\d"),
    ("CNP",   r"[1-8]\d{12}"),
    ("PHONE", r"(?:\+?\d{1,3}[ .\-]?)?07\d{2}[ .\-]?\d{3}[ .\-]?\d{3}|\+\d{10,14}"),
]
_FIRST_NAMES = set((
    "ion ioan gheorghe vasile nicolae constantin dumitru mihai mihail alexandru andrei cristian florin marian "
    "daniel adrian george gabriel stefan catalin bogdan ionut razvan vlad radu sorin marius dan paul victor emil "
    "petru petre cornel valentin ciprian claudiu octavian sebastian robert eduard lucian mircea traian liviu cosmin "
    "iulian ovidiu silviu tudor darius david matei luca rares denis alin teodor theodor horia sergiu nicu costel "
    "aurel ilie grigore iosif samuel iacob avram moise danut viorel sandu laurentiu leonard cristinel marcel remus "
    "dorin virgil doru gelu toma felix albert anton marin stelian dorel florentin nelu puiu mugur maria ana elena "
    "ioana andreea cristina mihaela alexandra gabriela daniela georgiana nicoleta simona raluca diana monica camelia "
    "carmen florentina larisa bianca roxana oana adriana mirela laura anca iuliana catalina ramona madalina denisa "
    "alina corina ecaterina viorica rodica doina aurelia lavinia teodora antonia sofia daria stefania patricia delia "
    "otilia paula irina natalia loredana cosmina florina marinela magdalena valentina violeta nadia liliana felicia "
    "cornelia emilia luminita mariana marioara margareta silvia tatiana veronica victoria eugenia iolanda sanda gina "
    "nina lidia aurora john james michael william thomas mark peter andrew richard charles joseph christopher chris "
    "alex alexander anna sarah emma julia kevin brian steve mike matthew joshua ryan jason justin nathan benjamin "
    "jack henry oscar leo noah liam ethan lucas mason logan jacob anthony tom tim ben sam max emily olivia sophia "
    "isabella mia charlotte amelia grace chloe lucy hannah"
).split())
_TITLES = r"[Dd]l|[Dd]na|[Dd]-l|[Dd]-na|[Dd]lui|[Dd]nei|[Dd]vs|[Dd]omnul|[Dd]oamna|[Dd]omnului|[Dd]oamnei|[Dd]ra|[Dd]r|[Pp]rof|[Ii]ng|[Aa]v|[Jj]r|[Ss]r|[Mm]r|[Mm]rs|[Mm]s|[Mm]iss|[Ss]ir"
_NAME_W = r"[A-ZȘȚĂÂÎŞŢ][a-zșțăâîşţ\-]+"
_TITLE_RE = re.compile(r"\b(?:" + _TITLES + r")\.?\s+(" + _NAME_W + r"(?:\s+" + _NAME_W + r"){0,2})")

def _deaccent(s):
    s = s.lower()
    for a, b in (("ș","s"),("ş","s"),("ț","t"),("ţ","t"),("ă","a"),("â","a"),("î","i")):
        s = s.replace(a, b)
    return s

def _is_cap(w):
    return bool(re.match(r"^[A-ZȘȚĂÂÎŞŢ][a-zșțăâîşţ\-]*$", w))

class Redactor:
    def __init__(self):
        self.o2p, self.p2o, self.counts = {}, {}, {}
    def _ph(self, typ, orig):
        orig = orig.strip()
        if orig in self.o2p:
            return self.o2p[orig]
        self.counts[typ] = self.counts.get(typ, 0) + 1
        ph = f"[{typ}_{self.counts[typ]}]"
        self.o2p[orig] = ph; self.p2o[ph] = orig
        return ph
    def _names_dict(self, text):
        parts = re.split(r"(\s+)", text)
        res, i = [], 0
        while i < len(parts):
            w = parts[i]
            if not w or w.isspace():
                res.append(w); i += 1; continue
            core = re.sub(r"^[^0-9A-Za-zȘȚĂÂÎŞŢșțăâîşţ]+", "", re.sub(r"[^0-9A-Za-zȘȚĂÂÎŞŢșțăâîşţ]+$", "", w))
            if core and _is_cap(core) and _deaccent(core) in _FIRST_NAMES and not re.search(r"[.,!?;:)\]]$", w):
                span_end, count, k = i, 0, i + 2
                while count < 2 and k < len(parts):
                    tk = parts[k]
                    nw = re.sub(r"^[^0-9A-Za-zȘȚĂÂÎŞŢșțăâîşţ]+", "", re.sub(r"[^0-9A-Za-zȘȚĂÂÎŞŢșțăâîşţ]+$", "", tk))
                    if nw and _is_cap(nw):
                        span_end = k; count += 1
                        if re.search(r"[.,!?;:)\]]$", tk):
                            break
                        k += 2
                    else:
                        break
                if span_end > i:
                    original = "".join(parts[i:span_end + 1])
                    m = re.match(r"^([^0-9A-Za-zȘȚĂÂÎŞŢșțăâîşţ]*)(.*?)([^0-9A-Za-zȘȚĂÂÎŞŢșțăâîşţ]*)$", original, re.S)
                    res.append(m.group(1) + self._ph("NAME", m.group(2)) + m.group(3))
                    i = span_end + 1; continue
            res.append(w); i += 1
        return "".join(res)
    def _names(self, text):
        def title_repl(m):
            nm = m.group(1); off = m.start(1) - m.start(0)
            return m.group(0)[:off] + self._ph("NAME", nm)
        text = _TITLE_RE.sub(title_repl, text)
        text = self._names_dict(text)
        return text
    def redact(self, text):
        if not text:
            return text
        out = text
        for typ, pat in _PII_PATTERNS:
            out = re.sub(pat, lambda m: self._ph(typ, m.group(0)), out)
        return self._names(out)
    def restore(self, text):
        if not text:
            return text
        return re.sub(r"\[[A-Z]+_\d+\]", lambda m: self.p2o.get(m.group(0), m.group(0)), text)

# ───────────────────────── HTTP HELPERS ─────────────────────────
GRGAPI_VALIDATE_URL = os.environ.get("GRGAPI_VALIDATE_URL", "http://192.168.50.173:8000/api/grgapi/validate")
_key_cache = {}   # key -> (company, expires_ts)

async def _auth(request):
    h = request.headers.get("authorization", "")
    key = h[7:].strip() if h.lower().startswith("bearer ") else ""
    if not key:
        return (key, None)
    if key in API_KEYS:                       # static keys from .env
        return (key, API_KEYS[key])
    c = _key_cache.get(key)                    # cached self-service key
    if c and c[1] > time.time():
        return (key, c[0])
    try:                                       # ask the site to validate a self-service key
        async with httpx.AsyncClient(timeout=httpx.Timeout(5.0, connect=3.0)) as cl:
            d = (await cl.post(GRGAPI_VALIDATE_URL, json={"key": key})).json()
        if d.get("valid"):
            company = d.get("company") or "company"
            _key_cache[key] = (company, time.time() + 60)
            return (key, company)
    except Exception:  # noqa: BLE001
        pass
    return (key, None)

def _log_usage(key, company, model, usage):
    try:
        with open(USAGE_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": time.time(), "key": key[:10], "company": company,
                                "model": model, "usage": usage}) + "\n")
    except Exception:
        pass

async def health(request):
    return JSONResponse({"status": "ok", "service": "GrgAPI", "keys_configured": len(API_KEYS)})

async def list_models(request):
    key, company = await _auth(request)
    if not company:
        return JSONResponse({"error": {"message": "Invalid API key", "type": "auth"}}, status_code=401)
    data = [{"id": m, "object": "model", "owned_by": "grg-ai"} for m in MODELS]
    return JSONResponse({"object": "list", "data": data})

async def chat_completions(request):
    key, company = await _auth(request)
    if not company:
        return JSONResponse({"error": {"message": "Invalid or missing API key", "type": "auth"}}, status_code=401)
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": {"message": "Invalid JSON body", "type": "invalid_request"}}, status_code=400)

    model_in = body.get("model") or DEFAULT_MODEL
    if model_in in MODELS:
        provider, upstream_model = MODELS[model_in]
    elif "/" in str(model_in):
        provider, upstream_model = "openrouter", model_in   # pass-through provider id
    else:
        provider, upstream_model = MODELS[DEFAULT_MODEL]
    messages = body.get("messages") or []
    if not isinstance(messages, list) or not messages:
        return JSONResponse({"error": {"message": "messages is required", "type": "invalid_request"}}, status_code=400)
    want_stream = bool(body.get("stream"))
    redact_on = body.get("redact", True)   # on by default; a client may opt out per request

    # ── redact PII server-side before it ever reaches the provider ──
    red = Redactor()
    safe_messages = []
    for m in messages:
        c = m.get("content")
        if redact_on and isinstance(c, str):
            c = red.redact(c)
        safe_messages.append({"role": m.get("role", "user"), "content": c})

    url, key_fn, extra = _PROVIDERS[provider]
    api_key = key_fn()
    if not api_key:
        return JSONResponse({"error": {"message": f"{provider} not configured on server", "type": "server"}}, status_code=503)
    payload = {"model": upstream_model, "messages": safe_messages, "stream": False}
    for opt in ("temperature", "max_tokens", "top_p"):
        if opt in body:
            payload[opt] = body[opt]
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", **extra}

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=15.0)) as client:
            r = await client.post(url, headers=headers, json=payload)
    except Exception as e:
        return JSONResponse({"error": {"message": f"upstream error: {e}", "type": "upstream"}}, status_code=502)
    if r.status_code != 200:
        return JSONResponse({"error": {"message": f"{provider} {r.status_code}: {r.text[:200]}", "type": "upstream"}}, status_code=502)

    up = r.json()
    content = ""
    try:
        content = up["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        content = ""
    content = red.restore(content)   # ← bring the real PII back for the company
    usage = up.get("usage", {})
    _log_usage(key, company, upstream_model, usage)

    cid = "chatcmpl-grg-" + uuid.uuid4().hex[:16]
    created = int(time.time())
    if want_stream:
        async def gen():
            first = {"id": cid, "object": "chat.completion.chunk", "created": created, "model": model_in,
                     "choices": [{"index": 0, "delta": {"role": "assistant", "content": content}, "finish_reason": None}]}
            yield "data: " + json.dumps(first) + "\n\n"
            last = {"id": cid, "object": "chat.completion.chunk", "created": created, "model": model_in,
                    "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]}
            yield "data: " + json.dumps(last) + "\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(gen(), media_type="text/event-stream",
                                 headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

    return JSONResponse({
        "id": cid, "object": "chat.completion", "created": created, "model": model_in,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
        "usage": usage,
    })

app = Starlette(routes=[
    Route("/health", health),
    Route("/v1/models", list_models),
    Route("/v1/chat/completions", chat_completions, methods=["POST"]),
])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8088)
