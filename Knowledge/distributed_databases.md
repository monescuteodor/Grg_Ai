Distributed Databases Complete Reference
CHAPTER 1: GETTING STARTED WITH DISTRIBUTED DATABASES
Remarks
Distributed databases store data across multiple physical/virtual nodes to achieve scalability, availability, and fault tolerance. Key challenges: data partitioning, replication, consistency models, distributed transactions, consensus, conflict resolution. Modern systems: CockroachDB (distributed SQL), Google Spanner (globally distributed), Cassandra (wide-column), DynamoDB (key-value), MongoDB (document), Redis Cluster (in-memory).
Tools: Python (for simulations), Go (production systems), CockroachDB, Cassandra, Redis, etcd, ZooKeeper.
Hello Distributed DB
# hello_distributed_db.py
"""
Minimal distributed key-value store with replication.
"""
import hashlib
import threading
import time
from collections import defaultdict

class DistributedKVStore:
    """Simple distributed KV store with consistent hashing."""
    
    def __init__(self, num_nodes=3, replication_factor=2):
        self.num_nodes = num_nodes
        self.replication_factor = replication_factor
        self.nodes = [{} for _ in range(num_nodes)]
        self.vector_clocks = [defaultdict(lambda: defaultdict(int)) 
                              for _ in range(num_nodes)]
        self.lock = threading.Lock()
    
    def _hash_key(self, key: str) -> int:
        """Consistent hash: map key to node."""
        h = hashlib.md5(key.encode()).hexdigest()
        return int(h, 16) % self.num_nodes
    
    def _get_replica_nodes(self, key: str) -> list:
        """Get nodes responsible for this key (primary + replicas)."""
        primary = self._hash_key(key)
        replicas = []
        for i in range(self.replication_factor):
            replicas.append((primary + i) % self.num_nodes)
        return replicas
    
    def write(self, key: str, value: str, node_id: int = None) -> bool:
        """Write to primary and replicas with vector clock."""
        with self.lock:
            if node_id is None:
                node_id = self._hash_key(key)
            
            # Update vector clock
            self.vector_clocks[node_id][key][node_id] += 1
            
            # Write to primary
            self.nodes[node_id][key] = (value, 
                                        dict(self.vector_clocks[node_id][key]))
            
            # Replicate to other nodes
            for replica_id in self._get_replica_nodes(key):
                if replica_id != node_id:
                    self.nodes[replica_id][key] = (value, 
                                                   dict(self.vector_clocks[node_id][key]))
                    self.vector_clocks[replica_id][key] = dict(self.vector_clocks[node_id][key])
            
            return True
    
    def read(self, key: str, node_id: int = None) -> tuple:
        """Read from any replica (eventual consistency)."""
        if node_id is None:
            node_id = self._hash_key(key)
        
        if key in self.nodes[node_id]:
            value, vc = self.nodes[node_id][key]
            return value, vc
        return None, None
    
    def read_all_replicas(self, key: str) -> list:
        """Read from all replicas (for conflict detection)."""
        results = []
        for node_id in self._get_replica_nodes(key):
            if key in self.nodes[node_id]:
                value, vc = self.nodes[node_id][key]
                results.append((node_id, value, vc))
        return results
    
    def get_stats(self) -> dict:
        """Get statistics for each node."""
        stats = {}
        for i, node in enumerate(self.nodes):
            stats[f"node_{i}"] = {
                'keys': len(node),
                'memory_approx': sum(len(k) + len(str(v)) for k, v in node.items())
            }
        return stats

# Example
db = DistributedKVStore(num_nodes=3, replication_factor=2)

# Write data
db.write("user:1", "Alice")
db.write("user:2", "Bob")
db.write("user:3", "Charlie")

# Read data
value, vc = db.read("user:1")
print(f"user:1 = {value} (vector clock: {vc})")

# Read from all replicas
replicas = db.read_all_replicas("user:2")
print(f"\nReplicas for user:2:")
for node_id, value, vc in replicas:
    print(f"  Node {node_id}: {value} (vc: {vc})")

print(f"\nCluster stats: {db.get_stats()}")

CHAPTER 2: CONSISTENCY MODELS
Consistency Spectrum
# Strong Consistency (Linearizability):
# - All reads return the most recent write
# - Operations appear atomic in some total order
# - Used in: Spanner, CockroachDB (with latency cost)

# Sequential Consistency:
# - All operations appear in some total order
# - Per-process operations in program order
# - Weaker than linearizability

# Causal Consistency:
# - Causally related operations seen in same order by all
# - Concurrent operations may be seen in different orders
# - Used in: Facebook Messenger, some CRDTs

# Eventual Consistency:
# - If no new writes, all replicas eventually converge
# - Reads may return stale data
# - Used in: Cassandra, DynamoDB, DNS

# Read Your Writes:
# - Client always sees its own writes
# - Important for user experience

# Monotonic Reads:
# - Once a client reads a value, future reads are same or newer

import threading
import time

class ConsistencyDemo:
    """Demonstrate different consistency models."""
    
    def __init__(self, model='eventual'):
        self.model = model
        self.data = {}
        self.lock = threading.Lock()
        self.write_timestamp = {}
    
    def write(self, key, value, node_id=0):
        with self.lock:
            if self.model == 'strong':
                # Block until all replicas updated (simplified)
                self.data[key] = value
                self.write_timestamp[key] = time.time()
                time.sleep(0.01)  # Simulate sync delay
            elif self.model == 'eventual':
                self.data[key] = value
                self.write_timestamp[key] = time.time()
                # Async replication (simplified)
                threading.Thread(
                    target=self._async_replicate,
                    args=(key, value)
                ).start()
    
    def _async_replicate(self, key, value):
        time.sleep(0.05)  # Simulate network delay
        # Already updated in simplified version
    
    def read(self, key):
        if self.model == 'strong':
            with self.lock:
                return self.data.get(key)
        else:
            # No lock for eventual (may read stale)
            return self.data.get(key)

# Demo
print("=== Consistency Models ===")
for model in ['strong', 'eventual']:
    db = ConsistencyDemo(model)
    db.write("x", 100)
    value = db.read("x")
    print(f"{model:10s}: x = {value}")

Vector Clocks for Causality
# Vector clock: each node maintains a vector of counters
# Used to determine causal ordering of events

