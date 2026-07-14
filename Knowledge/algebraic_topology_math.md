# CHAPTER 10: ALGEBRAIC TOPOLOGY & HOMOTOPY THEORY


## Classical Homotopy Theory

### Homotopy Groups

**Fundamental Group:**
π₁(X,x₀) = homotopy classes of loops based at x₀
- Group operation: concatenation of loops
- Simply connected: π₁ = 0
- π₁(S¹) = ℤ
- π₁(Sⁿ) = 0 for n ≥ 2
- π₁(Tⁿ) = ℤⁿ
- Van Kampen theorem: π₁(X∪Y) = π₁(X) *_{π₁(X∩Y)} π₁(Y)

**Higher Homotopy Groups:**
πₙ(X,x₀) = [(Sⁿ,*), (X,x₀)] for n ≥ 2
- Abelian groups for n ≥ 2
- πₙ(Sⁿ) = ℤ
- π₃(S²) = ℤ (Hopf fibration)
- π₄(S³) = ℤ/2ℤ
- π_{n+1}(Sⁿ) = ℤ/2ℤ for n ≥ 3
- π_{n+2}(Sⁿ) = ℤ/2ℤ for n ≥ 2

**Whitehead Products:**
[α,β] ∈ π_{m+n-1}(X) for α ∈ πₘ(X), β ∈ πₙ(X)
- Graded Lie algebra structure
- [α,β] = (-1)^{mn}[β,α]
- Jacobi identity

**EHP Sequence:**
Exact sequence relating homotopy groups of spheres:
... → π_{k+n}(Sⁿ) → π_{k+n+1}(S^{n+1}) → π_{k+n+1}(S^{2n+1}) → π_{k+n-1}(Sⁿ) → ...
- E = suspension, H = Hopf invariant, P = Whitehead product

**Freudenthal Suspension Theorem:**
For n-connected space X, suspension map:
πₖ(X) → π_{k+1}(ΣX) is isomorphism for k ≤ 2n+1, surjection for k = 2n+2.

**Stable Homotopy Groups:**
πₖ^S = colimₙ π_{k+n}(Sⁿ)
- Finite abelian groups for k > 0
- π₀^S = ℤ
- π₁^S = ℤ/2ℤ
- π₂^S = ℤ/2ℤ
- π₃^S = ℤ/24ℤ

### Fibrations & Cofibrations

**Fibration:**
p: E → B with homotopy lifting property.
- Fibre F = p⁻¹(b₀)
- Long exact sequence of homotopy groups
- Examples: covering spaces, Hopf fibration S³ → S², path space fibration

**Cofibration:**
i: A → X with homotopy extension property.
- Cofibre C = X/A
- Long exact sequence of cohomology
- Examples: subcomplex inclusion, mapping cylinder

**Serre Fibration:**
Weak fibration: homotopy lifting for CW complexes.
- All fibre bundles over paracompact base
- Spectral sequence for computing homology

**Path Space Fibration:**
PX → X where PX = {γ: [0,1] → X : γ(0) = x₀}
- Fibre: loop space ΩX
- ΩX → PX → X
- πₙ(ΩX) = π_{n+1}(X)

**Mapping Spaces:**
Map(X,Y) = space of continuous maps
- Path components: [X,Y] = π₀(Map(X,Y))
- Loop space: ΩX = Map(S¹, X)
- Suspension: ΣX = S¹ ∧ X
- Adjunction: [ΣX, Y] ≅ [X, ΩY]

### Spectral Sequences

**Definition:**
Sequence of pages Eʳ with differentials dʳ: Eʳ → Eʳ of degree r.
E^{r+1} = H(Eʳ, dʳ)

**Convergence:**
Eʳ ⇒ H*(C) means E^∞ is associated graded of filtration on H*(C).

**Leray-Serre Spectral Sequence:**
For fibration F → E → B:
E²_{p,q} = H_p(B; H_q(F)) ⇒ H_{p+q}(E)
- For cohomology: E₂^{p,q} = H^p(B; H^q(F)) ⇒ H^{p+q}(E)

**Examples:**
- Compute H*(CP^∞) from S¹ → S^{2n+1} → CPⁿ
- Compute H*(ΩSⁿ) from path space fibration
- Compute H*(BU(n)) from flag manifold fibration

**Atiyah-Hirzebruch Spectral Sequence:**
For generalized cohomology theory h*:
E₂^{p,q} = H^p(X; h^q(pt)) ⇒ h^{p+q}(X)

**Adams Spectral Sequence:**
E₂^{s,t} = Ext^{s,t}_{A_p}(H*(X), ℤ/p) ⇒ π_{t-s}(X) ⊗ ℤ_p
- Computes stable homotopy groups
- Based on Steenrod algebra A_p

**Bockstein Spectral Sequence:**
From short exact sequence 0 → ℤ → ℤ → ℤ/p → 0.
- Computes integral cohomology from mod p cohomology

### Obstruction Theory

**Primary Obstruction:**
For lifting problem:
... → K(π,n) → E → B
Obstruction in H^{n+1}(X; π).

**Postnikov Tower:**
... → Xₙ → X_{n-1} → ... → X₁ → X₀ = *
where Xₙ has πₖ(Xₙ) = πₖ(X) for k ≤ n, 0 for k > n.
- Killing higher homotopy groups
- X = lim Xₙ

