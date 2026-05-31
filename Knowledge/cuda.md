# CUDA Complete Reference — NVIDIA GPU Programming

## GPU Architecture Fundamentals

CUDA (Compute Unified Device Architecture) is NVIDIA's parallel computing platform extending C/C++ for GPU programming.

GPU vs CPU design philosophy:
- CPU: few powerful cores (4–32), optimized for latency, large cache, complex branch prediction.
- GPU: thousands of simpler cores, optimized for throughput, hides latency with massive parallelism.
- GPU wins on: matrix ops, image processing, neural networks, physics simulations, FFT.
- CPU wins on: sequential logic, complex branching, small data, low-latency single tasks.

NVIDIA GPU hierarchy:
- SM (Streaming Multiprocessor): the fundamental compute unit. Each SM has CUDA cores, warp schedulers, shared memory, L1 cache, tensor cores (Volta+).
- GPC (Graphics Processing Cluster): group of SMs.
- GPU chip: multiple GPCs + L2 cache + memory controllers + HBM/GDDR6 VRAM.

Examples:
- RTX 3090 (Ampere): 10496 CUDA cores, 82 SMs, 24 GB GDDR6X.
- RTX 4090 (Ada Lovelace): 16384 CUDA cores, 128 SMs, 24 GB GDDR6X.
- A100 (Ampere, data center): 6912 CUDA cores, 108 SMs, up to 80 GB HBM2e.
- H100 (Hopper): 16896 CUDA cores, 132 SMs, 80 GB HBM3.

Warp: the fundamental execution unit — 32 threads that execute together in lockstep (SIMT — Single Instruction Multiple Thread). All 32 threads execute the same instruction simultaneously.
Warp scheduler: each SM has 4 warp schedulers. When one warp stalls (waiting for memory), the scheduler switches to another ready warp — this is how the GPU hides memory latency.
Occupancy: ratio of active warps to maximum possible warps per SM. Higher = better latency hiding.

Compute capability: version number (e.g., 8.6 for Ampere RTX 30xx) that indicates feature support.
- 6.x: Pascal (GTX 10xx, P100)
- 7.0: Volta (V100) — first with tensor cores
- 7.5: Turing (RTX 20xx)
- 8.0: Ampere A100; 8.6: Ampere RTX 30xx
- 8.9: Ada Lovelace RTX 40xx
- 9.0: Hopper H100

## Thread Hierarchy and Indexing

Execution hierarchy: Thread → Warp (32 threads) → Block → Grid.

Built-in variables:
- threadIdx.x/y/z — thread index within its block
- blockIdx.x/y/z  — block index within the grid
- blockDim.x/y/z  — number of threads per block
- gridDim.x/y/z   — number of blocks in the grid
- warpSize        — always 32

Function qualifiers:
- __global__  : kernel — called from host, runs on device
- __device__  : helper — called from device only
- __host__    : runs on host (default, can combine with __device__)
- __forceinline__ / __noinline__ : optimization hints

Variable qualifiers:
- __shared__   : shared memory — fast, per-block, ~48–100 KB
- __constant__ : constant memory — read-only, cached, 64 KB total
- __device__   : global device memory — all threads, slow
- __restrict__ : pointer alias hint (like C99 restrict)

```cpp
// 1D global thread ID
int tid = blockIdx.x * blockDim.x + threadIdx.x;

// 2D (for matrices)
int row = blockIdx.y * blockDim.y + threadIdx.y;
int col = blockIdx.x * blockDim.x + threadIdx.x;
int idx = row * width + col;  // row-major linear index

// 3D (for volumes)
int x = blockIdx.x * blockDim.x + threadIdx.x;
int y = blockIdx.y * blockDim.y + threadIdx.y;
int z = blockIdx.z * blockDim.z + threadIdx.z;
int idx3d = z * (width * height) + y * width + x;

// Kernel launch syntax: kernel<<<gridDim, blockDim, sharedMemBytes, stream>>>
// gridDim and blockDim can be int (1D) or dim3 (up to 3D)
dim3 block(16, 16, 1);                           // 256 threads per block
dim3 grid((W + 15)/16, (H + 15)/16, 1);          // enough blocks to cover WxH
matrix_kernel<<<grid, block>>>(d_A, W, H);

// Calculate grid size to cover n elements
int threads = 256;
int blocks = (n + threads - 1) / threads;        // ceil division
kernel<<<blocks, threads>>>(d_data, n);
```

Limits (vary by compute capability):
- Max threads per block: 1024
- Max block dimensions: 1024 × 1024 × 64
- Max grid dimensions: 2³¹ × 65535 × 65535
- Warp size: always 32
- Max shared memory per block: 48 KB (can be increased to 96–164 KB on Ampere with cudaFuncSetAttribute)

## Memory Hierarchy

Understanding and using the right memory type is the most critical optimization in CUDA.

| Memory Type | Location | Speed | Scope | Lifetime | Size |
|---|---|---|---|---|---|
| Registers | SM | Fastest | Thread | Thread | ~255 per thread |
| Shared memory | SM (on-chip) | ~100× global | Block | Block | 48–164 KB per SM |
| L1 cache | SM (on-chip) | ~100× global | Block | Block | Automatic |
| Constant memory | DRAM + cache | Fast if cached | All threads | Application | 64 KB |
| Texture memory | DRAM + cache | Good for 2D locality | All threads | Application | Limited by DRAM |
| L2 cache | GPU-wide | ~10× global | All | N/A | 4–80 MB |
| Global memory | DRAM | Slowest | All | Application | GB (VRAM) |
| Unified memory | DRAM (CPU+GPU) | Same as global | All | Application | System RAM + VRAM |
| Pinned host memory | CPU RAM | Fast H↔D transfer | Host | Application | System RAM |

