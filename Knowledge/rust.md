# Rust Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH RUST


## Remarks

Rust is a systems programming language focused on memory safety, concurrency, and performance — without a garbage collector. Its ownership system, borrow checker, and lifetimes enforce memory safety at compile time.

Tools: `rustc`, `cargo` (build/package manager), `rustup` (toolchain), `clippy` (linter), `rustfmt`.


## Hello World

```rust
// main.rs
fn main() {
    println!("Hello, World!");
    println!("Hello, {}!", "Rust");
    eprintln!("This goes to stderr");
}
```

```bash
cargo new myproject
cd myproject
cargo run
cargo build --release
cargo test
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Types

```rust
fn main() {
    // Immutable by default
    let x = 5;
    // x = 6;  // ERROR: cannot assign twice

    // Mutable
    let mut y = 10;
    y += 1;

    // Type annotations
    let z: i32 = -42;
    let f: f64 = 3.14;
    let b: bool = true;
    let c: char = 'A';

    // Integer types: i8 i16 i32 i64 i128 isize
    //                u8 u16 u32 u64 u128 usize
    let n: u32 = 4_294_967_295;
    let hex: u8 = 0xFF;
    let bin: u8 = 0b1111_0000;

    // Float: f32, f64
    let pi: f64 = 3.141592653589793;

    // Tuple
    let tup: (i32, f64, bool) = (42, 3.14, true);
    let (a, b2, c2) = tup;   // destructure
    println!("{}", tup.0);   // access by index

    // Array (fixed size)
    let arr: [i32; 5] = [1, 2, 3, 4, 5];
    let zeros = [0; 10];     // [0,0,0,0,0,0,0,0,0,0]
    println!("{}", arr[0]);
    println!("{}", arr.len());

    // Shadowing
    let x = 5;
    let x = x + 1;       // new binding (shadows old)
    let x = x * 2;       // 12
    let x = x.to_string(); // different type!

    _ = (x, y, z, f, b, c, n, hex, bin, pi, a, b2, c2);
}
```

## String Types

```rust
// String (heap-allocated, mutable)
let mut s = String::from("hello");
s.push(' ');
s.push_str("world");
s += "!";
let len = s.len();

// &str (string slice, borrowed, immutable)
let s_ref: &str = "hello";   // string literal = &str
let slice: &str = &s[0..5];  // slice of String

// Conversions
let owned: String = "hello".to_string();
let owned2: String = String::from("hello");
let borrowed: &str = &owned;

// Format
let name = "Alice";
let greeting = format!("Hello, {}!", name);

// String methods
s.to_uppercase()
s.to_lowercase()
s.contains("world")
s.starts_with("hello")
s.replace("world", "Rust")
s.split_whitespace().collect::<Vec<_>>()
s.trim()
s.chars().count()
```


---

# CHAPTER 3: OWNERSHIP AND BORROWING


## The Ownership System

```rust
// Ownership rules:
// 1. Each value has exactly one owner
// 2. When owner goes out of scope, value is dropped
// 3. Only one owner at a time

fn main() {
    // Move semantics (heap types)
    let s1 = String::from("hello");
    let s2 = s1;    // s1 is MOVED to s2
    // println!("{}", s1);  // ERROR: s1 moved

    // Clone (deep copy)
    let s3 = String::from("hello");
    let s4 = s3.clone();   // both valid
    println!("{} {}", s3, s4);

    // Copy (stack types: i32, f64, bool, char, tuples of Copy types)
    let x = 5;
    let y = x;   // x is copied, both valid
    println!("{} {}", x, y);

    // Borrowing — references
    let s5 = String::from("hello");
    let len = calculate_length(&s5);  // borrow s5
    println!("{} has length {}", s5, len);  // s5 still valid

    // Mutable reference
    let mut s6 = String::from("hello");
    change(&mut s6);

    // Rules: only ONE mutable reference at a time
    //   OR multiple immutable references (not both)
    let r1 = &s6;
    let r2 = &s6;    // OK: multiple immutable
    println!("{} {}", r1, r2);

    let r3 = &mut s6; // OK: r1, r2 no longer used
    r3.push_str(" world");
}

fn calculate_length(s: &String) -> usize {
    s.len()
}  // s is dropped but NOT the value it refers to

