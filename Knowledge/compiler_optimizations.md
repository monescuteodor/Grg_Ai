Advanced Compiler Optimizations & LLVM IR Complete Reference
CHAPTER 1: GETTING STARTED WITH COMPILER OPTIMIZATIONS
Remarks
Compiler optimizations transform code to improve performance (speed, size, power) without changing its observable behavior. Modern compilers (GCC, Clang/LLVM) use Intermediate Representations (IR) like LLVM IR to perform machine-independent optimizations before code generation. Key concepts: Static Single Assignment (SSA), Control Flow Graphs (CFG), Data Dependence, Alias Analysis, Vectorization.
Tools: LLVM (opt, llc), GCC (gcc -O2/-O3), Godbolt Compiler Explorer, Perf (profiling), Valgrind.
Hello LLVM IR
; hello.ll - Simple LLVM IR
; Compile with: clang -S -emit-llvm hello.c -o hello.ll
; Or optimize: opt -O2 hello.ll -o hello_opt.ll

@.str = private unnamed_addr constant [14 x i8] c"Hello, World!\00", align 1

declare i32 @puts(i8* nocapture nounwind readonly)

define i32 @main() {
entry:
  %call = call i32 @puts(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str, i64 0, i64 0))
  ret i32 0
}

; View optimized IR:
; opt -O2 -S hello.ll

Optimization Levels
# -O0: No optimization (default, fast compile, easy debug)
# -O1: Basic optimizations (dead code elimination, simple inlining)
# -O2: Moderate optimizations (loop unrolling, vectorization, inlining)
# -O3: Aggressive optimizations (function inlining, loop transformations)
# -Os: Optimize for size
# -Oz: Optimize aggressively for size
# -Ofast: Breaks strict IEEE compliance for speed

CHAPTER 2: LLVM IR BASICS
SSA Form (Static Single Assignment)
# Each variable is assigned exactly once.
# Phi nodes merge values at control flow joins.

; Example: If-Else in SSA
define i32 @abs(i32 %x) {
entry:
  %cmp = icmp slt i32 %x, 0
  br i1 %cmp, label %neg, label %pos

neg:
  %neg_val = sub i32 0, %x
  br label %merge

pos:
  br label %merge

merge:
  %result = phi i32 [ %neg_val, %neg ], [ %x, %pos ]
  ret i32 %result
}

Basic Types
; i1: Boolean
; i8, i16, i32, i64: Integers
; float, double: Floating point
; pointer: i8*, i32*, etc.
; vector: <4 x i32>, <8 x float>

CHAPTER 3: LOCAL OPTIMIZATIONS
Constant Folding
# Evaluate constant expressions at compile time.

; Before:
%sum = add i32 5, 10

; After:
%sum = i32 15

Dead Code Elimination (DCE)
# Remove instructions whose results are never used.

; Before:
%tmp = mul i32 %a, %b   ; Result unused
%res = add i32 %c, %d

; After:
%res = add i32 %c, %d

Common Subexpression Elimination (CSE)
# Reuse previously computed values.

; Before:
%x = add i32 %a, %b
%y = add i32 %a, %b
%z = add i32 %x, %y

; After:
%x = add i32 %a, %b
%z = add i32 %x, %x

CHAPTER 4: GLOBAL OPTIMIZATIONS
Function Inlining
# Replace function call with function body.
# Reduces call overhead, enables further optimizations.

; Before:
define i32 @square(i32 %x) {
  %res = mul i32 %x, %x
  ret i32 %res
}

define i32 @main() {
  %val = call i32 @square(i32 5)
  ret i32 %val
}

; After (inlined):
define i32 @main() {
  %val = mul i32 5, 5
  ret i32 25
}

Interprocedural Optimization (IPO)
# Optimizations across function boundaries.
# Requires Whole Program Analysis or Link-Time Optimization (LTO).

# Enable LTO in Clang/GCC:
# clang -flto file.c -o file
# gcc -flto file.c -o file

Global Value Numbering (GVN)
# Assign unique numbers to equivalent values across basic blocks.
# More powerful than CSE.

CHAPTER 5: LOOP OPTIMIZATIONS
Loop Invariant Code Motion (LICM)
# Move calculations that don't change inside the loop to outside.

; Before:
for (i=0; i<n; i++) {
  a[i] = b[i] + c * d;  // c*d is invariant
}

; After:
temp = c * d;
for (i=0; i<n; i++) {
  a[i] = b[i] + temp;
}

Loop Unrolling
# Replicate loop body to reduce branch overhead and increase ILP.

; Before:
for (i=0; i<4; i++) {
  sum += arr[i];
}

; After (Unrolled by 4):
sum += arr[0];
sum += arr[1];
sum += arr[2];
sum += arr[3];

Loop Vectorization
# Use SIMD instructions to process multiple data elements simultaneously.
# Requires no data dependencies between iterations.

