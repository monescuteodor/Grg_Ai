# Scheme Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH SCHEME


## Remarks

Scheme is a minimalist dialect of Lisp with lexical scoping, proper tail recursion, first-class continuations, and hygienic macros. It is specified by the R5RS, R6RS, and R7RS standards. Known for its elegant simplicity and use in computer science education (SICP).

Implementations: Racket (most featureful), MIT Scheme, Guile, Chicken Scheme, Chez Scheme.


## Hello World

```scheme
; hello.scm
(display "Hello, World!")
(newline)

; With format (Racket/Guile)
(printf "Hello, ~a!\n" "Scheme")

; Run:
; racket hello.scm
; guile hello.scm
; mit-scheme --quiet < hello.scm
```


---

# CHAPTER 2: VALUES AND TYPES


## Types and Expressions

```scheme
; Booleans
#t          ; true
#f          ; false
; Any value other than #f is truthy!

; Numbers
42          ; exact integer
-7
3.14        ; inexact (floating point)
1/3         ; exact rational
3+4i        ; complex
#b1010      ; binary: 10
#o17        ; octal: 15
#xff        ; hex: 255

; Characters
#\a         ; lowercase a
#\A         ; uppercase A
#\space
#\newline
#\tab

; Strings
"hello"
"line1\nline2"

; Symbols
'hello
'my-variable
'+

; Pairs and lists
(cons 1 2)        ; (1 . 2) — a pair
(cons 1 '())      ; (1) — a list
(list 1 2 3)      ; (1 2 3)
'(1 2 3)          ; (1 2 3) — quoted list

; Vectors
#(1 2 3)          ; literal vector
(vector 1 2 3)    ; vector constructor
(make-vector 5 0) ; #(0 0 0 0 0)

; Procedures (first-class)
car
(lambda (x) (* x x))

; Predicates
(number? 42)       ; #t
(integer? 3.0)     ; #t (3.0 is an integer value)
(exact? 1/3)       ; #t
(inexact? 3.14)    ; #t
(string? "hi")     ; #t
(symbol? 'foo)     ; #t
(pair? '(1 2))     ; #t
(null? '())        ; #t
(boolean? #f)      ; #t
(procedure? car)   ; #t
(vector? #(1 2))   ; #t
(char? #\a)        ; #t

; Type conversions
(number->string 42)         ; "42"
(string->number "42")       ; 42
(string->number "3.14")     ; 3.14
(symbol->string 'hello)     ; "hello"
(string->symbol "hello")    ; hello
(char->integer #\A)         ; 65
(integer->char 65)          ; #\A
(exact->inexact 1/3)        ; .3333...
(inexact->exact 0.5)        ; 1/2
```


---

# CHAPTER 3: SPECIAL FORMS


## Core Syntax

```scheme
; define — bind a name
(define x 42)
(define name "Alice")
(define (square x) (* x x))    ; function shorthand
; equivalent to:
(define square (lambda (x) (* x x)))

; let — local bindings
(let ((x 10)
      (y 20))
  (+ x y))    ; 30

; let* — sequential bindings
(let* ((x 10)
       (y (* x 2))   ; can use x
       (z (+ x y)))
  z)    ; 30

; letrec — mutually recursive bindings
(letrec ((even? (lambda (n)
                  (if (= n 0) #t (odd? (- n 1)))))
         (odd?  (lambda (n)
                  (if (= n 0) #f (even? (- n 1))))))
  (even? 10))    ; #t

; if
(if (> 3 2) "yes" "no")    ; "yes"
(if (> 2 3) "yes")         ; unspecified if false (no else)

; cond
(cond
  ((< x 0) "negative")
  ((= x 0) "zero")
  ((< x 10) "small")
  (else "large"))

; case
(case day
  ((mon tue wed thu fri) "weekday")
  ((sat sun) "weekend")
  (else "unknown"))

; and / or
(and 1 2 3)    ; 3
(and #f 2 3)   ; #f
(or #f #f 3)   ; 3

; when / unless (not standard R7RS but common)
(when (> x 0) (display x) (newline))
(unless (zero? x) (display "non-zero"))

; begin (sequence of expressions)
(begin
  (display "first")
  (display "second")
  42)    ; returns 42

; set! (mutation)
(define count 0)
(set! count (+ count 1))

; do (loop)
(do ((i 0 (+ i 1))
     (sum 0 (+ sum i)))
    ((= i 10) sum))    ; 45

; values / call-with-values (multiple return)
(define-values (q r) (floor/ 17 5))    ; q=3, r=2
; or
(call-with-values
  (lambda () (values 1 2 3))
  +)    ; 6
```


---

# CHAPTER 4: PROCEDURES AND CLOSURES


## Functions

