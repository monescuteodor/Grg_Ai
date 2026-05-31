# Kotlin Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH KOTLIN


## Remarks

Kotlin is a statically-typed, multiplatform language that compiles to JVM bytecode, JavaScript, and native binaries. It is fully interoperable with Java and is the preferred language for Android development. Kotlin emphasizes safety (null-safety), conciseness, and expressiveness.

Tools: kotlinc compiler, IntelliJ IDEA, Android Studio, Gradle, Maven, Kotlin REPL.


## Hello World

```kotlin
// hello.kt
fun main() {
    println("Hello, World!")
    println("Hello, ${"Kotlin"}!")
}

// With args
fun main(args: Array<String>) {
    println("Hello, ${if (args.isEmpty()) "World" else args[0]}!")
}
```

```bash
kotlinc hello.kt -include-runtime -d hello.jar && java -jar hello.jar
# Or with Kotlin script
kotlinc -script hello.main.kts
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Types and Variables

```kotlin
// val = immutable (like final), var = mutable
val name: String = "Alice"
val age: Int = 30
var count = 0      // type inferred
count++

// Primitive types (map to JVM primitives)
val i: Int = 42
val l: Long = 9_000_000_000L
val d: Double = 3.14
val f: Float = 3.14f
val b: Byte = 127
val s: Short = 1000
val ch: Char = 'A'
val bool: Boolean = true

// Unsigned types
val ui: UInt = 42u
val ul: ULong = 9000000000u

// String operations
val str = "Hello, World!"
str.length                   // 13
str.uppercase()
str.lowercase()
str.substring(0, 5)          // "Hello"
str.contains("World")
str.replace("World", "Kotlin")
str.split(", ")
str.trim()
str.startsWith("Hello")
str.endsWith("!")
str.toInt()                  // exception if not valid
str.toIntOrNull()            // null if not valid
"42".toInt()                 // 42

// String templates
val greeting = "Hello, $name!"
val expr = "Age next year: ${age + 1}"

// Multiline strings
val text = """
    |Hello
    |World
""".trimMargin()

// Null safety — must declare nullable type with ?
val nullableName: String? = null
val length = nullableName?.length      // null (safe call)
val len = nullableName?.length ?: 0   // 0 (elvis operator)
val forced = nullableName!!.length     // NPE if null

// Smart casts
fun describe(obj: Any): String {
    return when (obj) {
        is Int    -> "Int: $obj"
        is String -> "String of length ${obj.length}"
        is Boolean -> "Boolean: $obj"
        else -> "Unknown: ${obj::class.simpleName}"
    }
}

// Type conversions (explicit)
val d2 = 42.toDouble()
val i2 = 3.14.toInt()
val s2 = 42.toString()
```


---

# CHAPTER 3: COLLECTIONS


## Collections

```kotlin
// Immutable collections (default)
val list = listOf(1, 2, 3, 4, 5)
val set  = setOf(1, 2, 3)
val map  = mapOf("Alice" to 30, "Bob" to 25)

// Mutable collections
val mlist = mutableListOf(1, 2, 3)
val mset  = mutableSetOf("a", "b")
val mmap  = mutableMapOf("x" to 1, "y" to 2)

// ArrayList, LinkedList, HashMap etc. (Java collections)
val al = ArrayList<Int>()
val hm = HashMap<String, Int>()

// List operations
list[0]                // 1
list.size              // 5
list.first()           // 1
list.last()            // 5
list.isEmpty()         // false
list.contains(3)       // true
list + listOf(6, 7)    // new list [1,2,3,4,5,6,7]

// Transformations
list.map { it * 2 }                  // [2,4,6,8,10]
list.filter { it % 2 == 0 }          // [2,4]
list.filterNot { it % 2 == 0 }       // [1,3,5]
list.find { it > 3 }                  // 4
list.first { it > 3 }                 // 4
list.any { it > 4 }                   // true
list.all { it > 0 }                   // true
list.none { it > 10 }                 // true
list.count { it % 2 == 0 }           // 2
list.sum()                            // 15
list.sumOf { it * 2 }                // 30
list.min(); list.max()
list.minOrNull(); list.maxOrNull()
list.sorted()
list.sortedDescending()
list.sortedBy { -it }
list.reversed()
list.take(3)                          // [1,2,3]
list.drop(2)                          // [3,4,5]
list.takeWhile { it < 4 }            // [1,2,3]
list.dropWhile { it < 4 }            // [4,5]
list.chunked(2)                       // [[1,2],[3,4],[5]]
list.windowed(3)                      // [[1,2,3],[2,3,4],[3,4,5]]
list.zip(list)                        // [(1,1),(2,2),...]
list.flatten()                        // (on list of lists)
list.flatMap { listOf(it, it*2) }    // [1,2,2,4,3,6,4,8,5,10]
list.groupBy { it % 2 == 0 }        // {false=[1,3,5], true=[2,4]}
list.partition { it % 2 == 0 }      // ([2,4],[1,3,5])
list.reduce { acc, x -> acc + x }   // 15
list.fold(0) { acc, x -> acc + x }  // 15

