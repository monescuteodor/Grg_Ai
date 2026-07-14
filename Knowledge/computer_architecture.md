Computer Architecture & Assembly Language Complete Reference
CHAPTER 1: GETTING STARTED WITH COMPUTER ARCHITECTURE
Remarks
Computer architecture studies the design and organization of computer systems. Key concepts: instruction set architecture (ISA), pipelining, cache hierarchy, virtual memory, parallelism. Assembly language provides direct hardware control. Modern architectures: x86-64 (Intel/AMD), ARM (mobile/embedded), RISC-V (open source).
Tools: NASM (assembler), GCC (compiler), GDB (debugger), QEMU (emulator), objdump (binary analysis).
Hello Assembly
; hello.asm - x86-64 Linux assembly
section .data
    msg db "Hello, Assembly!", 10
    len equ $ - msg

section .text
    global _start

_start:
    ; write(1, msg, len)
    mov rax, 1          ; syscall number (sys_write)
    mov rdi, 1          ; file descriptor (stdout)
    mov rsi, msg        ; message address
    mov rdx, len        ; message length
    syscall

    ; exit(0)
    mov rax, 60         ; syscall number (sys_exit)
    xor rdi, rdi        ; exit code 0
    syscall

; Build and run:
; nasm -f elf64 hello.asm -o hello.o
; ld hello.o -o hello
; ./hello

CHAPTER 2: CPU ARCHITECTURE FUNDAMENTALS
Instruction Set Architecture (ISA)
# ISA defines the interface between hardware and software.
# Components: instruction set, registers, memory model, addressing modes.

# x86-64 Registers (64-bit mode)
# General purpose: rax, rbx, rcx, rdx, rsi, rdi, rbp, rsp, r8-r15
# Special: rip (instruction pointer), rflags (status flags)

# Register breakdown (example: rax)
# rax: 64-bit
# eax: lower 32 bits
# ax: lower 16 bits
# ah: high 8 bits of ax
# al: low 8 bits of ax

# Example: Register operations
; mov rax, 0x123456789ABCDEF0  ; 64-bit move
; mov eax, 0x12345678          ; 32-bit move (zeros upper 32 bits)
; mov ax, 0x1234               ; 16-bit move
; mov al, 0x56                 ; 8-bit move

# Addressing Modes
# Immediate: mov rax, 42           ; constant value
# Register: mov rbx, rax           ; register to register
# Direct: mov rax, [0x1000]        ; memory address
# Indirect: mov rax, [rbx]         ; address in register
# Base+Offset: mov rax, [rbx+8]    ; base + displacement
# Scaled Index: mov rax, [rbx+rcx*4] ; base + index*scale

# Example: Array access
section .data
    array dq 10, 20, 30, 40, 50

section .text
    ; Access array[2] (30)
    mov rbx, array        ; base address
    mov rcx, 2            ; index
    mov rax, [rbx+rcx*8]  ; array[2] (8 bytes per element)

CPU Modes and Privilege Levels
# x86 has 4 privilege levels (rings 0-3)
# Ring 0: Kernel mode (full hardware access)
# Ring 3: User mode (restricted access)
# Most OS use only Ring 0 and Ring 3

# Privileged instructions (Ring 0 only):
# - CLI/STI (disable/enable interrupts)
# - HLT (halt CPU)
# - IN/OUT (port I/O)
# - MOV to/from control registers (CR0, CR3, etc.)
# - RDMSR/WRMSR (model-specific registers)

# Switching to kernel mode:
# - System call (syscall/sysenter)
# - Interrupt (INT instruction)
# - Exception (divide by zero, page fault)

; Example: System call (user → kernel)
; mov rax, 60    ; syscall number
; syscall        ; trap to kernel
; ; CPU switches to Ring 0, executes kernel handler
; ; Kernel returns with SYSRET, back to Ring 3

CHAPTER 3: PIPELINING AND HAZARDS
Pipeline Stages
# Classic 5-stage RISC pipeline:
# 1. IF (Instruction Fetch): Read instruction from memory
# 2. ID (Instruction Decode): Decode instruction, read registers
# 3. EX (Execute): ALU operation or address calculation
# 4. MEM (Memory): Load/store data
# 5. WB (Write Back): Write result to register

