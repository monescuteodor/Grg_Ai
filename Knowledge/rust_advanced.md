# Rust Advanced Complete Reference


---

# CHAPTER 1: OWNERSHIP AND BORROWING


## Remarks

Rust is a systems programming language that guarantees memory safety without garbage collection through its ownership system. It achieves the performance of C/C++ with the safety of managed languages. Rust has been voted "most loved programming language" in StackOverflow surveys for 8 consecutive years. Used by Firefox, Cloudflare, Discord, Figma, Dropbox, AWS (Firecracker), and the Linux kernel.

Key concepts: **Ownership** (each value has one owner), **Borrowing** (references without ownership), **Lifetimes** (how long references are valid), **Traits** (interfaces/type classes), **Enums with data** (algebraic data types), **Pattern matching**, **Error handling** (Result/Option, no exceptions), **Async/await** (tokio runtime), **Zero-cost abstractions** (no runtime overhead for high-level features).


## Ownership Rules

```rust
// RULE 1: Each value has exactly ONE owner
// RULE 2: When owner goes out of scope, value is DROPPED (freed)
// RULE 3: Value can be MOVED to new owner (old owner invalid)

fn main() {
    let s1 = String::from("hello");   // s1 owns the String
    let s2 = s1;                       // Ownership MOVED to s2
    // println!("{}", s1);             // ERROR: s1 no longer valid!
    println!("{}", s2);                // OK: s2 owns it now

    // Clone: explicit deep copy (both valid)
    let s3 = s2.clone();
    println!("{} {}", s2, s3);         // Both valid!

    // Copy types (stack-only, cheap to copy): integers, bools, chars, tuples of Copy types
    let x = 5;
    let y = x;                         // COPIED (not moved), both valid
    println!("{} {}", x, y);           // OK

    // Ownership and functions
    let s = String::from("hello");
    takes_ownership(s);                // s moved INTO function
    // println!("{}", s);              // ERROR: s was moved

    let x = 5;
    makes_copy(x);                     // x copied (i32 is Copy)
    println!("{}", x);                 // OK: x still valid
}

fn takes_ownership(s: String) {
    println!("{}", s);
}   // s dropped here (memory freed)

fn makes_copy(x: i32) {
    println!("{}", x);
}   // x goes out of scope, nothing special (Copy type)
```


## Borrowing and References

```rust
// BORROW: reference a value WITHOUT taking ownership
// RULE: At any time, you can have EITHER:
//   - ONE mutable reference (&mut T)
//   - ANY number of immutable references (&T)
//   (but not both simultaneously)

fn main() {
    let s = String::from("hello");

    // Immutable borrow
    let len = calculate_length(&s);    // &s = borrow (no ownership transfer)
    println!("'{}' has length {}", s, len);  // s still valid!

    // Multiple immutable borrows: OK
    let r1 = &s;
    let r2 = &s;
    println!("{} {}", r1, r2);         // OK: multiple immutable refs

    // Mutable borrow
    let mut s = String::from("hello");
    change(&mut s);
    println!("{}", s);                 // "hello, world"

    // CANNOT mix mutable and immutable borrows
    let mut s = String::from("hello");
    let r1 = &s;          // Immutable borrow
    // let r2 = &mut s;   // ERROR: can't borrow as mutable while immutable ref exists
    println!("{}", r1);    // r1's last use
    let r2 = &mut s;       // OK: r1 no longer used (NLL - Non-Lexical Lifetimes)
    r2.push_str("!");
}

fn calculate_length(s: &String) -> usize {   // Borrow, don't own
    s.len()
}   // s goes out of scope, but since it doesn't own the String, nothing is dropped

fn change(s: &mut String) {
    s.push_str(", world");
}

// WHY THIS MATTERS:
// - No data races at compile time (guaranteed!)
// - No dangling pointers (compiler checks lifetimes)
// - No double free (one owner, dropped once)
// - No null pointer (Option<T> instead)
```


## Lifetimes