fn change(s: &mut String) {
    s.push_str(", world");
}
```

## Lifetimes

```rust
// Lifetime annotation: 'a
fn longest<'a>(s1: &'a str, s2: &'a str) -> &'a str {
    if s1.len() > s2.len() { s1 } else { s2 }
}

// Struct with lifetime
struct Important<'a> {
    content: &'a str,
}

impl<'a> Important<'a> {
    fn announce(&self) -> &str {
        self.content
    }
}

// 'static lifetime
let s: &'static str = "I live forever";
```


---

# CHAPTER 4: ENUMS AND PATTERN MATCHING


## Enums

```rust
// Basic enum
enum Direction { North, South, East, West }

// Enum with data
#[derive(Debug)]
enum Shape {
    Circle(f64),
    Rectangle(f64, f64),
    Triangle { base: f64, height: f64 },
}

impl Shape {
    fn area(&self) -> f64 {
        match self {
            Shape::Circle(r)              => std::f64::consts::PI * r * r,
            Shape::Rectangle(w, h)        => w * h,
            Shape::Triangle { base, height } => 0.5 * base * height,
        }
    }
}

// Option<T> (no null in Rust)
let maybe: Option<i32> = Some(42);
let nothing: Option<i32> = None;

let val = maybe.unwrap();           // panics if None
let val = maybe.unwrap_or(0);       // default value
let val = maybe.unwrap_or_else(|| compute_default());
let val = maybe.expect("Should have value");

// map, and_then
let doubled = maybe.map(|x| x * 2);  // Some(84)
let chained = maybe.and_then(|x| if x > 0 { Some(x) } else { None });

// if let (single pattern)
if let Some(val) = maybe {
    println!("Got: {}", val);
}

// while let
while let Some(val) = stack.pop() {
    println!("{}", val);
}

// Result<T, E> (error handling)
let result: Result<i32, String> = Ok(42);
let err_result: Result<i32, String> = Err("failed".to_string());

result.unwrap()
result.unwrap_or(0)
result.map(|x| x * 2)
result.map_err(|e| format!("Error: {}", e))

// ? operator (propagate error)
fn parse_and_double(s: &str) -> Result<i32, std::num::ParseIntError> {
    let n = s.parse::<i32>()?;  // returns Err if parse fails
    Ok(n * 2)
}
```


---

# CHAPTER 5: STRUCTS AND TRAITS


## Structs and Traits

```rust
// Struct
#[derive(Debug, Clone, PartialEq)]
struct Point {
    x: f64,
    y: f64,
}

impl Point {
    // Associated function (constructor)
    fn new(x: f64, y: f64) -> Self {
        Point { x, y }
    }

    fn origin() -> Self { Point::new(0.0, 0.0) }

    // Method
    fn distance(&self, other: &Point) -> f64 {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        (dx*dx + dy*dy).sqrt()
    }

    fn translate(&mut self, dx: f64, dy: f64) {
        self.x += dx;
        self.y += dy;
    }
}

// Trait (interface)
trait Animal {
    fn name(&self) -> &str;
    fn sound(&self) -> &str;
    fn speak(&self) -> String {   // default implementation
        format!("{} says {}", self.name(), self.sound())
    }
}

struct Dog { name: String }
impl Animal for Dog {
    fn name(&self) -> &str { &self.name }
    fn sound(&self) -> &str { "Woof" }
}

// Generic function with trait bound
fn make_speak<T: Animal>(animal: &T) {
    println!("{}", animal.speak());
}

// impl Trait (shorthand)
fn make_animal() -> impl Animal {
    Dog { name: "Rex".to_string() }
}

// dyn Trait (dynamic dispatch)
fn speak_any(animal: &dyn Animal) {
    println!("{}", animal.speak());
}

// Common derived traits
#[derive(Debug, Clone, PartialEq, Eq, Hash, PartialOrd, Ord)]
struct Name(String);
```


---

# CHAPTER 6: COLLECTIONS AND ITERATORS


## Vec, HashMap, Iterators

```rust
use std::collections::{HashMap, HashSet, BTreeMap};

// Vec
let mut v: Vec<i32> = Vec::new();
v.push(1); v.push(2); v.push(3);
v.pop();
v.insert(0, 0);
v.remove(1);
v.len(); v.is_empty();
v.contains(&2);
v.sort(); v.dedup();
v.retain(|x| *x > 0);

