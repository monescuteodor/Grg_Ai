# Kotlin and Android Development Complete Reference


---

# CHAPTER 1: KOTLIN LANGUAGE FUNDAMENTALS


## Remarks

Kotlin is JetBrains' statically-typed JVM language, officially endorsed by Google for Android development since 2017 (became the recommended language in 2019). It interoperates 100% with Java, runs on JVM/Android/JS/Native, and powers most modern Android apps.

Key features: **Null safety** (compiler prevents NPEs), **Type inference**, **Coroutines** for async (lightweight threads), **Extension functions**, **Data classes** (auto equals/hashCode/copy), **Smart casts**, **Lambdas and higher-order functions**, **Sealed classes** for algebraic types.

Used by: Android apps (Google, Pinterest, Uber, Netflix, Trello), backend services (Spring Boot Kotlin), Gradle build scripts.

Tools: **Android Studio** (IDE based on IntelliJ), **Kotlin Multiplatform** (share code iOS/Android), **Jetpack Compose** (declarative UI), **Gradle** (build), **KSP** (annotation processing).


## Variables and Types

```kotlin
// val = immutable (like final), var = mutable
val name = "Alice"            // Type inferred: String
val age: Int = 25             // Explicit type
val pi = 3.14159              // Double inferred

var counter = 0
counter++

// Basic types: Int, Long, Float, Double, Boolean, Char, String, Byte, Short
val score: Int = 100
val height: Double = 1.75
val active: Boolean = true
val initial: Char = 'A'

// String templates
val greeting = "Hello, $name, age $age"
val math = "Sum: ${5 + 3}"

// Multi-line strings
val bio = """
    Kotlin developer.
    Android enthusiast.
    Loves clean code.
""".trimIndent()

// Type conversion (explicit only)
val intVal = 100
val longVal: Long = intVal.toLong()
val strVal = intVal.toString()
val parsed: Int? = "42".toIntOrNull()
```


## Null Safety - Kotlin's Killer Feature

```kotlin
// Non-null by default
var name: String = "Alice"
// name = null  // Compile error!

// Nullable with ?
var maybeName: String? = null
maybeName = "Bob"

// Safe call - returns null if receiver is null
val length = maybeName?.length   // Int?

// Elvis operator - default value
val len = maybeName?.length ?: 0

// Not-null assertion - !! throws NPE if null (avoid!)
val definite = maybeName!!.length

// Let scope function - run if non-null
maybeName?.let {
    println("Name is $it")
    println("Length: ${it.length}")
}

// Smart cast - compiler tracks nullability
fun greet(name: String?) {
    if (name != null) {
        // Compiler knows name is non-null here
        println(name.uppercase())   // No ? needed
    }
}

// Early return pattern
fun process(input: String?): String {
    val text = input ?: return "No input"
    return text.uppercase()
}

// requireNotNull - throws with meaningful message
val token = requireNotNull(authToken) { "Token missing!" }
```


## Functions

```kotlin
// Basic function
fun greet(name: String): String {
    return "Hello, $name"
}

// Single-expression function
fun double(x: Int) = x * 2
fun max(a: Int, b: Int) = if (a > b) a else b

// Default values
fun greet(name: String = "World", greeting: String = "Hello") =
    "$greeting, $name!"

greet()                                    // "Hello, World!"
greet("Alice")                             // "Hello, Alice!"
greet(name = "Bob", greeting = "Hi")       // Named args

// Vararg
fun sum(vararg nums: Int): Int = nums.sum()
sum(1, 2, 3, 4, 5)    // 15

// Spread operator
val numbers = intArrayOf(1, 2, 3)
sum(*numbers)

// Higher-order functions (take functions as params)
fun operate(a: Int, b: Int, op: (Int, Int) -> Int): Int = op(a, b)

operate(5, 3) { x, y -> x + y }    // 8
operate(5, 3, ::Int::times)         // 15

// Function references
val isEven: (Int) -> Boolean = { it % 2 == 0 }
listOf(1, 2, 3, 4).filter(isEven)   // [2, 4]

// Extension functions - add methods to existing classes!
fun String.shout(): String = this.uppercase() + "!"
"hello".shout()    // "HELLO!"

fun List<Int>.average(): Double = sum().toDouble() / size

// Infix functions (call without dot)
infix fun Int.power(exp: Int): Int {
    var result = 1
    repeat(exp) { result *= this }
    return result
}
2 power 10    // 1024
```


## Control Flow

