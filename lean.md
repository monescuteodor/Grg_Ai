# Lean Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH LEAN


## Remarks

Lean is a functional programming language and interactive theorem prover developed at Microsoft Research by Leonardo de Moura. Lean 4 (2021) is a complete rewrite targeting both theorem proving and general systems programming. It is used in formal mathematics (Mathlib), verified software, and research.

Tools: `lean` (CLI), `lake` (build tool), VS Code with Lean extension (best experience).


## Hello World

```lean
-- hello.lean
def main : IO Unit := do
  IO.println "Hello, World!"
  IO.println "Hello, Lean!"
```

```bash
lean --run hello.lean      # run directly
lake new myproject         # create project
lake build                 # build project
lake exe myapp             # run executable
```

### lakefile.lean (project config)

```lean
import Lake
open Lake DSL

package «myproject» where
  name := "myproject"

lean_lib «Myproject» where
  -- library settings

@[default_target]
lean_exe «myproject» where
  root := `Main
```


---

# CHAPTER 2: TYPES AND EXPRESSIONS


## Lean 4 Type System

```lean
-- === BASIC TYPES ===
#check Nat         -- ℕ (natural numbers: 0, 1, 2, ...)
#check Int         -- ℤ (integers: ..., -1, 0, 1, ...)
#check Float       -- 64-bit IEEE float
#check Bool        -- true | false
#check Char        -- Unicode character
#check String      -- UTF-8 string
#check Unit        -- ()  the unit type
#check Empty       -- uninhabited type

-- === LITERALS ===
#eval (42 : Nat)
#eval (42 : Int)
#eval (-10 : Int)
#eval (3.14 : Float)
#eval true
#eval 'A'
#eval "Hello"
#eval ()

-- === TYPE ASCRIPTION ===
def x : Nat := 42
def y : Int := -10
def f : Float := 3.14

-- === TYPE INFERENCE ===
def a := 42        -- inferred as Nat
def b := -10       -- inferred as Int
def c := 3.14      -- inferred as Float
def s := "hello"   -- String

-- === ARITHMETIC ===
#eval 3 + 4        -- 7
#eval 10 - 3       -- 7 (Nat: saturates at 0)
#eval (3 : Int) - 10  -- -7
#eval 3 * 4        -- 12
#eval 10 / 3       -- 3 (integer division for Nat)
#eval 10 % 3       -- 1
#eval 2 ^ 8        -- 256

-- === BOOLEANS ===
#eval true && false      -- false
#eval true || false      -- true
#eval !true              -- false
#eval (3 == 3)           -- true
#eval (3 != 4)           -- true
#eval (3 < 5)            -- true
#eval (3 ≤ 3)            -- true  (Unicode or <=)

-- === STRINGS ===
#eval String.length "Hello"      -- 5
#eval "Hello" ++ " " ++ "World"  -- "Hello World"
#eval String.toUpper "hello"     -- "HELLO"
#eval String.startsWith "hello" "hel"  -- true
```


---

# CHAPTER 3: FUNCTIONS AND PATTERN MATCHING


## Lean Functions

```lean
-- === BASIC FUNCTIONS ===
def double (n : Nat) : Nat := n * 2

def add (a b : Nat) : Nat := a + b

-- Implicit arguments (inferred by type checker)
def identity {α : Type} (x : α) : α := x

-- With multiple arguments
def compose {α β γ : Type} (f : β → γ) (g : α → β) (x : α) : γ :=
  f (g x)

-- === PATTERN MATCHING ===
def isZero : Nat → Bool
  | 0     => true
  | _ + 1 => false

def factorial : Nat → Nat
  | 0     => 1
  | n + 1 => (n + 1) * factorial n

def fib : Nat → Nat
  | 0 => 0
  | 1 => 1
  | n + 2 => fib (n + 1) + fib n

-- === STRUCTURES (pattern match) ===
structure Point where
  x : Float
  y : Float

