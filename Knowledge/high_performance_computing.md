High-Performance Computing Complete Reference
CHAPTER 1: GETTING STARTED WITH HIGH-PERFORMANCE COMPUTING
Remarks
High-Performance Computing (HPC) focuses on solving computationally intensive problems using parallel processing. Key paradigms: shared memory (OpenMP, pthreads), distributed memory (MPI), GPU acceleration (CUDA, OpenCL), vectorization (SIMD, AVX). Applications: scientific simulations, machine learning, financial modeling, weather forecasting, molecular dynamics, computational fluid dynamics.
Tools: GCC/Clang (compilers), OpenMP (shared memory), MPI (OpenMPI, MPICH), CUDA Toolkit (NVIDIA GPUs), Intel oneAPI, Valgrind (profiling), perf (Linux profiling), Nsight (GPU profiling).
Hello HPC
# hello_hpc.py
"""
First HPC program: parallel matrix multiplication comparison.
"""
import numpy as np
import time
from multiprocessing import Pool, cpu_count

def matmul_sequential(A, B):
    """Sequential matrix multiplication."""
    n = A.shape[0]
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i, j] += A[i, k] * B[k, j]
    return C

def matmul_numpy(A, B):
    """NumPy optimized (uses BLAS)."""
    return A @ B

def compute_row(args):
    """Compute one row of result matrix."""
    i, A, B = args
    n = A.shape[0]
    row = np.zeros(n)
    for j in range(n):
        for k in range(n):
            row[j] += A[i, k] * B[k, j]
    return row

def matmul_parallel(A, B, num_processes=None):
    """Parallel matrix multiplication using multiprocessing."""
    if num_processes is None:
        num_processes = cpu_count()
    
    n = A.shape[0]
    args = [(i, A, B) for i in range(n)]
    
    with Pool(num_processes) as pool:
        results = pool.map(compute_row, args)
    
    return np.array(results)

# Benchmark
n = 500
A = np.random.rand(n, n)
B = np.random.rand(n, n)

print(f"Matrix size: {n}x{n}")
print(f"CPU cores: {cpu_count()}")

# Sequential
start = time.time()
C_seq = matmul_sequential(A, B)
t_seq = time.time() - start
print(f"Sequential: {t_seq:.3f}s")

# NumPy (BLAS)
start = time.time()
C_np = matmul_numpy(A, B)
t_np = time.time() - start
print(f"NumPy (BLAS): {t_np:.3f}s (speedup: {t_seq/t_np:.1f}x)")

# Parallel
start = time.time()
C_par = matmul_parallel(A, B)
t_par = time.time() - start
print(f"Parallel: {t_par:.3f}s (speedup: {t_seq/t_par:.1f}x)")

# Verify correctness
print(f"Results match: {np.allclose(C_seq, C_np) and np.allclose(C_seq, C_par)}")

HPC Concepts
# Performance metrics:
# - FLOPS: Floating Point Operations Per Second
# - Speedup: S = T_seq / T_parallel
# - Efficiency: E = S / P (P = number of processors)
# - Scalability: how well performance scales with problem size/processes

# Amdahl's Law:
# S_max = 1 / (f + (1-f)/P)
# where f = fraction of sequential code
# Example: 10% sequential, 100 processors → S_max = 1/(0.1 + 0.9/100) = 9.17x

# Gustafson's Law:
# S = P - f*(P-1)
# Accounts for increased problem size with more processors

# Parallel overhead:
# - Thread/process creation
# - Synchronization (locks, barriers)
# - Communication (message passing)
# - Load imbalance

def amdahl_speedup(fractional, num_processors):
    """Calculate Amdahl's law speedup."""
    return 1.0 / (fractional + (1 - fractional) / num_processors)

# Example: impact of serial fraction
print("\nAmdahl's Law Speedup:")
for f in [0.01, 0.05, 0.10, 0.25]:
    for p in [4, 16, 64, 256]:
        s = amdahl_speedup(f, p)
        print(f"  f={f:.2f}, P={p:3d} → S={s:.2f}x")

CHAPTER 2: OPENMP (SHARED MEMORY PARALLELISM)
OpenMP Basics
// openmp_basics.c
#include <stdio.h>
#include <omp.h>
#include <math.h>

int main() {
    // Get number of threads
    int num_threads = omp_get_max_threads();
    printf("Max threads: %d\n", num_threads);
    
    // Parallel region
    #pragma omp parallel
    {
        int thread_id = omp_get_thread_num();
        printf("Hello from thread %d of %d\n", 
               thread_id, omp_get_num_threads());
    }
    
    // Parallel for loop
    int n = 1000000;
    double sum = 0.0;
    
    #pragma omp parallel for reduction(+:sum)
    for (int i = 0; i < n; i++) {
        sum += sin(i * 0.001);
    }
    
    printf("Sum: %.6f\n", sum);
    
    // Nested parallelism
    #pragma omp parallel num_threads(4)
    {
        #pragma omp parallel num_threads(2)
        {
            printf("Nested: outer=%d, inner=%d\n",
                   omp_get_ancestor_thread_num(0),
                   omp_get_thread_num());
        }
    }
    
    return 0;
}

// Compile: gcc -fopenmp openmp_basics.c -o openmp_basics -lm
// Run: OMP_NUM_THREADS=4 ./openmp_basics

OpenMP Worksharing Constructs
// openmp_worksharing.c
#include <stdio.h>
#include <omp.h>

void demonstrate_worksharing() {
    int n = 100;
    double a[100], b[100], c[100];
    
    // Initialize arrays
    for (int i = 0; i < n; i++) {
        a[i] = i;
        b[i] = i * 2;
    }
    
    // 1. Parallel for with different schedules
    printf("=== Schedule comparison ===\n");
    
    // Static schedule (default): divide iterations evenly
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
    
    // Dynamic schedule: assign chunks on demand (better for load imbalance)
    #pragma omp parallel for schedule(dynamic, 10)
    for (int i = 0; i < n; i++) {
        c[i] = a[i] * b[i];
    }
    
    // Guided schedule: decreasing chunk sizes
    #pragma omp parallel for schedule(guided, 5)
    for (int i = 0; i < n; i++) {
        c[i] = a[i] - b[i];
    }
    
    // 2. Sections (different tasks in parallel)
    #pragma omp parallel sections
    {
        #pragma omp section
        {
            printf("Section 1: Computing sum\n");
            double sum = 0;
            for (int i = 0; i < n; i++) sum += a[i];
        }
        
        #pragma omp section
        {
            printf("Section 2: Computing product\n");
            double prod = 1;
            for (int i = 0; i < 10; i++) prod *= (i + 1);
        }
        
        #pragma omp section
        {
            printf("Section 3: Finding max\n");
            double max_val = a[0];
            for (int i = 1; i < n; i++) {
                if (a[i] > max_val) max_val = a[i];
            }
        }
    }
    
    // 3. Single and master constructs
    #pragma omp parallel
    {
        #pragma omp single
        {
            printf("Only one thread executes this\n");
        }
        
        #pragma omp master
        {
            printf("Only master thread (thread 0) executes this\n");
        }
        
        #pragma omp barrier  // Synchronize all threads
        printf("All threads continue after barrier\n");
    }
    
    // 4. Tasking (irregular parallelism)
    #pragma omp parallel
    {
        #pragma omp single
        {
            for (int i = 0; i < 10; i++) {
                #pragma omp task
                {
                    int tid = omp_get_thread_num();
                    printf("Task %d executed by thread %d\n", i, tid);
                }
            }
        }
    }
}