```cpp
// Global memory (slowest, accessible by all threads)
float *d_data;
cudaMalloc(&d_data, n * sizeof(float));
cudaMemcpy(d_data, h_data, n * sizeof(float), cudaMemcpyHostToDevice);
cudaFree(d_data);

// Pinned (page-locked) memory — enables async DMA transfers, ~2–4× faster H↔D
float *h_pinned;
cudaMallocHost(&h_pinned, n * sizeof(float));     // allocate pinned
cudaHostAlloc(&h_pinned, bytes, cudaHostAllocDefault);  // alternative
cudaFreeHost(h_pinned);

// Unified memory — automatically migrates between CPU and GPU
float *u_data;
cudaMallocManaged(&u_data, n * sizeof(float));
// CPU can use u_data directly; GPU can use it in kernels
// Prefetch to GPU before kernel for better performance:
cudaMemPrefetchAsync(u_data, n * sizeof(float), device_id, 0);
cudaDeviceSynchronize();
// CPU access after kernel:
cudaMemPrefetchAsync(u_data, n * sizeof(float), cudaCpuDeviceId, 0);
cudaFree(u_data);

// Constant memory (64 KB, read-only, broadcast-cached)
__constant__ float c_filter[64];
cudaMemcpyToSymbol(c_filter, h_filter, 64 * sizeof(float));
// In kernel: read c_filter[i] — all threads in a warp get the value in ONE cycle

// Shared memory (declared inside kernel)
__global__ void kernel(float *data) {
    __shared__ float smem[256];          // static: size known at compile time
    extern __shared__ float dsmem[];     // dynamic: size given at launch
    smem[threadIdx.x] = data[blockIdx.x * blockDim.x + threadIdx.x];
    __syncthreads();                     // barrier — all threads must reach here
    // use smem...
}
// Dynamic shared memory launch: kernel<<<grid, block, size_bytes>>>(data);

// 2D pitched allocation (for coalesced matrix access)
size_t pitch;
float *d_matrix;
cudaMallocPitch(&d_matrix, &pitch, cols * sizeof(float), rows);
// Access: element[row][col] = d_matrix[row * (pitch/sizeof(float)) + col]
// pitch is padded to ensure each row starts at an aligned address

// Memory info
size_t free_mem, total_mem;
cudaMemGetInfo(&free_mem, &total_mem);
```

## Memory Coalescing — Most Important Optimization

Coalesced access: when all threads in a warp access consecutive memory addresses in a single transaction.
A warp of 32 threads accesses 32 × 4 = 128 bytes. If consecutive, this is ONE 128-byte transaction.
If scattered, it becomes up to 32 separate transactions — 32× slower.

```cpp
// GOOD — coalesced (thread i accesses element i)
__global__ void good(float *data, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) data[i] *= 2.0f;   // stride-1 access
}

// BAD — strided access (32 threads skip 32 elements each = 32 transactions)
__global__ void bad_strided(float *data, int n) {
    int i = threadIdx.x;
    data[i * 32] *= 2.0f;   // stride-32 access — terrible for coalescing
}

// Matrix transpose: naive vs coalesced
// Naive read: coalesced. Naive write: not coalesced (each thread writes to a different row).
// Tiled transpose using shared memory — coalesces both reads and writes:
#define TILE 32
__global__ void transpose(float *out, float *in, int rows, int cols) {
    __shared__ float tile[TILE][TILE + 1];  // +1 avoids bank conflicts
    int x = blockIdx.x * TILE + threadIdx.x;
    int y = blockIdx.y * TILE + threadIdx.y;
    if (x < cols && y < rows)
        tile[threadIdx.y][threadIdx.x] = in[y * cols + x];   // coalesced read
    __syncthreads();
    x = blockIdx.y * TILE + threadIdx.x;
    y = blockIdx.x * TILE + threadIdx.y;
    if (x < rows && y < cols)
        out[y * rows + x] = tile[threadIdx.x][threadIdx.y];  // coalesced write
}
```

Shared memory bank conflicts: shared memory has 32 banks (one per warp lane). If multiple threads in a warp access different addresses in the same bank simultaneously → bank conflict → serialized.
Solution: pad shared memory arrays by 1 element per row: `float smem[N][M + 1]`.
Broadcast: multiple threads accessing the SAME address → no conflict.

## Warp-Level Programming

Warps execute in SIMT — all 32 threads run the same instruction. Branch divergence occurs when threads in the same warp take different code paths — the GPU serializes both paths.

```cpp
// BAD — thread-level divergence within a warp
if (threadIdx.x % 2 == 0)   // half the warp goes one way, half the other
    do_something();

// BETTER — divergence across blocks (no divergence within warp)
if (blockIdx.x % 2 == 0)    // entire block takes one path
    do_something();

// Warp intrinsics (operate on all 32 threads in a warp atomically, no __syncthreads needed)
// __syncwarp(mask): sync threads within warp
// __ballot_sync(mask, predicate): returns bitmask of threads where predicate is true
// __any_sync(mask, predicate): 1 if any thread has predicate true
// __all_sync(mask, predicate): 1 if all threads have predicate true
// __popc(mask): count set bits (population count)

// Warp shuffle — exchange values between threads without shared memory
// __shfl_sync(mask, var, srcLane):   broadcast value from srcLane to all
// __shfl_up_sync(mask, var, delta):  get value from thread (lane - delta)
// __shfl_down_sync(mask, var, delta):get value from thread (lane + delta)
// __shfl_xor_sync(mask, var, laneMask): butterfly pattern

// Warp reduction using shuffle (no shared memory needed!)
__device__ float warp_reduce_sum(float val) {
    for (int offset = 16; offset > 0; offset >>= 1)
        val += __shfl_down_sync(0xffffffff, val, offset);
    return val;  // lane 0 holds the warp sum
}

__global__ void fast_reduce(float *data, float *result, int n) {
    float val = (blockIdx.x * blockDim.x + threadIdx.x < n)
                ? data[blockIdx.x * blockDim.x + threadIdx.x] : 0.0f;
    val = warp_reduce_sum(val);
    if (threadIdx.x % 32 == 0)
        atomicAdd(result, val);
}
```