```rust
// Lifetime: how long a reference is valid
// Usually inferred by compiler, but sometimes must be explicit

// PROBLEM: which input does the return reference point to?
// Compiler can't know → you must annotate
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
// 'a means: returned reference lives as long as the SHORTER of x and y

fn main() {
    let string1 = String::from("long");
    let result;
    {
        let string2 = String::from("hi");
        result = longest(&string1, &string2);
        println!("{}", result);   // OK: string2 still alive
    }
    // println!("{}", result);    // ERROR if result points to string2 (already dropped!)
}

// Lifetime in structs (struct can't outlive its references)
struct Excerpt<'a> {
    text: &'a str,
}

impl<'a> Excerpt<'a> {
    fn level(&self) -> i32 {
        3   // Doesn't return reference → no lifetime annotation needed
    }

    fn announce(&self, announcement: &str) -> &'a str {
        println!("Attention: {}", announcement);
        self.text   // Returns reference with lifetime 'a
    }
}

// LIFETIME ELISION RULES (compiler infers these):
// 1. Each input reference gets its own lifetime parameter
// 2. If exactly one input lifetime → output gets same lifetime
// 3. If &self or &mut self → output gets self's lifetime
// Most of the time, you don't need to write lifetimes!

// 'static lifetime: lives for entire program duration
let s: &'static str = "string literal";   // Embedded in binary
```


---

# CHAPTER 2: TRAITS AND GENERICS


## Traits (Interfaces)

```rust
// Trait: define shared behavior (like interface in Java/Go)

trait Summary {
    fn summarize(&self) -> String;

    // Default implementation (can be overridden)
    fn preview(&self) -> String {
        format!("{}...", &self.summarize()[..50.min(self.summarize().len())])
    }
}

struct Article {
    title: String,
    content: String,
    author: String,
}

impl Summary for Article {
    fn summarize(&self) -> String {
        format!("{} by {}", self.title, self.author)
    }
}

struct Tweet {
    username: String,
    content: String,
}

impl Summary for Tweet {
    fn summarize(&self) -> String {
        format!("@{}: {}", self.username, self.content)
    }
}

// Trait as parameter (static dispatch — monomorphized, zero cost)
fn notify(item: &impl Summary) {
    println!("Breaking: {}", item.summarize());
}

// Trait bound syntax (equivalent, more flexible)
fn notify_bound<T: Summary>(item: &T) {
    println!("Breaking: {}", item.summarize());
}

// Multiple traits
fn display_summary<T: Summary + std::fmt::Display>(item: &T) {
    println!("{}", item);
}

// Where clause (cleaner for complex bounds)
fn complex_function<T, U>(t: &T, u: &U) -> String
where
    T: Summary + Clone,
    U: std::fmt::Display + std::fmt::Debug,
{
    format!("{}: {:?}", t.summarize(), u)
}

// Return trait (one concrete type only)
fn create_summarizable() -> impl Summary {
    Article { title: "...".into(), content: "...".into(), author: "...".into() }
}

// Dynamic dispatch (trait objects — runtime polymorphism, small overhead)
fn print_all(items: &[Box<dyn Summary>]) {
    for item in items {
        println!("{}", item.summarize());
    }
}

// Common standard traits to implement:
// Display:   format with {}
// Debug:     format with {:?}
// Clone:     explicit deep copy (.clone())
// Copy:      implicit bitwise copy (only for simple stack types)
// PartialEq: == comparison
// Eq:        reflexive equality (NaN != NaN, so f64 is PartialEq but not Eq)
// PartialOrd/Ord: comparison/sorting
// Hash:      for HashMap keys
// Default:   default value (Default::default())
// From/Into: type conversion
// Iterator:  for loops

// Derive common traits automatically
#[derive(Debug, Clone, PartialEq, Eq, Hash, Default)]
struct Point {
    x: i32,
    y: i32,
}
```


## Enums and Pattern Matching