class VectorClock:
    """Vector clock implementation."""
    
    def __init__(self, node_id, num_nodes):
        self.node_id = node_id
        self.clock = [0] * num_nodes
    
    def increment(self):
        """Increment own counter."""
        self.clock[self.node_id] += 1
    
    def merge(self, other):
        """Merge with another vector clock (take max)."""
        for i in range(len(self.clock)):
            self.clock[i] = max(self.clock[i], other.clock[i])
    
    def happens_before(self, other) -> bool:
        """Check if self happens-before other."""
        at_least_one_less = False
        for i in range(len(self.clock)):
            if self.clock[i] > other.clock[i]:
                return False
            if self.clock[i] < other.clock[i]:
                at_least_one_less = True
        return at_least_one_less
    
    def concurrent(self, other) -> bool:
        """Check if self is concurrent with other."""
        return (not self.happens_before(other) and 
                not other.happens_before(self) and 
                self.clock != other.clock)
    
    def copy(self):
        vc = VectorClock(self.node_id, len(self.clock))
        vc.clock = self.clock.copy()
        return vc
    
    def __repr__(self):
        return f"VC{self.clock}"

# Example: causal ordering
vc1 = VectorClock(0, 3)  # Node 0
vc2 = VectorClock(1, 3)  # Node 1

vc1.increment()  # Event A on node 0: [1,0,0]
print(f"Event A: {vc1}")

vc2.increment()  # Event B on node 1: [0,1,0]
print(f"Event B: {vc2}")

print(f"A happens-before B: {vc1.happens_before(vc2)}")
print(f"A concurrent with B: {vc1.concurrent(vc2)}")

# Send message from node 0 to node 1
vc1.increment()  # Send event: [2,0,0]
vc2.merge(vc1)   # Receive event: [2,1,0]
vc2.increment()  # Local event: [2,2,0]

print(f"\nAfter message: A={vc1}, B={vc2}")
print(f"A happens-before B: {vc1.happens_before(vc2)}")

Lamport Timestamps
# Simpler than vector clocks but cannot detect concurrency

class LamportClock:
    """Lamport logical clock."""
    
    def __init__(self, node_id):
        self.node_id = node_id
        self.time = 0
    
    def tick(self):
        """Local event."""
        self.time += 1
        return self.time
    
    def send(self):
        """Send message."""
        self.time += 1
        return self.time
    
    def receive(self, timestamp):
        """Receive message."""
        self.time = max(self.time, timestamp) + 1
        return self.time

# Example
lc1 = LamportClock(0)
lc2 = LamportClock(1)

t1 = lc1.tick()  # Event A
print(f"\nLamport: Event A at t={t1}")

t2 = lc1.send()  # Send message
print(f"Lamport: Send at t={t2}")

t3 = lc2.receive(t2)  # Receive message
print(f"Lamport: Receive at t={t3}")

CHAPTER 3: REPLICATION STRATEGIES
Single-Leader Replication
# One node handles all writes, replicates to followers
# Pros: simple, strong consistency possible
# Cons: single point of failure, write bottleneck

class SingleLeaderReplication:
    """Single-leader replication with synchronous/async options."""
    
    def __init__(self, num_followers=2, sync_replication=True):
        self.leader = {}
        self.followers = [{} for _ in range(num_followers)]
        self.sync_replication = sync_replication
        self.lock = threading.Lock()
    
    def write(self, key, value, quorum=1):
        """Write with configurable durability."""
        with self.lock:
            # Always write to leader
            self.leader[key] = value
            
            if self.sync_replication:
                # Wait for followers
                for i in range(min(quorum, len(self.followers))):
                    self.followers[i][key] = value
            else:
                # Async replication
                for follower in self.followers:
                    threading.Thread(
                        target=lambda f=follower: f.update({key: value})
                    ).start()
            
            return True
    
    def read(self, key, from_leader=True):
        """Read from leader or follower."""
        if from_leader:
            return self.leader.get(key)
        else:
            # Read from any follower (may be stale)
            for follower in self.followers:
                if key in follower:
                    return follower[key]
            return None
    
    def failover(self):
        """Promote first follower to leader."""
        if self.followers:
            new_leader = self.followers.pop(0)
            old_leader = self.leader
            self.leader = new_leader
            self.followers.append(old_leader)
            return True
        return False

# Example
db = SingleLeaderReplication(num_followers=2, sync_replication=True)
db.write("x", 100, quorum=2)
print(f"Read from leader: {db.read('x')}")
print(f"Read from follower: {db.read('x', from_leader=False)}")

Multi-Leader Replication
# Multiple nodes accept writes, resolve conflicts
# Used in: multi-datacenter, offline-first apps

class MultiLeaderReplication:
    """Multi-leader with last-write-wins conflict resolution."""
    
    def __init__(self, node_ids):
        self.node_ids = node_ids
        self.data = {nid: {} for nid in node_ids}
        self.timestamps = {nid: {} for nid in node_ids}
        self.lock = threading.Lock()
    
    def write(self, node_id, key, value):
        """Write to specific node."""
        with self.lock:
            ts = time.time()
            self.data[node_id][key] = value
            self.timestamps[node_id][key] = ts
            
            # Async replication to other nodes
            for other_id in self.node_ids:
                if other_id != node_id:
                    threading.Thread(
                        target=self._replicate,
                        args=(node_id, other_id, key, value, ts)
                    ).start()
    
    def _replicate(self, from_id, to_id, key, value, ts):
        """Replicate with conflict resolution."""
        time.sleep(0.01)  # Simulate network
        with self.lock:
            existing_ts = self.timestamps[to_id].get(key, 0)
            if ts > existing_ts:
                # Last-write-wins
                self.data[to_id][key] = value
                self.timestamps[to_id][key] = ts
    
    def read(self, node_id, key):
        """Read from specific node."""
        return self.data[node_id].get(key)

# Example
db = MultiLeaderReplication(['DC1', 'DC2', 'DC3'])
db.write('DC1', 'user:1', 'Alice_v1')
time.sleep(0.05)
db.write('DC2', 'user:1', 'Alice_v2')
time.sleep(0.05)
print(f"DC1: {db.read('DC1', 'user:1')}")
print(f"DC2: {db.read('DC2', 'user:1')}")
print(f"DC3: {db.read('DC3', 'user:1')}")

Leaderless Replication (Dynamo-style)
# Any node can accept reads/writes
# Quorum-based consistency: W + R > N

