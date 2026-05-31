# SQL Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH SQL


## Remarks

SQL (Structured Query Language) is the standard language for relational databases. Different databases (PostgreSQL, MySQL, SQLite, SQL Server, Oracle) have slight syntax variations. This reference covers ANSI SQL with common extensions.

Concepts: tables, rows, columns, primary keys, foreign keys, indexes, ACID transactions, normalization.


## Basic Commands

```sql
-- Connect and list
\c mydb          -- psql: connect to database
SHOW DATABASES;  -- MySQL
\l               -- psql: list databases
\dt              -- psql: list tables

-- Create database
CREATE DATABASE myapp;
USE myapp;       -- MySQL

-- Show table structure
DESCRIBE users;  -- MySQL
\d users         -- psql
```


---

# CHAPTER 2: DATA DEFINITION LANGUAGE (DDL)


## Creating and Modifying Tables

```sql
-- CREATE TABLE
CREATE TABLE users (
    id          SERIAL PRIMARY KEY,     -- auto-increment (PostgreSQL)
    -- id       INT AUTO_INCREMENT PRIMARY KEY,  -- MySQL
    username    VARCHAR(50)  NOT NULL UNIQUE,
    email       VARCHAR(255) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    age         INT          CHECK (age >= 0 AND age <= 150),
    role        VARCHAR(20)  NOT NULL DEFAULT 'user',
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id          SERIAL PRIMARY KEY,
    user_id     INT     NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title       VARCHAR(200) NOT NULL,
    content     TEXT,
    published   BOOLEAN      DEFAULT FALSE,
    created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tags (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Many-to-many junction table
CREATE TABLE post_tags (
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    tag_id  INT REFERENCES tags(id)  ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);

-- ALTER TABLE
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users DROP COLUMN phone;
ALTER TABLE users ALTER COLUMN role SET DEFAULT 'member';
ALTER TABLE users RENAME COLUMN username TO user_name;
ALTER TABLE users ADD CONSTRAINT chk_age CHECK (age >= 18);

-- DROP TABLE
DROP TABLE IF EXISTS temp_table;
DROP TABLE posts CASCADE;   -- drop dependent objects

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE INDEX idx_posts_user_date ON posts(user_id, created_at DESC);
DROP INDEX idx_users_email;
```


---

# CHAPTER 3: DATA MANIPULATION LANGUAGE (DML)


## INSERT, UPDATE, DELETE

```sql
-- INSERT
INSERT INTO users (username, email, password, role)
VALUES ('alice', 'alice@example.com', 'hashed_pw', 'admin');

-- Insert multiple rows
INSERT INTO tags (name) VALUES
    ('technology'),
    ('science'),
    ('art'),
    ('sports');

-- Insert with subquery
INSERT INTO archive_users (id, username, email)
SELECT id, username, email FROM users WHERE is_active = FALSE;

-- INSERT ... ON CONFLICT (PostgreSQL UPSERT)
INSERT INTO users (username, email, password)
VALUES ('alice', 'alice@example.com', 'new_hash')
ON CONFLICT (username) DO UPDATE
    SET email = EXCLUDED.email,
        updated_at = NOW();

-- UPDATE
UPDATE users
SET is_active = TRUE,
    updated_at = NOW()
WHERE id = 5;

UPDATE posts p
SET content = content || ' [UPDATED]'
FROM users u
WHERE p.user_id = u.id AND u.role = 'admin';

-- DELETE
DELETE FROM users WHERE id = 10;
DELETE FROM posts WHERE created_at < NOW() - INTERVAL '1 year';

-- TRUNCATE (fast delete all rows)
TRUNCATE TABLE temp_data;
TRUNCATE TABLE temp_data RESTART IDENTITY CASCADE;
```


---

# CHAPTER 4: QUERYING DATA


## SELECT Statements

```sql
-- Basic SELECT
SELECT * FROM users;
SELECT id, username, email FROM users;

-- Aliases
SELECT username AS name,
       email    AS contact,
       age * 12 AS months_old
FROM users;

-- WHERE conditions
SELECT * FROM users
WHERE age > 18
  AND role = 'admin'
  AND is_active = TRUE;

SELECT * FROM users WHERE age BETWEEN 18 AND 65;
SELECT * FROM users WHERE role IN ('admin', 'moderator', 'editor');
SELECT * FROM users WHERE email LIKE '%@gmail.com';
SELECT * FROM users WHERE email ILIKE '%@gmail%';   -- case-insensitive
SELECT * FROM users WHERE phone IS NULL;
SELECT * FROM users WHERE phone IS NOT NULL;

-- DISTINCT
SELECT DISTINCT role FROM users;
SELECT DISTINCT ON (user_id) user_id, title, created_at
FROM posts ORDER BY user_id, created_at DESC;

-- ORDER BY
SELECT * FROM users ORDER BY age DESC, username ASC;

-- LIMIT and OFFSET (pagination)
SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 20;
-- Page 3 with 10 per page: OFFSET 20

-- CASE expression
SELECT username,
    CASE
        WHEN age < 18  THEN 'minor'
        WHEN age < 65  THEN 'adult'
        ELSE 'senior'
    END AS age_group
FROM users;

-- Aggregate functions
SELECT COUNT(*)       FROM users;
SELECT COUNT(phone)   FROM users;   -- counts non-null
SELECT SUM(salary)    FROM employees;
SELECT AVG(age)       FROM users;
SELECT MIN(age), MAX(age) FROM users;
SELECT STRING_AGG(username, ', ') FROM users;  -- PostgreSQL
SELECT GROUP_CONCAT(username)      FROM users; -- MySQL

-- GROUP BY
SELECT role, COUNT(*) AS count, AVG(age) AS avg_age
FROM users
GROUP BY role;

-- HAVING (filter on aggregates)
SELECT role, COUNT(*) AS cnt
FROM users
GROUP BY role
HAVING COUNT(*) > 5
ORDER BY cnt DESC;
```