// Map operations
map["Alice"]                          // 30
map.getOrDefault("Dave", 0)           // 0
map.keys; map.values; map.entries
map.contains("Alice")
map.filter { (_, v) -> v > 26 }
map.map { (k, v) -> k to v * 2 }     // new map
map.mapValues { (_, v) -> v + 1 }
for ((k, v) in map) println("$k: $v")
```


---

# CHAPTER 4: CONTROL FLOW


## Control Structures

```kotlin
// if (expression — returns value)
val max = if (a > b) a else b

if (x > 0) {
    println("positive")
} else if (x == 0) {
    println("zero")
} else {
    println("negative")
}

// when (pattern matching / switch)
val grade = when (score) {
    in 90..100 -> "A"
    in 80..89  -> "B"
    in 70..79  -> "C"
    else       -> "F"
}

when {
    x < 0    -> println("negative")
    x == 0   -> println("zero")
    else     -> println("positive")
}

when (day) {
    "Monday", "Tuesday" -> println("Early week")
    "Wednesday"          -> println("Mid week")
    "Thursday", "Friday" -> println("Late week")
    else                 -> println("Weekend")
}

// for loop
for (i in 1..10) print("$i ")
for (i in 1 until 10) print("$i ")   // exclusive
for (i in 10 downTo 1) print("$i ")
for (i in 1..10 step 2) print("$i ")
for (item in list) println(item)
for ((index, value) in list.withIndex()) println("$index: $value")
for ((key, value) in map) println("$key -> $value")

// while / do-while
var n = 1
while (n < 100) n *= 2
do { n++ } while (n < 200)

// break / continue with labels
outer@ for (i in 1..10) {
    for (j in 1..10) {
        if (i * j > 50) break@outer
        print("($i,$j) ")
    }
}

// try/catch/finally (expression)
val result = try {
    parseInt("42")
} catch (e: NumberFormatException) {
    -1
} finally {
    println("cleanup")
}

// throw as expression
fun fail(msg: String): Nothing = throw IllegalStateException(msg)
val name = nullableName ?: throw NullPointerException("Name cannot be null")
```


---

# CHAPTER 5: FUNCTIONS


## Functions and Lambdas

```kotlin
// Basic function
fun add(a: Int, b: Int): Int = a + b

// Default parameters
fun greet(name: String, greeting: String = "Hello"): String {
    return "$greeting, $name!"
}
greet("Alice")
greet("Bob", "Hi")
greet(greeting = "Hey", name = "Carol")   // named args

// Varargs
fun sum(vararg nums: Int): Int = nums.sum()
sum(1, 2, 3, 4, 5)
val arr = intArrayOf(1, 2, 3)
sum(*arr)   // spread operator

// Extension functions
fun String.isPalindrome(): Boolean = this == this.reversed()
"racecar".isPalindrome()   // true

fun Int.factorial(): Long = if (this <= 1) 1L else this * (this - 1).factorial()
5.factorial()   // 120

// Higher-order functions
fun apply(f: (Int) -> Int, x: Int) = f(x)
apply({ x -> x * x }, 5)   // 25
apply(::factorial, 5)       // 120 (function reference)

// Lambda syntax
val square = { x: Int -> x * x }
val add2 = { a: Int, b: Int -> a + b }
val greetLambda: (String) -> String = { name -> "Hello, $name!" }

// Trailing lambda (last param)
list.filter { it > 3 }
list.forEach { println(it) }
list.map { it * 2 }

// Inline functions (lambda inlined, no overhead)
inline fun <T> measure(block: () -> T): T {
    val start = System.nanoTime()
    val result = block()
    println("Time: ${System.nanoTime() - start} ns")
    return result
}

// Scope functions
val person = Person("Alice", 30)
val len = person.let { p -> p.name.length }  // transform
val p2 = person.also { p -> println(p.name) } // side effect, returns receiver
val p3 = person.apply { this.age = 31 }       // configure, returns receiver
with(person) {
    println(name)   // this = person
    println(age)
}
person.run {
    println("${name} is ${age}")   // returns last expression
}

// Infix functions
infix fun Int.times(str: String) = str.repeat(this)
3 times "ha"   // "hahaha"
```


---

# CHAPTER 6: CLASSES AND OOP


## Object-Oriented Programming

```kotlin
// Data class (auto equals, hashCode, copy, toString)
data class Person(
    val name: String,
    val age: Int,
    val city: String = "Unknown"
)

val alice = Person("Alice", 30, "NYC")
val older = alice.copy(age = 31)
val (name, age, city) = alice   // destructuring

// Regular class
class Animal(val name: String, val sound: String) {
    var age: Int = 0
        private set

    val isAdult: Boolean get() = age >= 1

