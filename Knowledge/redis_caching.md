# Redis Complete Reference


---

# CHAPTER 1: REDIS FUNDAMENTALS


## Remarks

Redis is an in-memory data store used as cache, message broker, session store, and real-time leaderboard engine. It's incredibly fast — 100,000+ operations per second on a single server. Used by Twitter, GitHub, Stack Overflow, Instagram, and virtually every high-traffic web application.

Key concepts: **Key-value store** (basic), **Data structures** (strings, lists, sets, hashes, sorted sets), **Pub/Sub** (messaging), **TTL** (expiration), **Persistence** (RDB snapshots, AOF log), **Transactions**, **Lua scripting**.


## Data Types and Commands

```bash
# STRINGS (most basic — key → value)
SET name "Alice"
GET name                    # "Alice"
SET counter 0
INCR counter                # 1 (atomic increment!)
INCRBY counter 10           # 11
DECR counter                # 10
SET session:abc123 '{"user_id":1}' EX 3600   # Expires in 1 hour

MSET key1 "a" key2 "b" key3 "c"   # Set multiple
MGET key1 key2 key3                 # Get multiple

SETNX lock:resource "owner1"       # Set only if Not eXists (distributed lock!)

# HASHES (object/dictionary — key → {field: value, ...})
HSET user:1 name "Alice" age 30 role "admin"
HGET user:1 name            # "Alice"
HGETALL user:1              # {name: "Alice", age: "30", role: "admin"}
HINCRBY user:1 age 1        # Age → 31
HDEL user:1 role

# LISTS (ordered, duplicates allowed — queue/stack)
LPUSH queue "task1"         # Push left (front)
LPUSH queue "task2"
RPUSH queue "task3"         # Push right (back)
RPOP queue                  # Pop from right: "task3"
LPOP queue                  # Pop from left: "task2"
LRANGE queue 0 -1           # All elements
LLEN queue                  # Length
BRPOP queue 30              # Blocking pop (wait 30s for element)

# SETS (unique, unordered)
SADD tags "python" "web" "api"
SADD tags "python"          # Ignored (already exists)
SMEMBERS tags               # {"python", "web", "api"}
SISMEMBER tags "python"     # 1 (true)
SCARD tags                  # 3 (count)
SINTER tags1 tags2          # Intersection
SUNION tags1 tags2          # Union
SDIFF tags1 tags2           # Difference

# SORTED SETS (unique, ordered by score — leaderboards!)
ZADD leaderboard 100 "alice"
ZADD leaderboard 200 "bob"
ZADD leaderboard 150 "carol"
ZRANGE leaderboard 0 -1 WITHSCORES     # Ascending by score
ZREVRANGE leaderboard 0 2 WITHSCORES   # Top 3
ZRANK leaderboard "alice"               # Rank (0-based)
ZINCRBY leaderboard 50 "alice"          # alice: 150

# KEY MANAGEMENT
DEL key                     # Delete
EXISTS key                  # 1 or 0
EXPIRE key 3600             # Set TTL (seconds)
TTL key                     # Remaining TTL (-1 = no expiry, -2 = expired)
KEYS user:*                 # Find keys (DON'T use in production — blocking!)
SCAN 0 MATCH user:* COUNT 100  # Safe iteration (cursor-based)
TYPE key                    # String, list, set, zset, hash
```


## Python with Redis

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Cache pattern
def get_user(user_id):
    cache_key = f"user:{user_id}"
    
    # Check cache
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Cache miss → query database
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)
    
    # Store in cache (5 min TTL)
    r.setex(cache_key, 300, json.dumps(user))
    return user

# Invalidate on update
def update_user(user_id, data):
    db.update("UPDATE users SET ... WHERE id = %s", user_id)
    r.delete(f"user:{user_id}")  # Invalidate cache

# Rate limiter
def is_rate_limited(user_id, limit=100, window=60):
    key = f"rate:{user_id}"
    current = r.get(key)
    if current and int(current) >= limit:
        return True
    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, window)
    pipe.execute()
    return False

# Leaderboard
def add_score(player, score):
    r.zincrby("leaderboard", score, player)

def get_top_players(n=10):
    return r.zrevrange("leaderboard", 0, n-1, withscores=True)

# Session store
def create_session(user_id):
    session_id = secrets.token_hex(32)
    r.setex(f"session:{session_id}", 86400, json.dumps({
        "user_id": user_id,
        "created": time.time(),
    }))
    return session_id

# Pub/Sub (real-time messaging)
def publish_event(channel, data):
    r.publish(channel, json.dumps(data))

def subscribe_events(channel):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            process_event(data)
```


---

# CHAPTER 2: COMMON PITFALLS

```
PITFALL 1: Using KEYS in production
  KEYS * scans ALL keys — blocks Redis for seconds on large datasets.
  Fix: use SCAN with cursor for safe iteration.

PITFALL 2: No TTL on cache entries
  Cache grows forever → Redis runs out of memory → crash.
  Fix: always set TTL. Configure maxmemory-policy (allkeys-lru).

PITFALL 3: Storing large values
  One key = 100MB JSON → slow, blocks other operations.
  Fix: break into smaller keys, use hashes for structured data.

PITFALL 4: Not using connection pooling
  New connection per request → connection overhead.
  Fix: redis.ConnectionPool or redis.Redis (pools by default in redis-py).

PITFALL 5: Cache stampede
  Cache expires → 1000 requests hit database simultaneously.
  Fix: lock (SETNX), or staggered TTL, or background refresh.

PITFALL 6: Not handling Redis being down
  App crashes when Redis is unavailable.
  Fix: try/except, fallback to database, circuit breaker pattern.
```