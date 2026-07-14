# CHAPTER 5: NUMBER THEORY (ADVANCED)


## Analytic Number Theory

### The Prime Number Theorem

**Statement:**
π(x) ~ x/log(x) as x → ∞
where π(x) = number of primes ≤ x.

**Equivalent forms:**
- π(x) ~ li(x) = ∫₂^x dt/log(t)
- θ(x) = Σ_{p≤x} log p ~ x
- ψ(x) = Σ_{p^k≤x} log p ~ x
- pₙ ~ n log n (n-th prime)

**Proof methods:**
- Hadamard and de la Vallée Poussin (1896): using complex analysis of ζ(s)
- Erdős and Selberg (1949): elementary proof (no complex analysis)
- Newman's short proof (1980)

**Error term:**
π(x) = li(x) + O(x exp(-c√(log x)))
Equivalent to Riemann Hypothesis: π(x) = li(x) + O(√x log x)

### The Riemann Zeta Function

**Definition:**
ζ(s) = Σ_{n=1}^∞ n^{-s} = ∏_p (1 - p^{-s})^{-1}  for Re(s) > 1

**Analytic continuation:**
- Meromorphic on ℂ with simple pole at s = 1 (residue 1)
- Functional equation: ζ(s) = 2^s π^{s-1} sin(πs/2) Γ(1-s) ζ(1-s)
- Or: ξ(s) = ½s(s-1)π^{-s/2}Γ(s/2)ζ(s) satisfies ξ(s) = ξ(1-s)

**Zeros:**
- Trivial zeros: s = -2, -4, -6, ... (from functional equation)
- Non-trivial zeros: in critical strip 0 < Re(s) < 1
- **Riemann Hypothesis:** All non-trivial zeros have Re(s) = ½

**Explicit Formula:**
ψ(x) = x - Σ_ρ x^ρ/ρ - log(2π) - ½log(1-x^{-2})
where sum is over non-trivial zeros ρ of ζ(s).

**Consequences of RH:**
- Prime gaps: p_{n+1} - pₙ = O(√pₙ log pₙ)
- Mertens function: M(x) = O(x^{1/2+ε})
- Lindelöf hypothesis: ζ(½ + it) = O(t^ε)

### Dirichlet L-Functions

**Definition:**
For Dirichlet character χ mod q:
L(s,χ) = Σ_{n=1}^∞ χ(n)n^{-s} = ∏_p (1 - χ(p)p^{-s})^{-1}

**Properties:**
- Analytic continuation (entire for non-principal χ)
- Functional equation
- **Dirichlet's Theorem:** L(1,χ) ≠ 0 for non-principal χ
  ⇒ infinitely many primes in arithmetic progressions

**Generalized Riemann Hypothesis:**
All non-trivial zeros of L(s,χ) have Re(s) = ½.

### Modular Forms

**Definition:**
Holomorphic f: ℍ → ℂ satisfying:
1. f(γz) = (cz+d)^k f(z) for γ = (a b; c d) ∈ SL(2,ℤ)
2. f holomorphic at ∞ (Fourier expansion has no negative terms)

**Fourier Expansion:**
f(z) = Σ_{n=0}^∞ aₙ e^{2πinz} = Σ_{n=0}^∞ aₙ qⁿ  (q = e^{2πiz})

**Eisenstein Series:**
G_k(z) = Σ_{(m,n)≠(0,0)} (mz+n)^{-k} for even k ≥ 4
- Normalized: E_k(z) = G_k(z)/(2ζ(k))
- E₄ = 1 + 240Σ σ₃(n)qⁿ
- E₆ = 1 - 504Σ σ₅(n)qⁿ

