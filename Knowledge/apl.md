# APL Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH APL


## Remarks

APL (A Programming Language) was created by Kenneth Iverson in 1962 and published in 1966. It uses a unique set of special mathematical symbols for array operations. APL is array-oriented, uses right-to-left evaluation, and can express complex algorithms in very few characters.

Implementations: Dyalog APL (most popular, commercial/free for personal use), GNU APL (open source), ngn/apl (web-based), APLX.


## Hello World

```apl
      'Hello, World!'
Hello, World!

      ⎕←'Hello, APL!'
Hello, APL!

⍝ APL uses ⍝ for comments (looks like a lamp)
⍝ ⎕← prints to output
⍝ Everything evaluates right-to-left
```

```bash
# Dyalog APL (Linux/Mac/Windows)
dyalog
# Then type expressions at the prompt

# ngn/apl (browser)
# https://ngn.github.io/apl/web/
```


---

# CHAPTER 2: PRIMITIVES AND OPERATORS


## APL Symbol Reference

```apl
⍝ === ARITHMETIC ===
3 + 4           ⍝ 7  (add)
10 - 3          ⍝ 7  (subtract)
3 × 4           ⍝ 12 (multiply, × not *)
10 ÷ 4          ⍝ 2.5 (divide, ÷ not /)
2 * 8           ⍝ 256 (power, * is exponent)
|¯5             ⍝ 5  (absolute value, | is monadic magnitude)
⌊3.7            ⍝ 3  (floor)
⌈3.2            ⍝ 4  (ceiling)
7 | 3           ⍝ 1  (residue/modulo: 7 mod 3)

⍝ === COMPARISON ===
3 < 5           ⍝ 1
3 > 5           ⍝ 0
3 = 3           ⍝ 1
3 ≠ 4           ⍝ 1
3 ≤ 3           ⍝ 1
3 ≥ 4           ⍝ 0

⍝ === BOOLEAN ===
1 ∧ 0           ⍝ 0  (AND)
1 ∨ 0           ⍝ 1  (OR)
~1              ⍝ 0  (NOT)
1 ⍲ 1           ⍝ 0  (NAND)
0 ⍱ 0           ⍝ 1  (NOR)

⍝ === RIGHT-TO-LEFT EVALUATION ===
2 + 3 × 4       ⍝ 14  (not 20! evaluated as 2+(3×4))
(2 + 3) × 4     ⍝ 20  (parentheses override)
```


---

# CHAPTER 3: ARRAYS


## APL Array Operations

```apl
⍝ === CREATING ARRAYS ===
1 2 3 4 5              ⍝ vector [1,2,3,4,5]
⍳5                     ⍝ iota: 1 2 3 4 5 (index generator)
⍳0                     ⍝ empty vector
2 3⍴⍳6                 ⍝ 2×3 matrix: reshape ⍳6 into 2 rows 3 cols
                       ⍝   1 2 3
                       ⍝   4 5 6

⍝ === SHAPE AND RANK ===
⍴ 1 2 3 4 5            ⍝ shape: 5  (vector of length 5)
⍴ 2 3⍴⍳6              ⍝ shape: 2 3
⍴⍴ 1 2 3               ⍝ rank: 1  (⍴⍴ gives number of dimensions)
⍴⍴ 2 3⍴⍳6             ⍝ rank: 2

⍝ === INDEXING ===
v ← 10 20 30 40 50     ⍝ assign vector
v[3]                   ⍝ 30  (1-indexed!)
v[2 4]                 ⍝ 20 40  (multiple indices)

m ← 3 3⍴⍳9            ⍝ 3×3 matrix
m[2;3]                 ⍝ 6  (row 2, col 3)
m[2;]                  ⍝ 4 5 6  (entire row 2)
m[;1]                  ⍝ 1 4 7  (entire col 1)

⍝ === ARITHMETIC ON ARRAYS ===
v + 1                  ⍝ 11 21 31 41 51  (scalar extends)
v × 2                  ⍝ 20 40 60 80 100
v + v                  ⍝ 20 40 60 80 100
v1 ← 1 2 3
v2 ← 4 5 6
v1 + v2                ⍝ 5 7 9

⍝ === REDUCTION (/) ===
+/1 2 3 4 5            ⍝ 15  (sum: insert + between all)
×/1 2 3 4 5            ⍝ 120 (product)
⌈/3 1 4 1 5 9 2 6      ⍝ 9   (maximum)
⌊/3 1 4 1 5 9 2 6      ⍝ 1   (minimum)

⍝ === SCAN (\) ===
+\1 2 3 4 5            ⍝ 1 3 6 10 15  (running sum)
×\1 2 3 4 5            ⍝ 1 2 6 24 120 (running product)
⌈\3 1 4 1 5 9          ⍝ 3 3 4 4 5 9  (running max)
```