class DynamoStyleStore:
    """Leaderless replication with quorum consistency."""
    
    def __init__(self, n=3, w=2, r=2):
        """
        n: replication factor
        w: write quorum (min nodes that must ack write)
        r: read quorum (min nodes that must respond to read)
        """
        self.n = n
        self.w = w
        self.r = r
        self.nodes = [{} for _ in range(n)]
        self.vector_clocks = [defaultdict(dict) for _ in range(n)]
        self.lock = threading.Lock()
    
    def _coordinator_nodes(self, key):
        """Get coordinator nodes for a key."""
        h = int(hashlib.md5(key.encode()).hexdigest(), 16)
        primary = h % self.n
        return [(primary + i) % self.n for i in range(self.n)]
    
    def write(self, key, value):
        """Write with quorum W."""
        with self.lock:
            nodes = self._coordinator_nodes(key)
            acks = 0
            
            # Update vector clock
            primary = nodes[0]
            self.vector_clocks[primary][key][primary] += 1
            vc = dict(self.vector_clocks[primary][key])
            
            for node_id in nodes[:self.w]:
                self.nodes[node_id][key] = (value, vc)
                self.vector_clocks[node_id][key] = vc.copy()
                acks += 1
            
            return acks >= self.w
    
    def read(self, key):
        """Read with quorum R, reconcile conflicts."""
        nodes = self._coordinator_nodes(key)
        results = []
        
        for node_id in nodes[:self.r]:
            if key in self.nodes[node_id]:
                value, vc = self.nodes[node_id][key]
                results.append((value, vc))
        
        if not results:
            return None
        
        # Reconcile: return latest value (simplified)
        # Real implementation would merge vector clocks
        return results[0][0]

# Example
db = DynamoStyleStore(n=3, w=2, r=2)
db.write("x", 100)
print(f"Read x: {db.read('x')}")

CHAPTER 4: PARTITIONING (SHARDING)
Hash Partitioning
# Distribute data across nodes using hash function

class HashPartitioner:
    """Hash-based partitioning."""
    
    def __init__(self, num_partitions):
        self.num_partitions = num_partitions
        self.partitions = [{} for _ in range(num_partitions)]
    
    def _partition_id(self, key):
        """Determine partition for a key."""
        h = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return h % self.num_partitions
    
    def put(self, key, value):
        """Store key-value in appropriate partition."""
        pid = self._partition_id(key)
        self.partitions[pid][key] = value
    
    def get(self, key):
        """Retrieve value from appropriate partition."""
        pid = self._partition_id(key)
        return self.partitions[pid].get(key)
    
    def get_partition_stats(self):
        """Get size of each partition."""
        return [len(p) for p in self.partitions]

# Example
partitioner = HashPartitioner(num_partitions=4)
for i in range(100):
    partitioner.put(f"user:{i}", f"data_{i}")

print(f"Partition sizes: {partitioner.get_partition_stats()}")
print(f"user:42 = {partitioner.get('user:42')}")

Range Partitioning
# Partition by key ranges (e.g., A-M, N-Z)

class RangePartitioner:
    """Range-based partitioning."""
    
    def __init__(self, ranges):
        """
        ranges: list of (start, end) tuples
        Example: [('A', 'M'), ('N', 'Z')]
        """
        self.ranges = ranges
        self.partitions = [{} for _ in range(len(ranges))]
    
    def _partition_id(self, key):
        """Find partition for key based on range."""
        for i, (start, end) in enumerate(self.ranges):
            if start <= key <= end:
                return i
        return len(self.ranges) - 1  # Overflow partition
    
    def put(self, key, value):
        pid = self._partition_id(key)
        self.partitions[pid][key] = value
    
    def get(self, key):
        pid = self._partition_id(key)
        return self.partitions[pid].get(key)
    
    def range_query(self, start, end):
        """Query across range of keys."""
        results = {}
        for i, (r_start, r_end) in enumerate(self.ranges):
            if not (end < r_start or start > r_end):
                # Overlapping range
                for k, v in self.partitions[i].items():
                    if start <= k <= end:
                        results[k] = v
        return results

# Example
partitioner = RangePartitioner([
    ('A', 'F'),
    ('G', 'M'),
    ('N', 'S'),
    ('T', 'Z')
])

for name in ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", 
             "George", "Helen", "Ivan", "John", "Kate", "Liam",
             "Mary", "Nick", "Olivia", "Paul", "Quinn", "Rachel",
             "Sam", "Tina", "Uma", "Victor", "Wendy", "Xavier", 
             "Yara", "Zoe"]:
    partitioner.put(name, f"data_{name}")

print(f"Partition sizes: {[len(p) for p in partitioner.partitions]}")
print(f"Range query D-K: {list(partitioner.range_query('D', 'K').keys())}")

Consistent Hashing
# Minimize data movement when nodes added/removed

class ConsistentHashRing:
    """Consistent hashing with virtual nodes."""
    
    def __init__(self, num_nodes=3, virtual_nodes=100):
        self.num_nodes = num_nodes
        self.virtual_nodes = virtual_nodes
        self.ring = {}  # hash -> node_id
        self.node_data = {i: {} for i in range(num_nodes)}
        self._build_ring()
    
    def _build_ring(self):
        """Build hash ring with virtual nodes."""
        for node_id in range(self.num_nodes):
            for v in range(self.virtual_nodes):
                vnode_key = f"node{node_id}:vnode{v}"
                h = int(hashlib.md5(vnode_key.encode()).hexdigest(), 16)
                self.ring[h] = node_id
    
    def _get_node(self, key):
        """Find node for a key."""
        h = int(hashlib.md5(key.encode()).hexdigest(), 16)
        
        # Find first node clockwise
        sorted_hashes = sorted(self.ring.keys())
        for node_hash in sorted_hashes:
            if node_hash >= h:
                return self.ring[node_hash]
        
        # Wrap around
        return self.ring[sorted_hashes[0]]
    
    def put(self, key, value):
        node_id = self._get_node(key)
        self.node_data[node_id][key] = value
    
    def get(self, key):
        node_id = self._get_node(key)
        return self.node_data[node_id].get(key)
    
    def get_distribution(self):
        """Get number of keys per node."""
        return {f"node_{i}": len(data) 
                for i, data in self.node_data.items()}

# Example
ring = ConsistentHashRing(num_nodes=3, virtual_nodes=150)
for i in range(1000):
    ring.put(f"key:{i}", f"value:{i}")

