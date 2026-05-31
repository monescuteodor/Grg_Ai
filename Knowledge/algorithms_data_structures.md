# Algorithms and Data Structures Complete Reference

## Big-O Notation and Complexity Analysis

Big-O describes the upper bound of time or space growth as input size n grows.

Common complexities (fastest to slowest):
- O(1)        — Constant. Array index, hash table lookup.
- O(log n)    — Logarithmic. Binary search, balanced BST operations.
- O(n)        — Linear. Linear search, single loop.
- O(n log n)  — Linearithmic. Merge sort, heap sort, fast sort.
- O(n²)       — Quadratic. Bubble/insertion/selection sort, nested loops.
- O(n³)       — Cubic. Naive matrix multiplication.
- O(2ⁿ)       — Exponential. Brute-force subsets, naive Fibonacci.
- O(n!)       — Factorial. Brute-force permutations, TSP brute force.

Rules:
- Drop constants: O(2n) = O(n).
- Drop lower-order terms: O(n² + n) = O(n²).
- Best case vs Worst case vs Average case — Big-O is usually worst case.

Space complexity: extra memory used by the algorithm (not counting input).
In-place algorithm: O(1) extra space. Example: insertion sort.

Amortized analysis: average cost per operation over a sequence. Example: dynamic array append is O(1) amortized even though resizing is O(n) occasionally.

## Arrays and Strings

Static array: fixed-size contiguous memory block.
- Access by index: O(1)
- Search (unsorted): O(n)
- Insert/delete at end: O(1)
- Insert/delete at arbitrary position: O(n) — must shift elements

Dynamic array (ArrayList, vector): resizes when full (typically doubles capacity).
- Amortized append: O(1)
- Random access: O(1)

String operations:
- Concatenation of n strings of length k: naively O(n²k); use StringBuilder/join: O(nk)
- Substring: O(k) where k = substring length
- Comparison: O(min(len1, len2))

Two-pointer technique: use two indices moving toward each other or in the same direction to solve problems in O(n) instead of O(n²).
Example: finding pair that sums to target in sorted array — start left=0, right=n-1.

Sliding window: maintain a window of fixed or variable size over an array.
Example: maximum sum subarray of size k — slide window right, add new element, remove leftmost.

Prefix sums: precompute cumulative sums so range sum queries are O(1).
prefix[i] = a[0] + a[1] + … + a[i]; sum(l,r) = prefix[r] − prefix[l−1].

## Linked Lists

Singly linked list: each node holds data + pointer to next node. Head pointer starts the list.
Doubly linked list: each node holds data + next + prev. Allows O(1) deletion if node is known.
Circular linked list: last node points back to head.

Operations:
- Access by index: O(n) — must traverse from head
- Insert/delete at head: O(1)
- Insert/delete at tail: O(1) if tail pointer maintained; O(n) otherwise
- Insert/delete at arbitrary position: O(n) to find position, O(1) to rewire

