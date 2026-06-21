# Data Structures and Algorithms Complete Reference


---

# CHAPTER 1: COMPLEXITY ANALYSIS (BIG O)


## Remarks

Data structures and algorithms are the foundation of computer science and the core of technical interviews at every major tech company. Understanding time and space complexity lets you predict performance and choose the right tool for each problem. This reference covers the structures and algorithms most commonly used in practice and interviews.

Key concepts: **Big O notation** (worst-case scaling), **Time vs Space complexity**, **Arrays vs Linked Lists** (contiguous vs pointer-based), **Trees** (hierarchical), **Graphs** (networks), **Hash Tables** (O(1) lookup), **Sorting** (comparison vs counting), **Dynamic Programming** (overlapping subproblems), **Greedy** (local optimal), **Two Pointers / Sliding Window** (array techniques).

Used in: every software system. Choosing ArrayList vs LinkedList, HashMap vs TreeMap, BFS vs DFS — these decisions shape performance.

Tools: **LeetCode** (practice), **NeetCode** (structured learning), **Visualgo** (visualizations), **Big-O Cheat Sheet** (bigocheatsheet.com).


## Big O Notation

```
Big O describes how performance scales with input size n.
Always consider WORST CASE unless specified.

COMMON COMPLEXITIES (fastest to slowest):

O(1)         Constant       Hash table lookup, array index access
O(log n)     Logarithmic    Binary search, balanced BST operations
O(n)         Linear         Array scan, linked list traversal
O(n log n)   Linearithmic   Merge sort, heap sort, efficient sorts
O(n²)        Quadratic      Nested loops, bubble sort, insertion sort
O(n³)        Cubic          Triple nested loops, naive matrix multiply
O(2ⁿ)        Exponential    Recursive Fibonacci (naive), subsets
O(n!)        Factorial      Permutations, brute-force TSP

GROWTH COMPARISON (n = 1,000,000):
  O(1):        1 operation
  O(log n):    20 operations
  O(n):        1,000,000 operations
  O(n log n):  20,000,000 operations
  O(n²):       1,000,000,000,000 operations (SLOW!)
  O(2ⁿ):       heat death of universe

RULES:
  1. Drop constants:     O(2n) → O(n)
  2. Drop lower terms:   O(n² + n) → O(n²)
  3. Different inputs:   O(n + m), not O(n) if two arrays
  4. Worst case default: unless problem guarantees average

SPACE COMPLEXITY:
  Same notation but for memory.
  In-place algorithm: O(1) extra space.
  Creating new array: O(n) space.
```


## Amortized Analysis

```
AMORTIZED: average cost over many operations.

Example: Dynamic Array (ArrayList/Vec/list)
  append() is usually O(1)
  BUT when full → resize (allocate 2x, copy all) → O(n)
  
  Over n appends:
    n-1 are O(1) + 1 is O(n) = total O(2n) = O(n)
    Amortized per operation: O(n)/n = O(1)
  
  So: ArrayList.append() is "amortized O(1)"

Example: Hash Table
  get/set is O(1) average
  Worst case (all collisions): O(n)
  With good hash function: amortized O(1)
```


---

# CHAPTER 2: LINEAR DATA STRUCTURES


## Arrays

```python
# Array: contiguous memory, indexed access
# Python list = dynamic array

arr = [1, 2, 3, 4, 5]

# Access by index: O(1)
val = arr[2]                   # 3

# Append: amortized O(1)
arr.append(6)                  # [1, 2, 3, 4, 5, 6]

# Insert at position: O(n) — must shift elements
arr.insert(0, 0)               # [0, 1, 2, 3, 4, 5, 6]

# Delete by index: O(n) — must shift
arr.pop(0)                     # [1, 2, 3, 4, 5, 6]

# Delete from end: O(1)
arr.pop()                      # [1, 2, 3, 4, 5]

# Search (unsorted): O(n)
idx = arr.index(3)             # 2
exists = 3 in arr              # True

# Search (sorted): O(log n) with binary search
import bisect
idx = bisect.bisect_left(sorted_arr, target)

# ARRAY COMPLEXITIES:
#   Access:  O(1)
#   Search:  O(n) unsorted, O(log n) sorted
#   Insert:  O(n) beginning/middle, O(1) amortized at end
#   Delete:  O(n) beginning/middle, O(1) from end
```