```kotlin
// if is an expression (returns value)
val max = if (a > b) a else b

val grade = if (score >= 90) "A"
            else if (score >= 80) "B"
            else if (score >= 70) "C"
            else "F"

// when (Kotlin's powerful switch)
when (status) {
    "active" -> handleActive()
    "pending", "queued" -> handleQueued()    // Multiple values
    in 1..10 -> handleSmall()                 // Range
    is Number -> handleNumber()               // Type check
    else -> handleDefault()
}

// when as expression
val description = when (x) {
    0 -> "zero"
    in 1..9 -> "small"
    in 10..99 -> "medium"
    else -> "large"
}

// when without argument (replaces complex if-else chains)
val signal = when {
    temp < 0 -> "freezing"
    temp < 20 -> "cold"
    temp < 30 -> "warm"
    else -> "hot"
}

// for loops
for (i in 1..10) print(i)                  // 1 to 10 inclusive
for (i in 1 until 10) print(i)             // 1 to 9
for (i in 10 downTo 1) print(i)            // 10 to 1
for (i in 1..10 step 2) print(i)           // 1, 3, 5, 7, 9

for (item in list) println(item)
for ((index, value) in list.withIndex()) println("$index: $value")

// while / do-while
while (condition) { /* ... */ }
do { /* ... */ } while (condition)
```


## Collections

```kotlin
// Lists (read-only vs mutable)
val readOnly = listOf("a", "b", "c")
val mutable = mutableListOf("x", "y", "z")
mutable.add("w")
mutable.removeAt(0)

// Sets
val set = setOf(1, 2, 3)
val mutableSet = mutableSetOf<Int>()

// Maps
val map = mapOf("a" to 1, "b" to 2, "c" to 3)
val mutableMap = mutableMapOf<String, Int>()
mutableMap["key"] = 42

for ((key, value) in map) println("$key -> $value")

// Functional operations
val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

val evens = numbers.filter { it % 2 == 0 }              // [2, 4, 6, 8, 10]
val doubled = numbers.map { it * 2 }                    // [2, 4, 6, ...]
val sum = numbers.reduce { acc, n -> acc + n }          // 55
val sumFolded = numbers.fold(100) { acc, n -> acc + n } // 155

val first3 = numbers.take(3)                            // [1, 2, 3]
val skip3 = numbers.drop(3)                             // [4, 5, ...]
val sorted = numbers.sortedDescending()

val grouped = numbers.groupBy { if (it % 2 == 0) "even" else "odd" }

// Chained operations
val result = numbers
    .filter { it > 3 }
    .map { it * it }
    .sum()    // 4²+5²+...+10² = 371

// Any / All / None
numbers.any { it > 5 }       // true
numbers.all { it > 0 }       // true
numbers.none { it < 0 }      // true

// Find
val firstEven = numbers.firstOrNull { it % 2 == 0 }
val foundIndex = numbers.indexOfFirst { it > 5 }
```


## Lambdas and Scope Functions

```kotlin
// Lambda basics
val square = { x: Int -> x * x }
square(5)    // 25

// Single param uses 'it'
val isPositive = { it: Int -> it > 0 }
val isNeg: (Int) -> Boolean = { it < 0 }

// Multi-line lambda
val complex = { x: Int, y: Int ->
    val sum = x + y
    sum * 2    // Last expression is return value
}

// Scope functions: let, run, with, apply, also

// let - operate on object, return result; safe-call friendly
val nameUpper = name?.let {
    it.trim().uppercase()
}

// run - same as let but uses 'this' inside
val len = name?.run {
    println("Working on $this")
    this.length
}

// apply - configure object, returns the object
val user = User().apply {
    name = "Alice"
    age = 30
    email = "alice@example.com"
}    // Returns the User

// also - side effects, returns the original
val list = mutableListOf(1, 2, 3).also {
    println("Created list: $it")
}    // Returns the list

// with - operate on receiver
with(user) {
    println(name)
    println(age)
}

// Decision rule:
// - need result?           -> let / run
// - configuring object?    -> apply
// - side effect only?      -> also
// - operating on existing? -> with
```


---

# CHAPTER 2: OBJECT-ORIENTED KOTLIN


## Classes and Objects

```kotlin
// Basic class with primary constructor
class Person(val name: String, var age: Int) {
    // Property with init
    val createdAt: Long = System.currentTimeMillis()

    // Computed property
    val isAdult: Boolean
        get() = age >= 18

    // Setter with validation
    var email: String = ""
        set(value) {
            require(value.contains("@")) { "Invalid email" }
            field = value   // 'field' is the backing variable
        }

    // Init block - runs on construction
    init {
        require(name.isNotBlank()) { "Name required" }
        println("Person created: $name")
    }

    // Secondary constructor (delegates to primary)
    constructor(name: String) : this(name, 0)

    // Method
    fun greet() = "Hi, I'm $name"
}

// Usage
val alice = Person("Alice", 30)
alice.age = 31
alice.email = "alice@example.com"
println(alice.greet())

// Companion object - "static" members
class User(val id: Int) {
    companion object {
        const val DEFAULT_AGE = 18

        fun create(name: String): User {
            return User(name.hashCode())
        }
    }
}
User.DEFAULT_AGE
User.create("Bob")

// Object declaration - singleton
object Database {
    private val records = mutableListOf<String>()

    fun save(record: String) {
        records.add(record)
    }

    fun all(): List<String> = records.toList()
}
Database.save("entry")
```


## Data Classes - Auto Boilerplate