def distance (p q : Point) : Float :=
  let dx := p.x - q.x
  let dy := p.y - q.y
  Float.sqrt (dx * dx + dy * dy)

-- Pattern match on structure:
def getX : Point → Float
  | ⟨x, _⟩ => x
  -- or: | p => p.x

-- === MATCH EXPRESSION ===
def classify (n : Int) : String :=
  match n.compare 0 with
  | .lt => "negative"
  | .eq => "zero"
  | .gt => "positive"

-- === LAMBDA ===
def double' : Nat → Nat := fun n => n * 2
def add' := fun (a b : Nat) => a + b
def triple := (· * 3)   -- dot notation shorthand

-- === DO NOTATION ===
def main : IO Unit := do
  let n ← IO.getStdin >>= fun h => do
    let line ← h.getLine
    return line.trim.toNat!
  IO.println s!"You entered: {n}"
  IO.println s!"Double: {double n}"
```


---

# CHAPTER 4: DATA STRUCTURES


## Lists, Options, and Algebraic Types

```lean
-- === LIST ===
#eval [1, 2, 3, 4, 5]
#eval ([] : List Nat)
#eval List.length [1, 2, 3]     -- 3
#eval List.head? [1, 2, 3]      -- some 1
#eval List.tail [1, 2, 3]       -- [2, 3]
#eval List.append [1, 2] [3, 4] -- [1, 2, 3, 4]
#eval [1, 2] ++ [3, 4]          -- same
#eval List.map (· * 2) [1, 2, 3]    -- [2, 4, 6]
#eval List.filter (· > 2) [1, 2, 3, 4]  -- [3, 4]
#eval List.foldl (· + ·) 0 [1, 2, 3, 4, 5]  -- 15
#eval List.sum [1, 2, 3, 4, 5]  -- 15
#eval List.reverse [1, 2, 3]    -- [3, 2, 1]
#eval List.zip [1, 2, 3] ['a', 'b', 'c']

-- Cons notation:
#eval 1 :: 2 :: 3 :: []    -- [1, 2, 3]

-- === OPTION ===
def safeDiv (a b : Nat) : Option Nat :=
  if b == 0 then none else some (a / b)

#eval safeDiv 10 2    -- some 5
#eval safeDiv 10 0    -- none

-- Pattern match on Option:
def printDiv (a b : Nat) : String :=
  match safeDiv a b with
  | none   => "Division by zero"
  | some r => s!"Result: {r}"

-- Option combinators:
#eval (some 5).map (· * 2)           -- some 10
#eval (none : Option Nat).map (· * 2) -- none
#eval (some 5).bind (safeDiv 10)     -- some 2
#eval (some 5).getD 0                -- 5
#eval (none : Option Nat).getD 0     -- 0

-- === RESULT (EXCEPT) ===
def parseNat (s : String) : Except String Nat :=
  match s.toNat? with
  | none   => .error s!"Not a number: {s}"
  | some n => .ok n

-- === ALGEBRAIC DATA TYPES ===
inductive Shape where
  | circle    : Float → Shape
  | rectangle : Float → Float → Shape
  | triangle  : Float → Float → Float → Shape

def area : Shape → Float
  | .circle r        => Float.pi * r * r
  | .rectangle w h   => w * h
  | .triangle a b c  =>
      let s := (a + b + c) / 2
      Float.sqrt (s * (s - a) * (s - b) * (s - c))

-- === MUTUAL RECURSION ===
mutual
  def isEven : Nat → Bool
    | 0     => true
    | n + 1 => isOdd n
  
  def isOdd : Nat → Bool
    | 0     => false
    | n + 1 => isEven n
end
```


---

# CHAPTER 5: THEOREM PROVING BASICS


## Propositions and Proofs

```lean
-- === PROPOSITIONS AS TYPES ===
-- In Lean, propositions are types, proofs are values
-- This is the Curry-Howard correspondence

