# Module 11.5 — Backpropagation: Derived and Implemented

---

## The Problem

> A neural network has millions of parameters.
> Training requires computing the gradient of the loss
> with respect to every single parameter — millions of partial derivatives.
>
> Computing each gradient separately by finite differences
> would require millions of forward passes — impossibly slow.
>
> Backpropagation computes all gradients in one backward pass
> using the chain rule of calculus.
> It is the algorithm that makes deep learning possible.
> Understanding it deeply is the difference between
> a user of ML tools and a builder of ML systems.

---

## The Story

### A Rediscovery That Changed Everything

The backpropagation algorithm (backprop) is an efficient application of the chain rule for computing gradients in computational graphs. It was independently discovered multiple times:

- **Seppo Linnainmaa** (1970, Finland): first description of reverse-mode automatic differentiation in his master's thesis
- **Paul Werbos** (1974): applied it to neural networks in his PhD thesis
- **David Rumelhart, Geoffrey Hinton, Ronald Williams** (1986): the paper "Learning Representations by Back-propagating Errors" — the paper that launched modern neural network research

The 1986 paper was not the first derivation, but it clearly articulated why backprop was significant for learning distributed representations in multi-layer networks. It showed that networks with hidden layers could learn features that were not hand-engineered.

---

## The Concept

### The Chain Rule

If y = f(x) and x = g(t), then `dy/dt = (dy/dx) × (dx/dt)`.

For a composed function `L = loss(softmax(W₂ × relu(W₁ × x + b₁) + b₂))`:

Each partial derivative propagates backward through all operations that depend on it.

### Computational Graphs

Think of the network as a graph where:
- **Nodes** are operations (+, ×, relu, sigmoid, etc.)
- **Edges** carry values (forward pass) and gradients (backward pass)

```
x → [W₁] → z₁ → [ReLU] → a₁ → [W₂] → z₂ → [Softmax] → p → [Loss] → L
```

**Forward pass**: compute values left to right, store intermediate values.
**Backward pass**: compute gradients right to left using chain rule.

### Deriving Backprop for a Simple Network

**Architecture**: input x → linear W₁ → ReLU → linear W₂ → MSE loss

**Forward:**
```python
z1 = x @ W1 + b1          # linear
a1 = relu(z1)              # activation
z2 = a1 @ W2 + b2          # output layer
L  = mse_loss(z2, y)       # loss
```

**Backward** (chain rule, right to left):
```python
# ∂L/∂z2 — gradient of MSE
dL_dz2 = 2/n * (z2 - y)            # shape: (n, out_dim)

# ∂L/∂W2 = a1ᵀ @ dL_dz2
dL_dW2 = a1.T @ dL_dz2             # shape: (hidden, out_dim)
dL_db2 = dL_dz2.mean(axis=0)

# ∂L/∂a1 = dL_dz2 @ W2ᵀ
dL_da1 = dL_dz2 @ W2.T             # shape: (n, hidden)

# ∂L/∂z1 — chain rule through ReLU: da1/dz1 = 1 if z1>0 else 0
dL_dz1 = dL_da1 * (z1 > 0)        # shape: (n, hidden)

# ∂L/∂W1 = xᵀ @ dL_dz1
dL_dW1 = x.T @ dL_dz1              # shape: (in_dim, hidden)
dL_db1 = dL_dz1.mean(axis=0)
```

**Update rules (SGD):**
```python
W2 -= lr * dL_dW2
b2 -= lr * dL_db2
W1 -= lr * dL_dW1
b1 -= lr * dL_db1
```

### The Vanishing Gradient Problem

For a deep network with sigmoid activations, the gradient of the loss with respect to early layers involves many products of `sigmoid'(z) = σ(z)(1-σ(z))` — which has maximum value 0.25.

For a 10-layer network: gradient magnitude ≈ 0.25¹⁰ ≈ 0.000001. The early layers receive almost no gradient signal — they learn extremely slowly or not at all.

**Solutions:**
- **ReLU activations**: gradient is 1 for positive inputs, 0 otherwise. No squashing for positive values → gradients can propagate further.
- **Residual connections (ResNets)**: add skip connections `output = F(x) + x`. Gradients flow directly through the `+x` path — no vanishing.
- **Batch normalisation**: normalises layer inputs, preventing extreme values that push activations into saturation.
- **Careful initialisation**: He (for ReLU) or Xavier (for sigmoid/tanh) initialisation keeps activation variances roughly constant across layers.

