# CHAPTER 17: CONTROL THEORY & OPTIMAL CONTROL


## Classical Control Theory

### Linear Systems

**State-Space Representation:**
ẋ(t) = Ax(t) + Bu(t)
y(t) = Cx(t) + Du(t)
where x ∈ ℝⁿ, u ∈ ℝᵐ, y ∈ ℝᵖ.

**Controllability:**
System is controllable if rank[B, AB, A²B, ..., Aⁿ⁻¹B] = n.
- Kalman controllability decomposition
- Controllable canonical form
- PBH test: rank[λI - A, B] = n for all λ ∈ ℂ

**Observability:**
System is observable if rank[C; CA; ...; CAⁿ⁻¹] = n.
- Dual of controllability
- Observable canonical form
- Luenberger observer

**Stability:**
- Asymptotic stability: Re(λ(A)) < 0
- Lyapunov equation: A*P + PA = -Q
- Hurwitz criterion, Routh-Hurwitz

**Transfer Functions:**
G(s) = C(sI - A)⁻¹B + D
- Poles and zeros
- Bode plots, Nyquist criterion
- Root locus

**Feedback Design:**
- Pole placement (Ackermann's formula)
- LQR (Linear Quadratic Regulator)
- LQG (Linear Quadratic Gaussian)
- H∞ control
- μ-synthesis

### Nonlinear Control

**Lyapunov Methods:**
- Direct method: V(x) > 0, V̇(x) < 0 ⇒ stable
- LaSalle's invariance principle
- Control Lyapunov functions (CLF)
- Sontag's formula: u = -(L_fV + √((L_fV)² + (L_gV)⁴))/(L_gV)

**Feedback Linearization:**
- Input-output linearization
- Full-state linearization
- Relative degree
- Zero dynamics
- Normal form

**Sliding Mode Control:**
- Switching surface s(x) = 0
- Reaching condition: s·ṡ < 0
- Chattering reduction
- Higher-order sliding modes

**Backstepping:**
Recursive design for strict-feedback systems.
- Virtual control inputs
- Lyapunov function construction
- Adaptive backstepping

**Passivity-Based Control:**
- Passive systems: yᵀu ≥ V̇
- Interconnection and damping assignment (IDA)
- Port-Hamiltonian systems

## Optimal Control

### Calculus of Variations in Control

**Problem Statement:**
Minimize J = ∫_{t₀}^{t_f} L(x,u,t) dt + Φ(x(t_f))
subject to ẋ = f(x,u,t), x(t₀) = x₀

**Pontryagin's Maximum Principle:**
Define Hamiltonian: H(x,u,p,t) = L(x,u,t) + pᵀf(x,u,t)
Necessary conditions:
1. ẋ = ∂H/∂p = f(x,u,t)
2. ṗ = -∂H/∂x (costate equation)
3. u* = argmin_u H(x,u,p,t) (minimization condition)
4. Transversality: p(t_f) = ∂Φ/∂x(t_f)

**Bang-Bang Control:**
For linear systems with bounded control:
u*(t) ∈ {u_min, u_max} almost everywhere.
- Switching function
- Singular arcs
- Time-optimal control

### Dynamic Programming

**Hamilton-Jacobi-Bellman Equation:**
For value function V(x,t) = min_u J:
-∂V/∂t = min_u [L(x,u,t) + ∇V·f(x,u,t)]
V(x,t_f) = Φ(x)

**Verification Theorem:**
If V satisfies HJB and u* achieves the min, then u* is optimal.

**Discrete-Time:**
V_k(x) = min_u [L(x,u) + V_{k+1}(f(x,u))]

**Curse of Dimensionality:**
HJB suffers from exponential growth in state dimension.
- Approximate dynamic programming
- Neural network value function approximation

### Stochastic Optimal Control

**Stochastic HJB:**
For dx = f(x,u)dt + σ(x,u)dW:
-∂V/∂t = min_u [L + ∇V·f + ½tr(σσᵀ∇²V)]

**Linear-Quadratic-Gaussian (LQG):**
- Separation principle: design controller and estimator separately
- Kalman filter for state estimation
- Certainty equivalence

**Risk-Sensitive Control:**
Minimize (1/γ) log E[exp(γJ)]
- γ > 0: risk-averse
- γ < 0: risk-seeking
- γ → 0: recovers LQG

**Mean Field Games:**
N-player games where N → ∞.
- Coupled HJB-Fokker-Planck equations
- Nash equilibrium in distribution
- Applications: economics, crowd dynamics, energy systems

### Model Predictive Control (MPC)

**Algorithm:**
1. At time t, measure/estimate current state x(t)
2. Solve finite-horizon optimal control problem
3. Apply first control input u*(t)
4. Repeat at t+1

**Stability:**
- Terminal cost and terminal set constraints
- Lyapunov function from value function
- Receding horizon principle

**Robust MPC:**
- Min-max MPC
- Tube MPC
- Scenario-based MPC

**Economic MPC:**
- Cost function not necessarily positive definite
- Steady-state optimization
- Dissipativity assumption

### Geometric Control Theory

**Distributions:**
Δ = span{f₁, ..., fₖ} on manifold M.
- Involutive: [X,Y] ∈ Δ for all X,Y ∈ Δ
- Frobenius theorem: involutive ⇔ integrable

**Accessibility:**
- Lie algebra rank condition (LARC)
- Chow's theorem: bracket-generating ⇒ accessible

**Controllability on Lie Groups:**
- Left-invariant systems
- Affine systems on Lie groups
- Rolling bodies
- Quantum control

**Sub-Riemannian Geometry:**
- Metric defined only on distribution
- Carnot-Carathéodory distance
- Geodesics: abnormal and normal
- Hörmander's condition
- Applications: robotics, vision, hypoelliptic PDEs

### Optimal Transport in Control

**Schrödinger Bridge:**
Most likely evolution between two probability distributions.
- Regularized optimal transport
- Connection to stochastic control
- Entropic regularization

**Steering of Distributions:**
- Schrödinger system
- Fortet-IPF algorithm
- Sinkhorn iterations
- Applications: mean field control, density control

---
