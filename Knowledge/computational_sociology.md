Computational Sociology & Social Simulation Complete Reference
CHAPTER 1: GETTING STARTED WITH COMPUTATIONAL SOCIOLOGY
Remarks
Computational sociology uses computer simulations, artificial intelligence, complex statistical methods, and social network analysis to study social phenomena. It bridges sociology, computer science, and physics. Key areas: Agent-Based Modeling (ABM), Social Network Analysis (SNA), Opinion Dynamics, Cultural Evolution, and Collective Behavior. Applications: Policy making, urban planning, epidemic control, marketing, understanding polarization.
Tools: Python (NetworkX, Mesa, NumPy, Matplotlib), NetLogo, GAMA Platform, R (statnet).
Hello Agent-Based Modeling
# hello_sociology.py
"""
First computational sociology program: Simple Schelling Segregation Model.
"""
import numpy as np
import matplotlib.pyplot as plt
import random

class SchellingAgent:
    def __init__(self, agent_type, x, y):
        self.type = agent_type  # 0 or 1
        self.x = x
        self.y = y
        self.happy = False

def schelling_model(grid_size=30, empty_ratio=0.2, similarity_threshold=0.4, iterations=50):
    # Initialize grid
    grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    agents = []
    
    num_agents = int(grid_size * grid_size * (1 - empty_ratio))
    for _ in range(num_agents):
        while True:
            x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
            if grid[x][y] is None:
                agent = SchellingAgent(random.choice([0, 1]), x, y)
                grid[x][y] = agent
                agents.append(agent)
                break
    
    history = []
    
    for iteration in range(iterations):
        unhappy_agents = []
        for agent in agents:
            similar = 0
            total = 0
            for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                nx, ny = agent.x + dx, agent.y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size and grid[nx][ny] is not None:
                    total += 1
                    if grid[nx][ny].type == agent.type:
                        similar += 1
            
            if total > 0 and similar / total >= similarity_threshold:
                agent.happy = True
            else:
                agent.happy = False
                unhappy_agents.append(agent)
        
        # Move unhappy agents
        for agent in unhappy_agents:
            grid[agent.x][agent.y] = None
            while True:
                x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
                if grid[x][y] is None:
                    agent.x, agent.y = x, y
                    grid[x][y] = agent
                    break
        
        # Calculate segregation index (average % of similar neighbors)
        total_similar = 0
        total_neighbors = 0
        for agent in agents:
            similar = 0
            total = 0
            for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                nx, ny = agent.x + dx, agent.y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size and grid[nx][ny] is not None:
                    total += 1
                    if grid[nx][ny].type == agent.type:
                        similar += 1
            if total > 0:
                total_similar += similar / total
                total_neighbors += 1
        
        avg_similarity = total_similar / total_neighbors if total_neighbors > 0 else 0
        history.append(avg_similarity)
        
    return grid, history

grid, history = schelling_model()

# Visualize final state
vis_grid = np.zeros((30, 30))
for i in range(30):
    for j in range(30):
        if grid[i][j] is not None:
            vis_grid[i][j] = grid[i][j].type + 1

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.imshow(vis_grid, cmap='viridis')
plt.title("Final Segregation State")
plt.colorbar(ticks=[1, 2], label='Agent Type')

plt.subplot(1, 2, 2)
plt.plot(history)
plt.title("Segregation Index Over Time")
plt.xlabel("Iteration")
plt.ylabel("Average Similarity")
plt.grid(True)
plt.tight_layout()
plt.show()

Key Concepts in Computational Sociology
# Emergence: Complex patterns arising from simple individual rules.
# Self-Organization: System organizes itself without central control.
# Tipping Points: Small changes leading to large systemic shifts.
# Homophily: "Birds of a feather flock together."
# Social Contagion: Spread of behaviors/ideas like diseases.

CHAPTER 2: SOCIAL NETWORK ANALYSIS (SNA)
Metrics
# Degree Centrality: Number of connections.
# Betweenness Centrality: Importance as a bridge.
# Closeness Centrality: Proximity to all other nodes.
# Eigenvector Centrality: Connected to important nodes.
# Clustering Coefficient: How connected neighbors are to each other.

Community Detection
# Louvain Algorithm: Maximizes modularity.
# Girvan-Newman: Removes edges with highest betweenness.
# Label Propagation: Fast, heuristic-based.

Diffusion Models
# Independent Cascade: Each node has one chance to infect neighbors.
# Linear Threshold: Node activates if fraction of active neighbors exceeds threshold.
# SIR/SIS: Epidemiological models applied to information spread.

CHAPTER 3: OPINION DYNAMICS
Voter Model
# Binary opinions. Randomly pick a node and copy a neighbor's opinion.
# Leads to consensus in finite networks.

Sznajdowski Model
# Unanimity rule: If two neighbors agree, they convince their neighbors.
# Can lead to polarization or consensus depending on initial conditions.

Bounded Confidence Model (Deffuant)
# Continuous opinions [-1, 1].
# Interaction only if |opinion_i - opinion_j| < epsilon.
# Leads to fragmentation if epsilon is small.

Axelrod's Cultural Model
# Multi-feature culture.
# Interaction increases similarity.
# Can lead to stable cultural regions.

CHAPTER 4: AGENT-BASED MODELING FRAMEWORKS
Mesa (Python)
# Modular ABM framework.
# Agents, Model, Scheduler, DataCollector.
# Web-based visualization.

NetLogo
# Logo-based language for ABM.
# Great for education and quick prototyping.
# Large library of existing models.

GAMA Platform
# GIS-integrated ABM.
# Good for spatially explicit models.

CHAPTER 5: DATA-DRIVEN SOCIOLOGY
Digital Traces
# Social media data, mobile phone records, credit card transactions.
# Privacy concerns: Anonymization, differential privacy.

Natural Language Processing
# Sentiment analysis of social media.
# Topic modeling for public discourse.
# Detecting bots and fake news.

Machine Learning
# Predicting social outcomes (crime, poverty, health).
# Bias in algorithms: Reinforcing existing inequalities.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Evolutionary Game Theory
# Prisoner's Dilemma, Hawk-Dove, Public Goods Game.
# Strategy evolution in populations.
# Replicator dynamics.

Urban Simulation
# Traffic flow, land use change, gentrification.
# Coupling ABM with GIS.

Policy Making
# Testing policies in silico before implementation.
# "What-if" scenarios for economic sanctions, tax changes, etc.

Recommended Reading
# - "Introduction to Computational Social Science" by Miller and Page
# - "Networks, Crowds, and Markets" by Easley and Kleinberg
# - "Agent-Based and Individual-Based Modeling" by Railsback and Lytinen
# - Mesa Documentation: https://mesa.readthedocs.io/
# - NetLogo Modeling Commons: https://ccl.northwestern.edu/netlogo/models/

# End of Computational Sociology Reference