# Advanced SQL Complete Reference


---

# CHAPTER 1: WINDOW FUNCTIONS


## Remarks

Advanced SQL goes beyond SELECT/JOIN/GROUP BY into powerful analytical features. Window functions perform calculations across related rows without collapsing them (unlike GROUP BY). CTEs and recursive queries simplify complex logic. Understanding query plans lets you optimize slow queries. This reference uses PostgreSQL syntax (most features work in MySQL 8+, SQLite 3.25+, SQL Server).


## Window Functions Basics

```sql
-- Window function: compute over a "window" of rows WITHOUT grouping
-- Syntax: function() OVER (PARTITION BY ... ORDER BY ...)

-- Regular GROUP BY: collapses rows
SELECT department, AVG(salary)
FROM employees
GROUP BY department;
-- Result: 1 row per department

-- Window function: keeps ALL rows, adds computed column
SELECT
    name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) AS diff_from_avg
FROM employees;
-- Result: every employee row, with department average alongside


-- RANKING FUNCTIONS

-- ROW_NUMBER: unique sequential number (no ties)
SELECT name, department, salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rank
FROM employees;
-- Each department's employees numbered 1, 2, 3... by salary

-- RANK: same rank for ties, gaps after
-- Salaries: 100, 90, 90, 80 → ranks: 1, 2, 2, 4 (skips 3)
SELECT name, salary,
    RANK() OVER (ORDER BY salary DESC) AS rank
FROM employees;

-- DENSE_RANK: same rank for ties, NO gaps
-- Salaries: 100, 90, 90, 80 → ranks: 1, 2, 2, 3
SELECT name, salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank
FROM employees;

-- NTILE: divide into N equal groups
SELECT name, salary,
    NTILE(4) OVER (ORDER BY salary DESC) AS quartile
FROM employees;
-- Divides employees into 4 quartiles by salary


-- Top N per group (CLASSIC interview query)
-- Get top 3 highest-paid employees per department
WITH ranked AS (
    SELECT name, department, salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
    FROM employees
)
SELECT name, department, salary
FROM ranked
WHERE rn <= 3;
```


## Aggregate Window Functions

```sql
-- Running total
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) AS running_total
FROM transactions;
-- date       amount   running_total
-- 2026-01-01   100         100
-- 2026-01-02   200         300
-- 2026-01-03   150         450

-- Running average
SELECT
    date,
    amount,
    AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7day
FROM daily_sales;
-- 7-day moving average (current row + 6 preceding)

-- FRAME SPECIFICATION:
-- ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW  (default for ORDER BY)
-- ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING           (centered window)
-- ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
-- RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW (time-based)

-- Cumulative percentage
SELECT
    name,
    salary,
    SUM(salary) OVER (ORDER BY salary DESC) AS cumulative,
    ROUND(100.0 * SUM(salary) OVER (ORDER BY salary DESC) /
          SUM(salary) OVER (), 2) AS cumulative_pct
FROM employees;

-- Percentage of total
SELECT
    department,
    salary,
    ROUND(100.0 * salary / SUM(salary) OVER (PARTITION BY department), 2) AS pct_of_dept
FROM employees;
```


## LAG, LEAD, FIRST_VALUE, LAST_VALUE

```sql
-- LAG: access PREVIOUS row's value
-- LEAD: access NEXT row's value

-- Month-over-month growth
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_month,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month)) /
          LAG(revenue) OVER (ORDER BY month), 2) AS growth_pct
FROM monthly_revenue;
-- month     revenue  prev_month  growth_pct
-- 2026-01   10000    NULL        NULL
-- 2026-02   12000    10000       20.00
-- 2026-03   11500    12000       -4.17

-- LAG with default (avoid NULL)
LAG(revenue, 1, 0) OVER (ORDER BY month)  -- default 0 if no previous

-- LEAD: look ahead
SELECT
    date,
    event,
    LEAD(date) OVER (ORDER BY date) AS next_event_date,
    LEAD(date) OVER (ORDER BY date) - date AS days_until_next
FROM events;

-- FIRST_VALUE / LAST_VALUE
SELECT
    name,
    department,
    salary,
    FIRST_VALUE(name) OVER (PARTITION BY department ORDER BY salary DESC) AS highest_paid,
    LAST_VALUE(name) OVER (
        PARTITION BY department ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS lowest_paid
FROM employees;
-- IMPORTANT: LAST_VALUE needs explicit frame, otherwise default frame
-- only includes up to current row (not what you want!)


-- NTH_VALUE: get Nth row's value
SELECT
    name,
    department,
    salary,
    NTH_VALUE(name, 2) OVER (
        PARTITION BY department ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS second_highest
FROM employees;
```


