# General Programming Concepts Reference


---

# CHAPTER 1: ALGORITHMS AND COMPLEXITY


## Algorithm Analysis

```
=== BIG-O NOTATION ===
Describes how runtime grows with input size n.

O(1)       - Constant time    : array access, hash lookup
O(log n)   - Logarithmic      : binary search, balanced BST ops
O(n)       - Linear           : linear search, single loop
O(n log n) - Linearithmic     : merge sort, heapsort, quicksort (avg)
O(n²)      - Quadratic        : bubble sort, nested loops
O(n³)      - Cubic            : matrix multiply (naive)
O(2ⁿ)      - Exponential      : brute-force subset enumeration
O(n!)      - Factorial        : brute-force TSP, permutations

Space complexity uses same notation for memory usage.

=== MASTER THEOREM ===
For T(n) = aT(n/b) + f(n):
- Case 1: f(n) = O(n^(log_b(a)-ε))  →  T(n) = Θ(n^log_b(a))
- Case 2: f(n) = Θ(n^log_b(a))      →  T(n) = Θ(n^log_b(a) · log n)
- Case 3: f(n) = Ω(n^(log_b(a)+ε))  →  T(n) = Θ(f(n))

Example: Merge sort T(n) = 2T(n/2) + Θ(n)
a=2, b=2, log_2(2)=1, f(n)=Θ(n) → Case 2 → T(n) = Θ(n log n)

=== SORTING ALGORITHMS ===
Algorithm       Best      Average    Worst     Space   Stable
Bubble sort     O(n)      O(n²)      O(n²)     O(1)    Yes
Insertion sort  O(n)      O(n²)      O(n²)     O(1)    Yes
Selection sort  O(n²)     O(n²)      O(n²)     O(1)    No
Merge sort      O(n logn) O(n logn)  O(n logn) O(n)    Yes
Quick sort      O(n logn) O(n logn)  O(n²)     O(logn) No
Heap sort       O(n logn) O(n logn)  O(n logn) O(1)    No
Counting sort   O(n+k)    O(n+k)     O(n+k)    O(k)    Yes
Radix sort      O(nk)     O(nk)      O(nk)     O(n+k)  Yes

=== SEARCH ALGORITHMS ===
Linear search: O(n) time, O(1) space, unsorted
Binary search: O(log n) time, O(1) space, sorted array required
Hash table search: O(1) avg, O(n) worst

=== GRAPH ALGORITHMS ===
BFS (Breadth-First Search): O(V+E), finds shortest path (unweighted)
DFS (Depth-First Search): O(V+E), detects cycles, topological sort
Dijkstra: O((V+E) log V) with min-heap, single-source shortest path (non-negative)
Bellman-Ford: O(VE), handles negative weights, detects negative cycles
Floyd-Warshall: O(V³), all-pairs shortest paths
Prim's/Kruskal's: O(E log V), minimum spanning tree

=== DYNAMIC PROGRAMMING PATTERNS ===
Optimal substructure + overlapping subproblems → use DP
Memoization (top-down): recursive + cache
Tabulation (bottom-up): iterative + table

Classic DP problems:
- Fibonacci, Coin change, Knapsack
- Longest common subsequence (LCS)
- Longest increasing subsequence (LIS)
- Edit distance, Matrix chain multiplication
- Rod cutting, Egg drop, Catalan numbers
```


---

# CHAPTER 2: DATA STRUCTURES


## Core Data Structures

```
=== ARRAYS ===
Random access: O(1)
Insert/delete at end: O(1) amortized (dynamic array)
Insert/delete at middle: O(n)
Search (unsorted): O(n)
Use when: random access needed, cache-friendly, fixed-size known

=== LINKED LIST ===
Access: O(n)
Insert/delete at head: O(1)
Insert/delete at tail: O(1) with tail pointer
Insert/delete in middle: O(n) search + O(1) modify
Use when: frequent insertions/deletions, no random access needed
Singly-linked: simpler, less memory
Doubly-linked: O(1) delete given node pointer

=== STACK (LIFO) ===
Push/pop/peek: O(1)
Use when: DFS, function calls, expression evaluation, undo operations
Implementations: array (stack pointer) or linked list (head)

=== QUEUE (FIFO) ===
Enqueue/dequeue: O(1)
Use when: BFS, scheduling, buffers
Deque (double-ended queue): O(1) both ends
Priority queue: O(log n) insert/extract-min via heap

=== HASH TABLE ===
Insert/delete/search: O(1) average, O(n) worst
Load factor: keep < 0.7 for good performance
Collision resolution: chaining (linked lists) or open addressing (probing)
Use when: fast lookup/insertion, no ordering needed

=== TREES ===
Binary Search Tree (BST):
  - Search/insert/delete: O(log n) avg, O(n) worst (unbalanced)
  
Balanced BSTs (AVL, Red-Black):
  - All operations: O(log n) guaranteed
  
B-Tree / B+ Tree:
  - Used in databases, filesystems
  - O(log n) operations, cache-friendly
  
Heap (Binary Heap):
  - Max/min in O(1)
  - Insert/delete: O(log n)
  - Build heap from array: O(n)
  - Used for priority queues and heapsort
  
Trie:
  - String prefix operations: O(L) where L = string length
  - Space-efficient for shared prefixes

=== GRAPHS ===
Representation:
  Adjacency Matrix: O(V²) space, O(1) edge lookup, dense graphs
  Adjacency List: O(V+E) space, O(degree) neighbor iteration, sparse graphs
  
Types:
  Directed (digraph): edges have direction
  Undirected: edges bidirectional
  Weighted: edges have costs
  DAG (Directed Acyclic Graph): no cycles, enables topological sort
```


