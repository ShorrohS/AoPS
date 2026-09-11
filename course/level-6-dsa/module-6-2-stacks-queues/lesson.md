# Module 6.2 — Stacks and Queues

---

## The Problem

> Two fundamental questions about collections:
>
> 1. When you take something out, should it be the *most recently added* item (Last In, First Out)?
>    → A stack of plates, the call stack, the browser back button.
>
> 2. Or should it be the *least recently added* item (First In, First Out)?
>    → A print queue, a line at a ticket counter, CPU job scheduling.
>
> Stacks and queues are not clever data structures.
> They are principled *restrictions* on how a collection is accessed —
> and those restrictions turn out to match the natural structure of dozens of important problems.

---

## The Story

### The Call Stack and the History of Stacks

The concept of a stack in computing is inseparable from the call stack — the hardware mechanism for function calls described in Module 4.2. Every time you call a function, the return address is pushed; every time you return, it is popped. This is a stack in its purest form.

Alan Turing described stack-like mechanisms in 1946 for his ACE computer design. Friedrich Bauer and Klaus Samelson in Germany, and Charles Hamblin in Australia, independently formalised the push-down stack in the late 1950s.

The calculator application of stacks came from Hamblin: **Reverse Polish Notation (RPN)** — write `3 4 +` instead of `3 + 4`. RPN evaluates perfectly with a stack and requires no parentheses, no operator precedence rules, no parse tree. HP's engineering calculators used RPN through the 1970s–80s. Understanding why RPN works is the clearest introduction to stack-based computation.

Queues formalise the fair waiting structure that humans already understood intuitively — but computers needed an explicit data structure to implement scheduling, buffering, and breadth-first search.

---

## The Concept

### Stacks — LIFO

A stack supports two operations:
- **push(item)**: add item to the top
- **pop()**: remove and return the top item
- **peek()**: look at the top item without removing it
- **is_empty()**: return True if no items

```python
class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)       # O(1) amortised

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()       # O(1) amortised

    def peek(self):
        return self._data[-1]         # O(1)

    def is_empty(self):
        return len(self._data) == 0
```

All operations O(1) amortised using a dynamic array as backing store.

**Key applications:**

**Expression evaluation** (RPN):
```python
def eval_rpn(tokens):
    stack = Stack()
    for t in tokens:
        if t in '+-*/':
            b, a = stack.pop(), stack.pop()
            result = {'+':a+b, '-':a-b, '*':a*b, '/':a/b}[t]
            stack.push(result)
        else:
            stack.push(float(t))
    return stack.pop()

eval_rpn(['3','4','+','2','*'])   # (3+4)*2 = 14
```

**Balanced parentheses check**:
```python
def is_balanced(s):
    stack = Stack()
    pairs = {')':'(', ']':'[', '}':'{'}
    for c in s:
        if c in '([{':
            stack.push(c)
        elif c in ')]}':
            if stack.is_empty() or stack.pop() != pairs[c]:
                return False
    return stack.is_empty()

is_balanced("({[]})")   # True
is_balanced("({[}])")   # False
```

**Undo/redo**: push each action onto the undo stack. `Ctrl+Z` pops from the undo stack and pushes onto the redo stack.

**DFS without recursion**:
```python
def dfs(graph, start):
    stack = Stack()
    visited = set()
    stack.push(start)
    while not stack.is_empty():
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbour in graph[node]:
                stack.push(neighbour)
```

### Queues — FIFO

A queue supports:
- **enqueue(item)**: add item to the back
- **dequeue()**: remove and return the front item
- **peek()**: look at the front item
- **is_empty()**

Implementing a queue with a Python list is inefficient: `list.pop(0)` is O(n) because it shifts every element. Use Python's `collections.deque` (doubly linked list):

```python
from collections import deque

class Queue:
    def __init__(self):
        self._data = deque()

    def enqueue(self, item):
        self._data.append(item)         # O(1)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()     # O(1)

    def is_empty(self):
        return len(self._data) == 0
```

**Key applications:**

**BFS (Breadth-First Search)**:
```python
def bfs(graph, start):
    queue = Queue()
    visited = set([start])
    queue.enqueue(start)
    while not queue.is_empty():
        node = queue.dequeue()
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.enqueue(neighbour)
```

**Process scheduling**: the OS maintains a run queue of processes waiting for CPU time. Round Robin scheduling enqueues a process when its turn ends and dequeues the next one.

**Printer spooler**: jobs arrive and are enqueued. The printer dequeues and prints one at a time.

### Circular Buffer (Ring Buffer)

A fixed-size queue implemented as an array with two pointers (`head` and `tail`). When they reach the end of the array, they wrap around. No dynamic resizing needed:

```
Array: [_, _, 3, 4, 5, _, _]   (size 7)
            ↑           ↑
           head         tail (next write position)
```

Used in: audio buffers (steady stream of samples), network packet buffers, producer-consumer queues in embedded systems. O(1) enqueue and dequeue with a fixed, pre-allocated memory footprint.

### Monotonic Stack

A stack where elements are always in sorted order (either monotonically increasing or decreasing). Used to solve problems like "next greater element" in O(n):

```python
def next_greater_element(arr):
    result = [-1] * len(arr)
    stack = []                    # stores indices
    for i, x in enumerate(arr):
        while stack and arr[stack[-1]] < x:
            idx = stack.pop()
            result[idx] = x       # x is the next greater for arr[idx]
        stack.append(i)
    return result

next_greater_element([4, 1, 2, 3])   # [-1, 2, 3, -1]
```

The naïve nested loop approach is O(n²). The monotonic stack approach is O(n) — each element is pushed and popped at most once.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Stack Operations**
- Push and pop items manually
- Visualise the stack growing and shrinking
- Run the balanced parentheses checker step by step
- Watch RPN expression evaluation

**Tool 2 — Queue Operations**
- Enqueue and dequeue items
- Visualise the front and back pointers
- Run BFS on a small graph and watch the queue guide the traversal

**Tool 3 — Circular Buffer**
- Set a fixed buffer size
- Enqueue items until full, then dequeue and enqueue again
- Watch head and tail pointers wrap around
- Observe what happens on overflow

---

## Going Deeper

**Priority queues**: a generalisation of the queue where each item has a priority, and `dequeue()` always returns the highest-priority item. Implemented with a heap (Module 6.5). Used in: Dijkstra's shortest path, A* search, OS task scheduling, Huffman coding, event-driven simulation.

**Lock-free queues**: in multi-threaded systems, locking a queue for every enqueue/dequeue creates a bottleneck. Lock-free queues use CPU atomic compare-and-swap (CAS) instructions to safely update head/tail pointers without locks. Michael and Scott's lock-free queue (1996) is the standard algorithm — it uses a sentinel node and a pair of atomic pointer updates. Used in high-performance message queues, garbage collectors, and OS schedulers.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Implement a stack using two queues, implement a queue using two stacks, evaluate RPN expressions step by step, and trace a BFS traversal on a given graph recording the queue state at each step.
