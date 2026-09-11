# Challenge 5.2 — Python: Abstraction for Humans

**Type:** Implementation + trace + reasoning  
**Estimated time:** 45–55 minutes  
**Tools needed:** Python interpreter (or `simulation.html`)

---

## Part A — Linked List in Python

Implement a singly linked list class with the following interface:

```python
class Node:
    def __init__(self, data, next=None): ...

class LinkedList:
    def __init__(self): ...
    def append(self, data): ...       # add to tail — O(n) acceptable
    def prepend(self, data): ...      # add to head — O(1)
    def delete(self, data): ...       # remove first occurrence
    def __iter__(self): ...           # enable: for x in linked_list
    def __repr__(self): ...           # e.g., "1 → 2 → 3 → None"
```

1. Implement the class. Test with: `ll = LinkedList(); ll.append(1); ll.append(2); ll.prepend(0); ll.delete(1); print(ll)` → should print `0 → 2 → None`.

2. What is the time complexity of `append`? How would you make it O(1)?

3. Write a `reverse()` method that reverses the list in-place (no new nodes created). What is its time complexity?

---

## Part B — Timing Decorator

Write a `@timer` decorator that:
- Times any function it wraps
- Prints `"function_name took X.XXXXs"`
- Returns the function's original return value unchanged

```python
@timer
def slow_sort(lst):
    import time; time.sleep(0.1)
    return sorted(lst)

result = slow_sort([3, 1, 2])
# slow_sort took 0.1003s
# result == [1, 2, 3]
```

4. Implement the decorator. Handle functions with any number of positional and keyword arguments.

5. How do you preserve the wrapped function's `__name__` and `__doc__`? Why does this matter?

6. Extend the decorator to accept a parameter: `@timer(unit='ms')` that prints time in milliseconds instead of seconds.

---

## Part C — Reference Counting

Trace the reference count of each object through this sequence:

```python
a = [1, 2, 3]    # (1)
b = a             # (2)
c = [a, a]        # (3)
del a             # (4)
b[0] = 99         # (5)
print(c)          # (6)
del b             # (7)
del c             # (8)
```

7. After line (2): what is the reference count of the list `[1, 2, 3]`?
8. After line (3): what is the reference count?
9. After line (4): what is the reference count? Is the list freed?
10. What does line (6) print? Why? (Think about what `c` contains.)
11. After lines (7) and (8): what happens to the list? Why?

---

## Part D — Mutability and Aliasing

```python
def add_item(lst, item, default=[]):   # BUG
    default.append(item)
    lst.append(default)

results = []
add_item(results, 1)
add_item(results, 2)
add_item(results, 3)
print(results)
```

12. What does `print(results)` actually output? Explain why, referencing how Python handles default argument evaluation.

13. What was the programmer's intent? Rewrite the function correctly.

14. Explain the difference between these two operations:
    ```python
    a = [1, 2, 3]
    b = a          # case 1
    b = a[:]       # case 2 (slice copy)
    b = a.copy()   # case 3
    ```
    In which case does modifying `b` affect `a`? Why?

---

## Part E — Python Internals

15. Why does this produce `True` in CPython but is not guaranteed by the language spec?
    ```python
    a = 256
    b = 256
    print(a is b)   # True
    a = 257
    b = 257
    print(a is b)   # False (usually)
    ```
    What is CPython's integer interning range? What does `is` test vs `==`?

16. Explain why Python's `dict` preserves insertion order (since Python 3.7) while a hash table normally does not. What does Python's implementation do differently?

17. What is the GIL? Give one scenario where threads run concurrently despite the GIL, and one where they don't.

---

## Rubric

| Part | Points |
|---|---|
| A linked list (3 questions) | 25 |
| B timer decorator (3 questions) | 25 |
| C reference counting (5 questions) | 25 |
| D mutability (3 questions) | 15 |
| E internals (3 questions) | 10 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A — Linked List</summary>

```python
class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None

    def prepend(self, data):
        self.head = Node(data, self.head)

    def append(self, data):
        if not self.head:
            self.head = Node(data); return
        curr = self.head
        while curr.next: curr = curr.next
        curr.next = Node(data)

    def delete(self, data):
        if not self.head: return
        if self.head.data == data:
            self.head = self.head.next; return
        curr = self.head
        while curr.next:
            if curr.next.data == data:
                curr.next = curr.next.next; return
            curr = curr.next

    def __iter__(self):
        curr = self.head
        while curr: yield curr.data; curr = curr.next

    def __repr__(self):
        return ' → '.join(str(x) for x in self) + ' → None'

    def reverse(self):
        prev, curr = None, self.head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr; curr = nxt
        self.head = prev
```
</details>

<details>
<summary>Part B — Timer decorator</summary>

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

# Parametrised version
def timer(unit='s'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            val = elapsed * 1000 if unit == 'ms' else elapsed
            print(f"{func.__name__} took {val:.4f}{unit}")
            return result
        return wrapper
    return decorator
```
</details>

<details>
<summary>Part C — Reference counting answers</summary>

After (1): refcount = 1. After (2): refcount = 2. After (3): refcount = 4 (b + c[0] + c[1] + still a). After (4) del a: refcount = 3 (b + c[0] + c[1]). Not freed.

Line (6): `c` contains two references to the SAME list object, which now has `b[0]` = 99. Output: `[[99, 2, 3], [99, 2, 3]]`.

After del b (refcount=2) and del c (refcount=0): list is freed immediately.
</details>

<details>
<summary>Part D</summary>

12. Output: `[[[1], [1, 2], [1, 2, 3]]]`... Actually: `results = [[1], [1, 2], [1, 2, 3]]`. All three inner lists are THE SAME list object, each modified by successive calls. The default list `[]` is evaluated once at function definition time, not each call.

13. Correct version:
```python
def add_item(lst, item, default=None):
    if default is None: default = []
    default.append(item)
    lst.append(default)
```
But if the intent was a fresh list each call: `lst.append([item])`.

14. Case 1 (`b = a`): same object. Modifying `b` modifies `a`. Case 2 and 3: shallow copy — new list object. Modifying `b` does not affect `a` (for non-nested lists).
</details>
