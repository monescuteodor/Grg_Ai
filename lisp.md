# Lisp Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH LISP


## Remarks

Lisp (List Processing) is one of the oldest high-level programming languages, created in 1958 by John McCarthy. It pioneered many concepts including tree data structures, automatic garbage collection, higher-order functions, recursion, and dynamic typing. This reference covers core Lisp concepts applicable across dialects (Common Lisp, Scheme, Racket, Clojure, Emacs Lisp).

Dialects: Common Lisp (SBCL, CCL), Scheme (Racket, Guile, MIT Scheme), Clojure (JVM), Emacs Lisp.


## Hello World

```lisp
;; Common Lisp
(print "Hello, World!")
(format t "Hello, World!~%")
(format t "Hello, ~a!~%" "Lisp")

;; Run:
;; sbcl --script hello.lisp
;; clisp hello.lisp
```

```scheme
;; Scheme (R7RS)
(display "Hello, World!")
(newline)
(display (string-append "Hello, " "Scheme!"))
(newline)

;; Run:
;; racket hello.scm
;; guile hello.scm
```


---

# CHAPTER 2: ATOMS AND LISTS


## Core Data Types

```lisp
;;; Atoms (indivisible values)
42          ; integer
3.14        ; float
"hello"     ; string
#\A         ; character
t           ; true (in CL)
nil         ; false/empty list (in CL)

;;; Symbols
'hello      ; quoted symbol
'my-variable
'some-name

;;; Lists (the fundamental data structure)
'(1 2 3)           ; list of 3 numbers
'(a b c)           ; list of 3 symbols
'(1 "hello" #\A)   ; heterogeneous list
'()                ; empty list = nil

;;; Pairs (cons cells)
(cons 1 2)         ; => (1 . 2) — a pair (dotted pair)
(cons 1 '())       ; => (1) — list with one element
(cons 1 '(2 3))    ; => (1 2 3)
(car '(1 2 3))     ; => 1 (head)
(cdr '(1 2 3))     ; => (2 3) (tail)
(cadr '(1 2 3))    ; => 2 (car of cdr = second)
(caddr '(1 2 3))   ; => 3 (third)
(cddr '(1 2 3))    ; => (3) (cdr of cdr)

;;; Nested lists (trees)
'(1 (2 3) (4 (5 6)))

;;; List operations
(list 1 2 3 4 5)          ; => (1 2 3 4 5)
(append '(1 2) '(3 4))    ; => (1 2 3 4)
(reverse '(1 2 3))         ; => (3 2 1)
(length '(1 2 3))          ; => 3
(nth 1 '(a b c))           ; => b (0-indexed in CL)
(last '(1 2 3))            ; => (3) (note: returns list)
(butlast '(1 2 3))         ; => (1 2)
(member 2 '(1 2 3))        ; => (2 3) (truthy if found)
(null '())                  ; => t (empty list?)
(listp '(1 2 3))            ; => t (is a list?)
(atom 'hello)               ; => t (is an atom?)

;;; Numeric predicates
(zerop 0)       ; t
(plusp 5)       ; t
(minusp -3)     ; t
(evenp 4)       ; t
(oddp 5)        ; t

;;; Arithmetic
(+ 1 2 3 4)    ; 10 (n-ary)
(- 10 3)       ; 7
(* 2 3 4)      ; 24
(/ 10 2)       ; 5
(expt 2 10)    ; 1024
(sqrt 16)      ; 4.0
(abs -5)       ; 5
(max 3 7 2)    ; 7
(min 3 7 2)    ; 2
(mod 17 5)     ; 2
(floor 3.7)    ; 3
(ceiling 3.2)  ; 4
(round 3.5)    ; 4
```


---

# CHAPTER 3: VARIABLES AND BINDING


## Variable Binding

```lisp
;;; Global variables
(defvar *counter* 0)         ; global, asterisks = convention for global
(defparameter *max* 100)     ; like defvar but always resets

;;; Set a variable
(setq *counter* 42)
(setf *counter* 43)          ; setf is more general

;;; Local binding (let)
(let ((x 10)
      (y 20))
  (+ x y))     ; => 30, x and y not visible outside

;;; let* (sequential — later bindings can see earlier ones)
(let* ((x 10)
       (y (* x 2))   ; y can use x
       (z (+ x y)))
  z)     ; => 30

;;; Lexical closure
(let ((count 0))
  (defun increment! ()
    (setq count (1+ count))
    count)
  (defun get-count ()
    count))

(increment!)  ; 1
(increment!)  ; 2
(get-count)   ; 2

;;; Destructuring
(destructuring-bind (a b c) '(1 2 3)
  (list a b c))    ; (1 2 3)

(destructuring-bind (first &rest rest) '(1 2 3 4)
  (cons first rest))  ; (1 2 3 4)

;;; Multiple values
(multiple-value-bind (q r) (floor 17 5)
  (list q r))    ; (3 2)

(values 1 2 3)   ; returns 3 values

;;; Constants
(defconstant +pi+ 3.14159265358979)
```


---

# CHAPTER 4: CONTROL FLOW


## Conditionals and Loops

