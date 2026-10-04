# React + Vite + TypeScript — best practices

## Setup
- Scaffold: `npm create vite@latest my-app -- --template react-ts`, then `npm i`.
- Dev: `npm run dev` (HMR). Build: `npm run build` → `dist/`. Preview: `npm run preview`.
- Add path alias in `vite.config.ts` (`resolve.alias { '@': '/src' }`) and `tsconfig` `paths`.

## Structure
```
src/
  main.tsx        # createRoot + <App/>
  App.tsx
  components/     # PascalCase.tsx, one component per file
  hooks/          # useXxx.ts
  lib/            # api.ts, utils.ts
  pages/          # if using a router
  types/          # shared TS types
```

## Component rules
- Function components + hooks only (no classes). Type props with an explicit `type Props = {...}`.
- Keep components small and pure; lift state up only when shared. Derive state instead of duplicating it.
- `useEffect` is for synchronizing with external systems, NOT for computing derived data — compute inline or with `useMemo`.
- Stable keys in lists (an id, never the array index for dynamic lists).
- Memoize expensive work with `useMemo`, callbacks passed to memo children with `useCallback`. Don't over-memoize.

## Data fetching
- Use **TanStack Query** (`@tanstack/react-query`) for server state: caching, retries, loading/error out of the box. Avoid manual `useEffect` fetch + `useState` for anything non-trivial.
- Keep a typed `api.ts` (fetch wrapper) returning parsed JSON; throw on `!res.ok`.

## Routing
- **React Router** (`react-router-dom` v6+): `createBrowserRouter` with route objects, `<Outlet/>`, loaders/actions for data.

## Quality
- ESLint + Prettier. `tsc --noEmit` in CI. Strict mode on in `tsconfig`.
- Env vars via `import.meta.env.VITE_*` (only `VITE_`-prefixed are exposed).
