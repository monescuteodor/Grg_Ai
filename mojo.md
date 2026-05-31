# Mojo Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH MOJO


## Remarks

Mojo is a programming language designed for AI/ML systems programming, combining Python's usability with systems-level performance. Created by Modular AI (Chris Lattner), Mojo is a superset of Python targeting MLIR/LLVM. It aims for performance comparable to C/C++/CUDA while being Python-compatible.

Tools: `magic` (package manager), `mojo` CLI, Modular platform, MAX Engine.


## Hello World

```python
# hello.mojo
def main():
    print("Hello, World!")
    print("Hello, Mojo!")
```

```bash
mojo hello.mojo          # run directly
mojo build hello.mojo    # compile to binary
./hello                  # run compiled binary
mojo repl                # interactive REPL
```

### Python vs Mojo

```python
# Python (dynamic, slow)
def python_sum(n: int) -> int:
    total = 0
    for i in range(n):
        total += i
    return total

# Mojo (static types, SIMD, fast)
fn mojo_sum(n: Int) -> Int:
    var total: Int = 0
    for i in range(n):
        total += i
    return total

# fn = Mojo function (strict, compiled)
# def = Python-compatible function (dynamic)
```


---

# CHAPTER 2: TYPES AND VARIABLES


## Mojo Type System

```python
# === BASIC TYPES ===
def types_demo():
    # Python-style (dynamic)
    x = 42
    s = "hello"
    f = 3.14

    # Mojo-style (static)
    var i: Int = 100          # signed integer (pointer-sized)
    var u: UInt = 200         # unsigned integer
    var f32: Float32 = 1.5    # 32-bit float
    var f64: Float64 = 3.14   # 64-bit float
    var b: Bool = True        # boolean
    var c: Int8 = -128        # 8-bit signed

    # SIMD types (vectorized)
    var v4: SIMD[DType.float32, 4] = SIMD[DType.float32, 4](1.0, 2.0, 3.0, 4.0)
    var vi8: SIMD[DType.int8, 16] = 0  # 16 int8s initialized to 0

    # String
    var name: String = "Mojo"
    var greeting = String("Hello, ") + name + "!"
    print(greeting)

    # StringLiteral (compile-time constant)
    alias LANG: StringLiteral = "Mojo"

    # Type aliases
    alias Float = Float64
    alias Index = Int

    print(i, u, f32, f64, b)

fn fn_types():
    # fn requires explicit types
    let x: Int = 5        # immutable
    var y: Int = 10       # mutable
    y += x
    # x = 20  # ERROR: let is immutable

    # Automatic type inference
    let auto = 3.14  # Float64
    let count = 100  # Int

    print(y, auto, count)
```


---

# CHAPTER 3: STRUCTS AND TRAITS


## Mojo Structs

```python
# === STRUCT (value type, stack allocated) ===
struct Point:
    var x: Float64
    var y: Float64

    fn __init__(inout self, x: Float64, y: Float64):
        self.x = x
        self.y = y

    fn distance(self, other: Point) -> Float64:
        let dx = self.x - other.x
        let dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5

    fn __str__(self) -> String:
        return "Point(" + String(self.x) + ", " + String(self.y) + ")"

    fn __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


# === USING STRUCTS ===
fn use_point():
    let p1 = Point(0.0, 0.0)
    let p2 = Point(3.0, 4.0)
    print(p1.distance(p2))   # 5.0
    let p3 = p1 + p2
    print(p3)


# === TRAIT (interface) ===
trait Animal:
    fn speak(self) -> String: ...
    fn name(self) -> String: ...

struct Dog(Animal):
    var dog_name: String

    fn __init__(inout self, name: String):
        self.dog_name = name

    fn speak(self) -> String:
        return "Woof!"

    fn name(self) -> String:
        return self.dog_name

struct Cat(Animal):
    var cat_name: String

    fn __init__(inout self, name: String):
        self.cat_name = name

    fn speak(self) -> String:
        return "Meow!"

    fn name(self) -> String:
        return self.cat_name

fn make_noise[T: Animal](animal: T):
    print(animal.name(), "says:", animal.speak())

fn test_traits():
    let dog = Dog("Rex")
    let cat = Cat("Whiskers")
    make_noise(dog)
    make_noise(cat)
```


---

# CHAPTER 4: FUNCTIONS AND OWNERSHIP


## Mojo Functions

