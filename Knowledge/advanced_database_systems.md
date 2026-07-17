Advanced Database Systems & Modern Storage Engines Complete Reference
CHAPTER 1: EVOLUTION OF DATABASE ARCHITECTURES
Remarks
The database landscape has shifted from monolithic RDBMS to specialized engines tailored for specific workloads: Vector databases for AI embeddings, Graph databases for connected data, NewSQL for distributed ACID transactions, and Time-Series databases for IoT/monitoring. Understanding the internal storage engines (B-Tree vs LSM-Tree vs Heap) is crucial for performance tuning. Key concepts: Write-Ahead Logging (WAL), Multi-Version Concurrency Control (MVCC), Sharding, Consensus Protocols (Raft/Paxos), and Columnar Storage.
Tools: PostgreSQL, MySQL, Redis, Neo4j, Milvus, Pinecone, CockroachDB, TiDB, ClickHouse.

1.1 The CAP Theorem in Practice
# Consistency: Every read receives the most recent write or an error.
# Availability: Every request receives a (non-error) response, without the guarantee that it contains the most recent write.
# Partition Tolerance: The system continues to operate despite arbitrary message loss or failure of part of the system.

# Real-world trade-offs:
# - CP Systems: MongoDB (default), HBase, ZooKeeper. Prioritize consistency over availability during partitions.
# - AP Systems: Cassandra, DynamoDB, CouchDB. Prioritize availability, eventual consistency.
# - CA Systems: Traditional RDBMS (MySQL, PostgreSQL) in single-node setups. Cannot handle network partitions gracefully without stopping.

1.2 ACID vs BASE
# ACID (Atomicity, Consistency, Isolation, Durability):
#   - Strong consistency guarantees.
#   - Suitable for financial transactions, inventory management.
#   - Performance cost: Locking, logging, synchronous replication.

# BASE (Basically Available, Soft state, Eventual consistency):
#   - High availability and scalability.
#   - Suitable for social media feeds, caching, analytics.
#   - Performance benefit: Asynchronous replication, no locking.

CHAPTER 2: NEWSQL & DISTRIBUTED SQL
NewSQL aims to provide the scalability of NoSQL while maintaining ACID guarantees of traditional RDBMS.

2.1 CockroachDB Architecture
# Built on RocksDB (LSM-Tree) for storage.
# Uses Raft consensus for replication.
# Automatic sharding (ranges) and rebalancing.
# Serializable Snapshot Isolation (SSI) for transactions.

# Key Concept: Range Splitting
# Data is divided into ranges (default 64MB).
# When a range exceeds size threshold, it splits.
# Each range is replicated via Raft across multiple nodes.

2.2 TiDB Architecture
# Separates Compute (TiDB Server) from Storage (TiKV).
# TiKV: Distributed key-value store using Raft.
# PD (Placement Driver): Manages metadata and scheduling.
# Supports HTAP (Hybrid Transactional/Analytical Processing).

2.3 Google Spanner & TrueTime
# Uses atomic clocks and GPS receivers to achieve globally synchronized time.
# Enables external consistency (linearizability) across continents.
# Uses Paxos for replication.

CHAPTER 3: VECTOR DATABASES FOR AI
Vector databases store high-dimensional vectors (embeddings) and enable similarity search.

3.1 Indexing Algorithms for Approximate Nearest Neighbor (ANN)
# Exact Search (KNN): O(N*D) complexity. Too slow for large datasets.
# ANN Algorithms: Trade accuracy for speed.

# HNSW (Hierarchical Navigable Small World):
# - Graph-based index.
# - Constructs a multi-layer graph where upper layers have fewer nodes and longer links.
# - Search starts at top layer, navigates down to bottom layer.
# - Complexity: O(log N).
# - Pros: High recall, fast query.
# - Cons: High memory usage, slow indexing.

# IVF (Inverted File Index):
# - Clusters vectors using K-Means.
# - Each cluster has a centroid.
# - Search: Find nearest centroids, then search within those clusters.
# - Pros: Low memory, fast indexing.
# - Cons: Lower recall if clusters are not well-defined.

