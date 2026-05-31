# F# Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH F#


## Remarks

F# is a strongly-typed, functional-first programming language on .NET. It combines functional programming (immutable data, type inference, pattern matching) with OOP and imperative features. Excellent for data science, finance, and domain-driven design.

Tools: dotnet CLI, Visual Studio, Rider, VS Code with Ionide extension.


## Hello World

```fsharp
// hello.fsx (script)
printfn "Hello, World!"
printfn "Hello, %s!" "F#"
printf "No newline "

// hello.fs (compiled)
module Hello

[<EntryPoint>]
let main _ =
    printfn "Hello, World!"
    0  // exit code
```

```bash
dotnet fsi hello.fsx        # run script
dotnet new console -lang F# -o HelloApp
cd HelloApp && dotnet run
```


---

# CHAPTER 2: TYPES AND VARIABLES


## Types and Bindings

```fsharp
// let bindings (immutable by default)
let name = "Alice"
let age  = 30
let pi   = 3.14159
let flag = true

// Mutable
let mutable count = 0
count <- count + 1

// Type annotations
let x : int    = 42
let y : float  = 3.14
let s : string = "hello"
let b : bool   = true

// Primitive types
let i8  : sbyte  = 127y
let i16 : int16  = 1000s
let i32 : int32  = 42
let i64 : int64  = 9000000000L
let u32 : uint32 = 42u
let f32 : float32= 3.14f
let f64 : float  = 3.14
let dec : decimal= 19.99m
let ch  : char   = 'A'
let bigint_val   = 123456789012345678901234567890I

// String operations
let str = "Hello, World!"
str.Length                   // 13
str.ToUpper()
str.ToLower()
str.Substring(0, 5)          // "Hello"
str.Contains("World")
str.Replace("World", "F#")
str.Split([|','|])           // array of strings
str.Trim()
str.StartsWith("Hello")
str.[0]                      // 'H' (char indexing)

// String interpolation (F# 5+)
let greeting = $"Hello, {name}! Age: {age}"
let expr     = $"Double: {age * 2}"

// Sprintf (type-safe formatting)
let msg = sprintf "Name: %s, Age: %d, Pi: %.2f" name age pi

// Tuple
let t = (1, "hello", 3.14)
let a, b, c = t        // destructuring
fst (1, 2)             // 1
snd (1, 2)             // 2

// Option (null-safe)
let some_val : int option = Some 42
let no_val   : int option = None
Option.get some_val           // 42
Option.defaultValue 0 no_val  // 0
Option.map (fun x -> x * 2) some_val  // Some 84
Option.bind (fun x -> if x > 0 then Some x else None) some_val
```


---

# CHAPTER 3: COLLECTIONS


## F# Collections

```fsharp
// List (immutable linked list)
let lst = [1; 2; 3; 4; 5]
let lst2 = 0 :: lst        // prepend: [0;1;2;3;4;5]
let lst3 = lst @ [6; 7]   // append

List.head lst       // 1
List.tail lst       // [2;3;4;5]
List.last lst       // 5
List.length lst     // 5
List.item 2 lst     // 3 (0-indexed)
lst.[2]             // 3

List.map (fun x -> x * 2) lst        // [2;4;6;8;10]
List.filter (fun x -> x % 2 = 0) lst // [2;4]
List.find (fun x -> x > 3) lst       // 4
List.tryFind (fun x -> x > 10) lst   // None
List.exists (fun x -> x > 4) lst     // true
List.forall (fun x -> x > 0) lst     // true
List.fold (fun acc x -> acc + x) 0 lst    // 15
List.foldBack (fun x acc -> x :: acc) lst []  // copy
List.reduce (+) lst                    // 15
List.sum lst                           // 15
List.sort lst
List.sortDescending lst
List.sortBy (fun x -> -x) lst
List.rev lst                           // [5;4;3;2;1]
List.take 3 lst                        // [1;2;3]
List.skip 2 lst                        // [3;4;5]
List.takeWhile (fun x -> x < 4) lst   // [1;2;3]
List.skipWhile (fun x -> x < 4) lst   // [4;5]
List.collect (fun x -> [x; x*2]) lst  // flatMap
List.zip lst lst                       // [(1,1);(2,2);...]
List.unzip [(1,"a");(2,"b")]          // ([1;2],["a";"b"])
List.chunkBySize 2 lst                 // [[1;2];[3;4];[5]]
List.partition (fun x -> x % 2 = 0) lst  // ([2;4],[1;3;5])
List.groupBy (fun x -> x % 2 = 0) lst   // [(false,[1;3;5]);(true,[2;4])]

// Array
let arr = [| 1; 2; 3; 4; 5 |]
arr.[0]           // 1
arr.[0] <- 99     // mutate!
Array.length arr
Array.map ((*) 2) arr
Array.filter (fun x -> x > 2) arr
Array.sort arr
Array.sortInPlace arr   // in-place

// Sequence (lazy)
let seq1 = seq { 1 .. 10 }
let seq2 = seq { for x in 1..10 do if x % 2 = 0 then yield x }
Seq.map (fun x -> x * 2) seq1
Seq.filter (fun x -> x > 5) seq1
Seq.take 5 (Seq.initInfinite id)  // [0;1;2;3;4]

// Map (immutable)
let m = Map.ofList [("Alice", 30); ("Bob", 25)]
m.["Alice"]                // 30
Map.find "Alice" m         // 30
Map.tryFind "Dave" m       // None
Map.add "Carol" 35 m
Map.remove "Bob" m
Map.containsKey "Alice" m  // true
Map.keys m
Map.values m
Map.map (fun k v -> v + 1) m
Map.filter (fun k v -> v > 26) m

// Set
let s = Set.ofList [1; 2; 3; 4; 5]
Set.contains 3 s            // true
Set.add 6 s
Set.remove 1 s
Set.union s (Set.ofList [4;5;6])
Set.intersect s (Set.ofList [3;4;5;6])
Set.difference s (Set.ofList [3;4])
```


