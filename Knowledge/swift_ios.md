# Swift and iOS Development Complete Reference


---

# CHAPTER 1: SWIFT LANGUAGE FUNDAMENTALS


## Remarks

Swift is Apple's modern, type-safe programming language for iOS, macOS, watchOS, tvOS, and visionOS development. Created in 2014 to replace Objective-C, it combines performance of compiled languages with expressiveness of scripting languages.

Key features: **Type inference** (compiler deduces types), **Optionals** (explicit nil handling), **Value types** (structs, enums by default), **Protocol-oriented** programming, **ARC** (Automatic Reference Counting for memory), **Generics**, **Async/await** for concurrency.

Used by: every iPhone app on App Store, macOS apps, Apple Watch, Apple TV, Apple Vision Pro.

Tools: **Xcode** (IDE, free from Mac App Store), **Swift Playgrounds** (learn Swift on iPad/Mac), `swift` command-line, **SwiftLint** (style enforcement).


## Variables and Constants

```swift
// Constants - immutable
let name = "Alice"
let pi: Double = 3.14159
let maxScore: Int = 100

// Variables - mutable
var counter = 0
counter += 1

// Type annotations (optional - usually inferred)
var temperature: Double = 22.5
var isActive: Bool = true
let message: String = "Hello"

// Multi-line strings
let bio = """
    Swift developer.
    iOS enthusiast.
    Loves clean code.
    """

// String interpolation
let age = 25
let intro = "I am \(name), \(age) years old"

// Type conversion (explicit, no implicit casts)
let score = 95
let scoreString = "\(score)"
let scoreFloat = Double(score)
let textNum = Int("42")    // Optional<Int>?
```


## Optionals — Swift's Killer Feature

```swift
// Optional means "might be nil"
var maybeName: String? = nil
maybeName = "Bob"

// Force unwrap (CRASHES if nil - use sparingly!)
let definitelyName = maybeName!

// Optional binding (safe)
if let name = maybeName {
    print("Name is \(name)")   // Only runs if non-nil
} else {
    print("No name")
}

// Guard - early exit pattern
func greet(_ name: String?) {
    guard let name = name else {
        print("Need a name")
        return
    }
    // name is now non-optional in this scope
    print("Hello, \(name)")
}

// Nil-coalescing operator
let displayName = maybeName ?? "Anonymous"

// Optional chaining
let upper = maybeName?.uppercased()       // String?
let length = maybeName?.count ?? 0        // Int

// Implicitly unwrapped optional (use with care)
var injected: String!    // Treated as non-nil after init

// Multiple optional binding
if let a = optA, let b = optB, a > 0 {
    print(a, b)
}
```


## Collections

```swift
// Arrays
var fruits = ["apple", "banana", "cherry"]
fruits.append("date")
fruits.insert("apricot", at: 1)
fruits.remove(at: 0)
fruits[0] = "blueberry"   // Mutate

let count = fruits.count
let first = fruits.first   // String? (might be empty)
let last = fruits.last
let contains = fruits.contains("banana")

// Iterate
for fruit in fruits {
    print(fruit)
}
for (index, fruit) in fruits.enumerated() {
    print("\(index): \(fruit)")
}

// Type annotations
var numbers: [Int] = []
var matrix: [[Int]] = [[1,2,3], [4,5,6]]

// Dictionaries
var prices = ["apple": 1.0, "banana": 0.5, "cherry": 2.5]
prices["date"] = 3.0          // Add or update
prices.removeValue(forKey: "apple")

if let price = prices["banana"] {
    print("Banana costs \(price)")
}

// Iterate dict
for (fruit, price) in prices {
    print("\(fruit): $\(price)")
}

// Sets - unique unordered
var colors: Set<String> = ["red", "green", "blue"]
colors.insert("red")   // No effect, already there
colors.contains("green")
let union = colors.union(["yellow", "red"])
let intersection = colors.intersection(["red", "purple"])
```


## Functions

