# J Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH J


## Remarks

J is an array programming language created by Kenneth Iverson and Roger Hui in 1990 as a successor to APL. J uses only ASCII characters (unlike APL's special symbols) and features a rich vocabulary of single-character and digraph primitives. J uses tacit (point-free) programming extensively.

Tools: `jconsole` (command line), `jqt` (Qt GUI IDE), J playground at jsoftware.com.


## Hello World

```j
   'Hello, World!'
Hello, World!

   'Hello, J!' 1!:2 <'/dev/stdout'

   echo 'Hello, J!'
Hello, J!

   NB. J uses NB. for comments (nota bene)
   NB. Everything evaluates right-to-left
   NB. Monad = one argument (right), Dyad = two arguments
```

```bash
# Run J script
jconsole script.ijs

# Interactive session
jconsole

# Or use the J IDE (jqt)
```


---

# CHAPTER 2: BASIC SYNTAX AND TYPES


## J Primitives and Types

```j
NB. === NUMERIC TYPES ===
   42             NB. integer
   3.14           NB. float
   2r3            NB. rational (2/3 exactly)
   3j4            NB. complex (3+4i)
   1b1010         NB. boolean array (1 0 1 0)

NB. === ARITHMETIC ===
   3 + 4          NB. 7
   10 - 3         NB. 7
   3 * 4          NB. 12
   10 % 4         NB. 2.5  (% is divide, not modulo)
   2 ^ 8          NB. 256  (power)
   | _5           NB. 5    (absolute value, | monadic)
   <. 3.7         NB. 3    (floor)
   >. 3.2         NB. 4    (ceiling)
   10 | 3         NB. 1    (residue/modulo: 3 mod 10... wait:)
   NB. Actually: x|y = y mod x
   7 | 3          NB. 3    (3 mod 7 = 3)
   7 | 10         NB. 3    (10 mod 7 = 3)

NB. === NEGATIVE NUMBERS ===
   _5             NB. negative 5 (underscore prefix)
   _3.14          NB. negative 3.14
   - 5            NB. negate 5 = _5
   5 - 3          NB. 2

NB. === COMPARISONS ===
   3 < 5          NB. 1
   3 > 5          NB. 0
   3 = 3          NB. 1
   3 ~: 4         NB. 1  (not equal)
   3 <: 3         NB. 1  (less-or-equal)
   3 >: 4         NB. 0  (greater-or-equal)

NB. === BOOLEAN LOGIC ===
   1 *. 0         NB. 0  (AND: *.)
   1 +. 0         NB. 1  (OR:  +.)
   -. 1           NB. 0  (NOT: -.)
```


---

# CHAPTER 3: ARRAYS AND OPERATIONS


## J Arrays

```j
NB. === CREATING ARRAYS ===
   1 2 3 4 5              NB. integer vector
   i. 5                   NB. 0 1 2 3 4  (iota, 0-indexed!)
   i. 10                  NB. 0 1 2 3 4 5 6 7 8 9
   i. _5                  NB. 0 _1 _2 _3 _4  (negative iota)

NB. === SHAPE ===
   $  1 2 3 4 5            NB. 5  (shape: vector of length 5)
   $$ 1 2 3 4 5            NB. 1  (rank: number of dimensions)
   # 1 2 3 4 5             NB. 5  (tally: count of items)

NB. === RESHAPE ===
   2 3 $ i. 6              NB. 2x3 matrix:
                           NB.  0 1 2
                           NB.  3 4 5
   4 $ 1 2 3               NB. 1 2 3 1  (recycle)

NB. === MATRIX ===
   m =: 3 3 $ i. 9
   m
NB.  0 1 2
NB.  3 4 5
NB.  6 7 8

NB. === INDEXING (0-based) ===
   v =: 10 20 30 40 50
   v { v                   NB. same (identity)
   2 { v                   NB. 30  (element at index 2)
   0 2 4 { v               NB. 10 30 50

NB. === ARITHMETIC ON ARRAYS ===
   v + 1                   NB. 11 21 31 41 51  (scalar broadcast)
   v * 2                   NB. 20 40 60 80 100
   1 2 3 + 4 5 6           NB. 5 7 9

NB. === REDUCTION (/) ===
   +/ 1 2 3 4 5            NB. 15  (sum)
   */ 1 2 3 4 5            NB. 120 (product)
   >./  3 1 4 1 5          NB. 5   (maximum)
   <./  3 1 4 1 5          NB. 1   (minimum)
   #/ 5 5 5                NB. 5^(5^5) (right-to-left!)

NB. === SCAN (\) ===
   +\ 1 2 3 4 5            NB. 1 3 6 10 15  (running sum)
   *\ 1 2 3 4 5            NB. 1 2 6 24 120
```


---

# CHAPTER 4: VERBS (FUNCTIONS)


## Defining Functions in J

```j
NB. === EXPLICIT DEFINITION ===
   double =: 3 : '2 * y'            NB. monad (one arg: y)
   double 5                          NB. 10
   double 1 2 3                      NB. 2 4 6

   add =: 4 : 'x + y'               NB. dyad (two args: x, y)
   3 add 4                           NB. 7

NB. === MULTI-LINE DEFINITION ===
   factorial =: 3 : 0
     if. y <: 1 do. 1
     else. y * factorial y - 1
     end.
   )
   factorial 5                        NB. 120

NB. === CONJUNCTIONS AND ADVERBS ===
   NB. / is an adverb (modifies verb)
   +/ 1 2 3                           NB. 6  (sum via reduce)
   
   NB. @: is composition (f @: g = f(g(x)))
   |@:- 5                             NB. 5  (abs of negate)

NB. === TACIT PROGRAMMING (point-free) ===
   NB. Forks: (f g h) x = (f x) g (h x)
   mean =: +/ % #                     NB. sum ÷ count
   mean 1 2 3 4 5                     NB. 3

   NB. Hooks: (f g) x = x f (g x)
   sumsq =: +/ @: *:                  NB. sum of squares
   sumsq 1 2 3 4                      NB. 30

NB. === COMMON TACIT PATTERNS ===
   NB. Identity
   ]  42                              NB. 42
   [  42                              NB. 42 (same for monad)
   3 [ 4                              NB. 3  (return left)
   3 ] 4                              NB. 4  (return right)

   NB. Self-reference
   +: 5                               NB. 10  (double: +: = 2*)
   *: 5                               NB. 25  (square: *: = ^2)
   %: 25                              NB. 5   (sqrt: %: = ^0.5)
   !. 5                               NB. 120 (factorial)
   !  5                               NB. 120 (same)

NB. === GERUND (list of verbs) ===
   verbs =: +`*`-                     NB. list of 3 verbs
   3 (+`* `:0) 4                      NB. apply each: 7 12 _1
```


---

# CHAPTER 5: CONTROL FLOW


## J Control Structures

```j
NB. === IF/ELSE ===
   classify =: 3 : 0
     if. y > 0 do. 'positive'
     elseif. y = 0 do. 'zero'
     else. 'negative'
     end.
   )
   classify 5      NB. 'positive'
   classify 0      NB. 'zero'
   classify _3     NB. 'negative'

NB. === WHILE ===
   collatz =: 3 : 0
     count =: 0
     while. y ~: 1 do.
       if. 0 = 2 | y do.
         y =: y % 2
       else.
         y =: 1 + 3 * y
       end.
       count =: count + 1
     end.
     count
   )
   collatz 27      NB. 111

NB. === FOR ===
   sumlist =: 3 : 0
     total =: 0
     for_n. y do.
       total =: total + n
     end.
     total
   )
   sumlist 1 2 3 4 5    NB. 15

NB. === SELECT (CASE) ===
   dayname =: 3 : 0
     select. y
       case. 0 do. 'Sunday'
       case. 1 do. 'Monday'
       case. 2 do. 'Tuesday'
       case. 3 4 5 do. 'Midweek'
       case. 6 do. 'Saturday'
       fcase. do. 'Invalid'
     end.
   )
   dayname 3           NB. 'Midweek'

NB. === TRY/CATCH ===
   safe_sqrt =: 3 : 0
     try.
       if. y < 0 do. error 'negative input' end.
       %: y
     catch.
       _1
     end.
   )
   safe_sqrt 16        NB. 4
   safe_sqrt _4        NB. _1
```


---

# CHAPTER 6: STRINGS AND BOXING


## Text and Heterogeneous Data

```j
NB. === STRINGS (character arrays) ===
   s =: 'Hello, World!'
   # s                     NB. 13  (length)
   s { ~ 0                 NB. 'H'  (first char)
   0 3 { s                 NB. 'Hel'... no: 'H' 'l' = 'Hl'
   3 {. s                  NB. 'Hel'  (take 3)
   _6 {. s                 NB. 'orld!'  (take last 6)

   NB. String search
   'l' I: s                NB. indices where 'l' appears
   'lo' E. s               NB. boolean: where 'lo' starts

   NB. Upcase/downcase
   toupper =: 3 : '(97+i.26) (I.@:e. 65+i.26)} y'  NB. complex
   NB. Simpler in J 8+:
   'hello' (9!:33) 'Hello World'   NB. not standard

   NB. Split by delimiter
   cuts =: ' ' = s
   NB. use ;: for word splitting
   ;: 'Hello World APL J'  NB. boxed words

NB. === BOXING (<) ===
   NB. Box wraps any value in a uniform container
   b1 =: < 1 2 3           NB. box containing 1 2 3
   b2 =: < 'hello'         NB. box containing string
   b3 =: < 42              NB. box containing scalar

   NB. Unbox (>)
   > b1                    NB. 1 2 3

   NB. Heterogeneous list (all elements boxed)
   mixed =: 1 2 3 ; 'hello' ; 42
   NB. Same as: (<1 2 3) , (<'hello') , (<42)

   NB. Access boxed element
   0 { mixed               NB. box of 1 2 3
   > 0 { mixed             NB. 1 2 3 (unboxed)

   NB. Apply to each boxed item
   # each mixed            NB. 3 5 1  (length of each item)

NB. === FORMATTING ===
   ": 42                   NB. format number as string '42'
   ": 3.14                 NB. '3.14'
   ": 1 2 3                NB. '1 2 3'
   NB. With format spec:
   '%.2f' 8!:2 3.14159     NB. '3.14'
```


---

# CHAPTER 7: ADVANCED OPERATIONS


## J Power Features

```j
NB. === RANK OPERATOR (") ===
   NB. Apply verb at specified rank
   + " 0  NB. add atoms (rank 0 = scalar)
   + " 1  NB. add vectors (rank 1)
   
   NB. Example: outer product
   (*"0)/~ i. 5            NB. 5x5 multiplication table
   NB. or:
   (i.5) */ (i.5)

NB. === UNDER OPERATOR (&.) ===
   NB. Apply f under g: g^-1 ∘ f ∘ g
   *: &. %: 4              NB. sqrt, square, sqrt back = 2 (identity)
   +/ &. (10&^) 10 100 1000 NB. sum in log domain

NB. === POWER CONJUNCTION (^:) ===
   NB. Apply verb N times
   (+ 1)^:5 ] 0            NB. 5  (add 1 five times to 0)
   (*2)^:10 ] 1            NB. 1024 (double 10 times)
   
   NB. Fixed point (^:_)
   ({.~ <.) ^:_ 1.618      NB. converges to fixed point
   
   NB. Apply while condition (^:verb)
   (<&100)^:_ 1            NB. double while <100... only works with self-ref

NB. === SPARSE ARRAYS (J 9+) ===
   NB. Large sparse matrix
   sm =: 2 2 3 $ 0         NB. start dense
   NB. $. for sparse representation

NB. === MATRIX OPERATIONS ===
   A =: 2 2 $ 1 2 3 4
   %. A                    NB. matrix inverse (% monadic extended)
   A (%. @:]) A            NB. solve linear system Ax=b
   (+/ . *) /~ A           NB. dot product approach
   A mp B =: +/ . * A      NB. matrix multiply

NB. === SORTING ===
   v =: 3 1 4 1 5 9 2 6
   /: v                    NB. grade up (sort indices ascending)
   \: v                    NB. grade down
   (/: v) { v              NB. sorted ascending: 1 1 2 3 4 5 6 9
   (\: v) { v              NB. sorted descending

NB. === INNER/OUTER PRODUCT ===
   1 2 3 +/ . * 4 5 6      NB. dot product: 32
   (i.3) */ (i.3)          NB. outer product: 3x3 table

NB. === KEY (/.) ===
   NB. Group-by using key
   (+/ /. ~) 1 2 1 3 2 1   NB. sum by unique value
   NB. Result: for each unique value, sum of occurrences
```


---

# CHAPTER 8: IDIOMS AND PRACTICAL EXAMPLES


## J One-Liners and Algorithms

```j
NB. === CLASSIC J IDIOMS ===

NB. Sum of 1..N
+/ i. 101                  NB. 5050

NB. Factorial
*/ 1 + i. 10               NB. 3628800
! 10                       NB. same

NB. Fibonacci (first N)
fib =: (0 1 {~ [: i. #) + (+ / @: |.) ^: (i. ]) NB. complex
NB. Simpler:
fib =: 3 : '>(+`]/@,&.>^:(y-1)) 0 1'

