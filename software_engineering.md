# Software Engineering — Real Applications Complete Reference

## Building Real Applications — Architecture Overview

Every real application has layers:
1. Presentation layer (UI / API endpoints)
2. Business logic layer (services, use cases)
3. Data access layer (repositories, ORM)
4. Infrastructure (database, cache, message queue, file storage, email)

Separation of concerns: each layer knows only about the layer below it. Business logic never talks directly to the database. UI never contains business rules.

Environment stages: Development → Testing/Staging → Production. Never deploy untested code to production. Use environment variables for secrets and config — never hardcode.

## Databases in Real Applications

### Relational Databases (SQL)
PostgreSQL, MySQL, SQLite, SQL Server, Oracle.

Schema design:
- Normalize to at least 3NF: eliminate data redundancy.
- 1NF: atomic values, no repeating groups.
- 2NF: 1NF + no partial dependencies on composite keys.
- 3NF: 2NF + no transitive dependencies.
- Denormalize only for read performance when justified.

Indexes: speed up reads at the cost of slower writes and disk space.
- B-tree index (default): great for equality and range queries.
- Hash index: only equality. Not persistent in some DBs.
- Composite index: index on multiple columns. Order matters — leftmost columns are used first.
- Covering index: all needed columns in the index; no table lookup needed.
- Full-text index: for text search.
- Unique index: enforces uniqueness + speeds up lookup.

EXPLAIN / EXPLAIN ANALYZE: show query execution plan. Identify slow queries and missing indexes.

Transactions and ACID:
- Atomicity: all operations succeed or all fail together.
- Consistency: transaction brings DB from one valid state to another.
- Isolation: concurrent transactions don't interfere.
- Durability: committed data persists through failures.

Isolation levels (weakest to strongest):
- Read Uncommitted: can read dirty (uncommitted) data.
- Read Committed: only reads committed data. Prevents dirty reads.
- Repeatable Read: same row gives same data within transaction. Prevents non-repeatable reads.
- Serializable: complete isolation. Prevents phantom reads. Slowest.

Connection pooling: reuse database connections instead of opening new ones per request. PgBouncer, HikariCP, SQLAlchemy pool.

N+1 query problem: fetching 1 list then N queries for each item. Fix with JOIN or eager loading.

ORM (Object-Relational Mapper): maps classes to tables. SQLAlchemy (Python), Hibernate (Java), Entity Framework (.NET), ActiveRecord (Rails), Prisma (Node.js).
Pros: less boilerplate, database agnostic. Cons: can hide performance issues, less control.

Migrations: version-controlled, incremental changes to the database schema. Never edit the database directly in production. Tools: Flyway, Liquibase, Alembic, Rails migrations.

### NoSQL Databases
Use when: need horizontal scaling, flexible schema, specific data access patterns.

Document store (MongoDB, CouchDB, Firestore):
- Data stored as JSON/BSON documents.
- No fixed schema. Nested documents and arrays.
- Best for: content management, user profiles, catalogs.
- Index on any field. Aggregation pipeline for complex queries.

Key-value store (Redis, DynamoDB, Memcached):
- Simple key → value mapping. Extremely fast O(1).
- Redis also supports: lists, sets, sorted sets, hashes, streams, pub/sub.
- Best for: caching, sessions, real-time leaderboards, queues, rate limiting.

Wide-column store (Cassandra, HBase):
- Data stored in rows and dynamic columns. Optimized for writes.
- Best for: time-series data, IoT, event logs, write-heavy workloads.
- Design around query patterns, not normalization.

Graph database (Neo4j, Amazon Neptune):
- Data as nodes and edges. Traverse relationships efficiently.
- Best for: social networks, recommendation engines, fraud detection, knowledge graphs.

Search engines (Elasticsearch, Solr, Meilisearch):
- Full-text search, fuzzy matching, faceted search, relevance ranking.
- Built on inverted indexes. Near real-time. Horizontally scalable.

## Caching

Why cache: avoid recomputing expensive results, reduce database load, reduce latency.

Cache levels:
1. In-memory (within process): Python dict, HashMap. Fastest. Lost on restart.
2. Distributed cache: Redis, Memcached. Shared between instances.
3. CDN (Content Delivery Network): cache static assets at edge servers geographically.
4. HTTP cache: browser caches responses using Cache-Control headers.

Cache strategies:
- Cache-aside (lazy loading): app checks cache first; on miss, reads from DB and populates cache.
- Write-through: write to cache and DB simultaneously. Always consistent. Slower writes.
- Write-behind (write-back): write to cache immediately; write to DB asynchronously. Risk of data loss.
- Read-through: cache sits in front of DB, fetches automatically on miss.