print(f"Key distribution: {ring.get_distribution()}")
print(f"key:42 = {ring.get('key:42')}")

CHAPTER 5: DISTRIBUTED TRANSACTIONS
Two-Phase Commit (2PC)
# Coordinator + participants
# Phase 1: Prepare (vote)
# Phase 2: Commit/Abort

class TwoPhaseCommit:
    """2PC coordinator implementation."""
    
    def __init__(self, participants):
        self.participants = participants
        self.transaction_log = []
    
    def execute(self, operations):
        """Execute distributed transaction."""
        # Phase 1: Prepare
        votes = []
        for participant in self.participants:
            vote = participant.prepare(operations)
            votes.append(vote)
            self.transaction_log.append({
                'phase': 'prepare',
                'participant': participant.node_id,
                'vote': vote
            })
        
        # Decide
        if all(votes):
            # Phase 2: Commit
            for participant in self.participants:
                participant.commit()
                self.transaction_log.append({
                    'phase': 'commit',
                    'participant': participant.node_id
                })
            return True
        else:
            # Phase 2: Abort
            for participant in self.participants:
                participant.abort()
                self.transaction_log.append({
                    'phase': 'abort',
                    'participant': participant.node_id
                })
            return False

class Participant:
    """2PC participant."""
    
    def __init__(self, node_id):
        self.node_id = node_id
        self.data = {}
        self.temp_data = {}
        self.prepared = False
    
    def prepare(self, operations):
        """Phase 1: Validate and lock."""
        try:
            # Simulate validation
            for op in operations:
                if op['type'] == 'write':
                    self.temp_data[op['key']] = op['value']
            
            self.prepared = True
            return True
        except Exception:
            return False
    
    def commit(self):
        """Phase 2: Apply changes."""
        if self.prepared:
            self.data.update(self.temp_data)
            self.temp_data.clear()
            self.prepared = False
    
    def abort(self):
        """Phase 2: Discard changes."""
        self.temp_data.clear()
        self.prepared = False

# Example
participants = [Participant(f"P{i}") for i in range(3)]
coordinator = TwoPhaseCommit(participants)

operations = [
    {'type': 'write', 'key': 'x', 'value': 100},
    {'type': 'write', 'key': 'y', 'value': 200}
]

success = coordinator.execute(operations)
print(f"Transaction success: {success}")
print(f"P0 data: {participants[0].data}")
print(f"Transaction log: {len(coordinator.transaction_log)} entries")

Sagas (Long-Running Transactions)
# Sequence of local transactions with compensating actions

class Saga:
    """Saga pattern for distributed transactions."""
    
    def __init__(self):
        self.steps = []
        self.compensations = []
        self.executed = []
    
    def add_step(self, action, compensation):
        """Add step with its compensation."""
        self.steps.append(action)
        self.compensations.append(compensation)
    
    def execute(self):
        """Execute saga with rollback on failure."""
        try:
            for i, step in enumerate(self.steps):
                step()
                self.executed.append(i)
                print(f"  ✓ Step {i+1} executed")
            return True
        except Exception as e:
            print(f"  ✗ Step {i+1} failed: {e}")
            # Compensate in reverse order
            for j in reversed(self.executed):
                try:
                    self.compensations[j]()
                    print(f"  ↩ Compensated step {j+1}")
                except Exception as ce:
                    print(f"  ✗ Compensation failed: {ce}")
            return False

# Example: travel booking saga
saga = Saga()

def book_flight():
    print("    Booking flight...")
    # Simulate failure on 3rd attempt
    if not hasattr(book_flight, 'attempts'):
        book_flight.attempts = 0
    book_flight.attempts += 1
    if book_flight.attempts > 2:
        raise Exception("Flight unavailable")

def cancel_flight():
    print("    Canceling flight...")

def book_hotel():
    print("    Booking hotel...")

def cancel_hotel():
    print("    Canceling hotel...")

def book_car():
    print("    Booking car...")

def cancel_car():
    print("    Canceling car...")

saga.add_step(book_flight, cancel_flight)
saga.add_step(book_hotel, cancel_hotel)
saga.add_step(book_car, cancel_car)

print("=== Saga Execution ===")
success = saga.execute()
print(f"Saga completed: {success}")

CHAPTER 6: CRDTs (CONFLICT-FREE REPLICATED DATA TYPES)
G-Counter (Grow-Only Counter)
# Each node maintains its own counter
# Value = sum of all node counters

class GCounter:
    """Grow-only counter CRDT."""
    
    def __init__(self, node_id, num_nodes):
        self.node_id = node_id
        self.counters = [0] * num_nodes
    
    def increment(self, amount=1):
        """Increment local counter."""
        self.counters[self.node_id] += amount
    
    def value(self):
        """Get total value (sum of all counters)."""
        return sum(self.counters)
    
    def merge(self, other):
        """Merge with another G-Counter (take max)."""
        for i in range(len(self.counters)):
            self.counters[i] = max(self.counters[i], other.counters[i])

# Example
gc1 = GCounter(0, 3)
gc2 = GCounter(1, 3)
gc3 = GCounter(2, 3)

gc1.increment(5)
gc2.increment(3)
gc3.increment(7)

print(f"GC1 value: {gc1.value()}")
print(f"GC2 value: {gc2.value()}")

# Merge
gc1.merge(gc2)
gc1.merge(gc3)
print(f"GC1 after merge: {gc1.value()}")  # Should be 15

PN-Counter (Positive-Negative Counter)
# Two G-Counters: one for increments, one for decrements

class PNCounter:
    """Positive-Negative counter CRDT."""
    
    def __init__(self, node_id, num_nodes):
        self.node_id = node_id
        self.p = GCounter(node_id, num_nodes)  # Positive
        self.n = GCounter(node_id, num_nodes)  # Negative
    
    def increment(self, amount=1):
        self.p.increment(amount)
    
    def decrement(self, amount=1):
        self.n.increment(amount)
    
    def value(self):
        return self.p.value() - self.n.value()
    
    def merge(self, other):
        self.p.merge(other.p)
        self.n.merge(other.n)

# Example
pn1 = PNCounter(0, 2)
pn2 = PNCounter(1, 2)

pn1.increment(10)
pn2.increment(5)
pn1.decrement(3)

