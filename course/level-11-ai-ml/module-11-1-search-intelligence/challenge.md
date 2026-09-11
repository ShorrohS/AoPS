# Challenge 11.1 — What is Intelligence? Search and Constraint Satisfaction

**Type:** Implementation + trace + reasoning  
**Estimated time:** 50–60 minutes  
**Tools needed:** Python + pen and paper

---

## Part A — A* Implementation

Implement A* search on a 6×6 grid with obstacles. Start = (0,0), Goal = (5,5). Obstacles at: (1,1), (1,2), (2,2), (3,3), (3,4).

1. Implement `astar(grid, start, goal, heuristic)` where:
   - Moves: up/down/left/right (cost 1 each), diagonal (cost √2)
   - Heuristic: Manhattan distance for cardinal, Euclidean for diagonal
   - Returns the path as a list of (row, col) tuples

2. Compare to BFS on the same grid: how many nodes does BFS explore vs A*? Show the exploration counts.

3. Make the heuristic 3× larger (inadmissible): `h(n) = 3 × manhattan(n, goal)`. Does A* still find the shortest path? What path does it find? (A* is no longer guaranteed optimal with an inadmissible heuristic.)

---

## Part B — Minimax with Alpha-Beta

Given this game tree (max at root, min at level 1, values at leaves):

```
             MAX
           /      \
         MIN       MIN
        /   \     /   \
       4     7   2     9
```

4. Apply minimax: what does the root choose? Show the bottom-up value propagation.

5. Apply **alpha-beta pruning** with the same tree traversed left-to-right. Which nodes/subtrees are pruned? Show the α and β values as they update.

6. For a full tic-tac-toe game tree: the branching factor is 9 (first move), 8 (second), etc. Without alpha-beta, how many leaf nodes exist? With alpha-beta (assuming optimal move ordering), approximately how many are evaluated?

---

## Part C — 4-Queens CSP

Place 4 queens on a 4×4 board so no two attack each other (no shared row, column, or diagonal).

7. Define the CSP formally: variables, domains, constraints.

8. Apply **backtracking with forward checking**:
   - Variable ordering: left to right (column 0, 1, 2, 3)
   - For each value assignment, eliminate inconsistent values from remaining domains
   - Show the search tree and mark every backtrack

9. How many assignments are tried? Compare to naive backtracking without forward checking.

10. Apply **MRV (Minimum Remaining Values)**: after placing a queen in column 0, which column (1, 2, or 3) has the fewest remaining valid values? Choose it next.

---

## Part D — Heuristic Admissibility

11. For the 8-puzzle (sliding tile puzzle): is the **misplaced tiles** heuristic admissible? Prove it by showing it never overestimates the actual cost.

12. Is the **Manhattan distance** heuristic admissible for the 8-puzzle? Why is Manhattan distance a "better" (more informed) heuristic than misplaced tiles, even though both are admissible?

13. Construct an example 8-puzzle state where Manhattan distance h = 6 but misplaced tiles h = 3. Show both calculations.

---

## Part E — Local Search

14. **Hill climbing** for finding the maximum of `f(x) = -x² + 4x - 1` on integers x ∈ [0, 5]. Starting at x=0, trace hill climbing: at each step, move to the neighbour with highest value.

15. Hill climbing gets stuck at **local maxima**. Construct a function with multiple local maxima and one global maximum. Show where hill climbing gets stuck depending on the starting point.

16. **Simulated annealing** accepts worse solutions with probability `e^(-Δ/T)`. If the current value is 5 and the neighbour's value is 4 (Δ=1), what is the acceptance probability at T=2? At T=0.5?

---

## Rubric

| Part | Points |
|---|---|
| A A* implementation | 24 |
| B minimax / alpha-beta | 22 |
| C 4-Queens CSP | 22 |
| D heuristic admissibility | 18 |
| E local search | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1 — A* implementation</summary>

```python
import heapq, math

def astar(grid, start, goal, heuristic):
    rows, cols = len(grid), len(grid[0])
    moves = [(0,1,1),(1,0,1),(0,-1,1),(-1,0,1),
             (1,1,math.sqrt(2)),(1,-1,math.sqrt(2)),
             (-1,1,math.sqrt(2)),(-1,-1,math.sqrt(2))]

    g = {start: 0}
    pq = [(heuristic(start, goal), 0, start, [start])]

    while pq:
        f, cost, node, path = heapq.heappop(pq)
        if node == goal: return path, cost
        if cost > g.get(node, float('inf')): continue

        for dr, dc, move_cost in moves:
            nr, nc = node[0]+dr, node[1]+dc
            if 0<=nr<rows and 0<=nc<cols and not grid[nr][nc]:
                new_g = cost + move_cost
                if new_g < g.get((nr,nc), float('inf')):
                    g[(nr,nc)] = new_g
                    f_new = new_g + heuristic((nr,nc), goal)
                    heapq.heappush(pq, (f_new, new_g, (nr,nc), path+[(nr,nc)]))
    return None, float('inf')
```
</details>

<details>
<summary>Part B.4–5 — minimax and alpha-beta</summary>

Minimax:
- MIN left: min(4,7) = 4
- MIN right: min(2,9) = 2
- MAX root: max(4,2) = **4** (choose left branch)

Alpha-beta (left-to-right):
- Start: α=-∞, β=+∞
- Evaluate left MIN: α=-∞, β=+∞
  - See 4: β=4. α=-∞, β=4
  - See 7: β=min(4,7)=4 (no change). Left MIN value=4. α=max(-∞,4)=4
- Evaluate right MIN: α=4, β=+∞
  - See 2: β=min(+∞,2)=2. Now α=4 > β=2 → **prune right subtree (9 never evaluated)**
- Root picks 4.

Node 9 is pruned. One node saved.
</details>