-- Simple theorem
theorem add_comm (a b : Nat) : a + b = b + a := by
  omega  -- omega solves linear arithmetic

-- === TACTICS ===
theorem example1 (p q : Prop) (hp : p) (hq : q) : p ∧ q := by
  constructor        -- split goal into p and q
  · exact hp         -- prove p using hp
  · exact hq         -- prove q using hq

theorem example2 (p q : Prop) (h : p ∧ q) : q ∧ p := by
  obtain ⟨hp, hq⟩ := h   -- destructure h
  exact ⟨hq, hp⟩

-- === INDUCTION ===
theorem sum_formula (n : Nat) : 2 * (List.range (n + 1)).sum = n * (n + 1) := by
  induction n with
  | zero      => simp
  | succ n ih => simp [List.sum_range_succ]; linarith

-- === BASIC TACTICS ===
-- rfl     : prove a = a (reflexivity)
-- exact   : provide exact proof term
-- apply   : apply a lemma
-- intro   : introduce hypothesis
-- cases   : case analysis
-- induction : proof by induction
-- simp    : simplify using lemmas
-- omega   : linear arithmetic over Nat/Int
-- linarith : linear arithmetic
-- ring    : ring identity
-- norm_num : numerical computation
-- tauto   : propositional tautology

example : 1 + 1 = 2 := by rfl
example : 2 + 2 = 4 := by norm_num
example (n : Nat) : n + 0 = n := by simp
example (a b c : Int) : (a + b) * c = a * c + b * c := by ring

-- === TERM-MODE PROOFS ===
theorem and_intro (p q : Prop) (hp : p) (hq : q) : p ∧ q :=
  And.intro hp hq

theorem and_elim_left (p q : Prop) (h : p ∧ q) : p :=
  h.left

theorem modus_ponens (p q : Prop) (h1 : p → q) (h2 : p) : q :=
  h1 h2
```


---

# CHAPTER 6: TYPE CLASSES


## Lean 4 Type Classes

```lean
-- === DEFINING TYPE CLASSES ===
class Printable (α : Type) where
  toString : α → String

instance : Printable Nat where
  toString := Nat.repr

instance : Printable Bool where
  toString | true => "true" | false => "false"

def print [Printable α] (x : α) : IO Unit :=
  IO.println (Printable.toString x)

-- === STANDARD TYPE CLASSES ===
-- BEq (boolean equality): ==, !=
-- Ord: compare, <, <=, >, >=
-- Repr: repr (debug display)
-- ToString: toString (human display)
-- Inhabited: default
-- Hashable: hash
-- Functor: map
-- Monad: bind, pure

-- Custom Ord instance:
structure Pair where
  fst : Nat
  snd : Nat

instance : Ord Pair where
  compare p q :=
    match compare p.fst q.fst with
    | .eq => compare p.snd q.snd
    | ord => ord

-- === FUNCTOR / MONAD ===
#eval List.map (· + 1) [1, 2, 3]   -- [2, 3, 4]
#eval (some 5).map (· * 2)          -- some 10

-- Monad do notation:
def example : Option Nat := do
  let x ← some 5
  let y ← some 10
  return x + y

-- IO monad:
def readAndDouble : IO Unit := do
  let line ← (← IO.getStdin).getLine
  let n := line.trim.toNat!
  IO.println s!"Double: {n * 2}"

-- === DERIVING ===
structure Color where
  r : Nat
  g : Nat
  b : Nat
deriving Repr, BEq, Hashable

-- Use:
def red : Color := ⟨255, 0, 0⟩
#eval red          -- Color.mk 255 0 0
```


---

# CHAPTER 7: DEPENDENT TYPES


## Lean's Powerful Type System

```lean
-- === DEPENDENT TYPES ===
-- Types can depend on values