Cache invalidation: one of the hardest problems in CS. Strategies:
- TTL (time-to-live): expire after a fixed duration. Simple but may serve stale data.
- Event-based: invalidate when the underlying data changes.
- Cache versioning: include version in cache key. Old versions naturally expire.

Cache stampede: many requests miss cache simultaneously, all hit DB. Fix with locking, probabilistic early expiration.
Cache eviction policies: LRU (Least Recently Used), LFU (Least Frequently Used), FIFO, Random.

Redis data structures for real applications:
- String: counters, sessions, simple cache. INCR, DECR for atomic counters.
- Hash: user objects, settings. HGET, HSET.
- List: queues, activity feeds. LPUSH, RPOP.
- Set: unique visitors, tags. SADD, SMEMBERS, SINTER.
- Sorted Set: leaderboards, rate limiting. ZADD, ZRANGE.
- Streams: event log, message queue. XADD, XREAD.

## Authentication and Security

### Authentication
Authentication: proving who you are. Authorization: proving what you can do.

Password storage: NEVER store plaintext passwords.
- Use bcrypt, scrypt, or Argon2 (memory-hard hashing functions designed for passwords).
- Add a random salt per user. Hash = bcrypt(password + salt, cost=12).
- PBKDF2 is acceptable but bcrypt/Argon2 are preferred.
- SHA-256/MD5 alone are NOT sufficient for passwords.

Session-based auth: server stores session in DB/Redis; client gets session ID cookie.
- Set cookie as HttpOnly (no JS access) and Secure (HTTPS only).
- Regenerate session ID after login to prevent session fixation.

JWT (JSON Web Token): self-contained token with encoded claims. Server doesn't need to store sessions.
- Structure: Header.Payload.Signature (base64url encoded).
- Signed with HMAC-SHA256 or RSA. Verify signature on each request.
- Store in HttpOnly cookie (not localStorage — XSS vulnerable) or Authorization header.
- Short expiry (15min) + refresh token (7 days, stored in HttpOnly cookie).
- Revoking JWTs is hard — use a blocklist or short expiry.

OAuth 2.0: authorization framework for delegated access.
- Authorization Code Flow (web apps): most secure, uses PKCE.
- Client Credentials Flow (machine-to-machine): no user involved.
- Implicit Flow: deprecated. Do not use.
Providers: Google, GitHub, Facebook, Auth0, Okta.

OIDC (OpenID Connect): identity layer on top of OAuth 2.0. Returns ID token (JWT with user info).

MFA (Multi-Factor Authentication): something you know + something you have (TOTP, SMS, hardware key).
TOTP: Time-based One-Time Password. RFC 6238. Apps: Google Authenticator, Authy.

### Web Security
OWASP Top 10 vulnerabilities:

1. Injection (SQL, NoSQL, OS, LDAP): attacker inserts malicious code into a query.
   Prevention: parameterized queries / prepared statements. NEVER string-concatenate user input into SQL.
   ```python
   # WRONG: cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
   # RIGHT: cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
   ```

2. Broken Authentication: weak passwords, no MFA, insecure session management.
   Prevention: bcrypt, MFA, secure session handling, account lockout.

3. XSS (Cross-Site Scripting): attacker injects client-side scripts.
   Prevention: escape/encode all output. Content Security Policy (CSP) header. HttpOnly cookies.

4. CSRF (Cross-Site Request Forgery): trick user's browser into making unwanted requests.
   Prevention: CSRF tokens in forms. SameSite cookie attribute. Verify Origin header.

5. Insecure Direct Object References (IDOR): user can access others' data by changing an ID.
   Prevention: always check authorization — "can THIS user access THIS resource?".

6. Security Misconfiguration: default passwords, unnecessary services, verbose error messages.
   Prevention: principle of least privilege, disable debug in production, security headers.

7. Sensitive Data Exposure: transmitting or storing data unencrypted.
   Prevention: HTTPS everywhere, encrypt at rest, don't log sensitive data.

8. Broken Access Control: users can access unauthorized functionality.
   Prevention: deny by default, check permissions on every request server-side.

HTTP Security Headers:
- Content-Security-Policy: restricts sources for scripts, styles, images.
- X-Content-Type-Options: nosniff — prevents MIME type sniffing.
- X-Frame-Options: DENY — prevents clickjacking.
- Strict-Transport-Security (HSTS): force HTTPS.
- Referrer-Policy: control what referrer info is sent.

Rate limiting: prevent brute force and DoS. Limit by IP, user, or endpoint. Redis sorted sets work well.

