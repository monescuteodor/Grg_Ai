# Databases & ORMs

## Choose
- **Postgres** — default relational DB (robust, JSON, full-text). Managed: Supabase/Neon/RDS.
- **SQLite** — zero-config, file-based; perfect for desktop/mobile/embedded and small apps.
- **MySQL/MariaDB** — fine alternative to Postgres.
- **MongoDB** — document store when schema is truly fluid (usually Postgres+JSONB is enough).
- **Redis** — cache, queues, rate-limits, sessions.

## ORMs / query layers
- **Prisma** (TS) — great DX, migrations, type-safe. `prisma migrate dev`.
- **Drizzle** (TS) — SQL-first, lightweight, edge-friendly.
- **SQLAlchemy / SQLModel** (Python), **GORM** (Go).

## Prisma quickstart
```prisma
model User { id Int @id @default(autoincrement()); email String @unique; posts Post[] }
model Post { id Int @id @default(autoincrement()); title String; authorId Int; author User @relation(fields:[authorId], references:[id]) }
```
```bash
npx prisma migrate dev --name init
```

## Rules
- Always use migrations (never hand-edit prod schema). Commit migration files.
- Index columns you filter/join/sort on. Watch N+1 (use includes/joins).
- Parameterize queries (ORMs do this) — never string-concatenate SQL.
- Back up before destructive migrations. Use transactions for multi-write ops.
