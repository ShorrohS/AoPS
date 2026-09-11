# Challenge 5.6 — Searching: Finding What You Need

**Type:** Trace + implementation + analysis  
**Estimated time:** 40–50 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — Binary Search Trace

Sort the array `[2, 5, 8, 12, 16, 23, 38, 44, 56, 72, 91]` (11 elements, indices 0–10).

1. Trace binary search for target = **38**: show `low`, `high`, and `mid` at each step, and which half is eliminated.

2. Trace binary search for target = **50** (not present): show every step until `low > high`.

3. Binary search on a 1-billion-element sorted array requires at most how many comparisons? Show the calculation.

4. At what value of n does linear search (average case n/2 comparisons) become slower than binary search (worst case log₂n comparisons)?

---

## Part B — Binary Search Variants

Implement these three variants on a sorted array that may contain duplicates:

```python
arr = [1, 2, 2, 2, 3, 4, 4, 5]
```

5. `find_first(arr, target)` — returns the index of the **first** occurrence of target, or -1. Show that `find_first(arr, 2)` returns 1.

6. `find_last(arr, target)` — returns the index of the **last** occurrence. Show that `find_last(arr, 2)` returns 3.

7. `count_occurrences(arr, target)` — count occurrences in O(log n). Use `find_first` and `find_last`. Show that `count_occurrences(arr, 4)` returns 2.

8. `insertion_point(arr, target)` — return the index where target should be inserted to keep the array sorted (like `bisect_left`). Show result for target=3 and target=2.5.

---

## Part C — Binary Search on the Answer

A worker can complete `speed` tasks per hour. You need to complete `n` tasks in at most `hours` hours. Find the **minimum speed** (integer tasks/hour) required.

```python
def min_speed(tasks, hours):
    """
    tasks: list of task counts, each processed at 'speed' per hour
    (rounded up to whole hours per task)
    Return minimum integer speed such that sum of ceil(t/speed) <= hours.
    """
    # Example: tasks=[3,6,7,11], hours=8
    # speed=4: ceil(3/4)+ceil(6/4)+ceil(7/4)+ceil(11/4) = 1+2+2+3 = 8 ≤ 8 ✓
    # speed=3: ceil(3/3)+ceil(6/3)+ceil(7/3)+ceil(11/3) = 1+2+3+4 = 10 > 8 ✗
```

9. What is the search space for `speed`? (minimum and maximum values)

10. Implement `min_speed` using binary search on the answer. Clearly show:
    - The feasibility function `can_finish(speed, tasks, hours)`
    - The binary search loop with correct boundary conditions

11. What is the time complexity? (let m = max(tasks), n = len(tasks))

---

## Part D — Trie for Prefix Search

Build a trie by inserting: `"cat"`, `"car"`, `"card"`, `"care"`, `"bat"`.

12. Draw the trie. Label each node with its character. Mark which nodes are word endings.

13. How many nodes does your trie have? How would this scale if you inserted 100,000 English words?

14. Implement a `Trie` class with `insert(word)` and `starts_with(prefix)` → returns list of all words with that prefix.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end   = False

class Trie:
    def insert(self, word): ...
    def starts_with(self, prefix): ...   # returns list of matching words
```

15. What is the time complexity of `starts_with` in terms of prefix length p and number of matching words k?

---

## Part E — When Linear Beats Binary

16. For what value of n does binary search (on sorted data) perform **fewer operations overall** than linear search (on unsorted data), given that sorting the array first takes O(n log n)?

    If you need to search the array only **once**, which is faster?
    If you search the array **k times**, at what k does sorting + binary search become worthwhile?

---

## Rubric

| Part | Points |
|---|---|
| A binary search trace | 20 |
| B variants | 28 |
| C answer space binary search | 24 |
| D trie | 20 |
| E analysis | 8 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1 — trace target=38</summary>

low=0, high=10, mid=5 → arr[5]=23 < 38 → low=6
low=6, high=10, mid=8 → arr[8]=56 > 38 → high=7
low=6, high=7,  mid=6 → arr[6]=38 = 38 → return 6. (3 comparisons)
</details>

<details>
<summary>Part B.5–8 implementations</summary>

```python
def find_first(arr, target):
    low, high, res = 0, len(arr)-1, -1
    while low <= high:
        mid = (low+high)//2
        if arr[mid] == target: res=mid; high=mid-1
        elif arr[mid] < target: low=mid+1
        else: high=mid-1
    return res

def find_last(arr, target):
    low, high, res = 0, len(arr)-1, -1
    while low <= high:
        mid = (low+high)//2
        if arr[mid] == target: res=mid; low=mid+1
        elif arr[mid] < target: low=mid+1
        else: high=mid-1
    return res

def count_occurrences(arr, target):
    f, l = find_first(arr,target), find_last(arr,target)
    return 0 if f==-1 else l-f+1

def insertion_point(arr, target):
    low, high = 0, len(arr)
    while low < high:
        mid=(low+high)//2
        if arr[mid] < target: low=mid+1
        else: high=mid
    return low
```
</details>

<details>
<summary>Part C.10 — min_speed</summary>

```python
import math
def min_speed(tasks, hours):
    def can_finish(speed):
        return sum(math.ceil(t/speed) for t in tasks) <= hours

    low, high = 1, max(tasks)
    while low < high:
        mid = (low+high)//2
        if can_finish(mid): high=mid
        else: low=mid+1
    return low
```

O(n log m): log m binary search steps, each O(n) feasibility check.
</details>

<details>
<summary>Part E</summary>

Single search: linear O(n) < sort O(n log n) + binary O(log n). Linear wins.

k searches: sort cost O(n log n) is paid once. After that, k binary searches = O(k log n). Break-even: k log n < k×(n/2), roughly k > n log n / (n/2 - log n) ≈ 2 log n for large n. For n=1000: break-even at about k ≈ 20 searches.
</details>
