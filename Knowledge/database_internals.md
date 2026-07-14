Database Internals Complete Reference: Storage Engines, B-Trees, MVCC, and Query Optimization
CHAPTER 1: GETTING STARTED WITH DATABASE INTERNALS
Remarks
A database management system (DBMS) is software that stores, retrieves, and manages data. Key components: storage engine, buffer pool, query parser, query optimizer, execution engine, transaction manager, recovery system. Modern databases: PostgreSQL, MySQL, SQLite, CockroachDB, TiDB, MongoDB, Redis.
Tools: Python (for educational implementations), C/C++ (production), SQLite (source study), PostgreSQL (advanced study).
Hello Database
# hello_database.py
"""
Minimal in-memory key-value store as a starting point.
"""

class SimpleKVStore:
    """Simple in-memory key-value store."""
    
    def __init__(self):
        self.data = {}
    
    def put(self, key, value):
        """Insert or update a key-value pair."""
        self.data[key] = value
    
    def get(self, key):
        """Retrieve value by key."""
        return self.data.get(key)
    
    def delete(self, key):
        """Delete a key-value pair."""
        if key in self.data:
            del self.data[key]
            return True
        return False
    
    def scan(self, start_key=None, end_key=None):
        """Range scan over keys."""
        keys = sorted(self.data.keys())
        if start_key:
            keys = [k for k in keys if k >= start_key]
        if end_key:
            keys = [k for k in keys if k <= end_key]
        return [(k, self.data[k]) for k in keys]

# Example
db = SimpleKVStore()
db.put("user:1", "Alice")
db.put("user:2", "Bob")
db.put("user:3", "Charlie")

print("Get user:2:", db.get("user:2"))
print("Range scan:", db.scan("user:1", "user:2"))
db.delete("user:3")
print("After delete:", db.scan())

CHAPTER 2: STORAGE ENGINES
B-Tree Implementation
# B-Tree: balanced tree data structure for disk-based storage.
# Properties:
# - All leaves at same depth
# - Internal nodes: ceil(m/2) to m children (m = order)
# - Leaf nodes: ceil((m-1)/2) to m-1 keys
# - Search, insert, delete: O(log n)

class BTreeNode:
    """B-Tree node."""
    
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []      # List of keys
        self.values = []    # List of values (only for leaf nodes)
        self.children = []  # List of child pointers (only for internal nodes)
    
    def __repr__(self):
        if self.leaf:
            return f"Leaf({self.keys})"
        return f"Internal({self.keys})"

class BTree:
    """B-Tree implementation."""
    
    def __init__(self, t=2):
        """
        t = minimum degree (order = 2t)
        - Internal nodes: t to 2t children
        - Leaf nodes: t-1 to 2t-1 keys
        """
        self.t = t
        self.root = BTreeNode(leaf=True)
    
    def search(self, key, node=None):
        """Search for a key in the B-Tree."""
        if node is None:
            node = self.root
        
        # Find the first key >= search key
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        # Key found
        if i < len(node.keys) and node.keys[i] == key:
            if node.leaf:
                return node.values[i]
            else:
                # For internal nodes, search in child
                return self.search(key, node.children[i + 1])
        
        # Key not found, go to child
        if node.leaf:
            return None
        return self.search(key, node.children[i])
    
    def insert(self, key, value):
        """Insert a key-value pair."""
        root = self.root
        
        # If root is full, split it
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        
        self._insert_non_full(self.root, key, value)
    
    def _insert_non_full(self, node, key, value):
        """Insert into a non-full node."""
        i = len(node.keys) - 1
        
        if node.leaf:
            # Insert into leaf node
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            node.keys.insert(i, key)
            node.values.insert(i, value)
        else:
            # Find child to insert into
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            
            # If child is full, split it
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            
            self._insert_non_full(node.children[i], key, value)
    
    def _split_child(self, parent, i):
        """Split the i-th child of parent."""
        t = self.t
        child = parent.children[i]
        new_node = BTreeNode(leaf=child.leaf)
        
        # New node gets the last t-1 keys
        new_node.keys = child.keys[t:]
        if child.leaf:
            new_node.values = child.values[t:]
        
        # Median key goes up to parent
        median_key = child.keys[t - 1]
        
        # Child keeps first t-1 keys
        child.keys = child.keys[:t - 1]
        if child.leaf:
            child.values = child.values[:t - 1]
        else:
            new_node.children = child.children[t:]
            child.children = child.children[:t]
        
        # Insert median into parent
        parent.keys.insert(i, median_key)
        parent.children.insert(i + 1, new_node)
    
    def display(self, node=None, level=0):
        """Display the B-Tree structure."""
        if node is None:
            node = self.root
        
        print("  " * level + str(node))
        if not node.leaf:
            for child in node.children:
                self.display(child, level + 1)

# Example
btree = BTree(t=2)  # Order 4 B-Tree
for i in [10, 20, 5, 6, 12, 30, 7, 17]:
    btree.insert(i, f"value_{i}")

print("B-Tree structure:")
btree.display()
print("\nSearch 12:", btree.search(12))
print("Search 25:", btree.search(25))

LSM-Tree (Log-Structured Merge-Tree)
# LSM-Tree: write-optimized storage structure used in Cassandra, RocksDB, LevelDB.
# Components:
# - MemTable (in-memory, sorted)
# - SSTable (Sorted String Table, on-disk, immutable)
# - WAL (Write-Ahead Log for crash recovery)

import heapq
from collections import defaultdict

class MemTable:
    """In-memory sorted table (simplified as sorted dict)."""
    
    def __init__(self, max_size=100):
        self.data = {}
        self.max_size = max_size
    
    def put(self, key, value):
        self.data[key] = value
    
    def get(self, key):
        return self.data.get(key)
    
    def is_full(self):
        return len(self.data) >= self.max_size
    
    def to_sorted_list(self):
        return sorted(self.data.items())
    
    def clear(self):
        self.data.clear()

class SSTable:
    """Sorted String Table (on-disk immutable file)."""
    
    def __init__(self, level, data, filename=None):
        self.level = level
        self.data = data  # Sorted list of (key, value) pairs
        self.filename = filename or f"sstable_L{level}_{id(self)}.sst"
        self.min_key = data[0][0] if data else None
        self.max_key = data[-1][0] if data else None
    
    def get(self, key):
        """Binary search for key."""
        left, right = 0, len(self.data) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.data[mid][0] == key:
                return self.data[mid][1]
            elif self.data[mid][0] < key:
                left = mid + 1
            else:
                right = mid - 1
        return None
    
    def range_scan(self, start_key, end_key):
        """Scan keys in range [start_key, end_key]."""
        result = []
        for k, v in self.data:
            if start_key <= k <= end_key:
                result.append((k, v))
            elif k > end_key:
                break
        return result
    
    def __repr__(self):
        return f"SSTable(L{self.level}, {len(self.data)} entries)"

