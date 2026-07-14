-- ============================================================
-- VHDL-AMS COMPLETE REFERENCE
-- Analog & Mixed-Signal Extensions to VHDL (IEEE 1076.1-2017)
-- ============================================================

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.electrical_systems.all;    -- Analog electrical domain
use IEEE.mechanical_systems.all;    -- Mechanical domain
use IEEE.thermal_systems.all;       -- Thermal domain
use IEEE.fundamental_constants.all; -- Physical constants

-- ============================================================
-- CHAPTER 1: QUANTITIES, NATURES, AND TERMINALS
-- ============================================================

entity Resistor is
  generic (
    R : REAL := 1.0e3   -- Resistance in Ohms
  );
  port (
    terminal T1, T2 : electrical   -- Electrical terminals (nodes)
  );
end entity Resistor;

architecture Ohmic of Resistor is
  -- Quantity: a continuous-time analog signal
  quantity V across I through T1 to T2;  -- V = voltage across, I = current through
begin
  V == I * R;  -- Analog equation (== is simultaneous statement, NOT assignment!)
end architecture Ohmic;

-- ============================================================
-- CHAPTER 2: CAPACITOR, INDUCTOR, DIODE
-- ============================================================

entity Capacitor is
  generic (
    C : REAL := 1.0e-6   -- Capacitance in Farads
  );
  port (
    terminal T1, T2 : electrical
  );
end entity Capacitor;

architecture Behavioral of Capacitor is
  quantity V across I through T1 to T2;
begin
  I == C * V'dot;  -- V'dot = derivative of V with respect to time
end architecture Behavioral;

entity Inductor is
  generic (
    L : REAL := 1.0e-3   -- Inductance in Henries
  );
  port (
    terminal T1, T2 : electrical
  );
end entity Inductor;

architecture Behavioral of Inductor is
  quantity V across I through T1 to T2;
begin
  V == L * I'dot;  -- I'dot = derivative of current
end architecture Behavioral;

-- Diode with Shockley equation
entity Diode is
  generic (
    ISAT : REAL := 1.0e-14;   -- Saturation current
    N    : REAL := 1.0;       -- Ideality factor
    VT   : REAL := 25.85e-3   -- Thermal voltage at 300K (~26mV)
  );
  port (
    terminal Anode, Cathode : electrical
  );
end entity Diode;

architecture Nonlinear of Diode is
  quantity VD across ID through Anode to Cathode;
begin
  ID == ISAT * (exp(VD / (N * VT)) - 1.0);
end architecture Nonlinear;

-- ============================================================
-- CHAPTER 3: MIXED-SIGNAL (DIGITAL + ANALOG INTERFACE)
-- ============================================================

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.electrical_systems.all;

entity ADC_Simple is
  generic (
    V_REF   : REAL := 3.3;      -- Reference voltage
    N_BITS  : INTEGER := 12     -- Resolution
  );
  port (
    signal CLK, START : in std_logic;
    signal DONE       : out std_logic;
    signal D_OUT      : out std_logic_vector(N_BITS-1 downto 0);
    terminal A_IN     : electrical   -- Analog input
  );
end entity ADC_Simple;

architecture Mixed of ADC_Simple is
  quantity V_IN across A_IN;
  signal   digital_value : INTEGER range 0 to 2**N_BITS - 1;
  constant LSB : REAL := V_REF / REAL(2**N_BITS);
begin
  -- Analog side: just read the voltage
  -- Digital side: convert on rising edge of START
  process (CLK)
  begin
    if rising_edge(CLK) then
      if START = '1' then
        digital_value <= INTEGER(V_IN / LSB);
        DONE <= '1';
      else
        DONE <= '0';
      end if;
    end if;
  end process;
  
  D_OUT <= std_logic_vector(to_unsigned(digital_value, N_BITS));
end architecture Mixed;

-- ============================================================
-- CHAPTER 4: MULTI-DOMAIN (ELECTRO-THERMAL-MECHANICAL)
-- ============================================================

use IEEE.thermal_systems.all;
use IEEE.mechanical_systems.all;

entity MEMS_Resonator is
  port (
    terminal elec_in, elec_out : electrical;
    terminal mech_anchor       : translational
  );
end entity MEMS_Resonator;

architecture MultiDomain of MEMS_Resonator is
  -- Electrical quantities
  quantity V_drive across I_drive through elec_in;
  quantity V_sense across I_sense through elec_out;
  
  -- Mechanical quantities
  quantity X across F through mech_anchor;  -- Displacement and force
  
  -- Thermal quantity (self-heating)
  quantity T : temperature;  -- Free quantity (not across/through)
  
  -- Physical parameters
  constant M : REAL := 1.0e-9;   -- Mass (kg)
  constant K : REAL := 10.0;     -- Spring constant (N/m)
  constant D : REAL := 1.0e-6;   -- Damping (N·s/m)
  
begin
  -- Mechanical: mass-spring-damper
  F == M * X'dot'dot + D * X'dot + K * X;
  
  -- Electrostatic coupling (simplified)
  F == 0.5 * V_drive * V_drive;  -- Electrostatic force ~ V^2
  
  -- Thermal: self-heating from power dissipation
  T'dot == (V_drive * I_drive - (T - 300.0) / 100.0) / (1.0e-6);
  
  -- Output sensing (capacitive)
  V_sense == X * 1.0e3;  -- Capacitive displacement sensing
end architecture MultiDomain;

-- ============================================================
-- CHAPTER 5: FREQUENCY DOMAIN (SMALL-SIGNAL AC ANALYSIS)
-- ============================================================

