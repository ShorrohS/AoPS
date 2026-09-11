# Module 12.1 — Large Language Models: Architecture and Training

---

## The Problem

> In 2017, a team at Google published "Attention Is All You Need."
> The transformer architecture they described — without convolutions or recurrence —
> became the foundation of GPT, BERT, Claude, Gemini, LLaMA,
> and virtually every large language model in existence.
>
> How does a system trained to predict the next word in a document
> learn to write code, translate languages, answer questions,
> and reason about complex problems?
>
> Understanding the transformer architecture — from attention mechanisms
> to the training process — is the prerequisite for working with
> any modern AI system at a technical level.

---

## The Story

### The Road to Transformers

**Recurrent Neural Networks (RNNs)** and their variants — LSTMs (Hochreiter & Schmidhuber, 1997) and GRUs — dominated sequence modelling from the 2000s. They processed tokens one at a time, maintaining a hidden state. The problem: long-range dependencies were hard to learn (vanishing gradients even with LSTM), and sequential processing prevented parallelisation.

**Sequence-to-sequence models** (Sutskever, Vinyals, Le, 2014) added an encoder-decoder structure with attention — the decoder could "attend" to different parts of the encoder's output. This was the breakthrough for machine translation.

**"Attention Is All You Need"** (Vaswani et al., Google, 2017) eliminated recurrence entirely. Pure attention. Every token attends to every other token in the sequence simultaneously. Training is fully parallelisable. The result: dramatically larger models could be trained.

**GPT-1** (OpenAI, 2018): the first demonstration that large-scale pretraining on text + fine-tuning worked for many tasks. 117 million parameters. GPT-2 (2019): 1.5B parameters. GPT-3 (2020): 175B parameters, few-shot learning without fine-tuning. GPT-4 (2023): architecture undisclosed, dramatically better. The scale at which capabilities emerged was surprising even to the researchers.

---

## The Concept

### Tokenisation

Before processing text, the model converts it to tokens — integer IDs from a fixed vocabulary.

**BPE (Byte Pair Encoding)**: the dominant tokenisation scheme for LLMs. Start with individual bytes, iteratively merge the most frequent adjacent pair:

```
"the cat sat" → ["the", " cat", " sat"]
                → [464, 3797, 4992]  (GPT-4 token IDs)
```

GPT-4 uses ~100,000 tokens. Common words are single tokens ("the" → 1 token). Uncommon or non-English words may split into multiple tokens ("Königsberg" → ["K", "ön", "igs", "berg"] → 4 tokens).

**Why it matters**: token count affects both cost and context length. A 4,096-token context window is roughly 3,000 words of English.

### The Transformer Architecture

```
Input tokens
     ↓
[Token Embeddings + Positional Embeddings]
     ↓
[Transformer Block 1]
[Transformer Block 2]
...
[Transformer Block N]
     ↓
[Linear + Softmax]
     ↓
Next token probabilities
```

**Each Transformer Block:**
```
Input
  ↓
[Multi-Head Self-Attention]
  ↓ (+ residual connection)
[Layer Normalisation]
  ↓
[Feed-Forward Network (MLP)]
  ↓ (+ residual connection)
[Layer Normalisation]
  ↓
Output
```

### Self-Attention — The Core Mechanism

Self-attention allows every token to "look at" every other token and incorporate relevant context.

For each token, compute three vectors via learned linear projections:
- **Query (Q)**: "what am I looking for?"
- **Key (K)**: "what do I contain?"
- **Value (V)**: "what do I provide if attended to?"

```python
import numpy as np

def self_attention(X, W_Q, W_K, W_V):
    # X shape: (seq_len, d_model)
    Q = X @ W_Q    # (seq_len, d_k)
    K = X @ W_K    # (seq_len, d_k)
    V = X @ W_V    # (seq_len, d_v)

    # Attention scores: how much each token attends to each other
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)    # (seq_len, seq_len)

    # For causal (decoder) models: mask future tokens
    # scores[i, j] = -inf if j > i  (can't attend to future)

    # Softmax over keys for each query
    weights = softmax(scores, axis=-1)    # (seq_len, seq_len)

    # Weighted sum of values
    output = weights @ V    # (seq_len, d_v)
    return output
```

**Multi-head attention**: run h parallel attention heads with different W_Q, W_K, W_V projections. Each head can attend to different aspects of the input. Concatenate and project:

```python
def multi_head_attention(X, num_heads, W_Q, W_K, W_V, W_O):
    # Split into heads, apply attention, concatenate
    head_dim = d_model // num_heads
    heads = []
    for h in range(num_heads):
        # Each head has its own projections
        out = self_attention(X, W_Q[h], W_K[h], W_V[h])
        heads.append(out)
    concat = np.concatenate(heads, axis=-1)   # (seq_len, d_model)
    return concat @ W_O                        # (seq_len, d_model)
```

### Positional Encoding

Self-attention is order-invariant (shuffling tokens gives the same attention scores). Positional encodings inject position information:

**Sinusoidal positional encoding** (original Transformer):
```python
def positional_encoding(seq_len, d_model):
    PE = np.zeros((seq_len, d_model))
    for pos in range(seq_len):
        for i in range(0, d_model, 2):
            PE[pos, i]   = np.sin(pos / 10000**(i / d_model))
            PE[pos, i+1] = np.cos(pos / 10000**(i / d_model))
    return PE
```

Modern LLMs (GPT-NeoX, LLaMA) use **RoPE (Rotary Positional Embedding)** — relative position encoding that generalises better to sequences longer than seen during training.

### Pretraining: Next-Token Prediction

LLMs are trained on the **causal language modelling** objective: given tokens 1..t, predict token t+1. For a sequence of N tokens, one forward pass generates N training examples (teacher forcing):

```python
# Input:  [The, cat, sat, on]
# Target: [cat, sat, on, the]   (each token predicts the next)

# Cross-entropy loss over vocabulary for each position
loss = -sum(log P(token_t+1 | tokens_1..t) for t in 1..N-1) / (N-1)
```

This simple objective — **predict the next token** — when applied to hundreds of billions of tokens from the web, books, and code, produces a model that learns to compress and generalise the statistical structure of human language and knowledge.

Why does next-token prediction produce "understanding"? The hypothesis: to predict the next token well, a model must learn everything knowable about the context — facts, reasoning patterns, coding conventions, stylistic norms. The task is simple; the knowledge required to do it well is enormous.

### Inference: Autoregressive Generation

At inference time, the model generates tokens one at a time:

```python
def generate(model, prompt_tokens, max_new_tokens, temperature=1.0):
    tokens = list(prompt_tokens)
    for _ in range(max_new_tokens):
        logits = model.forward(tokens)        # (vocab_size,) for last position
        logits /= temperature                  # temperature scales confidence
        probs = softmax(logits)
        next_token = np.random.choice(len(probs), p=probs)   # sample
        tokens.append(next_token)
        if next_token == EOS_TOKEN: break
    return tokens[len(prompt_tokens):]
```

**Temperature**: lower → more deterministic (greedy), higher → more random.
**Top-k sampling**: only consider the k most likely tokens.
**Top-p (nucleus) sampling**: only consider tokens whose cumulative probability ≥ p.

The **KV cache** stores key/value matrices for previously generated tokens, so each new token only requires one new row of attention computation rather than recomputing the entire sequence.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Attention Pattern Visualiser**
- Input a short sentence
- See the attention weight matrix for each head
- Observe which tokens attend to which others (e.g., pronouns attending to their antecedents)

**Tool 2 — Tokeniser**
- Enter text; watch it get tokenised
- See how different languages tokenise (English vs Chinese vs code)
- Count tokens to understand context window implications

**Tool 3 — Autoregressive Generation**
- A tiny language model (for demonstration)
- Watch token-by-token generation
- Adjust temperature: see deterministic vs random output

---

## Going Deeper

**Scaling laws**: Kaplan et al. (OpenAI, 2020) showed that language model loss decreases as a power law with: number of parameters (N), training tokens (D), and compute (C=6ND). These scaling laws predicted the performance of GPT-3 and GPT-4 before they were trained. They also suggested an "optimal" allocation of compute between model size and data size.

**Emergent capabilities**: behaviours that appear only above certain model scales — arithmetic, chain-of-thought reasoning, code generation, in-context learning. Smaller models simply cannot do these things; larger models do them without explicit training on those tasks. The emergence appears sudden relative to scale. Understanding why capabilities emerge at scale is one of the most important open questions in AI research.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Implement scaled dot-product attention from scratch in NumPy for a 4-token sequence, trace what happens to the KV cache as the model generates a 10-token response (how many key/value vectors are stored?), tokenise a given sentence using a simple BPE vocabulary, and explain why a model trained on next-token prediction can perform few-shot learning (completing tasks described in the prompt it has never explicitly trained on).