## Linked Lists

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Singly linked list operations

# Create: 1 → 2 → 3 → None
head = ListNode(1, ListNode(2, ListNode(3)))

# Traverse: O(n)
current = head
while current:
    print(current.val)
    current = current.next

# Insert at head: O(1)
new_head = ListNode(0, head)
head = new_head

# Insert at tail: O(n) — must traverse to end
current = head
while current.next:
    current = current.next
current.next = ListNode(4)

# Delete node: O(n) to find, O(1) to remove
# Delete node with value 2:
current = head
while current.next:
    if current.next.val == 2:
        current.next = current.next.next   # Skip the node
        break
    current = current.next

# Reverse linked list (CLASSIC INTERVIEW QUESTION)
def reverse_list(head):
    prev = None
    current = head
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    return prev

# Detect cycle (Floyd's algorithm — two pointers)
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Find middle (slow/fast pointers)
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

# LINKED LIST COMPLEXITIES:
#   Access:  O(n)
#   Search:  O(n)
#   Insert:  O(1) at head, O(n) at position
#   Delete:  O(1) at head, O(n) at position
#
# Use when: frequent insert/delete at beginning, unknown size
# Avoid when: need random access, cache-friendliness matters
```


## Stacks and Queues

```python
# STACK: LIFO (Last In, First Out)
# Like a stack of plates — add/remove from top only

stack = []
stack.append(1)         # Push: [1]
stack.append(2)         # Push: [1, 2]
stack.append(3)         # Push: [1, 2, 3]
top = stack[-1]         # Peek: 3
val = stack.pop()       # Pop: 3, stack = [1, 2]

# Use cases:
#   - Function call stack
#   - Undo/redo
#   - Expression evaluation (parentheses matching)
#   - DFS traversal
#   - Browser back button

# Classic: Valid Parentheses
def is_valid(s: str) -> bool:
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    return len(stack) == 0

is_valid("({[]})")    # True
is_valid("([)]")      # False


# QUEUE: FIFO (First In, First Out)
# Like a line at a store — join at back, leave from front

from collections import deque

queue = deque()
queue.append(1)         # Enqueue: [1]
queue.append(2)         # Enqueue: [1, 2]
queue.append(3)         # Enqueue: [1, 2, 3]
front = queue[0]        # Peek: 1
val = queue.popleft()   # Dequeue: 1, queue = [2, 3]

# Use cases:
#   - BFS traversal
#   - Task scheduling
#   - Message queues
#   - Print queue

# PRIORITY QUEUE (Heap)
import heapq

heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 4)
heapq.heappush(heap, 1)
heapq.heappush(heap, 5)

heapq.heappop(heap)     # 1 (smallest always comes out first)
heapq.heappop(heap)     # 1
heapq.heappop(heap)     # 3

# Max heap (negate values)
heapq.heappush(heap, -5)
max_val = -heapq.heappop(heap)   # 5

# STACK/QUEUE COMPLEXITIES:
#   Push/Enqueue: O(1)
#   Pop/Dequeue:  O(1)
#   Peek:         O(1)
#   Search:       O(n)
```


## Hash Tables

```python
# Hash table: key → value mapping with O(1) average access
# Python dict, JavaScript Object/Map, Java HashMap

d = {}
d["alice"] = 30              # Insert: O(1) average
age = d["alice"]             # Lookup: O(1) average
del d["alice"]               # Delete: O(1) average
exists = "alice" in d        # Contains: O(1) average

# Hash Set (unique elements)
s = set()
s.add(5)                     # O(1)
s.add(3)
s.add(5)                     # No duplicate
print(5 in s)                # O(1) lookup: True
s.remove(3)                  # O(1)