```lisp
;;; if (exactly 2 branches)
(if (> 3 2)
  "yes"
  "no")    ; "yes"

;;; when (one branch, multiple forms)
(when (> x 0)
  (format t "positive~%")
  x)

;;; unless (when not)
(unless (zerop x)
  (format t "non-zero~%"))

;;; cond (multi-branch)
(cond
  ((< x 0)  "negative")
  ((= x 0)  "zero")
  ((< x 10) "small")
  (t        "large"))

;;; case (switch on value)
(case day
  (:monday    "Start of week")
  (:friday    "End of week")
  ((:saturday :sunday) "Weekend")
  (otherwise  "Other"))

;;; and / or (short-circuit, return last truthy value)
(and 1 2 3)    ; 3
(and nil 2 3)  ; nil
(or nil nil 3) ; 3
(or 1 2 3)     ; 1

;;; Loops
;; dotimes
(dotimes (i 5)
  (format t "~a~%" i))    ; 0 1 2 3 4

;; dolist
(dolist (x '(a b c d))
  (format t "~a~%" x))

;; loop macro (powerful!)
(loop for i from 1 to 10 collect i)          ; (1 2 3 4 5 6 7 8 9 10)
(loop for i from 0 below 10 by 2 collect i)  ; (0 2 4 6 8)
(loop for x in '(1 2 3 4 5) sum x)           ; 15
(loop for x in '(1 2 3 4 5) when (evenp x) collect x)  ; (2 4)
(loop repeat 3 do (format t "hello~%"))

;; do (general loop)
(do ((i 0 (1+ i))
     (sum 0 (+ sum i)))
    ((>= i 10) sum))    ; 45

;; tagbody / go (rare, low-level)
(tagbody
  start
  (when (> *counter* 5) (go done))
  (incf *counter*)
  (go start)
  done)

;;; throw / catch (non-local exit)
(catch 'found
  (dolist (x '(1 2 3 4 5))
    (when (= x 3)
      (throw 'found x))))   ; 3
```


---

# CHAPTER 5: FUNCTIONS


## Functions and Closures

```lisp
;;; defun (define function)
(defun add (a b)
  "Add two numbers."   ; docstring
  (+ a b))

(add 3 4)    ; 7

;;; Factorial (recursive)
(defun factorial (n)
  (if (<= n 1)
    1
    (* n (factorial (- n 1)))))

;;; Tail-recursive with accumulator
(defun factorial-tail (n &optional (acc 1))
  (if (<= n 1)
    acc
    (factorial-tail (- n 1) (* n acc))))

;;; Optional parameters
(defun greet (name &optional (greeting "Hello"))
  (format nil "~a, ~a!" greeting name))

(greet "Alice")         ; "Hello, Alice!"
(greet "Bob" "Hi")      ; "Hi, Bob!"

;;; Keyword parameters
(defun create-user (&key name (age 0) (city "Unknown"))
  (list name age city))

(create-user :name "Alice" :age 30)

;;; Rest parameters (varargs)
(defun sum-all (&rest nums)
  (apply #'+ nums))

(sum-all 1 2 3 4 5)   ; 15

;;; Lambda (anonymous function)
(lambda (x) (* x x))
((lambda (x y) (+ x y)) 3 4)   ; 7

;;; funcall and apply
(funcall #'+ 1 2 3)      ; 6
(apply #'+ '(1 2 3 4))   ; 10
(apply #'+ 1 2 '(3 4))   ; 10

;;; Higher-order functions
(mapcar #'(lambda (x) (* x x)) '(1 2 3 4 5))    ; (1 4 9 16 25)
(remove-if #'oddp '(1 2 3 4 5 6))                ; (2 4 6)
(remove-if-not #'evenp '(1 2 3 4 5 6))           ; (2 4 6)
(reduce #'+ '(1 2 3 4 5))                         ; 15
(reduce #'max '(3 1 4 1 5 9 2 6))                ; 9
(sort '(3 1 4 1 5) #'<)                           ; (1 1 3 4 5)
(find-if #'evenp '(1 3 4 5))                      ; 4

;;; Closures
(defun make-adder (n)
  (lambda (x) (+ n x)))

(let ((add5 (make-adder 5)))
  (funcall add5 10))   ; 15
```


---

# CHAPTER 6: MACROS


## Lisp Macros

```lisp
;;; defmacro — code transformation at compile time
(defmacro when2 (test &body body)
  `(if ,test (progn ,@body)))

;;; Backquote, comma, comma-at
;; ` (backtick) = quasi-quote (don't evaluate)
;; , (comma) = unquote (evaluate inside backtick)
;; ,@ (comma-at) = splice list

(defmacro swap! (a b)
  `(let ((tmp ,a))
     (setf ,a ,b)
     (setf ,b tmp)))

;;; More useful macros
(defmacro while (test &body body)
  `(do ()
       ((not ,test))
     ,@body))

(defmacro with-logging (&body body)
  `(progn
     (format t "Starting~%")
     (let ((result (progn ,@body)))
       (format t "Done: ~a~%" result)
       result)))