# Pipeline timing (instructions per cycle):
# Cycle:  1  2  3  4  5  6  7
# Instr1: IF ID EX MEM WB
# Instr2:    IF ID EX MEM WB
# Instr3:       IF ID EX MEM WB
# Instr4:          IF ID EX MEM WB
# Instr5:             IF ID EX MEM WB

# Ideal throughput: 1 instruction completes per cycle (after fill)

Pipeline Hazards
# Hazards prevent next instruction from executing in next cycle.
# Types:
# 1. Structural hazard: Resource conflict (e.g., memory port)
# 2. Data hazard: Instruction depends on previous result
# 3. Control hazard: Branch/jump changes flow

# Data Hazard Example:
; add rax, rbx    ; rax = rax + rbx
; sub rcx, rax    ; rcx = rcx - rax (needs rax from above)
# Problem: SUB needs rax before ADD writes it

# Solutions:
# 1. Stalling (pipeline bubble): Wait until result ready
# 2. Forwarding (bypassing): Send result directly to next stage
# 3. Compiler reordering: Rearrange instructions to avoid hazard

# Forwarding example:
; Cycle:  1  2  3  4  5
# ADD:    IF ID EX MEM WB
# SUB:       IF ID EX MEM WB
#                  ↑
#         Forward rax from EX/MEM to EX stage

# Control Hazard (Branch):
; cmp rax, 0
; je label        ; branch if equal
; add rbx, 1      ; executed if branch not taken
; label:
; sub rcx, 1

# Problem: Don't know which path until branch resolved
# Solutions:
# 1. Stall until branch resolved
# 2. Branch prediction (guess direction)
# 3. Delayed branch (execute next instruction regardless)

Branch Prediction
# Modern CPUs predict branch direction to avoid stalls.
# Techniques:
# 1. Static prediction: Always taken/not taken
# 2. Dynamic prediction: Learn from history
# 3. Two-level prediction: Use pattern of recent branches

# Branch Target Buffer (BTB):
# Stores target address of predicted-taken branches
# Allows fetch to continue at predicted target

# Example: Loop branch prediction
; mov rcx, 10
; loop:
;   add rax, 1
;   dec rcx
;   jnz loop      ; branch back to loop
# Predictor learns: branch taken 9 times, not taken 1 time
# Accuracy: ~90% for simple loops

# Misprediction penalty: 15-20 cycles (flush pipeline)

; Example: Branch-free code (avoid misprediction)
; Instead of:
; cmp rax, rbx
; jge skip
; mov rcx, rax
; skip:

; Use conditional move:
; cmp rax, rbx
; cmovge rcx, rax    ; move if greater or equal (no branch)

Instruction-Level Parallelism (ILP)
# Superscalar CPUs execute multiple instructions per cycle.
# Requirements:
# 1. No dependencies between instructions
# 2. Multiple execution units (ALU, FPU, load/store)
# 3. Out-of-order execution

# Example: Parallel execution
; add rax, rbx      ; ALU1
; sub rcx, rdx      ; ALU2 (parallel)
; mov r8, [rsi]     ; Load unit (parallel)
; mul r9, r10       ; Multiply unit (parallel)

# Dependency example (cannot parallelize):
; add rax, rbx
; sub rax, rcx      ; depends on rax
; mul rax, rdx      ; depends on rax

# Compiler optimization: Reorder to maximize ILP
; Before:
; add rax, rbx
; sub rax, rcx
; add rdx, r8
; sub rdx, r9

; After (reordered):
; add rax, rbx
; add rdx, r8       ; independent, can execute in parallel
; sub rax, rcx
; sub rdx, r9

CHAPTER 4: CACHE HIERARCHY
Cache Basics
# Cache: Small, fast memory between CPU and main memory.
# Hierarchy: L1 (fastest, smallest) → L2 → L3 → RAM (slowest, largest)

# Typical sizes and latencies:
# L1: 32-64 KB, 1-4 cycles
# L2: 256 KB - 1 MB, 10-12 cycles
# L3: 4-32 MB, 30-40 cycles
# RAM: 8-128 GB, 200-300 cycles

