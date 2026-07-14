Operating Systems & Kernel Development Complete Reference
CHAPTER 1: GETTING STARTED WITH OS DEVELOPMENT
Remarks
Operating system development involves creating software that manages hardware resources and provides services to applications. Key components: kernel, process management, memory management, file systems, device drivers, system calls. Modern OS development uses C, Assembly, Rust, or C++.
Tools: QEMU (emulator), GCC cross-compiler, NASM/GAS (assembler), GDB (debugger), Bochs, VirtualBox.
Hello Kernel
; boot.asm - Minimal boot sector (512 bytes)
[bits 16]
[org 0x7C00]

start:
    ; Set up stack
    mov ax, 0x0000
    mov ss, ax
    mov sp, 0x7C00
    
    ; Print message
    mov si, msg
    call print_string
    
    ; Halt
    cli
    hlt

print_string:
    mov ah, 0x0E
.next_char:
    lodsb
    test al, al
    jz .done
    int 0x10
    jmp .next_char
.done:
    ret

msg db 'Hello from kernel!', 0

; Padding to 512 bytes
times 510-($-$$) db 0
dw 0xAA55

; Build and run:
; nasm -f bin boot.asm -o boot.bin
; qemu-system-x86_64 -fda boot.bin

CHAPTER 2: PROTECTED MODE AND LONG MODE
Switching to 32-bit Protected Mode
; protected_mode.asm
[bits 16]
[org 0x7C00]

start:
    ; Set up segments
    mov ax, 0x0000
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00
    
    ; Load GDT
    lgdt [gdt_descriptor]
    
    ; Enable protected mode
    mov eax, cr0
    or eax, 1
    mov cr0, eax
    
    ; Far jump to 32-bit code
    jmp 0x08:protected_mode

[bits 32]
protected_mode:
    ; Set up segment registers
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x90000
    
    ; Print message using VGA text mode
    mov edi, 0xB8000
    mov byte [edi], 'P'
    mov byte [edi+1], 0x0F
    
    cli
    hlt

; GDT (Global Descriptor Table)
gdt_start:
    ; Null descriptor
    dd 0x00000000
    dd 0x00000000
    
    ; Code segment (base=0, limit=0xFFFFF, 32-bit, execute/read)
    dw 0xFFFF      ; Limit (bits 0-15)
    dw 0x0000      ; Base (bits 0-15)
    db 0x00        ; Base (bits 16-23)
    db 10011010b   ; Access (present, ring 0, code, readable)
    db 11001111b   ; Granularity (4K, 32-bit, limit 16-19)
    db 0x00        ; Base (bits 24-31)
    
    ; Data segment (base=0, limit=0xFFFFF, 32-bit, read/write)
    dw 0xFFFF
    dw 0x0000
    db 0x00
    db 10010010b   ; Access (present, ring 0, data, writable)
    db 11001111b
    db 0x00

gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

times 510-($-$$) db 0
dw 0xAA55

Switching to 64-bit Long Mode
; long_mode.asm
[bits 32]

enable_long_mode:
    ; Check if CPU supports long mode
    mov eax, 0x80000000
    cpuid
    cmp eax, 0x80000001
    jb .no_long_mode
    
    ; Check extended features
    mov eax, 0x80000001
    cpuid
    test edx, 1 << 29  ; Long mode bit
    jz .no_long_mode
    
    ; Set up page tables
    ; Identity map first 2MB
    mov eax, page_table_l2
    or eax, 0x03        ; Present + writable
    mov [page_table_l3], eax
    
    mov eax, page_table_l3
    or eax, 0x03
    mov [page_table_l4], eax
    
    ; Map first 2MB to 0x000000
    mov eax, 0x00000000
    or eax, 0x83          ; Huge page + present + writable
    mov [page_table_l2], eax
    
    ; Load PML4 (Page Map Level 4)
    mov eax, page_table_l4
    mov cr3, eax
    
    ; Enable PAE (Physical Address Extension)
    mov eax, cr4
    or eax, 1 << 5
    mov cr4, eax
    
    ; Enable long mode in EFER MSR
    mov ecx, 0xC0000080
    rdmsr
    or eax, 1 << 8
    wrmsr
    
    ; Enable paging
    mov eax, cr0
    or eax, 1 << 31
    mov cr0, eax
    
    ; Load 64-bit GDT
    lgdt [gdt64_descriptor]
    
    ; Jump to 64-bit code
    jmp 0x08:long_mode_start

.no_long_mode:
    ; Error: long mode not supported
    mov byte [0xB8000], 'E'
    hlt

; Align page tables to 4KB
align 4096
page_table_l4: times 512 dq 0
page_table_l3: times 512 dq 0
page_table_l2: times 512 dq 0

gdt64:
    dq 0                    ; Null descriptor
    dq 0x00AF9A000000FFFF   ; Code segment (64-bit)
    dq 0x00CF92000000FFFF   ; Data segment (64-bit)

gdt64_descriptor:
    dw gdt64 - gdt64 - 1
    dd gdt64

[bits 64]
long_mode_start:
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov rsp, 0x90000
    
    ; Now in 64-bit long mode!
    mov rdi, 0xB8000
    mov byte [rdi], 'L'
    mov byte [rdi+1], 0x0F
    
    cli
    hlt

CHAPTER 3: PROCESS MANAGEMENT
Process Control Block (PCB)
// process.h
#ifndef PROCESS_H
#define PROCESS_H

