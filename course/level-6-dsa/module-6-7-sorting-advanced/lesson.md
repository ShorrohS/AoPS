# Module 6.7 — Sorting: Merge, Quick, Radix

---

## The Problem

> Module 5.5 introduced sorting and Big-O complexity.
> Now we go deeper: not just *what* these algorithms do,
> but *why* they work, *what guarantees* they provide,
> how to *implement* them correctly at the code level,
> and when to choose each one for a real problem.
>
> Three algorithms dominate practical sorting:
> Merge Sort for guaranteed O(n log n),
> Quick Sort for real-world speed,
> and Radix Sort for when you can beat the comparison lower bound.

---

## The Story

### The Race for Practical Sorting

By the 1960s, sorting was known to have an O(n log n) lower bound for comparison-based methods. Merge Sort (von Neumann, 1945) achieved this but required O(n) extra memory. Shell Sort (1959) was faster in practice but its worst case was unclear. **Tony Hoare's** Quicksort (1962) was average-case O(n log n) and in-place — a stunning combination.

For decades, the battle between Merge Sort and Quicksort dominated practical computing. IBM's OS/360 used Merge Sort for stability and predictability. Unix's `qsort` used Quicksort for speed. Java's Arrays.sort for primitives uses Dual-Pivot Quicksort (Yaroslavskiy, 2009). Python's `list.sort()` uses Timsort (Peters, 2002) — a hybrid Merge Sort that exploits real-world patterns.

The key insight that drove modern sort implementations: theoretical worst cases matter less than average-case performance on real data. Real data is often partially sorted, has repeated elements, or exhibits patterns. Good sorts exploit these patterns.

---

## The Concept

### Merge Sort — Full Implementation

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j  = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:     # <= for stability
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Bottom-up Merge Sort** (iterative, avoids recursion overhead):
```python
def merge_sort_iterative(arr):
    n = len(arr)
    width = 1
    while width < n:
        for i in range(0, n, 2 * width):
            left  = arr[i : i + width]
            right = arr[i + width : i + 2 * width]
            arr[i : i + len(left) + len(right)] = merge(left, right)
        width *= 2
    return arr
```

Bottom-up avoids the O(log n) recursion stack — useful when stack space is limited.

**Correctness proof by induction**: base case (len ≤ 1 is sorted), inductive step (merge of two sorted arrays is sorted), merge is correct (takes the smaller of two heads at each step). Merging two arrays of total size m takes exactly m-1 comparisons at most.

### Quicksort — Correct and Efficient Implementation

The key to correct Quicksort is the **partition function**. The most common bug: incorrect boundary conditions.

```python
import random

def quicksort(arr, lo=0, hi=None):
    if hi is None: hi = len(arr) - 1
    if lo >= hi: return
    pivot_idx = partition(arr, lo, hi)
    quicksort(arr, lo, pivot_idx - 1)
    quicksort(arr, pivot_idx + 1, hi)

def partition(arr, lo, hi):
    # Randomise pivot to avoid worst case on sorted input
    rand_idx = random.randint(lo, hi)
    arr[rand_idx], arr[hi] = arr[hi], arr[rand_idx]
    pivot = arr[hi]
    i = lo - 1
    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[hi] = arr[hi], arr[i+1]
    return i + 1
```

**Three-way partition** (Dutch National Flag, Dijkstra 1976) — handles duplicates efficiently:
```python
def quicksort_3way(arr, lo, hi):
    if lo >= hi: return
    lt, gt = lo, hi
    pivot  = arr[lo]
    i = lo + 1
    while i <= gt:
        if   arr[i] < pivot: arr[lt], arr[i] = arr[i], arr[lt]; lt += 1; i += 1
        elif arr[i] > pivot: arr[gt], arr[i] = arr[i], arr[gt]; gt -= 1
        else:                i += 1
    quicksort_3way(arr, lo, lt - 1)
    quicksort_3way(arr, gt + 1, hi)
```

With three-way partitioning, an array of all identical elements sorts in O(n) — each element is compared exactly once and placed in the "equal" region.

