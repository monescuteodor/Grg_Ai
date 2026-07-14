# CHAPTER 9: CATEGORY THEORY & TOPOS THEORY


## Higher Category Theory

### 2-Categories & Bicategories

**2-Category:**
A category enriched over Cat (categories).
- Objects: 0-cells
- Morphisms (1-morphisms): 1-cells between 0-cells
- 2-morphisms: 2-cells between 1-morphisms

**Vertical & Horizontal Composition:**
For 2-morphisms α: f ⇒ g, β: g ⇒ h:
- Vertical: β ∘ᵥ α: f ⇒ h
- For γ: f' ⇒ g' where f'∘f, g'∘g defined:
  Horizontal: γ ∘ₕ α: f'∘f ⇒ g'∘g

**Exchange Law:**
(β' ∘ᵥ β) ∘ₕ (α' ∘ᵥ α) = (β' ∘ₕ α') ∘ᵥ (β ∘ₕ α)

**Bicategory:**
Weak 2-category where associativity and unit laws hold only up to coherent isomorphism.
- Example: Bimod (rings, bimodules, bimodule homomorphisms)
- Example: Span(C) for category C with pullbacks

**String Diagrams:**
Graphical calculus for 2-categories.
- Objects = regions
- 1-morphisms = strings
- 2-morphisms = vertices
- Composition = vertical/horizontal juxtaposition

### ∞-Categories

**Simplicial Sets:**
Functors Δ^op → Set where Δ = category of finite ordinals.
- n-simplices: Δ[n]
- Face maps: dᵢ
- Degeneracy maps: sᵢ

**Kan Complexes:**
Simplicial set where all horns have fillers.
- Models spaces up to homotopy
- Fundamental ∞-groupoid of a space

**Quasi-Categories (∞-Categories):**
Simplicial set where all inner horns have fillers.
- Objects = 0-simplices
- Morphisms = 1-simplices
- Higher morphisms = higher simplices
- Composition defined up to homotopy

**Homotopy Category:**
ho(C) for ∞-category C: objects same, morphisms = homotopy classes of 1-morphisms.

**Limits & Colimits in ∞-Categories:**
Defined via homotopy limits/colimits.
- Homotopy pullback: replace pullback by fibrant replacement
- Homotopy pushout: replace pushout by cofibrant replacement

**Stable ∞-Categories:**
∞-category with zero object, finite limits/colimits, and where square is pullback iff pushout.
- Example: Spectra (stable homotopy theory)
- Homotopy category is triangulated

### Higher Topos Theory

**Definition:**
∞-category that behaves like ∞-category of sheaves of spaces.
- Has finite limits and colimits
- Has universal colimits
- Has object classifiers

**Examples:**
- ∞-category of spaces
- ∞-category of sheaves on site
- ∞-category of condensed sets

**Shape of Topos:**
Pro-∞-groupoid associated to topos.
- Shape of Sh(X) = Π_∞(X) for nice spaces
- Shape of étale topos = étale homotopy type

**Cohesive Topos:**
Topos with adjoint quadruple:
Disc ⊣ Γ ⊣ CoDisc ⊣ ♭
- Captures notions of cohesion (continuity, smoothness)
- Models differential geometry synthetically

**Modalities in Cohesive Topos:**
- ♭ (flat): discrete types
- ♯ (sharp): codiscrete types
- ʃ (shape): fundamental ∞-groupoid
- ℑ (im): infinitesimal shape


## Topos Theory

### Elementary Topoi

**Definition (Lawvere-Tierney):**
Category E such that:
1. E has all finite limits
2. E is cartesian closed
3. E has a subobject classifier Ω

**Subobject Classifier:**
Object Ω with morphism true: 1 → Ω such that every monomorphism is pullback of true along unique morphism.
- In Set: Ω = {0,1}, true = 1
- In sheaf topos: Ω = sieve classifier

**Power Object:**
P(A) = Ω^A, representing subobjects of A.

**Internal Logic:**
Every topos has intuitionistic higher-order logic.
- Connectives: ∧, ∨, ⇒, ¬, ∀, ∃
- No excluded middle in general
- Kripke-Joyal semantics

**Examples of Topoi:**
1. **Set:** category of sets
2. **Set^C^op:** presheaf category
3. **Sh(C,J):** sheaves on site (C,J)
4. **Eff:** effective topos (realizability)
5. **Troelstra's topos:** extensional realizability

### Sheaves & Sites

**Grothendieck Topology:**
Assignment J to each object U of collection of sieves satisfying:
1. Maximal sieve is covering
2. Stability under pullback
3. Local character (transitivity)

**Site:**
Category C with Grothendieck topology J.

**Sheaf:**
Functor F: C^op → Set satisfying gluing for covering sieves.
- Separation: local equality implies global equality
- Gluing: compatible local sections glue

**Sheafification:**
Left adjoint to inclusion Sh(C,J) ↪ Psh(C).
- a(F)(U) = colim_{R ∈ J(U)} Hom(R, F)

**Geometric Morphisms:**
f: F → E consists of adjunction f* ⊣ f_* where f* preserves finite limits.
- f*: E → F (inverse image)
- f_*: F → E (direct image)
- Essential if f* has left adjoint f_!

**Points of Topos:**
Geometric morphism p: Set → E.
- In sheaf topos: actual points of underlying space
- Topos may have no points (but still non-trivial)

### Cohomology in Topoi

**Abelian Group Objects:**
Group objects in topos with abelian structure.

