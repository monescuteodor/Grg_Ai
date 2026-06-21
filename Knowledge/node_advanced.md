# Node.js Advanced Complete Reference


---

# CHAPTER 1: NODE.JS RUNTIME INTERNALS


## Remarks

Node.js is a JavaScript runtime built on Chrome's V8 engine, designed for asynchronous, event-driven server applications. Created by Ryan Dahl in 2009 to solve the "thousands of concurrent connections" problem. Single-threaded but highly concurrent via the event loop. Powers Netflix, Uber, LinkedIn, PayPal backends.

Key concepts: **Event Loop** (libuv-based async scheduling), **Non-blocking I/O** (kernel async), **Streams** (data flowing in chunks), **Buffers** (raw binary), **Worker Threads** (parallel CPU work), **Clustering** (multi-process), **EventEmitter** (pub-sub patterns), **N-API** (native modules).

Used at: backend servers, CLI tools, build tools (Webpack, Vite), serverless (Lambda, Vercel), desktop (Electron), real-time (Socket.IO).

Tools: **npm/yarn/pnpm** (package managers), **TypeScript** (typed JS, very common), **Node Test Runner / Vitest / Jest** (testing), **ESLint** (linting), **PM2** (process manager), **clinic.js** (profiling), **Node Inspector** (debugging).


## The Event Loop

```
SINGLE-THREADED MODEL:
  Node.js JavaScript runs on ONE thread (main thread).
  Async I/O delegated to libuv thread pool / kernel.
  Callbacks queued; event loop picks them up.

EVENT LOOP PHASES (in order, each cycle):

  ┌───────────────────────────┐
  │ timers                    │  setTimeout, setInterval
  ├───────────────────────────┤
  │ pending callbacks         │  some system operations
  ├───────────────────────────┤
  │ idle, prepare             │  internal
  ├───────────────────────────┤
  │ poll                      │  I/O callbacks, retrieve new I/O
  ├───────────────────────────┤
  │ check                     │  setImmediate
  ├───────────────────────────┤
  │ close callbacks           │  socket.on('close'), etc.
  └───────────────────────────┘
              │
              └─► back to timers (next iteration)

MICROTASKS (Promise.then, queueMicrotask, process.nextTick):
  Run AFTER each phase callback, before next phase.
  process.nextTick has even higher priority than promises.
  
  CAREFUL: Recursive nextTick can starve I/O!
```


## process.nextTick vs setImmediate vs setTimeout

```javascript
console.log('1. sync');

setTimeout(() => console.log('2. setTimeout'), 0);
setImmediate(() => console.log('3. setImmediate'));

Promise.resolve().then(() => console.log('4. promise'));

process.nextTick(() => console.log('5. nextTick'));

console.log('6. sync end');

// Output:
// 1. sync
// 6. sync end
// 5. nextTick           ← highest priority microtask
// 4. promise            ← microtask, after nextTick
// 2. setTimeout         ← timer phase
// 3. setImmediate       ← check phase
// (setTimeout vs setImmediate order can vary outside I/O context)

// Inside an I/O callback, setImmediate ALWAYS runs first:
fs.readFile('file', () => {
    setTimeout(() => console.log('timeout'), 0);
    setImmediate(() => console.log('immediate'));
    // Output: immediate, then timeout (deterministic here)
});
```

**When to use what:**
- `process.nextTick`: emit events synchronously after constructor; rarely needed in app code
- `setImmediate`: yield to event loop, run on next iteration (most common)
- `setTimeout(0)`: minimum delay, but actually 1ms+ in practice
- `Promise/await`: standard async


## Blocking the Event Loop

```javascript
// BAD: blocks event loop for ~5 seconds!
function fibonacci(n) {
    if (n < 2) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

app.get('/fib/:n', (req, res) => {
    const result = fibonacci(parseInt(req.params.n));  // BLOCKS!
    res.json({ result });
});

// During the calculation: ENTIRE SERVER unresponsive.
// All concurrent requests hang.

// SOLUTIONS:

// 1. Worker threads (CPU work)
import { Worker } from 'worker_threads';

app.get('/fib/:n', (req, res) => {
    const worker = new Worker('./fib-worker.js', {
        workerData: { n: parseInt(req.params.n) }
    });
    worker.on('message', result => res.json({ result }));
    worker.on('error', err => res.status(500).json({ error: err.message }));
});

// 2. Break work into chunks with setImmediate
function fibAsync(n) {
    return new Promise((resolve) => {
        function step(curr, prev, i) {
            if (i === n) return resolve(curr);
            setImmediate(() => step(curr + prev, curr, i + 1));
        }
        step(0, 1, 0);
    });
}

// 3. Offload to external service / queue
// Use a job queue (BullMQ, RabbitMQ) for heavy work
```


