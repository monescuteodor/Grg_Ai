Advanced Bio-inspired Computing Complete Reference
CHAPTER 1: GETTING STARTED WITH BIO-INSPIRED COMPUTING
Remarks
Bio-inspired computing draws inspiration from biological systems to solve complex computational problems. It includes Evolutionary Algorithms (EA), Swarm Intelligence (SI), Artificial Immune Systems (AIS), and Neural Networks. Key concepts: Natural selection, mutation, crossover, pheromone trails, self-organization, emergence. Applications: Optimization, robotics control, scheduling, pattern recognition, network routing.
Tools: Python (DEAP, PySwarms, Mesa), NetLogo, MATLAB Global Optimization Toolbox.
Hello Genetic Algorithm
# hello_ga.py
"""
First bio-inspired program: Simple Genetic Algorithm to maximize f(x) = x^2.
"""
import random

def fitness(x):
    return x ** 2

def create_population(size, bounds=(0, 10)):
    return [random.uniform(*bounds) for _ in range(size)]

def select_parents(population, fitnesses):
    # Tournament selection
    tournament_size = 3
    parents = []
    for _ in range(2):
        candidates = random.sample(list(zip(population, fitnesses)), tournament_size)
        winner = max(candidates, key=lambda c: c[1])
        parents.append(winner[0])
    return parents

def crossover(parent1, parent2):
    # Arithmetic crossover
    alpha = random.random()
    child1 = alpha * parent1 + (1 - alpha) * parent2
    child2 = alpha * parent2 + (1 - alpha) * parent1
    return child1, child2

def mutate(individual, mutation_rate=0.1, bounds=(0, 10)):
    if random.random() < mutation_rate:
        individual += random.gauss(0, 1)
        individual = max(bounds[0], min(bounds[1], individual))
    return individual

def genetic_algorithm(pop_size=50, generations=100):
    population = create_population(pop_size)
    
    for gen in range(generations):
        fitnesses = [fitness(x) for x in population]
        new_population = []
        
        for _ in range(pop_size // 2):
            p1, p2 = select_parents(population, fitnesses)
            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1)
            c2 = mutate(c2)
            new_population.extend([c1, c2])
            
        population = new_population
        best_idx = fitnesses.index(max(fitnesses))
        if gen % 20 == 0:
            print(f"Gen {gen}: Best x = {population[best_idx]:.4f}, f(x) = {max(fitnesses):.4f}")
            
    return max(population, key=fitness)

best_x = genetic_algorithm()
print(f"\nFinal Best x: {best_x:.4f}")

Evolutionary Strategies
# Focus on continuous optimization.
# Mutation is the primary operator.
# Self-adaptive step sizes.

CHAPTER 2: SWARM INTELLIGENCE
Particle Swarm Optimization (PSO)
# Simulates social behavior of birds/fish.
# Particles move through search space guided by personal best and global best.

import numpy as np

def pso(func, bounds, n_particles=30, iterations=100, w=0.7, c1=1.5, c2=1.5):
    """
    func: Objective function to minimize
    bounds: List of (min, max) for each dimension
    """
    dim = len(bounds)
    particles = np.random.uniform(
        [b[0] for b in bounds], 
        [b[1] for b in bounds], 
        (n_particles, dim)
    )
    velocities = np.random.uniform(-1, 1, (n_particles, dim))
    
    personal_best_pos = particles.copy()
    personal_best_val = np.array([func(p) for p in particles])
    
    global_best_idx = np.argmin(personal_best_val)
    global_best_pos = personal_best_pos[global_best_idx].copy()
    global_best_val = personal_best_val[global_best_idx]
    
    for i in range(iterations):
        r1, r2 = np.random.rand(n_particles, dim), np.random.rand(n_particles, dim)
        
        velocities = (w * velocities + 
                      c1 * r1 * (personal_best_pos - particles) + 
                      c2 * r2 * (global_best_pos - particles))
        
        particles += velocities
        
        # Clip to bounds
        for j, (min_b, max_b) in enumerate(bounds):
            particles[:, j] = np.clip(particles[:, j], min_b, max_b)
            
        current_vals = np.array([func(p) for p in particles])
        
        improved = current_vals < personal_best_val
        personal_best_pos[improved] = particles[improved]
        personal_best_val[improved] = current_vals[improved]
        
        best_idx = np.argmin(personal_best_val)
        if personal_best_val[best_idx] < global_best_val:
            global_best_val = personal_best_val[best_idx]
            global_best_pos = personal_best_pos[best_idx].copy()
            
    return global_best_pos, global_best_val

# Example: Minimize Sphere function
def sphere(x):
    return np.sum(np.array(x)**2)

best_pos, best_val = pso(sphere, [(-5, 5), (-5, 5)])
print(f"\nPSO Best: {best_pos}, Val: {best_val:.6f}")

Ant Colony Optimization (ACO)
# Simulates ant foraging behavior using pheromones.
# Used for combinatorial optimization (TSP, Routing).

