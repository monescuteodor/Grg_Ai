# C++ Advanced Complete Reference


---

# CHAPTER 1: MODERN C++ FUNDAMENTALS


## Remarks

C++ is the backbone of high-performance software: game engines (Unreal), browsers (Chrome), databases (MySQL, MongoDB), operating systems (Windows, Linux kernel modules), and embedded systems. Modern C++ (C++11 through C++23) is dramatically different from old C++ — smart pointers replace raw `new/delete`, move semantics eliminate unnecessary copies, and templates enable zero-cost abstractions. Understanding modern C++ makes you a fundamentally better systems programmer.

Key concepts: **RAII** (Resource Acquisition Is Initialization), **Smart pointers** (unique_ptr, shared_ptr), **Move semantics** (rvalue references, std::move), **Templates** (generic programming), **STL** (containers, algorithms, iterators), **Constexpr** (compile-time computation), **Lambda expressions**, **Concurrency** (threads, mutexes, atomics).


## Smart Pointers

```cpp
#include <memory>
#include <iostream>

// RAW POINTER (OLD, DANGEROUS)
void old_style() {
    int* p = new int(42);
    // ... if exception here, memory LEAKS
    delete p;  // Must remember to delete!
}

// UNIQUE_PTR: single owner, auto-deletes
void modern_unique() {
    auto p = std::make_unique<int>(42);
    std::cout << *p << std::endl;  // 42
    // Auto-deleted when p goes out of scope. No leak possible!

    // Transfer ownership
    auto p2 = std::move(p);  // p is now nullptr, p2 owns it
}

// SHARED_PTR: multiple owners, reference counted
void modern_shared() {
    auto p1 = std::make_shared<std::string>("hello");
    {
        auto p2 = p1;  // Reference count: 2
        std::cout << p2->size() << std::endl;
    }  // p2 destroyed, ref count: 1
    // p1 still valid
}  // p1 destroyed, ref count: 0, string freed

// RULE: never use new/delete in modern C++
// unique_ptr for single ownership (99% of cases)
// shared_ptr for shared ownership (graphs, caches)
// weak_ptr to break reference cycles in shared_ptr


// RAII: Resource Acquisition Is Initialization
// Constructor acquires → Destructor releases → Exception-safe
class FileHandle {
    FILE* fp;
public:
    FileHandle(const char* path) : fp(fopen(path, "r")) {
        if (!fp) throw std::runtime_error("Cannot open file");
    }
    ~FileHandle() { if (fp) fclose(fp); }  // Always closes!

    // Delete copy (prevent double-close)
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    // Allow move
    FileHandle(FileHandle&& other) noexcept : fp(other.fp) {
        other.fp = nullptr;
    }
};
```


## Move Semantics

```cpp
#include <vector>
#include <string>
#include <utility>

// PROBLEM: returning large objects copies everything
std::vector<int> make_vector_old() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    return v;  // Copy all elements? SLOW for large vectors
}

// SOLUTION: Move semantics — steal the guts, leave empty shell
// The vector's internal pointer is transferred, not copied.
// v's data is "moved" to the caller. Zero copies!

// std::move = cast to rvalue reference = "I'm done with this, take it"
void move_example() {
    std::string a = "hello world";
    std::string b = std::move(a);  // a's data moved to b
    // a is now EMPTY (valid but unspecified state)
    // b is "hello world"
    // No copy happened — just pointer swap!
}

// Move constructor and move assignment
class Buffer {
    int* data;
    size_t size;
public:
    Buffer(size_t n) : data(new int[n]), size(n) {}
    ~Buffer() { delete[] data; }

    // Move constructor: steal resources
    Buffer(Buffer&& other) noexcept
        : data(other.data), size(other.size) {
        other.data = nullptr;  // Leave source empty
        other.size = 0;
    }

    // Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }
};

// WHEN MOVE HAPPENS AUTOMATICALLY:
// 1. Returning local variables (Return Value Optimization)
// 2. Passing temporaries to functions
// 3. Using std::move() explicitly
// 4. STL containers (push_back with rvalue, swap, etc.)
```


## Templates

```cpp
// Function template
template<typename T>
T max_val(T a, T b) {
    return (a > b) ? a : b;
}

max_val(3, 7);        // int
max_val(3.14, 2.71);  // double
max_val('a', 'z');    // char
// Compiler generates separate functions for each type (zero runtime cost!)

// Class template
template<typename T>
class Stack {
    std::vector<T> data;
public:
    void push(const T& val) { data.push_back(val); }
    void push(T&& val) { data.push_back(std::move(val)); }  // Move version
    T pop() {
        T val = std::move(data.back());
        data.pop_back();
        return val;
    }
    bool empty() const { return data.empty(); }
    size_t size() const { return data.size(); }
};

Stack<int> ints;
Stack<std::string> strings;

// Variadic templates (any number of arguments)
template<typename... Args>
void print_all(Args&&... args) {
    (std::cout << ... << args) << std::endl;  // C++17 fold expression
}
print_all(1, " hello ", 3.14, " world");

// Concepts (C++20): constrain template parameters
template<typename T>
concept Numeric = std::is_arithmetic_v<T>;

template<Numeric T>
T add(T a, T b) { return a + b; }

add(1, 2);        // OK
add(1.0, 2.0);    // OK
// add("a", "b"); // ERROR: string is not Numeric
```


