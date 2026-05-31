# Common Lisp Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH COMMON LISP


## Remarks

Common Lisp is a multi-paradigm, general-purpose Lisp dialect standardized by ANSI in 1994. It features an extremely powerful macro system, CLOS (Common Lisp Object System), the condition system, and the REPL-driven development workflow. Used in AI research, financial systems, and embedded applications.

Implementations: SBCL (Steel Bank Common Lisp), CCL (Clozure CL), CLISP, ECL, Allegro CL.


## Hello World

```lisp
;; hello.lisp
(defun main ()
  (format t "Hello, World!~%")
  (format t "Hello, ~a!~%" "Common Lisp"))

(main)

;; Run:
;; sbcl --script hello.lisp
;; sbcl --eval "(load \"hello.lisp\")" --eval "(main)" --eval "(quit)"
```

```lisp
;; REPL usage
;; sbcl
;; * (format t "Hello, World!~%")
;; Hello, World!
;; NIL
```


---

# CHAPTER 2: TYPES AND ARITHMETIC


## Types

```lisp
;;; Type hierarchy (simplified)
;;; T (top type — all types)
;;;   NUMBER
;;;     REAL
;;;       RATIONAL
;;;         INTEGER (fixnum, bignum)
;;;         RATIO
;;;       FLOAT (short-float, single-float, double-float, long-float)
;;;     COMPLEX
;;;   SEQUENCE
;;;     LIST (CONS, NULL)
;;;     VECTOR (SIMPLE-VECTOR, STRING, BIT-VECTOR)
;;;   ARRAY (including vectors and strings)
;;;   CHARACTER
;;;   SYMBOL
;;;   HASH-TABLE
;;;   STRUCTURE-OBJECT
;;;   STANDARD-OBJECT (CLOS)
;;;   FUNCTION

;;; Integers
42          ; fixnum
1000000000000  ; bignum (arbitrary precision)
#b1010      ; binary: 10
#o17        ; octal: 15
#xDEADBEEF  ; hex

;;; Rationals
2/3         ; exact rational
3/1         ; = 3
(+ 1/3 1/6) ; => 1/2

;;; Floating point
3.14        ; single-float
3.14d0      ; double-float (or 3.14D0)
1.0e-5      ; 0.00001
pi          ; 3.141592653589793D0 (double)

;;; Complex
#c(3 4)     ; 3 + 4i
(complex 3 4)

;;; Arithmetic
(+ 1 2 3 4)         ; 10 (n-ary)
(- 10 3 2)          ; 5
(* 2 3 4)           ; 24
(/ 10 2)            ; 5
(/ 10 3)            ; 10/3 (exact ratio!)
(/ 10.0 3)          ; 3.3333...
(floor 17 5)        ; 3, 2 (quotient and remainder as multiple values)
(ceiling 17 5)      ; 4, -3
(truncate 17 5)     ; 3, 2
(round 17 5)        ; 3, 2 (rounds to even)
(mod 17 5)          ; 2
(rem 17 5)          ; 2
(expt 2 10)         ; 1024
(expt 2.0 0.5)      ; 1.4142...
(sqrt 2)            ; 1.4142... (sqrt of 2 as float)
(isqrt 16)          ; 4 (integer sqrt)
(gcd 12 8)          ; 4
(lcm 4 6)           ; 12
(abs -5)            ; 5
(max 3 7 2)         ; 7
(min 3 7 2)         ; 2
(1+ 5)              ; 6 (increment)
(1- 5)              ; 4 (decrement)

;;; Type predicates
(numberp 42)        ; t
(integerp 42)       ; t
(floatp 3.14)       ; t
(rationalp 1/3)     ; t
(complexp #c(1 2))  ; t
(zerop 0)           ; t
(plusp 5)           ; t
(minusp -3)         ; t
(evenp 4)           ; t
(oddp 5)            ; t
(> 3 2 1)           ; t (chained comparison)
(= 1 1.0)           ; t (numeric equality)
(eql 1 1)           ; t (same object for atoms)
```


---

# CHAPTER 3: SEQUENCES AND STRINGS


## Strings and Sequences