-- Vector: list with known length
def Vec (α : Type) (n : Nat) := { v : List α // v.length = n }

-- Or use the built-in Fin type:
-- Fin n = {k : Nat // k < n}
#eval (⟨3, by norm_num⟩ : Fin 5)   -- ⟨3, ...⟩

-- === SIGMA TYPES (dependent pairs) ===
-- ⟨t, h⟩ : Σ (x : α), P x
-- The second component's type depends on first

def nonzero_example : Σ (n : Nat), n ≠ 0 :=
  ⟨5, by norm_num⟩

-- === SUBTYPE ===
def Positive := {n : Nat // 0 < n}

def pos5 : Positive := ⟨5, by norm_num⟩
#eval pos5.val     -- 5

-- === PROPOSITIONS AS TYPES ===
-- P : Prop means P is a proposition
-- h : P    means h is a proof of P

-- Functions between propositions are implications:
-- (h : P → Q) means h proves "P implies Q"

-- === REFINEMENT TYPES ===
def safeIndex (n : Nat) (xs : List α) (h : n < xs.length) : α :=
  xs.get ⟨n, h⟩

-- Usage: must provide proof that index is in bounds
example : (safeIndex 1 [10, 20, 30] (by norm_num)) = 20 := by rfl

-- === PROOFS IN PROGRAMS ===
def safeDivide (a : Nat) (b : Nat) (h : b ≠ 0) : Nat :=
  a / b

-- The h parameter ensures b ≠ 0 at type level

-- === UNIVERSE POLYMORPHISM ===
def myId.{u} {α : Type u} (x : α) : α := x

-- Works for any universe level:
#eval myId 42          -- works for Type 0
-- Also works for Type 1, Type 2, etc.
```


---

# CHAPTER 8: MATHLIB AND ADVANCED


## Mathematical Library and Advanced Features

```lean
-- Mathlib (add to lakefile.lean):
-- require mathlib from git "https://github.com/leanprover-community/mathlib4"

-- import Mathlib

-- === NUMBER THEORY ===
-- import Mathlib.Data.Nat.Prime

-- example (p : Nat) (hp : Nat.Prime p) : 2 ≤ p := hp.two_le

-- example : Nat.Prime 17 := by decide

-- theorem inf_primes : ∀ n, ∃ p, n ≤ p ∧ Nat.Prime p :=
--   Nat.infinite_setOf_prime.exists_gt

-- === ALGEBRA ===
-- import Mathlib.Algebra.Group.Basic
-- Variables can be over abstract groups/rings/fields

-- variable {G : Type*} [Group G]
-- theorem mul_self_inv (g : G) : g * g⁻¹ = 1 := mul_inv_cancel g

-- === ANALYSIS ===
-- import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

-- #check Real.sin_sq_add_cos_sq  -- sin²x + cos²x = 1

-- === TACTIC AUTOMATION ===
-- aesop   : automated search
-- decide  : decidable propositions
-- native_decide : faster decide
-- positivity : prove positivity
-- gcongr  : congruence lemmas

example : (0 : Int) ≤ 2^10 := by positivity
example : 2 + 3 = 5 := by decide
example : Nat.Prime 97 := by decide

-- === META-PROGRAMMING ===
-- Lean 4 has first-class macros

macro "swap" a:ident b:ident : tactic => `(tactic|
  (have tmp := $a; replace $a := $b; replace $b := tmp))

-- === PARTIAL EVALUATION / REFLECTION ===
#eval (open Lean in do
  let env ← getEnv
  return env.allImportedModuleNames.size)

-- === IO AND SYSTEM ===
def main : IO Unit := do
  let args ← IO.getArgs
  if args.isEmpty then
    IO.println "No arguments"
  else
    for arg in args do
      IO.println s!"Arg: {arg}"

  -- File I/O
  let contents ← IO.FS.readFile "data.txt"
  IO.println contents

  -- Exception handling
  try
    let n := "abc".toNat!
    IO.println n
  catch e =>
    IO.eprintln s!"Error: {e}"
```