```swift
// Basic
func greet(name: String) -> String {
    return "Hello, \(name)"
}
let msg = greet(name: "Alice")

// Multiple parameters with external names
func add(first: Int, second: Int) -> Int {
    return first + second
}
add(first: 5, second: 3)

// External vs internal names
func greet(to person: String) -> String {
    return "Hello, \(person)"
}
greet(to: "Bob")   // external: "to", internal: "person"

// Omit external name with _
func multiply(_ a: Int, _ b: Int) -> Int {
    return a * b
}
multiply(3, 4)

// Default values
func greet(name: String = "World") -> String {
    return "Hello, \(name)"
}
greet()              // "Hello, World"
greet(name: "Bob")

// Variadic parameters
func sum(_ numbers: Int...) -> Int {
    return numbers.reduce(0, +)
}
sum(1, 2, 3, 4, 5)   // 15

// Multiple return values (tuple)
func minMax(_ array: [Int]) -> (min: Int, max: Int)? {
    guard !array.isEmpty else { return nil }
    return (array.min()!, array.max()!)
}
if let result = minMax([3, 1, 4, 1, 5, 9, 2, 6]) {
    print("Min: \(result.min), Max: \(result.max)")
}

// In-out parameters (modify caller's variable)
func swap(_ a: inout Int, _ b: inout Int) {
    let temp = a
    a = b
    b = temp
}
var x = 1, y = 2
swap(&x, &y)
```


## Closures

```swift
// Closure syntax: { (params) -> ReturnType in body }
let square = { (x: Int) -> Int in x * x }
square(5)   // 25

// Type inference
let double: (Int) -> Int = { x in x * 2 }

// Trailing closure syntax
let numbers = [1, 2, 3, 4, 5]
let squared = numbers.map { $0 * $0 }                // [1, 4, 9, 16, 25]
let evens   = numbers.filter { $0 % 2 == 0 }         // [2, 4]
let total   = numbers.reduce(0) { $0 + $1 }          // 15

// Sort with closure
let sorted = numbers.sorted { $0 > $1 }   // descending

// Capturing values
func makeCounter() -> () -> Int {
    var count = 0
    return {
        count += 1
        return count
    }
}
let counter = makeCounter()
counter()   // 1
counter()   // 2
counter()   // 3

// Escaping closure - lives beyond function scope
var completionHandlers: [() -> Void] = []
func addHandler(_ handler: @escaping () -> Void) {
    completionHandlers.append(handler)
}
```


---

# CHAPTER 2: STRUCTS, CLASSES, AND ENUMS


## Structs vs Classes

```swift
// STRUCT - value type, copied on assignment
struct Point {
    var x: Double
    var y: Double

    // Method
    func distance(to other: Point) -> Double {
        let dx = x - other.x
        let dy = y - other.y
        return (dx*dx + dy*dy).squareRoot()
    }

    // Mutating method - changes self
    mutating func translate(by dx: Double, _ dy: Double) {
        x += dx
        y += dy
    }
}

var p1 = Point(x: 0, y: 0)
var p2 = p1                    // COPY
p2.x = 10
print(p1.x)   // Still 0 (independent copy)

// CLASS - reference type, shared
class Person {
    var name: String
    var age: Int

    init(name: String, age: Int) {   // Designated initializer required
        self.name = name
        self.age = age
    }

    func greet() {
        print("Hi, I'm \(name)")
    }

    deinit {
        print("\(name) deallocated")
    }
}

let alice = Person(name: "Alice", age: 30)
let bob = alice              // REFERENCE - same person!
bob.age = 31
print(alice.age)   // 31 (both vars point to same object)

// Identity vs equality
alice === bob       // true (same instance)
alice.name == bob.name   // true (equal values)
```


## Properties

```swift
struct Rectangle {
    var width: Double
    var height: Double

    // Computed property
    var area: Double {
        return width * height
    }

    // Read-write computed
    var perimeter: Double {
        get { 2 * (width + height) }
        set { /* derive width/height from perimeter */ }
    }

    // Property observers
    var label: String = "" {
        willSet {
            print("Will change from \(label) to \(newValue)")
        }
        didSet {
            print("Changed from \(oldValue) to \(label)")
        }
    }
}

// Lazy property - computed once on first access
class DataLoader {
    lazy var data: [String] = {
        print("Loading data...")
        return loadFromDisk()   // Only runs once
    }()

    private func loadFromDisk() -> [String] {
        return ["a", "b", "c"]
    }
}

// Static (type) properties
struct Math {
    static let pi = 3.14159
    static func square(_ x: Double) -> Double { x * x }
}
Math.pi
Math.square(5)
```


## Inheritance and Initialization