```lisp
;;; Strings
(length "hello")              ; 5
(char "hello" 0)              ; #\h
(string-upcase "hello")       ; "HELLO"
(string-downcase "HELLO")     ; "hello"
(string-capitalize "hello world")  ; "Hello World"
(string= "abc" "abc")         ; t
(string< "abc" "abd")         ; t
(string-trim '(#\space) "  hello  ")  ; "hello"
(string-left-trim '(#\space) "  hi")  ; "hi"
(string-right-trim '(#\space) "hi  ")  ; "hi"
(string-search "lo" "hello world")  ; some position (impl-specific)
(search "lo" "hello world")         ; 3 (standard)
(position #\l "hello")              ; 2 (first l)

;;; String concatenation
(concatenate 'string "hello" " " "world")  ; "hello world"
(format nil "~a ~a" "hello" "world")       ; "hello world"

;;; String to/from
(string 65)              ; "A" (char code)
(string #\A)             ; "A"
(coerce "hello" 'list)   ; (#\h #\e #\l #\l #\o)
(coerce '(#\h #\i) 'string)  ; "hi"

;;; Sequences (operations work on lists, vectors, strings)
;; Generic sequence functions:
(length seq)
(elt seq 0)           ; access by index
(setf (elt v 0) 99)  ; set by index
(reverse seq)
(sort seq #'<)        ; destructive sort
(stable-sort seq #'<) ; stable sort
(find 3 seq)          ; first match
(find-if #'evenp seq) ; find matching pred
(position 3 seq)      ; index of first match
(position-if #'evenp seq)
(count 3 seq)         ; count occurrences
(count-if #'evenp seq)
(remove 3 seq)        ; non-destructive remove all
(remove-if #'oddp seq)
(remove-duplicates seq)
(substitute 99 3 seq)        ; replace 3 with 99
(substitute-if 0 #'oddp seq) ; replace matching

;;; Subsequences
(subseq "hello world" 6)       ; "world"
(subseq "hello world" 0 5)     ; "hello"
(subseq '(1 2 3 4 5) 1 4)     ; (2 3 4)

;;; Mapping
(map 'list #'(lambda (x) (* x x)) '(1 2 3 4 5))  ; (1 4 9 16 25)
(map 'vector #'1+ #(1 2 3))    ; #(2 3 4)
(map nil #'print '(1 2 3))     ; side effects only
(mapcar #'1+ '(1 2 3))         ; (2 3 4) — list version
(maplist #'car '(a b c))       ; (a b c)
(mapc #'print '(1 2 3))        ; like mapcar but returns original list
```


---

# CHAPTER 4: LISTS IN DEPTH


## Advanced List Operations

```lisp
;;; Basic list operations
(cons 1 '(2 3))         ; (1 2 3)
(car '(1 2 3))           ; 1
(cdr '(1 2 3))           ; (2 3)
(list 1 2 3)             ; (1 2 3)
(list* 1 2 '(3 4))      ; (1 2 3 4)

;;; cXXr combinations (up to 4 levels)
(cadr '(1 2 3))     ; 2  = (car (cdr ...))
(caddr '(1 2 3))    ; 3  = (car (cddr ...))
(caadr '(1 (2 3)))  ; 2
(cddr '(1 2 3))     ; (3)

;;; Append and reverse
(append '(1 2) '(3 4) '(5))    ; (1 2 3 4 5)
(nconc '(1 2) '(3 4))          ; (1 2 3 4) — destructive
(reverse '(1 2 3))              ; (3 2 1)
(nreverse '(1 2 3))            ; (3 2 1) — destructive

;;; Searching
(member 3 '(1 2 3 4))          ; (3 4) or NIL
(member 3 '(1 2 3 4) :test #'=) ; with equality test
(memberp 3 '(1 2 3 4))         ; actually member returns the tail

(assoc 'b '((a 1)(b 2)(c 3)))  ; (b 2)
(rassoc 2 '((a 1)(b 2)(c 3)))  ; (b 2) — search by value

;;; Set operations on lists
(union '(1 2 3) '(2 3 4))      ; (1 2 3 4) — order unspecified
(intersection '(1 2 3) '(2 3 4))  ; (2 3) — order unspecified
(set-difference '(1 2 3 4) '(2 4))  ; (1 3)
(set-exclusive-or '(1 2 3) '(2 3 4))  ; (1 4)

;;; Plist (property list) operations
(getf '(:name "Alice" :age 30) :name)    ; "Alice"
(getf '(:name "Alice" :age 30) :city "NYC")  ; "NYC" (default)

;;; Functional list processing
(mapcar #'(lambda (x) (* x x)) '(1 2 3 4 5))  ; (1 4 9 16 25)
(mapc #'print '(1 2 3))   ; print each, return list
(mapcan #'(lambda (x) (list x (* x x))) '(1 2 3))  ; (1 1 2 4 3 9)
(apply #'+ '(1 2 3 4 5))  ; 15
(reduce #'+ '(1 2 3 4 5)) ; 15
(reduce #'+ '(1 2 3 4 5) :from-end t)  ; same
(reduce #'cons '(1 2 3) :initial-value '())  ; (3 2 1)
(reduce #'max '(3 1 4 1 5 9) :initial-value 0)  ; 9

;;; Higher-order filtering (via remove-if)
(remove-if #'oddp '(1 2 3 4 5 6))     ; (2 4 6)
(remove-if-not #'evenp '(1 2 3 4 5 6))  ; (2 4 6)

;;; Sort (destructive!)
(sort (list 3 1 4 1 5 9) #'<)  ; (1 1 3 4 5 9)
(sort (list "banana" "apple") #'string<)  ; ("apple" "banana")
(sort (list '(3 "c") '(1 "a") '(2 "b"))
      #'< :key #'car)  ; ((1 "a") (2 "b") (3 "c"))
```