# Cache line: Unit of transfer (typically 64 bytes)
# When CPU reads address, entire cache line loaded

# Cache hit: Data found in cache (fast)
# Cache miss: Data not in cache, fetch from lower level (slow)

# Example: Cache-friendly array access
section .data
    array dq 1000000 dup(0)

section .text
    ; Sequential access (cache-friendly)
    mov rcx, 1000000
    mov rbx, 0
loop_seq:
    add rax, [array+rbx*8]
    inc rbx
    dec rcx
    jnz loop_seq

    ; Random access (cache-unfriendly)
    mov rcx, 1000000
loop_rand:
    mov rdx, random_index
    add rax, [array+rdx*8]  ; likely cache miss
    dec rcx
    jnz loop_rand

Cache Organization
# Direct-mapped: Each address maps to exactly one cache line
# Fully associative: Address can go to any cache line
# Set-associative: Compromise (e.g., 8-way set-associative)

# Cache address breakdown (set-associative):
# [ tag | index | offset ]
# Offset: Byte within cache line (6 bits for 64-byte line)
# Index: Selects set (e.g., 6 bits for 64 sets)
# Tag: Identifies which block is stored

# Example: 32 KB, 8-way set-associative, 64-byte lines
# Total lines: 32 KB / 64 B = 512 lines
# Sets: 512 / 8 = 64 sets
# Index bits: log2(64) = 6 bits
# Offset bits: log2(64) = 6 bits
# Tag bits: 64 - 6 - 6 = 52 bits (for 64-bit address)

# Cache replacement policies:
# 1. LRU (Least Recently Used): Replace least recently accessed
# 2. FIFO (First In First Out): Replace oldest
# 3. Random: Replace random line

Cache Coherence (Multi-core)
# Problem: Multiple cores have private caches
# If core 1 writes to address X, core 2's cache may have stale value

# Solutions:
# 1. Snooping: Cores monitor bus for writes
# 2. Directory-based: Central directory tracks cache state
# 3. MESI protocol: Modified, Exclusive, Shared, Invalid states

# MESI states:
# Modified: Cache line modified, only in this cache
# Exclusive: Clean, only in this cache
# Shared: Clean, may be in multiple caches
# Invalid: Not valid, must fetch from memory

# Example: False sharing
# Two threads modify different variables on same cache line
; Thread 1: array[0] = 1
; Thread 2: array[1] = 2
# Both on same cache line → constant invalidation (slow)

; Solution: Pad variables to separate cache lines
struct padded_counter {
    int64_t value;
    char padding[56];  // pad to 64 bytes
};

CHAPTER 5: VIRTUAL MEMORY
Paging
# Virtual memory: Each process has its own address space.
# MMU (Memory Management Unit) translates virtual → physical addresses.
# Page: Fixed-size block (typically 4 KB).

# Page table: Maps virtual pages to physical frames.
# Multi-level page tables reduce memory usage.

# x86-64 4-level page table:
# PML4 (Page Map Level 4) → PDPT → PD → PT → Physical page

# Virtual address breakdown (4 KB pages):
# [ PML4 index | PDPT index | PD index | PT index | offset ]
# [   9 bits   |  9 bits    | 9 bits  | 9 bits  | 12 bits ]

# Example: Page table walk
; Virtual address: 0x0000_1234_5678_9ABC
; PML4 index: 0x000 (bits 39-47)
; PDPT index: 0x123 (bits 30-38)
; PD index: 0x456 (bits 21-29)
; PT index: 0x789 (bits 12-20)
; Offset: 0xABC (bits 0-11)

# Page fault: Virtual address not mapped
# 1. CPU traps to OS
# 2. OS handles fault (allocate page, load from disk, etc.)
# 3. OS updates page table
# 4. CPU retries instruction

TLB (Translation Lookaside Buffer)
# TLB: Cache for page table entries.
# Avoids expensive page table walks.
# Typical: 64-1024 entries, 1-4 cycle lookup.

# TLB hit: Translation found in TLB (fast)
# TLB miss: Must walk page table (slow)

