Space Systems Engineering Complete Reference
CHAPTER 1: GETTING STARTED WITH SPACE SYSTEMS
Remarks
Space Systems Engineering involves the design, development, and operation of spacecraft and launch vehicles. It integrates orbital mechanics, guidance navigation and control (GNC), propulsion, thermal control, power systems, and communications. Key challenges: extreme environments (vacuum, radiation, temperature extremes), high reliability requirements, mass/power constraints, and long communication delays. Applications: Satellites (communication, Earth observation), interplanetary probes, human spaceflight, launch services.
Tools: Python (NumPy, SciPy, Astropy, Poliastro), MATLAB/Simulink, GMAT (NASA General Mission Analysis Tool), STK (Systems Tool Kit), SPICE Toolkit (JPL).
Hello Orbital Mechanics
# hello_orbit.py
"""
First space program: Calculate orbital velocity and period for a circular orbit.
"""
import numpy as np

# Constants
MU_EARTH = 3.986004418e14  # m^3/s^2 (Standard Gravitational Parameter)
R_EARTH = 6371000          # m (Mean Radius)

def circular_orbit_velocity(altitude_m):
    """Calculate velocity for a circular orbit."""
    r = R_EARTH + altitude_m
    return np.sqrt(MU_EARTH / r)

def orbital_period(altitude_m):
    """Calculate orbital period in seconds."""
    r = R_EARTH + altitude_m
    return 2 * np.pi * np.sqrt(r**3 / MU_EARTH)

# Example: Low Earth Orbit (LEO) at 400 km (ISS altitude)
alt_iss = 400000  # meters
v_iss = circular_orbit_velocity(alt_iss)
T_iss = orbital_period(alt_iss)

print("=== Circular Orbit Calculations ===")
print(f"Altitude: {alt_iss/1000:.1f} km")
print(f"Orbital Velocity: {v_iss:.2f} m/s ({v_iss*3.6:.2f} km/h)")
print(f"Orbital Period: {T_iss:.1f} s ({T_iss/60:.2f} min)")

# Geostationary Orbit (GEO)
# Period must match Earth's rotation: 86164 seconds (sidereal day)
def geo_altitude():
    """Calculate altitude for geostationary orbit."""
    T_geo = 86164  # seconds
    # Kepler's Third Law: T^2 = (4*pi^2 / MU) * a^3
    a = ((MU_EARTH * T_geo**2) / (4 * np.pi**2))**(1/3)
    return a - R_EARTH

alt_geo = geo_altitude()
v_geo = circular_orbit_velocity(alt_geo)
print(f"\nGeostationary Orbit:")
print(f"Altitude: {alt_geo/1000:.1f} km")
print(f"Velocity: {v_geo:.2f} m/s")

CHAPTER 2: ORBITAL MECHANICS
Kepler's Laws
# 1. Orbits are ellipses with the central body at one focus.
# 2. A line segment joining a planet and the Sun sweeps out equal areas during equal intervals of time.
# 3. The square of the orbital period is proportional to the cube of the semi-major axis.

# Orbital Elements (Keplerian Elements):
# a: Semi-major axis
# e: Eccentricity (0=circle, 0<e<1=ellipse, e=1=parabola, e>1=hyperbola)
# i: Inclination
# Omega: Right Ascension of Ascending Node (RAAN)
# omega: Argument of Periapsis
# nu: True Anomaly (position in orbit)

def vis_viva_equation(a, r):
    """Calculate velocity at distance r for an orbit with semi-major axis a."""
    return np.sqrt(MU_EARTH * (2/r - 1/a))

