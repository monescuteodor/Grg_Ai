# Go Advanced Complete Reference


---

# CHAPTER 1: GO FUNDAMENTALS RECAP


## Remarks

Go (Golang) is a statically typed, compiled language created at Google by Rob Pike, Ken Thompson, and Robert Griesemer (2009). Go's philosophy is radical simplicity: no inheritance, no generics (until 1.18), no exceptions, no implicit conversions. This simplicity makes Go codebases remarkably readable and maintainable at scale. Go excels at concurrent networked services, CLI tools, and infrastructure (Docker, Kubernetes, Terraform, Prometheus — all written in Go).

Key concepts: **Goroutines** (lightweight threads), **Channels** (typed communication pipes), **Interfaces** (implicit satisfaction), **Error handling** (explicit return values), **Defer** (cleanup guarantee), **Composition over inheritance**, **Context** (cancellation/timeout propagation), **Generics** (Go 1.18+), **Testing** (built-in), **Tooling** (go fmt, go vet, go test, go build — batteries included).


## Types and Structs

```go
package main

import "fmt"

// Struct (Go's only compound type — no classes!)
type User struct {
    ID        int
    Name      string
    Email     string
    IsActive  bool
}

// Methods (functions with receiver)
func (u User) FullInfo() string {
    return fmt.Sprintf("%s <%s>", u.Name, u.Email)
}

// Pointer receiver (can MODIFY the struct)
func (u *User) Deactivate() {
    u.IsActive = false
}

// Value receiver: works on copy (can't modify original)
// Pointer receiver: works on original (can modify)
// Rule: if ANY method needs pointer receiver, ALL methods should use pointer receiver

func main() {
    // Struct literal
    user := User{
        ID:       1,
        Name:     "Alice",
        Email:    "alice@example.com",
        IsActive: true,
    }

    fmt.Println(user.FullInfo())
    user.Deactivate()
    fmt.Println(user.IsActive)   // false

    // Pointer to struct
    userPtr := &User{Name: "Bob"}
    userPtr.Name = "Robert"      // Go auto-dereferences

    // Embedding (composition, not inheritance!)
    type Admin struct {
        User                    // Embedded — Admin HAS a User
        Permissions []string
    }

    admin := Admin{
        User:        User{Name: "Carol", Email: "carol@example.com"},
        Permissions: []string{"admin", "write"},
    }
    fmt.Println(admin.Name)      // Promoted field from User
    fmt.Println(admin.FullInfo()) // Promoted method from User
}
```


---

# CHAPTER 2: INTERFACES


## Implicit Interface Satisfaction

```go
// Go interfaces are satisfied IMPLICITLY — no "implements" keyword
// If type has the methods → it satisfies the interface. Period.

type Writer interface {
    Write(data []byte) (int, error)
}

type Logger interface {
    Log(message string)
}

// FileWriter satisfies Writer (has Write method)
type FileWriter struct {
    Path string
}

func (fw *FileWriter) Write(data []byte) (int, error) {
    return os.WriteFile(fw.Path, data, 0644), nil
}

// ConsoleLogger satisfies Logger
type ConsoleLogger struct{}

func (cl ConsoleLogger) Log(message string) {
    fmt.Println("[LOG]", message)
}

// Accept interface, return struct (Go proverb)
func SaveData(w Writer, data []byte) error {
    _, err := w.Write(data)
    return err
}

// Works with any Writer: file, network, buffer, mock...
SaveData(&FileWriter{Path: "out.txt"}, []byte("hello"))
SaveData(&bytes.Buffer{}, []byte("hello"))
SaveData(os.Stdout, []byte("hello"))


// Empty interface (accepts ANY type) — pre-generics escape hatch
func printAnything(v interface{}) {    // or: v any (Go 1.18+)
    fmt.Println(v)
}

// Type assertion
func process(v interface{}) {
    // Check type
    if s, ok := v.(string); ok {
        fmt.Println("String:", s)
    }

    // Type switch
    switch val := v.(type) {
    case string:
        fmt.Println("String:", val)
    case int:
        fmt.Println("Int:", val)
    case []byte:
        fmt.Println("Bytes:", len(val))
    default:
        fmt.Printf("Unknown type: %T\n", val)
    }
}


// Interface composition
type ReadWriter interface {
    Reader
    Writer
}

// io.Reader and io.Writer are THE most important Go interfaces:
// type Reader interface { Read(p []byte) (n int, err error) }
// type Writer interface { Write(p []byte) (n int, err error) }
// Everything implements them: files, network, buffers, compressors, encryptors...
// Compose them to build powerful I/O pipelines


// Small interfaces (Go idiom: 1-2 methods)
type Stringer interface {
    String() string
}

type Closer interface {
    Close() error
}

// Large interfaces are a code smell in Go.
// Prefer: many small interfaces, composed when needed.
```


