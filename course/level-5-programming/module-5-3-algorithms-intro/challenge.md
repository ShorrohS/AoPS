# Challenge 5.3 — Algorithms: Thinking in Steps

**Type:** Analysis + implementation + complexity proof  
**Estimated time:** 45–55 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — Complexity Analysis

For each code snippet, determine the time complexity as a function of n. Show your reasoning.

**Snippet 1:**
```python
def f1(n):
    total = 0
    for i in range(n):
        for j in range(n):
            total += i * j
    return total
```

**Snippet 2:**
```python
def f2(arr):
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):   # inner loop starts at i+1
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
    return arr
```

**Snippet 3:**
```python
def f3(n):
    count = 0
    i = n
    while i > 1:
        i = i // 2
        count += 1
    return count
```

**Snippet 4:**
```python
def f4(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: low = mid + 1
        else: high = mid - 1
    return -1
```

1. What is the Big-O of f1, f2, f3, f4?
2. f2 has an inner loop from `i+1` to `n`. Why is it still O(n²) and not O(n²/2)?
3. What is the difference between O(log n) and O(n log n) in practice? Compute both for n = 1,000,000.

---

## Part B — Convert O(n²) to O(n)

The following function finds all pairs in an array that sum to a target:

```python
def find_pairs_slow(arr, target):
    pairs = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == target:
                pairs.append((arr[i], arr[j]))
    return pairs
```

4. What is its time complexity?
5. Rewrite it as `find_pairs_fast(arr, target)` using a hash set to achieve O(n). You may produce pairs in any order.
6. What is the space complexity trade-off?

---

## Part C — Recurrence Relations

Solve these recurrence relations using the Master Theorem where applicable:

7. `T(n) = 2T(n/2) + O(n)` — what algorithm has this recurrence? What is the solution?
8. `T(n) = T(n/2) + O(1)` — what algorithm? Solution?
9. `T(n) = 4T(n/2) + O(n)` — apply Master Theorem. (a=4, b=2, d=1)
10. `T(n) = T(n-1) + O(1)` — this does NOT fit the Master Theorem. What is the closed-form solution?

---

## Part D — Algorithm Design

**Problem:** Given an array of integers, find the maximum sum of any contiguous sub-array. Example: `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` → answer is `6` (sub-array `[4,-1,2,1]`).

11. Write a brute-force O(n²) solution that checks all sub-arrays.
12. Write the O(n) **Kadane's algorithm**:
    - Track `current_sum` (best sum ending at this position) and `best_sum`
    - At each element: `current_sum = max(element, current_sum + element)`
    - Update `best_sum = max(best_sum, current_sum)`
    - Trace this on the example array above, showing `current_sum` and `best_sum` at each step.
13. Why is `max(element, current_sum + element)` the right recurrence? Explain the intuition.

---

## Part E — Lower Bounds

14. A comparison-based sort must perform Ω(n log n) comparisons in the worst case. The proof uses decision trees with n! leaves. For n=3 elements, draw the **complete decision tree** for insertion sort, labelling every internal node with a comparison and every leaf with a permutation. How many comparisons does the deepest path require?

15. **Binary search lower bound**: prove that any algorithm for finding a target in a sorted array of n elements requires at least ⌈log₂(n+1)⌉ comparisons in the worst case.

---

## Rubric

| Part | Points |
|---|---|
| A complexity analysis | 20 |
| B O(n²) → O(n) | 18 |
| C recurrences | 24 |
| D Kadane's | 24 |
| E lower bounds | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A</summary>

1. f1: O(n²). f2: O(n²) (n(n-1)/2 ≈ n²/2 iterations). f3: O(log n) (halves each step). f4: O(log n) (binary search).

2. n(n-1)/2 = n²/2 - n/2. Big-O drops the coefficient 1/2 and the lower-order term. Both O(n²) and O(n²/2) are the same class.

3. For n=1,000,000: log₂(10⁶) ≈ 20. n log n ≈ 20,000,000. So n log n is 1 million times more operations than log n.
</details>

<details>
<summary>Part B.5 — O(n) pairs</summary>

```python
def find_pairs_fast(arr, target):
    seen = set()
    pairs = []
    for x in arr:
        complement = target - x
        if complement in seen:
            pairs.append((complement, x))
        seen.add(x)
    return pairs
```
Time: O(n). Space: O(n) for the set.
</details>

<details>
<summary>Part C</summary>

7. T(n) = 2T(n/2) + O(n): a=2, b=2, d=1. log_b(a) = log₂(2) = 1 = d → T(n) = **O(n log n)**. Merge Sort.

8. T(n) = T(n/2) + O(1): a=1, b=2, d=0. log₂(1) = 0 = d → T(n) = **O(log n)**. Binary search.

9. T(n) = 4T(n/2) + O(n): a=4, b=2, d=1. log_b(a) = log₂(4) = 2 > d=1 → T(n) = **O(n^log₂4) = O(n²)**.

10. T(n) = T(n-1) + O(1): expand → T(n) = T(n-2) + 2·O(1) = ... = T(0) + n·O(1) = **O(n)**.
</details>

<details>
<summary>Part D.12 — Kadane's trace</summary>

Array: [-2, 1, -3, 4, -1, 2, 1, -5, 4]

| i | val | current_sum | best_sum |
|---|-----|-------------|----------|
| 0 | -2  | -2          | -2       |
| 1 |  1  | 1           | 1        |
| 2 | -3  | -2          | 1        |
| 3 |  4  | 4           | 4        |
| 4 | -1  | 3           | 4        |
| 5 |  2  | 5           | 5        |
| 6 |  1  | 6           | 6        |
| 7 | -5  | 1           | 6        |
| 8 |  4  | 5           | 6        |

Answer: 6.
</details>
