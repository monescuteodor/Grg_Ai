# System Design Complete Reference


---

# CHAPTER 1: FOUNDATIONS


## Remarks

System design is the art of architecting scalable, reliable, maintainable software systems. It's the bread and butter of senior engineers and a critical skill for FAANG-style interviews (Google, Meta, Amazon, Netflix). Unlike coding, there's no single correct answer — design involves trade-offs across performance, cost, complexity, and team capability.

Key concepts: **Scalability** (handle more load), **Reliability** (keep working under failure), **Availability** (uptime, e.g. 99.9%), **Latency vs Throughput** (speed of one request vs total requests/sec), **Consistency vs Availability** (CAP theorem), **Vertical vs Horizontal scaling** (bigger machine vs more machines).

Used in: every backend system. Every interview at Google/Meta/Amazon/Stripe asks system design.

Tools mentioned: **Load balancers** (NGINX, HAProxy, AWS ALB), **Caches** (Redis, Memcached), **Databases** (PostgreSQL, MySQL, MongoDB, Cassandra), **Message queues** (Kafka, RabbitMQ, SQS), **CDNs** (Cloudflare, CloudFront).


## Core Metrics

```
LATENCY    = Time for one request (ms)
             Example: API responds in 200ms

THROUGHPUT = Requests per second (RPS, QPS)
             Example: 10,000 requests/sec

AVAILABILITY = Uptime percentage
  99%       = 87 hours down/year  (1 day, 14 hours)
  99.9%     = 8.7 hours down/year (3 nines)
  99.99%    = 52 minutes down/year (4 nines)
  99.999%   = 5 minutes down/year  (5 nines, "five nines")
  99.9999%  = 31 seconds down/year (six nines, very expensive)

RTT (Round Trip Time): time for packet to go to server and back

PERCENTILES (real-world):
  p50 (median)  = 50% of requests faster than this
  p95           = 95% of requests faster
  p99           = 99% faster (1% slower - tail latency)
  p99.9         = 99.9% faster (worst case still important)
```


## Back-of-the-Envelope Calculations

```
Critical numbers to know (latency):
  L1 cache:           1 ns
  L2 cache:           10 ns
  RAM access:         100 ns       (1000x slower than L1!)
  SSD random read:    100 us       (= 0.1 ms)
  HDD random seek:    10 ms        (100x slower than SSD)
  Network round-trip
    same datacenter:  500 us       (0.5 ms)
    same continent:   30-50 ms
    cross-continent:  150-200 ms
  HTTP request:       1-100 ms typical

Throughput estimates:
  Single SSD:         100,000 IOPS, ~500 MB/s
  Single HDD:         100 IOPS, ~100 MB/s
  10 Gbps network:    1.25 GB/s

Memory sizes:
  L1 cache:           32-64 KB per core
  L2 cache:           256 KB - 1 MB per core
  L3 cache:           4-64 MB shared
  RAM (modern server): 64 GB - 2 TB

Sample calculation: Twitter-scale tweet storage
  - 500M users × 10 tweets/day = 5B tweets/day
  - 5B tweets × 280 chars × 2 bytes (UTF-16) = 2.8 TB/day text
  - With metadata, indexes, replicas: ~10 TB/day
  - Yearly: ~3.6 PB
```


---

# CHAPTER 2: SCALING PATTERNS


## Vertical vs Horizontal Scaling

```
VERTICAL SCALING (Scale UP)
  - Bigger server: more CPU, RAM, faster disks
  - Pros: Simple, no code changes
  - Cons: Limit ~$50K for single server, single point of failure
  - When to use: <1M users, simple architecture

HORIZONTAL SCALING (Scale OUT)
  - More servers: distribute load
  - Pros: Effectively unlimited scale, fault tolerant
  - Cons: Complex (consistency, coordination, network)
  - When to use: >1M users, need high availability

Most modern systems: combine both. Scale up first (cheaper), then out.
```


## Load Balancing