#include <stdint.h>

#define MAX_PROCESSES 256
#define STACK_SIZE 4096

typedef enum {
    PROCESS_READY,
    PROCESS_RUNNING,
    PROCESS_BLOCKED,
    PROCESS_TERMINATED
} process_state_t;

typedef struct {
    // CPU registers
    uint64_t rax, rbx, rcx, rdx;
    uint64_t rsi, rdi, rbp, rsp;
    uint64_t r8, r9, r10, r11;
    uint64_t r12, r13, r14, r15;
    uint64_t rip, rflags;
    uint64_t cs, ss;
    uint64_t cr3;  // Page table base
    
    // Process metadata
    uint32_t pid;
    uint32_t ppid;  // Parent PID
    process_state_t state;
    int priority;
    uint64_t stack_base;
    uint64_t stack_size;
    
    // Memory management
    uint64_t page_directory;
    uint64_t code_start, code_end;
    uint64_t data_start, data_end;
    uint64_t heap_start, heap_end;
    
    // Scheduling
    uint64_t cpu_time;
    uint64_t start_time;
    int time_slice;
    
    // File descriptors
    int fd_table[64];
    
    // Signal handling
    uint64_t signal_mask;
    void (*signal_handlers[32])(int);
    
} process_t;

// Global process table
extern process_t process_table[MAX_PROCESSES];
extern int current_pid;

// Process management functions
int create_process(void (*entry)(void), int priority);
void destroy_process(int pid);
void schedule(void);
void yield(void);
void sleep_process(int pid, uint64_t ms);
void wake_process(int pid);

#endif

// process.c
#include "process.h"
#include <string.h>
#include <stdlib.h>

process_t process_table[MAX_PROCESSES];
int current_pid = 0;
int next_pid = 1;

// Context switch (assembly)
extern void context_switch(process_t* old, process_t* new);

int create_process(void (*entry)(void), int priority) {
    // Find free slot
    int pid = -1;
    for (int i = 1; i < MAX_PROCESSES; i++) {
        if (process_table[i].state == PROCESS_TERMINATED) {
            pid = i;
            break;
        }
    }
    
    if (pid == -1) return -1;  // No free slots
    
    process_t* proc = &process_table[pid];
    memset(proc, 0, sizeof(process_t));
    
    proc->pid = next_pid++;
    proc->ppid = current_pid;
    proc->state = PROCESS_READY;
    proc->priority = priority;
    proc->time_slice = 10;  // 10ms time slice
    
    // Allocate stack
    proc->stack_base = (uint64_t)malloc(STACK_SIZE);
    proc->stack_size = STACK_SIZE;
    proc->rsp = proc->stack_base + STACK_SIZE - 8;
    
    // Set up initial context
    proc->rip = (uint64_t)entry;
    proc->rflags = 0x202;  // Interrupts enabled
    proc->cs = 0x08;       // Code segment
    proc->ss = 0x10;       // Data segment
    
    // Copy page directory from parent
    proc->cr3 = process_table[current_pid].cr3;
    
    return proc->pid;
}

void destroy_process(int pid) {
    if (pid < 0 || pid >= MAX_PROCESSES) return;
    
    process_t* proc = &process_table[pid];
    if (proc->state == PROCESS_TERMINATED) return;
    
    // Free resources
    free((void*)proc->stack_base);
    
    proc->state = PROCESS_TERMINATED;
    
    // If current process, switch to another
    if (pid == current_pid) {
        schedule();
    }
}

void schedule(void) {
    int old_pid = current_pid;
    
    // Simple round-robin scheduler
    for (int i = 1; i < MAX_PROCESSES; i++) {
        int next_pid = (current_pid + i) % MAX_PROCESSES;
        process_t* proc = &process_table[next_pid];
        
        if (proc->state == PROCESS_READY) {
            proc->state = PROCESS_RUNNING;
            current_pid = next_pid;
            
            if (old_pid != 0) {
                process_table[old_pid].state = PROCESS_READY;
            }
            
            // Perform context switch
            context_switch(&process_table[old_pid], proc);
            return;
        }
    }
    
    // No ready processes, idle
    current_pid = 0;
}

void yield(void) {
    schedule();
}

void sleep_process(int pid, uint64_t ms) {
    if (pid < 0 || pid >= MAX_PROCESSES) return;
    
    process_t* proc = &process_table[pid];
    proc->state = PROCESS_BLOCKED;
    
    // TODO: Add to sleep queue with wake time
    
    if (pid == current_pid) {
        schedule();
    }
}

void wake_process(int pid) {
    if (pid < 0 || pid >= MAX_PROCESSES) return;
    
    process_t* proc = &process_table[pid];
    if (proc->state == PROCESS_BLOCKED) {
        proc->state = PROCESS_READY;
    }
}

Context Switch Assembly
; context_switch.asm
global context_switch

; void context_switch(process_t* old, process_t* new)
context_switch:
    ; Save current context
    push rbp
    push rbx
    push r12
    push r13
    push r14
    push r15
    
    ; Save stack pointer to old process
    mov rax, [rdi]          ; old->rsp
    mov [rax], rsp
    
    ; Load new stack pointer
    mov rax, [rsi]          ; new->rsp
    mov rsp, [rax]
    
    ; Restore new context
    pop r15
    pop r14
    pop r13
    pop r12
    pop rbx
    pop rbp
    
    ; Switch page tables if needed
    mov rax, [rsi + 120]    ; new->cr3
    mov rcx, [rdi + 120]    ; old->cr3
    cmp rax, rcx
    je .no_cr3_switch
    mov cr3, rax
