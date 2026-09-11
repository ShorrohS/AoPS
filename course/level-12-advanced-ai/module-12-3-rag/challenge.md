# Challenge 12.3 — Retrieval-Augmented Generation

**Type:** Implementation + analysis + evaluation  
**Estimated time:** 50–60 minutes  
**Tools needed:** Python + sentence-transformers

---

## Part A — Minimal RAG System

1. Build a minimal RAG system in Python that:
   - Indexes 10 text documents (hardcoded, no external API needed)
   - Embeds them using `sentence-transformers` (or mock with random vectors for testing)
   - For a query, retrieves the top-2 most similar documents by cosine similarity
   - Assembles and prints a prompt: `"Answer based on: {docs}\n\nQuestion: {query}"`

```python
docs = [
    "Python was created by Guido van Rossum and released in 1991.",
    "The GIL in CPython prevents true multi-threading for CPU-bound tasks.",
    "NumPy provides efficient n-dimensional array operations.",
    "Flask is a lightweight Python web framework.",
    "Django is a full-featured Python web framework with ORM.",
    "SQLite is a serverless, zero-configuration embedded database.",
    "Git is a distributed version control system created by Linus Torvalds.",
    "Docker containers package applications with their dependencies.",
    "Kubernetes orchestrates containerised applications at scale.",
    "REST APIs use HTTP methods for CRUD operations on resources.",
]
```

2. Query: "What is the GIL in Python?" Show which 2 documents are retrieved and the assembled prompt.

3. Query: "How do I deploy a Python app?" Show the retrieved documents. Are they the ideal retrievals? What would improve them?

---

## Part B — Retrieval Metrics

For a given set of 5 queries, you know the "gold" relevant documents:

| Query | Gold Relevant | Retrieved Top-3 |
|---|---|---|
| "Python GIL" | doc2 | doc2, doc1, doc3 |
| "web frameworks" | doc4, doc5 | doc4, doc10, doc5 |
| "databases" | doc6 | doc8, doc9, doc6 |
| "version control" | doc7 | doc7, doc1, doc2 |
| "containers" | doc8, doc9 | doc8, doc4, doc9 |

4. Calculate **context precision** for each query: of the retrieved Top-3, what fraction are actually relevant?

5. Calculate **context recall** for each query: of the gold relevant documents, what fraction were retrieved in the Top-3?

6. Average precision and recall across all 5 queries. Which is higher? What does this suggest about the retrieval system?

---

## Part C — Chunking Strategy

7. Take the following passage (3 paragraphs) and chunk it three different ways. Show the resulting chunks for each strategy:
   - Fixed-size: 100-character chunks with 20-character overlap
   - Sentence-level: split on `.`
   - Paragraph-level: split on `\n\n`

```
Python is a high-level programming language. It was created by Guido van Rossum.
Python emphasises code readability and simplicity. The language supports multiple programming paradigms.

Python's ecosystem includes NumPy for numerical computing. Pandas is used for data manipulation.
Flask and Django are popular web frameworks. SQLAlchemy provides database ORM functionality.

Python is widely used in data science and machine learning. TensorFlow and PyTorch are built on Python.
Jupyter notebooks enable interactive computing. The language has become dominant in AI research.
```

8. Which chunking strategy would produce the best retrieval for: "What numerical computing tools does Python have?" Show which chunk(s) would be retrieved.

---

## Part D — Failure Modes

For each scenario, identify the RAG failure mode and propose a mitigation:

9. A user asks about events that happened after the document corpus was last updated. The LLM correctly refuses to answer and says "I don't have information about that."

10. A user asks "What is the difference between Flask and Django?" The retrieval returns only the Flask document (doc4) and misses the Django document (doc5). The LLM gives an incomplete comparison.

11. A user asks a question whose answer requires synthesising information from 4 different documents. The system retrieves only 3 documents (top-k=3). The LLM produces a partially correct answer.

12. The retrieved document is correct but 3,000 words long. The LLM produces an answer that misses key details buried in the middle of the document (the "lost in the middle" problem).

---

## Part E — Hybrid Retrieval

13. Dense retrieval (embedding similarity) excels at semantic matching. BM25 sparse retrieval excels at keyword matching. Construct a query where dense retrieval fails but BM25 succeeds:
    - Query: "What is RFC 7519?"
    - Why would semantic search fail? What would BM25 find?

14. **Reciprocal Rank Fusion (RRF)** combines dense and sparse rankings:
    ```python
    rrf_score(doc, k=60) = Σ_rankers 1 / (k + rank(doc, ranker))
    ```
    For doc A ranked #1 by dense and #3 by BM25, and doc B ranked #2 by dense and #1 by BM25:
    - Calculate RRF score for A and B with k=60
    - Which document wins the combined ranking?

---

## Rubric

| Part | Points |
|---|---|
| A minimal RAG | 22 |
| B retrieval metrics | 20 |
| C chunking | 18 |
| D failure modes | 22 |
| E hybrid retrieval | 18 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part B.4–6 — metrics</summary>

Precision per query (relevant retrieved / 3):
- GIL: 1/3 = 0.33
- web: 2/3 = 0.67
- databases: 1/3 = 0.33
- VCS: 1/3 = 0.33
- containers: 2/3 = 0.67
Average precision: (0.33+0.67+0.33+0.33+0.67)/5 = **0.47**

Recall per query (relevant retrieved / total relevant):
- GIL: 1/1 = 1.0
- web: 2/2 = 1.0
- databases: 1/1 = 1.0
- VCS: 1/1 = 1.0
- containers: 2/2 = 1.0
Average recall: **1.0**

Recall is perfect (all relevant docs found) but precision is low (irrelevant docs included). The system retrieves too broadly. Reducing top-k or raising the similarity threshold would improve precision.
</details>

<details>
<summary>Part E.14 — RRF calculation</summary>

Doc A: dense rank=1, BM25 rank=3. RRF = 1/(60+1) + 1/(60+3) = 1/61 + 1/63 = 0.01639 + 0.01587 = **0.03226**

Doc B: dense rank=2, BM25 rank=1. RRF = 1/(60+2) + 1/(60+1) = 1/62 + 1/61 = 0.01613 + 0.01639 = **0.03252**

Doc B wins (0.03252 > 0.03226) — BM25 rank-1 outweighs the dense rank difference.
</details>
