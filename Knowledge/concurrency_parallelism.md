# Concurrency and Parallelism Complete Advanced Reference


---

# CHAPTER 1: FUNDAMENTALS


## Remarks

Concurrency is dealing with multiple things at once. Parallelism is doing multiple things at once. Concurrency is about structure — designing systems that can handle multiple tasks. Parallelism is about execution — actually running them simultaneously on multiple cores. A single-core CPU can be concurrent (context switching) but not parallel. A multi-core CPU can be both.

Key concepts: **Threads** (OS-scheduled execution units), **Processes** (isolated memory spaces), **Locks/Mutexes** (mutual exclusion), **Semaphores** (counting locks), **Deadlock** (circular wait), **Race conditions** (non-deterministic bugs), **Atomics** (lock-free operations), **Async/Await** (cooperative concurrency), **Actor model** (message passing), **CSP** (Communicating Sequential Processes — Go channels), **Event loop** (Node.js, Python asyncio).

Used by: every production system. Web servers (handle thousands of requests), databases (concurrent queries), games (physics + rendering + AI), mobile apps (UI thread + network), ML training (data parallelism across GPUs).

Tools: **pthreads** (C), **threading/multiprocessing/asyncio** (Python), **java.util.concurrent** (Java), **goroutines** (Go), **tokio** (Rust async), **Web Workers** (browser), **Worker Threads** (Node.js).


## Concurrency vs Parallelism

```
CONCURRENCY (structure):
  Multiple tasks make progress, not necessarily simultaneously.
  Single core: context switching between tasks.
  
  Example: Chef prepares 3 dishes.
  Starts soup → while soup simmers, chops salad → 
  while salad rests, grills steak → checks soup → ...
  One chef, three dishes, interleaved work.

PARALLELISM (execution):
  Multiple tasks run SIMULTANEOUSLY on multiple cores.
  
  Example: 3 chefs each prepare 1 dish at same time.
  Chef 1: soup. Chef 2: salad. Chef 3: steak.
  Three chefs, three dishes, truly simultaneous.

ASYNC (cooperative concurrency):
  Tasks voluntarily yield control when waiting (I/O).
  NO OS thread per task — lightweight (millions possible).
  
  Example: Chef starts boiling water, says "I'll wait" →
  event loop gives CPU to another task →
  water boils → event loop resumes chef.

MODELS:
  Multi-threading:     Shared memory, locks, OS-scheduled
  Multi-processing:    Separate memory, IPC, true isolation
  Async/Await:         Single thread, event loop, cooperative
  Actor model:         No shared state, message passing (Erlang, Akka)
  CSP:                 Channels for communication (Go)
```


## Threads vs Processes vs Async

```
THREADS:
  ✅ Shared memory (fast communication)
  ✅ Lightweight creation (~1MB stack)
  ❌ Race conditions (shared mutable state)
  ❌ Deadlocks possible
  ❌ Hard to debug
  Use: CPU-bound parallelism, shared data structures

PROCESSES:
  ✅ Isolated memory (crash one, others survive)
  ✅ True parallelism (no GIL in Python)
  ✅ Security (process boundaries)
  ❌ Heavy creation (~10MB+)
  ❌ IPC overhead (pipes, sockets, shared memory)
  Use: Isolation requirements, Python CPU-bound (bypass GIL)

ASYNC:
  ✅ Very lightweight (thousands on single thread)
  ✅ No locks needed (single thread)
  ✅ Perfect for I/O-bound (network, disk, DB)
  ❌ One CPU-heavy task blocks everything
  ❌ Can't use multiple cores (alone)
  ❌ Viral (async infects entire call chain)
  Use: Web servers, API clients, I/O-heavy applications

HYBRID (real-world):
  Node.js:   async event loop + worker threads for CPU
  Python:    asyncio + multiprocessing for CPU
  Go:        goroutines (M:N threading — many goroutines, few OS threads)
  Rust:      tokio async + rayon for CPU parallelism
  Java:      virtual threads (Project Loom) + thread pools
```