```scheme
; Basic procedure
(define (add a b)
  (+ a b))

(add 3 4)    ; 7

; Lambda
(define square (lambda (x) (* x x)))
((lambda (x y) (+ x y)) 3 4)    ; 7

; Optional and rest args (R7RS)
(define (greet name . rest)
  (let ((greeting (if (null? rest) "Hello" (car rest))))
    (string-append greeting ", " name "!")))

(greet "Alice")         ; "Hello, Alice!"
(greet "Bob" "Hi")      ; "Hi, Bob!"

; Varargs
(define (sum . nums)
  (apply + nums))
(sum 1 2 3 4 5)    ; 15

; Tail recursion (Scheme guarantees proper tail calls!)
(define (factorial n)
  (define (iter n acc)
    (if (<= n 1)
      acc
      (iter (- n 1) (* n acc))))
  (iter n 1))

(factorial 1000)    ; exact result!

; Named let (common pattern for loops)
(let loop ((n 10) (acc 0))
  (if (= n 0)
    acc
    (loop (- n 1) (+ acc n))))    ; 55

; Closures
(define (make-counter)
  (let ((count 0))
    (lambda ()
      (set! count (+ count 1))
      count)))

(define c (make-counter))
(c)    ; 1
(c)    ; 2
(c)    ; 3

; Currying / partial application
(define (curry f)
  (lambda (x) (lambda (y) (f x y))))

(define add-curried (curry +))
(define add5 (add-curried 5))
(add5 10)    ; 15

; Higher-order
(define (compose f g)
  (lambda (x) (f (g x))))

(define inc (lambda (x) (+ x 1)))
(define double (lambda (x) (* x 2)))
(define inc-then-double (compose double inc))
(inc-then-double 5)    ; 12

; apply
(apply + '(1 2 3 4 5))    ; 15
(apply max '(3 1 4 1 5))  ; 5
(apply string-append '("a" "b" "c"))  ; "abc"
```


---

# CHAPTER 5: LISTS AND HIGHER-ORDER FUNCTIONS


## List Processing

```scheme
; Core list operations
(car '(1 2 3))         ; 1
(cdr '(1 2 3))         ; (2 3)
(caar '((1 2) 3))      ; 1
(cadr '(1 2 3))        ; 2
(caddr '(1 2 3))       ; 3
(cons 0 '(1 2 3))      ; (0 1 2 3)
(append '(1 2) '(3 4)) ; (1 2 3 4)
(reverse '(1 2 3))      ; (3 2 1)
(length '(1 2 3))       ; 3
(list-ref '(a b c) 1)  ; b (0-indexed)
(list-tail '(a b c) 1) ; (b c)
(null? '())             ; #t
(pair? '(1 2))          ; #t

; Standard higher-order list functions
(map (lambda (x) (* x x)) '(1 2 3 4 5))    ; (1 4 9 16 25)
(map + '(1 2 3) '(4 5 6))                   ; (5 7 9)
(filter odd? '(1 2 3 4 5 6))                ; (1 3 5)
(for-each display '(1 2 3))                 ; prints 123

; fold operations (SRFI-1)
(fold + 0 '(1 2 3 4 5))           ; 15
(fold-right cons '() '(1 2 3))     ; (1 2 3)
(reduce + 0 '(1 2 3 4 5))         ; 15

; Searching and testing
(member 3 '(1 2 3 4))    ; (3 4) — or #f
(memq 'b '(a b c))       ; (b c) (uses eq?)
(assoc "b" '(("a" 1) ("b" 2) ("c" 3)))  ; ("b" 2)
(assq 'b '((a 1)(b 2)(c 3)))    ; (b 2) (uses eq?)

; List building
(list 1 2 3 4 5)
(iota 5)                  ; (0 1 2 3 4) — SRFI-1
(iota 5 1)                ; (1 2 3 4 5)
(iota 5 0 2)              ; (0 2 4 6 8)
(make-list 5 'x)          ; (x x x x x)

; Sorting
(sort '(3 1 4 1 5 9) <)   ; (1 1 3 4 5 9)
(sort '("banana" "apple" "cherry") string<?)

; String operations
(string-length "hello")         ; 5
(string-append "hello" " " "world")  ; "hello world"
(substring "hello" 1 4)         ; "ell"
(string-ref "hello" 0)          ; #\h
(string->list "hello")          ; (#\h #\e #\l #\l #\o)
(list->string '(#\h #\i))       ; "hi"
(string-upcase "hello")         ; "HELLO"
(string-downcase "HELLO")       ; "hello"
(string<? "abc" "abd")          ; #t
(string=? "abc" "abc")          ; #t
(number->string 42)             ; "42"
(string->number "42")           ; 42
```


---

# CHAPTER 6: TAIL CALLS AND CONTINUATIONS


## Advanced Control

