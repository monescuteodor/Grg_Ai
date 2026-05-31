# Go Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH GO


## Remarks

Go (Golang) is a statically typed, compiled language designed by Google for simplicity, performance, and concurrency. Go has garbage collection, goroutines (lightweight threads), channels, and a strong standard library. Go 1.21+ is the current stable version.

Tools: `go build`, `go run`, `go test`, `go mod`, `gofmt`, `golangci-lint`.


## Hello World

```go
// main.go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
    fmt.Printf("Hello, %s!\n", "Go")
}
```

```bash
go run main.go
go build -o myapp .
go mod init mymodule
go mod tidy
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Types and Variables

```go
package main

import "fmt"

func main() {
    // var declaration
    var x int = 42
    var y float64 = 3.14
    var s string = "hello"
    var b bool = true

    // Short declaration (inferred)
    n := 10
    pi := 3.14159
    name := "Alice"

    // Multiple assignment
    a, b2, c := 1, 2, 3
    x, y2 := y2, x    // swap

    // Constants
    const MAX = 100
    const (
        StatusOK  = 200
        StatusNotFound = 404
    )

    // iota (auto-increment in const blocks)
    const (
        Sunday = iota   // 0
        Monday          // 1
        Tuesday         // 2
    )

    // Zero values
    var i int     // 0
    var f float64 // 0.0
    var str string // ""
    var bl bool   // false
    var ptr *int  // nil

    fmt.Println(x, y, s, b, n, pi, name, a, b2, c)
    _ = i; _ = f; _ = str; _ = bl; _ = ptr
}
```

## Arrays, Slices, Maps

```go
// Array (fixed size, value type)
arr := [5]int{1, 2, 3, 4, 5}
arr2 := [...]int{10, 20, 30}   // size inferred

// Slice (dynamic, reference type)
s := []int{1, 2, 3}
s = append(s, 4, 5)
s = append(s, []int{6, 7, 8}...)

// Slice operations
s[1:3]      // [2, 3]
s[:3]       // first 3
s[2:]       // from index 2
len(s)      // length
cap(s)      // capacity

// make
sl := make([]int, 5)       // len=5, cap=5
sl2 := make([]int, 3, 10)  // len=3, cap=10

// copy
dst := make([]int, len(src))
copy(dst, src)

// 2D slice
matrix := [][]int{
    {1, 2, 3},
    {4, 5, 6},
}

// Map
m := map[string]int{"one": 1, "two": 2}
m["three"] = 3
val, ok := m["one"]   // ok is true if key exists
delete(m, "two")

// Map iteration
for k, v := range m {
    fmt.Printf("%s: %d\n", k, v)
}

// make map
scores := make(map[string]float64)
```


---

# CHAPTER 3: CONTROL FLOW


## Flow Control

```go
// if / else (no parentheses)
if x > 0 {
    fmt.Println("positive")
} else if x == 0 {
    fmt.Println("zero")
} else {
    fmt.Println("negative")
}

// if with init statement
if val, err := compute(); err != nil {
    fmt.Println("error:", err)
} else {
    fmt.Println("result:", val)
}

// switch (no break needed)
switch day {
case "Mon", "Tue", "Wed", "Thu", "Fri":
    fmt.Println("weekday")
case "Sat", "Sun":
    fmt.Println("weekend")
default:
    fmt.Println("unknown")
}

// Type switch
switch v := i.(type) {
case int:    fmt.Printf("int: %d\n", v)
case string: fmt.Printf("string: %s\n", v)
case bool:   fmt.Printf("bool: %t\n", v)
default:     fmt.Printf("unknown: %T\n", v)
}

// for (only loop in Go)
for i := 0; i < 10; i++ {
    fmt.Println(i)
}

// while-style
for n > 0 {
    n--
}

// infinite loop
for {
    if done { break }
}

// range
for i, v := range slice {
    fmt.Printf("[%d]=%d\n", i, v)
}
for k, v := range myMap { _ = k; _ = v }
for i := range slice { _ = i }   // index only
for _, v := range slice { _ = v } // value only

// defer (LIFO, runs when function returns)
defer fmt.Println("cleanup")
defer file.Close()
```


---

# CHAPTER 4: FUNCTIONS


## Functions

```go
// Basic function
func add(a, b int) int { return a + b }

// Multiple return values
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}

// Named return values
func minmax(nums []int) (min, max int) {
    min, max = nums[0], nums[0]
    for _, n := range nums[1:] {
        if n < min { min = n }
        if n > max { max = n }
    }
    return  // naked return
}

// Variadic
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}
sum(1, 2, 3)
sum(nums...)   // spread slice

// First-class functions
func apply(f func(int) int, x int) int { return f(x) }
double := func(x int) int { return x * 2 }
apply(double, 5)

// Closure
func makeCounter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}

// Recursion
func factorial(n int) int {
    if n <= 1 { return 1 }
    return n * factorial(n-1)
}

// init function
func init() {
    // runs automatically before main
}
```


---

# CHAPTER 5: STRUCTS AND INTERFACES


## Structs

```go
// Struct definition
type Point struct {
    X, Y float64
}

type Person struct {
    Name string
    Age  int
    Email string `json:"email,omitempty"`
}

// Struct literal
p := Point{X: 3.0, Y: 4.0}
p2 := Point{3.0, 4.0}   // positional (avoid)
pp := &Point{1.0, 2.0}  // pointer to struct