---

# CHAPTER 4: PATTERN MATCHING AND CONTROL FLOW


## Pattern Matching

```fsharp
// match expression
let classify n =
    match n with
    | 0 -> "zero"
    | n when n > 0 -> "positive"
    | _ -> "negative"

// Tuple matching
let describe_pair pair =
    match pair with
    | (0, 0) -> "origin"
    | (x, 0) -> sprintf "on x-axis at %d" x
    | (0, y) -> sprintf "on y-axis at %d" y
    | (x, y) -> sprintf "at (%d, %d)" x y

// List matching
let rec sumList lst =
    match lst with
    | [] -> 0
    | head :: tail -> head + sumList tail

// Option matching
let divideOpt a b =
    if b = 0 then None
    else Some (a / b)

match divideOpt 10 2 with
| Some result -> printfn "Result: %d" result
| None -> printfn "Division by zero"

// Union matching
type Shape =
    | Circle of float
    | Rectangle of float * float

let area shape =
    match shape with
    | Circle r       -> System.Math.PI * r * r
    | Rectangle(w,h) -> w * h

// Active patterns
let (|Even|Odd|) n =
    if n % 2 = 0 then Even else Odd

let describe_parity n =
    match n with
    | Even -> "even"
    | Odd  -> "odd"

// if/elif/else
let grade score =
    if score >= 90 then "A"
    elif score >= 80 then "B"
    elif score >= 70 then "C"
    else "F"

// for loops
for i in 1 .. 10 do
    printf "%d " i

for i in 10 .. -1 .. 1 do
    printf "%d " i

for x in [1; 2; 3] do
    printfn "%d" x

// while
let mutable n = 1
while n < 100 do
    n <- n * 2
printfn "%d" n   // 128

// try/with/finally
try
    let result = 10 / 0
    printfn "%d" result
with
| :? System.DivideByZeroException -> printfn "Division by zero"
| :? System.Exception as ex       -> printfn "Error: %s" ex.Message

try
    failwith "error"
with ex ->
    printfn "Caught: %s" ex.Message
```


---

# CHAPTER 5: FUNCTIONS AND FUNCTIONAL PATTERNS


## Functional Programming

```fsharp
// Functions are first-class values
let add a b = a + b
let add3 = add 3          // partial application

// Currying (all functions curried)
let multiply x y = x * y
let double = multiply 2
double 5   // 10

// Pipe operator |>
[1 .. 10]
|> List.filter (fun x -> x % 2 = 0)
|> List.map (fun x -> x * x)
|> List.sum               // 220

// Backward pipe <|
printfn "%d" <| List.sum [1..10]

// Function composition >>
let incThenDouble = (+) 1 >> (*) 2
incThenDouble 5   // 12

let doubleThenInc = (*) 2 >> (+) 1
doubleThenInc 5   // 11

// Lambda
let square = fun x -> x * x
let greet  = fun name greeting -> sprintf "%s, %s!" greeting name

// Recursion
let rec factorial n =
    if n <= 1 then 1
    else n * factorial (n - 1)

// Tail recursion with accumulator
let rec factTail n acc =
    if n <= 1 then acc
    else factTail (n - 1) (n * acc)
let factorial' n = factTail n 1

// Mutual recursion
let rec isEven n = if n = 0 then true  else isOdd  (n - 1)
and     isOdd  n = if n = 0 then false else isEven (n - 1)

// Higher-order functions
let applyTwice f x = f (f x)
applyTwice ((*) 2) 3   // 12

// Map / filter / fold
let nums = [1 .. 10]
List.map (fun x -> x * x) nums
List.filter (fun x -> x % 2 = 0) nums
List.fold (fun acc x -> acc + x) 0 nums

// Computation expressions (monad-like)
let result =
    option {
        let! x = Some 10
        let! y = Some 20
        return x + y
    }  // Some 30

// async computation
let asyncTask = async {
    let! result = async { return 42 }
    printfn "Result: %d" result
    return result
}
Async.RunSynchronously asyncTask
```


