# Distributed Systems Advanced Complete Reference


---

# CHAPTER 1: FUNDAMENTALS


## Remarks

A distributed system is a collection of independent computers that appear as a single system to users. Distributed systems exist because no single machine can handle the scale, availability, and fault tolerance requirements of modern applications. Google processes 99,000+ searches per second. Netflix streams to 260M+ subscribers. These systems MUST be distributed.

Key concepts: **CAP Theorem** (pick 2 of 3), **Consistency models** (strong, eventual, causal), **Consensus** (Raft, Paxos), **Replication** (leader-follower, multi-leader, leaderless), **Partitioning/Sharding** (split data across nodes), **Vector clocks** (track causality), **Gossip protocols** (epidemic information spread), **CRDTs** (conflict-free replicated data types), **Idempotency** (safe retries), **Exactly-once semantics** (the holy grail).

Used by: every large-scale system. Google (Spanner, Bigtable), Amazon (DynamoDB, S3), Facebook (TAO, Cassandra), Netflix, Uber, Stripe.

Books: "Designing Data-Intensive Applications" by Martin Kleppmann (THE bible), "Distributed Systems" by Van Steen & Tanenbaum.


## The Eight Fallacies of Distributed Computing

```
Peter Deutsch's fallacies (1994) — STILL relevant:

1. The network is reliable
   → Packets get lost, connections drop, cables get cut.
   → Design for failure: retries, timeouts, circuit breakers.

2. Latency is zero
   → Same datacenter: ~0.5ms. Cross-continent: ~100ms. 
   → Minimize round trips. Batch requests. Cache aggressively.

3. Bandwidth is infinite
   → Network has limits. Don't send 1GB payloads.
   → Compress. Paginate. Send only what's needed.

4. The network is secure
   → Encrypt everything. mTLS between services. Zero trust.

5. Topology doesn't change
   → Nodes join, leave, fail, move. IPs change.
   → Service discovery. DNS. Don't hardcode addresses.

6. There is one administrator
   → Multiple teams, orgs, cloud providers.
   → Clear ownership. Runbooks. Observability.

7. Transport cost is zero
   → Cross-region traffic costs money. Cloud egress fees.
   → Keep related data close. Minimize cross-region calls.

8. The network is homogeneous
   → Different hardware, OS, languages, versions.
   → Standard protocols (HTTP, gRPC). Schema evolution.
```


## CAP Theorem

```
CAP THEOREM (Brewer, 2000):
  A distributed system can guarantee at most TWO of:

  C — CONSISTENCY:      Every read gets the most recent write.
  A — AVAILABILITY:     Every request gets a response (no errors).
  P — PARTITION TOLERANCE: System works despite network splits.

  In practice, P is mandatory (networks DO partition).
  So the real choice is: CP or AP.

CP SYSTEMS (consistency over availability):
  During partition → some requests FAIL (to preserve consistency).
  Examples: HBase, MongoDB (default), Zookeeper, etcd, Spanner
  Use when: financial transactions, inventory counts, leader election

AP SYSTEMS (availability over consistency):
  During partition → all requests SUCCEED (but may return stale data).
  Examples: Cassandra, DynamoDB, CouchDB, DNS
  Use when: social media feeds, shopping carts, metrics

REALITY IS MORE NUANCED:
  - Partitions are rare (most of the time you have all three)
  - When partition heals, AP systems converge (eventual consistency)
  - Many systems are tunable (Cassandra: adjust consistency per query)

PACELC THEOREM (extends CAP):
  If Partition: choose Availability or Consistency
  Else (normal operation): choose Latency or Consistency
  
  PA/EL: Available during partition, low latency normally (DynamoDB, Cassandra)
  PC/EC: Consistent always, higher latency (Spanner, traditional RDBMS)
  PA/EC: Available during partition, consistent normally (MongoDB)
```


## Consistency Models