print(f"\nPN1 value: {pn1.value()}")  # 10 - 3 = 7
print(f"PN2 value: {pn2.value()}")  # 5

pn1.merge(pn2)
print(f"PN1 after merge: {pn1.value()}")  # 15 - 3 = 12

G-Set (Grow-Only Set)
# Elements can only be added, never removed

class GSet:
    """Grow-only set CRDT."""
    
    def __init__(self):
        self.elements = set()
    
    def add(self, element):
        self.elements.add(element)
    
    def contains(self, element):
        return element in self.elements
    
    def value(self):
        return self.elements.copy()
    
    def merge(self, other):
        self.elements.update(other.elements)

# Example
gs1 = GSet()
gs2 = GSet()

gs1.add("Alice")
gs1.add("Bob")
gs2.add("Charlie")
gs2.add("David")

gs1.merge(gs2)
print(f"\nG-Set: {gs1.value()}")

2P-Set (Two-Phase Set)
# Add set + remove set, tombstone semantics

class TwoPSet:
    """Two-phase set CRDT."""
    
    def __init__(self):
        self.add_set = set()
        self.remove_set = set()
    
    def add(self, element):
        if element not in self.remove_set:
            self.add_set.add(element)
    
    def remove(self, element):
        if element in self.add_set:
            self.remove_set.add(element)
    
    def contains(self, element):
        return element in self.add_set and element not in self.remove_set
    
    def value(self):
        return self.add_set - self.remove_set
    
    def merge(self, other):
        self.add_set.update(other.add_set)
        self.remove_set.update(other.remove_set)

# Example
tp1 = TwoPSet()
tp2 = TwoPSet()

tp1.add("Alice")
tp1.add("Bob")
tp2.add("Charlie")
tp1.remove("Bob")

tp1.merge(tp2)
print(f"2P-Set: {tp1.value()}")  # Alice, Charlie (Bob removed)

LWW-Register (Last-Writer-Wins)
# Each write has a timestamp, latest wins

class LWWRegister:
    """Last-Writer-Wins register CRDT."""
    
    def __init__(self, node_id):
        self.node_id = node_id
        self.value_data = None
        self.timestamp = 0
    
    def set(self, value):
        self.timestamp = time.time()
        self.value_data = value
    
    def get(self):
        return self.value_data
    
    def merge(self, other):
        if other.timestamp > self.timestamp:
            self.value_data = other.value_data
            self.timestamp = other.timestamp

# Example
reg1 = LWWRegister(0)
reg2 = LWWRegister(1)

reg1.set("value_A")
time.sleep(0.01)
reg2.set("value_B")

reg1.merge(reg2)
print(f"LWW Register: {reg1.get()}")  # value_B (later timestamp)

OR-Set (Observed-Remove Set)
# Add/remove with unique tags, supports concurrent operations

class ORSet:
    """Observed-Remove set CRDT."""
    
    def __init__(self, node_id):
        self.node_id = node_id
        self.elements = {}  # element -> set of unique tags
        self.tombstones = set()
        self.tag_counter = 0
    
    def _generate_tag(self):
        self.tag_counter += 1
        return f"{self.node_id}:{self.tag_counter}"
    
    def add(self, element):
        tag = self._generate_tag()
        if element not in self.elements:
            self.elements[element] = set()
        self.elements[element].add(tag)
        # Remove from tombstones if re-added
        self.tombstones.discard(tag)
    
    def remove(self, element):
        if element in self.elements:
            # Move all tags to tombstones
            self.tombstones.update(self.elements[element])
            del self.elements[element]
    
    def contains(self, element):
        return element in self.elements
    
    def value(self):
        return set(self.elements.keys())
    
    def merge(self, other):
        # Union of elements
        for elem, tags in other.elements.items():
            if elem not in self.elements:
                self.elements[elem] = set()
            self.elements[elem].update(tags)
        
        # Remove tombstoned tags
        self.tombstones.update(other.tombstones)
        for elem in list(self.elements.keys()):
            self.elements[elem] -= self.tombstones
            if not self.elements[elem]:
                del self.elements[elem]

# Example
or1 = ORSet(0)
or2 = ORSet(1)

or1.add("Alice")
or2.add("Alice")  # Concurrent add
or1.remove("Alice")

or1.merge(or2)
print(f"OR-Set: {or1.value()}")  # Alice (concurrent add wins)

CHAPTER 7: REAL-WORLD DISTRIBUTED DATABASES
CockroachDB Architecture
# Distributed SQL database built on Raft consensus
# Features: strong consistency, automatic sharding, geo-replication

class CockroachDBSimulator:
    """Simplified CockroachDB simulation."""
    
    def __init__(self, num_nodes=3):
        self.num_nodes = num_nodes
        self.ranges = {}  # range_id -> (start_key, end_key, replicas)
        self.raft_groups = {}  # range_id -> leader
        self.data = {i: {} for i in range(num_nodes)}
        self.range_counter = 0
    
    def split_range(self, start_key, end_key, split_key):
        """Split a range at split_key."""
        # Find existing range
        range_id = None
        for rid, (s, e, replicas) in self.ranges.items():
            if s <= start_key < e:
                range_id = rid
                break
        
        if range_id is None:
            return False
        
        # Create new range
        new_range_id = self.range_counter
        self.range_counter += 1
        
        old_start, old_end, replicas = self.ranges[range_id]
        
        # Update ranges
        self.ranges[range_id] = (old_start, split_key, replicas)
        self.ranges[new_range_id] = (split_key, old_end, replicas)
        
        # Elect leaders (simplified)
        self.raft_groups[range_id] = replicas[0]
        self.raft_groups[new_range_id] = replicas[0]
        
        return True
    
    def write(self, key, value):
        """Write to appropriate range."""
        # Find range
        for rid, (start, end, replicas) in self.ranges.items():
            if start <= key < end:
                leader = self.raft_groups[rid]
                # Replicate to followers
                for replica in replicas:
                    self.data[replica][key] = value
                return True
        return False
    
    def read(self, key):
        """Read from any replica (linearizable with lease)."""
        for rid, (start, end, replicas) in self.ranges.items():
            if start <= key < end:
                leader = self.raft_groups[rid]
                return self.data[leader].get(key)
        return None

# Example
cdb = CockroachDBSimulator(num_nodes=3)

# Create initial range
cdb.ranges[0] = ('a', 'z', [0, 1, 2])
cdb.raft_groups[0] = 0

