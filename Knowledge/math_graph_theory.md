# Graph Theory & Algorithms Reference

## Basic Concepts
- **Graph G = (V, E)**: Set of vertices V and edges E.
- **Directed vs Undirected**: Edges have direction or not.
- **Weighted Graph**: Edges have associated costs/weights.
- **Degree**: Number of edges incident to a vertex. In-degree/Out-degree for directed graphs.
- **Path**: Sequence of vertices connected by edges.
- **Cycle**: Path that starts and ends at the same vertex.
- **Connected Graph**: Path exists between any pair of vertices.

## Types of Graphs
- **Tree**: Connected acyclic graph. N vertices → N-1 edges.
- **Bipartite Graph**: Vertices divided into two sets; edges only between sets.
- **Complete Graph (K_n)**: Every pair of distinct vertices is connected.
- **Planar Graph**: Can be drawn on plane without edge crossings. Euler's Formula: V - E + F = 2.

## Traversal Algorithms
- **Breadth-First Search (BFS)**: Explores neighbors level by level. Uses queue. O(V+E). Finds shortest path in unweighted graphs.
- **Depth-First Search (DFS)**: Explores as far as possible along each branch. Uses stack/recursion. O(V+E). Detects cycles, topological sort.

## Shortest Path Algorithms
- **Dijkstra**: Non-negative weights. Greedy approach. O((V+E) log V) with priority queue.
- **Bellman-Ford**: Handles negative weights. Detects negative cycles. O(VE).
- **Floyd-Warshall**: All-pairs shortest path. Dynamic programming. O(V³).
- **A* Search**: Heuristic-based. f(n) = g(n) + h(n). Efficient for pathfinding if heuristic is admissible.

## Minimum Spanning Tree (MST)
- **Goal**: Connect all vertices with minimum total edge weight. No cycles.
- **Kruskal’s Algorithm**: Sort edges by weight. Add edge if it doesn’t form cycle (Union-Find). O(E log E).
- **Prim’s Algorithm**: Grow tree from start vertex. Add cheapest edge connecting tree to non-tree vertex. O((V+E) log V).

## Network Flow
- **Max-Flow Min-Cut Theorem**: Maximum flow equals capacity of minimum cut.
- **Ford-Fulkerson Method**: Find augmenting paths in residual graph. Increase flow. Repeat until no path.
- **Edmonds-Karp**: Implementation of Ford-Fulkerson using BFS. O(VE²).

## Graph Coloring
- **Chromatic Number χ(G)**: Minimum colors needed so no adjacent vertices share color.
- **Greedy Coloring**: Order vertices, assign smallest available color. Not always optimal.
- **Four Color Theorem**: Any planar map can be colored with ≤4 colors.

## Special Problems
- **Traveling Salesman Problem (TSP)**: Find shortest Hamiltonian cycle. NP-hard.
- **Vertex Cover**: Smallest set of vertices such that every edge is incident to at least one. NP-hard.
- **Independent Set**: Largest set of vertices with no edges between them. NP-hard.
- **Eulerian Path/Circuit**: Visits every edge exactly once. Exists if 0 or 2 vertices have odd degree.
- **Hamiltonian Path/Circuit**: Visits every vertex exactly once. NP-complete to determine existence.