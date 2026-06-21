# Operating Systems Concepts Complete Reference


---

# CHAPTER 1: PROCESSES AND THREADS


## Remarks

An operating system (OS) manages hardware resources and provides abstractions for programs. Understanding OS concepts is critical for writing performant software, debugging production issues (memory leaks, zombie processes, file descriptor exhaustion), and designing systems that scale. Every program runs within the OS's constraints.

Key concepts: **Process** (running program with own memory), **Thread** (lightweight execution unit within a process), **Scheduling** (which process runs when), **Virtual memory** (illusion of infinite RAM), **System calls** (interface between userspace and kernel), **File systems** (persistent storage abstraction), **IPC** (inter-process communication), **Signals** (async notifications), **File descriptors** (handles to I/O resources).

Tools: **top/htop** (process monitor), **ps** (process list), **strace/ltrace** (syscall tracing), **lsof** (open files), **vmstat/free** (memory), **iostat** (disk I/O), **perf** (performance profiling), **/proc** (virtual filesystem with kernel info).


## Process Lifecycle

```
STATES:
  New       → process being created
  Ready     → waiting for CPU (in ready queue)
  Running   → executing on CPU
  Blocked   → waiting for I/O, lock, or event
  Terminated → finished execution

  New → Ready → Running → Terminated
                  ↕
               Blocked

PROCESS CREATION:
  fork()    Create child process (copy of parent)
  exec()    Replace process image with new program
  
  Common pattern (Unix):
    pid = fork()
    if pid == 0:
        # Child process
        exec("/usr/bin/python3", "script.py")
    else:
        # Parent process
        wait(pid)   # Wait for child to finish

PROCESS ATTRIBUTES:
  PID:          unique process ID
  PPID:         parent process ID
  UID/GID:      user/group (determines permissions)
  File descriptors: open files, sockets, pipes
  Memory map:   code, data, heap, stack
  Environment:  env variables
  CWD:          current working directory
  Signal handlers: how to handle signals
```


## Process Memory Layout

```
HIGH ADDRESSES
┌─────────────────────┐
│     Kernel space     │  Not accessible from userspace
├─────────────────────┤
│       Stack          │  Function calls, local variables
│         ↓            │  Grows downward
│                      │
│         ↑            │
│        Heap          │  Dynamic allocation (malloc/new)
│                      │  Grows upward
├─────────────────────┤
│    BSS (uninitialized)│ Global vars initialized to 0
├─────────────────────┤
│    Data (initialized) │ Global vars with values
├─────────────────────┤
│    Text (code)       │  Executable instructions (read-only)
└─────────────────────┘
LOW ADDRESSES

STACK:
  - Function call frames (return address, parameters, locals)
  - Fixed size per thread (default 1-8 MB)
  - Stack overflow: recursion too deep → crash
  - Allocation: automatic (push/pop on function call/return)
  - Very fast (just move stack pointer)

HEAP:
  - Dynamic allocation (malloc, calloc, new, Python objects)
  - Managed by allocator (glibc malloc, jemalloc, tcmalloc)
  - Must be freed (C/C++) or garbage collected (Java, Python, Go)
  - Fragmentation: many small allocs/frees → unusable gaps
  - Slower than stack (allocator overhead, potential cache misses)

MEMORY LEAK:
  Allocate on heap but never free.
  Memory usage grows until OOM (Out Of Memory) killer intervenes.
  
  C:      malloc() without free()
  Java:   objects referenced but unused (held by collection)
  Python: reference cycles (usually caught by GC), C extension leaks
  Node:   closures holding references, event listener accumulation
```


## Linux Process Commands

