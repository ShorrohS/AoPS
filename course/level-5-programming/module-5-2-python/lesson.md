# Module 5.2 — Python: Abstraction for Humans

---

## The Problem

> C gives you total control and total responsibility.
> Writing a web scraper in C means managing memory, parsing strings byte by byte,
> handling network sockets manually.
>
> Most programmers most of the time are not writing operating systems.
> They are solving problems: process this data, build this web service, train this model.
>
> *What if the language handled memory, types, and low-level details automatically
> so the programmer could focus entirely on the problem?*

This question produced Python (1991), and then a generation of languages with similar philosophy. Python's design principle: **readability counts**. Code is read far more than it is written. A program that takes 10 lines in C and 2 lines in Python is almost always faster to write, debug, and maintain — even if it runs 50× slower at execution time.

---

## The Story

### Guido van Rossum and the Christmas Holiday

Guido van Rossum was a Dutch programmer working at CWI (Netherlands) in December 1989. During the holiday break, he decided to write a new scripting language as a personal project — something easier to use than C for quick programming tasks, better-designed than the shells and AWK scripts he was using.

He named it Python after Monty Python's Flying Circus, not the snake. His design goals:
- Elegant syntax that reads almost like pseudocode
- A comprehensive standard library ("batteries included")
- Automatic memory management — no `malloc`/`free`
- Dynamic typing — no type declarations needed
- A single, clear way to do each thing

Python 1.0 was released in 1994. Python 2.0 (2000) added garbage collection and list comprehensions. Python 3.0 (2008) was a backward-incompatible redesign that fixed accumulated design mistakes. By 2020, Python was the most-used programming language in the world by survey.

---

## The Concept

### Interpreted vs Compiled

C source code is compiled to machine code once; the CPU runs the machine code directly.

Python source code is interpreted at runtime by the Python interpreter (CPython, written in C):

```
Python source (.py)
      ↓ Compilation (fast, at runtime)
Bytecode (.pyc)
      ↓ Interpretation (CPython virtual machine)
Result
```

The CPython VM executes bytecode instructions in a loop. Each Python operation (like `x + y`) may compile to hundreds of machine instructions — type-checking, object dispatch, reference counting. This is why Python is 50–100× slower than C for CPU-intensive code.

**When Python speed doesn't matter:**
- I/O-bound tasks (network requests, file reads) — most time is waiting, not computing
- NumPy/SciPy/PyTorch operations — these call into C/Fortran/CUDA code, so the speed is C speed
- Prototyping — development time matters more than runtime for one-off scripts

### Dynamic Typing

In C: `int x = 5;` — the type `int` is fixed at compile time.

In Python: `x = 5` — the type is attached to the *value*, not the variable. `x` can point to any type:

```python
x = 5         # x refers to an int object
x = "hello"   # now x refers to a str object
x = [1, 2, 3] # now x refers to a list object
```

Under the hood, every Python value is a C struct (`PyObject`) containing:
- A reference count (for garbage collection)
- A pointer to the type object
- The actual value

This indirection — going through a type pointer for every operation — is most of Python's overhead compared to C.

### The Python Data Model

Everything in Python is an **object**. Integers, strings, functions, classes, modules — all objects. Every object has:
- An **identity** (`id(x)` — the memory address)
- A **type** (`type(x)`)
- A **value**

**Immutable types**: `int`, `float`, `str`, `tuple`, `frozenset` — cannot be changed after creation.  
**Mutable types**: `list`, `dict`, `set`, custom objects — can be modified in-place.

```python
# Immutable: creates a NEW object
x = "hello"
y = x.upper()    # y is a new string "HELLO", x unchanged

# Mutable: modifies IN PLACE
lst = [1, 2, 3]
lst.append(4)    # lst is now [1, 2, 3, 4] — same object
```

This distinction matters for correctness and performance. Passing a list to a function and modifying it changes the original (pass by reference to the object). Passing an int and "modifying" it just rebinds the local variable (pass by value of the reference — effectively pass by value for immutables).

