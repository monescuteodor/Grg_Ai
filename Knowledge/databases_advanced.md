# Databases Advanced Complete Reference


---

# CHAPTER 1: SQL FUNDAMENTALS (REFRESHER)


## Remarks

This reference focuses on **PostgreSQL** as the primary RDBMS — open source, ACID-compliant, used at scale by Instagram, Reddit, Discord, Stripe. Concepts transfer to MySQL, SQL Server, Oracle with minor syntax differences. Also covers query optimization, indexing strategies, transactions, replication, and operational concerns.

Key concepts: **ACID** (Atomicity, Consistency, Isolation, Durability), **Indexes** (B-tree, hash, GIN, BRIN), **Query planning** (EXPLAIN, statistics, joins), **Transactions** (isolation levels, locks, MVCC), **Normalization** (1NF-3NF) vs denormalization, **Constraints** (PK, FK, UNIQUE, CHECK), **Partitioning** (table split for size/performance).

Used at: every backend project. Knowing PostgreSQL deeply is one of the highest-leverage skills a backend developer can have.

Tools: **psql** (CLI), **pgAdmin** (GUI), **DBeaver** (cross-DB), **EXPLAIN ANALYZE** (query planning), **pg_stat_statements** (slow query log), **pgbench** (benchmarking).


## Core SELECT Patterns

```sql
-- Basic query
SELECT id, name, email FROM users WHERE active = true LIMIT 10;

-- Aggregations with GROUP BY
SELECT country, COUNT(*) as user_count, AVG(age) as avg_age
FROM users
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY country
HAVING COUNT(*) > 10           -- Filter on aggregation
ORDER BY user_count DESC;

-- DISTINCT vs GROUP BY (same result, GROUP BY more flexible)
SELECT DISTINCT country FROM users;
SELECT country FROM users GROUP BY country;

-- Subqueries
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 1000);

-- EXISTS (usually faster than IN for large sets)
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.total > 1000
);

-- LIMIT + OFFSET (pagination — has issues at scale, see CHAPTER 6)
SELECT * FROM products
ORDER BY created_at DESC
LIMIT 20 OFFSET 100;          -- Page 6 of 20-item pages

-- ORDER BY with multiple columns
SELECT * FROM employees
ORDER BY department ASC, salary DESC NULLS LAST;
```


## JOIN Types Demystified

```sql
-- INNER JOIN — only rows matching in both tables
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN — all from left, NULL where no match in right
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
-- Useful for: "users with NO orders"
SELECT u.* FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;

-- RIGHT JOIN — symmetric to LEFT (rarely used; just swap tables)

-- FULL OUTER JOIN — all rows from both, NULL where no match
SELECT u.name, o.total
FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id;

-- CROSS JOIN — Cartesian product (every row × every row)
SELECT a.name, b.name FROM categories a CROSS JOIN tags b;
-- Useful for generating combinations; can be expensive!

-- Self-join — table joined to itself
SELECT e1.name as employee, e2.name as manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.id;

-- Multiple joins
SELECT u.name, o.id, p.title
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE u.country = 'RO';
```


## CTEs (Common Table Expressions)

```sql
-- CTE: reusable, readable named subquery
WITH active_users AS (
    SELECT id, name FROM users WHERE last_login > NOW() - INTERVAL '7 days'
),
big_orders AS (
    SELECT user_id, SUM(total) as total
    FROM orders
    WHERE created_at > NOW() - INTERVAL '30 days'
    GROUP BY user_id
    HAVING SUM(total) > 1000
)
SELECT au.name, bo.total
FROM active_users au
JOIN big_orders bo ON au.id = bo.user_id;

-- Recursive CTE — hierarchies, graph traversal
WITH RECURSIVE employee_tree AS (
    -- Anchor: top-level (no manager)
    SELECT id, name, manager_id, 1 as level
    FROM employees WHERE manager_id IS NULL

    UNION ALL

    -- Recursive: each employee whose manager is in the tree
    SELECT e.id, e.name, e.manager_id, et.level + 1
    FROM employees e
    JOIN employee_tree et ON e.manager_id = et.id
)
SELECT * FROM employee_tree ORDER BY level, name;
```


## Window Functions

