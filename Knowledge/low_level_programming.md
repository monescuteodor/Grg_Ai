# Low-Level Programming Complete Reference


---

# CHAPTER 1: MEMORY FUNDAMENTALS


## Remarks

Low-level programming means understanding how computers actually work beneath high-level abstractions. Knowing memory layout, pointer arithmetic, CPU caches, and bit manipulation makes you a fundamentally better programmer — even in Python or JavaScript. Performance-critical code (games, databases, OS kernels, embedded systems, ML inference) demands this knowledge. Languages like C, C++, Rust, and Zig operate at this level.

Key concepts: **Stack vs Heap** (two memory regions), **Pointers** (memory addresses), **Cache hierarchy** (L1/L2/L3), **Memory alignment** (CPU access patterns), **Endianness** (byte order), **Bit manipulation** (flags, masks, shifts), **Value vs Reference semantics** (copy vs share), **ABI** (Application Binary Interface), **Calling conventions** (how functions receive arguments).


## Stack vs Heap

```c
// STACK: automatic, fast, limited, LIFO
// - Function local variables
// - Function parameters
// - Return addresses
// - Fixed size per thread (1-8 MB default)
// - Allocation = move stack pointer (1 CPU instruction!)
// - Deallocation = automatic on function return

void example() {
    int x = 42;              // Stack: 4 bytes
    char name[100];           // Stack: 100 bytes
    double coords[3];         // Stack: 24 bytes
    // All freed automatically when function returns
}

// HEAP: manual/GC, slower, large, random access
// - Dynamic allocation (malloc/new/Box)
// - Persists beyond function scope
// - Must be explicitly freed (C/C++) or garbage collected
// - Allocation = find free block (complex algorithm)
// - Fragmentation over time

void example2() {
    int *arr = malloc(1000 * sizeof(int));  // Heap: 4000 bytes
    // ... use arr ...
    free(arr);               // Must free! Or memory leak.
}

// WHY IT MATTERS:
//
// Stack allocation:  ~1 nanosecond (move pointer)
// Heap allocation:   ~100-1000 nanoseconds (find free block, bookkeeping)
//
// Stack is 100-1000x FASTER for allocation.
// Use stack when possible. Heap when you need:
//   - Dynamic size (unknown at compile time)
//   - Data that outlives function
//   - Large allocations (stack is limited)
//   - Shared ownership (multiple references)
```


## Memory Layout in Detail

```
PROCESS MEMORY (from low to high addresses):

┌─────────────────────────────────┐  0xFFFFFFFF (high)
│         Kernel Space            │  Not accessible
├─────────────────────────────────┤
│         Stack                   │  Grows ↓
│         (thread 1)              │  Local vars, return addresses
│              ↓                  │
│                                 │
│              ↑                  │
│         Heap                    │  Grows ↑
│                                 │  malloc/new allocations
├─────────────────────────────────┤
│         BSS                     │  Uninitialized globals (zeroed)
├─────────────────────────────────┤
│         Data                    │  Initialized globals
├─────────────────────────────────┤
│         Text (Code)             │  Machine instructions (read-only)
└─────────────────────────────────┘  0x00000000 (low)

STACK FRAME (per function call):
┌─────────────────────────┐  High address
│   Function arguments    │  Passed by caller
├─────────────────────────┤
│   Return address        │  Where to go after function returns
├─────────────────────────┤
│   Saved frame pointer   │  Previous function's base pointer
├─────────────────────────┤  ← Frame pointer (EBP/RBP)
│   Local variables       │  This function's locals
│   Saved registers       │  Preserved registers
└─────────────────────────┘  ← Stack pointer (ESP/RSP)

// Stack overflow = stack grows into heap or guard page
// Typical cause: infinite recursion, very large local arrays
```


## Pointers