# Example: Elliptical Orbit Transfer (Hohmann Transfer)
def hohmann_transfer(r1, r2):
    """
    Calculate delta-v for Hohmann transfer between two circular orbits.
    r1: radius of initial orbit
    r2: radius of final orbit
    """
    a_trans = (r1 + r2) / 2
    
    # Velocity in initial circular orbit
    v1 = np.sqrt(MU_EARTH / r1)
    
    # Velocity at periapsis of transfer orbit
    v_trans_1 = np.sqrt(MU_EARTH * (2/r1 - 1/a_trans))
    
    # Delta-v 1
    dv1 = abs(v_trans_1 - v1)
    
    # Velocity at apoapsis of transfer orbit
    v_trans_2 = np.sqrt(MU_EARTH * (2/r2 - 1/a_trans))
    
    # Velocity in final circular orbit
    v2 = np.sqrt(MU_EARTH / r2)
    
    # Delta-v 2
    dv2 = abs(v2 - v_trans_2)
    
    return dv1, dv2, dv1 + dv2

# LEO to GEO Transfer
r_leo = R_EARTH + 400000
r_geo = R_EARTH + alt_geo
dv1, dv2, dv_total = hohmann_transfer(r_leo, r_geo)

print("\n=== Hohmann Transfer (LEO to GEO) ===")
print(f"Delta-v 1 (Periapsis): {dv1:.2f} m/s")
print(f"Delta-v 2 (Apoapsis): {dv2:.2f} m/s")
print(f"Total Delta-v: {dv_total:.2f} m/s")

Lambert's Problem
# Given two position vectors and time of flight, find the orbit connecting them.
# Used for interplanetary trajectory design.

from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Earth, Mars
from poliastro.twobody import Orbit
from poliastro.maneuver import Maneuver
from poliastro.util import norm

def lambert_transfer_example():
    """Simple Lambert transfer from Earth to Mars."""
    # Define departure and arrival dates
    departure_date = Time("2025-01-01", scale="utc")
    arrival_date = Time("2025-07-01", scale="utc")
    tof = (arrival_date - departure_date).to(u.s)
    
    # Get planetary positions (simplified)
    # In real applications, use SPICE kernels or JPL Horizons
    earth_orbit = Orbit.from_body_ephem(Earth, departure_date)
    mars_orbit = Orbit.from_body_ephem(Mars, arrival_date)
    
    # Solve Lambert's problem
    # (ss_f, ss_b) = lambert(Earth.k, earth_orbit.r, mars_orbit.r, tof)
    
    print("Lambert Transfer Calculation requires poliastro installation.")
    print("pip install poliastro")

# lambert_transfer_example()

CHAPTER 3: GUIDANCE, NAVIGATION, AND CONTROL (GNC)
Attitude Determination
# Determining the orientation of the spacecraft.
# Sensors: Star trackers, Sun sensors, Magnetometers, Gyroscopes.
# Representations: Euler Angles, Quaternions, Direction Cosine Matrices.

import numpy as np

def euler_to_quaternion(phi, theta, psi):
    """Convert Euler angles (roll, pitch, yaw) to quaternion."""
    cy = np.cos(psi * 0.5)
    sy = np.sin(psi * 0.5)
    cp = np.cos(theta * 0.5)
    sp = np.sin(theta * 0.5)
    cr = np.cos(phi * 0.5)
    sr = np.sin(phi * 0.5)
    
    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy
    
    return np.array([w, x, y, z])

def quaternion_multiply(q1, q2):
    """Multiply two quaternions."""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    
    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2
    
    return np.array([w, x, y, z])

# Example
roll, pitch, yaw = np.radians([10, 20, 30])
q = euler_to_quaternion(roll, pitch, yaw)
print(f"Quaternion: {q}")

Attitude Control
# Actuators: Reaction Wheels, Control Moment Gyros (CMGs), Thrusters, Magnetorquers.
# Control Laws: PID, Sliding Mode, Adaptive Control.

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0
        
    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        return output