**Cohomology:**
H^n(E, A) = Ext^n_E(1, A) for abelian group object A.
- In Sh(X): H^n(X, A) = sheaf cohomology
- In Eff: realizability cohomology

**Čech Cohomology:**
For covering U = {Uᵢ}:
Ĥ^n(U, F) = H^n(C*(U, F))
- Agrees with sheaf cohomology under paracompactness

**Derived Categories in Topoi:**
D(E) = derived category of abelian sheaves.
- Standard and perverse t-structures
- Six-functor formalism (Grothendieck)

### Synthetic Differential Geometry

**Kock-Lawvere Axiom:**
In smooth topos, ring of smooth functions R satisfies:
For any f: D → R where D = {x ∈ R : x² = 0}:
∃! a,b ∈ R: f(d) = a + bd for all d ∈ D

**Infinitesimals:**
- Nilpotent: x^n = 0 for some n
- D = {d : d² = 0} (first-order infinitesimals)
- Dₙ = {d : d^{n+1} = 0}
- D_∞ = ∪ Dₙ (all nilpotents)

**Tangent Bundle:**
TM = M^D (exponential object)
- Tangent vectors: maps D → M
- Vector fields: maps M → M^D

**Differential Forms:**
- 1-forms: maps from infinitesimal paths
- k-forms: alternating multilinear maps on D^n
- Exterior derivative: defined via infinitesimal Stokes

**Integration:**
∫_a^b f(x) dx defined via microlinearity.
- Fundamental theorem holds
- No need for limits or ε-δ

**Models:**
- Cahiers topos: sheaves on cartesian closed category of smooth manifolds with infinitesimal thickenings
- Dubuc's topos: C^∞-rings
- Formal smooth sets


## Categorical Logic

### Type Theories

**Simply Typed Lambda Calculus:**
Types: A, B ::= base | A → B | A × B | 1
Terms: variables, lambda abstraction, application, pairing, projections

**Curry-Howard Correspondence:**
| Logic | Types | Programs |
|-------|-------|----------|
| Proposition | Type | Term |
| Proof | Term | Program |
| Implication | Function type | Function |
| Conjunction | Product type | Pair |
| Disjunction | Sum type | Either |
| Falsity | Empty type | Absurd |
| Universal quantifier | Dependent product | Dependent function |
| Existential quantifier | Dependent sum | Dependent pair |

**Dependent Type Theory:**
- Π-types: (x:A) → B(x)
- Σ-types: (x:A) × B(x)
- Identity types: Id_A(a,b) or a =_A b

**Martin-Löf Type Theory:**
- Intensional: identity proofs are data
- Extensional: identity types are propositions
- Univalence in HoTT requires intensional

**Homotopy Type Theory (HoTT):**
- Types = spaces
- Terms = points
- Identity types = paths
- Path induction = transport
- Univalence: (A ≃ B) ≃ (A = B)

### Categorical Semantics

**Cartesian Closed Categories (CCC):**
Models of simply typed lambda calculus.
- Terminal object, products, exponentials
- Evaluation: ev: B^A × A → B
- Currying: f: C × A → B ↦ f̃: C → B^A

**Locally Cartesian Closed Categories (LCCC):**
Models of dependent type theory.
- Slice categories C/A are cartesian closed
- Dependent product = right adjoint to pullback
- Dependent sum = left adjoint to pullback

**Interpretation:**
- Context Γ ⊢ type A ↦ object [A] in slice C/[Γ]
- Term Γ ⊢ a:A ↦ section [a]: [Γ] → [A]
- Substitution = pullback

**Internal Languages:**
Every CCC is equivalent to category of contexts and terms of some lambda theory.

### Proof Theory

**Natural Deduction:**
Introduction and elimination rules for each connective.
- ∧I, ∧E₁, ∧E₂
- ∨I₁, ∨I₂, ∨E
- ⇒I, ⇒E (modus ponens)
- ∀I, ∀E
- ∃I, ∃E

**Sequent Calculus:**
Γ ⊢ Δ where Γ, Δ are multisets of formulas.
- Structural rules: weakening, contraction, exchange
- Logical rules: left and right rules
- Cut rule: Γ ⊢ A, Δ and Γ', A ⊢ Δ' ⇒ Γ, Γ' ⊢ Δ, Δ'

**Cut Elimination (Gentzen):**
Any proof can be transformed to cut-free proof.
- Subformula property: only subformulas appear
- Consistency of arithmetic (PA)
- Complexity: non-elementary (Statman)

**Linear Logic:**
- Multiplicative: ⊗, ⅋, 1, ⊥
- Additive: ⊕, &, 0, ⊤
- Exponential: !, ?
- No weakening or contraction without exponentials
- Resource-sensitive computation

**Proof Nets:**
Graphical representation of linear logic proofs.
- Correctness criterion (Danos-Regnier)
- Eliminate bureaucracy of sequent calculus

### Categorical Proof Theory

**Proofs as Morphisms:**
In cartesian closed category, proofs of A ⊢ B are morphisms A → B.
- Identity proof = identity morphism
- Cut = composition
- Contraction = diagonal
- Weakening = projection to terminal

**Coherence Theorems:**
Mac Lane's coherence: any two canonical maps between same source/target in free monoidal category are equal.

**Proof Complexity:**
- Frege systems: propositional proof systems
- Polynomial simulation
- Lower bounds for resolution, cutting planes
- P vs NP connection: NP = coNP iff propositional proof systems are polynomially bounded


---
