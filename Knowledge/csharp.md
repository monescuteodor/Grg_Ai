# C# Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH C#


## Remarks

C# is a strongly typed, object-oriented language developed by Microsoft for the .NET platform. It supports functional, generic, async, and component-oriented programming. C# 12 (.NET 8) is the current version.

Tools: .NET SDK, Visual Studio, VS Code with C# Dev Kit, Rider.


## Hello World

```csharp
// Program.cs (top-level, C# 10+)
Console.WriteLine("Hello, World!");
Console.WriteLine($"Hello, {Environment.UserName}!");

// Classic form
using System;
class Program {
    static void Main(string[] args) {
        Console.WriteLine("Hello!");
    }
}
```

```bash
dotnet new console -n MyApp
cd MyApp
dotnet run
dotnet build
dotnet publish -c Release
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Types

```csharp
// Value types
int    n   = 42;
long   l   = 9_223_372_036_854_775_807L;
double d   = 3.14159265358979;
float  f   = 3.14f;
decimal dec = 9.99m;       // high precision (financial)
bool   b   = true;
char   c   = 'A';
byte   by  = 255;

// Nullable value types
int? maybeInt = null;
maybeInt ?? -1   // -1 (nullish coalescing)
maybeInt?.ToString()  // null if maybeInt is null

// var — type inference
var text = "Hello";
var list = new List<int>();

// string
string s = "Hello, World!";
s.Length         // 13
s.ToUpper()
s.ToLower()
s.Substring(0, 5)
s.Contains("World")
s.StartsWith("Hello")
s.Replace("World", "C#")
s.Split(',')
s.Trim()
string.IsNullOrEmpty(s)
string.IsNullOrWhiteSpace(s)
string.Join(", ", new[] {"a","b","c"})

// String interpolation
string name = "Alice";
string msg = $"Hello, {name}! Today is {DateTime.Now:dddd}.";

// Verbatim string
string path = @"C:\Users\Alice\Documents";

// Raw string literal (C# 11+)
string json = """
    {
        "name": "Alice"
    }
    """;
```


---

# CHAPTER 3: CONTROL FLOW


## Flow Control

```csharp
// if/else
if (x > 0) { Console.WriteLine("positive"); }
else if (x == 0) { Console.WriteLine("zero"); }
else { Console.WriteLine("negative"); }

// Ternary
string label = x > 0 ? "positive" : "non-positive";

// switch expression (C# 8+)
string result = x switch {
    > 0  => "positive",
    0    => "zero",
    < 0  => "negative",
    _    => "unknown"
};

// Pattern matching switch
object obj = 42;
string desc = obj switch {
    int n when n > 100 => "large int",
    int n              => $"int: {n}",
    string s           => $"string: {s}",
    null               => "null",
    _                  => "other"
};

// for / foreach
for (int i = 0; i < 10; i++) Console.WriteLine(i);

foreach (var item in collection) {
    Console.WriteLine(item);
}

// while
while (condition) { /* ... */ }

// LINQ (Language Integrated Query)
var nums = new[] {1,2,3,4,5,6,7,8,9,10};

var evens = from n in nums
            where n % 2 == 0
            select n * n;

// Method syntax (preferred)
var result2 = nums
    .Where(n => n % 2 == 0)
    .Select(n => n * n)
    .OrderByDescending(n => n)
    .Take(3)
    .ToList();

int total = nums.Sum();
double avg = nums.Average();
int max = nums.Max();
var grouped = nums.GroupBy(n => n % 3);
bool any = nums.Any(n => n > 8);
bool all = nums.All(n => n > 0);
```


---

# CHAPTER 4: CLASSES AND OOP


## Object-Oriented Programming

```csharp
// Class
public class Animal {
    private string _name;
    public string Sound { get; init; }   // init-only setter (C# 9)

    public string Name {
        get => _name;
        set => _name = value ?? throw new ArgumentNullException();
    }

    public Animal(string name, string sound) {
        Name = name;
        Sound = sound;
    }

    public virtual string Speak() => $"{Name} says {Sound}";

    public override string ToString() => $"Animal({Name})";
}

// Inheritance
public class Dog : Animal {
    public string Breed { get; }

    public Dog(string name, string breed) : base(name, "Woof") {
        Breed = breed;
    }

    public override string Speak() => base.Speak() + "!";
}

// Record (C# 9+) — immutable by default
public record Point(double X, double Y) {
    public double Distance(Point other) =>
        Math.Sqrt(Math.Pow(X-other.X,2) + Math.Pow(Y-other.Y,2));
}

// Record with mutation
var p1 = new Point(3, 4);
var p2 = p1 with { X = 0 };   // non-destructive mutation

// Interface
public interface IFlyable {
    void Fly();
    void Land() => Console.WriteLine("Landing...");   // default implementation
}

// Abstract class
public abstract class Shape {
    public abstract double Area { get; }
    public abstract double Perimeter { get; }
    public void Describe() => Console.WriteLine($"Area={Area:F2}");
}

// Struct (value type)
public struct Color {
    public byte R, G, B;
    public Color(byte r, byte g, byte b) { R=r; G=g; B=b; }
    public static readonly Color Red = new(255, 0, 0);
}

// Sealed class (no inheritance)
public sealed class Singleton {
    private static Singleton? _instance;
    private Singleton() {}
    public static Singleton Instance => _instance ??= new Singleton();
}
```


---

# CHAPTER 5: GENERICS AND COLLECTIONS


## Generic Types

```csharp
using System.Collections.Generic;

// Generic class
public class Stack<T> {
    private readonly List<T> _items = new();
    public void Push(T item) => _items.Add(item);
    public T Pop() { var item = _items[^1]; _items.RemoveAt(_items.Count-1); return item; }
    public T Peek() => _items[^1];
    public bool IsEmpty => _items.Count == 0;
}

