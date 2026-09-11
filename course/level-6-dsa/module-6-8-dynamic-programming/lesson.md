# Module 6.8 — Dynamic Programming

---

## The Problem

> Naive recursion for Fibonacci: each call to fib(n) spawns two more.
> fib(50) requires 2⁵⁰ ≈ 10¹⁵ calls — impossible.
>
> But fib(50) only has 50 distinct sub-problems: fib(0), fib(1), ..., fib(49).
> If we compute each one *once* and *store the result*, we need exactly 50 operations.
>
> This is dynamic programming in its essence:
> identify overlapping sub-problems, solve each once, store the result,
> and build the final answer from stored sub-results.

Dynamic programming (DP) transforms exponential-time recursive algorithms into polynomial-time ones — one of the most powerful algorithmic techniques in computer science.

---

## The Story

### Richard Bellman and the Name

**Richard Bellman** coined the term "dynamic programming" in 1953 while working at RAND Corporation on optimal control problems. The name was deliberately chosen to sound impressive and avoid scrutiny — Bellman was working under a Secretary of Defense who disliked mathematics research, so he named it to be vague and unchallengeable.

The actual technique — breaking problems into sub-problems and storing results — had been used informally for centuries. But Bellman formalised it as a general principle and developed the **principle of optimality**: an optimal solution to the whole problem contains optimal solutions to its sub-problems.

DP is fundamental to: sequence alignment in bioinformatics (finding how similar two DNA sequences are), compiler optimisation (code generation), network routing (Bellman-Ford), speech recognition (Viterbi algorithm), machine translation, and game playing (minimax with memoisation).

---

## The Concept

### Two Approaches: Top-Down and Bottom-Up

**Top-Down (Memoisation)**: write the natural recursion, cache results in a dictionary.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

# Or manually:
memo = {}
def fib_memo(n):
    if n in memo: return memo[n]
    if n <= 1: return n
    memo[n] = fib_memo(n-1) + fib_memo(n-2)
    return memo[n]
```

**Bottom-Up (Tabulation)**: fill a table from smallest sub-problems upward.

```python
def fib_dp(n):
    if n <= 1: return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# Space optimised (only need last two):
def fib_optimal(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

**When to use top-down vs bottom-up**:
- Top-down is easier to write (follow the recursion), handles sparse sub-problem spaces
- Bottom-up is often faster (no recursion overhead, better cache behaviour), more space-efficient

### Identifying a DP Problem

Two properties make a problem solvable with DP:

1. **Optimal substructure**: an optimal solution contains optimal solutions to sub-problems
2. **Overlapping sub-problems**: the same sub-problems are solved repeatedly in naive recursion

If a problem has both, DP applies.

### Canonical DP Problems

**Longest Common Subsequence (LCS)**:

Given two strings, find the length of their longest common subsequence (characters in order, not necessarily contiguous).

```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

lcs("ABCBDAB", "BDCAB")   # 4 (BCAB or BDAB)
```

Time: O(mn). Used in: `diff` (finding differences between files), DNA sequence alignment, version control systems.

**0/1 Knapsack**:

n items, each with weight w[i] and value v[i]. A bag with capacity W. Maximise total value without exceeding capacity. Each item used at most once.

```python
def knapsack(weights, values, W):
    n = len(weights)
    dp = [[0] * (W+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for w in range(W+1):
            dp[i][w] = dp[i-1][w]    # don't take item i
            if weights[i-1] <= w:
                take = dp[i-1][w - weights[i-1]] + values[i-1]
                dp[i][w] = max(dp[i][w], take)   # take item i
    return dp[n][W]
```

Time: O(nW) — pseudo-polynomial (polynomial in W, but W can be exponentially large).

**Coin Change**:

Given coin denominations and a target amount, find the minimum number of coins.

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for amt in range(1, amount + 1):
        for coin in coins:
            if coin <= amt:
                dp[amt] = min(dp[amt], dp[amt - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

coin_change([1, 5, 10, 25], 36)   # 3 coins: 25+10+1
```

**Longest Increasing Subsequence (LIS)**:

```python
def lis(arr):
    if not arr: return 0
    n = len(arr)
    dp = [1] * n             # each element alone is an LIS of length 1
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

lis([10, 9, 2, 5, 3, 7, 101, 18])   # 4 (2,3,7,101 or 2,5,7,101)
```

O(n²) DP. There is an O(n log n) solution using binary search and patience sorting.

### The DP Design Process

**Step 1 — Define the sub-problem**: what does `dp[i]` or `dp[i][j]` represent?

**Step 2 — Write the recurrence**: how does `dp[i]` depend on smaller sub-problems?

**Step 3 — Identify base cases**: what are the smallest sub-problems with known answers?

**Step 4 — Determine computation order**: which sub-problems must be solved before others?

**Step 5 — Extract the answer**: which cell(s) of the table contain the final answer?

**Step 6 — Optimise space**: often only the last row (or last two values) of the DP table is needed.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Fibonacci DP Table**
- Watch the DP table fill from left to right
- Compare total calls: naive recursion (exponential) vs DP (linear)
- See the memoisation cache fill in top-down mode

**Tool 2 — LCS Grid**
- Enter two strings
- Watch the 2D DP table fill cell by cell
- Trace back through the table to find the actual LCS (not just its length)

**Tool 3 — Knapsack Visualiser**
- Set item weights and values, set capacity
- Watch the DP table fill
- At each cell, see the choice: take or skip
- Trace back to find which items were selected

---

## Going Deeper

**Interval DP**: problems where sub-problems are defined over intervals [i,j] of a sequence. Matrix chain multiplication (minimise multiplications to compute A₁ × A₂ × ... × Aₙ), optimal BST construction, and burst balloons are classic interval DP problems. The recurrence considers all possible "split points" k within [i,j].

**DP on trees**: instead of a 1D or 2D table, the DP state is defined on tree nodes. For each node, compute a value that depends on its children's values. Used in: maximum independent set on a tree, tree diameter, re-rooting technique. The computation follows a post-order traversal.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace the LCS table for "ABCD" and "ACBD", solve the coin change problem for [2,5,10] with target 27, find the LIS of [3,1,4,1,5,9,2,6] with full DP table, and explain the difference between memoisation and tabulation with a concrete example.
