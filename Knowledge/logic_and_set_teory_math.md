# CHAPTER 12: MATHEMATICAL LOGIC & SET THEORY (ADVANCED)


## Descriptive Set Theory

### Polish Spaces

**Definition:**
Separable completely metrizable topological space.
- Examples: ℝⁿ, ℂⁿ, Baire space ℕ^ℕ, Cantor space 2^ℕ, Hilbert cube [0,1]^ℕ

**Borel Hierarchy:**
Σ⁰₁ = open sets
Π⁰₁ = closed sets
Σ⁰_{α+1} = countable unions of Π⁰_α
Π⁰_{α+1} = countable intersections of Σ⁰_α
For limit λ: Σ⁰_λ = Π⁰_λ = ∪_{α<λ} Σ⁰_α

**Properties:**
- Borel = ∪_{α<ω₁} Σ⁰_α = ∪_{α<ω₁} Π⁰_α
- For uncountable Polish space: hierarchy is proper
- Universal Σ⁰_α sets exist

**Analytic Sets (Σ¹₁):**
Continuous images of Borel sets.
- Souslin's theorem: A is Borel iff A and A' are analytic
- Separation: disjoint analytic sets can be separated by Borel set
- Projection of Borel in product is analytic

**Co-analytic (Π¹₁):**
Complements of analytic sets.

**Projective Hierarchy:**
Σ¹_{n+1} = projections of Π¹ₙ
Π¹_{n+1} = complements of Σ¹_{n+1}
Δ¹ₙ = Σ¹ₙ ∩ Π¹ₙ

**Regularity Properties:**
- Baire property: differs from open by meager set
- Lebesgue measurability
- Perfect set property: either countable or contains perfect subset
- All analytic sets have all three properties
- For projective sets: requires large cardinals

### Determinacy

**Games:**
For A ⊆ X^ℕ, players I and II alternate choosing xₙ ∈ X.
I wins if (x₀, x₁, ...) ∈ A.

**Determinacy (AD):**
Every game is determined (one player has winning strategy).
- False in ZFC (using AC)
- True in L(ℝ) under large cardinals

**Consequences of AD:**
- All sets of reals are Lebesgue measurable
- All sets have Baire property
- All sets have perfect set property
- No well-ordering of reals

**Projective Determinacy (PD):**
All projective games are determined.
- Consistent relative to large cardinals
- Implies regularity for projective sets

**Borel Determinacy:**
All Borel games are determined (Martin, 1975).
- Proof requires replacement to ω₁
- Friedman: cannot be proved in ZC alone

**Axiom of Determinacy (AD_L(ℝ)):**
AD holds in L(ℝ) (smallest inner model containing all reals).
- Follows from existence of infinitely many Woodin cardinals with measurable above (Martin-Steel)

### Large Cardinals

**Inaccessible Cardinal:**
κ is inaccessible if:
- Regular: cf(κ) = κ
- Strong limit: λ < κ ⇒ 2^λ < κ
- Existence: not provable in ZFC

**Measurable Cardinal:**
κ with non-principal κ-complete ultrafilter.
- First large cardinal beyond inaccessible
- Implies existence of 0#
- Inner model L[U]

**Supercompact Cardinal:**
For all λ ≥ κ, ∃ elementary embedding j: V → M with:
- crit(j) = κ
- j(κ) > λ
- M^λ ⊆ M

**Woodin Cardinal:**
For every f: κ → κ, ∃ α < κ and elementary j: V → M with:
- crit(j) = α
- j(α) > κ
- V_{j(f)(α)} ⊆ M

**Large Cardinal Hierarchy:**
ZFC + Inaccessible < Measurable < Supercompact < Huge < Rank-into-Rank

