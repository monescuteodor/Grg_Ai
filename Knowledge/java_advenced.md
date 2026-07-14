# Java Advanced Complete Reference


---

# CHAPTER 1: MODERN JAVA


## Remarks

Java powers enterprise backends, Android apps, big data (Hadoop, Spark), and high-frequency trading systems. Modern Java (17+) is dramatically cleaner than old Java — records, sealed classes, pattern matching, and virtual threads have transformed the language. The JVM's JIT compiler makes Java surprisingly fast — often within 10-20% of C++ for long-running processes.

Key concepts: **Streams API** (functional data processing), **Generics** (type-safe collections), **Records** (immutable data classes), **Sealed classes** (restricted inheritance), **Virtual threads** (lightweight concurrency), **Optional** (null safety), **CompletableFuture** (async programming), **Modules** (encapsulation at package level).


## Records and Modern Data Classes

```java
// OLD: boilerplate nightmare
public class User {
    private final String name;
    private final int age;
    
    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }
    public String getName() { return name; }
    public int getAge() { return age; }
    public boolean equals(Object o) { /* ... 10 lines ... */ }
    public int hashCode() { /* ... */ }
    public String toString() { return "User[name=" + name + ", age=" + age + "]"; }
}

// MODERN (Java 16+): one line!
public record User(String name, int age) {}
// Auto-generates: constructor, getters, equals, hashCode, toString
// Immutable by default!

var user = new User("Alice", 30);
System.out.println(user.name());   // "Alice"
System.out.println(user);          // User[name=Alice, age=30]

// Record with validation
public record Email(String value) {
    public Email {
        if (!value.contains("@"))
            throw new IllegalArgumentException("Invalid email: " + value);
    }
}

// Sealed classes (Java 17+): restrict who can extend
public sealed interface Shape permits Circle, Rectangle, Triangle {}
public record Circle(double radius) implements Shape {}
public record Rectangle(double width, double height) implements Shape {}
public record Triangle(double a, double b, double c) implements Shape {}

// Pattern matching (Java 21+)
public double area(Shape shape) {
    return switch (shape) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.width() * r.height();
        case Triangle t -> {
            double s = (t.a() + t.b() + t.c()) / 2;
            yield Math.sqrt(s * (s-t.a()) * (s-t.b()) * (s-t.c()));
        }
    };  // Compiler ensures ALL cases handled!
}
```


## Streams API

```java
import java.util.*;
import java.util.stream.*;

List<User> users = List.of(
    new User("Alice", 30, "Engineering"),
    new User("Bob", 25, "Sales"),
    new User("Carol", 35, "Engineering"),
    new User("Dave", 28, "Sales"),
    new User("Eve", 32, "Engineering")
);

// Filter + Map + Collect
List<String> engineerNames = users.stream()
    .filter(u -> u.department().equals("Engineering"))
    .map(User::name)
    .sorted()
    .collect(Collectors.toList());
// ["Alice", "Carol", "Eve"]

// Grouping
Map<String, List<User>> byDept = users.stream()
    .collect(Collectors.groupingBy(User::department));

// Average age per department
Map<String, Double> avgAge = users.stream()
    .collect(Collectors.groupingBy(
        User::department,
        Collectors.averagingInt(User::age)
    ));

// Any/All/None match
boolean hasMinors = users.stream().anyMatch(u -> u.age() < 18);
boolean allAdults = users.stream().allMatch(u -> u.age() >= 18);

// Reduce
int totalAge = users.stream()
    .mapToInt(User::age)
    .sum();

// Chaining operations
String report = users.stream()
    .filter(u -> u.age() > 25)
    .sorted(Comparator.comparing(User::name))
    .map(u -> u.name() + " (" + u.age() + ")")
    .collect(Collectors.joining(", "));
// "Alice (30), Carol (35), Dave (28), Eve (32)"

// Parallel streams (automatic multi-threading!)
long count = hugeList.parallelStream()
    .filter(item -> expensiveCheck(item))
    .count();
```


## Optional (Null Safety)

```java
// OLD: NullPointerException everywhere
String city = user.getAddress().getCity().toUpperCase();
// If user, address, or city is null → NPE!

// MODERN: Optional chains
Optional<String> city = Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .map(String::toUpperCase);

String result = city.orElse("Unknown");
city.ifPresent(c -> System.out.println("City: " + c));

// Creating Optional
Optional<String> present = Optional.of("hello");
Optional<String> empty = Optional.empty();
Optional<String> nullable = Optional.ofNullable(mayBeNull);

// Chaining
Optional<User> user = findUser(id);
String email = user
    .filter(u -> u.isActive())
    .map(User::getEmail)
    .orElseThrow(() -> new NotFoundException("User " + id));
```


---

# CHAPTER 2: CONCURRENCY


## Virtual Threads (Java 21+)

```java
// OLD: Platform threads (1 thread = 1 OS thread, ~1MB stack each)
// 10,000 threads = 10 GB RAM!
ExecutorService executor = Executors.newFixedThreadPool(100);

// MODERN: Virtual threads (millions possible, ~1KB each)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 100_000; i++) {
        executor.submit(() -> {
            // Each task gets its own virtual thread
            var response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            process(response);
        });
    }
}
// 100,000 concurrent HTTP requests. No thread pool tuning!

// Simple virtual thread
Thread.startVirtualThread(() -> {
    System.out.println("Running in virtual thread!");
});

// CompletableFuture (async composition)
CompletableFuture<User> userFuture = CompletableFuture
    .supplyAsync(() -> fetchUser(userId))
    .thenApply(user -> enrichWithProfile(user))
    .thenApply(user -> addPermissions(user))
    .exceptionally(ex -> {
        log.error("Failed: " + ex.getMessage());
        return defaultUser();
    });

// Combine multiple async operations
CompletableFuture<Void> allDone = CompletableFuture.allOf(
    fetchUsers(),
    fetchOrders(),
    fetchProducts()
);
allDone.join();  // Wait for ALL to complete
```


---

# CHAPTER 3: COMMON PITFALLS

```
PITFALL 1: Mutable collections returned from methods
  return this.items;  → caller can modify internal state!
  Fix: return Collections.unmodifiableList(items); or List.copyOf(items);

PITFALL 2: Using == instead of .equals() for strings
  "hello" == new String("hello")  → false (comparing references!)
  Fix: "hello".equals(other)  (always use .equals for objects)

PITFALL 3: Catching Exception (too broad)
  catch (Exception e) { }  → swallows everything including bugs.
  Fix: catch specific exceptions. Never catch and ignore.

PITFALL 4: Ignoring stream laziness
  stream.filter(...).peek(System.out::println);  → nothing happens!
  Streams are lazy. Need terminal operation (.collect, .forEach, .count).

PITFALL 5: Modifying collection while iterating
  for (Item i : list) { list.remove(i); }  → ConcurrentModificationException
  Fix: list.removeIf(i -> condition);  or use Iterator.remove()

PITFALL 6: Not closing resources
  Connection conn = getConnection();  → leaked if exception.
  Fix: try (var conn = getConnection()) { ... }  (try-with-resources)

PITFALL 7: Synchronized on wrong object
  synchronized("lock") { }  → string literals are shared across JVM!
  Fix: private final Object lock = new Object(); synchronized(lock) { }

PITFALL 8: HashMap with mutable keys
  If key object changes after insertion → can't find it anymore.
  Fix: use immutable keys (String, Integer, records).
```