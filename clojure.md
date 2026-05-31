# Clojure Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH CLOJURE


## Remarks

Clojure is a modern, dynamic, functional Lisp dialect on the JVM. It emphasizes immutability, functional programming, and concurrency through persistent data structures and Software Transactional Memory (STM). ClojureScript compiles to JavaScript. Used in data science, web development, and distributed systems.

Tools: Leiningen or deps.edn/tools.deps, CIDER (Emacs), Calva (VS Code), Clojure CLI.


## Hello World

```clojure
;; hello.clj
(ns hello.core)

(defn -main []
  (println "Hello, World!")
  (println (str "Hello, " "Clojure!")))

;; Run with Leiningen:
;; lein new app hello && cd hello && lein run

;; REPL:
;; clj     (Clojure CLI)
;; lein repl
```


---

# CHAPTER 2: BASICS AND SYNTAX


## Core Syntax

```clojure
;; Everything is a form (expression)
;; Function calls: (function-name arg1 arg2 ...)
(+ 1 2)         ;; 3
(- 10 3)        ;; 7
(* 4 5)         ;; 20
(/ 10 2)        ;; 5 (or 5/2 as ratio for integers)
(quot 10 3)     ;; 3 (integer division)
(rem 10 3)      ;; 1 (remainder)
(mod 10 3)      ;; 1
(inc 5)         ;; 6
(dec 5)         ;; 4
(max 3 7 2)     ;; 7
(min 3 7 2)     ;; 2
(abs -5)        ;; 5
(Math/sqrt 16)  ;; 4.0
(Math/pow 2 10) ;; 1024.0

;; Booleans
(and true false)   ;; false
(or true false)    ;; true
(not true)         ;; false
(= 1 1)            ;; true
(not= 1 2)         ;; true
(< 1 2 3)          ;; true (chained comparison)
(>= 3 3)           ;; true

;; Equality
(= 1 1)      ;; true (value equality)
(== 1 1.0)   ;; true (numeric equality)
(identical? "a" "a")  ;; reference equality

;; Atoms (symbols)
:hello          ;; keyword
:name
'hello          ;; quoted symbol
'some-symbol

;; Vars / def
(def name "Alice")
(def max-count 100)
(def pi Math/PI)

;; Type predicates
(integer? 42)    ;; true
(float? 3.14)    ;; true
(string? "hi")   ;; true
(keyword? :ok)   ;; true
(symbol? 'x)     ;; true
(nil? nil)       ;; true
(boolean? true)  ;; true
(fn? println)    ;; true
(seq? [1 2 3])   ;; false (it's a vector)
(vector? [1 2])  ;; true

;; Coercions
(str 42)           ;; "42"
(int 3.7)          ;; 3
(double 5)         ;; 5.0
(name :hello)      ;; "hello"
(keyword "hello")  ;; :hello
(Integer/parseInt "42")
```


---

# CHAPTER 3: COLLECTIONS


## Immutable Collections

