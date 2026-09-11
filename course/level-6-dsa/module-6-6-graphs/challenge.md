# Challenge 6.6 — Graphs: BFS, DFS, Dijkstra, A*

**Type:** Trace + implementation + reasoning  
**Estimated time:** 50–60 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — BFS and DFS by Hand

Given this undirected graph:
```
    1 --- 2 --- 5
    |     |     |
    3 --- 4 --- 6
          |
          7
```
Adjacency list (sorted): `{1:[2,3], 2:[1,4,5], 3:[1,4], 4:[2,3,6,7], 5:[2,6], 6:[4,5], 7:[4]}`

1. Run **BFS** from node 1. List nodes in discovery order and show the queue state after each dequeue.

2. Run **DFS** from node 1 (use sorted adjacency lists, so always visit the smallest neighbour first). List nodes in discovery order and show the stack state after each pop.

3. What is the **BFS discovery order** vs the **DFS discovery order**? For which source and target pairs does BFS find a shorter path than DFS on this graph?

---

## Part B — Dijkstra Trace

Weighted graph (directed):
```
Nodes: A, B, C, D, E
A→B: 4    A→C: 2
B→C: 1    B→D: 5
C→B: 1    C→D: 8    C→E: 10
D→E: 2
E→(none)
```

4. Run Dijkstra from source A. For each step, show:
   - The priority queue contents
   - The current node being settled
   - The updated distances

5. What is the shortest path from A to E? List the full path and its total cost.

6. What is the shortest path from A to D? List the path and cost.

---

## Part C — Cycle Detection

7. Given a **directed** graph: `{A:[B], B:[C], C:[A], D:[A]}` — does it contain a cycle? Detect it using DFS with three colours (WHITE=unvisited, GREY=in-stack, BLACK=done).

8. Given the same adjacency list but treating it as **undirected** — same cycle detection approach? What changes? (Hint: you must avoid marking parent edges as back edges.)

9. Implement `has_cycle_directed(graph)` using DFS with a "currently in recursion stack" set.

---

## Part D — Topological Sort

A project has tasks `{A,B,C,D,E,F}` with dependencies:
- B depends on A
- C depends on A
- D depends on B and C
- E depends on C
- F depends on D and E

10. Draw the dependency DAG. Perform a **topological sort** using DFS (add each node to a list after all its descendants are visited, then reverse). Show the DFS order.

11. Perform topological sort using **Kahn's algorithm** (BFS-based):
    - Compute in-degrees for all nodes
    - Start with nodes of in-degree 0
    - Remove them, decrement their neighbours' in-degrees
    Show the queue and result at each step.

12. What happens to Kahn's algorithm if the graph has a cycle? How does this detect the cycle?

---

## Part E — A* on a Grid

13. A 5×5 grid where `X` marks obstacles:
    ```
    . . . X .
    . X . X .
    . X . . .
    . . . X .
    . . . . .
    ```
    Start: (0,0), Goal: (4,4). Each step costs 1. Manhattan distance heuristic: h(r,c) = |4-r| + |4-c|.

    Trace A* for 5 steps: show the open set (priority queue) contents with f=g+h values, and which node is expanded at each step.

14. How many nodes does BFS explore to solve this same maze? How many does A* explore?

15. If the heuristic overestimates (inadmissible), A* may return a suboptimal path. Give a concrete example: design a heuristic that causes A* to miss the optimal path on the 5×5 grid above.

---

## Rubric

| Part | Points |
|---|---|
| A BFS and DFS traces | 24 |
| B Dijkstra trace | 28 |
| C cycle detection | 18 |
| D topological sort | 18 |
| E A* | 12 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part B.4 — Dijkstra from A</summary>

Initial: dist={A:0, B:∞, C:∞, D:∞, E:∞}, PQ=[(0,A)]

Step 1: settle A (d=0). Update B=0+4=4, C=0+2=2. PQ=[(2,C),(4,B)]
Step 2: settle C (d=2). Update B=min(4,2+1)=3, D=min(∞,2+8)=10, E=min(∞,2+10)=12. PQ=[(3,B),(4,B→stale),(10,D),(12,E)]
Step 3: settle B (d=3). Update D=min(10,3+5)=8, C already settled. PQ=[(4,B→stale),(8,D),(12,E)]
Step 4: skip stale (4,B). Settle D (d=8). Update E=min(12,8+2)=10. PQ=[(10,E),(12,E→stale)]
Step 5: settle E (d=10).

Shortest A→E: A→C→B→D→E, cost=10. Shortest A→D: A→C→B→D, cost=8.
</details>

<details>
<summary>Part C.9 — cycle detection</summary>

```python
def has_cycle_directed(graph):
    visited    = set()
    in_stack   = set()

    def dfs(node):
        visited.add(node)
        in_stack.add(node)
        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                if dfs(neighbour): return True
            elif neighbour in in_stack:
                return True    # back edge = cycle
        in_stack.remove(node)
        return False

    return any(dfs(n) for n in graph if n not in visited)
```
</details>

<details>
<summary>Part D.12 — Kahn's with cycle</summary>

If there's a cycle, the nodes in the cycle never reach in-degree 0 (they depend on each other). Kahn's algorithm terminates with nodes remaining in the graph (not all nodes were processed). Detecting this: if the output topological order has fewer nodes than the graph, a cycle exists.
</details>