```
LOAD BALANCER (LB)
  Distributes incoming traffic across multiple backend servers.

Layer 4 (TCP/transport):
  - Fast (works at packet level)
  - Doesn't see HTTP content
  - Example: AWS NLB, IPVS

Layer 7 (HTTP/application):
  - Routes based on URL, headers, cookies
  - SSL termination
  - Example: NGINX, HAProxy, AWS ALB, Cloudflare

ALGORITHMS:
  Round-robin:          Server 1, 2, 3, 1, 2, 3...
  Least connections:    Send to server with fewest active connections
  Least response time:  Server that's fastest right now
  IP hash:              Same client → same server (session affinity)
  Random:               Pick randomly (surprisingly effective)
  Weighted:             Bigger servers get more traffic

HEALTH CHECKS:
  LB pings backends every N seconds
  GET /health → 200 OK = healthy
  Mark unhealthy after K failures
  Remove from rotation, retry until healthy
```


### Example NGINX Load Balancer Config

```nginx
upstream backend {
    least_conn;                          # Algorithm
    server backend1.example.com:8080 weight=3;
    server backend2.example.com:8080 weight=1;
    server backend3.example.com:8080 backup;   # Only if others down
}

server {
    listen 80;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    location /health {
        access_log off;
        return 200 "OK\n";
    }
}
```


## Caching

```
WHY CACHE?
  - DB query: 50ms      vs    Redis: 0.5ms     (100x speedup)
  - Reduces load on origin (database, external API)
  - Lower latency for users

CACHE LEVELS (closer to user = faster):
  1. Browser cache         (in user's browser)
  2. CDN cache             (Cloudflare, AWS CloudFront)
  3. Reverse proxy cache   (NGINX, Varnish)
  4. Application cache     (Redis, Memcached)
  5. Database query cache  (MySQL query cache)
  6. Database disk cache   (OS page cache)

CACHE PATTERNS:
  Cache-aside (lazy load):
    1. App reads from cache
    2. Cache miss → fetch from DB
    3. App writes result to cache
    4. Return result
    Common, simple, can have stale data.

  Read-through:
    Cache is in front of DB; cache fetches on miss.
    Same end result but logic in cache.

  Write-through:
    App writes to cache AND DB synchronously.
    Slower writes, consistent.

  Write-behind (write-back):
    App writes to cache; cache writes to DB async later.
    Fast writes, risk of data loss on crash.

  Refresh-ahead:
    Cache predicts what's needed and refreshes BEFORE expiry.
    Complex but smooth UX.
```


### Cache Eviction Policies

```
LRU (Least Recently Used):
  Evict the item that hasn't been accessed for the longest.
  Good general default. Used by Redis, browsers.

LFU (Least Frequently Used):
  Evict the item accessed fewest times.
  Better when popularity skewed (long tail).

FIFO (First In First Out):
  Evict the oldest item by insertion time.
  Simple but ignores access patterns.

TTL (Time To Live):
  Each item expires after N seconds.
  Required for stale data prevention.

Random:
  Surprisingly effective for some workloads.
```


### Redis Caching Example

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_user(user_id: int) -> dict:
    cache_key = f"user:{user_id}"

    # 1. Try cache first
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    # 2. Cache miss - hit DB
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    if user is None:
        return None

    # 3. Write to cache with TTL
    r.setex(cache_key, 3600, json.dumps(user))   # 1 hour TTL

    return user

def update_user(user_id: int, **fields):
    # Update DB
    db.update("UPDATE users SET ... WHERE id = ?", user_id)
    # INVALIDATE cache (don't update, just delete)
    r.delete(f"user:{user_id}")
```


## Content Delivery Networks (CDN)

```
WHAT IS A CDN?
  Network of servers around the world (edge locations).
  Caches static content close to users.
  Reduces latency, offloads origin server.

USE FOR:
  - Static assets: images, CSS, JS, fonts, videos
  - HTML pages (with caution - need cache invalidation)
  - API responses (rarely-changing endpoints)

CACHE HEADERS:
  Cache-Control: public, max-age=31536000        # 1 year
  Cache-Control: private, no-cache               # Don't cache
  Cache-Control: must-revalidate                 # Check with origin
  ETag: "abc123"                                 # Version identifier
  Last-Modified: Mon, 9 Jun 2026 12:00:00 GMT