// Generic method with constraint
public T Max<T>(T a, T b) where T : IComparable<T>
    => a.CompareTo(b) >= 0 ? a : b;

// Constraints: class, struct, new(), IInterface, BaseClass

// Collections
List<int> list = new() { 1, 2, 3 };
list.Add(4); list.Remove(2); list.Sort();
list[0]; list.Count; list.Contains(3);
list.AddRange(new[] { 5, 6 });

Dictionary<string, int> dict = new() {
    ["one"] = 1, ["two"] = 2
};
dict.TryGetValue("one", out int val);
dict.GetValueOrDefault("missing", 0);
dict.ContainsKey("one");

HashSet<int> set = new() { 1, 2, 3 };
set.Add(4); set.Remove(1);
set.UnionWith(new[] { 5, 6 });
set.IntersectWith(other);
set.ExceptWith(other);

Queue<int> q = new(); q.Enqueue(1); q.Dequeue(); q.Peek();
Stack<int> stk = new(); stk.Push(1); stk.Pop();

// IEnumerable / IEnumerator (yield)
public IEnumerable<int> Fibonacci() {
    int a = 0, b = 1;
    while (true) {
        yield return a;
        (a, b) = (b, a + b);
    }
}

var fibs = Fibonacci().Take(10).ToArray();
```


---

# CHAPTER 6: ASYNC/AWAIT AND TASKS


## Asynchronous Programming

```csharp
using System.Threading.Tasks;
using System.Net.Http;

// async method returns Task or Task<T>
async Task<string> FetchDataAsync(string url) {
    using var client = new HttpClient();
    string content = await client.GetStringAsync(url);
    return content;
}

// await multiple
async Task FetchAllAsync() {
    var tasks = new[] {
        FetchDataAsync("https://api1.com"),
        FetchDataAsync("https://api2.com"),
    };
    string[] results = await Task.WhenAll(tasks);
}

// Task.WhenAny — first to complete
Task<string> first = await Task.WhenAny(tasks);

// ConfigureAwait
await SomeAsync().ConfigureAwait(false);  // avoid deadlocks in sync contexts

// CancellationToken
async Task LongOperationAsync(CancellationToken ct = default) {
    for (int i = 0; i < 100; i++) {
        ct.ThrowIfCancellationRequested();
        await Task.Delay(100, ct);
    }
}

var cts = new CancellationTokenSource(TimeSpan.FromSeconds(5));
await LongOperationAsync(cts.Token);

// IAsyncEnumerable (C# 8+)
async IAsyncEnumerable<int> GetNumbersAsync() {
    for (int i = 0; i < 10; i++) {
        await Task.Delay(100);
        yield return i;
    }
}

await foreach (int n in GetNumbersAsync()) {
    Console.WriteLine(n);
}

// ValueTask (avoids allocation when already complete)
async ValueTask<int> GetCachedAsync() {
    if (_cache != null) return _cache.Value;
    return await ComputeAsync();
}
```


---

# CHAPTER 7: DELEGATES AND EVENTS


## Functional C#

```csharp
using System;

// Delegate type
delegate int BinaryOp(int a, int b);

// Func and Action (built-in)
Func<int, int, int> add  = (a, b) => a + b;
Func<string, bool>  pred = s => s.Length > 3;
Action<string>      print = Console.WriteLine;
Predicate<int>      isEven = n => n % 2 == 0;

// Lambda expressions
var square = (int x) => x * x;
var greet  = (string name) => $"Hello, {name}!";

// Events
public class Button {
    public event EventHandler? Clicked;
    public event EventHandler<DataEventArgs>? DataReceived;

    protected virtual void OnClicked(EventArgs e) {
        Clicked?.Invoke(this, e);
    }
}

button.Clicked += (sender, e) => Console.WriteLine("Clicked!");
button.Clicked -= handler;

// LINQ with delegates
var nums = Enumerable.Range(1, 10);
nums.Where(isEven).Select(n => n * n).Sum();

// Expression trees
using System.Linq.Expressions;
Expression<Func<int,int>> expr = x => x * x;
var compiled = expr.Compile();
compiled(5);  // 25

// Span<T> and Memory<T> (high-performance)
Span<int> span = stackalloc int[100];
ReadOnlySpan<char> chars = "Hello".AsSpan();
```


---

# CHAPTER 8: EXCEPTION HANDLING AND PATTERNS


## Exceptions and Design Patterns

```csharp
// Exception handling
try {
    int result = int.Parse("abc");
} catch (FormatException ex) {
    Console.WriteLine($"Format error: {ex.Message}");
} catch (OverflowException ex) {
    Console.WriteLine($"Overflow: {ex.Message}");
} catch (Exception ex) when (ex.Message.Contains("special")) {
    Console.WriteLine("Filtered catch");
} finally {
    Console.WriteLine("Always runs");
}

// Custom exception
public class DomainException : Exception {
    public string Code { get; }
    public DomainException(string message, string code) : base(message) {
        Code = code;
    }
}

// using / IDisposable
using var conn = new SqlConnection(connStr);
using var reader = cmd.ExecuteReader();

// Null-safety operators
string? nullableStr = null;
int len = nullableStr?.Length ?? 0;
nullableStr!.Length;   // null-forgiving (assert non-null)

// Pattern matching
if (obj is string { Length: > 5 } s) {
    Console.WriteLine($"Long string: {s}");
}

if (animal is Dog { Breed: "Labrador" } lab) {
    lab.Fetch();
}

// Deconstruction
var (x, y) = point;
var (first, _, third) = tuple;

// Primary constructor (C# 12)
public class Person(string Name, int Age) {
    public string Greeting => $"Hi, I'm {Name}, aged {Age}";
}
```
