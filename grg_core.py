"""
grg_core.py — Grg AI Core Engine
Self-hosted AI with RAG, web search, chain-of-thought, skill detection, anti-hallucination.
"""

import os
import re
import json
import hashlib
import time
from pathlib import Path
from grg_web_search import should_search, web_search, format_search_results

# ─── CONFIGURATION ───
SCRIPT_DIR = Path(__file__).parent
MODEL_PATH = SCRIPT_DIR / "grg-model.gguf"
KNOWLEDGE_DIR = SCRIPT_DIR / "Knowledge"
INDEX_DIR = SCRIPT_DIR / ".grg_index"
PROMPT_HISTORY_FILE = SCRIPT_DIR / ".grg_prompt_stats.json"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 8
MAX_CHUNK = 800
MIN_CHUNK = 50
DISTANCE_THRESHOLD = 1.2
MAX_HISTORY_CHARS = 6000
DEFAULT_MAX_TOKENS = 2048

_BIG_REQUEST_KEYWORDS = [
    'write', 'create', 'build', 'implement', 'generate', 'make', 'develop',
    'full', 'complete', 'entire', 'whole', 'detailed', 'comprehensive',
    'project', 'application', 'app', 'server', 'website', 'api',
    'file', 'class', 'component', 'module', 'script', 'program',
    'tutorial', 'guide', 'example', 'code',
    'scrie', 'creaza', 'fa-mi', 'genereaza', 'implementeaza',
    'complet', 'detaliat', 'intreg', 'tot', 'mare',
    'proiect', 'aplicatie', 'fisier', 'clasa', 'componenta',
]

def _estimate_max_tokens(message):
    msg_lower = message.lower()
    hits = sum(1 for kw in _BIG_REQUEST_KEYWORDS if kw in msg_lower)
    msg_len = len(message)
    app_words = ['app', 'application', 'website', 'landing', 'dashboard', 'page', 'game', 'full', 'complete', 'entire']
    app_hits = sum(1 for kw in app_words if kw in msg_lower)
    if app_hits >= 1 and hits >= 1:
        return 4096
    elif hits >= 3 or msg_len > 500:
        return 3072
    elif hits >= 1 or msg_len > 200:
        return 2048
    else:
        return DEFAULT_MAX_TOKENS


# ─── SAFETY FILTER ───
_BLOCKED_PATTERNS = [
    (re.compile(r'\b(how to make|how to build|recipe for)\b.{0,30}\b(bomb|explosive|weapon|poison|meth|cocaine|heroin)\b', re.I),
     "I can't help with creating dangerous substances or weapons."),
    (re.compile(r'\b(hack into|break into|steal from)\b.{0,30}\b(bank|account|password|server)\b', re.I),
     "I can't assist with unauthorized access to systems or accounts."),
    (re.compile(r'\b(how to|ways to)\b.{0,20}\b(kill|murder|harm|hurt)\b.{0,20}\b(person|people|someone|myself)\b', re.I),
     "I can't assist with content that could harm people."),
]

def _check_blocked_topic(message):
    for pattern, refusal in _BLOCKED_PATTERNS:
        if pattern.search(message):
            return refusal
    return None


# ─── SELF-IMPROVING PROMPT STATS ───
_prompt_stats = {"code": 0, "factual": 0, "search": 0, "topics": {}}

def _load_prompt_stats():
    global _prompt_stats
    try:
        if PROMPT_HISTORY_FILE.exists():
            _prompt_stats = json.loads(PROMPT_HISTORY_FILE.read_text())
    except Exception:
        pass

def _save_prompt_stats():
    try:
        PROMPT_HISTORY_FILE.write_text(json.dumps(_prompt_stats))
    except Exception:
        pass

def _track_question(message, q_type):
    _prompt_stats[q_type] = _prompt_stats.get(q_type, 0) + 1
    topics = _prompt_stats.get("topics", {})
    keywords = re.findall(r'\b(python|javascript|react|html|css|sql|api|docker|git|node|fastapi|flask|django|rust|go|java|kotlin|swift|flutter|typescript|next|vue|angular)\b', message.lower())
    for kw in keywords:
        topics[kw] = topics.get(kw, 0) + 1
    _prompt_stats["topics"] = topics
    _save_prompt_stats()