```swift
class Vehicle {
    var speed: Double = 0
    var description: String {
        return "Vehicle at \(speed) km/h"
    }

    func makeNoise() {
        // Override in subclass
    }
}

class Car: Vehicle {
    var gear: Int = 1

    // Override property
    override var description: String {
        return "\(super.description) in gear \(gear)"
    }

    // Override method
    override func makeNoise() {
        print("Vroom!")
    }
}

class Bicycle: Vehicle {
    var hasBasket = false

    init(speed: Double, hasBasket: Bool) {
        self.hasBasket = hasBasket
        super.init()           // Call superclass init
        self.speed = speed
    }
}

// Required init (subclasses MUST implement)
class Shape {
    required init() { }
}

// Convenience init (delegates to designated init)
class Person {
    var name: String

    init(name: String) {       // Designated
        self.name = name
    }

    convenience init() {       // Convenience
        self.init(name: "Anonymous")
    }
}
```


## Enums

```swift
// Basic enum
enum Direction {
    case north, south, east, west
}

let heading = Direction.north
switch heading {
case .north: print("Going up")
case .south: print("Going down")
case .east:  print("Going right")
case .west:  print("Going left")
}

// Raw values
enum Planet: Int {
    case mercury = 1, venus, earth, mars   // venus=2, earth=3, ...
}
Planet.earth.rawValue   // 3
let p = Planet(rawValue: 1)   // Optional<Planet>?

enum Status: String {
    case active = "ACTIVE"
    case inactive = "INACTIVE"
    case pending = "PENDING"
}

// Associated values - SWIFT'S SUPERPOWER
enum NetworkResult {
    case success(data: Data, code: Int)
    case failure(error: Error)
    case loading
}

func handle(_ result: NetworkResult) {
    switch result {
    case .success(let data, let code):
        print("Got \(data.count) bytes, code \(code)")
    case .failure(let error):
        print("Error: \(error)")
    case .loading:
        print("Loading...")
    }
}

// Methods on enums
enum Coin {
    case heads, tails
    func flip() -> Coin {
        return self == .heads ? .tails : .heads
    }
}
```


## Protocols (Swift's Interfaces++)

```swift
// Define protocol
protocol Drawable {
    var color: String { get }      // Read-only property
    var name: String { get set }   // Read-write
    func draw()                    // Required method
    func area() -> Double          // Required
}

// Conform with struct
struct Circle: Drawable {
    let color: String
    var name: String
    let radius: Double

    func draw() {
        print("Drawing \(name) circle")
    }
    func area() -> Double {
        return 3.14 * radius * radius
    }
}

// Protocol extension - default implementations!
extension Drawable {
    func draw() {                    // Default implementation
        print("Drawing \(name)")
    }
    var description: String {        // Computed property
        return "\(color) shape"
    }
}

// Polymorphism through protocols
let shapes: [Drawable] = [
    Circle(color: "red", name: "C1", radius: 5),
    Circle(color: "blue", name: "C2", radius: 10),
]
for shape in shapes {
    shape.draw()
}

// Protocol composition
typealias Identifiable = Hashable & Codable
func process<T: Identifiable>(_ item: T) { /* ... */ }

// Conditional conformance
extension Array: Drawable where Element: Drawable {
    var color: String { "mixed" }
    var name: String {
        get { "array" }
        set { }
    }
    func draw() {
        forEach { $0.draw() }
    }
    func area() -> Double {
        return reduce(0) { $0 + $1.area() }
    }
}
```


---

# CHAPTER 3: SWIFTUI BASICS


## Hello World SwiftUI App

```swift
import SwiftUI

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    var body: some View {
        VStack(spacing: 20) {
            Text("Hello, SwiftUI!")
                .font(.largeTitle)
                .foregroundColor(.blue)
                .bold()

            Image(systemName: "star.fill")
                .font(.system(size: 50))
                .foregroundColor(.yellow)

            Button("Tap me") {
                print("Tapped!")
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}

#Preview {
    ContentView()
}
```


## Layout Views