---

# CHAPTER 4: FUNCTIONS


## Defining and Using Functions

```apl
⍝ === DFNS (Direct Functions, modern style) ===
double ← {⍵ × 2}           ⍝ ⍵ = right argument
double 5                    ⍝ 10

add ← {⍺ + ⍵}              ⍝ ⍺ = left argument
3 add 4                     ⍝ 7

⍝ Conditional in dfns (if:true⋄false)
abs ← {⍵ < 0: -⍵ ⋄ ⍵}     ⍝ if ⍵<0 return -⍵ else ⍵
abs ¯7                      ⍝ 7
abs 5                       ⍝ 5

⍝ Recursive dfn (∇ self-reference)
factorial ← {⍵ ≤ 1: 1 ⋄ ⍵ × ∇ ⍵-1}
factorial 5                 ⍝ 120
factorial¨ 1 2 3 4 5        ⍝ 1 2 6 24 120  (apply to each)

⍝ Fibonacci
fib ← {⍵ ≤ 1: ⍵ ⋄ (∇ ⍵-1) + ∇ ⍵-2}
fib 10                      ⍝ 55

⍝ === TACIT/POINT-FREE STYLE ===
mean ← +÷≢               ⍝ sum ÷ count (fork)
mean 1 2 3 4 5            ⍝ 3

double ← 2∘×              ⍝ partial application: 2×
double 5                  ⍝ 10

⍝ === OPERATORS ===
⍝ ¨ (each): apply to each element
⍝ / (reduce): fold with function
⍝ \ (scan): running fold
⍝ ∘ (compose): function composition
⍝ ⍨ (commute/selfie): swap args or repeat

2 +⍨ 3                    ⍝ 5  (same as 3 + 2, swapped)
+⍨ 5                      ⍝ 10 (5+5, apply to self)
(⊢-⌊)÷1∘⌈               ⍝ complex tacit expression (fractional part)

⍝ Atop (f⍤g: apply g then f)
⌈⍤÷/ 7 3                  ⍝ ceiling of 7÷3 = 3

⍝ Rank operator ⍤n (apply to rank-n subarrays)
+/⍤1 ⊢ 2 3⍴⍳6            ⍝ row sums: 6 15
```


---

# CHAPTER 5: ARRAY MANIPULATION


## Transforming Arrays

```apl
⍝ === SELECTION ===
v ← 10 20 30 40 50
1 0 1 0 1/v              ⍝ 10 30 50  (compress/select)
(v>25)/v                 ⍝ 30 40 50  (boolean select)
{⍵/⍨⍵>25} v             ⍝ same, dfn style

⍝ === TAKE AND DROP ===
3↑1 2 3 4 5              ⍝ 1 2 3    (take first 3)
¯2↑1 2 3 4 5             ⍝ 4 5      (take last 2)
2↓1 2 3 4 5              ⍝ 3 4 5    (drop first 2)
¯3↓1 2 3 4 5             ⍝ 1 2      (drop last 3)

⍝ === RESHAPE AND RAVEL ===
,m                        ⍝ ravel: matrix to vector
3 4⍴v                    ⍝ reshape v to 3×4 (recycle if needed)

⍝ === ROTATE AND REVERSE ===
⌽1 2 3 4 5               ⍝ 5 4 3 2 1  (reverse)
2⌽1 2 3 4 5              ⍝ 3 4 5 1 2  (rotate left by 2)
¯1⌽1 2 3 4 5             ⍝ 5 1 2 3 4  (rotate right by 1)
⊖m                        ⍝ flip matrix vertically
2⊖m                       ⍝ rotate rows

⍝ === TRANSPOSE ===
⍉m                        ⍝ transpose matrix

⍝ === SORT ===
⍋3 1 4 1 5 9 2 6         ⍝ 2 4 7 1 3 5 8 6  (grade up: sort indices)
⍒3 1 4 1 5 9 2 6         ⍝ 6 8 5 3 1 7 4 2  (grade down)
v ← 3 1 4 1 5 9
v[⍋v]                    ⍝ 1 1 3 4 5 9  (sort ascending)
v[⍒v]                    ⍝ 9 5 4 3 1 1  (sort descending)

⍝ === MEMBERSHIP AND SEARCH ===
3 ∊ 1 2 3 4 5            ⍝ 1  (member of)
1 2 6 ∊ 1 2 3 4 5        ⍝ 1 1 0
1 2 3 ⍳ 2                 ⍝ 2  (index of 2 in vector)
'AEIOU' ⍳ 'HELLO'        ⍝ 6 1 3 3 5  (positions)

⍝ === NESTING ===
nested ← (1 2 3)(4 5)(6)
≡nested                   ⍝ depth: 2
⊃nested                   ⍝ first item: 1 2 3
↑nested                   ⍝ mix: 1 2 3 / 4 5 0 / 6 0 0  (pad with 0)
```


