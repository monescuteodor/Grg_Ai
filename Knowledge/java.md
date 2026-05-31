# Java Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH JAVA


## Remarks

Java is a strongly typed, object-oriented, compiled-to-bytecode language running on the JVM. "Write once, run anywhere." Java 21 LTS is the current long-term support release. Features: garbage collection, generics, lambdas, streams, modules.

Tools: JDK (OpenJDK, Adoptium), Maven, Gradle, IntelliJ IDEA, Eclipse.


## Hello World

```java
// HelloWorld.java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        System.out.printf("Hello, %s!%n", "Java");
    }
}
```

```bash
javac HelloWorld.java
java HelloWorld

# Single-file (Java 11+)
java HelloWorld.java
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Primitive Types

```java
// Primitives
byte    b  = 127;
short   s  = 32767;
int     n  = 2147483647;
long    l  = 9223372036854775807L;
float   f  = 3.14f;
double  d  = 3.14159265358979;
boolean ok = true;
char    c  = 'A';

// Literals
int hex  = 0xFF;
int bin  = 0b1010;
long big = 1_000_000L;       // underscores allowed

// Wrapper classes (autoboxing)
Integer boxed = 42;          // autobox int -> Integer
int unboxed   = boxed;       // unbox
Integer.parseInt("42");      // 42
Integer.MAX_VALUE;           // 2147483647

// var (type inference, Java 10+)
var text = "Hello";          // inferred as String
var list = new ArrayList<>();

// String
String str = "Hello";
str.length()                 // 5
str.charAt(0)                // 'H'
str.substring(1, 4)          // "ell"
str.toLowerCase()
str.toUpperCase()
str.contains("ell")          // true
str.replace("l", "L")
str.split(",")
str.trim()
str.strip()                  // also removes Unicode whitespace
str.isBlank()                // true if empty or whitespace
String.format("Name: %s, Age: %d", name, age)

// String + (StringBuilder for loops)
StringBuilder sb = new StringBuilder();
sb.append("Hello");
sb.append(", World");
String result = sb.toString();

// Text blocks (Java 15+)
String json = """
    {
        "name": "Alice",
        "age": 30
    }
    """;
```


---

# CHAPTER 3: CONTROL FLOW


## Conditionals and Loops

```java
// if/else
if (x > 0) {
    System.out.println("positive");
} else if (x == 0) {
    System.out.println("zero");
} else {
    System.out.println("negative");
}

// Ternary
String label = x > 0 ? "pos" : "non-pos";

// switch statement
switch (day) {
    case "MON": case "TUE":
        System.out.println("weekday"); break;
    default:
        System.out.println("other");
}

// switch expression (Java 14+)
String result = switch (day) {
    case "MON", "TUE", "WED", "THU", "FRI" -> "Weekday";
    case "SAT", "SUN" -> "Weekend";
    default -> throw new IllegalArgumentException("Unknown: " + day);
};

// for
for (int i = 0; i < 10; i++) {
    if (i == 5) break;
    if (i % 2 == 0) continue;
    System.out.println(i);
}

// enhanced for
int[] arr = {1, 2, 3, 4, 5};
for (int item : arr) System.out.println(item);

// while / do-while
int n = 10;
while (n > 0) n--;

do {
    System.out.println(n);
    n++;
} while (n < 5);
```


---

# CHAPTER 4: ARRAYS AND COLLECTIONS


## Arrays

```java
// Array declaration and init
int[] arr = new int[5];
int[] arr2 = {1, 2, 3, 4, 5};
String[] names = {"Alice", "Bob"};

// Multi-dimensional
int[][] matrix = new int[3][3];
int[][] grid = {{1,2,3},{4,5,6},{7,8,9}};

// Arrays utility
import java.util.Arrays;
Arrays.sort(arr);
Arrays.fill(arr, 0);
Arrays.copyOf(arr, 10);
Arrays.binarySearch(arr, 3);
System.out.println(Arrays.toString(arr));
```

## Collections Framework

```java
import java.util.*;