Common techniques:
- Fast/slow pointer (Floyd's algorithm): detect cycles, find middle of list.
  Fast moves 2 steps, slow moves 1 step. If they meet, there's a cycle.
- Reverse a linked list: iterate keeping prev, curr, next pointers.
- Merge two sorted linked lists: compare heads, attach smaller, recurse.

## Stacks and Queues

Stack (LIFO — Last In First Out):
- push(x): add to top — O(1)
- pop(): remove from top — O(1)
- peek()/top(): view top without removing — O(1)
Implemented with: array (fixed stack), dynamic array, or linked list.
Uses: function call stack, undo/redo, expression parsing, DFS iteratively, balanced parentheses.

Queue (FIFO — First In First Out):
- enqueue(x): add to back — O(1)
- dequeue(): remove from front — O(1)
Implemented with: circular array (ring buffer), or linked list with head+tail pointers.
Uses: BFS, task scheduling, print queues, streaming data.

Deque (double-ended queue): insert/delete at both ends. O(1) for all four operations.

Priority Queue (Min/Max Heap):
- insert(x): O(log n)
- extractMin/extractMax: O(log n)
- peek: O(1)
Uses: Dijkstra's algorithm, A*, scheduling, heap sort, top-K elements.

Monotonic stack: stack that maintains elements in sorted order. Used for "next greater element" problems.

## Hash Tables

Maps keys to values using a hash function. Average-case O(1) for insert, delete, search.
Worst case O(n) with many collisions, but rare with a good hash function.

Collision resolution:
- Chaining: each slot holds a linked list of entries with the same hash.
- Open addressing: probe for next available slot (linear probing, quadratic probing, double hashing).

Load factor α = n/m (items/slots). Performance degrades as α approaches 1. Rehash when α exceeds threshold (typically 0.7).

Hash function requirements: deterministic, uniform distribution, fast to compute.
Common: modular hashing, polynomial rolling hash (for strings), MurmurHash, FNV.

Hash set: stores only keys (no values). O(1) membership test.

Applications: counting frequencies, detecting duplicates, caching (memoization), implementing sets.

## Trees

Binary tree: each node has at most 2 children (left and right).
Binary Search Tree (BST): for every node, left subtree < node < right subtree.
- Search, insert, delete: O(h) where h = height. O(log n) if balanced, O(n) if skewed.

Tree traversals:
- Inorder (L-Root-R): gives sorted order for BST.
- Preorder (Root-L-R): used to copy/serialize tree.
- Postorder (L-R-Root): used to delete tree, evaluate expressions.
- Level-order (BFS): processes nodes level by level using a queue.

Balanced BSTs (guarantee O(log n)):
- AVL tree: height difference between subtrees ≤ 1. Rotations maintain balance.
- Red-Black tree: used in most language standard library maps/sets.
- B-tree / B+-tree: used in databases and file systems. Many keys per node, optimized for disk.

Heap (binary heap): complete binary tree satisfying heap property.
- Min-heap: parent ≤ children. Root is the minimum.
- Max-heap: parent ≥ children. Root is the maximum.
- Stored as array: parent of i is (i−1)/2; children are 2i+1 and 2i+2.
- Heapify: O(n) to build heap from unsorted array.

Trie (prefix tree): tree where each node represents a character; paths from root spell words.
- Insert/search/delete: O(m) where m = word length.
- Uses: autocomplete, spell checking, IP routing, dictionary.

Segment tree: supports range queries (sum, min, max) and point updates in O(log n).
Fenwick tree (Binary Indexed Tree / BIT): simpler structure for prefix sum queries and updates in O(log n).

## Graphs

A graph G = (V, E) has vertices V and edges E.
- Directed (digraph): edges have direction.
- Undirected: edges have no direction.
- Weighted: edges have costs/weights.
- Sparse: E ≈ V. Dense: E ≈ V².

Representation:
- Adjacency list: array of lists. Space O(V+E). Efficient for sparse graphs.
- Adjacency matrix: V×V grid. Space O(V²). O(1) edge lookup. Efficient for dense graphs.

Graph search algorithms:

BFS (Breadth-First Search):
- Uses a queue. Explores level by level.
- Time: O(V+E). Space: O(V).
- Finds shortest path in unweighted graphs.
- Detects cycles, checks connectivity, bipartiteness.

DFS (Depth-First Search):
- Uses stack (or recursion). Explores as deep as possible first.
- Time: O(V+E). Space: O(V).
- Topological sort, cycle detection, connected components, maze solving.

Topological sort: linear ordering of vertices in a DAG (directed acyclic graph) such that u comes before v for every edge u→v. Kahn's algorithm (BFS) or DFS with finishing times.

Shortest path algorithms:
- Dijkstra's: single-source shortest paths, non-negative weights. O((V+E) log V) with priority queue.
- Bellman-Ford: handles negative weights, detects negative cycles. O(VE).
- Floyd-Warshall: all-pairs shortest paths. O(V³). DP approach.
- A*: heuristic search. Uses f(n)=g(n)+h(n). Optimal with admissible heuristic.

Minimum Spanning Tree (MST): spanning tree with minimum total edge weight.
- Kruskal's: sort edges by weight, add if no cycle (Union-Find). O(E log E).
- Prim's: greedy, grow from one vertex using priority queue. O((V+E) log V).

Union-Find (Disjoint Set Union / DSU):
- find(x): returns root of x's set. Path compression makes this nearly O(1).
- union(x, y): merges two sets. Union by rank.
- Nearly O(1) amortized with both optimizations (inverse Ackermann function α(n)).
- Uses: Kruskal's MST, cycle detection, network connectivity.

## Sorting Algorithms

Comparison sorts — cannot beat O(n log n) in general.

Bubble sort: repeatedly swap adjacent out-of-order elements. O(n²) time, O(1) space. Stable.
Selection sort: find minimum, place at front, repeat. O(n²) time, O(1) space. Not stable.
Insertion sort: insert each element into its correct position. O(n²) worst, O(n) best. O(1) space. Stable. Fast for small/nearly sorted arrays.
Shell sort: generalization of insertion sort with gaps. O(n^(3/2)) typical.

Merge sort: divide in half, sort recursively, merge. O(n log n) always. O(n) space. Stable. Preferred for linked lists.
Quick sort: pick pivot, partition, recurse. O(n log n) average, O(n²) worst. O(log n) space. Not stable. Fast in practice due to cache efficiency. Randomized pivot avoids worst case.
Heap sort: build heap, extract max repeatedly. O(n log n) always. O(1) space. Not stable.
Tim sort: hybrid of merge+insertion sort. O(n log n) worst, O(n) best. Used in Python and Java.

Non-comparison sorts (can beat O(n log n) for specific input types):
Counting sort: count occurrences, reconstruct. O(n+k) where k = range. Stable.
Radix sort: sort digit by digit using counting sort. O(d(n+k)) where d = digits.
Bucket sort: distribute into buckets, sort each. O(n+k) average. Good for uniform distribution.

Stability: a stable sort preserves the relative order of equal elements. Matters when sorting objects by multiple keys.

## Recursion and Dynamic Programming

Recursion: function that calls itself. Must have a base case and make progress toward it.
Call stack depth: O(depth). Stack overflow if too deep. Convert to iteration or use tail-call optimization.

Memoization (top-down DP): cache results of recursive calls to avoid recomputation.
Tabulation (bottom-up DP): fill table iteratively from base cases.

Dynamic programming steps:
1. Identify overlapping subproblems.
2. Define state (what varies between subproblems).
3. Write recurrence relation.
4. Determine base cases.
5. Implement with memoization or table.
6. Optimize space if possible.

Classic DP problems:

Fibonacci: fib(n) = fib(n-1) + fib(n-2). O(n) with memoization vs O(2ⁿ) naive.

0/1 Knapsack: given items with weights and values, maximize value within weight limit.
dp[i][w] = max value using first i items with weight limit w.
dp[i][w] = max(dp[i-1][w], value[i] + dp[i-1][w-weight[i]])

Longest Common Subsequence (LCS): find longest sequence present in both strings.
dp[i][j] = LCS of s1[0..i-1] and s2[0..j-1].
If s1[i-1]==s2[j-1]: dp[i][j] = dp[i-1][j-1] + 1; else dp[i][j] = max(dp[i-1][j], dp[i][j-1]).

Longest Increasing Subsequence (LIS): O(n²) DP or O(n log n) with patience sorting.

Edit distance (Levenshtein): minimum insert/delete/replace to transform s1 to s2.
dp[i][j] = min cost to transform s1[0..i] to s2[0..j].

Coin change: minimum number of coins to make amount. Unbounded knapsack variant.
dp[amount] = min(dp[amount-coin] + 1) for each coin.

Matrix chain multiplication: order of multiplications to minimize operations. O(n³) DP.

## Greedy Algorithms

Greedy: make the locally optimal choice at each step. Works when greedy choice property holds (local optimal leads to global optimal) and problem has optimal substructure.

Examples:
- Activity selection: choose maximum non-overlapping activities. Sort by end time.
- Huffman encoding: build optimal prefix-free code for compression. Min-heap of frequencies.
- Fractional knapsack: take fractions of items sorted by value/weight ratio.
- Dijkstra's shortest path: always extend shortest known path.
- Prim's and Kruskal's MST.
- Interval scheduling, task scheduling with deadlines.

## Divide and Conquer

Split problem into subproblems, solve recursively, combine results.
Recurrence relation: T(n) = aT(n/b) + f(n). Solved using Master Theorem.

Master Theorem: T(n) = aT(n/b) + O(nᵈ):
- d > log_b(a): T(n) = O(nᵈ)
- d = log_b(a): T(n) = O(nᵈ log n)
- d < log_b(a): T(n) = O(n^(log_b a))

Examples:
- Merge sort: T(n) = 2T(n/2) + O(n) → O(n log n)
- Binary search: T(n) = T(n/2) + O(1) → O(log n)
- Karatsuba multiplication: O(n^1.585) vs naive O(n²)
- Strassen matrix multiply: O(n^2.807) vs naive O(n³)
- Closest pair of points: O(n log n)
- Fast Fourier Transform (FFT): O(n log n), used for polynomial multiplication, signal processing.

## Searching Algorithms

Linear search: O(n). Works on unsorted data.
Binary search: O(log n). Requires sorted array. Find mid, compare, recurse on half.

Binary search template:
```
lo, hi = 0, n-1
while lo <= hi:
    mid = (lo + hi) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: lo = mid + 1
    else: hi = mid - 1
```

Binary search on answer: instead of searching in an array, binary search on the answer space.
Example: find minimum capacity to ship packages in D days — binary search on capacity.

Interpolation search: for uniformly distributed sorted data. O(log log n) average.
Exponential search: find range then binary search. Useful for unbounded arrays. O(log n).
Ternary search: find max/min of unimodal function. O(log n).

## String Algorithms

String matching:
- Naive: O(nm) where n=text length, m=pattern length.
- KMP (Knuth-Morris-Pratt): O(n+m) using failure function (prefix table).
- Rabin-Karp: rolling hash. O(n+m) average, O(nm) worst. Good for multiple patterns.
- Boyer-Moore: O(n/m) best case. Most practical for large alphabets.
- Z-algorithm: O(n+m). Builds Z-array: Z[i] = length of longest substring starting at i matching prefix of string.

Aho-Corasick: multi-pattern search. Build trie + failure links. O(n+m+matches).

Suffix array: sorted array of all suffixes. Build in O(n log n), enables O(m log n) pattern search.
Suffix automaton: compact structure for all substrings. O(n) construction, O(n) space.

Longest Palindromic Substring: Manacher's algorithm — O(n).
String hashing: polynomial rolling hash for O(1) substring comparison (after O(n) preprocessing).

## Bit Manipulation

Bit operations: AND (&), OR (|), XOR (^), NOT (~), left shift (<<), right shift (>>).

Useful tricks:
- Check if bit i is set: x & (1 << i)
- Set bit i: x | (1 << i)
- Clear bit i: x & ~(1 << i)
- Toggle bit i: x ^ (1 << i)
- Check if power of 2: x > 0 && (x & (x-1)) == 0
- Get lowest set bit: x & (-x)
- Clear lowest set bit: x & (x-1)
- Count set bits (popcount): Brian Kernighan's algorithm in O(set bits)
- XOR of a^a = 0 (self-inverse). Used to find the single non-duplicate in an array.
- Bitmask DP: represent subsets as integers (2ⁿ subsets for n elements)
- Traveling Salesman Problem (TSP): O(2ⁿ · n²) bitmask DP

## Advanced Data Structures

Segment tree with lazy propagation: range updates and range queries in O(log n).
Sparse table: immutable range minimum/maximum queries in O(1) after O(n log n) preprocessing.
Skip list: probabilistic structure with O(log n) expected search/insert/delete. Alternative to BSTs.
Bloom filter: probabilistic membership test. No false negatives; small false positive rate. O(1) operations, O(m) space.
LRU Cache: Least Recently Used eviction. Implement with doubly linked list + hash map for O(1) all operations.
Treap: BST with heap property on random priorities. Guarantees O(log n) expected.
Rope: binary tree for strings. O(log n) insert/delete/concat. Used in text editors.

## Algorithm Design Paradigms Summary

| Paradigm | When to use | Key insight |
|---|---|---|
| Brute force | Small n, no better algorithm known | Try all possibilities |
| Greedy | Optimal substructure + greedy choice | Local optimal → global optimal |
| Divide & Conquer | Problem splits cleanly, combine is cheap | Split, recurse, merge |
| Dynamic Programming | Overlapping subproblems + optimal substructure | Cache and reuse |
| Backtracking | Constraint satisfaction, explore tree | Try → fail → undo |
| Branch & Bound | Optimization with pruning | Prune suboptimal branches |
| Randomized | Hard worst cases | Add randomness to avoid adversarial input |
| Approximation | NP-hard problems | Good-enough solution in polynomial time |
