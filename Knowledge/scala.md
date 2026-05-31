# Scala Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH SCALA


## Remarks

Scala is a strong statically-typed, multi-paradigm programming language on the JVM that blends object-oriented and functional programming. Scala 3 (Dotty) is the current major version, introducing cleaner syntax and improved type system. Used widely in big data (Apache Spark), distributed systems (Akka), and backend services.

Tools: scalac compiler, sbt (build tool), Scala CLI, IntelliJ IDEA with Scala plugin.


## Hello World

```scala
// hello.scala
@main def hello(): Unit =
  println("Hello, World!")
  println(s"Hello, ${"Scala"}!")

// Scala 2 style
object Hello extends App {
  println("Hello, World!")
}
```

```bash
scala hello.scala              # Scala CLI
scalac hello.scala && scala Hello  # compile and run
sbt run                        # via sbt
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Types and Variables

```scala
// val = immutable, var = mutable
val name: String = "Alice"
val age: Int = 30
var count = 0          // type inferred
count += 1

// Primitive types
val i: Int = 42
val l: Long = 9_000_000_000L
val d: Double = 3.14
val f: Float = 3.14f
val b: Byte = 127
val s: Short = 1000
val ch: Char = 'A'
val bool: Boolean = true

// String operations
val str = "Hello, World!"
str.length                   // 13
str.toUpperCase
str.toLowerCase
str.substring(0, 5)          // "Hello"
str.contains("World")
str.replace("World", "Scala")
str.split(", ")
str.trim
str.startsWith("Hello")
str.endsWith("!")

// String interpolation
val s1 = s"Name: $name, Age: $age"
val s2 = s"Double: ${age * 2}"
val s3 = f"Pi is ${3.14159}%.2f"    // formatted
val s4 = raw"No \n escape"          // raw string

// Multi-line strings
val text = """
  |Hello
  |World
  """.stripMargin

// Type conversions
"42".toInt
"3.14".toDouble
42.toString
42.toDouble
42L.toInt

// Option (null-safe)
val some: Option[Int] = Some(42)
val none: Option[Int] = None
some.getOrElse(0)      // 42
none.getOrElse(0)      // 0
some.map(_ * 2)        // Some(84)
some.flatMap(x => if x > 0 then Some(x) else None)
for opt <- some yield opt * 2

// Tuples
val t = (1, "hello", 3.14)
t._1; t._2; t._3
val (a, b, c) = t   // destructuring
```


---

# CHAPTER 3: COLLECTIONS


## Collections

```scala
// List (immutable linked list)
val list = List(1, 2, 3, 4, 5)
val list2 = 0 :: list        // prepend: List(0,1,2,3,4,5)
val list3 = list :+ 6        // append: List(1,2,3,4,5,6)
val combined = list ++ list2 // concatenate

list.head      // 1
list.tail      // List(2,3,4,5)
list.last      // 5
list.init      // List(1,2,3,4)
list.length    // 5
list(2)        // 3 (index)

list.map(_ * 2)
list.filter(_ % 2 == 0)
list.filterNot(_ % 2 == 0)
list.find(_ > 3)         // Some(4)
list.exists(_ > 3)       // true
list.forall(_ > 0)       // true
list.count(_ % 2 == 0)   // 2
list.sum; list.product
list.sorted
list.sortBy(-_)          // descending
list.reverse
list.take(3)             // List(1,2,3)
list.drop(2)             // List(3,4,5)
list.takeWhile(_ < 4)    // List(1,2,3)
list.dropWhile(_ < 4)    // List(4,5)
list.flatten             // flatten nested
list.flatMap(x => List(x, x*2))
list.foldLeft(0)(_ + _)  // reduce left
list.foldRight(0)(_ + _) // reduce right
list.reduce(_ + _)
list.zip(list.map(_ * 10))  // List((1,10),(2,20)...)
list.zipWithIndex
list.grouped(2).toList    // List(List(1,2),List(3,4),List(5))
list.sliding(3).toList

// Vector (immutable indexed)
val v = Vector(1, 2, 3, 4, 5)
v(2)      // O(log n) access
v.updated(2, 99)   // returns new vector

// Map (immutable)
val m = Map("Alice" -> 30, "Bob" -> 25, "Carol" -> 35)
m("Alice")                    // 30
m.get("Alice")                // Some(30)
m.getOrElse("Dave", 0)        // 0
m + ("Dave" -> 28)            // add entry
m - "Bob"                     // remove entry
m.keys; m.values
m.contains("Alice")
for (k, v) <- m do println(s"$k: $v")
m.map((k, v) => k -> v * 2)
m.filter((_, v) => v > 26)

