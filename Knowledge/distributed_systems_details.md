Distributed Systems & Consensus Algorithms Complete Reference
CHAPTER 1: GETTING STARTED WITH DISTRIBUTED SYSTEMS
Remarks
Distributed systems are collections of independent computers that appear to users as a single coherent system. Key challenges: partial failures, network latency, clock synchronization, consensus, and consistency. Used in: cloud computing (AWS, GCP), databases (Cassandra, CockroachDB), blockchains, microservices, CDNs.
Tools: Python (for simulations), Go (production systems), etcd, Consul, ZooKeeper.
Hello Distributed
# hello_distributed.py
import socket
import threading
import time

def start_server(host='localhost', port=5000):
    """Simple TCP server that echoes messages."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")
    
    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()

def handle_client(conn):
    """Handle individual client connection."""
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Received: {data}")
        conn.send(f"Echo: {data}".encode())
    conn.close()

def start_client(host='localhost', port=5000, message="Hello"):
    """Simple TCP client."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(message.encode())
    response = client.recv(1024).decode()
    print(f"Response: {response}")
    client.close()

# Usage:
# threading.Thread(target=start_server).start()
# time.sleep(1)
# start_client(message="Test message")

CHAPTER 2: CAP THEOREM AND CONSISTENCY MODELS
CAP Theorem
# CAP Theorem: In a distributed system, you can only have 2 of 3:
# - Consistency (C): Every read returns the most recent write
# - Availability (A): Every request receives a response
# - Partition tolerance (P): System continues despite network failures
#
# Since partitions are inevitable in distributed systems, you must choose CP or AP.

class CAPSystem:
    """Demonstrates CAP tradeoffs."""
    
    def __init__(self, mode='CP'):
        self.mode = mode  # 'CP' or 'AP'
        self.data = {}
        self.partitioned = False
    
    def write(self, key, value):
        """Write operation."""
        if self.partitioned and self.mode == 'CP':
            raise Exception("Partition: write blocked for consistency")
        self.data[key] = value
        return True
    
    def read(self, key):
        """Read operation."""
        if self.partitioned and self.mode == 'AP':
            # Return stale data or None
            return self.data.get(key, "STALE_DATA")
        return self.data.get(key)
    
    def simulate_partition(self):
        """Simulate network partition."""
        self.partitioned = True
        print(f"Network partition simulated (mode={self.mode})")

# CP System (like ZooKeeper, HBase)
cp_system = CAPSystem('CP')
cp_system.write('x', 1)
cp_system.simulate_partition()
try:
    cp_system.write('x', 2)  # Will fail
except Exception as e:
    print(f"CP write failed: {e}")

# AP System (like Cassandra, DynamoDB)
ap_system = CAPSystem('AP')
ap_system.write('x', 1)
ap_system.simulate_partition()
print(f"AP read during partition: {ap_system.read('x')}")  # Returns stale data

Consistency Models
# Strong Consistency: Linearizability
# - All operations appear to execute atomically in some total order
# - Every read returns the value from the most recent write

# Sequential Consistency:
# - All operations appear to execute in some total order
# - Operations from each process appear in program order

# Eventual Consistency:
# - If no new updates, eventually all replicas converge
# - Reads may return stale data

class LinearizableStore:
    """Linearizable key-value store (single node for simplicity)."""
    
    def __init__(self):
        self.data = {}
        self.version = 0
        self.lock = threading.Lock()
    
    def write(self, key, value):
        with self.lock:
            self.version += 1
            self.data[key] = (value, self.version)
            return self.version
    
    def read(self, key):
        with self.lock:
            if key in self.data:
                value, version = self.data[key]
                return value, version
            return None, 0

store = LinearizableStore()
v1 = store.write('x', 10)
v2 = store.write('x', 20)
val, ver = store.read('x')
print(f"Read: {val} (version {ver})")  # Returns 20, version 2

CHAPTER 3: LOGICAL CLOCKS AND VECTOR CLOCKS
Lamport Logical Clocks
# Lamport clocks establish causal ordering of events in distributed systems.
# Rules:
# 1. Before executing an event, increment local clock
# 2. Sending a message: increment clock, attach timestamp to message
# 3. Receiving a message: set clock = max(local, received) + 1