---

# CHAPTER 6: STRING OPERATIONS


## Working with Text

```apl
⍝ === STRINGS (character vectors) ===
s ← 'Hello, World!'
≢s                         ⍝ 13  (length, ≢ is tally)
s[1]                       ⍝ 'H'
s[1 2 3]                   ⍝ 'Hel'
3↑s                        ⍝ 'Hel'
¯6↑s                       ⍝ 'World!'
⌽s                         ⍝ '!dlroW ,olleH'

⍝ Upcase/downcase (in Dyalog)
1⎕C s                      ⍝ uppercase: 'HELLO, WORLD!'
0⎕C s                      ⍝ lowercase: 'hello, world!'

⍝ Search
s⍳'W'                      ⍝ 8  (position of 'W')
'lo' ⍷ s                   ⍝ 0 0 0 1 0 0 ...  (find pattern)

⍝ Split on delimiter (Dyalog: ⊆)
words ← ' '(≠⊆⊢)'Hello World APL'
⍝ result: 'Hello' 'World' 'APL'

⍝ Join with separator
⊃,/' ',¨words              ⍝ rejoin with spaces

⍝ String formatting (⍕)
⍕3.14                      ⍝ '3.14'
⍕42                        ⍝ '42'
⍕1 2 3                     ⍝ '1 2 3'

⍝ Evaluate string (⍎)
⍎'1+2'                     ⍝ 3
⍎'⍳5'                      ⍝ 1 2 3 4 5

⍝ String comparison
'abc' = 'abc'              ⍝ 1 1 1
'abc' ≡ 'abc'              ⍝ 1  (match: entire arrays equal)
'abc' ≡ 'abd'              ⍝ 0
```


---

# CHAPTER 7: SYSTEM FUNCTIONS AND I/O


## APL System Interface

```apl
⍝ === SYSTEM VARIABLES ===
⎕IO ← 0        ⍝ index origin: 0-indexed (default 1)
⎕IO ← 1        ⍝ 1-indexed (traditional)
⎕PP ← 10       ⍝ print precision (decimal places)
⎕PW ← 80       ⍝ print width (columns)
⎕TS            ⍝ timestamp: year month day hour min sec ms
⎕AN            ⍝ account name (username)

⍝ === I/O ===
⎕ ← 'Print this'          ⍝ print to output
x ← ⎕                     ⍝ read from input
⍞ ← 'Prompt: '            ⍝ print without newline
x ← ⍞                     ⍝ read without echo

⍝ === FILE I/O (Dyalog) ===
⍝ Using ⎕NGET / ⎕NPUT
(content encoding newline) ← ⎕NGET 'file.txt' 1
⎕NPUT 'output.txt' 1 ⊢ content encoding

⍝ Using native file tie numbers
tie ← 'data.txt' ⎕NTIE 0         ⍝ tie file
data ← ⎕NREAD tie 80 (⎕NSIZE tie) 0  ⍝ read all
⎕NUNTIE tie                       ⍝ release tie

⍝ === WORKSPACE ===
)VARS          ⍝ list defined names
)FNS           ⍝ list functions
)SAVE ws       ⍝ save workspace
)LOAD ws       ⍝ load workspace
)CLEAR         ⍝ clear workspace
)OFF           ⍝ exit APL

⍝ === NAMESPACES (Dyalog) ===
ns ← ⎕NS ''              ⍝ create namespace
ns.x ← 42
ns.fn ← {⍵+1}
ns.fn ns.x               ⍝ 43

⍝ === ERROR HANDLING ===
:Trap 0                  ⍝ catch all errors
    result ← risky_fn ⍵
:Case 11                 ⍝ VALUE ERROR
    result ← 0
:Else
    result ← ¯1
:EndTrap

⍝ === PERFORMANCE ===
]runtime '⍳1000000'      ⍝ benchmark expression
]trace fn                 ⍝ execution trace
```