```rust
// Rust enums carry DATA (algebraic data types)

enum Message {
    Quit,                           // No data
    Move { x: i32, y: i32 },      // Named fields (like struct)
    Write(String),                  // Single value
    Color(u8, u8, u8),             // Tuple variant
}

impl Message {
    fn process(&self) {
        match self {
            Message::Quit => println!("Quitting"),
            Message::Move { x, y } => println!("Moving to ({}, {})", x, y),
            Message::Write(text) => println!("Writing: {}", text),
            Message::Color(r, g, b) => println!("Color: #{:02x}{:02x}{:02x}", r, g, b),
        }
    }
}

// Option<T> — Rust's null replacement
// enum Option<T> { Some(T), None }

fn find_user(id: u32) -> Option<String> {
    if id == 1 { Some("Alice".to_string()) } else { None }
}

let user = find_user(1);
match user {
    Some(name) => println!("Found: {}", name),
    None => println!("Not found"),
}

// Concise with if let
if let Some(name) = find_user(1) {
    println!("Found: {}", name);
}

// Chaining with map, and_then, unwrap_or
let upper = find_user(1)
    .map(|name| name.to_uppercase())
    .unwrap_or("UNKNOWN".to_string());


// Result<T, E> — error handling without exceptions
// enum Result<T, E> { Ok(T), Err(E) }

use std::fs;
use std::io;

fn read_config() -> Result<String, io::Error> {
    let content = fs::read_to_string("config.toml")?;   // ? = propagate error
    Ok(content)
}

// ? operator: if Err → return early with error. If Ok → unwrap value.
// Equivalent to:
// let content = match fs::read_to_string("config.toml") {
//     Ok(c) => c,
//     Err(e) => return Err(e),
// };

// Custom error types
#[derive(Debug)]
enum AppError {
    IoError(io::Error),
    ParseError(String),
    NotFound(String),
}

impl From<io::Error> for AppError {
    fn from(e: io::Error) -> Self { AppError::IoError(e) }
}

fn load_config() -> Result<Config, AppError> {
    let content = fs::read_to_string("config.toml")?;   // io::Error → AppError via From
    let config = parse_toml(&content)
        .map_err(|e| AppError::ParseError(e.to_string()))?;
    Ok(config)
}

// anyhow (simple error handling for applications)
// use anyhow::{Result, Context};
// fn load() -> Result<Config> {
//     let content = fs::read_to_string("config.toml")
//         .context("Failed to read config")?;
//     Ok(parse(content)?)
// }

// thiserror (for libraries — structured error types)
// #[derive(Debug, thiserror::Error)]
// enum MyError {
//     #[error("IO error: {0}")]
//     Io(#[from] io::Error),
//     #[error("Parse error at line {line}: {message}")]
//     Parse { line: usize, message: String },
// }
```


---

# CHAPTER 3: SMART POINTERS AND COLLECTIONS


## Smart Pointers

```rust
// Box<T>: heap allocation (single owner)
let b = Box::new(5);   // 5 stored on heap, b on stack
// Used for: recursive types, large data, trait objects

// Recursive type (must use Box — compiler needs known size)
enum List {
    Cons(i32, Box<List>),
    Nil,
}
let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));


// Rc<T>: reference-counted (multiple owners, single-threaded)
use std::rc::Rc;
let a = Rc::new(String::from("shared"));
let b = Rc::clone(&a);   // Increment reference count (cheap, no deep copy)
let c = Rc::clone(&a);
println!("Count: {}", Rc::strong_count(&a));   // 3
// Dropped when count reaches 0


// Arc<T>: atomic reference-counted (multiple owners, thread-safe)
use std::sync::Arc;
let data = Arc::new(vec![1, 2, 3]);
let data_clone = Arc::clone(&data);
std::thread::spawn(move || {
    println!("{:?}", data_clone);   // Safe across threads
});


// Mutex<T>: mutual exclusion (shared mutable state between threads)
use std::sync::Mutex;

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    handles.push(std::thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    }));
}

for handle in handles { handle.join().unwrap(); }
println!("Result: {}", *counter.lock().unwrap());   // 10


// RwLock<T>: multiple readers OR one writer
use std::sync::RwLock;
let lock = RwLock::new(vec![1, 2, 3]);

// Multiple readers simultaneously
let r1 = lock.read().unwrap();
let r2 = lock.read().unwrap();

// One writer (exclusive)
let mut w = lock.write().unwrap();
w.push(4);
```


