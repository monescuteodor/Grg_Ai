# Supabase & Prisma — database best practices

## Supabase
- Hosted Postgres + Auth + Storage + Realtime. Create a project; grab `SUPABASE_URL` and keys.
- Two keys: **anon** (public, browser-safe, gated by RLS) and **service_role** (server-only, bypasses RLS — NEVER ship to the client).
- Client: `createClient(url, anonKey)` in the browser; use the service key only in server code / edge functions.
- **Always enable Row Level Security (RLS)** on every table and write explicit policies (e.g. `auth.uid() = user_id`). Without RLS the anon key can read everything.
- Auth: `supabase.auth.signInWithOtp / signInWithPassword / signInWithOAuth`. Read the session; guard server routes by verifying the JWT.
- Prefer database access through RLS + the anon key from the client for simple apps; use the service key server-side for admin tasks.

## Prisma
- Install: `npm i -D prisma`, `npm i @prisma/client`. Init: `npx prisma init` (creates `schema.prisma` + `.env` with `DATABASE_URL`).
- Define models in `schema.prisma`; run `npx prisma migrate dev --name init` in dev, `prisma migrate deploy` in prod. `npx prisma generate` after schema changes.
- Single client instance (avoid exhausting connections in dev/serverless):
```ts
// lib/db.ts
import { PrismaClient } from '@prisma/client';
const g = globalThis as unknown as { prisma?: PrismaClient };
export const db = g.prisma ?? new PrismaClient();
if (process.env.NODE_ENV !== 'production') g.prisma = db;
```
- Use `select`/`include` to fetch only needed fields. Avoid N+1 with `include` or batched queries. Wrap multi-write ops in `db.$transaction([...])`.
- With Supabase + serverless, use the **connection pooler** URL (`?pgbouncer=true`) for `DATABASE_URL` and the direct URL for migrations (`directUrl`).

## Secrets
- All DB URLs and service keys live in `.env` (server only), never in client bundles. Add `.env` to `.gitignore`.