```sql
-- Running total per user
SELECT
    user_id,
    order_date,
    total,
    SUM(total) OVER (PARTITION BY user_id ORDER BY order_date) as running_total
FROM orders;

-- Rank within partition
SELECT
    department,
    name,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dense,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
FROM employees;
-- RANK: 1, 2, 2, 4 (skips on tie)
-- DENSE_RANK: 1, 2, 2, 3 (doesn't skip)
-- ROW_NUMBER: 1, 2, 3, 4 (always unique)

-- LAG/LEAD — access previous/next row
SELECT
    date,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY date) as prev_day,
    revenue - LAG(revenue, 1) OVER (ORDER BY date) as day_over_day
FROM daily_revenue;

-- Moving average
SELECT
    date,
    revenue,
    AVG(revenue) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as ma_7day
FROM daily_revenue;

-- First/last value
SELECT
    user_id,
    order_date,
    total,
    FIRST_VALUE(total) OVER (PARTITION BY user_id ORDER BY order_date) as first_order,
    LAST_VALUE(total) OVER (
        PARTITION BY user_id ORDER BY order_date
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as last_order
FROM orders;
```


---

# CHAPTER 2: SCHEMA DESIGN AND CONSTRAINTS


## Normalization (1NF, 2NF, 3NF)

```
1NF (First Normal Form):
  - Each cell has a single atomic value
  - No repeating groups
  
  BAD:   user.phones = "123, 456, 789"  (multi-value in one cell)
  GOOD:  separate phones table with user_id FK

2NF (Second Normal Form):
  - Already 1NF
  - All non-PK columns depend on the ENTIRE PK (not partial)
  
  BAD:  order_items(order_id, product_id, quantity, product_name)
        product_name depends only on product_id, not the composite PK.
  GOOD: split: order_items(order_id, product_id, quantity) + products(id, name)

3NF (Third Normal Form):
  - Already 2NF
  - Non-PK columns don't depend on OTHER non-PK columns
  
  BAD:  employees(id, name, dept_id, dept_name)
        dept_name depends on dept_id, not directly on id.
  GOOD: split into employees and departments

WHEN TO DENORMALIZE:
  - Reads vastly outnumber writes (analytical workloads, read-heavy)
  - Joins are too expensive
  - Specific access patterns warrant duplicated data
  
  Example: store user_name in orders (denormalized) to avoid joins for order listings.
  Trade-off: must update user_name in orders when user changes name.
```


## Constraints

```sql
CREATE TABLE users (
    -- PRIMARY KEY: unique + NOT NULL automatically
    id BIGSERIAL PRIMARY KEY,

    -- NOT NULL: column cannot be NULL
    email VARCHAR(255) NOT NULL,

    -- UNIQUE: no duplicates allowed
    username VARCHAR(50) UNIQUE NOT NULL,

    -- CHECK: enforce condition
    age INT CHECK (age >= 0 AND age <= 150),

    -- DEFAULT: value used when not specified
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Multiple constraints
    score INT CHECK (score >= 0) DEFAULT 0,

    -- UNIQUE on multiple columns (composite unique)
    UNIQUE (email),
    CONSTRAINT username_lowercase CHECK (username = LOWER(username))
);

-- FOREIGN KEY
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    total DECIMAL(10, 2) NOT NULL CHECK (total > 0),
    status VARCHAR(20) NOT NULL,

    -- FK with ON DELETE behavior
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE      -- Delete orders when user deleted
        -- ON DELETE RESTRICT  -- Forbid deleting user with orders
        -- ON DELETE SET NULL  -- Set user_id to NULL
        -- ON DELETE SET DEFAULT
);

-- Composite primary key
CREATE TABLE order_items (
    order_id BIGINT,
    product_id BIGINT,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Adding constraint after creation
ALTER TABLE users ADD CONSTRAINT email_format CHECK (email LIKE '%@%');
ALTER TABLE users DROP CONSTRAINT email_format;
```


## Picking Data Types