---

# CHAPTER 2: THREAD SYNCHRONIZATION


## Race Conditions

```python
import threading

# RACE CONDITION: two threads modify shared state simultaneously
counter = 0

def increment():
    global counter
    for _ in range(1_000_000):
        counter += 1   # NOT ATOMIC!
        # Actually: read counter → add 1 → write counter
        # Thread A reads 5, Thread B reads 5
        # Thread A writes 6, Thread B writes 6
        # Expected 7, got 6! Lost update.

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)
t1.start(); t2.start()
t1.join(); t2.join()

print(counter)   # NOT 2,000,000! Maybe 1,234,567 — different each run.

# This is a RACE CONDITION: result depends on thread scheduling (random).
```


## Mutex (Mutual Exclusion Lock)

```python
import threading

counter = 0
lock = threading.Lock()

def increment_safe():
    global counter
    for _ in range(1_000_000):
        lock.acquire()       # Block until lock available
        counter += 1         # Critical section (only one thread at a time)
        lock.release()       # Release for other threads

# Better: use context manager
def increment_safe_v2():
    global counter
    for _ in range(1_000_000):
        with lock:           # Auto acquire/release
            counter += 1

t1 = threading.Thread(target=increment_safe_v2)
t2 = threading.Thread(target=increment_safe_v2)
t1.start(); t2.start()
t1.join(); t2.join()

print(counter)   # Always 2,000,000 ✅


# REENTRANT LOCK (same thread can acquire multiple times)
rlock = threading.RLock()

def outer():
    with rlock:
        inner()   # Same thread re-acquires — OK with RLock, DEADLOCK with Lock!

def inner():
    with rlock:
        print("inner")
```


## Read-Write Lock

```python
import threading

class ReadWriteLock:
    """Multiple readers OR one writer, never both."""
    def __init__(self):
        self._readers = 0
        self._readers_lock = threading.Lock()
        self._writer_lock = threading.Lock()

    def acquire_read(self):
        with self._readers_lock:
            self._readers += 1
            if self._readers == 1:
                self._writer_lock.acquire()   # First reader blocks writers

    def release_read(self):
        with self._readers_lock:
            self._readers -= 1
            if self._readers == 0:
                self._writer_lock.release()   # Last reader unblocks writers

    def acquire_write(self):
        self._writer_lock.acquire()

    def release_write(self):
        self._writer_lock.release()

# Use case: config that's read 1000x/sec, written 1x/min
# Many readers simultaneously, writer gets exclusive access
```


## Semaphore

```python
import threading

# Semaphore: allows N threads to access resource simultaneously
# Mutex is semaphore with N=1

# Limit concurrent database connections to 5
db_semaphore = threading.Semaphore(5)

def query_database(query):
    with db_semaphore:   # At most 5 threads here at once
        connection = get_connection()
        result = connection.execute(query)
        connection.close()
        return result

# Bounded semaphore (can't release more than acquired — catches bugs)
pool = threading.BoundedSemaphore(10)
```


## Condition Variables

```python
import threading
from collections import deque

# Producer-Consumer pattern
class BoundedQueue:
    def __init__(self, maxsize):
        self.queue = deque()
        self.maxsize = maxsize
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def put(self, item):
        with self.not_full:
            while len(self.queue) >= self.maxsize:
                self.not_full.wait()   # Release lock and sleep until notified
            self.queue.append(item)
            self.not_empty.notify()    # Wake up a waiting consumer

    def get(self):
        with self.not_empty:
            while len(self.queue) == 0:
                self.not_empty.wait()  # Release lock and sleep until notified
            item = self.queue.popleft()
            self.not_full.notify()     # Wake up a waiting producer
            return item

# Usage
q = BoundedQueue(10)

def producer():
    for i in range(100):
        q.put(i)
        print(f"Produced {i}")

def consumer():
    for _ in range(100):
        item = q.get()
        print(f"Consumed {item}")

threading.Thread(target=producer).start()
threading.Thread(target=consumer).start()
```