POPULAR CDNs:
  - Cloudflare        (free tier, popular for indie projects)
  - AWS CloudFront    (integrates with AWS)
  - Fastly            (very fast, programmable)
  - Akamai            (enterprise, oldest)
  - Bunny.net         (cheap, good performance)

CDN cache levels (from edge to origin):
  Browser → CDN edge → CDN regional → Origin server

INVALIDATION:
  - Purge specific URLs
  - Purge by tag
  - Wait for TTL expiry
  - Use versioned URLs (app.v3.js) - no invalidation needed!
```


---

# CHAPTER 3: DATABASES


## SQL vs NoSQL

```
SQL (Relational):
  PostgreSQL, MySQL, SQLite, MariaDB, SQL Server, Oracle

  Strengths:
    - ACID transactions
    - Complex joins, aggregations
    - Strong consistency
    - Mature, well-understood
    - SQL standard query language

  Weaknesses:
    - Harder to scale horizontally (sharding complex)
    - Schema changes can be slow
    - Vertical limits (~1 TB on single instance comfortable)

  Use when:
    - Complex relationships (e-commerce, banking)
    - Need ACID (financial transactions)
    - Reporting and analytics
    - Schema is stable and well-known

NoSQL (Non-relational):
  Document:    MongoDB, CouchDB, Firestore
  Key-Value:   Redis, DynamoDB, Riak
  Column:      Cassandra, ScyllaDB, HBase, BigTable
  Graph:       Neo4j, ArangoDB

  Strengths:
    - Designed to scale horizontally
    - Flexible schema (evolving data)
    - High write throughput
    - Often simpler operations

  Weaknesses:
    - No joins (denormalize or app-level)
    - Often eventual consistency
    - Less mature tooling
    - Query language varies

  Use when:
    - Massive scale (>100M users)
    - High write volume (logs, events)
    - Flexible/changing schema
    - Specific access patterns known upfront
```


## Database Indexing

```
WHAT IS AN INDEX?
  Data structure (usually B-tree or hash) that makes lookups fast.
  Like a book's index: don't read every page, jump to right page.

WITHOUT INDEX:
  SELECT * FROM users WHERE email = 'alice@example.com';
  → Full table scan: O(n)
  → 10M rows = 10M comparisons

WITH INDEX ON email:
  → B-tree lookup: O(log n)
  → 10M rows = ~24 comparisons

COST OF INDEXES:
  - Slower INSERT/UPDATE/DELETE (must update index too)
  - Extra disk space (often 10-30% of table size)
  - More to backup

WHEN TO INDEX:
  ✅ WHERE clauses on the column
  ✅ JOIN columns
  ✅ ORDER BY columns
  ❌ Tiny tables (no benefit)
  ❌ Frequently-written, rarely-read columns
  ❌ Low cardinality (e.g. boolean: only 2 values)

COMPOSITE INDEXES:
  CREATE INDEX idx_users_country_city ON users(country, city);

  Helps queries like:
    WHERE country = ?                       ✅ Uses index
    WHERE country = ? AND city = ?          ✅ Uses index
    WHERE country = ? ORDER BY city         ✅ Uses index
    WHERE city = ?                          ❌ Doesn't help

  Order matters! Leading column first.

COVERING INDEX:
  Index that contains ALL columns needed by query.
  → DB never needs to read main table.

  CREATE INDEX idx_covering ON users(country) INCLUDE (name, email);

  SELECT name, email FROM users WHERE country = 'RO';
  → Read entirely from index, no table access
```


## Database Replication

```
PURPOSE:
  - High availability (if primary dies, replica takes over)
  - Read scaling (route reads to replicas)
  - Disaster recovery (geographically distant copies)