// Set (immutable)
val s = Set(1, 2, 3, 2, 1)   // Set(1,2,3)
s + 4; s - 1
s.contains(2)
s union Set(3, 4, 5)
s intersect Set(2, 3, 7)
s diff Set(2, 3)

// Mutable collections
import scala.collection.mutable
val buf = mutable.ListBuffer[Int]()
buf += 1; buf += 2; buf ++= List(3, 4)
buf.remove(0)

val mmap = mutable.HashMap[String, Int]()
mmap("key") = 42
mmap.getOrElseUpdate("other", 0)
```


---

# CHAPTER 4: CONTROL FLOW


## Control Structures

```scala
// if/else (expression — returns value)
val x = 10
val label = if x > 0 then "positive" else "non-positive"

if x > 0 then
  println("positive")
else if x == 0 then
  println("zero")
else
  println("negative")

// match (pattern matching)
val day = "Monday"
val kind = day match
  case "Saturday" | "Sunday" => "Weekend"
  case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday" => "Weekday"
  case _ => "Unknown"

// match with guards
val n = 42
n match
  case x if x < 0   => println("negative")
  case 0             => println("zero")
  case x if x < 10  => println("small positive")
  case x             => println(s"large: $x")

// match on types
def describe(x: Any): String = x match
  case i: Int    => s"Integer: $i"
  case s: String => s"String: $s"
  case d: Double => s"Double: $d"
  case _         => "Unknown"

// for comprehension
for i <- 1 to 10 do print(s"$i ")
for i <- 1 to 10 by 2 do print(s"$i ")

// for with filter
for
  i <- 1 to 10
  if i % 2 == 0
do println(i)

// for yield (produces collection)
val squares = for i <- 1 to 10 yield i * i
val pairs   = for
  i <- 1 to 3
  j <- 1 to 3
  if i != j
yield (i, j)

// while
var m = 1
while m < 100 do
  m *= 2
println(m)

// try/catch/finally
try
  val result = 10 / 0
catch
  case e: ArithmeticException => println(s"Math error: ${e.getMessage}")
  case e: Exception            => println(s"Error: ${e.getMessage}")
finally
  println("cleanup")
```


---

# CHAPTER 5: FUNCTIONS AND FUNCTIONAL PROGRAMMING


## Functional Programming

```scala
// Basic function
def add(a: Int, b: Int): Int = a + b

// Default parameters
def greet(name: String, greeting: String = "Hello"): String =
  s"$greeting, $name!"

// Named arguments
greet(greeting = "Hi", name = "Alice")

// Varargs
def sum(nums: Int*): Int = nums.sum
sum(1, 2, 3, 4, 5)

// Higher-order functions
def apply(f: Int => Int, x: Int): Int = f(x)
apply(x => x * x, 5)   // 25

def twice(f: Int => Int): Int => Int = x => f(f(x))
twice(_ + 1)(5)   // 7

// Anonymous functions
val square: Int => Int = x => x * x
val add2: (Int, Int) => Int = (a, b) => a + b
val isEven = (n: Int) => n % 2 == 0

// Partial application
def multiply(x: Int)(y: Int): Int = x * y
val triple = multiply(3)  // curried
triple(5)   // 15

// Function composition
val double = (x: Int) => x * 2
val inc    = (x: Int) => x + 1
val doubleInc = double andThen inc
val incDouble = double compose inc
doubleInc(5)   // 11
incDouble(5)   // 12

// Tail recursion
import scala.annotation.tailrec
@tailrec
def factorial(n: Long, acc: Long = 1): Long =
  if n <= 1 then acc
  else factorial(n - 1, n * acc)

// Recursion with pattern matching
def fib(n: Int): Int = n match
  case 0 => 0
  case 1 => 1
  case n => fib(n-1) + fib(n-2)

// Option operations (monadic)
def divide(a: Int, b: Int): Option[Double] =
  if b == 0 then None else Some(a.toDouble / b)

val result = for
  x <- divide(10, 2)
  y <- divide(x.toInt, 2)
yield y + 1

// Either
def parse(s: String): Either[String, Int] =
  try Right(s.toInt)
  catch case _ => Left(s"Cannot parse: $s")

parse("42")    // Right(42)
parse("abc")   // Left("Cannot parse: abc")
```


---

# CHAPTER 6: CASE CLASSES AND TRAITS


## OOP and ADTs

```scala
// Case class (immutable, structural equality, pattern matching)
case class Person(name: String, age: Int, city: String = "Unknown")

val alice = Person("Alice", 30, "NYC")
val bob   = Person("Bob", 25)

alice.name    // "Alice"
alice.copy(age = 31)   // create modified copy
alice == Person("Alice", 30, "NYC")  // true (structural)