```bash
# View processes
ps aux                           # All processes, detailed
ps aux | grep python             # Find Python processes
ps -ef --forest                  # Process tree

# Real-time monitor
top                              # Classic
htop                             # Better (interactive, colored)
# In htop: F5 = tree view, F6 = sort, F9 = kill

# Process details
cat /proc/PID/status             # Detailed status
cat /proc/PID/maps               # Memory map
cat /proc/PID/fd                 # Open file descriptors
ls -la /proc/PID/fd | wc -l     # Count open files

# Create processes
command &                        # Run in background
nohup command &                  # Survive terminal close
disown %1                        # Detach job from terminal

# Kill processes
kill PID                         # Send SIGTERM (graceful)
kill -9 PID                      # Send SIGKILL (force, can't be caught)
kill -HUP PID                    # Send SIGHUP (reload config)
killall python3                  # Kill all Python processes
pkill -f "server.py"             # Kill by command name pattern

# Process priority
nice -n 10 command               # Start with lower priority
renice -n -5 -p PID              # Change running process priority
# -20 (highest priority) to 19 (lowest)

# Wait for process
wait PID                         # Shell built-in
```


## Signals

```
COMMON SIGNALS:

SIGHUP   (1):   Terminal closed. Convention: reload config.
SIGINT   (2):   Ctrl+C. Interrupt. Graceful stop.
SIGQUIT  (3):   Ctrl+\. Quit with core dump.
SIGKILL  (9):   CANNOT be caught. Immediate death.
SIGSEGV  (11):  Segmentation fault (invalid memory access).
SIGTERM  (15):  Default kill signal. Graceful shutdown.
SIGCHLD  (17):  Child process terminated.
SIGSTOP  (19):  CANNOT be caught. Pause process (Ctrl+Z sends SIGTSTP).
SIGCONT  (18):  Resume paused process.
SIGUSR1  (10):  User-defined signal 1.
SIGUSR2  (12):  User-defined signal 2.
```

```python
import signal
import sys

def graceful_shutdown(signum, frame):
    print(f"Received signal {signum}. Cleaning up...")
    close_database()
    save_state()
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)

# Ignore signal
signal.signal(signal.SIGHUP, signal.SIG_IGN)
```


---

# CHAPTER 2: CPU SCHEDULING


## Scheduling Algorithms

```
PROBLEM: N processes, M CPUs (usually N >> M).
Which process runs on which CPU, and for how long?

GOALS:
  Maximize CPU utilization
  Maximize throughput (processes completed per time)
  Minimize latency (time to start/finish)
  Fairness (no starvation)

FCFS (First Come, First Served):
  Run each process until completion or I/O block.
  Simple but convoy effect: one slow process blocks all.

ROUND ROBIN:
  Each process gets fixed time slice (quantum, typically 10-100ms).
  After quantum expires → back to ready queue.
  Fair but context switching overhead.
  
  Short quantum: responsive but high overhead.
  Long quantum: less overhead but poor response time.

PRIORITY SCHEDULING:
  Each process has priority number.
  Higher priority runs first.
  Problem: starvation (low priority never runs).
  Fix: aging (increase priority over time).

MULTILEVEL FEEDBACK QUEUE (MLFQ):
  Multiple queues with different priorities.
  New process starts at highest priority.
  If uses full quantum → demoted to lower queue.
  If does I/O (yields early) → stays at high priority.
  
  Effect: interactive processes (I/O-bound) get high priority.
          CPU-bound processes get lower priority.
  
  Used by: Linux CFS (Completely Fair Scheduler) is similar concept.

CFS (Completely Fair Scheduler — Linux default):
  Uses red-black tree of processes sorted by "virtual runtime".
  Process with least vruntime runs next.
  vruntime increases faster for low-priority processes.
  O(log n) pick-next, O(log n) insert.
  
  Nice values: -20 (highest priority) to +19 (lowest).
  Default nice = 0.
```


## Context Switch