---

# CHAPTER 5: FUNCTIONS AND CLOSURES


## Functions

```lisp
;;; defun
(defun factorial (n)
  "Compute n! recursively."    ; docstring
  (if (<= n 1)
    1
    (* n (factorial (- n 1)))))

;;; Optional parameters
(defun greet (name &optional (greeting "Hello") (punct "!"))
  (format nil "~a, ~a~a" greeting name punct))

(greet "Alice")             ; "Hello, Alice!"
(greet "Bob" "Hi")          ; "Hi, Bob!"
(greet "Carol" "Hey" ".")   ; "Hey, Carol."

;;; Keyword parameters
(defun connect (&key (host "localhost") (port 8080) (protocol :http))
  (format t "~a://~a:~a~%" protocol host port))

(connect :port 443 :protocol :https)

;;; Rest parameters
(defun my-list (&rest args) args)
(my-list 1 2 3)    ; (1 2 3)

;;; Complex signature
(defun complex-fn (required1 required2
                   &optional opt1 (opt2 "default")
                   &rest rest-args
                   &key key1 (key2 0) &allow-other-keys)
  (list required1 required2 opt1 opt2 rest-args key1 key2))

;;; Lambda
(funcall (lambda (x y) (+ x y)) 3 4)    ; 7
(funcall #'+ 1 2 3)    ; 6

;;; Function objects
#'car           ; function object for car
(function car)  ; same

;;; Apply
(apply #'+ 1 2 '(3 4))    ; 10
(apply #'list 1 2 '(3 4))  ; (1 2 3 4)

;;; Closures
(defun make-adder (n)
  (lambda (x) (+ n x)))

(let ((add5 (make-adder 5)))
  (funcall add5 10))    ; 15

;;; flet / labels (local functions)
(flet ((double (x) (* x 2))
       (square (x) (* x x)))
  (double (square 3)))   ; 18

;; labels allows mutual recursion
(labels ((even? (n) (if (= n 0) t (odd?  (1- n))))
         (odd?  (n) (if (= n 0) nil (even? (1- n)))))
  (even? 10))    ; t
```


---

# CHAPTER 6: CLOS — OBJECT-ORIENTED PROGRAMMING


## Common Lisp Object System

```lisp
;;; Define class
(defclass shape ()
  ((color :initarg :color :accessor shape-color :initform "black")))

(defclass circle (shape)
  ((radius :initarg :radius :accessor circle-radius :initform 1.0)))

(defclass rectangle (shape)
  ((width  :initarg :width  :accessor rect-width  :initform 1.0)
   (height :initarg :height :accessor rect-height :initform 1.0)))

;;; Create instances
(defvar *c* (make-instance 'circle :radius 5.0 :color "red"))
(defvar *r* (make-instance 'rectangle :width 4.0 :height 6.0))

;;; Access slots
(circle-radius *c*)          ; 5.0
(shape-color *c*)            ; "red"
(setf (circle-radius *c*) 6.0)  ; set

;;; Generic functions
(defgeneric area (shape)
  (:documentation "Compute the area of a shape."))

(defmethod area ((c circle))
  (* pi (expt (circle-radius c) 2)))

(defmethod area ((r rectangle))
  (* (rect-width r) (rect-height r)))

(defmethod area :before ((s shape))
  (format t "Computing area for ~a~%" s))

;;; Auxiliary methods
(defmethod initialize-instance :after ((c circle) &key)
  (format t "Created circle with radius ~a~%" (circle-radius c)))

;;; Method combination
;; Standard: primary (main) + :before + :after + :around
;; Arithmetic: (defgeneric g () (:method-combination +))

;;; Slot options
;; :initarg   — keyword for make-instance
;; :initform  — default value
;; :accessor  — reader+writer
;; :reader    — reader only
;; :writer    — writer only
;; :allocation :class — shared across instances
;; :documentation — docstring
;; :type      — type constraint

;;; Introspection
(class-of *c*)           ; #<STANDARD-CLASS CIRCLE>
(typep *c* 'circle)      ; t
(typep *c* 'shape)       ; t
(slot-value *c* 'radius) ; 5.0 (or whatever it is)
(slot-boundp *c* 'color) ; t
(slot-makunbound *c* 'color)  ; unbind

;;; print-object
(defmethod print-object ((c circle) stream)
  (print-unreadable-object (c stream :type t :identity t)
    (format stream "r=~a" (circle-radius c))))
```