// Methods
func (p Point) Distance(other Point) float64 {
    dx := p.X - other.X
    dy := p.Y - other.Y
    return math.Sqrt(dx*dx + dy*dy)
}

func (p *Point) Scale(factor float64) {
    p.X *= factor
    p.Y *= factor
}

// Embedding (composition)
type Animal struct {
    Name string
}
func (a Animal) Speak() string { return a.Name + " speaks" }

type Dog struct {
    Animal             // embedded
    Breed string
}
dog := Dog{Animal: Animal{"Rex"}, Breed: "Lab"}
dog.Speak()   // promoted from Animal

// Interface
type Stringer interface {
    String() string
}

type Shape interface {
    Area() float64
    Perimeter() float64
}

// Interface implementation (implicit!)
type Circle struct{ Radius float64 }
func (c Circle) Area() float64 { return math.Pi * c.Radius * c.Radius }
func (c Circle) Perimeter() float64 { return 2 * math.Pi * c.Radius }

// Circle implicitly implements Shape
var s Shape = Circle{5.0}

// Interface composition
type ReadWriter interface {
    io.Reader
    io.Writer
}

// Empty interface / any
var anything any = 42
anything = "now a string"

// Type assertion
str, ok := anything.(string)
```


---

# CHAPTER 6: CONCURRENCY


## Goroutines and Channels

```go
import (
    "sync"
    "time"
)

// Goroutine — lightweight thread
go func() {
    fmt.Println("running concurrently")
}()

// Channel — typed communication pipe
ch := make(chan int)        // unbuffered
bch := make(chan int, 100)  // buffered

// Send and receive
go func() { ch <- 42 }()
val := <-ch   // blocks until value available

// Close channel
close(ch)
val, ok := <-ch   // ok=false if closed and empty

// Range over channel
for v := range ch {
    fmt.Println(v)
}

// select — multiplex channels
select {
case msg := <-ch1:
    fmt.Println("ch1:", msg)
case msg := <-ch2:
    fmt.Println("ch2:", msg)
case <-time.After(time.Second):
    fmt.Println("timeout")
default:
    fmt.Println("no data ready")
}

// WaitGroup
var wg sync.WaitGroup
for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        fmt.Printf("Worker %d\n", id)
    }(i)
}
wg.Wait()

// Mutex
var mu sync.Mutex
var counter int

func increment() {
    mu.Lock()
    defer mu.Unlock()
    counter++
}

// Once
var once sync.Once
once.Do(func() { /* runs exactly once */ })

// Context
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
```


---

# CHAPTER 7: ERROR HANDLING


## Errors

```go
import "errors"

// Error interface
type error interface {
    Error() string
}

// errors.New
err := errors.New("something went wrong")

// fmt.Errorf with %w (wrapping)
wrapped := fmt.Errorf("outer: %w", err)

// Unwrap / errors.Is / errors.As
errors.Is(wrapped, err)             // true (unwraps chain)
errors.As(wrapped, &targetErr)      // check type

// Custom error type
type ValidationError struct {
    Field   string
    Message string
}
func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error: %s - %s", e.Field, e.Message)
}

// Idiomatic error handling
result, err := someOperation()
if err != nil {
    return fmt.Errorf("myFunc: %w", err)
}

// Panic / recover
func safeDiv(a, b int) (result int, err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("recovered: %v", r)
        }
    }()
    return a / b, nil
}
```


---

# CHAPTER 8: STANDARD LIBRARY AND GENERICS


## Key Packages and Generics

```go
import (
    "bufio"
    "encoding/json"
    "net/http"
    "os"
    "strings"
    "strconv"
    "sort"
)

// strings
strings.Contains("hello world", "world")
strings.HasPrefix("hello", "he")
strings.ToUpper("hello")
strings.Split("a,b,c", ",")
strings.Join([]string{"a","b"}, "-")
strings.TrimSpace("  hi  ")
strings.Replace("aaa", "a", "b", 2)
strings.Builder{} // efficient string building

// strconv
strconv.Itoa(42)
strconv.Atoi("42")
strconv.ParseFloat("3.14", 64)
strconv.FormatFloat(3.14, 'f', 2, 64)

// sort
sort.Ints([]int{3,1,2})
sort.Strings([]string{"c","a","b"})
sort.Slice(people, func(i, j int) bool {
    return people[i].Age < people[j].Age
})

// JSON
type User struct {
    Name string `json:"name"`
    Age  int    `json:"age,omitempty"`
}
data, _ := json.Marshal(user)
json.Unmarshal(data, &user)
json.NewEncoder(w).Encode(user)
json.NewDecoder(r.Body).Decode(&user)

// HTTP
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "Hello")
})
http.ListenAndServe(":8080", nil)

// Generics (Go 1.18+)
func Map[T, U any](s []T, f func(T) U) []U {
    result := make([]U, len(s))
    for i, v := range s { result[i] = f(v) }
    return result
}

func Filter[T any](s []T, f func(T) bool) []T {
    var result []T
    for _, v := range s {
        if f(v) { result = append(result, v) }
    }
    return result
}

type Number interface { ~int | ~float64 }
func Sum[T Number](nums []T) T {
    var total T
    for _, n := range nums { total += n }
    return total
}
```