```kotlin
// Data class - auto-generates equals, hashCode, toString, copy
data class User(
    val id: Int,
    val name: String,
    val email: String,
    val isActive: Boolean = true
)

val alice = User(1, "Alice", "alice@example.com")
val sameAlice = User(1, "Alice", "alice@example.com")

println(alice == sameAlice)       // true (structural equality)
println(alice.toString())          // User(id=1, name=Alice, ...)

// Copy with modifications
val olderAlice = alice.copy(name = "Alice Smith")

// Destructuring
val (id, name, email) = alice
println("$id, $name, $email")
```


## Inheritance

```kotlin
// Classes are FINAL by default - must use 'open' to allow inheritance
open class Animal(val name: String) {
    open fun makeSound() = "Generic sound"
    open val species: String = "Unknown"
}

class Dog(name: String, val breed: String) : Animal(name) {
    override fun makeSound() = "Woof!"
    override val species: String = "Canine"
}

val dog = Dog("Rex", "Labrador")
println(dog.makeSound())   // Woof!

// Abstract class - can't be instantiated
abstract class Shape {
    abstract fun area(): Double
    abstract val name: String

    fun describe() = "$name with area ${area()}"
}

class Circle(val radius: Double) : Shape() {
    override fun area() = Math.PI * radius * radius
    override val name = "Circle"
}
```


## Interfaces

```kotlin
interface Drawable {
    val color: String

    fun draw()                          // Abstract
    fun area(): Double = 0.0           // Default implementation
}

interface Resizable {
    fun resize(factor: Double)
}

// Multiple interfaces
class Rectangle(val width: Double, val height: Double, override val color: String)
    : Drawable, Resizable {

    override fun draw() = println("Drawing rectangle")
    override fun area() = width * height
    override fun resize(factor: Double) {
        // resize logic
    }
}

// Conflict resolution
interface A {
    fun greet() = "Hello from A"
}
interface B {
    fun greet() = "Hello from B"
}
class C : A, B {
    override fun greet() = super<A>.greet() + " and " + super<B>.greet()
}
```


## Sealed Classes - Algebraic Data Types

```kotlin
// Sealed class - all subclasses known at compile time
sealed class NetworkResult {
    data class Success(val data: String) : NetworkResult()
    data class Error(val message: String, val code: Int) : NetworkResult()
    object Loading : NetworkResult()
    object Empty : NetworkResult()
}

// Exhaustive when - no else needed!
fun handle(result: NetworkResult): String = when (result) {
    is NetworkResult.Success -> "Got: ${result.data}"
    is NetworkResult.Error -> "Error ${result.code}: ${result.message}"
    NetworkResult.Loading -> "Loading..."
    NetworkResult.Empty -> "No data"
}

// Sealed interfaces (Kotlin 1.5+)
sealed interface Animal {
    val name: String
}
data class Dog(override val name: String, val breed: String) : Animal
data class Cat(override val name: String, val indoor: Boolean) : Animal
```


## Enums

```kotlin
enum class Direction {
    NORTH, SOUTH, EAST, WEST
}

// With values and methods
enum class Planet(val mass: Double, val radius: Double) {
    EARTH(5.97e24, 6.371e6),
    MARS(6.42e23, 3.389e6),
    JUPITER(1.898e27, 6.991e7);

    fun gravity(): Double = (6.674e-11 * mass) / (radius * radius)
}

val g = Planet.EARTH.gravity()    // ~9.8

// Enum with sealed-like behavior
enum class Status {
    ACTIVE {
        override fun describe() = "Currently active"
    },
    INACTIVE {
        override fun describe() = "Not active"
    };

    abstract fun describe(): String
}
```


## Generics

```kotlin
// Generic class
class Box<T>(val content: T) {
    fun get(): T = content
}

val intBox = Box(42)            // Box<Int>
val strBox = Box("hello")       // Box<String>

// Generic function
fun <T> singletonList(item: T): List<T> = listOf(item)
fun <T : Comparable<T>> max(a: T, b: T): T = if (a > b) a else b

// Constraints
fun <T : Number> sum(items: List<T>): Double {
    return items.sumOf { it.toDouble() }
}

// Variance: 'out' for producers, 'in' for consumers
// out T -> covariant (T or subtype)
interface Producer<out T> {
    fun produce(): T
}

// in T -> contravariant (T or supertype)
interface Consumer<in T> {
    fun consume(item: T)
}

// Star projection
fun printAll(items: List<*>) {
    items.forEach { println(it) }
}
```


---

# CHAPTER 3: COROUTINES


## Coroutine Basics

```kotlin
// build.gradle.kts:
// implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.0")

import kotlinx.coroutines.*

// Suspend functions - can be paused and resumed
suspend fun fetchUser(id: Int): User {
    delay(1000)    // Non-blocking - frees thread
    return User(id, "User$id")
}

// Launch coroutine
fun main() = runBlocking {
    println("Start")
    launch {
        delay(1000)
        println("World!")
    }
    println("Hello")
    // Output: Start, Hello, then 1s later: World!
}

// Async - returns Deferred<T>, can await result
suspend fun fetchData() = coroutineScope {
    val user = async { fetchUser(1) }       // Starts immediately
    val posts = async { fetchPosts() }      // Starts immediately, parallel

    Pair(user.await(), posts.await())       // Wait for both
}

// withContext - switch dispatcher
suspend fun loadAndShow(url: String) {
    val data = withContext(Dispatchers.IO) {
        downloadFile(url)    // I/O on IO thread pool
    }
    withContext(Dispatchers.Main) {
        showImage(data)      // UI update on main thread
    }
}
```