```c
// Pointer = variable that stores a MEMORY ADDRESS

int x = 42;
int *p = &x;       // p holds the ADDRESS of x

printf("%d\n", x);    // 42 (value)
printf("%p\n", &x);   // 0x7ffd5e8a3b2c (address of x)
printf("%p\n", p);     // 0x7ffd5e8a3b2c (same address, stored in p)
printf("%d\n", *p);    // 42 (dereference: read value AT the address)

*p = 100;              // Write to address → changes x!
printf("%d\n", x);     // 100

// POINTER ARITHMETIC
int arr[5] = {10, 20, 30, 40, 50};
int *ptr = arr;        // Points to first element

printf("%d\n", *ptr);       // 10 (arr[0])
printf("%d\n", *(ptr + 1)); // 20 (arr[1])
printf("%d\n", *(ptr + 2)); // 30 (arr[2])
// ptr + 1 advances by sizeof(int) = 4 bytes

// NULL POINTER
int *np = NULL;
// *np = 5;   // SEGFAULT! Accessing address 0.

// DANGLING POINTER
int *create() {
    int local = 42;
    return &local;     // DANGER: local destroyed after return!
}
int *dangling = create();
// *dangling is UNDEFINED BEHAVIOR — might work, might crash, might corrupt data

// VOID POINTER (generic pointer, no type info)
void *generic = malloc(100);
int *typed = (int *)generic;   // Cast to specific type

// POINTER TO POINTER
int x = 5;
int *p = &x;
int **pp = &p;
printf("%d\n", **pp);   // 5 (double dereference)

// FUNCTION POINTERS
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

int (*op)(int, int);    // Declare function pointer
op = add;
printf("%d\n", op(3, 4));   // 7
op = sub;
printf("%d\n", op(3, 4));   // -1
// Used for: callbacks, strategy pattern in C, vtables
```


## Value vs Reference Semantics

```python
# VALUE SEMANTICS: copy data, independent
a = 42
b = a        # b gets a COPY of 42
b = 100      # a is still 42

# In C: structs are copied by value by default
# struct Point p1 = {1, 2};
# struct Point p2 = p1;   // Deep copy
# p2.x = 99;              // p1.x still 1

# REFERENCE SEMANTICS: share data via reference/pointer
a = [1, 2, 3]
b = a        # b points to SAME list object
b.append(4)  # a is now [1, 2, 3, 4] too!

# To get a copy:
b = a.copy()       # Shallow copy
b = a[:]           # Shallow copy (slice)
import copy
b = copy.deepcopy(a)  # Deep copy (nested objects too)

# LANGUAGES:
# Value by default:   C (primitives, structs), Rust, Go (structs), Swift
# Reference by default: Python (objects), JavaScript (objects), Java (objects)
# Configurable:       C++ (value default, & for reference, * for pointer)

# Rust: explicit ownership + borrowing
# let s1 = String::from("hello");
# let s2 = s1;          // s1 is MOVED to s2 (s1 no longer valid!)
# let s3 = s2.clone();  // Explicit deep copy
```


---

# CHAPTER 2: CPU CACHE


## Cache Hierarchy

```
CPU REGISTER:    ~0.5 ns    ~1 KB      Fastest, smallest
L1 CACHE:        ~1 ns      32-64 KB   Per-core, split I/D
L2 CACHE:        ~4 ns      256-512 KB Per-core
L3 CACHE:        ~12 ns     4-64 MB    Shared across cores
RAM:             ~100 ns    8-128 GB   Main memory
SSD:             ~100 μs    256 GB-4 TB  100,000x slower than RAM
HDD:             ~10 ms     1-20 TB    10,000,000x slower than RAM

// L1 cache hit: 1 cycle (~0.3 ns at 3 GHz)
// RAM access:   ~300 cycles
// Cache miss is 300x SLOWER than cache hit!

CACHE LINE:
  CPU doesn't fetch single bytes — it fetches CACHE LINES (64 bytes).
  Access 1 byte → entire 64-byte line loaded into cache.
  
  CONSEQUENCE: accessing sequential memory is FAST (next bytes already in cache).
  Random access is SLOW (new cache line for each access).
```


## Cache-Friendly Code

```c
// EXAMPLE: Row-major vs Column-major array traversal
#define N 10000

int matrix[N][N];

// FAST: row-major traversal (sequential in memory)
// C arrays are row-major: matrix[0][0], matrix[0][1], ..., matrix[1][0], ...
long sum = 0;
for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++)
        sum += matrix[i][j];    // Sequential: cache-friendly

// SLOW: column-major traversal (jumping N*4 bytes each access)
long sum = 0;
for (int j = 0; j < N; j++)
    for (int i = 0; i < N; i++)
        sum += matrix[i][j];    // Stride N: cache-unfriendly

// Speed difference: 5-10x on large matrices!


// ARRAY OF STRUCTS vs STRUCT OF ARRAYS

// Array of Structs (AoS) — poor cache usage for single-field access
struct Particle {
    float x, y, z;         // 12 bytes
    float vx, vy, vz;      // 12 bytes
    float mass;             // 4 bytes
    int type;               // 4 bytes
};                          // 32 bytes total
struct Particle particles[10000];

// To process only positions: load 32 bytes per particle, use only 12.
// 62.5% of cache line wasted!

// Struct of Arrays (SoA) — excellent cache usage for single-field access
struct Particles {
    float x[10000];
    float y[10000];
    float z[10000];
    float vx[10000];
    float vy[10000];
    float vz[10000];
    float mass[10000];
    int type[10000];
};

// To process only positions: x[], y[], z[] are contiguous.
// Every byte in cache line is useful!
// Also enables SIMD vectorization.


// LINKED LIST vs ARRAY
// Array: sequential memory → cache-friendly → FAST iteration
// Linked list: nodes scattered in heap → cache-unfriendly → SLOW iteration
// This is why ArrayList beats LinkedList in practice for almost everything.
```