## Heap Memory and Garbage Collection

```javascript
// View heap stats
console.log(process.memoryUsage());
// {
//   rss: 50_000_000,         // Resident Set Size — total memory
//   heapTotal: 30_000_000,   // V8 allocated to heap
//   heapUsed: 20_000_000,    // V8 actually using
//   external: 2_000_000,     // C++ objects bound to JS
//   arrayBuffers: 1_000_000  // ArrayBuffer/SharedArrayBuffer
// }

// V8 generational GC:
//   - New space (young) — short-lived, fast minor GC
//   - Old space — long-lived, slow major GC
//
//   Objects survive 2 minor GCs → promoted to old space

// Force GC (only with --expose-gc flag, mostly for debugging)
node --expose-gc app.js
// In code:
if (global.gc) global.gc();

// Limit heap size
node --max-old-space-size=4096 app.js   // 4 GB

// Heap snapshots (debug memory leaks)
const v8 = require('v8');
v8.writeHeapSnapshot('snapshot.heapsnapshot');
// Open in Chrome DevTools → Memory tab

// Common memory leak sources:
// 1. Global variables accumulating data
// 2. EventEmitter listeners not removed
// 3. setInterval that never gets cleared
// 4. Closures holding references
// 5. Large in-memory caches without eviction
```


---

# CHAPTER 2: ASYNC PATTERNS


## Promises Deep Dive

```javascript
// Three states: pending → fulfilled OR rejected

// Construction
const p = new Promise((resolve, reject) => {
    setTimeout(() => {
        if (Math.random() > 0.5) resolve('success');
        else reject(new Error('failed'));
    }, 1000);
});

// Chain
p.then(value => value.toUpperCase())
 .then(upper => console.log(upper))
 .catch(err => console.error(err))
 .finally(() => console.log('done'));

// Promise.all — wait for all, fail-fast
const [users, posts, comments] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchComments(),
]);
// If ANY rejects, immediately rejects with that error
// Others continue but their results discarded

// Promise.allSettled — wait for all, no fail-fast
const results = await Promise.allSettled([
    fetchUsers(),
    fetchPosts(),
]);
// results[0] = { status: 'fulfilled', value: [...] }
// results[1] = { status: 'rejected', reason: Error }

// Promise.race — first to settle wins
const result = await Promise.race([
    fetchData(),
    new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 5000))
]);

// Promise.any — first to FULFILL wins (rejections accumulate)
const fastest = await Promise.any([
    fetchFromMirror1(),
    fetchFromMirror2(),
    fetchFromMirror3(),
]);
// AggregateError if ALL reject

// Promisify callback-style
import { promisify } from 'util';
import fs from 'fs';

const readFile = promisify(fs.readFile);
const data = await readFile('file.txt', 'utf-8');
```


## Async/Await Patterns

```javascript
// Sequential
async function sequential() {
    const a = await fetchA();
    const b = await fetchB();   // Starts only after A done
    return [a, b];
}
// Total time: time(A) + time(B)

// Parallel
async function parallel() {
    const [a, b] = await Promise.all([fetchA(), fetchB()]);
    return [a, b];
}
// Total time: max(time(A), time(B))

// Sequential with dependency
async function dependent() {
    const user = await fetchUser();
    const posts = await fetchPostsForUser(user.id);  // Needs user.id first
    return { user, posts };
}

// Loop sequentially
for (const item of items) {
    await process(item);   // One at a time
}

// Loop in parallel
await Promise.all(items.map(item => process(item)));

// Loop with concurrency limit (very common need)
import pLimit from 'p-limit';
const limit = pLimit(5);   // Max 5 concurrent

const results = await Promise.all(
    items.map(item => limit(() => process(item)))
);
// At most 5 processings at any time

// Error handling
try {
    const data = await fetchData();
    process(data);
} catch (err) {
    if (err.code === 'ENOENT') {
        // Specific error
    } else {
        logger.error('Unexpected', err);
        throw err;
    }
}

// Don't forget to await! (silent failures)
async function bad() {
    fetchData();   // ⚠️ Returns Promise, not awaited
                   // If it throws, you get UnhandledPromiseRejection
}

// Top-level await (ES modules only)
// In package.json: "type": "module"
const data = await fetchInitialData();
```