# TLB entry: [ virtual page number | physical frame number | flags ]

# Example: TLB shootdown (multi-core)
# Core 1 modifies page table
# Must invalidate TLB entries on other cores
# 1. Core 1 sends IPI (Inter-Processor Interrupt) to other cores
# 2. Other cores invalidate TLB entries
# 3. Cores acknowledge

Memory Protection
# Page table entries include protection flags:
# - Present: Page is in physical memory
# - Read/Write: Access permissions
# - User/Supervisor: Privilege level
# - Execute: Can execute code from this page (NX bit)

# Example: Segmentation fault
; mov rax, [0]      ; dereference null pointer
# Page 0 not mapped → page fault → SIGSEGV

# Example: Stack canary (buffer overflow protection)
; Function prologue:
; mov rax, fs:0x28      ; load canary value
; mov [rbp-8], rax      ; store on stack

; Function epilogue:
; mov rcx, [rbp-8]      ; load canary
; xor rcx, fs:0x28      ; compare with original
; jne stack_smashed     ; branch if different (overflow detected)

CHAPTER 6: X86-64 ASSEMBLY PROGRAMMING
Data Movement
; mov dest, src         ; move data
; mov rax, rbx          ; register to register
; mov rax, 42           ; immediate to register
; mov rax, [rbx]        ; memory to register
; mov [rbx], rax        ; register to memory

; movzx dest, src       ; move with zero extension
; movzx eax, byte [rbx] ; load byte, zero-extend to 32 bits

; movsx dest, src       ; move with sign extension
; movsx eax, byte [rbx] ; load byte, sign-extend to 32 bits

; lea dest, [src]       ; load effective address
; lea rax, [rbx+rcx*4+8] ; rax = rbx + rcx*4 + 8 (no memory access)

; xchg rax, rbx         ; exchange registers
; cmpxchg dest, src     ; compare and exchange (atomic)

Arithmetic Operations
; add dest, src         ; dest = dest + src
; sub dest, src         ; dest = dest - src
; inc dest              ; dest = dest + 1
; dec dest              ; dest = dest - 1
; neg dest              ; dest = -dest

; mul src               ; unsigned multiply
; rdx:rax = rax * src   ; 128-bit result

; imul src              ; signed multiply
; imul dest, src        ; dest = dest * src (32/64-bit result)

; div src               ; unsigned divide
; rax = rdx:rax / src   ; quotient in rax
; rdx = rdx:rax % src   ; remainder in rdx

; idiv src              ; signed divide

; Example: Compute (a * b) + c
; mov rax, [a]
; imul rax, [b]
; add rax, [c]
; mov [result], rax

Logical Operations
; and dest, src         ; bitwise AND
; or dest, src          ; bitwise OR
; xor dest, src         ; bitwise XOR
; not dest              ; bitwise NOT
; test dest, src        ; AND without storing (sets flags)

; shl dest, count       ; shift left (multiply by 2^n)
; shr dest, count       ; shift right unsigned
; sar dest, count       ; shift right signed

; Example: Check if even
; test rax, 1           ; test lowest bit
; jz is_even            ; jump if zero (even)

; Example: Multiply by 8
; shl rax, 3            ; rax = rax * 8

Control Flow
; cmp op1, op2          ; compare (subtract, set flags)
; jmp label             ; unconditional jump
; je label              ; jump if equal (ZF=1)
; jne label             ; jump if not equal (ZF=0)
; jg label              ; jump if greater (signed)
; jl label              ; jump if less (signed)
; ja label              ; jump if above (unsigned)
; jb label              ; jump if below (unsigned)

; Example: If-else
; cmp rax, rbx
; jge else_label
; ; then block
; mov rcx, 1
; jmp end_if
; else_label:
; mov rcx, 2
; end_if:

; Example: For loop
; mov rcx, 10           ; counter
; loop_start:
;   ; loop body
;   dec rcx
;   jnz loop_start

; Example: While loop
; while_start:
;   cmp rax, 0
;   jle while_end
;   ; loop body
;   dec rax
;   jmp while_start
; while_end:

