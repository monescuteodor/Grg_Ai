# Brainfuck Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH BRAINFUCK


## Remarks

Brainfuck is an esoteric programming language created by Urban Müller in 1993. It operates on a tape of memory cells using only 8 commands. Despite extreme minimalism, Brainfuck is Turing complete. It is used for recreational programming and studying computation theory.

Tools: Many interpreters exist — `bf` (Linux), online interpreters (copy.sh/brainfuck, replit), or embed in Python.


## Hello World

```brainfuck
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
```

```
Output: Hello World!
```

### Minimal Python Interpreter

```python
def brainfuck(code, input_str=""):
    tape = [0] * 30000
    ptr = 0
    ip = 0
    input_idx = 0
    output = []

    # Build bracket map for fast jumps
    bracket_map = {}
    stack = []
    for i, cmd in enumerate(code):
        if cmd == '[':
            stack.append(i)
        elif cmd == ']':
            j = stack.pop()
            bracket_map[j] = i
            bracket_map[i] = j

    while ip < len(code):
        cmd = code[ip]
        if   cmd == '>': ptr += 1
        elif cmd == '<': ptr -= 1
        elif cmd == '+': tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-': tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.': output.append(chr(tape[ptr]))
        elif cmd == ',':
            if input_idx < len(input_str):
                tape[ptr] = ord(input_str[input_idx]); input_idx += 1
            else:
                tape[ptr] = 0
        elif cmd == '[' and tape[ptr] == 0: ip = bracket_map[ip]
        elif cmd == ']' and tape[ptr] != 0: ip = bracket_map[ip]
        ip += 1

    return ''.join(output)

print(brainfuck("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."))
```


---

# CHAPTER 2: THE 8 COMMANDS


## Command Reference

```
Command  Equivalent C        Description
-------  -----------         -----------
>        ptr++               Move pointer right
<        ptr--               Move pointer left
+        tape[ptr]++         Increment current cell (mod 256)
-        tape[ptr]--         Decrement current cell (mod 256)
.        putchar(tape[ptr])  Output current cell as ASCII
,        tape[ptr]=getchar() Read one character of input
[        while(tape[ptr]){   Jump past matching ] if cell is 0
]        }                   Jump back to matching [ if cell is nonzero
```

```brainfuck
// Memory model:
// [0][0][0][0][0]...   <-- initial tape (30,000 cells of 0)
//  ^
//  ptr starts here

// Basic operations:
+++          // cell[0] = 3
>++          // move right; cell[1] = 2
<.           // move left; print cell[0] as char (ASCII 3 = ETX, not printable)

// Set cell to 65 (ASCII 'A') and print:
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
.            // 65 +'s then .  → prints 'A'

// Shorter: 8*8+1 = 65
++++++++[>++++++++<-]>+.   // prints 'A'
// Explanation:
//   ++++++++         set cell[0]=8
//   [>++++++++<-]    loop 8 times: add 8 to cell[1], dec cell[0]
//   >+               cell[1] = 64+1 = 65
//   .                print 'A'
```


---

# CHAPTER 3: COMMON PATTERNS


## Programming Patterns

```brainfuck
// === ZERO A CELL ===
[-]          // decrement until 0

// === COPY cell[0] to cell[1] (destructive of cell[0]) ===
[->+<]       // while cell[0]!=0: dec cell[0], inc cell[1]

// === COPY without destroying (cell[0] -> cell[1], uses cell[2] as temp) ===
[->+>+<<]    // copy cell[0] to cell[1] and cell[2]
>>[-<<+>>]<< // move cell[2] back to cell[0]
// Result: cell[0] unchanged, cell[1] = original cell[0]

// === ADD cell[0] and cell[1], result in cell[1] ===
[->+<]       // move cell[0] into cell[1]

// === SUBTRACT cell[1] from cell[0], result in cell[0] ===
>[-<->]<     // while cell[1]: dec cell[1], dec cell[0] (oops, sub)
// Better:
>[<->-]      // while cell[1]: dec cell[0], dec cell[1]  → cell[0]-=cell[1]

// === MULTIPLY cell[0]*cell[1], result in cell[2] ===
// cell layout: [a][b][0][temp]
//              [0][1][2][3]
>[-<[->+>+<<]>>[-<<+>>]<]
// Destroys cell[0] and cell[1]

// === IF cell[0] THEN ... ===
[[-]...]     // execute ... then zero cell, skip if 0
// But be careful: this always consumes cell[0]

// === SIMPLE IF (destructive) ===
[            // if cell[0] != 0
    [-]      // zero the flag
    ...      // do something
]

// === NOT (logical, 0→1, nonzero→0) ===
// cell[0] = !cell[0]  uses cell[1] as temp
>+<          // cell[1]=1
[->-<]       // if cell[0]: zero cell[0] and cell[1]
>[<+>-]<     // move cell[1] to cell[0]
// Result: cell[0] was 0 → now 1; cell[0] was nonzero → now 0
```


