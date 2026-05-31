# C++ Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH C++


## Remarks

C++ is a general-purpose, compiled, multi-paradigm language extending C with classes, templates, RAII, and the STL. Modern C++ (C++11/14/17/20/23) adds move semantics, lambdas, concepts, coroutines, and ranges.

Tools: GCC (g++), Clang (clang++), MSVC. Build: cmake, make, ninja.


## Hello World

```cpp
#include <iostream>
#include <format>   // C++20

int main() {
    std::cout << "Hello, World!\n";
    std::cout << std::format("Hello, {}!\n", "C++");
    return 0;
}
```

```bash
g++ -std=c++20 -Wall -Wextra -o hello hello.cpp
./hello
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Types and Variables

```cpp
#include <iostream>
#include <string>
#include <cstdint>

// Fundamental types
int         n  = 42;
long long   ll = 9223372036854775807LL;
double      d  = 3.14159265358979;
float       f  = 3.14f;
bool        b  = true;
char        c  = 'A';
std::string s  = "Hello";

// Fixed-width
int32_t  i32 = 2147483647;
uint64_t u64 = 18446744073709551615ULL;

// auto — type inference
auto x      = 42;          // int
auto y      = 3.14;        // double
auto z      = "hello"s;    // std::string (with 's' suffix)

// const and constexpr
const int MAX = 100;
constexpr double PI = 3.14159265358979;
constexpr int square(int n) { return n * n; }

// References
int val = 10;
int& ref = val;   // lvalue reference
ref = 20;         // modifies val

// rvalue reference (move semantics)
int&& rref = 42;

// nullptr
int* ptr = nullptr;

// Structured bindings (C++17)
auto [a, b, c] = std::make_tuple(1, 2.0, "three");
auto& [key, value] = *map.begin();
```

## Strings and Vectors

```cpp
#include <string>
#include <vector>
#include <array>

// string
std::string s = "Hello, World!";
s.length()       // 13
s.size()         // same
s.substr(0, 5)   // "Hello"
s.find("World")  // 7
s.replace(7, 5, "C++")
s.append("!")
s += " more"
s.empty()
s.at(0)          // 'H' (bounds checked)
s[0]             // 'H' (unchecked)

// string_view (non-owning, C++17)
std::string_view sv = s;

// vector
std::vector<int> v = {1, 2, 3, 4, 5};
v.push_back(6);
v.pop_back();
v.insert(v.begin() + 2, 99);
v.erase(v.begin());
v.size()
v.empty()
v.front(); v.back();
v.resize(10);
v.reserve(100);   // pre-allocate

// array (fixed-size)
std::array<int, 5> arr = {1, 2, 3, 4, 5};
arr.size()
arr.at(2)
arr.fill(0)
```


---

# CHAPTER 3: CONTROL FLOW


## Flow Control

```cpp
// if/else (C++17: init statement)
if (int x = getValue(); x > 0) {
    std::cout << "positive\n";
} else {
    std::cout << "non-positive\n";
}

// switch (C++17: init statement)
switch (int x = getValue(); x) {
    case 1: std::cout << "one\n"; break;
    case 2:
    case 3: std::cout << "two or three\n"; break;
    default: std::cout << "other\n";
}

// Range-based for
for (const auto& item : collection) {
    std::cout << item << "\n";
}

// for with index
for (auto [i, val] : std::views::enumerate(vec)) {  // C++23
    std::cout << i << ": " << val << "\n";
}

// while / do-while
while (condition) { /* ... */ }
do { /* ... */ } while (condition);

// Range for with structured binding
std::map<std::string, int> m = {{"a",1},{"b",2}};
for (const auto& [key, val] : m) {
    std::cout << key << "=" << val << "\n";
}
```


---

# CHAPTER 4: FUNCTIONS AND LAMBDAS


## Functions

```cpp
#include <functional>
#include <algorithm>