class LSMTree:
    """LSM-Tree implementation."""
    
    def __init__(self, memtable_size=100, num_levels=4):
        self.memtable = MemTable(max_size=memtable_size)
        self.sstables = [[] for _ in range(num_levels)]  # Level 0, 1, 2, ...
        self.wal = []  # Write-ahead log
        self.tombstone = "__DELETED__"
    
    def put(self, key, value):
        """Insert or update a key-value pair."""
        self.wal.append(('PUT', key, value))
        self.memtable.put(key, value)
        
        # Flush memtable to SSTable if full
        if self.memtable.is_full():
            self._flush_memtable()
    
    def get(self, key):
        """Retrieve value by key."""
        # Check memtable first
        value = self.memtable.get(key)
        if value is not None:
            return None if value == self.tombstone else value
        
        # Check SSTables from newest to oldest
        for level in range(len(self.sstables)):
            for sstable in reversed(self.sstables[level]):
                value = sstable.get(key)
                if value is not None:
                    return None if value == self.tombstone else value
        
        return None
    
    def delete(self, key):
        """Delete a key (tombstone)."""
        self.put(key, self.tombstone)
    
    def _flush_memtable(self):
        """Flush memtable to Level 0 SSTable."""
        data = self.memtable.to_sorted_list()
        if data:
            sstable = SSTable(level=0, data=data)
            self.sstables[0].append(sstable)
            self.memtable.clear()
            self.wal.clear()
            
            # Check if compaction needed
            if len(self.sstables[0]) >= 4:
                self._compact(0)
    
    def _compact(self, level):
        """Merge SSTables at given level."""
        if level >= len(self.sstables) - 1:
            return
        
        # Merge all SSTables at this level
        all_data = []
        for sstable in self.sstables[level]:
            all_data.extend(sstable.data)
        
        # Also merge with Level+1 SSTables that overlap
        if self.sstables[level]:
            min_key = min(s.min_key for s in self.sstables[level])
            max_key = max(s.max_key for s in self.sstables[level])
            
            next_level = []
            for sstable in self.sstables[level + 1]:
                if sstable.max_key < min_key or sstable.min_key > max_key:
                    next_level.append(sstable)
                else:
                    all_data.extend(sstable.data)
            
            self.sstables[level + 1] = next_level
        
        # Sort and deduplicate (keep latest value)
        all_data.sort(key=lambda x: x[0])
        deduped = {}
        for k, v in all_data:
            deduped[k] = v  # Later values overwrite earlier
        
        # Remove tombstones
        final_data = [(k, v) for k, v in deduped.items() if v != self.tombstone]
        
        if final_data:
            # Split into multiple SSTables if too large
            chunk_size = 100
            for i in range(0, len(final_data), chunk_size):
                chunk = final_data[i:i + chunk_size]
                new_sstable = SSTable(level=level + 1, data=chunk)
                self.sstables[level + 1].append(new_sstable)
        
        # Clear current level
        self.sstables[level] = []
    
    def range_scan(self, start_key, end_key):
        """Scan keys in range."""
        result = {}
        
        # Check memtable
        for k, v in self.memtable.data.items():
            if start_key <= k <= end_key:
                result[k] = v
        
        # Check SSTables
        for level in range(len(self.sstables)):
            for sstable in self.sstables[level]:
                for k, v in sstable.range_scan(start_key, end_key):
                    if k not in result:  # Keep latest value
                        result[k] = v
        
        # Remove tombstones and sort
        return sorted([(k, v) for k, v in result.items() if v != self.tombstone])
    
    def display(self):
        """Display LSM-Tree structure."""
        print(f"MemTable: {len(self.memtable.data)} entries")
        for level, sstables in enumerate(self.sstables):
            if sstables:
                print(f"Level {level}: {len(sstables)} SSTables")
                for sst in sstables:
                    print(f"  {sst}")

# Example
lsm = LSMTree(memtable_size=5)
for i in range(20):
    lsm.put(f"key{i:03d}", f"value{i}")

lsm.put("key005", "updated_value5")  # Update
lsm.delete("key010")  # Delete

print("\nLSM-Tree structure:")
lsm.display()
print("\nGet key005:", lsm.get("key005"))
print("Get key010:", lsm.get("key010"))  # Should be None (deleted)
print("Range scan key000-key005:", lsm.range_scan("key000", "key005"))

CHAPTER 3: BUFFER POOL MANAGER
Buffer Pool Implementation
# Buffer Pool: manages in-memory pages cached from disk.
# Uses LRU (Least Recently Used) or Clock algorithm for eviction.

class Page:
    """A page in the buffer pool."""
    
    def __init__(self, page_id, data=None):
        self.page_id = page_id
        self.data = data or bytearray(4096)  # 4KB page
        self.dirty = False
        self.pin_count = 0
    
    def __repr__(self):
        return f"Page({self.page_id}, dirty={self.dirty}, pins={self.pin_count})"