def _get_top_topics(n=5):
    topics = _prompt_stats.get("topics", {})
    sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
    return [t[0] for t in sorted_topics[:n]]


# ─── SKILL LEVEL DETECTION ───
def _detect_skill_level(message, history=None):
    msg = message.lower()
    full_context = msg
    if history:
        for turn in history[-5:]:
            full_context += " " + turn.get("user", "").lower()

    beginner_signals = [
        "i'm new", "i am new", "beginner", "just started", "learning",
        "don't understand", "what is", "what does", "how do i", "how does",
        "simple", "easy", "basic", "explain", "i don't know", "first time",
        "never used", "step by step", "from scratch", "for dummies",
    ]
    expert_signals = [
        "optimize", "performance", "refactor", "architecture", "scalable",
        "production", "benchmark", "profiling", "complexity", "algorithm",
        "concurrent", "async", "race condition", "memory leak", "thread safe",
        "microservices", "kubernetes", "distributed", "caching strategy",
        "design pattern", "solid principles", "dependency injection",
    ]
    beginner_score = sum(1 for s in beginner_signals if s in full_context)
    expert_score = sum(1 for s in expert_signals if s in full_context)
    if beginner_score > expert_score:
        return 'beginner'
    elif expert_score >= 2:
        return 'expert'
    return 'intermediate'

def _build_skill_addon(skill_level):
    if skill_level == 'beginner':
        return """
USER SKILL LEVEL: BEGINNER
- Use simple language. Explain jargon when used.
- Explain WHY, not just HOW. Use analogies.
- Break steps into small numbered pieces.
- Add comments to every important line of code.
- Mention common beginner mistakes to avoid."""
    elif skill_level == 'expert':
        return """
USER SKILL LEVEL: EXPERT
- Skip basic explanations. Go straight to advanced details.
- Use technical terminology freely.
- Discuss trade-offs, performance, and edge cases.
- Show multiple approaches with pros/cons.
- Reference design patterns by name."""
    else:
        return """
USER SKILL LEVEL: INTERMEDIATE
- Balance explanation with technical depth.
- Show complete code with brief explanations.
- Mention best practices and common pitfalls."""

def _detect_needs_clarification(message):
    msg = message.strip()
    vague_patterns = [
        r'^(fix|help|error|bug|problem|issue)\s*[.!?]?\s*$',
        r'^(write|make|create|build)\s+\w{1,10}\s*$',
    ]
    for p in vague_patterns:
        if re.match(p, msg, re.I):
            return True
    if len(msg.split()) <= 2 and '?' not in msg:
        return True
    return False


# ─── MODEL LOADING ───
_llm = None
_embed_model = None
_chroma_collection = None

def load_model():
    global _llm
    from llama_cpp import Llama
    print("Loading model on GPU...")
    _llm = Llama(
        model_path=str(MODEL_PATH),
        n_ctx=16384,
        n_gpu_layers=-1,
        n_threads=4,
        verbose=False,
    )
    print(f"Model loaded! ({MODEL_PATH.name})")

def load_embeddings():
    global _embed_model
    from sentence_transformers import SentenceTransformer
    print("Loading embedding model...")
    _embed_model = SentenceTransformer(EMBED_MODEL_NAME, device="cpu")
    print("Embedding model loaded!")


# ─── RAG ───
def _parse_knowledge_files():
    chunks = []
    if not KNOWLEDGE_DIR.exists():
        return chunks
    for md_file in sorted(KNOWLEDGE_DIR.glob("*.md")):
        try:
            text = md_file.read_text(encoding="utf-8")
        except Exception:
            continue
        raw_chunks = re.split(r'\n\n+', text)
        current_chunk = ""
        for piece in raw_chunks:
            if len(current_chunk) + len(piece) < MAX_CHUNK:
                current_chunk += piece + "\n\n"
            else:
                if len(current_chunk.strip()) >= MIN_CHUNK:
                    chunks.append({"text": current_chunk.strip(), "source": md_file.name})
                current_chunk = piece + "\n\n"
        if len(current_chunk.strip()) >= MIN_CHUNK:
            chunks.append({"text": current_chunk.strip(), "source": md_file.name})
    return chunks