## Deadlock

```python
# DEADLOCK: two threads each waiting for lock the other holds

lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_1():
    with lock_a:              # Acquires A
        time.sleep(0.1)
        with lock_b:          # Waits for B (held by thread_2)
            print("Thread 1")

def thread_2():
    with lock_b:              # Acquires B
        time.sleep(0.1)
        with lock_a:          # Waits for A (held by thread_1)
            print("Thread 2")

# DEADLOCK! Neither thread can proceed.

# FOUR CONDITIONS FOR DEADLOCK (all must be true):
# 1. Mutual exclusion: resource held exclusively
# 2. Hold and wait: hold one, wait for another
# 3. No preemption: can't force release
# 4. Circular wait: A waits for B, B waits for A

# PREVENTION STRATEGIES:
# 1. Lock ordering: always acquire locks in same order
def thread_1_fixed():
    with lock_a:
        with lock_b:
            print("Thread 1")

def thread_2_fixed():
    with lock_a:          # Same order as thread_1!
        with lock_b:
            print("Thread 2")

# 2. Timeout: try_lock with timeout
acquired = lock_a.acquire(timeout=1.0)
if not acquired:
    print("Could not acquire lock, abort")

# 3. Lock-free algorithms: use atomics instead of locks
```


## Atomic Operations

```python
# Atomics: single CPU instruction, no lock needed
# Python: threading module doesn't have true atomics (GIL helps though)
# In C/C++/Rust/Go/Java: atomic types available

# Python approximation with queue (thread-safe by design)
from queue import Queue

task_queue = Queue()     # Thread-safe, no locks needed
task_queue.put(item)     # Atomic enqueue
item = task_queue.get()  # Atomic dequeue


# Java-style atomics concept:
# AtomicInteger counter = new AtomicInteger(0);
# counter.incrementAndGet();   // Atomic increment
# counter.compareAndSet(expected, newValue);   // CAS operation

# CAS (Compare-And-Swap) — foundation of lock-free programming:
# 1. Read current value
# 2. Compute new value
# 3. CAS: if current == expected, write new (atomic)
# 4. If failed (someone else changed it), retry
#
# This is how lock-free queues, stacks, and counters work.
```


---

# CHAPTER 3: ASYNC PROGRAMMING


## Python asyncio

```python
import asyncio
import aiohttp

# async def = coroutine (can be suspended/resumed)
# await = suspend here, let event loop run other tasks

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        # Run ALL requests concurrently (not sequentially!)
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

# Sequential: 10 requests × 200ms = 2000ms
# Concurrent: 10 requests = ~200ms (all in parallel!)

async def main():
    urls = [f"https://httpbin.org/delay/0.2" for _ in range(10)]
    results = await fetch_all(urls)
    print(f"Fetched {len(results)} pages")

asyncio.run(main())


# Timeouts
async def fetch_with_timeout(url):
    try:
        async with asyncio.timeout(5.0):
            return await fetch_url(session, url)
    except asyncio.TimeoutError:
        return None


# Task groups (Python 3.11+)
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_url(session, url1))
        task2 = tg.create_task(fetch_url(session, url2))
        task3 = tg.create_task(process_data())
    # All tasks complete here (or exception if any fails)
    result1 = task1.result()


# Semaphore for rate limiting async tasks
semaphore = asyncio.Semaphore(10)   # Max 10 concurrent

async def limited_fetch(session, url):
    async with semaphore:
        return await fetch_url(session, url)

# Even with 1000 URLs, only 10 run at a time


# Queue-based worker pattern
async def worker(name, queue):
    while True:
        task = await queue.get()
        try:
            await process(task)
        finally:
            queue.task_done()

async def main():
    queue = asyncio.Queue()

    # Create workers
    workers = [asyncio.create_task(worker(f"worker-{i}", queue))
               for i in range(5)]

    # Add tasks
    for task in tasks:
        await queue.put(task)

    # Wait for all tasks to complete
    await queue.join()

    # Cancel workers
    for w in workers:
        w.cancel()
```