```clojure
;; Vectors (indexed, O(log n) update)
(def v [1 2 3 4 5])
(count v)        ;; 5
(first v)        ;; 1
(last v)         ;; 5
(rest v)         ;; (2 3 4 5) — lazy seq
(nth v 2)        ;; 3
(get v 2)        ;; 3
(v 2)            ;; 3 (vector is a function!)
(conj v 6)       ;; [1 2 3 4 5 6]
(assoc v 2 99)   ;; [1 2 99 4 5]
(subvec v 1 4)   ;; [2 3 4]
(pop v)          ;; [1 2 3 4]
(peek v)         ;; 5

;; Lists (linked, O(1) prepend)
(def lst '(1 2 3 4 5))
(conj lst 0)    ;; (0 1 2 3 4 5) — prepend!
(first lst)     ;; 1

;; Maps (persistent hash map)
(def m {:name "Alice" :age 30 :city "NYC"})
(:name m)              ;; "Alice"
(get m :name)          ;; "Alice"
(get m :missing "default")  ;; "default"
(m :age)               ;; 30
(assoc m :email "alice@example.com")  ;; add/update
(dissoc m :age)        ;; remove key
(contains? m :name)    ;; true
(keys m)               ;; (:name :age :city)
(vals m)               ;; ("Alice" 30 "NYC")
(count m)              ;; 3
(merge m {:score 90})
(merge-with + {:a 1 :b 2} {:a 3 :b 4})  ;; {:a 4 :b 6}
(update m :age inc)    ;; {:name "Alice" :age 31 ...}
(update-in m [:score] (fnil inc 0))

;; Nested access
(def data {:user {:name "Alice" :scores [90 85 92]}})
(get-in data [:user :name])         ;; "Alice"
(get-in data [:user :scores 0])     ;; 90
(assoc-in data [:user :age] 30)
(update-in data [:user :scores] conj 95)

;; Sets
(def s #{1 2 3 4 5})
(contains? s 3)       ;; true
(s 3)                 ;; 3 (set is a function)
(conj s 6)
(disj s 3)            ;; remove
(clojure.set/union s #{4 5 6})
(clojure.set/intersection s #{3 4 5 6})
(clojure.set/difference s #{3 4})

;; Sequences (abstraction over all collections)
(seq [1 2 3])        ;; (1 2 3)
(seq {:a 1 :b 2})    ;; ([:a 1] [:b 2])
(seq "hello")        ;; (\h \e \l \l \o)
```


---

# CHAPTER 4: CONTROL FLOW AND FUNCTIONS


## Functions and Control

```clojure
;; if (only 2 branches, use when for 1)
(if (> 3 2)
  "yes"
  "no")            ;; "yes"

(when (> 3 2)
  (println "yes")
  42)              ;; prints "yes", returns 42

(when-not false
  "executed")      ;; "executed"

;; cond (multi-way branch)
(defn classify [n]
  (cond
    (< n 0)   "negative"
    (= n 0)   "zero"
    (< n 10)  "small"
    :else     "large"))

;; case (switch on value)
(case day
  "Monday"                "Start of week"
  ("Saturday" "Sunday")   "Weekend"
  "Other")                ;; default

;; let (local bindings)
(let [x 10
      y 20
      z (+ x y)]
  (* z 2))   ;; 60

;; do (sequence of effects, returns last)
(do
  (println "first")
  (println "second")
  42)    ;; returns 42

;; loop / recur (tail recursion)
(loop [n 1, acc 1]
  (if (> n 10)
    acc
    (recur (inc n) (* acc n))))  ;; factorial 10

;; doseq (side effects over collection)
(doseq [item [1 2 3 4 5]]
  (println item))

(doseq [x (range 3) y (range 3)]
  (println [x y]))

;; dotimes
(dotimes [i 5]
  (println i))    ;; 0 1 2 3 4

;; Functions
(defn greet
  "Greet someone (docstring)"
  [name]
  (str "Hello, " name "!"))

;; Multiple arities
(defn greet
  ([name] (greet name "Hello"))
  ([name greeting] (str greeting ", " name "!")))

;; Variadic
(defn sum-all [& nums]
  (reduce + nums))
(sum-all 1 2 3 4 5)   ;; 15

;; Destructuring
(defn describe [[first & rest]]
  (str "Head: " first ", Rest: " rest))

(defn info [{:keys [name age]}]
  (str name " is " age))
(info {:name "Alice" :age 30})

;; Anonymous function
(fn [x] (* x x))
#(* % %)             ;; shorthand, % = first arg
#(* %1 %2)           ;; %1, %2 = first, second arg

;; Higher-order functions
(map #(* % 2) [1 2 3 4 5])          ;; (2 4 6 8 10)
(filter even? [1 2 3 4 5 6])         ;; (2 4 6)
(remove odd? [1 2 3 4 5 6])          ;; (2 4 6)
(reduce + 0 [1 2 3 4 5])             ;; 15
(reduce-kv (fn [m k v] (assoc m k (* v 2))) {} {:a 1 :b 2})

;; apply
(apply + [1 2 3 4 5])   ;; 15
(apply str ["a" "b" "c"])  ;; "abc"

;; comp and partial
(def double (partial * 2))
(def inc-then-double (comp double inc))
(inc-then-double 5)   ;; 12
```


