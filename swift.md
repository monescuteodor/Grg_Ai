# Swift Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH SWIFT


## Remarks

Swift is Apple's modern, compiled, type-safe language for iOS, macOS, watchOS, tvOS, and server-side development. Swift emphasizes safety (optionals, value types), performance, and expressiveness. Swift 5.9+ is current.

Tools: Xcode, Swift Package Manager (SPM), Swift Playgrounds, swift-format.


## Hello World

```swift
// hello.swift
import Foundation

print("Hello, World!")
print("Hello, \(NSProcessInfo.processInfo.userName)!")

// String interpolation
let name = "Swift"
print("Hello, \(name)!")
```

```bash
swift hello.swift
swift build
swift test
swift package init --type executable
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Types

```swift
// let (immutable) and var (mutable)
let pi = 3.14159
var count = 0
count += 1

// Type annotations
let name: String = "Alice"
var age: Int = 30
let score: Double = 98.5
let flag: Bool = true
let byte: UInt8 = 255
let big: Int64 = 9_223_372_036_854_775_807

// Type inference
let greeting = "Hello"   // String inferred
let num = 42             // Int inferred

// String
let s = "Hello, World!"
s.count           // 13
s.uppercased()
s.lowercased()
s.hasPrefix("Hello")
s.hasSuffix("!")
s.contains("World")
s.replacingOccurrences(of: "World", with: "Swift")
s.split(separator: ",")

// Multi-line string
let multiline = """
    First line
    Second line
    Third line
    """

// String interpolation
let x = 42
let msg = "x = \(x), doubled = \(x * 2)"
```

## Optional Types

```swift
// Optional — value may or may not exist
var maybeInt: Int? = 42
var nothing: String? = nil

// Forced unwrap (dangerous, can crash)
let val = maybeInt!

// Optional binding
if let value = maybeInt {
    print("Got: \(value)")
}

// guard let (early exit)
func process(value: Int?) {
    guard let v = value else {
        print("No value")
        return
    }
    print("Value: \(v)")
}

// Nil coalescing
let result = maybeInt ?? 0

// Optional chaining
let len = str?.count   // Int?
let upper = str?.uppercased()?.prefix(3)

// if let shorthand (Swift 5.7+)
if let maybeInt {   // binds to same name
    print(maybeInt)
}
```


---

# CHAPTER 3: CONTROL FLOW


## Flow Control

```swift
// if/else
if x > 0 {
    print("positive")
} else if x == 0 {
    print("zero")
} else {
    print("negative")
}

// Ternary
let label = x > 0 ? "positive" : "non-positive"

// switch (must be exhaustive)
switch day {
case "Monday", "Tuesday", "Wednesday", "Thursday", "Friday":
    print("Weekday")
case "Saturday", "Sunday":
    print("Weekend")
default:
    print("Unknown")
}

// switch with ranges and where
switch score {
case 90...100:    print("A")
case 80..<90:     print("B")
case let n where n < 60: print("Fail: \(n)")
default:          print("C or D")
}

// for-in
for i in 1...5 { print(i) }
for i in 0..<5 { print(i) }
for item in array { print(item) }
for (index, value) in array.enumerated() {
    print("\(index): \(value)")
}
for (key, value) in dict { print("\(key): \(value)") }

// while / repeat-while (do-while)
var n = 5
while n > 0 { n -= 1 }

repeat {
    print(n)
    n += 1
} while n < 5

// where clause in for
for i in 1...20 where i % 3 == 0 {
    print(i)
}

// defer (cleanup)
defer { print("cleanup") }
```


---

# CHAPTER 4: FUNCTIONS AND CLOSURES


## Functions

```swift
// Basic function
func add(_ a: Int, _ b: Int) -> Int { a + b }

// Argument labels
func greet(name: String, from hometown: String) -> String {
    "Hello \(name) from \(hometown)!"
}
greet(name: "Alice", from: "NYC")