.no_cr3_switch:
    
    ret

CHAPTER 4: MEMORY MANAGEMENT
Physical Memory Manager
// memory.h
#ifndef MEMORY_H
#define MEMORY_H

#include <stdint.h>
#include <stddef.h>

#define PAGE_SIZE 4096
#define PAGE_PRESENT  0x001
#define PAGE_WRITE    0x002
#define PAGE_USER     0x004
#define PAGE_HUGE     0x080

// Memory map entry from bootloader
typedef struct {
    uint64_t base;
    uint64_t length;
    uint32_t type;  // 1=available, 2=reserved, 3=ACPI, 4=nvs, 5=unusable
    uint32_t acpi_ext;
} memory_map_entry_t;

// Physical page frame
typedef struct page_frame {
    struct page_frame* next;
    int ref_count;
} page_frame_t;

// Virtual memory area
typedef struct vm_area {
    uint64_t start;
    uint64_t end;
    int flags;
    struct vm_area* next;
} vm_area_t;

// Process address space
typedef struct {
    uint64_t page_directory;
    vm_area_t* vm_list;
    uint64_t heap_start;
    uint64_t heap_end;
    uint64_t stack_start;
    uint64_t stack_end;
} address_space_t;

// Physical memory management
void memory_init(memory_map_entry_t* mmap, int mmap_count);
void* alloc_page(void);
void free_page(void* page);
uint64_t get_free_memory(void);

// Virtual memory management
void vm_init(void);
address_space_t* create_address_space(void);
void destroy_address_space(address_space_t* as);
int map_page(address_space_t* as, uint64_t virt, uint64_t phys, int flags);
void unmap_page(address_space_t* as, uint64_t virt);
uint64_t virt_to_phys(address_space_t* as, uint64_t virt);

// Heap management
void* kmalloc(size_t size);
void kfree(void* ptr);
void* krealloc(void* ptr, size_t size);

#endif

// memory.c
#include "memory.h"
#include <string.h>

// Free page list
static page_frame_t* free_list = NULL;
static uint64_t total_memory = 0;
static uint64_t free_memory = 0;

// Page frame array
#define MAX_PAGES (1024 * 1024)  // 4GB with 4KB pages
static page_frame_t page_frames[MAX_PAGES];

void memory_init(memory_map_entry_t* mmap, int mmap_count) {
    // Count total and available memory
    for (int i = 0; i < mmap_count; i++) {
        total_memory += mmap[i].length;
        if (mmap[i].type == 1) {  // Available
            free_memory += mmap[i].length;
        }
    }
    
    // Initialize free list from available regions
    for (int i = 0; i < mmap_count; i++) {
        if (mmap[i].type == 1) {
            uint64_t start = (mmap[i].base + PAGE_SIZE - 1) & ~(PAGE_SIZE - 1);
            uint64_t end = (mmap[i].base + mmap[i].length) & ~(PAGE_SIZE - 1);
            
            for (uint64_t addr = start; addr < end; addr += PAGE_SIZE) {
                int page_idx = addr / PAGE_SIZE;
                if (page_idx < MAX_PAGES) {
                    page_frames[page_idx].next = free_list;
                    page_frames[page_idx].ref_count = 0;
                    free_list = &page_frames[page_idx];
                }
            }
        }
    }
}

void* alloc_page(void) {
    if (free_list == NULL) {
        return NULL;  // Out of memory
    }
    
    page_frame_t* page = free_list;
    free_list = page->next;
    page->ref_count = 1;
    page->next = NULL;
    
    free_memory -= PAGE_SIZE;
    
    int page_idx = page - page_frames;
    return (void*)((uint64_t)page_idx * PAGE_SIZE);
}

void free_page(void* page) {
    uint64_t addr = (uint64_t)page;
    int page_idx = addr / PAGE_SIZE;
    
    if (page_idx >= MAX_PAGES) return;
    
    page_frame_t* frame = &page_frames[page_idx];
    frame->ref_count--;
    
    if (frame->ref_count == 0) {
        frame->next = free_list;
        free_list = frame;
        free_memory += PAGE_SIZE;
    }
}

uint64_t get_free_memory(void) {
    return free_memory;
}

Virtual Memory Management
// Page table structures (x86-64)
typedef struct {
    uint64_t entries[512];
} page_table_t;

// Virtual address breakdown (4KB pages):
// Bits 0-11:  Offset in page (4KB)
// Bits 12-20: Page table index (512 entries)
// Bits 21-29: Page directory index
// Bits 30-38: Page directory pointer index
// Bits 39-47: Page map level 4 index

static inline uint64_t get_pml4_index(uint64_t virt) {
    return (virt >> 39) & 0x1FF;
}

static inline uint64_t get_pdpt_index(uint64_t virt) {
    return (virt >> 30) & 0x1FF;
}

static inline uint64_t get_pd_index(uint64_t virt) {
    return (virt >> 21) & 0x1FF;
}

static inline uint64_t get_pt_index(uint64_t virt) {
    return (virt >> 12) & 0x1FF;
}

