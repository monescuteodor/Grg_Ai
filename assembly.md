# Assembly Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH ASSEMBLY


## Remarks

Assembly language is a low-level programming language with a strong correspondence to machine code instructions. Each line maps to one (or few) CPU instructions. This reference covers x86-64 (AMD64) assembly with NASM syntax and AT&T/GAS syntax where relevant.

Assemblers: NASM (Netwide Assembler), MASM (Microsoft), GAS (GNU Assembler), FASM.


## Hello World (Linux x86-64, NASM)

```nasm
; hello.asm — x86-64 Linux
section .data
    msg db "Hello, World!", 10   ; message + newline (10='\n')
    len equ $ - msg              ; length of message

section .text
    global _start

_start:
    ; sys_write(stdout, msg, len)
    mov rax, 1          ; syscall: write
    mov rdi, 1          ; fd: stdout
    mov rsi, msg        ; buffer pointer
    mov rdx, len        ; length
    syscall

    ; sys_exit(0)
    mov rax, 60         ; syscall: exit
    xor rdi, rdi        ; exit code 0
    syscall
```

```bash
nasm -f elf64 hello.asm -o hello.o
ld hello.o -o hello
./hello

# With C runtime (macOS/Windows friendly)
nasm -f elf64 hello.asm
gcc hello.o -o hello -nostartfiles
```


---

# CHAPTER 2: REGISTERS


## x86-64 Register Set

```
; General-purpose registers (64-bit)
rax   rcx   rdx   rbx   rsp   rbp   rsi   rdi
r8    r9    r10   r11   r12   r13   r14   r15

; 32-bit sub-registers (zero-extend to 64-bit on write)
eax   ecx   edx   ebx   esp   ebp   esi   edi
r8d   r9d   r10d  r11d  r12d  r13d  r14d  r15d

; 16-bit sub-registers
ax    cx    dx    bx    sp    bp    si    di
r8w   r9w   r10w  r11w  r12w  r13w  r14w  r15w

; 8-bit sub-registers
al    cl    dl    bl    spl   bpl   sil   dil
ah    ch    dh    bh                           ; high bytes of ax,cx,dx,bx
r8b   r9b   r10b  r11b  r12b  r13b  r14b  r15b

; Special registers
rip   ; instruction pointer
rsp   ; stack pointer
rbp   ; base pointer (frame pointer)
rflags ; flags register

; Segment registers
cs ds es fs gs ss

; SIMD registers
xmm0..xmm15   ; 128-bit (SSE/SSE2)
ymm0..ymm15   ; 256-bit (AVX)
zmm0..zmm31   ; 512-bit (AVX-512)

; Linux/System V AMD64 calling convention:
; Args:    rdi, rsi, rdx, rcx, r8, r9 (then stack)
; Return:  rax (rdx for second value)
; Callee-saved: rbx, rbp, r12-r15
; Caller-saved: rax, rcx, rdx, rsi, rdi, r8-r11

; Windows x64 calling convention:
; Args:    rcx, rdx, r8, r9 (then stack with shadow space)
; Return:  rax
; Callee-saved: rbx, rbp, rdi, rsi, r12-r15
```


---

# CHAPTER 3: DATA MOVEMENT


## MOV and Memory Access

```nasm
section .data
    byte_val  db 42          ; define byte  (1 byte)
    word_val  dw 1000        ; define word  (2 bytes)
    dword_val dd 100000      ; define dword (4 bytes)
    qword_val dq 1000000000  ; define qword (8 bytes)
    my_array  dd 1, 2, 3, 4, 5
    my_str    db "Hello", 0  ; null-terminated string

section .bss
    buffer  resb 256         ; reserve 256 bytes
    count   resq 1           ; reserve 1 qword

section .text
global _start

_start:
    ; Register to register
    mov rax, 42
    mov rbx, rax

    ; Immediate to register
    mov rax, 100             ; 64-bit immediate
    mov eax, 100             ; 32-bit (zero-extends to 64)
    mov ax,  100             ; 16-bit
    mov al,  100             ; 8-bit

    ; Memory to register
    mov rax, [qword_val]     ; load qword from memory
    mov eax, [dword_val]
    mov ax,  [word_val]
    mov al,  [byte_val]

    ; Register to memory
    mov [qword_val], rax
    mov qword [buffer], 0    ; explicit size

    ; Effective address
    mov rax, [rsi + 8]       ; base + offset
    mov rax, [rsi + rcx*8]  ; base + index*scale
    mov rax, [rsi + rcx*4 + 16] ; base + index*scale + disp

    ; LEA — load effective address (compute address, not load)
    lea rax, [rsi + rcx*8]  ; rax = address (not value)
    lea rdi, [my_str]        ; pointer to string

    ; MOVZX — move with zero-extension
    movzx rax, byte [buffer]    ; zero-extend byte to rax
    movzx eax, word [word_val]

    ; MOVSX — move with sign-extension
    movsx rax, dword [dword_val]

    ; XCHG — exchange
    xchg rax, rbx

    ; PUSH / POP
    push rax
    push rbx
    pop  rcx     ; rcx = old rbx
    pop  rdx     ; rdx = old rax

    ; CMOV — conditional move
    cmp rax, rbx
    cmovg rax, rbx   ; move if greater
    cmovl rax, rbx   ; move if less
```


