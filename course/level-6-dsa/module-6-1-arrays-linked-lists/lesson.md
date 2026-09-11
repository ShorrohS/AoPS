# Module 6.1 — Arrays and Linked Lists

---

## The Problem

> You need to store a collection of items.
> You will add items, remove items, and access them by position or by searching.
>
> The obvious choice: just put them all in a row.
> But "in a row" has hidden costs.
> Inserting in the middle means moving everything else.
> Not knowing the size in advance means either wasting space or copying everything.
>
> The first decision in every data structure course is the most fundamental:
> **contiguous or linked?**

---

## The Story

### Arrays — The First Data Structure

The array is as old as stored-program computing. A memory address is a number; an array is just a block of memory at a base address, with each element at `base + index × element_size`. The CPU can compute any element's address in one multiplication and one addition — O(1) access.

FORTRAN (1957), the first widely-used programming language, was built around arrays. Matrix arithmetic in FORTRAN was the entire point: scientific computing required fast access to elements by index. The array's O(1) access is why cache memory (Level 3) was designed the way it was — sequential memory access patterns fill cache lines efficiently.

Linked lists were invented slightly later, when programmers needed to handle collections whose size wasn't known at compile time. John McCarthy's **Lisp** (1958) was the first language built around linked lists — in Lisp, everything is a list. The language's name stands for "LISt Processing."

---

## The Concept

### Arrays

An array stores elements in **contiguous memory**. For an array of `int` (4 bytes each) starting at address `A`:

```
Element:  arr[0]   arr[1]   arr[2]   arr[3]
Address:  A+0      A+4      A+8      A+12
```

**Random access**: `arr[i]` → address `A + i * sizeof(element)` → one instruction. **O(1)**.

**Insertion at end**: if capacity remains, write at `arr[length]` and increment length. **O(1) amortised** (Python lists, C++ `vector` double capacity when full).

**Insertion at middle**: must shift all elements after the insertion point right. **O(n)**.

**Deletion at middle**: shift all elements after the deletion point left. **O(n)**.

**Search (unsorted)**: scan from index 0 until found. **O(n)**.

**Search (sorted)**: binary search. **O(log n)**.

**Memory**: no overhead per element — just the data itself.

### Dynamic Arrays

Static C arrays have fixed size declared at compile time. **Dynamic arrays** (Python `list`, C++ `vector`, Java `ArrayList`) grow automatically:

```python
lst = []           # empty, capacity 0
lst.append(1)      # allocates initial capacity (e.g., 4 slots)
lst.append(2)      # fits in existing capacity
# ... append until capacity full
lst.append(x)      # RESIZE: allocate new array (2× capacity),
                   # copy all elements, free old array
```

The resize is O(n) work, but it happens rarely. Amortised analysis: n appends on a fresh list do at most O(2n) total work (geometric series: n + n/2 + n/4 + ...) → **O(1) amortised per append**.

### Linked Lists

A linked list stores elements in **nodes** scattered anywhere in memory. Each node contains the data and a pointer to the next node:

```
[data:1 | next:→] → [data:2 | next:→] → [data:3 | next:None]
  head                                     tail
```

In Python:
```python
class Node:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node

class LinkedList:
    def __init__(self):
        self.head = None

    def prepend(self, data):
        self.head = Node(data, self.head)   # O(1)

    def append(self, data):                  # O(n) — must traverse to tail
        if not self.head:
            self.head = Node(data); return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = Node(data)

    def delete(self, data):                  # O(n) — must find node
        if not self.head: return
        if self.head.data == data:
            self.head = self.head.next; return
        curr = self.head
        while curr.next:
            if curr.next.data == data:
                curr.next = curr.next.next; return
            curr = curr.next
```

**Insert at head**: update head pointer only. **O(1)**.  
**Insert at tail** (without tail pointer): traverse to last node. **O(n)**.  
**Insert at tail** (with tail pointer maintained): **O(1)**.  
**Delete given node pointer**: update previous node's `next`. **O(1)** if you have the previous node, **O(n)** if you must find it.  
**Random access** (`list[5]`): must traverse from head. **O(n)** — no index formula exists.  
**Memory**: each node stores a pointer (8 bytes on 64-bit) plus the data. More overhead than arrays.

### Doubly Linked Lists

Each node has both a `next` and `prev` pointer:

```
None ← [1] ↔ [2] ↔ [3] → None
```

Enables O(1) deletion when you have a pointer to the node (update both neighbours without traversing). Python's `collections.deque` is implemented as a doubly linked list — O(1) append and pop from both ends.

### When to Use Each

| Operation | Array (dynamic) | Linked List |
|---|---|---|
| Access by index | O(1) | O(n) |
| Insert at end | O(1) amortised | O(1) with tail ptr |
| Insert at start | O(n) | O(1) |
| Insert at middle | O(n) | O(1) with node ptr |
| Delete at middle | O(n) | O(1) with node ptr |
| Memory per element | Low | High (pointer overhead) |
| Cache friendliness | Excellent | Poor (nodes scattered) |

**In practice**: dynamic arrays (Python lists, C++ vectors) are used for almost everything. Their cache friendliness makes them faster than linked lists even for operations where linked lists have better asymptotic complexity. Linked lists are used when: insertions/deletions in the middle are extremely frequent and you already have node pointers, or when elements must not be moved in memory (e.g., intrusive linked lists in the Linux kernel, where struct members point to each other directly).

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Array Operations**
- Insert, delete, and access elements in a dynamic array
- Watch the resize happen when capacity is exceeded
- Count comparisons and copies for each operation

**Tool 2 — Linked List Visualiser**
- Build a linked list node by node
- Insert at head, tail, and arbitrary position
- Delete a node — watch the pointer update
- Traverse the list following arrows

**Tool 3 — Head-to-Head: Array vs Linked List**
- Same sequence of operations on both structures
- Compare total operation counts
- Visualise memory layout side by side

---

## Going Deeper

**Intrusive linked lists**: the Linux kernel uses a linked list where the `next`/`prev` pointers live *inside* the struct being managed, rather than in a separate node wrapper. This eliminates one allocation per element and one pointer dereference. The entire kernel's scheduler, file system, and network stack use `list_head` — a two-line struct. Understanding this requires understanding pointer arithmetic, struct layout, and `container_of` macros.

**Skip lists**: a probabilistic data structure that adds multiple levels of linked lists, each skipping more elements. Supports O(log n) search, insert, and delete — competitive with balanced BSTs but much simpler to implement. Used in Redis as the backing data structure for sorted sets.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Implement a singly linked list with `prepend`, `append`, `delete`, and `reverse` in Python. Trace the insertion of 4 elements. Calculate the total bytes used for a linked list vs array of 1,000 integers. Prove that reversing a linked list is O(n).
