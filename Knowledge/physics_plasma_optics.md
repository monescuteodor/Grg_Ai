# Plasma Physics & Advanced Optics Reference

## Plasma Physics
### Fundamentals
- **Plasma Definition**: Ionized gas with quasi-neutrality (n_e ≈ n_i). Collective behavior.
- **Debye Shielding**: Charge screening length λ_D = √(ε₀ kT / n_e e²). Plasma condition: L >> λ_D.
- **Plasma Frequency**: ω_p = √(n_e e² / ε₀ m_e). Natural oscillation frequency of electrons.
- **Temperature**: Measured in eV. 1 eV ≈ 11,600 K. T_e, T_i, T_n may differ.

### Single Particle Motion
- **Lorentz Force**: F = q(E + v × B).
- **Gyration**: Circular motion around B field lines. Larmor radius r_L = mv⊥/qB. Cyclotron frequency ω_c = qB/m.
- **Drifts**:
  - E × B Drift: v_E = (E × B)/B². Independent of charge/mass.
  - Gradient B Drift: Due to magnetic field gradient. Charge dependent.
  - Curvature Drift: Due to curved field lines. Charge dependent.

### Magnetohydrodynamics (MHD)
- **Assumption**: Plasma as conducting fluid. Timescales >> gyroperiod.
- **Ohm's Law**: E + v × B = ηJ. η = resistivity. Ideal MHD: η = 0 → E = -v × B.
- **Frozen-in Flux**: Magnetic field lines move with plasma in ideal MHD.
- **MHD Waves**: Alfvén waves (transverse, along B), Magnetosonic waves (compressional).

### Confinement & Fusion
- **Tokamak**: Toroidal device. Toroidal B from coils, Poloidal B from plasma current. Helical field lines.
- **Stellarator**: Twisted torus. External coils create helical field. No plasma current needed.
- **Lawson Criterion**: nτ_E T > threshold. Triple product for ignition. DT fusion: ~3×10²¹ keV·s/m³.
- **Instabilities**: Kink, sausage, tearing modes. Disrupt confinement. Control via feedback, shaping.

## Advanced Optics
### Interference & Diffraction
- **Young's Double Slit**: Fringe spacing Δy = λL/d. Coherence required.
- **Thin Film Interference**: Phase shift upon reflection. Constructive/destructive depending on thickness n_d.
- **Fraunhofer Diffraction**: Far-field. Fourier transform of aperture. Single slit: I(θ) = I₀ sinc²(β).
- **Fresnel Diffraction**: Near-field. Curved wavefronts. Fresnel zones.

### Polarization
- **States**: Linear, Circular, Elliptical. Jones vectors describe state.
- **Malus' Law**: I = I₀ cos²θ. Transmitted intensity through polarizer.
- **Birefringence**: Different refractive indices for different polarizations. Ordinary/extraordinary rays.
- **Optical Activity**: Rotation of polarization plane. Chiral molecules.

### Lasers
- **Stimulated Emission**: Photon induces excited atom to emit identical photon. Coherence.
- **Population Inversion**: More atoms in excited state than ground state. Required for gain.
- **Resonator**: Mirrors provide feedback. Modes determined by cavity length L. Longitudinal modes: ν_q = qc/2L.
- **Types**: Gas (HeNe, CO₂), Solid-state (Nd:YAG), Semiconductor (Diode), Fiber.

### Nonlinear Optics
- **High Intensity**: Polarization P depends nonlinearly on E. P = ε₀(χ⁽¹⁾E + χ⁽²⁾E² + χ⁽³⁾E³ + ...).
- **Second Harmonic Generation (SHG)**: χ⁽²⁾ process. 2ω output from ω input. Requires non-centrosymmetric crystal.
- **Kerr Effect**: χ⁽³⁾ process. Refractive index depends on intensity: n(I) = n₀ + n₂I. Self-focusing.
- **Four-Wave Mixing**: Interaction of four waves. Parametric amplification.