---

# CHAPTER 3: CONCURRENCY


## Goroutines

```go
// Goroutine: lightweight thread (~2 KB stack, grows as needed)
// Go runtime multiplexes goroutines onto OS threads (M:N scheduling)
// Can run millions of goroutines on a single machine

func main() {
    // Launch goroutine
    go doWork()

    // Anonymous goroutine
    go func() {
        fmt.Println("Hello from goroutine")
    }()

    // PROBLEM: main() exits before goroutines finish!
    // Need synchronization...
    time.Sleep(time.Second)   // BAD: unreliable
}

// WaitGroup: wait for multiple goroutines
func main() {
    var wg sync.WaitGroup

    for i := 0; i < 10; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            fmt.Printf("Worker %d\n", id)
        }(i)   // Pass i as argument (avoid closure over loop variable!)
    }

    wg.Wait()   // Block until all Done()
    fmt.Println("All workers completed")
}
```


## Channels

```go
// Channel: typed pipe for goroutine communication
// "Don't communicate by sharing memory; share memory by communicating."

// Unbuffered channel (synchronous: sender blocks until receiver ready)
ch := make(chan string)

go func() {
    ch <- "hello"    // Send (blocks until someone receives)
}()

msg := <-ch          // Receive (blocks until someone sends)
fmt.Println(msg)     // "hello"


// Buffered channel (async up to buffer size)
ch := make(chan int, 5)
ch <- 1    // Doesn't block (buffer not full)
ch <- 2
ch <- 3
val := <-ch   // 1 (FIFO)


// Channel direction (restrict in function signatures)
func producer(out chan<- int) {     // Send-only
    for i := 0; i < 10; i++ {
        out <- i
    }
    close(out)
}

func consumer(in <-chan int) {      // Receive-only
    for val := range in {           // Range over channel until closed
        fmt.Println(val)
    }
}

func main() {
    ch := make(chan int, 10)
    go producer(ch)
    consumer(ch)
}


// Select: wait on multiple channels
func main() {
    ch1 := make(chan string)
    ch2 := make(chan string)

    go func() { time.Sleep(1 * time.Second); ch1 <- "one" }()
    go func() { time.Sleep(2 * time.Second); ch2 <- "two" }()

    for i := 0; i < 2; i++ {
        select {
        case msg := <-ch1:
            fmt.Println("ch1:", msg)
        case msg := <-ch2:
            fmt.Println("ch2:", msg)
        case <-time.After(3 * time.Second):
            fmt.Println("Timeout!")
        }
    }
}

// Non-blocking select (with default)
select {
case msg := <-ch:
    fmt.Println(msg)
default:
    fmt.Println("No message available")   // Doesn't block
}
```


## Concurrency Patterns