class BufferPool:
    """Buffer pool manager with LRU eviction."""
    
    def __init__(self, pool_size=10):
        self.pool_size = pool_size
        self.pages = {}  # page_id -> Page
        self.lru_order = []  # Track access order
        self.disk = {}  # Simulated disk storage
    
    def read_page(self, page_id):
        """Read a page from disk into buffer pool."""
        # Page already in buffer pool
        if page_id in self.pages:
            page = self.pages[page_id]
            page.pin_count += 1
            self._touch(page_id)
            return page
        
        # Buffer pool full, need to evict
        if len(self.pages) >= self.pool_size:
            self._evict()
        
        # Read from disk
        data = self.disk.get(page_id, bytearray(4096))
        page = Page(page_id, data)
        page.pin_count = 1
        self.pages[page_id] = page
        self.lru_order.append(page_id)
        
        return page
    
    def write_page(self, page_id, data):
        """Write data to a page."""
        if page_id not in self.pages:
            page = self.read_page(page_id)
        else:
            page = self.pages[page_id]
        
        page.data = data
        page.dirty = True
        self._touch(page_id)
    
    def unpin_page(self, page_id, dirty=False):
        """Unpin a page (decrement pin count)."""
        if page_id in self.pages:
            page = self.pages[page_id]
            page.pin_count = max(0, page.pin_count - 1)
            if dirty:
                page.dirty = True
    
    def flush_page(self, page_id):
        """Flush a dirty page to disk."""
        if page_id in self.pages:
            page = self.pages[page_id]
            if page.dirty:
                self.disk[page_id] = page.data
                page.dirty = False
    
    def flush_all(self):
        """Flush all dirty pages to disk."""
        for page_id in list(self.pages.keys()):
            self.flush_page(page_id)
    
    def _touch(self, page_id):
        """Move page to end of LRU list (most recently used)."""
        if page_id in self.lru_order:
            self.lru_order.remove(page_id)
        self.lru_order.append(page_id)
    
    def _evict(self):
        """Evict a page using LRU policy."""
        # Find unpinned page (pin_count == 0)
        for page_id in self.lru_order:
            page = self.pages[page_id]
            if page.pin_count == 0:
                # Flush if dirty
                if page.dirty:
                    self.flush_page(page_id)
                
                # Remove from buffer pool
                del self.pages[page_id]
                self.lru_order.remove(page_id)
                return
        
        raise Exception("All pages are pinned, cannot evict")
    
    def display(self):
        """Display buffer pool contents."""
        print(f"Buffer Pool ({len(self.pages)}/{self.pool_size} pages):")
        for page_id, page in self.pages.items():
            print(f"  {page}")
        print(f"LRU order: {self.lru_order}")

# Example
bp = BufferPool(pool_size=3)

# Read pages
p1 = bp.read_page(1)
p2 = bp.read_page(2)
p3 = bp.read_page(3)

print("\nInitial buffer pool:")
bp.display()

# Write to page 1
bp.write_page(1, b"Updated data for page 1")

# Read page 4 (should evict page 2 - LRU)
p4 = bp.read_page(4)

print("\nAfter reading page 4 (page 2 evicted):")
bp.display()

# Unpin and flush
bp.unpin_page(1, dirty=True)
bp.flush_all()

print("\nDisk contents after flush:")
for page_id, data in bp.disk.items():
    print(f"  Page {page_id}: {data[:20]}...")

Clock Algorithm (Second Chance)
# Clock algorithm: circular buffer with reference bits.
# More efficient than LRU for large buffer pools.

class ClockBufferPool:
    """Buffer pool using Clock (Second Chance) algorithm."""
    
    def __init__(self, pool_size=10):
        self.pool_size = pool_size
        self.pages = {}
        self.clock = []  # Circular list of page_ids
        self.hand = 0  # Clock hand position
        self.disk = {}
    
    def read_page(self, page_id):
        """Read a page with Clock algorithm."""
        # Page already in buffer pool
        if page_id in self.pages:
            page = self.pages[page_id]
            page.pin_count += 1
            page.referenced = True
            return page
        
        # Buffer pool full, need to evict
        if len(self.pages) >= self.pool_size:
            self._evict()
        
        # Read from disk
        data = self.disk.get(page_id, bytearray(4096))
        page = Page(page_id, data)
        page.pin_count = 1
        page.referenced = True
        self.pages[page_id] = page
        self.clock.append(page_id)
        
        return page
    
    def _evict(self):
        """Evict a page using Clock algorithm."""
        while True:
            page_id = self.clock[self.hand]
            page = self.pages[page_id]
            
            if page.pin_count > 0:
                # Page is pinned, skip
                self.hand = (self.hand + 1) % len(self.clock)
                continue
            
            if page.referenced:
                # Give second chance
                page.referenced = False
                self.hand = (self.hand + 1) % len(self.clock)
            else:
                # Evict this page
                if page.dirty:
                    self.disk[page_id] = page.data
                
                del self.pages[page_id]
                self.clock.pop(self.hand)
                if self.hand >= len(self.clock):
                    self.hand = 0
                return

CHAPTER 4: WRITE-AHEAD LOGGING (WAL)
WAL Implementation
# WAL: ensures durability by logging changes before applying them.
# Protocol: Write log record → Flush log → Apply changes → Commit

import time
import json

class LogRecord:
    """A single log record."""
    
    def __init__(self, lsn, txn_id, operation, page_id, before_image, after_image):
        self.lsn = lsn  # Log Sequence Number
        self.txn_id = txn_id
        self.operation = operation  # 'UPDATE', 'INSERT', 'DELETE'
        self.page_id = page_id
        self.before_image = before_image
        self.after_image = after_image
        self.timestamp = time.time()
    
    def to_dict(self):
        return {
            'lsn': self.lsn,
            'txn_id': self.txn_id,
            'operation': self.operation,
            'page_id': self.page_id,
            'before_image': self.before_image.hex() if self.before_image else None,
            'after_image': self.after_image.hex() if self.after_image else None,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            lsn=data['lsn'],
            txn_id=data['txn_id'],
            operation=data['operation'],
            page_id=data['page_id'],
            before_image=bytes.fromhex(data['before_image']) if data['before_image'] else None,
            after_image=bytes.fromhex(data['after_image']) if data['after_image'] else None
        )
    
    def __repr__(self):
        return f"LogRecord(LSN={self.lsn}, TXN={self.txn_id}, OP={self.operation})"

class WriteAheadLog:
    """Write-Ahead Log implementation."""
    
    def __init__(self, log_file='wal.log'):
        self.log_file = log_file
        self.current_lsn = 0
        self.flushed_lsn = 0
        self.log_buffer = []
        self.buffer_size = 100
    
    def append(self, txn_id, operation, page_id, before_image, after_image):
        """Append a log record."""
        self.current_lsn += 1
        record = LogRecord(
            lsn=self.current_lsn,
            txn_id=txn_id,
            operation=operation,
            page_id=page_id,
            before_image=before_image,
            after_image=after_image
        )
        self.log_buffer.append(record)
        
        # Flush if buffer full
        if len(self.log_buffer) >= self.buffer_size:
            self.flush()
        
        return self.current_lsn
    
    def flush(self):
        """Flush log buffer to disk."""
        if not self.log_buffer:
            return
        
        # Write to disk (simplified)
        with open(self.log_file, 'a') as f:
            for record in self.log_buffer:
                f.write(json.dumps(record.to_dict()) + '\n')
        
        self.flushed_lsn = self.current_lsn
        self.log_buffer.clear()
    
    def read_all(self):
        """Read all log records from disk."""
        records = []
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    records.append(LogRecord.from_dict(data))
        except FileNotFoundError:
            pass
        return records
    
    def truncate(self, lsn):
        """Truncate log up to given LSN (after checkpoint)."""
        records = self.read_all()
        records = [r for r in records if r.lsn > lsn]
        
        with open(self.log_file, 'w') as f:
            for record in records:
                f.write(json.dumps(record.to_dict()) + '\n')