; Scalar:
for (i=0; i<N; i++) {
  C[i] = A[i] + B[i];
}

; Vectorized (AVX2, 8 floats at once):
for (i=0; i<N; i+=8) {
  va = load_8_floats(&A[i]);
  vb = load_8_floats(&B[i]);
  vc = add_8_floats(va, vb);
  store_8_floats(&C[i], vc);
}

Loop Fusion
# Combine two loops iterating over same range into one.
# Improves cache locality.

; Before:
for (i=0; i<N; i++) A[i] = B[i] + 1;
for (i=0; i<N; i++) C[i] = A[i] * 2;

; After:
for (i=0; i<N; i++) {
  A[i] = B[i] + 1;
  C[i] = A[i] * 2;
}

CHAPTER 6: MEMORY OPTIMIZATIONS
Alias Analysis
# Determine if two pointers can point to the same memory location.
# Crucial for reordering loads/stores.

# Types:
# NoAlias: Pointers never overlap.
# MayAlias: Pointers might overlap.
# MustAlias: Pointers always overlap.

# Restrict keyword (C99) helps compiler assume NoAlias.
void add(int* __restrict__ a, int* __restrict__ b, int n) {
  for (int i=0; i<n; i++) a[i] += b[i];
}

Stack Promotion
# Convert heap allocations (malloc) to stack allocations if lifetime is local.
# Faster allocation/deallocation.

Structure Splitting
# Split large structs into smaller ones if only few fields are accessed.
# Reduces cache pressure.

Cache Optimization
# Data Layout Transformation: Arrange data to fit cache lines.
# Array of Structures (AoS) vs Structure of Arrays (SoA).

; AoS (Bad for SIMD):
struct Point { float x, y, z; };
Point points[N];

; SoA (Good for SIMD):
float x[N], y[N], z[N];

CHAPTER 7: AUTO-VECTORIZATION
SIMD Intrinsics vs Auto-Vectorization
# Intrinsics: Manual SIMD coding (complex, high performance).
# Auto-Vectorization: Compiler generates SIMD automatically.

# Enable auto-vectorization reports:
# clang -Rpass=loop-vectorize file.c
# gcc -fopt-info-vec-all

# Requirements for auto-vectorization:
# 1. Loop count known or predictable.
# 2. No data dependencies between iterations.
# 3. Aligned memory access (preferred).
# 4. Simple loop body.

# Example:
void scale(float* a, float b, int n) {
  #pragma clang loop vectorize(enable)
  for (int i=0; i<n; i++) {
    a[i] *= b;
  }
}

Polyhedral Model
# Advanced mathematical model for loop optimizations.
# Handles complex nested loops and data dependencies.
# Used in LLVM's Polly optimizer.

# Enable Polly:
# clang -O3 -mllvm -polly file.c

CHAPTER 8: PROFILE-GUIDED OPTIMIZATION (PGO)
How PGO Works
# 1. Instrumented Build: Compile with profiling instrumentation.
# 2. Training Run: Execute program with representative data.
# 3. Optimized Build: Recompile using profile data.

# Clang PGO:
# Step 1: clang -fprofile-generate file.c -o file_instr
# Step 2: ./file_instr < input_data
# Step 3: clang -fprofile-use=file.profdata file.c -o file_opt

# Benefits:
# - Better inlining decisions.
# - Accurate branch prediction hints.
# - Improved register allocation.

Link-Time Optimization (LTO)
# Optimize across translation units (.c files).
# Requires whole-program visibility.

# Clang/GCC LTO:
# clang -flto file1.c file2.c -o app

# ThinLTO: Scalable LTO for large projects.
# clang -flto=thin file1.c file2.c -o app

CHAPTER 9: ADVANCED TOPICS AND RESOURCES
Compiler Flags CheatSheet
# GCC:
# -O2, -O3: Optimization levels
# -march=native: Tune for current CPU
# -funroll-loops: Force loop unrolling
# -ftree-vectorize: Enable vectorization
# -flto: Link-time optimization

# Clang/LLVM:
# -O2, -O3
# -march=native
# -Rpass=.*: Report all optimizations
# -flto
# -fvectorize

Debugging Optimizations
# Use -g to keep debug info.
# Use -Og: Optimize for debugging experience.
# Inspect LLVM IR: clang -S -emit-llvm file.c
# Inspect Assembly: objdump -d app

Recommended Reading
# - "Compilers: Principles, Techniques, and Tools" (Dragon Book)
# - "Engineering a Compiler" by Cooper & Torczon
# - LLVM Documentation: https://llvm.org/docs/
# - GCC Optimization Options: https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html

# Online Resources
# - Godbolt Compiler Explorer: https://godbolt.org/
# - LLVM Passes: https://llvm.org/docs/Passes.html
# - Intel Intrinsics Guide: https://www.intel.com/content/www/us/en/develop/documentation/intrinsics-guide.html

# End of Advanced Compiler Optimizations Reference