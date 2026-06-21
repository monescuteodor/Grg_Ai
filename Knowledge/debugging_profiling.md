# Advanced Debugging and Profiling Complete Reference


---

# CHAPTER 1: SYSTEMATIC DEBUGGING


## Remarks

Debugging is the most time-consuming part of software development. The difference between a junior and senior developer is not writing fewer bugs — it's finding and fixing them 10x faster. Systematic debugging replaces random guessing with methodical investigation. Profiling identifies performance bottlenecks with data, not intuition. Together they are the most valuable skills a developer can master.

Key concepts: **Scientific method** (hypothesis → test → observe), **Binary search debugging** (narrow the problem space), **Rubber duck debugging** (explain to find the flaw), **Reproduce first** (can't fix what you can't see), **Flame graphs** (visualize CPU time), **Heap snapshots** (find memory leaks), **Profiling** (measure before optimizing), **Post-mortems** (learn from incidents).


## The Debugging Process

```
STEP 1: REPRODUCE
  Can you make the bug happen reliably?
  If not → gather more info (logs, user steps, environment).
  Without reproduction → you're guessing.
  
  Questions:
    - What's the exact input/state that triggers it?
    - Does it happen every time or intermittently?
    - Which environment? (dev, staging, prod, specific OS/browser)
    - When did it start? (git bisect to find the commit)

STEP 2: ISOLATE
  Narrow down WHERE the bug is.
  
  Techniques:
    - Binary search: comment out half the code. Bug gone? It's in that half.
    - Minimal reproduction: strip away everything except the bug.
    - Print/log statements at key points (poor man's debugger).
    - Debugger breakpoints at suspected locations.
    - git bisect: find exact commit that introduced bug.

STEP 3: UNDERSTAND
  WHY does the bug happen?
  
  Don't just find the broken line — understand the ROOT CAUSE.
  "Off by one in loop" is the symptom.
  "No test for boundary condition" is the root cause.

STEP 4: FIX
  Change the minimum amount of code.
  Write a test that catches this bug (regression test).
  
  Verify: does the fix actually solve the problem?
  Verify: does the fix break anything else?

STEP 5: REFLECT
  How did this bug get in? How to prevent similar bugs?
  Update tests, add validation, improve documentation.
```


## Debugger Usage

```python
# PYTHON DEBUGGER (pdb / ipdb)

# Insert breakpoint in code
breakpoint()   # Python 3.7+ (uses pdb by default)

# Or explicitly
import pdb; pdb.set_trace()

# Or better: ipdb (colored, tab completion)
import ipdb; ipdb.set_trace()

# PDB COMMANDS:
# n (next):      execute next line (step over)
# s (step):      step INTO function call
# c (continue):  run until next breakpoint
# r (return):    run until current function returns
# l (list):      show code around current line
# p expr:        print expression value
# pp expr:       pretty-print expression
# w (where):     show call stack
# u (up):        go up one frame in call stack
# d (down):      go down one frame
# b 42:          set breakpoint at line 42
# b file.py:42:  breakpoint in specific file
# cl:            clear all breakpoints
# q (quit):      exit debugger

# CONDITIONAL BREAKPOINT:
# b 42, x > 100  → only break when x > 100

# POST-MORTEM debugging (after crash):
try:
    buggy_function()
except Exception:
    import pdb; pdb.post_mortem()
    # Drops you into the frame where exception occurred!


# JAVASCRIPT DEBUGGER
# In code:
# debugger;   // Browser DevTools stops here

# Chrome DevTools:
# F12 → Sources tab → click line number to set breakpoint
# Conditional breakpoint: right-click line → "Add conditional breakpoint"
# Logpoint: right-click → "Add logpoint" (logs without pausing)
# DOM breakpoint: right-click element → "Break on subtree modifications"
# XHR breakpoint: Sources → XHR/fetch Breakpoints → add URL pattern
# Event listener breakpoint: Sources → Event Listener Breakpoints


# NODE.JS DEBUGGER
# node --inspect server.js
# Open chrome://inspect in Chrome → click "inspect"
# Full DevTools debugging with breakpoints, profiling, heap snapshots
```


## Git Bisect

```bash
# Find EXACT commit that introduced a bug using binary search

git bisect start
git bisect bad                    # Current commit has the bug
git bisect good v1.0              # v1.0 was known good

# Git checks out middle commit
# Test manually:
git bisect good    # This commit is OK
# or
git bisect bad     # This commit has the bug

# Git narrows range, checks out next middle commit
# Repeat until found (~7 steps for 100 commits)

git bisect reset   # Return to original branch

# AUTOMATED (best!)
git bisect start HEAD v1.0
git bisect run npm test
# Git automatically finds the commit that broke the test!

# With custom script
git bisect run bash -c 'python -c "from mymodule import func; assert func(5) == 10"'
```