## Synchronization and Atomics

```cpp
// Thread block barrier — all threads in block must reach before any proceeds
__syncthreads();
__syncthreads_count(pred);  // also returns count of threads where pred != 0
__syncthreads_and(pred);    // returns 1 if pred != 0 for ALL threads
__syncthreads_or(pred);     // returns 1 if pred != 0 for ANY thread

// Warp-level barrier (doesn't flush L1/shared)
__syncwarp(0xffffffff);

// Memory fence — ensure memory ordering
__threadfence();        // all threads in device see this thread's writes
__threadfence_block();  // only threads in same block

// Atomic operations (guaranteed thread-safe, returns old value)
int old = atomicAdd(&shared_counter, 1);   // atomic increment
atomicSub(&val, amount);
atomicMin(&min_val, candidate);
atomicMax(&max_val, candidate);
int old = atomicExch(&lock, 1);            // atomic swap (returns old)
int old = atomicCAS(&addr, expected, new); // compare-and-swap
atomicAnd(&flags, mask);
atomicOr(&flags, bit);
atomicXor(&val, mask);

// Float atomicAdd supported natively on compute 2.0+
atomicAdd(&f_val, 1.0f);

// Mutex using atomicCAS
__device__ void lock(int *mutex) {
    while (atomicCAS(mutex, 0, 1) != 0);  // spin until we get the lock
}
__device__ void unlock(int *mutex) { atomicExch(mutex, 0); }
```

## Kernel Optimization Techniques

```cpp
// 1. Loop unrolling — reduce loop overhead
#pragma unroll 4
for (int i = 0; i < 16; i++) sum += a[i] * b[i];

// 2. Instruction-level optimizations
__fmaf_rn(a, b, c)  // fused multiply-add: a*b+c in ONE instruction
__fdividef(a, b)     // fast (approximate) division — 2 ULP error
__expf(x)            // fast exp
__logf(x)            // fast log
__sinf(x) __cosf(x) // fast trig — lower precision but 2× faster
__rsqrtf(x)          // fast reciprocal square root

// 3. Registers — limit usage to increase occupancy
// Use --maxrregcount=32 compile flag to cap register use
// Or: __launch_bounds__(maxThreadsPerBlock, minBlocksPerSM)
__global__ __launch_bounds__(256, 4) void optimized_kernel(...) {}

// 4. Vectorized loads — load 4 floats in one transaction
float4 val = *reinterpret_cast<float4*>(&data[i]);
// All threads load 4 consecutive floats — very efficient

// 5. Tiling pattern — bring global data into shared memory in tiles
__global__ void tiled_kernel(float *A, float *B, float *C, int N) {
    const int TILE = 16;
    __shared__ float sA[TILE][TILE], sB[TILE][TILE];
    int row = blockIdx.y * TILE + threadIdx.y;
    int col = blockIdx.x * TILE + threadIdx.x;
    float sum = 0.0f;
    for (int t = 0; t < N/TILE; t++) {
        sA[threadIdx.y][threadIdx.x] = A[row * N + t * TILE + threadIdx.x];
        sB[threadIdx.y][threadIdx.x] = B[(t * TILE + threadIdx.y) * N + col];
        __syncthreads();
        #pragma unroll
        for (int k = 0; k < TILE; k++) sum += sA[threadIdx.y][k] * sB[k][threadIdx.x];
        __syncthreads();
    }
    if (row < N && col < N) C[row * N + col] = sum;
}
```

## Streams and Concurrency

CUDA streams enable overlapping kernel execution, memory transfers, and CPU work.

```cpp
// Create and destroy streams
cudaStream_t stream;
cudaStreamCreate(&stream);
cudaStreamDestroy(stream);
cudaStream_t priority_stream;
int lowPri, highPri;
cudaDeviceGetStreamPriorityRange(&lowPri, &highPri);
cudaStreamCreateWithPriority(&priority_stream, cudaStreamNonBlocking, highPri);

// Async operations in streams (all return immediately to CPU)
cudaMemcpyAsync(dst, src, bytes, kind, stream);
kernel<<<grid, block, 0, stream>>>(args);
cudaMemsetAsync(ptr, value, bytes, stream);

// Synchronization
cudaStreamSynchronize(stream);   // wait for one stream
cudaDeviceSynchronize();         // wait for ALL streams on this device

// Events — for timing and inter-stream synchronization
cudaEvent_t start, stop;
cudaEventCreate(&start);
cudaEventCreate(&stop);
cudaEventRecord(start, stream);
kernel<<<grid, block, 0, stream>>>(data, n);
cudaEventRecord(stop, stream);
cudaEventSynchronize(stop);
float ms;
cudaEventElapsedTime(&ms, start, stop);
printf("Kernel: %.3f ms\n", ms);
cudaEventDestroy(start); cudaEventDestroy(stop);

// Inter-stream dependency: stream2 waits for stream1's event
cudaEvent_t event;
cudaEventCreate(&event);
cudaEventRecord(event, stream1);
cudaStreamWaitEvent(stream2, event, 0);  // stream2 blocks until event
cudaEventDestroy(event);

// Pipeline: overlap H2D copy with computation
void pipeline(float *h_A, float *h_B, float *h_C, int n) {
    const int CHUNKS = 4;
    int chunk = n / CHUNKS;
    cudaStream_t streams[CHUNKS];
    float *d_A[CHUNKS], *d_B[CHUNKS], *d_C[CHUNKS];
    for (int i = 0; i < CHUNKS; i++) {
        cudaStreamCreate(&streams[i]);
        cudaMalloc(&d_A[i], chunk * sizeof(float));
        cudaMalloc(&d_B[i], chunk * sizeof(float));
        cudaMalloc(&d_C[i], chunk * sizeof(float));
    }
    for (int i = 0; i < CHUNKS; i++) {
        int offset = i * chunk;
        cudaMemcpyAsync(d_A[i], h_A + offset, chunk * sizeof(float), cudaMemcpyH2D, streams[i]);
        cudaMemcpyAsync(d_B[i], h_B + offset, chunk * sizeof(float), cudaMemcpyH2D, streams[i]);
        add_kernel<<<(chunk+255)/256, 256, 0, streams[i]>>>(d_A[i], d_B[i], d_C[i], chunk);
        cudaMemcpyAsync(h_C + offset, d_C[i], chunk * sizeof(float), cudaMemcpyD2H, streams[i]);
    }
    cudaDeviceSynchronize();
}
```

