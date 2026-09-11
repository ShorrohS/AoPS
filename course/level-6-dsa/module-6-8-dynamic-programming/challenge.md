# Challenge 6.8 — Dynamic Programming

**Type:** Trace + implementation + design  
**Estimated time:** 50–60 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — LCS Table

Compute the **Longest Common Subsequence** of `"ABCD"` and `"ACBD"`.

1. Fill in the complete DP table (5×5 including the empty-string base case). Use the recurrence:
   - `dp[i][j] = dp[i-1][j-1] + 1` if `s1[i-1] == s2[j-1]`
   - `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` otherwise

2. What is the length of the LCS?

3. **Reconstruct** the actual LCS string by tracing back through the table. Show every step of the traceback.

4. Is the LCS unique? For these two strings, list all LCS strings of maximum length.

---

## Part B — Coin Change

Given coins `[2, 5, 10]` and target amount `27`:

5. Is it possible to make change for 27 with these coins? (Can you make 27 from 2, 5, and 10?)

6. Fill in the DP table for `dp[0..27]` where `dp[i]` = minimum coins to make amount `i` (or ∞ if impossible). Show values for `dp[0]` through `dp[15]` and `dp[27]`.

7. Reconstruct the coin combination: trace back from `dp[27]` to identify which coins were used.

8. Modify the problem: count the **number of distinct ways** to make change for target=10 using coins [1,2,5]. Write the recurrence and compute the answer.

---

## Part C — Longest Increasing Subsequence

Find the LIS length of `[3, 1, 4, 1, 5, 9, 2, 6]`.

9. Fill in the DP table where `dp[i]` = length of LIS ending at index i.

10. What is the LIS length? List all LIS sequences of that length.

11. The O(n²) DP can be improved to O(n log n) using patience sorting + binary search. Explain the patience sorting algorithm and show how it processes `[3, 1, 4, 1, 5, 9, 2, 6]`.

---

## Part D — Design a DP Solution

**Problem**: Given an m×n grid, count the number of distinct paths from the top-left corner to the bottom-right corner, moving only right or down.

12. Define the sub-problem: what does `dp[i][j]` represent?

13. Write the recurrence and base cases.

14. Implement `count_paths(m, n)` using bottom-up DP. What is the time and space complexity?

15. **Space optimisation**: the current row only depends on the previous row. Optimise to O(n) space. Show the implementation.

16. Can you solve this with a closed-form formula? Hint: a path from (0,0) to (m-1, n-1) requires exactly (m-1) down moves and (n-1) right moves. The number of distinct orderings is the binomial coefficient C(m+n-2, n-1). Calculate for m=4, n=4.

---

## Part E — Memoisation vs Tabulation

17. The knapsack problem (`n=10 items, W=50`) has 10×50=500 sub-problems but not all may be needed. When would memoisation (top-down) be preferred over tabulation (bottom-up)?

18. For the Fibonacci sequence, compare: naive recursion, memoisation, tabulation, and the O(1) space iterative solution. Fill in the table:

| Approach | Time | Space | Code complexity |
|---|---|---|---|
| Naive recursion | | | |
| Memoisation | | | |
| Tabulation | | | |
| O(1) iterative | | | |

---

## Rubric

| Part | Points |
|---|---|
| A LCS table | 24 |
| B coin change | 22 |
| C LIS | 20 |
| D grid paths | 22 |
| E analysis | 12 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A — LCS table for "ABCD" / "ACBD"</summary>

```
     ""  A   C   B   D
""  [ 0   0   0   0   0 ]
A   [ 0   1   1   1   1 ]
B   [ 0   1   1   2   2 ]
C   [ 0   1   2   2   2 ]
D   [ 0   1   2   2   3 ]
```

LCS length = 3. Traceback: dp[4][4]=3, s1[3]='D'=s2[3]='D' → take D, go to [3][3].
dp[3][3]=2, s1[2]='C'=s2[1]='C' → take C, go to [2][1]. Actually C≠B so go left: dp[3][2]=2, s1[2]='C'=s2[1]='C' → take C. Continue to find 'A'.
LCS = "ACD" or "ABD" (both length 3).
</details>

<details>
<summary>Part D.16 — closed form</summary>

m=4, n=4: C(4+4-2, 4-1) = C(6,3) = 6!/(3!3!) = 720/36 = **20** paths.
</details>

<details>
<summary>Part E.18 — Fibonacci comparison</summary>

| Approach | Time | Space | Code complexity |
|---|---|---|---|
| Naive recursion | O(2ⁿ) | O(n) stack | Low |
| Memoisation | O(n) | O(n) cache + stack | Low |
| Tabulation | O(n) | O(n) array | Low |
| O(1) iterative | O(n) | O(1) | Low |
</details>