# HOW IT WORKS:
#   1. Hash function converts key → integer (hash code)
#   2. Hash code % array_size → index (bucket)
#   3. Store value at that index
#   Collision: two keys → same index
#     Chaining: linked list at each bucket
#     Open addressing: probe next empty slot
#   Load factor: items / buckets (resize when > 0.75)

# Classic: Two Sum (most asked interview question)
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

two_sum([2, 7, 11, 15], 9)    # [0, 1]

# Classic: Count frequency
from collections import Counter
freq = Counter([1, 2, 2, 3, 3, 3])
# Counter({3: 3, 2: 2, 1: 1})
freq.most_common(2)   # [(3, 3), (2, 2)]

# HASH TABLE COMPLEXITIES:
#   Insert:  O(1) average, O(n) worst (all collisions)
#   Lookup:  O(1) average, O(n) worst
#   Delete:  O(1) average, O(n) worst
#   Space:   O(n)
```


---

# CHAPTER 3: TREES


## Binary Tree

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Example:
#       1
#      / \
#     2   3
#    / \
#   4   5

root = TreeNode(1,
    TreeNode(2, TreeNode(4), TreeNode(5)),
    TreeNode(3)
)

# TRAVERSALS (must know all four!)

# Inorder (Left → Root → Right) — gives sorted order for BST
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)
# [4, 2, 5, 1, 3]

# Preorder (Root → Left → Right) — used for serialization
def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)
# [1, 2, 4, 5, 3]

# Postorder (Left → Right → Root) — used for deletion
def postorder(root):
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]
# [4, 5, 2, 3, 1]

# Level-order (BFS — level by level)
from collections import deque

def level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
# [[1], [2, 3], [4, 5]]

# Max depth
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# Invert binary tree (CLASSIC)
def invert_tree(root):
    if not root:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
```


## Binary Search Tree (BST)

```python
# BST property: left < root < right (for all nodes)
# Enables O(log n) search, insert, delete (if balanced)

class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        if not node:
            return TreeNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        return node

    def search(self, val):
        return self._search(self.root, val)

    def _search(self, node, val):
        if not node:
            return False
        if val == node.val:
            return True
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)

    def delete(self, val):
        self.root = self._delete(self.root, val)

    def _delete(self, node, val):
        if not node:
            return None
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            # Node found
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            # Two children: replace with inorder successor
            successor = node.right
            while successor.left:
                successor = successor.left
            node.val = successor.val
            node.right = self._delete(node.right, successor.val)
        return node

# Validate BST
def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):
    if not root:
        return True
    if root.val <= min_val or root.val >= max_val:
        return False
    return (is_valid_bst(root.left, min_val, root.val) and
            is_valid_bst(root.right, root.val, max_val))

# BST COMPLEXITIES:
#   Search:  O(log n) balanced, O(n) worst (degenerate)
#   Insert:  O(log n) balanced, O(n) worst
#   Delete:  O(log n) balanced, O(n) worst
# Self-balancing trees (AVL, Red-Black) guarantee O(log n)
```


## Heap (Priority Queue)

```python
# Heap: complete binary tree where parent ≤ children (min-heap)
# Used for: priority queues, top-K problems, median finding

import heapq

# Top K largest elements
def top_k_largest(nums, k):
    return heapq.nlargest(k, nums)

# Top K smallest
def top_k_smallest(nums, k):
    return heapq.nsmallest(k, nums)

# Kth largest element (INTERVIEW CLASSIC)
def kth_largest(nums, k):
    # Use min-heap of size k
    heap = nums[:k]
    heapq.heapify(heap)
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)   # Pop smallest, push new
    return heap[0]

# Merge K sorted lists
def merge_k_lists(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0].val, i, lst[0]))

    dummy = current = ListNode(0)
    while heap:
        val, i, node = heapq.heappop(heap)
        current.next = node
        current = current.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next

# HEAP COMPLEXITIES:
#   Insert:       O(log n)
#   Extract min:  O(log n)
#   Peek min:     O(1)
#   Heapify:      O(n) — surprisingly not O(n log n)!
#   Space:        O(n)
```


## Trie (Prefix Tree)