# PQ (Product Quantization):
# - Compresses vectors by splitting them into sub-vectors and quantizing each.
# - Reduces memory footprint significantly.
# - Often combined with IVF (IVF-PQ).

3.2 Distance Metrics
# Euclidean Distance (L2): sqrt(sum((xi - yi)^2)). Good for spatial data.
# Cosine Similarity: (A·B) / (||A|| ||B||). Good for text embeddings (direction matters, not magnitude).
# Dot Product: A·B. Used when vectors are normalized (equivalent to cosine).
# Manhattan Distance (L1): sum(|xi - yi|). Less sensitive to outliers.

3.3 Implementation Example: HNSW Search
import numpy as np
import heapq

class HNSWNode:
    def __init__(self, vector, level):
        self.vector = vector
        self.level = level
        self.connections = {i: [] for i in range(level + 1)}

class SimpleHNSW:
    def __init__(self, m=16, ef_construction=200, ef_search=50):
        self.m = m  # Max connections per layer
        self.ef_construction = ef_construction
        self.ef_search = ef_search
        self.nodes = []
        self.entry_point = None
        self.max_level = 0

    def _distance(self, v1, v2):
        return np.linalg.norm(v1 - v2)

    def _select_neighbors_heuristic(self, candidates, query, m):
        # Greedy algorithm to select diverse neighbors
        results = []
        for dist, node in candidates:
            if len(results) >= m:
                break
            # Check if node is closer to query than to any existing result
            good = True
            for _, existing_node in results:
                if self._distance(node.vector, existing_node.vector) < self._distance(query, existing_node.vector):
                    good = False
                    break
            if good:
                results.append((dist, node))
        return results

    def insert(self, vector):
        level = int(-np.log(np.random.random()) * (1.0 / np.log(self.m)))
        new_node = HNSWNode(vector, level)
        
        if not self.nodes:
            self.entry_point = new_node
            self.max_level = level
            self.nodes.append(new_node)
            return

        # Find entry point at top layer
        current = self.entry_point
        for l in range(self.max_level, level, -1):
            while True:
                nearest_dist = float('inf')
                nearest_node = None
                for neighbor in current.connections[l]:
                    d = self._distance(neighbor.vector, vector)
                    if d < nearest_dist:
                        nearest_dist = d
                        nearest_node = neighbor
                if nearest_node and nearest_dist < self._distance(current.vector, vector):
                    current = nearest_node
                else:
                    break
        
        # Insert at each layer from level down to 0
        for l in range(min(level, self.max_level), -1, -1):
            # Find ef_construction nearest neighbors in layer l
            candidates = self._search_layer(current, vector, l, self.ef_construction)
            neighbors = self._select_neighbors_heuristic(candidates, vector, self.m)
            
            new_node.connections[l] = [n for _, n in neighbors]
            for _, neighbor in neighbors:
                neighbor.connections[l].append(new_node)
                # Prune neighbor's connections if > m
                if len(neighbor.connections[l]) > self.m:
                    neighbor_candidates = [(self._distance(neighbor.vector, n.vector), n) for n in neighbor.connections[l]]
                    neighbor.connections[l] = [n for _, n in self._select_neighbors_heuristic(neighbor_candidates, neighbor.vector, self.m)]

        if level > self.max_level:
            self.max_level = level
            self.entry_point = new_node
        
        self.nodes.append(new_node)

    def _search_layer(self, entry_point, query, layer, ef):
        # Best-first search in a single layer
        visited = set()
        candidates = [(self._distance(entry_point.vector, query), entry_point)]
        best_results = candidates[:]
        heapq.heapify(candidates)
        visited.add(id(entry_point))

        while candidates:
            dist, current = heapq.heappop(candidates)
            if dist > best_results[-1][0] and len(best_results) == ef:
                break
            
            for neighbor in current.connections[layer]:
                if id(neighbor) not in visited:
                    visited.add(id(neighbor))
                    d = self._distance(neighbor.vector, query)
                    if len(best_results) < ef or d < best_results[-1][0]:
                        heapq.heappush(candidates, (d, neighbor))
                        best_results.append((d, neighbor))
                        best_results.sort(key=lambda x: x[0])
                        if len(best_results) > ef:
                            best_results.pop()
        
        return best_results

    def search(self, query, k=5):
        if not self.nodes:
            return []
        
        current = self.entry_point
        for l in range(self.max_level, 0, -1):
            while True:
                nearest_dist = float('inf')
                nearest_node = None
                for neighbor in current.connections[l]:
                    d = self._distance(neighbor.vector, query)
                    if d < nearest_dist:
                        nearest_dist = d
                        nearest_node = neighbor
                if nearest_node and nearest_dist < self._distance(current.vector, query):
                    current = nearest_node
                else:
                    break
        
        candidates = self._search_layer(current, query, 0, self.ef_search)
        return [(dist, node.vector) for dist, node in candidates[:k]]

