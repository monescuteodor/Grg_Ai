# Mathematics & Geometry Complete Reference

---

# CHAPTER 1: FOUNDATIONS OF MATHEMATICS


## Remarks

Mathematics is the abstract science of number, quantity, and space, either as abstract concepts (pure mathematics) or as applied to other disciplines (applied mathematics). Geometry, one of its oldest branches, studies shapes, sizes, properties of space, and relationships between figures. Modern mathematics spans from foundational logic to advanced abstract structures, with applications in physics, engineering, computer science, cryptography, and artificial intelligence.

Key Areas: Algebra, Analysis, Geometry, Topology, Number Theory, Combinatorics, Probability, Logic, Category Theory.


## Mathematical Notation & Symbols

```
ℕ  = {0, 1, 2, 3, ...}          -- Natural numbers
ℤ  = {..., -2, -1, 0, 1, 2, ...} -- Integers
ℚ  = {p/q : p,q ∈ ℤ, q ≠ 0}     -- Rational numbers
ℝ  = (-∞, +∞)                   -- Real numbers
ℂ  = {a + bi : a,b ∈ ℝ}         -- Complex numbers
ℍ  = Quaternions                -- Hamilton numbers

∀  -- For all (universal quantifier)
∃  -- There exists (existential quantifier)
∃! -- There exists exactly one
∈  -- Element of
⊆  -- Subset of
⊂  -- Proper subset of
∪  -- Union
∩  -- Intersection
∅  -- Empty set
¬  -- Not (logical negation)
∧  -- And (logical conjunction)
∨  -- Or (logical disjunction)
⇒  -- Implies
⇔  -- If and only if (iff)
∴  -- Therefore
∎  -- End of proof (QED)
∑  -- Summation
∏  -- Product
∫  -- Integral
∂  -- Partial derivative
∇  -- Nabla / Del operator
∞  -- Infinity
≈  -- Approximately equal
≡  -- Congruent / Identically equal
⊕  -- Direct sum
⊗  -- Tensor product
```


## Basic Axioms & Laws

### Field Axioms (ℝ)
For all a, b, c ∈ ℝ:

**Addition:**
- Closure:       a + b ∈ ℝ
- Commutativity: a + b = b + a
- Associativity: (a + b) + c = a + (b + c)
- Identity:      a + 0 = a
- Inverse:       a + (-a) = 0

**Multiplication:**
- Closure:       a · b ∈ ℝ
- Commutativity: a · b = b · a
- Associativity: (a · b) · c = a · (b · c)
- Identity:      a · 1 = a
- Inverse:       a · a⁻¹ = 1  (for a ≠ 0)

**Distributivity:** a · (b + c) = a · b + a · c

### Order Axioms
- Trichotomy: ∀a ∈ ℝ, exactly one holds: a > 0, a = 0, or a < 0
- Closure under +, ·: If a > 0 and b > 0, then a + b > 0 and a · b > 0

### Completeness Axiom
Every non-empty subset of ℝ bounded above has a least upper bound (supremum).


## Logical Foundations

### Propositional Logic
A proposition is a declarative statement that is either true (T) or false (F).

**Truth Table for Logical Connectives:**

| P | Q | ¬P | P∧Q | P∨Q | P⇒Q | P⇔Q |
|---|---|----|-----|-----|-----|-----|
| T | T | F  |  T  |  T  |  T  |  T  |
| T | F | F  |  F  |  T  |  F  |  F  |
| F | T | T  |  F  |  T  |  T  |  F  |
| F | F | T  |  F  |  F  |  T  |  T  |

### Predicate Logic
Extends propositional logic with quantifiers over variables.

**Quantifier Laws:**
- ¬(∀x P(x)) ⇔ ∃x ¬P(x)        -- De Morgan's for ∀
- ¬(∃x P(x)) ⇔ ∀x ¬P(x)        -- De Morgan's for ∃
- ∀x (P(x) ∧ Q(x)) ⇔ (∀x P(x)) ∧ (∀x Q(x))
- ∃x (P(x) ∨ Q(x)) ⇔ (∃x P(x)) ∨ (∃x Q(x))

### Proof Techniques

**Direct Proof:**
Assume P is true, deduce Q through logical steps.
Example: Prove "If n is even, then n² is even."
Proof: n even ⇒ n = 2k for some k ∈ ℤ
       n² = (2k)² = 4k² = 2(2k²), which is even. ∎

**Proof by Contradiction (Reductio ad absurdum):**
Assume ¬P, derive a contradiction.
Example: Prove √2 is irrational.
Proof: Assume √2 = p/q in lowest terms.
       2 = p²/q² ⇒ p² = 2q² ⇒ p² even ⇒ p even.
       Let p = 2k: 4k² = 2q² ⇒ q² = 2k² ⇒ q even.
       Contradiction: p,q both even, not in lowest terms. ∎