## False Sharing

```c
// FALSE SHARING: two threads access DIFFERENT variables
// that happen to be on the SAME cache line.
// Each write invalidates the other core's cache → performance disaster.

// BAD:
struct Counters {
    long counter_a;    // Thread A uses this
    long counter_b;    // Thread B uses this
};
// Both on same 64-byte cache line!
// Thread A writes counter_a → invalidates Thread B's cache line
// Thread B writes counter_b → invalidates Thread A's cache line
// "Ping-pong" between caches. 10-100x slower!

// FIX: Padding to separate cache lines
struct Counters {
    long counter_a;
    char padding[56];  // 64 - 8 = 56 bytes padding
    long counter_b;    // Now on different cache line
};

// C11: _Alignas(64) long counter_a;
// Rust: #[repr(align(64))]
// Java: @Contended annotation
```


---

# CHAPTER 3: BIT MANIPULATION


## Bitwise Operators

```python
# AND (&): both bits 1 → 1
0b1100 & 0b1010    # 0b1000 (8)

# OR (|): either bit 1 → 1
0b1100 | 0b1010    # 0b1110 (14)

# XOR (^): bits differ → 1
0b1100 ^ 0b1010    # 0b0110 (6)

# NOT (~): flip all bits
~0b1100            # ...0011 (inverted, two's complement)

# LEFT SHIFT (<<): multiply by 2^n
5 << 1     # 10 (5 × 2)
5 << 3     # 40 (5 × 8)
1 << n     # 2^n

# RIGHT SHIFT (>>): divide by 2^n (integer division)
20 >> 1    # 10 (20 / 2)
20 >> 2    # 5  (20 / 4)
```


## Common Bit Tricks

```python
# Check if number is even/odd
def is_even(n): return (n & 1) == 0
def is_odd(n):  return (n & 1) == 1

# Check if power of 2
def is_power_of_2(n): return n > 0 and (n & (n - 1)) == 0
# 8 = 1000, 7 = 0111 → 1000 & 0111 = 0000 ✅
# 6 = 0110, 5 = 0101 → 0110 & 0101 = 0100 ❌

# Set bit at position k
def set_bit(n, k): return n | (1 << k)

# Clear bit at position k
def clear_bit(n, k): return n & ~(1 << k)

# Toggle bit at position k
def toggle_bit(n, k): return n ^ (1 << k)

# Check bit at position k
def check_bit(n, k): return bool(n & (1 << k))

# Count set bits (population count)
def popcount(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

# Brian Kernighan's algorithm (faster — skips zeros)
def popcount_fast(n):
    count = 0
    while n:
        n &= n - 1   # Clear lowest set bit
        count += 1
    return count

# Swap without temporary variable
a, b = 5, 3
a ^= b    # a = 5^3 = 6
b ^= a    # b = 3^6 = 5
a ^= b    # a = 6^5 = 3
# Now a=3, b=5 (swapped!)

# Absolute value without branching
def abs_val(n):
    mask = n >> 31           # All 1s if negative, all 0s if positive
    return (n ^ mask) - mask


# BIT FLAGS (compact boolean storage)
READ    = 1 << 0   # 0001 = 1
WRITE   = 1 << 1   # 0010 = 2
EXECUTE = 1 << 2   # 0100 = 4
ADMIN   = 1 << 3   # 1000 = 8

permissions = READ | WRITE        # 0011 = 3
permissions |= EXECUTE            # 0111 = 7 (add execute)
permissions &= ~WRITE             # 0101 = 5 (remove write)
has_read = bool(permissions & READ)  # True
has_write = bool(permissions & WRITE) # False

# Unix file permissions work this way:
# chmod 755 = rwxr-xr-x
# 7 = 111 (rwx owner), 5 = 101 (r-x group), 5 = 101 (r-x others)
```


---

# CHAPTER 4: MEMORY ALIGNMENT AND ENDIANNESS


## Memory Alignment