---

# CHAPTER 5: JOINS


## Combining Tables

```sql
-- INNER JOIN (only matching rows)
SELECT u.username, p.title
FROM users u
INNER JOIN posts p ON p.user_id = u.id;

-- LEFT JOIN (all from left, matching from right)
SELECT u.username, COUNT(p.id) AS post_count
FROM users u
LEFT JOIN posts p ON p.user_id = u.id
GROUP BY u.id, u.username;

-- RIGHT JOIN (all from right)
SELECT * FROM posts p
RIGHT JOIN users u ON p.user_id = u.id;

-- FULL OUTER JOIN (all from both)
SELECT u.username, p.title
FROM users u
FULL OUTER JOIN posts p ON p.user_id = u.id;

-- CROSS JOIN (cartesian product)
SELECT u.username, t.name
FROM users u CROSS JOIN tags t;

-- Self join
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- Multiple joins
SELECT u.username, p.title, t.name AS tag
FROM users u
JOIN posts p ON p.user_id = u.id
JOIN post_tags pt ON pt.post_id = p.id
JOIN tags t ON t.id = pt.tag_id
WHERE u.is_active = TRUE
ORDER BY p.created_at DESC;
```


---

# CHAPTER 6: SUBQUERIES AND CTEs


## Advanced Querying

```sql
-- Subquery in WHERE
SELECT * FROM users
WHERE id IN (SELECT DISTINCT user_id FROM posts WHERE published = TRUE);

-- Subquery in FROM
SELECT dept, avg_salary
FROM (
    SELECT department AS dept, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
) sub
WHERE avg_salary > 50000;

-- Correlated subquery
SELECT u.username, u.age
FROM users u
WHERE u.age > (SELECT AVG(age) FROM users WHERE role = u.role);

-- EXISTS
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM posts p WHERE p.user_id = u.id AND p.published = TRUE
);

-- CTE (Common Table Expression)
WITH active_users AS (
    SELECT id, username, email FROM users WHERE is_active = TRUE
),
user_posts AS (
    SELECT user_id, COUNT(*) AS post_count FROM posts GROUP BY user_id
)
SELECT u.username, COALESCE(up.post_count, 0) AS posts
FROM active_users u
LEFT JOIN user_posts up ON up.user_id = u.id
ORDER BY posts DESC;

-- Recursive CTE (hierarchical data)
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 0 AS depth
    FROM categories WHERE parent_id IS NULL
    
    UNION ALL
    
    SELECT c.id, c.name, c.parent_id, ct.depth + 1
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT *, REPEAT('  ', depth) || name AS indented_name
FROM category_tree ORDER BY id;
```


---

# CHAPTER 7: WINDOW FUNCTIONS


## Analytical Functions

```sql
-- ROW_NUMBER, RANK, DENSE_RANK
SELECT username, score,
    ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num,
    RANK()       OVER (ORDER BY score DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank
FROM leaderboard;

-- PARTITION BY (per group)
SELECT username, department, salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;

-- LAG and LEAD (access adjacent rows)
SELECT date, revenue,
    LAG(revenue, 1) OVER (ORDER BY date) AS prev_revenue,
    revenue - LAG(revenue, 1) OVER (ORDER BY date) AS change,
    LEAD(revenue, 1) OVER (ORDER BY date) AS next_revenue
FROM sales;

-- Running totals and moving averages
SELECT date, revenue,
    SUM(revenue) OVER (ORDER BY date) AS cumulative,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM sales;

-- NTILE (quartiles/percentiles)
SELECT username, score,
    NTILE(4) OVER (ORDER BY score) AS quartile
FROM scores;

-- FIRST_VALUE, LAST_VALUE
SELECT department, employee, salary,
    FIRST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary DESC) AS dept_max_salary
FROM employees;
```


---

# CHAPTER 8: TRANSACTIONS AND INDEXES


## ACID Transactions

```sql
-- Transaction
BEGIN;
-- or START TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT;
-- or ROLLBACK;

-- Savepoints
BEGIN;
UPDATE users SET role = 'admin' WHERE id = 5;
SAVEPOINT my_savepoint;
UPDATE users SET role = 'superadmin' WHERE id = 5;
ROLLBACK TO SAVEPOINT my_savepoint;  -- undo last update
COMMIT;

-- Isolation levels
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_created ON posts(created_at DESC);
CREATE INDEX idx_partial ON users(email) WHERE is_active = TRUE;
CREATE INDEX idx_composite ON orders(customer_id, created_at);
CREATE INDEX idx_expression ON users(LOWER(email));

EXPLAIN SELECT * FROM users WHERE email = 'alice@example.com';
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@example.com';

-- Views
CREATE VIEW active_users AS
    SELECT id, username, email FROM users WHERE is_active = TRUE;

CREATE MATERIALIZED VIEW user_stats AS
    SELECT u.id, u.username, COUNT(p.id) AS post_count
    FROM users u LEFT JOIN posts p ON p.user_id = u.id
    GROUP BY u.id, u.username;

REFRESH MATERIALIZED VIEW user_stats;

-- Stored procedure (PostgreSQL)
CREATE OR REPLACE FUNCTION get_user_posts(user_id INT)
RETURNS TABLE(post_id INT, title VARCHAR, created_at TIMESTAMP) AS $$
BEGIN
    RETURN QUERY
    SELECT id, title, created_at
    FROM posts
    WHERE posts.user_id = $1 AND published = TRUE
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_user_posts(5);
```