## EventEmitter

```javascript
import { EventEmitter } from 'events';

class OrderService extends EventEmitter {
    async create(orderData) {
        const order = await this.repo.save(orderData);
        this.emit('order:created', order);     // Sync emit
        return order;
    }
}

const service = new OrderService();

// Listeners
service.on('order:created', (order) => {
    console.log('New order:', order.id);
});

// Async listener (use carefully — errors not caught by emitter)
service.on('order:created', async (order) => {
    try {
        await emailService.sendConfirmation(order);
    } catch (err) {
        logger.error('Email failed', err);
    }
});

// Listener count
service.listenerCount('order:created');     // 2

// Remove listener
service.off('order:created', handler);
service.removeAllListeners('order:created');

// One-time
service.once('order:created', (order) => {
    console.log('First order!', order.id);
});

// Max listeners (default 10, warning if exceeded)
service.setMaxListeners(20);

// Errors special — must have 'error' handler or process exits!
service.on('error', err => logger.error(err));
service.emit('error', new Error('Something failed'));

// COMMON LEAK: forgetting to remove listeners
const intervals = setInterval(() => {
    eventEmitter.on('tick', () => { /* ... */ });  // ⚠️ Accumulates!
}, 1000);
```


## AbortController — Cancelling Async Operations

```javascript
const controller = new AbortController();
const { signal } = controller;

// Pass to fetch
fetch('https://api.example.com/slow', { signal })
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(err => {
        if (err.name === 'AbortError') {
            console.log('Cancelled');
        }
    });

// Cancel after 5 seconds
setTimeout(() => controller.abort(), 5000);

// Combine multiple signals
const userCancel = new AbortController();
const timeout = AbortSignal.timeout(5000);
const combined = AbortSignal.any([userCancel.signal, timeout]);

await fetch(url, { signal: combined });

// In custom async functions
async function fetchWithRetry(url, { signal, retries = 3 }) {
    for (let i = 0; i < retries; i++) {
        if (signal?.aborted) throw new DOMException('Aborted', 'AbortError');
        try {
            return await fetch(url, { signal });
        } catch (err) {
            if (err.name === 'AbortError') throw err;
            // retry on other errors
        }
    }
}
```


---

# CHAPTER 3: STREAMS AND BUFFERS


## Stream Types

```
READABLE STREAMS:
  Source of data. Read in chunks.
  Examples: fs.createReadStream, http request, process.stdin

WRITABLE STREAMS:
  Destination. Write data in chunks.
  Examples: fs.createWriteStream, http response, process.stdout

DUPLEX STREAMS:
  Both readable AND writable (e.g. TCP sockets, net.Socket).

TRANSFORM STREAMS:
  Duplex that transforms output based on input (zlib, crypto).
  Read chunk → modify → write chunk.

OPERATING MODES:
  - Flowing: data pushed automatically (event-driven)
  - Paused: must explicitly read

OBJECT MODE vs BUFFER MODE:
  Default: Buffers/strings.
  Object mode: any JS object (useful for transforms).
```


## Reading Files (Stream vs readFile)

```javascript
import fs from 'fs';

// BAD for big files: loads entire content into memory
const data = await fs.promises.readFile('huge-10gb-file.log', 'utf-8');
// → Out of memory!

// GOOD: stream
const stream = fs.createReadStream('huge-10gb-file.log', {
    encoding: 'utf-8',
    highWaterMark: 64 * 1024   // 64 KB chunks (default for files)
});

stream.on('data', chunk => {
    // chunk is 64 KB at a time
    processChunk(chunk);
});

stream.on('end', () => {
    console.log('Done');
});

stream.on('error', err => {
    console.error('Stream error', err);
});

// MODERN async iteration (cleanest)
for await (const chunk of stream) {
    processChunk(chunk);
}

// Line-by-line with readline
import { createInterface } from 'readline';
const rl = createInterface({
    input: fs.createReadStream('logs.txt'),
    crlfDelay: Infinity
});

let lineCount = 0;
for await (const line of rl) {
    lineCount++;
    if (line.includes('ERROR')) console.log(line);
}
```


## Pipe and Piping