```go
// PATTERN 1: Fan-Out / Fan-In
func fanOut(input <-chan int, workers int) []<-chan int {
    channels := make([]<-chan int, workers)
    for i := 0; i < workers; i++ {
        channels[i] = worker(input)
    }
    return channels
}

func fanIn(channels ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    merged := make(chan int)
    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()
            for val := range c {
                merged <- val
            }
        }(ch)
    }
    go func() {
        wg.Wait()
        close(merged)
    }()
    return merged
}


// PATTERN 2: Worker Pool
func workerPool(jobs <-chan Job, results chan<- Result, numWorkers int) {
    var wg sync.WaitGroup
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            for job := range jobs {
                result := processJob(job)
                results <- result
            }
        }(i)
    }
    wg.Wait()
    close(results)
}


// PATTERN 3: Pipeline
func generate(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

func filter(in <-chan int, predicate func(int) bool) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            if predicate(n) {
                out <- n
            }
        }
        close(out)
    }()
    return out
}

// Compose pipeline
func main() {
    ch := generate(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    squared := square(ch)
    evens := filter(squared, func(n int) bool { return n%2 == 0 })

    for result := range evens {
        fmt.Println(result)   // 4, 16, 36, 64, 100
    }
}


// PATTERN 4: Semaphore (limit concurrency)
func processAll(items []Item, maxConcurrent int) {
    sem := make(chan struct{}, maxConcurrent)
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1)
        sem <- struct{}{}    // Acquire (blocks if buffer full)

        go func(it Item) {
            defer wg.Done()
            defer func() { <-sem }()   // Release
            process(it)
        }(item)
    }

    wg.Wait()
}
```


---

# CHAPTER 4: CONTEXT AND ERROR HANDLING


## Context (Cancellation and Timeouts)

```go
import "context"

// Context carries: deadlines, cancellation signals, request-scoped values
// Pass context as FIRST parameter to every function in the chain

// Timeout context
func fetchWithTimeout(url string) ([]byte, error) {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()   // ALWAYS defer cancel to free resources

    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, err   // Returns context.DeadlineExceeded on timeout
    }
    defer resp.Body.Close()

    return io.ReadAll(resp.Body)
}


// Cancellation context
func longRunningTask(ctx context.Context) error {
    for i := 0; i < 1000; i++ {
        select {
        case <-ctx.Done():
            return ctx.Err()   // context.Canceled or DeadlineExceeded
        default:
            doWork(i)
        }
    }
    return nil
}

func main() {
    ctx, cancel := context.WithCancel(context.Background())

    go func() {
        time.Sleep(2 * time.Second)
        cancel()   // Cancel after 2 seconds
    }()

    err := longRunningTask(ctx)
    fmt.Println(err)   // context canceled
}


// Context with values (request-scoped, NOT for passing function parameters!)
type contextKey string
const requestIDKey contextKey = "requestID"

func middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        ctx := context.WithValue(r.Context(), requestIDKey, uuid.New().String())
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

func handler(w http.ResponseWriter, r *http.Request) {
    reqID := r.Context().Value(requestIDKey).(string)
    log.Printf("[%s] Handling request", reqID)
}
```


## Error Handling

```go
// Go errors are VALUES, not exceptions
// Convention: return error as last return value

import (
    "errors"
    "fmt"
)

// Simple error
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Formatted error
func validateAge(age int) error {
    if age < 0 || age > 150 {
        return fmt.Errorf("invalid age: %d (must be 0-150)", age)
    }
    return nil
}

// Custom error type
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s with id '%s' not found", e.Resource, e.ID)
}

func findUser(id string) (*User, error) {
    user := db.Find(id)
    if user == nil {
        return nil, &NotFoundError{Resource: "User", ID: id}
    }
    return user, nil
}

// Error wrapping (Go 1.13+)
func loadConfig() error {
    data, err := os.ReadFile("config.yaml")
    if err != nil {
        return fmt.Errorf("loading config: %w", err)   // %w wraps error
    }
    return nil
}

// Unwrap and check error types
err := loadConfig()
if errors.Is(err, os.ErrNotExist) {
    fmt.Println("Config file missing")
}

var notFound *NotFoundError
if errors.As(err, &notFound) {
    fmt.Printf("Not found: %s %s\n", notFound.Resource, notFound.ID)
}


// Defer for cleanup (runs when function returns, LIFO order)
func processFile(path string) error {
    f, err := os.Open(path)
    if err != nil {
        return err
    }
    defer f.Close()   // Guaranteed to run, even on error/panic

    // Process file...
    return nil
}

// Panic/Recover (use sparingly — only for truly unrecoverable errors)
func safeHandler(w http.ResponseWriter, r *http.Request) {
    defer func() {
        if r := recover(); r != nil {
            log.Printf("Panic recovered: %v", r)
            http.Error(w, "Internal error", 500)
        }
    }()

    handleRequest(w, r)   // If this panics, recover catches it
}
```


---

# CHAPTER 5: GENERICS AND TESTING


