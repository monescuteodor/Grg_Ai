Computational Social Science & Network Analysis Complete Reference
CHAPTER 1: GETTING STARTED WITH COMPUTATIONAL SOCIAL SCIENCE
Remarks
Computational Social Science (CSS) uses computational methods to study social phenomena. It combines sociology, psychology, economics, and computer science to analyze large-scale social data. Key areas: Social Network Analysis (SNA), Opinion Dynamics, Agent-Based Modeling (ABM), Sentiment Analysis, Cultural Analytics. Applications: Viral marketing, political polarization, disease spread modeling, community detection, recommendation systems.
Tools: Python (NetworkX, Gephi, Pandas, Matplotlib), R (igraph, statnet), NodeXL, UCINET.
Hello Social Networks
# hello_social.py
"""
First CSS program: Create a simple social network and calculate basic metrics.
"""
import networkx as nx
import matplotlib.pyplot as plt

# Create a graph
G = nx.Graph()

# Add nodes (people)
G.add_nodes_from(["Alice", "Bob", "Charlie", "David", "Eve", "Frank"])

# Add edges (friendships)
G.add_edges_from([
    ("Alice", "Bob"),
    ("Alice", "Charlie"),
    ("Bob", "Charlie"),
    ("Bob", "David"),
    ("Charlie", "Eve"),
    ("David", "Eve"),
    ("Eve", "Frank")
])

# Basic metrics
print("=== Social Network Metrics ===")
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")
print(f"Average degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
print(f"Density: {nx.density(G):.2f}")

# Visualize
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue', 
        node_size=1000, font_size=10, font_weight='bold')
plt.title("Simple Social Network")
plt.show()

Centrality Measures
# Degree Centrality: Number of connections. Popularity.
# Betweenness Centrality: How often a node lies on shortest paths. Bridge/Connector.
# Closeness Centrality: Average distance to all other nodes. Information spreader.
# Eigenvector Centrality: Connected to well-connected nodes. Influence.

def analyze_centrality(G):
    degree_cent = nx.degree_centrality(G)
    betweenness_cent = nx.betweenness_centrality(G)
    closeness_cent = nx.closeness_centrality(G)
    eigenvector_cent = nx.eigenvector_centrality(G, max_iter=1000)
    
    print("\n=== Centrality Analysis ===")
    for node in G.nodes():
        print(f"{node:10s}: Deg={degree_cent[node]:.2f}, Bet={betweenness_cent[node]:.2f}, Clo={closeness_cent[node]:.2f}, Eig={eigenvector_cent[node]:.2f}")

analyze_centrality(G)

CHAPTER 2: COMMUNITY DETECTION
Modularity and Clustering
# Communities: Groups of nodes densely connected internally, sparsely connected externally.
# Modularity (Q): Measure of structure quality. Q > 0 indicates community structure.

from community import community_louvain

# Louvain Algorithm: Greedy optimization of modularity.
partition = community_louvain.best_partition(G)
modularity = community_louvain.modularity(partition, G)

print(f"\n=== Community Detection (Louvain) ===")
print(f"Modularity: {modularity:.3f}")
print("Communities:")
communities = {}
for node, comm_id in partition.items():
    if comm_id not in communities:
        communities[comm_id] = []
    communities[comm_id].append(node)

for comm_id, members in communities.items():
    print(f"  Community {comm_id}: {members}")

# Visualize communities
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42)
colors = [partition[node] for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=colors, 
        node_size=1000, font_size=10, cmap=plt.cm.Set3)
plt.title("Community Structure")
plt.show()

Other Algorithms
# Girvan-Newman: Edge betweenness-based divisive algorithm.
# Label Propagation: Fast, near-linear time.
# Clique Percolation: Overlapping communities.

CHAPTER 3: OPINION DYNAMICS
Voter Model
# Simple model of opinion change.
# Each agent has an opinion (0 or 1).
# At each step, a random agent adopts the opinion of a random neighbor.

def voter_model(G, initial_opinions, steps=100):
    opinions = initial_opinions.copy()
    history = [sum(opinions.values()) / len(opinions)]  # Fraction of 1s
    
    for _ in range(steps):
        node = random.choice(list(G.nodes()))
        neighbors = list(G.neighbors(node))
        if neighbors:
            neighbor = random.choice(neighbors)
            opinions[node] = opinions[neighbor]
        
        history.append(sum(opinions.values()) / len(opinions))
        
    return history

# Example
initial_opinions = {node: random.choice([0, 1]) for node in G.nodes()}
history = voter_model(G, initial_opinions)

plt.plot(history)
plt.title("Voter Model: Opinion Consensus")
plt.xlabel("Time Step")
plt.ylabel("Fraction of Opinion 1")
plt.grid(True)
plt.show()

Sznajdowski Model (Deffuant)
# Continuous opinions [-1, 1].
# Interaction only if opinions are close enough (bounded confidence).
# Can lead to polarization or consensus.

def sznajdowski_model(G, initial_opinions, epsilon=0.5, steps=100):
    opinions = initial_opinions.copy()
    history = [list(opinions.values())]
    
    for _ in range(steps):
        edge = random.choice(list(G.edges()))
        u, v = edge
        
        if abs(opinions[u] - opinions[v]) < epsilon:
            avg = (opinions[u] + opinions[v]) / 2
            opinions[u] = avg
            opinions[v] = avg
            
        history.append(list(opinions.values()))
        
    return opinions, history