# Example
wal = WriteAheadLog('test_wal.log')

# Simulate transaction
txn_id = 1
page_id = 100
before = b"old data"
after = b"new data"

lsn1 = wal.append(txn_id, 'UPDATE', page_id, before, after)
print(f"Appended log record with LSN {lsn1}")

lsn2 = wal.append(txn_id, 'INSERT', 101, None, b"inserted data")
print(f"Appended log record with LSN {lsn2}")

wal.flush()
print("Log flushed to disk")

# Read back
records = wal.read_all()
print(f"Read {len(records)} log records:")
for r in records:
    print(f"  {r}")

Recovery with WAL
# Recovery: redo committed transactions, undo uncommitted ones.

class RecoveryManager:
    """Recovery manager using WAL."""
    
    def __init__(self, wal, buffer_pool):
        self.wal = wal
        self.buffer_pool = buffer_pool
        self.committed_txns = set()
        self.active_txns = set()
    
    def begin_transaction(self, txn_id):
        """Mark transaction as active."""
        self.active_txns.add(txn_id)
    
    def commit_transaction(self, txn_id):
        """Mark transaction as committed."""
        self.active_txns.discard(txn_id)
        self.committed_txns.add(txn_id)
    
    def abort_transaction(self, txn_id):
        """Mark transaction as aborted."""
        self.active_txns.discard(txn_id)
    
    def recover(self):
        """Perform recovery after crash."""
        print("Starting recovery...")
        
        # Read all log records
        records = self.wal.read_all()
        
        # Redo phase: reapply all changes
        print(f"Redo phase: {len(records)} records")
        for record in records:
            self._redo(record)
        
        # Undo phase: rollback uncommitted transactions
        print(f"Undo phase: {len(self.active_txns)} active transactions")
        for record in reversed(records):
            if record.txn_id in self.active_txns:
                self._undo(record)
        
        print("Recovery complete")
    
    def _redo(self, record):
        """Redo a log record."""
        page = self.buffer_pool.read_page(record.page_id)
        if record.after_image:
            page.data = record.after_image
            page.dirty = True
        self.buffer_pool.unpin_page(record.page_id)
    
    def _undo(self, record):
        """Undo a log record."""
        page = self.buffer_pool.read_page(record.page_id)
        if record.before_image:
            page.data = record.before_image
            page.dirty = True
        self.buffer_pool.unpin_page(record.page_id, dirty=True)

# Example
wal = WriteAheadLog('recovery_wal.log')
bp = BufferPool(pool_size=5)
rm = RecoveryManager(wal, bp)

# Simulate transactions
rm.begin_transaction(1)
lsn1 = wal.append(1, 'UPDATE', 100, b"old1", b"new1")
rm.commit_transaction(1)

rm.begin_transaction(2)
lsn2 = wal.append(2, 'UPDATE', 101, b"old2", b"new2")
# Transaction 2 not committed (crash)

wal.flush()

print("\nBefore recovery:")
bp.display()

# Simulate crash and recovery
rm2 = RecoveryManager(wal, bp)
rm2.begin_transaction(2)  # Transaction 2 still active
rm2.recover()

print("\nAfter recovery:")
bp.display()

CHAPTER 5: TRANSACTIONS AND CONCURRENCY
Two-Phase Locking (2PL)
# 2PL: ensures serializability by acquiring all locks before releasing any.
# Phases:
# 1. Growing phase: acquire locks, no releases
# 2. Shrinking phase: release locks, no acquisitions

class Lock:
    """Lock on a data item."""
    
    def __init__(self):
        self.shared_holders = set()   # Transaction IDs with shared locks
        self.exclusive_holder = None  # Transaction ID with exclusive lock
        self.wait_queue = []          # Queue of waiting transactions
    
    def acquire_shared(self, txn_id):
        """Acquire shared (read) lock."""
        if self.exclusive_holder is None:
            self.shared_holders.add(txn_id)
            return True
        return False
    
    def acquire_exclusive(self, txn_id):
        """Acquire exclusive (write) lock."""
        if self.exclusive_holder is None and not self.shared_holders:
            self.exclusive_holder = txn_id
            return True
        return False
    
    def release(self, txn_id):
        """Release lock held by transaction."""
        if txn_id in self.shared_holders:
            self.shared_holders.remove(txn_id)
        elif self.exclusive_holder == txn_id:
            self.exclusive_holder = None

class LockManager:
    """Lock manager implementing 2PL."""
    
    def __init__(self):
        self.locks = {}  # data_item -> Lock
        self.txn_locks = {}  # txn_id -> set of locked items
        self.txn_phase = {}  # txn_id -> 'growing' or 'shrinking'
    
    def begin_transaction(self, txn_id):
        """Begin a new transaction."""
        self.txn_locks[txn_id] = set()
        self.txn_phase[txn_id] = 'growing'
    
    def lock_shared(self, txn_id, data_item):
        """Acquire shared lock on data item."""
        if self.txn_phase[txn_id] == 'shrinking':
            raise Exception("Cannot acquire lock in shrinking phase")
        
        if data_item not in self.locks:
            self.locks[data_item] = Lock()
        
        lock = self.locks[data_item]
        if lock.acquire_shared(txn_id):
            self.txn_locks[txn_id].add(data_item)
            return True
        return False
    
    def lock_exclusive(self, txn_id, data_item):
        """Acquire exclusive lock on data item."""
        if self.txn_phase[txn_id] == 'shrinking':
            raise Exception("Cannot acquire lock in shrinking phase")
        
        if data_item not in self.locks:
            self.locks[data_item] = Lock()
        
        lock = self.locks[data_item]
        if lock.acquire_exclusive(txn_id):
            self.txn_locks[txn_id].add(data_item)
            return True
        return False
    
    def unlock(self, txn_id, data_item):
        """Release lock on data item."""
        if data_item in self.txn_locks[txn_id]:
            self.txn_phase[txn_id] = 'shrinking'
            self.locks[data_item].release(txn_id)
            self.txn_locks[txn_id].remove(data_item)
    
    def commit(self, txn_id):
        """Commit transaction and release all locks."""
        for data_item in self.txn_locks[txn_id]:
            self.locks[data_item].release(txn_id)
        del self.txn_locks[txn_id]
        del self.txn_phase[txn_id]
    
    def abort(self, txn_id):
        """Abort transaction and release all locks."""
        self.commit(txn_id)  # Same cleanup