# Write data
cdb.write('user:1', 'Alice')
cdb.write('user:2', 'Bob')

# Split range
cdb.split_range('a', 'z', 'm')

print("CockroachDB ranges:")
for rid, (start, end, replicas) in cdb.ranges.items():
    leader = cdb.raft_groups[rid]
    print(f"  Range {rid}: [{start}, {end}) → leader={leader}, replicas={replicas}")

print(f"Read user:1 = {cdb.read('user:1')}")

Google Spanner Architecture
# Globally distributed, strong consistency via TrueTime
# Uses Paxos for replication, 2PC for transactions

class SpannerSimulator:
    """Simplified Spanner simulation with TrueTime."""
    
    def __init__(self):
        self.data = {}
        self.timestamps = {}
        self.true_time_offset = 0  # Simulated clock uncertainty
    
    def _get_commit_timestamp(self):
        """Get commit timestamp with TrueTime guarantee."""
        # In real Spanner: TrueTime API returns [earliest, latest]
        # Commit timestamp must be > latest
        return time.time() + self.true_time_offset
    
    def begin_transaction(self):
        """Begin a read-write transaction."""
        return {
            'read_timestamp': time.time(),
            'writes': [],
            'commit_timestamp': None
        }
    
    def read(self, txn, key):
        """Read within transaction (snapshot isolation)."""
        # Read at transaction's read timestamp
        if key in self.data:
            # Find version <= read_timestamp
            versions = self.data[key]
            for ts, value in reversed(versions):
                if ts <= txn['read_timestamp']:
                    return value
        return None
    
    def write(self, txn, key, value):
        """Buffer write in transaction."""
        txn['writes'].append((key, value))
    
    def commit(self, txn):
        """Commit transaction with 2PC."""
        # Get commit timestamp
        commit_ts = self._get_commit_timestamp()
        
        # Check for conflicts (simplified)
        for key, _ in txn['writes']:
            if key in self.data:
                latest_ts = max(ts for ts, _ in self.data[key])
                if latest_ts > txn['read_timestamp']:
                    # Conflict detected
                    return False
        
        # Apply writes
        for key, value in txn['writes']:
            if key not in self.data:
                self.data[key] = []
            self.data[key].append((commit_ts, value))
        
        txn['commit_timestamp'] = commit_ts
        return True

# Example
spanner = SpannerSimulator()

# Transaction 1
txn1 = spanner.begin_transaction()
spanner.write(txn1, 'account:1', 100)
spanner.write(txn1, 'account:2', 200)
success = spanner.commit(txn1)
print(f"\nSpanner TX1 committed: {success}")

# Transaction 2 (read snapshot)
txn2 = spanner.begin_transaction()
val1 = spanner.read(txn2, 'account:1')
val2 = spanner.read(txn2, 'account:2')
print(f"Spanner read: account:1={val1}, account:2={val2}")

Cassandra Data Model
# Wide-column store, partition key + clustering key
# Tunable consistency (ONE, QUORUM, ALL)