## CUDA Graphs

CUDA Graphs capture a sequence of operations (kernels, copies) as a graph and replay it with minimal CPU overhead. Ideal for repeated workloads (training loops, game physics, inference).

```cpp
// Method 1: Stream capture
cudaGraph_t graph;
cudaGraphExec_t graphExec;
cudaStreamBeginCapture(stream, cudaStreamCaptureModeGlobal);
cudaMemcpyAsync(d_data, h_data, bytes, cudaMemcpyH2D, stream);
kernelA<<<grid, block, 0, stream>>>(d_data, n);
kernelB<<<grid, block, 0, stream>>>(d_data, n);
cudaMemcpyAsync(h_result, d_data, bytes, cudaMemcpyD2H, stream);
cudaStreamEndCapture(stream, &graph);
cudaGraphInstantiate(&graphExec, graph, NULL, NULL, 0);

// Replay many times with minimal overhead
for (int i = 0; i < 1000; i++) {
    cudaGraphLaunch(graphExec, stream);
    cudaStreamSynchronize(stream);
}
cudaGraphExecDestroy(graphExec);
cudaGraphDestroy(graph);
```

## Cooperative Groups

Cooperative Groups allow synchronization across thread groups more flexibly than __syncthreads().

```cpp
#include <cooperative_groups.h>
namespace cg = cooperative_groups;

__global__ void cg_kernel(float *data, int n) {
    // Thread block group
    cg::thread_block block = cg::this_thread_block();
    block.sync();  // same as __syncthreads()

    // Warp group (32 threads)
    cg::thread_block_tile<32> warp = cg::tiled_partition<32>(block);
    float val = data[block.thread_rank()];
    // Warp-level reduce
    for (int i = warp.size() / 2; i > 0; i >>= 1)
        val += warp.shfl_down(val, i);

    // Tile of 4 threads
    cg::thread_block_tile<4> tile4 = cg::tiled_partition<4>(block);
    tile4.sync();

    // Grid-wide sync (requires cooperative launch)
    cg::grid_group grid = cg::this_grid();
    grid.sync();  // all blocks synchronize
}

// Cooperative kernel launch (for grid-wide sync)
void *args[] = {&data, &n};
cudaLaunchCooperativeKernel((void*)cg_kernel, grid, block, args);
```

## Dynamic Parallelism

Kernels can launch child kernels from the GPU without returning to the CPU.

```cpp
// Compile with: nvcc -rdc=true -lcudadevrt
__global__ void child_kernel(float *data, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid < n) data[tid] *= 2.0f;
}

__global__ void parent_kernel(float *data, int n) {
    // Parent decides how to launch child based on data
    int child_n = n / gridDim.x;
    int offset   = blockIdx.x * child_n;
    child_kernel<<<(child_n + 255)/256, 256>>>(data + offset, child_n);
    cudaDeviceSynchronize();  // wait for children in this block
}
```

## Tensor Cores (Volta+)

Tensor Cores perform 4×4 matrix multiply-accumulate in a single clock cycle — 8× faster than CUDA cores for FP16.
Used automatically by cuBLAS for large matrices. Also accessible via WMMA API.

```cpp
#include <mma.h>
using namespace nvcuda::wmma;

__global__ void wmma_kernel(half *A, half *B, float *C, int M, int N, int K) {
    // Each warp computes a 16×16 matrix tile
    fragment<matrix_a, 16, 16, 16, half, row_major> a_frag;
    fragment<matrix_b, 16, 16, 16, half, col_major> b_frag;
    fragment<accumulator, 16, 16, 16, float>         c_frag;

    fill_fragment(c_frag, 0.0f);

    int warp_row = (blockIdx.y * blockDim.y + threadIdx.y) / 32 * 16;
    int warp_col =  blockIdx.x * 16;

    for (int k = 0; k < K; k += 16) {
        load_matrix_sync(a_frag, A + warp_row * K + k, K);
        load_matrix_sync(b_frag, B + k * N + warp_col, N);
        mma_sync(c_frag, a_frag, b_frag, c_frag);
    }
    store_matrix_sync(C + warp_row * N + warp_col, c_frag, N, mem_row_major);
}
// In practice, use cuBLAS or cutlass — they handle all edge cases optimally
```

## Error Handling