address_space_t* create_address_space(void) {
    address_space_t* as = (address_space_t*)kmalloc(sizeof(address_space_t));
    
    // Allocate PML4
    page_table_t* pml4 = (page_table_t*)alloc_page();
    memset(pml4, 0, PAGE_SIZE);
    
    as->page_directory = (uint64_t)pml4;
    as->vm_list = NULL;
    as->heap_start = 0x400000;  // 4MB
    as->heap_end = as->heap_start;
    as->stack_start = 0x7FFFFFFF000;  // Near top of user space
    as->stack_end = as->stack_start;
    
    return as;
}

void destroy_address_space(address_space_t* as) {
    // TODO: Free all page tables and mapped pages
    kfree(as);
}

int map_page(address_space_t* as, uint64_t virt, uint64_t phys, int flags) {
    page_table_t* pml4 = (page_table_t*)as->page_directory;
    
    // Get or create PDPT
    int pml4_idx = get_pml4_index(virt);
    if (!(pml4->entries[pml4_idx] & PAGE_PRESENT)) {
        page_table_t* pdpt = (page_table_t*)alloc_page();
        memset(pdpt, 0, PAGE_SIZE);
        pml4->entries[pml4_idx] = (uint64_t)pdpt | PAGE_PRESENT | PAGE_WRITE | PAGE_USER;
    }
    page_table_t* pdpt = (page_table_t*)(pml4->entries[pml4_idx] & ~0xFFF);
    
    // Get or create PD
    int pdpt_idx = get_pdpt_index(virt);
    if (!(pdpt->entries[pdpt_idx] & PAGE_PRESENT)) {
        page_table_t* pd = (page_table_t*)alloc_page();
        memset(pd, 0, PAGE_SIZE);
        pdpt->entries[pdpt_idx] = (uint64_t)pd | PAGE_PRESENT | PAGE_WRITE | PAGE_USER;
    }
    page_table_t* pd = (page_table_t*)(pdpt->entries[pdpt_idx] & ~0xFFF);
    
    // Get or create PT
    int pd_idx = get_pd_index(virt);
    if (!(pd->entries[pd_idx] & PAGE_PRESENT)) {
        page_table_t* pt = (page_table_t*)alloc_page();
        memset(pt, 0, PAGE_SIZE);
        pd->entries[pd_idx] = (uint64_t)pt | PAGE_PRESENT | PAGE_WRITE | PAGE_USER;
    }
    page_table_t* pt = (page_table_t*)(pd->entries[pd_idx] & ~0xFFF);
    
    // Map the page
    int pt_idx = get_pt_index(virt);
    pt->entries[pt_idx] = (phys & ~0xFFF) | flags | PAGE_PRESENT;
    
    // Invalidate TLB
    asm volatile("invlpg (%0)" :: "r"(virt) : "memory");
    
    return 0;
}

void unmap_page(address_space_t* as, uint64_t virt) {
    // Similar to map_page, but clear the entry
    // TODO: Implement
}

uint64_t virt_to_phys(address_space_t* as, uint64_t virt) {
    page_table_t* pml4 = (page_table_t*)as->page_directory;
    
    int pml4_idx = get_pml4_index(virt);
    if (!(pml4->entries[pml4_idx] & PAGE_PRESENT)) return 0;
    page_table_t* pdpt = (page_table_t*)(pml4->entries[pml4_idx] & ~0xFFF);
    
    int pdpt_idx = get_pdpt_index(virt);
    if (!(pdpt->entries[pdpt_idx] & PAGE_PRESENT)) return 0;
    page_table_t* pd = (page_table_t*)(pdpt->entries[pdpt_idx] & ~0xFFF);
    
    int pd_idx = get_pd_index(virt);
    if (!(pd->entries[pd_idx] & PAGE_PRESENT)) return 0;
    
    // Check for huge page
    if (pd->entries[pd_idx] & PAGE_HUGE) {
        return (pd->entries[pd_idx] & ~0x1FFFFF) | (virt & 0x1FFFFF);
    }
    
    page_table_t* pt = (page_table_t*)(pd->entries[pd_idx] & ~0xFFF);
    int pt_idx = get_pt_index(virt);
    
    if (!(pt->entries[pt_idx] & PAGE_PRESENT)) return 0;
    
    return (pt->entries[pt_idx] & ~0xFFF) | (virt & 0xFFF);
}

Kernel Heap Allocator
// Simple first-fit allocator
#define HEAP_START 0xFFFF800000000000
#define HEAP_SIZE  (16 * 1024 * 1024)  // 16MB

typedef struct block_header {
    size_t size;
    int free;
    struct block_header* next;
} block_header_t;

static block_header_t* heap_start = NULL;

void heap_init(void) {
    // Allocate initial heap pages
    uint64_t heap_phys = (uint64_t)alloc_page();
    // Map heap to virtual address
    // TODO: Map multiple pages
    
    heap_start = (block_header_t*)HEAP_START;
    heap_start->size = HEAP_SIZE - sizeof(block_header_t);
    heap_start->free = 1;
    heap_start->next = NULL;
}