int main() {
    demonstrate_worksharing();
    return 0;
}

OpenMP Data Sharing and Synchronization
// openmp_sync.c
#include <stdio.h>
#include <omp.h>

void demonstrate_sync() {
    int n = 1000;
    double data[1000];
    
    // 1. Data sharing attributes
    int shared_var = 0;
    double private_var;
    
    #pragma omp parallel shared(shared_var) private(private_var)
    {
        // shared_var: same memory location for all threads
        // private_var: each thread has its own copy
        
        int tid = omp_get_thread_num();
        private_var = tid * 1.5;  // Each thread has different value
        
        #pragma omp atomic
        shared_var++;  // Atomic update (thread-safe)
    }
    
    printf("Shared var: %d (should be %d)\n", shared_var, omp_get_max_threads());
    
    // 2. Reduction operations
    double sum = 0.0;
    double product = 1.0;
    int max_val = 0;
    
    #pragma omp parallel for reduction(+:sum) reduction(*:product) reduction(max:max_val)
    for (int i = 0; i < n; i++) {
        data[i] = i + 1;
        sum += data[i];
        product *= (i < 10) ? data[i] : 1.0;  // Avoid overflow
        if (data[i] > max_val) max_val = data[i];
    }
    
    printf("Sum: %.0f, Product (first 10): %.0f, Max: %d\n", 
           sum, product, max_val);
    
    // 3. Critical sections
    int counter = 0;
    
    #pragma omp parallel for
    for (int i = 0; i < 100; i++) {
        #pragma omp critical
        {
            counter++;  // Only one thread at a time
        }
    }
    
    printf("Counter: %d\n", counter);
    
    // 4. Locks (more flexible than critical)
    omp_lock_t lock;
    omp_init_lock(&lock);
    
    int locked_counter = 0;
    
    #pragma omp parallel for
    for (int i = 0; i < 100; i++) {
        omp_set_lock(&lock);
        locked_counter++;
        omp_unset_lock(&lock);
    }
    
    printf("Locked counter: %d\n", locked_counter);
    omp_destroy_lock(&lock);
    
    // 5. Ordered construct (maintain iteration order)
    #pragma omp parallel for ordered
    for (int i = 0; i < 5; i++) {
        #pragma omp ordered
        {
            printf("Iteration %d (ordered)\n", i);
        }
    }
}

int main() {
    demonstrate_sync();
    return 0;
}

OpenMP Memory Model and Performance
// openmp_performance.c
#include <stdio.h>
#include <omp.h>
#include <time.h>

// Matrix multiplication with OpenMP
void matmul_openmp(double *A, double *B, double *C, int n) {
    #pragma omp parallel for collapse(2) schedule(static)
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0.0;
            for (int k = 0; k < n; k++) {
                sum += A[i * n + k] * B[k * n + j];
            }
            C[i * n + j] = sum;
        }
    }
}

// Optimized with cache-friendly access pattern
void matmul_openmp_optimized(double *A, double *B, double *C, int n) {
    // Initialize C to zero
    #pragma omp parallel for
    for (int i = 0; i < n * n; i++) {
        C[i] = 0.0;
    }
    
    // Reorder loops for better cache usage (i-k-j order)
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < n; i++) {
        for (int k = 0; k < n; k++) {
            double a_ik = A[i * n + k];
            #pragma omp simd
            for (int j = 0; j < n; j++) {
                C[i * n + j] += a_ik * B[k * n + j];
            }
        }
    }
}

int main() {
    int n = 1000;
    double *A = malloc(n * n * sizeof(double));
    double *B = malloc(n * n * sizeof(double));
    double *C1 = malloc(n * n * sizeof(double));
    double *C2 = malloc(n * n * sizeof(double));
    
    // Initialize
    for (int i = 0; i < n * n; i++) {
        A[i] = (double)(i % 100) / 100.0;
        B[i] = (double)((i + 50) % 100) / 100.0;
    }
    
    // Benchmark standard version
    clock_t start = clock();
    matmul_openmp(A, B, C1, n);
    double t1 = (double)(clock() - start) / CLOCKS_PER_SEC;
    printf("Standard OpenMP: %.3f s\n", t1);
    
    // Benchmark optimized version
    start = clock();
    matmul_openmp_optimized(A, B, C2, n);
    double t2 = (double)(clock() - start) / CLOCKS_PER_SEC;
    printf("Optimized OpenMP: %.3f s (speedup: %.2fx)\n", t2, t1 / t2);
    
    // Verify results match
    double max_diff = 0.0;
    for (int i = 0; i < n * n; i++) {
        double diff = fabs(C1[i] - C2[i]);
        if (diff > max_diff) max_diff = diff;
    }
    printf("Max difference: %e\n", max_diff);
    
    free(A); free(B); free(C1); free(C2);
    return 0;
}

// Compile: gcc -fopenmp -O3 openmp_performance.c -o openmp_perf -lm

CHAPTER 3: MPI (DISTRIBUTED MEMORY PARALLELISM)
MPI Basics
// mpi_basics.c
#include <stdio.h>
#include <mpi.h>

int main(int argc, char** argv) {
    // Initialize MPI
    MPI_Init(&argc, &argv);
    
    // Get rank (process ID) and size (total processes)
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    printf("Hello from process %d of %d\n", rank, size);
    
    // Finalize MPI
    MPI_Finalize();
    return 0;
}

// Compile: mpicc mpi_basics.c -o mpi_basics
// Run: mpirun -np 4 ./mpi_basics

