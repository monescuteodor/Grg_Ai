Advanced Compiler Optimizations & LLVM IR Complete Reference
CHAPTER 1: FUNDAMENTALS OF COMPILER OPTIMIZATION
Remarks
Compiler optimizations aim to improve the performance (speed, size, power) of executable code without changing its observable behavior. Modern compilers use Intermediate Representations (IR) like LLVM IR to perform machine-independent optimizations before code generation. Key concepts: Static Single Assignment (SSA), Control Flow Graphs (CFG), Data Dependence Analysis, Alias Analysis, and Vectorization. Tools: LLVM (opt, llc), GCC, Clang, Godbolt Compiler Explorer.

1.1 Optimization Levels
# -O0: No optimization (default, fast compile, easy debug).
# -O1: Basic optimizations (dead code elimination, simple inlining).
# -O2: Moderate optimizations (loop unrolling, vectorization, inlining).
# -O3: Aggressive optimizations (function inlining, loop transformations).
# -Os: Optimize for size.
# -Oz: Optimize aggressively for size.
# -Ofast: Breaks strict IEEE compliance for speed (enables -ffast-math).

1.2 Static Single Assignment (SSA) Form
# Each variable is assigned exactly once.
# Phi nodes merge values at control flow joins.
# Example:
# if (cond) { x = 1; } else { x = 2; }
# y = x + 3;
# In SSA:
# entry:
#   br i1 %cond, label %then, label %else
# then:
#   %x1 = add i32 0, 1
#   br label %merge
# else:
#   %x2 = add i32 0, 2
#   br label %merge
# merge:
#   %x3 = phi i32 [ %x1, %then ], [ %x2, %else ]
#   %y = add i32 %x3, 3

CHAPTER 2: LLVM IR BASICS
LLVM IR is a low-level programming language similar to assembly but with strong typing and infinite registers.

2.1 Basic Types and Instructions
# i1, i8, i16, i32, i64: Integers
# float, double: Floating point
# pointer: i8*, i32*
# vector: <4 x i32>, <8 x float>

# Common Instructions:
# %result = add i32 %a, %b
# %result = sub i32 %a, %b
# %result = mul i32 %a, %b
# %result = sdiv i32 %a, %b (signed division)
# %result = icmp eq i32 %a, %b (integer comparison)
# br i1 %cond, label %true, label %false (branch)
# call i32 @printf(i8* %fmt, ...)

2.2 Memory Access
# %ptr = alloca i32 (stack allocation)
# store i32 %val, i32* %ptr
# %val = load i32, i32* %ptr

# Global variables:
# @global_var = global i32 0

CHAPTER 3: LOCAL OPTIMIZATIONS
Performed within a single basic block.

3.1 Constant Folding
# Evaluate constant expressions at compile time.
# Before: %sum = add i32 5, 10
# After: %sum = i32 15

3.2 Dead Code Elimination (DCE)
# Remove instructions whose results are never used.
# Before:
#   %tmp = mul i32 %a, %b  ; Result unused
#   %res = add i32 %c, %d
# After:
#   %res = add i32 %c, %d

3.3 Common Subexpression Elimination (CSE)
# Reuse previously computed values.
# Before:
#   %x = add i32 %a, %b
#   %y = add i32 %a, %b
#   %z = add i32 %x, %y
# After:
#   %x = add i32 %a, %b
#   %z = add i32 %x, %x

CHAPTER 4: GLOBAL OPTIMIZATIONS
Performed across basic blocks or functions.

4.1 Function Inlining
# Replace function call with function body.
# Reduces call overhead, enables further optimizations.
# Heuristics: Cost model based on instruction count, complexity.

# Before:
# define i32 @square(i32 %x) {
#   %res = mul i32 %x, %x
#   ret i32 %res
# }
# define i32 @main() {
#   %val = call i32 @square(i32 5)
#   ret i32 %val
# }

# After (inlined):
# define i32 @main() {
#   %val = mul i32 5, 5
#   ret i32 25
# }

4.2 Interprocedural Optimization (IPO)
# Optimizations across function boundaries.
# Requires Whole Program Analysis or Link-Time Optimization (LTO).
# Enable LTO: clang -flto file.c -o file

4.3 Global Value Numbering (GVN)
# Assign unique numbers to equivalent values across basic blocks.
# More powerful than CSE.
# Uses dominance tree to find available expressions.

CHAPTER 5: LOOP OPTIMIZATIONS
Critical for performance in scientific computing and data processing.

5.1 Loop Invariant Code Motion (LICM)
# Move calculations that don't change inside the loop to outside.
# Before:
# for (i=0; i<n; i++) {
#   a[i] = b[i] + c * d;  // c*d is invariant
# }
# After:
# temp = c * d;
# for (i=0; i<n; i++) {
#   a[i] = b[i] + temp;
# }

