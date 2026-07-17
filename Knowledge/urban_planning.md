Urban Planning & Smart Cities Complete Reference
CHAPTER 1: GETTING STARTED WITH URBAN PLANNING SIMULATION
Remarks
Urban planning involves the design and regulation of the use of space that focuses on the physical form, economic functions, and social impacts of the urban environment. Smart Cities leverage IoT, data analytics, and AI to optimize infrastructure, reduce energy consumption, and improve quality of life. Key areas: Traffic flow optimization, resource distribution (water, electricity), waste management, public transport scheduling, and emergency response.
Tools: Python (NumPy, Pandas, NetworkX), SUMO (Simulation of Urban MObility), AnyLogic, GIS tools (QGIS), MATLAB.
Hello Smart City
# hello_city.py
"""
First simulation: Simple grid-based city with traffic lights.
"""
import numpy as np
import random

class CityGrid:
    def __init__(self, size=10):
        self.size = size
        # 0: Empty, 1: Building, 2: Road, 3: Traffic Light
        self.grid = np.zeros((size, size), dtype=int)
        self.cars = []
        
    def add_road(self, x1, y1, x2, y2):
        """Add a horizontal or vertical road."""
        if x1 == x2: # Vertical
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.grid[x1, y] = 2
        elif y1 == y2: # Horizontal
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.grid[x, y1] = 2
                
    def add_traffic_light(self, x, y):
        if self.grid[x, y] == 2:
            self.grid[x, y] = 3
            
    def spawn_car(self):
        """Spawn a car at a random road location."""
        roads = np.argwhere(self.grid == 2)
        if len(roads[0]) > 0:
            idx = random.randint(0, len(roads[0]) - 1)
            x, y = roads[0][idx], roads[1][idx]
            self.cars.append({'x': x, 'y': y, 'moved': False})
            
    def step(self):
        """Simulate one time step."""
        for car in self.cars:
            car['moved'] = False
            # Simple random movement logic
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = car['x'] + dx, car['y'] + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    cell = self.grid[nx, ny]
                    if cell == 2: # Road
                        car['x'], car['y'] = nx, ny
                        car['moved'] = True
                        break
                    elif cell == 3: # Traffic Light (50% chance to stop)
                        if random.random() > 0.5:
                            car['x'], car['y'] = nx, ny
                            car['moved'] = True
                            break

# Simulation
city = CityGrid(10)
city.add_road(5, 0, 5, 9) # Vertical main street
city.add_road(0, 5, 9, 5) # Horizontal main street
city.add_traffic_light(5, 5)

for _ in range(10):
    city.spawn_car()

print("Initial Cars:", len(city.cars))
city.step()
print("Cars after 1 step:", len([c for c in city.cars if c['moved']]))

CHAPTER 2: TRAFFIC FLOW OPTIMIZATION
Cellular Automata for Traffic
# Nagel-Schreckenberg model:
# 1. Acceleration: v -> min(v+1, v_max)
# 2. Slowing down: v -> min(v, gap)
# 3. Randomization: v -> max(v-1, 0) with probability p
# 4. Movement: x -> x + v

def nagel_schreckenberg(L=100, N=20, v_max=5, p=0.3, steps=100):
    """Simulate single-lane traffic flow."""
    # Initialize positions and velocities
    positions = sorted(random.sample(range(L), N))
    velocities = [0] * N
    
    flow_data = []
    
    for t in range(steps):
        new_velocities = []
        new_positions = []
        
        for i in range(N):
            v = velocities[i]
            x = positions[i]
            
            # Find next car ahead
            next_idx = (i + 1) % N
            gap = (positions[next_idx] - x - 1) % L
            
            # 1. Acceleration
            v = min(v + 1, v_max)
            
            # 2. Slowing down
            v = min(v, gap)
            
            # 3. Randomization
            if v > 0 and random.random() < p:
                v -= 1
                
            # 4. Movement
            new_x = (x + v) % L
            new_positions.append(new_x)
            new_velocities.append(v)
            
        positions = new_positions
        velocities = new_velocities
        
        # Calculate flow (cars passing a point per time step)
        flow = sum(1 for v in velocities if v > 0) / L
        flow_data.append(flow)
        
    return np.mean(flow_data)