```
STRONG CONSISTENCY (linearizability):
  After write completes, ALL subsequent reads see the new value.
  Behaves as if there's ONE copy of data.
  Cost: high latency (must coordinate across nodes).
  Example: bank account balance.

SEQUENTIAL CONSISTENCY:
  All nodes see operations in SAME order.
  But not necessarily real-time order.
  Weaker than linearizability.

CAUSAL CONSISTENCY:
  If operation A causally precedes B, everyone sees A before B.
  Concurrent operations can be seen in any order.
  Example: reply to a comment always appears AFTER the comment.

EVENTUAL CONSISTENCY:
  If no new writes, all replicas EVENTUALLY converge.
  No guarantee WHEN — could be milliseconds or seconds.
  Example: DNS propagation, social media likes count.
  
  Variants:
    Read-your-writes: you see your own writes immediately.
    Monotonic reads: you never see older data after seeing newer.
    Consistent prefix: you see operations in order they were applied.

SESSION CONSISTENCY:
  Within a session, read-your-writes + monotonic reads guaranteed.
  Different sessions may see different states.
  Common in web apps (user's session is consistent).
```


---

# CHAPTER 2: CONSENSUS


## Why Consensus Matters

```
PROBLEM:
  Multiple nodes must agree on a value (leader, transaction, config).
  Nodes can crash, messages can be lost/delayed.
  How to reach agreement despite failures?

USE CASES:
  - Leader election (who is primary database?)
  - Distributed locks (only one service processes this order)
  - State machine replication (all replicas apply same operations in same order)
  - Configuration management (all nodes see same config)
  - Atomic broadcast (all nodes deliver same messages in same order)

IMPOSSIBILITY: FLP Theorem (1985)
  In an asynchronous system with even ONE crash failure,
  NO deterministic algorithm guarantees consensus.
  
  In practice: we use timeouts (partial synchrony) to work around this.
```


## Raft Consensus Algorithm

```
RAFT (2014, Diego Ongaro): understandable consensus algorithm.
Equivalent to Paxos but designed for clarity.

THREE ROLES:
  Leader:    handles all client requests, replicates log
  Follower:  passive, responds to leader
  Candidate: attempting to become leader

LEADER ELECTION:
  1. All nodes start as Followers
  2. If follower doesn't hear from leader (timeout) → becomes Candidate
  3. Candidate increments term, votes for self, requests votes from others
  4. If majority votes → becomes Leader
  5. If another leader exists with higher term → steps down
  6. If split vote → timeout, try again with new term

  Terms: monotonically increasing numbers (like epoch).
  Each term has at most ONE leader.
  If node sees higher term → immediately becomes follower.

LOG REPLICATION:
  1. Client sends command to Leader
  2. Leader appends to its log (uncommitted)
  3. Leader sends AppendEntries RPC to all followers
  4. Followers append to their logs, respond OK
  5. When MAJORITY respond → Leader commits entry
  6. Leader responds to client: "committed"
  7. Leader notifies followers of commit in next heartbeat
  8. Followers apply committed entries to state machine

  Log: ordered sequence of entries
    Entry: { term, index, command }
    [1:SET x=1] [1:SET y=2] [2:SET x=3] [2:DEL y]

SAFETY GUARANTEES:
  - Election Safety: at most one leader per term
  - Leader Append-Only: leader never overwrites its log
  - Log Matching: if two logs have entry with same index+term,
    all preceding entries are identical
  - Leader Completeness: committed entries are present in all future leaders
  - State Machine Safety: all nodes apply same entries → same state

FAILURE HANDLING:
  Leader crashes:
    Followers timeout → new election → new leader
    New leader has all committed entries (guaranteed)
    Uncommitted entries may be lost (client should retry)
  
  Follower crashes:
    Leader retries AppendEntries until follower recovers
    Follower catches up from leader's log
  
  Network partition:
    Minority partition can't elect leader (need majority)
    Majority partition continues operating
    When partition heals, minority catches up

IMPLEMENTATIONS:
  etcd (Kubernetes), Consul (HashiCorp), CockroachDB, TiKV
```