---

# CHAPTER 2: LOGGING FOR DEBUGGING


## Structured Logging

```python
import logging
import json
from datetime import datetime

# STRUCTURED LOGGING (machine-parseable, searchable)
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
)
logger = logging.getLogger(__name__)

def log_event(event: str, **kwargs):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event,
        **kwargs,
    }
    logger.info(json.dumps(entry))

# Usage
log_event("request_received", method="GET", path="/api/users", ip="1.2.3.4")
log_event("db_query", table="users", duration_ms=45, rows=150)
log_event("request_completed", status=200, duration_ms=120)

# Output (JSON lines — parseable by log aggregators):
# {"timestamp":"2026-06-10T14:30:00","event":"request_received","method":"GET","path":"/api/users"}
# {"timestamp":"2026-06-10T14:30:00","event":"db_query","table":"users","duration_ms":45}


# LOG LEVELS (use correctly!):
# DEBUG:    detailed diagnostic info (disabled in production)
# INFO:     normal operation events (request received, job completed)
# WARNING:  unexpected but handled (retry succeeded, fallback used)
# ERROR:    operation failed (request error, timeout, exception)
# CRITICAL: system failure (database down, out of memory)

# WHAT TO LOG:
#   ✅ Request start/end with duration
#   ✅ External service calls (DB, API, cache) with duration
#   ✅ Errors with full context (user_id, request_id, input)
#   ✅ Business events (order created, payment processed)
#   ✅ State transitions (user activated, job queued → running → completed)

# WHAT NOT TO LOG:
#   ❌ Passwords, tokens, credit cards, PII
#   ❌ Every loop iteration (too verbose)
#   ❌ Success for trivially common operations


# REQUEST ID (correlate logs across services)
import uuid

class RequestContext:
    def __init__(self):
        self.request_id = str(uuid.uuid4())[:8]

    def log(self, event, **kwargs):
        log_event(event, request_id=self.request_id, **kwargs)

ctx = RequestContext()
ctx.log("request_start", path="/api/users")
ctx.log("cache_miss", key="users:all")
ctx.log("db_query", duration_ms=45)
ctx.log("request_end", status=200, total_ms=120)
# All logs share request_id → can trace full request lifecycle
```


---

# CHAPTER 3: CPU PROFILING


## Python Profiling

```python
# cProfile — built-in profiler
import cProfile
import pstats

# Profile a function
cProfile.run('heavy_function()', 'output.prof')

# Analyze results
stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative')
stats.print_stats(20)   # Top 20 functions by cumulative time

# Output:
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#     1000    2.500    0.003    5.000    0.005 database.py:42(query)
#     5000    1.200    0.000    1.200    0.000 utils.py:10(parse)
#     1       0.001    0.001   12.000   12.000 main.py:1(process_all)

# COLUMNS:
# ncalls:  number of calls
# tottime: time in this function ONLY (excluding subcalls)
# cumtime: time in this function INCLUDING subcalls
# percall: per-call average

# Profile decorator
def profile(func):
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)
        return result
    return wrapper

@profile
def my_function():
    pass


# LINE PROFILER (per-line timing — most useful!)
# pip install line_profiler

# Add decorator
# @profile      # line_profiler's decorator (different from above)
# def slow_function():
#     data = load_data()        #   0.5s
#     processed = process(data) #  12.0s  ← BOTTLENECK
#     save(processed)           #   0.3s

# Run: kernprof -l -v script.py


# py-spy (sampling profiler — no code changes, attach to running process!)
# pip install py-spy

# Profile running process
# py-spy top --pid 12345
# py-spy record --pid 12345 -o profile.svg   # Flame graph!

# Profile script
# py-spy record -o profile.svg -- python script.py
```


## Flame Graphs

```
FLAME GRAPH: visualization of where CPU time is spent.

  X-axis: proportion of time (wider = more time)
  Y-axis: call stack depth (bottom = entry, top = leaf)

READING:
  ┌──────────────────────────────────────────────┐
  │                    main()                      │ Entry point
  ├───────────────────────┬────────────────────────┤
  │     process_data()    │     send_results()     │ 60% vs 40%
  ├──────────┬────────────┤                        │
  │ parse()  │  transform()│                       │
  │  20%     │    40%      │                       │
  └──────────┴────────────┴────────────────────────┘

  transform() is the widest box → taking 40% of CPU time.
  THIS is where to optimize.

TOOLS:
  py-spy record → SVG flame graph (Python)
  perf record + flamegraph.pl (Linux, any language)
  async-profiler (Java)
  Chrome DevTools → Performance tab (JavaScript)
  Instruments → Time Profiler (macOS/iOS)
  speedscope.app (universal viewer — open any profile)

TYPES:
  CPU flame graph:    where CPU time goes
  Off-CPU flame graph: where time is spent WAITING (I/O, locks)
  Memory flame graph:  where allocations happen
  
  Off-CPU is crucial: function shows 0% CPU but takes 5 seconds
  because it's waiting on network/disk/lock.


# Generate flame graph on Linux (any language)
# perf record -g -p PID sleep 30
# perf script | stackcollapse-perf.pl | flamegraph.pl > profile.svg
```


