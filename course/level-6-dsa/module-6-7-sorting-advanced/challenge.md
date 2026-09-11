# Challenge 6.7 — Sorting: Merge, Quick, Radix

**Type:** Trace + implementation + analysis  
**Estimated time:** 50–60 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — Merge Sort Full Trace

Sort `[5, 3, 8, 1, 9, 2, 7, 4]` using merge sort.

1. Draw the complete **recursion tree**: show every split and every merge, with the sub-array contents at each node.

2. Count exact comparisons per merge operation. Sum to get the total. Compare to the theoretical bound n log n.

3. Implement **bottom-up merge sort** (iterative, no recursion): start with sub-arrays of width 1, merge to width 2, then 4, then 8. Show the array state after each pass.

4. Merge sort is **stable**. Demonstrate: sort `[(B,3), (A,3), (C,1), (D,2)]` by the second element. Verify equal-second-element items maintain their original relative order in the output.

---

## Part B — Quicksort Partition

5. Implement the **Lomuto partition** (last element as pivot). Trace it on `[3, 7, 8, 5, 2, 1, 9, 5, 4]` with pivot=4: show the state of the array after every swap.

6. Implement the **Hoare partition** (two converging pointers, first element as pivot). Trace it on the same array with pivot=3.

7. **Three-way partition (DNF)**: partition `[3, 1, 3, 3, 2, 3, 1]` around pivot=3. After one partition pass, nothing in the "equal to pivot" region is ever recursed into. Show the three regions and count the comparisons.

8. For an array of n identical elements, three-way quicksort runs in O(n). Prove this: after one call to the 3-way partition, how many elements remain to be sorted?

---

## Part C — Radix Sort

9. Sort `[329, 457, 657, 839, 436, 720, 355]` using **LSD radix sort** (base 10). Show the array state after sorting by each digit (ones, tens, hundreds).

10. Radix sort uses counting sort as a subroutine. Show the counting sort array for the **ones digit** of the above array.

11. For 32-bit unsigned integers using base 256: how many passes does radix sort make? Calculate the total number of operations for n = 1,000,000 integers and compare to n log₂(n).

12. Why does LSD radix sort require a **stable** subroutine sort at each digit pass? Construct a counterexample showing what goes wrong with an unstable subroutine.

---

## Part D — Sorting Algorithm Selection

For each scenario, choose the best sorting algorithm and justify your choice:

13. Sort 1,000,000 random 64-bit integers. Memory is not a concern.

14. Sort a nearly-sorted array of 100,000 strings where at most 5% of elements are out of place.

15. Sort 50,000,000 network log entries where the sort key is a 4-byte source IP address (integer ∈ [0, 2³²)).

16. Sort a small array of exactly 8 elements inside a tight loop that executes 10,000,000 times. Latency matters more than throughput.

17. Sort a 100 GB file on disk that cannot fit in RAM. RAM limit: 8 GB.

---

## Part E — Comparison Lower Bound

18. For n=4 elements, the minimum number of comparisons needed (in the worst case) to sort them is 5. Show a sorting network (a fixed sequence of comparisons) that sorts any 4 elements in exactly 5 comparisons.

---

## Rubric

| Part | Points |
|---|---|
| A merge sort trace | 24 |
| B quicksort partitions | 28 |
| C radix sort | 24 |
| D algorithm selection | 14 |
| E lower bound | 10 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part C.11 — radix sort operation count</summary>

Base 256 passes: ⌈32/8⌉ = 4 passes. Each pass = O(n + 256) = O(n) for large n.
Total: 4n ≈ 4 × 10⁶ = 4,000,000 operations.
n log₂(n) for n=10⁶: 10⁶ × 20 = 20,000,000.
Radix sort is 5× fewer operations — but cache behaviour and constant factors matter in practice.
</details>

<details>
<summary>Part D answers</summary>

13. Introsort (std::sort equivalent): Quicksort average O(n log n) with fallback to Heapsort for guaranteed O(n log n).
14. Timsort: exploits nearly-sorted runs, near-O(n) in this case.
15. Radix sort: key is 32-bit integer, O(n) with 4 passes at base 256.
16. Insertion sort or sorting network: for n=8, insertion sort has very low overhead; sorting networks have 0 branch mispredictions.
17. External merge sort: sort 8 GB chunks in RAM, write to disk, merge k sorted files using a k-way heap merge.
</details>