## Lambda Expressions

```cpp
#include <algorithm>
#include <vector>

// Lambda = anonymous function
auto greet = [](const std::string& name) {
    std::cout << "Hello, " << name << std::endl;
};
greet("Alice");

// Captures: access variables from enclosing scope
int threshold = 10;
auto is_above = [threshold](int x) { return x > threshold; };
// [=]  capture all by value
// [&]  capture all by reference
// [x]  capture x by value
// [&x] capture x by reference

// With STL algorithms
std::vector<int> nums = {5, 2, 8, 1, 9, 3, 7};

std::sort(nums.begin(), nums.end());  // Ascending
std::sort(nums.begin(), nums.end(), [](int a, int b) { return a > b; });  // Descending

auto it = std::find_if(nums.begin(), nums.end(),
    [](int x) { return x > 5; });

int count = std::count_if(nums.begin(), nums.end(),
    [threshold](int x) { return x > threshold; });

// Transform
std::vector<int> squared;
std::transform(nums.begin(), nums.end(), std::back_inserter(squared),
    [](int x) { return x * x; });

// Generic lambda (C++14)
auto add = [](auto a, auto b) { return a + b; };
add(1, 2);      // int
add(1.5, 2.5);  // double
```


---

# CHAPTER 2: STL CONTAINERS AND ALGORITHMS


## Containers

```cpp
#include <vector>
#include <array>
#include <map>
#include <unordered_map>
#include <set>
#include <queue>
#include <stack>
#include <deque>
#include <string>

// SEQUENCE CONTAINERS
std::vector<int> v = {1, 2, 3};        // Dynamic array (most used!)
v.push_back(4);                         // Add to end: O(1) amortized
v[0];                                   // Access by index: O(1)
v.size();                               // Number of elements
v.reserve(1000);                        // Pre-allocate capacity

std::array<int, 5> a = {1, 2, 3, 4, 5}; // Fixed-size array (stack)
std::deque<int> d;                       // Double-ended queue
d.push_front(1);                         // O(1) front insert
d.push_back(2);                          // O(1) back insert

// ASSOCIATIVE CONTAINERS
std::map<std::string, int> m;           // Sorted key-value (red-black tree)
m["alice"] = 30;                         // Insert/update: O(log n)
m.count("alice");                        // Check existence: O(log n)

std::unordered_map<std::string, int> um; // Hash map (FAST!)
um["bob"] = 25;                          // Insert/update: O(1) average
um.count("bob");                         // Check existence: O(1)
// Use unordered_map for 99% of cases (faster than map)

std::set<int> s = {3, 1, 4, 1, 5};     // Sorted unique values
// s = {1, 3, 4, 5} (duplicates removed, sorted)

std::unordered_set<int> us;             // Hash set (O(1) lookup)

// ADAPTERS
std::stack<int> stk;                    // LIFO (uses deque internally)
stk.push(1); stk.top(); stk.pop();

std::queue<int> q;                      // FIFO
q.push(1); q.front(); q.pop();

std::priority_queue<int> pq;            // Max-heap
pq.push(3); pq.push(1); pq.push(4);
pq.top();  // 4 (largest)
pq.pop();  // removes 4

// WHEN TO USE WHAT:
// Random access, iterate    → vector (95% of the time)
// Key-value lookup          → unordered_map (hash map)
// Sorted key-value          → map (tree)
// Unique elements           → unordered_set
// FIFO queue                → queue or deque
// LIFO stack                → stack
// Priority queue/heap       → priority_queue
```


## Algorithms

