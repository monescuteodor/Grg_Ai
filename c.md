# C Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH C


## Remarks

C is a general-purpose, procedural, compiled language. It provides low-level memory access, minimal runtime, and is the foundation for operating systems, embedded systems, and many other languages. C11 is the current standard.

Tools: GCC, Clang, MSVC. Build: make, cmake.


## Hello World

```c
#include <stdio.h>

int main(void) {
    printf("Hello, World!\n");
    return 0;
}
```

```bash
gcc -Wall -Wextra -std=c11 -o hello hello.c
./hello
clang -o hello hello.c
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Fundamental Types

```c
#include <stdio.h>
#include <stdint.h>   // fixed-width integers
#include <stdbool.h>  // bool

// Integer types
char    c  = 'A';       // 1 byte
short   s  = 100;       // >= 2 bytes
int     n  = 42;        // >= 2 bytes (usually 4)
long    l  = 100000L;
long long ll = 1000000LL;

// Unsigned
unsigned int  u  = 4294967295U;
unsigned char uc = 255;

// Fixed-width (stdint.h)
int8_t   i8  = 127;
int16_t  i16 = 32767;
int32_t  i32 = 2147483647;
int64_t  i64 = 9223372036854775807LL;
uint8_t  u8  = 255;
uint32_t u32 = 0xFFFFFFFF;

// Floating point
float       f  = 3.14f;
double      d  = 3.14159265358979;
long double ld = 3.141592653589793238L;

// Boolean (stdbool.h)
bool flag = true;
bool off  = false;

// Printing
printf("int: %d\n", n);
printf("float: %f\n", f);
printf("double: %lf\n", d);
printf("char: %c\n", c);
printf("string: %s\n", "hello");
printf("hex: %x\n", 255);
printf("pointer: %p\n", (void*)&n);
```

## Arrays and Strings

```c
#include <string.h>

// Array declaration
int arr[5] = {1, 2, 3, 4, 5};
int zeros[10] = {0};           // all zeros
int partial[5] = {1, 2};      // rest are 0

// Array access
printf("%d\n", arr[0]);        // 1
printf("size: %zu\n", sizeof(arr) / sizeof(arr[0]));

// Multi-dimensional array
int matrix[3][3] = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// String (char array)
char name[20] = "Alice";
char greeting[] = "Hello";   // size auto-calculated

// String functions
strlen(name)                  // length (without null)
strcpy(dest, src)             // copy
strncpy(dest, src, n)        // safe copy
strcat(dest, src)             // concatenate
strcmp(s1, s2)                // compare (0 = equal)
strstr(s, "sub")             // find substring
sprintf(buf, "%d", 42)       // format to string
snprintf(buf, sizeof(buf), "%s", name)   // safe format
```


---

# CHAPTER 3: POINTERS


## Pointer Fundamentals

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int x = 10;
    int *ptr = &x;    // pointer to x

    printf("x = %d\n", x);        // 10
    printf("*ptr = %d\n", *ptr);  // 10 (dereference)
    printf("&x = %p\n", (void*)&x);
    printf("ptr = %p\n", (void*)ptr);

    *ptr = 20;         // modify through pointer
    printf("x = %d\n", x);   // 20

    // Pointer arithmetic
    int arr[] = {1, 2, 3, 4, 5};
    int *p = arr;      // points to arr[0]

    for (int i = 0; i < 5; i++) {
        printf("%d ", *(p + i));
    }
    printf("\n");

    // Pointer to pointer
    int **pp = &ptr;
    printf("**pp = %d\n", **pp);

    // Null pointer
    int *null_ptr = NULL;
    if (null_ptr == NULL) printf("null!\n");

    // const pointer
    const int *cptr = &x;    // can't modify through cptr
    int *const cptr2 = &x;  // can't change cptr2 itself

    // Function pointer
    int (*add)(int, int);
    // add = &some_function;
    // add(3, 4);

    return 0;
}
```

## Dynamic Memory