// Function overloading
int add(int a, int b) { return a + b; }
double add(double a, double b) { return a + b; }

// Default arguments
std::string greet(const std::string& name, const std::string& prefix = "Hello") {
    return prefix + ", " + name + "!";
}

// Template function
template<typename T>
T max_val(T a, T b) { return a > b ? a : b; }

// Variadic template
template<typename... Args>
auto sum(Args... args) { return (args + ...); }   // fold expression

// Lambda
auto square = [](int x) { return x * x; };
auto add_n  = [n = 5](int x) { return x + n; };  // capture by value

// Capture
int offset = 10;
auto add_offset = [offset](int x) { return x + offset; };   // by value
auto modify     = [&offset](int x) { offset += x; };        // by reference
auto move_cap   = [s = std::move(str)]() { return s; };     // move capture

// Generic lambda (C++14)
auto print_any = [](const auto& x) { std::cout << x << "\n"; };

// std::function
std::function<int(int,int)> fn = [](int a, int b) { return a + b; };

// Algorithm + lambda
std::vector<int> nums = {3,1,4,1,5,9,2,6};
std::sort(nums.begin(), nums.end());
std::sort(nums.begin(), nums.end(), std::greater<>());
auto it = std::find_if(nums.begin(), nums.end(), [](int x) { return x > 4; });
std::transform(nums.begin(), nums.end(), nums.begin(), [](int x) { return x*2; });
int total = std::accumulate(nums.begin(), nums.end(), 0);
```


---

# CHAPTER 5: CLASSES AND OOP


## Classes

```cpp
#include <memory>
#include <utility>

class Animal {
private:
    std::string name_;
    std::string sound_;

public:
    // Constructor
    Animal(std::string name, std::string sound)
        : name_(std::move(name)), sound_(std::move(sound)) {}

    // Rule of five (or zero)
    Animal(const Animal&) = default;             // copy constructor
    Animal& operator=(const Animal&) = default;  // copy assignment
    Animal(Animal&&) = default;                  // move constructor
    Animal& operator=(Animal&&) = default;       // move assignment
    virtual ~Animal() = default;                 // virtual destructor

    // Accessors
    const std::string& name() const { return name_; }

    // Virtual method
    virtual std::string speak() const {
        return name_ + " says " + sound_;
    }

    // Operator overload
    bool operator==(const Animal& other) const {
        return name_ == other.name_;
    }

    friend std::ostream& operator<<(std::ostream& os, const Animal& a) {
        return os << "Animal(" << a.name_ << ")";
    }
};

class Dog : public Animal {
    std::string breed_;
public:
    Dog(std::string name, std::string breed)
        : Animal(std::move(name), "Woof"), breed_(std::move(breed)) {}

    std::string speak() const override {
        return Animal::speak() + "!";
    }

    std::string breed() const { return breed_; }
};

// Abstract class (pure virtual)
class Shape {
public:
    virtual double area() const = 0;
    virtual double perimeter() const = 0;
    virtual ~Shape() = default;

    void describe() const {
        std::cout << "Area=" << area() << "\n";
    }
};

// CRTP (Curiously Recurring Template Pattern)
template<typename Derived>
class Printable {
public:
    void print() const {
        std::cout << static_cast<const Derived*>(this)->to_string() << "\n";
    }
};
```


---

# CHAPTER 6: MEMORY MANAGEMENT AND SMART POINTERS


## RAII and Smart Pointers

```cpp
#include <memory>

// unique_ptr — exclusive ownership
auto up = std::make_unique<Dog>("Rex", "Labrador");
up->speak();
// auto up2 = up;   // ERROR: can't copy
auto up3 = std::move(up);  // transfer ownership

// shared_ptr — shared ownership (ref-counted)
auto sp1 = std::make_shared<Dog>("Buddy", "Poodle");
auto sp2 = sp1;   // ref count = 2
sp1.use_count();  // 2