---

# CHAPTER 3: DESIGN PATTERNS


## Software Design Patterns

```
=== CREATIONAL PATTERNS ===

Singleton: ensure only one instance
  - private constructor, static getInstance()
  - Use for: logging, config, connection pools
  - Beware: global state, testing difficulty

Factory Method: define interface for creating objects
  - Subclasses decide which class to instantiate
  - Use for: plugin systems, UI widget factories

Abstract Factory: create families of related objects
  - Use for: cross-platform UI (Windows/Mac/Linux)

Builder: construct complex objects step by step
  - Use for: SQL query builders, HTTP request builders
  - Fluent interface: obj.setA(1).setB(2).build()

Prototype: clone existing objects
  - Use for: expensive initialization, object templates

=== STRUCTURAL PATTERNS ===

Adapter: convert interface to another expected
  - Wrapper around incompatible interface
  - Use for: legacy code integration, third-party APIs

Decorator: add behavior dynamically
  - Wraps object, adds functionality
  - Use for: middleware, logging, caching, auth

Facade: simplified interface to complex system
  - Use for: library wrappers, subsystem isolation

Composite: tree structures of objects
  - Uniform treatment of individual/composite
  - Use for: file systems, UI component trees

Proxy: placeholder for another object
  - Lazy loading, access control, caching
  - Use for: remote proxies, virtual proxies

=== BEHAVIORAL PATTERNS ===

Observer (Pub/Sub): notify dependents of state change
  - Subject maintains list of observers
  - Use for: event systems, MVC, reactive programming

Strategy: define family of algorithms, make interchangeable
  - Use for: sorting strategies, payment methods, compression

Command: encapsulate action as object
  - Use for: undo/redo, queued operations, logging

Iterator: access elements sequentially without exposing structure
  - Use for: custom collections

State: object behavior changes based on internal state
  - Use for: FSMs, workflow systems, UI states

Template Method: define algorithm skeleton in base class
  - Steps implemented by subclasses

Chain of Responsibility: pass request along handler chain
  - Use for: middleware pipelines, logging levels

Visitor: add operations to object without modifying them
  - Use for: compiler AST operations, document rendering
```


---

# CHAPTER 4: PRINCIPLES AND PARADIGMS


## Programming Principles

```
=== SOLID PRINCIPLES (OOP) ===

S - Single Responsibility Principle (SRP)
    "A class should have one, and only one, reason to change."
    → Each class/function does exactly one thing

O - Open/Closed Principle (OCP)
    "Open for extension, closed for modification."
    → Add new behavior via new code, not changing existing

L - Liskov Substitution Principle (LSP)
    "Subclasses must be substitutable for their base classes."
    → If S extends T, code using T should work with S

I - Interface Segregation Principle (ISP)
    "Clients should not be forced to depend on interfaces they don't use."
    → Many specific interfaces > one general interface

D - Dependency Inversion Principle (DIP)
    "Depend on abstractions, not concretions."
    → High-level modules should not depend on low-level modules

=== OTHER PRINCIPLES ===

DRY - Don't Repeat Yourself
    "Every piece of knowledge must have a single, unambiguous representation."
    → Extract repeated code into functions/modules

KISS - Keep It Simple, Stupid
    "Simplicity should be a key design goal."
    → Avoid unnecessary complexity

YAGNI - You Aren't Gonna Need It
    "Don't add functionality until it's needed."
    → Don't over-engineer

Law of Demeter (LoD)
    "Talk only to your immediate friends."
    → object.getA().getB().getC() is a smell
    → Better: object.doWhatINeed()

Composition over Inheritance
    "Favor object composition over class inheritance."
    → More flexible, avoids fragile base class problem

=== PROGRAMMING PARADIGMS ===

Imperative: step-by-step instructions (C, assembly)
Procedural: organize into procedures/functions (C)
Object-Oriented: data + behavior in objects (Java, C++)
Functional: computation as function evaluation, pure (Haskell, Clojure)
Declarative: what, not how (SQL, HTML, Prolog)
Reactive: data flows and propagation (RxJS, Redux)
Logic: express facts and rules (Prolog, Mercury)
Event-Driven: respond to events (JavaScript DOM, GUI)
Concurrent: multiple computations simultaneously (Go, Erlang)
```


