# Partial Differential Equations & Complex Analysis Reference

## Partial Differential Equations (PDEs)
### Classification
- **Second Order Linear PDE**: A u_xx + B u_xy + C u_yy + D u_x + E u_y + F u = G
- **Discriminant**: Δ = B² - 4AC
  - Δ < 0: Elliptic (e.g., Laplace, Poisson). Steady-state problems. No time dependence.
  - Δ = 0: Parabolic (e.g., Heat equation). Diffusion processes. Time-dependent.
  - Δ > 0: Hyperbolic (e.g., Wave equation). Wave propagation. Time-dependent.

### Key Equations
- **Laplace Equation**: ∇²u = 0. Potential theory, electrostatics, steady-state heat.
- **Poisson Equation**: ∇²u = f(x,y,z). Source term present. Gravity, electrostatics with charge.
- **Heat Equation**: u_t = k ∇²u. Thermal diffusion. Initial value problem.
- **Wave Equation**: u_tt = c² ∇²u. Vibrations, sound, light. Initial and boundary conditions.

### Solution Methods
- **Separation of Variables**: Assume u(x,t) = X(x)T(t). Reduces PDE to ODEs.
- **Fourier Series**: For bounded domains with periodic or fixed boundary conditions.
- **Fourier Transform**: For infinite domains. Converts PDE to ODE in frequency domain.
- **Laplace Transform**: For initial value problems. Converts time derivative to algebraic term.
- **Method of Characteristics**: For first-order PDEs and hyperbolic equations. Reduces PDE to ODE along characteristic curves.
- **Green's Functions**: Solves inhomogeneous PDEs with point source. G(x,x') satisfies L[G] = δ(x-x').

## Complex Analysis Advanced
### Conformal Mapping
- **Definition**: Analytic function f(z) preserves angles locally. f'(z) ≠ 0.
- **Applications**: Solving Laplace equation in complex geometries by mapping to simpler domain.
- **Common Maps**:
  - w = z²: Maps quadrant to half-plane.
  - w = e^z: Maps strip to half-plane.
  - w = 1/z: Inversion. Maps interior/exterior of circle.
  - Möbius Transform: w = (az+b)/(cz+d). Maps circles/lines to circles/lines.

### Residue Theorem Applications
- **Real Integrals**: ∫_{-∞}^{∞} f(x)dx. Close contour in upper/lower half-plane. Sum residues inside.
- **Trigonometric Integrals**: ∫₀^{2π} R(cosθ, sinθ)dθ. Substitute z=e^{iθ}. Integrate over unit circle.
- **Summation of Series**: Use π cot(πz) or π csc(πz) as kernel. Sum residues at integers.

### Analytic Continuation
- **Principle**: Unique extension of analytic function beyond original domain.
- **Riemann Surface**: Multi-valued functions (log, sqrt) become single-valued on surface.
- **Branch Cuts**: Artificial cuts to define single-valued branch. Choice affects integration path.

### Gamma & Zeta Functions
- **Gamma Function**: Γ(z) = ∫₀^∞ t^{z-1}e^{-t}dt. Extension of factorial. Γ(n+1)=n!.
- **Properties**: Γ(z+1)=zΓ(z). Reflection formula: Γ(z)Γ(1-z) = π/sin(πz).
- **Riemann Zeta**: ζ(s) = Σ 1/n^s. Analytic continuation to whole complex plane except s=1.
- **Riemann Hypothesis**: All non-trivial zeros have real part 1/2. Deep connection to prime distribution.