## Paxos (Brief Overview)

```
PAXOS (Leslie Lamport, 1989): original consensus algorithm.
Correct but notoriously difficult to understand and implement.

BASIC PAXOS (single value agreement):
  Proposers: propose values
  Acceptors: vote on proposals
  Learners: learn the chosen value

  Phase 1 (Prepare):
    Proposer sends Prepare(n) to majority of acceptors
    Acceptor: if n > any seen → promise to not accept lower proposals
  
  Phase 2 (Accept):
    Proposer sends Accept(n, value) to majority
    Acceptor: if no higher promise → accept
  
  Value is chosen when majority of acceptors accept same proposal.

MULTI-PAXOS: extends to sequence of values (log replication).
  Optimizes by keeping stable leader (skip Phase 1 after first round).

WHY RAFT WON:
  Paxos is correct but:
  - Extremely hard to understand (Lamport wrote it as a story about Greek parliament)
  - Leaves many implementation details unspecified
  - Multi-Paxos was never fully specified
  
  Raft was designed for understandability first.
  Same guarantees, clearer algorithm, real implementations.
```


---

# CHAPTER 3: REPLICATION


## Replication Strategies

```
SINGLE-LEADER (Primary-Replica):
  One leader handles writes. Replicas handle reads.
  
  Leader ──writes──→ Replica 1 (read)
    │                Replica 2 (read)
    │                Replica 3 (read)
    └──writes──→ Client gets response
  
  Sync replication: leader waits for ALL replicas → strong consistency, slow
  Async replication: leader responds immediately → fast, eventual consistency
  Semi-sync: leader waits for ONE replica → compromise
  
  Used by: PostgreSQL, MySQL, MongoDB, Redis Sentinel
  
  Pros: simple, strong consistency possible
  Cons: leader is bottleneck + SPOF (need failover)

MULTI-LEADER:
  Multiple nodes accept writes. Sync between each other.
  
  Leader A ←→ Leader B ←→ Leader C
  
  Used by: multi-datacenter setups, CouchDB, Tungsten Replicator
  
  Pros: low latency writes in each datacenter, survives datacenter failure
  Cons: CONFLICT RESOLUTION needed (same key written on two leaders)
  
  Conflict resolution:
    Last-Write-Wins (LWW): latest timestamp wins (data loss!)
    Merge: application-specific merge logic
    CRDTs: mathematically guaranteed conflict-free
    Human: flag conflict, let user resolve

LEADERLESS:
  Any node accepts reads AND writes. Quorum-based.
  
  Write to W nodes, read from R nodes.
  If W + R > N → guaranteed to read latest write.
  
  Example (N=3, W=2, R=2):
    Write to 2 of 3 nodes.
    Read from 2 of 3 nodes.
    At least 1 node has latest write (overlap guaranteed).
  
  Used by: Cassandra, DynamoDB, Riak
  
  Pros: no SPOF, highly available, tunable consistency
  Cons: complex conflict resolution, read repair needed
```


## Vector Clocks

```
PROBLEM: In distributed systems, wall clocks are unreliable.
  Node A's clock: 10:00:01
  Node B's clock: 10:00:03
  Does B's event happen after A's? NOT NECESSARILY (clock skew).

SOLUTION: Logical clocks that track CAUSALITY, not time.

LAMPORT CLOCKS:
  Each node has counter. Increment on each event.
  On send: attach counter. On receive: max(local, received) + 1.
  Gives total order but can't distinguish concurrent events.

VECTOR CLOCKS:
  Each node has vector of counters (one per node).
  
  Node A: [A:1, B:0, C:0]
  Node B: [A:0, B:1, C:0]
  Node C: [A:0, B:0, C:1]
  
  A sends message to B:
    A increments own counter: [A:2, B:0, C:0]
    B receives, merges: max each element + increment own
    B: [A:2, B:2, C:0]
  
  COMPARISON:
    V1 < V2 (V1 happened before V2): all V1[i] ≤ V2[i], at least one strict <
    V1 || V2 (concurrent): neither V1 < V2 nor V2 < V1
  
  Example:
    [A:2, B:1] < [A:3, B:2]   → first happened before second
    [A:2, B:1] || [A:1, B:2]   → CONCURRENT (need conflict resolution)

  Used by: DynamoDB (simplified), Riak
  
  Problem: vector grows with number of nodes.
  Solution: version vectors (prune old entries), dotted version vectors.
```


