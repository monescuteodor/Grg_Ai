# Mathematical Logic & Set Theory Reference

## Propositional Logic
### Syntax & Semantics
- **Atoms**: p, q, r...
- **Connectives**: ¬ (not), ∧ (and), ∨ (or), → (implies), ↔ (iff).
- **Truth Tables**: Define truth value of compound statements.
- **Tautology**: True under all interpretations. Contradiction: False under all.

### Normal Forms
- **CNF (Conjunctive Normal Form)**: AND of ORs. (p∨q) ∧ (¬p∨r).
- **DNF (Disjunctive Normal Form)**: OR of ANDs.
- **Resolution**: Rule of inference for CNF. Used in automated theorem proving.

### Logical Equivalence
- **De Morgan's Laws**: ¬(p∧q) ≡ ¬p∨¬q; ¬(p∨q) ≡ ¬p∧¬q.
- **Implication**: p→q ≡ ¬p∨q.
- **Contrapositive**: p→q ≡ ¬q→¬p.

## First-Order Logic (Predicate Logic)
### Quantifiers
- **Universal (∀)**: "For all". ∀x P(x).
- **Existential (∃)**: "There exists". ∃x P(x).
- **Negation**: ¬∀x P(x) ≡ ∃x ¬P(x); ¬∃x P(x) ≡ ∀x ¬P(x).

### Structures & Models
- **Domain**: Set of objects.
- **Interpretation**: Assigns meaning to predicates/functions.
- **Validity**: True in all models. Satisfiability: True in at least one model.

### Completeness & Soundness
- **Soundness**: If ⊢ φ then ⊨ φ. Provable implies true.
- **Completeness**: If ⊨ φ then ⊢ φ. True implies provable. Gödel's Completeness Theorem holds for FOL.

## Set Theory
### ZFC Axioms
- **Extensionality**: Sets equal if same elements.
- **Pairing**: {a,b} exists.
- **Union**: ∪A exists.
- **Power Set**: P(A) exists. |P(A)| = 2^|A|.
- **Infinity**: Infinite set exists.
- **Replacement**: Image of set under function is set.
- **Choice**: Cartesian product of non-empty sets is non-empty.

### Cardinality
- **Countable**: Same size as ℕ (integers, rationals).
- **Uncountable**: Larger than ℕ (reals ℝ). Cantor's Diagonal Argument.
- **Continuum Hypothesis**: No cardinality between ℵ₀ and 2^ℵ₀. Independent of ZFC.

### Ordinals
- **Well-Ordered Sets**: Every non-empty subset has least element.
- **Transfinite Induction**: Generalization of mathematical induction to ordinals.

## Computability & Complexity
### Turing Machines
- **Model**: Tape, head, state transition table.
- **Church-Turing Thesis**: Any effectively calculable function is computable by TM.

### Undecidability
- **Halting Problem**: No algorithm determines if arbitrary program halts. Proof by diagonalization.
- **Rice's Theorem**: All non-trivial semantic properties of programs are undecidable.

### Complexity Classes
- **P**: Solvable in polynomial time.
- **NP**: Verifiable in polynomial time.
- **NP-Complete**: Hardest problems in NP (SAT, TSP, Clique). If one in P, then P=NP.
- **EXPTIME**: Solvable in exponential time.