### Automatic Differentiation (Autograd)

Modern frameworks (PyTorch, JAX, TensorFlow) implement **automatic differentiation** — the computer derives and computes gradients automatically from the forward computation:

```python
import torch

x  = torch.tensor([[1.0, 2.0]], requires_grad=True)
W1 = torch.randn(2, 3, requires_grad=True)
b1 = torch.zeros(3, requires_grad=True)
W2 = torch.randn(3, 1, requires_grad=True)
b2 = torch.zeros(1, requires_grad=True)
y  = torch.tensor([[3.0]])

# Forward — PyTorch builds a computational graph
z1 = x @ W1 + b1
a1 = torch.relu(z1)
z2 = a1 @ W2 + b2
L  = ((z2 - y)**2).mean()

# Backward — traverse the graph, compute gradients
L.backward()

print(W1.grad)   # ∂L/∂W1 — computed automatically
print(W2.grad)   # ∂L/∂W2
```

PyTorch builds a dynamic computational graph during the forward pass and traverses it in reverse during `backward()`. This is exactly reverse-mode automatic differentiation (Linnainmaa's algorithm from 1970).

### The Complete Training Loop (NumPy from Scratch)

```python
class TwoLayerNet:
    def __init__(self, in_d, h_d, out_d):
        self.W1 = np.random.randn(in_d, h_d)  * np.sqrt(2/in_d)
        self.b1 = np.zeros(h_d)
        self.W2 = np.random.randn(h_d, out_d) * np.sqrt(2/h_d)
        self.b2 = np.zeros(out_d)

    def forward(self, X):
        self.X  = X
        self.z1 = X  @ self.W1 + self.b1
        self.a1 = np.maximum(0, self.z1)    # ReLU
        self.z2 = self.a1 @ self.W2 + self.b2
        return self.z2

    def backward(self, y_true, lr=0.01):
        n = len(y_true)
        dz2 = 2/n * (self.z2 - y_true)          # ∂L/∂z2

        dW2 = self.a1.T @ dz2                    # ∂L/∂W2
        db2 = dz2.mean(axis=0)
        da1 = dz2 @ self.W2.T
        dz1 = da1 * (self.z1 > 0)               # chain rule through ReLU

        dW1 = self.X.T @ dz1
        db1 = dz1.mean(axis=0)

        self.W2 -= lr * dW2; self.b2 -= lr * db2
        self.W1 -= lr * dW1; self.b1 -= lr * db1

        return np.mean((self.z2 - y_true)**2)    # loss
```

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Chain Rule Calculator**
- Build a computational graph node by node
- Enter function compositions (e.g., f(g(h(x))))
- Watch the chain rule applied step by step in both directions

**Tool 2 — Gradient Flow Visualiser**
- A 4-layer network with sigmoid vs ReLU activations
- Train both and watch gradient magnitudes at each layer
- Observe vanishing gradients with sigmoid, healthy flow with ReLU

**Tool 3 — Numerical vs Analytical Gradients**
- For a given network and input, compute gradients by finite difference: (f(w+ε) - f(w-ε)) / 2ε
- Compare to backprop gradients
- Verify they match (gradient checking — used to debug implementations)

---

## Going Deeper

**Second-order methods**: gradient descent uses only first derivatives. Newton's method also uses second derivatives (Hessian matrix) to take a better step direction. But the Hessian of a neural network is n×n (n = number of parameters) — storing it requires n² memory (billions of elements for a modern network). **Quasi-Newton methods** (L-BFGS, Adam) approximate the curvature from gradient history, achieving better convergence than pure SGD without the Hessian cost.

**Transformers and attention gradients**: the self-attention mechanism in transformers (Module 12.1) introduces a specific gradient structure. The query-key dot product creates a score matrix; softmax converts scores to weights; the weighted sum of values computes the output. Deriving the gradient of this operation — and understanding why it works for sequence modelling — requires applying backprop to matrix operations with batch dimensions.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Derive the gradient of MSE loss with respect to weights in a single linear layer (no activation). Implement gradient checking (compare numerical vs analytical gradients) for a 2-layer network. Trace the backward pass through a sigmoid activation: if the forward sigmoid output is 0.7, what is the gradient that flows back? And explain why the vanishing gradient problem is worse with 10 layers of sigmoid than 10 layers of ReLU.
