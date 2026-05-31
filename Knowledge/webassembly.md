# WebAssembly Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH WEBASSEMBLY


## Remarks

WebAssembly (Wasm) is a binary instruction format for a stack-based virtual machine. It is designed as a portable compilation target for programming languages, enabling deployment on the web for client and server applications. Near-native performance in browsers and beyond (WASI for system interfaces).

Tools: emscripten (C/C++ to Wasm), wasm-pack (Rust to Wasm), wat2wasm (WAT to binary), wabt tools, Node.js, browser JS engine.


## Hello World (WAT — WebAssembly Text Format)

```wat
;; hello.wat — WebAssembly Text Format
(module
  ;; Import the log function from the host environment
  (import "env" "log_i32" (func $log_i32 (param i32)))

  ;; Export the hello function
  (func $hello (export "hello")
    i32.const 42
    call $log_i32
  )
)
```

```bash
# Convert WAT to binary Wasm
wat2wasm hello.wat -o hello.wasm

# Load in Node.js
node -e "
const fs = require('fs');
const wasm = new WebAssembly.Module(fs.readFileSync('hello.wasm'));
const inst = new WebAssembly.Instance(wasm, {env: {log_i32: console.log}});
inst.exports.hello();  // logs 42
"
```


---

# CHAPTER 2: WAT BASICS


## WebAssembly Text Format

```wat
;; Basic module structure
(module
  ;; Memory declaration (page = 64KiB)
  (memory 1)           ;; 1 page = 64KiB
  (export "memory" (memory 0))

  ;; Global variables
  (global $g_i32 (mut i32) (i32.const 0))
  (global $PI f64 (f64.const 3.14159265358979))

  ;; Data segment (initialize memory)
  (data (i32.const 0) "Hello, World!\n")

  ;; Function: add two integers
  (func $add (export "add") (param $a i32) (param $b i32) (result i32)
    local.get $a
    local.get $b
    i32.add
  )

  ;; Function with local variables
  (func $compute (export "compute") (param $n i32) (result i32)
    (local $result i32)
    (local $i i32)

    i32.const 0
    local.set $result

    i32.const 0
    local.set $i

    (block $break
      (loop $continue
        local.get $i
        local.get $n
        i32.ge_s
        br_if $break

        local.get $result
        local.get $i
        i32.add
        local.set $result

        local.get $i
        i32.const 1
        i32.add
        local.set $i

        br $continue
      )
    )

    local.get $result
  )

  ;; Factorial (recursive)
  (func $factorial (export "factorial") (param $n i32) (result i32)
    local.get $n
    i32.const 1
    i32.le_s
    if (result i32)
      i32.const 1
    else
      local.get $n
      local.get $n
      i32.const 1
      i32.sub
      call $factorial
      i32.mul
    end
  )
)
```


---

# CHAPTER 3: TYPES AND INSTRUCTIONS


## Core Instructions

```wat
;; Value types
;; i32 — 32-bit integer
;; i64 — 64-bit integer
;; f32 — 32-bit float
;; f64 — 64-bit float
;; v128 — 128-bit SIMD vector (Wasm SIMD)

;; Integer constants
i32.const 42
i64.const 9000000000

;; Float constants
f32.const 3.14
f64.const 3.14159265358979

;; Integer arithmetic
i32.add
i32.sub
i32.mul
i32.div_s    ;; signed division
i32.div_u    ;; unsigned division
i32.rem_s    ;; signed remainder
i32.rem_u
i32.and
i32.or
i32.xor
i32.shl      ;; shift left
i32.shr_s    ;; shift right signed
i32.shr_u    ;; shift right unsigned
i32.rotl     ;; rotate left
i32.rotr     ;; rotate right
i32.clz      ;; count leading zeros
i32.ctz      ;; count trailing zeros
i32.popcnt   ;; population count (set bits)

;; Integer comparison
i32.eq
i32.ne
i32.lt_s; i32.lt_u
i32.gt_s; i32.gt_u
i32.le_s; i32.le_u
i32.ge_s; i32.ge_u
i32.eqz      ;; equal to zero

;; Float arithmetic
f64.add
f64.sub
f64.mul
f64.div
f64.sqrt
f64.min; f64.max
f64.abs; f64.neg
f64.ceil; f64.floor; f64.trunc; f64.nearest
f64.copysign

;; Float comparison
f64.eq; f64.ne
f64.lt; f64.gt; f64.le; f64.ge

;; Conversions
i32.wrap_i64          ;; i64 -> i32 (truncate)
i64.extend_i32_s      ;; i32 -> i64 (sign extend)
i64.extend_i32_u      ;; i32 -> i64 (zero extend)
f32.convert_i32_s     ;; i32 -> f32
f64.convert_i32_s     ;; i32 -> f64
i32.trunc_f64_s       ;; f64 -> i32 (truncate toward zero)
f32.demote_f64        ;; f64 -> f32
f64.promote_f32       ;; f32 -> f64
i32.reinterpret_f32   ;; reinterpret bits
```