```cpp
// Always check CUDA API calls
#define CUDA_CHECK(call) do {                                           \
    cudaError_t err = (call);                                           \
    if (err != cudaSuccess) {                                           \
        fprintf(stderr, "CUDA error %s:%d '%s'\n",                     \
                __FILE__, __LINE__, cudaGetErrorString(err));           \
        exit(EXIT_FAILURE);                                             \
    }                                                                   \
} while(0)

// Check after kernel launch
kernel<<<grid, block>>>(data, n);
CUDA_CHECK(cudaGetLastError());
CUDA_CHECK(cudaDeviceSynchronize());

// Query device properties
cudaDeviceProp prop;
CUDA_CHECK(cudaGetDeviceProperties(&prop, 0));
printf("GPU: %s | CC: %d.%d | SMs: %d | VRAM: %.1f GB\n",
    prop.name, prop.major, prop.minor,
    prop.multiProcessorCount, prop.totalGlobalMem / 1e9);
printf("Max threads/block: %d | Shared mem/block: %zu KB\n",
    prop.maxThreadsPerBlock, prop.sharedMemPerBlock / 1024);
printf("L2 cache: %d MB | Memory bandwidth: %.0f GB/s\n",
    prop.l2CacheSize / (1<<20),
    2.0 * prop.memoryClockRate * (prop.memoryBusWidth / 8) / 1e6);

// Occupancy helper
int block_size, min_grid;
CUDA_CHECK(cudaOccupancyMaxPotentialBlockSize(&min_grid, &block_size, my_kernel, 0, 0));
printf("Optimal block size: %d, min grid: %d\n", block_size, min_grid);

// Multi-GPU
int n_gpus;
cudaGetDeviceCount(&n_gpus);
for (int i = 0; i < n_gpus; i++) {
    cudaSetDevice(i);
    // allocate, launch, etc. on GPU i
}
```

## cuBLAS — Optimized Linear Algebra

```cpp
#include <cublas_v2.h>

cublasHandle_t handle;
cublasCreate(&handle);
cublasSetStream(handle, stream);  // associate with a stream

float alpha = 1.0f, beta = 0.0f;

// SGEMM: C = alpha * A * B + beta * C  (single-precision)
// cuBLAS is column-major! Trick: compute B*A in row-major = (A^T * B^T)^T = C
cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N,
    N, M, K,          // dimensions of C: N×M, inner dim K
    &alpha,
    d_B, N,           // B: N×K (cuBLAS col-major = row-major transposed)
    d_A, K,           // A: K×M
    &beta,
    d_C, N);          // C: N×M

// DGEMM for double precision
cublasDgemm(handle, ...);

// HGEMM for half precision (uses Tensor Cores automatically!)
cublasHgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N, N, M, K, &alpha_h, d_B_h, N, d_A_h, K, &beta_h, d_C_h, N);

// Batched GEMM — many small matrix multiplications
cublasGemmBatchedEx(handle, CUBLAS_OP_N, CUBLAS_OP_N, m, n, k,
    &alpha, A_array, CUDA_R_32F, lda, B_array, CUDA_R_32F, ldb,
    &beta,  C_array, CUDA_R_32F, ldc, batch_count,
    CUBLAS_COMPUTE_32F, CUBLAS_GEMM_DEFAULT_TENSOR_OP);

// Other routines
cublasSaxpy(handle, n, &alpha, d_x, 1, d_y, 1);      // y = alpha*x + y
float dot;
cublasSdot(handle, n, d_x, 1, d_y, 1, &dot);          // dot product
float nrm;
cublasSnrm2(handle, n, d_x, 1, &nrm);                 // L2 norm
int idx;
cublasIsamax(handle, n, d_x, 1, &idx);                // index of max absolute

cublasDestroy(handle);
```

## cuFFT — Fast Fourier Transform

```cpp
#include <cufft.h>

// 1D complex-to-complex FFT
int N = 1024;
cufftComplex *d_signal;
cudaMalloc(&d_signal, N * sizeof(cufftComplex));
cufftHandle plan;
cufftPlan1d(&plan, N, CUFFT_C2C, 1);
cufftExecC2C(plan, d_signal, d_signal, CUFFT_FORWARD);
cufftExecC2C(plan, d_signal, d_signal, CUFFT_INVERSE);
// Normalize: divide by N after inverse FFT
cufftDestroy(plan);

// 2D real-to-complex (for image processing)
int rows = 1024, cols = 1024;
cufftReal    *d_input;
cufftComplex *d_output;
cudaMalloc(&d_input,  rows * cols * sizeof(cufftReal));
cudaMalloc(&d_output, rows * (cols/2+1) * sizeof(cufftComplex));  // R2C size
cufftHandle plan2d;
cufftPlan2d(&plan2d, rows, cols, CUFFT_R2C);
cufftExecR2C(plan2d, d_input, d_output);
cufftDestroy(plan2d);

// Batched 1D FFT (many signals at once)
cufftHandle batch_plan;
int n[1] = {N};
cufftPlanMany(&batch_plan, 1, n,
    NULL, 1, N,   // inembed, istride, idist
    NULL, 1, N,   // onembed, ostride, odist
    CUFFT_C2C, batch_size);
cufftExecC2C(batch_plan, d_batch_in, d_batch_out, CUFFT_FORWARD);
cufftDestroy(batch_plan);
```

## cuDNN — Deep Learning Primitives