```
Numbers:
  SMALLINT       -32768 to 32767 (2 bytes)
  INT/INTEGER    -2.1B to 2.1B (4 bytes) — most common for IDs
  BIGINT         -9.2 × 10¹⁸ to 9.2 × 10¹⁸ (8 bytes) — for large IDs/counts
  NUMERIC(p, s)  Exact decimal — USE FOR MONEY! NEVER FLOAT
  DECIMAL(p, s)  Same as NUMERIC
  REAL           4-byte float (avoid for money)
  DOUBLE PRECISION 8-byte float

Strings:
  VARCHAR(n)     Variable length up to n
  TEXT           Unlimited length (in PG, same perf as VARCHAR)
  CHAR(n)        Fixed length, padded (rarely useful)

Date/Time:
  DATE           Just date: 2026-06-10
  TIME           Just time
  TIMESTAMP      Date + time, no TZ
  TIMESTAMPTZ    Date + time WITH TZ (ALWAYS USE THIS!)
  INTERVAL       Duration: '7 days', '2 hours'

JSON:
  JSONB          Binary JSON — indexable, faster, USE THIS
  JSON           Text JSON (slower, kept for compatibility)

UUIDs:
  UUID           128-bit identifier
                 SELECT gen_random_uuid();   -- Built-in (PG 13+)

Booleans:
  BOOLEAN        TRUE/FALSE/NULL

Arrays:
  INT[]          Array of integers
  TEXT[]         Array of strings
                 INSERT VALUES ('{1,2,3}'::INT[])

Special:
  BYTEA          Binary data (file blobs — usually better to store externally)
  INET           IP address (with subnet)
  CIDR           IP network
  ENUM           Custom restricted set (CREATE TYPE)

GOLDEN RULES:
  - Money: NUMERIC(precision, scale), e.g. NUMERIC(10, 2)
  - Timestamps: ALWAYS TIMESTAMPTZ, store in UTC
  - IDs: BIGINT or UUID (BIGSERIAL auto-increments)
  - Don't use VARCHAR(n) for arbitrary text — use TEXT
```


---

# CHAPTER 3: INDEXING STRATEGIES


## How Indexes Work (B-tree)

```
Without index:
  SELECT * FROM users WHERE email = 'alice@example.com';
  → Scan every row in users (Sequential Scan)
  → O(n) — 10M rows = 10M comparisons

With B-tree index on email:
  → Walk tree from root to leaf
  → O(log n) — 10M rows = ~24 comparisons (log₂(10M) ≈ 23.25)

B-tree properties:
  - Sorted, balanced (every leaf same depth)
  - Each node has multiple keys (typically 100s)
  - Great for: equality (=), range (<, >, BETWEEN), prefix LIKE 'abc%'
  - Bad for:   suffix LIKE '%abc', function calls
```


## Index Types (PostgreSQL)

```sql
-- B-tree (default, most common)
CREATE INDEX idx_users_email ON users (email);
-- Equality, range, ORDER BY

-- Hash (PG 10+, rarely needed)
CREATE INDEX idx_users_email_hash ON users USING HASH (email);
-- Only =, slightly faster than B-tree for that

-- GIN (Generalized Inverted Index) — for arrays, JSONB, full-text
CREATE INDEX idx_post_tags ON posts USING GIN (tags);     -- tags TEXT[]
-- Speeds up: tags @> ARRAY['python'], tags && ARRAY['ai','python']

CREATE INDEX idx_doc_search ON docs USING GIN (to_tsvector('english', body));
-- Full-text search

CREATE INDEX idx_data_gin ON events USING GIN (payload);  -- payload JSONB
-- Speeds up: payload @> '{"user_id": 123}'

-- GiST (Generalized Search Tree) — geometric, range types
CREATE INDEX idx_locations ON places USING GIST (coords);  -- coords POINT
-- Spatial queries

-- BRIN (Block Range Index) — for very large tables with natural ordering
CREATE INDEX idx_logs_time ON logs USING BRIN (created_at);
-- Tiny index (KB instead of GB), great for time-series data

-- Partial index (smaller, faster — for filtering subset)
CREATE INDEX idx_active_users ON users (last_login)
    WHERE active = true;
-- Index ONLY active users — much smaller than full index

-- Covering index (INCLUDE — PG 11+)
CREATE INDEX idx_covering ON users (country) INCLUDE (name, email);
-- Query "SELECT name, email FROM users WHERE country = ?" reads ONLY index

-- Expression index
CREATE INDEX idx_users_email_lower ON users (LOWER(email));
-- For case-insensitive: WHERE LOWER(email) = LOWER(?)
```


## Composite Indexes — Column Order Matters

```sql
CREATE INDEX idx_orders_user_status ON orders (user_id, status, created_at);

-- This index helps these queries:
SELECT * FROM orders WHERE user_id = 123;                          ✅
SELECT * FROM orders WHERE user_id = 123 AND status = 'paid';      ✅
SELECT * FROM orders WHERE user_id = 123 AND status = 'paid' 
    AND created_at > '2026-01-01';                                 ✅
SELECT * FROM orders WHERE user_id = 123 ORDER BY status, created_at; ✅

-- These DO NOT use the index efficiently:
SELECT * FROM orders WHERE status = 'paid';                        ❌ (no user_id)
SELECT * FROM orders WHERE created_at > '2026-01-01';              ❌ (no user_id)
SELECT * FROM orders WHERE status = 'paid' AND created_at > ...;   ❌

RULE: Index columns are used left-to-right.
      Skip a column = stop using the index.

CARDINALITY RULE: put high-cardinality (many unique values) columns first.
  Bad:  INDEX (is_active, user_id)  -- is_active only 2 values
  Good: INDEX (user_id, is_active)
```