```python
# Trie: tree for string prefix lookups
# Used for: autocomplete, spell check, IP routing

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, prefix: str):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def autocomplete(self, prefix: str) -> list[str]:
        node = self._find(prefix)
        if not node:
            return []
        results = []
        self._collect(node, prefix, results)
        return results

    def _collect(self, node, prefix, results):
        if node.is_end:
            results.append(prefix)
        for char, child in node.children.items():
            self._collect(child, prefix + char, results)

# Usage
trie = Trie()
for word in ["apple", "app", "application", "apply", "banana"]:
    trie.insert(word)

trie.search("app")           # True
trie.search("ap")            # False
trie.starts_with("app")      # True
trie.autocomplete("app")     # ["app", "apple", "application", "apply"]

# TRIE COMPLEXITIES:
#   Insert:  O(m) where m = word length
#   Search:  O(m)
#   Space:   O(ALPHABET_SIZE × m × n) worst case
```


---

# CHAPTER 4: GRAPHS


## Graph Representations

```python
# ADJACENCY LIST (most common, memory efficient for sparse graphs)
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E'],
}

# Weighted graph
weighted = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('D', 3)],
    'C': [('A', 2), ('D', 1)],
    'D': [('B', 3), ('C', 1)],
}

# ADJACENCY MATRIX (good for dense graphs)
# 0 = no edge, 1 = edge, weight = weighted edge
matrix = [
    [0, 1, 1, 0],   # A → B, C
    [1, 0, 0, 1],   # B → A, D
    [1, 0, 0, 1],   # C → A, D
    [0, 1, 1, 0],   # D → B, C
]
```


## BFS (Breadth-First Search)

```python
from collections import deque

# BFS: explore level by level (shortest path in unweighted graph)
def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order

# Shortest path (unweighted)
def shortest_path(graph, start, end):
    if start == end:
        return [start]
    visited = {start}
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()
        for neighbor in graph[node]:
            if neighbor == end:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None   # No path exists

# Level-order traversal (distance from start)
def bfs_levels(graph, start):
    visited = {start}
    queue = deque([(start, 0)])
    levels = {}

    while queue:
        node, level = queue.popleft()
        levels[node] = level
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, level + 1))

    return levels

# BFS COMPLEXITY: O(V + E) time, O(V) space
# V = vertices, E = edges
```


## DFS (Depth-First Search)

```python
# DFS: explore as deep as possible, then backtrack

# Recursive DFS
def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    print(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

# Iterative DFS (using stack)
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                stack.append(neighbor)

    return order

# Detect cycle in directed graph
def has_cycle(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}

    def dfs(node):
        color[node] = GRAY   # Being processed
        for neighbor in graph.get(node, []):
            if color[neighbor] == GRAY:
                return True    # Back edge = cycle!
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        color[node] = BLACK   # Done processing
        return False

    return any(dfs(node) for node in graph if color[node] == WHITE)

# Number of connected components
def count_components(n, edges):
    graph = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    count = 0

    for node in range(n):
        if node not in visited:
            dfs_recursive(graph, node, visited)
            count += 1

    return count

# DFS COMPLEXITY: O(V + E) time, O(V) space
```


## Dijkstra's Algorithm (Shortest Path, Weighted)

```python
import heapq

def dijkstra(graph, start):
    # graph = { 'A': [('B', 4), ('C', 2)], ... }
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    heap = [(0, start)]

    while heap:
        current_dist, current = heapq.heappop(heap)

        if current_dist > distances[current]:
            continue   # Already found shorter path

        for neighbor, weight in graph[current]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current
                heapq.heappush(heap, (distance, neighbor))

    return distances, previous

# Reconstruct path
def get_path(previous, start, end):
    path = []
    current = end
    while current:
        path.append(current)
        current = previous[current]
    return path[::-1] if path[-1] == start else []

# Usage
distances, previous = dijkstra(weighted_graph, 'A')
print(f"Shortest distance A → D: {distances['D']}")
print(f"Path: {get_path(previous, 'A', 'D')}")

# DIJKSTRA COMPLEXITY:
#   Time:  O((V + E) log V) with min-heap
#   Space: O(V)
#   NOTE: doesn't work with negative weights! Use Bellman-Ford.
```


