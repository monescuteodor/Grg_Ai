Advanced Database Indexing & Storage Structures Complete Reference
CHAPTER 1: GETTING STARTED WITH ADVANCED INDEXING
Remarks
Database indexing is crucial for query performance. While B-Trees are the standard, modern workloads (high write throughput, time-series data, analytical queries) require specialized structures. Key concepts: LSM-Trees (Log-Structured Merge-Trees), Fractal Trees, Learned Indexes, Bitmap Indexes, and Columnar Storage. Used in: Cassandra, RocksDB, MongoDB, ClickHouse, PostgreSQL extensions.
Tools: Python (for simulations), C++ (production implementations), LevelDB, RocksDB, SQLite.
Hello Indexing
# hello_indexing.py
"""
First program: Compare linear search vs binary search on a sorted list.
"""
import random
import time

def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# Generate sorted data
data = sorted([random.randint(0, 10_000_000) for _ in range(1_000_000)])
target = data[500_000]

# Benchmark Linear
start = time.time()
linear_search(data, target)
t_linear = time.time() - start

# Benchmark Binary
start = time.time()
binary_search(data, target)
t_binary = time.time() - start

print(f"Linear Search: {t_linear:.6f}s")
print(f"Binary Search: {t_binary:.6f}s")
print(f"Speedup: {t_linear/t_binary:.1f}x")

CHAPTER 2: LOG-STRUCTURED MERGE-TREES (LSM)
LSM-Tree Architecture
# LSM-Trees optimize for write throughput.
# Components:
# 1. MemTable: In-memory sorted structure (SkipList or AVL Tree).
# 2. WAL (Write-Ahead Log): Durability before ack.
# 3. SSTables (Sorted String Tables): Immutable on-disk files.
# 4. Compaction: Merging overlapping SSTables to remove duplicates/deletes.