## When NOT to Index

```
DON'T INDEX:
  - Tiny tables (<1000 rows) — sequential scan is fine
  - Low cardinality columns (boolean alone) — bitmap better
  - Columns frequently updated — index maintenance cost
  - Columns never used in WHERE/JOIN/ORDER BY

EVERY INDEX:
  - Slows down INSERT/UPDATE/DELETE (must maintain index)
  - Uses disk space (often 10-30% of table size)
  - Memory pressure on buffer cache

RULE OF THUMB:
  - Index foreign keys (almost always)
  - Index columns in WHERE clauses
  - Composite indexes for multi-column WHEREs
  - Don't index "just in case"
  - Audit with pg_stat_user_indexes — drop unused indexes
```


## Finding Unused Indexes

```sql
-- Find indexes with low usage
SELECT
    schemaname,
    relname AS table_name,
    indexrelname AS index_name,
    idx_scan AS times_used,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan < 50           -- Used fewer than 50 times
ORDER BY pg_relation_size(indexrelid) DESC;

-- Find duplicate indexes
SELECT
    indrelid::regclass AS table,
    array_agg(indexrelid::regclass) AS indexes
FROM pg_index
GROUP BY indrelid, indkey
HAVING COUNT(*) > 1;
```


---

# CHAPTER 4: QUERY OPTIMIZATION


## EXPLAIN — Read Query Plans

```sql
-- Show estimated plan
EXPLAIN SELECT * FROM users WHERE email = 'alice@example.com';

-- Show actual execution (runs the query!)
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@example.com';

-- With buffer usage stats
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;

-- Verbose, formatted
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT TEXT) SELECT ...;
```

Example output:
```
Index Scan using idx_users_email on users  (cost=0.42..8.44 rows=1 width=64) (actual time=0.041..0.042 rows=1 loops=1)
  Index Cond: (email = 'alice@example.com'::text)
  Buffers: shared hit=4
Planning Time: 0.140 ms
Execution Time: 0.060 ms
```

Key things to look for:
- **Scan type**: Index Scan (good) > Bitmap Scan > Seq Scan (bad for big tables)
- **cost**: estimated relative cost (lower = better)
- **rows**: estimated vs actual — big mismatch = bad statistics
- **loops**: how many times this node was executed
- **Buffers**: shared hit = cache, read = disk
- **Filter**: applied after scan (often means missing index)


## Common Plan Nodes

```
SEQ SCAN
  Reads every row. OK for small tables or if returning most rows.
  Bad when filtering small subset of large table → need index.

INDEX SCAN
  Walks B-tree, returns matching rows in index order.
  Good for: WHERE on indexed column, ORDER BY indexed column.

INDEX ONLY SCAN
  Reads ONLY the index — table not accessed.
  Best case! Requires query columns all in index (covering index).

BITMAP SCAN
  Builds bitmap of matching rows, then fetches. Good for medium selectivity.
  Often Bitmap Index Scan + Bitmap Heap Scan combination.

NESTED LOOP
  For each row in outer, scan inner. Good when outer is small.
  Bad when both are big — explodes O(n×m).

HASH JOIN
  Build hash table of one side, probe with other. Good for medium-large equi-joins.
  Requires memory; spills to disk if work_mem too small.

MERGE JOIN
  Sort both inputs, walk in parallel. Best for very large pre-sorted inputs.

SORT
  Expensive if doesn't fit in work_mem (spills to disk = slow).

AGGREGATE / HASH AGGREGATE
  GROUP BY: hash-based usually fast.

GATHER / PARALLEL
  Multiple workers in parallel. PG 9.6+ auto-parallelizes when worthwhile.
```


## Optimization Examples

