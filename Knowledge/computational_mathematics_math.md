# CHAPTER 15: ALGORITHMIC & COMPUTATIONAL MATHEMATICS


## Computational Algebra

### Computer Algebra Systems

**Symbolic Computation:**
Exact arithmetic with algebraic expressions.
- Polynomial arithmetic: addition, multiplication, GCD, factorization
- Rational function manipulation
- Symbolic integration (Risch algorithm)
- Symbolic summation (Gosper, Zeilberger)

**Polynomial Factorization:**
- Berlekamp algorithm (finite fields)
- Cantor-Zassenhaus algorithm
- Hensel lifting for ℤ[x]
- LLL-based factorization (Lenstra-Lenstra-Lovász)

**Gröbner Bases:**
For ideal I ⊆ k[x₁,...,xₙ]:
- Monomial ordering: lex, grlex, grevlex
- S-polynomial: S(f,g) = (LCM(LT(f),LT(g))/LT(f))f - (LCM(LT(f),LT(g))/LT(g))g
- Buchberger's algorithm: compute Gröbner basis
- Elimination: compute elimination ideals
- Applications: solving polynomial systems, implicitization, integer programming

**F4/F5 Algorithms:**
Matrix-based Gröbner basis computation.
- F4: linear algebra approach
- F5: signature-based, avoids useless reductions
- Complexity: doubly exponential in worst case

**Triangular Decomposition:**
- Wu's method (characteristic sets)
- Regular chains
- Lazard's method
- Applications: geometry theorem proving

### Computational Number Theory

**Primality Testing:**
- Trial division: O(√n)
- Miller-Rabin: probabilistic, O(log³n)
- AKS (Agrawal-Kayal-Saxena): deterministic, O(log^{7.5}n)
- Elliptic curve primality proving (ECPP)

**Integer Factorization:**
- Trial division
- Pollard's rho: O(n^{1/4})
- Pollard's p-1: finds factors where p-1 is smooth
- Elliptic curve method (ECM): subexponential
- Quadratic sieve: L_n[1/2, 1]
- Number field sieve (NFS): L_n[1/3, c] — best known

**Discrete Logarithm:**
- Baby-step giant-step: O(√p)
- Pollard's rho for DLP
- Index calculus: subexponential
- Number field sieve for DLP
- Quantum: Shor's algorithm (polynomial time)

**Lattice Algorithms:**
- LLL algorithm: polynomial-time lattice reduction
- BKZ (Block Korkine-Zolotarev)
- SVP (Shortest Vector Problem): NP-hard
- CVP (Closest Vector Problem): NP-hard
- Applications: cryptanalysis, coding theory, integer programming

### Computational Algebraic Geometry

**Resultants:**
- Sylvester resultant for two polynomials
- Macaulay resultant for multivariate systems
- Dixon resultant
- Applications: solving polynomial systems

**Homotopy Continuation:**
- Track solutions from known system to target system
- Numerical algebraic geometry
- Bertini, PHCpack software
- Witness sets, numerical irreducible decomposition

**Tropical Geometry (Computational):**
- Tropical varieties as polyhedral complexes
- Computing tropical bases
- Applications: implicitization, mixed volume

**Toric Geometry & Combinatorics:**
- Newton polytopes
- Mixed volume via Bernstein's theorem
- Counting solutions to polynomial systems

### Computational Topology

**Persistent Homology:**
- Filtration: nested sequence of simplicial complexes
- Persistence diagram: birth-death pairs
- Stability: bottleneck distance bounded by Hausdorff distance
- Algorithms: reduction of boundary matrix O(n³)
- Clear/collect optimizations

**Mapper Algorithm:**
- Topological data analysis tool
- Cover data with overlapping intervals
- Cluster within each interval
- Build nerve of clustering

**Reeb Graphs:**
- Quotient space by level sets of function
- Simplified representation of shape
- Applications: shape analysis, visualization

**Discrete Morse Theory:**
- Forman: combinatorial version
- Morse complexes from simplicial complexes
- Homology computation via Morse complex

### Symbolic Integration