## JavaScript Concurrency Model

```javascript
// JavaScript is SINGLE-THREADED with event loop
// async/await is syntactic sugar over Promises

// Promise.all — concurrent execution
async function fetchAll(urls) {
    const promises = urls.map(url => fetch(url).then(r => r.json()));
    const results = await Promise.all(promises);
    return results;
}

// Promise.allSettled — don't fail on single rejection
const results = await Promise.allSettled([
    fetch('/api/users'),
    fetch('/api/posts'),
    fetch('/api/broken'),   // This fails
]);
// results: [{status:'fulfilled',value:...}, {status:'fulfilled',value:...}, {status:'rejected',reason:...}]

// Promise.race — first to complete wins
const result = await Promise.race([
    fetch('/api/primary'),
    new Promise((_, reject) => setTimeout(() => reject('timeout'), 5000)),
]);

// Promise.any — first to SUCCEED wins (ignores rejections)
const fastest = await Promise.any([
    fetch('https://cdn1.example.com/data'),
    fetch('https://cdn2.example.com/data'),
    fetch('https://cdn3.example.com/data'),
]);


// Web Workers (true parallelism in browser)
// main.js
const worker = new Worker('worker.js');
worker.postMessage({ data: largeArray, operation: 'sort' });
worker.onmessage = (event) => {
    console.log('Sorted:', event.data);
};

// worker.js
self.onmessage = (event) => {
    const { data, operation } = event.data;
    if (operation === 'sort') {
        const sorted = data.sort((a, b) => a - b);
        self.postMessage(sorted);
    }
};


// Node.js Worker Threads
import { Worker, isMainThread, parentPort, workerData } from 'worker_threads';

if (isMainThread) {
    const worker = new Worker('./worker.js', {
        workerData: { numbers: [5, 3, 1, 4, 2] },
    });
    worker.on('message', (result) => console.log('Result:', result));
    worker.on('error', (err) => console.error('Worker error:', err));
} else {
    const sorted = workerData.numbers.sort((a, b) => a - b);
    parentPort.postMessage(sorted);
}
```


## Go Concurrency (Goroutines + Channels)

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

// Goroutine: lightweight thread (~2KB stack, millions possible)
func main() {
    // Launch goroutine
    go func() {
        fmt.Println("Hello from goroutine")
    }()

    // Channel: typed pipe for communication between goroutines
    // "Don't communicate by sharing memory; share memory by communicating."
    ch := make(chan string)

    go func() {
        time.Sleep(time.Second)
        ch <- "result"   // Send to channel
    }()

    msg := <-ch   // Receive from channel (blocks until data available)
    fmt.Println(msg)


    // Buffered channel
    buffered := make(chan int, 10)   // Buffer 10 items without blocking
    buffered <- 42


    // Fan-out / Fan-in pattern
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    // Launch 5 workers (fan-out)
    for w := 0; w < 5; w++ {
        go worker(w, jobs, results)
    }

    // Send 20 jobs
    for j := 0; j < 20; j++ {
        jobs <- j
    }
    close(jobs)

    // Collect results (fan-in)
    for i := 0; i < 20; i++ {
        <-results
    }


    // Select: wait on multiple channels
    ch1 := make(chan string)
    ch2 := make(chan string)

    go func() { time.Sleep(1 * time.Second); ch1 <- "one" }()
    go func() { time.Sleep(2 * time.Second); ch2 <- "two" }()

    select {
    case msg := <-ch1:
        fmt.Println("Received from ch1:", msg)
    case msg := <-ch2:
        fmt.Println("Received from ch2:", msg)
    case <-time.After(3 * time.Second):
        fmt.Println("Timeout!")
    }


    // WaitGroup: wait for multiple goroutines
    var wg sync.WaitGroup
    for i := 0; i < 10; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            fmt.Printf("Worker %d done\n", id)
        }(i)
    }
    wg.Wait()   // Block until all done


    // Mutex (when you must share memory)
    var mu sync.Mutex
    counter := 0

    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            mu.Lock()
            counter++
            mu.Unlock()
        }()
    }
    wg.Wait()
    fmt.Println("Counter:", counter)   // Always 1000
}

