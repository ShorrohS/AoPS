# Module 6.5 — Heaps and Priority Queues

---

## The Problem

> You are managing a hospital emergency room.
> Patients arrive continuously, each with a severity score.
> At any moment, the next patient to be treated should be the one with the highest severity — not the one who arrived first, and not a random one.
>
> This is the **priority queue** problem: a collection where we always want efficient access to the *minimum* (or *maximum*) element.
>
> An unsorted array gives O(n) for "find the minimum" — too slow.
> A sorted array gives O(1) for "find the minimum" but O(n) for insert — still too slow.
> A heap gives O(log n) for both insert and extract-min, with O(1) find-min.

---

## The Story

### Heapsort and Priority Queues

The heap data structure was invented by **J. W. J. Williams** in 1964, in the same paper that introduced Heapsort. Williams needed a data structure that could both maintain a partially-sorted order and allow efficient extraction of the maximum element — essentially a priority queue. The key insight was to store the structure as a binary tree implicitly in an array, using index arithmetic instead of pointers.

**Robert Floyd** (1964) improved the heap construction algorithm from O(n log n) to O(n) in the same year — a beautiful result showing that you can build a heap from an arbitrary array in linear time by "heapifying" from the bottom up rather than inserting elements one by one.

Heaps are used pervasively in systems software: Linux's Completely Fair Scheduler uses a red-black tree (a tree with heap-like properties) to manage processes. Dijkstra's algorithm, first described in 1959, uses a priority queue (typically a heap) to always expand the nearest unvisited node.

---

## The Concept

### The Heap Property

A **binary heap** is a complete binary tree (every level filled except possibly the last, filled left to right) satisfying the **heap property**:

**Max-heap**: every node's value ≥ its children's values. The maximum is always at the root.  
**Min-heap**: every node's value ≤ its children's values. The minimum is always at the root.

```
Max-heap example:
        90
       /  \
      80   70
     / \  / \
    50  60 40 30
   / \
  20  10
```

### Array Representation — No Pointers Needed

A complete binary tree maps to an array without any pointers:

```
Index:   0   1   2   3   4   5   6   7   8
Value:  [90, 80, 70, 50, 60, 40, 30, 20, 10]

For node at index i:
  Parent:       (i - 1) // 2
  Left child:   2*i + 1
  Right child:  2*i + 2
```

This is elegant: the heap is just an array, and all navigation is index arithmetic. Cache-friendly, zero pointer overhead.

### Core Operations

**peek_max()** / **peek_min()**: return `heap[0]`. **O(1)**.

**insert(x)** — "sift up" (also called "bubble up"):
1. Append x to end of array (at position `n`)
2. While x is greater than its parent and we're not at root:
   - Swap x with parent
   - Move up (i = parent index)
3. Heap property restored. **O(log n)** — tree height.

```python
def insert(heap, x):
    heap.append(x)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[i] > heap[parent]:      # max-heap condition
            heap[i], heap[parent] = heap[parent], heap[i]
            i = parent
        else:
            break
```

**extract_max()** — "sift down" (also called "heapify down"):
1. Root (maximum) is the answer to return
2. Move last element to root (to fill the gap)
3. While root is less than either child:
   - Swap with the larger child
   - Move down
4. Return the original root. **O(log n)**.

```python
def extract_max(heap):
    if not heap: raise IndexError
    max_val = heap[0]
    heap[0] = heap.pop()    # move last to root
    # sift down
    i = 0
    n = len(heap)
    while True:
        left, right = 2*i+1, 2*i+2
        largest = i
        if left < n and heap[left] > heap[largest]:   largest = left
        if right < n and heap[right] > heap[largest]: largest = right
        if largest == i: break
        heap[i], heap[largest] = heap[largest], heap[i]
        i = largest
    return max_val
```

**build_heap(arr)** — Floyd's algorithm, **O(n)**:

Rather than inserting n elements one by one (O(n log n)), start from the last non-leaf and sift down every internal node:

```python
def build_heap(arr):
    n = len(arr)
    for i in range((n-2)//2, -1, -1):    # start from last non-leaf
        sift_down(arr, i, n)
    return arr
```

The O(n) analysis: most nodes are near the bottom of the tree and need to sift down very few levels. The total work is bounded by the sum of heights, which is O(n) (geometric series).

### Python's heapq Module

Python provides a **min-heap** implementation:

```python
import heapq

heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 3)
heapq.heappush(heap, 8)
heapq.heappush(heap, 1)

print(heapq.heappop(heap))   # 1 (minimum)
print(heapq.heappop(heap))   # 3

# Build heap in O(n):
data = [5, 3, 8, 1, 9, 2]
heapq.heapify(data)          # in-place, O(n)

# nlargest and nsmallest:
heapq.nlargest(3, data)      # [9, 8, 5]
heapq.nsmallest(2, data)     # [1, 2]
```

For a max-heap in Python, negate values: push `-x` and negate on pop.

### Heapsort — O(n log n) In-Place

```python
def heapsort(arr):
    # Step 1: build max-heap O(n)
    n = len(arr)
    for i in range((n-2)//2, -1, -1):
        sift_down(arr, i, n)
    # Step 2: extract max n times O(n log n)
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]   # swap max to end
        sift_down(arr, 0, i)               # restore heap on remaining
```

Heapsort is in-place (O(1) extra space) and always O(n log n). In practice it is slower than Quicksort due to poor cache behaviour — elements are accessed in a tree pattern rather than sequentially.

### The Priority Queue as an Interface

The heap implements the **priority queue abstract data type** (ADT):
- `insert(item, priority)` — add item with given priority
- `extract_min()` / `extract_max()` — remove and return highest-priority item
- `decrease_key(item, new_priority)` — lower the priority of an existing item (needed for Dijkstra's)

**Applications**:
- **Dijkstra's shortest path**: priority queue of (distance, node) — always expand the nearest unvisited node
- **A\* search**: priority queue of (f-score, node) — expand most promising node first
- **Huffman coding**: extract the two smallest-frequency symbols to merge
- **k-way merge**: merge k sorted lists using a min-heap of (current_element, list_index)
- **Event simulation**: process events in time order using a min-heap of (time, event)

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Heap Visualiser**
- Insert elements and watch the array representation and tree diagram update simultaneously
- Step through each sift-up operation after insert
- Step through each sift-down operation after extract

**Tool 2 — Floyd's Build**
- Enter an arbitrary array
- Watch Floyd's algorithm transform it into a valid heap in O(n)
- Compare to inserting one by one (O(n log n))

**Tool 3 — Priority Queue Simulation**
- Patients arrive with random severity scores
- Enqueue each patient
- Dequeue the highest-severity patient
- Observe the heap maintain order throughout

---

## Going Deeper

**Fibonacci heaps**: a more complex heap structure that achieves O(1) amortised insert and decrease-key (vs O(log n) for binary heaps). This reduces Dijkstra's complexity from O((V+E) log V) to O(E + V log V) — significant for dense graphs. In practice, Fibonacci heaps have high constant factors and are rarely used in real implementations.

**d-ary heaps**: a heap where each node has d children (instead of 2). Larger d means faster decrease-key (fewer levels to sift) but slower extract-min (more children to compare). For Dijkstra's on graphs with many edge relaxations, a 4-heap or 8-heap often outperforms a binary heap.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace `insert(7)` into a max-heap, trace `extract_max()` step by step, implement a priority queue using Python's `heapq` module, and use a heap to find the k-th largest element in an unsorted array.