```swift
// VStack - vertical
VStack(alignment: .leading, spacing: 12) {
    Text("Title")
    Text("Subtitle")
    Text("Body")
}

// HStack - horizontal
HStack(alignment: .center, spacing: 8) {
    Image(systemName: "person")
    Text("Profile")
    Spacer()
    Image(systemName: "chevron.right")
}

// ZStack - layered (z-axis)
ZStack {
    Color.blue.ignoresSafeArea()
    Text("On top")
        .foregroundColor(.white)
}

// Grid (iOS 16+)
Grid {
    GridRow {
        Text("Name")
        Text("Age")
    }
    GridRow {
        Text("Alice")
        Text("30")
    }
}

// LazyVGrid (efficient for large content)
let columns = [GridItem(.adaptive(minimum: 80))]
LazyVGrid(columns: columns, spacing: 16) {
    ForEach(0..<100) { i in
        Text("\(i)")
            .frame(width: 60, height: 60)
            .background(Color.blue.opacity(0.3))
    }
}

// ScrollView
ScrollView {
    VStack {
        ForEach(0..<50) { i in
            Text("Item \(i)")
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.gray.opacity(0.2))
        }
    }
}

// Horizontal ScrollView
ScrollView(.horizontal, showsIndicators: false) {
    HStack {
        ForEach(images, id: \.self) { image in
            Image(image)
                .resizable()
                .frame(width: 100, height: 100)
        }
    }
}
```


## Modifiers

```swift
Text("Styled text")
    .font(.title)                              // Font
    .fontWeight(.bold)                         // Weight
    .foregroundColor(.red)                     // Color
    .padding()                                 // All sides
    .padding(.horizontal, 16)                  // Specific
    .background(Color.yellow)                  // Background
    .cornerRadius(8)                           // Rounded corners
    .shadow(color: .gray, radius: 4, x: 2, y: 2)
    .frame(width: 200, height: 50)             // Fixed size
    .frame(maxWidth: .infinity)                // Flexible
    .opacity(0.8)
    .rotationEffect(.degrees(15))
    .scaleEffect(1.2)
    .offset(x: 10, y: 0)

// Tap gesture
.onTapGesture {
    print("Tapped!")
}

// Long press
.onLongPressGesture(minimumDuration: 1) {
    print("Long pressed!")
}

// Conditional modifier
Text("Hello")
    .foregroundColor(isHighlighted ? .red : .black)

// Modifier order MATTERS!
// Padding then background = bigger background
Text("A").padding().background(Color.red)
// Background then padding = smaller colored area
Text("A").background(Color.red).padding()
```


## Common UI Components

```swift
// Text
Text("Hello")
Text(date, style: .relative)   // "2 days ago"
Text("Bold word: ").bold() + Text("here").italic()

// Image
Image("logo")                              // Asset
Image(systemName: "heart.fill")            // SF Symbol
    .resizable()
    .aspectRatio(contentMode: .fit)
    .frame(width: 100, height: 100)

// AsyncImage - load from URL
AsyncImage(url: URL(string: "https://example.com/img.jpg")) { image in
    image.resizable().aspectRatio(contentMode: .fit)
} placeholder: {
    ProgressView()
}

// Button styles
Button("Tap") { print("tap") }                    // Plain
Button("Action") { }.buttonStyle(.bordered)
Button("Primary") { }.buttonStyle(.borderedProminent)
Button(role: .destructive, action: { }) {        // Red destructive
    Label("Delete", systemImage: "trash")
}

// TextField
@State private var name = ""
TextField("Enter name", text: $name)
    .textFieldStyle(.roundedBorder)
    .padding()

SecureField("Password", text: $password)

TextEditor(text: $longText)   // Multi-line

// Toggle
@State private var isOn = false
Toggle("Notifications", isOn: $isOn)

// Slider
@State private var value: Double = 50
Slider(value: $value, in: 0...100, step: 1)

// Picker
@State private var selection = "Apple"
Picker("Fruit", selection: $selection) {
    Text("Apple").tag("Apple")
    Text("Banana").tag("Banana")
    Text("Cherry").tag("Cherry")
}
.pickerStyle(.segmented)   // or .wheel, .menu

// DatePicker
@State private var date = Date()
DatePicker("Date", selection: $date, displayedComponents: .date)

// ProgressView
ProgressView()                                    // Spinner
ProgressView("Loading...")
ProgressView(value: 0.7)                          // Progress bar
```


---

# CHAPTER 4: STATE AND DATA FLOW


## @State - Local View State

```swift
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("+") { count += 1 }
        }
    }
}
```


## @Binding - Two-way Connection

```swift
// Parent owns the state
struct ParentView: View {
    @State private var isActive = false

    var body: some View {
        ToggleView(isActive: $isActive)   // Pass binding
    }
}

// Child receives binding
struct ToggleView: View {
    @Binding var isActive: Bool   // Two-way connection

    var body: some View {
        Button(isActive ? "Active" : "Inactive") {
            isActive.toggle()    // Modifies parent's state!
        }
    }
}
```