---

# CHAPTER 4: PARTITIONING (SHARDING)


## Partitioning Strategies

```
WHY PARTITION:
  Single node can't hold all data or handle all queries.
  Split data across multiple nodes.

KEY-BASED (Hash) PARTITIONING:
  partition = hash(key) % num_partitions
  
  Pros: even distribution (if hash is good)
  Cons: range queries impossible, rebalancing hard
  Used by: Cassandra, DynamoDB, Redis Cluster

RANGE PARTITIONING:
  Split by key ranges: A-F → Node 1, G-M → Node 2, N-Z → Node 3
  
  Pros: range queries efficient (all A-F on one node)
  Cons: hotspots (if "S" names are 40% of traffic)
  Used by: HBase, Bigtable, CockroachDB

CONSISTENT HASHING:
  Nodes and keys mapped to positions on a virtual ring.
  Key is assigned to next node clockwise on ring.
  
  Adding/removing node → only neighbors affected (minimal data movement).
  Virtual nodes: each physical node gets multiple ring positions (better balance).
  
  Used by: DynamoDB, Cassandra, CDN routing, memcached

REBALANCING:
  When nodes join/leave, data must redistribute.
  
  Fixed partitions: create 1000 partitions, assign to N nodes.
    Add node → steal partitions from others.
    Much better than hash(key) % N (which reshuffles everything).
  
  Dynamic partitioning: split partition when too large, merge when too small.
    Used by: HBase, RethinkDB.
```


## Secondary Indexes with Partitions

```
PROBLEM: data partitioned by primary key, but need to query by other fields.
  Users partitioned by user_id, but query by country.

APPROACH 1: Local index (document-partitioned)
  Each partition has its own index covering ONLY its data.
  
  Query by country → must query ALL partitions (scatter/gather).
  Write: fast (update local index only).
  Read: slow (fan out to all partitions).
  
  Used by: MongoDB, Cassandra, Elasticsearch

APPROACH 2: Global index (term-partitioned)
  Index itself is partitioned (e.g., countries A-M on Node 1, N-Z on Node 2).
  
  Query by country → query ONE partition of index.
  Write: slower (must update remote index partition).
  Read: fast (single partition lookup).
  
  Used by: DynamoDB global secondary indexes, Riak
```


---

# CHAPTER 5: PATTERNS FOR RELIABILITY


## Circuit Breaker

```python
import time
from enum import Enum

class State(Enum):
    CLOSED = "closed"          # Normal operation
    OPEN = "open"              # Failing, reject immediately
    HALF_OPEN = "half_open"    # Testing if service recovered

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=30):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = State.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
    
    async def call(self, func, *args, **kwargs):
        if self.state == State.OPEN:
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = State.HALF_OPEN
            else:
                raise CircuitOpenError("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        self.state = State.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = State.OPEN

# Usage
payment_breaker = CircuitBreaker(failure_threshold=3, reset_timeout=60)

async def process_payment(order):
    try:
        return await payment_breaker.call(stripe.charge, order.total)
    except CircuitOpenError:
        return await fallback_payment(order)
```


## Retry with Exponential Backoff