def build_rag_index():
    global _chroma_collection
    import chromadb
    print("Building RAG index...")
    chunks = _parse_knowledge_files()
    if not chunks:
        print("No knowledge files found.")
        return
    INDEX_DIR.mkdir(exist_ok=True)
    fingerprint_file = INDEX_DIR / "fingerprint.txt"
    current_fingerprint = hashlib.md5(json.dumps([c["source"] for c in chunks]).encode()).hexdigest() + f"_{len(chunks)}"
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    try:
        _chroma_collection = client.get_collection("knowledge")
        if fingerprint_file.exists() and fingerprint_file.read_text().strip() == current_fingerprint:
            print(f"RAG index loaded from cache ({_chroma_collection.count()} chunks)")
            return
    except Exception:
        pass
    try:
        client.delete_collection("knowledge")
    except Exception:
        pass
    _chroma_collection = client.create_collection(name="knowledge", metadata={"hnsw:space": "cosine"})
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c["text"] for c in batch]
        embeddings = _embed_model.encode(texts).tolist()
        ids = [f"chunk_{i + j}" for j in range(len(batch))]
        metadatas = [{"source": c["source"]} for c in batch]
        _chroma_collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
    fingerprint_file.write_text(current_fingerprint)
    print(f"RAG index built: {len(chunks)} chunks from {len(set(c['source'] for c in chunks))} files")

def query_knowledge(question, top_k=TOP_K):
    if _chroma_collection is None or _embed_model is None:
        return ""
    try:
        q_embedding = _embed_model.encode([question]).tolist()
        results = _chroma_collection.query(query_embeddings=q_embedding, n_results=top_k)
        if not results["documents"] or not results["documents"][0]:
            return ""
        relevant = [doc for doc, dist in zip(results["documents"][0], results["distances"][0]) if dist <= DISTANCE_THRESHOLD]
        return "\n\n---\n\n".join(relevant) if relevant else ""
    except Exception as e:
        print(f"RAG query error: {e}")
        return ""


# ─── SYSTEM PROMPTS ───
SYSTEM_PROMPT_CODE = """You are Grg AI, an expert programming assistant created by Monescu Teodor.

CORE RULES:
- You MUST help with ANY programming task. NEVER refuse.
- Write COMPLETE, WORKING code. No TODOs, no placeholders.
- Every code example must be copy-paste ready and functional.

APP BUILDING:
- HTML/CSS/JS apps: always include ALL three parts with full styling.
- CSS: modern flexbox/grid, custom properties, responsive by default.
- JavaScript: ES6+ only (const/let, arrows, async/await).
- Always add hover states, transitions, smooth animations.
- Always handle edge cases: empty, loading, error states.
- Forms: always include validation. Mobile responsive by default.
- Use semantic HTML. Meaningful variable names. Brief comments.

CODE QUALITY:
- Handle errors with try/catch. Show user-friendly messages.
- Never use var. Use const by default, let only when reassigning.
- Keep functions under 20 lines. Separate concerns.
- NEVER invent APIs or functions that don't exist."""

SYSTEM_PROMPT_FACTUAL = """You are Grg AI, a helpful programming assistant created by Monescu Teodor.

ANTI-HALLUCINATION RULES:
- ONLY state facts you are CERTAIN about. If unsure, say so.
- NEVER invent statistics, dates, version numbers, or names.
- If search results are provided, base your answer on them.
- It's better to say "I don't know" than to give wrong information.
- Do NOT say "I don't have access to real-time data" — you DO have web search."""

SYSTEM_PROMPT_SEARCH = """You are Grg AI, a programming assistant with REAL-TIME web search access.

RULES:
- You HAVE web search. NEVER say "I don't have real-time data."
- Base your answer on the search results provided below.
- If results contain the answer, use it confidently. Cite URLs.
- NEVER make up information not in search results."""