---

# CHAPTER 5: SEQUENCES AND LAZY EVALUATION


## Sequence Operations

```clojure
;; Core sequence functions
(range 5)           ;; (0 1 2 3 4)
(range 1 11)        ;; (1 2 3 4 5 6 7 8 9 10)
(range 0 10 2)      ;; (0 2 4 6 8)
(repeat 5 "hi")     ;; ("hi" "hi" "hi" "hi" "hi")
(repeat "hi")       ;; infinite lazy seq!
(cycle [1 2 3])     ;; (1 2 3 1 2 3 ...)
(iterate inc 0)     ;; (0 1 2 3 4 ...)
(take 5 (iterate #(* % 2) 1))  ;; (1 2 4 8 16)

;; Transformation
(take 5 [1 2 3 4 5 6 7 8 9])    ;; (1 2 3 4 5)
(drop 3 [1 2 3 4 5])             ;; (4 5)
(take-while #(< % 5) [1 2 3 4 5 6])  ;; (1 2 3 4)
(drop-while odd? [1 3 5 6 7 8])       ;; (6 7 8)
(partition 3 [1 2 3 4 5 6 7 8 9])    ;; ((1 2 3)(4 5 6)(7 8 9))
(partition-all 3 [1 2 3 4 5])         ;; ((1 2 3)(4 5))
(partition-by even? [1 3 5 2 4 6 1])  ;; ((1 3 5)(2 4 6)(1))
(group-by even? [1 2 3 4 5 6])        ;; {false (1 3 5), true (2 4 6)}
(frequencies [1 1 2 3 3 3])           ;; {1 2, 2 1, 3 3}
(distinct [1 2 2 3 3 4])              ;; (1 2 3 4)
(flatten [[1 2] [3 [4 5]]])           ;; (1 2 3 4 5)
(interleave [1 2 3] [:a :b :c])       ;; (1 :a 2 :b 3 :c)
(interpose ", " ["a" "b" "c"])        ;; ("a" ", " "b" ", " "c")
(zipmap [:a :b :c] [1 2 3])           ;; {:a 1, :b 2, :c 3}
(map vector [1 2 3] [:a :b :c])       ;; ([1 :a] [2 :b] [3 :c])

;; String
(apply str (interpose ", " ["a" "b" "c"]))  ;; "a, b, c"
(clojure.string/join ", " ["a" "b" "c"])    ;; "a, b, c"
(clojure.string/split "a,b,c" #",")         ;; ["a" "b" "c"]
(clojure.string/upper-case "hello")
(clojure.string/lower-case "HELLO")
(clojure.string/trim "  hello  ")
(clojure.string/replace "hello" "l" "L")
(clojure.string/includes? "hello" "ell")

;; Transducers (composable transformations)
(def xf (comp (filter even?) (map #(* % 2))))
(transduce xf + (range 10))     ;; 40
(into [] xf (range 10))          ;; [4 8 12 16]
```


---

# CHAPTER 6: CONCURRENCY


## State and Concurrency