class LamportClock:
    """Lamport logical clock implementation."""
    
    def __init__(self, node_id):
        self.node_id = node_id
        self.time = 0
    
    def tick(self):
        """Increment clock for local event."""
        self.time += 1
        return self.time
    
    def send(self):
        """Prepare message with timestamp."""
        self.time += 1
        return {'sender': self.node_id, 'timestamp': self.time}
    
    def receive(self, msg):
        """Update clock on receiving message."""
        self.time = max(self.time, msg['timestamp']) + 1
        return self.time

# Example: Two processes communicating
p1 = LamportClock('P1')
p2 = LamportClock('P2')

# P1 executes event
t1 = p1.tick()  # P1 time = 1
print(f"P1 event at time {t1}")

# P1 sends message to P2
msg = p1.send()  # P1 time = 2
print(f"P1 sends message with timestamp {msg['timestamp']}")

# P2 receives message
t2 = p2.receive(msg)  # P2 time = 3
print(f"P2 receives message, time = {t2}")

# P2 executes event
t3 = p2.tick()  # P2 time = 4
print(f"P2 event at time {t3}")

Vector Clocks
# Vector clocks capture causal relationships more precisely than Lamport clocks.
# Each node maintains a vector of counters, one for each node.
# Rules:
# 1. Before event: increment own counter in vector
# 2. Send message: attach entire vector
# 3. Receive message: element-wise max of vectors, then increment own counter

class VectorClock:
    """Vector clock implementation."""
    
    def __init__(self, node_id, all_nodes):
        self.node_id = node_id
        self.clock = {node: 0 for node in all_nodes}
    
    def tick(self):
        """Increment own counter."""
        self.clock[self.node_id] += 1
        return self.clock.copy()
    
    def send(self):
        """Prepare message with vector clock."""
        self.clock[self.node_id] += 1
        return {'sender': self.node_id, 'vector': self.clock.copy()}
    
    def receive(self, msg):
        """Update vector on receiving message."""
        for node, time in msg['vector'].items():
            self.clock[node] = max(self.clock[node], time)
        self.clock[self.node_id] += 1
        return self.clock.copy()
    
    def compare(self, other):
        """Compare two vector clocks.
        Returns: '<' if self < other, '>' if self > other, '=' if equal, None if concurrent
        """
        le = all(self.clock[n] <= other.clock[n] for n in self.clock)
        ge = all(self.clock[n] >= other.clock[n] for n in self.clock)
        
        if le and ge:
            return '='
        elif le:
            return '<'
        elif ge:
            return '>'
        else:
            return None  # Concurrent events

# Example: Three nodes
nodes = ['A', 'B', 'C']
vc_a = VectorClock('A', nodes)
vc_b = VectorClock('B', nodes)
vc_c = VectorClock('C', nodes)

# A executes event
vc_a.tick()  # A: {A:1, B:0, C:0}

# A sends to B
msg1 = vc_a.send()  # A: {A:2, B:0, C:0}

# B receives from A
vc_b.receive(msg1)  # B: {A:2, B:1, C:0}

# B executes event
vc_b.tick()  # B: {A:2, B:2, C:0}

# B sends to C
msg2 = vc_b.send()  # B: {A:2, B:3, C:0}

# C receives from B
vc_c.receive(msg2)  # C: {A:2, B:3, C:1}

print(f"A: {vc_a.clock}")  # {A:2, B:0, C:0}
print(f"B: {vc_b.clock}")  # {A:2, B:3, C:0}
print(f"C: {vc_c.clock}")  # {A:2, B:3, C:1}

# Compare causal relationships
print(f"A < B: {vc_a.compare(vc_b)}")  # '<' (A happened before B)
print(f"B < C: {vc_b.compare(vc_c)}")  # '<' (B happened before C)

CHAPTER 4: RAFT CONSENSUS ALGORITHM
Raft Overview
# Raft is a consensus algorithm designed for understandability.
# Key properties:
# - Leader election: One leader coordinates all log replication
# - Log replication: Leader replicates log entries to followers
# - Safety: Never returns incorrect result (linearizability)
# - Terms: Time divided into terms, each with at most one leader

import random
import time
from enum import Enum