```cpp
#include <cudnn.h>

cudnnHandle_t cudnn;
cudnnCreate(&cudnn);

// Tensor descriptor: [N, C, H, W] in NCHW format
cudnnTensorDescriptor_t input_desc;
cudnnCreateTensorDescriptor(&input_desc);
cudnnSetTensor4dDescriptor(input_desc, CUDNN_TENSOR_NCHW, CUDNN_DATA_FLOAT,
    batch_size, channels, height, width);  // N, C, H, W

// 2D Convolution
cudnnFilterDescriptor_t filter_desc;
cudnnCreateFilterDescriptor(&filter_desc);
cudnnSetFilter4dDescriptor(filter_desc, CUDNN_DATA_FLOAT, CUDNN_TENSOR_NCHW,
    out_channels, in_channels, kernel_h, kernel_w);

cudnnConvolutionDescriptor_t conv_desc;
cudnnCreateConvolutionDescriptor(&conv_desc);
cudnnSetConvolution2dDescriptor(conv_desc,
    pad_h, pad_w,       // zero-padding
    stride_h, stride_w, // strides
    dilation_h, dilation_w,
    CUDNN_CROSS_CORRELATION, CUDNN_DATA_FLOAT);

// Enable Tensor Core math
cudnnSetConvolutionMathType(conv_desc, CUDNN_TENSOR_OP_MATH);

// Find best algorithm
cudnnConvolutionFwdAlgo_t algo;
cudnnGetConvolutionForwardAlgorithm(cudnn, input_desc, filter_desc,
    conv_desc, output_desc, CUDNN_CONVOLUTION_FWD_PREFER_FASTEST, 0, &algo);

// Workspace
size_t workspace_bytes;
cudnnGetConvolutionForwardWorkspaceSize(cudnn, input_desc, filter_desc,
    conv_desc, output_desc, algo, &workspace_bytes);
void *d_workspace;
cudaMalloc(&d_workspace, workspace_bytes);

float alpha = 1.0f, beta = 0.0f;
cudnnConvolutionForward(cudnn, &alpha,
    input_desc, d_input, filter_desc, d_filter,
    conv_desc, algo, d_workspace, workspace_bytes,
    &beta, output_desc, d_output);

// Activation (ReLU, sigmoid, tanh)
cudnnActivationDescriptor_t act_desc;
cudnnCreateActivationDescriptor(&act_desc);
cudnnSetActivationDescriptor(act_desc, CUDNN_ACTIVATION_RELU, CUDNN_NOT_PROPAGATE_NAN, 0.0);
cudnnActivationForward(cudnn, act_desc, &alpha, output_desc, d_output, &beta, output_desc, d_output);

// Batch Normalization
cudnnBatchNormalizationForwardTraining(cudnn, CUDNN_BATCHNORM_SPATIAL,
    &alpha, &beta, input_desc, d_input, input_desc, d_output,
    bn_desc, d_scale, d_bias, 0.9, d_running_mean, d_running_var,
    1e-5, d_save_mean, d_save_inv_var);

// Pooling (Max, Average)
cudnnPoolingDescriptor_t pool_desc;
cudnnCreatePoolingDescriptor(&pool_desc);
cudnnSetPooling2dDescriptor(pool_desc, CUDNN_POOLING_MAX, CUDNN_NOT_PROPAGATE_NAN,
    2, 2, 0, 0, 2, 2);  // window 2x2, pad 0, stride 2
cudnnPoolingForward(cudnn, pool_desc, &alpha, input_desc, d_input, &beta, output_desc, d_output);

cudnnDestroy(cudnn);
```

## Thrust — High-Level GPU Algorithms

```cpp
#include <thrust/device_vector.h>
#include <thrust/host_vector.h>
#include <thrust/sort.h>
#include <thrust/reduce.h>
#include <thrust/transform.h>
#include <thrust/scan.h>
#include <thrust/copy.h>
#include <thrust/functional.h>
#include <thrust/iterator/counting_iterator.h>

// Vectors
thrust::host_vector<float> h_vec(n, 1.0f);
thrust::device_vector<float> d_vec = h_vec;          // implicit H2D
thrust::device_vector<float> d_result(n);

// Sort
thrust::sort(d_vec.begin(), d_vec.end());             // ascending
thrust::sort(d_vec.begin(), d_vec.end(), thrust::greater<float>());  // descending

// Reduce
float sum = thrust::reduce(d_vec.begin(), d_vec.end(), 0.0f, thrust::plus<float>());
float minv = *thrust::min_element(d_vec.begin(), d_vec.end());
float maxv = *thrust::max_element(d_vec.begin(), d_vec.end());

// Transform (element-wise operation)
thrust::transform(d_vec.begin(), d_vec.end(), d_result.begin(), thrust::negate<float>());
// Binary transform
thrust::transform(d_a.begin(), d_a.end(), d_b.begin(), d_result.begin(), thrust::plus<float>());

// Custom functor
struct square { __device__ float operator()(float x) { return x * x; } };
thrust::transform(d_vec.begin(), d_vec.end(), d_result.begin(), square());

// Scan (prefix sum)
thrust::inclusive_scan(d_vec.begin(), d_vec.end(), d_result.begin()); // [1,2,3] → [1,3,6]
thrust::exclusive_scan(d_vec.begin(), d_vec.end(), d_result.begin()); // [1,2,3] → [0,1,3]

// Copy with predicate (filter)
thrust::copy_if(d_vec.begin(), d_vec.end(), d_result.begin(),
    [] __device__ (float x) { return x > 0; });

// Count elements matching predicate
int count = thrust::count_if(d_vec.begin(), d_vec.end(),
    [] __device__ (float x) { return x > 0.5f; });

// Generate sequence
thrust::counting_iterator<int> first(0);
thrust::transform(first, first + n, d_vec.begin(),
    [] __device__ (int i) { return (float)i * 0.1f; });

// Raw pointer from device_vector (for use in kernels)
float *raw = thrust::raw_pointer_cast(d_vec.data());
my_kernel<<<grid, block>>>(raw, n);
```