```clojure
;; Atoms (synchronous, uncoordinated)
(def counter (atom 0))
@counter                           ;; 0 (deref)
(swap! counter inc)                ;; returns new value
(swap! counter + 5)
(reset! counter 0)
(compare-and-set! counter 0 1)    ;; returns true if swapped

;; Refs (synchronous, coordinated — STM)
(def balance (ref 1000))
(def savings (ref 500))

(dosync
  (alter balance - 100)
  (alter savings + 100))   ;; atomic!

@balance   ;; 900
@savings   ;; 600

;; Agents (asynchronous)
(def agent-val (agent 0))
(send agent-val inc)
(send-off agent-val #(do (Thread/sleep 100) (inc %)))
(await agent-val)
@agent-val

;; Futures
(def f (future (Thread/sleep 100) 42))
@f         ;; blocks until done: 42
(realized? f)  ;; true after completion

;; Promises
(def p (promise))
(future (Thread/sleep 100) (deliver p 42))
@p         ;; blocks until delivered: 42

;; core.async (CSP-style channels)
(require '[clojure.core.async :as async :refer [chan go <! >! <!! >!! close!]])

(def ch (chan 10))

(go (>! ch 1) (>! ch 2) (>! ch 3) (close! ch))

(go-loop []
  (when-let [val (<! ch)]
    (println val)
    (recur)))

;; pipeline
(def in  (chan 10))
(def out (chan 10))
(async/pipeline 4 out (map #(* % 2)) in)
```


---

# CHAPTER 7: NAMESPACES AND JAVA INTEROP


## Namespaces and JVM

```clojure
;; Namespace definition
(ns my.app.core
  (:require [clojure.string :as str]
            [clojure.set :refer [union intersection]]
            [clojure.java.io :as io])
  (:import [java.util Date]
           [java.io File]))

;; Using the namespace
(str/upper-case "hello")
(union #{1 2} #{2 3})
(io/file "test.txt")

;; Java interop
;; Create objects
(Date.)              ;; new Date()
(StringBuilder.)
(java.util.ArrayList.)

;; Call methods (. operator)
(.toUpperCase "hello")      ;; "HELLO"
(.length "hello")           ;; 5
(.substring "hello" 1 3)    ;; "el"

;; Chain (..  operator)
(.. "hello" toUpperCase (substring 0 3))  ;; "HEL"

;; Static methods
(Math/sqrt 16.0)
(System/currentTimeMillis)
(Integer/parseInt "42")

;; Fields
(.-width (java.awt.Dimension. 800 600))  ;; 800

;; instanceof
(instance? String "hello")   ;; true
(instance? Number 42)         ;; true

;; Type hints (performance)
(defn fast-str [^String s]
  (.toUpperCase s))

;; Collections interop
(into [] (java.util.Arrays/asList (object-array [1 2 3])))
(java.util.Arrays/sort (int-array [3 1 4 1 5]))
```


---

# CHAPTER 8: MACROS AND METAPROGRAMMING


## Macros

```clojure
;; defmacro — code that generates code
(defmacro when2 [test & body]
  `(if ~test (do ~@body)))

(defmacro swap! [a f & args]
  `(reset! ~a (~f @~a ~@args)))

;; Quote (') — don't evaluate
'(+ 1 2)          ;; (+ 1 2) — a list, not 42

;; Syntax-quote (`) — don't evaluate, but allow ~
(let [x 42]
  `(the answer is ~x))   ;; (the answer is 42)

;; Unquote (~) — evaluate inside a syntax-quote
;; Unquote-splicing (~@) — splice a sequence

;; Practical macro: threading
;; -> and ->> are macros!
;; (-> x f g h) becomes (h (g (f x)))
(-> {:name "alice"}
    (assoc :age 30)
    (update :name str/upper-case))
;; {:name "ALICE", :age 30}

(->> [1 2 3 4 5]
     (filter even?)
     (map #(* % 2))
     (reduce +))
;; 12

;; as-> for more complex threading
(as-> "hello world" s
  (str/split s #" ")
  (map str/upper-case s)
  (str/join ", " s))  ;; "HELLO, WORLD"

;; some-> (short-circuit on nil)
(some-> {:name "Alice" :address {:city "NYC"}}
        :address
        :city
        str/upper-case)   ;; "NYC"

;; Testing with clojure.test
(require '[clojure.test :refer :all])

(deftest test-add
  (is (= 3 (+ 1 2)))
  (is (not= 4 (+ 1 2)))
  (is (= [2 4 6] (map #(* % 2) [1 2 3]))))

(run-tests)
```