```javascript
import fs from 'fs';
import zlib from 'zlib';

// Read → Gzip → Write
fs.createReadStream('input.txt')
    .pipe(zlib.createGzip())
    .pipe(fs.createWriteStream('output.txt.gz'));

// Modern pipeline (better error handling)
import { pipeline } from 'stream/promises';

await pipeline(
    fs.createReadStream('input.txt'),
    zlib.createGzip(),
    fs.createWriteStream('output.txt.gz')
);
// Auto-cleanup, all errors propagate

// HTTP server: stream file to client
import http from 'http';

http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'video/mp4' });
    fs.createReadStream('video.mp4').pipe(res);
}).listen(3000);
// No memory blow-up for large files
```


## Transform Streams

```javascript
import { Transform } from 'stream';

// Custom transform: uppercase
const upper = new Transform({
    transform(chunk, encoding, callback) {
        const upperChunk = chunk.toString().toUpperCase();
        callback(null, upperChunk);
    }
});

await pipeline(
    fs.createReadStream('input.txt'),
    upper,
    fs.createWriteStream('output.txt')
);

// Object mode transform (e.g. CSV parser)
const parser = new Transform({
    readableObjectMode: true,
    writableObjectMode: false,
    transform(chunk, encoding, callback) {
        const lines = chunk.toString().split('\n');
        for (const line of lines) {
            if (line.trim()) {
                const fields = line.split(',');
                this.push({ name: fields[0], age: parseInt(fields[1]) });
            }
        }
        callback();
    }
});

// Backpressure handling (auto with pipe/pipeline)
// Manually:
function writeChunks(writableStream, chunks) {
    let i = 0;
    function next() {
        let ok = true;
        while (i < chunks.length && ok) {
            const isLast = i === chunks.length - 1;
            if (isLast) {
                writableStream.end(chunks[i]);
            } else {
                ok = writableStream.write(chunks[i]);
            }
            i++;
        }
        if (i < chunks.length) {
            // Wait for drain before continuing
            writableStream.once('drain', next);
        }
    }
    next();
}
```


## Buffers — Binary Data

```javascript
// Create buffers
const buf1 = Buffer.from('hello', 'utf-8');           // From string
const buf2 = Buffer.from([0x48, 0x65, 0x6c]);         // From bytes
const buf3 = Buffer.alloc(1024);                       // Zero-filled 1KB
const buf4 = Buffer.allocUnsafe(1024);                // Faster but contains old memory

// Inspect
buf1.length;                              // 5 bytes
buf1.toString('utf-8');                   // 'hello'
buf1.toString('hex');                     // '68656c6c6f'
buf1.toString('base64');                  // 'aGVsbG8='

// Manipulate
buf1[0] = 0x48;                          // Direct byte access
buf1.write('world', 0, 5, 'utf-8');     // Write at offset

// Concatenate
const combined = Buffer.concat([buf1, buf2], buf1.length + buf2.length);

// Compare
Buffer.compare(buf1, buf2);              // -1, 0, or 1

// Convert from various encodings
Buffer.from('SGVsbG8=', 'base64').toString('utf-8');  // 'Hello'

// IMPORTANT: Buffer is NOT garbage collected like regular objects
// Large buffers can cause OOM. Always close streams, release references.
```


---

# CHAPTER 4: HTTP AND NETWORKING


## HTTP Server (Native)

```javascript
import http from 'http';

const server = http.createServer((req, res) => {
    console.log(`${req.method} ${req.url}`);

    // Routing
    if (req.url === '/health' && req.method === 'GET') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'ok' }));
        return;
    }

    if (req.url === '/users' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            const data = JSON.parse(body);
            res.writeHead(201, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ id: 1, ...data }));
        });
        return;
    }

    res.writeHead(404);
    res.end('Not Found');
});

server.listen(3000, () => console.log('Server on :3000'));

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received, closing...');
    server.close(() => {
        console.log('Server closed');
        process.exit(0);
    });
});
```


## Express Essentials