## Dispatchers

```kotlin
// Dispatchers - where coroutines run

Dispatchers.Main        // Android UI thread
Dispatchers.IO          // Background I/O (file, network)
Dispatchers.Default     // CPU-intensive work
Dispatchers.Unconfined  // Don't dispatch (caller thread)

// Switch dispatcher in scope
viewModelScope.launch(Dispatchers.IO) {
    val data = repository.fetchData()    // On IO
    withContext(Dispatchers.Main) {
        _state.value = data              // UI update on Main
    }
}
```


## Coroutine Scopes

```kotlin
// GlobalScope - lives until process death (avoid in apps!)
GlobalScope.launch { /* ... */ }

// In Android ViewModel - automatically cancelled
class MyViewModel : ViewModel() {
    fun loadData() {
        viewModelScope.launch {
            try {
                _state.value = repository.fetch()
            } catch (e: Exception) {
                _error.value = e.message
            }
        }
    }
}

// In Activity/Fragment - tied to lifecycle
class MyFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        lifecycleScope.launch {
            // Auto-cancelled on lifecycle DESTROYED
        }

        // Launch only when STARTED
        viewLifecycleOwner.lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect { state ->
                    updateUI(state)
                }
            }
        }
    }
}

// Custom scope
class MyService {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)

    fun start() {
        scope.launch { /* ... */ }
    }

    fun stop() {
        scope.cancel()    // Cancel all coroutines in scope
    }
}
```


## Flow - Reactive Streams

```kotlin
// Cold flow - executes when collected
fun numbers(): Flow<Int> = flow {
    for (i in 1..10) {
        delay(100)
        emit(i)        // Emit value
    }
}

// Collect (terminal operator)
viewModelScope.launch {
    numbers().collect { value ->
        println(value)
    }
}

// Flow operators (intermediate, lazy)
viewModelScope.launch {
    numbers()
        .filter { it % 2 == 0 }
        .map { it * it }
        .take(3)
        .collect { println(it) }
    // Output: 4, 16, 36
}

// StateFlow - hot, holds latest value
class MyViewModel : ViewModel() {
    private val _state = MutableStateFlow<UiState>(UiState.Loading)
    val state: StateFlow<UiState> = _state.asStateFlow()

    fun load() {
        viewModelScope.launch {
            _state.value = UiState.Loading
            try {
                val data = repository.fetch()
                _state.value = UiState.Success(data)
            } catch (e: Exception) {
                _state.value = UiState.Error(e.message ?: "Unknown")
            }
        }
    }
}

// SharedFlow - hot, multiple subscribers, supports replay
class EventBus {
    private val _events = MutableSharedFlow<Event>(replay = 0)
    val events: SharedFlow<Event> = _events.asSharedFlow()

    suspend fun emit(event: Event) {
        _events.emit(event)
    }
}

// Combine multiple flows
combine(
    userFlow,
    settingsFlow
) { user, settings ->
    "${user.name} - ${settings.theme}"
}.collect { /* ... */ }

// Debounce, throttle
searchTextFlow
    .debounce(300)         // Wait 300ms idle
    .distinctUntilChanged()
    .filter { it.length >= 2 }
    .flatMapLatest { query ->
        searchRepository.search(query)
    }
    .collect { results -> _searchResults.value = results }
```


## Error Handling

```kotlin
// Try-catch in coroutine
viewModelScope.launch {
    try {
        val data = repository.fetch()
        _state.value = data
    } catch (e: IOException) {
        _error.value = "Network error"
    } catch (e: HttpException) {
        _error.value = "Server error ${e.code()}"
    }
}

// Coroutine exception handler
val handler = CoroutineExceptionHandler { _, exception ->
    Log.e("App", "Caught $exception")
}
scope.launch(handler) {
    throw RuntimeException("Oops")
}

// SupervisorJob - child failures don't cancel siblings
val scope = CoroutineScope(SupervisorJob())
scope.launch { /* if this fails, sibling continues */ }
scope.launch { /* unaffected by other's failure */ }
```


---

# CHAPTER 4: JETPACK COMPOSE BASICS


## Hello World

```kotlin
// build.gradle.kts:
// implementation("androidx.compose.material3:material3")
// implementation("androidx.activity:activity-compose")

import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface {
                    Greeting("Android")
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text(text = "Hello, $name!", style = MaterialTheme.typography.headlineLarge)
        Spacer(modifier = Modifier.height(8.dp))
        Text(text = "Welcome to Compose", style = MaterialTheme.typography.bodyMedium)
    }
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MaterialTheme {
        Greeting("Android")
    }
}
```


## Layout Composables

