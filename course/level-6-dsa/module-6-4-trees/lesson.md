# Module 6.4 — Trees: BST, AVL, Red-Black

---

## The Problem

> A sorted array gives O(log n) search via binary search.
> But inserting into a sorted array is O(n) — you must shift elements.
>
> A linked list gives O(1) insert (given the right position).
> But search is O(n) — no binary search without random access.
>
> Can we have both O(log n) search AND O(log n) insert?

Yes. The answer is the **balanced binary search tree** — a data structure that maintains sorted order dynamically, giving O(log n) for search, insert, and delete simultaneously.

---

## The Story

### Binary Search Trees — The Concept

A binary search tree (BST) stores keys in a tree structure such that for any node with key k:
- All keys in the **left subtree** < k
- All keys in the **right subtree** > k

This property enables binary-search-style lookups: at each node, compare the target to k and go left (smaller) or right (larger). With a balanced tree of n nodes, height ≈ log₂ n, so search takes O(log n) steps.

**George Boole's** logical algebra (1854) and **Leonhard Euler's** graph theory (1736) laid mathematical groundwork, but BSTs as a data structure were formalised in the early 1960s in connection with symbol tables for compilers. Compilers needed to look up variable names rapidly — a BST on variable names gave O(log n) lookup vs O(n) for a linear scan.

The problem came quickly: trees go wrong. Insert keys in sorted order (1, 2, 3, 4, 5...) and the BST degenerates into a linked list — O(n) for everything. The solution: **self-balancing trees**.

**G.M. Adelson-Velsky and E.M. Landis** (1962) invented the AVL tree — the first self-balancing BST, named after their initials. **Rudolf Bayer and Ed McCreight** (1972) invented the B-tree (used in databases, Module 9.2). **Leonidas Guibas and Robert Sedgewick** (1978) invented the red-black tree, now used in Linux's scheduler, C++ `std::map`, Java `TreeMap`, and virtually every language's sorted map.

---

## The Concept

### Binary Search Tree (BST)

```python
class BSTNode:
    def __init__(self, key, val=None):
        self.key   = key
        self.val   = val
        self.left  = None
        self.right = None

class BST:
    def search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self.search(node.left, key)
        return self.search(node.right, key)

    def insert(self, node, key, val=None):
        if node is None:
            return BSTNode(key, val)
        if key < node.key:
            node.left  = self.insert(node.left, key, val)
        elif key > node.key:
            node.right = self.insert(node.right, key, val)
        else:
            node.val = val   # update existing
        return node
```

**In-order traversal** (left → root → right) produces keys in sorted order — this is the fundamental property:

```python
def inorder(node):
    if node:
        inorder(node.left)
        print(node.key)
        inorder(node.right)
```

**Delete**: three cases:
1. Node has no children → remove it
2. Node has one child → replace node with child
3. Node has two children → replace node's key with in-order successor (smallest key in right subtree), then delete the successor

**Complexity (balanced tree)**: O(log n) search, insert, delete.  
**Complexity (worst case — degenerate)**: O(n) for all operations.

### AVL Trees — Height-Balanced

An AVL tree maintains the **balance factor** for every node: `height(left) - height(right) ∈ {-1, 0, 1}`. After every insert or delete, the tree **rotates** nodes to restore balance.

**Rotations** (O(1) operations):

**Right rotation** at node y:
```
    y              x
   / \            / \
  x   C    →    A   y
 / \                / \
A   B              B   C
```

**Left rotation** at node x:
```
  x                y
 / \              / \
A   y    →      x   C
   / \          / \
  B   C        A   B
```

Four cases after insertion:
- **Left-Left**: single right rotation at unbalanced node
- **Right-Right**: single left rotation
- **Left-Right**: left rotation on left child, then right rotation on node
- **Right-Left**: right rotation on right child, then left rotation on node

AVL trees guarantee height ≤ 1.44 × log₂(n+2). All operations strictly O(log n).

### Red-Black Trees — Practically Faster

A red-black tree uses node colours (red/black) and a simpler set of invariants to maintain approximate balance:

1. Every node is red or black
2. The root is black
3. Every leaf (null sentinel) is black
4. If a node is red, both children are black (no two consecutive reds)
5. All paths from any node to its descendant leaves contain the same number of black nodes

These rules guarantee height ≤ 2 × log₂(n+1). Red-black trees perform fewer rotations than AVL trees on average (AVL is more strictly balanced), making them faster in practice for workloads with many insertions and deletions.

**Used in**: Linux kernel (CFS scheduler, memory management), C++ `std::map`/`std::set`, Java `TreeMap`/`TreeSet`, Rust `BTreeMap`, most language standard library sorted containers.

### Tree Traversals

```python
# In-order: left → root → right → sorted output for BST
def inorder(node, result=[]):
    if node:
        inorder(node.left, result)
        result.append(node.key)
        inorder(node.right, result)

# Pre-order: root → left → right → tree serialisation
def preorder(node):
    if node:
        print(node.key)
        preorder(node.left)
        preorder(node.right)

# Post-order: left → right → root → safe deletion order
def postorder(node):
    if node:
        postorder(node.left)
        postorder(node.right)
        print(node.key)         # process after children

# Level-order: breadth-first (uses a queue)
from collections import deque
def level_order(root):
    q = deque([root])
    while q:
        node = q.popleft()
        print(node.key)
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
```

### BST as a Sorted Map

A balanced BST implements the **sorted map** (or **ordered dictionary**) ADT:
- `search(key)` → O(log n)
- `insert(key, value)` → O(log n)
- `delete(key)` → O(log n)
- `min()` / `max()` → O(log n)
- `successor(key)` / `predecessor(key)` → O(log n)
- `range_query(lo, hi)` → O(log n + k) where k = number of results

This range query capability is what makes BSTs superior to hash tables when you need ordered queries (e.g., "find all users with age between 20 and 30").

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — BST Builder**
- Insert keys one at a time and watch the tree form
- Insert in sorted order — observe the degenerate case
- Search for a key and watch the comparison path

**Tool 2 — AVL Rotations**
- Insert keys into an AVL tree
- When an imbalance occurs, step through the rotation
- See balance factors update after each operation

**Tool 3 — Traversal Animator**
- A built tree on screen
- Click In-order, Pre-order, Post-order, Level-order
- Watch nodes highlight in visit order

---

## Going Deeper

**Treaps**: a BST where each node also has a random priority, maintained as a max-heap. The result is a balanced tree with O(log n) expected height — no rotations, just priority-guided structure. Simpler to implement than AVL or red-black trees.

**Splay trees**: a self-adjusting BST where every accessed node is moved to the root via rotations. Recently accessed nodes are near the root, giving O(1) amortised access for repeated lookups of the same key. Used in GCC's C++ runtime and some cache implementations.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Build a BST from a sequence of insertions, trace an AVL rotation, write in-order traversal iteratively using an explicit stack, and explain why inserting [1,2,3,4,5] into a BST is worst-case.
