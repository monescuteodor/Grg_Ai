# OpenCL Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH OPENCL


## Remarks

OpenCL (Open Computing Language) is an open, cross-platform framework for parallel programming on heterogeneous systems (CPUs, GPUs, FPGAs, DSPs). Developed by Khronos Group, it runs on NVIDIA, AMD, Intel, and ARM hardware. More verbose than CUDA but portable across vendors.

Tools: OpenCL runtime (from GPU vendor), ocl-icd-opencl-dev (Linux), clang with OpenCL support, Intel OpenCL SDK, pocl (portable OpenCL).


## Hello World

```c
// hello.c — OpenCL host code
#define CL_TARGET_OPENCL_VERSION 120
#include <CL/cl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char* kernel_src = "                           \n"
"__kernel void hello(__global float* result) {       \n"
"    int gid = get_global_id(0);                     \n"
"    result[gid] = gid * 2.0f;                       \n"
"}                                                   \n";

int main() {
    // Get platform
    cl_platform_id platform;
    clGetPlatformIDs(1, &platform, NULL);

    // Get device (GPU)
    cl_device_id device;
    clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, NULL);

    // Create context and command queue
    cl_context ctx = clCreateContext(NULL, 1, &device, NULL, NULL, NULL);
    cl_command_queue queue = clCreateCommandQueue(ctx, device, 0, NULL);

    // Build program
    cl_program program = clCreateProgramWithSource(ctx, 1, &kernel_src, NULL, NULL);
    clBuildProgram(program, 1, &device, NULL, NULL, NULL);
    cl_kernel kernel = clCreateKernel(program, "hello", NULL);

    // Create buffer
    int n = 16;
    cl_mem buf = clCreateBuffer(ctx, CL_MEM_WRITE_ONLY, n * sizeof(float), NULL, NULL);

    // Set kernel args and run
    clSetKernelArg(kernel, 0, sizeof(cl_mem), &buf);
    size_t global_size = n;
    clEnqueueNDRangeKernel(queue, kernel, 1, NULL, &global_size, NULL, 0, NULL, NULL);

    // Read result
    float result[16];
    clEnqueueReadBuffer(queue, buf, CL_TRUE, 0, n * sizeof(float), result, 0, NULL, NULL);
    for (int i = 0; i < n; i++) printf("%.1f ", result[i]);
    printf("\n");

    // Cleanup
    clReleaseMemObject(buf);
    clReleaseKernel(kernel);
    clReleaseProgram(program);
    clReleaseCommandQueue(queue);
    clReleaseContext(ctx);
    return 0;
}
```

```bash
gcc hello.c -lOpenCL -o hello && ./hello
```


---

# CHAPTER 2: PLATFORM AND DEVICE MANAGEMENT


## OpenCL Setup

```c
#define CL_TARGET_OPENCL_VERSION 120
#include <CL/cl.h>
#include <stdio.h>
#include <string.h>

void query_platforms() {
    cl_uint num_platforms;
    clGetPlatformIDs(0, NULL, &num_platforms);
    printf("Platforms: %u\n", num_platforms);

    cl_platform_id platforms[8];
    clGetPlatformIDs(num_platforms, platforms, NULL);

    for (cl_uint i = 0; i < num_platforms; i++) {
        char name[256], vendor[256], version[256];
        clGetPlatformInfo(platforms[i], CL_PLATFORM_NAME,    256, name,    NULL);
        clGetPlatformInfo(platforms[i], CL_PLATFORM_VENDOR,  256, vendor,  NULL);
        clGetPlatformInfo(platforms[i], CL_PLATFORM_VERSION, 256, version, NULL);
        printf("Platform %u: %s (%s) %s\n", i, name, vendor, version);

        // Get devices
        cl_uint num_devices;
        clGetDeviceIDs(platforms[i], CL_DEVICE_TYPE_ALL, 0, NULL, &num_devices);

        cl_device_id devices[8];
        clGetDeviceIDs(platforms[i], CL_DEVICE_TYPE_ALL, num_devices, devices, NULL);

        for (cl_uint j = 0; j < num_devices; j++) {
            char dev_name[256];
            cl_device_type dev_type;
            cl_ulong global_mem, local_mem;
            cl_uint compute_units, max_freq;
            size_t max_work_group;

            clGetDeviceInfo(devices[j], CL_DEVICE_NAME,       256, dev_name,      NULL);
            clGetDeviceInfo(devices[j], CL_DEVICE_TYPE,       sizeof(cl_device_type), &dev_type, NULL);
            clGetDeviceInfo(devices[j], CL_DEVICE_GLOBAL_MEM_SIZE,    sizeof(cl_ulong), &global_mem, NULL);
            clGetDeviceInfo(devices[j], CL_DEVICE_LOCAL_MEM_SIZE,     sizeof(cl_ulong), &local_mem,  NULL);
            clGetDeviceInfo(devices[j], CL_DEVICE_MAX_COMPUTE_UNITS,  sizeof(cl_uint),  &compute_units, NULL);
            clGetDeviceInfo(devices[j], CL_DEVICE_MAX_CLOCK_FREQUENCY,sizeof(cl_uint),  &max_freq, NULL);
            clGetDeviceInfo(devices[j], CL_DEVICE_MAX_WORK_GROUP_SIZE,sizeof(size_t),   &max_work_group, NULL);

            printf("  Device %u: %s (%s)\n", j, dev_name,
                   dev_type == CL_DEVICE_TYPE_GPU ? "GPU" :
                   dev_type == CL_DEVICE_TYPE_CPU ? "CPU" : "Other");
            printf("    Compute units: %u @ %u MHz\n", compute_units, max_freq);
            printf("    Global mem: %lu MB\n", global_mem >> 20);
            printf("    Local mem: %lu KB\n", local_mem >> 10);
            printf("    Max work group: %zu\n", max_work_group);
        }
    }
}

// Error checking
#define CL_CHECK(err) \
    if (err != CL_SUCCESS) { \
        fprintf(stderr, "OpenCL error %d at %s:%d\n", err, __FILE__, __LINE__); \
        exit(1); \
    }

cl_int err;
cl_context ctx = clCreateContext(NULL, 1, &device, NULL, NULL, &err);
CL_CHECK(err);
```