MPI Point-to-Point Communication
// mpi_point2point.c
#include <stdio.h>
#include <mpi.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    if (size < 2) {
        if (rank == 0) printf("Need at least 2 processes\n");
        MPI_Finalize();
        return 1;
    }
    
    // 1. Send and Receive (blocking)
    if (rank == 0) {
        int data = 42;
        MPI_Send(&data, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
        printf("Process 0 sent: %d\n", data);
    } else if (rank == 1) {
        int received;
        MPI_Recv(&received, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Process 1 received: %d\n", received);
    }
    
    // 2. Sendrecv (simultaneous send and receive)
    int send_data = rank * 10;
    int recv_data = -1;
    int left = (rank - 1 + size) % size;
    int right = (rank + 1) % size;
    
    MPI_Sendrecv(&send_data, 1, MPI_INT, right, 1,
                 &recv_data, 1, MPI_INT, left, 1,
                 MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    
    printf("Process %d: sent %d to %d, received %d from %d\n",
           rank, send_data, right, recv_data, left);
    
    // 3. Non-blocking communication
    if (rank == 0) {
        int buffer[3] = {10, 20, 30};
        MPI_Request request;
        MPI_Isend(buffer, 3, MPI_INT, 1, 2, MPI_COMM_WORLD, &request);
        printf("Process 0 initiated non-blocking send\n");
        
        // Do other work while message is being sent
        MPI_Wait(&request, MPI_STATUS_IGNORE);
        printf("Process 0 send completed\n");
    } else if (rank == 1) {
        int buffer[3];
        MPI_Request request;
        MPI_Irecv(buffer, 3, MPI_INT, 0, 2, MPI_COMM_WORLD, &request);
        printf("Process 1 initiated non-blocking receive\n");
        
        MPI_Wait(&request, MPI_STATUS_IGNORE);
        printf("Process 1 received: %d %d %d\n", buffer[0], buffer[1], buffer[2]);
    }
    
    MPI_Finalize();
    return 0;
}

MPI Collective Operations
// mpi_collective.c
#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    // 1. Broadcast (one-to-all)
    int data = 0;
    if (rank == 0) data = 100;
    MPI_Bcast(&data, 1, MPI_INT, 0, MPI_COMM_WORLD);
    printf("Process %d after broadcast: %d\n", rank, data);
    
    // 2. Scatter (one-to-all, different data)
    int *send_data = NULL;
    int recv_data;
    
    if (rank == 0) {
        send_data = malloc(size * sizeof(int));
        for (int i = 0; i < size; i++) {
            send_data[i] = i * 10;
        }
    }
    
    MPI_Scatter(send_data, 1, MPI_INT, &recv_data, 1, MPI_INT, 0, MPI_COMM_WORLD);
    printf("Process %d scattered data: %d\n", rank, recv_data);
    
    // 3. Gather (all-to-one)
    int gather_data = rank * 5;
    int *gathered = NULL;
    
    if (rank == 0) {
        gathered = malloc(size * sizeof(int));
    }
    
    MPI_Gather(&gather_data, 1, MPI_INT, gathered, 1, MPI_INT, 0, MPI_COMM_WORLD);
    
    if (rank == 0) {
        printf("Process 0 gathered: ");
        for (int i = 0; i < size; i++) {
            printf("%d ", gathered[i]);
        }
        printf("\n");
        free(gathered);
        free(send_data);
    }
    
    // 4. Reduce (all-to-one with operation)
    double local_value = rank + 1.0;
    double global_sum;
    
    MPI_Reduce(&local_value, &global_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
    
    if (rank == 0) {
        printf("Sum of all values: %.1f\n", global_sum);
    }
    
    // 5. Allreduce (all-to-all with operation)
    double all_sum;
    MPI_Allreduce(&local_value, &all_sum, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    printf("Process %d allreduce sum: %.1f\n", rank, all_sum);
    
    // 6. Alltoall (every process sends to every other)
    int send_buf[4] = {rank * 10 + 0, rank * 10 + 1, rank * 10 + 2, rank * 10 + 3};
    int recv_buf[4];
    
    MPI_Alltoall(send_buf, 1, MPI_INT, recv_buf, 1, MPI_INT, MPI_COMM_WORLD);
    
    printf("Process %d alltoall received: ", rank);
    for (int i = 0; i < size && i < 4; i++) {
        printf("%d ", recv_buf[i]);
    }
    printf("\n");
    
    MPI_Finalize();
    return 0;
}

MPI Parallel Matrix Multiplication
// mpi_matmul.c
#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>

void matmul_serial(double *A, double *B, double *C, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0.0;
            for (int k = 0; k < n; k++) {
                sum += A[i * n + k] * B[k * n + j];
            }
            C[i * n + j] = sum;
        }
    }
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    int n = 1000;  // Matrix dimension
    
    // Allocate matrices
    double *A = NULL, *B = NULL, *C = NULL;
    double *local_A = NULL, *local_C = NULL;
    
    int rows_per_proc = n / size;
    int remainder = n % size;
    
    // Process 0 initializes matrices
    if (rank == 0) {
        A = malloc(n * n * sizeof(double));
        B = malloc(n * n * sizeof(double));
        C = malloc(n * n * sizeof(double));
        
        srand(42);
        for (int i = 0; i < n * n; i++) {
            A[i] = (double)rand() / RAND_MAX;
            B[i] = (double)rand() / RAND_MAX;
        }
    }
    
    // Allocate local matrices
    local_A = malloc(rows_per_proc * n * sizeof(double));
    local_C = malloc(rows_per_proc * n * sizeof(double));
    
    // Broadcast B to all processes
    if (rank == 0) {
        MPI_Bcast(B, n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    } else {
        B = malloc(n * n * sizeof(double));
        MPI_Bcast(B, n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    }
    
    // Scatter A to all processes
    MPI_Scatter(A, rows_per_proc * n, MPI_DOUBLE,
                local_A, rows_per_proc * n, MPI_DOUBLE,
                0, MPI_COMM_WORLD);
    
    // Each process computes its portion of C
    clock_t start = clock();
    
    for (int i = 0; i < rows_per_proc; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0.0;
            for (int k = 0; k < n; k++) {
                sum += local_A[i * n + k] * B[k * n + j];
            }
            local_C[i * n + j] = sum;
        }
    }
    
    clock_t end = clock();
    double local_time = (double)(end - start) / CLOCKS_PER_SEC;
    
    // Gather results
    if (rank == 0) {
        MPI_Gather(local_C, rows_per_proc * n, MPI_DOUBLE,
                   C, rows_per_proc * n, MPI_DOUBLE,
                   0, MPI_COMM_WORLD);
        
        printf("Parallel computation time: %.3f s\n", local_time);
        printf("Speedup: %.2fx\n", local_time / local_time);  // Placeholder
    } else {
        MPI_Gather(local_C, rows_per_proc * n, MPI_DOUBLE,
                   NULL, 0, MPI_DOUBLE,
                   0, MPI_COMM_WORLD);
    }
    
    // Cleanup
    free(local_A);
    free(local_C);
    free(B);
    if (rank == 0) {
        free(A);
        free(C);
    }
    
    MPI_Finalize();
    return 0;
}

// Compile: mpicc -O3 mpi_matmul.c -o mpi_matmul
// Run: mpirun -np 4 ./mpi_matmul

CHAPTER 4: CUDA (GPU PROGRAMMING)
CUDA Basics
// cuda_basics.cu
#include <stdio.h>
#include <cuda_runtime.h>

// CUDA kernel (runs on GPU)
__global__ void vector_add(float *A, float *B, float *C, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        C[idx] = A[idx] + B[idx];
    }
}

// Error checking macro
#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            printf("CUDA error at %s:%d: %s\n", __FILE__, __LINE__, \
                   cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while (0)

int main() {
    int n = 1000000;
    size_t size = n * sizeof(float);
    
    // Allocate host memory
    float *h_A = (float*)malloc(size);
    float *h_B = (float*)malloc(size);
    float *h_C = (float*)malloc(size);
    
    // Initialize data
    for (int i = 0; i < n; i++) {
        h_A[i] = i;
        h_B[i] = i * 2;
    }
    
    // Allocate device memory
    float *d_A, *d_B, *d_C;
    CUDA_CHECK(cudaMalloc(&d_A, size));
    CUDA_CHECK(cudaMalloc(&d_B, size));
    CUDA_CHECK(cudaMalloc(&d_C, size));
    
    // Copy data from host to device
    CUDA_CHECK(cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice));
    
    // Define execution configuration
    int threads_per_block = 256;
    int blocks_per_grid = (n + threads_per_block - 1) / threads_per_block;
    
    // Launch kernel
    vector_add<<<blocks_per_grid, threads_per_block>>>(d_A, d_B, d_C, n);
    
    // Wait for GPU to finish
    CUDA_CHECK(cudaDeviceSynchronize());
    
    // Copy result back to host
    CUDA_CHECK(cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost));
    
    // Verify result
    for (int i = 0; i < 10; i++) {
        printf("C[%d] = %.1f (expected %.1f)\n", i, h_C[i], h_A[i] + h_B[i]);
    }
    
    // Free memory
    CUDA_CHECK(cudaFree(d_A));
    CUDA_CHECK(cudaFree(d_B));
    CUDA_CHECK(cudaFree(d_C));
    free(h_A);
    free(h_B);
    free(h_C);
    
    return 0;
}

