# Module 12.3 — Retrieval-Augmented Generation

---

## The Problem

> A large language model knows everything in its training data — up to its cutoff date.
> But it cannot:
> - Access information created after training
> - Look up specific private documents you have
> - Cite its sources reliably
> - Know about your company's internal policies
>
> **RAG (Retrieval-Augmented Generation)** solves this by combining
> a retrieval system with a language model:
> instead of relying entirely on parametric memory (weights),
> the model retrieves relevant context at query time and uses it to answer.

---

## The Story

### From Parametric to Non-Parametric Knowledge

Early neural networks had no external memory — all knowledge was encoded in parameters. **Neural Turing Machines** (Graves et al., Google DeepMind, 2014) added an external memory with differentiable read/write heads — inspired by Turing's theoretical computing model.

**RAG** (Lewis et al., Facebook AI Research, 2020) applied a simpler but practical approach: use a non-parametric retrieval system (dense passage retrieval with FAISS) combined with a generative model. The model sees retrieved documents concatenated to the question. It was the first major demonstration that retrieval could dramatically improve factuality.

With the commercial success of ChatGPT (2022), RAG became the dominant architecture for enterprise AI applications: internal knowledge bases, customer support chatbots, code assistance with private repositories, legal document search.

---

## The Concept

### RAG System Architecture

```
User query
    ↓
[Query Encoder]          ← embedding model
    ↓
Query embedding vector
    ↓
[Vector Similarity Search]  ← FAISS / Pinecone / Weaviate
    ↓
Top-k relevant documents
    ↓
[Prompt Assembly]
    ↓
"Answer based on these documents: {docs}\n\nQuestion: {query}"
    ↓
[LLM (GPT-4, Claude, Llama, etc.)]
    ↓
Response (grounded in retrieved documents)
```

### Embeddings and Vector Search

A **text embedding** is a dense vector representation of text that captures semantic meaning. Texts with similar meaning have similar vectors (high cosine similarity).

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

texts = [
    "The cat sat on the mat.",
    "A feline rested on a rug.",
    "The stock market rose today.",
]

embeddings = model.encode(texts)    # shape: (3, 384)

# Cosine similarity between first two (semantically similar)
cos_01 = np.dot(embeddings[0], embeddings[1]) / (
         np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
# ≈ 0.85 (very similar)

# Cosine similarity between first and third (different topic)
cos_02 = np.dot(embeddings[0], embeddings[2]) / (
         np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[2]))
# ≈ 0.15 (very different)
```

### Building a RAG System from Scratch

**Step 1: Indexing** — run once when documents change

```python
import faiss
from sentence_transformers import SentenceTransformer

def build_index(documents):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(documents, convert_to_numpy=True)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)  # normalise

    # FAISS index for cosine similarity (using inner product on normalised vectors)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index, embeddings

documents = [
    "Python was created by Guido van Rossum in 1991.",
    "The GIL in CPython prevents true parallelism for CPU-bound threads.",
    "NumPy provides efficient array operations built on LAPACK/BLAS.",
    # ... thousands more documents
]
index, embeddings = build_index(documents)
```

**Step 2: Retrieval** — run for each query

```python
def retrieve(query, index, documents, model, k=3):
    query_embedding = model.encode([query], convert_to_numpy=True)
    query_embedding /= np.linalg.norm(query_embedding, axis=1, keepdims=True)

    # Find k nearest neighbours
    scores, indices = index.search(query_embedding, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        results.append({
            'document': documents[idx],
            'score': float(score),
        })
    return results
```

**Step 3: Generation** — use retrieved documents as context

```python
import openai

def rag_answer(query, retrieved_docs):
    context = "\n\n".join([f"[{i+1}] {d['document']}" for i, d in enumerate(retrieved_docs)])

    prompt = f"""You are a helpful assistant. Answer the question using ONLY the provided context.
If the context does not contain the answer, say "I don't have information about that."

Context:
{context}

Question: {query}

Answer:"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Full pipeline
query = "Does Python have a GIL?"
retrieved = retrieve(query, index, documents, embedding_model)
answer = rag_answer(query, retrieved)
```

### Chunking Strategy

Documents must be split into chunks before embedding. Chunking strategy dramatically affects retrieval quality:

**Fixed-size chunks**: split every N characters (simple, fast, breaks mid-sentence).

**Sentence/paragraph chunks**: split on sentence boundaries (better coherence, variable size).

**Sliding window**: overlapping chunks so context boundaries don't cause misses:
```python
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        if i + chunk_size >= len(words): break
    return chunks
```

**Semantic chunking**: split when topic changes (detected by embedding similarity drop). More expensive but better for heterogeneous documents.

### RAG Evaluation

How do you measure whether a RAG system is working?

**Retrieval metrics:**
- **Context recall**: what fraction of the answer's relevant information was retrieved?
- **Context precision**: what fraction of retrieved documents are relevant?

**Generation metrics:**
- **Faithfulness**: does the answer only use information from the retrieved context? (measures hallucination)
- **Answer relevance**: does the answer actually address the question?

**Ragas** (open-source RAG evaluation framework) automates these measurements using an LLM as a judge.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Embedding Similarity Visualiser**
- Enter several text snippets
- See their 2D PCA projection (collapsed from high-dimensional embedding space)
- Watch similar texts cluster together

**Tool 2 — RAG Pipeline Demo**
- A pre-indexed set of 20 documents
- Enter a query and watch: embedding → retrieval → top-k → prompt assembly → answer
- Edit the prompt template and see how the answer changes

**Tool 3 — Chunking Strategies**
- A long document chunked in three ways: fixed-size, sentence-level, sliding window
- Issue a query and see which strategy retrieves the best context

---

## Going Deeper

**Hybrid retrieval**: combine dense vector search (semantic similarity) with BM25 sparse retrieval (keyword matching). Reciprocal Rank Fusion (RRF) merges the two ranked lists. Hybrid retrieval consistently outperforms pure dense or sparse retrieval on diverse queries — especially for technical terms and proper nouns that dense models may not embed well.

**GraphRAG** (Microsoft, 2024): instead of retrieving individual document chunks, build a knowledge graph from the corpus. Queries traverse the graph to find semantically related entities and relationships, then summarise the subgraph. Dramatically better for questions that require synthesising information across many documents rather than finding a single relevant passage.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Build a minimal RAG system in Python that indexes 10 text documents, retrieves the top-2 relevant documents for a query, and assembles a prompt. Calculate the retrieval precision and recall for a given query given known relevant documents. Explain when RAG fails to retrieve the right context (give two concrete scenarios), and describe how you would handle a query that requires synthesising information from 5 different documents.