```javascript
import express from 'express';
import morgan from 'morgan';
import helmet from 'helmet';
import compression from 'compression';
import rateLimit from 'express-rate-limit';

const app = express();

// Middleware order matters!
app.use(helmet());                                 // Security headers
app.use(compression());                            // gzip responses
app.use(morgan('combined'));                       // Request logging
app.use(express.json({ limit: '10mb' }));         // JSON parser
app.use(express.urlencoded({ extended: true }));

// Rate limiting
app.use('/api/', rateLimit({
    windowMs: 15 * 60 * 1000,  // 15 minutes
    max: 100,                   // 100 requests per window
    message: 'Too many requests'
}));

// Routes
app.get('/users/:id', async (req, res, next) => {
    try {
        const user = await getUserById(req.params.id);
        if (!user) return res.status(404).json({ error: 'Not found' });
        res.json(user);
    } catch (err) {
        next(err);   // Forward to error middleware
    }
});

// Async errors automatically forwarded in Express 5+
// In Express 4, must wrap or use express-async-errors

// 404 handler (after all routes)
app.use((req, res) => {
    res.status(404).json({ error: 'Not found' });
});

// Error handler (last, 4 params)
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(err.status || 500).json({
        error: err.message || 'Internal server error'
    });
});

app.listen(3000);
```


## Fastify (Faster Alternative)

```javascript
import Fastify from 'fastify';

const fastify = Fastify({ logger: true });

// Schema validation built-in (very fast)
const userSchema = {
    body: {
        type: 'object',
        required: ['name', 'email'],
        properties: {
            name: { type: 'string', minLength: 1 },
            email: { type: 'string', format: 'email' },
            age: { type: 'integer', minimum: 0 }
        }
    },
    response: {
        201: {
            type: 'object',
            properties: {
                id: { type: 'integer' },
                name: { type: 'string' },
                email: { type: 'string' }
            }
        }
    }
};

fastify.post('/users', { schema: userSchema }, async (request, reply) => {
    const user = await createUser(request.body);
    reply.code(201).send(user);
});

// Plugins (Fastify's middleware model)
fastify.register(import('@fastify/cors'));
fastify.register(import('@fastify/jwt'), { secret: process.env.JWT_SECRET });

await fastify.listen({ port: 3000, host: '0.0.0.0' });

// Fastify is ~2-3x faster than Express for typical workloads.
// Better TypeScript support, built-in schema validation, structured logging.
```


## HTTP Client (Fetch / axios / undici)

```javascript
// Built-in fetch (Node 18+, stable in 21+)
const res = await fetch('https://api.example.com/users/1');
if (!res.ok) throw new Error(`HTTP ${res.status}`);
const user = await res.json();

// With AbortController for timeout
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 5000);

try {
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeout);
    return await res.json();
} catch (err) {
    if (err.name === 'AbortError') throw new Error('Request timed out');
    throw err;
}

// undici (very fast, official Node HTTP client)
import { request } from 'undici';

const { statusCode, body } = await request('https://api.example.com/users/1', {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` },
    bodyTimeout: 10_000
});

const data = await body.json();

// With connection pooling (recommended for high traffic)
import { Pool } from 'undici';
const pool = new Pool('https://api.example.com', {
    connections: 100,
    pipelining: 10
});

const { body } = await pool.request({
    path: '/users/1',
    method: 'GET'
});
```


---

# CHAPTER 5: CLUSTERING AND WORKER THREADS


## Cluster (Multi-Process)

```javascript
// cluster: fork N child processes, share port
import cluster from 'cluster';
import os from 'os';
import http from 'http';

if (cluster.isPrimary) {
    const numWorkers = os.cpus().length;
    console.log(`Primary ${process.pid} starting ${numWorkers} workers`);

    for (let i = 0; i < numWorkers; i++) {
        cluster.fork();
    }

    cluster.on('exit', (worker, code) => {
        console.log(`Worker ${worker.process.pid} died (${code})`);
        cluster.fork();   // Replace dead worker
    });
} else {
    // Worker process
    http.createServer((req, res) => {
        res.end(`Hello from worker ${process.pid}\n`);
    }).listen(3000);

    console.log(`Worker ${process.pid} listening on :3000`);
}

// → All workers share port 3000. OS load-balances.
// → Saturates all CPU cores
// → If one crashes, others continue

// PM2 is much better in production:
//   pm2 start app.js -i max         # cluster mode, all CPUs
//   pm2 start app.js -i 0           # auto-detect
//   pm2 reload app                  # zero-downtime reload
//   pm2 logs / pm2 monit
```


## Worker Threads (Parallel CPU Work)

```javascript
// main.js
import { Worker } from 'worker_threads';