---

# CHAPTER 8: CLASSIC APL IDIOMS


## Famous One-Liners and Algorithms

```apl
⍝ === CLASSIC APL ONE-LINERS ===

⍝ Sum of integers 1 to N
+/⍳100                        ⍝ 5050

⍝ Factorial
×/⍳10                         ⍝ 3628800

⍝ Fibonacci sequence (first N)
{+\∨\0,⍵↑1}                  ⍝ or:
{1 1{+\⌽⍺,⍵}/⍳⍵}            ⍝ generates N fibonacci numbers

⍝ Prime sieve (Sieve of Eratosthenes)
{(~R∊R∘.×R)/R←1↓⍳⍵}         ⍝ primes up to ⍵
{(~v∊v∘.×v)/v←1↓⍳⍵} 50      ⍝ primes to 50

⍝ Matrix determinant (for small matrices)
det ← {1=≢⍵:⊃⍵ ⋄ +/⍵[1;]×(¯1*1+⍳≢⍵)×∇⍵[1+⍳¯1+≢⍵;]}

⍝ Inner product (matrix multiply)
A +.× B                       ⍝ dot product (generalized inner product)
A ∧.= B                       ⍝ row-wise equality test

⍝ Outer product
∘.×⍨⍳5                       ⍝ 5×5 multiplication table
∘.+⍨⍳5                       ⍝ 5×5 addition table

⍝ Conway's Game of Life (classic one-liner)
life ← {↑1 ⍵∨.∧3 4=+/,¯1 0 1∘.⊖¯1 0 1∘.⌽⊂⍵}

⍝ Longest common subsequence length
lcs ← {+/∊v∧.(=\v←(≢⍺)>⌈\⍺∘.=⍵)/1}

⍝ Sort (using grade up)
sort ← {⍵[⍋⍵]}
sort 3 1 4 1 5 9 2 6          ⍝ 1 1 2 3 4 5 6 9

⍝ Unique elements (nub)
∪3 1 4 1 5 9 2 6              ⍝ 3 1 4 5 9 2 6

⍝ Group by first occurrence
{⍵/⍨⍵=∪⍵}                    ⍝ keep first occurrence of each

⍝ Polynomial evaluation (Horner's method)
poly ← {⍺+.×∘.(⍵*⊢)⍳1+≢⍺}   ⍝ coefficients ⍺ at point ⍵

⍝ Base conversion
10 ⊥ 1 0 1 0 1                ⍝ from binary: 21
2 ⊤ 42                        ⍝ to binary: 0 0 1 0 1 0 1 0

⍝ Date calculations
+/31 28 31 30 31 30 31 31 30 31 30 31   ⍝ days in year: 365

⍝ === KEY SYMBOLS SUMMARY ===
⍝ ← assignment      ⍝ comment      ⎕ system/output
⍝ ⍳ iota (range)    ⍴ shape/reshape  ⌽ rotate/reverse
⍝ ⊖ flip up/down    ⍉ transpose    ⊂ enclose (nest)
⍝ ⊃ disclose/first  ∊ member/enlist  ⍷ find pattern
⍝ ↑ take/mix        ↓ drop/split   / compress/reduce
⍝ \ expand/scan     ¨ each         ∘ compose/outer product
⍝ ⍨ commute/selfie  ⌿ reduce along first axis
⍝ ⍤ atop/rank       ∧ AND          ∨ OR
⍝ ⌊ floor/min       ⌈ ceiling/max  ≡ match (deep equal)
⍝ ≢ tally (≠count)  ⍋ grade up     ⍒ grade down
⍝ ⊤ encode          ⊥ decode       +.× inner product
```