PRIMARY-REPLICA (Master-Slave):
  1 primary handles writes
  N replicas handle reads
  Primary streams changes to replicas

  Pros: Simple, read scales linearly
  Cons: Writes don't scale, replica lag (eventual consistency)
  
  ┌──────┐  writes  ┌──────────┐  reads  ┌────────┐
  │ App  │ ───────► │ Primary  │ ◄────── │ App    │
  └──────┘          └────┬─────┘         └────────┘
                         │ replicate
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          ┌───────┐  ┌───────┐  ┌───────┐
          │ Repl1 │  │ Repl2 │  │ Repl3 │
          └───────┘  └───────┘  └───────┘
                     reads ↑

PRIMARY-PRIMARY (Multi-Master):
  Multiple primaries accept writes
  Conflicts resolved via vector clocks / CRDTs / last-write-wins

  Pros: Higher write throughput, geographically distributed
  Cons: Complex, conflict resolution needed

REPLICATION TYPES:
  Synchronous:  Wait for replica to confirm before returning to client.
                Slower but no data loss.

  Asynchronous: Return immediately; replica catches up later.
                Faster but risk of data loss on primary failure.

  Semi-sync:    Wait for ≥1 replica to confirm.
                Compromise: speed with safety.

REPLICA LAG:
  Typical: 10-200ms
  Problems with "read your writes":
    User posts comment → next page load reads from replica → comment missing!
  Solutions:
    - Stick reads to primary briefly after writes
    - Read from primary for that user temporarily
    - Cache the user's recent writes in app
```


## Database Sharding (Partitioning)

```
PURPOSE:
  When 1 server can't hold all data or handle all writes.
  Split data across N servers ("shards").
  Each shard is independent.

SHARDING STRATEGIES:

  Range-based:
    User IDs 1-1M → shard 1
    User IDs 1M-2M → shard 2
    ...
    Pros: Simple, range queries fast
    Cons: Hotspots (new IDs all on one shard)

  Hash-based:
    shard = hash(user_id) % N
    Pros: Uniform distribution
    Cons: Range queries hit ALL shards (slow)

  Geographic:
    EU users → shard EU
    US users → shard US
    Pros: Low latency for local users, GDPR compliance
    Cons: User moves regions = complex migration

  Directory-based:
    Lookup table: user_id → shard
    Pros: Flexible, easy rebalancing
    Cons: Extra hop for lookup, lookup table = bottleneck

CONSISTENT HASHING:
  Used by Cassandra, DynamoDB.
  Adding/removing nodes moves minimal data.
  Avoids "cascading rehash" problem of mod-N hashing.

CHALLENGES:
  - Cross-shard transactions (very hard)
  - Joins across shards (often impossible in practice)
  - Resharding (expensive, often offline)
  - Distributed transactions = slow
```


## CAP Theorem

```
You cannot have ALL THREE simultaneously:
  C - Consistency      (all nodes see same data at same time)
  A - Availability     (every request gets a response)
  P - Partition tolerance (system works despite network failures)

In practice, P is unavoidable (networks fail). So choose:

CP (Consistency + Partition tolerance):
  Sacrifice availability during partitions.
  Example: bank transfers, MongoDB (default), HBase, Redis cluster
  "Better to refuse than to give wrong answer."

AP (Availability + Partition tolerance):
  Sacrifice consistency during partitions.
  Example: shopping carts, Cassandra, DynamoDB, CouchDB
  "Better to take order, fix conflicts later."

CA: Only when no partitions (impractical for distributed).

REAL-WORLD: most systems are PACELC:
  When Partition: choose A or C
  Else (normal operation): choose Latency or Consistency
```


---

# CHAPTER 4: COMMUNICATION PATTERNS


## REST vs GraphQL vs gRPC

```
REST (REpresentational State Transfer):
  GET    /users/123          # Get user
  POST   /users              # Create
  PUT    /users/123          # Update
  DELETE /users/123          # Delete

  Pros: Universal, simple, cacheable, every language supports it
  Cons: Over/under-fetching (returns all fields or multiple round-trips)
  Use for: Public APIs, simple CRUD, microservice-to-microservice

GraphQL:
  Single endpoint /graphql
  Client specifies exactly what fields to return:

    query {
      user(id: 123) {
        name
        email
        posts(limit: 5) {
          title
        }
      }
    }

  Pros: No over-fetching, strongly typed schema, one round-trip for nested data
  Cons: Complex caching, complex auth, N+1 problem if naive
  Use for: Complex frontends (mobile app + web), evolving schemas