## @StateObject and @ObservedObject

```swift
// Observable class
class UserSettings: ObservableObject {
    @Published var username = "Guest"
    @Published var theme = "Light"
    @Published var fontSize = 16

    func reset() {
        username = "Guest"
        theme = "Light"
        fontSize = 16
    }
}

// Owner creates with @StateObject
struct ContentView: View {
    @StateObject private var settings = UserSettings()

    var body: some View {
        SettingsView(settings: settings)
    }
}

// Receiver uses @ObservedObject
struct SettingsView: View {
    @ObservedObject var settings: UserSettings

    var body: some View {
        Form {
            TextField("Username", text: $settings.username)
            Picker("Theme", selection: $settings.theme) {
                Text("Light").tag("Light")
                Text("Dark").tag("Dark")
            }
            Stepper("Font Size: \(settings.fontSize)",
                    value: $settings.fontSize, in: 12...24)
        }
    }
}
```


## @EnvironmentObject - App-wide Shared State

```swift
// Inject at root
@main
struct MyApp: App {
    @StateObject private var settings = UserSettings()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(settings)   // Available everywhere
        }
    }
}

// Use anywhere in view hierarchy
struct DeeplyNestedView: View {
    @EnvironmentObject var settings: UserSettings

    var body: some View {
        Text("Hello, \(settings.username)")
    }
}
```


## @Observable (iOS 17+) - Modern API

```swift
import Observation

@Observable
class UserSettings {
    var username = "Guest"     // No @Published needed
    var theme = "Light"
}

// Use directly
struct ContentView: View {
    @State private var settings = UserSettings()

    var body: some View {
        Text(settings.username)
    }
}

// Bindable for two-way binding
struct EditView: View {
    @Bindable var settings: UserSettings

    var body: some View {
        TextField("Name", text: $settings.username)
    }
}
```


## @AppStorage - UserDefaults

```swift
struct SettingsView: View {
    @AppStorage("username") private var username = ""
    @AppStorage("isDarkMode") private var isDarkMode = false
    @AppStorage("fontSize") private var fontSize = 14

    var body: some View {
        Form {
            TextField("Username", text: $username)
            Toggle("Dark Mode", isOn: $isDarkMode)
            Stepper("Font Size: \(fontSize)", value: $fontSize, in: 10...24)
        }
    }
}
// Automatically saved to UserDefaults, persists across launches
```


---

# CHAPTER 5: NAVIGATION


## NavigationStack (iOS 16+)

```swift
struct ContentView: View {
    var body: some View {
        NavigationStack {
            List {
                NavigationLink("Profile", value: "profile")
                NavigationLink("Settings", value: "settings")
                NavigationLink("About", value: "about")
            }
            .navigationTitle("Home")
            .navigationDestination(for: String.self) { destination in
                switch destination {
                case "profile": ProfileView()
                case "settings": SettingsView()
                case "about": AboutView()
                default: EmptyView()
                }
            }
        }
    }
}

// Programmatic navigation
struct AppView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            VStack {
                Button("Go to Profile") {
                    path.append("profile")
                }
                Button("Deep link") {
                    path.append("profile")
                    path.append("settings")
                }
                Button("Pop all") {
                    path = NavigationPath()
                }
            }
            .navigationDestination(for: String.self) { _ in
                DetailView()
            }
        }
    }
}

// Type-safe navigation
struct User: Hashable {
    let id: Int
    let name: String
}

NavigationLink("View user", value: User(id: 1, name: "Alice"))
    .navigationDestination(for: User.self) { user in
        UserDetailView(user: user)
    }
```


## TabView

```swift
struct MainView: View {
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem {
                    Label("Home", systemImage: "house")
                }
                .tag(0)

            SearchView()
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }
                .tag(1)

            ProfileView()
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
                .tag(2)
                .badge(3)   // Notification badge
        }
    }
}
```


## Sheets and Alerts