---

# CHAPTER 2: COMMON TABLE EXPRESSIONS (CTEs)


## Basic CTEs

```sql
-- CTE: temporary named result set (readable subquery)
WITH active_users AS (
    SELECT id, name, email
    FROM users
    WHERE status = 'active'
    AND last_login > NOW() - INTERVAL '30 days'
)
SELECT u.name, COUNT(o.id) AS order_count
FROM active_users u
JOIN orders o ON o.user_id = u.id
GROUP BY u.name
ORDER BY order_count DESC;


-- Multiple CTEs
WITH
monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', created_at) AS month,
        SUM(total) AS revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY 1
),
monthly_costs AS (
    SELECT
        DATE_TRUNC('month', date) AS month,
        SUM(amount) AS costs
    FROM expenses
    GROUP BY 1
)
SELECT
    r.month,
    r.revenue,
    c.costs,
    r.revenue - c.costs AS profit,
    ROUND(100.0 * (r.revenue - c.costs) / r.revenue, 2) AS margin_pct
FROM monthly_revenue r
JOIN monthly_costs c ON c.month = r.month
ORDER BY r.month;
```


## Recursive CTEs

```sql
-- RECURSIVE CTE: query references itself
-- Perfect for: hierarchies, trees, graphs, sequences

-- Org chart (manager → reports hierarchy)
WITH RECURSIVE org_tree AS (
    -- Base case: CEO (no manager)
    SELECT id, name, manager_id, 0 AS depth, name AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: employees with manager in previous level
    SELECT e.id, e.name, e.manager_id, t.depth + 1,
           t.path || ' → ' || e.name
    FROM employees e
    JOIN org_tree t ON e.manager_id = t.id
)
SELECT depth, path
FROM org_tree
ORDER BY path;
-- 0  Alice
-- 1  Alice → Bob
-- 1  Alice → Carol
-- 2  Alice → Bob → Dave
-- 2  Alice → Carol → Eve


-- Generate date series (fill gaps in data)
WITH RECURSIVE dates AS (
    SELECT DATE '2026-01-01' AS date
    UNION ALL
    SELECT date + INTERVAL '1 day'
    FROM dates
    WHERE date < DATE '2026-12-31'
)
SELECT d.date, COALESCE(s.revenue, 0) AS revenue
FROM dates d
LEFT JOIN daily_sales s ON s.date = d.date;
-- Every day of 2026, with 0 for days with no sales


-- Bill of Materials (parts → subparts)
WITH RECURSIVE bom AS (
    SELECT part_id, component_id, quantity, 1 AS level
    FROM components
    WHERE part_id = 'BICYCLE'

    UNION ALL

    SELECT c.part_id, c.component_id, c.quantity * b.quantity, b.level + 1
    FROM components c
    JOIN bom b ON c.part_id = b.component_id
)
SELECT component_id, SUM(quantity) AS total_needed
FROM bom
GROUP BY component_id;


-- Graph shortest path (BFS via recursive CTE)
WITH RECURSIVE paths AS (
    SELECT target AS node, 1 AS distance, ARRAY[source, target] AS path
    FROM edges
    WHERE source = 'A'

    UNION ALL

    SELECT e.target, p.distance + 1, p.path || e.target
    FROM edges e
    JOIN paths p ON e.source = p.node
    WHERE NOT e.target = ANY(p.path)   -- Prevent cycles
    AND p.distance < 10                 -- Limit depth
)
SELECT node, distance, path
FROM paths
WHERE node = 'Z'
ORDER BY distance
LIMIT 1;
```


---

# CHAPTER 3: QUERY OPTIMIZATION


## EXPLAIN and Query Plans

