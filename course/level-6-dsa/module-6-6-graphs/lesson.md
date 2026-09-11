# Module 6.6 — Graphs: BFS, DFS, Dijkstra, A*

---

## The Problem

> A road network. A social network. The internet. A circuit board. A gene regulatory network.
> All of these are the same mathematical object: a **graph**.
>
> How do you find the shortest route from A to B in a city with 10,000 intersections?
> How does Google find the shortest degree of separation between two people?
> How does a GPS recalculate a route in real time?
>
> These all reduce to graph search problems — and understanding them
> means understanding the structure of almost every networked system ever built.

---

## The Story

### Leonhard Euler and the Bridges of Königsberg

In 1736, Leonhard Euler solved the first graph theory problem: is it possible to walk through Königsberg (now Kaliningrad, Russia) crossing each of its seven bridges exactly once? He proved it was impossible by abstraction: replace land masses with nodes, bridges with edges. The problem reduces to whether an **Eulerian path** exists — which requires at most two nodes of odd degree. Königsberg had four nodes of odd degree: impossible.

This was the birth of graph theory, 200 years before computers.

**Edsger Dijkstra** invented his shortest-path algorithm in 1956, reportedly in 20 minutes while sitting in a café in Amsterdam, without pen and paper. He was designing software for the first Dutch computer (ARMAC) and needed a test program. The algorithm he invented became one of the most widely used in computer science.

**Peter Hart, Nils Nilsson, and Bertram Raphael** invented A* at Stanford Research Institute in 1968, as part of the Shakey robot project — a robot that needed to navigate a room. A* added a heuristic to Dijkstra's algorithm to guide the search toward the goal, dramatically reducing unnecessary exploration.

---

## The Concept

### Graph Representation

**Adjacency List** (preferred for sparse graphs):
```python
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}
```
Space: O(V + E). Checking if edge (u,v) exists: O(degree(u)).

**Adjacency Matrix** (preferred for dense graphs):
```python
# n×n matrix where matrix[i][j] = 1 if edge exists
matrix = [
    [0, 1, 1, 0, 0, 0],  # A
    [1, 0, 0, 1, 1, 0],  # B
    ...
]
```
Space: O(V²). Checking edge existence: O(1).

### Breadth-First Search (BFS)

Explores all neighbours of a node before moving to their neighbours. Uses a **queue**. Finds the **shortest path** (fewest edges) in an unweighted graph.

```python
from collections import deque

def bfs(graph, start):
    visited = {start: None}    # node → parent (for path reconstruction)
    queue   = deque([start])
    while queue:
        node = queue.popleft()
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited[neighbour] = node
                queue.append(neighbour)
    return visited

def shortest_path(graph, start, end):
    visited = bfs(graph, start)
    if end not in visited: return None
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = visited[node]
    return list(reversed(path))
```

**Time**: O(V + E). **Space**: O(V). Guarantees shortest path in unweighted graphs.

### Depth-First Search (DFS)

Goes as deep as possible before backtracking. Uses a **stack** (or recursion). Finds connected components, detects cycles, produces topological orderings.

```python
def dfs_recursive(graph, node, visited=None):
    if visited is None: visited = set()
    visited.add(node)
    for neighbour in graph[node]:
        if neighbour not in visited:
            dfs_recursive(graph, neighbour, visited)
    return visited

def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbour in graph[node]:
                if neighbour not in visited:
                    stack.append(neighbour)
    return visited
```

**Applications of DFS**:
- **Cycle detection**: if DFS encounters a grey (in-progress) node, there's a cycle
- **Topological sort**: DFS-based, used in build systems (make, Gradle)
- **Connected components**: run DFS from each unvisited node
- **Maze solving**: DFS finds *a* path (not necessarily shortest)

### Dijkstra's Shortest Path

For **weighted graphs** (each edge has a cost/distance). Generalises BFS using a **priority queue** instead of a plain queue — always expand the unvisited node with the smallest known distance.

