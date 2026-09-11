# Challenge 11.5 — Backpropagation: Derived and Implemented

**Type:** Derivation + implementation + verification  
**Estimated time:** 55–65 minutes  
**Tools needed:** Python + NumPy

---

## Part A — Chain Rule Derivation

A single linear layer (no activation): `ŷ = Xw + b`, loss `L = (1/n)||ŷ - y||²`.

1. Derive `∂L/∂ŷ` analytically. Show every step.

2. Using the chain rule, derive `∂L/∂w = ∂L/∂ŷ × ∂ŷ/∂w`. What is `∂ŷ/∂w`? Write the final expression for `∂L/∂w` in matrix form.

3. Derive `∂L/∂b`. What is it in vector form?

4. Verify your gradients numerically (gradient checking): compute `∂L/∂w[i]` as `(L(w + ε·eᵢ) - L(w - ε·eᵢ)) / (2ε)` for ε=1e-5 and compare to your analytical gradient. They should agree to ~5 decimal places.

---

## Part B — Sigmoid Backward Pass

5. The sigmoid activation `σ(z) = 1/(1+e⁻ᶻ)` has derivative `σ'(z) = σ(z)(1-σ(z))`.
   Prove this: start from `σ(z) = (1+e⁻ᶻ)⁻¹` and apply the chain rule.

6. If the forward sigmoid output is `a = 0.7`, what is `σ'(z)`? (You don't need z — express it in terms of a.)

7. In a network: `...→ z = Wx + b → a = σ(z) → L`. Given `∂L/∂a = 0.5`, compute `∂L/∂z` using the chain rule.

8. Why does the sigmoid derivative become very small for large |z|? How does this cause the vanishing gradient problem in a 5-layer sigmoid network?

---

## Part C — ReLU Backward Pass

9. ReLU: `f(z) = max(0, z)`. Write the derivative `f'(z)`.

10. Given `z = [-1, 2, 0.5, -3, 4]` and `dL/da = [1, -1, 2, 0.5, -2]`, compute `dL/dz` element-wise using the ReLU backward pass.

11. For z=0, `f'(0)` is technically undefined. What value do implementations use? Does it matter in practice?

12. Compare: for a 5-layer network processing an input, trace the gradient magnitude through sigmoid vs ReLU activations. Assume all pre-activation values are in [−2, 2]. How much smaller is the gradient at layer 1 vs layer 5 for each activation?

---

## Part D — Full Two-Layer Network

Implement forward and backward pass for a 2-layer network from scratch:
- Layer 1: `z1 = X @ W1 + b1`, `a1 = relu(z1)`
- Layer 2: `z2 = a1 @ W2 + b2`, `a2 = sigmoid(z2)`
- Loss: binary cross-entropy `L = -(y log a2 + (1-y) log(1-a2))`

13. Implement `forward(X, W1, b1, W2, b2)` returning `(a2, cache)` where cache stores all intermediate values needed for backprop.

14. Implement `backward(y, a2, cache, W1, W2)` returning gradients `(dW1, db1, dW2, db2)`. Show the full chain of chain-rule applications.

15. Run one forward+backward pass on `X = np.random.randn(10, 3)`, `y = np.random.randint(0,2,(10,1))`. Print all gradient shapes to verify they match the parameter shapes.

---

## Part E — Gradient Checking

16. For the two-layer network above, implement `gradient_check(X, y, params, ε=1e-5)` that:
    - For each parameter in W1, W2, b1, b2:
      - Compute numerical gradient: `(L(p+ε) - L(p-ε)) / (2ε)`
      - Compare to analytical gradient
    - Report the maximum relative error: `|numerical - analytical| / (|numerical| + |analytical| + 1e-8)`

17. A correct implementation should show max relative error < 1e-5. If the error is large (>1e-2), what are the most common bugs to check?

---

## Rubric

| Part | Points |
|---|---|
| A chain rule derivation | 22 |
| B sigmoid backward | 20 |
| C ReLU backward | 18 |
| D full network | 28 |
| E gradient checking | 12 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1–3 — gradients</summary>

ŷ = Xw + b, L = (1/n)||ŷ-y||²

∂L/∂ŷ = (2/n)(ŷ - y)   shape: (n,1)

∂ŷ/∂w = X   (each element of ŷ is a linear function of w through X)

∂L/∂w = Xᵀ @ ∂L/∂ŷ = (2/n) Xᵀ(ŷ - y)   shape: (d,1) ✓

∂L/∂b = mean of (2/n)(ŷ - y) over samples = (2/n) Σ(ŷᵢ - yᵢ)   scalar ✓
</details>

<details>
<summary>Part B.6–7</summary>

a = 0.7 → σ'(z) = a(1-a) = 0.7 × 0.3 = **0.21**

∂L/∂z = (∂L/∂a) × (∂a/∂z) = 0.5 × 0.21 = **0.105**
</details>

<details>
<summary>Part D.13–14</summary>

```python
def forward(X, W1, b1, W2, b2):
    z1 = X  @ W1 + b1
    a1 = np.maximum(0, z1)           # ReLU
    z2 = a1 @ W2 + b2
    a2 = 1 / (1 + np.exp(-z2))       # sigmoid
    return a2, (X, z1, a1, z2, a2, W1, W2)

def backward(y, cache):
    X, z1, a1, z2, a2, W1, W2 = cache
    n = len(y)
    # Loss: binary cross-entropy
    da2 = -(y/a2 - (1-y)/(1-a2)) / n
    dz2 = da2 * a2 * (1-a2)          # sigmoid derivative
    dW2 = a1.T @ dz2
    db2 = dz2.sum(axis=0)
    da1 = dz2 @ W2.T
    dz1 = da1 * (z1 > 0)             # ReLU derivative
    dW1 = X.T @ dz1
    db1 = dz1.sum(axis=0)
    return dW1, db1, dW2, db2
```
</details>