```c
// CPUs access memory in ALIGNED chunks (2, 4, or 8 bytes).
// Misaligned access: slower (extra read) or crash (some architectures).

// STRUCT PADDING:
struct Bad {
    char a;      // 1 byte  + 3 bytes padding
    int b;       // 4 bytes
    char c;      // 1 byte  + 3 bytes padding
    int d;       // 4 bytes
};               // Total: 16 bytes (only 10 useful!)

struct Good {
    int b;       // 4 bytes (aligned to 4)
    int d;       // 4 bytes
    char a;      // 1 byte
    char c;      // 1 byte  + 2 bytes padding
};               // Total: 12 bytes (10 useful)

// RULE: order fields from largest to smallest to minimize padding.

// Check size and alignment:
printf("Size: %zu\n", sizeof(struct Bad));    // 16
printf("Size: %zu\n", sizeof(struct Good));   // 12

// Python struct module for binary data:
import struct
data = struct.pack('iic', 42, 7, b'A')   # Pack into bytes
values = struct.unpack('iic', data)        # Unpack from bytes
```


## Endianness

```
ENDIANNESS: byte order within multi-byte values.

Example: integer 0x12345678 stored in memory

BIG-ENDIAN (network byte order):
  Address:  0x00  0x01  0x02  0x03
  Value:    0x12  0x34  0x56  0x78
  Most significant byte FIRST.
  Used by: network protocols, Java, big-iron (SPARC, PowerPC)

LITTLE-ENDIAN:
  Address:  0x00  0x01  0x02  0x03
  Value:    0x78  0x56  0x34  0x12
  Least significant byte FIRST.
  Used by: x86, x86-64, ARM (usually), most modern CPUs

WHY IT MATTERS:
  - Network protocols use big-endian (must convert on little-endian CPUs)
  - Binary file formats specify endianness
  - Cross-platform serialization must handle both
```

```python
import sys
print(sys.byteorder)   # 'little' on most modern systems

# Convert between host and network byte order
import socket
network_int = socket.htonl(12345)    # Host to network (big-endian)
host_int = socket.ntohl(network_int) # Network to host

# struct module handles endianness
import struct
big = struct.pack('>I', 12345)       # > = big-endian
little = struct.pack('<I', 12345)    # < = little-endian
native = struct.pack('=I', 12345)    # = = native byte order
```


---

# CHAPTER 5: COMMON PITFALLS


## Low-Level Pitfalls

```
PITFALL 1: Buffer overflow
  Writing past array bounds → overwrite adjacent memory → crash or exploit.
  Fix: bounds checking, safe string functions (strncpy, snprintf), Rust.

PITFALL 2: Use after free
  Access memory after free() → undefined behavior.
  Fix: set pointer to NULL after free. Use RAII (C++), ownership (Rust).

PITFALL 3: Double free
  free() same memory twice → heap corruption.
  Fix: set pointer to NULL after free. Use smart pointers (C++).

PITFALL 4: Memory leak
  malloc without free → memory grows until OOM.
  Fix: pair every malloc with free. Use RAII, GC, or ownership system.

PITFALL 5: Uninitialized memory
  Reading variable before assigning → garbage value.
  Fix: always initialize. Compiler warnings (-Wall -Werror).

PITFALL 6: Stack overflow
  Deep recursion or large local arrays → exceed stack limit.
  Fix: use iteration, allocate large arrays on heap, increase stack size.

PITFALL 7: Integer overflow
  255 + 1 = 0 (uint8). INT_MAX + 1 = INT_MIN (signed → undefined in C!).
  Fix: check before arithmetic, use wider types, compiler sanitizers.

PITFALL 8: Ignoring cache behavior
  Random access patterns → cache misses → 100x slower.
  Fix: sequential access, SoA layout, cache-conscious data structures.

PITFALL 9: False sharing in multithreaded code
  Two threads writing adjacent memory → cache line ping-pong.
  Fix: pad to cache line size (64 bytes), align with compiler directives.

PITFALL 10: Endianness bugs
  Sending binary data between big/little-endian systems.
  Fix: always convert to network byte order for transmission.

PITFALL 11: Struct padding assumptions
  Assuming sizeof(struct) == sum of field sizes → wrong.
  Fix: use sizeof(), or pack structs explicitly (__attribute__((packed))).

PITFALL 12: Pointer arithmetic on void*
  void pointer has no size info → can't do arithmetic portably.
  Fix: cast to typed pointer first, then do arithmetic.

PITFALL 13: Premature optimization
  Optimizing at bit level when algorithm is O(n²).
  Fix: optimize algorithm first (O(n²)→O(n log n)), then micro-optimize.

PITFALL 14: Not profiling
  Guessing where bottleneck is → optimizing wrong thing.
  Fix: profile first (perf, Instruments, VTune), then optimize hot spots.

PITFALL 15: Ignoring compiler optimizations
  Writing "clever" bit tricks that compiler already does.
  Fix: write clear code, enable -O2/-O3, check generated assembly.
  Modern compilers are incredibly smart.
```