```sql
-- BAD: Function on indexed column prevents index use
SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';
-- Index on email NOT used!

-- FIX 1: Expression index
CREATE INDEX idx_users_email_lower ON users (LOWER(email));

-- FIX 2: Store normalized data
-- Always lowercase emails at insert time, then use plain WHERE.


-- BAD: Leading wildcard prevents index use
SELECT * FROM users WHERE name LIKE '%john%';

-- FIX: GIN trigram index for substring search
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_users_name_trgm ON users USING GIN (name gin_trgm_ops);
-- Now LIKE '%john%' uses the index


-- BAD: OR conditions often prevent index use
SELECT * FROM users WHERE email = 'x' OR username = 'y';

-- FIX: UNION (uses both indexes)
SELECT * FROM users WHERE email = 'x'
UNION
SELECT * FROM users WHERE username = 'y';


-- BAD: NOT IN with NULL
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM banned);
-- If banned.user_id has any NULL, returns NO rows!

-- FIX: NOT EXISTS
SELECT * FROM users u
WHERE NOT EXISTS (SELECT 1 FROM banned b WHERE b.user_id = u.id);


-- BAD: SELECT * fetches unused columns
SELECT * FROM users WHERE id = 123;

-- GOOD: Only what you need
SELECT id, name, email FROM users WHERE id = 123;
-- Less I/O, less network, can use Index Only Scan if covering index exists


-- BAD: N+1 query pattern (from app code)
SELECT * FROM orders WHERE user_id = 5;       -- 1 query
-- For each order:
SELECT * FROM order_items WHERE order_id = ?; -- N queries
SELECT * FROM products WHERE id = ?;          -- N more queries

-- FIX: Join or batch
SELECT o.*, oi.*, p.*
FROM orders o
LEFT JOIN order_items oi ON oi.order_id = o.id
LEFT JOIN products p ON p.id = oi.product_id
WHERE o.user_id = 5;
-- Or use ORM dataloader / eager loading
```


## Statistics and ANALYZE

```sql
-- PG uses table statistics to plan queries
-- Auto-runs ANALYZE periodically but not always frequently enough

-- Manual update of statistics
ANALYZE users;

-- For large tables, run after big imports/changes
INSERT INTO orders ... (millions of rows);
ANALYZE orders;

-- Tune sampling for important tables
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 1000;
-- Default is 100. Higher = better estimates for skewed data.

-- View stats
SELECT * FROM pg_stats WHERE tablename = 'users';
```


---

# CHAPTER 5: TRANSACTIONS AND CONCURRENCY


## ACID Properties

```
ATOMICITY
  All-or-nothing. Either all statements succeed or all roll back.
  Example: transfer money — either both accounts updated, or neither.

CONSISTENCY
  Database constraints maintained. Triggers, FKs, CHECKs satisfied.

ISOLATION
  Concurrent transactions don't interfere (mostly).
  Different "isolation levels" — see below.

DURABILITY
  Once committed, survives crashes (written to disk + WAL).
```


## Transaction Basics

```sql
BEGIN;  -- Start transaction (also: START TRANSACTION)

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- If everything is good:
COMMIT;

-- Or undo all:
ROLLBACK;

-- Savepoints (nested-like behavior)
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
SAVEPOINT s1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- Oops, error
ROLLBACK TO SAVEPOINT s1;
-- Now we're back to just having debited account 1
COMMIT;  -- Or ROLLBACK to undo everything
```


## Isolation Levels

```
READ UNCOMMITTED:
  Can see uncommitted changes from other transactions.
  "Dirty reads" possible. (PostgreSQL treats this as READ COMMITTED.)

READ COMMITTED (PG default):
  Only see committed data.
  But: non-repeatable reads — same SELECT in transaction can return different data.

REPEATABLE READ (snapshot isolation):
  Transaction sees database snapshot at start.
  Same SELECT returns same data throughout.
  But: phantom reads possible (new rows from other tx).
  In PG: actually serializable for read-only.

SERIALIZABLE:
  As if transactions ran one at a time (strongest).
  PG uses SSI (Serializable Snapshot Isolation).
  May abort with serialization errors that must be retried.

CHANGE IT:
  SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
  BEGIN;
  ...
  COMMIT;
```


## Concurrency Anomalies

```
DIRTY READ:
  Tx1 writes (uncommitted).
  Tx2 reads that uncommitted data.
  Tx1 rolls back.
  Tx2 saw data that "never existed."
  → Prevented by READ COMMITTED and stricter.

NON-REPEATABLE READ:
  Tx1 reads row.
  Tx2 updates and commits.
  Tx1 reads same row again — sees different value.
  → Prevented by REPEATABLE READ and stricter.

PHANTOM READ:
  Tx1: SELECT WHERE age > 30 → 5 rows.
  Tx2: INSERT new row matching, commits.
  Tx1: SELECT same → 6 rows.
  → Prevented by SERIALIZABLE.

LOST UPDATE:
  Both transactions read same value, both update independently.
  Last commit wins; first update lost.
  → Prevented by row locks (SELECT FOR UPDATE) or higher isolation.
```


