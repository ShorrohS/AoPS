# Module 12.2 — Embeddings and Vector Databases

---

## The Problem

> Computers understand numbers. Text, images, audio, code — all must be converted to numbers before a computer can process them.
>
> But a simple conversion (character codes, pixel values) misses semantic structure.
> "cat" and "feline" are the same concept — but their character codes share nothing.
> "cat" and "can" differ by one character — but they are completely different concepts.
>
> **Embeddings** solve this: map objects (words, sentences, images, code) to vectors
> such that semantically similar objects are geometrically close.
> **Vector databases** provide efficient similarity search over millions of these vectors.

---

## The Story

### Word2Vec — Meaning from Context

**Word2Vec** (Mikolov et al., Google, 2013) demonstrated that word meaning could be captured by training a shallow neural network to predict words from their context in a large text corpus ("you shall know a word by the company it keeps" — J.R. Firth, 1957).

The emergent property was remarkable: the resulting vectors supported arithmetic: `king - man + woman ≈ queen`. Geographic capitals, verb tenses, comparative adjectives — the structure of meaning was encoded in geometric relationships between vectors.

**GloVe** (Stanford, 2014) and **FastText** (Facebook, 2016) improved on Word2Vec. But word-level embeddings had a fundamental limitation: "bank" had one vector regardless of whether it meant a financial institution or a river bank.

**BERT** (Google, 2018) introduced contextual embeddings — each token's embedding depends on all surrounding tokens. "Bank" has a different vector in "river bank" and "bank transfer." These contextual embeddings, derived from transformers (Module 12.1), are now the foundation of all embedding models.

---

## The Concept

### What Is an Embedding?

An embedding is a function that maps an object to a dense vector in ℝᵈ where d is typically 128–4096 dimensions.

The critical property: **semantic similarity ≈ geometric proximity**. Objects with similar meaning have vectors that are close (high cosine similarity).

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions

# Text embeddings
e1 = model.encode("The quick brown fox")
e2 = model.encode("A fast auburn canine")    # similar meaning
e3 = model.encode("The stock market fell")   # different topic

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(cosine_sim(e1, e2))   # ≈ 0.78 (similar)
print(cosine_sim(e1, e3))   # ≈ 0.12 (different)
```

### Types of Embeddings

**Word embeddings**: map individual words to vectors. Word2Vec, GloVe, FastText. Useful for token-level tasks.

**Sentence/document embeddings**: map entire sentences or paragraphs to a single vector. Sentence-BERT, OpenAI Ada, Cohere Embed. Used for semantic search, classification, clustering.

**Multimodal embeddings**: map different modalities (text and images) to the same vector space. **CLIP** (OpenAI, 2021) — trained on 400M image-text pairs, can compare images and text directly. Enables: image search with text queries, text-to-image generation guidance.

**Code embeddings**: map code snippets to vectors capturing functional semantics. OpenAI code-embedding, CodeBERT. Enables: code search ("find all functions that sort a list"), similar code detection, documentation search.

### Vector Similarity Search

Given a query vector `q` and a database of `n` vectors `{v₁, ..., vₙ}`, find the k most similar vectors.

**Brute force**: compute cosine similarity with all `n` vectors. O(n×d) per query. Exact but slow for large n.

**Approximate Nearest Neighbour (ANN)**: trade small accuracy loss for massive speed-up. Used in all production vector databases.

**FAISS** (Facebook AI Similarity Search):

```python
import faiss
import numpy as np

# Build an index
d = 384            # embedding dimension
n = 1_000_000      # number of vectors

embeddings = np.random.randn(n, d).astype('float32')
embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)   # normalise

# IVF (Inverted File) index: cluster vectors, search only relevant clusters
nlist = 100        # number of clusters
quantiser = faiss.IndexFlatIP(d)   # exact search within cluster
index = faiss.IndexIVFFlat(quantiser, d, nlist, faiss.METRIC_INNER_PRODUCT)
index.train(embeddings)            # cluster the data
index.add(embeddings)              # add all vectors