gRPC:
  Binary protocol over HTTP/2.
  Protobuf schema → generated client/server code.
  
  Pros: Very fast (binary), streaming, strong types, multi-language
  Cons: Browser support tricky (gRPC-Web), harder to debug
  Use for: Service-to-service in microservices, high-performance

REST/GraphQL = JSON over HTTP/1.1
gRPC          = Protobuf over HTTP/2
```


## Message Queues

```
WHY USE QUEUES?
  Decouple producers from consumers.
  Smooth out spikes (buffer).
  Reliable delivery (retry on failure).
  Async processing (return to user fast).

PATTERNS:

  Point-to-point (queue):
    1 producer → queue → 1 consumer
    Each message processed once.
    Example: order processing, email sending

  Pub/Sub (topic):
    1 producer → topic → N subscribers
    Each subscriber gets every message.
    Example: event broadcasting, notifications

POPULAR QUEUES:
  RabbitMQ:    Versatile, AMQP, classic message broker
  Kafka:       High throughput, event streaming, replay
  AWS SQS:     Managed queue, simple
  Redis:       Lightweight pub/sub, lists as queues
  NATS:        Very fast, simple, modern

DELIVERY GUARANTEES:
  At-most-once:    Message might be lost (never duplicated)
  At-least-once:   Might be duplicated (never lost)  ← most common
  Exactly-once:    Theoretical ideal; complex in practice

DEAD LETTER QUEUE (DLQ):
  Messages that fail after N retries go to DLQ.
  Manual inspection / replay.
  Prevents infinite retry loops.
```


### Example: Order Processing with Queue

```python
# Producer (API server)
import pika

def create_order(user_id: int, items: list):
    order_id = db.insert("orders", {...})

    # Publish to queue (very fast)
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='orders', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='orders',
        body=json.dumps({"order_id": order_id, "user_id": user_id}),
        properties=pika.BasicProperties(delivery_mode=2)   # Persistent
    )

    return {"order_id": order_id, "status": "queued"}   # Return immediately


# Consumer (worker - runs separately, can scale to N workers)
def process_order(ch, method, properties, body):
    data = json.loads(body)
    try:
        # Heavy work: payment, inventory, email, etc.
        charge_payment(data["user_id"])
        reserve_inventory(data["order_id"])
        send_confirmation_email(data["user_id"])

        ch.basic_ack(delivery_tag=method.delivery_tag)   # Mark done
    except Exception:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)   # Retry

channel.basic_consume(queue='orders', on_message_callback=process_order)
channel.start_consuming()
```


---

# CHAPTER 5: COMMON ARCHITECTURE PATTERNS


## Monolith vs Microservices

```
MONOLITH:
  One codebase, one deployment, one database.
  
  Pros:
    ✅ Simple to develop, test, deploy
    ✅ Easy local development
    ✅ No network calls between modules
    ✅ ACID transactions across all data
    ✅ Better for small teams (1-20 devs)
  
  Cons:
    ❌ Slow deployments as codebase grows
    ❌ Tech stack locked
    ❌ Scaling = scale ENTIRE app
    ❌ One bug can take down everything

  Use when: <100K users, small team, MVP, unclear domain

MICROSERVICES:
  Multiple independent services, each with own DB.
  
  Pros:
    ✅ Each service scales independently
    ✅ Different tech per service
    ✅ Independent deployment
    ✅ Team autonomy
    ✅ Fault isolation
  
  Cons:
    ❌ Massively more complex (network, observability)
    ❌ Distributed transactions hard
    ❌ Eventual consistency
    ❌ Need DevOps maturity
    ❌ Latency from network hops

  Use when: >100 devs, clear domain boundaries, hyper-scale