NB. Primes (sieve)
isprime =: 3 : '+/ y = p * p */ p =: 2 + i. y - 1' NB. slow
NB. Better sieve:
sieve =: 3 : 0
  b =: (y+1) $ 1
  b =: 0 1 } b
  for_i. 2 + i. <. %: y do.
    if. i { b do.
      b =: 0 (i * 1 + i. <. y % i) } b
    end.
  end.
  I. b
)
sieve 50                   NB. 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47

NB. Mean
(+/ % #) 1 2 3 4 5         NB. 3

NB. Standard deviation
std =: [: %: [: +/ [: *: ] - +/ % #
std 2 4 4 4 5 5 7 9        NB. 2

NB. Binary to decimal
2 #. 1 0 1 1               NB. 11  (#. base conversion)

NB. Decimal to binary
#: 42                      NB. 0 0 1 0 1 0 1 0  (antibase)

NB. Anagram check
anagram =: -: &(/:~)       NB. same when sorted
'listen' anagram 'silent'  NB. 1

NB. Palindrome check
palindrome =: -: |.
palindrome 1 2 3 2 1       NB. 1
palindrome 1 2 3           NB. 0

NB. Transpose
|: 2 3 $ i. 6              NB. transposed matrix

NB. Outer product table
*/~ i. 5                   NB. 5x5 multiplication table

NB. Power set
powerset =: #: i.@(2&^)@#  NB. generates boolean membership matrix
(powerset 1 2 3) #"1 (,1 2 3)  NB. not quite right, but concept

NB. === LOADING AND SAVING ===
   load 'math/fftw'        NB. load J addon
   load '~/myfile.ijs'     NB. load script
   save '~/myscript.ijs'   NB. save workspace functions
   
NB. === DEBUGGING ===
   13!:0 ]                 NB. enable debug mode
   13!:8 ]                 NB. print execution trace
   
NB. === PERFORMANCE ===
   time =: 6!:2            NB. time verb
   time 'NB. +/ i. 1000000'
   
   NB. Use immutable locals (=.) vs globals (=:)
   fn =: 3 : 0
     local =. y * 2    NB. local (=.)
     global =: local   NB. global (=:)
     local
   )
```