function runWorker(workerData) {
    return new Promise((resolve, reject) => {
        const worker = new Worker('./worker.js', { workerData });
        worker.on('message', resolve);
        worker.on('error', reject);
        worker.on('exit', (code) => {
            if (code !== 0) reject(new Error(`Worker exit ${code}`));
        });
    });
}

// Parallel CPU-bound work
const results = await Promise.all([
    runWorker({ n: 40 }),
    runWorker({ n: 41 }),
    runWorker({ n: 42 }),
]);

// worker.js
import { parentPort, workerData } from 'worker_threads';

function fibonacci(n) {
    if (n < 2) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

const result = fibonacci(workerData.n);
parentPort.postMessage(result);
```


## Worker Pool Pattern

```javascript
// worker-pool.js
import { Worker } from 'worker_threads';
import { AsyncResource } from 'async_hooks';
import { EventEmitter } from 'events';

class WorkerPoolTask extends AsyncResource {
    constructor(callback) {
        super('WorkerPoolTask');
        this.callback = callback;
    }
    done(err, result) {
        this.runInAsyncScope(this.callback, null, err, result);
        this.emitDestroy();
    }
}

const kTaskInfo = Symbol('kTaskInfo');
const kWorkerFreedEvent = Symbol('kWorkerFreedEvent');

export class WorkerPool extends EventEmitter {
    constructor(numThreads, workerPath) {
        super();
        this.numThreads = numThreads;
        this.workerPath = workerPath;
        this.workers = [];
        this.freeWorkers = [];
        this.tasks = [];

        for (let i = 0; i < numThreads; i++) {
            this.addNewWorker();
        }

        this.on(kWorkerFreedEvent, () => {
            if (this.tasks.length > 0) {
                const { task, callback } = this.tasks.shift();
                this.runTask(task, callback);
            }
        });
    }

    addNewWorker() {
        const worker = new Worker(this.workerPath);

        worker.on('message', (result) => {
            worker[kTaskInfo].done(null, result);
            worker[kTaskInfo] = null;
            this.freeWorkers.push(worker);
            this.emit(kWorkerFreedEvent);
        });

        worker.on('error', (err) => {
            if (worker[kTaskInfo]) worker[kTaskInfo].done(err, null);
            // Replace dead worker
            this.workers.splice(this.workers.indexOf(worker), 1);
            this.addNewWorker();
        });

        this.workers.push(worker);
        this.freeWorkers.push(worker);
        this.emit(kWorkerFreedEvent);
    }

    runTask(task, callback) {
        if (this.freeWorkers.length === 0) {
            this.tasks.push({ task, callback });
            return;
        }
        const worker = this.freeWorkers.pop();
        worker[kTaskInfo] = new WorkerPoolTask(callback);
        worker.postMessage(task);
    }

    close() {
        for (const w of this.workers) w.terminate();
    }
}

// Usage
const pool = new WorkerPool(4, './worker.js');
pool.runTask({ n: 40 }, (err, result) => console.log(result));
```


---

# CHAPTER 6: PERFORMANCE AND PROFILING


## Profiling Tools

```bash
# Built-in CPU profiler
node --prof app.js
# Generates isolate-0xXXX-v8.log
node --prof-process isolate-*.log > profile.txt

# Heap snapshots
# In code:
const v8 = require('v8');
v8.writeHeapSnapshot('./snapshot.heapsnapshot');
# Open in Chrome DevTools → Memory → Load

# Inspector with Chrome DevTools
node --inspect app.js
# Open chrome://inspect, click "inspect"

# clinic.js — high-level profiling
npm install -g clinic
clinic doctor -- node app.js      # Overall diagnosis
clinic flame -- node app.js       # Flame graph (find hot functions)
clinic bubbleprof -- node app.js  # Async time visualization
clinic heapprofiler -- node app.js # Memory issues

# autocannon — load testing
npm install -g autocannon
autocannon -c 100 -d 30 http://localhost:3000/api/users
# 100 connections, 30 seconds
```


## Performance Optimization Patterns

```javascript
// 1. AVOID synchronous file I/O in request handlers
// Bad
app.get('/config', (req, res) => {
    const config = fs.readFileSync('./config.json', 'utf-8');  // BLOCKS!
    res.json(JSON.parse(config));
});

// Good
let configCache = null;
app.get('/config', async (req, res) => {
    if (!configCache) {
        configCache = JSON.parse(await fs.promises.readFile('./config.json', 'utf-8'));
    }
    res.json(configCache);
});


// 2. AVOID unnecessary JSON parsing/stringify
const cached = JSON.stringify(data);   // Stringify once
app.get('/data', (req, res) => {
    res.type('json').send(cached);     // Send raw
});


// 3. STREAM large responses
app.get('/users/export', (req, res) => {
    res.type('json');
    res.write('[');

    const stream = db.queryStream('SELECT * FROM users');
    let first = true;

    stream.on('data', (row) => {
        if (!first) res.write(',');
        res.write(JSON.stringify(row));
        first = false;
    });

    stream.on('end', () => {
        res.write(']');
        res.end();
    });
});


// 4. CONNECTION POOLING for DB
import pg from 'pg';
const pool = new pg.Pool({
    host: 'localhost',
    database: 'mydb',
    max: 20,                          // Max connections
    idleTimeoutMillis: 30_000,
    connectionTimeoutMillis: 2_000,
});

// Use pool.query, not new clients per request
const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);