---

# CHAPTER 3: KERNELS AND WORK ITEMS


## OpenCL Kernel Language

```opencl
// kernels.cl — OpenCL C kernel code

// Simple vector addition
__kernel void vector_add(
    __global const float* a,
    __global const float* b,
    __global float* c,
    int n
) {
    int gid = get_global_id(0);   // global work item ID
    if (gid < n) {
        c[gid] = a[gid] + b[gid];
    }
}

// 2D kernel (matrix operations)
__kernel void matrix_add(
    __global const float* A,
    __global const float* B,
    __global float* C,
    int rows,
    int cols
) {
    int row = get_global_id(1);   // 2D global ID
    int col = get_global_id(0);

    if (row < rows && col < cols) {
        int idx = row * cols + col;
        C[idx] = A[idx] + B[idx];
    }
}

// Work group info
get_global_id(dim)       // global work-item ID in dimension
get_local_id(dim)        // local work-item ID within group
get_group_id(dim)        // work-group ID
get_global_size(dim)     // total global work items
get_local_size(dim)      // work-group size (local)
get_num_groups(dim)      // number of work groups

// Local (shared) memory
__kernel void reduction_sum(
    __global const float* data,
    __global float* result,
    __local float* scratch,   // local memory param
    int n
) {
    int gid = get_global_id(0);
    int lid = get_local_id(0);
    int lsize = get_local_size(0);

    scratch[lid] = (gid < n) ? data[gid] : 0.0f;
    barrier(CLK_LOCAL_MEM_FENCE);   // sync within work group

    for (int stride = lsize / 2; stride > 0; stride >>= 1) {
        if (lid < stride) {
            scratch[lid] += scratch[lid + stride];
        }
        barrier(CLK_LOCAL_MEM_FENCE);
    }

    if (lid == 0) {
        result[get_group_id(0)] = scratch[0];
    }
}

// Address space qualifiers
__global  float* global_ptr;    // global memory (slow, all work items)
__local   float* local_ptr;     // local memory (fast, per work group)
__constant float* const_ptr;    // constant memory (read-only, cached)
__private float  priv_var;      // private (per work item, like registers)

// Built-in math functions
float x = sin(val);
float y = cos(val);
float z = sqrt(val);
float w = pow(base, exp);
float a = fabs(val);
float b = floor(val);
float c = ceil(val);
float d = fmin(x, y);
float e = fmax(x, y);
float f = clamp(val, lo, hi);
float g = mix(a_val, b_val, t);   // linear interpolation
float h = mad(a_val, b_val, c_val);  // multiply-add (fast)
float i = native_sin(val);        // fast but less accurate
float j = half_sqrt(val);         // half-precision

// Vector types (SIMD)
float4 v = (float4)(1.0f, 2.0f, 3.0f, 4.0f);
v.x; v.y; v.z; v.w;
v.xy; v.zw;    // swizzle
v.s0; v.s1; v.s2; v.s3;  // component access

float4 a4 = (float4)(1.0f);    // broadcast
float4 b4 = v * 2.0f;
float dot_result = dot(v, v);
float4 norm = normalize(v);
float len = length(v);
```