```
CONTEXT SWITCH: saving state of current process, loading state of next.

WHAT'S SAVED:
  CPU registers (general purpose, program counter, stack pointer)
  Memory mappings (page table pointer)
  Kernel stack
  Floating point state
  I/O state

COST:
  Direct: ~1-10 microseconds (save/restore registers)
  Indirect: cache pollution (new process has cold cache)
  TLB flush (translation lookaside buffer — virtual→physical mapping cache)
  
  Total effective cost: 10-100 microseconds
  
  This is why:
  - Too many threads = too many context switches = slow
  - Async I/O (single thread) avoids context switches
  - Go's goroutines: user-space scheduling, cheaper context switch
```


---

# CHAPTER 3: MEMORY MANAGEMENT


## Virtual Memory

```
VIRTUAL MEMORY: each process sees its own address space (0 to 2^64).
Physical RAM is shared and managed by OS transparently.

PAGE TABLE:
  Virtual address → Physical address mapping.
  Memory divided into pages (typically 4 KB).
  
  Virtual Page 0 → Physical Frame 42
  Virtual Page 1 → Physical Frame 7
  Virtual Page 2 → [DISK] (swapped out)
  Virtual Page 3 → [UNMAPPED] (segfault if accessed)

TLB (Translation Lookaside Buffer):
  CPU cache for page table entries.
  TLB hit: ~1 ns (fast!)
  TLB miss: ~10-100 ns (walk page table)
  Context switch: may flush TLB (expensive!)

PAGE FAULT:
  Process accesses page not in physical RAM.
  
  Minor fault: page is in memory but not mapped yet (first access).
    → Map and continue. Fast.
  
  Major fault: page is on disk (swapped out).
    → Read from disk → map → continue. SLOW (~10ms = millions of cycles).
  
  Invalid fault: page doesn't exist (unmapped region).
    → SIGSEGV → process crash.

SWAP:
  When RAM is full, OS moves least-recently-used pages to disk.
  Disk is 100,000x slower than RAM.
  Heavy swapping = "thrashing" = system crawls.
  
  Monitor: vmstat, free -h, /proc/meminfo
  
  Production servers often DISABLE swap:
    swapoff -a
  Better to OOM-kill one process than thrash everything.
```


## Memory Tools

```bash
# Memory overview
free -h                          # Total, used, free, cached
cat /proc/meminfo                # Detailed memory info
vmstat 1                         # Memory stats every 1 second

# Process memory
ps aux --sort=-%mem | head -10   # Top memory consumers
pmap PID                         # Memory map of process
cat /proc/PID/status | grep -i vm  # VmRSS, VmSize

# KEY METRICS:
# VmSize (VSZ): total virtual memory (includes mapped files, shared libs)
# VmRSS (RSS):  resident set size = actually in physical RAM
# RSS is what matters for "how much RAM is this using?"

# OOM Killer
dmesg | grep -i "oom\|killed"    # Check if OOM killer ran
cat /proc/PID/oom_score          # OOM score (higher = more likely to be killed)

# Memory leak detection
valgrind --leak-check=full ./program   # C/C++ (comprehensive)
# Python: tracemalloc, objgraph
# Node: --inspect + Chrome DevTools heap snapshot
# Go: pprof
```


---

# CHAPTER 4: FILE SYSTEMS AND I/O


## File Descriptors

```
FILE DESCRIPTOR (FD): integer handle to an I/O resource.
Every process starts with:
  0 = stdin  (standard input)
  1 = stdout (standard output)
  2 = stderr (standard error)

FDs represent: files, sockets, pipes, devices, /proc entries.
Everything in Unix is a file (or file-like).

LIMIT:
  Per-process: ulimit -n (default 1024, can increase)
  System-wide: /proc/sys/fs/file-max
  
  Running out of FDs → "Too many open files" error.
  Common cause: connection leak (open socket, never close).

CHECK:
  ls -la /proc/PID/fd | wc -l     # FDs used by process
  lsof -p PID                      # List open files/sockets
  lsof -i :8000                    # What's using port 8000?
```