**Proof by Induction:**
Base case: Prove P(0) or P(1).
Inductive step: Assume P(k), prove P(k+1).
Example: Prove 1 + 2 + ... + n = n(n+1)/2.
Base: n=1: 1 = 1(2)/2 = 1 ✓
Step: Assume for n=k. For n=k+1:
      1+...+k+(k+1) = k(k+1)/2 + (k+1) = (k+1)(k/2 + 1) = (k+1)(k+2)/2. ∎

**Proof by Contrapositive:**
Prove P ⇒ Q by proving ¬Q ⇒ ¬P.
Example: "If n² is even, then n is even."
Contrapositive: "If n is odd, then n² is odd."
Proof: n odd ⇒ n = 2k+1 ⇒ n² = 4k²+4k+1 = 2(2k²+2k)+1, odd. ∎


## Set Theory

### Basic Definitions
A set is a well-defined collection of distinct objects.

**Set Operations:**
- Union:        A ∪ B = {x : x ∈ A ∨ x ∈ B}
- Intersection: A ∩ B = {x : x ∈ A ∧ x ∈ B}
- Difference:   A \ B = {x : x ∈ A ∧ x ∉ B}
- Complement:   A' = {x ∈ U : x ∉ A}
- Symmetric:    A Δ B = (A \ B) ∪ (B \ A)
- Cartesian:    A × B = {(a,b) : a ∈ A, b ∈ B}
- Power set:    P(A) = {S : S ⊆ A}, |P(A)| = 2^|A|

**Laws of Set Theory:**
- Idempotent:    A ∪ A = A,  A ∩ A = A
- Commutative:   A ∪ B = B ∪ A,  A ∩ B = B ∩ A
- Associative:   (A ∪ B) ∪ C = A ∪ (B ∪ C)
- Distributive:  A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)
- De Morgan:     (A ∪ B)' = A' ∩ B'
- Absorption:    A ∪ (A ∩ B) = A

### Cardinality
- |A| = number of elements in finite set A
- ℵ₀ = |ℕ| (countably infinite)
- 𝔠 = |ℝ| = 2^ℵ₀ (continuum, uncountably infinite)
- Cantor's Theorem: |A| < |P(A)| for any set A
- Continuum Hypothesis: There is no set S with ℵ₀ < |S| < 𝔠

### Relations & Functions

**Relation:** R ⊆ A × B
- Reflexive:    ∀a ∈ A, (a,a) ∈ R
- Symmetric:    (a,b) ∈ R ⇒ (b,a) ∈ R
- Transitive:   (a,b) ∈ R ∧ (b,c) ∈ R ⇒ (a,c) ∈ R
- Equivalence:  Reflexive + Symmetric + Transitive

**Function:** f: A → B, ∀a ∈ A, ∃! b ∈ B: f(a) = b
- Injective (one-to-one): f(a₁) = f(a₂) ⇒ a₁ = a₂
- Surjective (onto):      ∀b ∈ B, ∃a ∈ A: f(a) = b
- Bijective:              Injective + Surjective
- Inverse:                f⁻¹ exists iff f is bijective

**Function Composition:**
(f ∘ g)(x) = f(g(x))
- Associative: (f ∘ g) ∘ h = f ∘ (g ∘ h)
- Identity:    f ∘ id = id ∘ f = f


## Number Theory Foundations

### Divisibility
a | b ("a divides b") iff ∃k ∈ ℤ: b = a·k

**Properties:**
- a | b ∧ a | c ⇒ a | (bx + cy) for any x,y ∈ ℤ
- a | b ∧ b | c ⇒ a | c
- a | b ∧ b | a ⇒ a = ±b

### Division Algorithm
For a, b ∈ ℤ, b > 0: ∃! q, r ∈ ℤ:
a = bq + r,  where 0 ≤ r < b

### GCD & LCM
- gcd(a,b) = largest d such that d | a and d | b
- lcm(a,b) = smallest m such that a | m and b | m
- gcd(a,b) · lcm(a,b) = |a·b|
- Euclidean Algorithm: gcd(a,b) = gcd(b, a mod b)

### Fundamental Theorem of Arithmetic
Every integer n > 1 can be written uniquely as:
n = p₁^a₁ · p₂^a₂ · ... · pₖ^aₖ
where p₁ < p₂ < ... < pₖ are primes and aᵢ ≥ 1.

### Congruences
a ≡ b (mod n) iff n | (a - b)