**Risch Algorithm:**
Decision procedure for elementary integrals.
- Hermite reduction: rational part
- Rothstein-Trager: logarithmic part
- Risch differential equation
- Liouville's theorem: structure of elementary integrals

**Differential Algebra:**
- Differential fields
- Differential ideals
- Characteristic sets (Rosenfeld-Gröbner)
- Kolchin's work on differential algebraic groups

**Creative Telescoping:**
- Zeilberger's algorithm for hypergeometric sums
- Wilf-Zeilberger method
- Chyzak's algorithm for multiple sums/integrals
- Applications: combinatorial identities, Feynman integrals

### Computer-Assisted Proofs

**Formal Verification:**
- Coq, Lean, Isabelle/HOL, Agda
- Type theory as foundation
- Proof checking vs proof search

**Four Color Theorem:**
- Appel-Haken (1976): first major computer-assisted proof
- Robertson-Sanders-Seymour-Thomas (1997): simplified
- Gonthier (2008): fully formalized in Coq

**Kepler Conjecture:**
- Hales (1998): densest sphere packing in 3D
- Flyspeck project: fully formalized in HOL Light

**Odd Order Theorem:**
- Feit-Thompson: every finite group of odd order is solvable
- Gonthier et al.: formalized in Coq (2012)

**Liquid Tensor Experiment:**
- Scholze's challenge: formalize condensed mathematics
- Completed in Lean (2022)

**Proof Assistants for Mathematics:**
- Lean Mathlib: comprehensive mathematical library
- Coq Mathematical Components: algebra, analysis
- Isabelle Archive of Formal Proofs

### Quantum Computing & Algorithms

**Shor's Algorithm:**
- Integer factorization in polynomial time
- Period finding via quantum Fourier transform
- Discrete logarithm

**Grover's Algorithm:**
- Unstructured search in O(√N)
- Optimal for quantum
- Amplitude amplification

**Quantum Walks:**
- Exponential speedup for some graph problems
- Element distinctness
- Triangle finding

**Quantum Error Correction:**
- Stabilizer codes
- Surface codes
- Threshold theorem

**Post-Quantum Cryptography:**
- Lattice-based (LWE, Ring-LWE)
- Code-based (McEliece)
- Hash-based signatures
- Isogeny-based (SIDH, CSIDH)
- Multivariate polynomial

### Numerical Analysis

**Floating Point Arithmetic:**
- IEEE 754 standard
- Rounding modes
- Machine epsilon
- Catastrophic cancellation

**Linear Algebra:**
- LU decomposition
- QR decomposition (Gram-Schmidt, Householder)
- SVD (Golub-Kahan, Jacobi)
- Iterative methods: Jacobi, Gauss-Seidel, CG, GMRES
- Preconditioning

**Eigenvalue Problems:**
- Power iteration
- QR algorithm
- Lanczos/Arnoldi iteration
- FEAST algorithm

**ODE Solvers:**
- Explicit: Euler, Runge-Kutta
- Implicit: backward Euler, Crank-Nicolson
- Adaptive step size
- Stiff equations

**PDE Solvers:**
- Finite difference method
- Finite element method (FEM)
- Spectral methods
- Multigrid methods
- Domain decomposition

**Optimization:**
- Gradient descent
- Newton's method
- Quasi-Newton (BFGS)
- Interior point methods
- Stochastic gradient descent
- Convex optimization (CVX, MOSEK)

### Machine Learning Mathematics

**Deep Learning Theory:**
- Neural tangent kernel (NTK)
- Mean field limit
- Universal approximation theorems
- Barron spaces
- Rademacher complexity
- PAC learning theory

**Optimization in ML:**
- Landscape of neural network loss
- Saddle points
- Flat minima
- Sharpness-aware minimization (SAM)
- Implicit regularization

**Information Geometry:**
- Fisher metric on statistical manifolds
- Natural gradient
- Amari's α-connections
- Applications: natural policy gradient

**Topological Data Analysis in ML:**
- Persistent homology features
- Mapper for clustering
- Topological regularization
- Shape of data

**Probabilistic ML:**
- Gaussian processes
- Variational inference
- MCMC methods (HMC, NUTS)
- Normalizing flows
- Diffusion models (score-based generative models)


---