// Compile: nvcc cuda_basics.cu -o cuda_basics
// Run: ./cuda_basics

CUDA Memory Hierarchy
// cuda_memory.cu
#include <stdio.h>
#include <cuda_runtime.h>

// Kernel demonstrating different memory types
__global__ void memory_demo(float *global_mem, float *output, int n) {
    // Shared memory (shared within block)
    __shared__ float shared_data[256];
    
    int tid = threadIdx.x;
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    // Load data into shared memory
    if (idx < n) {
        shared_data[tid] = global_mem[idx];
    }
    
    // Synchronize threads in block
    __syncthreads();
    
    // Perform computation using shared memory
    if (idx < n) {
        float sum = 0.0f;
        for (int i = 0; i < blockDim.x && i < n; i++) {
            sum += shared_data[i];
        }
        output[idx] = sum;
    }
    
    // Registers (private to each thread)
    float reg_var = shared_data[tid] * 2.0f;
    
    // Constant memory (read-only, cached, shared across all blocks)
    // Declared outside kernel: __constant__ float const_data[100];
    
    // Texture memory (optimized for 2D/3D spatial locality)
    // Declared outside kernel: texture<float, 2> tex_ref;
}

// Reduction using shared memory
__global__ void reduce_shared(float *input, float *output, int n) {
    __shared__ float sdata[256];
    
    int tid = threadIdx.x;
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    // Load data into shared memory
    sdata[tid] = (idx < n) ? input[idx] : 0.0f;
    __syncthreads();
    
    // Parallel reduction in shared memory
    for (int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (tid < s) {
            sdata[tid] += sdata[tid + s];
        }
        __syncthreads();
    }
    
    // Write result for this block
    if (tid == 0) {
        output[blockIdx.x] = sdata[0];
    }
}

int main() {
    int n = 1000000;
    size_t size = n * sizeof(float);
    
    float *h_input = (float*)malloc(size);
    float *h_output = (float*)malloc(size);
    
    for (int i = 0; i < n; i++) {
        h_input[i] = 1.0f;
    }
    
    float *d_input, *d_output;
    cudaMalloc(&d_input, size);
    cudaMalloc(&d_output, size);
    
    cudaMemcpy(d_input, h_input, size, cudaMemcpyHostToDevice);
    
    int threads = 256;
    int blocks = (n + threads - 1) / threads;
    
    reduce_shared<<<blocks, threads>>>(d_input, d_output, n);
    
    cudaMemcpy(h_output, d_output, blocks * sizeof(float), cudaMemcpyDeviceToHost);
    
    // Final reduction on CPU
    float total = 0.0f;
    for (int i = 0; i < blocks; i++) {
        total += h_output[i];
    }
    
    printf("Sum: %.1f (expected %.1f)\n", total, (float)n);
    
    cudaFree(d_input);
    cudaFree(d_output);
    free(h_input);
    free(h_output);
    
    return 0;
}

CUDA Matrix Operations
// cuda_matmul.cu
#include <stdio.h>
#include <cuda_runtime.h>

#define TILE_SIZE 16

// Tiled matrix multiplication (optimized for shared memory)
__global__ void matmul_tiled(float *A, float *B, float *C, int n) {
    __shared__ float tile_A[TILE_SIZE][TILE_SIZE];
    __shared__ float tile_B[TILE_SIZE][TILE_SIZE];
    
    int row = blockIdx.y * TILE_SIZE + threadIdx.y;
    int col = blockIdx.x * TILE_SIZE + threadIdx.x;
    
    float sum = 0.0f;
    
    // Loop over tiles
    for (int t = 0; t < (n + TILE_SIZE - 1) / TILE_SIZE; t++) {
        // Load tiles into shared memory
        if (row < n && t * TILE_SIZE + threadIdx.x < n) {
            tile_A[threadIdx.y][threadIdx.x] = A[row * n + t * TILE_SIZE + threadIdx.x];
        } else {
            tile_A[threadIdx.y][threadIdx.x] = 0.0f;
        }
        
        if (col < n && t * TILE_SIZE + threadIdx.y < n) {
            tile_B[threadIdx.y][threadIdx.x] = B[(t * TILE_SIZE + threadIdx.y) * n + col];
        } else {
            tile_B[threadIdx.y][threadIdx.x] = 0.0f;
        }
        
        __syncthreads();
        
        // Compute partial sum
        for (int k = 0; k < TILE_SIZE; k++) {
            sum += tile_A[threadIdx.y][k] * tile_B[k][threadIdx.x];
        }
        
        __syncthreads();
    }
    
    // Write result
    if (row < n && col < n) {
        C[row * n + col] = sum;
    }
}

// Simple matrix multiplication (no tiling)
__global__ void matmul_simple(float *A, float *B, float *C, int n) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (row < n && col < n) {
        float sum = 0.0f;
        for (int k = 0; k < n; k++) {
            sum += A[row * n + k] * B[k * n + col];
        }
        C[row * n + col] = sum;
    }
}