```c
#include <stdlib.h>
#include <string.h>

// malloc — allocate uninitialized memory
int *arr = malloc(10 * sizeof(int));
if (arr == NULL) { /* handle error */ }

// calloc — allocate and zero-initialize
int *zarr = calloc(10, sizeof(int));

// realloc — resize allocation
arr = realloc(arr, 20 * sizeof(int));

// free — release memory
free(arr);
arr = NULL;   // avoid dangling pointer

// String duplication
char *dup = malloc(strlen(src) + 1);
strcpy(dup, src);
free(dup);

// Struct allocation
typedef struct Node {
    int val;
    struct Node *next;
} Node;

Node *node = malloc(sizeof(Node));
node->val = 42;
node->next = NULL;
free(node);
```


---

# CHAPTER 4: FUNCTIONS


## Function Basics

```c
#include <stdio.h>

// Function declaration (prototype)
int add(int a, int b);
void swap(int *a, int *b);
int *create_array(int size);

// Function definition
int add(int a, int b) {
    return a + b;
}

// Pass by pointer (simulate pass by reference)
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Return pointer (must point to heap or static, not local!)
int *create_array(int size) {
    int *arr = malloc(size * sizeof(int));
    return arr;
}

// Variadic function
#include <stdarg.h>

double average(int count, ...) {
    va_list args;
    va_start(args, count);
    double sum = 0;
    for (int i = 0; i < count; i++) {
        sum += va_arg(args, double);
    }
    va_end(args);
    return sum / count;
}

// Inline function
static inline int max(int a, int b) {
    return a > b ? a : b;
}

// Recursive
int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

// Function pointers
typedef int (*BinOp)(int, int);

int apply(BinOp op, int a, int b) {
    return op(a, b);
}

int main(void) {
    int x = 3, y = 5;
    swap(&x, &y);
    printf("x=%d y=%d\n", x, y);
    printf("avg=%.2f\n", average(3, 1.0, 2.0, 3.0));
    printf("max=%d\n", max(x, y));
    printf("apply=%d\n", apply(add, 4, 5));
    return 0;
}
```


---

# CHAPTER 5: STRUCTS AND UNIONS


## User-Defined Types

```c
#include <stdio.h>
#include <string.h>

// Struct definition
typedef struct {
    char name[50];
    int  age;
    float gpa;
} Student;

// Nested struct
typedef struct {
    float x, y;
} Point;

typedef struct {
    Point center;
    float radius;
} Circle;

// Struct initialization
Student s1 = {"Alice", 20, 3.8f};
Student s2 = {.name="Bob", .age=22, .gpa=3.5f};

// Member access
printf("Name: %s\n", s1.name);
printf("GPA: %.1f\n", s1.gpa);

// Struct pointer
Student *ptr = &s1;
printf("Name: %s\n", ptr->name);  // arrow for pointer
printf("Age: %d\n", (*ptr).age);   // equivalent

// Linked list node
typedef struct Node {
    int data;
    struct Node *next;  // must use 'struct Node' before typedef
} Node;

Node *head = NULL;

void push(Node **head, int val) {
    Node *n = malloc(sizeof(Node));
    n->data = val;
    n->next = *head;
    *head = n;
}

// Union (shared memory)
typedef union {
    int   i;
    float f;
    char  bytes[4];
} Data;

Data d;
d.i = 42;
printf("%d\n", d.i);   // 42
d.f = 3.14f;
printf("%f\n", d.f);   // 3.14 (i is now meaningless)

// Enum
typedef enum {
    RED = 0,
    GREEN,
    BLUE,
    COLOR_COUNT
} Color;

Color c = GREEN;
```


---

# CHAPTER 6: MEMORY AND POINTERS ADVANCED


## Memory Layout and Management

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Stack vs Heap
void stack_example(void) {
    int local = 42;         // stack: auto-freed
    int arr[100];           // stack: fixed size
}

void heap_example(void) {
    int *p = malloc(100 * sizeof(int));  // heap: must free
    if (!p) { perror("malloc"); exit(1); }
    memset(p, 0, 100 * sizeof(int));
    p[0] = 42;
    free(p);
}

// Dynamic 2D array
int **alloc_matrix(int rows, int cols) {
    int **m = malloc(rows * sizeof(int*));
    for (int i = 0; i < rows; i++) {
        m[i] = malloc(cols * sizeof(int));
        memset(m[i], 0, cols * sizeof(int));
    }
    return m;
}