---

# CHAPTER 4: MEMORY OBJECTS AND TRANSFERS


## Buffers, Images, and Transfers

```c
// Buffer creation flags
// CL_MEM_READ_ONLY  — device only reads
// CL_MEM_WRITE_ONLY — device only writes
// CL_MEM_READ_WRITE — device reads and writes (default)
// CL_MEM_COPY_HOST_PTR — copy from host pointer
// CL_MEM_USE_HOST_PTR  — use host pointer directly
// CL_MEM_ALLOC_HOST_PTR — allocate pinned memory

// Create buffer with initial data
float h_data[1024];
cl_mem d_buf = clCreateBuffer(ctx,
    CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
    sizeof(h_data), h_data, &err);

// Write to buffer (blocking)
err = clEnqueueWriteBuffer(queue, d_buf, CL_TRUE,
    0, sizeof(h_data), h_data,
    0, NULL, NULL);

// Read from buffer (blocking)
float result[1024];
err = clEnqueueReadBuffer(queue, d_buf, CL_TRUE,
    0, sizeof(result), result,
    0, NULL, NULL);

// Non-blocking with events
cl_event write_done;
clEnqueueWriteBuffer(queue, d_buf, CL_FALSE,
    0, bytes, h_data, 0, NULL, &write_done);
clEnqueueNDRangeKernel(queue, kernel, 1, NULL,
    &global, &local, 1, &write_done, &kernel_done);
clEnqueueReadBuffer(queue, d_result, CL_FALSE,
    0, bytes, h_result, 1, &kernel_done, &read_done);
clWaitForEvents(1, &read_done);
clReleaseEvent(write_done);
clReleaseEvent(kernel_done);
clReleaseEvent(read_done);

// Map / Unmap (zero-copy on shared memory)
float* mapped = (float*)clEnqueueMapBuffer(queue, d_buf,
    CL_TRUE, CL_MAP_WRITE,
    0, bytes, 0, NULL, NULL, &err);
// ... write to mapped ...
clEnqueueUnmapMemObject(queue, d_buf, mapped, 0, NULL, NULL);

// Image objects (2D texture-like)
cl_image_format fmt = { CL_RGBA, CL_FLOAT };
cl_image_desc desc = {
    .image_type = CL_MEM_OBJECT_IMAGE2D,
    .image_width = 640,
    .image_height = 480
};
cl_mem img = clCreateImage(ctx, CL_MEM_READ_ONLY, &fmt, &desc, NULL, &err);

size_t origin[3] = {0, 0, 0};
size_t region[3] = {640, 480, 1};
clEnqueueWriteImage(queue, img, CL_TRUE, origin, region, 0, 0, h_pixels, 0, NULL, NULL);

// Sub-buffers
cl_buffer_region sub_region = { .origin = offset, .size = sub_bytes };
cl_mem sub_buf = clCreateSubBuffer(d_buf, CL_MEM_READ_WRITE,
    CL_BUFFER_CREATE_TYPE_REGION, &sub_region, &err);
```


---

# CHAPTER 5: KERNEL COMPILATION AND EXECUTION


## Program Building and Execution