class NodeState(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3

class RaftNode:
    """Simplified Raft node implementation."""
    
    def __init__(self, node_id, all_nodes):
        self.node_id = node_id
        self.all_nodes = all_nodes
        self.state = NodeState.FOLLOWER
        
        # Persistent state
        self.current_term = 0
        self.voted_for = None
        self.log = []  # List of (term, command)
        
        # Volatile state
        self.commit_index = -1
        self.last_applied = -1
        
        # Leader state
        self.next_index = {}
        self.match_index = {}
        
        # Election timeout
        self.election_timeout = random.uniform(150, 300) / 1000  # 150-300ms
        self.last_heartbeat = time.time()
    
    def start_election(self):
        """Start election (transition to CANDIDATE)."""
        self.current_term += 1
        self.state = NodeState.CANDIDATE
        self.voted_for = self.node_id
        
        votes_received = 1  # Vote for self
        
        # Request votes from other nodes
        for node in self.all_nodes:
            if node != self.node_id:
                # Simulate RequestVote RPC
                if self._request_vote(node):
                    votes_received += 1
        
        # Check if won election
        if votes_received > len(self.all_nodes) // 2:
            self.state = NodeState.LEADER
            print(f"Node {self.node_id} became leader for term {self.current_term}")
            self._initialize_leader_state()
        else:
            self.state = NodeState.FOLLOWER
    
    def _request_vote(self, target_node):
        """Simulate RequestVote RPC."""
        # Simplified: always grant vote (real implementation checks log completeness)
        return True
    
    def _initialize_leader_state(self):
        """Initialize leader state after election."""
        next_idx = len(self.log)
        for node in self.all_nodes:
            if node != self.node_id:
                self.next_index[node] = next_idx
                self.match_index[node] = -1
    
    def append_entry(self, command):
        """Leader appends entry to log."""
        if self.state != NodeState.LEADER:
            raise Exception("Not leader")
        
        entry = (self.current_term, command)
        self.log.append(entry)
        
        # Replicate to followers
        for node in self.all_nodes:
            if node != self.node_id:
                self._replicate_entry(node, entry)
        
        # Update commit index
        self.commit_index = len(self.log) - 1
    
    def _replicate_entry(self, target_node, entry):
        """Simulate AppendEntries RPC."""
        # Simplified: always succeed
        pass
    
    def receive_heartbeat(self, leader_term):
        """Follower receives heartbeat from leader."""
        if leader_term >= self.current_term:
            self.current_term = leader_term
            self.state = NodeState.FOLLOWER
            self.last_heartbeat = time.time()

# Simulate Raft cluster
nodes = ['A', 'B', 'C']
raft_nodes = {node: RaftNode(node, nodes) for node in nodes}

# Node A starts election
raft_nodes['A'].start_election()

# Node A (now leader) appends entry
if raft_nodes['A'].state == NodeState.LEADER:
    raft_nodes['A'].append_entry("set x = 10")
    print(f"Leader log: {raft_nodes['A'].log}")

Paxos Algorithm (Simplified)
# Paxos is another consensus algorithm, more complex than Raft.
# Three phases:
# 1. Prepare: Proposer sends prepare request to acceptors
# 2. Promise: Acceptors respond with promise not to accept lower proposals
# 3. Accept: Proposer sends accept request, acceptors accept if no higher promise

class PaxosProposer:
    """Simplified Paxos proposer."""
    
    def __init__(self, proposer_id, acceptors):
        self.proposer_id = proposer_id
        self.acceptors = acceptors
        self.proposal_number = 0
    
    def propose(self, value):
        """Propose a value."""
        self.proposal_number += 1
        
        # Phase 1: Prepare
        promises = []
        for acceptor in self.acceptors:
            promise = acceptor.prepare(self.proposal_number)
            if promise:
                promises.append(promise)
        
        # Check if majority promised
        if len(promises) <= len(self.acceptors) // 2:
            return None
        
        # Phase 2: Accept
        accepts = []
        for acceptor in self.acceptors:
            accepted = acceptor.accept(self.proposal_number, value)
            if accepted:
                accepts.append(accepted)
        
        # Check if majority accepted
        if len(accepts) > len(self.acceptors) // 2:
            return value
        return None

class PaxosAcceptor:
    """Simplified Paxos acceptor."""
    
    def __init__(self, acceptor_id):
        self.acceptor_id = acceptor_id
        self.promised_number = 0
        self.accepted_number = 0
        self.accepted_value = None
    
    def prepare(self, proposal_number):
        """Handle prepare request."""
        if proposal_number >= self.promised_number:
            self.promised_number = proposal_number
            return (self.accepted_number, self.accepted_value)
        return None
    
    def accept(self, proposal_number, value):
        """Handle accept request."""
        if proposal_number >= self.promised_number:
            self.promised_number = proposal_number
            self.accepted_number = proposal_number
            self.accepted_value = value
            return True
        return False

# Simulate Paxos
acceptors = [PaxosAcceptor(i) for i in range(3)]
proposer = PaxosProposer('P1', acceptors)

result = proposer.propose("value1")
print(f"Paxos consensus result: {result}")

CHAPTER 5: DISTRIBUTED HASH TABLES (DHT)
Chord DHT
# Chord is a DHT protocol that provides efficient key lookup.
# Uses consistent hashing to map keys to nodes.
# Each node maintains a finger table for O(log N) lookups.

import hashlib

class ChordNode:
    """Simplified Chord DHT node."""
    
    def __init__(self, node_id, m_bits=4):
        self.node_id = node_id
        self.m_bits = m_bits
        self.max_id = 2 ** m_bits
        self.data = {}
        self.successor = None
        self.predecessor = None
        self.finger_table = [None] * m_bits
    
    def hash_key(self, key):
        """Hash a key to the Chord ring."""
        return int(hashlib.sha1(key.encode()).hexdigest(), 16) % self.max_id
    
    def store(self, key, value):
        """Store key-value pair."""
        hashed_key = self.hash_key(key)
        self.data[key] = value
    
    def lookup(self, key):
        """Lookup key in DHT."""
        hashed_key = self.hash_key(key)
        
        # Check if key belongs to this node
        if self._in_range(hashed_key):
            return self.data.get(key)
        
        # Forward to appropriate finger
        next_node = self._find_successor(hashed_key)
        if next_node and next_node != self:
            return next_node.lookup(key)
        
        return None
    
    def _in_range(self, key):
        """Check if key belongs to this node's range."""
        if self.predecessor is None:
            return True
        return (self.predecessor.node_id < key <= self.node_id) or \
               (self.predecessor.node_id > self.node_id and \
                (key > self.predecessor.node_id or key <= self.node_id))
    
    def _find_successor(self, key):
        """Find successor node for key."""
        # Simplified: return successor
        return self.successor

# Create Chord ring
nodes = [ChordNode(i, m_bits=4) for i in [0, 2, 5, 8, 11]]

# Link nodes in ring
for i in range(len(nodes)):
    nodes[i].successor = nodes[(i + 1) % len(nodes)]
    nodes[i].predecessor = nodes[(i - 1) % len(nodes)]

# Store and lookup
nodes[0].store("user:alice", "data1")
nodes[2].store("user:bob", "data2")

result = nodes[0].lookup("user:alice")
print(f"Lookup result: {result}")

CHAPTER 6: REPLICATION STRATEGIES
Single-Leader Replication
# Single-leader: One node handles all writes, replicates to followers.
# Pros: Simple, strong consistency possible
# Cons: Single point of failure, write bottleneck

class SingleLeaderReplication:
    """Single-leader replication system."""
    
    def __init__(self, leader_id, follower_ids):
        self.leader_id = leader_id
        self.follower_ids = follower_ids
        self.leader_data = {}
        self.follower_data = {fid: {} for fid in follower_ids}
        self.replication_factor = len(follower_ids)
    
    def write(self, key, value, sync=True):
        """Write to leader and replicate."""
        self.leader_data[key] = value
        
        if sync:
            # Synchronous replication
            for fid in self.follower_ids:
                self.follower_data[fid][key] = value
        else:
            # Asynchronous replication (simplified)
            pass
    
    def read(self, key, from_leader=True):
        """Read from leader or follower."""
        if from_leader:
            return self.leader_data.get(key)
        else:
            # Read from any follower
            for fid in self.follower_ids:
                if key in self.follower_data[fid]:
                    return self.follower_data[fid][key]
            return None

replication = SingleLeaderReplication('L1', ['F1', 'F2', 'F3'])
replication.write('x', 100, sync=True)
print(f"Read from leader: {replication.read('x', from_leader=True)}")
print(f"Read from follower: {replication.read('x', from_leader=False)}")

Multi-Leader Replication
# Multi-leader: Multiple nodes accept writes, resolve conflicts.
# Used in: multi-datacenter deployments, offline-first apps
# Conflict resolution: Last-write-wins, vector clocks, CRDTs

class MultiLeaderReplication:
    """Multi-leader replication with conflict resolution."""
    
    def __init__(self, node_ids):
        self.node_ids = node_ids
        self.data = {nid: {} for nid in node_ids}
        self.vector_clocks = {nid: {} for nid in node_ids}
    
    def write(self, node_id, key, value):
        """Write to specific node."""
        if node_id not in self.node_ids:
            raise ValueError("Invalid node")
        
        # Update vector clock
        if key not in self.vector_clocks[node_id]:
            self.vector_clocks[node_id][key] = {nid: 0 for nid in self.node_ids}
        
        self.vector_clocks[node_id][key][node_id] += 1
        self.data[node_id][key] = value
    
    def read(self, node_id, key):
        """Read from specific node."""
        return self.data[node_id].get(key)
    
    def sync(self, node1, node2):
        """Sync data between two nodes (simplified)."""
        # Merge data using last-write-wins
        for key in set(self.data[node1].keys()) | set(self.data[node2].keys()):
            if key in self.data[node1] and key in self.data[node2]:
                # Conflict: use last-write-wins (simplified)
                vc1 = self.vector_clocks[node1][key]
                vc2 = self.vector_clocks[node2][key]
                
                # Compare vector clocks
                sum1 = sum(vc1.values())
                sum2 = sum(vc2.values())
                
                if sum1 >= sum2:
                    self.data[node2][key] = self.data[node1][key]
                    self.vector_clocks[node2][key] = vc1.copy()
                else:
                    self.data[node1][key] = self.data[node2][key]
                    self.vector_clocks[node1][key] = vc2.copy()

multi_leader = MultiLeaderReplication(['N1', 'N2', 'N3'])
multi_leader.write('N1', 'x', 10)
multi_leader.write('N2', 'x', 20)

print(f"Before sync - N1: {multi_leader.read('N1', 'x')}, N2: {multi_leader.read('N2', 'x')}")
multi_leader.sync('N1', 'N2')
print(f"After sync - N1: {multi_leader.read('N1', 'x')}, N2: {multi_leader.read('N2', 'x')}")

CHAPTER 7: DISTRIBUTED TRANSACTIONS
Two-Phase Commit (2PC)
# 2PC ensures atomicity across distributed nodes.
# Phase 1 (Prepare): Coordinator asks participants if they can commit
# Phase 2 (Commit/Abort): Coordinator decides and notifies participants

class TransactionCoordinator:
    """2PC Coordinator."""
    
    def __init__(self, participants):
        self.participants = participants
    
    def execute_transaction(self, operations):
        """Execute distributed transaction."""
        # Phase 1: Prepare
        prepare_results = []
        for participant in self.participants:
            result = participant.prepare(operations)
            prepare_results.append(result)
        
        # Check if all participants are ready
        if all(prepare_results):
            # Phase 2: Commit
            for participant in self.participants:
                participant.commit()
            return True
        else:
            # Phase 2: Abort
            for participant in self.participants:
                participant.abort()
            return False

class TransactionParticipant:
    """2PC Participant."""
    
    def __init__(self, participant_id):
        self.participant_id = participant_id
        self.data = {}
        self.temp_data = {}
        self.prepared = False
    
    def prepare(self, operations):
        """Phase 1: Prepare to commit."""
        try:
            # Validate and tentatively apply operations
            for key, value in operations.items():
                self.temp_data[key] = value
            self.prepared = True
            return True
        except Exception:
            return False
    
    def commit(self):
        """Phase 2: Commit transaction."""
        if self.prepared:
            self.data.update(self.temp_data)
            self.temp_data.clear()
            self.prepared = False
    
    def abort(self):
        """Phase 2: Abort transaction."""
        self.temp_data.clear()
        self.prepared = False

# Simulate 2PC
participants = [TransactionParticipant(f"P{i}") for i in range(3)]
coordinator = TransactionCoordinator(participants)

operations = {'x': 100, 'y': 200}
success = coordinator.execute_transaction(operations)
print(f"Transaction success: {success}")
print(f"P0 data: {participants[0].data}")

Three-Phase Commit (3PC)
# 3PC adds a pre-commit phase to reduce blocking in 2PC.
# Phases:
# 1. Can-commit: Coordinator asks if participants can commit
# 2. Pre-commit: Coordinator tells participants to prepare
# 3. Do-commit: Coordinator tells participants to commit

class ThreePhaseCoordinator:
    """3PC Coordinator."""
    
    def __init__(self, participants):
        self.participants = participants
    
    def execute_transaction(self, operations):
        """Execute 3PC transaction."""
        # Phase 1: Can-commit
        can_commit_results = []
        for participant in self.participants:
            result = participant.can_commit(operations)
            can_commit_results.append(result)
        
        if not all(can_commit_results):
            for participant in self.participants:
                participant.abort()
            return False
        
        # Phase 2: Pre-commit
        for participant in self.participants:
            participant.pre_commit()
        
        # Phase 3: Do-commit
        for participant in self.participants:
            participant.do_commit()
        
        return True

class ThreePhaseParticipant:
    """3PC Participant."""
    
    def __init__(self, participant_id):
        self.participant_id = participant_id
        self.data = {}
        self.temp_data = {}
        self.state = 'INIT'
    
    def can_commit(self, operations):
        """Phase 1: Check if can commit."""
        try:
            for key, value in operations.items():
                self.temp_data[key] = value
            self.state = 'READY'
            return True
        except Exception:
            return False
    
    def pre_commit(self):
        """Phase 2: Pre-commit."""
        if self.state == 'READY':
            self.state = 'PREPARED'
    
    def do_commit(self):
        """Phase 3: Commit."""
        if self.state == 'PREPARED':
            self.data.update(self.temp_data)
            self.temp_data.clear()
            self.state = 'COMMITTED'
    
    def abort(self):
        """Abort transaction."""
        self.temp_data.clear()
        self.state = 'ABORTED'

# Simulate 3PC
participants_3pc = [ThreePhaseParticipant(f"P{i}") for i in range(3)]
coordinator_3pc = ThreePhaseCoordinator(participants_3pc)

success = coordinator_3pc.execute_transaction({'x': 300, 'y': 400})
print(f"3PC Transaction success: {success}")
print(f"P0 data: {participants_3pc[0].data}")

CHAPTER 8: BYZANTINE FAULT TOLERANCE
PBFT (Practical Byzantine Fault Tolerance)
# PBFT tolerates up to f Byzantine faults with 3f+1 nodes.
# Phases:
# 1. Pre-prepare: Primary proposes a value
# 2. Prepare: Nodes broadcast prepare messages
# 3. Commit: Nodes broadcast commit messages
# 4. Reply: Nodes send reply to client

class PBFTNode:
    """Simplified PBFT node."""
    
    def __init__(self, node_id, all_nodes):
        self.node_id = node_id
        self.all_nodes = all_nodes
        self.is_primary = (node_id == 0)
        self.prepared = set()
        self.committed = set()
        self.data = {}
    
    def pre_prepare(self, view, sequence, value):
        """Primary sends pre-prepare message."""
        if not self.is_primary:
            return
        
        # Broadcast pre-prepare to all nodes
        for node in self.all_nodes:
            if node != self.node_id:
                # Simulate sending pre-prepare
                pass
    
    def prepare(self, view, sequence, value, sender):
        """Node receives pre-prepare and broadcasts prepare."""
        # Check if valid
        if (view, sequence, value) not in self.prepared:
            self.prepared.add((view, sequence, value))
            
            # Broadcast prepare to all nodes
            for node in self.all_nodes:
                if node != self.node_id:
                    # Simulate sending prepare
                    pass
    
    def commit(self, view, sequence, value, sender):
        """Node receives prepare messages and broadcasts commit."""
        # Check if received 2f+1 prepare messages
        if len([p for p in self.prepared if p == (view, sequence, value)]) >= 2:
            self.committed.add((view, sequence, value))
            
            # Broadcast commit to all nodes
            for node in self.all_nodes:
                if node != self.node_id:
                    # Simulate sending commit
                    pass
    
    def execute(self, view, sequence, value):
        """Execute request after consensus."""
        # Check if received 2f+1 commit messages
        if len([c for c in self.committed if c == (view, sequence, value)]) >= 2:
            self.data[sequence] = value
            return value
        return None

# Simulate PBFT
nodes = [PBFTNode(i, range(4)) for i in range(4)]

# Primary proposes value
nodes[0].pre_prepare(view=0, sequence=1, value="transaction1")

# Nodes prepare
for node in nodes[1:]:
    node.prepare(view=0, sequence=1, value="transaction1", sender=0)

# Nodes commit
for node in nodes:
    node.commit(view=0, sequence=1, value="transaction1", sender=0)

# Execute
result = nodes[0].execute(view=0, sequence=1, value="transaction1")
print(f"PBFT consensus result: {result}")

CHAPTER 9: PRACTICAL IMPLEMENTATIONS
Raft Implementation with Threading
import threading
import queue
import time

class ThreadedRaftNode:
    """Raft node with threading for simulation."""
    
    def __init__(self, node_id, all_nodes):
        self.node_id = node_id
        self.all_nodes = all_nodes
        self.state = 'FOLLOWER'
        self.current_term = 0
        self.log = []
        self.message_queue = queue.Queue()
        self.running = False
        self.thread = None
    
    def start(self):
        """Start node thread."""
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
    
    def stop(self):
        """Stop node thread."""
        self.running = False
        if self.thread:
            self.thread.join()
    
    def _run(self):
        """Main node loop."""
        while self.running:
            try:
                msg = self.message_queue.get(timeout=0.1)
                self._handle_message(msg)
            except queue.Empty:
                # Check for election timeout
                pass
    
    def _handle_message(self, msg):
        """Handle incoming message."""
        msg_type = msg['type']
        
        if msg_type == 'REQUEST_VOTE':
            self._handle_request_vote(msg)
        elif msg_type == 'APPEND_ENTRIES':
            self._handle_append_entries(msg)
    
    def _handle_request_vote(self, msg):
        """Handle RequestVote RPC."""
        if msg['term'] >= self.current_term:
            self.current_term = msg['term']
            # Grant vote (simplified)
            response = {'term': self.current_term, 'vote_granted': True}
            # Send response back to candidate
            self._send_message(msg['candidate'], {'type': 'VOTE_RESPONSE', **response})
    
    def _handle_append_entries(self, msg):
        """Handle AppendEntries RPC."""
        if msg['term'] >= self.current_term:
            self.current_term = msg['term']
            self.state = 'FOLLOWER'
            # Append entries to log
            self.log.extend(msg['entries'])
            # Send response
            response = {'term': self.current_term, 'success': True}
            self._send_message(msg['leader'], {'type': 'APPEND_RESPONSE', **response})
    
    def _send_message(self, target, msg):
        """Send message to another node."""
        # Find target node and put message in queue
        for node in self.all_nodes:
            if node.node_id == target:
                node.message_queue.put(msg)
                break

# Simulate threaded Raft cluster
nodes_threaded = [ThreadedRaftNode(i, None) for i in range(3)]
for node in nodes_threaded:
    node.all_nodes = nodes_threaded

# Start all nodes
for node in nodes_threaded:
    node.start()

# Simulate some time
time.sleep(1)

# Stop all nodes
for node in nodes_threaded:
    node.stop()

print("Threaded Raft simulation complete")

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Consensus in Practice
# Real-world consensus systems:
# - etcd: Uses Raft, used in Kubernetes
# - Consul: Uses Raft, service discovery
# - ZooKeeper: Uses ZAB (ZooKeeper Atomic Broadcast)
# - CockroachDB: Uses Raft, distributed SQL database
# - FoundationDB: Uses custom consensus

# Performance considerations:
# - Batch operations to reduce RPC overhead
# - Pipelining for log replication
# - Snapshotting to reduce log size
# - Leader leasing for read optimization

Byzantine Fault Tolerance in Blockchains
# Blockchain consensus:
# - Proof of Work (Bitcoin): Computationally expensive, secure
# - Proof of Stake (Ethereum 2.0): Energy efficient, validator-based
# - PBFT variants: Used in permissioned blockchains (Hyperledger Fabric)
# - Tendermint: BFT consensus for blockchain

# Blockchain properties:
# - Immutability: Once committed, cannot be changed
# - Finality: Transactions are irreversible after confirmation
# - Liveness: System continues to make progress

Recommended Reading
# - "Designing Data-Intensive Applications" by Martin Kleppmann
# - "Distributed Systems" by Maarten van Steen and Andrew S. Tanenbaum
# - "In Search of an Understandable Consensus Algorithm" (Raft paper)
# - "The Part-Time Parliament" (Paxos paper)
# - "Practical Byzantine Fault Tolerance" (PBFT paper)

# End of Distributed Systems Reference