avg_flow = nagel_schreckenberg()
print(f"Average Traffic Flow: {avg_flow:.4f}")

Green Wave Optimization
# Coordinating traffic lights to allow continuous flow.
# Speed = Distance between lights / Cycle time

def calculate_green_wave_speed(distance_meters, cycle_time_seconds):
    """Calculate optimal speed for green wave."""
    return (distance_meters / cycle_time_seconds) * 3.6 # km/h

speed = calculate_green_wave_speed(500, 60)
print(f"Optimal Green Wave Speed: {speed:.1f} km/h")

CHAPTER 3: RESOURCE DISTRIBUTION
Water Network Analysis
# Graph theory for pipe networks.
# Nodes: Junctions, Tanks. Edges: Pipes.
# Constraints: Pressure limits, flow conservation.

import networkx as nx

def analyze_water_network():
    G = nx.DiGraph()
    
    # Add nodes (Junctions)
    G.add_node('Source', type='tank')
    G.add_node('J1', type='junction')
    G.add_node('J2', type='junction')
    G.add_node('Demand1', type='demand')
    
    # Add edges (Pipes) with capacity
    G.add_edge('Source', 'J1', capacity=100, length=50)
    G.add_edge('J1', 'J2', capacity=80, length=30)
    G.add_edge('J1', 'Demand1', capacity=50, length=20)
    G.add_edge('J2', 'Demand1', capacity=60, length=40)
    
    # Max flow from Source to Demand1
    flow_value, flow_dict = nx.maximum_flow(G, 'Source', 'Demand1')
    
    print(f"Max Water Flow: {flow_value} units")
    print("Flow Distribution:", flow_dict)

analyze_water_network()

Power Grid Load Balancing
# Distributing electrical load across substations.
# Objective: Minimize loss, prevent overload.

def balance_load(substations, total_demand):
    """Simple proportional load balancing."""
    capacities = [s['capacity'] for s in substations]
    total_cap = sum(capacities)
    
    if total_demand > total_cap:
        print("WARNING: Demand exceeds capacity!")
        return None
        
    loads = []
    for s in substations:
        share = s['capacity'] / total_cap
        load = total_demand * share
        loads.append(load)
        
    return loads

subs = [
    {'id': 'A', 'capacity': 100},
    {'id': 'B', 'capacity': 200},
    {'id': 'C', 'capacity': 150}
]

loads = balance_load(subs, 300)
if loads:
    for s, l in zip(subs, loads):
        print(f"Substation {s['id']}: {l:.1f} MW")

CHAPTER 4: WASTE MANAGEMENT OPTIMIZATION
Vehicle Routing Problem (VRP)
# Optimizing garbage truck routes.
# Minimize distance/time while visiting all bins.

def solve_vrp(locations, depot):
    """Nearest Neighbor heuristic for VRP."""
    unvisited = locations[:]
    route = [depot]
    current = depot
    
    while unvisited:
        nearest = min(unvisited, key=lambda loc: np.linalg.norm(np.array(loc) - np.array(current)))
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest
        
    route.append(depot) # Return to depot
    return route

bins = [(1, 2), (3, 4), (5, 1), (2, 5)]
depot = (0, 0)
route = solve_vrp(bins, depot)
print(f"Optimized Route: {route}")

Smart Bins
# IoT sensors detect fill level.
# Dynamic routing: Only visit bins that are >80% full.

def dynamic_routing(bins_status):
    """Filter bins needing collection."""
    urgent_bins = [loc for loc, status in bins_status.items() if status > 80]
    return urgent_bins

status = {'Bin1': 90, 'Bin2': 40, 'Bin3': 85}
urgent = dynamic_routing(status)
print(f"Urgent Collections: {urgent}")

CHAPTER 5: PUBLIC TRANSPORT SCHEDULING
Bus Frequency Optimization
# Balance waiting time vs. operational cost.
# Formula: Frequency = Demand / Capacity