---

# CHAPTER 4: I/O AND ASCII


## Working with ASCII

```brainfuck
// ASCII chart essentials:
// 10  = newline (\n)
// 32  = space
// 48  = '0'   (digits: 48-57)
// 65  = 'A'   (uppercase: 65-90)
// 97  = 'a'   (lowercase: 97-122)

// Print newline:
++++++++++.   // cell=10, print newline

// Print 'A' (65):
++++++++[>++++++++<-]>+.   // cell=65, print 'A'

// Print 'a' (97):
++++++++[>++++++++++++<-]>+.   // 8*12+1=97

// Print digit '0' (48):
++++++[>++++++++<-]>.   // 6*8=48

// Read a character and echo it back:
,.

// Read a character and print its value +1:
,+.

// Cat program (echo until EOF or 0):
,[.,]

// Print "BF":
++++++++[>+++++++++<-]>.   // 72='H'? No: 8*9=72='H'
// Let's do 'B' (66):
++++++++[>++++++++<-]>>++.   // 8*8=64, +2=66 'B'
// 'F' (70):
++++[>+++++++++++++++++++<-]>.   // 4*17.5 ... let's use:
+++++++++++[>++++++<-]>+++++.    // 11*6+5=71? close
// Simpler: reuse register
++++++++[>++++++++<-]>++.        // 64+2=66 'B'
<++++++++[>+<-]>++++++++.        // add 8 more to reach 'B'... 

// Cleaner BF Hello World breakdown:
// The classic program sets up multiple cells simultaneously
```


---

# CHAPTER 5: LOOPS AND ALGORITHMS


## Algorithmic Examples

```brainfuck
// === COUNTDOWN from N ===
// Print characters from ASCII N down to ASCII 1
// (assuming N already in cell[0])
// Example: countdown from 5
+++++          // cell[0] = 5
[.-]           // print cell[0] then decrement; loop until 0

// === COUNT UP and print digits '0'-'9' ===
++++++++++     // cell[0]=10 (loop counter)
>++++++++++++++++++++++++++++++++++++++++++++++++ // cell[1]=48='0'
<[>.<+<-]      // print cell[1], increment, dec counter

// === Fibonacci (simplified, print raw bytes) ===
// Cells: [0][a=1][b=1][temp]
>+>+           // a=1, b=1
<<             // back to cell[0]=0 (loop uses cell[0] as flag)
++++++++       // loop 8 times
[
    >>[-<+>]   // temp=b, b=0
    <[->+>+<<] // a→b and temp2, a=0
    >>[-<<+>>] // temp2→a
    <<<.       // print a (raw byte — not human-readable digits)
    -          // decrement loop counter
]

// === TRUTH MACHINE (if input is '1', print '1' forever; if '0', print '0') ===
,              // read char ('0'=48, '1'=49)
[              // if nonzero (i.e. not null, but really check for '1')
    ---------- // subtract 10
    ---------- // subtract 10
    ---------- // subtract 10
    ---------- // subtract 10
    -          // now cell = char - 49
    [          // if '1' (cell=0 means it was '1')
        +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        +++++++++++++++++++.  // reset to 49='1' and print... this doesn't loop forever
    ]          // 
]
.              // print whatever we have

// Cleaner truth machine:
,>++++++[<-------->-]<  // read char, subtract 48 ('0'=0, '1'=1)
[                       // if '1':
    >+<                 // set flag
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++.  // print '1'
]
[.] // if '0': print '0' once (cell still holds 48-48=0... actually print 0)
```


---

# CHAPTER 6: OPTIMIZATIONS AND TRANSLATION


## Brainfuck Optimization

```brainfuck
// === COMMON OPTIMIZATIONS ===

// Clear cell (idiom):
[-]            // standard clear — runs in O(n) where n=cell value

// Set cell to specific value:
[-]++++++      // clear then set to 6

// Multiplication by constant (set cell to N*M):
// Set to 30 = 6*5:
++++++[>+++++<-]>   // 6 loops of +5 = 30

// === EQUIVALENT C CODE ===
// BF:  +++[>++<-]>.
// C:   tape[0]=3; while(tape[0]){tape[0]--;tape[1]+=2;} putchar(tape[1]);

// === TRANSLATION TABLE ===
// BF  → C
// >   → ++ptr;
// <   → --ptr;
// +   → ++*ptr;
// -   → --*ptr;
// .   → putchar(*ptr);
// ,   → *ptr=getchar();
// [   → while(*ptr){
// ]   → }

// === C IMPLEMENTATION ===
/*
#include <stdio.h>
int main() {
    unsigned char tape[30000] = {0};
    unsigned char *ptr = tape;
    // paste BF as C operations
    return 0;
}
*/

// === OPTIMIZED INTERPRETER TRICKS ===
// 1. Precompute bracket jump table
// 2. Fold repeated +/- into single add
//    "++++++" → tape[ptr] += 6
// 3. Fold repeated >/<
//    ">>>>>>" → ptr += 6
// 4. Recognize common patterns:
//    [-]      → tape[ptr] = 0
//    [->+<]   → tape[ptr+1]+=tape[ptr]; tape[ptr]=0
```