---

# CHAPTER 6: DISCRIMINATED UNIONS AND RECORDS


## F# Type System

```fsharp
// Discriminated Union (ADT)
type Shape =
    | Circle    of radius : float
    | Rectangle of width : float * height : float
    | Triangle  of base_ : float * height : float

let area = function
    | Circle r         -> System.Math.PI * r * r
    | Rectangle(w, h)  -> w * h
    | Triangle(b, h)   -> 0.5 * b * h

// Recursive union
type Tree<'a> =
    | Leaf
    | Node of Tree<'a> * 'a * Tree<'a>

let rec insert tree value =
    match tree with
    | Leaf -> Node(Leaf, value, Leaf)
    | Node(left, v, right) ->
        if value < v then Node(insert left value, v, right)
        elif value > v then Node(left, v, insert right value)
        else tree

// Records
type Person = {
    Name : string
    Age  : int
    City : string
}

let alice = { Name = "Alice"; Age = 30; City = "NYC" }
alice.Name               // "Alice"
let older = { alice with Age = 31 }  // copy with update

// Record pattern matching
let greet { Name = n; Age = a } =
    sprintf "Hello %s, you are %d" n a

// Generic record
type Pair<'a, 'b> = { First : 'a; Second : 'b }
let pair = { First = 1; Second = "hello" }

// Interfaces and OOP
type IAnimal =
    abstract member Name  : string
    abstract member Speak : unit -> string

type Dog(name : string) =
    interface IAnimal with
        member _.Name = name
        member _.Speak() = "Woof!"
    member _.Fetch() = sprintf "%s fetches!" name

let dog = Dog("Rex")
let animal = dog :> IAnimal
animal.Speak()   // "Woof!"
dog.Fetch()      // "Rex fetches!"

// Classes
type Counter(initial : int) =
    let mutable count = initial

    member _.Value = count

    member _.Increment() =
        count <- count + 1
        count

    member _.Reset() =
        count <- initial

let c = Counter(0)
c.Increment() |> ignore
c.Increment() |> ignore
c.Value   // 2
```


---

# CHAPTER 7: MODULES AND PROJECT STRUCTURE


## Modules

```fsharp
// Module definition
module MathUtils =

    let add a b = a + b
    let sub a b = a - b
    let mul a b = a * b

    let rec factorial n =
        if n <= 1 then 1
        else n * factorial (n-1)

    module Advanced =
        let fibonacci n =
            let rec fib a b n =
                if n = 0 then a
                else fib b (a+b) (n-1)
            fib 0 1 n

// Usage
MathUtils.add 3 4            // 7
MathUtils.Advanced.fibonacci 10  // 55

// Open module
open MathUtils
add 3 4   // 7

// Open in local scope
let result =
    let open MathUtils
    factorial 5    // 120

// Type extensions
type System.String with
    member s.WordCount = s.Split(' ').Length
    member s.IsPalindrome = s = System.String(Array.rev (s.ToCharArray()))

"hello world".WordCount    // 2
"racecar".IsPalindrome     // true

// Measure types (physical units)
[<Measure>] type m
[<Measure>] type s
[<Measure>] type kg

let distance = 100.0<m>
let time     = 10.0<s>
let speed    = distance / time   // 10.0<m/s>

let mass = 70.0<kg>
let force = mass * 9.81<m/s^2>  // Newtons

// Type providers (compile-time data access)
// #r "nuget: FSharp.Data"
// open FSharp.Data
// type WeatherJson = JsonProvider<"https://api.weather.com/data">
// let data = WeatherJson.Load("...")
```


---

# CHAPTER 8: ASYNC AND ADVANCED FEATURES


## Async Programming

```fsharp
open System.Net.Http
open System.Threading.Tasks

// Async workflows
let fetchUrl (url : string) = async {
    use client = new HttpClient()
    let! response = client.GetStringAsync(url) |> Async.AwaitTask
    return response.Length
}

// Run async
let length = Async.RunSynchronously (fetchUrl "https://example.com")

// Parallel async
let urls = ["https://example.com"; "https://google.com"]
let tasks = urls |> List.map fetchUrl
let results = Async.Parallel tasks |> Async.RunSynchronously

// Task (interop with .NET Tasks)
let taskExample () : Task<int> =
    task {
        do! Task.Delay(100)
        return 42
    }

// Mailbox processor (actor model)
let counter =
    MailboxProcessor.Start(fun inbox ->
        let rec loop n = async {
            let! msg = inbox.Receive()
            match msg with
            | "inc" -> return! loop (n + 1)
            | "get" ->
                inbox.Reply(n)
                return! loop n
            | _ -> return ()
        }
        loop 0)

counter.Post "inc"
counter.Post "inc"
let v = counter.PostAndReply (fun r -> "get")

// Reflection and quotations
open Microsoft.FSharp.Quotations
let expr = <@ 1 + 2 * 3 @>   // quoted expression
```