```swift
struct ContentView: View {
    @State private var showSheet = false
    @State private var showAlert = false
    @State private var showConfirmation = false

    var body: some View {
        VStack {
            Button("Show Sheet") { showSheet = true }
            Button("Show Alert") { showAlert = true }
            Button("Show Confirmation") { showConfirmation = true }
        }
        // Modal sheet
        .sheet(isPresented: $showSheet) {
            SheetView()
                .presentationDetents([.medium, .large])
        }
        // Alert
        .alert("Delete?", isPresented: $showAlert) {
            Button("Cancel", role: .cancel) { }
            Button("Delete", role: .destructive) {
                deleteItem()
            }
        } message: {
            Text("This action cannot be undone.")
        }
        // Confirmation dialog (action sheet)
        .confirmationDialog("Choose", isPresented: $showConfirmation) {
            Button("Option 1") { }
            Button("Option 2") { }
            Button("Cancel", role: .cancel) { }
        }
    }
}

// Pass data via sheet item
struct ContentView: View {
    @State private var selectedItem: Item?

    var body: some View {
        Button("Edit Item 1") {
            selectedItem = Item(id: 1, name: "Item")
        }
        .sheet(item: $selectedItem) { item in
            EditView(item: item)
        }
    }
}
```


---

# CHAPTER 6: LISTS


## Static and Dynamic Lists

```swift
// Static list
List {
    Text("Item 1")
    Text("Item 2")
    Text("Item 3")
}

// Dynamic with ForEach
struct ContentView: View {
    let items = ["Apple", "Banana", "Cherry"]

    var body: some View {
        List(items, id: \.self) { item in
            Text(item)
        }
    }
}

// Identifiable items - cleaner
struct Fruit: Identifiable {
    let id = UUID()
    let name: String
    let color: String
}

let fruits = [
    Fruit(name: "Apple", color: "red"),
    Fruit(name: "Banana", color: "yellow"),
]

List(fruits) { fruit in
    HStack {
        Circle().fill(Color(fruit.color))
            .frame(width: 20, height: 20)
        Text(fruit.name)
    }
}

// Sections
List {
    Section("Fruits") {
        ForEach(fruits) { Text($0.name) }
    }
    Section("Vegetables") {
        ForEach(vegetables) { Text($0.name) }
    }
}

// Swipe actions
List(items) { item in
    Text(item.name)
        .swipeActions(edge: .trailing) {
            Button(role: .destructive) {
                delete(item)
            } label: {
                Label("Delete", systemImage: "trash")
            }
            Button {
                archive(item)
            } label: {
                Label("Archive", systemImage: "archivebox")
            }
            .tint(.blue)
        }
}

// Pull to refresh
List(items) { item in
    Text(item.name)
}
.refreshable {
    await loadData()
}

// Searchable
struct SearchableList: View {
    @State private var searchText = ""

    var filtered: [String] {
        if searchText.isEmpty { return items }
        return items.filter { $0.localizedCaseInsensitiveContains(searchText) }
    }

    var body: some View {
        NavigationStack {
            List(filtered, id: \.self) { Text($0) }
                .searchable(text: $searchText, prompt: "Search items")
        }
    }
}
```


---

# CHAPTER 7: CONCURRENCY WITH ASYNC/AWAIT


## Async Functions

```swift
// Async function
func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, response) = try await URLSession.shared.data(from: url)

    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw URLError(.badServerResponse)
    }

    return try JSONDecoder().decode(User.self, from: data)
}

// Calling from a view
struct UserView: View {
    @State private var user: User?
    @State private var error: Error?

    var body: some View {
        VStack {
            if let user = user {
                Text(user.name)
            } else if error != nil {
                Text("Error loading user")
            } else {
                ProgressView()
            }
        }
        .task {
            do {
                user = try await fetchUser(id: 1)
            } catch {
                self.error = error
            }
        }
    }
}

// Parallel async
func fetchMultiple() async throws -> ([User], [Post]) {
    async let users = fetchAllUsers()       // Starts immediately
    async let posts = fetchAllPosts()       // Starts immediately, parallel

    return try await (users, posts)        // Wait for both
}

// TaskGroup - dynamic parallelism
func fetchAllUsers(ids: [Int]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask {
                try await fetchUser(id: id)
            }
        }
        var users: [User] = []
        for try await user in group {
            users.append(user)
        }
        return users
    }
}
```


## URLSession Modern API

