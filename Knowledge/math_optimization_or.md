# Optimization & Operations Research Reference

## Linear Programming (LP)
### Standard Form
- **Maximize**: cᵀx
- **Subject to**: Ax ≤ b, x ≥ 0
- **Feasible Region**: Convex polytope defined by constraints.
- **Optimal Solution**: Always at a vertex (corner point) of the feasible region.

### Simplex Method
- **Algorithm**: Moves from vertex to adjacent vertex along edges, improving objective value.
- **Pivot Operation**: Swaps basic and non-basic variables.
- **Complexity**: Exponential worst-case, but efficient in practice.
- **Degeneracy**: Multiple bases for same vertex → cycling risk. Solved by Bland's rule.

### Duality
- **Primal**: Max cᵀx s.t. Ax ≤ b.
- **Dual**: Min bᵀy s.t. Aᵀy ≥ c, y ≥ 0.
- **Weak Duality**: Dual objective ≥ Primal objective for any feasible solutions.
- **Strong Duality**: Optimal Primal = Optimal Dual if both feasible.
- **Complementary Slackness**: If primal constraint is not tight, dual variable is 0.

## Integer Programming (IP)
### NP-Hardness
- IP is NP-hard. No polynomial-time algorithm known for general case.
- Relaxation: Solve LP relaxation (ignore integer constraints) → upper bound.

### Branch and Bound
- **Branch**: Split problem into subproblems (e.g., x ≤ k, x ≥ k+1).
- **Bound**: Solve LP relaxation for each node. Prune if bound < current best integer solution.
- **Cutting Planes**: Add valid inequalities to tighten LP relaxation (Gomory cuts).

## Nonlinear Programming
### Unconstrained Optimization
- **Gradient Descent**: x_{k+1} = x_k - α∇f(x_k). Step size α critical.
- **Newton's Method**: x_{k+1} = x_k - [Hf(x_k)]⁻¹∇f(x_k). Uses Hessian matrix. Quadratic convergence near optimum.
- **BFGS**: Quasi-Newton method. Approximates inverse Hessian. Efficient for large problems.

### Constrained Optimization
- **Lagrange Multipliers**: L(x,λ) = f(x) + λᵀg(x). ∇L = 0 gives stationary points.
- **KKT Conditions**: Generalization for inequality constraints.
  1. Stationarity: ∇f + Σλᵢ∇gᵢ = 0
  2. Primal Feasibility: gᵢ(x) ≤ 0
  3. Dual Feasibility: λᵢ ≥ 0
  4. Complementary Slackness: λᵢgᵢ(x) = 0

## Combinatorial Optimization
### Graph Problems
- **Shortest Path**: Dijkstra (non-negative weights), Bellman-Ford (negative weights).
- **Minimum Spanning Tree**: Kruskal (sort edges), Prim (grow tree).
- **Traveling Salesman Problem (TSP)**: Find shortest Hamiltonian cycle. NP-hard. Heuristics: Nearest Neighbor, 2-opt, Genetic Algorithms.
- **Maximum Flow**: Ford-Fulkerson algorithm. Min-Cut Max-Flow Theorem.

### Dynamic Programming
- **Principle**: Break problem into overlapping subproblems. Store results.
- **Bellman Equation**: V(s) = max_a [R(s,a) + γΣ P(s'|s,a)V(s')].
- **Examples**: Knapsack problem, Sequence alignment, Matrix chain multiplication.