---

# CHAPTER 4: ARITHMETIC AND LOGIC


## Operations

```nasm
; ADD / SUB
add rax, rbx       ; rax += rbx
add rax, 10        ; rax += 10
sub rax, rbx       ; rax -= rbx
sub rax, [mem]

; INC / DEC
inc rax
dec rcx

; MUL / IMUL (unsigned/signed multiply)
; MUL: rdx:rax = rax * operand
mul rbx            ; rdx:rax = rax * rbx (128-bit result)
imul rbx           ; signed version
imul rax, rbx      ; rax *= rbx (2-op)
imul rax, rbx, 5   ; rax = rbx * 5 (3-op)

; DIV / IDIV (unsigned/signed divide)
; DIV: rax = rdx:rax / operand, rdx = remainder
xor rdx, rdx       ; clear rdx
mov rax, 100
mov rbx, 7
div rbx            ; rax = 14, rdx = 2

; NEG (negate, 2's complement)
neg rax            ; rax = -rax

; AND / OR / XOR / NOT
and rax, rbx
and rax, 0xFF      ; mask to 8 bits
or  rax, 0x01      ; set bit 0
xor rax, rax       ; rax = 0 (fast clear)
xor rax, 0xFF
not rax            ; bitwise not

; SHL / SHR / SAR / ROL / ROR
shl rax, 1         ; left shift 1 (multiply by 2)
shl rax, cl        ; shift by cl amount
shr rax, 1         ; right shift (unsigned)
sar rax, 1         ; arithmetic right shift (sign-extend)
rol rax, 4         ; rotate left
ror rax, 4         ; rotate right

; BSF / BSR — bit scan forward/reverse
bsf rcx, rax       ; rcx = index of lowest set bit
bsr rcx, rax       ; rcx = index of highest set bit

; POPCNT — count set bits
popcnt rax, rbx

; Flags (set by arithmetic)
; ZF: zero flag    (result = 0)
; SF: sign flag    (result < 0)
; OF: overflow flag (signed overflow)
; CF: carry flag   (unsigned overflow)
; PF: parity flag
```


---

# CHAPTER 5: CONTROL FLOW


## Jumps and Calls

```nasm
; CMP — compare (sets flags, no result stored)
cmp rax, rbx      ; rax - rbx (flags only)
cmp rax, 0
test rax, rax     ; rax & rax (check if zero)
test al, 1        ; check bit 0

; Unconditional jump
jmp label
jmp rax            ; indirect jump

; Conditional jumps (signed)
je  label  ; jump if equal (ZF=1)
jne label  ; jump if not equal (ZF=0)
jg  label  ; jump if greater (ZF=0 and SF=OF)
jge label  ; jump if greater or equal
jl  label  ; jump if less (SF!=OF)
jle label  ; jump if less or equal

; Conditional jumps (unsigned)
ja  label  ; jump if above (CF=0 and ZF=0)
jae label  ; jump if above or equal
jb  label  ; jump if below (CF=1)
jbe label  ; jump if below or equal

; Jump on flags
jz  label  ; jump if zero (ZF=1)
jnz label  ; jump if not zero
jc  label  ; jump if carry
jnc label  ; jump if no carry
js  label  ; jump if sign (negative)
jns label  ; jump if no sign (positive)
jo  label  ; jump if overflow
jno label  ; jump if no overflow

; LOOP — decrement RCX, jump if not zero
mov rcx, 10
.loop:
    ; do something
    loop .loop     ; rcx--; if rcx != 0: jump

; CALL / RET
call my_function
; ... return here
ret

my_function:
    push rbp
    mov  rbp, rsp
    sub  rsp, 32     ; allocate local space
    ; function body
    mov  rsp, rbp
    pop  rbp
    ret

; CALL with arguments (System V)
mov rdi, arg1
mov rsi, arg2
mov rdx, arg3
call my_func
; result in rax
```


---

# CHAPTER 6: PROCEDURES AND STACK


## Stack Frame Conventions