**Properties:**
- a ≡ b (mod n) ∧ c ≡ d (mod n) ⇒ a+c ≡ b+d (mod n)
- a ≡ b (mod n) ∧ c ≡ d (mod n) ⇒ ac ≡ bd (mod n)
- a ≡ b (mod n) ⇒ aᵏ ≡ bᵏ (mod n)

**Fermat's Little Theorem:** If p is prime and p ∤ a:
a^(p-1) ≡ 1 (mod p)

**Euler's Theorem:** If gcd(a,n) = 1:
a^φ(n) ≡ 1 (mod n)
where φ(n) = number of integers 1 ≤ k ≤ n with gcd(k,n) = 1

**Chinese Remainder Theorem:**
If n₁, n₂, ..., nₖ are pairwise coprime, the system:
x ≡ a₁ (mod n₁)
x ≡ a₂ (mod n₂)
...
x ≡ aₖ (mod nₖ)
has a unique solution modulo N = n₁·n₂·...·nₖ.


## Mathematical Structures

### Groups
A group (G, ·) is a set G with operation · satisfying:
1. Closure:     ∀a,b ∈ G, a·b ∈ G
2. Associative: (a·b)·c = a·(b·c)
3. Identity:    ∃e ∈ G: a·e = e·a = a
4. Inverse:     ∀a ∈ G, ∃a⁻¹ ∈ G: a·a⁻¹ = e

**Abelian Group:** Also commutative: a·b = b·a

**Examples:**
- (ℤ, +), (ℚ, +), (ℝ, +), (ℂ, +) -- additive groups
- (ℤₙ, +) -- integers mod n
- (ℤₙ*, ·) -- units mod n (multiplicative group)
- Sₙ -- symmetric group (permutations of n elements)
- GL(n,ℝ) -- general linear group (invertible n×n matrices)

**Subgroups:** H ⊆ G is a subgroup if H is closed under · and inverses.

**Cyclic Group:** G = ⟨g⟩ = {gⁿ : n ∈ ℤ} for some generator g.

**Lagrange's Theorem:** If H ≤ G is finite, |H| divides |G|.

### Rings
A ring (R, +, ·) is an abelian group under + with · satisfying:
1. Closure under ·
2. Associative: (a·b)·c = a·(b·c)
3. Distributive: a·(b+c) = a·b + a·c and (b+c)·a = b·a + c·a

**Commutative Ring:** a·b = b·a
**Ring with Unity:** ∃1 ∈ R: a·1 = 1·a = a
**Integral Domain:** Commutative ring with unity, no zero divisors
**Field:** Commutative ring with unity where every non-zero element has multiplicative inverse

**Examples:**
- (ℤ, +, ·) -- ring (not field)
- (ℚ, +, ·), (ℝ, +, ·), (ℂ, +, ·) -- fields
- ℤₙ -- ring; field iff n is prime
- ℝ[x] -- polynomial ring
- Mₙ(ℝ) -- matrix ring (non-commutative)

### Fields
A field F is a set with + and · where:
- (F, +) is an abelian group
- (F\{0}, ·) is an abelian group
- Distributive law holds

**Field Extensions:**
If K ⊆ F are fields, F is an extension of K.
- [F:K] = dimension of F as vector space over K
- Algebraic extension: every element of F is algebraic over K
- Transcendental: not algebraic (e.g., π, e over ℚ)

**Finite Fields (Galois Fields):**
For every prime p and n ≥ 1, there exists a unique field with pⁿ elements, denoted GF(pⁿ) or 𝔽_{pⁿ}.

### Vector Spaces
A vector space V over field F with operations + and scalar multiplication satisfies:
1. (V, +) is an abelian group
2. 1·v = v
3. a·(b·v) = (ab)·v
4. a·(u+v) = a·u + a·v
5. (a+b)·v = a·v + b·v

**Basis:** Linearly independent set that spans V.
**Dimension:** Number of vectors in any basis (dim V).

**Key Results:**
- Every vector space has a basis (requires AC for infinite dimensions)
- All bases have the same cardinality
- dim(V + W) = dim(V) + dim(W) - dim(V ∩ W)


## Category Theory (Advanced)

### Categories
A category C consists of:
- Objects: Ob(C)
- Morphisms: Hom(A,B) for A,B ∈ Ob(C)
- Composition: ∘: Hom(B,C) × Hom(A,B) → Hom(A,C)
- Identity: id_A ∈ Hom(A,A)

Axioms:
1. Associativity: h ∘ (g ∘ f) = (h ∘ g) ∘ f
2. Identity: f ∘ id_A = f = id_B ∘ f for f: A → B