```c
// Load kernel from file
FILE* f = fopen("kernels.cl", "rb");
fseek(f, 0, SEEK_END);
size_t src_size = ftell(f);
rewind(f);
char* src = (char*)malloc(src_size + 1);
fread(src, 1, src_size, f);
src[src_size] = '\0';
fclose(f);

cl_program program = clCreateProgramWithSource(ctx, 1,
    (const char**)&src, &src_size, &err);
free(src);

// Build with options
const char* options = "-cl-std=CL1.2 -cl-fast-relaxed-math -DWIDTH=16";
err = clBuildProgram(program, 1, &device, options, NULL, NULL);

// Check build errors
if (err != CL_SUCCESS) {
    size_t log_size;
    clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, 0, NULL, &log_size);
    char* log = (char*)malloc(log_size);
    clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, log_size, log, NULL);
    fprintf(stderr, "Build error:\n%s\n", log);
    free(log);
}

// Save/load binary (for faster loading)
size_t binary_size;
clGetProgramInfo(program, CL_PROGRAM_BINARY_SIZES, sizeof(size_t), &binary_size, NULL);
unsigned char* binary = malloc(binary_size);
clGetProgramInfo(program, CL_PROGRAM_BINARIES, sizeof(binary), &binary, NULL);
// ... save binary to file ...

// Create kernel and set arguments
cl_kernel kernel = clCreateKernel(program, "vector_add", &err);

int n = 1024;
clSetKernelArg(kernel, 0, sizeof(cl_mem), &d_a);    // arg 0: __global float* a
clSetKernelArg(kernel, 1, sizeof(cl_mem), &d_b);    // arg 1: __global float* b
clSetKernelArg(kernel, 2, sizeof(cl_mem), &d_c);    // arg 2: __global float* c
clSetKernelArg(kernel, 3, sizeof(int), &n);          // arg 3: int n
clSetKernelArg(kernel, 4, local_size * sizeof(float), NULL);  // local memory

// Enqueue kernel
size_t global_work_size = 1024;
size_t local_work_size  = 64;    // must divide global_work_size
err = clEnqueueNDRangeKernel(queue, kernel,
    1,                    // work dimensions
    NULL,                 // global offset (NULL = 0)
    &global_work_size,    // global work items
    &local_work_size,     // local work items
    0, NULL, NULL);       // events

// Query kernel work group info
size_t preferred_work_group;
clGetKernelWorkGroupInfo(kernel, device,
    CL_KERNEL_PREFERRED_WORK_GROUP_SIZE_MULTIPLE,
    sizeof(size_t), &preferred_work_group, NULL);
printf("Preferred work group multiple: %zu\n", preferred_work_group);

clFinish(queue);     // blocking wait for all queued commands
```


---

# CHAPTER 6: PROFILING AND OPTIMIZATION


## Performance Tuning

```c
// Enable profiling on command queue
cl_command_queue queue = clCreateCommandQueue(ctx, device,
    CL_QUEUE_PROFILING_ENABLE, &err);

// Event-based timing
cl_event kernel_event;
clEnqueueNDRangeKernel(queue, kernel, 1, NULL,
    &global, &local, 0, NULL, &kernel_event);
clFinish(queue);

cl_ulong start, end;
clGetEventProfilingInfo(kernel_event, CL_PROFILING_COMMAND_START,
    sizeof(cl_ulong), &start, NULL);
clGetEventProfilingInfo(kernel_event, CL_PROFILING_COMMAND_END,
    sizeof(cl_ulong), &end, NULL);
double elapsed_ms = (end - start) * 1e-6;
printf("Kernel time: %.3f ms\n", elapsed_ms);

// Bandwidth calculation
double bytes_transferred = 3.0 * n * sizeof(float);  // read a,b; write c
double bandwidth = bytes_transferred / ((end-start) * 1e-9) / 1e9;
printf("Bandwidth: %.1f GB/s\n", bandwidth);

// Optimization strategies:
// 1. Coalesced memory access — adjacent work items access adjacent memory
// 2. Local memory — reduce global memory bandwidth
// 3. Avoid branching — divergence kills performance
// 4. Vector types — use float4, float8, float16 when possible
// 5. Loop unrolling — #pragma unroll N
// 6. Use native_* functions for speed at cost of accuracy
// 7. Proper work group sizing — use CL_KERNEL_PREFERRED_WORK_GROUP_SIZE_MULTIPLE
// 8. Minimize host-device transfers — batch operations

// Example: optimized with vector types
__kernel void vector_add_opt(
    __global const float4* a,
    __global const float4* b,
    __global float4* c,
    int n4    // n/4
) {
    int gid = get_global_id(0);
    if (gid < n4) {
        c[gid] = a[gid] + b[gid];
    }
}

// Launch with n/4 work items
size_t global_opt = n / 4;
clEnqueueNDRangeKernel(queue, kernel_opt, 1, NULL, &global_opt, &local, 0, NULL, NULL);
```


---

# CHAPTER 7: OPENCL FOR IMAGES AND FILTERS


## Image Processing