```bash
# Redirect
command > output.txt              # stdout to file (overwrite)
command >> output.txt             # stdout to file (append)
command 2> errors.txt             # stderr to file
command > out.txt 2>&1            # Both stdout and stderr to file
command 2>/dev/null               # Discard errors
command < input.txt               # File as stdin

# Pipes
command1 | command2               # stdout of 1 → stdin of 2
ls -la | grep ".py" | wc -l      # Chain commands

# Process substitution
diff <(sort file1) <(sort file2)  # Compare sorted versions
```


## I/O Models

```
BLOCKING I/O (default):
  Thread calls read() → blocks until data available.
  Simple but one thread stuck per I/O operation.

NON-BLOCKING I/O:
  read() returns immediately with data or EAGAIN (no data yet).
  Application must poll repeatedly (busy-waiting, wasteful).

I/O MULTIPLEXING (select/poll/epoll):
  Monitor MULTIPLE file descriptors with ONE thread.
  "Tell me when ANY of these 1000 sockets has data."
  
  select():  O(n) scan, limited to 1024 FDs. Legacy.
  poll():    O(n) scan, no FD limit. Better.
  epoll():   O(1) notification, no FD limit. Linux-specific. BEST.
  kqueue():  BSD/macOS equivalent of epoll.
  
  This is how Node.js, Nginx, and Redis handle thousands of connections
  with a single thread.

ASYNC I/O (io_uring, Linux 5.1+):
  Submit I/O requests to kernel ring buffer.
  Kernel completes them asynchronously.
  Application polls completion queue.
  Zero-copy possible. Lowest overhead.
  Used by: modern database engines, high-performance networking.

COMPARISON (10,000 concurrent connections):
  Blocking:      10,000 threads × 1MB stack = 10 GB RAM
  epoll:         1 thread, 10,000 FDs monitored = ~10 MB RAM
  io_uring:      1 thread, zero-copy = even less overhead
```


---

# CHAPTER 5: INTER-PROCESS COMMUNICATION (IPC)


## IPC Mechanisms

```
PIPES:
  Unidirectional byte stream between related processes.
  ls | grep ".py"  → pipe connects ls's stdout to grep's stdin.
  
  Named pipes (FIFO): persist in filesystem, unrelated processes can use.
    mkfifo /tmp/mypipe
    echo "hello" > /tmp/mypipe    # Blocks until reader
    cat /tmp/mypipe               # Reads "hello"

SOCKETS:
  Network communication (TCP/UDP) or local (Unix domain sockets).
  Unix socket: /var/run/docker.sock, /tmp/mysql.sock
  Faster than TCP loopback for same-machine communication.

SHARED MEMORY:
  Fastest IPC — both processes access same physical memory.
  Must use synchronization (semaphore/mutex) to avoid races.
  
  POSIX: shm_open(), mmap()
  Python: multiprocessing.shared_memory

MESSAGE QUEUES:
  Kernel-managed queue. Processes send/receive discrete messages.
  POSIX: mq_open(), mq_send(), mq_receive()
  Higher level: Redis pub/sub, RabbitMQ, ZeroMQ

SIGNALS:
  Async notification to process.
  Limited information (just the signal number).
  kill -SIGUSR1 PID

MEMORY-MAPPED FILES:
  Map file into process address space.
  Changes to memory → reflected in file (and vice versa).
  Multiple processes can mmap same file = shared memory via filesystem.
```


---

# CHAPTER 6: SYSTEM CALLS


## Essential Syscalls

```
PROCESS:
  fork()      Create child process
  exec()      Replace process image
  wait()      Wait for child termination
  exit()      Terminate process
  getpid()    Get process ID
  kill()      Send signal to process

FILE:
  open()      Open file, get FD
  close()     Close FD
  read()      Read bytes from FD
  write()     Write bytes to FD
  lseek()     Move file position
  stat()      Get file metadata
  unlink()    Delete file
  mkdir()     Create directory
  rename()    Rename/move file

MEMORY:
  mmap()      Map memory/file
  munmap()    Unmap memory
  brk()       Change heap size (used by malloc internally)

NETWORK:
  socket()    Create socket
  bind()      Bind to address
  listen()    Start listening
  accept()    Accept connection
  connect()   Connect to server
  send/recv() Send/receive data

MISC:
  ioctl()     Device control
  select()/poll()/epoll()  I/O multiplexing
  clone()     Create thread/process (Linux-specific)
```