// ArrayList
List<String> list = new ArrayList<>();
list.add("Alice");
list.add(0, "Bob");     // insert at index
list.get(0);
list.set(0, "Carol");
list.remove(0);
list.size();
list.contains("Alice");
list.sort(Comparator.naturalOrder());
Collections.sort(list);
Collections.reverse(list);
Collections.shuffle(list);

// LinkedList
Deque<Integer> deque = new LinkedList<>();
deque.addFirst(1);
deque.addLast(2);
deque.peekFirst();
deque.pollLast();

// HashMap
Map<String, Integer> map = new HashMap<>();
map.put("one", 1);
map.get("one");
map.getOrDefault("missing", 0);
map.containsKey("one");
map.remove("one");
map.putIfAbsent("one", 1);
map.computeIfAbsent("two", k -> k.length());

for (Map.Entry<String, Integer> e : map.entrySet()) {
    System.out.println(e.getKey() + "=" + e.getValue());
}

// TreeMap (sorted)
Map<String, Integer> sorted = new TreeMap<>(map);

// HashSet
Set<String> set = new HashSet<>();
set.add("a"); set.add("b");
set.contains("a");
set.remove("a");

// Queue / PriorityQueue
Queue<Integer> pq = new PriorityQueue<>();
pq.offer(3); pq.offer(1); pq.offer(2);
pq.poll();   // 1 (min)
pq.peek();   // peek without remove
```


---

# CHAPTER 5: OBJECT-ORIENTED PROGRAMMING


## Classes and Inheritance

```java
// Class with encapsulation
public class Animal {
    private String name;
    private String sound;
    protected int age;

    public Animal(String name, String sound) {
        this.name = name;
        this.sound = sound;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String speak() {
        return name + " says " + sound;
    }

    @Override
    public String toString() {
        return "Animal(" + name + ")";
    }

    // Static factory
    public static Animal create(String name, String sound) {
        return new Animal(name, sound);
    }
}

// Inheritance
public class Dog extends Animal {
    private String breed;

    public Dog(String name, String breed) {
        super(name, "Woof");
        this.breed = breed;
    }

    @Override
    public String speak() {
        return super.speak() + "!";
    }

    public String fetch() {
        return getName() + " fetches!";
    }
}

// Interface
public interface Flyable {
    double MAX_HEIGHT = 10000.0;   // implicitly public static final

    void fly();
    default void land() { System.out.println("Landing..."); }
    static Flyable create() { return () -> System.out.println("Flying!"); }
}

// Abstract class
public abstract class Shape {
    public abstract double area();
    public abstract double perimeter();

    public void describe() {
        System.out.printf("Area=%.2f, Perimeter=%.2f%n", area(), perimeter());
    }
}

// Record (Java 16+)
public record Point(double x, double y) {
    // compact canonical constructor
    Point {
        if (Double.isNaN(x) || Double.isNaN(y))
            throw new IllegalArgumentException("NaN not allowed");
    }

    public double distance(Point other) {
        double dx = this.x - other.x;
        double dy = this.y - other.y;
        return Math.sqrt(dx*dx + dy*dy);
    }
}

// Sealed class (Java 17+)
public sealed class Result<T> permits Result.Ok, Result.Err {
    public record Ok<T>(T value) extends Result<T> {}
    public record Err<T>(String message) extends Result<T> {}
}
```


---

# CHAPTER 6: GENERICS AND FUNCTIONAL


## Generics and Lambdas

```java
import java.util.function.*;
import java.util.stream.*;

// Generic class
public class Pair<A, B> {
    private final A first;
    private final B second;

    public Pair(A first, B second) {
        this.first = first; this.second = second;
    }

    public A getFirst() { return first; }
    public B getSecond() { return second; }
}

// Generic method
public static <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) >= 0 ? a : b;
}

// Functional interfaces
Function<String, Integer> len = String::length;
Predicate<Integer> isEven = n -> n % 2 == 0;
Supplier<List<String>> listFactory = ArrayList::new;
Consumer<String> printer = System.out::println;
BiFunction<Integer, Integer, Integer> add = Integer::sum;