```cpp
#include <algorithm>
#include <numeric>
#include <vector>

std::vector<int> v = {5, 2, 8, 1, 9, 3, 7, 4, 6};

// SORTING
std::sort(v.begin(), v.end());                    // Ascending
std::sort(v.begin(), v.end(), std::greater<>());  // Descending
std::stable_sort(v.begin(), v.end());             // Preserves order of equal elements
std::partial_sort(v.begin(), v.begin()+3, v.end()); // Sort only first 3

// SEARCHING
bool found = std::binary_search(v.begin(), v.end(), 5);  // Requires sorted!
auto it = std::lower_bound(v.begin(), v.end(), 5);       // First >= 5
auto it = std::find(v.begin(), v.end(), 5);               // Linear search

// COUNTING
int n = std::count(v.begin(), v.end(), 5);
int n = std::count_if(v.begin(), v.end(), [](int x) { return x > 5; });

// MIN/MAX
auto [mn, mx] = std::minmax_element(v.begin(), v.end());

// ACCUMULATE
int sum = std::accumulate(v.begin(), v.end(), 0);
int product = std::accumulate(v.begin(), v.end(), 1, std::multiplies<>());

// TRANSFORM (map)
std::vector<int> result;
std::transform(v.begin(), v.end(), std::back_inserter(result),
    [](int x) { return x * 2; });

// REMOVE-ERASE idiom
v.erase(std::remove_if(v.begin(), v.end(),
    [](int x) { return x < 3; }), v.end());

// C++20 RANGES (cleaner syntax)
// #include <ranges>
// auto result = v | std::views::filter([](int x) { return x > 3; })
//                 | std::views::transform([](int x) { return x * 2; });
```


---

# CHAPTER 3: CONCURRENCY


## Threads and Mutexes

```cpp
#include <thread>
#include <mutex>
#include <atomic>
#include <future>

// Basic thread
void worker(int id) {
    std::cout << "Thread " << id << " running\n";
}

int main() {
    std::thread t1(worker, 1);
    std::thread t2(worker, 2);
    t1.join();  // Wait for t1 to finish
    t2.join();

    // Lambda thread
    std::thread t3([]() {
        std::cout << "Lambda thread\n";
    });
    t3.join();
}

// MUTEX: protect shared data
std::mutex mtx;
int shared_counter = 0;

void increment(int n) {
    for (int i = 0; i < n; i++) {
        std::lock_guard<std::mutex> lock(mtx);  // RAII lock
        shared_counter++;
    }  // lock released automatically
}

// ATOMIC: lock-free thread-safe operations
std::atomic<int> atomic_counter{0};

void atomic_increment(int n) {
    for (int i = 0; i < n; i++) {
        atomic_counter.fetch_add(1);  // No mutex needed!
    }
}

// ASYNC/FUTURE: return values from threads
std::future<int> fut = std::async(std::launch::async, []() {
    // Heavy computation in background
    return 42;
});
int result = fut.get();  // Blocks until ready, returns 42

// CONDITION VARIABLE: producer-consumer
std::mutex m;
std::condition_variable cv;
std::queue<int> data_queue;
bool done = false;

void producer() {
    for (int i = 0; i < 10; i++) {
        {
            std::lock_guard lock(m);
            data_queue.push(i);
        }
        cv.notify_one();
    }
    { std::lock_guard lock(m); done = true; }
    cv.notify_all();
}

void consumer() {
    while (true) {
        std::unique_lock lock(m);
        cv.wait(lock, [] { return !data_queue.empty() || done; });
        while (!data_queue.empty()) {
            int val = data_queue.front();
            data_queue.pop();
            lock.unlock();
            process(val);
            lock.lock();
        }
        if (done) break;
    }
}
```


---

# CHAPTER 4: COMMON PITFALLS


## C++ Pitfalls

```
PITFALL 1: Using new/delete instead of smart pointers
  Memory leaks, double free, dangling pointers.
  Fix: std::make_unique, std::make_shared. Never write new/delete.

PITFALL 2: Returning reference to local variable
  int& bad() { int x = 5; return x; }  // Dangling reference!
  Fix: return by value. Move semantics makes it efficient.

PITFALL 3: Iterator invalidation
  Modifying a vector while iterating → undefined behavior.
  Fix: use erase-remove idiom, or iterate backwards.

PITFALL 4: Not using const
  Passing large objects by value when you only read them.
  Fix: const reference: void f(const std::string& s)

PITFALL 5: Slicing
  Assigning derived class to base class variable → loses derived data.
  Fix: use pointers or references for polymorphism.

PITFALL 6: Undefined behavior
  Integer overflow, null dereference, out-of-bounds access.
  Fix: use sanitizers: -fsanitize=address,undefined

PITFALL 7: Not using override keyword
  Virtual function signature mismatch → creates new function instead of overriding.
  Fix: always use override keyword.

PITFALL 8: Forgetting virtual destructor
  Base class pointer to derived → delete doesn't call derived destructor.
  Fix: virtual ~Base() = default;

PITFALL 9: std::endl instead of '\n'
  std::endl flushes buffer every time → 10x slower for output.
  Fix: use '\n' for newlines, std::endl only when flush needed.

PITFALL 10: Not using move semantics
  Copying large objects unnecessarily.
  Fix: std::move for transfers, return by value (compiler optimizes).
```