# Next.js (App Router) — best practices

## Project setup
- Scaffold: `npx create-next-app@latest my-app --ts --tailwind --eslint --app --src-dir --import-alias "@/*"`.
- Use the **App Router** (`src/app/`), not the legacy `pages/` router.
- Node 18+; prefer `pnpm` or `npm`. Keep `package.json` scripts: `dev`, `build`, `start`, `lint`.

## Routing & files
- `app/layout.tsx` = root layout (html/body, fonts, providers). `app/page.tsx` = home route.
- Folder = route segment. `app/blog/[slug]/page.tsx` for dynamic routes; `loading.tsx`, `error.tsx`, `not-found.tsx` per segment.
- Route groups `(marketing)` don't affect the URL. Private folders `_lib` are not routed.
- API routes: `app/api/<name>/route.ts` exporting `GET`/`POST` async handlers returning `Response`/`NextResponse.json()`.

## Server vs Client components
- Components are **Server Components by default** — no `useState`/`useEffect`/browser APIs, but can `await` data and read secrets.
- Add `"use client"` only for interactivity (state, effects, event handlers, browser APIs). Keep client components small; push them to the leaves.
- Fetch data in Server Components with `async/await`; Next dedupes and caches `fetch`. Use `{ cache: 'no-store' }` for dynamic, `{ next: { revalidate: 60 } }` for ISR.
- Never import server-only secrets into client components. Use `server-only` package to guard.

## Data & mutations
- Prefer **Server Actions** (`"use server"`) for mutations from forms; progressive-enhancement friendly.
- Revalidate with `revalidatePath('/x')` / `revalidateTag('tag')` after a mutation.
- Metadata: export `const metadata` or `generateMetadata()` per route for SEO.

## Structure
```
src/
  app/            # routes, layouts
  components/     # reusable UI (ui/ for primitives)
  lib/            # helpers, db client, utils.ts
  hooks/          # client hooks
```
- `@/*` import alias → `src/*`.

## Gotchas
- Environment: `NEXT_PUBLIC_*` is exposed to the browser; everything else is server-only.
- Images: use `next/image`. Fonts: `next/font`. Links: `next/link`.
- Don't fetch in `useEffect` when a Server Component can fetch it directly.