// Method references
List<String> names = List.of("Alice", "Bob", "Carol");
names.stream()
     .map(String::toUpperCase)
     .forEach(System.out::println);

// Streams
List<Integer> nums = List.of(1,2,3,4,5,6,7,8,9,10);

int sum = nums.stream()
    .filter(n -> n % 2 == 0)
    .mapToInt(Integer::intValue)
    .sum();

List<String> result = nums.stream()
    .filter(n -> n > 5)
    .map(n -> "num" + n)
    .sorted()
    .collect(Collectors.toList());

// Collectors
Map<Boolean, List<Integer>> partitioned =
    nums.stream().collect(Collectors.partitioningBy(n -> n % 2 == 0));

Map<String, Long> grouped =
    names.stream().collect(Collectors.groupingBy(s -> s.substring(0,1), Collectors.counting()));

// Optional
Optional<String> opt = Optional.of("hello");
opt.isPresent()
opt.get()
opt.orElse("default")
opt.orElseGet(() -> "computed default")
opt.map(String::toUpperCase)
opt.filter(s -> s.length() > 3)
opt.ifPresent(System.out::println)
```


---

# CHAPTER 7: EXCEPTIONS AND I/O


## Exception Handling

```java
// try-catch-finally
try {
    int result = 10 / 0;
    String s = null;
    s.length();
} catch (ArithmeticException e) {
    System.out.println("Math error: " + e.getMessage());
} catch (NullPointerException e) {
    System.out.println("Null pointer: " + e.getMessage());
} catch (Exception e) {
    e.printStackTrace();
} finally {
    System.out.println("Always runs");
}

// try-with-resources (AutoCloseable)
try (var reader = new BufferedReader(new FileReader("file.txt"));
     var writer = new FileWriter("out.txt")) {
    String line;
    while ((line = reader.readLine()) != null) {
        writer.write(line + "\n");
    }
} catch (IOException e) {
    e.printStackTrace();
}

// Custom exception
public class AppException extends RuntimeException {
    private final int code;
    public AppException(String msg, int code) {
        super(msg);
        this.code = code;
    }
    public int getCode() { return code; }
}

// File I/O with NIO
import java.nio.file.*;
import java.nio.charset.StandardCharsets;

Path p = Path.of("data.txt");
String content = Files.readString(p, StandardCharsets.UTF_8);
List<String> lines = Files.readAllLines(p);
Files.writeString(p, "content\n", StandardOpenOption.APPEND);
Files.copy(src, dst, StandardCopyOption.REPLACE_EXISTING);
Files.createDirectories(Path.of("a/b/c"));
try (var stream = Files.list(Path.of("."))) {
    stream.filter(f -> f.toString().endsWith(".java"))
          .forEach(System.out::println);
}
```


---

# CHAPTER 8: CONCURRENCY


## Threads and Executors

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

// Thread
Thread t = new Thread(() -> System.out.println("Hello from thread"));
t.start();
t.join();

// ExecutorService
ExecutorService ex = Executors.newFixedThreadPool(4);
Future<Integer> future = ex.submit(() -> {
    Thread.sleep(100);
    return 42;
});
int result = future.get(1, TimeUnit.SECONDS);
ex.shutdown();

// CompletableFuture
CompletableFuture<String> cf = CompletableFuture
    .supplyAsync(() -> "hello")
    .thenApply(String::toUpperCase)
    .thenCompose(s -> CompletableFuture.completedFuture(s + "!"));

// Atomic
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();
counter.compareAndSet(1, 2);

// synchronized
class SafeCounter {
    private int count = 0;
    public synchronized void increment() { count++; }
    public synchronized int get() { return count; }
}

// ReentrantLock
import java.util.concurrent.locks.*;
Lock lock = new ReentrantLock();
lock.lock();
try { /* critical section */ }
finally { lock.unlock(); }

// Virtual threads (Java 21)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> System.out.println("Virtual thread!"));
}
```