// Default parameters
func connect(host: String, port: Int = 8080) -> String {
    "\(host):\(port)"
}

// Variadic parameters
func sum(_ numbers: Int...) -> Int {
    numbers.reduce(0, +)
}

// inout parameters
func swap(_ a: inout Int, _ b: inout Int) {
    let temp = a; a = b; b = temp
}
swap(&x, &y)

// Multiple return (tuple)
func minMax(of array: [Int]) -> (min: Int, max: Int) {
    (array.min()!, array.max()!)
}
let (min, max) = minMax(of: [3,1,4,1,5,9])

// Throwing functions
enum AppError: Error { case invalid, notFound }

func parse(_ s: String) throws -> Int {
    guard let n = Int(s) else { throw AppError.invalid }
    return n
}

do {
    let n = try parse("42")
    print(n)
} catch AppError.invalid {
    print("Invalid input")
} catch {
    print("Error: \(error)")
}

// Closures
let square: (Int) -> Int = { x in x * x }
let add: (Int, Int) -> Int = { $0 + $1 }  // shorthand args

// Trailing closure syntax
[1,2,3,4,5].filter { $0 % 2 == 0 }
            .map { $0 * $0 }
            .forEach { print($0) }

// Capturing values
func makeCounter() -> () -> Int {
    var count = 0
    return { count += 1; return count }
}

// @escaping (stored for later)
func loadData(completion: @escaping (Data) -> Void) {
    DispatchQueue.global().async {
        let data = Data()
        completion(data)
    }
}
```


---

# CHAPTER 5: TYPES: STRUCT, CLASS, ENUM


## Value vs Reference Types

```swift
// Struct (value type)
struct Point {
    var x: Double
    var y: Double

    init(_ x: Double, _ y: Double) {
        self.x = x; self.y = y
    }

    func distance(to other: Point) -> Double {
        let dx = x - other.x; let dy = y - other.y
        return (dx*dx + dy*dy).squareRoot()
    }

    mutating func translate(by dx: Double, _ dy: Double) {
        x += dx; y += dy
    }

    static let origin = Point(0, 0)
}

// Class (reference type, supports inheritance)
class Animal {
    let name: String
    var sound: String

    init(name: String, sound: String) {
        self.name = name
        self.sound = sound
    }

    deinit { print("\(name) is being deinitialized") }

    func speak() -> String { "\(name) says \(sound)" }
}

class Dog: Animal {
    let breed: String
    init(name: String, breed: String) {
        self.breed = breed
        super.init(name: name, sound: "Woof")
    }
    override func speak() -> String { super.speak() + "!" }
}

// Enum (powerful in Swift)
enum Shape {
    case circle(radius: Double)
    case rectangle(width: Double, height: Double)
    case triangle(base: Double, height: Double)

    var area: Double {
        switch self {
        case .circle(let r):           return .pi * r * r
        case .rectangle(let w, let h): return w * h
        case .triangle(let b, let h):  return 0.5 * b * h
        }
    }
}

// Enum with raw value
enum Planet: Int, CaseIterable {
    case mercury = 1, venus, earth, mars
}

Planet.earth.rawValue   // 3
Planet(rawValue: 3)     // Optional<Planet>.earth
Planet.allCases         // [.mercury, .venus, .earth, .mars]

// Protocol (interface)
protocol Describable {
    var description: String { get }
    func describe()
}

extension Describable {
    func describe() { print(description) }  // default implementation
}
```


---

# CHAPTER 6: PROTOCOLS AND GENERICS


## Protocol-Oriented Programming

```swift
// Protocol with associated type
protocol Container {
    associatedtype Element
    var count: Int { get }
    subscript(i: Int) -> Element { get }
    mutating func append(_ item: Element)
}

// Conditional conformance
extension Array: Container where Element: Equatable { }

// Generics
func swap<T>(_ a: inout T, _ b: inout T) {
    let temp = a; a = b; b = temp
}