5.2 Loop Unrolling
# Replicate loop body to reduce branch overhead and increase Instruction Level Parallelism (ILP).
# Before:
# for (i=0; i<4; i++) {
#   sum += arr[i];
# }
# After (Unrolled by 4):
# sum += arr[0];
# sum += arr[1];
# sum += arr[2];
# sum += arr[3];

# Heuristics: Trip count known? Body size small?

5.3 Loop Vectorization
# Use SIMD instructions to process multiple data elements simultaneously.
# Requires no data dependencies between iterations.
# Before:
# for (i=0; i<N; i++) {
#   C[i] = A[i] + B[i];
# }
# After (AVX2, 8 floats at once):
# for (i=0; i<N; i+=8) {
#   va = load_8_floats(&A[i]);
#   vb = load_8_floats(&B[i]);
#   vc = add_8_floats(va, vb);
#   store_8_floats(&C[i], vc);
# }

# Enable reports: clang -Rpass=loop-vectorize file.c

5.4 Loop Fusion
# Combine two loops iterating over same range into one.
# Improves cache locality.
# Before:
# for (i=0; i<N; i++) A[i] = B[i] + 1;
# for (i=0; i<N; i++) C[i] = A[i] * 2;
# After:
# for (i=0; i<N; i++) {
#   A[i] = B[i] + 1;
#   C[i] = A[i] * 2;
# }

CHAPTER 6: MEMORY OPTIMIZATIONS
6.1 Alias Analysis
# Determine if two pointers can point to the same memory location.
# Crucial for reordering loads/stores.
# Types:
# - NoAlias: Pointers never overlap.
# - MayAlias: Pointers might overlap.
# - MustAlias: Pointers always overlap.

# Restrict keyword (C99) helps compiler assume NoAlias.
# void add(int* __restrict__ a, int* __restrict__ b, int n) {
#   for (int i=0; i<n; i++) a[i] += b[i];
# }

6.2 Stack Promotion
# Convert heap allocations (malloc) to stack allocations if lifetime is local.
# Faster allocation/deallocation.

6.3 Cache Optimization
# Data Layout Transformation: Arrange data to fit cache lines.
# Array of Structures (AoS) vs Structure of Arrays (SoA).

# AoS (Bad for SIMD):
# struct Point { float x, y, z; };
# Point points[N];

# SoA (Good for SIMD):
# float x[N], y[N], z[N];

CHAPTER 7: AUTO-VECTORIZATION & POLYHEDRAL MODEL
7.1 Auto-Vectorization Requirements
# 1. Loop count known or predictable.
# 2. No data dependencies between iterations.
# 3. Aligned memory access (preferred).
# 4. Simple loop body.

# Example:
# void scale(float* a, float b, int n) {
#   #pragma clang loop vectorize(enable)
#   for (int i=0; i<n; i++) {
#     a[i] *= b;
#   }
# }

7.2 Polyhedral Model
# Advanced mathematical model for loop optimizations.
# Handles complex nested loops and data dependencies.
# Used in LLVM's Polly optimizer.
# Transformations: Tiling, Skewing, Interchange.

# Enable Polly: clang -O3 -mllvm -polly file.c

# Tiling Example:
# Before:
# for (i=0; i<N; i++)
#   for (j=0; j<M; j++)
#     A[i][j] = B[i][j] + C[i][j];

# After (Tiled 32x32):
# for (ii=0; ii<N; ii+=32)
#   for (jj=0; jj<M; jj+=32)
#     for (i=ii; i<min(ii+32, N); i++)
#       for (j=jj; j<min(jj+32, M); j++)
#         A[i][j] = B[i][j] + C[i][j];

CHAPTER 8: PROFILE-GUIDED OPTIMIZATION (PGO)
8.1 How PGO Works
# 1. Instrumented Build: Compile with profiling instrumentation.
# 2. Training Run: Execute program with representative data.
# 3. Optimized Build: Recompile using profile data.

# Clang PGO:
# Step 1: clang -fprofile-generate file.c -o file_instr
# Step 2: ./file_instr < input_data
# Step 3: clang -fprofile-use=file.profdata file.c -o file_opt

8.2 Benefits
# - Better inlining decisions.
# - Accurate branch prediction hints.
# - Improved register allocation.
# - Hot/Cold code splitting.

CHAPTER 9: ADVANCED TOPICS AND RESOURCES
9.1 Link-Time Optimization (LTO)
# Optimize across translation units (.c files).
# Requires whole-program visibility.
# ThinLTO: Scalable LTO for large projects.
# clang -flto=thin file1.c file2.c -o app

9.2 Debugging Optimizations
# Use -g to keep debug info.
# Use -Og: Optimize for debugging experience.
# Inspect LLVM IR: clang -S -emit-llvm file.c
# Inspect Assembly: objdump -d app

9.3 Compiler Flags CheatSheet
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