**Discriminant Form:**
Δ(z) = (E₄³ - E₆²)/1728 = q ∏_{n=1}^∞ (1-qⁿ)²⁴ = Σ τ(n)qⁿ
- Ramanujan τ function
- τ(p^{k+1}) = τ(p)τ(p^k) - p^{11}τ(p^{k-1})
- |τ(p)| ≤ 2p^{11/2} (Deligne's proof of Ramanujan conjecture)

**Hecke Operators:**
Tₙ acting on modular forms.
- Eigenforms: simultaneous eigenvectors
- L-function of eigenform: L(f,s) = Σ aₙ n^{-s}
- Functional equation and analytic continuation

**Modularity Theorem (Wiles et al.):**
Every rational elliptic curve is modular.
- L-function of elliptic curve = L-function of modular form
- Implies Fermat's Last Theorem

### Sieve Methods

**Sieve of Eratosthenes-Legendre:**
π(x) - π(√x) + 1 = Σ_{d|P} μ(d)⌊x/d⌋
where P = product of primes ≤ √x.

**Brun's Sieve:**
Upper bound for twin primes:
π₂(x) = O(x(log log x)²/log²x)
⇒ Sum of reciprocals of twin primes converges (Brun's constant)

**Large Sieve:**
For set of integers avoiding many residue classes:
Σ_{q≤Q} Σ_{(a,q)=1} |S(a/q)|² ≤ (N + Q²) Σ |aₙ|²

**Bombieri-Vinogradov Theorem:**
Average form of ERH for Dirichlet L-functions:
Σ_{q≤Q} max_{y≤x} max_{(a,q)=1} |ψ(y;q,a) - y/φ(q)| = O(x/(log x)^A)
for Q = x^{1/2}/(log x)^B

### Additive Number Theory

**Goldbach's Conjecture:**
Every even n > 2 is sum of two primes.
- Verified up to very large numbers
- Chen's theorem: every sufficiently large even n is sum of prime and product of at most two primes (P₂)
- Vinogradov: every sufficiently large odd n is sum of three primes

**Waring's Problem:**
Every sufficiently large integer is sum of at most g(k) k-th powers.
- g(2) = 4 (Lagrange's four squares)
- g(3) = 9, g(4) = 19
- G(k): minimum s such that all sufficiently large n are sum of s k-th powers
- G(2) = 4, G(3) ≤ 7, G(4) = 16

**Partition Function:**
p(n) = number of ways to write n as sum of positive integers
- p(1)=1, p(2)=2, p(3)=3, p(4)=5, p(5)=7, ...
- Hardy-Ramanujan-Rademacher formula:
  p(n) = (1/π√2) Σ_{k=1}^∞ A_k(n) √k · d/dn [sinh(π/k √(2/3(n-1/24)))/√(n-1/24)]
- Asymptotic: p(n) ~ exp(π√(2n/3))/(4n√3)

**Circle Method (Hardy-Littlewood-Ramanujan):**
For additive problems, express counting function as integral over unit circle.
- Major arcs: near rational points with small denominator
- Minor arcs: estimate using bounds on exponential sums


## Algebraic Number Theory

### Algebraic Number Fields

**Number Field:**
Finite extension K of ℚ.
- [K:ℚ] = degree
- K = ℚ(α) for some algebraic α (primitive element theorem)

**Ring of Integers:**
O_K = {α ∈ K : α is root of monic polynomial in ℤ[x]}
- Dedekind domain (Noetherian, integrally closed, dimension 1)
- Not always UFD, but always has unique factorization of ideals

**Discriminant:**
For basis {α₁,...,αₙ} of K:
d_K = det(Tr_{K/ℚ}(αᵢαⱼ))
- Independent of basis up to square factor
- d_K determines ramification

### Ideal Theory

**Prime Ideal Factorization:**
For prime p ∈ ℤ:
(p) = P₁^{e₁} ... P_g^{e_g} in O_K
- eᵢ = ramification index
- fᵢ = [O_K/Pᵢ : ℤ/pℤ] = inertia degree
- Σ eᵢfᵢ = [K:ℚ]

**Ramification:**
- p ramifies if some eᵢ > 1
- p ramifies iff p | d_K
- Only finitely many ramified primes

**Class Group:**
Cl(K) = fractional ideals / principal ideals
- Finite abelian group (Minkowski bound)
- h_K = |Cl(K)| = class number
- h_K = 1 iff O_K is UFD

**Unit Group:**
O_K* = group of units in O_K
**Dirichlet's Unit Theorem:**
O_K* ≅ μ(K) × ℤ^{r₁+r₂-1}
where r₁ = number of real embeddings, r₂ = number of pairs of complex embeddings.

**Regulator:**
Volume of fundamental domain of lattice of units.
- Appears in class number formula

### Class Field Theory

**Hilbert Class Field:**
Maximal unramified abelian extension H of K.
- Gal(H/K) ≅ Cl(K)
- Every ideal of K becomes principal in H (principal ideal theorem)

**Artin Reciprocity:**
For abelian extension L/K:
Gal(L/K) ≅ I_K / (K* · N_{L/K}(I_L))
where I_K = idele group.

**Local Class Field Theory:**
For local field K (completion of number field):
- Maximal abelian extension ↔ K*
- Lubin-Tate theory: explicit construction using formal groups

### L-Functions & Zeta Functions

**Dedekind Zeta Function:**
ζ_K(s) = Σ_{I ideal} N(I)^{-s} = ∏_P (1 - N(P)^{-s})^{-1}
- Analytic continuation, functional equation
- Class number formula:
  lim_{s→1} (s-1)ζ_K(s) = (2^{r₁}(2π)^{r₂}h_K R_K)/(w_K √|d_K|)

**Artin L-Functions:**
For Galois representation ρ: Gal(L/K) → GL(V):
L(s,ρ) = ∏_P det(I - ρ(Frob_P)N(P)^{-s})^{-1}
- **Artin Conjecture:** L(s,ρ) is entire for non-trivial irreducible ρ
- Proved for monomial (induced from 1-dimensional) by Brauer induction

**Hecke L-Functions:**
For Grössencharakter (Hecke character) χ:
L(s,χ) = Σ χ(I)N(I)^{-s}
- Analytic continuation, functional equation
- Generalizes Dirichlet L-functions

### Elliptic Curves over Number Fields

**Mordell-Weil Theorem:**
E(K) is finitely generated abelian group.
E(K) ≅ E(K)_{tors} × ℤ^r
where r = rank.

**Torsion:**
- Mazur's theorem over ℚ: E(ℚ)_{tors} is one of 15 groups
- Merel's theorem: uniform bound on torsion for fixed degree

**Rank:**
- Average rank over ℚ is bounded (Bhargava-Shankar: ≤ 7/6)
- Birch and Swinnerton-Dyer conjecture relates rank to L-function

**BSD Conjecture:**
For elliptic curve E over ℚ:
ord_{s=1} L(E,s) = rank(E(ℚ))
And leading coefficient involves regulator, period, Tate-Shafarevich group, etc.
- Proved for rank 0 and 1 (Gross-Zagier, Kolyvagin)
- Tate-Shafarevich group Ш(E/ℚ) is conjecturally finite

**Isogenies:**
Rational maps between elliptic curves preserving group structure.
- Dual isogeny
- Tate module: T_ℓ(E) = lim E[ℓⁿ]
- Tate's isogeny theorem: E₁, E₂ isogenous iff T_ℓ(E₁) ≅ T_ℓ(E₂) as Galois modules

### Iwasawa Theory

**Iwasawa Algebra:**
Λ = ℤ_p[[Γ]] ≅ ℤ_p[[T]] where Γ ≅ ℤ_p

**Cyclotomic ℤ_p-extension:**
ℚ_∞ = ∪ ℚ(μ_{p^{n+1}}) for p odd
- Gal(ℚ_∞/ℚ) ≅ ℤ_p

**Iwasawa Main Conjecture:**
Characteristic ideal of X (Galois group of maximal unramified abelian p-extension) = ideal generated by p-adic L-function.
- Proved by Mazur-Wiles, Rubin
- Relates algebraic and analytic p-adic invariants


## Diophantine Geometry

### Heights

**Weil Height:**
For P = [x₀:...:xₙ] ∈ ℙⁿ(ℚ):
H(P) = max{|xᵢ|} where xᵢ are coprime integers

**Logarithmic Height:**
h(P) = log H(P)

**Properties:**
- h(P) ≥ 0
- h(σ(P)) = h(P) for σ ∈ Gal(ℚ̄/ℚ)
- h(P^d) = d·h(P) for d-th power map
- Northcott's theorem: finite number of points with h(P) ≤ B and [ℚ(P):ℚ] ≤ d

**Canonical Height on Elliptic Curves:**
ĥ(P) = lim_{n→∞} 4^{-n} h(2ⁿP)
- Quadratic form: ĥ(mP) = m²ĥ(P)
- ĥ(P) = 0 iff P is torsion

### Rational Points on Varieties

**Mordell Conjecture (Faltings' Theorem):**
For curve C of genus g ≥ 2 over number field K:
C(K) is finite.

**Bombieri-Lang Conjecture:**
For variety V of general type over number field:
V(K) is not Zariski dense.

**Vojta's Conjecture:**
Height inequality generalizing Roth's theorem:
h_K(D,P) ≤ d_K(P) + εh_H(P) + O(1)
for appropriate divisors.

### Arithmetic Geometry

**Arakelov Theory:**
Intersection theory on arithmetic surfaces.
- Includes archimedean places ("infinite primes")
- Arithmetic intersection numbers
- Arithmetic Riemann-Roch

**Arakelov Height:**
For line bundle with metric on arithmetic variety.

**Gross-Zagier Formula:**
For elliptic curve E over ℚ and Heegner point P_K:
L'(E/K,1) = ĥ(P_K) · (period terms)

### p-adic Analysis

**p-adic Numbers:**
ℚ_p = completion of ℚ with respect to |·|_p
- |p|_p = p^{-1}
- Every element: Σ_{n≥N} aₙ pⁿ with aₙ ∈ {0,...,p-1}
- ℚ_p is locally compact, totally disconnected

**p-adic Integers:**
ℤ_p = {x ∈ ℚ_p : |x|_p ≤ 1}
- Compact, open subring
- ℤ_p/pℤ_p ≅ ℤ/pℤ = 𝔽_p

**Hensel's Lemma:**
If f ∈ ℤ_p[x] and f(a) ≡ 0 (mod p) with f'(a) ≢ 0 (mod p):
∃! α ∈ ℤ_p: f(α) = 0 and α ≡ a (mod p)

**p-adic L-Functions:**
- Kubota-Leopoldt p-adic L-functions
- Iwasawa construction via measures on ℤ_p*
- p-adic regulator, p-adic class number formula

**p-adic Integration:**
- Volkenborn integral
- p-adic measure theory
- p-adic Fourier transform


---
