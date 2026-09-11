# Challenge 6.5 — Heaps and Priority Queues

**Type:** Trace + implementation + application  
**Estimated time:** 45–55 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — Heap Operations

Start with this **max-heap** (array representation): `[90, 80, 70, 50, 60, 40, 30, 20, 10]`

Indices: 0=90, 1=80, 2=70, 3=50, 4=60, 5=40, 6=30, 7=20, 8=10

1. **Insert 85**: trace the sift-up operation. Show the array after every swap.

2. **Extract-max**: remove the maximum (90). Show every swap in the sift-down operation. What is the final array?

3. What is the height of a max-heap containing n elements? Express as a function of n.

4. For n=1,000,000 elements, what is the maximum number of swaps for a single `insert` or `extract-max`?

---

## Part B — Floyd's Build-Heap

Given the arbitrary array `[3, 9, 2, 1, 4, 5, 8, 7, 6]`, build a max-heap using Floyd's O(n) algorithm (sift down from last non-leaf).

5. Identify the index of the last non-leaf node. (For n=9: `(9-2)//2 = 3`, so index 3.)

6. Trace Floyd's algorithm: sift down from index 3 down to index 0. Show the array after each sift-down operation.

7. **Compare to naive approach**: if you insert each element one by one using the standard O(log n) insert, show the total number of swaps. Compare to Floyd's approach's total swaps.

---

## Part C — Heapsort

8. Apply **heapsort** to `[4, 10, 3, 5, 1]`:
   - Step 1: build a max-heap (show the array)
   - Step 2: repeatedly swap root with last element, sift down on reduced heap
   - Show the array after each swap-and-sift-down

9. Heapsort is in-place but has poor cache behaviour. Explain why: what is the access pattern of sift-down compared to merge sort's sequential access?

---

## Part D — Priority Queue Applications

10. **K-th largest element**: given an unsorted array of n integers, find the k-th largest element in O(n log k) time using a min-heap of size k. Implement this and trace on `arr=[3,2,1,5,6,4], k=2`. The answer is 5.

11. **Merge k sorted lists**: given k sorted lists with a total of n elements, merge them into one sorted list in O(n log k). Use a min-heap of size k. Trace on: `[[1,4,7],[2,5,8],[3,6,9]]`.

12. **Sliding window maximum**: given `arr=[1,3,-1,-3,5,3,6,7]` and window size k=3, find the maximum in each window of size k. The expected output is `[3,3,5,5,6,7]`. Implement using a deque (monotonic decreasing). What is the time complexity?

---

## Part E — Heap Variants

13. A **d-ary heap** has d children per node instead of 2. The height of an n-element d-ary heap is log_d(n). What is the trade-off between d=2 (binary) and d=4 (4-ary) for:
    - Insert (sift-up) time
    - Extract-min (sift-down) time

14. For Dijkstra's algorithm, which is better: a binary heap or a 4-ary heap? The algorithm performs E edge relaxations (decrease-key or insert) and V extract-min operations. Set up the inequality.

---

## Rubric

| Part | Points |
|---|---|
| A heap operations | 24 |
| B Floyd's build-heap | 20 |
| C heapsort | 14 |
| D applications | 30 |
| E heap variants | 12 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1 — insert 85</summary>

Append 85 at index 9. Parent of index 9 = (9-1)//2 = 4 (value 60).
85 > 60 → swap. Array: [90,80,70,50,**85**,40,30,20,10,**60**]
New index=4, parent=(4-1)//2=1 (value 80). 85 > 80 → swap.
Array: [90,**85**,70,50,**80**,40,30,20,10,60]
New index=1, parent=0 (value 90). 85 < 90 → stop.
Final: [90,85,70,50,80,40,30,20,10,60]
</details>

<details>
<summary>Part D.10 — k-th largest</summary>

```python
import heapq

def kth_largest(arr, k):
    heap = []  # min-heap of size k
    for x in arr:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)   # remove smallest, keep k largest
    return heap[0]   # root of min-heap = k-th largest

# Trace on [3,2,1,5,6,4], k=2:
# After 3: heap=[3]
# After 2: heap=[2,3]
# After 1: heap=[2,3] (1 popped immediately)
# After 5: heap=[3,5] (2 popped)
# After 6: heap=[5,6] (3 popped)
# After 4: heap=[5,6] (4 popped)
# Answer: 5 ✓
```
</details>

<details>
<summary>Part D.11 — merge k sorted lists</summary>

```python
import heapq

def merge_k_sorted(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst: heapq.heappush(heap, (lst[0], i, 0))  # (val, list_idx, elem_idx)

    result = []
    while heap:
        val, i, j = heapq.heappop(heap)
        result.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j+1], i, j+1))
    return result
```

Trace on [[1,4,7],[2,5,8],[3,6,9]]:
- Initial heap: [(1,0,0),(2,1,0),(3,2,0)]
- Pop (1,0,0): output 1, push (4,0,1)
- Pop (2,1,0): output 2, push (5,1,1)
- Pop (3,2,0): output 3, push (6,2,1)
- ... continues to produce [1,2,3,4,5,6,7,8,9]
</details>