```nasm
; Standard function prologue/epilogue (x86-64 Linux)
my_function:
    ; Prologue
    push rbp
    mov  rbp, rsp
    sub  rsp, 48        ; reserve stack space (16-byte aligned)

    ; Save callee-saved registers if used
    push rbx
    push r12
    push r13

    ; Function body
    ; Parameters: rdi, rsi, rdx, rcx, r8, r9
    ; Return: rax

    ; Restore callee-saved registers
    pop r13
    pop r12
    pop rbx

    ; Epilogue
    mov rsp, rbp
    pop rbp
    ret

; Factorial (recursive)
factorial:
    push rbp
    mov  rbp, rsp
    push rbx
    mov  rbx, rdi       ; save n

    cmp  rdi, 1
    jle  .base_case

    dec  rdi
    call factorial       ; factorial(n-1)
    imul rax, rbx        ; n * factorial(n-1)
    jmp  .done

.base_case:
    mov  rax, 1

.done:
    pop  rbx
    pop  rbp
    ret

; Variadic function example
print_ints:              ; (count, v1, v2, ...)
    ; rdi=count, rsi=v1, rdx=v2, rcx=v3, r8=v4, r9=v5
    ; [rsp+8], [rsp+16], ... for v6+
```


---

# CHAPTER 7: SIMD AND FPU


## SSE/AVX Operations

```nasm
; SSE2 — 128-bit SIMD (4x float or 2x double or 16x byte, etc.)
section .data
    floats  dd 1.0, 2.0, 3.0, 4.0     ; 4 floats

section .text
    ; Load 128-bit (4 floats)
    movaps  xmm0, [floats]   ; aligned load
    movups  xmm0, [floats]   ; unaligned load

    ; Arithmetic (packed single-precision)
    addps   xmm0, xmm1       ; xmm0 += xmm1 (4 adds)
    subps   xmm0, xmm1
    mulps   xmm0, xmm1
    divps   xmm0, xmm1
    sqrtps  xmm0, xmm1       ; square root of 4 floats

    ; Scalar (one float)
    addss   xmm0, xmm1       ; add one float
    mulss   xmm0, xmm1

    ; Double precision
    addpd   xmm0, xmm1       ; 2 doubles
    addsd   xmm0, xmm1       ; 1 double

    ; Compare
    cmpeqps xmm0, xmm1       ; 4 equality comparisons

    ; Shuffle / permute
    shufps  xmm0, xmm1, 0b01001110

    ; AVX (256-bit, 8 floats)
    vmovaps  ymm0, [floats8]
    vaddps   ymm0, ymm0, ymm1
    vmulps   ymm2, ymm0, ymm1

; x87 FPU (legacy, still used for long double)
    fld     qword [val]       ; push to FP stack (st0)
    fld     qword [val2]      ; push (st0=val2, st1=val)
    fadd                      ; st0 = st0 + st1
    fstp    qword [result]    ; pop and store
    fmul    st0, st1
    fdiv    st0, st1
    fsqrt
    fabs
    fchs    ; change sign
```


---

# CHAPTER 8: SYSTEM CALLS AND MACROS


## Linux Syscalls and NASM Macros

```nasm
; Linux x86-64 syscall numbers (partial)
; sys_read   = 0    (fd, buf, count)
; sys_write  = 1    (fd, buf, count)
; sys_open   = 2    (pathname, flags, mode)
; sys_close  = 3    (fd)
; sys_exit   = 60   (error_code)
; sys_fork   = 57
; sys_mmap   = 9    (addr, len, prot, flags, fd, offset)
; sys_brk    = 12   (addr)

; Syscall: args in rdi,rsi,rdx,r10,r8,r9
;          return value in rax (negative = error)

; Write "Hello\n" to stdout
section .data
    msg db "Hello", 10
    msglen equ $ - msg

section .text
global _start

%macro write_string 2     ; NASM macro
    mov rax, 1
    mov rdi, 1
    mov rsi, %1
    mov rdx, %2
    syscall
%endmacro

%macro exit_code 1
    mov rax, 60
    mov rdi, %1
    syscall
%endmacro

_start:
    write_string msg, msglen
    exit_code 0

; NASM macro with local labels
%macro print_newline 0
    push rax
    push rdi
    push rsi
    push rdx
    mov  rax, 1
    mov  rdi, 1
    mov  rsi, .nl
    mov  rdx, 1
    syscall
    pop  rdx
    pop  rsi
    pop  rdi
    pop  rax
    jmp  .end
.nl: db 10
.end:
%endmacro

; Conditional assembly
%ifdef DEBUG
    %define LOG(x) mov rdi, x; call debug_print
%else
    %define LOG(x)
%endif
```
