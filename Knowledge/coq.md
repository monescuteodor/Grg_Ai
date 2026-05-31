# Coq Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH COQ


## Remarks

Coq is an interactive theorem prover (proof assistant) based on the Calculus of Inductive Constructions. Developed at INRIA (France) since 1984. Coq is used for formal verification of software (CompCert C compiler, Fiat cryptography), mathematics (4-color theorem, Feit-Thompson theorem), and teaching type theory.

Tools: `coqc` (compiler), `coqtop` (REPL), `coqide` (GUI), VS Code with VsCoq extension, ProofGeneral (Emacs).


## Hello World

```coq
(* hello.v *)
Require Import Coq.Strings.String.

Definition hello := "Hello, World!"%string.

Compute hello.
(* = "Hello, World!" : string *)

(* Check extracts the type without evaluating *)
Check hello.
(* hello : string *)
```

```bash
coqc hello.v          # compile
coqtop -l hello.v     # load in interactive mode
coqide hello.v        # open in GUI
```

### Structure of a Coq File

```coq
(* 1. Import libraries *)
Require Import Coq.Arith.Arith.
Require Import Coq.Lists.List.
Import ListNotations.

(* 2. Definitions *)
Definition square (n : nat) : nat := n * n.

(* 3. Lemmas and Theorems *)
Lemma square_positive : forall n : nat, 0 <= square n.
Proof.
  intro n.
  unfold square.
  apply Nat.le_0_l.
Qed.

(* 4. Extraction (to OCaml/Haskell) *)
(* Require Extraction.
   Extraction "mycode.ml" square. *)
```


---

# CHAPTER 2: TYPES AND DEFINITIONS


## Coq's Type System

```coq
(* === SORTS (type universes) === *)
Check nat.        (* nat : Set   (computational type) *)
Check bool.       (* bool : Set *)
Check True.       (* True : Prop  (logical proposition) *)
Check Set.        (* Set : Type  *)
Check Prop.       (* Prop : Type *)
Check Type.       (* Type : Type *)

(* === BASIC TYPES === *)
Check 42.         (* 42 : nat    (natural number) *)
Check (-10)%Z.    (* -10 : Z     (integer, requires Require Import ZArith) *)
Check 3.14.       (* not built-in; use rationals or reals *)
Check true.       (* true : bool *)
Check false.      (* false : bool *)
Check tt.         (* tt : unit   (unit value) *)

(* === DEFINITIONS === *)
Definition mynat : nat := 42.
Definition mybool := true.   (* type inferred *)
Definition pi := 314159265%Z. (* no built-in float *)

(* Functions *)
Definition double (n : nat) : nat := n + n.
Definition add (a b : nat) : nat := a + b.

(* Anonymous function (lambda) *)
Definition triple := fun n : nat => n + n + n.

(* Implicit arguments *)
Definition id {A : Type} (x : A) : A := x.
(* Call: id 5 or @id nat 5 *)

(* === NOTATION === *)
Notation "x ^2" := (x * x) (at level 30).
Compute 5^2.  (* = 25 : nat *)

(* === COMPUTE and EVAL === *)
Compute double 21.    (* = 42 : nat *)
Compute add 3 4.      (* = 7 : nat *)
Eval simpl in add 3 4. (* same *)

(* === SECTION === *)
Section MySection.
  Variable n : nat.  (* section variable *)
  
  Definition double_n := n + n.
  Lemma dn_eq : double_n = 2 * n.
  Proof. unfold double_n. ring. Qed.
End MySection.
(* After section: double_n : nat -> nat *)
```


---

# CHAPTER 3: INDUCTIVE TYPES


## Defining Data Types