**Inner Model Theory:**
- L = Gödel's constructible universe
- L[U] for measurable U
- Core model induction
- Ultimate L (Woodin's program)

**Forcing Axioms:**
- MA(κ): Martin's Axiom for κ
- PFA: Proper Forcing Axiom
- MM: Martin's Maximum
- BPFA: Bounded PFA

**Consequences of PFA:**
- 2^{ℵ₀} = ℵ₂
- Every two ℵ₁-dense sets of reals are isomorphic
- Souslin hypothesis
- Failure of square principles

### Forcing

**Cohen Forcing:**
Add generic real not in ground model.
- Conditions: finite partial functions p: ω → 2
- Generic filter G gives new real g = ∪G
- Cohen real: generic for this forcing

**Cardinal Arithmetic:**
- Cohen forcing: preserves cardinals, adds ℵ₂^V Cohen reals
- Easton forcing: control 2^κ for regular κ
- Prikry forcing: change cofinality without collapsing cardinals

**Iterated Forcing:**
- Finite support iteration
- Countable support iteration
- Revised countable support
- Proper iteration

**Cardinal Invariants of the Continuum:**
- add(N): additivity of null ideal
- cov(N): covering number of null ideal
- non(N): smallest non-null set
- cof(N): cofinality of null ideal
- b: bounding number
- d: dominating number
- Cichon's diagram: inequalities between invariants

**Forcing and Large Cardinals:**
- Levy collapse: collapse cardinals
- Silver forcing: preserve large cardinals
- Radin forcing: iterate Prikry forcing

### Inner Models & Constructibility

**Constructible Universe L:**
L = ∪_{α∈Ord} L_α
- L₀ = ∅
- L_{α+1} = Def(L_α) (definable subsets)
- L_λ = ∪_{α<λ} L_α for limit λ

**Properties of L:**
- Axiom of Constructibility: V = L
- V = L implies GCH and AC
- L is smallest inner model
- 0# exists iff L ≠ HOD

**Fine Structure:**
Jensen's analysis of L and related models.
- Projecta
- Master codes
- □_κ principles
- Morasses

**Core Model:**
K = core model (under no large cardinals).
- Absoluteness properties
- Covering lemma
- Anti-large cardinal hypothesis

### Reverse Mathematics

**Subsystems of Second-Order Arithmetic:**
- RCA₀: recursive comprehension + Σ⁰₁ induction
- WKL₀: RCA₀ + weak König's lemma
- ACA₀: RCA₀ + arithmetic comprehension
- ATR₀: ACA₀ + arithmetical transfinite recursion
- Π¹₁-CA₀: ACA₀ + Π¹₁ comprehension

**Equivalences:**
- WKL₀ ⇔ Heine-Borel theorem, extreme value theorem, Jordan curve theorem
- ACA₀ ⇔ Bolzano-Weierstrass, sequential completeness, existence of bases
- ATR₀ ⇔ determinacy of open games, comparability of well-orderings
- Π¹₁-CA₀ ⇔ Cantor-Bendixson theorem, perfect set theorem for analytic sets

**Big Five:**
Most theorems of ordinary mathematics equivalent to one of RCA₀, WKL₀, ACA₀, ATR₀, Π¹₁-CA₀.

### Computability Theory

**Turing Degrees:**
For A, B ⊆ ℕ: A ≤_T B if A computable from oracle B.
- Turing degree: equivalence class under ≤_T
- 0 = computable sets
- 0' = halting problem
- 0'' = jump of 0'

**Jump Operator:**
A' = {e : φ_e^A(e) halts}
- A <_T A'
- A' is complete Σ⁰₁(A)

**Post's Problem:**
∃ c with 0 < c < 0'?
- Solved by Friedberg-Muchnik: yes (independent)
- Priority method

**Priority Constructions:**
- Finite injury
- Infinite injury
- Tree method
- 0'''-priority

**Randomness:**
- Martin-Löf random: passes all computable statistical tests
- Kolmogorov random: K(x|n) ≥ n - O(1)
- 1-random, 2-random, etc.
- K-trivial sets

**Reverse Mathematics of Combinatorics:**
- Ramsey's theorem for pairs: equivalent to systems between RCA₀ and ACA₀
- Hindman's theorem: very strong
- Graph minor theorem: beyond Π¹₁-CA₀


---