# Simulation of attitude stabilization
def simulate_attitude_control(initial_angle, target_angle, duration=100, dt=0.1):
    angle = initial_angle
    angular_velocity = 0
    controller = PIDController(kp=0.5, ki=0.01, kd=0.1)
    
    history = []
    
    for _ in range(int(duration/dt)):
        error = target_angle - angle
        torque = controller.update(error, dt)
        
        # Simple dynamics: I * alpha = torque
        inertia = 100
        angular_acceleration = torque / inertia
        
        angular_velocity += angular_acceleration * dt
        angle += angular_velocity * dt
        
        history.append((angle, torque))
        
    return history

history = simulate_attitude_control(np.radians(45), 0)
print(f"Final Angle: {np.degrees(history[-1][0]):.2f} degrees")

CHAPTER 4: PROPULSION SYSTEMS
Rocket Equation
# Tsiolkovsky Rocket Equation:
# Delta-v = Ve * ln(m0 / mf)
# Ve: Effective exhaust velocity
# m0: Initial mass (wet)
# mf: Final mass (dry)

def rocket_equation(ve, m0, mf):
    """Calculate Delta-v using Tsiolkovsky equation."""
    return ve * np.log(m0 / mf)

# Example: Single Stage to Orbit (SSTO) concept
ve = 3000  # m/s (typical for LOX/LH2)
m0 = 100000  # kg
mf = 10000   # kg (10% dry mass fraction)
dv = rocket_equation(ve, m0, mf)
print(f"\n=== Rocket Equation ===")
print(f"Delta-v: {dv:.2f} m/s")

Specific Impulse (Isp)
# Isp = Ve / g0
# Measure of efficiency. Higher Isp means less propellant needed.

def isp_to_ve(isp):
    """Convert Specific Impulse to Exhaust Velocity."""
    g0 = 9.80665
    return isp * g0

isp_lox_lh2 = 450  # seconds
ve_lox_lh2 = isp_to_ve(isp_lox_lh2)
print(f"Isp: {isp_lox_lh2} s -> Ve: {ve_lox_lh2:.2f} m/s")

Electric Propulsion
# Ion Thrusters, Hall Effect Thrusters.
# High Isp (2000-5000 s), low thrust.
# Used for station keeping and deep space missions.

def electric_propulsion_delta_v(isp, power, efficiency, mass_flow_rate, duration):
    """Calculate Delta-v for electric propulsion."""
    ve = isp_to_ve(isp)
    thrust = mass_flow_rate * ve
    # Power = 0.5 * mass_flow_rate * ve^2 / efficiency
    # This is a simplified model
    
    # Total mass ejected
    dm = mass_flow_rate * duration
    
    # Assume constant mass for simplicity (low thrust, long duration)
    # For accurate calculation, integrate over changing mass
    
    return ve * np.log(1000 / (1000 - dm)) # Assuming 1000kg spacecraft

CHAPTER 5: THERMAL CONTROL
Heat Transfer in Space
# Conduction, Convection (internal only), Radiation.
# No convection in vacuum.
# Stefan-Boltzmann Law: P = epsilon * sigma * A * T^4

SIGMA = 5.670374419e-8  # W/m^2/K^4

def radiative_power(epsilon, area, temperature_k):
    """Calculate radiated power."""
    return epsilon * SIGMA * area * temperature_k**4

def equilibrium_temperature(alpha, area_absorb, epsilon, area_emit, solar_flux=1361):
    """Calculate equilibrium temperature of a satellite."""
    # Absorbed Power = Emitted Power
    # alpha * A_abs * S = epsilon * A_emit * sigma * T^4
    t_eq = ((alpha * area_absorb * solar_flux) / (epsilon * area_emit * SIGMA))**0.25
    return t_eq

# Example: CubeSat
alpha = 0.2  # Absorptivity
epsilon = 0.8  # Emissivity
area = 0.01  # m^2 (one face of 10cm cube)
# Assume all faces emit, but only one face absorbs sunlight directly
t_eq = equilibrium_temperature(alpha, area, epsilon, area*6)
print(f"\n=== Thermal Control ===")
print(f"Equilibrium Temperature: {t_eq:.2f} K ({t_eq-273.15:.2f} C)")

