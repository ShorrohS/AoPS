# Module 11.1 — What is Intelligence? Search and Constraint Satisfaction

---

## The Problem

> A chess program examines millions of board positions per second.
> A GPS finds the optimal driving route through 10,000 intersections.
> A Sudoku solver fills in 81 cells satisfying 27 constraints.
>
> Are these programs "intelligent"?
> What does intelligence mean for a computer?
>
> Before neural networks and large language models,
> AI was built almost entirely from **search** and **constraint satisfaction** —
> systematic exploration of a problem space to find solutions.
> These techniques still power many practical AI systems.

---

## The Story

### The Birth of AI as a Field

**John McCarthy** coined the term "Artificial Intelligence" in 1956 when he organised the Dartmouth Conference — the founding event of AI as a research discipline. The optimism was extraordinary: McCarthy and others believed that within a generation, machines would match human intelligence.

The early approach: intelligence = search. Given a problem with a well-defined state space, intelligent behaviour means searching that space efficiently. Chess, theorem proving, and game playing all reduced to search.

**Allen Newell and Herbert Simon** built the General Problem Solver (1957) — a program that could solve many types of problems by means-ends analysis (measure the gap between current state and goal, take actions to reduce it). Simon predicted in 1958 that within 10 years, computers would be chess champions.

It took 40 years. **Deep Blue** (IBM, 1997) defeated world chess champion Garry Kasparov — using search (alpha-beta pruning) plus an evaluation function trained by chess grandmasters. It searched ~200 million positions per second.

---

## The Concept

### State Space Search

A **state space** defines:
- **States**: all possible configurations of the problem
- **Initial state**: starting configuration
- **Goal test**: how to recognise a solution
- **Actions**: what transitions between states are possible
- **Path cost**: cost of reaching a state along a path

**Example — Romania driving problem**: find the shortest route from Arad to Bucharest. States = cities, initial state = Arad, goal = Bucharest, actions = road connections, path cost = road distance.

This is exactly Dijkstra's algorithm (Module 6.6). Search IS graph traversal.

### Uninformed Search

**BFS**: guaranteed optimal (fewest steps), exponential memory O(b^d) where b = branching factor, d = depth.

**DFS**: O(m) memory (m = max depth), not optimal, can get lost in infinite branches.

**Iterative Deepening DFS (IDDFS)**: run DFS with increasing depth limits (1, 2, 3, ...). Gets DFS memory advantage + BFS optimality. Repeats work but only by a constant factor. The practical uninformed search algorithm of choice.

**Uniform Cost Search (Dijkstra)**: expands lowest-cost node first. Optimal when all costs > 0. Used in GPS routing.

### Informed Search — Heuristics

A **heuristic function** `h(n)` estimates the cost from node n to the goal. Good heuristics reduce search dramatically.

**Greedy Best-First Search**: always expand node with smallest `h(n)`. Fast but not optimal.

**A\* Search**: expand node with smallest `f(n) = g(n) + h(n)` where g(n) = actual cost from start, h(n) = estimated cost to goal.

- If h is **admissible** (never overestimates): A* is optimal
- If h is **consistent** (h(n) ≤ cost(n,n') + h(n')): A* is also efficient

For the Romania example: h(n) = straight-line distance to Bucharest. This never overestimates (roads are longer than straight lines) → admissible.

```python
import heapq

def astar(graph, start, goal, heuristic):
    pq = [(heuristic(start, goal), 0, start, [start])]
    visited = set()
    while pq:
        f, g, node, path = heapq.heappop(pq)
        if node == goal:
            return path, g
        if node in visited:
            continue
        visited.add(node)
        for neighbour, cost in graph[node]:
            if neighbour not in visited:
                new_g = g + cost
                new_f = new_g + heuristic(neighbour, goal)
                heapq.heappush(pq, (new_f, new_g, neighbour, path + [neighbour]))
    return None, float('inf')
```

### Adversarial Search — Games

In two-player zero-sum games (chess, checkers, Go, tic-tac-toe), one player tries to maximise score, the other tries to minimise it. **Minimax** search:

