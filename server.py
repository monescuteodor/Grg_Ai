"""
server.py — Grg AI Web Server
FastAPI + SSE streaming + search status events
"""

import json
import asyncio
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

import grg_core
from grg_web_search import should_search

app = FastAPI(title="Grg AI")
STATIC_DIR = Path(__file__).parent / "static"

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

@app.post("/api/chat")
async def chat(request: Request):
    try:
        body = await request.json()
    except Exception:
        return {"error": "Invalid JSON"}

    message = body.get("message", "").strip()
    history = body.get("history", [])

    if not message:
        return {"error": "Empty message"}

    async def event_stream():
        try:
            # Send status: searching
            if should_search(message):
                status = json.dumps({"status": "searching"})
                yield f"data: {status}\n\n"
                await asyncio.sleep(0)

            for chunk in grg_core.generate_stream(message, history):
                # Send status: thinking on first token
                if "token" in chunk and not hasattr(event_stream, '_started'):
                    event_stream._started = True
                    status = json.dumps({"status": "generating"})
                    yield f"data: {status}\n\n"

                data = json.dumps(chunk, ensure_ascii=False)
                yield f"data: {data}\n\n"
                await asyncio.sleep(0)
        except Exception as e:
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

@app.on_event("startup")
async def startup():
    print("\n" + "=" * 50)
    print("   GRG AI — Starting up...")
    print("=" * 50 + "\n")
    grg_core.initialize()
    print("\n" + "=" * 50)
    print("   GRG AI — Ready at http://localhost:8000")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