func worker(id int, jobs <-chan int, results chan<- int) {
    for j := range jobs {
        fmt.Printf("Worker %d processing job %d\n", id, j)
        time.Sleep(100 * time.Millisecond)
        results <- j * 2
    }
}
```


---

# CHAPTER 4: CONCURRENCY PATTERNS


## Thread Pool

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

# Thread pool: reuse threads (avoid creation overhead)
def process_item(item):
    time.sleep(0.1)   # Simulate I/O
    return item * 2

items = list(range(100))

# ThreadPoolExecutor (I/O-bound)
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_item, item) for item in items]
    
    for future in as_completed(futures):
        result = future.result()
        print(result)

# ProcessPoolExecutor (CPU-bound — bypasses Python GIL)
def cpu_heavy(n):
    return sum(i * i for i in range(n))

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(cpu_heavy, [10_000_000] * 8))

# executor.map: ordered results
# executor.submit + as_completed: results as they finish (faster perceived)
```


## Actor Model

```python
# Actor: isolated unit with own state, communicates via messages
# No shared memory, no locks, no race conditions
# Used by: Erlang/OTP, Akka (Scala/Java), Elixir

import asyncio
from asyncio import Queue

class Actor:
    def __init__(self):
        self.mailbox = Queue()
        self._task = None

    async def start(self):
        self._task = asyncio.create_task(self._run())

    async def _run(self):
        while True:
            message = await self.mailbox.get()
            if message is None:
                break
            await self.handle(message)

    async def handle(self, message):
        raise NotImplementedError

    async def send(self, message):
        await self.mailbox.put(message)

    async def stop(self):
        await self.mailbox.put(None)
        await self._task


class CounterActor(Actor):
    def __init__(self):
        super().__init__()
        self.count = 0

    async def handle(self, message):
        if message["type"] == "increment":
            self.count += 1
        elif message["type"] == "get":
            message["reply"].set_result(self.count)

async def main():
    counter = CounterActor()
    await counter.start()

    # Send 1000 increments (no locks needed!)
    for _ in range(1000):
        await counter.send({"type": "increment"})

    # Get result
    future = asyncio.get_event_loop().create_future()
    await counter.send({"type": "get", "reply": future})
    result = await future
    print(f"Count: {result}")   # Always 1000

    await counter.stop()

asyncio.run(main())
```


## Pipeline Pattern

```python
import asyncio

# Pipeline: chain of processing stages connected by queues
# Each stage runs concurrently, data flows through

async def producer(queue, items):
    for item in items:
        await queue.put(item)
    await queue.put(None)   # Sentinel

async def stage_transform(in_queue, out_queue, fn):
    while True:
        item = await in_queue.get()
        if item is None:
            await out_queue.put(None)
            break
        result = await fn(item)
        await out_queue.put(result)

async def consumer(queue):
    results = []
    while True:
        item = await queue.get()
        if item is None:
            break
        results.append(item)
    return results

# Build pipeline
async def main():
    q1 = asyncio.Queue()
    q2 = asyncio.Queue()
    q3 = asyncio.Queue()

    data = list(range(100))

    await asyncio.gather(
        producer(q1, data),
        stage_transform(q1, q2, async_double),     # Stage 1: double
        stage_transform(q2, q3, async_to_string),   # Stage 2: stringify
        consumer(q3),                                # Collect results
    )
```


---

# CHAPTER 5: PYTHON GIL AND WORKAROUNDS


## The Global Interpreter Lock

