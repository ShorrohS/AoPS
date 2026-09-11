# Challenge 12.1 — Large Language Models: Architecture and Training

**Type:** Derivation + implementation + analysis  
**Estimated time:** 55–65 minutes  
**Tools needed:** Python + NumPy

---

## Part A — Self-Attention from Scratch

Implement **scaled dot-product attention** for a 4-token sequence.

Given:
```python
import numpy as np

# 4 tokens, d_model=4, d_k=4
Q = np.array([[1,0,1,0],[0,1,0,1],[1,1,0,0],[0,0,1,1]], dtype=float)  # (4,4)
K = np.array([[1,0,0,1],[0,1,1,0],[1,1,0,0],[0,0,1,1]], dtype=float)  # (4,4)
V = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], dtype=float)  # (4,4)
```

1. Compute the **attention scores**: `scores = Q @ K.T / sqrt(d_k)`. Show the resulting (4,4) matrix.

2. Apply **causal masking** (decoder/GPT-style): set `scores[i,j] = -inf` for all j > i (token i cannot attend to future token j). Show the masked matrix.

3. Apply **softmax** row-wise to the masked scores. What does softmax(-inf) become?

4. Compute the **output**: `output = softmax_scores @ V`. What is the shape? What does each row represent?

5. Implement this complete function: `scaled_dot_product_attention(Q, K, V, mask=None)`. Verify your result matches NumPy computation.

---

## Part B — KV Cache

A GPT-style model generates a response to a 10-token prompt, producing 20 new tokens.

6. Without a KV cache: for each new token, the model recomputes K and V for all previous tokens. For token generation step t (generating the t-th new token after the prompt), how many tokens' K and V vectors are recomputed unnecessarily?

7. With a KV cache: K and V are computed once and stored. For each attention layer L, what is the shape of the KV cache after generating 20 tokens? (prompt=10, generated=20, d_model=512, n_heads=8, d_k=64)

8. The KV cache grows linearly with sequence length. For a 1M-token context window, a 32-layer model, 32 heads, d_k=128, float16 (2 bytes): calculate the KV cache size in GB.

---

## Part C — Tokenisation

9. Using a simple BPE vocabulary where single characters and the following bigrams are tokens:
   `{'th': 100, 'he': 101, 'in': 102, 'er': 103, 'an': 104, ' t': 105, 'ion': 106}`
   
   Tokenise the word "attention" greedily (longest match first). Show each step.

10. The same word "attention" in a language model with a different vocabulary might tokenise differently. Why does this matter for tasks like counting letters or reversing words?

11. A user asks an LLM to count the letters in "strawberry". The model often says 8 (wrong — it's 10). Explain why this happens at the token level. What would help the model get it right?

---

## Part D — Training and Scaling

12. A transformer with:
    - Layers: 12
    - Hidden size: 768
    - Attention heads: 12
    - FFN intermediate size: 3072
    
    Calculate the parameter count for one transformer block (attention + FFN only). Then multiply by 12 for the full model.
    (Attention params per head: 4 matrices of shape d_model × d_k; FFN: two matrices)

13. **Scaling laws**: a model trained on 10× more data (same architecture) reduces loss by roughly 0.5×. A model with 10× more parameters (same data) reduces loss by roughly 0.3×. Which provides more benefit per dollar of compute? What does this suggest about optimal training strategy?

14. GPT-3 (175B parameters) was trained on 300B tokens. Is this optimal per Chinchilla scaling laws (`optimal_tokens ≈ 20 × parameters`)? How many tokens would be optimal for 175B parameters?

---

## Part E — Inference and Generation

15. Explain the difference between **greedy decoding**, **top-k sampling**, and **top-p (nucleus) sampling**. For each:
    - Describe the algorithm in one sentence
    - Give a scenario where it produces better or worse output than the others

16. **Temperature**: a logit vector is `[-2, 0, 3, 1]`. Compute the softmax at temperature T=0.5 and T=2.0. Which temperature makes the distribution more peaked? Which makes it more uniform?

---

## Rubric

| Part | Points |
|---|---|
| A self-attention | 28 |
| B KV cache | 20 |
| C tokenisation | 18 |
| D training and scaling | 20 |
| E inference | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1–4 — attention computation</summary>

```python
import numpy as np

def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)         # (4,4)

    if mask is not None:
        scores = np.where(mask, scores, -1e9)  # -1e9 approximates -inf

    # Softmax (numerically stable)
    scores_exp = np.exp(scores - scores.max(axis=-1, keepdims=True))
    weights = scores_exp / scores_exp.sum(axis=-1, keepdims=True)

    return weights @ V   # (4,4)

# Causal mask (lower triangular)
mask = np.tril(np.ones((4,4), dtype=bool))
output = scaled_dot_product_attention(Q, K, V, mask)
```

Output shape: (4, 4). Each row i is the attention-weighted combination of V rows, where token i can only attend to tokens 0..i (causal).
</details>

<details>
<summary>Part B.8 — KV cache size</summary>

After 30 tokens (10 prompt + 20 generated):
- Per layer, K shape: (30, 32, 128) = 122,880 values
- Per layer, V shape: same
- Both K and V: 245,760 values per layer
- 32 layers: 32 × 245,760 = 7,864,320 values
- float16 (2 bytes): 15,728,640 bytes ≈ 15 MB for 30 tokens

For 1M tokens: 1,000,000/30 × 15 MB ≈ **500 GB**. This is why long-context models require significant GPU memory.
</details>

<details>
<summary>Part E.16 — temperature</summary>

logits = [-2, 0, 3, 1]. Softmax at temperature T: softmax(logits/T).

T=0.5: logits/T = [-4, 0, 6, 2]. exp = [0.018, 1, 403.4, 7.39]. Sum=411.8. Probs ≈ [0.000, 0.002, 0.979, 0.018]. Very peaked on token 2.

T=2.0: logits/T = [-1, 0, 1.5, 0.5]. exp = [0.368, 1, 4.48, 1.65]. Sum=7.50. Probs ≈ [0.049, 0.133, 0.597, 0.220]. More uniform.

Lower temperature → sharper/more deterministic. Higher temperature → softer/more random.
</details>