```scheme
; Proper tail calls — Scheme guarantees no stack overflow
; These are all tail recursive:

(define (sum-to n)
  (let loop ((i n) (acc 0))
    (if (= i 0)
      acc
      (loop (- i 1) (+ acc i)))))

(sum-to 1000000)    ; works without stack overflow

; call/cc — call with current continuation
; Captures the "return address" as a first-class value
(call-with-current-continuation
  (lambda (k)
    (display "before")
    (k 42)            ; "return" 42 from call/cc
    (display "never reached")))
; => 42

; Escape from deep recursion
(define (search tree pred)
  (call/cc
    (lambda (return)
      (let recurse ((node tree))
        (when (pair? node)
          (when (pred (car node))
            (return (car node)))
          (recurse (cdr node))))
      #f)))

; Coroutines with generators
(define (make-generator lst)
  (define return #f)
  (define (generator)
    (for-each
      (lambda (x)
        (call/cc
          (lambda (k)
            (set! generator k)
            (return x))))
      lst)
    (return 'done))
  (lambda ()
    (call/cc
      (lambda (k)
        (set! return k)
        (generator)))))

; Dynamic wind (setup/teardown)
(dynamic-wind
  (lambda () (display "enter "))
  (lambda () (display "body "))
  (lambda () (display "exit ")))
; prints: enter body exit

; with-exception-handler (R7RS)
(guard (exn
        ((string? (condition/report-string exn))
         (display "Error: ")
         (display (condition/report-string exn))))
  (error "something went wrong" 42))

; raise and condition
(raise (make-error "custom error" '(context)))
```


---

# CHAPTER 7: MACROS


## Hygienic Macros

```scheme
; define-syntax with syntax-rules — hygienic macros
(define-syntax my-if
  (syntax-rules ()
    ((_ test then else)
     (cond (test then)
           (else else)))))

; when and unless as macros
(define-syntax my-when
  (syntax-rules ()
    ((_ test body ...)
     (if test (begin body ...) (void)))))

(define-syntax my-unless
  (syntax-rules ()
    ((_ test body ...)
     (if (not test) (begin body ...) (void)))))

; swap! macro
(define-syntax swap!
  (syntax-rules ()
    ((_ a b)
     (let ((tmp a))
       (set! a b)
       (set! b tmp)))))

(let ((x 1) (y 2))
  (swap! x y)
  (list x y))    ; (2 1)

; while loop macro
(define-syntax while
  (syntax-rules ()
    ((_ test body ...)
     (let loop ()
       (when test
         body ...
         (loop))))))

; Pattern matching macro (simplified)
(define-syntax match
  (syntax-rules (else)
    ((_ val (else expr))
     expr)
    ((_ val ((pattern ...) expr) rest ...)
     (if (matches? val '(pattern ...))
       expr
       (match val rest ...)))))

; Ellipsis patterns
(define-syntax my-list
  (syntax-rules ()
    ((_ elem ...)
     (list elem ...))))

(my-list 1 2 3 4 5)    ; (1 2 3 4 5)

; Nested ellipsis
(define-syntax my-let
  (syntax-rules ()
    ((_ ((var init) ...) body ...)
     ((lambda (var ...) body ...) init ...))))

(my-let ((x 1) (y 2) (z 3))
  (+ x y z))    ; 6
```


---

# CHAPTER 8: I/O AND STANDARD LIBRARY


## Input/Output

```scheme
; Output
(display "Hello")           ; no newline
(newline)                   ; newline
(write "Hello")             ; "Hello" (with quotes, readable)
(writeln "Hello")           ; write + newline
(print "Hello")             ; some implementations

; Format (Racket/Guile)
(format #t "~a ~s ~d~n" "hello" "world" 42)
; hello "world" 42

; sprintf equivalent
(format #f "~a ~d" "value" 42)    ; returns a string

; Input
(define line (read-line))
(define expr (read))    ; reads a Scheme expression!

; Port operations (files)
; Write to file
(let ((out (open-output-file "test.txt")))
  (display "Hello, World!" out)
  (newline out)
  (close-output-port out))

; Read from file
(let ((in (open-input-file "test.txt")))
  (let ((line (read-line in)))
    (display line)
    (newline))
  (close-input-port in))

; with-output-to-file / with-input-from-file
(with-output-to-file "out.txt"
  (lambda ()
    (display "hello")
    (newline)))

(with-input-from-file "out.txt"
  (lambda ()
    (display (read-line))
    (newline)))

; call-with-port (auto-close)
(call-with-port
  (open-input-file "test.txt")
  (lambda (port)
    (let loop ((line (read-line port)))
      (unless (eof-object? line)
        (display line)
        (newline)
        (loop (read-line port))))))

; String ports
(define sp (open-input-string "hello world"))
(read sp)     ; hello (symbol)
(read sp)     ; world (symbol)

(define op (open-output-string))
(display "hello" op)
(get-output-string op)    ; "hello"

; Environment
(getenv "PATH")
(current-directory)    ; Racket: working directory
```