    init {
        // initializer block
        println("Created animal: $name")
    }

    open fun speak(): String = "$name says $sound"

    override fun toString() = "Animal($name)"
}

// Inheritance
class Dog(name: String, val breed: String) : Animal(name, "Woof") {
    override fun speak(): String = "${super.speak()}!"
    fun fetch(): String = "$name fetches!"
}

// Interface
interface Printable {
    fun printDescription()
    fun prettyDescription(): String = toString()  // default impl
}

// Abstract class
abstract class Shape {
    abstract val area: Double
    abstract val perimeter: Double
    fun printInfo() = println("Area: $area, Perimeter: $perimeter")
}

class Circle(val radius: Double) : Shape(), Printable {
    override val area get() = Math.PI * radius * radius
    override val perimeter get() = 2 * Math.PI * radius
    override fun printDescription() = println("Circle r=$radius")
}

// Object (singleton)
object Config {
    const val MAX_SIZE = 100
    var debug = false
    fun log(msg: String) = if (debug) println(msg) else Unit
}

// Companion object (static-like)
class MyClass {
    companion object {
        const val TAG = "MyClass"
        fun create(): MyClass = MyClass()
    }
}
MyClass.TAG
MyClass.create()

// Sealed class (restricted hierarchy)
sealed class Result<out T> {
    data class Success<T>(val value: T) : Result<T>()
    data class Failure(val error: Throwable) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

fun handleResult(r: Result<Int>) = when (r) {
    is Result.Success -> println("Got ${r.value}")
    is Result.Failure -> println("Error: ${r.error.message}")
    Result.Loading    -> println("Loading...")
}

// Enum class
enum class Direction(val degrees: Int) {
    NORTH(0), EAST(90), SOUTH(180), WEST(270);
    fun opposite() = values()[(ordinal + 2) % 4]
}
```


---

# CHAPTER 7: GENERICS AND FUNCTIONAL


## Generics

```kotlin
// Generic function
fun <T : Comparable<T>> max(a: T, b: T): T = if (a > b) a else b
max(3, 5)
max("abc", "xyz")

// Generic class
class Box<T>(val value: T) {
    fun map(f: (T) -> T) = Box(f(value))
    override fun toString() = "Box($value)"
}

// Variance
// out T — covariant (producer)
// in T — contravariant (consumer)
interface Producer<out T> { fun produce(): T }
interface Consumer<in T> { fun consume(item: T) }

// Reified type parameters (inline only)
inline fun <reified T> isType(obj: Any) = obj is T
isType<String>("hello")  // true

// Extension functions on generic types
fun <T> List<T>.second(): T = this[1]

// Sequences (lazy)
val seq = generateSequence(1) { it * 2 }
seq.take(10).toList()   // [1,2,4,8,16,32,64,128,256,512]

generateSequence { readLine() }
    .takeWhile { it.isNotEmpty() }
    .forEach { println(it) }

// Destructuring declarations
val (a, b) = Pair(1, 2)
val (x, y, z) = Triple(1, 2, 3)

// Delegation
class Logger(private val delegate: MutableList<String> = mutableListOf()) :
    MutableList<String> by delegate {
    override fun add(element: String): Boolean {
        println("Adding: $element")
        return delegate.add(element)
    }
}

// Lazy delegation
val expensive: String by lazy { "computed once" }

// Observable delegation
var count by Delegates.observable(0) { _, old, new ->
    println("Changed from $old to $new")
}
```


---

# CHAPTER 8: COROUTINES AND ASYNC


## Coroutines

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

// Launch coroutine
fun main() = runBlocking {
    launch {
        delay(100)
        println("World!")
    }
    println("Hello,")
}

// async/await
suspend fun fetchData(): String {
    delay(1000)
    return "data"
}

val result = coroutineScope {
    val a = async { fetchData() }
    val b = async { fetchData() }
    "${a.await()} + ${b.await()}"
}

// Structured concurrency
fun main() = runBlocking {
    val job = launch {
        repeat(5) {
            println("Working $it")
            delay(500)
        }
    }
    delay(1200)
    job.cancel()
    println("Done")
}

// Flow (cold stream)
fun numbersFlow(): Flow<Int> = flow {
    for (i in 1..5) {
        delay(100)
        emit(i)
    }
}

fun main() = runBlocking {
    numbersFlow()
        .map { it * it }
        .filter { it > 5 }
        .collect { println(it) }
}

// StateFlow / SharedFlow (hot streams)
val stateFlow = MutableStateFlow(0)
val sharedFlow = MutableSharedFlow<Int>()

// Channel (buffered communication)
val channel = Channel<Int>(10)
launch { for (i in 1..5) channel.send(i) }
launch { for (msg in channel) println(msg) }

// Dispatcher (thread context)
withContext(Dispatchers.IO) { /* I/O work */ }
withContext(Dispatchers.Default) { /* CPU work */ }
withContext(Dispatchers.Main) { /* UI update */ }
```