---

# CHAPTER 5: CONCURRENCY AND PARALLELISM


## Concurrent Programming Concepts

```
=== CONCURRENCY VS PARALLELISM ===
Concurrency: multiple tasks making progress (may interleave on 1 CPU)
Parallelism: multiple tasks running simultaneously (multiple CPUs)
"Concurrency is about structure; parallelism is about execution."

=== SYNCHRONIZATION PRIMITIVES ===
Mutex (Mutual Exclusion Lock):
  - Only one thread holds it at a time
  - Use for: shared mutable state
  - Risks: deadlock if not properly ordered

Semaphore:
  - Counter-based, allows N concurrent accesses
  - Binary semaphore = mutex
  - Use for: resource limiting, producer-consumer

Monitor:
  - High-level: mutex + condition variables
  - Java synchronized, Python with statement

Condition Variable:
  - Thread waits until condition is true
  - Used with mutex: wait/signal/broadcast

Atomic Operations:
  - Hardware-guaranteed indivisible operations
  - CAS (Compare-and-Swap): foundation of lock-free algorithms

=== CONCURRENCY MODELS ===
Shared Memory + Locks (C++, Java):
  - Threads share heap memory
  - Synchronize with mutexes, semaphores

Actor Model (Erlang, Akka):
  - Each actor has private state
  - Communicate only via message passing
  - No shared state → no data races

CSP / Channels (Go):
  - "Don't communicate by sharing memory; share memory by communicating."
  - Goroutines + channels

Software Transactional Memory (Clojure, Haskell STM):
  - Atomic transactions on shared state
  - Optimistic concurrency control

Async/Await / Event Loop (JavaScript, Python asyncio):
  - Single-threaded concurrency
  - Non-blocking I/O with callbacks/promises

=== COMMON CONCURRENCY BUGS ===
Race Condition: outcome depends on thread scheduling order
  → Fix: use synchronization

Deadlock: two+ threads wait for each other forever
  → Prevention: lock ordering, timeouts, deadlock detection

Livelock: threads keep changing state but make no progress
  → Fix: randomized retry, priorities

Starvation: thread never gets scheduled
  → Fix: fair scheduling algorithms

Priority Inversion: high-priority task blocked by low-priority
  → Fix: priority inheritance protocols
```


---

# CHAPTER 6: COMPUTER ARCHITECTURE


## Systems and Hardware Concepts

```
=== MEMORY HIERARCHY ===
Registers:      ~0.3 ns,  <1 KB   (CPU registers)
L1 Cache:       ~1 ns,    32 KB   (per core)
L2 Cache:       ~3 ns,    256 KB  (per core)
L3 Cache:       ~10 ns,   8 MB    (shared)
DRAM (RAM):     ~100 ns,  GBs
SSD:            ~100 μs,  TBs
HDD:            ~10 ms,   TBs
Network:        ~1-100 ms

Cache line: typically 64 bytes
Cache-friendly code: access memory sequentially (spatial locality)

=== CACHE PERFORMANCE ===
Cache hit: data found in cache (fast)
Cache miss: data not in cache, fetch from lower level (slow)
False sharing: different data on same cache line, thrashes

=== CPU CONCEPTS ===
Pipelining: overlap instruction stages (fetch/decode/execute/writeback)
Branch prediction: speculative execution of predicted branch
Out-of-order execution: execute instructions when operands ready
SIMD: Single Instruction Multiple Data (SSE, AVX, NEON)
IPC: Instructions Per Cycle (measure of parallelism)

=== MEMORY MODEL ===
Stack: automatic storage, LIFO, function frames
Heap: dynamic allocation, explicit or GC managed
BSS: uninitialized global/static variables
Data: initialized global/static variables
Text: program code (instructions)

Virtual memory: each process has own address space
TLB: Translation Lookaside Buffer (cache for page table)
Page fault: access unmapped memory → OS maps page

=== BIT MANIPULATION ===
x & (x-1)      : clear lowest set bit
x | (x-1)      : set all bits below lowest set bit
x & -x          : isolate lowest set bit
x ^ x           : 0 (clear)
x ^ ~0          : bitwise NOT (~x)
(x >> k) & 1    : test bit k
x | (1 << k)    : set bit k
x & ~(1 << k)   : clear bit k
x ^ (1 << k)    : toggle bit k

Power of 2: (n & (n-1)) == 0 && n > 0
Population count (number of 1s): __builtin_popcount(x)
```


---

# CHAPTER 7: NETWORKING