```python
import heapq

def dijkstra(graph_weighted, start):
    # graph_weighted: {node: [(neighbour, weight), ...]}
    dist = {start: 0}
    pq   = [(0, start)]        # (distance, node)
    while pq:
        d, node = heapq.heappop(pq)
        if d > dist.get(node, float('inf')):
            continue           # stale entry
        for neighbour, weight in graph_weighted[node]:
            new_dist = dist[node] + weight
            if new_dist < dist.get(neighbour, float('inf')):
                dist[neighbour] = new_dist
                heapq.heappush(pq, (new_dist, neighbour))
    return dist
```

**Time**: O((V + E) log V) with a binary heap.  
**Correctness**: only works on graphs with **non-negative edge weights**. Negative weights require Bellman-Ford.

### A* Search

Dijkstra explores in all directions equally — expanding the cheapest frontier node regardless of direction. A* adds a **heuristic** h(n) estimating the cost from n to the goal:

```
f(n) = g(n) + h(n)
```
where g(n) = actual cost from start to n, h(n) = estimated cost from n to goal.

If h(n) is **admissible** (never overestimates the true cost), A* always finds the optimal path while exploring fewer nodes than Dijkstra.

```python
def astar(graph, start, goal, heuristic):
    pq = [(heuristic(start, goal), 0, start)]
    g  = {start: 0}
    while pq:
        f, cost, node = heapq.heappop(pq)
        if node == goal:
            return cost
        if cost > g.get(node, float('inf')):
            continue
        for neighbour, weight in graph[node]:
            new_g = g[node] + weight
            if new_g < g.get(neighbour, float('inf')):
                g[neighbour] = new_g
                f_score = new_g + heuristic(neighbour, goal)
                heapq.heappush(pq, (f_score, new_g, neighbour))
    return float('inf')   # no path found
```

**GPS navigation**: heuristic = straight-line distance to destination (Euclidean or haversine). Nodes = road intersections. Edges = road segments with travel time as weight.

### Algorithm Comparison

| Algorithm | Graph type | Guarantee | Time | When to use |
|---|---|---|---|---|
| BFS | Unweighted | Shortest (by edges) | O(V+E) | Unweighted shortest path, level-order |
| DFS | Any | Finds path (not shortest) | O(V+E) | Cycle detection, topological sort, components |
| Dijkstra | Weighted ≥0 | Shortest (by weight) | O((V+E)log V) | Weighted shortest path |
| A* | Weighted ≥0 | Shortest (with heuristic) | O((V+E)log V) | Goal-directed search, navigation |
| Bellman-Ford | Any weights | Shortest, detects neg cycles | O(VE) | Negative weights |
| Floyd-Warshall | Any weights | All-pairs shortest paths | O(V³) | Small dense graphs |

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — BFS vs DFS Visualiser**
- A graph with 10–12 nodes on screen
- Run BFS and DFS from the same start node
- Watch nodes change colour as they are discovered
- Compare the order of discovery between the two algorithms

**Tool 2 — Dijkstra Step-by-Step**
- A weighted graph (road network style)
- Step through Dijkstra: see the priority queue, distances updating, nodes being settled
- Reconstruct the shortest path at the end

**Tool 3 — A* vs Dijkstra**
- A grid graph (like a map)
- Run Dijkstra and A* side by side
- Compare the number of nodes explored — A* explores far fewer with a good heuristic

---

## Going Deeper

**Topological sort**: for a directed acyclic graph (DAG), produce an ordering of nodes such that every edge goes from earlier to later in the order. Used in build systems (compile A before B because B depends on A), course prerequisite planning, and spreadsheet formula evaluation. Two algorithms: Kahn's (BFS-based) and DFS postorder (DFS-based).

**Strongly connected components (SCCs)**: in a directed graph, an SCC is a maximal set of nodes where every node is reachable from every other. Tarjan's algorithm and Kosaraju's algorithm both find all SCCs in O(V + E). Used in compiler dead-code elimination, social network analysis, and satisfiability solvers.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Run BFS and DFS by hand on a given graph and record visited order, trace Dijkstra on a 6-node weighted graph finding shortest distances from source, design a heuristic for grid-based A* navigation, and identify whether a given directed graph has a cycle using DFS.