;;; Macro expansion (debug)
(macroexpand-1 '(when2 (> x 0) (print x)))

;;; Gensym (unique symbols to avoid variable capture)
(defmacro safe-when (test &body body)
  (let ((test-sym (gensym)))
    `(let ((,test-sym ,test))
       (when ,test-sym ,@body))))

;;; Reader macros (extend the reader)
;; ' = (quote ...)
;; ` = (quasiquote ...)
;; , = (unquote ...)
;; ,@ = (unquote-splicing ...)
;; # = dispatch macro character
;; #' = (function ...)
;; #( = vector
;; #\A = character literal

;;; Compile-time computation
(defmacro add-at-compile-time (a b)
  (+ a b))   ; computed when macro is expanded!

(add-at-compile-time 3 4)  ; expands to 7
```


---

# CHAPTER 7: ASSOCIATION LISTS AND HASH TABLES


## Data Structures

```lisp
;;; Association lists (alists) — simple key-value pairs
(defvar *alist* '((name . "Alice")
                  (age . 30)
                  (city . "NYC")))

(assoc 'name *alist*)         ; (NAME . "Alice")
(cdr (assoc 'name *alist*))   ; "Alice"
(assocq 'name *alist*)        ; (with eq comparison)

;;; Functional update
(acons 'email "alice@example.com" *alist*)

;;; Property lists (plists) — flat list alternating key/value
(defvar *plist* '(:name "Alice" :age 30))
(getf *plist* :name)           ; "Alice"
(setf (getf *plist* :city) "NYC")

;;; Hash tables
(defvar *ht* (make-hash-table))
(setf (gethash 'name *ht*) "Alice")
(setf (gethash 'age  *ht*) 30)
(gethash 'name *ht*)          ; "Alice", t (second value: found?)
(gethash 'missing *ht* "default")  ; "default"
(remhash 'age *ht*)
(hash-table-count *ht*)       ; 1

;; Iterate over hash table
(maphash (lambda (k v)
           (format t "~a: ~a~%" k v))
         *ht*)

;; String keys hash table
(defvar *str-ht* (make-hash-table :test #'equal))
(setf (gethash "key" *str-ht*) "value")

;;; Arrays / Vectors
(make-array 5)                    ; #(0 0 0 0 0)
(make-array 5 :initial-element 0)
(make-array '(3 3))               ; 3x3 array
#(1 2 3 4 5)                      ; literal vector
(aref v 2)                        ; access element
(setf (aref v 2) 99)             ; set element
(vector-push-extend 6 v)          ; append (to adjustable vector)

;;; Sequences (strings, lists, vectors are all sequences)
(elt '(a b c) 1)    ; b
(elt #(a b c) 1)    ; b
(elt "abc" 1)       ; #\b

(length '(1 2 3))   ; 3
(length #(1 2 3))   ; 3
(length "hello")    ; 5

(subseq '(a b c d) 1 3)   ; (b c)
(subseq "hello" 1 3)       ; "el"
```


---

# CHAPTER 8: OBJECT-ORIENTED PROGRAMMING (CLOS)


## Common Lisp Object System

```lisp
;;; CLOS — the most powerful OOP system

;;; Define a class
(defclass animal ()
  ((name  :initarg :name  :accessor animal-name  :initform "Unknown")
   (sound :initarg :sound :accessor animal-sound :initform "...")))

;;; Create instances
(defvar *dog* (make-instance 'animal :name "Rex" :sound "Woof"))
(animal-name *dog*)    ; "Rex"
(animal-sound *dog*)   ; "Woof"
(setf (animal-name *dog*) "Max")

;;; Define methods (generic functions)
(defgeneric speak (animal)
  (:documentation "Make the animal speak"))

(defmethod speak ((a animal))
  (format nil "~a says ~a!" (animal-name a) (animal-sound a)))

;;; Inheritance
(defclass dog (animal)
  ((breed :initarg :breed :accessor dog-breed :initform "Mixed")))

(defmethod speak ((d dog))
  (format nil "~a!" (call-next-method)))  ; call parent method

(defclass poodle (dog)
  ()
  (:default-initargs :sound "Yip" :breed "Poodle"))

;;; Multiple inheritance
(defclass flyer () ())
(defmethod fly ((f flyer)) "I can fly!")

(defclass flying-dog (dog flyer) ())
;; inherits from both dog and flyer

;;; Method combination
(defmethod speak :before ((d dog))
  (format t "Dog is about to speak...~%"))

(defmethod speak :after ((d dog))
  (format t "Dog finished speaking.~%"))

(defmethod speak :around ((d dog))
  (format t "[Around before]~%")
  (let ((result (call-next-method)))
    (format t "[Around after]~%")
    result))

;;; Introspection
(class-of *dog*)               ; #<STANDARD-CLASS DOG>
(typep *dog* 'animal)          ; t
(typep *dog* 'dog)             ; t
(slot-value *dog* 'name)       ; "Max"
(slot-boundp *dog* 'breed)     ; t

;;; print-object (customize printing)
(defmethod print-object ((a animal) stream)
  (print-unreadable-object (a stream :type t)
    (format stream "~a" (animal-name a))))
```