REALITY: Most companies do "service-oriented architecture" — a few large services, not 100 tiny ones.
Start with MONOLITH. Split into services only when proven necessary.
```


## API Gateway

```
WHAT IS IT?
  Single entry point for all client requests.
  Routes to appropriate backend service.
  Handles cross-cutting concerns.
  
  ┌────────┐
  │ Client │
  └───┬────┘
      │
      ▼
  ┌──────────────────┐
  │   API Gateway    │  ← auth, rate limit, logging
  └────┬──────────┬──┘
       │          │
       ▼          ▼
  ┌────────┐  ┌────────┐
  │ Users  │  │ Orders │
  │ service│  │service │
  └────────┘  └────────┘

RESPONSIBILITIES:
  - Routing      (URL pattern → service)
  - Auth         (JWT validation, OAuth)
  - Rate limit   (prevent abuse)
  - Logging      (centralized request logs)
  - Caching      (HTTP responses)
  - SSL term     (one place to manage certs)
  - Transformation (REST ↔ gRPC, JSON ↔ XML)
  - Aggregation  (combine multiple backend calls)

POPULAR GATEWAYS:
  Kong, AWS API Gateway, Apigee, Tyk, Zuul, Envoy, Cloudflare
```


## Event-Driven Architecture

```
TRADITIONAL (Request-Response):
  Service A directly calls Service B.
  Tight coupling. If B is down, A fails.

EVENT-DRIVEN:
  Service A emits event "OrderPlaced".
  Multiple services subscribe and react independently.
  
  ┌─────────┐   "OrderPlaced"   ┌──────────┐
  │ Orders  │ ──── event ─────► │  Queue   │
  └─────────┘                   └─┬────┬───┘
                                  │    │
                  ┌───────────────┘    └───────────────┐
                  ▼                                    ▼
            ┌──────────┐                         ┌──────────┐
            │  Email   │                         │ Analytics│
            │  Service │                         │  Service │
            └──────────┘                         └──────────┘

BENEFITS:
  - Loose coupling
  - Easy to add new subscribers
  - Resilient (if one consumer fails, others work)
  - Audit trail (all events logged)

EVENT SOURCING:
  Store EVENTS instead of current state.
  Current state = replay all events.
  
  Example bank account:
    Events: AccountOpened, Deposited 100, Withdrew 30, Deposited 50
    State: Balance = 120

  Pros: Full audit, time travel, easy to add features
  Cons: Complex, queries slow without snapshots
```


---

# CHAPTER 6: SCALABILITY CASE STUDIES


## Designing a URL Shortener (tinyurl.com)

```
REQUIREMENTS:
  - Shorten long URL → short alias
  - Redirect from short → original
  - 100M URLs created/month
  - 10:1 read:write ratio (10x more reads)
  - Custom aliases supported
  - 99.9% availability

CAPACITY:
  Writes: 100M / month = 40 writes/sec average
  Reads: 400 reads/sec average, ~10x peak = 4000 reads/sec
  Storage: 100M URLs × 500 bytes = 50 GB/month, 600 GB/year

KEY DESIGN: how to generate short codes?
  Option 1: Random hash
    Hash original URL → take first 7 chars
    Risk: collisions (rare but possible)
  
  Option 2: Auto-increment counter + Base62
    Counter: 1, 2, 3, ... → encode as Base62 [a-zA-Z0-9]
    7 chars → 62^7 = 3.5 trillion URLs
    But counter is centralized → bottleneck
  
  Option 3: Distributed ID generator (Snowflake)
    Each server has unique prefix + timestamp + counter
    No coordination needed.

SCHEMA (relational):
  CREATE TABLE urls (
      short_code  VARCHAR(7) PRIMARY KEY,
      long_url    TEXT NOT NULL,
      user_id     INT,
      created_at  TIMESTAMP DEFAULT NOW(),
      expires_at  TIMESTAMP,
      INDEX idx_user (user_id)
  );

ARCHITECTURE:
  Client → CDN → LB → API server → Cache (Redis) → DB (PostgreSQL)
                                                ↓
                                          Read replica

  Write: API → DB primary → invalidate cache
  Read: API → Redis cache → fallback to DB read replica → cache result

OPTIMIZATIONS:
  - Cache hot URLs in Redis (LRU, TTL 1 hour)
  - Use 301/302 redirects (308 for permanent)
  - Track analytics async (queue → analytics service)
