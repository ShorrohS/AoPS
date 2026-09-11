# Challenge 5.5 — Sorting: Putting Things in Order

**Type:** Trace + implementation + analysis  
**Estimated time:** 45–55 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — Merge Sort Trace

Sort the array `[5, 3, 8, 1, 9, 2, 7, 4]` using Merge Sort. Show every step.

1. Draw the **divide phase**: show the array split recursively into sub-arrays until you reach single elements.

2. Draw the **merge phase**: show every merge operation, listing the two input sub-arrays and the merged output.

3. Count the total number of comparisons made during all merge operations. Compare to the theoretical bound of n log n = 8 × 3 = 24.

4. Merge Sort is **stable** — equal elements maintain their original relative order. Show why: if two equal elements appear in different halves during a merge, which one ends up first, and why?

---

## Part B — Quicksort Worst Case

5. What input array causes O(n²) behaviour in a Quicksort that always picks the **last element** as pivot? Show the partition sequence for this worst-case input of length 6.

6. What input causes O(n²) behaviour in a Quicksort that always picks the **first element** as pivot?

7. With **randomised pivot** (random element from the sub-array), what is the probability of always choosing the minimum element as pivot for an array of length n? How does this explain why the average case is O(n log n)?

8. Implement 3-way partitioning (Dutch National Flag). Show that `quicksort_3way([3,1,3,3,2,3,1])` runs in O(n) — one partition, elements equal to the pivot are never recursed into.

---

## Part C — Counting Sort

Counting sort is O(n + k) where k is the range of values.

9. Sort `[3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]` using counting sort. Show:
   - The count array after tallying
   - The cumulative count array
   - How each element from the input is placed in the output (right to left for stability)

10. Implement `counting_sort(arr, k)` where k is the maximum value. Return the sorted array.

11. Counting sort requires O(k) space. If the values are in range [0, 10⁹], is counting sort practical? What does this suggest about when to use it?

---

## Part D — The Lower Bound

The O(n log n) lower bound for comparison-based sorting comes from decision trees.

12. For sorting 3 elements {a, b, c}, there are 3! = 6 possible orderings. Draw the decision tree for **insertion sort** on 3 elements:
    - Each internal node is a comparison
    - Each leaf is one of the 6 orderings
    - The tree must have at least 6 leaves

13. What is the **height** of your tree? How does this relate to log₂(6) ≈ 2.58?

14. For n = 4 elements (4! = 24 orderings), the minimum tree height is ⌈log₂(24)⌉ = 5. This means at least 5 comparisons are needed in the worst case for any comparison sort. Verify: does Merge Sort achieve this minimum for n=4?

---

## Part E — Real-World Sorting

15. Python's `list.sort()` uses **Timsort**. Run the following and explain why the output appears before the program ends:

    ```python
    import time

    # Nearly sorted array
    arr1 = list(range(1000)) + [500]   # almost sorted
    arr2 = list(range(1000, 0, -1))    # reverse sorted

    t1 = time.perf_counter()
    sorted(arr1)
    t2 = time.perf_counter()
    sorted(arr2)
    t3 = time.perf_counter()

    print(f"Nearly sorted: {(t2-t1)*1000:.3f}ms")
    print(f"Reverse sorted: {(t3-t2)*1000:.3f}ms")
    ```
    Which is faster? Why? What does Timsort detect?

16. You need to sort 10 million 32-bit integers. The values are uniformly distributed in [0, 10⁶]. Compare Merge Sort vs Radix Sort (base 256, 4 passes) in terms of: number of operations, cache behaviour, memory usage. Which would you choose?

---

## Rubric

| Part | Points |
|---|---|
| A Merge Sort trace | 28 |
| B Quicksort worst case | 24 |
| C Counting Sort | 20 |
| D Lower bound | 18 |
| E Real-world | 10 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.3 — comparison count</summary>

For 8 elements, merge sort makes at most n·log₂(n) = 8·3 = 24 comparisons. The actual count depends on data: merging [1,5] with [2,3] makes 3 comparisons (1<2→take 1; 5>2→take 2; 5>3→take 3; then take 5 without comparison). For random data, the expected count is n·log₂(n) - n + 1 ≈ 17 for n=8.
</details>

<details>
<summary>Part B.5 — worst case pivot sequence</summary>

With last-element pivot, sorted array [1,2,3,4,5,6] is worst case:
- Partition [1,2,3,4,5,**6**]: pivot=6, left=[1,2,3,4,5], right=[]
- Partition [1,2,3,4,**5**]: pivot=5, left=[1,2,3,4], right=[]
- ... each partition produces one sub-array of size n-1
- Total partitions: n-1 = 5. Total comparisons: 5+4+3+2+1 = 15 = O(n²).
</details>

<details>
<summary>Part C.9 — Counting Sort trace</summary>

Array: [3,1,4,1,5,9,2,6,5,3,5], k=9

Count: [0,2,1,2,1,3,1,0,0,1] (index = value, value = count)
Cumulative: [0,2,3,5,6,9,10,10,10,11]

Place elements right to left for stability:
- 5 → cumulative[5]=9, place at index 8 (0-indexed), decrement to 8
- 3 → cumulative[3]=5, place at index 4, decrement to 4
- ... continue for all elements
</details>
