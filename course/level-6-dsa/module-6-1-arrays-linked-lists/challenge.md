# Challenge 6.1 — Arrays and Linked Lists

**Type:** Implementation + trace + analysis  
**Estimated time:** 45–55 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — Linked List Implementation

Implement a singly linked list with these methods:

```python
class Node:
    def __init__(self, data): ...

class LinkedList:
    def prepend(self, data): ...      # O(1)
    def append(self, data): ...       # O(n) — no tail pointer
    def delete(self, data): ...       # remove first occurrence
    def reverse(self): ...            # in-place, O(n)
    def to_list(self): ...            # convert to Python list
```

1. Implement all five methods. Test: `ll = LinkedList(); [ll.append(i) for i in [1,2,3,4]]; ll.reverse(); print(ll.to_list())` → `[4,3,2,1]`.

2. Trace `reverse()` on `[1→2→3→4→None]` step by step. Draw the pointer state after each reassignment.

3. What three operations on a singly linked list require O(n) time? For which of these could a doubly linked list help? When?

---

## Part B — Memory Layout Calculation

4. A Python list (`[]`) stores object **references** (pointers). Each pointer is 8 bytes on 64-bit systems, plus the list object overhead of 56 bytes. Calculate the memory used by a Python list of 1,000 integers.

5. A singly linked list of 1,000 Python integers: each `Node` has a `data` field and a `next` pointer. Python object overhead is ~28 bytes per Node object plus 8 bytes per pointer field. Estimate total memory.

6. Which uses more memory for 1,000 elements, and by roughly how much? What does this suggest about when to prefer each structure?

---

## Part C — Dynamic Array Internals

7. A Python list starts empty. Trace the capacity at each step after appending elements 1 through 9. (Python doubles capacity starting from some initial value when the list is full.) What is the capacity after each append?

8. n appends to an initially empty list cost O(2n) total (geometric series). Prove this: if the list doubles from size k to 2k, the cost of that resize is k copies. Sum all resize costs for n appends.

9. Implement a `DynamicArray` class in Python that manages its own backing array (use a fixed-size list pre-allocated to `capacity`). When full, double the capacity and copy. Include `append`, `__getitem__`, and `__len__`.

---

## Part D — Practical Choice

For each scenario, state whether you would use a dynamic array or linked list, and why:

10. A undo/redo history for a text editor where the most recent 1,000 actions are stored and you frequently add/remove from the front.

11. A database result set of 10 million rows that will be iterated once from beginning to end and accessed by index.

12. A scheduler that processes jobs in order of arrival, inserting new jobs at the back and removing from the front, with at most 10,000 jobs at any time.

13. A cache of the 100 most recently accessed web pages where you need to move an accessed page to the front in O(1).

---

## Part E — Classic Linked List Problems

14. **Detect a cycle**: given a linked list, determine if it contains a cycle (a node whose `next` points to an earlier node). Implement **Floyd's tortoise and hare algorithm** — two pointers moving at speeds 1 and 2. If they ever point to the same node, there is a cycle.

15. **Find the middle node**: return the middle node of a linked list in a single pass (no pre-computing the length). Use slow/fast pointers. For even-length lists, return the second of the two middle nodes.

16. **Merge two sorted linked lists**: given `l1 = 1→3→5→None` and `l2 = 2→4→6→None`, return `1→2→3→4→5→6→None`. Implement this recursively and iteratively. What are the time and space complexities of each?

---

## Rubric

| Part | Points |
|---|---|
| A linked list (3 questions) | 25 |
| B memory layout | 15 |
| C dynamic array | 20 |
| D practical choice | 16 |
| E classic problems | 24 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.2 — reverse trace</summary>

```
Initial: head → [1] → [2] → [3] → [4] → None

Step 1: prev=None, curr=[1], nxt=[2]
  [1].next = None; prev=[1]; curr=[2]
  State: None ← [1]   [2] → [3] → [4] → None

Step 2: prev=[1], curr=[2], nxt=[3]
  [2].next = [1]; prev=[2]; curr=[3]
  State: None ← [1] ← [2]   [3] → [4] → None

Step 3: prev=[2], curr=[3], nxt=[4]
  [3].next = [2]; prev=[3]; curr=[4]

Step 4: prev=[3], curr=[4], nxt=None
  [4].next = [3]; prev=[4]; curr=None

head = [4]; done.
Result: [4] → [3] → [2] → [1] → None
```
</details>

<details>
<summary>Part C.9 — DynamicArray</summary>

```python
class DynamicArray:
    def __init__(self):
        self._capacity = 1
        self._size = 0
        self._data = [None] * self._capacity

    def _resize(self):
        new_data = [None] * (self._capacity * 2)
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity *= 2

    def append(self, val):
        if self._size == self._capacity:
            self._resize()
        self._data[self._size] = val
        self._size += 1

    def __getitem__(self, i):
        if 0 <= i < self._size: return self._data[i]
        raise IndexError

    def __len__(self): return self._size
```
</details>

<details>
<summary>Part E.14 — Floyd's cycle detection</summary>

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast: return True
    return False
```

If there's a cycle of length k, and the cycle starts at position m from the head: the fast pointer enters the cycle first. Once both are in the cycle, fast gains 1 position per step. They meet after at most k steps.
</details>