## cuRAND — Random Number Generation

```cpp
#include <curand.h>

curandGenerator_t gen;
curandCreateGenerator(&gen, CURAND_RNG_PSEUDO_XORWOW);   // fast, good quality
// Also: CURAND_RNG_PSEUDO_MRG32K3A, CURAND_RNG_QUASI_SOBOL32
curandSetPseudoRandomGeneratorSeed(gen, 42ULL);

float *d_random;
cudaMalloc(&d_random, n * sizeof(float));

curandGenerateUniform(gen, d_random, n);        // [0, 1)
curandGenerateUniformDouble(gen, d_dbl, n);
curandGenerateNormal(gen, d_random, n, 0.0f, 1.0f);   // mean=0, std=1
curandGenerateNormalDouble(gen, d_dbl, n, 0.0, 1.0);
curandGenerateLogNormal(gen, d_random, n, 0.0f, 1.0f);

unsigned int *d_uint;
cudaMalloc(&d_uint, n * sizeof(unsigned int));
curandGenerate(gen, d_uint, n);               // raw uint32
curandGeneratePoisson(gen, d_uint, n, 4.0);  // Poisson λ=4

// Device API (inside kernels — no host setup needed)
#include <curand_kernel.h>
__global__ void generate_kernel(float *out, int n, unsigned long long seed) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    curandState state;
    curand_init(seed, tid, 0, &state);  // initialize state per thread
    if (tid < n)
        out[tid] = curand_uniform(&state);   // or curand_normal, curand_log_normal
}

curandDestroyGenerator(gen);
```

## Python CUDA — CuPy, Numba, PyCUDA

```python
# ── CuPy ────────────────────────────────────────────────────────────────────
import cupy as cp

# Drop-in NumPy replacement on GPU
a = cp.array([1, 2, 3, 4, 5], dtype=cp.float32)
b = cp.random.randn(1000, 1000, dtype=cp.float32)

# All NumPy operations work
c = cp.dot(b, b.T)
d = cp.fft.fft(a)
e = cp.sum(b, axis=0)
f = cp.linalg.norm(b)

# Custom CUDA kernel in Python
add_kernel = cp.RawKernel(r'''
extern "C" __global__ void add(float *a, float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}
''', 'add')
n = 1024
a_gpu = cp.ones(n, dtype=cp.float32)
b_gpu = cp.ones(n, dtype=cp.float32)
c_gpu = cp.zeros(n, dtype=cp.float32)
add_kernel((n//256,), (256,), (a_gpu, b_gpu, c_gpu, n))

# Move data between NumPy and CuPy
import numpy as np
h_array = np.array([1, 2, 3])
d_array = cp.asarray(h_array)      # CPU → GPU
h_back  = cp.asnumpy(d_array)      # GPU → CPU
h_back2 = d_array.get()            # alternative

# Stream support
stream = cp.cuda.Stream()
with stream:
    result = cp.dot(a, b)

# ── Numba CUDA ──────────────────────────────────────────────────────────────
from numba import cuda
import numpy as np

@cuda.jit
def add_kernel(a, b, c):
    i = cuda.grid(1)                # equivalent to blockIdx.x * blockDim.x + threadIdx.x
    if i < a.size:
        c[i] = a[i] + b[i]

n = 1024
a = np.ones(n, dtype=np.float32)
b = np.ones(n, dtype=np.float32)
c = np.zeros(n, dtype=np.float32)

threads_per_block = 256
blocks = (n + threads_per_block - 1) // threads_per_block
add_kernel[blocks, threads_per_block](a, b, c)   # auto transfers to/from GPU

# With explicit device arrays (faster — avoid implicit copies)
d_a = cuda.to_device(a)
d_b = cuda.to_device(b)
d_c = cuda.device_array(n, dtype=np.float32)
add_kernel[blocks, threads_per_block](d_a, d_b, d_c)
result = d_c.copy_to_host()

# Shared memory in Numba
@cuda.jit
def matmul(A, B, C):
    TILE = 16
    sA = cuda.shared.array((TILE, TILE), dtype=float32)
    sB = cuda.shared.array((TILE, TILE), dtype=float32)
    tx, ty = cuda.threadIdx.x, cuda.threadIdx.y
    row = cuda.blockIdx.y * TILE + ty
    col = cuda.blockIdx.x * TILE + tx
    tmp = 0.0
    for t in range(A.shape[1] // TILE):
        sA[ty, tx] = A[row, t * TILE + tx]
        sB[ty, tx] = B[t * TILE + ty, col]
        cuda.syncthreads()
        for k in range(TILE): tmp += sA[ty, k] * sB[k, tx]
        cuda.syncthreads()
    C[row, col] = tmp
```

## Profiling and Performance Analysis

Tools:
- Nsight Systems (nsys): system-level profiler. Shows CPU + GPU timeline, streams, memory transfers.
- Nsight Compute (ncu): kernel-level profiler. Detailed metrics — occupancy, memory throughput, stall reasons, tensor core utilization.
- nvprof: legacy profiler (deprecated in CUDA 11+).
- CUDA Visual Profiler (nvvp): GUI wrapper for nvprof.

```bash
# Profile with Nsight Systems
nsys profile --trace=cuda,nvtx ./my_program

# Profile with Nsight Compute (detailed kernel metrics)
ncu --set full ./my_program
ncu --metrics sm__throughput.avg.pct_of_peak_sustained_elapsed,\
              l1tex__t_bytes.sum.per_second ./my_program

# Quick timing in code (use events, not CPU timers)
cudaEvent_t t0, t1;
cudaEventCreate(&t0); cudaEventCreate(&t1);
cudaEventRecord(t0);
kernel<<<grid, block>>>(data);
cudaEventRecord(t1);
cudaEventSynchronize(t1);
float ms; cudaEventElapsedTime(&ms, t0, t1);
printf("%.3f ms | %.1f GB/s\n", ms,
       (bytes_accessed / 1e9) / (ms / 1000));
```

