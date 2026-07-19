# Advanced Discrete Mathematics Reference

## Combinatorics Advanced
- **Generating Functions**: Encode sequences as power series. Solve recurrence relations.
  - Ordinary GF: A(x) = Σ aₙ xⁿ.
  - Exponential GF: A(x) = Σ aₙ xⁿ/n!.
- **Inclusion-Exclusion Principle**: |A∪B| = |A| + |B| - |A∩B|. Generalized for n sets.
- **Stirling Numbers**:
  - S(n,k): Ways to partition n elements into k non-empty subsets.
  - s(n,k): Signed Stirling numbers of first kind. Permutations with k cycles.
- **Catalan Numbers**: Cₙ = (1/(n+1)) * C(2n, n). Count binary trees, valid parenthesis strings, triangulations.

## Graph Theory Advanced
- **Planarity**: Kuratowski's Theorem: Graph is planar iff it contains no subdivision of K₅ or K₃,₃.
- **Coloring**: Chromatic polynomial P(G, k). Counts ways to color G with k colors.
- **Matching**: Hall's Marriage Theorem: Bipartite graph has perfect matching iff |N(S)| ≥ |S| for all subsets S.
- **Flows**: Max-Flow Min-Cut Theorem. Ford-Fulkerson algorithm.
- **Random Graphs**: Erdős–Rényi model G(n,p). Phase transitions for connectivity, giant component.

## Number Theory Advanced
- **Quadratic Residues**: a is quadratic residue mod p if x² ≡ a (mod p) has solution.
  - Legendre Symbol (a/p): 1 if residue, -1 if non-residue, 0 if a≡0.
  - Quadratic Reciprocity: (p/q)(q/p) = (-1)^((p-1)(q-1)/4).
- **Continued Fractions**: [a₀; a₁, a₂, ...]. Best rational approximations.
- **Diophantine Equations**: Polynomial equations with integer solutions.
  - Linear: ax + by = c. Solvable iff gcd(a,b)|c.
  - Pell's Equation: x² - Dy² = 1. Infinite solutions if D not square.

## Logic & Computability
- **Predicate Logic**: Quantifiers ∀, ∃. Prenex normal form.
- **Gödel's Incompleteness Theorems**:
  1. Any consistent formal system F within which a certain amount of elementary arithmetic can be carried out is incomplete; i.e., there are statements of the language of F which can neither be proved nor disproved in F.
  2. For any such system F, the consistency of F cannot be proved within F itself.
- **Turing Completeness**: System can simulate any Turing machine. Lambda calculus, cellular automata, modern CPUs are Turing complete.
- **P vs NP**:
  - P: Problems solvable in polynomial time.
  - NP: Problems verifiable in polynomial time.
  - Open question: Is P = NP? Most believe P ≠ NP.
  - NP-Complete: Hardest problems in NP (SAT, TSP, Clique). If one is in P, all are.

## Algebraic Structures
- **Groups**: Set with associative operation, identity, inverse.
- **Rings**: Set with two operations (+, *). (+) is abelian group, (*) is associative, distributive.
- **Fields**: Ring where every non-zero element has multiplicative inverse. Q, R, C, GF(p).
- **Lattices**: Partially ordered set where every pair has supremum (join) and infimum (meet). Boolean algebra is a lattice.