Multi-Layer Insulation (MLI)
# Layers of reflective foil separated by spacers.
# Reduces radiative heat transfer.
# Effective emissivity can be very low (<0.05).

CHAPTER 6: POWER SYSTEMS
Solar Arrays
# Power = Solar Flux * Area * Efficiency * Cos(theta)
# Degradation over time due to radiation.

def solar_power(area, efficiency, degradation_years, years):
    """Calculate solar power after degradation."""
    solar_flux = 1361  # W/m^2 (AM0)
    deg_factor = (1 - 0.02)**years  # 2% degradation per year
    return solar_flux * area * efficiency * deg_factor

power_initial = solar_power(1.0, 0.3, 0, 0)
power_10yr = solar_power(1.0, 0.3, 0, 10)
print(f"\n=== Power Systems ===")
print(f"Initial Power (1m^2, 30% eff): {power_initial:.2f} W")
print(f"Power after 10 years: {power_10yr:.2f} W")

Batteries
# Lithium-Ion, Nickel-Hydrogen.
# Depth of Discharge (DoD) affects lifespan.
# Eclipse periods require battery power.

def battery_capacity_required(power_load, eclipse_duration_hours, dod_max=0.8):
    """Calculate required battery capacity in Wh."""
    energy_needed = power_load * eclipse_duration_hours
    capacity = energy_needed / dod_max
    return capacity

cap = battery_capacity_required(100, 0.7)  # 100W load, 42min eclipse
print(f"Required Battery Capacity: {cap:.2f} Wh")

CHAPTER 7: COMMUNICATIONS
Link Budget
# Calculates signal strength at receiver.
# Friis Transmission Equation:
# Pr = Pt * Gt * Gr * (lambda / (4*pi*d))^2

def friis_equation(pt_watts, gt_db, gr_db, frequency_hz, distance_m):
    """Calculate received power in Watts."""
    c = 299792458
    lambda_m = c / frequency_hz
    
    gt = 10**(gt_db/10)
    gr = 10**(gr_db/10)
    
    pr = pt_watts * gt * gr * (lambda_m / (4 * np.pi * distance_m))**2
    return pr

# Example: Ground Station to LEO Satellite
pt = 10  # Watts
gt = 40  # dBi
gr = 10  # dBi
freq = 2e9  # 2 GHz
dist = 1000000  # 1000 km

pr = friis_equation(pt, gt, gr, freq, dist)
pr_dbm = 10 * np.log10(pr / 0.001)

print(f"\n=== Communications Link Budget ===")
print(f"Received Power: {pr:.2e} W ({pr_dbm:.2f} dBm)")

Antenna Types
# Parabolic Dish (High gain, directional)
# Patch Antenna (Medium gain, compact)
# Monopole/Dipole (Low gain, omnidirectional)

CHAPTER 8: ADVANCED TOPICS AND RESOURCES
Interplanetary Trajectories
# Gravity Assists (Slingshot)
# Weak Stability Boundary Theory
# Low Energy Transfers

Constellation Design
# Walker Delta Pattern
# Coverage Analysis
# Inter-satellite Links

Space Debris Mitigation
# Passivation
# De-orbiting
# Active Debris Removal

Recommended Reading
# - "Fundamentals of Astrodynamics and Applications" by Vallado
# - "Spacecraft Systems Engineering" by Fortescue et al.
# - "Rocket Propulsion Elements" by Sutton
# - NASA SPICE Toolkit Documentation

# Online Resources
# - NASA Horizons System: https://ssd.jpl.nasa.gov/horizons/
# - Poliastro Documentation: https://docs.poliastro.space/
# - GMAT User Guide: https://gmat.gsfc.nasa.gov/

# End of Space Systems Engineering Reference