void* kmalloc(size_t size) {
    if (size == 0) return NULL;
    
    // Align size to 8 bytes
    size = (size + 7) & ~7;
    
    block_header_t* current = heap_start;
    
    while (current) {
        if (current->free && current->size >= size) {
            // Split block if large enough
            if (current->size > size + sizeof(block_header_t) + 32) {
                block_header_t* new_block = (block_header_t*)((char*)current + sizeof(block_header_t) + size);
                new_block->size = current->size - size - sizeof(block_header_t);
                new_block->free = 1;
                new_block->next = current->next;
                
                current->size = size;
                current->next = new_block;
            }
            
            current->free = 0;
            return (void*)((char*)current + sizeof(block_header_t));
        }
        current = current->next;
    }
    
    return NULL;  // Out of memory
}

void kfree(void* ptr) {
    if (!ptr) return;
    
    block_header_t* block = (block_header_t*)((char*)ptr - sizeof(block_header_t));
    block->free = 1;
    
    // Coalesce with next block if free
    if (block->next && block->next->free) {
        block->size += sizeof(block_header_t) + block->next->size;
        block->next = block->next->next;
    }
    
    // Coalesce with previous block if free
    block_header_t* current = heap_start;
    while (current && current->next != block) {
        current = current->next;
    }
    
    if (current && current->free) {
        current->size += sizeof(block_header_t) + block->size;
        current->next = block->next;
    }
}

CHAPTER 5: INTERRUPT HANDLING
Interrupt Descriptor Table (IDT)
// interrupts.h
#ifndef INTERRUPTS_H
#define INTERRUPTS_H

#include <stdint.h>

// IDT entry (16 bytes)
typedef struct {
    uint16_t offset_low;
    uint16_t selector;
    uint8_t ist;
    uint8_t type_attr;
    uint16_t offset_mid;
    uint32_t offset_high;
    uint32_t zero;
} __attribute__((packed)) idt_entry_t;

// IDT pointer
typedef struct {
    uint16_t limit;
    uint64_t base;
} __attribute__((packed)) idt_ptr_t;

// Interrupt frame (pushed by CPU)
typedef struct {
    uint64_t r15, r14, r13, r12, r11, r10, r9, r8;
    uint64_t rbp, rdi, rsi, rdx, rcx, rbx, rax;
    uint64_t int_no, error_code;
    uint64_t rip, cs, rflags, rsp, ss;
} __attribute__((packed)) interrupt_frame_t;

// Interrupt handlers
void idt_init(void);
void set_interrupt_handler(int irq, void (*handler)(interrupt_frame_t*));

// IRQ handlers
void irq_timer(interrupt_frame_t* frame);
void irq_keyboard(interrupt_frame_t* frame);

// PIC (Programmable Interrupt Controller)
void pic_init(void);
void pic_send_eoi(int irq);

#endif

// interrupts.c
#include "interrupts.h"
#include <string.h>

#define IDT_ENTRIES 256

static idt_entry_t idt[IDT_ENTRIES];
static idt_ptr_t idt_pointer;

// External assembly handlers
extern void isr0(void);
extern void isr1(void);
// ... (define all 32 CPU exceptions)
extern void irq0(void);
extern void irq1(void);
// ... (define all 16 IRQs)

// Interrupt handler table
static void (*interrupt_handlers[IDT_ENTRIES])(interrupt_frame_t*) = {0};

void idt_set_gate(int num, uint64_t handler, uint16_t selector, uint8_t type_attr) {
    idt[num].offset_low = handler & 0xFFFF;
    idt[num].selector = selector;
    idt[num].ist = 0;
    idt[num].type_attr = type_attr;
    idt[num].offset_mid = (handler >> 16) & 0xFFFF;
    idt[num].offset_high = (handler >> 32) & 0xFFFFFFFF;
    idt[num].zero = 0;
}

void idt_init(void) {
    idt_pointer.limit = sizeof(idt) - 1;
    idt_pointer.base = (uint64_t)&idt;
    
    // Remap PIC
    pic_init();
    
    // Set up CPU exception handlers
    idt_set_gate(0, (uint64_t)isr0, 0x08, 0x8E);   // Division by zero
    idt_set_gate(1, (uint64_t)isr1, 0x08, 0x8E);   // Debug exception
    // ... (set up all 32 exceptions)
    
    // Set up IRQ handlers
    idt_set_gate(32, (uint64_t)irq0, 0x08, 0x8E);  // Timer
    idt_set_gate(33, (uint64_t)irq1, 0x08, 0x8E);  // Keyboard
    // ... (set up all 16 IRQs)
    
    // Load IDT
    asm volatile("lidt %0" :: "m"(idt_pointer));
    
    // Enable interrupts
    asm volatile("sti");
}

void set_interrupt_handler(int irq, void (*handler)(interrupt_frame_t*)) {
    interrupt_handlers[irq] = handler;
}

// Common interrupt handler (called from assembly)
void interrupt_handler(interrupt_frame_t* frame) {
    if (interrupt_handlers[frame->int_no]) {
        interrupt_handlers[frame->int_no](frame);
    }
    
    // Send EOI for IRQs
    if (frame->int_no >= 32 && frame->int_no < 48) {
        pic_send_eoi(frame->int_no - 32);
    }
}

PIC (8259A) Initialization
// pic.c
#include "interrupts.h"

#define PIC1_CMD  0x20
#define PIC1_DATA 0x21
#define PIC2_CMD  0xA0
#define PIC2_DATA 0xA1

#define ICW1_ICW4       0x01
#define ICW1_INIT       0x10
#define ICW4_8086       0x01

