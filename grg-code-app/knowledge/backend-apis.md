# Backend APIs (FastAPI / Express / Go)

## Pick
- **FastAPI** (Python) — fast to build, auto OpenAPI docs, great for AI/data.
- **Express/Fastify** (Node/TS) — ubiquitous, same language as frontend.
- **Go (net/http, chi)** — high performance, single static binary, great for services.

## FastAPI minimal
```python
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class Item(BaseModel): name: str; qty: int = 1
@app.post("/items")
def create(i: Item): return {"ok": True, "item": i}
# run: uvicorn main:app --reload
```

## Express minimal
```js
import express from 'express';
const app = express(); app.use(express.json());
app.post('/items', (req,res)=> res.json({ ok:true, item:req.body }));
app.listen(3000);
```

## Good API design
- REST: nouns + HTTP verbs; proper status codes (200/201/400/401/403/404/409/422/500).
- Validate all input (pydantic / zod). Never trust the client.
- Pagination (limit/offset or cursor), filtering, consistent error shape `{error, detail}`.
- Auth: JWT (stateless) or sessions; see `auth-and-payments`.
- CORS only for the origins you need. Rate-limit public endpoints.
- Version the API (`/v1`). Document with OpenAPI/Swagger.
- Async I/O for DB/network. Return early on errors.