// weak_ptr — non-owning observer
std::weak_ptr<Dog> wp = sp1;
if (auto locked = wp.lock()) {
    locked->speak();
}

// Custom deleter
auto file = std::unique_ptr<FILE, decltype(&fclose)>(
    fopen("file.txt", "r"), fclose
);

// Move semantics
std::string s1 = "hello";
std::string s2 = std::move(s1);  // s1 is now valid but unspecified
s1.empty();  // likely true

// Perfect forwarding
template<typename T, typename... Args>
std::unique_ptr<T> make(Args&&... args) {
    return std::make_unique<T>(std::forward<Args>(args)...);
}

// std::optional
#include <optional>
std::optional<int> maybe_int = 42;
maybe_int.has_value()    // true
maybe_int.value()        // 42
maybe_int.value_or(0)    // 42
maybe_int = std::nullopt;

// std::variant (type-safe union, C++17)
#include <variant>
std::variant<int, double, std::string> v = 42;
std::get<int>(v)         // 42
std::holds_alternative<int>(v)  // true
std::visit([](auto&& arg) { std::cout << arg; }, v);
```


---

# CHAPTER 7: TEMPLATES AND CONCEPTS


## Template Programming

```cpp
// Class template
template<typename T, size_t N>
class Stack {
    std::array<T, N> data_{};
    size_t top_ = 0;
public:
    void push(const T& val) { data_[top_++] = val; }
    T pop() { return data_[--top_]; }
    bool empty() const { return top_ == 0; }
    size_t size() const { return top_; }
};

// Template specialization
template<>
class Stack<bool, 64> { /* bitset-based specialization */ };

// Concepts (C++20)
template<typename T>
concept Numeric = std::is_arithmetic_v<T>;

template<Numeric T>
T add(T a, T b) { return a + b; }

template<typename T>
concept Container = requires(T c) {
    c.begin(); c.end(); c.size();
    typename T::value_type;
};

// Ranges (C++20)
#include <ranges>
auto result = std::views::iota(1, 11)
    | std::views::filter([](int n) { return n % 2 == 0; })
    | std::views::transform([](int n) { return n * n; });

for (int x : result) std::cout << x << " ";  // 4 16 36 64 100
```


---

# CHAPTER 8: STL CONTAINERS AND ALGORITHMS


## Standard Template Library

```cpp
#include <map>
#include <set>
#include <unordered_map>
#include <queue>
#include <stack>
#include <algorithm>
#include <numeric>

// map (sorted)
std::map<std::string, int> m;
m["one"] = 1;
m.insert({"two", 2});
m.emplace("three", 3);
m.count("one")    // 1
m.find("one") != m.end()

// unordered_map (hash, O(1) avg)
std::unordered_map<std::string, int> hm;
hm.reserve(100);

// set / unordered_set
std::set<int> s = {3, 1, 4, 1, 5, 9};
s.insert(2); s.erase(3);
s.count(4)   // 1

// priority_queue
std::priority_queue<int> maxpq;  // max-heap
std::priority_queue<int, std::vector<int>, std::greater<>> minpq;

// Algorithms
std::vector<int> v = {3,1,4,1,5,9,2,6};
std::sort(v.begin(), v.end());
std::reverse(v.begin(), v.end());
std::unique(v.begin(), v.end());
std::binary_search(v.begin(), v.end(), 5);
std::lower_bound(v.begin(), v.end(), 4);
std::max_element(v.begin(), v.end());
std::min_element(v.begin(), v.end());
std::accumulate(v.begin(), v.end(), 0);
std::partial_sum(v.begin(), v.end(), out.begin());
std::count_if(v.begin(), v.end(), [](int x){ return x > 3; });
std::remove_if(v.begin(), v.end(), [](int x){ return x < 3; });
std::copy_if(v.begin(), v.end(), back_inserter(out), pred);
std::for_each(v.begin(), v.end(), [](int& x){ x *= 2; });
```