---

# CHAPTER 7: ADVANCED PROGRAMS


## Complex Brainfuck Programs

```brainfuck
// === ROT13 (rotate letters by 13) ===
// Input: text, EOF=0
-,+[                // read char; if not 0
    -[              // not 1
        >>++++[>++++++++<-]    // set up 'A'=65
        <+<-[       // compare with char
            >>[               
                >%<           
                [>]           
                >[->]         
                <<[           
                    <]        
                <-            
            ]                 
        ]                     
    >                         
    >[<+>-]         
    <[              
        <           
        +++++++++++++
        [>+++++++++++++++<-]  
        >-          
        [<          
            [->]    
            >       
            [<+>-]  
            <-      
        ]           
    ]               
    >>              
    ]<,+]           
// ROT13 is complex in BF; here's a simpler approximation:

// === SIMPLE UPPERCASE to lowercase ===
,[.++++++++++++++++++++++++++++++++++,]
// reads chars, adds 32 to each (A→a), prints, reads next

// === REVERSE INPUT (limited buffer) ===
// Read up to 10 chars, print in reverse
>>>>>>>>>>,>,>,>,>,>,>,>,>,>,   // read 10 chars into cells 1-10
<.  <.  <.  <.  <.  <.  <.  <.  <.  <.  // print in reverse

// === PRINT NUMBER AS DECIMAL DIGITS ===
// Assumes number in cell[0], uses cells 1-4
// Works for 0-255
// cell[0]=number, cell[1-4]=workspace
// Divide by 100, 10, 1
>>++++++++++<<[->+>-[>+>>]>[+[-<+>]>+>>]<<<<<<]>>[-]>>>++++++++++<[->-[>+>>]>[+[-<+>]>+>>]<<<<<]>[-]>>[>++++++[-<++++++++>]<.<<+>+>[-]]<[<[->-<]++++++[->++++++++<]>.[-]]<<++++++[-<++++++++>]<.[-]<<[-<+>]<
```


---

# CHAPTER 8: ESOTERIC VARIANTS AND THEORY


## Brainfuck Variants and Theory

```
=== TURING COMPLETENESS ===
Brainfuck is Turing complete because:
1. Infinite tape = infinite memory
2. Conditional branching ([ ])
3. Arbitrary computation possible

Proof: BF can simulate a 2-tag system, which is Turing complete.


=== BRAINFUCK VARIANTS ===

Ook! — uses "Ook." "Ook?" "Ook!" instead of BF commands
  Ook. Ook? = >
  Ook? Ook. = <
  Ook. Ook. = +
  Ook! Ook! = -
  Ook! Ook. = .
  Ook. Ook! = ,
  Ook! Ook? = [
  Ook? Ook! = ]

Whitespace — uses spaces, tabs, newlines only

///  — uses only / \ and newline for string substitution

Chicken — uses only the word "chicken" repeated N times


=== COMPUTATIONAL COMPLEXITY ===
- BF programs can be exponentially longer than equivalent programs
- Shortest BF for "Hello World" is ~80 chars (optimized versions)
- BF is a "pathological" language: correct but impractical
- Time complexity: same as Turing machines (any computable function)


=== SELF-INTERPRETERS ===
A BF interpreter written in BF exists (Daniel Cristofani's quine-relay)
Demonstrates BF is powerful enough for meta-programming


=== GOLF (Shortest Programs) ===
Print 'A' (65):
  --[----->+<]>.        (12 chars) 65=13*5
  
Print newline (10):
  ++++++++++.           (11 chars)

Print 0-9:
  ++++++++++[>++++++++++<-]>[>+<-]+++++[<++++++>-]<.>>.   (complex)

Echo input forever:
  ,[.,]                 (5 chars — minimal cat program)

Print empty string (do nothing):
  (empty program)       (0 chars)


=== MEMORY LAYOUT CONVENTIONS ===
Common register conventions:
  cell[0]  — current working register / loop counter
  cell[1]  — secondary register / accumulator
  cell[2+] — scratch space / string buffer

Stack simulation: use a portion of tape as a stack
  Move right to push, left to pop
  Keep track of base pointer

String storage:
  Store chars in consecutive cells
  Use 0 as terminator
  Process with loop that checks for 0


=== DEBUGGING TECHNIQUES ===
1. Add debug output: insert . at key points to print cell values
2. Use an interpreter with memory visualization
3. Trace execution step by step
4. Use comments (any non-command char is ignored)
5. Label cells mentally: [counter][temp1][temp2][output]

=== ONLINE RESOURCES ===
- copy.sh/brainfuck — web interpreter
- esolangs.org/wiki/Brainfuck — community wiki
- Brainfuck constants: esolangs.org/wiki/Brainfuck_constants
```