```sql
-- EXPLAIN: show HOW PostgreSQL will execute query
EXPLAIN SELECT * FROM users WHERE email = 'alice@example.com';

-- EXPLAIN ANALYZE: actually RUN and show real timing
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM users WHERE email = 'alice@example.com';

-- OUTPUT READING:
-- Seq Scan on users  (cost=0.00..1234.00 rows=1 width=100)
--   Filter: (email = 'alice@example.com'::text)
--   Rows Removed by Filter: 99999
--   Actual time=0.012..45.678 rows=1 loops=1

-- KEY TERMS:
-- Seq Scan:     full table scan (BAD for large tables with selective filter)
-- Index Scan:   uses index (GOOD)
-- Bitmap Scan:  index → bitmap → table (multiple matches)
-- Hash Join:    build hash table, probe (fast for equality)
-- Merge Join:   sorted inputs merged (fast for sorted/indexed)
-- Nested Loop:  for each row in A, scan B (fast for small A)

-- cost: estimated (startup_cost..total_cost)
-- rows: estimated row count
-- actual time: real milliseconds (only with ANALYZE)
-- loops: how many times this node executed


-- COMMON SLOW QUERY PATTERNS:

-- 1. Sequential scan on large table (missing index)
EXPLAIN SELECT * FROM orders WHERE user_id = 123;
-- Seq Scan on orders → needs index!
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- 2. Index not used (function on column)
-- BAD: index on created_at not used
SELECT * FROM orders WHERE DATE(created_at) = '2026-06-10';
-- GOOD: range query uses index
SELECT * FROM orders
WHERE created_at >= '2026-06-10' AND created_at < '2026-06-11';

-- 3. Index not used (type mismatch)
-- Column is integer, query passes string
SELECT * FROM users WHERE id = '123';   -- May not use index!
SELECT * FROM users WHERE id = 123;     -- Uses index

-- 4. Selecting too many columns
-- BAD: fetches all columns, can't use covering index
SELECT * FROM users WHERE status = 'active';
-- GOOD: select only needed columns
SELECT id, name, email FROM users WHERE status = 'active';
```


## Index Strategies

```sql
-- B-TREE INDEX (default, most common)
CREATE INDEX idx_users_email ON users(email);

-- COMPOSITE INDEX (multi-column)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);
-- Order matters! This index helps:
--   WHERE user_id = 123                    ✅
--   WHERE user_id = 123 AND created_at > X ✅
--   WHERE user_id = 123 ORDER BY created_at DESC ✅
-- Does NOT help:
--   WHERE created_at > X                   ❌ (second column alone)

-- PARTIAL INDEX (index subset of rows)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';
-- Smaller index, faster for queries that filter on status='active'

-- UNIQUE INDEX
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);
-- Enforces uniqueness + provides index

-- EXPRESSION INDEX (index on computed value)
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
-- Enables: WHERE LOWER(email) = 'alice@example.com'

-- GIN INDEX (for arrays, JSONB, full-text search)
CREATE INDEX idx_posts_tags ON posts USING GIN(tags);
-- Enables: WHERE tags @> ARRAY['python', 'web']

CREATE INDEX idx_users_data ON users USING GIN(metadata jsonb_path_ops);
-- Enables: WHERE metadata @> '{"role": "admin"}'

-- COVERING INDEX (includes extra columns to avoid table lookup)
CREATE INDEX idx_orders_covering ON orders(user_id) INCLUDE (total, status);
-- Index-only scan: reads index without touching table heap


-- WHEN NOT TO INDEX:
-- Small tables (<1000 rows): seq scan is faster
-- Columns with low cardinality (boolean, status with 3 values)
-- Frequently updated columns (index maintenance cost)
-- Write-heavy tables with few reads
```


## Advanced Joins and Techniques