**Whitehead Tower:**
... → X⟨n⟩ → X⟨n-1⟩ → ... → X⟨1⟩ → X⟨0⟩ = X
where X⟨n⟩ is n-connected and X⟨n⟩ → X induces isomorphism on πₖ for k > n.
- Killing lower homotopy groups
- X⟨1⟩ = universal cover

**k-invariants:**
Obstructions in H^{n+2}(X_{n-1}; π_{n+1}(X)) for Postnikov tower.
- Determine homotopy type of space

## Generalized Cohomology Theories

### Axioms (Eilenberg-Steenrod)

**Generalized Cohomology Theory:**
Sequence of functors h^n: CW² → Ab with:
1. Homotopy invariance
2. Excision
3. Long exact sequence of pair
4. Additivity for disjoint unions

**Brown Representability:**
Every generalized cohomology theory is represented by a spectrum.
h^n(X) = [X, Eₙ] for spectrum E = {Eₙ}

### K-Theory

**Topological K-Theory:**
For compact space X:
- K⁰(X): Grothendieck group of vector bundles
- K⁻ⁿ(X) = K⁰(ΣⁿX)
- Bott periodicity: K⁻ⁿ(X) ≅ K⁻ⁿ⁻²(X)

**Bott Periodicity:**
- K⁰(S²) = ℤ ⊕ ℤ
- K⁰(S^{2n}) = ℤ ⊕ ℤ
- K⁰(S^{2n+1}) = ℤ
- K⁰(X × S²) ≅ K⁰(X) ⊕ K⁰(X)

**Chern Character:**
ch: K⁰(X) → H^{even}(X; ℚ)
- Ring homomorphism
- Isomorphism over ℚ for finite CW complexes
- ch(E ⊕ F) = ch(E) + ch(F)
- ch(E ⊗ F) = ch(E) ∪ ch(F)

**Atiyah-Singer Index Theorem:**
For elliptic operator D on compact manifold:
index(D) = ∫_M ch(σ(D)) ∧ td(TM)
- Analytical index = topological index
- Generalizes: Riemann-Roch, Chern-Gauss-Bonnet, Hirzebruch signature

**K-Theory of C*-Algebras:**
K₀(A) = Grothendieck group of projections in matrix algebras over A
K₁(A) = GL(A)/GL(A)₀
- Bott periodicity: Kₙ(A) ≅ K_{n+2}(A)
- Six-term exact sequence

### Cobordism Theories

**Thom Spectra:**
MO, MSO, MSU, MSpin, etc.
- MO = Thom spectrum for orthogonal group
- π_*(MO) = cobordism ring of unoriented manifolds

**Cobordism Ring:**
Ω_*^O = π_*(MO)
- Ω₀^O = ℤ/2ℤ
- Ω₁^O = 0
- Ω₂^O = ℤ/2ℤ
- Ω₃^O = 0
- Ω₄^O = ℤ/2ℤ ⊕ ℤ/2ℤ

**Thom's Theorem:**
Ω_*^O ≅ ℤ/2ℤ[x₂, x₄, x₅, x₆, x₈, ...] with generators in degrees 2,4,5,6,8,...

**Complex Cobordism:**
MU = Thom spectrum for unitary group
- π_*(MU) = ℤ[x₂, x₄, x₆, ...] polynomial ring
- Universal formal group law

### Stable Homotopy Theory

**Spectra:**
Sequence of spaces Eₙ with structure maps ΣEₙ → E_{n+1} (or Eₙ → ΩE_{n+1}).
- Suspension spectrum: Σ^∞X
- Eilenberg-MacLane spectrum: H(G,n)
- K-theory spectrum: K
- Cobordism spectra: MO, MSO, MU

**Smash Product:**
E ∧ F for spectra.
- Symmetric monoidal structure on stable homotopy category
- Homotopy category of spectra = SHC

**Spanier-Whitehead Duality:**
For finite spectrum X, ∃ DX such that:
X ∧ DX ≃ S⁰ (in stable homotopy category)
- Alexander duality: D(X) ≃ S⁰/X for X ⊂ Sⁿ
- Atiyah duality for manifolds

**Adams Spectral Sequence (revisited):**
E₂^{s,t} = Ext^{s,t}_{A}(H*(X), H*(Y)) ⇒ [X,Y]_{t-s}^∧
- A = Steenrod algebra at prime p
- Computes stable homotopy classes of maps

**Chromatic Homotopy Theory:**
- Morava K-theories K(n)
- Morava E-theories Eₙ
- Chromatic filtration of stable homotopy category
- Telescope conjecture (open)
- Nilpotence theorem (Devinatz-Hopkins-Smith)

### Equivariant & Motivic Homotopy Theory

**Equivariant Homotopy Theory:**
Spaces with G-action for compact Lie group G.
- Fixed points X^H for H ≤ G
- Orbit category O_G
- Bredon cohomology
- RO(G)-graded theories

**Motivic Homotopy Theory:**
Homotopy theory of schemes over base field.
- A¹-homotopy equivalences
- Motivic spheres: S^{p,q} = (S¹)^{∧p} ∧ (𝔾ₘ)^{∧q}
- Stable motivic homotopy category SH(k)
- Motivic cohomology: H^{p,q}(X, ℤ)
- Algebraic K-theory: represented by motivic spectrum

**Voevodsky's Motives:**
- Triangulated category of motives DM(k)
- Chow motives (pure motives)
- Mixed motives
- Motivic cohomology = Ext in category of motives


---
