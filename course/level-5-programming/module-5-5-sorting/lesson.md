# Module 5.5 — Sorting: Putting Things in Order

---

## The Problem

> A database table has 50 million rows.
> A search engine needs to rank 10 billion web pages.
> A hospital system needs to sort 100,000 patient records by urgency in real time.
>
> Sorting is one of the most fundamental operations in computing.
> It is estimated that 25% of all CPU time in the world is spent sorting.
> And the difference between a bad sort algorithm and a good one
> is the difference between a program that works and one that never finishes.

---

## The Story

### The Sorting Problem Drove Algorithm Theory

In the 1950s and 60s, IBM's core business was data processing — payroll, census tabulation, inventory management. Sorting punched cards and magnetic tape records was the bottleneck. IBM researchers spent enormous effort on sort algorithms because a 2× speedup in sort performance would save millions of dollars in computing time.

**John von Neumann** wrote Mergesort in 1945 — the first O(n log n) sort algorithm. **Tony Hoare** invented Quicksort in 1959 while working on machine translation at Moscow State University. The sorting problem was so important that it drove major theoretical advances: the proof that no comparison-based sort can be faster than O(n log n) in the worst case (the information-theoretic lower bound), and the discovery of Radix sort which breaks this barrier by not using comparisons.

The standard sort algorithm in production today (Timsort, used in Python, Java, and Android) was invented in 2002 by Tim Peters specifically for Python. It exploits real-world patterns in data — partially sorted runs — to achieve near-linear performance on common inputs.

---

## The Concept

### The Sorting Problem

**Input**: an array of n elements with a total order (we can compare any two elements).  
**Output**: the same elements in non-decreasing order.  
**Constraint**: we count comparisons and swaps; we want to minimise them.

### Bubble Sort — O(n²) — The Slow Baseline

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
```

Each pass "bubbles" the largest unsorted element to its final position. n passes × n comparisons each = O(n²).

In practice: never use bubble sort. It is taught because it is simple to understand and implement, but its performance is catastrophically bad for n > 1,000.

### Merge Sort — O(n log n) — Guaranteed

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])    # sort left half
    right = merge_sort(arr[mid:])    # sort right half
    return merge(left, right)        # merge two sorted halves

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Why O(n log n)?**  
Divide: log₂(n) levels of recursion. Each level merges total n elements. Total: n × log n comparisons.

**Stable**: elements with equal keys maintain their original relative order.  
**Not in-place**: requires O(n) extra space for the merge step.  
**Predictable**: always O(n log n), never worse. Preferred when worst-case matters (e.g., real-time systems).

### Quick Sort — O(n log n) average, O(n²) worst

```python
def quick_sort(arr, low=0, high=None):
    if high is None: high = len(arr) - 1
    if low < high:
        p = partition(arr, low, high)
        quick_sort(arr, low, p - 1)
        quick_sort(arr, p + 1, high)

def partition(arr, low, high):
    pivot = arr[high]    # choose last element as pivot
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1
```

**Pivot selection** is everything. With a good pivot (median-of-three, random), the array splits roughly in half each time: O(n log n). With the worst pivot (always the smallest or largest element, e.g., sorted input with naive pivot choice): one partition gets n-1 elements → O(n²).

**In-place**: O(log n) stack space for recursion, O(1) extra space otherwise.  
**Cache-friendly**: accesses memory sequentially — excellent real-world performance.  
**Not stable**: equal elements may be reordered.

In practice, Quicksort with randomised or median-of-three pivot is faster than Mergesort on random data by a constant factor, despite the same O(n log n) asymptotics.

### Heap Sort — O(n log n), in-place

Builds a max-heap from the array (O(n)), then repeatedly extracts the maximum (O(log n) each × n times).

- Always O(n log n), in-place, not stable
- Cache-unfriendly (heap accesses jump around memory)
- Used when guaranteed in-place O(n log n) is required

### Radix Sort — O(nk) — Beats the Lower Bound

The O(n log n) lower bound applies only to **comparison-based** sorts. Radix sort does not compare elements — it distributes them into buckets by individual digits.

```python
def radix_sort(arr, base=10):
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_by_digit(arr, base, exp)
        exp *= base
```

For 32-bit integers with base 256: 4 passes, each O(n) → O(4n) = **O(n)**. In practice, the constant factor is large, and Radix sort is only faster than comparison sorts for very large n with bounded key size (e.g., sorting IP addresses, DNA sequences).

### Timsort — The Real-World Champion

Python's built-in `sorted()` and `list.sort()` use **Timsort** (Tim Peters, 2002):

1. Find natural **runs** of already-sorted data in the input (forward or backward)
2. Ensure each run is at least `minrun` elements (typically 32–64) using insertion sort
3. **Merge** runs pairwise using a merge sort variant with "galloping" mode for runs with long sequential matches

**Best case**: O(n) on already-sorted data (just finds one run).  
**Average/worst case**: O(n log n).  
**Stable and adaptive**: exploits existing order in the data.  
**Used in**: Python, Java (Arrays.sort for objects), Android, V8 (JavaScript engine).

### The Lower Bound Proof

**Theorem**: any comparison-based sort requires Ω(n log n) comparisons in the worst case.

**Proof sketch**: think of all possible orderings of n elements — there are n! of them. Each comparison eliminates at most half the remaining possibilities (binary decision tree with n! leaves). The tree has height at least log₂(n!) ≈ n log n (Stirling's approximation). Therefore, at least n log n comparisons are needed in the worst case. □

No comparison sort can do better. Mergesort and Heapsort achieve this bound.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Sort Race**
- Array of 50 random integers
- Run Bubble Sort, Merge Sort, Quick Sort simultaneously
- Watch each algorithm sort in real time, colour-coding comparisons and swaps
- Compare final step counts

**Tool 2 — Merge Sort Tree**
- See the divide phase: array split recursively into halves
- See the conquer phase: merges happening level by level
- Count comparisons at each level

**Tool 3 — Quicksort Partition**
- Choose pivot strategy: last element, first element, random, median-of-three
- Run on sorted, reverse-sorted, and random input
- Observe how pivot choice affects the partition balance and total steps

---

## Going Deeper

**External sorting**: what if the data doesn't fit in RAM? Sorting 1 TB on a machine with 16 GB RAM requires a disk-based sort. The standard approach: (1) split into 16 GB chunks, sort each in memory, write to disk; (2) merge all chunks using a k-way merge with a priority queue. This is how databases sort large result sets. The I/O cost dominates, not the CPU cost.

**Sorting networks**: fixed circuits (no data-dependent branching) that sort n elements in parallel. Used in hardware (GPUs sort using sorting networks) and for small n where branch misprediction is costly. Batcher's odd-even merge sort produces a sorting network with O(n log² n) comparators.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace Merge Sort on an 8-element array step by step, identify the worst-case input for naive Quicksort, implement counting sort for small integers, and prove the information-theoretic lower bound for n=3 by drawing the full decision tree.