```python
# === ARGUMENT CONVENTIONS ===

# borrowed (default, read-only reference)
fn read_only(x: Int):
    print(x)
    # x = 10  # ERROR

# inout (mutable reference)
fn increment(inout x: Int):
    x += 1

# owned (takes ownership, can move)
fn consume(owned s: String):
    print(s)
    # s is dropped here

# === FUNCTION OVERLOADING ===
fn add(a: Int, b: Int) -> Int:
    return a + b

fn add(a: Float64, b: Float64) -> Float64:
    return a + b

fn add(a: Int, b: Int, c: Int) -> Int:
    return a + b + c

# === DEFAULT ARGUMENTS ===
fn greet(name: String, greeting: String = "Hello") -> String:
    return greeting + ", " + name + "!"

# === KEYWORD ARGUMENTS ===
fn power(base: Float64, exp: Float64 = 2.0) -> Float64:
    return base ** exp

# === GENERIC FUNCTIONS ===
fn generic_max[T: Comparable](a: T, b: T) -> T:
    return a if a > b else b

# === CLOSURES (def style) ===
def make_adder(n: Int):
    def adder(x: Int) -> Int:
        return x + n
    return adder

# === RAISES (error handling) ===
fn might_fail(x: Int) raises -> Int:
    if x < 0:
        raise Error("negative input")
    return x * 2

fn call_raising():
    try:
        let result = might_fail(-1)
        print(result)
    except e:
        print("Error:", e)

def main():
    var x = 10
    increment(x)
    print(x)  # 11

    let s = add(3, 4)
    let f = add(1.5, 2.5)
    print(s, f)

    print(greet("World"))
    print(greet("Mojo", greeting="Hi"))
    print(power(2.0, exp=10.0))
    print(generic_max(3, 7))
    call_raising()
```


---

# CHAPTER 5: MEMORY AND POINTERS


## Low-Level Memory in Mojo

```python
from memory import UnsafePointer, memset_zero, memcpy

# === UNSAFE POINTER ===
fn pointer_demo():
    # Allocate memory
    let ptr = UnsafePointer[Int].alloc(10)
    
    # Initialize
    for i in range(10):
        ptr[i] = i * i
    
    # Access
    print(ptr[3])   # 9
    
    # Free
    ptr.free()

# === REFERENCE TYPES ===
struct Buffer:
    var data: UnsafePointer[Float32]
    var size: Int

    fn __init__(inout self, size: Int):
        self.size = size
        self.data = UnsafePointer[Float32].alloc(size)
        memset_zero(self.data, size)

    fn __del__(owned self):
        self.data.free()

    fn __getitem__(self, idx: Int) -> Float32:
        return self.data[idx]

    fn __setitem__(inout self, idx: Int, val: Float32):
        self.data[idx] = val

fn use_buffer():
    var buf = Buffer(100)
    buf[0] = 1.5
    buf[1] = 2.5
    print(buf[0] + buf[1])  # 4.0

# === SIMD OPERATIONS (key for ML) ===
from sys.info import simdwidthof

fn simd_add():
    alias width = simdwidthof[DType.float32]()
    var a = SIMD[DType.float32, 4](1.0, 2.0, 3.0, 4.0)
    var b = SIMD[DType.float32, 4](5.0, 6.0, 7.0, 8.0)
    var c = a + b
    print(c)  # [6.0, 8.0, 10.0, 12.0]

    # Reduction
    var sum = c.reduce_add()
    print(sum)  # 34.0

    # FMA (fused multiply-add)
    var result = a.fma(b, c)  # a*b + c
    print(result)
```


---

# CHAPTER 6: PYTHON INTEROP AND MODULES


## Python Integration

```python
# === IMPORTING PYTHON PACKAGES ===
from python import Python

def use_numpy():
    let np = Python.import_module("numpy")
    let arr = np.array([1, 2, 3, 4, 5])
    print(arr.mean())   # 3.0
    print(arr.std())    # std dev

    let zeros = np.zeros((3, 3))
    print(zeros)

def use_matplotlib():
    let plt = Python.import_module("matplotlib.pyplot")
    let np = Python.import_module("numpy")
    
    let x = np.linspace(0, 2 * np.pi, 100)
    let y = np.sin(x)
    plt.plot(x, y)
    plt.savefig("sine.png")

def use_torch():
    let torch = Python.import_module("torch")
    let tensor = torch.randn(3, 4)
    print(tensor)
    print(tensor.shape)

# === MOJO MODULE (package) ===
# mymodule/__init__.mojo
# mymodule/math_ops.mojo

# math_ops.mojo:
fn fast_dot(a: SIMD[DType.float32, 4],
            b: SIMD[DType.float32, 4]) -> Float32:
    return (a * b).reduce_add()

# Import in main:
# from mymodule.math_ops import fast_dot

# === CALLING MOJO FROM PYTHON (via MAX Engine) ===
# In Python:
# from max import engine
# session = engine.InferenceSession()
# model = session.load("model.mojopkg")

def main():
    use_numpy()
```


---

# CHAPTER 7: PARALLELISM AND PERFORMANCE