---

# CHAPTER 4: MEMORY AND TABLES


## Memory Operations

```wat
(module
  (memory 1)

  ;; Load from memory
  (func $memory_ops (result i32)
    ;; Store i32 at address 0
    i32.const 0      ;; address
    i32.const 42     ;; value
    i32.store

    ;; Load i32 from address 0
    i32.const 0
    i32.load          ;; => 42

    ;; Store/load bytes
    i32.const 100    ;; address
    i32.const 255    ;; value
    i32.store8

    i32.const 100
    i32.load8_u      ;; zero-extended

    ;; Alignment hint (2^n bytes, optional)
    i32.const 0
    i32.load align=4
  )

  ;; Grow memory
  (func $grow_mem (param $pages i32) (result i32)
    local.get $pages
    memory.grow          ;; returns old size or -1 on failure
  )

  ;; Current memory size
  (func $mem_size (result i32)
    memory.size          ;; in pages
  )

  ;; Table (function references)
  (table 10 funcref)     ;; 10 function slots

  ;; Indirect call (call through table)
  (type $fn_type (func (param i32) (result i32)))

  (func $call_indirect_example (param $idx i32) (param $arg i32) (result i32)
    local.get $arg
    local.get $idx
    call_indirect (type $fn_type)
  )

  ;; Element segment (initialize table)
  (elem (i32.const 0) $factorial $add)
)
```


---

# CHAPTER 5: CONTROL FLOW


## Control Instructions

```wat
;; Block / Loop / If
(func $control_flow (param $n i32) (result i32)
  (local $result i32)

  ;; if/else
  (if (result i32)
    (i32.gt_s (local.get $n) (i32.const 0))
    (then
      local.get $n
      i32.const 2
      i32.mul
    )
    (else
      i32.const -1
    )
  )
  drop

  ;; block with break
  (block $outer (result i32)
    (block $inner
      local.get $n
      i32.eqz
      br_if $inner     ;; break inner if n == 0

      i32.const 1
      br $outer        ;; break outer with value 1
    )
    i32.const 0        ;; fallthrough value
  )
  drop

  ;; loop with continue
  i32.const 0
  local.set $result

  (loop $loop
    local.get $n
    i32.eqz
    br_if $loop       ;; stop if n == 0 (note: br exits loop here, not continues)
    ;; To continue: br_if $loop from inside
    local.get $result
    local.get $n
    i32.add
    local.set $result
    local.get $n
    i32.const 1
    i32.sub
    local.set $n
    br $loop          ;; continue loop
  )

  local.get $result   ;; return result

  ;; br_table (switch)
  (block $case0
    (block $default
      local.get $n
      i32.const 0
      i32.eq
      br_if $case0
      br $default
    )
    ;; default case
    i32.const 99
    return
  )
  ;; case 0
  i32.const 0
)

;; select (conditional expression)
(func $max (param $a i32) (param $b i32) (result i32)
  local.get $a
  local.get $b
  local.get $a
  local.get $b
  i32.gt_s
  select              ;; picks a if condition is true, else b
)
```


---

# CHAPTER 6: JAVASCRIPT INTEROP


## Using WebAssembly from JavaScript

```javascript
// Load and instantiate Wasm module
async function loadWasm(url) {
    const response = await fetch(url);
    const buffer   = await response.arrayBuffer();
    const module   = await WebAssembly.compile(buffer);

    const imports = {
        env: {
            // Provide JS functions to Wasm
            log_i32: (n) => console.log('i32:', n),
            log_f64: (n) => console.log('f64:', n),
            // Memory shared with JS
            memory: new WebAssembly.Memory({ initial: 1, maximum: 10 })
        }
    };

    const instance = await WebAssembly.instantiate(module, imports);
    return instance.exports;
}

// Use the module
const wasm = await loadWasm('module.wasm');

// Call exported functions
const result = wasm.add(3, 4);        // 7
const fact   = wasm.factorial(10);    // 3628800

// Access exported memory
const memory = new Uint8Array(wasm.memory.buffer);
memory[0] = 65;  // 'A'

// Read a string from Wasm memory
function readString(memory, ptr, len) {
    const bytes = new Uint8Array(memory.buffer, ptr, len);
    return new TextDecoder().decode(bytes);
}

// Write a string into Wasm memory
function writeString(memory, ptr, str) {
    const bytes = new TextEncoder().encode(str);
    new Uint8Array(memory.buffer, ptr).set(bytes);
}

// Streaming instantiation (more efficient)
const { instance } = await WebAssembly.instantiateStreaming(
    fetch('module.wasm'),
    imports
);

// Table access
const table = new WebAssembly.Table({ initial: 10, element: 'anyfunc' });
const fn = table.get(0);
fn(42);

// Global
const global = new WebAssembly.Global({ value: 'i32', mutable: true }, 42);
global.value = 100;
```