---

# CHAPTER 7: CONDITIONS AND RESTARTS


## Error Handling

```lisp
;;; CL condition system — more powerful than try/catch

;;; Define condition types
(define-condition my-error (error)
  ((message :initarg :message :reader error-message))
  (:report (lambda (c stream)
             (format stream "My error: ~a" (error-message c)))))

(define-condition file-not-found-error (my-error)
  ((filename :initarg :filename :reader error-filename)))

;;; signal / error / warn
(error "Something went wrong!")
(error 'my-error :message "custom error")
(warn  "This is a warning")
(signal 'my-error :message "soft error")

;;; handler-case (catch errors)
(handler-case
  (progn
    (error "oops")
    "success")
  (my-error (c)
    (format t "Got my-error: ~a~%" c)
    "recovered")
  (error (c)
    (format t "Got error: ~a~%" c)
    "fallback"))

;;; ignore-errors (catch all, return nil + condition)
(multiple-value-bind (result error)
  (ignore-errors (/ 1 0))
  (if error
    (format t "Error: ~a~%" error)
    (format t "Result: ~a~%" result)))

;;; handler-bind (intercept without unwinding)
(handler-bind
  ((error (lambda (c)
            (format t "Intercepted: ~a~%" c)
            ;; don't invoke restart — control returns to handler-case
            )))
  (error "test"))

;;; Restarts — allow recovery at point of error
(defun carefully-divide (x y)
  (restart-case
    (if (zerop y)
      (error 'division-by-zero-error)
      (/ x y))
    (use-value (new-y)
      :report "Provide a different divisor"
      (/ x new-y))
    (return-zero ()
      :report "Return 0 instead"
      0)))

;;; Invoke restart from handler
(handler-bind
  ((division-by-zero-error
    (lambda (c)
      (declare (ignore c))
      (invoke-restart 'return-zero))))
  (carefully-divide 10 0))   ; => 0
```


---

# CHAPTER 8: MACROS AND COMPILATION


## Macros

```lisp
;;; defmacro — code generation at compile time
(defmacro while (test &body body)
  `(do ()
       ((not ,test))
     ,@body))

(defmacro swap! (a b)
  (let ((tmp (gensym "TMP")))   ; gensym avoids name capture
    `(let ((,tmp ,a))
       (setf ,a ,b)
       (setf ,b ,tmp))))

;;; Backquote operators
;; `(...) = quasi-quote
;; ,x     = unquote (insert value of x)
;; ,@x    = splice (insert list x)
;; ,.x    = nconc splice (rare)

(defmacro assert-equal (a b)
  `(unless (equal ,a ,b)
     (error "Assertion failed: ~s /= ~s~%  Actual: ~s~%  Expected: ~s"
            ',a ',b ,a ,b)))

;;; Macroexpand (debug)
(macroexpand-1 '(while (> x 0) (decf x)))
;; => (DO NIL ((NOT (> X 0))) (DECF X))

;;; define-symbol-macro
(define-symbol-macro year (nth-value 5 (get-decoded-time)))

;;; Reader macros
(set-macro-character #\[
  (lambda (stream char)
    (declare (ignore char))
    (let ((items (read-delimited-list #\] stream t)))
      `(vector ,@items))))

;; now [1 2 3] reads as (vector 1 2 3)

;;; Compile and load
(compile-file "my-module.lisp")    ; creates .fasl
(load "my-module.fasl")
(load "my-module.lisp")            ; interpret

;;; ASDF (project system — like make)
;; my-system.asd
(asdf:defsystem "my-system"
  :version "1.0"
  :components ((:file "package")
               (:file "utils" :depends-on ("package"))
               (:file "main"  :depends-on ("utils")))
  :depends-on ("alexandria" "cl-ppcre"))

;; Quicklisp (package manager)
;; (ql:quickload "alexandria")
;; (ql:quickload "cl-ppcre")
```