```python
# GIL: only ONE thread executes Python bytecode at a time
# Even on 8-core CPU, Python threads can't run Python code in parallel

# GIL DOES affect: CPU-bound Python code (math, data processing)
# GIL does NOT affect: I/O operations (network, disk, DB)
# Because: I/O releases the GIL while waiting

# CONSEQUENCE:
# Threading in Python is GREAT for I/O-bound (web requests, file I/O)
# Threading in Python is USELESS for CPU-bound (number crunching)

# WORKAROUNDS FOR CPU-BOUND:

# 1. multiprocessing (separate processes, each has own GIL)
from multiprocessing import Pool

def cpu_task(n):
    return sum(i * i for i in range(n))

with Pool(4) as pool:
    results = pool.map(cpu_task, [10_000_000] * 8)
    # Uses 4 CPU cores truly in parallel


# 2. C extensions (NumPy, Pandas release GIL internally)
import numpy as np
# NumPy operations run in C — no GIL, true parallelism
arr = np.random.rand(10_000_000)
result = np.sum(arr ** 2)   # Runs on all cores via BLAS


# 3. concurrent.futures.ProcessPoolExecutor
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(cpu_task, n) for n in inputs]
    results = [f.result() for f in futures]


# 4. Cython / PyPy / Rust extensions (release GIL manually)
# 5. Python 3.13+: experimental free-threaded mode (no GIL!)
#    python3.13t (built with --disable-gil)
```


---

# CHAPTER 6: COMMON PITFALLS


## Concurrency Pitfalls

```
PITFALL 1: Race condition
  Two threads modify shared state → unpredictable result.
  Fix: use locks, atomics, or avoid shared mutable state.

PITFALL 2: Deadlock
  Thread A holds lock 1, waits for lock 2.
  Thread B holds lock 2, waits for lock 1.
  Fix: always acquire locks in consistent order. Use timeouts.

PITFALL 3: Livelock
  Threads keep yielding to each other, neither makes progress.
  Like two people in a hallway both stepping aside the same direction.
  Fix: add randomized backoff.

PITFALL 4: Starvation
  Low-priority thread never gets to run because high-priority threads dominate.
  Fix: fair locks, priority aging, bounded waiting.

PITFALL 5: Python GIL confusion
  Using threading for CPU-bound Python → no speedup.
  Fix: use multiprocessing or C extensions for CPU work.

PITFALL 6: Forgetting to join threads
  Main thread exits before worker threads finish → lost work, corrupted state.
  Fix: always join() or use executor context manager.

PITFALL 7: Shared mutable state without protection
  "It works in testing" — race conditions are non-deterministic.
  Fix: every shared variable needs synchronization or be immutable.

PITFALL 8: Over-synchronization
  Lock on every operation → effectively sequential (worse than single-threaded due to lock overhead).
  Fix: minimize critical sections, use lock-free where possible.

PITFALL 9: Async function that blocks
  Calling time.sleep() or requests.get() in async function blocks entire event loop.
  Fix: use await asyncio.sleep() and aiohttp/httpx async client.

PITFALL 10: Thread safety assumptions
  "Dict is thread-safe in Python" — GIL makes some ops atomic but NOT all.
  Fix: use threading.Lock or concurrent data structures.

PITFALL 11: Callback hell (pre-async)
  Deeply nested callbacks → unreadable.
  Fix: use async/await (it was invented to solve this).

PITFALL 12: Not handling task exceptions
  asyncio.gather swallows exceptions by default.
  Fix: use return_exceptions=True or TaskGroup (Python 3.11+).

PITFALL 13: Resource leaks in concurrent code
  Thread creates connection, crashes before closing.
  Fix: context managers (with), try/finally, RAII pattern.

PITFALL 14: Unbounded concurrency
  Launching 10,000 concurrent requests → overwhelm server/network.
  Fix: semaphore or thread pool with max_workers.

PITFALL 15: Testing concurrent code
  Race conditions don't show up in unit tests (deterministic).
  Fix: stress testing, ThreadSanitizer (C/C++/Go), property-based testing.
```