---

# CHAPTER 4: ASYNC RUST


## Async/Await with Tokio

```rust
// Rust async is zero-cost: compiles to state machines, no runtime overhead
// Need a runtime: tokio (most popular), async-std, smol

// Cargo.toml:
// [dependencies]
// tokio = { version = "1", features = ["full"] }
// reqwest = { version = "0.11", features = ["json"] }
// serde = { version = "1", features = ["derive"] }

use tokio;
use reqwest;
use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct User {
    id: u32,
    name: String,
    email: String,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Sequential
    let user1 = fetch_user(1).await?;
    let user2 = fetch_user(2).await?;

    // Concurrent (like Promise.all)
    let (u1, u2, u3) = tokio::join!(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    );

    // Spawn tasks (true concurrency on thread pool)
    let handle = tokio::spawn(async {
        fetch_user(1).await
    });
    let result = handle.await??;

    // Select (first to complete wins, like Promise.race)
    tokio::select! {
        result = fetch_user(1) => println!("User 1: {:?}", result),
        _ = tokio::time::sleep(std::time::Duration::from_secs(5)) => {
            println!("Timeout!");
        }
    }

    Ok(())
}

async fn fetch_user(id: u32) -> Result<User, reqwest::Error> {
    let url = format!("https://jsonplaceholder.typicode.com/users/{}", id);
    let user = reqwest::get(&url).await?.json::<User>().await?;
    Ok(user)
}

// Async channels
use tokio::sync::mpsc;

async fn producer_consumer() {
    let (tx, mut rx) = mpsc::channel(32);

    tokio::spawn(async move {
        for i in 0..10 {
            tx.send(i).await.unwrap();
        }
    });

    while let Some(value) = rx.recv().await {
        println!("Received: {}", value);
    }
}
```


---

# CHAPTER 5: COMMON PITFALLS

```
PITFALL 1: Fighting the borrow checker
  "Compiler won't let me do anything!"
  Fix: learn ownership patterns. Clone when learning, optimize later.

PITFALL 2: Overusing clone()
  .clone() everywhere to avoid borrow errors → performance hit.
  Fix: use references (&T), Rc/Arc for shared ownership, restructure code.

PITFALL 3: String vs &str confusion
  String = owned, heap-allocated, mutable.
  &str = borrowed slice, immutable, can point to String, literal, or slice.
  Fix: accept &str in functions (more flexible), return String when creating.

PITFALL 4: Unwrapping in production
  .unwrap() panics on None/Err → crash in production.
  Fix: use ?, match, unwrap_or, unwrap_or_else, or expect("msg").

PITFALL 5: Not using iterators
  Writing manual loops when iterator chains are cleaner and often faster.
  Fix: learn map, filter, fold, collect, enumerate, zip, chain.

PITFALL 6: Lifetime annotation confusion
  Adding lifetimes randomly until compiler is happy.
  Fix: understand what lifetimes MEAN (returned ref lives as long as input ref).

PITFALL 7: Async function coloring
  Async infects everything — can't easily call async from sync.
  Fix: use block_on at boundaries, or go fully async.

PITFALL 8: Not leveraging the type system
  Using String where enum would be better. Using i32 for IDs.
  Fix: newtype pattern, enums for states, strong typing prevents bugs.

PITFALL 9: Ignoring clippy
  Clippy catches hundreds of common mistakes and anti-patterns.
  Fix: cargo clippy -- -W clippy::all. Fix ALL warnings.

PITFALL 10: Premature optimization
  Writing unsafe code for "performance."
  Fix: safe Rust is already fast. Profile first. unsafe only when proven needed.
```