```kotlin
// Column - vertical
Column(
    modifier = Modifier.fillMaxWidth(),
    verticalArrangement = Arrangement.spacedBy(8.dp),
    horizontalAlignment = Alignment.CenterHorizontally
) {
    Text("Item 1")
    Text("Item 2")
    Text("Item 3")
}

// Row - horizontal
Row(
    modifier = Modifier.fillMaxWidth(),
    horizontalArrangement = Arrangement.SpaceBetween,
    verticalAlignment = Alignment.CenterVertically
) {
    Icon(Icons.Default.Home, contentDescription = null)
    Text("Profile")
    Icon(Icons.Default.ArrowForward, contentDescription = null)
}

// Box - stacked / overlay
Box(
    modifier = Modifier.size(100.dp),
    contentAlignment = Alignment.Center
) {
    Image(painter = painterResource(R.drawable.bg), contentDescription = null)
    Text("Overlay", color = Color.White)
}

// Spacer
Spacer(modifier = Modifier.height(16.dp))   // Vertical gap
Spacer(modifier = Modifier.width(8.dp))     // Horizontal
Spacer(modifier = Modifier.weight(1f))      // Fills remaining

// LazyColumn - efficient list (like RecyclerView)
LazyColumn(
    modifier = Modifier.fillMaxSize(),
    contentPadding = PaddingValues(16.dp),
    verticalArrangement = Arrangement.spacedBy(8.dp)
) {
    item {
        Text("Header", style = MaterialTheme.typography.headlineMedium)
    }

    items(items = users, key = { it.id }) { user ->
        UserCard(user)
    }

    itemsIndexed(items = users) { index, user ->
        Text("$index: ${user.name}")
    }

    item { Text("Footer") }
}

// LazyRow - horizontal scrollable
LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
    items(photos) { photo ->
        AsyncImage(model = photo.url, contentDescription = null,
            modifier = Modifier.size(120.dp))
    }
}

// LazyVerticalGrid
LazyVerticalGrid(
    columns = GridCells.Fixed(3),
    contentPadding = PaddingValues(8.dp),
    verticalArrangement = Arrangement.spacedBy(8.dp),
    horizontalArrangement = Arrangement.spacedBy(8.dp)
) {
    items(photos) { photo ->
        AsyncImage(model = photo.url, contentDescription = null)
    }
}
```


## Modifiers

```kotlin
Text(
    text = "Styled text",
    modifier = Modifier
        .fillMaxWidth()
        .padding(16.dp)
        .background(Color.Yellow)
        .border(2.dp, Color.Red, RoundedCornerShape(8.dp))
        .clip(RoundedCornerShape(8.dp))
        .clickable { println("clicked") }
        .padding(8.dp)
)

// Common modifiers:
// .size(width, height) / .size(48.dp)
// .width(100.dp) / .height(50.dp)
// .fillMaxWidth() / .fillMaxHeight() / .fillMaxSize()
// .padding(all) / .padding(horizontal, vertical) / .padding(start, top, end, bottom)
// .background(color, shape)
// .clip(shape)
// .border(width, color, shape)
// .clickable { ... }
// .alpha(0.5f)
// .rotate(45f)
// .scale(1.2f)
// .offset(x, y)
// .weight(1f)   // In Row/Column - fills remaining

// IMPORTANT: Modifier order matters!
// Padding then background = bigger background
.padding(16.dp).background(Color.Red)
// Background then padding = colored area smaller
.background(Color.Red).padding(16.dp)
```


## Material 3 Components

```kotlin
// Buttons
Button(onClick = { /* ... */ }) { Text("Primary") }
OutlinedButton(onClick = { }) { Text("Outlined") }
TextButton(onClick = { }) { Text("Text") }
FilledTonalButton(onClick = { }) { Text("Tonal") }
ElevatedButton(onClick = { }) { Text("Elevated") }

// Icon button
IconButton(onClick = { }) {
    Icon(Icons.Default.Favorite, contentDescription = "Favorite")
}

// FAB
FloatingActionButton(onClick = { }) {
    Icon(Icons.Default.Add, contentDescription = "Add")
}

// Text field
var text by remember { mutableStateOf("") }
TextField(
    value = text,
    onValueChange = { text = it },
    label = { Text("Name") },
    placeholder = { Text("Enter your name") },
    leadingIcon = { Icon(Icons.Default.Person, contentDescription = null) },
    modifier = Modifier.fillMaxWidth()
)

OutlinedTextField(
    value = email,
    onValueChange = { email = it },
    label = { Text("Email") },
    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
    isError = email.isNotBlank() && !email.contains("@")
)

// Checkbox / Switch / Radio
var checked by remember { mutableStateOf(false) }
Checkbox(checked = checked, onCheckedChange = { checked = it })
Switch(checked = checked, onCheckedChange = { checked = it })
RadioButton(selected = checked, onClick = { checked = true })

// Slider
var value by remember { mutableFloatStateOf(0.5f) }
Slider(
    value = value,
    onValueChange = { value = it },
    valueRange = 0f..1f
)

// Card
Card(
    modifier = Modifier.fillMaxWidth().padding(8.dp),
    elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Card title", style = MaterialTheme.typography.titleLarge)
        Text("Card content")
    }
}

// AlertDialog
var showDialog by remember { mutableStateOf(false) }
if (showDialog) {
    AlertDialog(
        onDismissRequest = { showDialog = false },
        title = { Text("Delete?") },
        text = { Text("This cannot be undone.") },
        confirmButton = {
            TextButton(onClick = { showDialog = false }) { Text("Confirm") }
        },
        dismissButton = {
            TextButton(onClick = { showDialog = false }) { Text("Cancel") }
        }
    )
}

// Snackbar (with Scaffold)
val snackbarHostState = remember { SnackbarHostState() }
val scope = rememberCoroutineScope()

Scaffold(
    snackbarHost = { SnackbarHost(snackbarHostState) }
) { padding ->
    Button(onClick = {
        scope.launch {
            snackbarHostState.showSnackbar("Item saved")
        }
    }) { Text("Save") }
}
```