```python
def minimax(state, depth, maximising):
    if depth == 0 or is_terminal(state):
        return evaluate(state)

    if maximising:
        best = -float('inf')
        for child in get_children(state):
            best = max(best, minimax(child, depth-1, False))
        return best
    else:
        best = float('inf')
        for child in get_children(state):
            best = min(best, minimax(child, depth-1, True))
        return best
```

**Alpha-Beta Pruning**: prune branches that cannot affect the final decision. With good move ordering, reduces the effective branching factor from b to √b — searching twice as deep in the same time.

```python
def alphabeta(state, depth, alpha, beta, maximising):
    if depth == 0 or is_terminal(state):
        return evaluate(state)

    if maximising:
        for child in get_children(state):
            value = alphabeta(child, depth-1, alpha, beta, False)
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # β cutoff — minimiser won't allow this
        return alpha
    else:
        for child in get_children(state):
            value = alphabeta(child, depth-1, alpha, beta, True)
            beta = min(beta, value)
            if beta <= alpha:
                break  # α cutoff — maximiser won't allow this
        return beta
```

### Constraint Satisfaction Problems (CSPs)

A CSP is defined by:
- **Variables**: X₁, X₂, ..., Xₙ
- **Domains**: D₁, D₂, ..., Dₙ (possible values for each variable)
- **Constraints**: relations between variables that valid solutions must satisfy

**Examples**: Sudoku (81 variables, domain {1–9}, 27 all-different constraints), N-Queens, map colouring, scheduling.

**Backtracking search for CSPs**:
```python
def backtrack(assignment, csp):
    if is_complete(assignment): return assignment
    var = select_unassigned_variable(assignment, csp)
    for value in order_domain_values(var, assignment, csp):
        if is_consistent(var, value, assignment, csp):
            assignment[var] = value
            result = backtrack(assignment, csp)
            if result is not None: return result
            del assignment[var]
    return None   # failure
```

**Key heuristics** for efficient backtracking:
- **MRV** (Minimum Remaining Values): pick the variable with the fewest legal values — most constrained first
- **Degree heuristic**: tie-break by most constraints with other unassigned variables
- **LCV** (Least Constraining Value): try the value that eliminates fewest values from neighbours
- **Forward checking**: after each assignment, eliminate inconsistent values from unassigned variables
- **Arc Consistency (AC-3)**: propagate constraints more aggressively, potentially detecting failure earlier

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — A\* Pathfinding**
- A grid map with obstacles
- Run BFS, Dijkstra, and A* simultaneously
- Compare nodes explored: A* explores far fewer with a good heuristic
- Adjust heuristic weight (inadmissible) and see paths become suboptimal

**Tool 2 — Minimax / Alpha-Beta**
- A tic-tac-toe board
- Watch minimax explore the game tree
- Enable alpha-beta pruning — see which branches are cut
- Count nodes evaluated with and without pruning

**Tool 3 — CSP Solver: N-Queens**
- N-Queens on an 8×8 board (place 8 queens so no two attack)
- Watch backtracking + MRV + forward checking solve it
- See how quickly failures are detected vs blind backtracking

---

## Going Deeper

**Monte Carlo Tree Search (MCTS)**: used by AlphaGo (2016) and its successors. Instead of minimax with alpha-beta, MCTS selects moves by running thousands of random simulations from the current position and choosing the most promising move by average outcome. Combined with a neural network to guide the search (AlphaGo Zero), it beat the world Go champion — a game considered too complex for traditional tree search.

**Local search and optimisation**: instead of systematic search, start with a random complete assignment and make local improvements. Hill climbing, simulated annealing, genetic algorithms. No completeness guarantee (may get stuck in local optima) but can handle continuous and high-dimensional spaces where systematic search is impossible.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Implement A* to find the shortest path in a weighted grid with obstacles, trace alpha-beta pruning on a given game tree (mark which branches are cut), implement a backtracking CSP solver for 4-queens with MRV heuristic, and explain why the straight-line distance heuristic is admissible for road routing problems.
