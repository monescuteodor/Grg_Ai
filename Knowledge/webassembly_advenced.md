# WebAssembly (WASM) Complete Reference


---

# CHAPTER 1: WHAT IS WEBASSEMBLY


## Remarks

WebAssembly is a binary instruction format that runs in the browser at near-native speed. It doesn't replace JavaScript — it complements it for CPU-intensive tasks. You write in C/C++/Rust/Go, compile to WASM, and run in browser alongside JavaScript. Used by Figma, Google Earth, AutoCAD Web, Photoshop Web, Unity Web Games.

Key concepts: **Binary format** (compact, fast to parse), **Sandboxed** (same security as JS), **Language-agnostic** (compile from any language), **Near-native speed** (10-20x faster than JS for compute), **Interop** (call JS from WASM and vice versa).


## How It Works

```
SOURCE CODE (C/Rust/Go/etc.)
       │
       ▼  compile
WASM BINARY (.wasm file)
       │
       ▼  browser loads
WASM RUNTIME (in browser)
       │
       ▼  executes
NEAR-NATIVE SPEED

JavaScript                    WebAssembly
─────────────────────────────────────────────
Text-based (.js)              Binary (.wasm)
Interpreted + JIT             Pre-compiled AOT
Dynamic typing                Static typing
GC managed                    Manual memory (linear)
Good for: UI, DOM, events     Good for: compute, games, codecs
Speed: 1x baseline            Speed: 10-20x for math/loops
```


## Rust to WASM (Most Popular Path)

```rust
// lib.rs — Rust code compiled to WASM
use wasm_bindgen::prelude::*;

// Export function to JavaScript
#[wasm_bindgen]
pub fn fibonacci(n: u32) -> u64 {
    if n <= 1 { return n as u64; }
    let mut a: u64 = 0;
    let mut b: u64 = 1;
    for _ in 2..=n {
        let temp = a + b;
        a = b;
        b = temp;
    }
    b
}

#[wasm_bindgen]
pub fn process_image(pixels: &mut [u8], width: u32, height: u32) {
    // Grayscale filter — processes millions of pixels FAST
    for i in (0..pixels.len()).step_by(4) {
        let gray = (pixels[i] as u16 + pixels[i+1] as u16 + pixels[i+2] as u16) / 3;
        pixels[i] = gray as u8;     // R
        pixels[i+1] = gray as u8;   // G
        pixels[i+2] = gray as u8;   // B
        // pixels[i+3] = alpha (unchanged)
    }
}
```

```bash
# Build with wasm-pack
cargo install wasm-pack
wasm-pack build --target web
# Generates: pkg/my_wasm_bg.wasm + pkg/my_wasm.js (JS bindings)
```

```javascript
// Use in JavaScript
import init, { fibonacci, process_image } from './pkg/my_wasm.js';

await init();  // Load WASM binary

// Call Rust function from JS!
console.log(fibonacci(50));  // 12586269025 — instant!

// Process image data
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
process_image(imageData.data, canvas.width, canvas.height);
ctx.putImageData(imageData, 0, 0);  // Grayscale applied!
```


## C/C++ to WASM (Emscripten)

```c
// math.c
#include <emscripten.h>

EMSCRIPTEN_KEEPALIVE
int add(int a, int b) {
    return a + b;
}

EMSCRIPTEN_KEEPALIVE
double mandelbrot(double cx, double cy, int max_iter) {
    double zx = 0, zy = 0;
    int i;
    for (i = 0; i < max_iter; i++) {
        double temp = zx*zx - zy*zy + cx;
        zy = 2*zx*zy + cy;
        zx = temp;
        if (zx*zx + zy*zy > 4.0) break;
    }
    return (double)i / max_iter;
}
```

```bash
# Compile with Emscripten
emcc math.c -o math.js -s EXPORTED_FUNCTIONS='["_add","_mandelbrot"]' -s MODULARIZE=1
```

```javascript
const Module = await createModule();
console.log(Module._add(2, 3));  // 5
console.log(Module._mandelbrot(0.3, 0.5, 1000));
```


## When to Use WASM

```
USE WASM:
  ✅ Image/video processing (filters, encoding, compression)
  ✅ Games (Unity, Unreal Engine export to web)
  ✅ Scientific computation (simulations, physics)
  ✅ Cryptography (hashing, encryption)
  ✅ Audio processing (synthesizers, effects)
  ✅ CAD / 3D modeling in browser
  ✅ Porting existing C/C++/Rust libraries to web

DON'T USE WASM:
  ❌ DOM manipulation (JS is faster for DOM)
  ❌ Simple web apps (WASM adds complexity)
  ❌ String-heavy operations (JS strings are optimized)
  ❌ Small functions (call overhead outweighs speed gain)
```


---

# CHAPTER 2: COMMON PITFALLS

```
PITFALL 1: Using WASM for everything
  DOM access from WASM goes through JS bridge → SLOWER than direct JS.
  Fix: use WASM for compute, JS for DOM/UI.

PITFALL 2: Large WASM binary size
  Full C++ stdlib compiled → 2MB+ WASM file.
  Fix: optimize with -Oz flag, use wasm-opt, tree-shake unused code.

PITFALL 3: No garbage collection in WASM
  Memory leaks if you malloc without free (C/C++).
  Fix: use Rust (ownership system), or careful manual memory management.

PITFALL 4: Expecting automatic parallelism
  WASM runs single-threaded by default.
  Fix: use SharedArrayBuffer + Web Workers for parallel WASM.

PITFALL 5: Not measuring before optimizing
  Assuming JS is too slow without benchmarking.
  Fix: profile JS first. V8 JIT is surprisingly fast for many workloads.
```