struct Stack<Element> {
    private var items: [Element] = []
    mutating func push(_ item: Element) { items.append(item) }
    mutating func pop() -> Element? { items.popLast() }
    var top: Element? { items.last }
    var isEmpty: Bool { items.isEmpty }
}

// Generic constraints
func findMax<T: Comparable>(_ array: [T]) -> T? {
    array.max()
}

// Where clauses
func allEqual<T>(_ a: T, _ b: T) -> Bool where T: Equatable {
    a == b
}

// Opaque types (some)
func makeAnimal() -> some Animal {
    Dog(name: "Rex", breed: "Lab")
}

// Existential types (any, Swift 5.7+)
func describe(animal: any Animal) {
    print(animal.speak())
}

// Result type
func fetchUser(id: Int) -> Result<String, Error> {
    guard id > 0 else { return .failure(AppError.invalid) }
    return .success("Alice")
}

switch fetchUser(id: 1) {
case .success(let name): print(name)
case .failure(let err):  print(err)
}
```


---

# CHAPTER 7: COLLECTIONS AND FUNCTIONAL


## Collections

```swift
// Array
var arr = [1, 2, 3, 4, 5]
arr.append(6)
arr.insert(0, at: 0)
arr.remove(at: 0)
arr.count
arr.isEmpty
arr.contains(3)
arr.sorted()
arr.sorted(by: >)
arr.reversed()
arr.first; arr.last
arr.dropFirst(2)
arr.prefix(3)
arr.filter { $0 > 2 }
arr.map { $0 * 2 }
arr.compactMap { Int("\($0)") }
arr.flatMap { [$0, $0*2] }
arr.reduce(0, +)
arr.reduce(into: [:]) { dict, n in dict[n] = n * n }
arr.forEach { print($0) }

// Dictionary
var dict = ["one": 1, "two": 2]
dict["three"] = 3
dict["one"]                    // Optional<Int>
dict["one", default: 0]       // Int
dict.removeValue(forKey: "two")
dict.keys; dict.values
dict.filter { $0.value > 1 }
dict.mapValues { $0 * 10 }
dict.merge(["four": 4]) { old, _ in old }

// Set
var s: Set = [1, 2, 3, 4]
s.insert(5)
s.remove(1)
s.contains(3)
s.union([5,6])
s.intersection([2,3,4,5])
s.subtracting([1,2])

// zip
let names = ["Alice", "Bob"]
let scores = [95, 87]
zip(names, scores).forEach { print("\($0): \($1)") }
```


---

# CHAPTER 8: CONCURRENCY


## Async/Await and Actors

```swift
import Foundation

// async function
func fetchUser(id: Int) async throws -> String {
    // Simulate network call
    try await Task.sleep(nanoseconds: 1_000_000_000)
    return "User \(id)"
}

// await
Task {
    do {
        let user = try await fetchUser(id: 1)
        print(user)
    } catch {
        print("Error: \(error)")
    }
}

// async let (parallel)
Task {
    async let user  = fetchUser(id: 1)
    async let posts = fetchPosts(userId: 1)
    let (u, p) = try await (user, posts)
    print(u, p)
}

// TaskGroup
Task {
    await withTaskGroup(of: String.self) { group in
        for i in 1...5 {
            group.addTask { await fetchUser(id: i) }
        }
        for await result in group {
            print(result)
        }
    }
}

// Actor (thread-safe reference type)
actor BankAccount {
    private var balance: Double = 0

    func deposit(_ amount: Double) { balance += amount }
    func withdraw(_ amount: Double) throws -> Double {
        guard balance >= amount else { throw BankError.insufficientFunds }
        balance -= amount
        return amount
    }
    var currentBalance: Double { balance }
}

let account = BankAccount()
await account.deposit(100)
let amount = try await account.withdraw(50)

// @MainActor — run on main thread
@MainActor
func updateUI(with text: String) {
    label.text = text
}

// Sendable — safe to pass across concurrency boundaries
struct User: Sendable {
    let name: String
    let age: Int
}
```