Input validation: validate on the server side always (never trust client-side only). Whitelist expected formats. Sanitize before storing.

## APIs and Web Servers

### HTTP Fundamentals
Request parts: Method, URL, Headers, Body.
Response parts: Status code, Headers, Body.

Content-Type: tells receiver how to parse body. application/json, multipart/form-data, application/x-www-form-urlencoded.

CORS (Cross-Origin Resource Sharing): browser security policy. Server must send Access-Control-Allow-Origin header to permit cross-origin requests.
Preflight request: browser sends OPTIONS request before cross-origin POST/PUT/DELETE.

HTTP/2: multiplexing (multiple requests on one connection), header compression, server push. Significant performance improvement.
HTTP/3: based on QUIC (UDP), even better for lossy connections.

### Building REST APIs
Validation: validate input before processing. Return 400 with clear error messages.
Pagination: never return unlimited results. Offset pagination or cursor-based (for large/changing datasets).
Filtering and sorting: allow via query parameters.
Versioning: /api/v1/... Allows breaking changes without affecting existing clients.
Error responses: consistent format. Include error code, message, and optional details.
```json
{"error": {"code": "USER_NOT_FOUND", "message": "No user with id 123"}}
```

OpenAPI / Swagger: standard format for documenting REST APIs. Auto-generate client SDKs and docs.

### Web Frameworks
Python: FastAPI (async, auto docs, type hints), Django (batteries-included), Flask (minimal).
Node.js: Express (minimal), NestJS (structured, TypeScript), Fastify (performance).
Java/Kotlin: Spring Boot (enterprise), Quarkus (cloud-native).
Go: Gin, Echo, Fiber — minimal and fast.
Ruby: Rails (convention over configuration, rapid development).
.NET: ASP.NET Core — cross-platform, high performance.

## Message Queues and Async Processing

Why async: long-running tasks (email, image processing, reports) should not block the HTTP response. Decouple producers from consumers. Handle traffic spikes.

Message queue concepts:
- Producer: sends messages to the queue.
- Consumer (worker): picks up and processes messages.
- Queue: persists messages until consumed.
- Dead letter queue (DLQ): holds failed messages for inspection.
- Acknowledgment: consumer confirms message processed; otherwise it's re-delivered.
- At-least-once delivery: message delivered at least once (possible duplicates). Make consumers idempotent.
- Exactly-once delivery: guaranteed once but complex and slower.

Tools:
- RabbitMQ: flexible routing, multiple exchange types (direct, fanout, topic). AMQP protocol.
- Kafka: high-throughput log-based streaming. Consumers can re-read messages. Great for event sourcing and analytics.
- SQS (AWS): managed, simple, scalable.
- Redis Streams / Bull: lightweight queue for smaller scale.
- Celery (Python): task queue with RabbitMQ or Redis backend.

Background jobs: send email, resize images, generate PDFs, sync with external APIs, run scheduled reports.

## Containerization and Deployment

### Docker
Container: isolated process with its own filesystem, network, and process space. Consistent environment from dev to prod.

Dockerfile:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Key commands: docker build, docker run, docker ps, docker logs, docker exec, docker stop.
Docker Compose: define multi-container apps (app + db + redis + nginx) in docker-compose.yml. docker-compose up.
Best practices: use official base images, minimize layers, don't run as root, use .dockerignore, multi-stage builds.

### Kubernetes (K8s)
Orchestrates containers at scale. Handles deployment, scaling, load balancing, self-healing.
Pod: smallest unit; one or more containers sharing network and storage.
Deployment: manages pods, rolling updates, rollbacks.
Service: stable network endpoint; load balances across pods.
Ingress: HTTP routing rules, TLS termination.
ConfigMap / Secret: inject configuration and secrets into pods.
Horizontal Pod Autoscaler: scale pods based on CPU/memory.

### CI/CD — Continuous Integration / Continuous Deployment
CI: automatically build, test, and lint code on every commit.
CD: automatically deploy to staging/production after CI passes.

Pipeline stages: checkout → install deps → lint → unit tests → integration tests → build → deploy.

Tools: GitHub Actions, GitLab CI, Jenkins, CircleCI, Travis CI.

GitHub Actions example:
```yaml
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install -r requirements.txt
      - run: pytest
```

Deployment strategies:
- Blue-Green: run two identical environments; switch traffic instantly.
- Canary: send small percentage of traffic to new version first.
- Rolling: gradually replace old instances with new ones. Zero downtime.
- Feature flags: deploy code disabled; enable per-user or percentage.

## Logging, Monitoring, and Observability

The three pillars of observability:

Logs: timestamped records of events. Use structured logging (JSON). Include: timestamp, level, message, request ID, user ID, stack trace for errors.
Log levels: DEBUG (verbose dev info) → INFO (normal operation) → WARNING (unexpected but handled) → ERROR (failure, needs attention) → CRITICAL (system down).
Tools: ELK stack (Elasticsearch + Logstash + Kibana), Loki + Grafana, Datadog, Splunk.

Metrics: numerical measurements over time. CPU, memory, request rate, error rate, response time.
Key metrics (RED method): Rate (requests/sec), Errors (error rate), Duration (latency).
Tools: Prometheus + Grafana, Datadog, CloudWatch, New Relic.

Traces: follow a request through multiple services. Distributed tracing.
Tools: Jaeger, Zipkin, OpenTelemetry, Datadog APM.

Alerts: notify on-call engineer when metrics exceed thresholds. Avoid alert fatigue — only alert on actionable issues.

Health checks: /health endpoint returns 200 if service is operational. Kubernetes uses these for liveness and readiness probes.

## Performance and Scalability

Horizontal scaling (scale out): add more servers. Requires stateless services (sessions in Redis, not in-memory).
Vertical scaling (scale up): bigger server. Simpler but has limits.

Load balancing: distribute traffic across instances. Round-robin, least connections, IP hash, weighted.
Tools: Nginx, HAProxy, AWS ALB/NLB, Cloudflare.

Database scaling:
- Read replicas: offload read queries. Primary handles writes, replicas serve reads.
- Sharding: split data across multiple databases by a shard key. Complex.
- Connection pooling: reuse connections, reduce overhead.

Latency vs throughput: latency = time for one request. Throughput = requests per second.
Caching reduces both latency and database load.

N+1 problem: fetching a list then querying DB for each item. Fix: JOIN, batch fetch, DataLoader (GraphQL).

Profiling: measure where time is spent. Python: cProfile, py-spy. Java: VisualVM, async-profiler. Node: --prof flag.

CDN (Content Delivery Network): serve static assets (images, JS, CSS) from edge nodes close to users. CloudFlare, AWS CloudFront, Fastly.

Async/non-blocking I/O: Node.js, Python asyncio, Go goroutines — handle many concurrent connections without threads.

## Version Control with Git

Branching strategies:
- Git Flow: main + develop + feature/release/hotfix branches. Good for versioned releases.
- GitHub Flow: main + feature branches. Simple, continuous deployment.
- Trunk-Based Development: everyone commits to main frequently. Feature flags for unfinished features.

Good commit messages: imperative mood ("Fix bug" not "Fixed bug"). Subject line ≤ 72 chars. Body explains WHY not WHAT.

Pull Request best practices: small PRs, meaningful description, screenshots for UI, tests included, link to issue.

Code review: check for correctness, security, performance, readability, edge cases. Nitpicks should be labeled.

Git commands reference:
- git stash / git stash pop — save/restore uncommitted work.
- git rebase -i — interactive rebase to clean up commits.
- git cherry-pick — apply specific commit to another branch.
- git bisect — binary search through commits to find which introduced a bug.
- git reflog — history of HEAD movements (recover lost commits).

Semantic versioning (SemVer): MAJOR.MINOR.PATCH.
MAJOR: breaking changes. MINOR: new features, backward-compatible. PATCH: bug fixes.

## System Design Concepts

CAP Theorem: distributed system can guarantee only 2 of 3:
- Consistency: all nodes see the same data.
- Availability: every request gets a response.
- Partition tolerance: system works despite network failures.
Network partitions always happen, so real choice is CP vs AP.

BASE (vs ACID): Basically Available, Soft state, Eventually consistent. Common in NoSQL.

Eventual consistency: writes propagate to all nodes over time. Reads may be stale temporarily.

Back-of-envelope estimation:
- 1 byte = 8 bits. 1 KB = 1,024 bytes. 1 MB = 10⁶ bytes. 1 GB = 10⁹ bytes.
- SSD read: ~0.1ms. Network within datacenter: ~1ms. Cross-region: ~100ms.
- 1 million requests/day ≈ 12 requests/second.
- Average HTTP request: 1KB. 1 million daily users × 1KB = 1GB/day data.

Rate limiting algorithms:
- Token bucket: tokens refill at fixed rate; each request consumes one.
- Leaky bucket: requests drain at fixed rate; excess queued or dropped.
- Sliding window: count requests in rolling time window.

Consistent hashing: distribute data across nodes such that only K/n keys move when a node is added/removed (K = keys, n = nodes). Used in distributed caches and databases.

Idempotency: operation can be applied multiple times with same result. Important for retries.
Idempotency key: unique ID with each request; server ignores duplicates.