# Usage
hnsw = SimpleHNSW(m=16, ef_construction=200, ef_search=50)
for i in range(1000):
    hnsw.insert(np.random.rand(128))

query_vec = np.random.rand(128)
results = hnsw.search(query_vec, k=5)
print(f"Top 5 similar vectors: {len(results)} found")

CHAPTER 4: GRAPH DATABASES
Graph databases excel at storing and querying highly connected data.

4.1 Property Graph Model
# Nodes: Entities (e.g., Person, Product)
# Edges: Relationships (e.g., FRIENDS_WITH, PURCHASED)
# Properties: Key-value pairs on nodes and edges.

4.2 Traversal Algorithms
# Breadth-First Search (BFS): Finds shortest path in unweighted graphs.
# Depth-First Search (DFS): Explores as far as possible along each branch.
# Dijkstra's Algorithm: Shortest path in weighted graphs.
# A* Search: Heuristic-based shortest path.

4.3 Cypher Query Language (Neo4j)
# Pattern matching syntax.
# MATCH (p:Person)-[:FRIENDS_WITH]->(f:Friend)
# WHERE p.name = 'Alice'
# RETURN f.name

4.4 Graph Neural Networks (GNNs)
# Combine graph structure with node features.
# Message Passing: Nodes aggregate information from neighbors.
# Applications: Fraud detection, recommendation systems, molecular property prediction.

CHAPTER 5: TIME-SERIES DATABASES (TSDB)
Optimized for handling metrics, events, and logs over time.

5.1 Key Features
# High ingest rate: Millions of points per second.
# Compression: Delta-of-delta encoding for timestamps, XOR for values.
# Downsampling: Aggregating old data (e.g., 1s -> 1m averages).
# Retention Policies: Automatically delete old data.

5.2 Storage Engine: TSM (Time-Structured Merge Tree)
# Used by InfluxDB.
# Similar to LSM-Tree but optimized for time-series data.
# Data is written to WAL, then flushed to TSM files.
# TSM files are immutable and indexed by time range.

5.3 Query Optimization
# Predicate Pushdown: Filter data at storage level before returning.
# Columnar Storage: Store timestamps and values in separate columns for efficient aggregation.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
6.1 Federated Learning with Databases
# Train models on decentralized data without moving it.
# Requires secure aggregation and differential privacy.

6.2 Blockchain as a Database
# Immutable ledger.
# Smart contracts as stored procedures.
# Limitations: Low throughput, high latency, expensive storage.

6.3 Quantum Databases
# Theoretical concept: Using quantum states to store and query data.
# Potential for exponential speedup in search (Grover's algorithm).

Recommended Reading
# - "Designing Data-Intensive Applications" by Martin Kleppmann
# - "Database Internals" by Alex Petrov
# - "Graph Databases" by Robinson et al.
# - "Streaming Systems" by Akidau et al.

# Online Resources
# - CockroachDB Docs: https://www.cockroachlabs.com/docs/
# - Neo4j Developer Guide: https://neo4j.com/developer/
# - Milvus Documentation: https://milvus.io/docs
# - ClickHouse Docs: https://clickhouse.com/docs

# End of Advanced Database Systems Reference