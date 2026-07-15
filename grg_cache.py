"""
grg_cache.py — Response Cache for Grg AI
Caches question->answer pairs. Similar questions return cached answers instantly.
"""

import os
import json
import time
import hashlib

CACHE_FILE = "grg_response_cache.json"
MAX_CACHE_SIZE = 5000
CACHE_TTL_DAYS = 30


class ResponseCache:
    def __init__(self, cache_dir="."):
        self.cache_path = os.path.join(cache_dir, CACHE_FILE)
        self.cache = self._load()
        self.stats = {"hits": 0, "misses": 0}

    def _load(self):
        if not os.path.exists(self.cache_path):
            return {"exact": {}, "entries": []}
        try:
            with open(self.cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            now = time.time()
            cutoff = now - (CACHE_TTL_DAYS * 86400)
            data["entries"] = [e for e in data.get("entries", []) if e.get("timestamp", 0) > cutoff]
            return data
        except Exception:
            return {"exact": {}, "entries": []}

    def _save(self):
        if len(self.cache["entries"]) > MAX_CACHE_SIZE:
            self.cache["entries"].sort(key=lambda e: e.get("timestamp", 0), reverse=True)
            self.cache["entries"] = self.cache["entries"][:MAX_CACHE_SIZE]
            self.cache["exact"] = {e["hash"]: i for i, e in enumerate(self.cache["entries"])}
        try:
            with open(self.cache_path, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False)
        except Exception:
            pass

    @staticmethod
    def _hash(question):
        normalized = " ".join(question.lower().strip().split())
        return hashlib.md5(normalized.encode()).hexdigest()

    def lookup(self, question):
        q_hash = self._hash(question)
        if q_hash in self.cache.get("exact", {}):
            idx = self.cache["exact"][q_hash]
            if idx < len(self.cache["entries"]):
                entry = self.cache["entries"][idx]
                entry["hits"] = entry.get("hits", 0) + 1
                self.stats["hits"] += 1
                return entry["answer"]
        self.stats["misses"] += 1
        return None

    def save(self, question, answer):
        if not answer or len(answer.strip()) < 10:
            return
        q_hash = self._hash(question)
        if q_hash in self.cache.get("exact", {}):
            return
        entry = {
            "question": question,
            "answer": answer,
            "hash": q_hash,
            "timestamp": time.time(),
            "hits": 0,
        }
        idx = len(self.cache["entries"])
        self.cache["entries"].append(entry)
        if "exact" not in self.cache:
            self.cache["exact"] = {}
        self.cache["exact"][q_hash] = idx
        self._save()

    def get_stats(self):
        total = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total * 100) if total > 0 else 0
        return {
            "total_cached": len(self.cache["entries"]),
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "hit_rate": f"{hit_rate:.1f}%",
        }

    def get_all_entries(self):
        return self.cache.get("entries", [])

    def clear(self):
        self.cache = {"exact": {}, "entries": []}
        self._save()