def optimize_frequency(passengers_per_hour, bus_capacity):
    buses_needed = passengers_per_hour / bus_capacity
    interval_minutes = 60 / buses_needed
    return interval_minutes

freq = optimize_frequency(1200, 60)
print(f"Optimal Bus Interval: {freq:.1f} minutes")

Real-time Arrival Prediction
# Using GPS data and historical traffic patterns.
# Kalman Filter for state estimation.

def predict_arrival(current_pos, target_pos, avg_speed, traffic_factor):
    distance = np.linalg.norm(np.array(target_pos) - np.array(current_pos))
    time_hours = distance / (avg_speed * traffic_factor)
    return time_hours * 60 # minutes

eta = predict_arrival((1, 1), (10, 10), 30, 0.8)
print(f"Estimated Arrival: {eta:.1f} minutes")

CHAPTER 6: EMERGENCY RESPONSE SIMULATION
Facility Location Problem
# Where to place fire stations/hospitals to minimize response time.
# p-Median Problem.

def place_facilities(nodes, p=2):
    """Greedy algorithm for facility location."""
    facilities = []
    covered = set()
    
    # Simplified: Pick nodes with highest degree/connectivity
    # In real scenario, use integer linear programming
    for _ in range(p):
        best_node = max(nodes, key=lambda n: n['connectivity'])
        facilities.append(best_node['id'])
        nodes.remove(best_node)
        
    return facilities

nodes = [
    {'id': 'A', 'connectivity': 5},
    {'id': 'B', 'connectivity': 8},
    {'id': 'C', 'connectivity': 3},
    {'id': 'D', 'connectivity': 6}
]

stations = place_facilities(nodes[:], p=2)
print(f"Fire Stations at: {stations}")

Evacuation Modeling
# Simulating crowd movement during emergencies.
# Social Force Model: Pedestrians repel each other and obstacles.

CHAPTER 7: ENVIRONMENTAL MONITORING
Air Quality Index (AQI) Calculation
# Combining pollutants: PM2.5, PM10, O3, NO2, SO2, CO.

def calculate_aqi(pm25):
    """Simplified AQI based on PM2.5."""
    if pm25 <= 12:
        return 50 # Good
    elif pm25 <= 35:
        return 100 # Moderate
    elif pm25 <= 55:
        return 150 # Unhealthy for Sensitive Groups
    else:
        return 200 # Unhealthy

aqi = calculate_aqi(40)
print(f"AQI: {aqi}")

Noise Pollution Mapping
# Interpolating sound levels from sensor data.
# Inverse Distance Weighting (IDW).

def idw_interpolation(points, values, target, power=2):
    """Interpolate value at target location."""
    numerator = 0
    denominator = 0
    for p, v in zip(points, values):
        dist = np.linalg.norm(np.array(target) - np.array(p))
        if dist == 0: return v
        weight = 1 / dist**power
        numerator += weight * v
        denominator += weight
    return numerator / denominator

sensors = [(0,0), (10,0), (0,10)]
noise_levels = [60, 70, 65] # dB
target_noise = idw_interpolation(sensors, noise_levels, (5, 5))
print(f"Estimated Noise at (5,5): {target_noise:.1f} dB")

CHAPTER 8: ADVANCED TOPICS AND RESOURCES
Digital Twins
# Virtual replica of physical city.
# Real-time data synchronization.
# Used for testing policies before implementation.

Citizen Engagement Platforms
# Apps for reporting issues (potholes, broken lights).
# Participatory budgeting.

Privacy in Smart Cities
# Anonymizing data from cameras and sensors.
# GDPR compliance.
# Edge computing to process data locally.

Recommended Reading
# - "Smart Cities: Big Data, Civic Hackers, and the Quest for a New Utopia" by Anthony Townsend
# - "Urban Analytics" by Singleton et al.
# - SUMO Documentation: https://sumo.dlr.de/
# - NetworkX Documentation: https://networkx.org/

# End of Urban Planning & Smart Cities Reference