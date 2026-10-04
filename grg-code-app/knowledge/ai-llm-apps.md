# AI / LLM apps

## Building blocks
- **Chat/completion** via provider APIs (OpenAI, Anthropic, Groq, OpenRouter). Stream tokens (SSE) for UX.
- **Tool/function calling** — give the model JSON-schema tools; execute them; feed results back in a loop (this is how agents work).
- **RAG** — embed docs -> vector DB (pgvector, Qdrant, Chroma) -> retrieve top-k -> stuff into the prompt with citations.
- **Structured output** — ask for JSON and validate (zod/pydantic); retry on parse failure.

## Streaming (SSE) sketch
```js
const res = await fetch(url,{method:'POST',body:JSON.stringify({stream:true, messages})});
const reader = res.body.getReader(); const dec = new TextDecoder();
for(;;){ const {done,value}=await reader.read(); if(done)break;
  for(const line of dec.decode(value).split('\n')){ if(line.startsWith('data:')){ /* parse token */ } } }
```

## Practices
- Keep API keys server-side; proxy from the backend (never in the client).
- Control cost: pick the smallest model that works, cap max_tokens, cache, and meter usage.
- Handle rate limits (429) with backoff; handle context limits (trim/summarize old turns).
- Guard against prompt injection when tools can act; validate tool args; confirm destructive actions.
- Evaluate: keep a set of test prompts and check outputs when you change prompts/models.