Function Calls
; Calling convention (System V AMD64 ABI):
; Arguments: rdi, rsi, rdx, rcx, r8, r9 (first 6)
; Return value: rax
; Caller-saved: rax, rcx, rdx, rsi, rdi, r8-r11
; Callee-saved: rbx, rbp, r12-r15

; Example: Function call
; mov rdi, arg1
; mov rsi, arg2
; call function_name
; ; result in rax

; Example: Function implementation
; function_name:
;   push rbp            ; save frame pointer
;   mov rbp, rsp        ; set up frame
;   push rbx            ; save callee-saved registers
;   
;   ; function body
;   mov rax, rdi        ; access arg1
;   add rax, rsi        ; access arg2
;   
;   pop rbx             ; restore callee-saved
;   pop rbp             ; restore frame pointer
;   ret                 ; return

Stack Frame
; Stack grows downward (high to low addresses)
; RSP points to top of stack

; Stack frame layout:
; [ local variables ]
; [ saved RBP ]       ← RBP points here
; [ return address ]
; [ arguments ]       ← RSP points here (after call)

; Example: Function with local variables
; my_function:
;   push rbp
;   mov rbp, rsp
;   sub rsp, 32         ; allocate 32 bytes for locals
;   
;   mov [rbp-8], rax    ; local variable 1
;   mov [rbp-16], rbx   ; local variable 2
;   
;   add rsp, 32         ; deallocate locals
;   pop rbp
;   ret

CHAPTER 7: SIMD (SINGLE INSTRUCTION, MULTIPLE DATA)
SIMD Basics
# SIMD: Process multiple data elements with one instruction.
# x86 SIMD extensions: MMX (64-bit), SSE (128-bit), AVX (256-bit), AVX-512 (512-bit)

# SSE registers: xmm0-xmm15 (128-bit each)
# AVX registers: ymm0-ymm15 (256-bit each, extend xmm)
# AVX-512: zmm0-zmm31 (512-bit each, extend ymm)

# Data types:
# 128-bit: 16×8-bit, 8×16-bit, 4×32-bit, 2×64-bit, 4×float, 2×double
# 256-bit: 32×8-bit, 16×16-bit, 8×32-bit, 4×64-bit, 8×float, 4×double

# Example: Vector addition (4 floats at once)
; movups xmm0, [a]      ; load 4 floats from a
; movups xmm1, [b]      ; load 4 floats from b
; addps xmm0, xmm1      ; add packed singles (4 adds)
; movups [c], xmm0      ; store result

SSE Instructions
; Data movement
; movaps dest, src      ; move aligned packed singles
; movups dest, src      ; move unaligned packed singles
; movss dest, src       ; move scalar single

; Arithmetic
; addps dest, src       ; add packed singles
; subps dest, src       ; subtract packed singles
; mulps dest, src       ; multiply packed singles
; divps dest, src       ; divide packed singles
; sqrtps dest, src      ; square root packed singles

; Comparison
; cmpps dest, src, imm  ; compare packed singles
; ; imm: 0=eq, 1=lt, 2=le, 3=unord, 4=ne, 5=nlt, 6=nle, 7=ord

; Conversion
; cvtps2pd dest, src    ; convert packed singles to doubles
; cvtpi2ps dest, src    ; convert packed integers to singles

; Example: Dot product (4 elements)
; movups xmm0, [a]      ; load a[0..3]
; movups xmm1, [b]      ; load b[0..3]
; mulps xmm0, xmm1      ; a[i] * b[i]
; movaps xmm1, xmm0     ; copy
; shufps xmm1, xmm1, 0x4E ; shuffle: [1,0,3,2]
; addps xmm0, xmm1      ; add pairs: [0+1, 1+0, 2+3, 3+2]
; movaps xmm1, xmm0
; shufps xmm1, xmm1, 0x11 ; shuffle: [1,1,1,1]
; addss xmm0, xmm1      ; add scalars: result in xmm0[0]

AVX Instructions
; 256-bit operations (8 floats or 4 doubles)
; vmovups ymm0, [a]     ; load 8 floats
; vaddps ymm0, ymm1, ymm2 ; ymm0 = ymm1 + ymm2
; vmulps ymm0, ymm1, ymm2 ; ymm0 = ymm1 * ymm2