**Introsort** (David Musser, 1997): Quicksort with a fallback to Heapsort when recursion depth exceeds 2·log₂(n). Guarantees O(n log n) worst case while keeping Quicksort's average-case speed. Used in C++ `std::sort`.

### Counting Sort and Radix Sort

When keys are integers in a bounded range [0, k], we can sort in **O(n + k)** — faster than O(n log n).

**Counting Sort**:
```python
def counting_sort(arr, k):
    count = [0] * (k + 1)
    for x in arr:
        count[x] += 1
    # Cumulative counts (for stable positioning)
    for i in range(1, k+1):
        count[i] += count[i-1]
    output = [0] * len(arr)
    for x in reversed(arr):    # reversed for stability
        count[x] -= 1
        output[count[x]] = x
    return output
```

O(n + k) time and space. Optimal when k = O(n) — e.g., sorting ages (k=150), test scores (k=100), ASCII characters (k=128).

**Radix Sort** — sort digit by digit, least significant to most significant:
```python
def radix_sort(arr):
    if not arr: return arr
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        arr = counting_sort_by_digit(arr, exp)
        exp *= 10
    return arr

def counting_sort_by_digit(arr, exp):
    n = len(arr)
    count  = [0] * 10
    output = [0] * n
    for x in arr:
        digit = (x // exp) % 10
        count[digit] += 1
    for i in range(1, 10):
        count[i] += count[i-1]
    for x in reversed(arr):
        digit = (x // exp) % 10
        count[digit] -= 1
        output[count[digit]] = x
    return output
```

For 32-bit integers with base 256: 4 passes, each O(n) → **O(4n) = O(n)** total.

**Why does it work?** Sorting by LSD (Least Significant Digit) first, then MSD last, with a *stable* sort at each step, produces a correctly sorted array. Stability is critical: elements equal on the current digit must retain their relative order from previous digit sorts.

### The Lower Bound and When to Break It

**Comparison-based lower bound theorem**: any sort that only uses comparisons (a < b?) requires Ω(n log n) comparisons in the worst case. Proof: the decision tree has n! leaves (all possible orderings), height ≥ log₂(n!) = Θ(n log n).

**Radix sort breaks this bound** because it doesn't compare — it uses the key's digits as array indices. It operates outside the comparison model. But the price: it only works on integer (or integer-encoded) keys and requires O(n) extra space.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Merge Sort Tree**
- Watch the recursion tree as merge sort executes
- See each merge operation with two sorted sub-arrays combining
- Count total comparisons across all levels

**Tool 2 — Quicksort Partition Visualiser**
- Step through each partition: see the pivot chosen, the swap sequence, and the final placement
- Try: already sorted input (bad for naive pivot), reverse sorted, random
- Enable randomised pivot — see how it protects against worst case

**Tool 3 — Radix Sort Digit-by-Digit**
- An array of 3-digit numbers
- Watch sorting happen one digit at a time
- After each pass, verify the partial sort is stable

---

## Going Deeper

**Timsort in detail**: Python's Timsort finds natural "runs" of already-sorted data. If a run is shorter than `minrun` (≈32), it extends it with binary insertion sort. Runs are merged using a careful strategy that maintains a stack of runs satisfying size invariants — ensuring no merge is much larger than its neighbours. This is why `sorted([1,2,3,4,5,6,7,8])` is nearly instant in Python even though Mergesort is O(n log n): Timsort detects the single ascending run in O(n) and returns immediately.

**Parallel sorting**: modern CPUs have many cores. Merge Sort parallelises naturally — sort left and right halves on separate threads, then merge. The parallel time complexity is O(n/p + n) where p = number of processors. GPU-based radix sort can sort 100 million integers per second on modern hardware.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace merge sort on [5,3,8,1,9,2,7,4], identify the worst-case input for Quicksort with a fixed last-element pivot, implement counting sort for a range [0,9], and explain why the three-way partition makes sorting an array of identical elements O(n).