class SkipListNode:
    def __init__(self, key, value, level):
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    """In-memory component of an LSM-Tree (MemTable)."""
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level
        self.p = p
        self.level = 0
        self.header = SkipListNode(None, None, max_level)
    
    def _random_level(self):
        level = 0
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level
    
    def insert(self, key, value):
        update = [None] * (self.max_level + 1)
        current = self.header
        
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
            
        current = current.forward[0]
        
        if current and current.key == key:
            current.value = value  # Update existing
        else:
            new_level = self._random_level()
            if new_level > self.level:
                for i in range(self.level + 1, new_level + 1):
                    update[i] = self.header
                self.level = new_level
            
            new_node = SkipListNode(key, value, new_level)
            for i in range(new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node
                
    def search(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.key == key:
            return current.value
        return None

# Example
memtable = SkipList()
memtable.insert("user:1", "Alice")
memtable.insert("user:2", "Bob")
print(f"Search user:1 -> {memtable.search('user:1')}")

SSTable Format
# On-disk format:
# 1. Data Block: Sorted key-value pairs.
# 2. Index Block: Sparse index pointing to data blocks.
# 3. Bloom Filter: Probabilistic structure to quickly check if key exists.
# 4. Footer: Pointers to index and bloom filter.

import hashlib

class BloomFilter:
    """Space-efficient probabilistic membership test."""
    def __init__(self, size=1000, hash_count=3):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size
        
    def _hashes(self, item):
        hashes = []
        for i in range(self.hash_count):
            h = hashlib.md5(f"{item}{i}".encode()).hexdigest()
            hashes.append(int(h, 16) % self.size)
        return hashes
    
    def add(self, item):
        for h in self._hashes(item):
            self.bit_array[h] = 1
            
    def might_contain(self, item):
        return all(self.bit_array[h] == 1 for h in self._hashes(item))

# Example
bf = BloomFilter(size=100)
bf.add("key1")
bf.add("key2")
print(f"Contains key1? {bf.might_contain('key1')}")  # True
print(f"Contains key3? {bf.might_contain('key3')}")  # Likely False

Compaction Strategies
# 1. Size-Tiered: Merge SSTables of similar size. Good for read-heavy.
# 2. Leveled: Maintain levels of increasing size. Less space amplification, better read latency.
# 3. Universal: Hybrid approach.

CHAPTER 3: FRACTAL TREES (TOKUTEK)
Fractal Tree Index
# Used in TokuDB (now Percona TokuMX).
# Similar to B-Tree but with message buffers at internal nodes.
# Messages (inserts/deletes) are buffered and injected down lazily.
# Benefits: High write throughput, efficient range queries, online schema changes.

class FractalNode:
    def __init__(self, is_leaf=False):
        self.keys = []
        self.children = []
        self.message_buffer = []  # Buffer for pending operations
        self.is_leaf = is_leaf
        
    def add_message(self, op, key, value=None):
        """Buffer an operation instead of executing immediately."""
        self.message_buffer.append((op, key, value))
        if len(self.message_buffer) > 100:  # Threshold
            self.flush_messages()
            
    def flush_messages(self):
        """Inject buffered messages into children or leaf data."""
        # Simplified: In real implementation, messages are sorted and merged
        print(f"Flushing {len(self.message_buffer)} messages...")
        self.message_buffer.clear()

# Conceptual Advantage:
# Instead of rewriting entire pages for every insert (B-Tree),
# Fractal Trees batch updates in memory buffers, reducing I/O.

CHAPTER 4: LEARNED INDEXES
Learned Index Structure
# Paper: "The Case for Learned Index Structures" (Kraska et al., 2018).
# Replaces traditional index structures with Machine Learning models.
# Idea: If data distribution is known, a model can predict the position of a key.
# Model: f(key) ≈ position. Then use binary search in a small window.

import numpy as np
from sklearn.linear_model import LinearRegression

class LearnedIndex:
    def __init__(self):
        self.model = LinearRegression()
        self.data = []
        self.error_bound = 0
        
    def train(self, keys):
        """Train model on sorted keys."""
        self.data = sorted(keys)
        X = np.array(self.data).reshape(-1, 1)
        y = np.arange(len(self.data)).reshape(-1, 1)
        
        self.model.fit(X, y)
        predictions = self.model.predict(X)
        residuals = np.abs(predictions - y)
        self.error_bound = int(np.max(residuals)) + 1
        
    def lookup(self, key):
        """Predict position and search locally."""
        pred_pos = self.model.predict([[key]])[0][0]
        start = max(0, int(pred_pos) - self.error_bound)
        end = min(len(self.data), int(pred_pos) + self.error_bound)
        
        # Local binary search
        for i in range(start, end):
            if self.data[i] == key:
                return i
        return -1

# Example
keys = [i * 2 for i in range(1000)]  # Even numbers
li = LearnedIndex()
li.train(keys)
print(f"Lookup 100: Index {li.lookup(100)}")  # Should be 50

Recursive Model Index (RMI)
# Hierarchical learned index.
# Root model predicts which sub-model to use.
# Sub-model predicts position.
# Handles complex distributions better than single linear model.

CHAPTER 5: COLUMNAR STORAGE & INDEXES
Column-Oriented Storage
# Row-store: Good for OLTP (transactional).
# Column-store: Good for OLAP (analytical).
# Benefits: Better compression, vectorized execution, only read needed columns.

# Compression Techniques:
# 1. Run-Length Encoding (RLE): AAAABBB -> 4A3B
# 2. Dictionary Encoding: Map strings to integers.
# 3. Bit-Packing: Store small integers in fewer bits.

def run_length_encode(data):
    if not data:
        return []
    encoded = []
    count = 1
    current = data[0]
    for i in range(1, len(data)):
        if data[i] == current:
            count += 1
        else:
            encoded.append((current, count))
            current = data[i]
            count = 1
    encoded.append((current, count))
    return encoded

data = ["A", "A", "A", "B", "B", "C", "A", "A"]
print(f"RLE: {run_length_encode(data)}")

Bitmap Indexes
# Efficient for low-cardinality columns (e.g., Gender, Status).
# One bit per row for each unique value.
# Fast boolean operations (AND, OR, NOT).

# Example: Column "Status" with values [Active, Inactive, Pending]
# Active:   10110
# Inactive: 01001
# Pending:  00000

# Query: Status = Active AND Status != Pending
# Result: 10110 AND NOT(00000) = 10110

CHAPTER 6: SPATIAL INDEXES
R-Tree
# Index for multi-dimensional information (GIS, Geometry).
# Groups nearby objects using Minimum Bounding Rectangles (MBR).
# Used in: PostGIS, SQLite R*Tree, MySQL Spatial.

class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        
    def intersects(self, other):
        return not (self.x2 < other.x1 or self.x1 > other.x2 or
                    self.y2 < other.y1 or self.y1 > other.y2)
                    
    def area(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1)

class RTreeNode:
    def __init__(self, is_leaf=False):
        self.children = []  # List of (Rectangle, ChildNode/Data)
        self.is_leaf = is_leaf
        self.mbr = None     # Minimum Bounding Rectangle
        
    def update_mbr(self):
        if not self.children:
            return
        self.mbr = self.children[0][0]
        for rect, _ in self.children[1:]:
            self.mbr = Rectangle(
                min(self.mbr.x1, rect.x1), min(self.mbr.y1, rect.y1),
                max(self.mbr.x2, rect.x2), max(self.mbr.y2, rect.y2)
            )

# Query: Find all objects intersecting a query rectangle
def r_tree_search(node, query_rect):
    results = []
    if node.is_leaf:
        for rect, data in node.children:
            if rect.intersects(query_rect):
                results.append(data)
    else:
        for rect, child in node.children:
            if rect.intersects(query_rect):
                results.extend(r_tree_search(child, query_rect))
    return results

Quadtree
# Recursive subdivision of 2D space into four quadrants.
# Simpler than R-Tree, good for uniform data distribution.

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Concurrent Indexing
# Lock-free B-Trees
# Optimistic Latch Coupling
# Multi-Version Concurrency Control (MVCC) in indexes

Hardware-Aware Indexing
# NVM (Non-Volatile Memory) optimized structures
# GPU-accelerated index builds
# SIMD-friendly search algorithms

Recommended Reading
# - "The Art of Computer Science" Vol 3 by Knuth (Sorting/Searching)
# - "Designing Data-Intensive Applications" by Kleppmann
# - "The Case for Learned Index Structures" (Paper)
# - RocksDB Documentation: https://rocksdb.org/
# - LSM-Tree Visualizer: https://www.cs.umb.edu/~poneil/lsmtree.html

# End of Advanced Database Indexing Reference