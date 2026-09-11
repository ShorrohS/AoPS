# Challenge 5.4 — Recursion: Functions That Call Themselves

**Type:** Trace + implementation + induction proof  
**Estimated time:** 45–55 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — Stack Frame Trace

Trace the execution of `factorial(5)` completely. For each function call, show:
- The call being made
- The current stack depth
- The return value when it unwinds

```
factorial(5)
  → 5 × factorial(4)
       → 4 × factorial(3)
            → ...
```

1. Complete the trace all the way to the base case and back.
2. How many stack frames are on the call stack simultaneously at the deepest point?
3. If each stack frame uses 64 bytes, and the default Python stack limit is 1,000 frames, what is the maximum input to `factorial` before a stack overflow?

---

## Part B — Memoised Fibonacci

The naive recursive Fibonacci has exponential time complexity.

4. Count the exact number of calls to `fib_naive(n)` for n = 0, 1, 2, 3, 4, 5. Do you see a pattern? What is the recurrence for call count C(n)?

5. Implement `fib_memo(n)` using a dictionary cache. Show that the number of unique sub-problems computed is exactly n+1.

6. Implement `fib_bottom_up(n)` using a loop (tabulation). What is the space complexity? Can you reduce it to O(1) space? Write the O(1) space version.

---

## Part C — Recursive List Flattening

Write a recursive function `flatten(lst)` that converts a nested list of arbitrary depth into a flat list:

```python
flatten([1, [2, [3, 4], 5], [6, 7]])
# → [1, 2, 3, 4, 5, 6, 7]

flatten([1, [2, [3, [4, [5]]]]])
# → [1, 2, 3, 4, 5]

flatten([])
# → []
```

7. Implement `flatten` recursively. What is the base case? What is the recursive case?

8. What is the time complexity in terms of the total number of elements (including all nested elements)?

9. Python's default recursion limit is 1,000. What happens if the nesting depth exceeds that? Write an iterative version using an explicit stack that handles arbitrary depth.

---

## Part D — Tower of Hanoi

The Tower of Hanoi with n disks requires exactly 2ⁿ − 1 moves.

10. Prove by **mathematical induction** that the recursive `hanoi(n, A, C, B)` algorithm makes exactly 2ⁿ − 1 moves:
    - Base case: n=1
    - Inductive step: assume true for n-1, prove for n

11. For n=4 disks, `hanoi` generates 15 moves. Run the algorithm mentally (or trace the code) and list all 15 moves in order. Verify the count.

12. Why can't you solve Hanoi in fewer than 2ⁿ − 1 moves? Construct an informal proof: to move the largest disk, all n-1 others must be on one peg, requiring at least 2^(n-1) − 1 moves. Then the largest disk moves (1 move). Then all n-1 disks move again (2^(n-1) − 1 moves). Total?

---

## Part E — Mutual Recursion

```python
def is_even(n):
    if n == 0: return True
    return is_odd(n - 1)

def is_odd(n):
    if n == 0: return False
    return is_even(n - 1)
```

13. Trace `is_even(4)` showing every call. How deep is the call stack at the deepest point?

14. This algorithm is correct but O(n) time and O(n) space. Write an O(1) replacement that doesn't use recursion.

15. The mutual recursion version will stack overflow for large n (e.g., `is_even(10000)`). Rewrite using **tail call optimisation by hand** — convert to a loop that avoids stack growth.

---

## Rubric

| Part | Points |
|---|---|
| A stack frame trace | 20 |
| B memoised Fibonacci | 24 |
| C list flattening | 20 |
| D Tower of Hanoi proof | 24 |
| E mutual recursion | 12 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A — factorial(5) trace</summary>

```
factorial(5) calls factorial(4)     [depth 2]
  factorial(4) calls factorial(3)   [depth 3]
    factorial(3) calls factorial(2) [depth 4]
      factorial(2) calls factorial(1) [depth 5]
        factorial(1) returns 1       [base case]
      factorial(2) returns 2×1 = 2
    factorial(3) returns 3×2 = 6
  factorial(4) returns 4×6 = 24
factorial(5) returns 5×24 = 120
```

Max stack depth: 5 frames (factorial(5) down to factorial(1)).
For 64 bytes/frame, limit 1000 frames: max input ≈ 999 (factorial(999) uses 999 frames).
</details>

<details>
<summary>Part B.4 — call counts</summary>

fib(0)=1, fib(1)=1, fib(2)=3, fib(3)=5, fib(4)=9, fib(5)=15. Pattern: C(n) = C(n-1) + C(n-2) + 1. C(n) = 2×fib(n+1) - 1 = O(φⁿ) where φ ≈ 1.618.
</details>

<details>
<summary>Part C — flatten</summary>

```python
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# Iterative version (handles arbitrary depth):
def flatten_iter(lst):
    result = []
    stack = [lst]
    while stack:
        current = stack.pop()
        if isinstance(current, list):
            for item in reversed(current):
                stack.append(item)
        else:
            result.append(current)
    return result
```
</details>

<details>
<summary>Part D — Induction proof</summary>

**Base case** n=1: hanoi(1) makes 1 move (directly moves disk 1 from A to C). 2¹ - 1 = 1. ✓

**Inductive step**: Assume hanoi(n-1) makes exactly 2^(n-1) - 1 moves. For hanoi(n):
- Step 1: move n-1 disks A→B via C: 2^(n-1) - 1 moves (inductive hypothesis)
- Step 2: move disk n A→C: 1 move
- Step 3: move n-1 disks B→C via A: 2^(n-1) - 1 moves (same sub-problem)

Total: 2×(2^(n-1) - 1) + 1 = 2ⁿ - 2 + 1 = **2ⁿ - 1**. ✓
</details>