## Tracing System Calls

```bash
# strace: trace system calls of a process
strace ls                        # Trace ls command
strace -p PID                    # Attach to running process
strace -c command                # Count/summary of syscalls
strace -e trace=network command  # Only network syscalls
strace -e trace=file command     # Only file syscalls
strace -f command                # Follow child processes
strace -t command                # Show timestamps
strace -T command                # Show time spent in each syscall

# Output shows:
# open("/etc/passwd", O_RDONLY) = 3        (returned FD 3)
# read(3, "root:x:0:0:root:/root:/bin/bash\n", 4096) = 1234
# close(3) = 0

# ltrace: trace library calls (malloc, printf, etc.)
ltrace command

# PRACTICAL: why is my program slow?
strace -c -p PID
# Shows: 80% time in futex() → lock contention
# Shows: 60% time in read() → I/O bound
# Shows: 90% time in nanosleep() → sleeping/polling
```


---

# CHAPTER 7: COMMON PITFALLS


## OS Pitfalls

```
PITFALL 1: Zombie processes
  Child exits but parent doesn't call wait() → zombie.
  Shows as <defunct> in ps. Consumes PID slot.
  Fix: always wait() on children. Use SIGCHLD handler.

PITFALL 2: File descriptor leak
  Open files/sockets without closing → "Too many open files."
  Fix: always close FDs. Use context managers (with statement).
  Check: lsof -p PID | wc -l

PITFALL 3: Fork bomb
  :(){ :|:& };: → creates processes exponentially → system crash.
  Fix: ulimit -u (max user processes). cgroups in production.

PITFALL 4: Ignoring signals
  SIGTERM sent but process doesn't handle it → unclean shutdown.
  Fix: handle SIGTERM and SIGINT for graceful cleanup.

PITFALL 5: Running as root
  Everything has full access → one bug = total compromise.
  Fix: run as unprivileged user. Use capabilities for specific permissions.

PITFALL 6: Swap thrashing
  Too many processes, not enough RAM → constant swapping → system crawls.
  Fix: add RAM, reduce processes, disable swap (production servers).

PITFALL 7: Disk full
  /var/log fills up → application can't write → crash.
  Fix: log rotation (logrotate), monitoring, disk usage alerts.

PITFALL 8: ulimit too low
  Default 1024 open files → web server fails under load.
  Fix: ulimit -n 65535 in service config or /etc/security/limits.conf.

PITFALL 9: OOM killer surprise
  Linux kills largest process when RAM exhausted.
  Fix: set oom_score_adj for critical processes. Monitor memory usage.

PITFALL 10: Not using cgroups/containers
  One runaway process consumes all CPU/RAM.
  Fix: cgroups limit CPU, memory, I/O per process group. Docker uses cgroups.

PITFALL 11: Ignoring EINTR
  System call interrupted by signal → returns EINTR error.
  Fix: retry the syscall. Most high-level languages handle this.

PITFALL 12: PATH and environment assumptions
  Script works in terminal but fails in cron/systemd (different PATH).
  Fix: use absolute paths. Set environment explicitly in service files.

PITFALL 13: Time zone confusion
  Server in UTC, logs in local time, database in another timezone.
  Fix: use UTC everywhere. Convert to local only at display.

PITFALL 14: Not monitoring I/O wait
  CPU looks idle but system is slow → disk I/O bottleneck.
  Check: top shows %wa (I/O wait). Fix: faster disk, reduce I/O, caching.

PITFALL 15: Symlink and permission confusion
  Symlink has different permissions than target.
  Fix: check real file permissions. Use stat, not ls -l on symlink.
```