# Search
query = np.random.randn(1, d).astype('float32')
query /= np.linalg.norm(query)

index.nprobe = 10                  # search 10 clusters (speed/accuracy tradeoff)
distances, indices = index.search(query, k=5)
# Returns indices of 5 nearest neighbours in ~milliseconds
```

**HNSW (Hierarchical Navigable Small World)**: a graph-based ANN algorithm. Vectors are nodes; edges connect nearby vectors in a hierarchy of layers. Search navigates the graph greedily from the top layer. Very fast (~1ms for millions of vectors), good accuracy. Used by Weaviate, Qdrant.

### Vector Databases

Production systems managing millions of embeddings use purpose-built **vector databases**:

| Database | Backend | Hosted | Open source |
|---|---|---|---|
| Pinecone | Proprietary | Yes | No |
| Weaviate | HNSW | Self/hosted | Yes |
| Qdrant | HNSW | Self/hosted | Yes |
| Chroma | HNSW | Self | Yes |
| pgvector | IVF/HNSW | PostgreSQL | Yes |
| FAISS | IVF/PQ | Self | Yes (library) |

They provide: vector storage + retrieval, metadata filtering, hybrid search (dense + sparse), real-time updates.

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(":memory:")  # in-memory for demo

client.create_collection(
    collection_name="docs",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Insert vectors with metadata
client.upsert("docs", [
    PointStruct(id=1, vector=embeddings[0].tolist(), payload={"text": "...", "source": "doc1.pdf"}),
    PointStruct(id=2, vector=embeddings[1].tolist(), payload={"text": "...", "source": "doc2.pdf"}),
])

# Search
results = client.search("docs", query_vector=query[0].tolist(), limit=5)
```

### Embedding Fine-Tuning

Pre-trained embedding models may not capture domain-specific meaning. Fine-tuning on domain data improves retrieval quality:

**Contrastive learning**: train the model so similar pairs (query, relevant document) have high similarity and dissimilar pairs have low similarity:

```
Loss = -log(exp(sim(q, d+) / τ) / Σⱼ exp(sim(q, dⱼ) / τ))
```
where d+ is the positive (relevant) document, dⱼ are all documents in the batch, τ is temperature.

**INSTRUCTOR** and **E5** are instruction-tuned embedding models that can be customised via natural language: `INSTRUCTION: Represent the technical documentation for retrieval. INPUT: {document}`.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Embedding Space Explorer**
- Enter 6–8 sentences on different topics
- See their 2D PCA projection
- Watch semantic clusters emerge (technology, food, sports)

**Tool 2 — Semantic Search Demo**
- 20 pre-embedded documents
- Type a query and see top-3 retrieved by cosine similarity
- Compare to keyword search — see where semantic search wins and loses

**Tool 3 — Embedding Arithmetic**
- Word embeddings with addition/subtraction
- "king" - "man" + "woman" → see nearest vectors
- "Paris" - "France" + "Germany" → see nearest vectors

---

## Going Deeper

**Matryoshka Representation Learning (MRL)**: train embedding models so that the first d dimensions of a 1536-d embedding are themselves a good d-dimensional embedding. This allows using shorter embeddings (faster, cheaper) for coarse search and longer embeddings for re-ranking. OpenAI's text-embedding-3 models support Matryoshka embeddings.

**Late interaction models (ColBERT)**: instead of compressing a document to one vector, keep all token-level vectors. At query time, compute the maximum similarity between each query token and each document token (MaxSim). Much more accurate than single-vector retrieval, but requires more storage and more compute.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Implement cosine similarity from scratch (without any ML library), build a simple 10-document semantic search engine using sentence-transformers and FAISS, demonstrate the analogy `"king - man + woman"` using pre-computed word vectors, and explain the tradeoff between HNSW accuracy and speed (what happens as you increase ef_search in an HNSW index?).