### Garbage Collection

Python uses **reference counting** as its primary GC mechanism:

```python
x = [1, 2, 3]    # ref count of the list = 1
y = x             # ref count = 2
del x             # ref count = 1
del y             # ref count = 0 → object freed
```

When an object's reference count reaches 0, it is immediately freed. This is fast and deterministic — no GC pause.

Problem: **circular references**:
```python
a = {}
b = {}
a['other'] = b    # b's ref count = 2 (b itself + a['other'])
b['other'] = a    # a's ref count = 2
del a             # a's ref count = 1 (still referenced by b)
del b             # b's ref count = 1 (still referenced by a)
# Both are now unreachable but neither is freed!
```

Python's **cycle garbage collector** (runs periodically) detects and collects such cycles. This is why Python can have occasional GC pauses for long-lived programs.

### Key Built-in Types and Their Internals

**List** — a dynamic array of object pointers:
```python
lst = [1, 2, 3]
lst.append(4)     # O(1) amortised — pre-allocates extra space
lst.insert(0, 0)  # O(n) — shifts all elements right
lst[2]            # O(1) — direct index access
```

**Dict** — a hash table:
```python
d = {'name': 'Alice', 'age': 30}
d['name']         # O(1) average — hash lookup
d['city'] = 'NYC' # O(1) average — insert
'name' in d       # O(1) average — membership test
```

Python dicts since 3.7 maintain insertion order. The implementation uses open addressing with a compact layout since Python 3.6.

**Set** — a hash table without values:
```python
s = {1, 2, 3, 4}
s.add(5)           # O(1) average
3 in s             # O(1) average
s1 & s2            # set intersection — O(min(len(s1), len(s2)))
```

### Decorators — Functions That Transform Functions

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

slow_function()   # prints: slow_function took 1.0003s
```

`@timer` is syntactic sugar for `slow_function = timer(slow_function)`. The decorator wraps the function in new behaviour without modifying its source. This pattern is used extensively in Python frameworks — Flask's `@app.route`, Django's `@login_required`, pytest's `@pytest.mark.parametrize`.

### The Python Object Model: Everything is an Object

```python
def add(a, b):
    return a + b

print(type(add))        # <class 'function'>
print(add.__name__)     # 'add'
print(add.__code__)     # code object with bytecode
print(add(3, 4))        # 7
```

Functions are first-class objects. They can be passed to other functions, stored in lists, returned from functions. This enables functional programming patterns and closures.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Reference Counter**
- Create objects and take references
- Watch reference counts increment and decrement
- Delete references and watch objects get freed
- Create a circular reference — observe that it doesn't free automatically

**Tool 2 — Data Structure Internals**
- Create a list, dict, and set
- Insert and look up elements
- See the underlying array/hash table structure
- Observe time complexity of operations

**Tool 3 — Decorator Builder**
- Write a function
- Apply a timer decorator
- Step through: the decorator wraps the function, the wrapper is called, timing is captured

---

## Going Deeper

**The GIL (Global Interpreter Lock)**: CPython has a single lock that any thread must hold to execute Python bytecode. This means multiple Python threads cannot run Python code truly in parallel, even on a multi-core CPU. CPU-bound multithreaded Python code often runs slower than single-threaded code due to GIL contention. The workarounds: use `multiprocessing` (separate processes, no GIL), use `asyncio` (cooperative concurrency for I/O-bound code), or use libraries that release the GIL (NumPy, I/O operations). Python 3.13 introduced experimental GIL removal (`python3.13t`).

**CPython vs alternatives**: CPython is the reference implementation. PyPy uses a JIT compiler and runs many Python programs 5–10× faster. Cython compiles Python-like code to C extensions. Numba JIT-compiles numerical Python to LLVM IR. MicroPython runs on microcontrollers with 256 KB of RAM.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Implement a linked list in pure Python using classes, write a timing decorator, trace reference counting for a circular structure, and explain why `a = []; b = a; a.append(1)` makes `b` contain `[1]`.