## Pessimistic Locking (SELECT FOR UPDATE)

```sql
-- Bank transfer example
BEGIN;

-- Lock the row so no other transaction can update until we commit
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;

-- Compute new balance in app
-- Then update
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT;
-- Lock released
```

Other lock modes:
```sql
SELECT ... FOR UPDATE        -- Exclusive lock, blocks others
SELECT ... FOR UPDATE NOWAIT -- Fail immediately if locked
SELECT ... FOR UPDATE SKIP LOCKED -- Skip locked rows (great for queues!)
SELECT ... FOR SHARE         -- Shared lock, others can read but not write
```

Queue pattern with SKIP LOCKED (very useful!):
```sql
-- Worker process pulls one job
BEGIN;
SELECT * FROM jobs
WHERE status = 'pending'
ORDER BY created_at
LIMIT 1
FOR UPDATE SKIP LOCKED;
-- → other workers skip this row automatically

UPDATE jobs SET status = 'processing', worker_id = $1 WHERE id = $job_id;
COMMIT;
```


## Optimistic Locking (Version Column)

```sql
-- Add version column
ALTER TABLE products ADD COLUMN version INT DEFAULT 0;

-- Application reads
SELECT id, name, price, version FROM products WHERE id = 5;
-- Got version = 7

-- App computes update, then:
UPDATE products
SET price = 99.99, version = version + 1
WHERE id = 5 AND version = 7;     -- Only updates if version still 7
-- Affected rows = 0 means another tx updated → conflict → retry
```


## Deadlocks

```
DEADLOCK:
  Tx1 holds lock on A, wants B.
  Tx2 holds lock on B, wants A.
  Neither can proceed.

PostgreSQL detects and kills one (the "victim") with error 40P01.

PREVENTION:
  - Always lock resources in the SAME ORDER across transactions
  - Keep transactions SHORT
  - Use NOWAIT or timeouts
  - Consider SERIALIZABLE — but expect more retries
```


## MVCC (How PostgreSQL Achieves Concurrency)

```
Multi-Version Concurrency Control:
  - Readers don't block writers
  - Writers don't block readers
  - Each transaction sees a consistent snapshot

HOW IT WORKS:
  - UPDATE creates a NEW row version (doesn't overwrite!)
  - Old version kept for transactions that started before the update
  - Each row has xmin (creating tx) and xmax (deleting tx)
  - VACUUM cleans up old versions no transaction needs

IMPLICATIONS:
  - UPDATE is like INSERT + mark old as deleted
  - Long-running transactions prevent vacuum (table bloat!)
  - Always tune autovacuum for write-heavy tables
```


---

# CHAPTER 6: ADVANCED PATTERNS


## Pagination — Done Right

```sql
-- BAD: OFFSET pagination at scale
SELECT * FROM products ORDER BY created_at DESC
LIMIT 20 OFFSET 100000;
-- DB must skip 100,000 rows just to discard them → slow

-- GOOD: Cursor (keyset) pagination
SELECT * FROM products
WHERE created_at < $last_seen_timestamp
ORDER BY created_at DESC
LIMIT 20;
-- O(log n), fast even at page 1,000,000

-- For ties on created_at, include unique tiebreaker:
WHERE (created_at, id) < ($last_seen_timestamp, $last_seen_id)
```


## Upsert (INSERT ... ON CONFLICT)

```sql
-- Insert or update if email exists
INSERT INTO users (email, name, last_login)
VALUES ('alice@example.com', 'Alice', NOW())
ON CONFLICT (email) DO UPDATE
    SET name = EXCLUDED.name,
        last_login = EXCLUDED.last_login;

-- Insert only if not exists (DO NOTHING)
INSERT INTO events (id, type) VALUES (123, 'login')
ON CONFLICT (id) DO NOTHING;

-- Conditional update
INSERT INTO counters (key, value) VALUES ('hits', 1)
ON CONFLICT (key) DO UPDATE
    SET value = counters.value + 1;
```


## Soft Deletes

```sql
-- Add deleted_at column
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;

-- Index for active users
CREATE INDEX idx_users_active ON users (id) WHERE deleted_at IS NULL;

-- "Delete"
UPDATE users SET deleted_at = NOW() WHERE id = 5;

-- Query active users
SELECT * FROM users WHERE deleted_at IS NULL;

-- Cleanup old soft-deleted rows
DELETE FROM users WHERE deleted_at < NOW() - INTERVAL '30 days';
```


## Audit Tables (History Tracking)