```


## Designing a Chat Application (WhatsApp-lite)

```
REQUIREMENTS:
  - 1-on-1 and group chat
  - Online presence
  - Message history
  - Push notifications
  - Read receipts
  - 100M users, 50M DAU

CAPACITY:
  Messages: 50M users × 100 messages/day = 5B messages/day = 58K msgs/sec
  Storage: 5B msgs × 300 bytes = 1.5 TB/day, ~550 TB/year

KEY CHALLENGE: real-time delivery

CONNECTION OPTIONS:
  HTTP polling:       Easy but inefficient (constant requests)
  Long polling:       Slightly better
  WebSocket:          Persistent connection, real-time push  ✅
  Server-Sent Events: One-way push from server

ARCHITECTURE:
  
  User A ─WebSocket─► Connection Service ─► Message Queue ─► Storage
                                                            (Cassandra)
                          │
                          ▼
                     Push Notification ─► APN/FCM ─► User B (offline)
                          │
                          ▼
                    Online users via WebSocket

SCHEMA (Cassandra - high write throughput):
  Table: messages
    chat_id     UUID
    message_id  TIMEUUID    -- Sorted by time, distributed
    sender_id   UUID
    content     TEXT
    created_at  TIMESTAMP
    PRIMARY KEY (chat_id, message_id)

  Partition by chat_id → all messages of a chat on same node.
  Naturally sorted by message_id (time-based UUID).

ONLINE PRESENCE:
  Redis with TTL:
    SET user:123:online "1" EX 30   # Expires in 30s
  Heartbeat every 20s keeps it alive.
  Missing heartbeats → user offline.

OPTIMIZATION:
  - Connection servers stateless (load balanced)
  - Sticky sessions via consistent hashing on user_id
  - Pull latest 50 messages on chat open (paginate older)
  - Compress messages (Protobuf)
```


## Designing a News Feed (Twitter/Facebook timeline)

```
REQUIREMENTS:
  - User follows others
  - Timeline of posts from followed users
  - Sorted by time (or algorithm)
  - 200M DAU
  - Average 200 follows per user
  - 1000 posts/sec (peak), 100K timeline reads/sec

KEY CHALLENGE: timeline generation

APPROACH 1: PULL (compute on read)
  When user opens feed:
  1. Get list of who they follow
  2. Query posts WHERE author IN (follow_list) ORDER BY time DESC LIMIT 50
  
  Pros: Simple, fresh data, no storage overhead
  Cons: Slow for users following many people (cold queries)
  Use for: low-traffic, "celebrity" accounts with millions of followers

APPROACH 2: PUSH (precompute on write)
  When someone posts:
  1. Get list of their followers
  2. Inject post into each follower's "feed cache" (Redis)
  
  Pros: Read is O(1) - just fetch user's cached feed
  Cons: Heavy write amplification (post once → write to 1M follower caches)
  
  Use for: most users