---

# CHAPTER 5: STATE MANAGEMENT IN COMPOSE


## Remember and MutableState

```kotlin
@Composable
fun Counter() {
    // remember - survives recomposition
    var count by remember { mutableStateOf(0) }

    Column {
        Text("Count: $count")
        Button(onClick = { count++ }) {
            Text("Increment")
        }
    }
}

// rememberSaveable - survives configuration changes (rotation)
var name by rememberSaveable { mutableStateOf("") }

// derivedStateOf - computed value, only recomputes when dependencies change
val isLong by remember(text) {
    derivedStateOf { text.length > 10 }
}
```


## State Hoisting Pattern

```kotlin
// BAD - state inside reusable component
@Composable
fun BadCheckbox() {
    var checked by remember { mutableStateOf(false) }
    Checkbox(checked = checked, onCheckedChange = { checked = it })
}

// GOOD - hoisted (parent owns state)
@Composable
fun MyCheckbox(checked: Boolean, onCheckedChange: (Boolean) -> Unit) {
    Checkbox(checked = checked, onCheckedChange = onCheckedChange)
}

// Parent owns state
@Composable
fun ParentScreen() {
    var isAccepted by remember { mutableStateOf(false) }

    Column {
        Text("Accepted: $isAccepted")
        MyCheckbox(checked = isAccepted, onCheckedChange = { isAccepted = it })
    }
}
```


## ViewModel with Compose

```kotlin
class UserViewModel : ViewModel() {
    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    private val repository = UserRepository()

    init {
        loadUsers()
    }

    fun loadUsers() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            try {
                val users = repository.getAllUsers()
                _uiState.value = UiState.Success(users)
            } catch (e: Exception) {
                _uiState.value = UiState.Error(e.message ?: "Unknown")
            }
        }
    }
}

sealed class UiState {
    object Loading : UiState()
    data class Success(val users: List<User>) : UiState()
    data class Error(val message: String) : UiState()
}

@Composable
fun UserScreen(viewModel: UserViewModel = viewModel()) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    when (val s = state) {
        is UiState.Loading -> CircularProgressIndicator()
        is UiState.Success -> UserList(s.users)
        is UiState.Error -> ErrorView(s.message, onRetry = { viewModel.loadUsers() })
    }
}
```


## Side Effects

```kotlin
// LaunchedEffect - run suspend code when key changes
@Composable
fun MyScreen(userId: Int) {
    var user by remember { mutableStateOf<User?>(null) }

    LaunchedEffect(userId) {            // Re-launches if userId changes
        user = fetchUser(userId)
    }

    user?.let { UserDetail(it) }
}

// DisposableEffect - cleanup logic
@Composable
fun LocationScreen() {
    val context = LocalContext.current

    DisposableEffect(Unit) {
        val listener = LocationListener { /* ... */ }
        val locationManager = context.getSystemService(LocationManager::class.java)
        locationManager.requestLocationUpdates(/* ... */)

        onDispose {
            locationManager.removeUpdates(listener)
        }
    }
}

// rememberCoroutineScope - launch coroutines from event handlers
@Composable
fun MyButton() {
    val scope = rememberCoroutineScope()

    Button(onClick = {
        scope.launch {
            delay(1000)
            doSomething()
        }
    }) { Text("Click") }
}

// produceState - convert non-Compose to State
@Composable
fun NetworkImage(url: String): State<ImageState> = produceState<ImageState>(
    initialValue = ImageState.Loading,
    key1 = url
) {
    value = try {
        val image = downloadImage(url)
        ImageState.Success(image)
    } catch (e: Exception) {
        ImageState.Error(e)
    }
}
```


---

# CHAPTER 6: NAVIGATION


## Navigation Compose