```python
import asyncio
import random

async def retry_with_backoff(
    func,
    max_retries=5,
    base_delay=1.0,
    max_delay=60.0,
    jitter=True,
):
    for attempt in range(max_retries):
        try:
            return await func()
        except (ConnectionError, TimeoutError) as e:
            if attempt == max_retries - 1:
                raise
            
            delay = min(base_delay * (2 ** attempt), max_delay)
            if jitter:
                delay *= random.uniform(0.5, 1.5)   # Avoid thundering herd
            
            await asyncio.sleep(delay)

# Delays: 1s, 2s, 4s, 8s, 16s (with jitter)
# Without jitter: all failed clients retry at same time → overload again!
```


## Saga Pattern (Distributed Transactions)

```python
# When operation spans multiple services, can't use regular transactions.
# Saga: sequence of local transactions with compensating actions.

class OrderSaga:
    async def execute(self, order):
        steps = [
            (self.reserve_inventory, self.release_inventory),
            (self.charge_payment, self.refund_payment),
            (self.create_shipment, self.cancel_shipment),
            (self.send_confirmation, self.send_cancellation),
        ]
        
        completed = []
        try:
            for action, compensation in steps:
                await action(order)
                completed.append(compensation)
        except Exception as e:
            # COMPENSATE: undo completed steps in reverse
            for compensation in reversed(completed):
                try:
                    await compensation(order)
                except Exception as comp_err:
                    log.error(f"Compensation failed: {comp_err}")
                    # Alert ops team — manual intervention needed
            raise SagaFailed(f"Order saga failed: {e}")
    
    async def reserve_inventory(self, order):
        await inventory_service.reserve(order.items)
    
    async def release_inventory(self, order):
        await inventory_service.release(order.items)
    
    async def charge_payment(self, order):
        await payment_service.charge(order.total)
    
    async def refund_payment(self, order):
        await payment_service.refund(order.total)
```


## CRDTs (Conflict-Free Replicated Data Types)

```
CRDT: data structures that can be replicated across nodes
and merged WITHOUT conflicts. Mathematically guaranteed convergence.

G-COUNTER (Grow-only counter):
  Each node has its own counter.
  Value = sum of all counters.
  Merge = max of each counter.
  
  Node A: {A:3, B:0} → value = 3
  Node B: {A:0, B:5} → value = 5
  Merge:  {A:3, B:5} → value = 8  ✅ No conflict!

PN-COUNTER (Positive-Negative counter):
  Two G-Counters: one for increments, one for decrements.
  Value = sum(increments) - sum(decrements).

G-SET (Grow-only set):
  Only add, never remove. Merge = union.
  
  Node A: {1, 2, 3}
  Node B: {2, 3, 4}
  Merge:  {1, 2, 3, 4}  ✅

OR-SET (Observed-Remove set):
  Add and remove supported.
  Each element tagged with unique ID.
  Add: insert (element, unique_id).
  Remove: remove all known (element, id) pairs.
  Concurrent add+remove → add wins (element stays).

LWW-REGISTER (Last-Writer-Wins):
  Each write has timestamp.
  Merge: keep the one with latest timestamp.
  Simple but can lose data!

USED BY:
  Redis CRDT (active-active geo-replication)
  Riak (distributed database)
  Automerge / Yjs (collaborative editing — Google Docs-like)
  Figma (multiplayer design)
```


---

# CHAPTER 6: OBSERVABILITY


## Distributed Tracing

```
PROBLEM: Request passes through 10 microservices.
  Where is the bottleneck? Which service failed?

SOLUTION: Distributed tracing (OpenTelemetry)
  Assign unique trace ID to each request.
  Each service creates a SPAN (start time, end time, metadata).
  Spans linked by parent-child relationship.

  Trace: [trace_id: abc123]
    └─ Span: API Gateway (0ms - 250ms)
        ├─ Span: Auth Service (5ms - 20ms)
        ├─ Span: User Service (25ms - 80ms)
        │   └─ Span: Database Query (30ms - 75ms)  ← SLOW!
        └─ Span: Notification Service (85ms - 240ms)
            ├─ Span: Email Send (90ms - 230ms)  ← SLOW!
            └─ Span: SMS Send (90ms - 110ms)

TOOLS: Jaeger, Zipkin, Datadog APM, Honeycomb, Grafana Tempo

PROPAGATION:
  HTTP header: traceparent: 00-abc123-def456-01
  gRPC metadata: same header
  Message queue: attach trace context to message headers
```