int main() {
    int n = 1024;
    size_t size = n * n * sizeof(float);
    
    float *h_A = (float*)malloc(size);
    float *h_B = (float*)malloc(size);
    float *h_C = (float*)malloc(size);
    
    // Initialize
    for (int i = 0; i < n * n; i++) {
        h_A[i] = (float)(i % 100) / 100.0f;
        h_B[i] = (float)((i + 50) % 100) / 100.0f;
    }
    
    float *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, size);
    cudaMalloc(&d_B, size);
    cudaMalloc(&d_C, size);
    
    cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice);
    
    // Benchmark simple version
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    
    dim3 block(16, 16);
    dim3 grid((n + 15) / 16, (n + 15) / 16);
    
    cudaEventRecord(start);
    matmul_simple<<<grid, block>>>(d_A, d_B, d_C, n);
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    
    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);
    printf("Simple matmul: %.3f ms\n", milliseconds);
    
    // Benchmark tiled version
    cudaEventRecord(start);
    matmul_tiled<<<grid, block>>>(d_A, d_B, d_C, n);
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    
    cudaEventElapsedTime(&milliseconds, start, stop);
    printf("Tiled matmul: %.3f ms\n", milliseconds);
    
    cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost);
    
    // Verify
    printf("C[0][0] = %.4f\n", h_C[0]);
    
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    free(h_A);
    free(h_B);
    free(h_C);
    
    cudaEventDestroy(start);
    cudaEventDestroy(stop);
    
    return 0;
}

// Compile: nvcc -O3 cuda_matmul.cu -o cuda_matmul

CHAPTER 5: SIMD AND VECTORIZATION
SIMD Basics (AVX)
// simd_basics.c
#include <stdio.h>
#include <immintrin.h>  // AVX headers
#include <time.h>

// Scalar version
void vector_add_scalar(float *A, float *B, float *C, int n) {
    for (int i = 0; i < n; i++) {
        C[i] = A[i] + B[i];
    }
}

// SIMD version (AVX - 8 floats at once)
void vector_add_avx(float *A, float *B, float *C, int n) {
    int i;
    for (i = 0; i <= n - 8; i += 8) {
        __m256 a = _mm256_loadu_ps(&A[i]);
        __m256 b = _mm256_loadu_ps(&B[i]);
        __m256 c = _mm256_add_ps(a, b);
        _mm256_storeu_ps(&C[i], c);
    }
    
    // Handle remaining elements
    for (; i < n; i++) {
        C[i] = A[i] + B[i];
    }
}

// Dot product with SIMD
float dot_product_scalar(float *A, float *B, int n) {
    float sum = 0.0f;
    for (int i = 0; i < n; i++) {
        sum += A[i] * B[i];
    }
    return sum;
}

float dot_product_avx(float *A, float *B, int n) {
    __m256 sum_vec = _mm256_setzero_ps();
    
    int i;
    for (i = 0; i <= n - 8; i += 8) {
        __m256 a = _mm256_loadu_ps(&A[i]);
        __m256 b = _mm256_loadu_ps(&B[i]);
        __m256 prod = _mm256_mul_ps(a, b);
        sum_vec = _mm256_add_ps(sum_vec, prod);
    }
    
    // Horizontal sum
    float temp[8];
    _mm256_storeu_ps(temp, sum_vec);
    float sum = 0.0f;
    for (int j = 0; j < 8; j++) {
        sum += temp[j];
    }
    
    // Handle remaining elements
    for (; i < n; i++) {
        sum += A[i] * B[i];
    }
    
    return sum;
}

int main() {
    int n = 10000000;
    float *A = (float*)malloc(n * sizeof(float));
    float *B = (float*)malloc(n * sizeof(float));
    float *C1 = (float*)malloc(n * sizeof(float));
    float *C2 = (float*)malloc(n * sizeof(float));
    
    for (int i = 0; i < n; i++) {
        A[i] = (float)i;
        B[i] = (float)i * 2;
    }
    
    // Benchmark scalar
    clock_t start = clock();
    vector_add_scalar(A, B, C1, n);
    double t1 = (double)(clock() - start) / CLOCKS_PER_SEC;
    printf("Scalar: %.3f s\n", t1);
    
    // Benchmark AVX
    start = clock();
    vector_add_avx(A, B, C2, n);
    double t2 = (double)(clock() - start) / CLOCKS_PER_SEC;
    printf("AVX: %.3f s (speedup: %.2fx)\n", t2, t1 / t2);
    
    // Dot product
    start = clock();
    float dot1 = dot_product_scalar(A, B, n);
    t1 = (double)(clock() - start) / CLOCKS_PER_SEC;
    printf("Scalar dot product: %.1f (%.3f s)\n", dot1, t1);
    
    start = clock();
    float dot2 = dot_product_avx(A, B, n);
    t2 = (double)(clock() - start) / CLOCKS_PER_SEC;
    printf("AVX dot product: %.1f (%.3f s, speedup: %.2fx)\n", dot2, t2, t1 / t2);
    
    free(A); free(B); free(C1); free(C2);
    return 0;
}

// Compile: gcc -O3 -mavx2 simd_basics.c -o simd_basics

Auto-Vectorization
// auto_vectorize.c
#include <stdio.h>
#include <time.h>

// Compiler can auto-vectorize simple loops
void scale_array(float *A, float scalar, int n) {
    for (int i = 0; i < n; i++) {
        A[i] *= scalar;
    }
}

// More complex - may not auto-vectorize
void complex_operation(float *A, float *B, float *C, int n) {
    for (int i = 0; i < n; i++) {
        C[i] = A[i] * B[i] + A[i] - B[i];
    }
}

// With pragmas to help compiler
void scale_array_pragma(float *A, float scalar, int n) {
    #pragma omp simd
    for (int i = 0; i < n; i++) {
        A[i] *= scalar;
    }
}

// Aligned data helps vectorization
void scale_aligned(float *__restrict__ A, float scalar, int n) {
    #pragma omp simd aligned(A:32)
    for (int i = 0; i < n; i++) {
        A[i] *= scalar;
    }
}

int main() {
    int n = 10000000;
    float *A = (float*)aligned_alloc(32, n * sizeof(float));
    float *B = (float*)aligned_alloc(32, n * sizeof(float));
    float *C = (float*)aligned_alloc(32, n * sizeof(float));
    
    for (int i = 0; i < n; i++) {
        A[i] = (float)i;
        B[i] = (float)i * 2;
    }
    
    clock_t start = clock();
    scale_array(A, 2.0f, n);
    double t1 = (double)(clock() - start) / CLOCKS_PER_SEC;
    printf("Scale: %.3f s\n", t1);
    
    start = clock();
    complex_operation(A, B, C, n);
    t1 = (double)(clock() - start) / CLOCKS_PER_SEC;
    printf("Complex: %.3f s\n", t1);
    
    start = clock();
    scale_array_pragma(A, 2.0f, n);
    t1 = (double)(clock() - start) / CLOCKS_PER_SEC;
    printf("Scale pragma: %.3f s\n", t1);
    
    start = clock();
    scale_aligned(A, 2.0f, n);
    t1 = (double)(clock() - start) / CLOCKS_PER_SEC;
    printf("Scale aligned: %.3f s\n", t1);
    
    free(A); free(B); free(C);
    return 0;
}