```kotlin
// build.gradle.kts:
// implementation("androidx.navigation:navigation-compose:2.7.0")

import androidx.navigation.compose.*

// Routes (sealed class for type safety)
sealed class Screen(val route: String) {
    object Home : Screen("home")
    object Profile : Screen("profile/{userId}") {
        fun createRoute(userId: Int) = "profile/$userId"
    }
    object Settings : Screen("settings")
}

@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Screen.Home.route
    ) {
        composable(Screen.Home.route) {
            HomeScreen(
                onUserClick = { userId ->
                    navController.navigate(Screen.Profile.createRoute(userId))
                },
                onSettingsClick = {
                    navController.navigate(Screen.Settings.route)
                }
            )
        }

        composable(
            route = Screen.Profile.route,
            arguments = listOf(navArgument("userId") { type = NavType.IntType })
        ) { backStackEntry ->
            val userId = backStackEntry.arguments?.getInt("userId") ?: 0
            ProfileScreen(
                userId = userId,
                onBack = { navController.popBackStack() }
            )
        }

        composable(Screen.Settings.route) {
            SettingsScreen(onBack = { navController.popBackStack() })
        }
    }
}

// Navigate with options
navController.navigate(Screen.Login.route) {
    popUpTo(Screen.Home.route) { inclusive = true }   // Clear back stack
    launchSingleTop = true                              // Don't duplicate
}

// Pop back to specific destination
navController.popBackStack(Screen.Home.route, inclusive = false)
```


## Bottom Navigation

```kotlin
@Composable
fun MainScreen() {
    val navController = rememberNavController()

    Scaffold(
        bottomBar = {
            BottomNavBar(navController = navController)
        }
    ) { padding ->
        NavHost(
            navController = navController,
            startDestination = "home",
            modifier = Modifier.padding(padding)
        ) {
            composable("home") { HomeScreen() }
            composable("search") { SearchScreen() }
            composable("profile") { ProfileScreen() }
        }
    }
}

@Composable
fun BottomNavBar(navController: NavController) {
    val items = listOf(
        BottomNavItem("home", "Home", Icons.Default.Home),
        BottomNavItem("search", "Search", Icons.Default.Search),
        BottomNavItem("profile", "Profile", Icons.Default.Person)
    )

    NavigationBar {
        val currentBackStack by navController.currentBackStackEntryAsState()
        val currentRoute = currentBackStack?.destination?.route

        items.forEach { item ->
            NavigationBarItem(
                icon = { Icon(item.icon, contentDescription = item.title) },
                label = { Text(item.title) },
                selected = currentRoute == item.route,
                onClick = {
                    navController.navigate(item.route) {
                        popUpTo(navController.graph.findStartDestination().id) {
                            saveState = true
                        }
                        launchSingleTop = true
                        restoreState = true
                    }
                }
            )
        }
    }
}
```


---

# CHAPTER 7: NETWORKING WITH RETROFIT


## Retrofit + OkHttp

```kotlin
// build.gradle.kts:
// implementation("com.squareup.retrofit2:retrofit:2.9.0")
// implementation("com.squareup.retrofit2:converter-moshi:2.9.0")
// implementation("com.squareup.okhttp3:logging-interceptor:4.11.0")

import retrofit2.Retrofit
import retrofit2.http.*

// Data classes
@JsonClass(generateAdapter = true)
data class User(
    val id: Int,
    val name: String,
    val email: String,
    @Json(name = "created_at") val createdAt: String
)

@JsonClass(generateAdapter = true)
data class CreateUserRequest(
    val name: String,
    val email: String
)

// API interface
interface UserApi {
    @GET("users")
    suspend fun getUsers(@Query("page") page: Int = 1): List<User>

    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: Int): User

    @POST("users")
    suspend fun createUser(@Body request: CreateUserRequest): User

    @PUT("users/{id}")
    suspend fun updateUser(@Path("id") id: Int, @Body user: User): User

    @DELETE("users/{id}")
    suspend fun deleteUser(@Path("id") id: Int): Response<Unit>

    @Multipart
    @POST("upload")
    suspend fun uploadAvatar(
        @Part("user_id") userId: RequestBody,
        @Part file: MultipartBody.Part
    ): UploadResponse
}

// Setup
object ApiClient {
    private val logging = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    private val authInterceptor = Interceptor { chain ->
        val token = TokenStore.getToken()
        val request = chain.request().newBuilder().apply {
            if (token != null) addHeader("Authorization", "Bearer $token")
        }.build()
        chain.proceed(request)
    }

    private val client = OkHttpClient.Builder()
        .addInterceptor(logging)
        .addInterceptor(authInterceptor)
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    private val moshi = Moshi.Builder()
        .add(KotlinJsonAdapterFactory())
        .build()

    private val retrofit = Retrofit.Builder()
        .baseUrl("https://api.example.com/")
        .client(client)
        .addConverterFactory(MoshiConverterFactory.create(moshi))
        .build()

    val userApi: UserApi = retrofit.create(UserApi::class.java)
}

// Repository
class UserRepository(private val api: UserApi) {
    suspend fun getAllUsers(): Result<List<User>> = runCatching {
        api.getUsers()
    }

    suspend fun getUser(id: Int): User? = try {
        api.getUser(id)
    } catch (e: HttpException) {
        if (e.code() == 404) null else throw e
    }
}

// Usage in ViewModel
class UserViewModel(private val repo: UserRepository) : ViewModel() {
    fun load() {
        viewModelScope.launch {
            repo.getAllUsers()
                .onSuccess { users -> _state.value = UiState.Success(users) }
                .onFailure { error -> _state.value = UiState.Error(error.message) }
        }
    }
}
```