; Example: Vectorized array addition
; add_arrays:
;   mov rcx, n
;   xor rax, rax        ; index
; loop:
;   vmovups ymm0, [a+rax*4]   ; load 8 floats
;   vmovups ymm1, [b+rax*4]   ; load 8 floats
;   vaddps ymm0, ymm0, ymm1   ; add
;   vmovups [c+rax*4], ymm0   ; store
;   add rax, 8
;   cmp rax, rcx
;   jl loop

; Example: Horizontal sum (8 floats)
; vextractf128 xmm1, ymm0, 1  ; extract high 128 bits
; vaddps xmm0, xmm0, xmm1     ; add low and high
; vhaddps xmm0, xmm0, xmm0    ; horizontal add (pairs)
; vhaddps xmm0, xmm0, xmm0    ; horizontal add again
; ; result in xmm0[0]

SIMD Optimization Techniques
# Alignment: Aligned data faster (movaps vs movups)
# Loop unrolling: Process multiple vectors per iteration
# Avoid dependencies: Use separate registers

# Example: Optimized dot product
; dot_product:
;   vxorps ymm0, ymm0, ymm0   ; accumulator = 0
;   mov rcx, n
;   xor rax, rax
; loop:
;   vmovups ymm1, [a+rax*4]
;   vmovups ymm2, [b+rax*4]
;   vfmadd231ps ymm0, ymm1, ymm2  ; ymm0 += ymm1 * ymm2
;   add rax, 8
;   cmp rax, rcx
;   jl loop
; ; horizontal sum ymm0
; vextractf128 xmm1, ymm0, 1
; vaddps xmm0, xmm0, xmm1
; vhaddps xmm0, xmm0, xmm0
; vhaddps xmm0, xmm0, xmm0
; movss [result], xmm0

CHAPTER 8: PERFORMANCE OPTIMIZATION
Memory Access Patterns
# Sequential access: Cache-friendly (spatial locality)
# Random access: Cache-unfriendly
# Stride access: Moderate (depends on stride)

# Example: Matrix multiplication (naive - poor locality)
; for i in 0..n:
;   for j in 0..n:
;     for k in 0..n:
;       C[i][j] += A[i][k] * B[k][j]  ; B access is column-wise (bad)

# Example: Matrix multiplication (optimized - loop interchange)
; for i in 0..n:
;   for k in 0..n:
;     for j in 0..n:
;       C[i][j] += A[i][k] * B[k][j]  ; B access is row-wise (good)

# Example: Cache blocking (process sub-matrices)
; for i in 0..n step BLOCK:
;   for j in 0..n step BLOCK:
;     for k in 0..n step BLOCK:
;       ; multiply BLOCK×BLOCK sub-matrices

Branch Optimization
# Branches are expensive (misprediction penalty)
# Techniques:
# 1. Sort data (predictable branches)
# 2. Use conditional moves (cmov)
# 3. Branch-free code (arithmetic instead of branches)

# Example: Branch-free max
; Instead of:
; cmp rax, rbx
; jge skip
; mov rax, rbx
; skip:

; Use:
; mov rcx, rax
; sub rcx, rbx          ; rcx = rax - rbx
; sar rcx, 63           ; rcx = (rax < rbx) ? -1 : 0
; and rcx, rbx          ; rcx = (rax < rbx) ? rbx : 0
; not rcx               ; rcx = (rax < rbx) ? 0 : -1
; and rax, rcx          ; rax = (rax >= rbx) ? rax : 0
; or rax, rcx           ; rax = max(rax, rbx)

; Simpler with cmov:
; cmp rax, rbx
; cmovl rax, rbx        ; rax = (rax < rbx) ? rbx : rax

Loop Optimization
# Loop unrolling: Reduce loop overhead
# Loop fusion: Combine loops with same bounds
# Loop fission: Split loop for better cache usage

