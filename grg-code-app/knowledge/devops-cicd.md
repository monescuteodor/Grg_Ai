# DevOps, CI/CD & deployment

## Docker
```dockerfile
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./ ; RUN npm ci
COPY . . ; RUN npm run build
FROM node:22-alpine
WORKDIR /app ; COPY --from=build /app/dist ./dist ; COPY package*.json ./
RUN npm ci --omit=dev ; CMD ["node","dist/index.js"]
```
- Multi-stage builds keep images small. `.dockerignore` node_modules/.git. Pin base image versions.

## GitHub Actions CI
```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npm run lint && npm test && npm run build
```

## Deploy targets
- **Web frontends**: Vercel / Netlify / Cloudflare Pages.
- **APIs/containers**: Fly.io, Railway, Render, or a VPS (Docker + Caddy/Nginx + systemd).
- **Static**: any CDN / object storage.

## Ops rules
- Secrets in the platform's secret store / `.env` (never committed). Provide `.env.example`.
- Health checks, structured logs, error tracking (Sentry). Zero-downtime deploys.
- Roll forward with small PRs; keep a rollback path.