## Network Protocols and Concepts

```
=== OSI MODEL ===
7. Application:    HTTP, FTP, SMTP, DNS, TLS (user-facing)
6. Presentation:   Encoding, encryption, compression
5. Session:        Session management, RPC
4. Transport:      TCP (reliable), UDP (unreliable), ports
3. Network:        IP, ICMP, routing
2. Data Link:      Ethernet, WiFi (MAC addresses, frames)
1. Physical:       Bits over medium (cables, radio)

TCP/IP model layers: Application / Transport / Internet / Link

=== TCP vs UDP ===
TCP (Transmission Control Protocol):
  - Connection-oriented (3-way handshake: SYN, SYN-ACK, ACK)
  - Reliable: acknowledgments, retransmission
  - Ordered delivery
  - Flow control and congestion control
  - Use for: HTTP, FTP, SMTP, SSH

UDP (User Datagram Protocol):
  - Connectionless
  - No reliability guarantees
  - Lower latency
  - Use for: DNS, video streaming, gaming, VoIP

=== HTTP ===
Methods: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
Status codes:
  1xx Informational: 100 Continue
  2xx Success: 200 OK, 201 Created, 204 No Content
  3xx Redirect: 301 Moved, 302 Found, 304 Not Modified
  4xx Client Error: 400 Bad Request, 401 Unauthorized, 403 Forbidden,
                    404 Not Found, 429 Too Many Requests
  5xx Server Error: 500 Internal Server Error, 503 Service Unavailable

HTTP/2: multiplexing, header compression, server push
HTTP/3: QUIC (UDP-based), reduced latency

=== REST PRINCIPLES ===
1. Stateless: each request self-contained
2. Client-Server: separated concerns
3. Cacheable: responses indicate cacheability
4. Uniform Interface: standard verbs + URIs
5. Layered System: intermediaries OK
6. Code on Demand (optional)

=== IMPORTANT PORTS ===
22   SSH         80   HTTP        443  HTTPS
21   FTP         25   SMTP        110  POP3
143  IMAP        53   DNS         3306 MySQL
5432 PostgreSQL  6379 Redis       27017 MongoDB
```


---

# CHAPTER 8: SECURITY AND TESTING


## Security Principles and Testing

```
=== SECURITY FUNDAMENTALS ===
CIA Triad:
  Confidentiality: data private (encryption)
  Integrity: data unmodified (hashing, signing)
  Availability: system accessible (redundancy)

Authentication: who are you? (password, token, biometric)
Authorization: what can you do? (RBAC, permissions)
Non-repudiation: can't deny actions (audit logs, signatures)

=== COMMON VULNERABILITIES (OWASP Top 10) ===
1. Broken Access Control
2. Cryptographic Failures (store plaintext passwords, weak algo)
3. Injection (SQL injection, command injection, XSS)
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Authentication Failures
8. Data Integrity Failures (CSRF)
9. Logging & Monitoring Failures
10. Server-Side Request Forgery (SSRF)

=== CRYPTOGRAPHY BASICS ===
Symmetric: same key for encrypt/decrypt (AES-256, ChaCha20)
  - Fast, but key distribution problem
Asymmetric: public/private key pair (RSA, ECDSA, Ed25519)
  - Slow, but no key distribution problem
  - Encrypt with public, decrypt with private
  - Sign with private, verify with public
Hash functions: one-way (SHA-256, SHA-3, BLAKE3)
  - Passwords: bcrypt, scrypt, Argon2 (with salt)
MAC: Message Authentication Code (HMAC, Poly1305)
TLS/SSL: combines symmetric + asymmetric for secure channels

=== TESTING TYPES ===
Unit tests: individual functions/classes in isolation
Integration tests: multiple components together
End-to-end (E2E): full user journey through the system
Regression tests: ensure bugs don't reappear
Performance tests: load, stress, soak, spike
Security tests: penetration testing, fuzzing

=== TESTING PRINCIPLES ===
F.I.R.S.T.: Fast, Isolated, Repeatable, Self-validating, Timely
AAA pattern: Arrange → Act → Assert
TDD: Test-Driven Development (Red → Green → Refactor)
BDD: Behavior-Driven Development (Given/When/Then)
Code coverage: lines, branches, paths (aim for ~80%+)
Mocking: replace dependencies with test doubles
  - Mock: verifies interactions
  - Stub: returns canned responses
  - Spy: records calls, uses real implementation
  - Fake: simplified working implementation

=== CODE QUALITY METRICS ===
Cyclomatic complexity: number of linearly independent paths
  < 10 = simple, 10-20 = moderate, > 20 = complex
Coupling: dependencies between modules (lower = better)
Cohesion: how related module's responsibilities are (higher = better)
Technical debt: cost of rework from shortcuts
Code review: pair/team review before merge
Linting: static analysis for style and common errors
```
