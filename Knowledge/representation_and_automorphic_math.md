# CHAPTER 13: REPRESENTATION THEORY & AUTOMORPHIC FORMS


## Representation Theory of Finite Groups

### Character Theory

**Definitions:**
- Representation: ρ: G → GL(V)
- Character: χ_ρ(g) = tr(ρ(g))
- Class function: constant on conjugacy classes

**Orthogonality Relations:**
1. ⟨χᵢ, χⱼ⟩ = (1/|G|) Σ_g χᵢ(g) χ̄ⱼ(g) = δᵢⱼ
2. Σᵢ χᵢ(g) χ̄ᵢ(h) = |C_G(g)| if g~h, 0 otherwise

**Consequences:**
- Number of irreducible representations = number of conjugacy classes
- Σ (dim Vᵢ)² = |G|
- dim Vᵢ divides |G|
- Character table determines group up to isomorphism? (No: Brauer pairs)

**Burnside's Theorem:**
Every group of order p^a q^b is solvable.
- Proof uses character theory

**Frobenius Reciprocity:**
For H ≤ G, V representation of G, W of H:
Hom_G(V, Ind_H^G(W)) ≅ Hom_H(Res_H^G(V), W)

**Mackey's Irreducibility Criterion:**
Ind_H^G(W) is irreducible iff:
1. W is irreducible
2. For all g ∉ H, Res_{H∩gHg⁻¹}^H(W) and Res_{H∩gHg⁻¹}^{gHg⁻¹}(gW) have no common irreducible constituents

### Modular Representation Theory

**Setup:**
Characteristic p dividing |G|.
- Simple modules over algebraically closed field of char p
- Blocks: decomposition of group algebra
- Defect groups: p-subgroups associated to blocks

**Brauer Characters:**
For p-regular elements (order prime to p).
- Lift eigenvalues to characteristic 0
- Brauer character table

**Cartan Matrix:**
C = D^T D where D is decomposition matrix.
- C is symmetric, positive definite
- det(C) = p^d for some d

**Green Correspondence:**
For block with defect group D:
Bijection between indecomposable modules with vertex D and modules of normalizer N_G(D).

**Broué's Abelian Defect Group Conjecture:**
For block with abelian defect group D:
Derived category of block equivalent to derived category of Brauer correspondent.
- Proved for many cases
- Implies Alperin weight conjecture

### Representation Theory of Lie Groups

**Compact Lie Groups:**
Finite-dimensional representations are completely reducible.
- Peter-Weyl theorem: L²(G) = ⊕_λ V_λ ⊗ V_λ*
- Characters form orthonormal basis of class functions

**Highest Weight Theory:**
For semisimple Lie group G with maximal torus T:
- Irreducible representations classified by dominant integral weights
- Highest weight vector: annihilated by all positive root vectors
- Weight spaces: decomposition under T-action

**Weyl Character Formula:**
For irreducible V_λ with highest weight λ:
char(V_λ) = Σ_{w∈W} ε(w) e^{w(λ+ρ)} / Σ_{w∈W} ε(w) e^{w(ρ)}
where W = Weyl group, ρ = half-sum of positive roots.

**Weyl Dimension Formula:**
dim(V_λ) = ∏_{α>0} ⟨λ+ρ, α⟩ / ⟨ρ, α⟩

**Borel-Weil-Bott Theorem:**
Irreducible representations realized as cohomology of line bundles on flag variety.
- H^i(G/B, L_λ) = 0 or V_{w·λ} for unique w

### Automorphic Forms

**Classical Modular Forms:**
Holomorphic f: ℍ → ℂ satisfying f(γz) = (cz+d)^k f(z) for γ ∈ SL(2,ℤ).
- Fourier expansion: f(z) = Σ_{n=0}^∞ aₙ qⁿ
- Eisenstein series, cusp forms
- Hecke operators

**Maass Forms:**
Eigenfunctions of Laplacian on modular surface.
- Δf = λf where Δ = y²(∂²/∂x² + ∂²/∂y²)
- Real-analytic, not holomorphic
- Connection to quantum chaos

**Automorphic Representations:**
For reductive group G over number field F:
- Adelic formulation: G(𝔸_F)
- Automorphic form: function on G(F)\G(𝔸_F)
- Cusp form: vanishing of constant terms

**Langlands Program:**
1. **Local Langlands:** Correspondence between representations of G(F_v) and homomorphisms from Weil-Deligne group to ^L G.
2. **Global Langlands:** Correspondence between automorphic representations and Galois representations.
3. **Functoriality:** Transfer of automorphic representations between groups.

**Key Conjectures:**
- Ramanujan conjecture (proved by Deligne)
- Sato-Tate conjecture (proved by Clozel-Harris-Taylor, et al.)
- Langlands reciprocity for GL(n)
- Functoriality principle

### L-Functions

**Artin L-Functions:**
For Galois representation ρ: Gal(L/K) → GL(V):
L(s,ρ) = ∏_P det(I - ρ(Frob_P)N(P)^{-s})^{-1}
- **Artin Conjecture:** L(s,ρ) is entire for non-trivial irreducible ρ
- Proved for monomial (Brauer)
- Open in general

**Automorphic L-Functions:**
For automorphic representation π of GL(n):
L(s,π) = ∏_v L(s,π_v)
- Analytic continuation, functional equation
- Langlands: all "nice" L-functions are automorphic

**Hasse-Weil L-Functions:**
For variety X over number field:
L(s,X) from étale cohomology
- BSD conjecture for elliptic curves
- Tate conjecture for surfaces
- Swinnerton-Dyer conjecture for abelian varieties

**Special Values:**
- ζ(2) = π²/6, ζ(4) = π⁴/90
- L(1,χ) = πh/w√|D| for quadratic χ
- Birch-Swinnerton-Dyer: L'(E,1) related to rank and regulator
- Deligne's conjecture on critical values
- Beilinson's conjectures on higher K-theory

### Shimura Varieties

**Definition:**
Moduli spaces of Hodge structures with additional structure.
- Parameterized by symmetric spaces G(ℝ)/K
- Have canonical models over number fields

**Examples:**
- Modular curves: SL(2,ℤ)\ℍ
- Hilbert modular varieties
- Siegel modular varieties
- Picard modular varieties

**Reciprocity Laws:**
- Complex multiplication: Shimura-Taniyama-Weil theory
- Points with CM correspond to abelian extensions
- Kronecker's Jugendtraum: explicit class field theory via special values

**André-Oort Conjecture:**
Special subvarieties of Shimura varieties are exactly those containing a dense set of special points.
- Proved by Klingler-Ullmo-Yafaev (under GRH)
- Unconditional for Ag (moduli of abelian varieties)

### Theta Correspondence

**Howe Duality:**
For reductive dual pair (G,H) in symplectic group:
- Oscillator representation
- Theta correspondence: bijection between representations of G and H

**Examples:**
- (GL(m), GL(n)) in GL(mn)
- (O(n), Sp(2m))
- (U(n), U(m))

**Applications:**
- Construction of automorphic forms
- Lifting problems
- Local Langlands correspondence


---