let v2 = vec![1, 2, 3, 4, 5];
v2[2]          // 3 (panic if out of bounds)
v2.get(10)     // None (safe)

// Slices
let slice: &[i32] = &v2[1..4];

// HashMap
let mut map: HashMap<String, i32> = HashMap::new();
map.insert("one".to_string(), 1);
map.get("one")                    // Option<&i32>
map.contains_key("one")
map.remove("one")
map.entry("two".to_string()).or_insert(2);
map.entry("cnt".to_string()).and_modify(|v| *v += 1).or_insert(1);

// Iterators
let nums = vec![1,2,3,4,5];
let sum: i32 = nums.iter().sum();
let doubled: Vec<i32> = nums.iter().map(|&x| x * 2).collect();
let evens: Vec<&i32> = nums.iter().filter(|&&x| x % 2 == 0).collect();
let total = nums.iter().fold(0, |acc, &x| acc + x);
let any = nums.iter().any(|&x| x > 4);
let all = nums.iter().all(|&x| x > 0);
let first = nums.iter().find(|&&x| x > 3);
let count = nums.iter().filter(|&&x| x % 2 == 0).count();

// Chaining
nums.iter()
    .filter(|&&x| x % 2 == 0)
    .map(|&x| x * x)
    .take(3)
    .collect::<Vec<_>>();

// into_iter vs iter vs iter_mut
for x in nums.iter() { }         // borrow each element
for x in nums.iter_mut() { }     // mutable borrow
for x in nums.into_iter() { }    // consume (move)
```


---

# CHAPTER 7: ERROR HANDLING AND CLOSURES


## Advanced Patterns

```rust
use std::io::{self, Read, Write};
use std::fs::File;

// Custom error type
#[derive(Debug)]
enum AppError {
    Io(io::Error),
    Parse(std::num::ParseIntError),
    Custom(String),
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            AppError::Io(e)     => write!(f, "IO error: {}", e),
            AppError::Parse(e)  => write!(f, "Parse error: {}", e),
            AppError::Custom(s) => write!(f, "Error: {}", s),
        }
    }
}

impl From<io::Error> for AppError {
    fn from(e: io::Error) -> Self { AppError::Io(e) }
}

fn read_file(path: &str) -> Result<String, AppError> {
    let mut f = File::open(path)?;   // io::Error -> AppError via From
    let mut contents = String::new();
    f.read_to_string(&mut contents)?;
    Ok(contents)
}

// Closures
let add = |x: i32, y: i32| x + y;
let double = |x: i32| x * 2;

// Move closure (capture by value)
let msg = String::from("hello");
let print_msg = move || println!("{}", msg);
print_msg();

// Fn / FnMut / FnOnce traits
fn apply<F: Fn(i32) -> i32>(f: F, x: i32) -> i32 { f(x) }
fn apply_once<F: FnOnce() -> String>(f: F) -> String { f() }

// Box<dyn Fn> for dynamic dispatch
let fns: Vec<Box<dyn Fn(i32) -> i32>> = vec![
    Box::new(|x| x + 1),
    Box::new(|x| x * 2),
];
```


---

# CHAPTER 8: CONCURRENCY AND ASYNC


## Threads and Async/Await

```rust
use std::thread;
use std::sync::{Arc, Mutex};

// Thread
let handle = thread::spawn(|| {
    println!("Hello from thread!");
    42
});
let result = handle.join().unwrap();

// Shared state with Arc<Mutex<T>>
let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let c = Arc::clone(&counter);
    handles.push(thread::spawn(move || {
        let mut val = c.lock().unwrap();
        *val += 1;
    }));
}

for h in handles { h.join().unwrap(); }
println!("Counter: {}", *counter.lock().unwrap());

// Channels
use std::sync::mpsc;
let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    tx.send("hello").unwrap();
    tx.send("world").unwrap();
});

for msg in rx { println!("{}", msg); }

// async/await (with tokio)
// Add to Cargo.toml: tokio = { version = "1", features = ["full"] }
use tokio;

#[tokio::main]
async fn main() {
    let result = fetch_data("https://example.com").await;
    println!("{}", result);
}

async fn fetch_data(url: &str) -> String {
    // reqwest::get(url).await.unwrap().text().await.unwrap()
    format!("data from {}", url)
}
```