void pic_init(void) {
    // Save masks
    uint8_t mask1 = inb(PIC1_DATA);
    uint8_t mask2 = inb(PIC2_DATA);
    
    // Start initialization
    outb(PIC1_CMD, ICW1_INIT | ICW1_ICW4);
    io_wait();
    outb(PIC2_CMD, ICW1_INIT | ICW1_ICW4);
    io_wait();
    
    // Set vector offsets (IRQ 0-7 → INT 32-39, IRQ 8-15 → INT 40-47)
    outb(PIC1_DATA, 32);
    io_wait();
    outb(PIC2_DATA, 40);
    io_wait();
    
    // Tell Master PIC there's a slave at IRQ2
    outb(PIC1_DATA, 4);
    io_wait();
    outb(PIC2_DATA, 2);
    io_wait();
    
    // Set 8086 mode
    outb(PIC1_DATA, ICW4_8086);
    io_wait();
    outb(PIC2_DATA, ICW4_8086);
    io_wait();
    
    // Restore masks
    outb(PIC1_DATA, mask1);
    outb(PIC2_DATA, mask2);
}

void pic_send_eoi(int irq) {
    if (irq >= 8) {
        outb(PIC2_CMD, 0x20);
    }
    outb(PIC1_CMD, 0x20);
}

void pic_enable_irq(int irq) {
    uint16_t port;
    if (irq < 8) {
        port = PIC1_DATA;
    } else {
        port = PIC2_DATA;
        irq -= 8;
    }
    uint8_t mask = inb(port) & ~(1 << irq);
    outb(port, mask);
}

void pic_disable_irq(int irq) {
    uint16_t port;
    if (irq < 8) {
        port = PIC1_DATA;
    } else {
        port = PIC2_DATA;
        irq -= 8;
    }
    uint8_t mask = inb(port) | (1 << irq);
    outb(port, mask);
}

Timer Interrupt Handler
// timer.c
#include "interrupts.h"

#define PIT_CHANNEL0 0x40
#define PIT_CMD      0x43
#define PIT_FREQ     1193182

static uint64_t ticks = 0;
static uint64_t tick_rate = 100;  // 100 Hz

void timer_init(int frequency) {
    tick_rate = frequency;
    
    // Calculate divisor
    uint16_t divisor = PIT_FREQ / frequency;
    
    // Channel 0, lobyte/hibyte, rate generator
    outb(PIT_CMD, 0x36);
    outb(PIT_CHANNEL0, divisor & 0xFF);
    outb(PIT_CHANNEL0, (divisor >> 8) & 0xFF);
    
    // Register handler
    set_interrupt_handler(32, irq_timer);
    pic_enable_irq(0);
}

void irq_timer(interrupt_frame_t* frame) {
    ticks++;
    
    // Update process CPU time
    if (current_pid > 0) {
        process_table[current_pid].cpu_time++;
        
        // Check time slice
        if (process_table[current_pid].cpu_time >= process_table[current_pid].time_slice) {
            process_table[current_pid].cpu_time = 0;
            schedule();
        }
    }
    
    // TODO: Wake up sleeping processes
}

uint64_t get_ticks(void) {
    return ticks;
}

void sleep(uint64_t ms) {
    uint64_t target = ticks + (ms * tick_rate / 1000);
    while (ticks < target) {
        asm volatile("hlt");
    }
}

Keyboard Interrupt Handler
// keyboard.c
#include "interrupts.h"

#define KB_DATA 0x60
#define KB_STATUS 0x64