// 5. CACHE expensive computations
import { LRUCache } from 'lru-cache';

const cache = new LRUCache({
    max: 500,
    ttl: 1000 * 60 * 5   // 5 minutes
});

async function getUser(id) {
    if (cache.has(id)) return cache.get(id);
    const user = await db.users.findById(id);
    cache.set(id, user);
    return user;
}


// 6. USE Buffer.alloc(0) sparingly; pool buffers
// Bad: creates new buffer per request
function makeResponse() {
    return Buffer.alloc(1024 * 1024);   // 1 MB!
}

// Better: reuse from pool, or use existing buffers
```


## Tracking Memory Leaks

```javascript
// Symptom: heapUsed grows over time without releasing

// 1. Take heap snapshots at intervals
function takeSnapshot(label) {
    const fileName = `./snap-${label}-${Date.now()}.heapsnapshot`;
    v8.writeHeapSnapshot(fileName);
    return fileName;
}

const s1 = takeSnapshot('start');
// ... do operations
const s2 = takeSnapshot('after-ops');

// In Chrome DevTools → Memory → Load both → Comparison
// → Shows objects that grew between snapshots

// 2. Common leaks:

// Global state accumulation
const allUsers = [];   // Forever growing
app.post('/login', (req, res) => {
    allUsers.push(req.body);   // LEAK!
});

// Forgotten event listeners
emitter.on('event', handler);   // If never removed and emitter persists

// Closure references
function createHandler(largeData) {
    return function() {
        // largeData kept alive even if not used!
    };
}

// Module-level caches without eviction
const cache = {};
app.get('/:key', (req, res) => {
    cache[req.params.key] = compute();  // Grows forever
});

// Timers not cleared
const id = setInterval(() => { /* ... */ }, 1000);
// Never clearInterval(id) → kept alive
```


---

# CHAPTER 7: SECURITY AND BEST PRACTICES


## Common Vulnerabilities

```javascript
// 1. INJECTION (SQL, NoSQL, command)

// BAD
const query = `SELECT * FROM users WHERE name = '${name}'`;
// → SQL injection: name = "'; DROP TABLE users--"

// GOOD: parameterized
const result = await db.query(
    'SELECT * FROM users WHERE name = $1',
    [name]
);


// 2. COMMAND INJECTION
const { exec } = require('child_process');

// BAD
exec(`ping ${userInput}`);   // userInput = "google.com; rm -rf /"

// GOOD
const { execFile } = require('child_process');
execFile('ping', [userInput]);   // userInput treated as single argument


// 3. PROTOTYPE POLLUTION
function merge(target, source) {
    for (const key in source) {
        if (typeof source[key] === 'object') {
            target[key] = merge(target[key] || {}, source[key]);
        } else {
            target[key] = source[key];
        }
    }
    return target;
}

// Attacker sends: { "__proto__": { "admin": true } }
// Now ALL objects inherit admin: true!

// FIX: Object.create(null) or lodash/lodash-es with safe defaults
function safeMerge(target, source) {
    for (const key in source) {
        if (key === '__proto__' || key === 'constructor' || key === 'prototype') continue;
        // ...
    }
}


// 4. PATH TRAVERSAL
app.get('/files/:name', (req, res) => {
    // BAD: ?name=../../etc/passwd
    res.sendFile(`/uploads/${req.params.name}`);
});

