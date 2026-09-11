# Challenge 12.2 — Embeddings and Vector Databases

**Type:** Implementation + calculation + analysis  
**Estimated time:** 50–60 minutes  
**Tools needed:** Python + NumPy (sentence-transformers optional)

---

## Part A — Cosine Similarity from Scratch

1. Implement `cosine_similarity(a, b)` without using any ML library. Only NumPy for array operations is allowed.

2. Given these vectors:
   ```python
   cat   = [0.9, 0.1, -0.3, 0.7, -0.2]
   feline = [0.8, 0.2, -0.4, 0.6, -0.1]
   dog    = [0.7, -0.2, 0.5, 0.1, 0.4]
   car    = [-0.1, 0.9, 0.8, -0.3, 0.6]
   ```
   Compute all pairwise cosine similarities. Which pair is most similar? Which is least?

3. Normalise all four vectors to unit length. What is the cosine similarity between two unit vectors equal to? What operation does this reduce to?

---

## Part B — Word Analogy

4. Using pre-computed word vectors from a `dict` (provided below), compute the vector for the analogy `king - man + woman`:
   ```python
   vectors = {
       'king':  [0.9, 0.1, 0.8, -0.1],
       'man':   [0.8, -0.1, 0.2, 0.0],
       'woman': [0.7, 0.1, 0.2, 0.9],
       'queen': [0.8, 0.1, 0.8, 0.8],
       'prince':[0.9, 0.2, 0.7, -0.2],
       'cat':   [0.1, 0.9, -0.1, 0.0],
   }
   ```
   
   Compute `king - man + woman`. Which of the other vectors is closest to the result?

5. Why does vector arithmetic like this "work"? What property of the embedding space enables this? Is it guaranteed to work for all analogies?

---

## Part C — FAISS Index

6. Implement a simple brute-force vector search:
   ```python
   class SimpleVectorIndex:
       def __init__(self): self.vectors = []; self.ids = []
       def add(self, vector, id): ...
       def search(self, query, k=3): ...   # return k most similar (id, score) pairs
   ```
   Use cosine similarity for scoring.

7. For 1,000,000 vectors of dimension 384, how many multiplications does brute-force search perform per query? Calculate in millions of operations.

8. FAISS with an IVF index clusters vectors into C=1000 groups. With `nprobe=10` (search 10 clusters), what fraction of vectors is examined per query? How does this trade accuracy for speed?

---

## Part D — Semantic Search Demo

9. Build a 10-document semantic search engine using cosine similarity:
   - Use the 10 documents from the RAG challenge (or similar)
   - Embed each with a real or mock embedding function
   - For a query, return top-3 documents sorted by similarity
   - Print document text and similarity score

10. Compare semantic search vs keyword search for: "fast numerical operations in Python"
    - Keyword: which documents contain all of "fast", "numerical", "operations", "Python"?
    - Semantic: which documents have the closest embedding to the query?
    - Which gives better results?

---

## Part E — Matryoshka Embeddings

11. OpenAI's `text-embedding-3-small` supports **Matryoshka embeddings**: the first 256 dimensions of a 1536-dim embedding are themselves a good 256-dim embedding.

    Suppose you have a collection of 10 million documents. Compare:
    - Search with full 1536-dim vectors (exact brute-force): memory and compute
    - Two-stage search: retrieve top-1000 with 256-dim vectors (fast), re-rank top-1000 with full 1536-dim (accurate)
    
    Calculate memory savings for storing 10M vectors at each dimensionality (float32 = 4 bytes per dimension).

12. What is the practical trade-off of using shorter embeddings? When would you use 256-dim vs 1536-dim?

---

## Rubric

| Part | Points |
|---|---|
| A cosine similarity | 20 |
| B word analogy | 18 |
| C FAISS index | 22 |
| D semantic search | 22 |
| E Matryoshka | 18 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1–3</summary>

```python
import numpy as np

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0: return 0.0
    return dot / (norm_a * norm_b)
```

cat-feline ≈ 0.996 (most similar). cat-car ≈ -0.03 (least similar — near orthogonal).

Unit vectors: cosine similarity = dot product (since both norms = 1). `cos(a,b) = a·b / (1×1) = a·b`.
</details>

<details>
<summary>Part E.11 — memory calculation</summary>

1536-dim × 4 bytes × 10M = 61,440 MB ≈ **60 GB**
256-dim × 4 bytes × 10M = 10,240 MB ≈ **10 GB**

Two-stage approach saves 50 GB of memory for the main index. The full 1536-dim vectors are only loaded for the top-1000 candidates (1000 × 1536 × 4 = 6 MB — tiny).

Trade-off: shorter embeddings have lower recall (may miss some relevant documents in the first stage). Use 256-dim when memory is constrained or latency matters most; use 1536-dim when recall/accuracy is critical.
</details>