entity OpAmp_AC is
  port (
    terminal In_P, In_N, Out : electrical
  );
end entity OpAmp_AC;

architecture AC of OpAmp_AC is
  quantity V_diff across In_P to In_N;
  quantity V_out across I_out through Out;
  
  -- AC quantity: phasor (magnitude and phase)
  quantity V_out_ac : REAL spectrum 1.0, 0.0;  -- AC magnitude=1, phase=0
  
  constant A0   : REAL := 1.0e5;    -- DC gain
  constant F_P1 : REAL := 10.0;     -- First pole (Hz)
  constant F_P2 : REAL := 1.0e6;   -- Second pole (Hz)
  constant W_P1 : REAL := math_2_pi * F_P1;
  constant W_P2 : REAL := math_2_pi * F_P2;
begin
  -- Laplace-domain transfer function using 'ltf attribute
  V_out == V_diff * A0 / ((1.0 + (frequency / F_P1)) * (1.0 + (frequency / F_P2)));
  
  -- Alternative: use 'ztf for Z-domain (discrete-time)
end architecture AC;

-- ============================================================
-- CHAPTER 6: NOISE ANALYSIS (SMALL-SIGNAL NOISE)
-- ============================================================

entity Noisy_Resistor is
  generic (
    R     : REAL := 1.0e3;
    T_K   : REAL := 300.0   -- Temperature in Kelvin
  );
  port (
    terminal T1, T2 : electrical
  );
end entity Noisy_Resistor;

architecture ThermalNoise of Noisy_Resistor is
  quantity V across I through T1 to T2;
  
  -- Noise source: thermal (Johnson-Nyquist) noise
  -- 4 * k * T * R * delta_f
  quantity V_noise : REAL noise 4.0 * boltzmann_constant * T_K * R;
begin
  V == I * R + V_noise;  -- Add noise to ideal resistor
end architecture ThermalNoise;

-- ============================================================
-- CHAPTER 7: BREAK STATEMENTS AND INITIAL CONDITIONS
-- ============================================================

entity RLC_Circuit is
  port (
    terminal N1, N2 : electrical
  );
end entity RLC_Circuit;

architecture Transient of RLC_Circuit is
  quantity V across I through N1 to N2;
  quantity V_C across I_C through N1;  -- Capacitor voltage
  quantity V_L across I_L through N2;  -- Inductor current
  
  constant R : REAL := 10.0;
  constant C : REAL := 1.0e-6;
  constant L : REAL := 1.0e-3;
begin
  -- Initial conditions using 'dot and break
  break V_C => 0.0, I_L => 0.0;  -- Initial condition at t=0
  
  V == I * R;
  I_C == C * V_C'dot;
  V_L == L * I_L'dot;
  
  -- Break on event (e.g., switch closing at t=1ms)
  if NOW > 1.0e-3 sec use
    break I => 1.0e-3;  -- Inject current step
  end use;
end architecture Transient;

-- ============================================================
-- CHAPTER 8: SPECTRAL SOURCE (NOISE, MODULATION)
-- ============================================================

entity FM_Modulator is
  port (
    terminal Mod_In, RF_Out : electrical
  );
end entity FM_Modulator;

architecture Spectral of FM_Modulator is
  quantity V_mod across Mod_In;
  quantity V_rf across I_rf through RF_Out;
  
  constant FC : REAL := 1.0e9;   -- Carrier frequency (1 GHz)
  constant KF : REAL := 1.0e6;  -- Frequency sensitivity (Hz/V)
begin
  -- FM signal: spectral source
  V_rf == 1.0 * sin(
    math_2_pi * FC * NOW + 
    math_2_pi * KF * integral(V_mod)
  );
end architecture Spectral;

-- ============================================================
-- CHAPTER 9: TERMINAL ARRAYS AND GENERATE (STRUCTURAL)
-- ============================================================

entity Resistor_Ladder is
  generic (
    N : INTEGER := 8
  );
  port (
    terminal In_Term  : electrical;
    terminal Out_Term : electrical;
    terminal Taps     : electrical_vector(1 to N)  -- Array of terminals!
  );
end entity Resistor_Ladder;

architecture Structural of Resistor_Ladder is
  -- Internal node array
  terminal Internal(0 to N) : electrical;
begin
  -- Connect ends
  Internal(0) == In_Term;
  Internal(N) == Out_Term;
  
  -- Generate N resistors
  gen_resistors: for I in 1 to N generate
    R: entity work.Resistor
      generic map (R => 1.0e3)
      port map (T1 => Internal(I-1), T2 => Internal(I));
  end generate gen_resistors;
  
  -- Tap connections
  gen_taps: for I in 1 to N generate
    Taps(I) == Internal(I);
  end generate gen_taps;
end architecture Structural;

-- ============================================================
-- CHAPTER 10: REAL-VALUED ATTRIBUTES AND SIMULATION CONTROL
-- ============================================================

entity Simulation_Control is
end entity Simulation_Control;

architecture Behav of Simulation_Control is
  quantity T : REAL;  -- Free quantity
begin
  -- Access simulation time and control
  T == NOW;  -- NOW = current simulation time
  
  -- Breakpoints for detailed analysis
  break on T when T > 1.0e-3;  -- Stop/restart at 1ms
  
  -- Tolerance control
  -- 'above threshold detection
  if T'above(1.0e-6) use
    -- Code for t > 1 microsecond
  end use;
  
  -- Ramping (pseudo-transient for DC convergence)
  -- 'ramp attribute for gradual change
end architecture Behav;