// GOOD: validate
import path from 'path';
app.get('/files/:name', (req, res) => {
    const safePath = path.join('/uploads', req.params.name);
    if (!safePath.startsWith('/uploads/')) {
        return res.status(400).send('Invalid path');
    }
    res.sendFile(safePath);
});


// 5. INSECURE DESERIALIZATION
// Never use eval() or Function() with user input
eval(req.body.code);   // ALWAYS BAD
```


## Authentication Patterns

```javascript
// JWT signing/verification
import jwt from 'jsonwebtoken';

// Sign
const token = jwt.sign(
    { userId: user.id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: '15m', issuer: 'myapp' }
);

// Verify
function authMiddleware(req, res, next) {
    const authHeader = req.headers.authorization;
    if (!authHeader?.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'Missing token' });
    }
    const token = authHeader.slice(7);
    try {
        const payload = jwt.verify(token, process.env.JWT_SECRET);
        req.user = payload;
        next();
    } catch (err) {
        if (err.name === 'TokenExpiredError') {
            return res.status(401).json({ error: 'Token expired' });
        }
        return res.status(401).json({ error: 'Invalid token' });
    }
}

// Refresh token pattern
// - Short-lived access token (15min)
// - Long-lived refresh token (7-30 days, stored in DB, can be revoked)
// - When access expires: client calls /refresh with refresh token


// Password hashing (NEVER store plaintext!)
import bcrypt from 'bcrypt';

const hash = await bcrypt.hash(password, 12);   // 12 rounds (cost)
await db.users.create({ ..., password_hash: hash });

// Verify
const valid = await bcrypt.compare(submittedPassword, user.password_hash);
```


## Common Pitfalls

```javascript
// PITFALL 1: Unhandled promise rejection
async function loadData() {
    return fetch('/api/data').then(r => r.json());
}
loadData();   // Forgot to await — silent failures!
// Node 15+: process exits on unhandled rejection
process.on('unhandledRejection', err => {
    logger.error('Unhandled rejection', err);
    // Don't continue running — exit
    process.exit(1);
});


// PITFALL 2: Blocking the event loop
const data = JSON.parse(hugeString);   // Sync, blocks
// Better: stream-based JSON parser for >100KB


// PITFALL 3: Memory leaks via closures and global state
function createApp() {
    const requests = [];   // Grows forever
    return (req, res) => {
        requests.push(req);   // LEAK
        res.end();
    };
}


// PITFALL 4: SQL injection via "ORMs" that aren't
db.query(`SELECT * FROM users WHERE id = ${id}`);   // NEVER
db.query('SELECT * FROM users WHERE id = ?', [id]); // CORRECT


// PITFALL 5: Synchronous CPU work in request handler
app.post('/hash', (req, res) => {
    const hash = expensiveHashSync(req.body.data);   // Blocks!
    res.json({ hash });
});
// Use worker threads or queue


// PITFALL 6: Not validating input
app.post('/users', (req, res) => {
    const { name, email, age } = req.body;   // What if missing? Wrong type?
    db.users.create({ name, email, age });
});
// Use zod, joi, ajv, or Fastify schema


// PITFALL 7: console.log in production
// Slow, blocking I/O. Use proper logger (pino, winston).
// pino is fastest:
import pino from 'pino';
const logger = pino({ level: 'info' });
logger.info({ userId: 123 }, 'User logged in');


// PITFALL 8: Not setting timeouts on HTTP clients
// Default fetch/axios timeout = infinite → connections hang forever
await fetch(url, { signal: AbortSignal.timeout(5000) });


// PITFALL 9: Exposing stack traces in production
// next(err) shows stack to client!
app.use((err, req, res, next) => {
    logger.error(err);
    if (process.env.NODE_ENV === 'production') {
        res.status(500).json({ error: 'Internal error' });
    } else {
        res.status(500).json({ error: err.message, stack: err.stack });
    }
});


// PITFALL 10: Using == instead of ===
0 == false      // true (!)
'' == 0         // true
null == undefined  // true
// Always === unless you specifically want loose equality.


// PITFALL 11: Mutating shared state in async
let totalSum = 0;
items.map(async (item) => {
    const v = await fetchValue(item);
    totalSum += v;   // Race condition!
});
// Use Promise.all + reduce
const values = await Promise.all(items.map(i => fetchValue(i)));
const totalSum = values.reduce((a, b) => a + b, 0);


// PITFALL 12: Running root in production / Docker
// Use non-root user in Dockerfile:
// USER 1000
```