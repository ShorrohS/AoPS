# Module 6.3 — Hash Tables

---

## The Problem

> You have 10 million user records.
> For each web request, you need to look up a user by username.
> A sorted array gives O(log n) — about 23 comparisons per lookup.
> A linear scan gives O(n) — up to 10 million comparisons.
>
> Can we do better than O(log n)?
> Can we achieve O(1) — constant time regardless of how many users exist?

Yes. The answer is a **hash table** — one of the most important data structures ever invented, used in every database, every caching layer, every programming language's built-in dictionary type.

---

## The Story

### The Birth of Hashing

The concept of hash functions appeared in the early 1950s as a way to accelerate data retrieval on magnetic tape systems, where random access was impossible. **Hans Peter Luhn** of IBM described a hashing technique in 1953 for chained overflow buckets — essentially the same as what we use today.

The first thorough theoretical treatment came from **Arnold Dumey** (1956), who coined the term "hash" and analysed collision resolution strategies. By the 1960s, every major database system used hash indexes for O(1) lookup.

The insight: instead of storing elements in order (requiring log n steps to find), store each element at the index determined by a function of its key. Finding it later requires only recomputing that function — one step, regardless of table size.

---

## The Concept

### The Core Idea

A hash table uses an array of fixed size `M` (the "buckets") and a **hash function** `h(key) → [0, M-1]` to map keys to array indices.

**Insert**: compute `h(key)`, store the key-value pair at `table[h(key)]`.  
**Lookup**: compute `h(key)`, return `table[h(key)]`.  
**Delete**: compute `h(key)`, remove from `table[h(key)]`.

If the hash function maps different keys to different indices, all operations are O(1).

```python
# Extremely simplified — no collision handling
class TinyHashTable:
    def __init__(self, size=16):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        return hash(key) % self.size   # Python's built-in hash function

    def set(self, key, value):
        self.table[self._hash(key)] = value

    def get(self, key):
        return self.table[self._hash(key)]
```

### The Collision Problem

A collision occurs when two different keys hash to the same index. This is inevitable: if you store 1 million keys in a table of 1 million slots, by the Birthday Paradox, collisions start happening after only ~1,000 insertions. Two strategies:

**1. Chaining (Separate Chaining)**

Each bucket holds a linked list of all key-value pairs that hash there:

```
Table:
index 0: → [(alice, 30)] → None
index 1: → None
index 2: → [(bob, 25)] → [(carol, 28)] → None   ← collision
index 3: → [(dave, 22)] → None
...
```

Lookup: hash key → find bucket → scan linked list for matching key.

- **Average case**: O(1) if the load factor (n/M) is bounded by a constant
- **Worst case**: O(n) if all keys hash to the same bucket
- **Space**: extra pointer per element

Python's `dict` uses a variant of open addressing (below), but conceptually, chaining is the cleaner mental model.

**2. Open Addressing (Linear Probing)**

No linked lists — all entries stored in the array itself. On collision, probe for the next empty slot:

```python
def _insert(self, key, value):
    idx = self._hash(key)
    while self.table[idx] is not None:
        if self.table[idx][0] == key:    # update existing
            self.table[idx] = (key, value); return
        idx = (idx + 1) % self.size      # linear probe: try next slot
    self.table[idx] = (key, value)
```

- **Better cache performance** than chaining (no pointer chasing, everything in one array)
- **Clustering problem**: long runs of occupied slots form, making probing slow
- **Load factor must stay below ~0.7** — resize when exceeded
- **Deletion is tricky**: cannot just clear a slot (breaks the probe chain). Use a "tombstone" marker.

**Quadratic probing** (`idx = (idx + c₁i + c₂i²) % M`) and **double hashing** (`idx = (h1(key) + i × h2(key)) % M`) spread keys more evenly and reduce clustering.

### The Hash Function

A good hash function:
- Is deterministic: `h(k) = h(k)` always
- Is fast to compute: ideally O(1) for fixed-size keys
- Distributes keys uniformly across buckets
- Minimises collisions for real-world key distributions

**For integers**: simple approaches include modular hashing `h(k) = k mod M`. But if M is a power of 2, only the low bits matter — if keys cluster in low bits, so do their hashes. Better: use a prime M, or multiply by a large constant and take the high bits.

**For strings**: sum character values mod M is poor (anagrams collide). Better:

```python
def hash_string(s, M):
    h = 0
    for c in s:
        h = (h * 31 + ord(c)) % M   # Horner's method, prime multiplier
    return h
```

Python's `hash()` for strings uses **SipHash-1-3**, a cryptographic-strength hash function, specifically to prevent **hash flooding attacks** — an adversary who knows the hash function can craft inputs that all map to the same bucket, turning O(1) lookup into O(n). SipHash uses a secret seed randomised per process startup.

### Load Factor and Resizing

The **load factor** α = n / M (number of stored items / table size).

With chaining: expected O(1 + α) per lookup. Keep α < 1.  
With open addressing: performance degrades rapidly above α ≈ 0.7. Keep α < 0.7.

When α exceeds the threshold, **resize**: allocate a new table of size ~2M, rehash all existing entries into the new table. This is O(n) work but happens infrequently.

Python's `dict` resizes when 2/3 full. Java's `HashMap` resizes at load factor 0.75.

### Python's dict Implementation

Python `dict` uses **open addressing with pseudo-random probing**:

1. Initial size: 8 slots
2. Hash function: `hash(key) % size` for initial index
3. On collision: use a probe sequence based on the full hash value (not linear) to reduce clustering
4. Load factor threshold: 2/3 → resize to ~2× size, rehash all entries
5. Since Python 3.7: dicts preserve **insertion order** — achieved by maintaining a separate compact array of entry indices

The CPython dict implementation is one of the most carefully optimised data structures in existence. It has been tuned over 30 years to be fast for the most common Python use cases.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Hash Table with Chaining**
- Insert key-value pairs and watch buckets fill
- See collisions form chains
- Look up keys and trace the hash → bucket → list scan
- Observe how uneven hash functions cause clusters

**Tool 2 — Open Addressing / Linear Probing**
- Watch probing in action when a collision occurs
- See the clustering problem develop
- Trigger a resize and watch rehashing

**Tool 3 — Hash Function Quality**
- Test different hash functions on the same set of keys
- See the distribution across buckets
- Compare good vs bad hash functions visually

---

## Going Deeper

**Consistent hashing**: used in distributed databases and content delivery networks. When you add or remove a server, consistent hashing reassigns only n/m keys (where n = total keys, m = number of servers) rather than all keys. This is why DynamoDB, Cassandra, and Memcached can add/remove nodes without a full data reshuffle.

**Robin Hood hashing**: an open addressing variant that keeps probe sequences short by "stealing" slots from rich (low probe count) elements and giving them to poor (high probe count) ones. Used in Rust's `HashMap` and several modern hash table implementations. Achieves better worst-case performance than standard linear probing.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace the insertion of 5 keys into a table of size 7 using linear probing, calculate the expected probe length at load factor 0.5 vs 0.9, implement a hash table class with chaining in Python, and explain why deletion in open addressing requires tombstones.
