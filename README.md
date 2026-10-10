# Grg AI

> A privacy-first AI assistant and developer platform — free to start, with specialist agents, client-side data redaction, and a desktop coding agent.

**Live:** https://grg-ai.com  ·  **Desktop app:** GrgCode (Windows)  ·  **Author:** Monescu Teodor

Grg AI is a web chat assistant (grg-ai.com) plus **GrgCode**, an Electron desktop coding agent. It routes your question to the best available model (Claude, GPT-5, Gemini, or free Grg models), can build apps/sites/documents/images, help with hardware and robotics, and run a library of **specialist agents** with optional **client-side PII redaction**.

---

## Table of contents

- [1. What's in this repository](#1-whats-in-this-repository)
- [2. Architecture](#2-architecture)
- [3. AutoGrg — the smart router](#3-autogrg--the-smart-router)
- [4. Models](#4-models)
- [5. Credits and plans (two-bucket, margin-safe)](#5-credits-and-plans-two-bucket-margin-safe)
- [6. GrgAgent — specialist agents and privacy](#6-grgagent--specialist-agents-and-privacy)
- [7. Chat features](#7-chat-features)
- [8. Share and Publish](#8-share-and-publish)
- [9. Knowledge base and real images](#9-knowledge-base-and-real-images)
- [10. Authentication](#10-authentication)
- [11. SEO](#11-seo)
- [12. Security and privacy](#12-security-and-privacy)
- [13. HTTP API](#13-http-api)
- [14. GrgCode desktop app](#14-grgcode-desktop-app)
- [15. Running and deploying](#15-running-and-deploying)
- [16. Status and roadmap](#16-status-and-roadmap)

---

## 1. What's in this repository

```
Grg_Ai/
├── grgai/                  » the web app (FastAPI backend + single-page frontend)
│   ├── server.py           » API: chat, agent, images, docs, share/publish, SEO
│   ├── billing.py          » credits, two-bucket economics, per-message pricing
│   ├── stripe_handler.py   » Stripe checkout + webhooks + daily limits
│   ├── nhash_handler.py    » crypto (nHash) payment verification
│   ├── docgen.py           » .pptx / .xlsx / .docx generation
│   ├── static/             » index.html (the whole SPA), privacy/terms/share pages
│   ├── knowledge/          » 35 skill docs the backend injects on demand
│   └── .env.example        » required environment variables (no real secrets)
├── grg-code-app/           » GrgCode — the Electron desktop coding agent
│   ├── main.js             » Electron main + agent loop + tools + MCP client
│   ├── preload.js, renderer/
│   ├── knowledge/, templates/
│   └── package.json        » electron-builder config (single portable .exe)
└── (root)                  » the original early version is kept for history
```

Secrets are never committed. All keys come from the environment — see `grgai/.env.example`.

---

## 2. Architecture

```
  Browser / GrgCode
        │ HTTPS (TLS 1.3, Cloudflare tunnel)
        ▼
  grg-ai.com  ──►  Raspberry Pi 4  ──►  FastAPI (uvicorn, systemd: grgai.service)
                                         │  reads keys from /home/pi/GrgAI/.env
                                         ├─► Groq            (free models, tool-calling)
                                         ├─► OpenRouter      (premium: Claude/GPT-5/Gemini)
                                         └─► Firebase        (auth + Firestore: users, billing)
```

- **Host:** a single Raspberry Pi 4 on the author's LAN, exposed publicly through a Cloudflare tunnel (TLS terminates at Cloudflare).
- **Backend:** FastAPI + uvicorn, one process, managed by systemd. The frontend is one static `index.html` (inline CSS/JS) served at `/`.
- **Auth and data:** Firebase Authentication (email/password + Google) and Firestore (user profiles, consent, credits, usage).
- **Model providers:** Groq for free models (only Groq free models support tool-calling); OpenRouter for premium models (Claude, GPT-5, Gemini, etc.). Keys stay server-side; the browser never sees them.

---

## 3. AutoGrg — the smart router

`AutoGrg` is the default model. On each message the backend:

1. **Classifies** the task with regular expressions into one of: `hardware`, `app_build`, `code`, `research`, `general`.
2. **Checks availability** (`/api/models/status`): which Groq models are live and whether OpenRouter has credit.
3. **Routes** to the best model the user can afford:
   - **Funded** (GrgPro/GrgUltra or wallet credits + OpenRouter has credit) → a flagship premium model. It runs at **maximum capability**: Claude Opus 4.8 for general/app/hardware/research, GPT-5.1 Codex for code, with a large token budget and a "be thorough, use clean Markdown" directive.
   - **Free** → the strongest free Groq model (`gpt-oss-120b`), with a lighter "clean Markdown, be efficient" directive.
4. **Injects expertise**: a task brief plus, when relevant, a single best-matching knowledge document (see section 9). For hardware/research it also runs a live web search (DuckDuckGo, no key) and cites the results.

---

## 4. Models

The picker is intentionally curated to the recognizable brands; every other model stays defined and routable inside the AutoGrg pool.

- **Free (Grg house / Groq):** AutoGrg, Grg Code, Grg Fast, Grg Image.
- **Premium (OpenRouter, need credits):** Claude Opus 4.8, Claude Sonnet 5, Claude Fable, GPT-5.6, GPT-5.5, GPT-5.1 Codex, GPT-4o, Gemini 3 Pro, Gemini 2.5 Pro, Gemini 3 Image.

Premium models only run when OpenRouter has credit AND the user has a paid plan or wallet credits.

---

## 5. Credits and plans (two-bucket, margin-safe)

Usage is charged **per message**, by how heavy the model is and how hard it works (effort) — not per word. **Every message costs credits, including free models**, so usage is always metered. There are two separate buckets so margin is guaranteed:

- **Free bucket** — pays for FREE models (these cost the platform almost nothing, but still consume credits). Refills on a cycle:
  - **GrgFree:** 100 credits / week
  - **GrgPro:** 500 credits / day
  - **GrgUltra:** 2000 credits / day
- **Premium bucket** — a MONTHLY budget sized to the plan's price, pays for PREMIUM models only:
  - **GrgPro (EUR 5 / mo):** 500 premium credits / month
  - **GrgUltra (EUR 20 / mo):** 2000 premium credits / month

Each premium message costs `real_API_cost x MARKUP` credits (a flat amount per model x effort, derived from an assumed message size), so spending the whole bucket can never cost more real API than the plan paid for. Example: a GrgUltra user burning everything on the most expensive model stays profitable for the operator.

- **1 credit = EUR 0.01** for display; euros are never shown as a balance.
- **Effort multipliers:** Low x1, Mid x1.5, High x2, Ultra x3.
- **Plans:** GrgFree (EUR 0), GrgPro (EUR 5/mo or EUR 50/yr), GrgUltra (EUR 20/mo or EUR 200/yr).
- **Payments:** Stripe (card) and nHash (crypto). All economics constants live at the top of `billing.py` and are easy to tune.

> Note: payments are currently in Stripe test mode and OpenRouter is unfunded, so no real money moves yet. The system is wired and margin-safe for when it goes live.

---

## 6. GrgAgent — specialist agents and privacy

Grg AI stays a normal chatbot, but you can pick a **specialist agent** from a large list, each with its own expertise and style.

### Built-in agents (26, by category)

- **Legal:** Litigation Lawyer, Contracts Lawyer, GDPR / Privacy Auditor, Employment Lawyer, IP Lawyer
- **Development:** Senior Architect, React / Node, Python / Data, DevOps / Cloud, Mobile, Database Architect, Code Reviewer, Embedded / IoT
- **Security:** Security / Pentest, Compliance (ISO / SOC 2)
- **Business:** Business Analyst, Marketing Strategist, Financial Analyst, Startup Advisor
- **Writing:** Technical Writer, Copywriter, Academic Editor
- **Data & AI:** ML / AI Engineer, Data Scientist
- **Other:** Research Assistant, Translator / Localizer

### Custom agents

The picker has a **"+ Create your own agent"** option. You set a name, category, short description, system prompt, and an optional privacy flag. Custom agents are saved per device (browser localStorage), appear in a **"Your Agents"** section, and can be edited or deleted.

### Privacy mode (agents marked PRIVATE)

When a PRIVATE agent is active, the frontend runs a **client-side PII redaction pipeline** before anything leaves your device:

1. **Redact** — emails, phone numbers, national IDs (CNP), IBANs, card numbers, and API secrets are replaced with typed placeholders like `[EMAIL_1]`, `[IBAN_1]`, `[SECRET_1]`.
2. **Send** — only the redacted text (plus history) reaches the model. The substitution map lives **only in memory**, never saved or sent.
3. **Restore** — the model keeps the placeholders in its reply, and the interface substitutes your real values back locally.
4. **Zero-persistence** — PRIVATE agent sessions are ephemeral: nothing is written to storage and no auto-title request is made.

> Limitation: person names are not redacted yet (reliable name detection needs a dedicated NER model). All structured PII above is covered.

---

## 7. Chat features

- **Markdown rendering** — a proper block parser: headings, ordered/unordered lists, GFM tables, blockquotes, paragraphs, bold/italic, links, inline code, and fenced code blocks with Run / Copy / open-in-panel.
- **Advanced preview** — runs HTML/CSS/JS and transpiles React/JSX in a sandboxed iframe, with a desktop/tablet/mobile device toggle and an in-frame console.
- **Image generation** — `Grg Image` and premium image models.
- **Document generation** — the model can emit a spec that becomes a downloadable `.pptx`, `.xlsx`, or `.docx`.
- **Per-message actions** — copy, edit-and-resend, regenerate, read aloud, and Continue (if a reply was cut off by the token cap).
- **History** — search, rename, pin, delete, export to Markdown / PDF / Excel.
- **Private session** — a zero-persistence mode where nothing is saved.
- **Mobile** — iPhone-safe layout: notch safe-area, keyboard handling (the composer lifts above the keyboard), responsive composer.

---

## 8. Share and Publish

- **Share a conversation** — `POST /api/share` stores a read-only snapshot and returns a public link `grg-ai.com/s/<id>` with a self-contained viewer.
- **Publish a generated page** — `POST /api/publish` hosts the HTML from the preview at `grg-ai.com/p/<id>`. It is served with a `Content-Security-Policy: sandbox` header, so the page runs in an **opaque origin**: it can run its own scripts and CDNs but cannot read grg-ai.com cookies or localStorage. Safe multi-tenant hosting.

---

## 9. Knowledge base and real images

- **Knowledge / skills** — `grgai/knowledge/*.md` holds 35 in-depth docs (web, mobile, desktop, backend, databases, auth, testing, DevOps, games, Arduino, ESP32, microcontrollers, robotics, PID, kinematics/IK, ROS 2, computer vision, and more). On each chat the backend matches the question and injects the single best doc, so answers have real depth without blowing the token budget.
- **Real images** — a keyless image search (Openverse, then Wikimedia Commons, then Picsum) powers `GET /img?q=...&w=&h=`, which 302-redirects to a real photo. Models embed `<img src="https://grg-ai.com/img?q=...">` so generated pages show genuine images, not placeholders.

---

## 10. Authentication

- **Email + password** — on sign-up, a Firebase verification email is sent automatically; the interface reminds unverified users at sign-in.
- **Continue with Google** — Google sign-in/up via Firebase (`signInWithPopup`). For Google to work in production the domain must be listed under Firebase Authentication » Settings » Authorized domains.
- **Client-side encryption key** — a per-device key is derived at sign-in and used to encrypt local chat history.

---

## 11. SEO

- Keyword-rich `<title>` and meta description, Open Graph and Twitter cards, and JSON-LD `WebApplication` structured data.
- A `<noscript>` fallback for crawlers that do not run JavaScript.
- `GET /robots.txt` (allows indexing, points to the sitemap) and `GET /sitemap.xml`.

---

## 12. Security and privacy

- **In transit:** TLS 1.3 via Cloudflare.
- **Secrets:** API keys (Groq, OpenRouter, Stripe) live only in the server `.env`; they are never sent to the browser and never committed. See `grgai/.env.example`.
- **Firebase web API key:** present in the frontend by design — it is a public identifier, not a secret; data access is controlled by Firestore Security Rules and authorized domains.
- **Rate limiting:** a per-IP sliding window on the expensive endpoints protects the scarce free-tier tokens and the server.
- **Billing/data separation:** usage metering records token/credit counts and model id, not prompt or response content.
- **Published pages** are sandboxed to an opaque origin (see section 8).

---

## 13. HTTP API

Selected endpoints (all under `https://grg-ai.com`):

| Method | Path | Purpose |
| :-- | :-- | :-- |
| POST | `/api/chat` | Streaming chat (SSE); AutoGrg routing, per-message credit charge |
| POST | `/api/agent` · `/api/agent/stream` | The desktop agent's brain (tool-calling, SSE) |
| GET  | `/api/models/status` | Which models are live right now |
| GET  | `/api/account?uid=` | Credits, plan, usage snapshot |
| POST | `/api/create-checkout` | Stripe checkout for GrgPro / GrgUltra |
| POST | `/api/create-topup` · `/api/topup-confirm` | Wallet top-ups |
| POST | `/api/webhook` | Stripe webhook (activates plans, credits top-ups) |
| GET  | `/api/images/search` · `/img` | Real-photo search and redirect |
| GET  | `/api/web/search` | Keyless web search (DuckDuckGo) |
| POST | `/api/doc/generate` | Render a spec into .pptx / .xlsx / .docx |
| POST | `/api/share` · GET `/s/{id}` | Share a conversation (read-only) |
| POST | `/api/publish` · GET `/p/{id}` | Publish a generated page (sandboxed) |
| GET  | `/robots.txt` · `/sitemap.xml` | SEO |

---

## 14. GrgCode desktop app

`grg-code-app/` is an Electron desktop coding agent (like a local pair-programmer). It talks to the same backend and runs an agentic tool loop on your machine with per-action approval.

- **Tools:** list_dir, read_file (with line ranges), search, write_file, edit_file, apply_patch (multi-file), run_command, git, web_search, fetch_url, image_search, add_image, update_plan, task (sub-agents), scaffold, knowledge, remember, create_document, plus dynamic `mcp__*` tools.
- **MCP host:** reads `.grgcode/mcp.json` and spawns MCP servers over stdio, exposing their tools to the agent.
- **UI:** sessions grouped by folder, file explorer, Monaco editor, a persistent terminal, diff-on-approval, reasoning display, the advanced code preview, a Publish button, @-file mentions, and Checkpoints/Undo.
- **Packaging:** `electron-builder --win portable` produces a single portable `.exe` (no install) that bundles the knowledge and templates.

---

## 15. Running and deploying

### Backend (grgai/)

```bash
cd grgai
python -m venv venv && . venv/bin/activate      # Windows: venv\Scripts\activate
pip install fastapi uvicorn httpx stripe firebase-admin pillow python-pptx openpyxl python-docx
cp .env.example .env                             # then fill in your keys
python server.py                                 # serves on http://localhost:8000
```

Fill `.env` with: `GROQ_API_KEY`, `OPENROUTER_API_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRICE_ID*`, `FRONTEND_URL`.

On the production host the frontend is one static file: deploying the site is copying `static/index.html`. Deploying the backend is copying `server.py` and restarting the `grgai` service.

### Desktop app (grg-code-app/)

```bash
cd grg-code-app
npm install
npm start                 # run in dev
npm run dist              # build the single portable .exe (electron-builder)
```

---

## 16. Status and roadmap

**Live now:** chat with AutoGrg routing, curated models, two-bucket margin-safe credits (every message is metered, free models included), GrgFree/GrgPro/GrgUltra plans, 26 specialist agents + custom agents with client-side PII redaction, Share and Publish, document/image generation, the knowledge base, email + Google auth, SEO, and the GrgCode desktop app.

**Pending / future:**
- Fund OpenRouter and switch Stripe to live mode to actually earn (the economics are wired and margin-safe).
- Sync custom agents to the user account (Firestore) so they follow across devices.
- NER-based name redaction, OCR ingestion, fine-tuning, GraphRAG, per-tenant KMS and MicroVM isolation, and an agent marketplace — these belong to a cloud phase, not the single Raspberry Pi.

---

Built by Monescu Teodor. (C) 2026.