```opencl
// Image filter kernel (Gaussian blur)
__kernel void gaussian_blur(
    __read_only image2d_t input,
    __write_only image2d_t output,
    __constant float* kernel_weights,
    int kernel_radius
) {
    const sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE |
                               CLK_ADDRESS_CLAMP_TO_EDGE |
                               CLK_FILTER_NEAREST;

    int x = get_global_id(0);
    int y = get_global_id(1);

    float4 sum = 0.0f;
    float weight_sum = 0.0f;

    for (int ky = -kernel_radius; ky <= kernel_radius; ky++) {
        for (int kx = -kernel_radius; kx <= kernel_radius; kx++) {
            float4 pixel = read_imagef(input, sampler, (int2)(x + kx, y + ky));
            float w = kernel_weights[(ky + kernel_radius) * (2*kernel_radius+1)
                                    + (kx + kernel_radius)];
            sum += pixel * w;
            weight_sum += w;
        }
    }

    write_imagef(output, (int2)(x, y), sum / weight_sum);
}

// Edge detection (Sobel)
__kernel void sobel(
    __read_only image2d_t input,
    __write_only image2d_t output
) {
    const sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE |
                               CLK_ADDRESS_CLAMP_TO_EDGE |
                               CLK_FILTER_NEAREST;

    int x = get_global_id(0);
    int y = get_global_id(1);

    float gx = 0.0f, gy = 0.0f;

    // Sobel kernels
    float kx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    float ky[3][3] = {{-1,-2,-1}, { 0, 0, 0}, { 1, 2, 1}};

    for (int dy = -1; dy <= 1; dy++) {
        for (int dx = -1; dx <= 1; dx++) {
            float4 p = read_imagef(input, sampler, (int2)(x+dx, y+dy));
            float gray = dot(p.xyz, (float3)(0.299f, 0.587f, 0.114f));
            gx += gray * kx[dy+1][dx+1];
            gy += gray * ky[dy+1][dx+1];
        }
    }

    float magnitude = clamp(sqrt(gx*gx + gy*gy), 0.0f, 1.0f);
    write_imagef(output, (int2)(x, y), (float4)(magnitude, magnitude, magnitude, 1.0f));
}
```


---

# CHAPTER 8: OPENCL 2.0 AND ADVANCED FEATURES


## Modern OpenCL

```c
// OpenCL 2.0 features

// SVM (Shared Virtual Memory) — zero-copy host-device memory sharing
// CL_DEVICE_SVM_CAPABILITIES must include CL_DEVICE_SVM_FINE_GRAIN_BUFFER

// Coarse-grained SVM buffer
void* svm_ptr = clSVMAlloc(ctx, CL_MEM_READ_WRITE, bytes, 0);
clEnqueueSVMMap(queue, CL_TRUE, CL_MAP_WRITE, svm_ptr, bytes, 0, NULL, NULL);
// ... fill svm_ptr ...
clEnqueueSVMUnmap(queue, svm_ptr, 0, NULL, NULL);
clSetKernelArgSVMPointer(kernel, 0, svm_ptr);
// ... run kernel ...
clSVMFree(ctx, svm_ptr);

// Pipes (producer-consumer)
// __kernel void producer(__write_only pipe float p_out) { write_pipe(p_out, &val); }
// __kernel void consumer(__read_only pipe float p_in)   { read_pipe(p_in, &val);  }
// cl_mem pipe = clCreatePipe(ctx, 0, sizeof(float), 1024, NULL, &err);

// Device-side enqueue (OpenCL 2.0)
// __kernel void parent(__global int* data, queue_t queue) {
//     enqueue_kernel(queue, CLK_ENQUEUE_FLAGS_NO_WAIT,
//                    ndrange_1D(n), ^{ child(data); });
// }

// OpenCL / SPIR-V (OpenCL 2.1)
// Compile to SPIR-V with clang:
// clang -x cl -cl-std=CL2.0 --target=spir64 -emit-llvm kernel.cl -o kernel.bc
// llvm-spirv kernel.bc -o kernel.spv

// Load SPIR-V binary
// cl_program prog = clCreateProgramWithIL(ctx, spirv_data, spirv_size, &err);

// Interoperability with OpenGL
// cl_context ctx = clCreateContextFromType(props, CL_DEVICE_TYPE_GPU, NULL, NULL, &err);
// where props include: CL_GL_CONTEXT_KHR, CL_GLX_DISPLAY_KHR

// Event callback
void CL_CALLBACK event_callback(cl_event e, cl_int exec_status, void* user_data) {
    printf("Event complete, status: %d\n", exec_status);
}
clSetEventCallback(kernel_event, CL_COMPLETE, event_callback, NULL);

// cl.hpp / cl2.hpp (C++ bindings)
// #include <CL/cl2.hpp>
// cl::Platform platform = cl::Platform::getDefault();
// cl::Device device = cl::Device::getDefault();
// cl::Context ctx(device);
// cl::CommandQueue queue(ctx, device);
// cl::Buffer buf(ctx, CL_MEM_READ_WRITE, bytes);
// cl::Kernel k(program, "kernel_name");
// k.setArg(0, buf);
// queue.enqueueNDRangeKernel(k, cl::NullRange, cl::NDRange(n), cl::NDRange(64));
// queue.finish();
```