---

# CHAPTER 8: ROOM DATABASE


## Room Setup

```kotlin
// build.gradle.kts:
// implementation("androidx.room:room-runtime:2.6.0")
// implementation("androidx.room:room-ktx:2.6.0")
// ksp("androidx.room:room-compiler:2.6.0")

import androidx.room.*

// Entity
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val name: String,
    val email: String,
    @ColumnInfo(name = "created_at") val createdAt: Long = System.currentTimeMillis()
)

// DAO
@Dao
interface UserDao {
    @Query("SELECT * FROM users ORDER BY created_at DESC")
    fun getAllFlow(): Flow<List<UserEntity>>      // Reactive!

    @Query("SELECT * FROM users WHERE id = :id")
    suspend fun getById(id: Long): UserEntity?

    @Query("SELECT * FROM users WHERE name LIKE '%' || :query || '%'")
    suspend fun search(query: String): List<UserEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(user: UserEntity): Long

    @Update
    suspend fun update(user: UserEntity)

    @Delete
    suspend fun delete(user: UserEntity)

    @Query("DELETE FROM users WHERE id = :id")
    suspend fun deleteById(id: Long)

    @Query("DELETE FROM users")
    suspend fun clearAll()
}

// Database
@Database(
    entities = [UserEntity::class],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao

    companion object {
        @Volatile private var INSTANCE: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database"
                ).build().also { INSTANCE = it }
            }
        }
    }
}

// Repository with Room
class UserRepository(private val dao: UserDao) {
    val allUsersFlow: Flow<List<UserEntity>> = dao.getAllFlow()

    suspend fun add(name: String, email: String): Long {
        return dao.insert(UserEntity(name = name, email = email))
    }

    suspend fun remove(user: UserEntity) {
        dao.delete(user)
    }
}

// Usage in Compose
@Composable
fun UserListScreen(repository: UserRepository) {
    val users by repository.allUsersFlow.collectAsStateWithLifecycle(initialValue = emptyList())

    LazyColumn {
        items(users, key = { it.id }) { user ->
            ListItem(
                headlineContent = { Text(user.name) },
                supportingContent = { Text(user.email) }
            )
        }
    }
}
```


## Common Pitfalls

```kotlin
// PITFALL 1: NullPointerException with !!
val name: String? = null
val length = name!!.length   // CRASH!

// FIX
val length = name?.length ?: 0

// PITFALL 2: Coroutine launched on wrong dispatcher
viewModelScope.launch {
    val data = api.fetchData()   // Network on Main - might block!
}

// FIX
viewModelScope.launch(Dispatchers.IO) {
    val data = api.fetchData()
    withContext(Dispatchers.Main) {
        _state.value = data
    }
}

// PITFALL 3: Memory leak with non-cancelled scopes
class MyService {
    val scope = CoroutineScope(Job())   // Job never cancelled!

    fun start() {
        scope.launch { /* runs forever */ }
    }
}

// FIX
fun stop() {
    scope.cancel()
}

// PITFALL 4: Forgotten remember in Compose
@Composable
fun BadCounter() {
    var count = mutableStateOf(0)   // Recreated every recomposition!
    Button(onClick = { count.value++ }) {
        Text("${count.value}")
    }
}

// FIX
@Composable
fun GoodCounter() {
    var count by remember { mutableStateOf(0) }
    Button(onClick = { count++ }) {
        Text("$count")
    }
}

// PITFALL 5: Mutating list state directly
val list = remember { mutableStateListOf<String>() }
val regularList = remember { mutableListOf<String>() }
regularList.add("x")   // No recomposition - won't update UI!

// FIX
list.add("x")   // mutableStateListOf triggers recomposition

// PITFALL 6: Heavy work in @Composable function
@Composable
fun BadScreen() {
    val data = loadDataFromDisk()    // Runs on every recomposition!
    Text(data)
}

// FIX
@Composable
fun GoodScreen() {
    var data by remember { mutableStateOf("") }
    LaunchedEffect(Unit) {
        data = loadDataFromDisk()    // Only runs once
    }
    Text(data)
}

// PITFALL 7: Forgetting to use Stable types
data class User(val id: Int, val name: String)   // Stable - good

class MutableUser {                                 // Unstable - causes extra recompositions
    var name: String = ""
}

// PITFALL 8: ViewModel referenced from Composable lambdas captures Activity
@Composable
fun Screen(viewModel: MyViewModel) {
    Button(onClick = {
        viewModel.doStuff()   // OK
    }) { Text("Click") }
}

// PITFALL 9: Using GlobalScope in Android
GlobalScope.launch { /* ... */ }   // Lives forever, no lifecycle awareness

// FIX
viewModelScope.launch { /* ... */ }
lifecycleScope.launch { /* ... */ }
```