## Node.js Profiling

```javascript
// Built-in profiler
// node --prof app.js
// → generates isolate-xxx.log
// node --prof-process isolate-xxx.log > processed.txt

// Clinic.js (excellent Node profiler suite)
// npx clinic doctor -- node server.js
// npx clinic flame -- node server.js    // Flame graph
// npx clinic bubbleprof -- node server.js  // Async bottlenecks

// Chrome DevTools (best for interactive debugging)
// node --inspect server.js
// Open chrome://inspect → click inspect
// Performance tab → Record → do actions → Stop
// → Flame chart, call tree, bottom-up analysis

// console.time for quick measurements
console.time('database-query');
await db.query('SELECT * FROM users');
console.timeEnd('database-query');
// Output: database-query: 45.123ms

// Performance hooks (Node.js)
const { performance, PerformanceObserver } = require('perf_hooks');

const obs = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
        console.log(`${entry.name}: ${entry.duration.toFixed(2)}ms`);
    }
});
obs.observe({ entryTypes: ['measure'] });

performance.mark('start');
await doWork();
performance.mark('end');
performance.measure('doWork', 'start', 'end');
```


---

# CHAPTER 4: MEMORY PROFILING


## Finding Memory Leaks

```python
# Python memory profiling

# tracemalloc (built-in, Python 3.4+)
import tracemalloc

tracemalloc.start()

# ... run code that might leak ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("Top 10 memory consumers:")
for stat in top_stats[:10]:
    print(stat)

# Output:
# /app/models.py:42: size=10.5 MiB, count=150000, average=73 B
# /app/cache.py:15: size=5.2 MiB, count=50000, average=109 B

# Compare snapshots (find growth)
snapshot1 = tracemalloc.take_snapshot()
do_work()
snapshot2 = tracemalloc.take_snapshot()

diff = snapshot2.compare_to(snapshot1, 'lineno')
print("Memory growth:")
for stat in diff[:10]:
    print(stat)
# Shows which lines INCREASED memory between snapshots


# memory_profiler (per-line memory usage)
# pip install memory_profiler

from memory_profiler import profile

@profile
def my_function():
    a = [1] * 1000000       # +7.6 MiB
    b = [2] * 2000000       # +15.3 MiB
    del b                    # -15.3 MiB
    return a

# Run: python -m memory_profiler script.py


# objgraph (find reference cycles, object growth)
# pip install objgraph

import objgraph

objgraph.show_most_common_types(limit=10)
# dict       15234
# list       8456
# function   3201

objgraph.show_growth(limit=5)   # Objects created since last call
# Call periodically to find leaks:
# list  +500  (growing!)
# dict  +200  (growing!)
```


## JavaScript Memory Profiling

```javascript
// Chrome DevTools → Memory tab

// 1. HEAP SNAPSHOT
//    Take snapshot → find large objects
//    Take another after actions → compare (delta)
//    Filter by "Objects allocated between snapshot 1 and 2"

// 2. ALLOCATION TIMELINE
//    Record → do actions → stop
//    Shows WHERE and WHEN memory was allocated
//    Blue bars = still alive (potential leak)
//    Gray bars = garbage collected (OK)

// 3. ALLOCATION SAMPLING
//    Lower overhead than timeline
//    Good for production profiling

// Common Node.js memory leaks:

// LEAK 1: Growing array/cache without eviction
const cache = {};   // Never cleared!
function handle(req) {
    cache[req.id] = processData(req);   // Grows forever
}
// FIX: use LRU cache with max size
const LRU = require('lru-cache');
const cache = new LRU({ max: 1000 });

// LEAK 2: Event listener accumulation
function setupConnection() {
    emitter.on('data', handleData);
    // Called 1000 times → 1000 listeners registered!
}
// FIX: remove listeners, or use once()
function setupConnection() {
    emitter.removeAllListeners('data');
    emitter.on('data', handleData);
}

// LEAK 3: Closure holding reference
function createHandler() {
    const hugeData = loadHugeDataset();   // 100MB
    return function handler(req) {
        // Uses hugeData only for one field
        return { config: hugeData.config };
    };
    // hugeData is captured by closure → never GC'd!
}
// FIX: extract what you need
function createHandler() {
    const config = loadHugeDataset().config;   // Only keep config
    return function handler(req) {
        return { config };
    };
}


// Monitor memory in production
setInterval(() => {
    const usage = process.memoryUsage();
    console.log({
        rss: Math.round(usage.rss / 1024 / 1024) + 'MB',
        heapUsed: Math.round(usage.heapUsed / 1024 / 1024) + 'MB',
        heapTotal: Math.round(usage.heapTotal / 1024 / 1024) + 'MB',
    });
}, 30000);

// If heapUsed keeps growing over hours → leak!
```


