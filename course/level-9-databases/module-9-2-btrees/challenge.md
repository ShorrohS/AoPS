# Challenge 9.2 — B-Trees and Why Databases Use Them

**Type:** Build + trace + calculation  
**Estimated time:** 45–55 minutes  
**Tools needed:** pen and paper

---

## Part A — Building a B-Tree

Insert the keys `[10, 20, 5, 6, 12, 30, 7, 17]` into a B-tree of **order t=2** (minimum degree 2):
- Each node has 1–3 keys (min=t-1=1, max=2t-1=3)
- Each internal node has 2–4 children
- Splits when a node reaches 4 keys

1. Show the tree state after each insertion, including any splits. For each split, clearly show:
   - The full node before the split
   - The median key promoted to the parent
   - The two resulting nodes

2. How many disk reads are needed to find key `17` in the final tree? Trace the path.

3. What is the height of the final tree?

---

## Part B — B-Tree vs BST Comparison

For a B-tree of order t=100 (typical for a 4KB block with 4-byte keys and 8-byte child pointers):

4. How many keys can one node hold? How many child pointers?

5. A database table has **100 million rows**. What is the maximum height of a B+tree index with t=100?
   Show the calculation: height = ⌈log₁₀₀(100,000,000)⌉

6. Compare to a BST with 100 million nodes: what is the expected height? (log₂ of 100 million)

7. Each tree level requires one disk read (10ms). What is the total time to locate one row using:
   - The B+tree (from question 5)
   - The BST (from question 6)

---

## Part C — Range Scan

8. A B+tree stores sorted keys in its leaf nodes, and leaf nodes are linked in a doubly-linked list. Explain step by step how the range query `WHERE age BETWEEN 25 AND 35` is executed:
   - How does the database find the first matching key?
   - How does it collect all matching keys without scanning the entire tree?

9. A hash index cannot efficiently answer `WHERE age BETWEEN 25 AND 35`. Explain why. Under what condition is a hash index preferred over a B+tree index?

10. The B+tree has 10,000 rows with `age BETWEEN 25 AND 35` out of 1 million total. With a B+tree of height 3: how many disk reads are needed for the range query? Compare to a full table scan.

---

## Part D — Clustered vs Secondary Index

11. In InnoDB (MySQL), the primary key index is a **clustered index**: the actual row data is stored in the leaf nodes. A secondary index (e.g., on `email`) stores `(email, primary_key)` in its leaf nodes.

    Trace the disk accesses for:
    - `SELECT * FROM users WHERE id = 42` (uses clustered index)
    - `SELECT * FROM users WHERE email = 'alice@example.com'` (uses secondary index on email)
    
    How many B+tree lookups does each require?

12. Why does InnoDB store the primary key in every secondary index leaf (rather than a direct page pointer)?

13. What is a **covering index**? Give an example query and index that avoids the second B+tree lookup entirely.

---

## Part E — Write Amplification

14. Every INSERT into a table with a B+tree index requires updating the B+tree. For a table with 3 indexes (primary, secondary on email, secondary on city), how many B+tree pages might need to be updated for a single INSERT?

15. **LSM-trees** (Log-Structured Merge-trees, used in RocksDB, Cassandra) write all new data as sequential appends. This avoids the random writes of B+tree updates. What is the trade-off for reads? (Hint: LSM-trees may have multiple sorted "levels" to check.)

---

## Rubric

| Part | Points |
|---|---|
| A building B-tree | 28 |
| B comparison | 20 |
| C range scan | 22 |
| D clustered index | 20 |
| E write amplification | 10 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part B.5–7 — height comparison</summary>

B+tree with t=100: max keys per node = 199. Nodes at level 0 = 1 (root), level 1 = 200, level 2 = 40,000, level 3 = 8,000,000, level 4 = 1,600,000,000. For 100M rows: height = 4 levels (4 disk reads).

BST with 100M nodes: log₂(10⁸) ≈ 27 levels (27 disk reads).

Time: B+tree = 4 × 10ms = 40ms. BST = 27 × 10ms = 270ms. **B+tree is 6.75× faster per lookup.**
</details>

<details>
<summary>Part C.10 — range query reads</summary>

1. B+tree descent to first key ≥ 25: 3 reads (one per level).
2. Leaf scan: 10,000 matching rows. If each leaf page holds ~100 rows: 100 leaf page reads.
Total: ~103 reads.

Full table scan: 1,000,000 / 100 rows per page = 10,000 page reads. B+tree range query is ~97× fewer reads.
</details>

<details>
<summary>Part D.11 — clustered vs secondary</summary>

`SELECT * WHERE id=42`: one B+tree lookup, leaf node contains the full row. **1 B+tree traversal**.

`SELECT * WHERE email='alice@...'`: (1) traverse email secondary index B+tree → find (email, primary_key). (2) traverse primary B+tree using that primary key → get full row. **2 B+tree traversals**.
</details>