HYBRID (Twitter's approach):
  - Push for normal users
  - Pull for celebrities (would explode write costs)
  - Mix at read time
  
ARCHITECTURE:
  
                        ┌─► Fanout service ─► User cache (Redis)
                        │      (push)
  Post API ──► Queue ───┤
                        │
                        └─► Storage (Cassandra)
                              (long-term)
  
  Read:
    GET /feed/me → Redis cache (hot) → fallback: Cassandra
```


---

# CHAPTER 7: RELIABILITY PATTERNS


## Circuit Breaker

```
PURPOSE:
  Prevent cascading failures when a downstream service is failing.
  Like an electrical circuit breaker.

STATES:
  CLOSED:     Normal operation, requests pass through.
  OPEN:       Service is failing; reject all requests immediately.
  HALF-OPEN:  Allow few test requests to see if service recovered.

LOGIC:
  - In CLOSED, count failures
  - After N failures in time window, → OPEN
  - In OPEN, reject immediately for cooldown period (e.g. 30s)
  - After cooldown, → HALF-OPEN
  - HALF-OPEN: if test requests succeed → CLOSED; else → OPEN
```

### Circuit Breaker Implementation

```python
from enum import Enum
import time
from threading import Lock

class State(Enum):
    CLOSED = 1
    OPEN = 2
    HALF_OPEN = 3

class CircuitBreaker:
    def __init__(self, failure_threshold=5, cooldown_seconds=30):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self.failure_count = 0
        self.state = State.CLOSED
        self.opened_at = None
        self.lock = Lock()

    def call(self, func, *args, **kwargs):
        with self.lock:
            if self.state == State.OPEN:
                if time.time() - self.opened_at > self.cooldown_seconds:
                    self.state = State.HALF_OPEN
                else:
                    raise Exception("Circuit breaker OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        with self.lock:
            self.failure_count = 0
            self.state = State.CLOSED

    def _on_failure(self):
        with self.lock:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = State.OPEN
                self.opened_at = time.time()

# Usage
breaker = CircuitBreaker()
try:
    result = breaker.call(call_external_api, user_id)
except Exception:
    result = use_fallback()
```


## Retry with Exponential Backoff

```python
import time
import random

def retry_with_backoff(func, max_retries=5, base_delay=0.5):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise   # Final attempt failed

            # Exponential backoff with jitter
            delay = base_delay * (2 ** attempt)
            jitter = random.uniform(0, delay * 0.1)
            time.sleep(delay + jitter)

# Why jitter? Prevents "thundering herd" - all clients retrying simultaneously.
```


## Rate Limiting

```
ALGORITHMS:

  Token Bucket:
    Bucket has N tokens. Each request consumes 1.
    Tokens refill at rate R per second.
    Allows bursts up to bucket size.

  Leaky Bucket:
    Requests fill bucket. Processed at constant rate.
    Smooths traffic.

  Fixed Window:
    "100 requests per minute" - reset counter every minute boundary.
    Simple but allows 2x burst at window boundaries.

  Sliding Window:
    Track timestamps of each request. Count in last 60s.
    More accurate but expensive.

WHERE TO ENFORCE:
  - Client (polite, but easily bypassed)
  - API Gateway (centralized, recommended)
  - Per-service (defense in depth)
  - Database (last resort)

REDIS-BASED RATE LIMITER (token bucket):

import redis
r = redis.Redis()

def is_allowed(user_id, limit=100, window=60):
    key = f"ratelimit:{user_id}"
    pipe = r.pipeline()
    now = int(time.time())
    
    # Remove expired tokens
    pipe.zremrangebyscore(key, 0, now - window)
    # Count current
    pipe.zcard(key)
    # Add current request
    pipe.zadd(key, {str(now): now})
    pipe.expire(key, window)
    
    _, count, _, _ = pipe.execute()
    return count < limit
```


## Common Pitfalls

```
PITFALL 1: Premature optimization
  Building microservices for 100 users.
  → Start monolith, scale later.

PITFALL 2: Ignoring the database
  Putting all logic in app, treating DB as dumb storage.
  → DBs are optimized; use indexes, materialized views, stored procs when sensible.

PITFALL 3: No monitoring
  No idea what's happening in production.
  → Logs, metrics, traces. Tools: Prometheus, Grafana, Sentry, Datadog.

PITFALL 4: Cache stampede
  Hot key expires → 1000 requests hit DB simultaneously.
  → Use cache-aside with lock, or stale-while-revalidate pattern.

PITFALL 5: Distributed transactions
  Trying to ACID across microservices.
  → Use Saga pattern (compensating transactions) or eventual consistency.

PITFALL 6: Synchronous chain of services
  Service A → B → C → D → E. Total latency = sum of all.
  → Parallelize where possible. Use events.

PITFALL 7: No backups / DR plan
  Database fails → permanent data loss.
  → Daily backups + offsite + tested restore procedures.

PITFALL 8: Single point of failure
  Everything goes through one node.
  → Multi-AZ, multi-region, leader election.

PITFALL 9: Hot partitions
  Sharding by user_id but all activity from one viral user.
  → Better sharding strategy, or hot key splitting.

PITFALL 10: Ignoring failure modes
  "What if Redis is down?"
  → Always have fallback. Cache miss should hit DB, not crash app.
```