## The Three Pillars

```
1. LOGS:    What happened (events, errors, debug info)
2. METRICS: How much/how fast (counters, gauges, histograms)
3. TRACES:  Where it went (request path across services)

ALL THREE needed for production systems.

METRICS TYPES:
  Counter:   only goes up (requests_total, errors_total)
  Gauge:     goes up and down (active_connections, cpu_usage)
  Histogram: distribution (request_duration_seconds)

KEY METRICS (RED method for services):
  Rate:      requests per second
  Errors:    error rate / error count
  Duration:  latency (p50, p95, p99)

KEY METRICS (USE method for resources):
  Utilization: % of resource in use (CPU 80%)
  Saturation:  queue depth / backlog
  Errors:      error count

ALERTING:
  Alert on SYMPTOMS, not causes.
  Good: "error rate > 1% for 5 minutes" (symptom)
  Bad: "CPU > 90%" (cause — might be fine if service is healthy)
  
  Avoid alert fatigue: every alert must be actionable.
```


---

# CHAPTER 7: COMMON PITFALLS


## Distributed Systems Pitfalls

```
PITFALL 1: Assuming network is reliable
  Fix: retries with backoff, timeouts, circuit breakers, idempotency.

PITFALL 2: Using wall clock for ordering
  Clocks drift. NTP can jump. Two events at "same time" → ambiguous.
  Fix: logical clocks, vector clocks, or TrueTime (Spanner).

PITFALL 3: Two-Phase Commit (2PC) at scale
  Coordinator fails → all participants blocked.
  Fix: Saga pattern, eventual consistency, or Raft-based consensus.

PITFALL 4: Split-brain
  Network partition → two nodes both think they're leader.
  Fix: fencing tokens, consensus algorithm (Raft), quorum.

PITFALL 5: Unbounded queues
  Producer faster than consumer → queue grows → OOM.
  Fix: bounded queues, backpressure, rate limiting.

PITFALL 6: Not designing for failure
  "This service never goes down" → it will.
  Fix: chaos engineering, graceful degradation, fallbacks.

PITFALL 7: Distributed monolith
  Microservices that must all be deployed together → worst of both worlds.
  Fix: loose coupling, async communication, independent deployment.

PITFALL 8: No idempotency
  Retry creates duplicate orders, charges, messages.
  Fix: idempotency keys, deduplication, exactly-once processing.

PITFALL 9: Ignoring partial failures
  5 of 10 service calls succeed. What now?
  Fix: define SLA per operation, compensating transactions, fallbacks.

PITFALL 10: N+1 across services
  Loop calling another service per item → 1000 HTTP calls.
  Fix: batch APIs, GraphQL, data locality.

PITFALL 11: No observability
  "Something is slow" → can't find where.
  Fix: distributed tracing (OpenTelemetry), structured logging, dashboards.

PITFALL 12: Premature distribution
  Distributing before you need to → 10x complexity for no benefit.
  Fix: start with monolith. Distribute when you actually hit scaling limits.

PITFALL 13: Ignoring data locality
  Service in US queries database in EU → 200ms per query.
  Fix: co-locate services with their data. Multi-region replication.

PITFALL 14: No backpressure
  Upstream floods downstream → cascading failure.
  Fix: rate limiting, queue depth limits, load shedding, bulkheads.

PITFALL 15: Testing only happy path
  Distributed failures are combinatorial (any subset of nodes can fail).
  Fix: chaos engineering (Chaos Monkey), fault injection, game days.
```