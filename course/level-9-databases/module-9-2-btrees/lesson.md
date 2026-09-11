# Module 9.2 — B-Trees and Why Databases Use Them

---

## The Problem

> A database table has 100 million rows.
> You need to find the row where `user_id = 7,482,991` in under a millisecond.
>
> A BST (Module 6.4) gives O(log n) — about 27 comparisons.
> That sounds fast. But each comparison may require a disk read.
> A disk read takes ~10 ms.
> 27 disk reads × 10 ms = 270 ms per query.
> For 100 concurrent users: 27 seconds of disk I/O per second.
>
> The problem is not the number of comparisons — it's the number of **disk accesses**.
> The B-tree was designed to minimise disk accesses.

---

## The Story

### Designed for Disk

Rudolf Bayer and Ed McCreight invented the B-tree at Boeing Research Labs in 1972. Their paper title: "Organization and Maintenance of Large Ordered Indexes." The context was clear: they needed a data structure for storing and searching indexes on disk, not in RAM.

The key insight: disk I/O is the bottleneck, not CPU operations. A disk read fetches an entire **block** (typically 4–16 KB) at once, regardless of how much data you actually need. The B-tree exploits this by storing many keys in each node — the node fills exactly one disk block. One disk read retrieves a node with hundreds of keys; binary search within that node is pure CPU work (cheap).

IBM's IMS database (1968, pre-B-tree) used VSAM (Virtual Storage Access Method) with similar ideas. Oracle, IBM DB2, PostgreSQL, MySQL/InnoDB — every major relational database uses B-trees (or the closely related B+tree variant) for their primary storage.

---

## The Concept

### B-Tree Properties

A B-tree of order `t` (minimum degree):
- Every node except root has at least `t-1` keys
- Every node has at most `2t-1` keys
- A node with `k` keys has `k+1` children
- All leaves are at the same depth
- Keys within a node are sorted

For `t = 100` (typical for a disk-based B-tree with 4 KB blocks):
- Each node holds 99–199 keys
- Each internal node has 100–200 child pointers
- Height of a tree with 1 billion keys: log₁₀₀(10⁹) ≈ **4.5 levels** → **5 disk reads** maximum

Compare: a BST with 1 billion nodes has height ~30, requiring **30 disk reads**.

### B-Tree vs B+Tree

Almost all databases use the **B+tree** variant:

**B-tree**: keys and data records stored in all nodes (internal and leaf).

**B+tree**: 
- Internal nodes store **only keys and child pointers** (routing keys)
- All actual data (records or record pointers) stored in **leaf nodes**
- Leaf nodes are **linked in a doubly-linked list**

Benefits of B+tree:
1. Internal nodes can hold more keys (no data overhead) → shorter tree → fewer disk reads
2. Leaf linked list enables efficient **range scans**: `WHERE age BETWEEN 25 AND 35` traverses leaf nodes sequentially
3. All queries touch leaf nodes → more predictable access patterns

### Search

```python
def btree_search(node, key):
    # Binary search for key in node.keys
    i = bisect_left(node.keys, key)

    if i < len(node.keys) and node.keys[i] == key:
        return node.vals[i]          # found in this node

    if node.is_leaf:
        return None                  # not found

    # Recurse into appropriate child
    return btree_search(node.children[i], key)
```

One disk read per level traversed. For a 4-level B+tree with `t=100`: maximum **4 disk reads** to find any record among 200 million rows.

### Insertion

1. Search to find the correct leaf node
2. Insert the key in sorted position in the leaf
3. If the leaf is not full (< 2t-1 keys): done
4. If the leaf is full: **split** it:
   - Create two nodes, each with ~half the keys
   - Promote the middle key to the parent
   - If parent is also full, split the parent recursively
   - If root splits, create a new root → tree height increases by 1

The only way a B-tree grows taller is when the root splits. All leaves remain at the same depth — the tree is always balanced.

### Deletion

More complex:
1. Find the key to delete
2. If in a leaf: remove it
3. If in an internal node: replace with in-order successor (from leaf), delete from leaf
4. If deletion causes underflow (< t-1 keys):
   - Try to **borrow** from a sibling (redistribute keys via parent)
   - If sibling is at minimum too: **merge** with sibling + pull down parent key
   - Merging may propagate up to the root; if root becomes empty, tree shrinks

### Database Index Implementation

In PostgreSQL, MySQL's InnoDB, and SQLite:

**Clustered index** (InnoDB's primary key): the actual table data is stored in the B+tree leaf nodes, ordered by the primary key. One disk read at leaf level = the actual row data.

**Secondary index**: leaf nodes store the primary key value (not the row data). To retrieve the full row: look up the secondary index B+tree to get the primary key, then look up the clustered B+tree. **Two B+tree lookups** per secondary index query (unless using a covering index).

```sql
-- This uses the name index (secondary index B+tree)
-- then the primary key B+tree to get the full row
SELECT * FROM users WHERE name = 'Alice';

-- This uses only the name index (covering index)
-- All needed columns are in the leaf nodes
SELECT id, name FROM users WHERE name = 'Alice';
```

### Why Not Hash Tables for Databases?

Hash tables give O(1) lookup — faster than B+trees O(log n). So why do databases use B+trees?

1. **Range queries**: `WHERE price BETWEEN 10 AND 50` — hash tables are useless for ranges; B+trees handle them in O(log n + k)
2. **Ordering**: `ORDER BY name` — B+tree traversal produces sorted order; hash tables don't
3. **Prefix queries**: `WHERE name LIKE 'Ali%'` — B+trees handle prefix scans; hash tables don't
4. **Predictable worst case**: hash tables have O(n) worst case; B+trees are always O(log n)

Databases do use hash indexes for equality-only lookups where ranges aren't needed (PostgreSQL has hash indexes). But the B+tree is the universal default because it supports everything.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — B-Tree Visualiser**
- Insert keys into a B-tree with order t=2 (minimum 1 key, maximum 3 keys per node)
- Watch nodes split when they overflow
- Watch the tree height increase only when the root splits

**Tool 2 — Search Trace**
- Enter a search key
- Watch the traversal: root → internal node → leaf
- Count the disk reads (one per level)

**Tool 3 — Range Scan**
- Run a range query (e.g., keys between 20 and 50)
- Watch the B+tree: navigate to the first matching leaf, then scan the leaf linked list

---

## Going Deeper

**Write amplification**: database writes to B-trees cause significant write amplification — a single row insert may require reading and rewriting multiple B-tree nodes. LSM-trees (Log-Structured Merge-trees), used in RocksDB, Cassandra, and LevelDB, trade write amplification for read amplification: writes are always sequential appends (fast on SSDs), reads merge multiple sorted runs. Understanding B-tree vs LSM-tree is fundamental to database internals.

**Fractional cascading**: a technique to speed up searches in multiple sorted lists by maintaining links between lists at matching keys. Reduces multi-list search from O(k log n) to O(log n + k). Used in range trees and priority search trees for multi-dimensional spatial queries.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Build a B-tree of order 2 by inserting [10,20,5,6,12,30,7,17] step by step (draw each state after insertion), calculate the maximum number of disk reads to find a key in a B+tree holding 1 billion records with t=200, explain why secondary indexes require two B+tree lookups, and describe when a database query planner would choose a sequential scan over an index lookup.
