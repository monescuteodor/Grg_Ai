# Advanced Physics Reference for Grg AI

## Classical Mechanics
### Newton's Laws & Dynamics
- **First Law**: Inertia. Object remains at rest/uniform motion unless acted upon by force.
- **Second Law**: F = dp/dt = ma (for constant mass). Relates force, mass, acceleration.
- **Third Law**: Action-Reaction. Forces occur in pairs, equal magnitude, opposite direction.
- **Work-Energy Theorem**: W_net = ΔK. Work done by net force equals change in kinetic energy.
- **Conservation of Momentum**: Σp_initial = Σp_final (isolated system). Valid for collisions/explosions.
- **Lagrangian Mechanics**: L = T - V. Euler-Lagrange eq: d/dt(∂L/∂q̇) - ∂L/∂q = 0. Powerful for constrained systems.
- **Hamiltonian Mechanics**: H = Σpᵢq̇ᵢ - L. Hamilton's eqs: q̇ = ∂H/∂p, ṗ = -∂H/∂q. Phase space formulation.

### Rotational Motion
- **Torque**: τ = r × F = Iα. Rotational analog of force.
- **Angular Momentum**: L = Iω = r × p. Conserved if net external torque is zero.
- **Moment of Inertia**: I = Σmᵢrᵢ² or ∫r²dm. Resistance to rotational acceleration.
- **Rolling Without Slipping**: v_cm = Rω, a_cm = Rα. Static friction provides torque.

## Electromagnetism
### Electrostatics & Magnetostatics
- **Coulomb's Law**: F = k(q₁q₂)/r². Force between point charges.
- **Electric Field**: E = F/q₀. Gauss's Law: ∮E·dA = Q_enc/ε₀. Symmetry simplifies E calculation.
- **Electric Potential**: V = -∫E·dl. ΔV = -W/q. Equipotential surfaces ⊥ E field lines.
- **Biot-Savart Law**: dB = (μ₀/4π)(Idl×r̂)/r². Magnetic field from current element.
- **Ampere's Law**: ∮B·dl = μ₀I_enc. Useful for symmetric current distributions (solenoids, toroids).

### Electrodynamics
- **Faraday's Law**: ε = -dΦ_B/dt. Induced EMF from changing magnetic flux. Lenz's Law gives direction.
- **Maxwell's Equations**: Unify E and B fields. Predict EM waves travel at c = 1/√(μ₀ε₀).
- **Displacement Current**: ε₀(dΦ_E/dt). Completes Ampere's law for time-varying fields.
- **Poynting Vector**: S = (1/μ₀)(E×B). Energy flux density of EM wave. Intensity I = <|S|>.

## Thermodynamics & Statistical Mechanics
### Laws of Thermodynamics
- **Zeroth Law**: Thermal equilibrium defines temperature.
- **First Law**: ΔU = Q - W. Conservation of energy. Sign convention: Q>0 (heat in), W>0 (work by system).
- **Second Law**: Entropy S never decreases in isolated system. Heat flows hot→cold spontaneously. Carnot efficiency η = 1 - T_C/T_H.
- **Third Law**: S → 0 as T → 0 K. Absolute zero unattainable.

### Kinetic Theory & Stat Mech
- **Ideal Gas Law**: PV = nRT = NkT. Microscopic: P = (1/3)(N/V)m<v²>.
- **Equipartition Theorem**: Each quadratic DOF contributes (1/2)kT to avg energy. f DOFs → U = (f/2)nRT.
- **Boltzmann Distribution**: P(E) ∝ exp(-E/kT). Probability of state with energy E at temp T.
- **Entropy (Statistical)**: S = k ln Ω. Ω = number of microstates. Links macro/micro descriptions.

## Modern Physics
### Special Relativity
- **Postulates**: Laws of physics same in all inertial frames; c is constant.
- **Lorentz Factor**: γ = 1/√(1-v²/c²). Time dilation Δt = γΔt₀. Length contraction L = L₀/γ.
- **Relativistic Momentum**: p = γmv. Energy-momentum relation: E² = (pc)² + (mc²)².
- **Mass-Energy Equivalence**: E = mc². Rest energy E₀ = mc². Binding energy ΔE = Δmc².

### Quantum Mechanics
- **Wave-Particle Duality**: λ = h/p (de Broglie). Photoelectric effect: E_photon = hf = Φ + K_max.
- **Schrödinger Equation**: iℏ∂Ψ/∂t = ĤΨ. Time-dependent. Stationary states: Ĥψ = Eψ.
- **Uncertainty Principle**: ΔxΔp ≥ ℏ/2. Fundamental limit on simultaneous measurement precision.
- **Quantum Numbers**: n (principal), l (orbital), m_l (magnetic), m_s (spin). Pauli exclusion principle.
- **Tunneling**: Particle penetrates classically forbidden barrier. Probability ∝ exp(-2κL). Basis of STM, alpha decay.

## Common Formulas Quick Reference
- Kinematics: x = x₀ + v₀t + ½at²; v² = v₀² + 2aΔx
- Circular: a_c = v²/r = ω²r; F_c = mv²/r
- Gravitation: F = G(m₁m₂)/r²; U = -G(m₁m₂)/r
- Circuits: V=IR; P=IV; Series R_eq=ΣR; Parallel 1/R_eq=Σ(1/R)
- Optics: n₁sinθ₁=n₂sinθ₂; 1/f=1/d_o+1/d_i; m=-d_i/d_o
- Waves: v=fλ; f_n=nv/2L (string fixed both ends)