// Compile with vectorization reports:
// gcc -O3 -fopt-info-vec-optimized auto_vectorize.c -o auto_vec
// gcc -O3 -mavx2 -fopt-info-vec-missed auto_vectorize.c -o auto_vec

CHAPTER 6: MEMORY OPTIMIZATION
Cache-Friendly Code
// cache_optimization.c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 2000

// Row-major order (C-style) - cache friendly
void matrix_add_row_major(double *A, double *B, double *C, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            C[i * n + j] = A[i * n + j] + B[i * n + j];
        }
    }
}

// Column-major order - cache unfriendly in C
void matrix_add_col_major(double *A, double *B, double *C, int n) {
    for (int j = 0; j < n; j++) {
        for (int i = 0; i < n; i++) {
            C[i * n + j] = A[i * n + j] + B[i * n + j];
        }
    }
}

// Loop interchange for better cache usage
void matrix_multiply_naive(double *A, double *B, double *C, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0.0;
            for (int k = 0; k < n; k++) {
                sum += A[i * n + k] * B[k * n + j];  // B access is cache-unfriendly
            }
            C[i * n + j] = sum;
        }
    }
}

// Optimized: reorder loops for cache-friendly access
void matrix_multiply_optimized(double *A, double *B, double *C, int n) {
    // Initialize C to zero
    for (int i = 0; i < n * n; i++) {
        C[i] = 0.0;
    }
    
    // i-k-j order: B[k][j] accessed sequentially
    for (int i = 0; i < n; i++) {
        for (int k = 0; k < n; k++) {
            double a_ik = A[i * n + k];
            for (int j = 0; j < n; j++) {
                C[i * n + j] += a_ik * B[k * n + j];
            }
        }
    }
}

// Blocking for better cache utilization
void matrix_multiply_blocked(double *A, double *B, double *C, int n, int block_size) {
    for (int i = 0; i < n * n; i++) {
        C[i] = 0.0;
    }
    
    for (int ii = 0; ii < n; ii += block_size) {
        for (int kk = 0; kk < n; kk += block_size) {
            for (int jj = 0; jj < n; jj += block_size) {
                for (int i = ii; i < ii + block_size && i < n; i++) {
                    for (int k = kk; k < kk + block_size && k < n; k++) {
                        double a_ik = A[i * n + k];
                        for (int j = jj; j < jj + block_size && j < n; j++) {
                            C[i * n + j] += a_ik * B[k * n + j];
                        }
                    }
                }
            }
        }
    }
}

int main() {
    double *A = malloc(N * N * sizeof(double));
    double *B = malloc(N * N * sizeof(double));
    double *C1 = malloc(N * N * sizeof(double));
    double *C2 = malloc(N * N * sizeof(double));
    double *C3 = malloc(N * N * sizeof(double));
    
    for (int i = 0; i < N * N; i++) {
        A[i] = (double)(i % 100) / 100.0;
        B[i] = (double)((i + 50) % 100) / 100.0;
    }
    
    clock_t start;
    
    start = clock();
    matrix_add_row_major(A, B, C1, N);
    printf("Row-major: %.3f s\n", (double)(clock() - start) / CLOCKS_PER_SEC);
    
    start = clock();
    matrix_add_col_major(A, B, C2, N);
    printf("Col-major: %.3f s\n", (double)(clock() - start) / CLOCKS_PER_SEC);
    
    start = clock();
    matrix_multiply_naive(A, B, C1, N);
    printf("Naive matmul: %.3f s\n", (double)(clock() - start) / CLOCKS_PER_SEC);
    
    start = clock();
    matrix_multiply_optimized(A, B, C2, N);
    printf("Optimized matmul: %.3f s\n", (double)(clock() - start) / CLOCKS_PER_SEC);
    
    start = clock();
    matrix_multiply_blocked(A, B, C3, N, 64);
    printf("Blocked matmul: %.3f s\n", (double)(clock() - start) / CLOCKS_PER_SEC);
    
    free(A); free(B); free(C1); free(C2); free(C3);
    return 0;
}

// Compile: gcc -O3 cache_optimization.c -o cache_opt

Memory Alignment and Prefetching
// memory_alignment.c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Aligned allocation
void* aligned_malloc(size_t size, size_t alignment) {
    void *ptr;
    if (aligned_alloc(alignment, size, &ptr) != 0) {
        return NULL;
    }
    return ptr;
}

// Software prefetching
void array_sum_prefetch(float *A, int n) {
    float sum = 0.0f;
    
    for (int i = 0; i < n; i++) {
        // Prefetch data 4 iterations ahead
        if (i + 64 < n) {
            __builtin_prefetch(&A[i + 64], 0, 3);
        }
        sum += A[i];
    }
    
    printf("Sum: %.1f\n", sum);
}

// Cache line optimization
#define CACHE_LINE_SIZE 64

typedef struct {
    int data[CACHE_LINE_SIZE / sizeof(int)];
} cache_line_t;

void cache_line_access(cache_line_t *array, int n) {
    // Access entire cache line at once
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < CACHE_LINE_SIZE / sizeof(int); j++) {
            array[i].data[j] = i + j;
        }
    }
}

int main() {
    int n = 10000000;
    
    // Unaligned allocation
    float *A_unaligned = (float*)malloc(n * sizeof(float));
    
    // Aligned allocation (32-byte aligned for AVX)
    float *A_aligned = (float*)aligned_alloc(32, n * sizeof(float));
    
    for (int i = 0; i < n; i++) {
        A_unaligned[i] = (float)i;
        A_aligned[i] = (float)i;
    }
    
    clock_t start;
    
    start = clock();
    array_sum_prefetch(A_unaligned, n);
    printf("Unaligned with prefetch: %.3f s\n", (double)(clock() - start) / CLOCKS_PER_SEC);
    
    start = clock();
    array_sum_prefetch(A_aligned, n);
    printf("Aligned with prefetch: %.3f s\n", (double)(clock() - start) / CLOCKS_PER_SEC);
    
    free(A_unaligned);
    free(A_aligned);
    
    return 0;
}

CHAPTER 7: PARALLEL ALGORITHMS
Parallel Sorting
// parallel_sort.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

// Sequential quicksort
void quicksort_sequential(float *arr, int low, int high) {
    if (low < high) {
        float pivot = arr[high];
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                float temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        
        float temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;
        
        int pi = i + 1;
        quicksort_sequential(arr, low, pi - 1);
        quicksort_sequential(arr, pi + 1, high);
    }
}

// Parallel merge sort
void merge(float *arr, float *temp, int left, int mid, int right) {
    int i = left, j = mid + 1, k = left;
    
    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
        }
    }
    
    while (i <= mid) temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];
    
    for (i = left; i <= right; i++) {
        arr[i] = temp[i];
    }
}

