# Module 5.4 — Recursion: Functions That Call Themselves

---

## The Problem

> Some problems are defined in terms of themselves.
> The factorial of n is n times the factorial of n-1.
> The height of a tree is one plus the maximum height of its subtrees.
> The files in a folder include all the files in all its subfolders.
>
> Writing loops to solve these problems forces you to manage explicit stacks,
> state variables, and awkward index arithmetic.
> The code obscures the problem's natural structure.
>
> Recursion expresses these problems directly — the code mirrors the definition.

---

## The Story

### Recursive Thinking Before Computers

Long before programming languages, mathematicians defined functions recursively. **Giuseppe Peano** (1889) defined the natural numbers recursively: 0 is a number; if n is a number, then the successor of n is a number. **Ackermann's function** (1928) was one of the first examples of a function that is computable but not *primitive recursive* — it grows faster than any fixed power of n.

In programming, recursive functions became possible once CPUs had the call stack (Module 4.2). The ability to call a function from within itself, with each call getting its own stack frame, is precisely what makes recursion work. Early languages like FORTRAN (1957) did not support recursion — function calls used a fixed return address, so a function calling itself would overwrite its own return address. ALGOL 60 introduced proper recursion with a hardware-supported call stack.

---

## The Concept

### The Structure of a Recursive Function

Every correct recursive function has two parts:

**Base case**: the simplest input that can be answered directly, without further recursion. Without a base case, the function recurses forever → stack overflow.

**Recursive case**: the function calls itself with a *smaller* version of the problem, moving toward the base case.

```python
def factorial(n):
    # Base case
    if n <= 1:
        return 1
    # Recursive case: n! = n × (n-1)!
    return n * factorial(n - 1)
```

Trace for `factorial(4)`:
```
factorial(4)
  → 4 × factorial(3)
       → 3 × factorial(2)
            → 2 × factorial(1)
                 → 1          (base case returns)
            ← 2 × 1 = 2
       ← 3 × 2 = 6
  ← 4 × 6 = 24
```

Each call waits on the stack until its sub-call returns. The call stack holds 4 frames simultaneously for `factorial(4)`.

### Stack Frames and Depth

Every recursive call creates a new stack frame (as shown in Module 4.2). The maximum recursion depth is limited by the stack size. Python's default limit is 1,000 frames:

```python
import sys
print(sys.getrecursionlimit())   # 1000

def infinite(n):
    return infinite(n + 1)

infinite(0)  # RecursionError: maximum recursion depth exceeded
```

For problems that require deep recursion (trees with depth 10,000, files nested 500 levels), you need either:
- An iterative solution using an explicit stack data structure
- Tail call optimisation (TCO) — the compiler reuses the stack frame when the recursive call is the very last thing done (Python does not do TCO; Scheme requires it)
- Increasing the stack size (risky)

### Fibonacci — The Classic Trap

```python
def fib_naive(n):
    if n <= 1: return n
    return fib_naive(n-1) + fib_naive(n-2)
```

This is **O(2ⁿ)** — exponential time. `fib(50)` takes about 10¹⁰ operations. The problem: the same sub-problems are computed repeatedly:

```
fib(5)
├── fib(4)
│   ├── fib(3)        ← computed again below
│   │   ├── fib(2)
│   │   └── fib(1)
│   └── fib(2)
└── fib(3)            ← duplicate
    ├── fib(2)        ← duplicate
    └── fib(1)
```

**Memoisation** fixes this in one line:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
```

Now O(n) — each sub-problem computed once, result cached. This is the core idea of **dynamic programming**: cache sub-problem results.

### Recursion on Data Structures

Recursion shines on naturally recursive structures — particularly **trees** (covered in Level 6):

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val   = val
        self.left  = left
        self.right = right

def tree_height(node):
    if node is None:           # base case: empty tree has height 0
        return 0
    left_h  = tree_height(node.left)   # height of left subtree
    right_h = tree_height(node.right)  # height of right subtree
    return 1 + max(left_h, right_h)    # this node adds 1

def tree_sum(node):
    if node is None: return 0
    return node.val + tree_sum(node.left) + tree_sum(node.right)
```

An iterative tree traversal requires an explicit stack. The recursive version is identical in structure to the mathematical definition.

### Mutual Recursion

Two or more functions can call each other:

```python
def is_even(n):
    if n == 0: return True
    return is_odd(n - 1)

def is_odd(n):
    if n == 0: return False
    return is_even(n - 1)
```

This is elegant but not efficient — use `n % 2 == 0` in practice. The concept matters: parsers for context-free grammars are often built as mutually recursive functions, where each function handles one grammar rule.

### Tower of Hanoi

The canonical recursive problem: move n disks from peg A to peg C, using peg B as auxiliary, without placing a larger disk on a smaller one.

```python
def hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    hanoi(n-1, source, auxiliary, target)   # move n-1 disks out of the way
    print(f"Move disk {n} from {source} to {target}")
    hanoi(n-1, auxiliary, target, source)   # move n-1 disks to target

hanoi(3, 'A', 'C', 'B')
```

The solution requires exactly **2ⁿ − 1** moves. There is no simpler way — the recursion captures the entire problem structure. The Tower of Hanoi is also a model for the recursive nature of the call stack itself: each invocation contains smaller subproblems, just as each disk move enables the next.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Recursion Tree Visualiser**
- Enter a recursive function call (factorial, fibonacci, hanoi)
- Watch the recursion tree expand in real time
- See each call frame on the call stack
- Observe the order of returns

**Tool 2 — Memoisation Demo**
- Run naive fibonacci for increasing n — watch the exponential explosion
- Enable memoisation — see the call count drop to n
- Inspect the cache: which sub-problems were stored and how many times reused

**Tool 3 — Tower of Hanoi Animator**
- Set number of disks (1–6)
- Watch the recursive solution execute move by move
- Count total moves and verify 2ⁿ − 1

---

## Going Deeper

**Continuation-passing style (CPS)**: a transform that makes all recursive calls tail calls. Every recursive function can be converted to CPS, making it TCO-compatible. Compilers for functional languages (Haskell, ML, Scheme) use CPS internally. Understanding CPS gives insight into how compilers handle recursion without stack growth.

**Structural induction**: to prove a recursive function is correct, use mathematical induction: (1) prove the base case is correct, (2) assume the recursive case gives the correct result for all smaller inputs, (3) prove the current call gives the correct result using that assumption. This is the recursive analogue of loop invariants.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace `factorial(5)` through all stack frames, convert a naive recursive Fibonacci to memoised, write a recursive solution to flatten a nested list, and prove the Tower of Hanoi requires exactly 2ⁿ − 1 moves by induction.
