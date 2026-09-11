# Module 5.3 — Algorithms: Thinking in Steps

---

## The Problem

> You have a program that works.
> It processes 100 records in 0.01 seconds.
> You run it on 1,000,000 records.
> It takes 27 hours.
>
> What went wrong?

Nothing *crashed*. The logic is correct. But the **algorithm** — the sequence of steps used to solve the problem — scales so poorly that the program becomes useless at the scale it was designed for.

Understanding algorithms means understanding not just *how* to solve a problem, but *how efficiently* — and being able to predict what happens when the input grows by 10×, 100×, or 1,000,000×.

---

## The Story

### The Algorithm Predates the Computer

The word **algorithm** comes from the name of the 9th-century Persian mathematician Muhammad ibn Musa al-Khwarizmi, whose book *Kitab al-mukhtasar fi hisab al-jabr wal-muqabala* (825 AD) introduced systematic procedures for solving equations. "Algorithm" is a Latinisation of al-Khwarizmi. "Algebra" comes from "al-jabr" in the title.

Long before computers, people described algorithms: Euclid's algorithm for the GCD of two numbers (300 BC) is still used in every modern computer's arithmetic library. Long division is an algorithm. A recipe is an algorithm. The question is always the same: *how many steps does it take, and how does that grow as the input grows?*

Alan Turing formalised the concept of a computable algorithm in 1936 with the Turing machine — a theoretical model that defines exactly what it means for a problem to be solvable by a mechanical process.

---

## The Concept

### Big-O Notation

Big-O notation describes how an algorithm's runtime (or memory usage) scales as the input size *n* grows. It describes the **worst-case upper bound**, ignoring constant factors.

| Notation | Name | Example | n=100 | n=1,000 | n=1,000,000 |
|---|---|---|---|---|---|
| O(1) | Constant | Array index access | 1 op | 1 op | 1 op |
| O(log n) | Logarithmic | Binary search | 7 ops | 10 ops | 20 ops |
| O(n) | Linear | Linear scan | 100 | 1,000 | 1,000,000 |
| O(n log n) | Linearithmic | Merge sort | 664 | 9,966 | 19,931,568 |
| O(n²) | Quadratic | Bubble sort | 10,000 | 1,000,000 | 10¹² |
| O(2ⁿ) | Exponential | Naive TSP | 10³⁰ | — | — |

The difference between O(n log n) and O(n²) is the difference between a sort that handles a million records in 1 second and one that takes 12 days.

**Formal definition**: f(n) = O(g(n)) if there exist constants c > 0 and n₀ such that f(n) ≤ c·g(n) for all n ≥ n₀. In practice: keep only the fastest-growing term, drop coefficients.

### Analysing an Algorithm

```python
def find_duplicates(lst):          # n = len(lst)
    for i in range(len(lst)):      # n iterations
        for j in range(len(lst)):  # n iterations (inner)
            if i != j and lst[i] == lst[j]:
                return True
    return False
```

Inner loop runs n times for each of n outer iterations: **O(n²)**.

Better approach:
```python
def find_duplicates_fast(lst):
    seen = set()                   # O(1) lookup
    for x in lst:                  # n iterations
        if x in seen:              # O(1) average
            return True
        seen.add(x)                # O(1) average
    return False
```

Single loop, O(1) operations per iteration: **O(n)**. For n=1,000,000: the first version does 10¹² comparisons; the second does 1,000,000.

### Space Complexity

Runtime is not the only resource that scales. Memory usage also has a Big-O:

```python
def sum_list(lst):
    total = 0              # O(1) space — one variable
    for x in lst:
        total += x
    return total           # Total: O(1) space
```

```python
def reverse_list(lst):
    result = []            # O(n) space — new list same size as input
    for i in range(len(lst) - 1, -1, -1):
        result.append(lst[i])
    return result          # Total: O(n) space
```

There is often a space-time tradeoff: use more memory to get faster runtime (hash tables, memoisation) or use less memory at the cost of more computation (in-place sorts).

### Recursion and the Recurrence Relation

Many algorithms are naturally recursive. Their complexity is expressed as a **recurrence relation**:

```python
def binary_search(arr, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, high)
    else:
        return binary_search(arr, target, low, mid - 1)
```

At each step, the problem size halves: T(n) = T(n/2) + O(1). Solving: T(n) = **O(log n)**.

**The Master Theorem** gives a formula for recurrences of the form T(n) = aT(n/b) + O(n^d):
- If d > log_b(a): T(n) = O(n^d)
- If d = log_b(a): T(n) = O(n^d log n)
- If d < log_b(a): T(n) = O(n^(log_b a))

Merge sort: T(n) = 2T(n/2) + O(n), so a=2, b=2, d=1. log_2(2)=1=d → T(n) = O(n log n).

### Greedy, Divide-and-Conquer, Dynamic Programming

These three paradigms cover most algorithm design:

**Greedy**: at each step, make the locally optimal choice and never reconsider.
- Coin change (specific denominations), activity selection, Dijkstra's shortest path
- Fast, simple — but often does not produce the global optimum

**Divide and Conquer**: split the problem into independent sub-problems, solve each, combine.
- Merge sort, binary search, quicksort, fast Fourier transform
- Enables O(n log n) where naive approaches are O(n²)

**Dynamic Programming**: break into overlapping sub-problems; store results to avoid recomputation.
- Fibonacci, longest common subsequence, shortest path (Bellman-Ford), knapsack
- Turns exponential recursion into polynomial iteration

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Complexity Plotter**
- Enter two algorithm complexities (e.g., O(n²) vs O(n log n))
- See the actual operation counts plotted as n grows
- Observe the crossover point where the faster algorithm wins

**Tool 2 — Linear vs Binary Search**
- An array of 1,000 sorted elements
- Run linear search and watch it step through elements one by one
- Run binary search and watch it halve the search space each step
- Compare step counts directly

**Tool 3 — Recurrence Solver**
- Enter a recurrence relation (e.g., T(n) = 2T(n/2) + n)
- See the recursion tree drawn
- Watch the Master Theorem apply and produce the complexity class

---

## Going Deeper

**NP-completeness**: some problems have no known polynomial-time algorithm. The **Travelling Salesman Problem** (find the shortest route through n cities) can be solved in O(n!) by brute force or O(n² × 2ⁿ) with dynamic programming — still exponential. No one has found a polynomial algorithm, but no one has proven one doesn't exist. This is the famous P vs NP question — one of the Millennium Prize Problems. If P=NP were proven, essentially all cryptography would be broken.

**Amortised analysis**: some data structures (dynamic arrays, hash tables) occasionally do expensive operations (resizing). The cost averaged over a sequence of operations — the *amortised* cost — is much lower. Python lists use amortised O(1) for `append()`: the list doubles in capacity when full, so n appends cost O(n) total, or O(1) per append amortised.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Analyse the time complexity of given code snippets, convert a naive O(n²) solution to O(n), trace a binary search, and solve a simple recurrence relation using the Master Theorem.