```sql
CREATE TABLE users_audit (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    action VARCHAR(10) NOT NULL,  -- INSERT, UPDATE, DELETE
    old_data JSONB,
    new_data JSONB,
    changed_by BIGINT,
    changed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger to auto-populate
CREATE OR REPLACE FUNCTION users_audit_trigger() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        INSERT INTO users_audit (user_id, action, old_data, new_data)
        VALUES (OLD.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW));
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO users_audit (user_id, action, old_data)
        VALUES (OLD.id, 'DELETE', to_jsonb(OLD));
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO users_audit (user_id, action, new_data)
        VALUES (NEW.id, 'INSERT', to_jsonb(NEW));
    END IF;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_audit
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION users_audit_trigger();
```


## JSONB — Schemaless Within SQL

```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert
INSERT INTO events (type, payload) VALUES
    ('login', '{"user_id": 123, "ip": "1.2.3.4", "device": "mobile"}');

-- Access fields
SELECT payload->>'user_id' as user_id FROM events;
-- -> returns JSONB, ->> returns text
-- payload->'tags'->>'priority' nested

-- Filter on JSON keys
SELECT * FROM events WHERE payload->>'user_id' = '123';

-- Containment (uses GIN index!)
SELECT * FROM events WHERE payload @> '{"device": "mobile"}';

-- Exists key
SELECT * FROM events WHERE payload ? 'session_id';

-- Update specific key
UPDATE events SET payload = payload || '{"processed": true}'::jsonb
WHERE id = 1;

-- Remove key
UPDATE events SET payload = payload - 'temp_field' WHERE id = 1;

-- Index for fast JSON queries
CREATE INDEX idx_events_payload ON events USING GIN (payload);
-- For specific paths:
CREATE INDEX idx_events_user_id ON events ((payload->>'user_id'));
```


## Partitioning Large Tables

```sql
-- Partition by range (e.g., time)
CREATE TABLE measurements (
    id BIGSERIAL,
    sensor_id INT NOT NULL,
    value DOUBLE PRECISION,
    measured_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (measured_at);

-- Create monthly partitions
CREATE TABLE measurements_2026_06 PARTITION OF measurements
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');

CREATE TABLE measurements_2026_07 PARTITION OF measurements
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');

-- Inserts auto-routed to correct partition
INSERT INTO measurements (sensor_id, value, measured_at)
VALUES (1, 23.5, '2026-06-15');   -- Goes to _2026_06

-- Queries scan only relevant partitions (partition pruning)
SELECT AVG(value) FROM measurements
WHERE measured_at >= '2026-06-01' AND measured_at < '2026-07-01';
-- Only scans _2026_06 partition

-- Drop old partitions super fast (no row-by-row delete)
DROP TABLE measurements_2025_01;

-- Partition by hash (for distributed sharding)
CREATE TABLE users (id BIGINT, ...) PARTITION BY HASH (id);
CREATE TABLE users_0 PARTITION OF users FOR VALUES WITH (modulus 4, remainder 0);
CREATE TABLE users_1 PARTITION OF users FOR VALUES WITH (modulus 4, remainder 1);
-- etc.
```


---

# CHAPTER 7: OPERATIONS AND MAINTENANCE


## Backup Strategies

```bash
# Logical backup (portable, slower for large DBs)
pg_dump -U postgres mydb > backup.sql
pg_dump -U postgres -F c mydb > backup.dump   # Custom format (compressed)
pg_dump -U postgres -F d -j 4 mydb -f backup_dir   # Parallel directory format

# Restore
psql -U postgres mydb < backup.sql
pg_restore -U postgres -d mydb -j 4 backup.dump

# Physical backup (binary, faster, requires same PG version)
pg_basebackup -U replicator -D /backup/base -Ft -z -P

# Point-in-time recovery (PITR) — requires WAL archiving
# postgresql.conf:
#   wal_level = replica
#   archive_mode = on
#   archive_command = 'cp %p /backup/wal/%f'
```

**Backup best practices:**
- Daily full backup minimum
- WAL archive for point-in-time recovery
- Test restore procedures regularly (untested backups = no backups)
- Store backups offsite
- Encrypt sensitive backups


## Replication Setup (Streaming)

```bash
# Primary postgresql.conf:
wal_level = replica
max_wal_senders = 10
hot_standby = on

# Primary pg_hba.conf:
host replication replicator REPLICA_IP/32 scram-sha-256

# Create replication user on primary
CREATE USER replicator REPLICATION LOGIN PASSWORD 'secret';

# On replica, base backup from primary
pg_basebackup -h PRIMARY_HOST -U replicator -D /var/lib/postgresql/data -P -R

# -R adds standby.signal and connection info — replica starts in streaming mode

# On replica, start postgres
# It will continuously stream WAL from primary
```