# Example
lm = LockManager()

# Transaction 1
lm.begin_transaction(1)
lm.lock_shared(1, 'A')
print("T1 acquired shared lock on A")

# Transaction 2
lm.begin_transaction(2)
lm.lock_shared(2, 'A')
print("T2 acquired shared lock on A")

# Transaction 1 tries exclusive lock
success = lm.lock_exclusive(1, 'A')
print(f"T1 exclusive lock on A: {success}")  # False (T2 has shared lock)

# Transaction 2 releases
lm.unlock(2, 'A')
print("T2 released lock on A")

# Now T1 can get exclusive lock
success = lm.lock_exclusive(1, 'A')
print(f"T1 exclusive lock on A: {success}")  # True

lm.commit(1)

MVCC (Multi-Version Concurrency Control)
# MVCC: multiple versions of data items for concurrent access.
# Readers don't block writers, writers don't block readers.

class MVCCVersion:
    """A version of a data item."""
    
    def __init__(self, value, txn_id, timestamp):
        self.value = value
        self.txn_id = txn_id
        self.timestamp = timestamp
        self.next_version = None  # Linked list of versions

class MVCCManager:
    """MVCC implementation."""
    
    def __init__(self):
        self.data = {}  # data_item -> MVCCVersion (latest)
        self.current_timestamp = 0
    
    def begin_transaction(self):
        """Begin transaction with snapshot timestamp."""
        self.current_timestamp += 1
        return self.current_timestamp
    
    def read(self, data_item, txn_timestamp):
        """Read data item at given timestamp."""
        if data_item not in self.data:
            return None
        
        # Find version visible to this transaction
        version = self.data[data_item]
        while version:
            if version.timestamp <= txn_timestamp:
                return version.value
            version = version.next_version
        
        return None
    
    def write(self, data_item, value, txn_id, txn_timestamp):
        """Write new version of data item."""
        new_version = MVCCVersion(value, txn_id, txn_timestamp)
        
        if data_item in self.data:
            new_version.next_version = self.data[data_item]
        
        self.data[data_item] = new_version
    
    def commit(self, txn_id, txn_timestamp):
        """Commit transaction (versions become visible)."""
        pass  # Versions already visible at commit timestamp
    
    def abort(self, txn_id, txn_timestamp):
        """Abort transaction (remove uncommitted versions)."""
        for data_item in list(self.data.keys()):
            version = self.data[data_item]
            if version.txn_id == txn_id:
                # Remove this version
                if version.next_version:
                    self.data[data_item] = version.next_version
                else:
                    del self.data[data_item]
    
    def garbage_collect(self, oldest_active_timestamp):
        """Remove old versions no longer needed."""
        for data_item in list(self.data.keys()):
            version = self.data[data_item]
            prev = None
            
            while version:
                if version.timestamp < oldest_active_timestamp:
                    # Remove this version
                    if prev:
                        prev.next_version = version.next_version
                    else:
                        if version.next_version:
                            self.data[data_item] = version.next_version
                        else:
                            del self.data[data_item]
                    break
                prev = version
                version = version.next_version

# Example
mvcc = MVCCManager()

# Transaction 1
t1 = mvcc.begin_transaction()
mvcc.write('A', 100, 1, t1)
mvcc.commit(1, t1)

# Transaction 2
t2 = mvcc.begin_transaction()
mvcc.write('A', 200, 2, t2)
mvcc.commit(2, t2)

# Transaction 3 reads at timestamp 1
t3 = mvcc.begin_transaction()
value = mvcc.read('A', 1)
print(f"T3 reads A at t=1: {value}")  # 100

# Transaction 4 reads at timestamp 2
t4 = mvcc.begin_transaction()
value = mvcc.read('A', 2)
print(f"T4 reads A at t=2: {value}")  # 200

# Transaction 5 reads at current timestamp
t5 = mvcc.begin_transaction()
value = mvcc.read('A', t5)
print(f"T5 reads A at t={t5}: {value}")  # 200

CHAPTER 6: QUERY PARSING AND PLANNING
SQL Parser (Simplified)
# Parser: converts SQL text into abstract syntax tree (AST).

class ASTNode:
    """Base class for AST nodes."""
    pass

class SelectNode(ASTNode):
    def __init__(self, columns, tables, where=None, order_by=None, limit=None):
        self.columns = columns
        self.tables = tables
        self.where = where
        self.order_by = order_by
        self.limit = limit
    
    def __repr__(self):
        return f"SELECT {self.columns} FROM {self.tables}"

class WhereNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class ColumnNode(ASTNode):
    def __init__(self, name, table=None):
        self.name = name
        self.table = table

class TableNode(ASTNode):
    def __init__(self, name, alias=None):
        self.name = name
        self.alias = alias