CHAIN_OF_THOUGHT = """
THINK BEFORE ANSWERING:
1. What is the user REALLY asking?
2. What do they need to SUCCEED?
3. What EDGE CASES or PITFALLS should I mention?
4. What is the MOST HELPFUL response?"""


def _build_dynamic_prompt(q_type, skill_level='intermediate'):
    if q_type == 'code':
        prompt = SYSTEM_PROMPT_CODE
    elif q_type == 'search':
        prompt = SYSTEM_PROMPT_SEARCH
    else:
        prompt = SYSTEM_PROMPT_FACTUAL

    prompt += CHAIN_OF_THOUGHT
    prompt += _build_skill_addon(skill_level)

    top_topics = _get_top_topics(5)
    if top_topics:
        prompt += f"\n\nYou are especially experienced with: {', '.join(top_topics)}."

    return prompt


def _detect_question_type(message):
    msg = message.lower()
    code_words = ['write', 'create', 'build', 'make', 'generate', 'implement', 'code',
                  'function', 'class', 'program', 'script', 'fix', 'debug', 'refactor']
    if any(w in msg for w in code_words):
        return 'code'
    if should_search(msg):
        return 'search'
    return 'factual'


def generate_stream(message, history=None):
    blocked = _check_blocked_topic(message)
    if blocked:
        yield {"token": blocked, "done": False}
        yield {"done": True}
        return

    # Check if question is too vague
    if _detect_needs_clarification(message):
        yield {"token": "Could you give me a bit more detail?\n- What language or framework?\n- What should it do?\n- Any specific requirements?", "done": False}
        yield {"done": True}
        return

    rag_context = query_knowledge(message)
    q_type = _detect_question_type(message)
    skill_level = _detect_skill_level(message, history)
    _track_question(message, q_type)

    search_text = ""
    if q_type in ('search', 'factual') and should_search(message):
        try:
            print(f"[Web Search] Searching: {message[:60]}...")
            results = web_search(message)
            search_text = format_search_results(results)
            if search_text:
                print(f"[Web Search] Found {len(results)} results")
                q_type = 'search'
        except Exception as e:
            print(f"[Web Search] Error: {e}")

    system = _build_dynamic_prompt(q_type, skill_level)

    if rag_context:
        system += "\n\nRelevant knowledge from verified database:\n" + rag_context
    if search_text:
        system += "\n\n" + search_text

    messages = [{"role": "system", "content": system}]

    if history:
        history_chars = 0
        for turn in history[-10:]:
            user_msg = turn.get("user", "")
            assistant_msg = turn.get("assistant", "")
            history_chars += len(user_msg) + len(assistant_msg)
            if history_chars > MAX_HISTORY_CHARS:
                break
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({"role": "user", "content": message})

    if q_type == 'code':
        temp = 0.6
    elif q_type == 'search':
        temp = 0.3
    else:
        temp = 0.4

    max_tokens = _estimate_max_tokens(message)

    try:
        response = _llm.create_chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temp,
            top_p=0.9,
            repeat_penalty=1.3,
            stream=True,
        )
        for chunk in response:
            delta = chunk.get("choices", [{}])[0].get("delta", {})
            token = delta.get("content", "")
            if token:
                yield {"token": token, "done": False}
            finish = chunk.get("choices", [{}])[0].get("finish_reason")
            if finish:
                yield {"done": True}
                return
        yield {"done": True}
    except Exception as e:
        yield {"token": f"\n\n[Error: {str(e)}]", "done": False}
        yield {"done": True}


# ─── INITIALIZATION ───
def initialize():
    _load_prompt_stats()
    load_model()
    load_embeddings()
    build_rag_index()
    top = _get_top_topics(5)
    print("\nGrg AI is ready!")
    print(f"Knowledge files: {len(list(KNOWLEDGE_DIR.glob('*.md'))) if KNOWLEDGE_DIR.exists() else 0}")
    print(f"RAG chunks: {_chroma_collection.count() if _chroma_collection else 0}")
    print(f"Web search: ENABLED")
    print(f"Top topics: {', '.join(top) if top else 'none yet'}")