```sql
-- LATERAL JOIN (correlated subquery as join)
-- "For each user, get their 3 most recent orders"
SELECT u.name, o.id, o.total, o.created_at
FROM users u
CROSS JOIN LATERAL (
    SELECT id, total, created_at
    FROM orders
    WHERE user_id = u.id
    ORDER BY created_at DESC
    LIMIT 3
) o;
-- Without LATERAL: would need window function + filter

-- SELF JOIN
-- Find employees who earn more than their manager
SELECT e.name AS employee, e.salary, m.name AS manager, m.salary AS manager_salary
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;

-- UPSERT (INSERT or UPDATE)
INSERT INTO users (email, name, login_count)
VALUES ('alice@example.com', 'Alice', 1)
ON CONFLICT (email)
DO UPDATE SET
    login_count = users.login_count + 1,
    last_login = NOW();

-- RETURNING (get affected rows back)
INSERT INTO orders (user_id, total)
VALUES (123, 99.99)
RETURNING id, created_at;

UPDATE users SET status = 'inactive'
WHERE last_login < NOW() - INTERVAL '1 year'
RETURNING id, email;

DELETE FROM expired_sessions
WHERE expires_at < NOW()
RETURNING user_id;

-- GROUPING SETS (multiple GROUP BY in one query)
SELECT
    COALESCE(department, 'ALL') AS department,
    COALESCE(role, 'ALL') AS role,
    COUNT(*) AS count,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY GROUPING SETS (
    (department, role),    -- Per department+role
    (department),          -- Per department (role = ALL)
    (role),                -- Per role (department = ALL)
    ()                     -- Grand total
);

-- FILTER clause (conditional aggregation)
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE status = 'active') AS active,
    COUNT(*) FILTER (WHERE status = 'inactive') AS inactive,
    AVG(salary) FILTER (WHERE department = 'Engineering') AS eng_avg_salary
FROM employees;
```


---

# CHAPTER 4: COMMON PITFALLS


## SQL Pitfalls

```
PITFALL 1: SELECT * in production
  Fetches all columns → more I/O, can't use covering index.
  Fix: select only needed columns.

PITFALL 2: N+1 queries
  Loop: for each user, query their orders → 1000 queries.
  Fix: JOIN or IN clause. Fetch all related data in one query.

PITFALL 3: No indexes on foreign keys
  JOIN on user_id without index → full table scan.
  Fix: index every foreign key column.

PITFALL 4: Function on indexed column
  WHERE YEAR(created_at) = 2026 → can't use index.
  Fix: WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'.

PITFALL 5: Not using EXPLAIN
  Guessing why query is slow.
  Fix: EXPLAIN ANALYZE every slow query. Read the plan.

PITFALL 6: Missing LIMIT on potentially huge results
  SELECT * FROM logs → returns 10 million rows.
  Fix: always LIMIT, or paginate with cursor.

PITFALL 7: Implicit type conversion
  WHERE id = '123' (string vs integer) → index bypass.
  Fix: match types exactly.

PITFALL 8: OFFSET pagination on large tables
  OFFSET 100000 → DB reads and discards 100,000 rows.
  Fix: cursor-based pagination (WHERE id > last_seen_id LIMIT 20).

PITFALL 9: Not handling NULLs
  WHERE status != 'active' does NOT include NULLs!
  Fix: WHERE status != 'active' OR status IS NULL.
  Or: WHERE status IS DISTINCT FROM 'active' (PostgreSQL).

PITFALL 10: Correlated subquery in SELECT
  SELECT (SELECT COUNT(*) FROM orders WHERE user_id = u.id) FROM users
  → runs subquery for EVERY row.
  Fix: LEFT JOIN with GROUP BY, or window function.

PITFALL 11: Too many indexes
  Index on every column → slow writes (each INSERT updates all indexes).
  Fix: index only columns used in WHERE, JOIN, ORDER BY.

PITFALL 12: Not using transactions for related operations
  Insert order then items separately → partial data if crash between.
  Fix: BEGIN; INSERT order; INSERT items; COMMIT;

PITFALL 13: DISTINCT as band-aid
  Query returns duplicates → add DISTINCT → hide the real JOIN bug.
  Fix: fix the JOIN logic. DISTINCT masks problems.

PITFALL 14: Storing CSV in a column
  tags = "python,web,api" → can't index, can't JOIN.
  Fix: array column, JSONB, or junction table.

PITFALL 15: Not vacuuming (PostgreSQL)
  Dead tuples accumulate → table bloat → slow queries.
  Fix: autovacuum enabled (default), monitor pg_stat_user_tables.
```