---

# CHAPTER 5: POST-MORTEM AND INCIDENT RESPONSE


## Post-Mortem Template

```
INCIDENT POST-MORTEM

Title: [Brief description]
Date: [When it happened]
Duration: [How long]
Severity: [P1/P2/P3/P4]
Author: [Who wrote this]

SUMMARY:
  One paragraph describing what happened and impact.

TIMELINE (UTC):
  14:00 - Deployment of v2.3.1 started
  14:05 - Deployment completed
  14:12 - Error rate spike detected by monitoring
  14:15 - On-call engineer paged
  14:20 - Investigation started
  14:35 - Root cause identified: missing DB migration
  14:40 - Rollback to v2.3.0 initiated
  14:45 - Rollback completed, error rate normalizing
  14:55 - Incident resolved, all systems nominal

ROOT CAUSE:
  Database migration for new column was not included in
  deployment pipeline. Application code expected column
  "user_preferences" which didn't exist, causing 500 errors
  on all user profile requests.

IMPACT:
  - 30 minutes of degraded service
  - ~5,000 users affected
  - Profile pages returned 500 errors
  - No data loss

WHAT WENT WELL:
  - Monitoring detected the issue within 7 minutes
  - Rollback was fast and clean
  - On-call response time was excellent

WHAT WENT WRONG:
  - Migration not included in deploy checklist
  - No pre-deploy smoke test for new endpoints
  - Staging environment didn't catch it (different DB state)

ACTION ITEMS:
  [ ] Add DB migration check to CI/CD pipeline (owner: Alice, due: June 15)
  [ ] Add smoke test for critical endpoints post-deploy (owner: Bob, due: June 20)
  [ ] Sync staging DB schema with production weekly (owner: Carol, due: June 22)
  [ ] Add runbook for "500 spike after deploy" scenario (owner: Dave, due: June 25)

LESSONS LEARNED:
  Post-mortems are BLAMELESS. We focus on systems, not people.
  The question is "how did the system allow this?" not "who caused this?"
```


---

# CHAPTER 6: COMMON PITFALLS


## Debugging and Profiling Pitfalls

```
PITFALL 1: Debugging by guessing
  "I think it's this line..." → change random things → hours wasted.
  Fix: reproduce → isolate → understand → fix. Scientific method.

PITFALL 2: Not reproducing first
  "User says it's broken" → start changing code.
  Fix: reproduce the exact bug FIRST. Then fix.

PITFALL 3: Fixing symptoms, not root cause
  Add try-catch around crash → bug "fixed" but real issue remains.
  Fix: understand WHY it crashes, fix the cause.

PITFALL 4: Optimizing without profiling
  "This function looks slow" → rewrite in C.
  Fix: profile first. The bottleneck is often NOT where you think.

PITFALL 5: Premature optimization
  Optimizing code that runs once during startup.
  Fix: optimize hot paths (inner loops, per-request code).

PITFALL 6: Console.log debugging in production
  Leaves debug logs that expose internals or fill disk.
  Fix: use proper logging levels. DEBUG only in development.

PITFALL 7: Ignoring warnings
  "It's just a deprecation warning" → breaks in next version.
  Fix: fix warnings promptly. Treat warnings as errors in CI.

PITFALL 8: No error context
  Log: "Error: null". Useless.
  Fix: log with context: user_id, request_id, input, stack trace.

PITFALL 9: Blaming users
  "User did something wrong."
  Fix: if users can trigger errors, that's YOUR bug to handle.

PITFALL 10: Not writing regression tests
  Fix bug → no test → same bug returns months later.
  Fix: every bug fix includes a test that catches it.

PITFALL 11: Debugging in production
  Adding print statements to production code.
  Fix: structured logging, feature flags for debug mode, observability.

PITFALL 12: Ignoring intermittent failures
  "It only fails sometimes, probably transient."
  Fix: intermittent bugs are the WORST bugs. Race conditions, memory corruption.

PITFALL 13: Tool overload
  Learning 10 profiling tools superficially.
  Fix: master ONE profiler deeply (py-spy, Chrome DevTools, perf).

PITFALL 14: Not monitoring post-fix
  Deploy fix → move on → bug is actually still happening.
  Fix: watch metrics/logs for 30 minutes after deploy.

PITFALL 15: Blameful post-mortems
  "Bob broke production." → people hide mistakes → fewer learnings.
  Fix: blameless post-mortems. Focus on systems and processes.
```