## Topological Sort (DAG)

```python
# Order nodes so that every edge u→v, u comes before v
# Only works on DAGs (Directed Acyclic Graphs)
# Use case: build systems, task scheduling, course prerequisites

def topological_sort(graph):
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1

    queue = deque([node for node in in_degree if in_degree[node] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(in_degree):
        return None   # Cycle detected!
    return order

# Example: course prerequisites
# CS101 → CS201 → CS301
# CS101 → CS202
graph = {
    'CS101': ['CS201', 'CS202'],
    'CS201': ['CS301'],
    'CS202': [],
    'CS301': [],
}
print(topological_sort(graph))   # ['CS101', 'CS201', 'CS202', 'CS301']
```


---

# CHAPTER 5: SORTING ALGORITHMS


## Comparison Sorts

```python
# MERGE SORT: O(n log n) guaranteed, stable, O(n) space
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# QUICK SORT: O(n log n) average, O(n²) worst, O(log n) space, in-place
def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# SORTING COMPARISON:
#
# Algorithm    Time (avg)   Time (worst)  Space    Stable?
# ──────────────────────────────────────────────────────────
# Merge Sort   O(n log n)   O(n log n)    O(n)     Yes
# Quick Sort   O(n log n)   O(n²)         O(log n) No
# Heap Sort    O(n log n)   O(n log n)    O(1)     No
# Tim Sort     O(n log n)   O(n log n)    O(n)     Yes ← Python/Java default
# Bubble Sort  O(n²)        O(n²)         O(1)     Yes
# Insertion    O(n²)        O(n²)         O(1)     Yes ← good for nearly sorted
# Selection    O(n²)        O(n²)         O(1)     No
#
# USE: built-in sort (Tim Sort) for almost everything.
# Know merge sort + quick sort for interviews.

# Python's built-in (Tim Sort — hybrid of merge + insertion)
arr.sort()                     # In-place
sorted_arr = sorted(arr)       # Returns new list
sorted_arr = sorted(arr, key=lambda x: x.name)   # Custom key
sorted_arr = sorted(arr, key=lambda x: (-x.score, x.name))  # Multi-key
```


## Non-Comparison Sorts

```python
# COUNTING SORT: O(n + k) where k = range of values
# Only works for integers with small range
def counting_sort(arr):
    if not arr:
        return arr
    max_val = max(arr)
    count = [0] * (max_val + 1)

    for num in arr:
        count[num] += 1

    result = []
    for val, cnt in enumerate(count):
        result.extend([val] * cnt)

    return result

# When to use:
#   ✅ Small range of integer values (ages 0-150, grades 0-100)
#   ✅ Need O(n) sorting
#   ❌ Large range (wastes memory)
#   ❌ Non-integer data
```


## Binary Search

```python
# Binary search: O(log n) on SORTED array

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Bisect (find insertion point)
def lower_bound(arr, target):
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left

# Search in rotated sorted array (INTERVIEW CLASSIC)
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```


---

# CHAPTER 6: COMMON INTERVIEW PATTERNS


## Two Pointers

```python
# TWO SUM (sorted array)
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left, right]
        elif total < target:
            left += 1
        else:
            right -= 1
    return []

# Remove duplicates in-place
def remove_duplicates(nums):
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    return write

# Container with most water (CLASSIC)
def max_area(heights):
    left, right = 0, len(heights) - 1
    max_water = 0
    while left < right:
        width = right - left
        height = min(heights[left], heights[right])
        max_water = max(max_water, width * height)
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return max_water
```


## Sliding Window

```python
# Maximum sum subarray of size k
def max_sum_subarray(nums, k):
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]   # Slide: add right, remove left
        max_sum = max(max_sum, window_sum)
    return max_sum

# Longest substring without repeating characters (CLASSIC)
def length_of_longest_substring(s):
    seen = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len

length_of_longest_substring("abcabcbb")   # 3 ("abc")
```


## Dynamic Programming