# Example: Loop unrolling (4x)
; mov rcx, n
; shr rcx, 2            ; rcx = n / 4
; loop:
;   ; process 4 elements
;   add rax, [arr+rdx]
;   add rax, [arr+rdx+8]
;   add rax, [arr+rdx+16]
;   add rax, [arr+rdx+24]
;   add rdx, 32
;   dec rcx
;   jnz loop
; ; handle remainder
; mov rcx, n
; and rcx, 3            ; rcx = n % 4
; remainder_loop:
;   add rax, [arr+rdx]
;   add rdx, 8
;   dec rcx
;   jnz remainder_loop

Function Inlining
# Inline small functions to eliminate call overhead
# Trade-off: Code size vs. performance

# Example: Before inlining
; int add(int a, int b) { return a + b; }
; int x = add(1, 2);

# After inlining:
; int x = 1 + 2;  ; directly computed

CHAPTER 9: GPU ARCHITECTURE BASICS
GPU vs CPU
# CPU: Few cores, complex control logic, large caches
# GPU: Many cores, simple cores, high memory bandwidth

# GPU architecture:
# - Streaming Multiprocessors (SMs): 50-100+ SMs
# - CUDA cores per SM: 64-128+
# - Total cores: 1000-10000+
# - Memory: GDDR6/HBM (high bandwidth)

# Execution model:
# - Threads grouped into warps (32 threads)
# - Warps execute in SIMT (Single Instruction, Multiple Threads)
# - All threads in warp execute same instruction

CUDA Programming Model
; Example: CUDA kernel (GPU function)
; __global__ void vector_add(float* a, float* b, float* c, int n) {
;     int idx = blockIdx.x * blockDim.x + threadIdx.x;
;     if (idx < n) {
;         c[idx] = a[idx] + b[idx];
;     }
; }

; Launch kernel:
; int threads_per_block = 256;
; int blocks = (n + threads_per_block - 1) / threads_per_block;
; vector_add<<<blocks, threads_per_block>>>(a, b, c, n);

Memory Hierarchy (GPU)
# Registers: Per-thread, fastest
# Shared memory: Per-block, shared between threads
# L1 cache: Per-SM
# L2 cache: Global
# Global memory: Slowest, largest

# Memory coalescing: Adjacent threads access adjacent memory
# Example: Coalesced access
; thread 0: a[0]
; thread 1: a[1]
; thread 2: a[2]
; ; single 128-byte transaction

# Example: Uncoalesced access
; thread 0: a[0]
; thread 1: a[32]
; thread 2: a[64]
; ; multiple transactions (slow)

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Performance Counters
# Hardware performance counters measure:
# - Instructions executed
# - Cache hits/misses
# - Branch mispredictions
# - Cycles stalled

# Example: Using perf (Linux)
; perf stat ./program
; ; shows: cycles, instructions, cache-misses, etc.

; perf record ./program
; perf report
; ; shows: which functions are hot

# Example: Using PAPI (Performance Application Programming Interface)
; #include <papi.h>
; PAPI_start(PAPI_TOT_CYC);
; // code to measure
; PAPI_stop(PAPI_TOT_CYC, &values);

Debugging with GDB
; gdb ./program
; (gdb) break main
; (gdb) run
; (gdb) info registers
; (gdb) x/10x $rsp        ; examine stack
; (gdb) stepi             ; step one instruction
; (gdb) disassemble       ; show assembly

Binary Analysis
; objdump -d program      ; disassemble
; objdump -t program      ; show symbol table
; readelf -a program      ; show ELF info
; nm program              ; list symbols

; Example: Analyze cache behavior
; valgrind --tool=cachegrind ./program
; cg_annotate cachegrind.out

Recommended Reading
# - "Computer Organization and Design" by Patterson & Hennessy
# - "Computer Architecture: A Quantitative Approach" by Hennessy & Patterson
# - "Professional Assembly Language" by Richard Blum
# - Intel Software Developer Manual (Volume 1-3)
# - AMD64 Architecture Programmer's Manual

# Online Resources
# - https://www.felixcloutier.com/x86/ (x86 instruction reference)
# - https://godbolt.org/ (Compiler Explorer)
# - https://uops.info/ (microarchitecture database)

# End of Computer Architecture Reference  