```coq
(* === BOOL === *)
Print bool.
(* Inductive bool : Set := true : bool | false : bool *)

(* === NAT (Peano arithmetic) === *)
Print nat.
(* Inductive nat : Set := O : nat | S : nat -> nat *)
(* 0 = O, 1 = S O, 2 = S (S O), ... *)

(* === DEFINING INDUCTIVE TYPES === *)
Inductive day : Type :=
  | Monday | Tuesday | Wednesday | Thursday
  | Friday | Saturday | Sunday.

Definition next_day (d : day) : day :=
  match d with
  | Monday    => Tuesday
  | Tuesday   => Wednesday
  | Wednesday => Thursday
  | Thursday  => Friday
  | Friday    => Saturday
  | Saturday  => Sunday
  | Sunday    => Monday
  end.

(* === PARAMETERIZED TYPES === *)
Inductive option (A : Type) : Type :=
  | None : option A
  | Some : A -> option A.

(* The built-in option is the same *)
Check Some 42.    (* Some 42 : option nat *)
Check None.       (* None : option ?A *)
Check @None nat.  (* None : option nat *)

(* === LISTS === *)
Inductive list (A : Type) : Type :=
  | nil  : list A
  | cons : A -> list A -> list A.
(* Built-in: Require Import Coq.Lists.List *)

(* Using built-in list: *)
Require Import Coq.Lists.List.
Import ListNotations.

Check [1; 2; 3].      (* : list nat *)
Compute length [1;2;3;4].  (* = 4 : nat *)
Compute [1;2] ++ [3;4].    (* = [1;2;3;4] *)
Compute map (fun n => n*2) [1;2;3].  (* = [2;4;6] *)
Compute filter (fun n => n mod 2 =? 0) [1;2;3;4].  (* = [2;4] *)
Compute fold_left (fun a b => a + b) [1;2;3;4;5] 0. (* = 15 *)

(* === RECURSIVE TYPES === *)
Inductive tree (A : Type) : Type :=
  | Leaf : tree A
  | Node : tree A -> A -> tree A -> tree A.

Fixpoint tree_sum (t : tree nat) : nat :=
  match t with
  | Leaf         => 0
  | Node l v r  => tree_sum l + v + tree_sum r
  end.
```


---

# CHAPTER 4: PROPOSITIONS AND PROOFS


## Logic in Coq

```coq
(* === LOGICAL CONNECTIVES === *)
(* In Coq, propositions are types and proofs are terms *)

(* Conjunction: A /\ B *)
Theorem and_intro : forall A B : Prop, A -> B -> A /\ B.
Proof.
  intros A B ha hb.
  split.
  - exact ha.
  - exact hb.
Qed.

(* Disjunction: A \/ B *)
Theorem or_left : forall A B : Prop, A -> A \/ B.
Proof.
  intros A B ha.
  left. exact ha.
Qed.

(* Negation: ~A = A -> False *)
Theorem not_false : ~False.
Proof.
  unfold not. intro h. exact h.
Qed.

(* Implication *)
Theorem modus_ponens : forall P Q : Prop, (P -> Q) -> P -> Q.
Proof.
  intros P Q h hp.
  apply h. exact hp.
Qed.

(* Biconditional: A <-> B *)
Theorem iff_sym : forall A B : Prop, (A <-> B) -> (B <-> A).
Proof.
  intros A B h.
  split.
  - apply h.
  - apply h.
Qed.

(* Universal quantifier: forall x, P x *)
Theorem forall_example : forall n : nat, n + 0 = n.
Proof.
  intro n. ring.
Qed.

(* Existential: exists x, P x *)
Theorem exists_example : exists n : nat, n > 5.
Proof.
  exists 6. auto.
Qed.

(* Equality *)
Theorem eq_symm : forall A : Type, forall x y : A, x = y -> y = x.
Proof.
  intros A x y h. symmetry. exact h.
Qed.
```


---

# CHAPTER 5: TACTICS


## Proof Tactics Reference