void merge_sort_parallel(float *arr, float *temp, int left, int right) {
    if (left < right) {
        int mid = (left + right) / 2;
        
        #pragma omp task
        merge_sort_parallel(arr, temp, left, mid);
        
        #pragma omp task
        merge_sort_parallel(arr, temp, mid + 1, right);
        
        #pragma omp taskwait
        merge(arr, temp, left, mid, right);
    }
}

void sort_parallel(float *arr, int n) {
    float *temp = (float*)malloc(n * sizeof(float));
    
    #pragma omp parallel
    {
        #pragma omp single
        {
            merge_sort_parallel(arr, temp, 0, n - 1);
        }
    }
    
    free(temp);
}

int main() {
    int n = 1000000;
    float *arr1 = (float*)malloc(n * sizeof(float));
    float *arr2 = (float*)malloc(n * sizeof(float));
    
    srand(42);
    for (int i = 0; i < n; i++) {
        arr1[i] = (float)rand() / RAND_MAX;
        arr2[i] = arr1[i];
    }
    
    clock_t start;
    
    start = clock();
    quicksort_sequential(arr1, 0, n - 1);
    printf("Sequential quicksort: %.3f s\n", (double)(clock() - start) / CLOCKS_PER_SEC);
    
    start = clock();
    sort_parallel(arr2, n);
    printf("Parallel merge sort: %.3f s\n", (double)(clock() - start) / CLOCKS_PER_SEC);
    
    // Verify
    int correct = 1;
    for (int i = 0; i < n - 1; i++) {
        if (arr2[i] > arr2[i + 1]) {
            correct = 0;
            break;
        }
    }
    printf("Sort correct: %s\n", correct ? "Yes" : "No");
    
    free(arr1);
    free(arr2);
    return 0;
}

// Compile: gcc -fopenmp -O3 parallel_sort.c -o parallel_sort

Parallel Reduction
// parallel_reduction.c
#include <stdio.h>
#include <omp.h>
#include <time.h>

// Sequential reduction
float sum_sequential(float *arr, int n) {
    float sum = 0.0f;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum;
}

// OpenMP reduction
float sum_openmp(float *arr, int n) {
    float sum = 0.0f;
    #pragma omp parallel for reduction(+:sum)
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum;
}

// Custom parallel reduction (tree-based)
float sum_tree(float *arr, int n) {
    int num_threads = omp_get_max_threads();
    float *partial_sums = (float*)malloc(num_threads * sizeof(float));
    
    #pragma omp parallel
    {
        int tid = omp_get_thread_num();
        int chunk_size = (n + num_threads - 1) / num_threads;
        int start = tid * chunk_size;
        int end = (start + chunk_size < n) ? start + chunk_size : n;
        
        float local_sum = 0.0f;
        for (int i = start; i < end; i++) {
            local_sum += arr[i];
        }
        partial_sums[tid] = local_sum;
    }
    
    // Final reduction
    float total = 0.0f;
    for (int i = 0; i < num_threads; i++) {
        total += partial_sums[i];
    }
    
    free(partial_sums);
    return total;
}

int main() {
    int n = 100000000;
    float *arr = (float*)malloc(n * sizeof(float));
    
    for (int i = 0; i < n; i++) {
        arr[i] = 1.0f;
    }
    
    clock_t start;
    
    start = clock();
    float sum1 = sum_sequential(arr, n);
    printf("Sequential: %.1f (%.3f s)\n", sum1, (double)(clock() - start) / CLOCKS_PER_SEC);
    
    start = clock();
    float sum2 = sum_openmp(arr, n);
    printf("OpenMP: %.1f (%.3f s)\n", sum2, (double)(clock() - start) / CLOCKS_PER_SEC);
    
    start = clock();
    float sum3 = sum_tree(arr, n);
    printf("Tree: %.1f (%.3f s)\n", sum3, (double)(clock() - start) / CLOCKS_PER_SEC);
    
    free(arr);
    return 0;
}

// Compile: gcc -fopenmp -O3 parallel_reduction.c -o parallel_reduction

CHAPTER 8: PROFILING AND PERFORMANCE ANALYSIS
Linux perf Profiler
# profiling.sh
#!/bin/bash

# Compile with debug info
gcc -g -O3 -fopenmp program.c -o program

# Basic profiling
perf stat ./program

# Detailed statistics
perf stat -e cycles,instructions,cache-references,cache-misses ./program

# Record and analyze
perf record -g ./program
perf report

# Hotspot analysis
perf record -F 99 -g ./program
perf report --stdio

# Cache miss analysis
perf stat -e L1-dcache-load-misses,L1-dcache-loads ./program

# Branch prediction
perf stat -e branch-misses,branch-loads ./program

Valgrind (Cache Profiling)
# valgrind_profiling.sh
#!/bin/bash

# Compile without optimization for better profiling
gcc -g -O0 program.c -o program

# Cache profiling
valgrind --tool=cachegrind ./program
cg_annotate cachegrind.out.<pid>

# Memory profiling
valgrind --tool=massif ./program
ms_print massif.out.<pid>

# Call graph profiling
valgrind --tool=callgrind ./program
callgrind_annotate callgrind.out.<pid>

NVIDIA Nsight (GPU Profiling)
# nsight_profiling.sh
#!/bin/bash

# Compile CUDA program
nvcc -lineinfo program.cu -o program

# Profile with nsight compute
ncu --set full -o profile_report ./program

# View results
ncu --import profile_report.ncu-rep

# Basic profiling
ncu --metrics sm__throughput.avg.pct_of_peak_sustained_elapsed ./program

# Memory analysis
ncu --metrics l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum ./program

# Kernel comparison
ncu --kernel-name regex:'matmul.*' ./program

Performance Counters (C Code)
// perf_counters.c
#include <stdio.h>
#include <time.h>
#include <stdint.h>

// Read CPU cycle counter
static inline uint64_t read_cycles() {
    uint32_t lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}

// Measure function execution
#define MEASURE(func, ...) do { \
    uint64_t start = read_cycles(); \
    func(__VA_ARGS__); \
    uint64_t end = read_cycles(); \
    printf(#func ": %lu cycles\n", end - start); \
} while (0)

void compute_heavy(int n) {
    double sum = 0.0;
    for (int i = 0; i < n; i++) {
        sum += i * 0.5;
    }
}

int main() {
    int n = 10000000;
    
    MEASURE(compute_heavy, n);
    
    // Multiple measurements for accuracy
    uint64_t total = 0;
    int iterations = 100;
    
    for (int i = 0; i < iterations; i++) {
        uint64_t start = read_cycles();
        compute_heavy(n);
        uint64_t end = read_cycles();
        total += (end - start);
    }
    
    printf("Average: %.1f cycles\n", (double)total / iterations);
    
    return 0;
}

// Compile: gcc -O3 perf_counters.c -o perf_counters

CHAPTER 9: DISTRIBUTED COMPUTING PATTERNS
MapReduce Pattern
// mapreduce.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mpi.h>
#include <omp.h>