// Pattern matching on case class
def greetPerson(p: Person): String = p match
  case Person(name, age, _) if age < 30 => s"Young $name"
  case Person(name, _, city) => s"$name from $city"

// Sealed trait + case classes (ADT)
sealed trait Shape
case class Circle(radius: Double)           extends Shape
case class Rectangle(width: Double, height: Double) extends Shape
case class Triangle(base: Double, height: Double)   extends Shape

def area(s: Shape): Double = s match
  case Circle(r)        => math.Pi * r * r
  case Rectangle(w, h)  => w * h
  case Triangle(b, h)   => 0.5 * b * h

// Traits (like interfaces with default methods)
trait Animal:
  def name: String
  def speak(): String
  def describe(): String = s"$name says: ${speak()}"

trait Domestic:
  def owner: String

class Dog(val name: String, val owner: String)
    extends Animal with Domestic:
  def speak(): String = "Woof!"
  override def describe(): String = s"Dog $name owned by $owner"

// Abstract class
abstract class Vehicle(val make: String):
  def maxSpeed: Double
  def describe(): String = s"$make going up to $maxSpeed km/h"

class Car(make: String, val maxSpeed: Double) extends Vehicle(make)

// Companion object (static methods)
object Person:
  def fromString(s: String): Option[Person] =
    s.split(",") match
      case Array(n, a) => Some(Person(n.trim, a.trim.toInt))
      case _ => None

  val anonymous = Person("Anonymous", 0)

Person.fromString("Alice, 30")
Person.anonymous

// Enum (Scala 3)
enum Direction:
  case North, South, East, West

enum Color(val hex: String):
  case Red   extends Color("#FF0000")
  case Green extends Color("#00FF00")
  case Blue  extends Color("#0000FF")
```


---

# CHAPTER 7: IMPLICITS AND TYPE CLASSES


## Advanced Type System

```scala
// Extension methods (Scala 3)
extension (s: String)
  def isPalindrome: Boolean = s == s.reverse
  def wordCount: Int = s.split("\\s+").length

"racecar".isPalindrome   // true
"Hello World".wordCount  // 2

// Type classes
trait Show[A]:
  def show(a: A): String

object Show:
  given Show[Int]    with def show(n: Int) = n.toString
  given Show[String] with def show(s: String) = s""""$s""""
  given Show[Boolean] with def show(b: Boolean) = if b then "true" else "false"

  def apply[A](using s: Show[A]): Show[A] = s

def printShow[A: Show](a: A): Unit =
  println(summon[Show[A]].show(a))

printShow(42)
printShow("hello")

// Generic programming with type bounds
def max[A: Ordering](a: A, b: A): A =
  if summon[Ordering[A]].lt(a, b) then b else a

max(3, 5)
max("abc", "xyz")

// Implicit conversions (use sparingly)
given Conversion[String, Int] = _.length

// Context functions
type Env[A] = Map[String, String] ?=> A
def getConfig(key: String): Env[Option[String]] =
  summon[Map[String, String]].get(key)

// Higher-kinded types
trait Functor[F[_]]:
  def map[A, B](fa: F[A])(f: A => B): F[B]

given Functor[Option] with
  def map[A, B](fa: Option[A])(f: A => B): Option[B] = fa.map(f)

given Functor[List] with
  def map[A, B](fa: List[A])(f: A => B): List[B] = fa.map(f)
```


---

# CHAPTER 8: CONCURRENCY AND EFFECTS


## Futures and Effect Systems

```scala
import scala.concurrent.{Future, Await}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration._

// Future
val f1 = Future { Thread.sleep(100); 42 }
val f2 = Future { Thread.sleep(50); "hello" }

// Map and flatMap
val result = f1.map(_ * 2)
val chained = f1.flatMap(n => Future { n.toString })

// for comprehension with futures
val combined = for
  n <- f1
  s <- f2
yield s"$s: $n"

combined.foreach(println)

// Future.sequence
val futures = List(Future(1), Future(2), Future(3))
val all = Future.sequence(futures)   // Future[List[Int]]

// Error handling
val safe = Future { 10 / 0 }
  .recover { case e: ArithmeticException => -1 }

safe.failed.foreach(e => println(s"Error: $e"))

// Await (blocking — use sparingly)
val value = Await.result(f1, 5.seconds)
println(value)   // 42

// Promise
import scala.concurrent.Promise
val p = Promise[Int]()
Future { Thread.sleep(100); p.success(42) }
val pf = p.future
pf.foreach(println)

// Cats Effect / ZIO (popular effect libraries)
// import cats.effect._
// object App extends IOApp.Simple:
//   def run: IO[Unit] =
//     IO.println("Hello from Cats Effect!")
```
