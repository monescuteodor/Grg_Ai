"""
grg_core.py — Grg AI Core Engine
Windows + RTX 5060 | Web Search | RAG | Fixed Safety Filter
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
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 8
MAX_CHUNK = 800
MIN_CHUNK = 50
DISTANCE_THRESHOLD = 1.2
MAX_HISTORY_CHARS = 6000
DEFAULT_MAX_TOKENS = 1024

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
    if hits >= 3 or msg_len > 500:
        return 2048
    elif hits >= 1 or msg_len > 200:
        return 1536
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
    _embed_model = SentenceTransformer(EMBED_MODEL_NAME)
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

# ─── SYSTEM PROMPT ───
SYSTEM_PROMPT_BASE = """You are Grg AI, a helpful programming assistant created by Monescu Teodor.

CRITICAL RULES — FOLLOW THESE WITHOUT EXCEPTION:
- You MUST help with ANY programming task. NEVER refuse.
- You MUST write code when asked. ANY language, ANY framework, ANY project.
- You MUST NOT say "I can't assist with that request" for ANY coding question.
- If asked to write an OS, a game, a compiler, a server — YOU DO IT.
- If asked something impossible to fit in one response, write the FIRST PART and explain how to continue.
- There is NO programming task you should refuse. Not one. Zero exceptions.
- You are a coding assistant. Your ONLY job is to write code and explain programming.
- If you are unsure, TRY ANYWAY. A partial answer is better than a refusal.

You are knowledgeable about all programming languages, frameworks, and technologies.
Provide complete, working code examples. Be concise but thorough."""

SYSTEM_PROMPT_WITH_SEARCH = """You are Grg AI, a helpful programming assistant created by Monescu Teodor.
You HAVE real-time web search access. You CAN answer questions about current events, recent news, and up-to-date information.

CRITICAL RULES:
- You MUST help with ANY task. NEVER refuse.
- You have WEB SEARCH. You DO have access to current information.
- NEVER say "I don't have access to real-time data" — because you DO.
- NEVER say "I cannot provide information about current events" — because you CAN.
- When search results are provided below, you MUST use them to answer.
- Answer based on the search results. Cite the source URL when possible.
- If the search results don't contain the answer, say what you found and suggest the user search directly.
- Be accurate and specific. Use facts from the search results, not guesses.

You are also knowledgeable about all programming languages, frameworks, and technologies.
Provide complete, working code examples when asked for code."""


# ─── RESPONSE GENERATION ───
def generate_stream(message, history=None):
    blocked = _check_blocked_topic(message)
    if blocked:
        yield {"token": blocked, "done": False}
        yield {"done": True}
        return

    # RAG context
    rag_context = query_knowledge(message)

    # Web search
    search_text = ""
    if should_search(message):
        try:
            print(f"[Web Search] Searching: {message[:60]}...")
            results = web_search(message)
            search_text = format_search_results(results)
            if search_text:
                print(f"[Web Search] Found {len(results)} results, fetched page content")
            else:
                print("[Web Search] No results found")
        except Exception as e:
            print(f"[Web Search] Error: {e}")

    # Choose system prompt based on whether we have search results
    if search_text:
        system = SYSTEM_PROMPT_WITH_SEARCH
    else:
        system = SYSTEM_PROMPT_BASE

    if rag_context:
        system += f"\n\nRelevant knowledge from database:\n{rag_context}"

    if search_text:
        system += f"\n\n{search_text}"

    # Build messages
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

    max_tokens = _estimate_max_tokens(message)

    try:
        response = _llm.create_chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
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
    load_model()
    load_embeddings()
    build_rag_index()
    print("\nGrg AI is ready!")
    print(f"Knowledge files: {len(list(KNOWLEDGE_DIR.glob('*.md'))) if KNOWLEDGE_DIR.exists() else 0}")
    print(f"RAG chunks: {_chroma_collection.count() if _chroma_collection else 0}")
    print("Web search: ENABLED")