```python
# DP: break problem into overlapping subproblems, cache results

# Fibonacci (classic DP intro)
# Recursive (exponential) → DP (linear)

# Top-down (memoization)
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Bottom-up (tabulation)
def fib_bottom_up(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# Space-optimized
def fib_optimal(n):
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1


# Climbing Stairs (variant of Fibonacci)
def climb_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


# Coin Change (classic DP)
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

coin_change([1, 5, 10, 25], 36)   # 3 (25 + 10 + 1)


# Longest Common Subsequence
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

lcs("abcde", "ace")   # 3 ("ace")


# DP FRAMEWORK:
# 1. Define state: what variables describe a subproblem?
# 2. Define transition: how does state[i] relate to smaller states?
# 3. Base case: what are the trivial answers?
# 4. Order: which subproblems must be solved first?
# 5. Answer: which state contains the final answer?
```


## Backtracking

```python
# Generate all permutations
def permutations(nums):
    result = []

    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        for i in range(len(remaining)):
            path.append(remaining[i])
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()   # Undo choice (backtrack)

    backtrack([], nums)
    return result

permutations([1, 2, 3])
# [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]


# Generate all subsets
def subsets(nums):
    result = []

    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result

subsets([1, 2, 3])
# [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]


# N-Queens (CLASSIC backtracking)
def solve_n_queens(n):
    result = []

    def is_safe(queens, row, col):
        for r, c in enumerate(queens):
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def backtrack(queens):
        row = len(queens)
        if row == n:
            result.append(queens[:])
            return
        for col in range(n):
            if is_safe(queens, row, col):
                queens.append(col)
                backtrack(queens)
                queens.pop()

    backtrack([])
    return result
```


---

# CHAPTER 7: COMMON PITFALLS


## Algorithm and Interview Pitfalls

```
PITFALL 1: Not clarifying the problem
  Jump to coding without understanding constraints.
  Fix: ask about input size, edge cases, constraints.

PITFALL 2: Not considering edge cases
  Empty input, single element, duplicates, negative numbers.
  Fix: always test with [], [1], [1,1,1], [-1,0,1].

PITFALL 3: Off-by-one errors
  Binary search, loop bounds, substring indices.
  Fix: trace through with small example on paper.

PITFALL 4: Mutating input
  Sorting the input array changes original order.
  Fix: make a copy if order matters: sorted_arr = sorted(arr).

PITFALL 5: Integer overflow
  Sum of large numbers exceeds int range.
  Fix: Python handles big ints natively. In C++/Java: use long.

PITFALL 6: Wrong complexity
  "My solution works!" — on small input. O(n³) on 10⁶ elements = timeout.
  Fix: calculate complexity BEFORE coding. n=10⁶ needs O(n log n) or better.

PITFALL 7: Not using built-in data structures
  Writing your own hash map in interview.
  Fix: use dict, set, heapq, deque, Counter, defaultdict.

PITFALL 8: Forgetting to handle None/null
  root.left.val when root.left is None → crash.
  Fix: always check for None before accessing.

PITFALL 9: Modifying collection while iterating
  for item in list: list.remove(item) → skips elements.
  Fix: iterate over a copy, or build new list.

PITFALL 10: Brute force when pattern exists
  Nested loops when two-pointer or sliding window works.
  Fix: learn the 15-20 common patterns (NeetCode roadmap).

PITFALL 11: Not testing solution
  Submit without tracing through examples.
  Fix: walk through 2-3 examples by hand before submitting.

PITFALL 12: Premature optimization
  Optimizing before having a working solution.
  Fix: brute force first, then optimize. Working > fast.

PITFALL 13: Forgetting space complexity
  "O(1) space" but using recursion (stack space = O(n)).
  Fix: count stack frames in recursive solutions.

PITFALL 14: Graph: not marking visited
  BFS/DFS without visited set → infinite loop on cycles.
  Fix: ALWAYS maintain visited set for graphs.

PITFALL 15: DP: wrong state definition
  State doesn't capture enough info → wrong answer.
  Fix: think carefully about what defines a subproblem.
  Common states: index, remaining amount, last choice, True/False flag.
```