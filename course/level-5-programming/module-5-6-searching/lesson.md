# Module 5.6 — Searching: Finding What You Need

---

## The Problem

> A phone book has 5 million entries.
> Finding a name by scanning every entry takes minutes.
> Finding it by binary search takes microseconds.
>
> Google's index has 100 billion web pages.
> Finding pages matching a query in under 100 milliseconds
> requires not just a fast search algorithm but an entirely
> different data structure designed for search from the ground up.

Searching is the inverse of sorting, and understanding how to find things efficiently — from a sorted array, an unsorted collection, a graph, or a text string — is foundational to almost every software system ever built.

---

## The Story

### From Card Catalogues to Search Engines

Before computers, librarians invented efficient search structures: alphabetical catalogues, Dewey Decimal classification, card indexes. These were manual implementations of data structures designed to reduce lookup time from O(n) (scan every card) to O(log n) (binary search through a sorted index).

**Vannevar Bush** (1945) described the Memex in his essay "As We May Think" — a hypothetical device that could store and rapidly retrieve vast amounts of information using associative links. This vision directly inspired hypertext and the web.

The first web search engine, **Archie** (1990), simply indexed FTP filenames. **AltaVista** (1995) indexed full page text. **Google** (1998) introduced PageRank — ranking by link structure rather than just keyword frequency — and transformed search from a text-matching problem into a graph analysis problem. Today, a Google search traverses an index of 100 billion pages in under 100ms on a cluster of thousands of machines.

---

## The Concept

### Linear Search — O(n)

The simplest possible search: check every element until you find the target or exhaust the collection.

```python
def linear_search(arr, target):
    for i, x in enumerate(arr):
        if x == target:
            return i      # found at index i
    return -1             # not found
```

**When to use**: unsorted data, small collections (n < ~50), or when you need to find all occurrences.  
**When not to use**: large sorted collections — binary search is orders of magnitude faster.

### Binary Search — O(log n)

Requires the array to be sorted. At each step, compare the target to the middle element and eliminate half the remaining search space.

```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1    # target is in the right half
        else:
            high = mid - 1   # target is in the left half
    return -1                 # not found
```

**Why O(log n)?** Each comparison halves the remaining search space. Starting with n elements, after k comparisons we have n/2^k elements left. When n/2^k = 1, k = log₂(n). For n = 1,000,000: at most 20 comparisons.

**Invariant**: at every iteration, if the target exists, it is in `arr[low..high]`. Maintaining this invariant is the key to getting the boundary conditions right.

**Common mistakes**:
- Off-by-one in `mid + 1` / `mid - 1` — leads to infinite loops or missed elements
- Integer overflow in `(low + high) // 2` for very large arrays (use `low + (high - low) // 2` in C)

### Binary Search Variants

Binary search has many useful generalisations:

**Find first occurrence of target** (duplicates in array):
```python
def first_occurrence(arr, target):
    low, high, result = 0, len(arr) - 1, -1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            result = mid
            high = mid - 1   # keep searching left for earlier occurrence
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return result
```

**Find insertion point** (like Python's `bisect.bisect_left`):
Returns the index where target should be inserted to keep the array sorted.

**Search on answer** — a powerful technique: binary search on the *answer space* rather than the data. For example: "what is the minimum speed at which I can complete a task within T hours?" Binary search over possible speeds, using a feasibility function to check each candidate.

### Hash Tables — O(1) Average

Binary search requires sorted data and gives O(log n). For O(1) average-case search, we use a **hash table** (covered in depth in Level 6):

```python
d = {'alice': 30, 'bob': 25, 'carol': 28}
d['alice']        # O(1) average — hash lookup
'bob' in d        # O(1) average
```

The hash function maps the key to an array index. Lookup: hash the key, go directly to that index. No comparisons needed. The price: hash tables use more memory, and worst-case is O(n) if many keys hash to the same slot.

### Graph Search — BFS and DFS

When data has relationships (not just linear order), we need graph search. Covered fully in Level 6 (Module 6.6), but the foundations are:

**Breadth-First Search (BFS)**: explore level by level, using a queue.
- Finds the shortest path (fewest edges) in an unweighted graph
- O(V + E) where V = vertices, E = edges

**Depth-First Search (DFS)**: go as deep as possible before backtracking, using a stack (or recursion).
- Detects cycles, topological sort, connected components
- O(V + E)

### String Search — KMP Algorithm

Finding a pattern of length m within a text of length n. Naive: try every position → O(nm). The **Knuth-Morris-Pratt (KMP)** algorithm preprocesses the pattern to avoid redundant comparisons → O(n + m).

```
Text:     AAABAAABAAAC
Pattern:  AAABAAAC

Naive: would restart from scratch on each mismatch
KMP: uses a failure function to skip characters already matched
```

The core idea: when a mismatch occurs, the pattern's internal structure tells us how far to shift without losing already-matched characters. This makes substring search in a 1GB log file fast enough to be done in seconds.

### Trie — O(m) Prefix Search

A trie (prefix tree) stores strings as paths in a tree where each node is a character:

```
Insert: "cat", "car", "card", "care", "bat"

         root
        /    \
       c      b
       |      |
       a      a
      / \     |
     t   r    t
         |
        d/e
```

Lookup: "care" → follow c→a→r→e. O(m) where m = string length, regardless of how many strings are stored. Tries enable prefix-based autocomplete: finding all words starting with "car" takes O(m + output size).

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Linear vs Binary Search Race**
- An array of 1,000 sorted integers
- Search for the same target using both algorithms simultaneously
- Watch the step counter: linear takes up to 1,000 steps, binary at most 10
- Try a worst-case search (target not present)

**Tool 2 — Binary Search Variants**
- An array with duplicates
- Run: find any occurrence, find first occurrence, find last occurrence, find insertion point
- See how each variant differs only in how it updates `low`/`high` on a match

**Tool 3 — Trie Builder**
- Type words to insert into a trie
- Watch the prefix tree grow
- Type a prefix and see all matching words highlighted
- Count how many nodes are traversed vs scanning a list

---

## Going Deeper

**Bloom filters**: a probabilistic data structure that can answer "is this element in the set?" with no false negatives and a configurable false positive rate, using a fraction of the memory of a hash table. Used in databases (avoid expensive disk lookups for non-existent keys), web browsers (safe browsing lists), and network routers. The tradeoff: you cannot enumerate elements, and you cannot delete elements without a counting variant.

**B-trees and database indices**: database tables with millions of rows need search in O(log n) disk accesses. A B-tree keeps all data sorted in a balanced tree where each node holds many keys — a typical node fills one disk page (4–16 KB). This minimises disk reads. B-trees are the data structure behind almost every database index ever built. Level 9 covers them in detail.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace binary search on a 16-element sorted array, implement `bisect_left`, analyse when linear search beats binary search (hint: consider overhead), and insert five words into a trie by hand and draw the resulting tree.