## Connection Pooling

```
PROBLEM: Each connection = process in PostgreSQL.
1000 connections = 1000 processes = lots of memory.

SOLUTION: Connection pooler in front of PG.

PgBouncer (most popular):
  Pool modes:
    session   — connection sticks for client's session
    transaction — connection reused after each transaction (RECOMMENDED)
    statement  — connection reused after each statement (limited features)
  
  App connects to PgBouncer → PgBouncer multiplexes onto fewer PG connections.
  
  Typical: 100 PG connections serving 10,000 app connections.

Example pgbouncer.ini:
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
listen_port = 6432
listen_addr = *
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
default_pool_size = 25
max_client_conn = 1000
```


## Monitoring Queries

```sql
-- Slowest queries (requires pg_stat_statements extension)
SELECT
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Currently running queries
SELECT pid, age(clock_timestamp(), query_start), usename, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;

-- Locks blocking other queries
SELECT
    blocked.pid AS blocked_pid,
    blocked.query AS blocked_query,
    blocking.pid AS blocking_pid,
    blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking ON blocked.wait_event_type = 'Lock'
    AND blocking.pid = ANY(pg_blocking_pids(blocked.pid));

-- Kill a query
SELECT pg_cancel_backend(pid);   -- Polite
SELECT pg_terminate_backend(pid); -- Forceful

-- Table sizes
SELECT
    schemaname || '.' || tablename AS table,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) AS table_size,
    pg_size_pretty(pg_indexes_size(schemaname || '.' || tablename)) AS indexes_size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC
LIMIT 20;
```


## Vacuum and Autovacuum

```
WHY VACUUM:
  MVCC keeps dead row versions until vacuum runs.
  Without vacuum: table bloat, slow queries, eventual transaction ID wraparound.

AUTO-VACUUM:
  Runs automatically. Tune for write-heavy tables:
  
  ALTER TABLE busy_table SET (
      autovacuum_vacuum_scale_factor = 0.05,   -- Default 0.2 (vacuum at 5% dead)
      autovacuum_analyze_scale_factor = 0.02
  );

MANUAL VACUUM:
  VACUUM users;              -- Reclaim space
  VACUUM ANALYZE users;      -- Also update statistics
  VACUUM FULL users;         -- Rewrite table (LOCKS! avoid in production)

REINDEX:
  Sometimes indexes bloat. Rebuild:
  REINDEX INDEX idx_users_email;
  REINDEX TABLE users;
  REINDEX TABLE CONCURRENTLY users;   -- No lock (PG 12+)
```


## Common Pitfalls

```
PITFALL 1: Forgetting indexes on FK columns
  Foreign key implies relationship but NOT an index!
  Manual: CREATE INDEX idx_orders_user_id ON orders (user_id);

PITFALL 2: VARCHAR length validation as data type
  VARCHAR(255) doesn't help; use TEXT and validate in app/CHECK constraint.

PITFALL 3: Using FLOAT/REAL for money
  Floating point rounding errors → financial discrepancies. Use NUMERIC.

PITFALL 4: Storing timestamps without TZ
  TIMESTAMP (without TZ) is ambiguous. Use TIMESTAMPTZ + store UTC.

PITFALL 5: Premature denormalization
  Causes update anomalies. Normalize first, denormalize when needed for performance.

PITFALL 6: SELECT * in production queries
  Fetches more data than needed. Specify columns explicitly.

PITFALL 7: ORM N+1 queries
  Most ORMs lazy-load relationships → 1+N queries.
  Use eager loading: .includes() / .options(joinedload()) / .prefetch_related()

PITFALL 8: Locking strategies
  Long-running transactions hold locks → block everyone.
  Keep transactions short. Use FOR UPDATE SKIP LOCKED for queues.

PITFALL 9: Not testing with realistic data
  Query that's fast on 100 rows can be terrible on 10M.
  Test with production-sized datasets.

PITFALL 10: Ignoring pg_stat_user_indexes
  Unused indexes cost write performance AND disk space.
  Audit and drop them.

PITFALL 11: Connection leaks
  App doesn't close connections → PG runs out of connections.
  Use connection pool with timeouts.

PITFALL 12: No backups (or untested backups)
  "We have backups" but never tested. Disaster strikes — restore fails.
  Test restore monthly.
```