// US keyboard layout (simplified)
static const char scancode_to_ascii[128] = {
    0, 27, '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '\b',
    '\t', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\n',
    0, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', '`',
    0, '\\', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 0,
    '*', 0, ' '
};

static char key_buffer[256];
static int buffer_pos = 0;

void keyboard_init(void) {
    set_interrupt_handler(33, irq_keyboard);
    pic_enable_irq(1);
}

void irq_keyboard(interrupt_frame_t* frame) {
    uint8_t scancode = inb(KB_DATA);
    
    // Key release (bit 7 set)
    if (scancode & 0x80) {
        return;
    }
    
    char c = scancode_to_ascii[scancode];
    if (c) {
        if (buffer_pos < 255) {
            key_buffer[buffer_pos++] = c;
        }
        
        // Echo to screen
        // TODO: Implement proper console output
    }
}

int keyboard_read(char* buffer, int max_len) {
    int len = (buffer_pos < max_len) ? buffer_pos : max_len;
    memcpy(buffer, key_buffer, len);
    buffer_pos = 0;
    return len;
}

CHAPTER 6: SYSTEM CALLS
System Call Interface
// syscall.h
#ifndef SYSCALL_H
#define SYSCALL_H

#include <stdint.h>

// System call numbers
#define SYS_EXIT        1
#define SYS_READ        2
#define SYS_WRITE       3
#define SYS_OPEN        4
#define SYS_CLOSE       5
#define SYS_MMAP        6
#define SYS_MUNMAP      7
#define SYS_FORK        8
#define SYS_EXEC        9
#define SYS_WAIT        10
#define SYS_GETPID      11
#define SYS_BRK         12

// System call handler
void syscall_init(void);
void syscall_handler(interrupt_frame_t* frame);

#endif

// syscall.c
#include "syscall.h"
#include "interrupts.h"
#include "process.h"
#include "memory.h"

#define SYSCALL_VECTOR 0x80

void syscall_init(void) {
    // Set up syscall interrupt gate
    idt_set_gate(SYSCALL_VECTOR, (uint64_t)syscall_entry, 0x08, 0xEE);
}

// Assembly entry point
extern void syscall_entry(void);

void syscall_handler(interrupt_frame_t* frame) {
    uint64_t syscall_num = frame->rax;
    uint64_t arg1 = frame->rdi;
    uint64_t arg2 = frame->rsi;
    uint64_t arg3 = frame->rdx;
    uint64_t arg4 = frame->r10;
    uint64_t arg5 = frame->r8;
    
    int64_t result = 0;
    
    switch (syscall_num) {
        case SYS_EXIT:
            destroy_process(current_pid);
            break;
        
        case SYS_READ:
            // TODO: Implement file reading
            result = -1;
            break;
        
        case SYS_WRITE:
            // TODO: Implement file writing
            result = -1;
            break;
        
        case SYS_GETPID:
            result = process_table[current_pid].pid;
            break;
        
        case SYS_FORK:
            // TODO: Implement fork
            result = -1;
            break;
        
        case SYS_BRK:
            // Adjust program break (heap)
            if (arg1 > process_table[current_pid].heap_start) {
                process_table[current_pid].heap_end = arg1;
                result = 0;
            } else {
                result = -1;
            }
            break;
        
        default:
            result = -1;  // Invalid syscall
            break;
    }
    
    frame->rax = result;
}

System Call Assembly Wrapper
; syscall.asm
global syscall_entry

extern syscall_handler

syscall_entry:
    ; Save user registers
    push rax
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
    push rbp
    push r8
    push r9
    push r10
    push r11
    push r12
    push r13
    push r14
    push r15
    
    ; Call C handler
    call syscall_handler
    
    ; Restore registers
    pop r15
    pop r14
    pop r13
    pop r12
    pop r11
    pop r10
    pop r9
    pop r8
    pop rbp
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rax
    
    ; Return from interrupt
    iretq

User-space syscall wrapper (C library)
// syscall_lib.c
#include <stdint.h>

static inline int64_t syscall(int num, ...) {
    int64_t ret;
    __asm__ volatile (
        "int $0x80"
        : "=a"(ret)
        : "a"(num)
        : "memory"
    );
    return ret;
}

// Wrapper functions
int sys_exit(int status) {
    return syscall(SYS_EXIT, status);
}

int sys_getpid(void) {
    return syscall(SYS_GETPID);
}

int sys_write(int fd, const void* buf, int count) {
    int64_t ret;
    __asm__ volatile (
        "int $0x80"
        : "=a"(ret)
        : "a"(SYS_WRITE), "D"(fd), "S"(buf), "d"(count)
        : "memory"
    );
    return ret;
}

int sys_read(int fd, void* buf, int count) {
    int64_t ret;
    __asm__ volatile (
        "int $0x80"
        : "=a"(ret)
        : "a"(SYS_READ), "D"(fd), "S"(buf), "d"(count)
        : "memory"
    );
    return ret;
}

void* sys_mmap(void* addr, size_t length, int prot, int flags, int fd, int offset) {
    int64_t ret;
    __asm__ volatile (
        "int $0x80"
        : "=a"(ret)
        : "a"(SYS_MMAP), "D"(addr), "S"(length), "d"(prot), "r"(flags), "r"(fd), "r"(offset)
        : "memory"
    );
    return (void*)ret;
}

CHAPTER 7: FILE SYSTEMS
Virtual File System (VFS)
// vfs.h
#ifndef VFS_H
#define VFS_H

#include <stdint.h>
#include <stddef.h>

#define MAX_PATH 256
#define MAX_FILENAME 64

// File types
typedef enum {
    FILE_REGULAR,
    FILE_DIRECTORY,
    FILE_SYMLINK,
    FILE_DEVICE
} file_type_t;

// File permissions
#define PERM_READ    0x04
#define PERM_WRITE   0x02
#define PERM_EXECUTE 0x01

// Inode (file metadata)
typedef struct inode {
    uint64_t inode_num;
    file_type_t type;
    uint32_t permissions;
    uint32_t uid, gid;
    uint64_t size;
    uint64_t atime, mtime, ctime;  // Access, modify, change times
    uint32_t nlinks;
    
    // File data pointers
    uint64_t blocks[12];      // Direct blocks
    uint64_t indirect_block;  // Single indirect
    uint64_t double_indirect; // Double indirect
    uint64_t triple_indirect; // Triple indirect
    
    // File system specific
    void* fs_data;
    
    // VFS operations
    struct vfs_operations* ops;
} inode_t;

// Directory entry
typedef struct dirent {
    uint64_t inode_num;
    char name[MAX_FILENAME];
} dirent_t;

// File descriptor
typedef struct {
    inode_t* inode;
    uint64_t offset;
    int flags;
    int ref_count;
} file_descriptor_t;

// VFS operations
typedef struct vfs_operations {
    int (*read)(inode_t* inode, void* buf, size_t size, uint64_t offset);
    int (*write)(inode_t* inode, const void* buf, size_t size, uint64_t offset);
    int (*open)(inode_t* inode, int flags);
    int (*close)(inode_t* inode);
    int (*mkdir)(inode_t* parent, const char* name, uint32_t mode);
    int (*rmdir)(inode_t* parent, const char* name);
    int (*unlink)(inode_t* parent, const char* name);
    int (*readdir)(inode_t* dir, dirent_t* entry, int index);
    inode_t* (*lookup)(inode_t* dir, const char* name);
    inode_t* (*create)(inode_t* dir, const char* name, uint32_t mode);
} vfs_operations_t;

// Mount point
typedef struct mount_point {
    char path[MAX_PATH];
    inode_t* root;
    vfs_operations_t* ops;
    struct mount_point* next;
} mount_point_t;

// VFS functions
void vfs_init(void);
int vfs_mount(const char* path, inode_t* root, vfs_operations_t* ops);
file_descriptor_t* vfs_open(const char* path, int flags);
int vfs_close(file_descriptor_t* fd);
int vfs_read(file_descriptor_t* fd, void* buf, size_t size);
int vfs_write(file_descriptor_t* fd, const void* buf, size_t size);
inode_t* vfs_lookup(const char* path);

#endif

// vfs.c
#include "vfs.h"
#include "memory.h"
#include <string.h>

#define MAX_FILE_DESCRIPTORS 1024

static file_descriptor_t fd_table[MAX_FILE_DESCRIPTORS];
static mount_point_t* mount_list = NULL;
static inode_t* root_inode = NULL;

void vfs_init(void) {
    memset(fd_table, 0, sizeof(fd_table));
}

int vfs_mount(const char* path, inode_t* root, vfs_operations_t* ops) {
    mount_point_t* mp = (mount_point_t*)kmalloc(sizeof(mount_point_t));
    strncpy(mp->path, path, MAX_PATH);
    mp->root = root;
    mp->ops = ops;
    mp->next = mount_list;
    mount_list = mp;
    
    if (strcmp(path, "/") == 0) {
        root_inode = root;
    }
    
    return 0;
}

inode_t* vfs_lookup(const char* path) {
    if (!root_inode) return NULL;
    
    // Start from root
    inode_t* current = root_inode;
    
    // Parse path components
    char component[MAX_FILENAME];
    const char* p = path;
    
    if (*p == '/') p++;  // Skip leading slash
    
    while (*p) {
        // Extract next component
        int i = 0;
        while (*p && *p != '/' && i < MAX_FILENAME - 1) {
            component[i++] = *p++;
        }
        component[i] = '\0';
        
        if (*p == '/') p++;
        
        // Look up component in current directory
        if (!current->ops || !current->ops->lookup) {
            return NULL;
        }
        
        current = current->ops->lookup(current, component);
        if (!current) return NULL;
    }
    
    return current;
}

file_descriptor_t* vfs_open(const char* path, int flags) {
    inode_t* inode = vfs_lookup(path);
    if (!inode) return NULL;
    
    // Find free file descriptor
    int fd_num = -1;
    for (int i = 0; i < MAX_FILE_DESCRIPTORS; i++) {
        if (fd_table[i].inode == NULL) {
            fd_num = i;
            break;
        }
    }
    
    if (fd_num == -1) return NULL;
    
    file_descriptor_t* fd = &fd_table[fd_num];
    fd->inode = inode;
    fd->offset = 0;
    fd->flags = flags;
    fd->ref_count = 1;
    
    // Call file system open
    if (inode->ops && inode->ops->open) {
        inode->ops->open(inode, flags);
    }
    
    return fd;
}

int vfs_close(file_descriptor_t* fd) {
    if (!fd) return -1;
    
    fd->ref_count--;
    if (fd->ref_count == 0) {
        if (fd->inode->ops && fd->inode->ops->close) {
            fd->inode->ops->close(fd->inode);
        }
        fd->inode = NULL;
    }
    
    return 0;
}

int vfs_read(file_descriptor_t* fd, void* buf, size_t size) {
    if (!fd || !fd->inode || !fd->inode->ops || !fd->inode->ops->read) {
        return -1;
    }
    
    int bytes_read = fd->inode->ops->read(fd->inode, buf, size, fd->offset);
    if (bytes_read > 0) {
        fd->offset += bytes_read;
    }
    
    return bytes_read;
}

int vfs_write(file_descriptor_t* fd, const void* buf, size_t size) {
    if (!fd || !fd->inode || !fd->inode->ops || !fd->inode->ops->write) {
        return -1;
    }
    
    int bytes_written = fd->inode->ops->write(fd->inode, buf, size, fd->offset);
    if (bytes_written > 0) {
        fd->offset += bytes_written;
    }
    
    return bytes_written;
}

Simple File System Implementation
// simplefs.h
#ifndef SIMPLEFS_H
#define SIMPLEFS_H

#include "vfs.h"

#define BLOCK_SIZE 4096
#define MAX_BLOCKS 1024

// Superblock
typedef struct {
    uint32_t magic;
    uint32_t block_size;
    uint32_t num_blocks;
    uint32_t num_inodes;
    uint32_t inode_bitmap_block;
    uint32_t data_bitmap_block;
    uint32_t inode_table_block;
    uint32_t root_inode;
} superblock_t;

// SimpleFS functions
int simplefs_init(uint64_t device);
inode_t* simplefs_get_root(void);
vfs_operations_t* simplefs_get_ops(void);

#endif

// simplefs.c
#include "simplefs.h"
#include "memory.h"
#include <string.h>

static superblock_t sb;
static uint64_t device_id;

// Block bitmap operations
static int block_alloc