# Example
initial_opinions_cont = {node: random.uniform(-1, 1) for node in G.nodes()}
final_opinions, hist = sznajdowski_model(G, initial_opinions_cont, epsilon=0.3)
print(f"Final Opinions: {final_opinions}")

CHAPTER 4: AGENT-BASED MODELING (ABM)
Schelling's Segregation Model
# Agents have a preference for similar neighbors.
# Even mild preference leads to high segregation.

class SchellingAgent:
    def __init__(self, agent_type, x, y):
        self.type = agent_type  # 0 or 1
        self.x = x
        self.y = y
        self.happy = False

def schelling_model(grid_size=20, empty_ratio=0.2, similarity_threshold=0.3, iterations=50):
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
                    
    return grid

# Run model
grid = schelling_model(grid_size=30, similarity_threshold=0.4)

# Visualize
import numpy as np
vis_grid = np.zeros((30, 30))
for i in range(30):
    for j in range(30):
        if grid[i][j] is not None:
            vis_grid[i][j] = grid[i][j].type + 1  # 1 or 2

plt.imshow(vis_grid, cmap='viridis')
plt.title("Schelling's Segregation Model")
plt.colorbar(ticks=[1, 2], label='Agent Type')
plt.show()

CHAPTER 5: INFORMATION DIFFUSION
Epidemic Models on Networks
# SIR Model: Susceptible -> Infected -> Recovered.
# Used for disease spread, viral marketing, rumor spreading.

def sir_model_on_network(G, beta=0.3, gamma=0.1, steps=100):
    """Simulate SIR epidemic on a network."""
    status = {node: 'S' for node in G.nodes()}
    # Start with one infected node
    start_node = random.choice(list(G.nodes()))
    status[start_node] = 'I'
    
    history = {'S': [], 'I': [], 'R': []}
    
    for _ in range(steps):
        s_count = sum(1 for s in status.values() if s == 'S')
        i_count = sum(1 for s in status.values() if s == 'I')
        r_count = sum(1 for s in status.values() if s == 'R')
        
        history['S'].append(s_count)
        history['I'].append(i_count)
        history['R'].append(r_count)
        
        new_status = status.copy()
        for node in G.nodes():
            if status[node] == 'I':
                # Infect neighbors
                for neighbor in G.neighbors(node):
                    if status[neighbor] == 'S' and random.random() < beta:
                        new_status[neighbor] = 'I'
                # Recover
                if random.random() < gamma:
                    new_status[node] = 'R'
                    
        status = new_status
        
    return history

# Example
history_sir = sir_model_on_network(G, beta=0.5, gamma=0.2)

plt.plot(history_sir['S'], label='Susceptible')
plt.plot(history_sir['I'], label='Infected')
plt.plot(history_sir['R'], label='Recovered')
plt.title("SIR Model on Social Network")
plt.xlabel("Time Step")
plt.ylabel("Count")
plt.legend()
plt.grid(True)
plt.show()

Independent Cascade Model
# For information/viral spread.
# Each infected node has one chance to infect each neighbor.

CHAPTER 6: SENTIMENT ANALYSIS & TEXT MINING
Social Media Analysis
# Collecting tweets/posts.
# Preprocessing: Tokenization, Stopword removal, Lemmatization.
# Sentiment Scoring: VADER, TextBlob, BERT.

from textblob import TextBlob

def analyze_sentiment(texts):
    sentiments = []
    for text in texts:
        blob = TextBlob(text)
        sentiments.append(blob.sentiment.polarity)  # -1 to 1
    return sentiments

posts = [
    "I love this new product!",
    "This is terrible service.",
    "It's okay, nothing special.",
    "Amazing experience, highly recommend!",
    "Waste of money."
]

scores = analyze_sentiment(posts)
for post, score in zip(posts, scores):
    print(f"{post:40s}: {score:.2f}")

Topic Modeling (LDA)
# Latent Dirichlet Allocation: Discover abstract topics in document collection.
# Used for trend detection, content categorization.

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def topic_modeling(documents, n_topics=2):
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    dtm = vectorizer.fit_transform(documents)
    
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)
    
    feature_names = vectorizer.get_feature_names_out()
    
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-5:-1]]
        print(f"Topic {topic_idx}: {', '.join(top_words)}")

docs = [
    "Python is great for data science and machine learning",
    "JavaScript is used for web development and frontend",
    "Deep learning requires lots of data and GPU power",
    "React and Vue are popular frontend frameworks",
    "Natural language processing uses transformers and attention"
]

print("\n=== Topic Modeling ===")
topic_modeling(docs)

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Causal Inference in Social Science
# Correlation vs Causation.
# Methods: Propensity Score Matching, Instrumental Variables, Difference-in-Differences.
# Libraries: DoWhy, CausalML.

Ethical Considerations
# Privacy: Anonymization, Differential Privacy.
# Bias: Algorithmic bias in hiring, lending, policing.
# Consent: Data collection from social media.

Big Data Challenges
# Scalability: Graph databases (Neo4j), Distributed computing (Spark).
# Real-time analysis: Streaming data (Kafka, Flink).

Recommended Reading
# - "Networks, Crowds, and Markets" by Easley and Kleinberg
# - "Social Physics" by Alex Pentland
# - "Agent-Based and Individual-Based Modeling" by Railsback and Lytinen
# - NetworkX Documentation: https://networkx.org/
# - Gephi: https://gephi.org/

# End of Computational Social Science Reference