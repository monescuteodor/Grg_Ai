# Fluid Dynamics Reference

## Fundamental Properties
- **Density (ρ)**: Mass per unit volume.
- **Viscosity (μ)**: Resistance to deformation/shear stress.
- **Pressure (P)**: Force per unit area.
- **Surface Tension**: Cohesive forces at liquid surface.

## Flow Regimes
- **Laminar Flow**: Smooth, orderly layers. Low Reynolds number.
- **Turbulent Flow**: Chaotic, mixing eddies. High Reynolds number.
- **Reynolds Number (Re)**: Re = ρvL/μ. Ratio of inertial to viscous forces.
  - Pipe flow: Laminar if Re < 2300, Turbulent if Re > 4000.

## Conservation Laws
- **Continuity Equation**: ∂ρ/∂t + ∇·(ρv) = 0. Mass conservation.
  - Incompressible: ∇·v = 0. A₁v₁ = A₂v₂.
- **Navier-Stokes Equations**: ρ(∂v/∂t + v·∇v) = -∇P + μ∇²v + f. Momentum conservation. Nonlinear PDEs.
- **Bernoulli’s Principle**: P + ½ρv² + ρgh = constant. Energy conservation along streamline. Valid for inviscid, steady, incompressible flow.

## Drag & Lift
- **Drag Force**: F_D = ½ C_D ρ A v². Opposes motion.
  - C_D: Drag coefficient (depends on shape, Re).
- **Lift Force**: F_L = ½ C_L ρ A v². Perpendicular to flow.
  - C_L: Lift coefficient (depends on angle of attack, airfoil shape).
- **Boundary Layer**: Thin layer near surface where viscosity effects are significant. Separation causes drag increase.

## Pipe Flow
- **Poiseuille’s Law**: Q = (π R⁴ ΔP) / (8 μ L). Volumetric flow rate in laminar pipe flow.
- **Darcy-Weisbach Equation**: h_f = f (L/D) (v²/2g). Head loss due to friction.
  - f: Darcy friction factor (Moody chart).

## Compressible Flow
- **Mach Number (M)**: M = v/c. Ratio of flow speed to speed of sound.
  - Subsonic (M<1), Transonic (M≈1), Supersonic (M>1), Hypersonic (M>>1).
- **Shock Waves**: Discontinuous changes in P, T, ρ. Occur in supersonic flow.
- **Nozzles**: Converging (subsonic acceleration), Converging-Diverging (supersonic acceleration).

## Dimensional Analysis
- **Buckingham Pi Theorem**: Physical laws are independent of units. Reduce variables to dimensionless groups.
- **Key Numbers**:
  - Reynolds (Re): Inertia/Viscosity.
  - Froude (Fr): Inertia/Gravity.
  - Mach (M): Inertia/Compressibility.
  - Weber (We): Inertia/Surface Tension.