// Map function: count words in text
void map_words(char *text, int *local_counts, int vocab_size) {
    // Simple word counting (vocabulary size = vocab_size)
    char *token = strtok(text, " \n\t");
    while (token != NULL) {
        int hash = 0;
        for (char *p = token; *p; p++) {
            hash = (hash * 31 + *p) % vocab_size;
        }
        local_counts[hash]++;
        token = strtok(NULL, " \n\t");
    }
}

// Reduce function: sum counts
void reduce_counts(int *local_counts, int *global_counts, int vocab_size) {
    MPI_Reduce(local_counts, global_counts, vocab_size, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    int vocab_size = 1000;
    
    // Each process reads its portion of data
    char text[10000];
    sprintf(text, "word%d word%d word%d word%d", rank, rank + 1, rank + 2, rank + 3);
    
    // Map phase (can be parallelized with OpenMP)
    int *local_counts = (int*)calloc(vocab_size, sizeof(int));
    
    #pragma omp parallel for
    for (int i = 0; i < 100; i++) {
        map_words(text, local_counts, vocab_size);
    }
    
    // Reduce phase
    int *global_counts = NULL;
    if (rank == 0) {
        global_counts = (int*)calloc(vocab_size, sizeof(int));
    }
    
    reduce_counts(local_counts, global_counts, vocab_size);
    
    // Output results
    if (rank == 0) {
        printf("Top words:\n");
        for (int i = 0; i < 10; i++) {
            printf("  Word %d: %d occurrences\n", i, global_counts[i]);
        }
        free(global_counts);
    }
    
    free(local_counts);
    MPI_Finalize();
    return 0;
}

// Compile: mpicc -fopenmp mapreduce.c -o mapreduce
// Run: mpirun -np 4 ./mapreduce

Pipeline Pattern
// pipeline.c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define BUFFER_SIZE 10

typedef struct {
    int buffer[BUFFER_SIZE];
    int count;
    int in;
    int out;
    pthread_mutex_t mutex;
    pthread_cond_t not_full;
    pthread_cond_t not_empty;
} bounded_buffer_t;

void buffer_init(bounded_buffer_t *buf) {
    buf->count = 0;
    buf->in = 0;
    buf->out = 0;
    pthread_mutex_init(&buf->mutex, NULL);
    pthread_cond_init(&buf->not_full, NULL);
    pthread_cond_init(&buf->not_empty, NULL);
}

void buffer_put(bounded_buffer_t *buf, int item) {
    pthread_mutex_lock(&buf->mutex);
    while (buf->count == BUFFER_SIZE) {
        pthread_cond_wait(&buf->not_full, &buf->mutex);
    }
    buf->buffer[buf->in] = item;
    buf->in = (buf->in + 1) % BUFFER_SIZE;
    buf->count++;
    pthread_cond_signal(&buf->not_empty);
    pthread_mutex_unlock(&buf->mutex);
}

int buffer_get(bounded_buffer_t *buf) {
    pthread_mutex_lock(&buf->mutex);
    while (buf->count == 0) {
        pthread_cond_wait(&buf->not_empty, &buf->mutex);
    }
    int item = buf->buffer[buf->out];
    buf->out = (buf->out + 1) % BUFFER_SIZE;
    buf->count--;
    pthread_cond_signal(&buf->not_full);
    pthread_mutex_unlock(&buf->mutex);
    return item;
}

bounded_buffer_t buf1, buf2;

// Stage 1: Generate data
void* stage1(void* arg) {
    for (int i = 0; i < 100; i++) {
        buffer_put(&buf1, i);
        printf("Stage 1: produced %d\n", i);
    }
    return NULL;
}

// Stage 2: Process data
void* stage2(void* arg) {
    for (int i = 0; i < 100; i++) {
        int item = buffer_get(&buf1);
        int processed = item * 2;
        buffer_put(&buf2, processed);
        printf("Stage 2: %d -> %d\n", item, processed);
    }
    return NULL;
}

// Stage 3: Consume data
void* stage3(void* arg) {
    for (int i = 0; i < 100; i++) {
        int item = buffer_get(&buf2);
        printf("Stage 3: consumed %d\n", item);
    }
    return NULL;
}

int main() {
    buffer_init(&buf1);
    buffer_init(&buf2);
    
    pthread_t t1, t2, t3;
    pthread_create(&t1, NULL, stage1, NULL);
    pthread_create(&t2, NULL, stage2, NULL);
    pthread_create(&t3, NULL, stage3, NULL);
    
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);
    
    return 0;
}

// Compile: gcc -pthread pipeline.c -o pipeline

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Modern HPC Frameworks
# Dask (Python parallel computing)
# from dask import delayed
# import dask
# 
# @delayed
# def process_chunk(data):
#     return sum(data)
# 
# chunks = [delayed(process_chunk)(chunk) for chunk in data_chunks]
# total = dask.compute(*chunks)

# Ray (distributed execution)
# import ray
# ray.init()
# 
# @ray.remote
# def process(data):
#     return heavy_computation(data)
# 
# futures = [process.remote(chunk) for chunk in chunks]
# results = ray.get(futures)

# Julia for HPC
# using Distributed
# addprocs(4)
# 
# @distributed (+) for i in 1:1000000
#     heavy_computation(i)
# end

Performance Optimization Checklist
# 1. Algorithm selection
#    - Choose O(n log n) over O(n²) algorithms
#    - Use appropriate data structures
#    - Consider cache-friendly algorithms

# 2. Memory optimization
#    - Minimize memory allocations
#    - Use cache-friendly access patterns
#    - Align data structures
#    - Prefetch data

# 3. Vectorization
#    - Use SIMD instructions (AVX, SSE)
#    - Structure loops for auto-vectorization
#    - Use aligned memory

# 4. Parallelization
#    - Identify independent computations
#    - Minimize synchronization
#    - Balance workload
#    - Consider Amdahl's law

# 5. GPU acceleration
#    - Offload compute-intensive kernels
#    - Minimize host-device transfers
#    - Use shared memory effectively
#    - Optimize thread block size

# 6. Profiling and tuning
#    - Profile before optimizing
#    - Identify bottlenecks
#    - Measure speedup
#    - Iterate

Recommended Reading
# - "Introduction to Parallel Computing" by Grama et al.
# - "CUDA by Example" by Sanders and Kandrot
# - "Using OpenMP" by Chapman, Jost, van der Pas
# - "MPI: The Complete Reference" by Snell et al.
# - "Is Parallel Programming Hard?" by IBM
# - "High Performance Computing" by David Henty

# Online Resources
# - LLVM documentation: https://llvm.org/docs/
# - CUDA Programming Guide: https://docs.nvidia.com/cuda/
# - OpenMP specification: https://www.openmp.org/specifications/
# - MPI Forum: https://www.mpi-forum.org/
# - HPC Wiki: https://hpc-wiki.info/

# End of High-Performance Computing Reference