```swift
class APIClient {
    let baseURL = URL(string: "https://api.example.com")!
    let session = URLSession.shared

    func get<T: Decodable>(_ path: String) async throws -> T {
        let url = baseURL.appendingPathComponent(path)
        var request = URLRequest(url: url)
        request.setValue("application/json", forHTTPHeaderField: "Accept")

        if let token = await TokenStore.shared.token {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        switch httpResponse.statusCode {
        case 200...299:
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            return try decoder.decode(T.self, from: data)
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.notFound
        default:
            throw APIError.serverError(httpResponse.statusCode)
        }
    }

    func post<T: Encodable, U: Decodable>(_ path: String, body: T) async throws -> U {
        let url = baseURL.appendingPathComponent(path)
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(body)

        let (data, _) = try await session.data(for: request)
        return try JSONDecoder().decode(U.self, from: data)
    }
}

enum APIError: Error {
    case invalidResponse
    case unauthorized
    case notFound
    case serverError(Int)
}
```


---

# CHAPTER 8: CORE DATA AND SWIFTDATA


## SwiftData (iOS 17+) - Modern Persistence

```swift
import SwiftData

// Define model
@Model
class Task {
    var title: String
    var isDone: Bool
    var createdAt: Date
    var priority: Int

    init(title: String, priority: Int = 1) {
        self.title = title
        self.isDone = false
        self.createdAt = Date()
        self.priority = priority
    }
}

// Setup container
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Task.self)
    }
}

// Query and modify
struct TaskListView: View {
    @Environment(\.modelContext) private var modelContext
    @Query(sort: \Task.createdAt, order: .reverse) private var tasks: [Task]
    @State private var newTaskTitle = ""

    var body: some View {
        NavigationStack {
            List {
                ForEach(tasks) { task in
                    HStack {
                        Image(systemName: task.isDone ? "checkmark.square" : "square")
                            .onTapGesture { task.isDone.toggle() }
                        Text(task.title)
                            .strikethrough(task.isDone)
                    }
                }
                .onDelete { offsets in
                    for offset in offsets {
                        modelContext.delete(tasks[offset])
                    }
                }
            }
            .navigationTitle("Tasks")
            .toolbar {
                ToolbarItem(placement: .bottomBar) {
                    HStack {
                        TextField("New task", text: $newTaskTitle)
                        Button("Add") {
                            let task = Task(title: newTaskTitle)
                            modelContext.insert(task)
                            newTaskTitle = ""
                        }
                    }
                }
            }
        }
    }
}

// Filtered query
@Query(filter: #Predicate<Task> { !$0.isDone },
       sort: \Task.priority, order: .reverse)
private var openTasks: [Task]
```


## Common Pitfalls

```swift
// PITFALL 1: Force unwrap on optional - CRASH
let url = URL(string: invalidURL)!   // Crashes if nil!

// FIX: Safe unwrapping
guard let url = URL(string: urlString) else { return }

// PITFALL 2: Retain cycles in closures
class ViewModel {
    var onUpdate: (() -> Void)?

    func setup() {
        someManager.observe {
            self.update()   // self captured strongly - cycle!
        }
    }
}

// FIX: weak self
someManager.observe { [weak self] in
    self?.update()
}

// PITFALL 3: Modifying state during view update
struct BadView: View {
    @State var count = 0
    var body: some View {
        Text("Count: \(count)")
            .onAppear {
                count += 1   // OK
            }
        // Bad: doing this in body itself causes infinite re-render
    }
}

// PITFALL 4: @State for reference types
class DataModel {
    var items: [Item] = []
}

struct BadView: View {
    @State var model = DataModel()   // Wrong - won't notify on mutations
}

// FIX: Use @StateObject for classes
@StateObject var model = DataModel()   // Where DataModel: ObservableObject

// PITFALL 5: Force unwrap UI components
let button: UIButton!   // Crashes if not connected in IB

// FIX: Use guard or optional chaining
guard let button = self.button else { return }

// PITFALL 6: Heavy work on main thread
Button("Process") {
    let result = heavyComputation()   // Blocks UI!
    showResult(result)
}

// FIX: Async work
Button("Process") {
    Task {
        let result = await heavyComputation()
        showResult(result)
    }
}

// PITFALL 7: NavigationView (deprecated) vs NavigationStack
// OLD: NavigationView - deprecated in iOS 16+
// NEW: NavigationStack - use this

// PITFALL 8: Forgetting @MainActor for UI updates
func updateUI() {   // Might run on background!
    label.text = "Updated"   // CRASH or undefined behavior
}

// FIX
@MainActor
func updateUI() {
    label.text = "Updated"
}
// Or wrap:
await MainActor.run {
    label.text = "Updated"
}
```