## High Performance Computing

```python
from algorithm import parallelize, vectorize
from sys.info import simdwidthof, num_physical_cores

# === VECTORIZE ===
fn vectorized_add(a: DTypePointer[DType.float32],
                  b: DTypePointer[DType.float32],
                  c: DTypePointer[DType.float32],
                  n: Int):
    alias width = simdwidthof[DType.float32]()

    @parameter
    fn add_chunk[width: Int](idx: Int):
        let va = a.load[width=width](idx)
        let vb = b.load[width=width](idx)
        c.store[width=width](idx, va + vb)

    vectorize[add_chunk, width](n)

# === PARALLELIZE ===
fn parallel_sum(data: DTypePointer[DType.float64], n: Int) -> Float64:
    var results = DTypePointer[DType.float64].alloc(num_physical_cores())
    
    @parameter
    fn compute_chunk(core_id: Int):
        let chunk = n // num_physical_cores()
        let start = core_id * chunk
        let end = start + chunk
        var local_sum: Float64 = 0.0
        for i in range(start, end):
            local_sum += data[i]
        results[core_id] = local_sum
    
    parallelize[compute_chunk](num_physical_cores())
    
    var total: Float64 = 0.0
    for i in range(num_physical_cores()):
        total += results[i]
    results.free()
    return total

# === MATRIX MULTIPLY (optimized) ===
fn matmul(C: DTypePointer[DType.float32],
          A: DTypePointer[DType.float32],
          B: DTypePointer[DType.float32],
          M: Int, N: Int, K: Int):
    alias width = simdwidthof[DType.float32]()
    
    @parameter
    fn compute_row(m: Int):
        for n in range(0, N, width):
            var acc = SIMD[DType.float32, width](0)
            for k in range(K):
                let a_val = A.load(m * K + k)
                let b_vec = B.load[width=width](k * N + n)
                acc = acc + a_val * b_vec
            C.store[width=width](m * N + n, acc)
    
    parallelize[compute_row](M)

# === BENCHMARKING ===
from time import perf_counter_ns

fn benchmark():
    let start = perf_counter_ns()
    # ... computation ...
    let end = perf_counter_ns()
    print("Time:", (end - start) // 1_000_000, "ms")
```


---

# CHAPTER 8: AI/ML PATTERNS AND MAX ENGINE


## Machine Learning with Mojo

```python
# === TENSOR OPERATIONS ===
from tensor import Tensor, TensorShape

fn tensor_basics():
    # Create tensors
    var t1 = Tensor[DType.float32](TensorShape(3, 4))
    var t2 = Tensor[DType.float32](3, 4)  # same shape

    # Access elements
    t1[0, 0] = 1.0
    print(t1[0, 0])

    # Shape info
    print(t1.shape())
    print(t1.num_elements())

# === NEURAL NETWORK LAYER ===
struct LinearLayer:
    var weights: Tensor[DType.float32]
    var bias: Tensor[DType.float32]
    var in_features: Int
    var out_features: Int

    fn __init__(inout self, in_feat: Int, out_feat: Int):
        self.in_features = in_feat
        self.out_features = out_feat
        self.weights = Tensor[DType.float32](in_feat, out_feat)
        self.bias = Tensor[DType.float32](out_feat)

    fn forward(self, x: Tensor[DType.float32]) -> Tensor[DType.float32]:
        # Matrix multiply x @ weights + bias
        var out = Tensor[DType.float32](x.dim(0), self.out_features)
        # ... SIMD-accelerated implementation ...
        return out

# === MAX ENGINE INFERENCE ===
# from max import engine
#
# fn run_inference():
#     let session = engine.InferenceSession()
#     let model = session.load("llama.mojopkg")
#
#     let input_ids = Tensor[DType.int64](1, 512)
#     # ... fill input_ids ...
#
#     let outputs = model.execute("input_ids", input_ids)
#     let logits = outputs.get[DType.float32]("logits")
#     print(logits.shape())

# === DECORATOR PATTERNS ===
@value          # auto-generates copy/move constructors
struct MyValue:
    var data: Int

@register_passable("trivial")   # pass by register
struct SmallStruct:
    var x: Int32
    var y: Int32

# === COMPILE-TIME COMPUTATION ===
alias TILE_SIZE = 16
alias NUM_HEADS = 8
alias HEAD_DIM = 64
alias EMBED_DIM = NUM_HEADS * HEAD_DIM

fn compile_time():
    # Computed at compile time
    alias total = TILE_SIZE * TILE_SIZE
    print("tile elements:", total)  # 256

def main():
    tensor_basics()
    compile_time()
    print("Mojo version: superset of Python with systems performance")
    print("Target: AI/ML applications with C-level speed")
```