## Generics (Go 1.18+)

```go
// Generic function
func Map[T any, U any](slice []T, fn func(T) U) []U {
    result := make([]U, len(slice))
    for i, v := range slice {
        result[i] = fn(v)
    }
    return result
}

func Filter[T any](slice []T, predicate func(T) bool) []T {
    var result []T
    for _, v := range slice {
        if predicate(v) {
            result = append(result, v)
        }
    }
    return result
}

// Usage
names := Map([]int{1, 2, 3}, func(n int) string {
    return fmt.Sprintf("item_%d", n)
})

evens := Filter([]int{1, 2, 3, 4, 5}, func(n int) bool {
    return n%2 == 0
})


// Constraints
type Number interface {
    ~int | ~int32 | ~int64 | ~float32 | ~float64
}

func Sum[T Number](nums []T) T {
    var total T
    for _, n := range nums {
        total += n
    }
    return total
}

Sum([]int{1, 2, 3})         // 6
Sum([]float64{1.1, 2.2})    // 3.3


// Generic struct
type Stack[T any] struct {
    items []T
}

func (s *Stack[T]) Push(item T)  { s.items = append(s.items, item) }
func (s *Stack[T]) Pop() (T, bool) {
    if len(s.items) == 0 {
        var zero T
        return zero, false
    }
    item := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return item, true
}
```


## Testing (Built-in)

```go
// Go has testing built into the language. No framework needed!
// File: math_test.go (must end in _test.go)

package math

import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d, want 5", result)
    }
}

// Table-driven tests (Go idiom)
func TestDivide(t *testing.T) {
    tests := []struct {
        name    string
        a, b    float64
        want    float64
        wantErr bool
    }{
        {"positive", 10, 2, 5, false},
        {"negative", -10, 2, -5, false},
        {"zero divisor", 10, 0, 0, true},
        {"both zero", 0, 0, 0, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Divide(tt.a, tt.b)
            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("Divide(%g, %g) = %g, want %g", tt.a, tt.b, got, tt.want)
            }
        })
    }
}

// Benchmarks
func BenchmarkSort(b *testing.B) {
    data := generateTestData(10000)
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        sort.Ints(data)
    }
}

// Run tests:  go test ./...
// Verbose:    go test -v ./...
// Coverage:   go test -cover ./...
// Benchmarks: go test -bench=. ./...
// Race detector: go test -race ./...
```


---

# CHAPTER 6: COMMON PITFALLS

```
PITFALL 1: Goroutine leak
  Goroutine blocked forever (waiting on channel nobody sends to).
  Fix: always ensure channels are closed or context cancelled.

PITFALL 2: Loop variable capture in goroutine
  for _, v := range items { go func() { use(v) }() }
  All goroutines see LAST value of v!
  Fix: go func(val Item) { use(val) }(v)   // Pass as argument
  (Fixed in Go 1.22 with loop variable scoping change)

PITFALL 3: Nil map write
  var m map[string]int; m["key"] = 1  → PANIC
  Fix: m := make(map[string]int)

PITFALL 4: Data race
  Multiple goroutines access shared variable without sync.
  Fix: use channels, sync.Mutex, or sync/atomic. Run go test -race.

PITFALL 5: Forgetting to close response body
  resp, _ := http.Get(url)
  // Must: defer resp.Body.Close()
  Fix: always defer resp.Body.Close() after checking error.

PITFALL 6: Ignoring errors
  result, _ := doSomething()   // Ignoring error!
  Fix: ALWAYS handle errors. Use errcheck linter.

PITFALL 7: Using sync.WaitGroup incorrectly
  wg.Add(1) inside goroutine (race with wg.Wait()).
  Fix: wg.Add(1) BEFORE launching goroutine.

PITFALL 8: Sending on closed channel
  close(ch); ch <- value  → PANIC
  Fix: only close from sender side, use sync.Once for single close.

PITFALL 9: Large structs passed by value
  func process(data HugeStruct) → copies entire struct each call.
  Fix: use pointer: func process(data *HugeStruct).

PITFALL 10: Not using context for cancellation
  HTTP handler spawns goroutines that outlive the request.
  Fix: pass request context, check ctx.Done() in goroutines.
```