```coq
(* === INTRODUCTION TACTICS === *)
(* intro / intros    : introduce hypothesis *)
(* revert            : move hypothesis back to goal *)
(* generalize        : generalize a term *)

Theorem intro_ex : forall n m : nat, n + m = m + n.
Proof.
  intros n m.   (* introduce n and m *)
  ring.
Qed.

(* === EQUALITY TACTICS === *)
(* reflexivity / rfl : prove x = x *)
(* symmetry          : flip equality goal *)
(* rewrite h         : rewrite using h : a = b *)
(* rewrite <- h      : rewrite right-to-left *)
(* congruence        : equality reasoning *)

Theorem rw_ex (n : nat) (h : n = 5) : n + 1 = 6.
Proof.
  rewrite h. reflexivity.
Qed.

(* === LOGICAL TACTICS === *)
(* split              : A /\ B -> prove A, prove B *)
(* left / right       : A \/ B -> choose branch *)
(* destruct h         : case analysis on h *)
(* exists x           : provide witness for exists *)
(* exact h            : close goal with h *)
(* apply h            : apply lemma h to goal *)
(* assumption         : goal is in hypotheses *)
(* contradiction      : derive False *)
(* exfalso            : change goal to False *)

(* === COMPUTATION TACTICS === *)
(* simpl             : reduce by computation *)
(* unfold f          : unfold definition f *)
(* fold f            : fold definition f *)
(* compute           : fully compute *)
(* cbv               : call-by-value reduction *)
(* cbn               : call-by-name reduction *)
(* change e          : replace goal with equal e *)

(* === INDUCTION === *)
(* induction n       : structural induction *)
(* induction n using f_ind : custom induction *)

Theorem plus_0_r : forall n : nat, n + 0 = n.
Proof.
  induction n as [| n' IHn'].
  - simpl. reflexivity.
  - simpl. rewrite IHn'. reflexivity.
Qed.

(* === AUTOMATION === *)
(* auto              : tries simple proofs *)
(* eauto             : like auto with unification *)
(* tauto             : propositional tautology *)
(* omega             : linear arithmetic *)
(* lia               : linear integer arithmetic *)
(* ring              : commutative ring identity *)
(* field             : field identity *)
(* decide            : decidable propositions *)
(* firstorder        : first-order logic *)

Example omega_ex : forall n m : nat, n + m = m + n.
Proof. intros. lia. Qed.
```


---

# CHAPTER 6: FIXPOINTS AND RECURSION


## Recursive Definitions

```coq
Require Import Coq.Arith.Arith.

(* === FIXPOINT (Recursive Functions) === *)
(* Coq requires structurally decreasing recursion *)

Fixpoint factorial (n : nat) : nat :=
  match n with
  | O    => 1
  | S n' => S n' * factorial n'
  end.

Compute factorial 5.  (* = 120 : nat *)

(* === FIBONACCI === *)
Fixpoint fib (n : nat) : nat :=
  match n with
  | O        => 0
  | S O      => 1
  | S (S n') => fib (S n') + fib n'
  end.

Compute fib 10.  (* = 55 *)

(* === MUTUAL FIXPOINT === *)
Fixpoint even (n : nat) : bool :=
  match n with
  | O    => true
  | S n' => odd n'
  end
with odd (n : nat) : bool :=
  match n with
  | O    => false
  | S n' => even n'
  end.

(* === PROVING PROPERTIES OF FIXPOINTS === *)
Theorem factorial_pos : forall n : nat, 0 < factorial n.
Proof.
  induction n as [| n' IH].
  - simpl. auto.
  - simpl. apply Nat.mul_pos_pos.
    + apply Nat.lt_0_succ.
    + exact IH.
Qed.

(* === WELL-FOUNDED RECURSION === *)
(* For non-structural recursion, use Program or measure *)
Require Import Program.

Program Fixpoint gcd (a b : nat) {measure (a + b)} : nat :=
  match b with
  | O => a
  | S _ => gcd b (a mod b)
  end.
Next Obligation.
  apply Nat.lt_add_pos_r.
  apply Nat.mod_upper_bound.
  discriminate.
Defined.

Compute gcd 48 18.  (* = 6 *)
```


---

# CHAPTER 7: MODULES AND LIBRARIES


## Coq Library System