class SQLParser:
    """Simple SQL parser."""
    
    def __init__(self):
        self.tokens = []
        self.pos = 0
    
    def tokenize(self, sql):
        """Tokenize SQL string."""
        import re
        pattern = r'\b(SELECT|FROM|WHERE|AND|OR|ORDER|BY|LIMIT|ASC|DESC|INSERT|INTO|VALUES|UPDATE|SET|DELETE)\b|[\w.*]+|[=<>!]+|\d+|[,;()]'
        self.tokens = re.findall(pattern, sql, re.IGNORECASE)
        self.pos = 0
    
    def parse(self, sql):
        """Parse SQL into AST."""
        self.tokenize(sql)
        return self._parse_select()
    
    def _parse_select(self):
        """Parse SELECT statement."""
        if not self._match('SELECT'):
            raise Exception("Expected SELECT")
        
        # Parse column list
        columns = []
        while True:
            col = self._parse_column()
            columns.append(col)
            if not self._match(','):
                break
        
        # Parse FROM clause
        if not self._match('FROM'):
            raise Exception("Expected FROM")
        
        tables = []
        while True:
            table = self._parse_table()
            tables.append(table)
            if not self._match(','):
                break
        
        # Parse WHERE clause (optional)
        where = None
        if self._match('WHERE'):
            where = self._parse_expression()
        
        # Parse ORDER BY (optional)
        order_by = None
        if self._match('ORDER'):
            self._expect('BY')
            order_by = self._parse_column()
            if self._match('ASC'):
                order_by = (order_by, 'ASC')
            elif self._match('DESC'):
                order_by = (order_by, 'DESC')
            else:
                order_by = (order_by, 'ASC')
        
        # Parse LIMIT (optional)
        limit = None
        if self._match('LIMIT'):
            limit = int(self._current())
            self._advance()
        
        return SelectNode(columns, tables, where, order_by, limit)
    
    def _parse_column(self):
        """Parse column reference."""
        name = self._current()
        self._advance()
        
        if self._match('.'):
            table = name
            name = self._current()
            self._advance()
            return ColumnNode(name, table)
        
        return ColumnNode(name)
    
    def _parse_table(self):
        """Parse table reference."""
        name = self._current()
        self._advance()
        
        alias = None
        if self._current() and self._current().upper() != 'WHERE':
            alias = self._current()
            self._advance()
        
        return TableNode(name, alias)
    
    def _parse_expression(self):
        """Parse WHERE expression."""
        left = self._parse_column()
        operator = self._current()
        self._advance()
        right = self._parse_column()
        
        return WhereNode(left, operator, right)
    
    def _match(self, expected):
        """Match and consume token."""
        if self.pos < len(self.tokens) and self.tokens[self.pos].upper() == expected.upper():
            self.pos += 1
            return True
        return False
    
    def _expect(self, expected):
        """Expect and consume token."""
        if not self._match(expected):
            raise Exception(f"Expected {expected}")
    
    def _current(self):
        """Get current token."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def _advance(self):
        """Advance to next token."""
        self.pos += 1

# Example
parser = SQLParser()
sql = "SELECT name, age FROM users WHERE age > 18 ORDER BY name LIMIT 10"
ast = parser.parse(sql)
print(f"Parsed: {ast}")
print(f"Columns: {ast.columns}")
print(f"Tables: {ast.tables}")
print(f"Where: {ast.where}")

Query Optimizer
# Optimizer: transforms query plan for better performance.
# Uses cost-based optimization with statistics.

class QueryPlan:
    """Query execution plan."""
    
    def __init__(self, operation, children=None, cost=0, rows=0):
        self.operation = operation
        self.children = children or []
        self.cost = cost
        self.rows = rows
    
    def __repr__(self):
        return f"{self.operation}(cost={self.cost}, rows={self.rows})"

class TableStats:
    """Table statistics for optimization."""
    
    def __init__(self, num_rows, num_pages, column_stats=None):
        self.num_rows = num_rows
        self.num_pages = num_pages
        self.column_stats = column_stats or {}

class QueryOptimizer:
    """Cost-based query optimizer."""
    
    def __init__(self, table_stats):
        self.table_stats = table_stats
    
    def optimize(self, ast):
        """Optimize query AST into execution plan."""
        if isinstance(ast, SelectNode):
            return self._optimize_select(ast)
        raise Exception("Unsupported query type")
    
    def _optimize_select(self, node):
        """Optimize SELECT query."""
        # Start with base table scan
        table = node.tables[0]
        stats = self.table_stats.get(table.name)
        
        if not stats:
            # No statistics, use default
            plan = QueryPlan('SeqScan', cost=1000, rows=1000)
        else:
            plan = QueryPlan('SeqScan', cost=stats.num_pages, rows=stats.num_rows)
        
        # Apply WHERE clause
        if node.where:
            selectivity = self._estimate_selectivity(node.where, stats)
            plan = QueryPlan(
                'Filter',
                children=[plan],
                cost=plan.cost + plan.rows * 0.01,
                rows=int(plan.rows * selectivity)
            )
        
        # Apply ORDER BY
        if node.order_by:
            plan = QueryPlan(
                'Sort',
                children=[plan],
                cost=plan.cost + plan.rows * 0.1,
                rows=plan.rows
            )
        
        # Apply LIMIT
        if node.limit:
            plan = QueryPlan(
                'Limit',
                children=[plan],
                cost=plan.cost + node.limit,
                rows=min(plan.rows, node.limit)
            )
        
        # Consider index scan
        if node.where and self._can_use_index(node.where, table.name):
            index_plan = QueryPlan(
                'IndexScan',
                cost=10,  # Much cheaper than seq scan
                rows=int(stats.num_rows * 0.1)  # Assume 10% selectivity
            )
            
            if index_plan.cost < plan.cost:
                plan = index_plan
        
        return plan
    
    def _estimate_selectivity(self, where, stats):
        """Estimate selectivity of WHERE clause."""
        # Simplified: assume 10% selectivity for equality, 30% for range
        if where.operator == '=':
            return 0.1
        elif where.operator in ('>', '<', '>=', '<='):
            return 0.3
        return 0.5
    
    def _can_use_index(self, where, table_name):
        """Check if an index can be used."""
        # Simplified: assume index exists on any column
        return True

# Example
stats = {
    'users': TableStats(num_rows=10000, num_pages=100)
}

optimizer = QueryOptimizer(stats)
ast = parser.parse("SELECT name FROM users WHERE age = 25")
plan = optimizer.optimize(ast)
print(f"\nOptimized plan: {plan}")

CHAPTER 7: QUERY EXECUTION
Volcano Model (Iterator Model)
# Volcano: each operator implements open(), next(), close() methods.
# Operators pull tuples from children.

class Operator:
    """Base class for query operators."""
    
    def open(self):
        """Initialize operator."""
        pass
    
    def next(self):
        """Return next tuple or None."""
        return None
    
    def close(self):
        """Clean up resources."""
        pass

class SeqScanOperator(Operator):
    """Sequential scan operator."""
    
    def __init__(self, table_name, data):
        self.table_name = table_name
        self.data = data
        self.pos = 0
    
    def open(self):
        self.pos = 0
    
    def next(self):
        if self.pos < len(self.data):
            tuple = self.data[self.pos]
            self.pos += 1
            return tuple
        return None
    
    def close(self):
        self.pos = 0

class FilterOperator(Operator):
    """Filter operator (WHERE clause)."""
    
    def __init__(self, child, predicate):
        self.child = child
        self.predicate = predicate
    
    def open(self):
        self.child.open()
    
    def next(self):
        while True:
            tuple = self.child.next()
            if tuple is None:
                return None
            if self.predicate(tuple):
                return tuple
    
    def close(self):
        self.child.close()

class ProjectOperator(Operator):
    """Project operator (SELECT columns)."""
    
    def __init__(self, child, columns):
        self.child = child
        self.columns = columns
    
    def open(self):
        self.child.open()
    
    def next(self):
        tuple = self.child.next()
        if tuple is None:
            return None
        return {col: tuple[col] for col in self.columns}
    
    def close(self):
        self.child.close()

class SortOperator(Operator):
    """Sort operator (ORDER BY)."""
    
    def __init__(self, child, sort_key, ascending=True):
        self.child = child
        self.sort_key = sort_key
        self.ascending = ascending
        self.sorted_data = []
        self.pos = 0
    
    def open(self):
        self.child.open()
        self.sorted_data = []
        
        # Collect all tuples
        while True:
            tuple = self.child.next()
            if tuple is None:
                break
            self.sorted_data.append(tuple)
        
        # Sort
        self.sorted_data.sort(
            key=lambda t: t[self.sort_key],
            reverse=not self.ascending
        )
        self.pos = 0
    
    def next(self):
        if self.pos < len(self.sorted_data):
            tuple = self.sorted_data[self.pos]
            self.pos += 1
            return tuple
        return None
    
    def close(self):
        self.sorted_data = []
        self.child.close()

class LimitOperator(Operator):
    """Limit operator."""
    
    def __init__(self, child, limit):
        self.child = child
        self.limit = limit
        self.count = 0
    
    def open(self):
        self.child.open()
        self.count = 0
    
    def next(self):
        if self.count >= self.limit:
            return None
        tuple = self.child.next()
        if tuple:
            self.count += 1
        return tuple
    
    def close(self):
        self.child.close()

# Example
data = [
    {'name': 'Alice', 'age': 25, 'city': 'NYC'},
    {'name': 'Bob', 'age': 30, 'city': 'LA'},
    {'name': 'Charlie', 'age': 25, 'city': 'NYC'},
    {'name': 'David', 'age': 35, 'city': 'Chicago'},
]

# SELECT name, city FROM users WHERE age = 25 ORDER BY name
scan = SeqScanOperator('users', data)
filter_op = FilterOperator(scan, lambda t: t['age'] == 25)
project = ProjectOperator(filter_op, ['name', 'city'])
sort = SortOperator(project, 'name')
limit = LimitOperator(sort, 10)

limit.open()
print("\nQuery results:")
while True:
    tuple = limit.next()
    if tuple is None:
        break
    print(f"  {tuple}")
limit.close()

Hash Join
# Hash Join: build hash table on smaller relation, probe with larger.

class HashJoinOperator(Operator):
    """Hash join operator."""
    
    def __init__(self, left, right, left_key, right_key):
        self.left = left
        self.right = right
        self.left_key = left_key
        self.right_key = right_key
        self.hash_table = {}
        self.right_tuples = []
        self.right_pos = 0
    
    def open(self):
        self.left.open()
        self.right.open()
        
        # Build phase: hash left relation
        self.hash_table = {}
        while True:
            tuple = self.left.next()
            if tuple is None:
                break
            key = tuple[self.left_key]
            if key not in self.hash_table:
                self.hash_table[key] = []
            self.hash_table[key].append(tuple)
        
        # Collect right tuples
        self.right_tuples = []
        while True:
            tuple = self.right.next()
            if tuple is None:
                break
            self.right_tuples.append(tuple)
        
        self.right_pos = 0
    
    def next(self):
        # Probe phase
        while self.right_pos < len(self.right_tuples):
            right_tuple = self.right_tuples[self.right_pos]
            self.right_pos += 1
            
            key = right_tuple[self.right_key]
            if key in self.hash_table:
                for left_tuple in self.hash_table[key]:
                    # Merge tuples
                    merged = {**left_tuple, **right_tuple}
                    return merged
        
        return None
    
    def close(self):
        self.left.close()
        self.right.close()
        self.hash_table = {}

# Example
users = [
    {'id': 1, 'name': 'Alice'},
    {'id': 2, 'name': 'Bob'},
    {'id': 3, 'name': 'Charlie'},
]

orders = [
    {'user_id': 1, 'product': 'Laptop'},
    {'user_id': 1, 'product': 'Mouse'},
    {'user_id': 2, 'product': 'Keyboard'},
]

left_scan = SeqScanOperator('users', users)
right_scan = SeqScanOperator('orders', orders)
join = HashJoinOperator(left_scan, right_scan, 'id', 'user_id')

join.open()
print("\nJoin results:")
while True:
    tuple = join.next()
    if tuple is None:
        break
    print(f"  {tuple}")
join.close()

CHAPTER 8: INDEXING
B+ Tree Index
# B+ Tree: all data in leaf nodes, internal nodes only for navigation.
# Better for range queries than B-Tree.

class BPlusTreeNode:
    """B+ Tree node."""
    
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.values = [] if leaf else []  # Leaf: values, Internal: children
        self.next_leaf = None  # For leaf nodes (linked list)

class BPlusTree:
    """B+ Tree implementation."""
    
    def __init__(self, t=2):
        self.t = t  # Minimum degree
        self.root = BPlusTreeNode(leaf=True)
    
    def search(self, key):
        """Search for a key."""
        return self._search(self.root, key)
    
    def _search(self, node, key):
        """Recursive search."""
        # Find first key >= search key
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        if node.leaf:
            if i < len(node.keys) and node.keys[i] == key:
                return node.values[i]
            return None
        else:
            return self._search(node.values[i], key)
    
    def insert(self, key, value):
        """Insert a key-value pair."""
        root = self.root
        
        # If root is full, split
        if len(root.keys) == 2 * self.t - 1:
            new_root = BPlusTreeNode(leaf=False)
            new_root.values.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        
        self._insert_non_full(self.root, key, value)
    
    def _insert_non_full(self, node, key, value):
        """Insert into non-full node."""
        i = len(node.keys) - 1
        
        if node.leaf:
            # Insert into leaf
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            node.keys.insert(i, key)
            node.values.insert(i, value)
            
            # Split if full
            if len(node.keys) == 2 * self.t - 1:
                self._split_leaf(node)
        else:
            # Find child
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            
            # Split child if full
            if len(node.values[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            
            self._insert_non_full(node.values[i], key, value)
    
    def _split_child(self, parent, i):
        """Split internal node child."""
        child = parent.values[i]
        new_node = BPlusTreeNode(leaf=False)
        
        # Median key goes up
        median_idx = self.t - 1
        median_key = child.keys[median_idx]
        
        # New node gets right half
        new_node.keys = child.keys[median_idx + 1:]
        new_node.values = child.values[median_idx + 1:]
        
        # Child keeps left half
        child.keys = child.keys[:median_idx]
        child.values = child.values[:median_idx + 1]
        
        # Insert median into parent
        parent.keys.insert(i, median_key)
        parent.values.insert(i + 1, new_node)
    
    def _split_leaf(self, leaf):
        """Split leaf node."""
        new_leaf = BPlusTreeNode(leaf=True)
        
        # Split keys and values
        mid = len(leaf.keys) // 2
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.values = leaf.values[mid:]
        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]
        
        # Update linked list
        new_leaf.next_leaf = leaf.next_leaf
        leaf.next_leaf = new_leaf
        
        # Add separator to parent
        # (Simplified: in real implementation, update parent)
    
    def range_scan(self, start_key, end_key):
        """Scan keys in range [start_key, end_key]."""
        # Find starting leaf
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and start_key > node.keys[i]:
                i += 1
            node = node.values[i]
        
        # Scan through linked list of leaves
        result = []
        while node:
            for i, key in enumerate(node.keys):
                if start_key <= key <= end_key:
                    result.append((key, node.values[i]))
                elif key > end_key:
                    return result
            node = node.next_leaf
        
        return result

# Example
bpt = BPlusTree(t=2)
for i in range(1, 20):
    bpt.insert(i, f"value_{i}")

print("B+ Tree search 10:", bpt.search(10))
print("B+ Tree range scan 5-10:", bpt.range_scan(5, 10))

Hash Index
# Hash Index: O(1) lookup for equality queries.

class HashIndex:
    """Hash-based index."""
    
    def __init__(self):
        self.hash_table = {}
    
    def insert(self, key, row_id):
        """Insert key-row_id mapping."""
        if key not in self.hash_table:
            self.hash_table[key] = []
        self.hash_table[key].append(row_id)
    
    def search(self, key):
        """Search for key."""
        return self.hash_table.get(key, [])
    
    def delete(self, key, row_id):
        """Delete key-row_id mapping."""
        if key in self.hash_table:
            self.hash_table[key] = [r for r in self.hash_table[key] if r != row_id]
            if not self.hash_table[key]:
                del self.hash_table[key]

# Example
hash_idx = HashIndex()
hash_idx.insert("Alice", 1)
hash_idx.insert("Bob", 2)
hash_idx.insert("Alice", 3)  # Duplicate key

print("Hash index search 'Alice':", hash_idx.search("Alice"))
print("Hash index search 'Charlie':", hash_idx.search("Charlie"))

CHAPTER 9: RECOVERY AND CHECKPOINTING
Checkpoint Manager
# Checkpoint: periodically flush all dirty pages and record state.
# Reduces recovery time by limiting WAL scan.

class CheckpointManager:
    """Checkpoint manager."""
    
    def __init__(self, wal, buffer_pool):
        self.wal = wal
        self.buffer_pool = buffer_pool
        self.last_checkpoint_lsn = 0
        self.active_transactions = set()
    
    def take_checkpoint(self):
        """Take a checkpoint."""
        print("Taking checkpoint...")
        
        # Log checkpoint record
        checkpoint_lsn = self.wal.append(
            txn_id=0,
            operation='CHECKPOINT',
            page_id=0,
            before_image=None,
            after_image=None
        )
        
        # Flush all dirty pages
        self.buffer_pool.flush_all()
        
        # Flush WAL
        self.wal.flush()
        
        # Record checkpoint LSN
        self.last_checkpoint_lsn = checkpoint_lsn
        
        print(f"Checkpoint taken at LSN {checkpoint_lsn}")
        return checkpoint_lsn
    
    def recover_from_checkpoint(self):
        """Recover from last checkpoint."""
        print(f"Recovering from checkpoint at LSN {self.last_checkpoint_lsn}")
        
        # Read log from checkpoint
        records = self.wal.read_all()
        records = [r for r in records if r.lsn > self.last_checkpoint_lsn]
        
        # Redo phase
        for record in records:
            if record.operation != 'CHECKPOINT':
                self._redo(record)
        
        print("Recovery complete")
    
    def _redo(self, record):
        """Redo a log record."""
        page = self.buffer_pool.read_page(record.page_id)
        if record.after_image:
            page.data = record.after_image
            page.dirty = True
        self.buffer_pool.unpin_page(record.page_id)

# Example
wal = WriteAheadLog('checkpoint_wal.log')
bp = BufferPool(pool_size=5)
cm = CheckpointManager(wal, bp)

# Simulate some operations
bp.write_page(1, b"data1")
bp.write_page(2, b"data2")

# Take checkpoint
cm.take_checkpoint()

# More operations
bp.write_page(3, b"data3")
wal.append(1, 'UPDATE', 3, b"old3", b"data3")
wal.flush()

# Recover
cm.recover_from_checkpoint()

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Query Execution Strategies
# Volcano (Iterator) Model: simple, extensible, but high overhead
# Vectorized Execution: process batches of tuples, better CPU cache usage
# Code Generation: compile queries to machine code (HyPer, Umbra)

# Vectorized execution example
class VectorizedScan:
    """Vectorized scan operator."""
    
    def __init__(self, data, batch_size=1024):
        self.data = data
        self.batch_size = batch_size
        self.pos = 0
    
    def next_batch(self):
        """Return next batch of tuples."""
        if self.pos >= len(self.data):
            return None
        
        batch = self.data[self.pos:self.pos + self.batch_size]
        self.pos += self.batch_size
        return batch

# Database Tuning and Optimization
# - Index selection: choose indexes based on query workload
# - Query rewriting: transform queries for better performance
# - Materialized views: precompute expensive queries
# - Partitioning: split large tables for better performance

# Modern Database Architectures
# - NewSQL: CockroachDB, TiDB (distributed SQL)
# - HTAP: Hybrid Transactional/Analytical Processing
# - Cloud-native: Aurora, Spanner, CosmosDB
# - Embedded: SQLite, DuckDB, libSQL

Recommended Reading
# - "Database System Concepts" by Silberschatz, Korth, Sudarshan
# - "Readings in Database Systems" (Red Book) by Hellerstein, Stonebraker
# - "Transaction Processing: Concepts and Techniques" by Gray, Reuter
# - "Database Internals" by Alex Petrov
# - CMU Database Group lectures: https://15445.courses.cs.cmu.edu/

# End of Database Internals Reference