**Examples:**
- **Set:** Objects = sets, Morphisms = functions
- **Grp:** Objects = groups, Morphisms = group homomorphisms
- **Vect_F:** Objects = vector spaces over F, Morphisms = linear maps
- **Top:** Objects = topological spaces, Morphisms = continuous maps

### Functors
A functor F: C → D maps:
- Objects: F(A) ∈ Ob(D) for A ∈ Ob(C)
- Morphisms: F(f): F(A) → F(B) for f: A → B

Preserving:
- F(g ∘ f) = F(g) ∘ F(f)
- F(id_A) = id_{F(A)}

**Examples:**
- Forgetful functor: Grp → Set (forgets group structure)
- Free functor: Set → Grp (free group on a set)
- Hom functor: Hom(A, -): C → Set

### Natural Transformations
A natural transformation η: F ⇒ G between functors F,G: C → D assigns to each A ∈ Ob(C) a morphism η_A: F(A) → G(A) such that for all f: A → B:
    η_B ∘ F(f) = G(f) ∘ η_A

This makes the following diagram commute:
```
    F(A) --F(f)--> F(B)
     | η_A           | η_B
     v               v
    G(A) --G(f)--> G(B)
```

### Universal Properties
- **Initial object:** I such that ∀A, ∃! f: I → A
- **Terminal object:** T such that ∀A, ∃! f: A → T
- **Product:** A × B with projections π₁, π₂
- **Coproduct:** A ⊔ B with injections ι₁, ι₂
- **Pullback / Pushout:** Universal constructions in diagrams

### Adjunctions
Functors F: C → D and G: D → C are adjoint (F ⊣ G) if:
Hom_D(F(A), B) ≅ Hom_C(A, G(B))  naturally in A,B

F is left adjoint to G; G is right adjoint to F.

**Examples:**
- Free ⊣ Forgetful (Set → Grp)
- Tensor ⊣ Hom (in module categories)
- Direct image ⊣ Inverse image (in sheaf theory)

### Limits & Colimits
- **Limit:** Universal cone over a diagram
- **Colimit:** Universal cocone under a diagram
- Products, equalizers, pullbacks are limits
- Coproducts, coequalizers, pushouts are colimits

**Theorem:** A category has all finite limits iff it has finite products and equalizers.


## Type Theory & Foundations

### ZFC (Zermelo-Fraenkel with Choice)
Standard foundation of mathematics.

**Axioms:**
1. Extensionality: Sets with same elements are equal
2. Empty Set: ∃∅
3. Pairing: {a,b} exists
4. Union: ∪A exists for any set A
5. Power Set: P(A) exists
6. Infinity: ∃ infinite set (ℕ)
7. Separation: {x ∈ A : P(x)} exists
8. Replacement: Image of a set under a function is a set
9. Regularity: No set contains itself (no infinite descending ∈-chains)
10. Choice: Every set of non-empty sets has a choice function

### Ordinal & Cardinal Numbers

**Ordinals:** Transitive sets well-ordered by ∈.
- 0 = ∅, 1 = {0}, 2 = {0,1}, ..., ω = {0,1,2,...}
- ω+1, ω+2, ..., ω·2, ..., ω², ..., ω^ω, ..., ε₀, ...

**Cardinals:** Initial ordinals (smallest ordinal of given cardinality).
- ℵ₀ = ω, ℵ₁, ℵ₂, ...
- ℵ_ω = sup{ℵₙ : n ∈ ℕ}

**Cardinal Arithmetic:**
- ℵ₀ + ℵ₀ = ℵ₀,  ℵ₀ · ℵ₀ = ℵ₀
- 2^ℵ₀ = 𝔠 (continuum)
- For infinite κ: κ + κ = κ, κ · κ = κ
- κ^λ for cardinals

### Gödel's Incompleteness Theorems

**First Incompleteness Theorem:**
Any consistent formal system F strong enough to encode arithmetic contains statements that are true but unprovable in F.

**Second Incompleteness Theorem:**
If F is consistent, F cannot prove its own consistency.

**Implications:**
- No complete axiomatization of arithmetic exists
- Truth and provability diverge
- Hilbert's program (prove consistency of math from finitary methods) is impossible

### Homotopy Type Theory (HoTT)
New foundation replacing sets with homotopy types.

**Key Ideas:**
- Types = spaces, terms = points
- Identity types = paths
- Univalence Axiom: (A = B) ≃ (A ≃ B)
  (Isomorphic types are equal)
- Higher inductive types
- Synthetic homotopy theory

**Applications:**
- Formal verification of mathematics
- Computer proof assistants (Coq, Lean, Agda)
- Homotopy theory without point-set topology


---