```coq
(* === REQUIRE AND IMPORT === *)
Require Import Coq.Arith.Arith.          (* arithmetic *)
Require Import Coq.Bool.Bool.            (* booleans *)
Require Import Coq.Lists.List.           (* lists *)
Require Import Coq.Strings.String.       (* strings *)
Require Import Coq.ZArith.ZArith.        (* integers *)
Require Import Coq.QArith.QArith.        (* rationals *)
Require Import Coq.Reals.Reals.          (* reals *)
Require Import Coq.Sets.Ensembles.       (* sets *)
Require Import Coq.Logic.Classical.      (* classical logic *)
Require Import Coq.Logic.FunctionalExtensionality.

(* === MODULE SYSTEM === *)
Module MyMath.
  Definition square n := n * n.
  Definition cube n := n * n * n.
  
  Lemma sq_nonneg : forall n : nat, 0 <= square n.
  Proof. intro. apply Nat.le_0_l. Qed.
End MyMath.

(* Use *)
Compute MyMath.square 5.  (* 25 *)
Import MyMath.
Compute square 5.          (* 25 after import *)

(* === STANDARD LIBRARY HIGHLIGHTS === *)

(* Nat arithmetic *)
Check Nat.add_comm.     (* n + m = m + n *)
Check Nat.add_assoc.    (* n + (m + p) = (n + m) + p *)
Check Nat.mul_comm.
Check Nat.div_mod.

(* Boolean *)
Require Import Coq.Bool.Bool.
Check andb_true_iff.    (* a && b = true <-> a = true /\ b = true *)
Check orb_true_iff.

(* Lists *)
Check List.map.
Check List.fold_left.
Check List.In.
Check List.length_app.  (* length (l ++ r) = length l + length r *)
Check List.rev_involutive.  (* rev (rev l) = l *)

(* === COQDOC COMMENTS === *)
(** This is a documentation comment.
    Used by coqdoc to generate HTML documentation.
    
    @param n the input number
    @return the square of n
*)
Definition documented_square (n : nat) : nat := n * n.
```


---

# CHAPTER 8: ADVANCED COQ


## Type Classes, Extraction, and Verification

```coq
(* === TYPE CLASSES === *)
Class Eq (A : Type) := {
  eqb : A -> A -> bool;
  eqb_correct : forall x y, eqb x y = true <-> x = y
}.

Instance NatEq : Eq nat := {
  eqb := Nat.eqb;
  eqb_correct := Nat.eqb_eq
}.

Definition elem {A : Type} `{Eq A} (x : A) (l : list A) : bool :=
  existsb (eqb x) l.

Compute elem 3 [1;2;3;4].  (* = true : bool *)

(* === SIGMA TYPES AND REFINEMENT === *)
(* {x : A | P x} = Sigma type with proof *)
Definition Positive := {n : nat | 0 < n}.

Definition pos5 : Positive := exist _ 5 (Nat.lt_0_succ 4).

Definition add_pos (a b : Positive) : Positive.
  destruct a as [a ha], b as [b hb].
  exists (a + b).
  apply Nat.add_pos_pos; assumption.
Defined.

(* === PROGRAM VERIFIED EXTRACTION === *)
(* Programs extracted to OCaml/Haskell are proved correct *)

Require Extraction.

Definition certified_reverse {A : Type} (l : list A) : 
    {r : list A | r = List.rev l} :=
  exist _ (List.rev l) eq_refl.

(* Extract: *)
(* Extraction "reverse.ml" certified_reverse. *)

(* === CLASSICAL LOGIC (optional) === *)
Require Import Coq.Logic.Classical.

(* Law of excluded middle (not provable in pure CIC) *)
Check classic.   (* forall P : Prop, P \/ ~ P *)

(* Double negation elimination *)
Check NNPP.      (* forall P : Prop, ~~P -> P *)

(* === SSREFLECT (alternative tactic language) === *)
(* From mathcomp.ssreflect Require Import ssreflect ssrbool. *)
(* ssreflect uses: by, case, move=>, apply:, exact: *)

(* === COINDUCTION (infinite structures) === *)
CoInductive Stream (A : Type) : Type :=
  | Cons : A -> Stream A -> Stream A.

CoFixpoint nats_from (n : nat) : Stream nat :=
  Cons n (nats_from (n + 1)).

Definition nat_stream := nats_from 0.
(* Represents the infinite stream 0, 1, 2, 3, ... *)

(* Head and tail of stream *)
Definition hd {A} (s : Stream A) : A :=
  match s with Cons x _ => x end.

Definition tl {A} (s : Stream A) : Stream A :=
  match s with Cons _ s' => s' end.

Compute hd nat_stream.           (* 0 *)
Compute hd (tl nat_stream).      (* 1 *)
Compute hd (tl (tl nat_stream)). (* 2 *)
```