Key metrics to optimize:
- Achieved occupancy: higher is usually better, but not always.
- Memory throughput: compare to peak bandwidth (e.g., A100 has 2 TB/s HBM2e).
- SM efficiency: % of time SMs are active.
- Warp efficiency: % of active threads (divergence reduces this).
- L2 cache hit rate: high rate = less DRAM traffic.
- Tensor core utilization: for matmul workloads, should be high.

## Complete Example — Image Convolution

```cpp
#include <cuda_runtime.h>
#include <stdio.h>

#define CHANNELS 3
#define KERNEL_SIZE 3
#define TILE_W 16
#define TILE_H 16

__constant__ float c_kernel[KERNEL_SIZE][KERNEL_SIZE];

__global__ void convolution_2d(
    unsigned char *input, unsigned char *output,
    int width, int height)
{
    __shared__ float tile[TILE_H + KERNEL_SIZE - 1][TILE_W + KERNEL_SIZE - 1][CHANNELS];

    int tx = threadIdx.x, ty = threadIdx.y;
    int col = blockIdx.x * TILE_W + tx;
    int row = blockIdx.y * TILE_H + ty;
    int half = KERNEL_SIZE / 2;

    // Load into shared memory (with halo)
    for (int c = 0; c < CHANNELS; c++) {
        int in_row = row - half, in_col = col - half;
        if (in_row >= 0 && in_row < height && in_col >= 0 && in_col < width)
            tile[ty][tx][c] = input[(in_row * width + in_col) * CHANNELS + c];
        else
            tile[ty][tx][c] = 0.0f;
    }
    __syncthreads();

    if (tx < TILE_W && ty < TILE_H && col < width && row < height) {
        for (int c = 0; c < CHANNELS; c++) {
            float sum = 0.0f;
            for (int ky = 0; ky < KERNEL_SIZE; ky++)
                for (int kx = 0; kx < KERNEL_SIZE; kx++)
                    sum += tile[ty + ky][tx + kx][c] * c_kernel[ky][kx];
            output[(row * width + col) * CHANNELS + c] =
                (unsigned char)fminf(fmaxf(sum, 0.0f), 255.0f);
        }
    }
}

int main() {
    int W = 1920, H = 1080;
    size_t img_bytes = W * H * CHANNELS;

    unsigned char *h_in  = (unsigned char*)malloc(img_bytes);
    unsigned char *h_out = (unsigned char*)malloc(img_bytes);

    // Gaussian blur kernel
    float h_kernel[3][3] = {{1,2,1},{2,4,2},{1,2,1}};
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            h_kernel[i][j] /= 16.0f;
    cudaMemcpyToSymbol(c_kernel, h_kernel, sizeof(h_kernel));

    unsigned char *d_in, *d_out;
    cudaMalloc(&d_in,  img_bytes);
    cudaMalloc(&d_out, img_bytes);
    cudaMemcpy(d_in, h_in, img_bytes, cudaMemcpyHostToDevice);

    dim3 block(TILE_W + KERNEL_SIZE - 1, TILE_H + KERNEL_SIZE - 1);
    dim3 grid((W + TILE_W - 1) / TILE_W, (H + TILE_H - 1) / TILE_H);

    cudaEvent_t t0, t1;
    cudaEventCreate(&t0); cudaEventCreate(&t1);
    cudaEventRecord(t0);
    convolution_2d<<<grid, block>>>(d_in, d_out, W, H);
    cudaEventRecord(t1);
    cudaEventSynchronize(t1);
    float ms; cudaEventElapsedTime(&ms, t0, t1);
    printf("Convolution: %.3f ms (%.1f GB/s)\n", ms,
           2.0 * img_bytes / 1e9 / (ms / 1000));

    cudaMemcpy(h_out, d_out, img_bytes, cudaMemcpyDeviceToHost);
    cudaFree(d_in); cudaFree(d_out);
    free(h_in); free(h_out);
    return 0;
}
```

## Performance Checklist

Memory:
- Use shared memory to reduce global memory accesses.
- Ensure coalesced global memory access (stride-1 per warp).
- Use __ldg() for read-only global data (L1 texture cache path).
- Avoid L1/shared bank conflicts — pad arrays by +1.
- Prefer pinned memory for transfers. Use async transfers + streams.
- Prefetch unified memory with cudaMemPrefetchAsync.

Computation:
- Avoid branch divergence within warps.
- Use float over double unless precision required (2× faster).
- Use fast math: --use_fast_math compile flag or individual __expf, __sinf.
- Use FMA: a*b+c → __fmaf_rn(a,b,c).
- Unroll short loops with #pragma unroll.
- Use vectorized loads: float4, int4.

Occupancy and concurrency:
- Tune block size (powers of 2, 128–256 typical). Use cudaOccupancyMaxPotentialBlockSize.
- Reduce register usage with --maxrregcount or __launch_bounds__.
- Overlap computation and memory transfers using multiple streams.
- Use CUDA Graphs to reduce CPU launch overhead in repeated workloads.

Libraries:
- Use cuBLAS for GEMM — always faster than hand-written kernels.
- Use cuDNN for convolutions, activations, normalization in DL.
- Use cuFFT for FFT.
- Use Thrust for reductions, sorts, scans on GPU.
- Use CUTLASS for custom GEMM with Tensor Cores.
