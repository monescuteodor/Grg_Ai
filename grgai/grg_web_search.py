"""
grg_web_search.py — Smart Web Search for Grg AI
Searches DuckDuckGo, fetches actual page content, extracts relevant info.
"""

import re
import urllib.parse
import urllib.request
import json
import ssl

_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/json",
    "Accept-Language": "en-US,en;q=0.9",
}

# ─── SMART TRIGGER DETECTION ───

_MUST_SEARCH = re.compile(
    r'\b(who (is|was|won|created|founded|invented|discovered|leads|runs|owns))\b'
    r'|\b(what (is|are|was|were|happened|does))\b'
    r'|\b(when (is|was|did|will|does))\b'
    r'|\b(where (is|are|was|can))\b'
    r'|\b(how (much|many|old|long|far|tall|big|fast))\b'
    r'|\b(latest|newest|current|recent|today|now|2024|2025|2026|2027)\b'
    r'|\b(news|update|release|version|price|cost|worth|salary|population)\b'
    r'|\b(best|top|recommend|popular|trending|fastest|biggest|largest)\b'
    r'|\b(download|install|setup|configure|tutorial|guide)\b'
    r'|\b(error|bug|fix|issue|problem|crash|not working|solution)\b'
    r'|\b(vs|versus|compare|comparison|difference|between)\b'
    r'|\b(meaning|definition|define)\b'
    r'|\b(weather|temperature|forecast)\b'
    r'|\b(score|winner|champion|result|standings)\b'
    r'|\b(died|born|age|alive|married)\b'
    r'|\b(country|capital|president|minister|king|queen|leader)\b'
    r'|\b(company|ceo|founder|stock|market)\b'
    r'|\?',
    re.IGNORECASE
)

_NO_SEARCH = re.compile(
    r'^\s*(write|create|make|build|generate|implement|code|develop|design)\b'
    r'|^\s*(fix|debug|refactor|optimize|improve|review)\s+(this|my|the)\b'
    r'|\b(function|class|program|script|app|game|website|api|server|component)\s*(for|that|which|to)\b'
    r'|```'
    r'|^\s*(hi|hello|hey|salut|buna|thanks|mersi|ok|da|nu|bye)\s*[!.]?\s*$',
    re.IGNORECASE
)


def should_search(query):
    query = query.strip()
    if len(query) < 3:
        return False
    if _NO_SEARCH.search(query):
        return False
    if _MUST_SEARCH.search(query):
        return True
    words = query.split()
    if len(words) <= 15 and '```' not in query:
        if query.rstrip().endswith('?') or words[0].lower() in ('who','what','when','where','why','how','is','are','was','were','did','does','do','can','will','which'):
            return True
    return False


# ─── SEARCH ENGINE ───

def web_search(query, max_results=5):
    raw_results = _ddg_search(query, max_results)
    if not raw_results:
        raw_results = _ddg_instant(query)
    if not raw_results:
        return []

    enriched = []
    fetch_count = 0
    for r in raw_results:
        if fetch_count < 2 and r.get('url') and r['url'].startswith('http'):
            try:
                content = _fetch_page_text(r['url'], max_chars=2000)
                if content and len(content) > 100:
                    r['content'] = content
                    fetch_count += 1
            except Exception:
                pass
        enriched.append(r)
    return enriched


def _ddg_search(query, max_results=5):
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=_SSL_CTX) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        results = []
        links = re.findall(r'class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</(?:a|span|div)', html, re.DOTALL)

        for i in range(min(max_results, len(links))):
            href, title_html = links[i]
            title = re.sub(r'<[^>]+>', '', title_html).strip()
            snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else ""

            if 'uddg=' in href:
                match = re.search(r'uddg=([^&]+)', href)
                if match:
                    href = urllib.parse.unquote(match.group(1))

            if title and (snippet or href):
                results.append({"title": title[:200], "snippet": snippet[:500], "url": href})

        return results
    except Exception as e:
        print(f"[Web Search] DDG HTML error: {e}")
        return []


def _ddg_instant(query):
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "GrgAI/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        results = []
        if data.get("AbstractText"):
            results.append({
                "title": data.get("Heading", "Answer"),
                "snippet": data["AbstractText"][:800],
                "url": data.get("AbstractURL", ""),
            })
        for topic in data.get("RelatedTopics", [])[:3]:
            if isinstance(topic, dict) and "Text" in topic:
                results.append({
                    "title": topic.get("FirstURL", "").split("/")[-1].replace("_", " "),
                    "snippet": topic["Text"][:500],
                    "url": topic.get("FirstURL", ""),
                })
        return results
    except Exception as e:
        print(f"[Web Search] DDG API error: {e}")
        return []


def _fetch_page_text(url, max_chars=2000):
    try:
        req = urllib.request.Request(url, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=8, context=_SSL_CTX) as resp:
            content_type = resp.headers.get('Content-Type', '')
            if 'text/html' not in content_type and 'application/json' not in content_type:
                return None
            raw = resp.read(100000)
            html = raw.decode("utf-8", errors="replace")

        html = re.sub(r'<(script|style|nav|footer|header|aside|iframe|noscript)[^>]*>[\s\S]*?</\1>', '', html, flags=re.I)
        html = re.sub(r'<!--[\s\S]*?-->', '', html)
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'(Cookie|cookie|GDPR|privacy policy|Terms of Service|Subscribe|Sign up|Log in|Menu|Navigation)[\s,.]', '', text)

        if len(text) > max_chars:
            start = min(200, len(text) // 10)
            text = text[start:start + max_chars]

        return text.strip() if len(text.strip()) > 50 else None
    except Exception as e:
        print(f"[Web Search] Fetch error for {url[:50]}: {e}")
        return None


# ─── FORMAT FOR LLM ───

def format_search_results(results):
    if not results:
        return ""

    parts = ["=== WEB SEARCH RESULTS ==="]
    parts.append("Use the following real-time information to give an accurate, up-to-date answer.\n")

    for i, r in enumerate(results, 1):
        parts.append(f"[Source {i}] {r['title']}")
        if r.get('snippet'):
            parts.append(f"Summary: {r['snippet']}")
        if r.get('content'):
            parts.append(f"Page content: {r['content'][:1500]}")
        if r.get('url'):
            parts.append(f"URL: {r['url']}")
        parts.append("")

    parts.append("=== END SEARCH RESULTS ===")
    parts.append("IMPORTANT: Base your answer on the search results above. If the results contain the answer, use it. Cite sources when possible.")
    return "\n".join(parts)