def aco_tsp(dist_matrix, n_ants=10, n_iterations=50, alpha=1, beta=2, rho=0.5):
    """
    Solve Traveling Salesman Problem using ACO.
    dist_matrix: Distance matrix between cities.
    """
    n_cities = len(dist_matrix)
    pheromones = np.ones((n_cities, n_cities))
    
    best_path = None
    best_length = float('inf')
    
    for _ in range(n_iterations):
        paths = []
        lengths = []
        
        for _ in range(n_ants):
            path = [0] # Start at city 0
            visited = set([0])
            
            for _ in range(n_cities - 1):
                current = path[-1]
                # Calculate probabilities for next city
                probs = []
                candidates = []
                for next_city in range(n_cities):
                    if next_city not in visited:
                        tau = pheromones[current][next_city] ** alpha
                        eta = (1.0 / dist_matrix[current][next_city]) ** beta
                        probs.append(tau * eta)
                        candidates.append(next_city)
                
                probs = np.array(probs)
                probs /= probs.sum()
                
                next_city = np.random.choice(candidates, p=probs)
                path.append(next_city)
                visited.add(next_city)
                
            # Return to start
            path.append(0)
            length = sum(dist_matrix[path[i]][path[i+1]] for i in range(len(path)-1))
            
            paths.append(path)
            lengths.append(length)
            
            if length < best_length:
                best_length = length
                best_path = path[:]
                
        # Update pheromones
        pheromones *= (1 - rho) # Evaporation
        
        for path, length in zip(paths, lengths):
            deposit = 1.0 / length
            for i in range(len(path)-1):
                pheromones[path[i]][path[i+1]] += deposit
                
    return best_path, best_length

# Example TSP
cities = 5
dist = np.random.randint(1, 100, (cities, cities))
np.fill_diagonal(dist, 0)
# Make symmetric
dist = (dist + dist.T) / 2

path, length = aco_tsp(dist)
print(f"\nACO TSP Best Path: {path}, Length: {length}")

CHAPTER 3: ARTIFICIAL IMMUNE SYSTEMS
Negative Selection Algorithm
# Used for anomaly detection.
# Generate detectors that do NOT match "self" (normal data).
# Any match with "non-self" indicates an anomaly.

def generate_detectors(self_data, num_detectors=100, detector_len=8):
    """Generate random detectors that don't match self."""
    detectors = []
    for _ in range(num_detectors):
        while True:
            detector = [random.randint(0, 1) for _ in range(detector_len)]
            # Check if it matches any self string (simple Hamming distance check)
            match = False
            for self_str in self_data:
                # Simplified matching: exact match or close match
                if detector == self_str: 
                    match = True
                    break
            if not match:
                detectors.append(detector)
                break
    return detectors

def detect_anomaly(detectors, test_data):
    for detector in detectors:
        if detector == test_data:
            return True # Anomaly detected
    return False

# Example
self_strings = [[0,0,0,0], [1,1,1,1]]
detectors = generate_detectors(self_strings)
print(f"Detectors generated: {len(detectors)}")
print(f"Normal [0,0,0,0] detected as anomaly? {detect_anomaly(detectors, [0,0,0,0])}")
print(f"Anomaly [0,1,0,1] detected? {detect_anomaly(detectors, [0,1,0,1])}")

Clonal Selection Algorithm
# Simulates immune response to antigens.
# High-affinity antibodies are cloned and mutated (hypermutation).

CHAPTER 4: ARTIFICIAL LIFE
Cellular Automata
# Grid of cells with simple rules.
# Conway's Game of Life:
# 1. Underpopulation: <2 neighbors -> dies.
# 2. Survival: 2 or 3 neighbors -> lives.
# 3. Overpopulation: >3 neighbors -> dies.
# 4. Reproduction: 3 neighbors -> becomes alive.

def game_of_life_step(grid):
    new_grid = grid.copy()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            neighbors = 0
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0: continue
                    nr, nc = (r+i) % rows, (c+j) % cols
                    neighbors += grid[nr, nc]
            
            if grid[r, c] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[r, c] = 0
            else:
                if neighbors == 3:
                    new_grid[r, c] = 1
    return new_grid

# Simulation
grid = np.random.choice([0, 1], size=(10, 10), p=[0.8, 0.2])
for _ in range(5):
    grid = game_of_life_step(grid)
print("\nGame of Life Grid after 5 steps:")
print(grid)

Boids Model
# Simulates flocking behavior.
# Three rules: Separation, Alignment, Cohesion.

class Boid:
    def __init__(self, x, y):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.random.randn(2)
        self.acc = np.zeros(2)
        
    def update(self):
        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0 # Reset acceleration

def apply_rules(boids):
    for boid in boids:
        separation = np.zeros(2)
        alignment = np.zeros(2)
        cohesion = np.zeros(2)
        count = 0
        
        for other in boids:
            if other is boid: continue
            dist = np.linalg.norm(boid.pos - other.pos)
            if dist < 5.0: # Perception radius
                separation += boid.pos - other.pos
                alignment += other.vel
                cohesion += other.pos
                count += 1
                
        if count > 0:
            separation /= count
            alignment /= count
            cohesion = (cohesion / count) - boid.pos
            
            boid.acc += separation * 1.5
            boid.acc += alignment * 1.0
            boid.acc += cohesion * 1.0

# Simulation setup
boids = [Boid(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(20)]
for _ in range(10):
    apply_rules(boids)
    for b in boids:
        b.update()
print(f"\nBoids final positions: {boids[0].pos}")

CHAPTER 5: ADVANCED TOPICS AND RESOURCES
Memetic Algorithms
# Hybrid of Genetic Algorithms and Local Search.
# Individuals undergo "cultural evolution" (learning) before reproduction.

Artificial Chemistries
# Simulates chemical reactions in silico.
# Used for studying origin of life, self-replication.

Neuromorphic Hardware
# Hardware that mimics brain structure (spiking neurons).
# Low power, event-driven processing.

Recommended Reading
# - "Evolutionary Computation: A Unified Approach" by Kenneth De Jong
# - "Swarm Intelligence" by Kennedy and Eberhart
# - "Artificial Life: A Report on the Discipline" by Langton
# - DEAP Documentation: https://deap.readthedocs.io/

# End of Bio-inspired Computing Reference