---

# CHAPTER 7: C TO WEBASSEMBLY


## Compiling C/C++ with Emscripten

```c
// math.c
#include <emscripten/emscripten.h>
#include <math.h>

// EMSCRIPTEN_KEEPALIVE prevents dead-code elimination
EMSCRIPTEN_KEEPALIVE
int add(int a, int b) {
    return a + b;
}

EMSCRIPTEN_KEEPALIVE
double sqrt_wrapper(double x) {
    return sqrt(x);
}

EMSCRIPTEN_KEEPALIVE
void fill_array(int* arr, int len, int value) {
    for (int i = 0; i < len; i++) {
        arr[i] = value;
    }
}
```

```bash
# Compile C to Wasm
emcc math.c -o math.js \
    -s EXPORTED_FUNCTIONS='["_add","_sqrt_wrapper","_fill_array"]' \
    -s EXPORTED_RUNTIME_METHODS='["ccall","cwrap","HEAP32"]' \
    -s WASM=1 \
    -O2

# Standalone Wasm (no JS glue)
emcc math.c -o math.wasm --no-entry \
    -s EXPORTED_FUNCTIONS='["_add"]' \
    -s STANDALONE_WASM

# With WASI
emcc math.c -o math.wasm \
    -s STANDALONE_WASM \
    --target=wasm32-wasi
```

```javascript
// Use generated JS glue
const Module = require('./math.js');
Module.onRuntimeInitialized = () => {
    // ccall: call by name
    const result = Module.ccall('add', 'number', ['number','number'], [3, 4]);
    console.log(result); // 7

    // cwrap: create wrapper function
    const add = Module.cwrap('add', 'number', ['number','number']);
    console.log(add(10, 20)); // 30

    // Direct heap access
    const ptr = Module._malloc(4 * 5);  // allocate 5 ints
    const arr = new Int32Array(Module.HEAP32.buffer, ptr, 5);
    Module.ccall('fill_array', null, ['number','number','number'], [ptr, 5, 99]);
    console.log(Array.from(arr)); // [99,99,99,99,99]
    Module._free(ptr);
};
```


---

# CHAPTER 8: WASI AND RUST TO WASM


## Rust to WebAssembly

```rust
// lib.rs (Rust library for Wasm)
use wasm_bindgen::prelude::*;

// Export to JavaScript
#[wasm_bindgen]
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[wasm_bindgen]
pub fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

#[wasm_bindgen]
pub struct Counter {
    count: u32,
}

#[wasm_bindgen]
impl Counter {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Counter {
        Counter { count: 0 }
    }

    pub fn increment(&mut self) {
        self.count += 1;
    }

    pub fn get(&self) -> u32 {
        self.count
    }
}

// Call JS from Rust
#[wasm_bindgen]
extern "C" {
    fn alert(s: &str);
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}
```

```bash
# Build with wasm-pack
wasm-pack build --target web    # for browsers
wasm-pack build --target nodejs # for Node.js
wasm-pack build --target bundler # for webpack/rollup
```

```javascript
// Use Rust Wasm module
import init, { add, greet, Counter } from './pkg/my_lib.js';

async function main() {
    await init();  // initialize the Wasm module

    console.log(add(3, 4));         // 7
    console.log(greet("World"));    // "Hello, World!"

    const counter = new Counter();
    counter.increment();
    counter.increment();
    console.log(counter.get());     // 2
}
main();
```

```wat
;; WASI (WebAssembly System Interface) example
;; Allows Wasm to access system resources

(module
  ;; WASI imports
  (import "wasi_snapshot_preview1" "fd_write"
    (func $fd_write (param i32 i32 i32 i32) (result i32)))

  (memory 1)
  (export "memory" (memory 0))

  ;; Store string and iovec in memory
  (data (i32.const 8) "Hello, WASI!\n")

  (func $main (export "_start")
    ;; Set up iovec: ptr=8, len=13
    (i32.store (i32.const 0) (i32.const 8))   ;; buf ptr
    (i32.store (i32.const 4) (i32.const 13))  ;; buf len

    ;; fd_write(stdout=1, iovec=0, count=1, nwritten_ptr=20)
    (call $fd_write
      (i32.const 1)   ;; stdout
      (i32.const 0)   ;; iovec ptr
      (i32.const 1)   ;; num iovecs
      (i32.const 20)  ;; nwritten output ptr
    )
    drop
  )
)
```