class CassandraSimulator:
    """Simplified Cassandra simulation."""
    
    def __init__(self, num_nodes=3, replication_factor=3):
        self.num_nodes = num_nodes
        self.rf = replication_factor
        self.nodes = [{} for _ in range(num_nodes)]
        self.token_ring = self._build_token_ring()
    
    def _build_token_ring(self):
        """Build consistent hash ring."""
        ring = []
        for i in range(self.num_nodes):
            token = (2**64 // self.num_nodes) * i
            ring.append((token, i))
        return sorted(ring)
    
    def _get_token(self, partition_key):
        """Get token for partition key."""
        return int(hashlib.md5(partition_key.encode()).hexdigest(), 16) % (2**64)
    
    def _get_replicas(self, token):
        """Get replica nodes for token."""
        replicas = []
        for i, (ring_token, node_id) in enumerate(self.token_ring):
            if ring_token >= token:
                # Start from this node
                for j in range(self.rf):
                    replicas.append(self.token_ring[(i + j) % len(self.token_ring)][1])
                break
        return replicas
    
    def write(self, table, partition_key, clustering_key, columns, 
              consistency='QUORUM'):
        """Write with specified consistency level."""
        token = self._get_token(partition_key)
        replicas = self._get_replicas(token)
        
        # Determine required acks
        if consistency == 'ONE':
            required = 1
        elif consistency == 'QUORUM':
            required = (self.rf // 2) + 1
        elif consistency == 'ALL':
            required = self.rf
        else:
            required = 1
        
        # Write to replicas
        acks = 0
        for replica_id in replicas[:required]:
            key = f"{partition_key}:{clustering_key}"
            if key not in self.nodes[replica_id]:
                self.nodes[replica_id][key] = {}
            self.nodes[replica_id][key].update(columns)
            acks += 1
        
        return acks >= required
    
    def read(self, table, partition_key, clustering_key=None,
             consistency='QUORUM'):
        """Read with specified consistency level."""
        token = self._get_token(partition_key)
        replicas = self._get_replicas(token)
        
        # Determine required responses
        if consistency == 'ONE':
            required = 1
        elif consistency == 'QUORUM':
            required = (self.rf // 2) + 1
        else:
            required = self.rf
        
        # Read from replicas
        results = []
        for replica_id in replicas[:required]:
            if clustering_key:
                key = f"{partition_key}:{clustering_key}"
                if key in self.nodes[replica_id]:
                    results.append(self.nodes[replica_id][key])
            else:
                # Range query
                prefix = f"{partition_key}:"
                for k, v in self.nodes[replica_id].items():
                    if k.startswith(prefix):
                        results.append(v)
        
        # Read repair: reconcile differences (simplified)
        return results[0] if results else None

# Example
cass = CassandraSimulator(num_nodes=3, replication_factor=3)

# Write data
cass.write('users', 'user:1', 'profile', 
           {'name': 'Alice', 'age': 30}, consistency='QUORUM')
cass.write('users', 'user:1', 'settings',
           {'theme': 'dark', 'lang': 'en'}, consistency='QUORUM')

# Read data
profile = cass.read('users', 'user:1', 'profile', consistency='ONE')
print(f"\nCassandra read: {profile}")

CHAPTER 8: QUERY PROCESSING IN DISTRIBUTED DBs
Distributed Query Planning
# Break query into subqueries, execute on relevant nodes

class DistributedQueryPlanner:
    """Simplified distributed query planner."""
    
    def __init__(self, num_shards):
        self.num_shards = num_shards
        self.shard_stats = {i: {'rows': 1000, 'selectivity': 0.1} 
                           for i in range(num_shards)}
    
    def plan_table_scan(self, table, predicate=None):
        """Plan a table scan across all shards."""
        plan = {
            'type': 'distributed_scan',
            'shards': list(range(self.num_shards)),
            'predicate': predicate,
            'estimated_cost': 0
        }
        
        # Estimate cost
        for shard_id in plan['shards']:
            stats = self.shard_stats[shard_id]
            rows = stats['rows']
            if predicate:
                rows *= stats['selectivity']
            plan['estimated_cost'] += rows
        
        return plan
    
    def plan_index_lookup(self, table, index_key, value):
        """Plan an index lookup (single shard)."""
        # Determine which shard owns this key
        shard_id = hash(value) % self.num_shards
        
        return {
            'type': 'index_lookup',
            'shard': shard_id,
            'index': index_key,
            'value': value,
            'estimated_cost': 1
        }
    
    def plan_join(self, left_table, right_table, join_key, strategy='broadcast'):
        """Plan a distributed join."""
        if strategy == 'broadcast':
            # Broadcast smaller table to all shards
            return {
                'type': 'broadcast_join',
                'broadcast_table': right_table,
                'probe_table': left_table,
                'join_key': join_key,
                'shards': list(range(self.num_shards))
            }
        elif strategy == 'shuffle':
            # Shuffle both tables by join key
            return {
                'type': 'shuffle_join',
                'left_table': left_table,
                'right_table': right_table,
                'join_key': join_key,
                'shards': list(range(self.num_shards))
            }
    
    def optimize(self, query_plan):
        """Optimize query plan."""
        # Simple optimization: push down predicates
        if query_plan['type'] == 'distributed_scan':
            if query_plan.get('predicate'):
                # Reduce estimated rows
                for shard_id in query_plan['shards']:
                    self.shard_stats[shard_id]['selectivity'] = 0.01
        
        return query_plan

# Example
planner = DistributedQueryPlanner(num_shards=4)

# Plan queries
scan_plan = planner.plan_table_scan('users', predicate='age > 30')
print(f"Table scan plan: {scan_plan['type']}, cost: {scan_plan['estimated_cost']}")

lookup_plan = planner.plan_index_lookup('users', 'idx_email', 'alice@example.com')
print(f"Index lookup plan: shard {lookup_plan['shard']}")

join_plan = planner.plan_join('users', 'orders', 'user_id', strategy='broadcast')
print(f"Join plan: {join_plan['type']}")

Distributed Aggregation
# Partial aggregation on each shard, final aggregation on coordinator

class DistributedAggregator:
    """Distributed aggregation (MapReduce-style)."""
    
    def __init__(self, num_shards):
        self.num_shards = num_shards
        self.shard_data = {i: [] for i in range(num_shards)}
    
    def load_data(self, shard_id, data):
        """Load data into a shard."""
        self.shard_data[shard_id] = data
    
    def map_phase(self, map_func):
        """Apply map function to each shard."""
        partial_results = {}
        for shard_id, data in self.shard_data.items():
            partial_results[shard_id] = map_func(data)
        return partial_results
    
    def reduce_phase(self, partial_results, reduce_func):
        """Reduce partial results."""
        return reduce_func(list(partial_results.values()))
    
    def aggregate(self, map_func, reduce_func):
        """Full MapReduce aggregation."""
        partial = self.map_phase(map_func)
        return self.reduce_phase(partial, reduce_func)

# Example: distributed sum
aggregator = DistributedAggregator(num_shards=3)
aggregator.load_data(0, [1, 2, 3, 4, 5])
aggregator.load_data(1, [6, 7, 8, 9, 10])
aggregator.load_data(2, [11, 12, 13, 14, 15])

def map_sum(data):
    return sum(data)

def reduce_sum(partial_sums):
    return sum(partial_sums)

total = aggregator.aggregate(map_sum, reduce_sum)
print(f"\nDistributed sum: {total}")  # Should be 120

# Distributed count
def map_count(data):
    return len(data)

def reduce_count(partial_counts):
    return sum(partial_counts)

count = aggregator.aggregate(map_count, reduce_count)
print(f"Distributed count: {count}")  # Should be 15

CHAPTER 9: FAULT TOLERANCE AND RECOVERY
Failure Detection
# Heartbeat-based failure detection

class FailureDetector:
    """Phi accrual failure detector."""
    
    def __init__(self, threshold=8.0):
        self.threshold = threshold
        self.heartbeats = {}  # node_id -> list of timestamps
        self.last_heartbeat = {}
    
    def record_heartbeat(self, node_id):
        """Record heartbeat from node."""
        now = time.time()
        
        if node_id not in self.heartbeats:
            self.heartbeats[node_id] = []
        
        self.heartbeats[node_id].append(now)
        self.last_heartbeat[node_id] = now
        
        # Keep only last 100 heartbeats
        if len(self.heartbeats[node_id]) > 100:
            self.heartbeats[node_id] = self.heartbeats[node_id][-100:]
    
    def phi(self, node_id):
        """Calculate phi value (suspicion level)."""
        if node_id not in self.heartbeats:
            return 0.0
        
        now = time.time()
        intervals = []
        heartbeats = self.heartbeats[node_id]
        
        for i in range(1, len(heartbeats)):
            intervals.append(heartbeats[i] - heartbeats[i-1])
        
        if not intervals:
            return 0.0
        
        # Calculate mean and std dev
        mean = sum(intervals) / len(intervals)
        variance = sum((x - mean) ** 2 for x in intervals) / len(intervals)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            return 0.0
        
        # Time since last heartbeat
        t = now - self.last_heartbeat[node_id]
        
        # Phi = -log10(P(t > now - last))
        # Simplified: use normal distribution
        z = (t - mean) / std_dev
        from math import erfc
        p_later = 0.5 * erfc(z / (2 ** 0.5))
        
        if p_later <= 0:
            return 16.0  # Max phi
        
        return -math.log10(p_later)
    
    def is_alive(self, node_id):
        """Check if node is alive."""
        return self.phi(node_id) < self.threshold

# Example
detector = FailureDetector(threshold=8.0)

# Simulate heartbeats
for i in range(10):
    detector.record_heartbeat('node_1')
    time.sleep(0.1)

print(f"Node 1 phi: {detector.phi('node_1'):.2f}")
print(f"Node 1 alive: {detector.is_alive('node_1')}")

# Simulate failure (no heartbeats)
time.sleep(2)
print(f"After 2s - Node 1 phi: {detector.phi('node_1'):.2f}")
print(f"Node 1 alive: {detector.is_alive('node_1')}")

Write-Ahead Logging (WAL)
# Ensure durability by logging before applying

class WriteAheadLog:
    """WAL for crash recovery."""
    
    def __init__(self):
        self.log = []
        self.applied_lsn = 0
    
    def append(self, operation):
        """Append operation to log."""
        lsn = len(self.log) + 1
        self.log.append({
            'lsn': lsn,
            'operation': operation,
            'timestamp': time.time()
        })
        return lsn
    
    def apply(self, lsn):
        """Mark operation as applied."""
        self.applied_lsn = max(self.applied_lsn, lsn)
    
    def recover(self):
        """Recover unapplied operations."""
        unapplied = []
        for entry in self.log:
            if entry['lsn'] > self.applied_lsn:
                unapplied.append(entry)
        return unapplied
    
    def checkpoint(self):
        """Create checkpoint (truncate log)."""
        self.log = [e for e in self.log if e['lsn'] > self.applied_lsn]

# Example
wal = WriteAheadLog()

# Write operations
lsn1 = wal.append({'type': 'INSERT', 'table': 'users', 'data': {'id': 1}})
lsn2 = wal.append({'type': 'UPDATE', 'table': 'users', 'data': {'id': 1, 'name': 'Alice'}})

# Apply first operation
wal.apply(lsn1)

# Simulate crash and recovery
unapplied = wal.recover()
print(f"\nWAL recovery: {len(unapplied)} unapplied operations")
for op in unapplied:
    print(f"  LSN {op['lsn']}: {op['operation']}")

Anti-Entropy (Read Repair)
# Background process to fix inconsistencies

class AntiEntropyRepair:
    """Anti-entropy repair mechanism."""
    
    def __init__(self, replicas):
        self.replicas = replicas  # list of data stores
    
    def compare_digests(self, replica1_id, replica2_id):
        """Compare Merkle trees between replicas."""
        # Simplified: compare key sets
        keys1 = set(self.replicas[replica1_id].keys())
        keys2 = set(self.replicas[replica2_id].keys())
        
        missing_in_1 = keys2 - keys1
        missing_in_2 = keys1 - keys2
        common = keys1 & keys2
        
        # Check for value differences
        different_values = []
        for key in common:
            val1 = self.replicas[replica1_id][key]
            val2 = self.replicas[replica2_id][key]
            if val1 != val2:
                different_values.append(key)
        
        return {
            'missing_in_1': missing_in_1,
            'missing_in_2': missing_in_2,
            'different_values': different_values
        }
    
    def repair(self, replica1_id, replica2_id):
        """Repair inconsistencies between replicas."""
        diff = self.compare_digests(replica1_id, replica2_id)
        
        # Copy missing keys
        for key in diff['missing_in_1']:
            self.replicas[replica1_id][key] = self.replicas[replica2_id][key]
        
        for key in diff['missing_in_2']:
            self.replicas[replica2_id][key] = self.replicas[replica1_id][key]
        
        # Resolve conflicts (LWW)
        for key in diff['different_values']:
            # Simplified: keep replica1's value
            self.replicas[replica2_id][key] = self.replicas[replica1_id][key]
        
        return len(diff['missing_in_1']) + len(diff['missing_in_2']) + len(diff['different_values'])

# Example
replicas = [
    {'a': 1, 'b': 2, 'c': 3},
    {'a': 1, 'b': 2, 'd': 4},  # Missing 'c', has extra 'd'
    {'a': 1, 'b': 99, 'c': 3}  # Different value for 'b'
]

repair = AntiEntropyRepair(replicas)
repaired = repair.repair(0, 1)
print(f"\nAnti-entropy repair: {repaired} inconsistencies fixed")
print(f"Replica 0: {replicas[0]}")
print(f"Replica 1: {replicas[1]}")

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Modern Distributed DB Trends
# NewSQL: CockroachDB, TiDB, YugabyteDB
# - SQL compatibility + distributed scalability
# - Strong consistency + high availability

# Multi-model databases:
# - ArangoDB (document, graph, key-value)
# - OrientDB (document, graph)
# - Cosmos DB (multi-API: SQL, MongoDB, Cassandra, Gremlin, Table)

# Edge databases:
# - Data locality for low latency
# - Geo-replication by default
# - Examples: FaunaDB, PlanetScale

# Serverless databases:
# - Auto-scaling, pay-per-use
# - Examples: Aurora Serverless, PlanetScale, Neon

Performance Tuning
# 1. Partitioning strategy
#    - Hash: even distribution, poor range queries
#    - Range: good range queries, hotspots possible
#    - Consistent hashing: minimal rebalancing

# 2. Replication factor
#    - Higher RF = more availability, more storage
#    - Typical: RF=3 for production

# 3. Consistency level
#    - Strong: higher latency, guaranteed correctness
#    - Eventual: lower latency, possible stale reads
#    - Tunable: balance per query

# 4. Connection pooling
#    - Reuse connections to reduce overhead
#    - Tools: PgBouncer (PostgreSQL), ProxySQL (MySQL)

# 5. Caching
#    - Read cache: Redis, Memcached
#    - Write buffer: reduce write amplification

# 6. Indexing
#    - Secondary indexes in distributed DBs are expensive
#    - Consider materialized views for complex queries

Recommended Reading
# - "Designing Data-Intensive Applications" by Martin Kleppmann
# - "Database Internals" by Alex Petrov
# - "Distributed Systems: Principles and Paradigms" by Tanenbaum
# - Google Spanner paper (Corbett et al., 2013)
# - Dynamo paper (DeCandia et al., 2007)
# - Bigtable paper (Chang et al., 2006)

# Online Resources
# - CockroachDB docs: https://www.cockroachlabs.com/docs/
# - Cassandra docs: https://cassandra.apache.org/doc/
# - Spanner docs: https://cloud.google.com/spanner/docs
# - Jepsen (consistency testing): https://jepsen.io/
# - CIDR conference (database research)

# End of Distributed Databases Reference