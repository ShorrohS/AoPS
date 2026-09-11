# Challenge 6.3 — Hash Tables

**Type:** Trace + implementation + analysis  
**Estimated time:** 45–55 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — Linear Probing Trace

Hash table of size **M = 7**. Hash function: `h(k) = k % 7`. Collision resolution: **linear probing** (probe at `(h(k) + i) % M` for i = 0, 1, 2, ...).

Insert keys in order: **10, 22, 31, 4, 15, 28, 17, 88, 59**

1. For each key, calculate `h(k)` and trace the probe sequence until an empty slot is found. Draw the final table.

2. How many total probes were needed across all insertions?

3. What is the load factor after all 9 insertions?

4. Now search for key **28**. Trace the probe sequence. How many probes are needed?

---

## Part B — Tombstone Deletion

Using the table from Part A:

5. Delete key **31** by placing a **tombstone** (a marker indicating "deleted but probed-through").

6. After deletion, search for key **59**. Does the tombstone affect the search? Show the probe sequence.

7. Now insert key **100** (`100 % 7 = 2`). Does the tombstone affect the insertion? At which slot does it land?

8. Why can't you simply mark a slot as "empty" when deleting in linear probing? Construct a concrete example where doing so would cause a search to incorrectly report "not found."

---

## Part C — Chaining vs Open Addressing

9. Insert keys `{10, 17, 24, 31, 38}` into a hash table of size **M = 7** using **separate chaining** (`h(k) = k % 7`). Draw the table with chains.

10. Compare the worst-case lookup time for chaining vs linear probing when the load factor α = 0.9. What is the expected probe count for linear probing: `1/(1 - α)` (unsuccessful) and `(1 + 1/(1-α)²)/2` (successful)?

11. For which load factor does linear probing's expected probe count exceed 5? Use the formula for unsuccessful search.

---

## Part D — Hash Table Implementation

Implement a hash table with **separate chaining** in Python:

```python
class HashTable:
    def __init__(self, capacity=16):
        self._buckets  = [[] for _ in range(capacity)]
        self._size     = 0
        self._capacity = capacity
        self._threshold = 0.75   # resize when load factor exceeds this

    def _hash(self, key): ...
    def set(self, key, value): ...   # O(1) average
    def get(self, key): ...          # O(1) average, raises KeyError if absent
    def delete(self, key): ...       # O(1) average
    def _resize(self): ...           # double capacity and rehash all entries
    def __len__(self): return self._size
```

12. Implement all methods. Test with 100 random insertions + 50 lookups.

13. What happens to existing keys when you resize? Why must you **rehash** rather than just copy?

14. Implement `keys()` that returns all keys and `items()` that returns all (key, value) pairs.

---

## Part E — Hash Flooding Attack

15. Consider a hash table where all keys hash to the same bucket (adversarially crafted input). What is the lookup time in the worst case?

16. Python (since 3.3) uses **SipHash** with a random seed for string hashing. How does this prevent hash flooding? What is the trade-off?

17. For a hash function `h(k) = k % M`, if M is a power of 2 (e.g., 16), only the low bits of k affect the bucket. Why is this problematic? What is a better choice for M?

---

## Rubric

| Part | Points |
|---|---|
| A linear probing trace | 24 |
| B tombstone deletion | 20 |
| C chaining vs open addressing | 18 |
| D implementation | 24 |
| E security analysis | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A — final table after insertions</summary>

h values: 10%7=3, 22%7=1, 31%7=3(→4), 4%7=4(→5), 15%7=1(→2), 28%7=0, 17%7=3(→6), 88%7=4(→6 already taken→new slot), 59%7=3(probe 3,4,5,6,0,1,2→2 taken→...).

| Slot | Key  |
|------|------|
| 0    | 28   |
| 1    | 22   |
| 2    | 15   |
| 3    | 10   |
| 4    | 31   |
| 5    | 4    |
| 6    | 17   |
Remaining 88 and 59 require additional probes as the table is nearly full (load=9/7 > 1 — this table would need resizing in practice).
</details>

<details>
<summary>Part B.8 — deletion bug</summary>

Example: keys A, B, C all hash to slot 0. Inserted with linear probing → A at 0, B at 1, C at 2. Delete B: if we mark slot 1 as empty, searching for C: hash=0, check slot 0 (A, not C), check slot 1 (empty → stop). C is not found even though it's in slot 2. The tombstone ensures we continue probing past the deleted slot.
</details>

<details>
<summary>Part C.11 — α for probe count > 5</summary>

Unsuccessful search: 1/(1-α)² × 1/2 for some formulas, or simply 1/(1-α). 

For 1/(1-α) > 5: 1-α < 0.2, so α > 0.8.
</details>