void free_matrix(int **m, int rows) {
    for (int i = 0; i < rows; i++) free(m[i]);
    free(m);
}

// memcpy, memmove, memset
char src[] = "Hello, World!";
char dst[20];
memcpy(dst, src, strlen(src) + 1);
memmove(src + 3, src, 5);   // overlapping regions
memset(dst, 0, sizeof(dst));

// void pointer (generic pointer)
void *generic_copy(const void *src, size_t size) {
    void *dst = malloc(size);
    return dst ? memcpy(dst, src, size) : NULL;
}
```


---

# CHAPTER 7: FILE I/O


## File Operations

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    // Write to file
    FILE *fp = fopen("output.txt", "w");
    if (!fp) { perror("fopen"); return 1; }

    fprintf(fp, "Hello, %s!\n", "World");
    fputs("Another line\n", fp);
    fputc('X', fp);
    fclose(fp);

    // Read from file
    FILE *in = fopen("output.txt", "r");
    if (!in) { perror("fopen"); return 1; }

    // Read line by line
    char buf[256];
    while (fgets(buf, sizeof(buf), in)) {
        printf("Line: %s", buf);
    }
    rewind(in);

    // Read formatted
    char word[50];
    int num;
    fscanf(in, "%s %d", word, &num);
    fclose(in);

    // Binary I/O
    int data[] = {1, 2, 3, 4, 5};
    FILE *bin = fopen("data.bin", "wb");
    fwrite(data, sizeof(int), 5, bin);
    fclose(bin);

    int read_data[5];
    bin = fopen("data.bin", "rb");
    fread(read_data, sizeof(int), 5, bin);
    fclose(bin);

    // File position
    FILE *f = fopen("file.txt", "r");
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);
    fclose(f);

    return 0;
}
```


---

# CHAPTER 8: PREPROCESSOR AND MACROS


## Preprocessor Directives

```c
// Include guards
#ifndef MY_HEADER_H
#define MY_HEADER_H

// Macros
#define PI 3.14159265
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define SQUARE(x) ((x) * (x))
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))

// Variadic macro
#define LOG(fmt, ...) fprintf(stderr, fmt "\n", ##__VA_ARGS__)

// Conditional compilation
#ifdef DEBUG
    #define DBG(msg) printf("DEBUG: %s\n", msg)
#else
    #define DBG(msg) ((void)0)
#endif

#if defined(_WIN32)
    #define OS "Windows"
#elif defined(__linux__)
    #define OS "Linux"
#elif defined(__APPLE__)
    #define OS "macOS"
#endif

// Stringification and concatenation
#define STRINGIFY(x) #x
#define CONCAT(a, b) a##b

#endif /* MY_HEADER_H */

// Pragma
#pragma once   // alternative to include guard (non-standard but widespread)
#pragma pack(1)  // pack structs tightly
```


---

# CHAPTER 9: COMMON PATTERNS AND ALGORITHMS


## Data Structures and Algorithms in C

```c
// Linked list
typedef struct Node { int val; struct Node *next; } Node;

Node *push(Node *head, int val) {
    Node *n = malloc(sizeof(Node));
    n->val = val; n->next = head;
    return n;
}

// Stack (using linked list)
typedef struct { Node *top; int size; } Stack;

void stack_push(Stack *s, int val) { s->top = push(s->top, val); s->size++; }
int  stack_pop(Stack *s)  { int v = s->top->val; Node *t = s->top; s->top = t->next; free(t); s->size--; return v; }

// Binary search
int bsearch_int(const int *arr, int n, int target) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}

// Quicksort
void quicksort(int *arr, int lo, int hi) {
    if (lo >= hi) return;
    int pivot = arr[hi], i = lo - 1;
    for (int j = lo; j < hi; j++) {
        if (arr[j] <= pivot) { int t=arr[++i]; arr[i]=arr[j]; arr[j]=t; }
    }
    int t=arr[++i]; arr[i]=arr[hi]; arr[hi]=t;
    quicksort(arr, lo, i-1);
    quicksort(arr, i+1, hi);
}

// qsort with stdlib
int cmp_int(const void *a, const void *b) {
    return (*(int*)a) - (*(int*)b);
}
qsort(arr, n, sizeof(int), cmp_int);
```
