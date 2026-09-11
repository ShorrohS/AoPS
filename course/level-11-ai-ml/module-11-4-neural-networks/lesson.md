# Module 11.4 — Neural Networks from Scratch

---

## The Problem

> Linear regression can fit a line.
> Logistic regression can draw a straight boundary between classes.
> But most real problems are not linearly separable.
>
> An image classifier needs to recognise cats — not a feature that any linear function can capture.
> A fraud detector needs to identify complex patterns in transaction sequences.
> A language model needs to understand context and meaning.
>
> These problems require learning **hierarchical, nonlinear representations** from data.
> Neural networks are the general-purpose function approximators that do this.

---

## The Story

### From Perceptrons to Deep Learning

**Frank Rosenblatt's** perceptron (1958) was the first algorithm that learned from data. It could classify linearly separable data. Marvin Minsky and Seymour Papert's book "Perceptrons" (1969) proved that a single-layer perceptron cannot compute XOR — an apparently simple function. This killed neural network funding for a decade.

The **multi-layer perceptron (MLP)** with backpropagation, popularised by **David Rumelhart, Geoffrey Hinton, and Ronald Williams** (1986), solved the XOR problem and sparked renewed interest. But training deep networks (many layers) remained elusive due to the **vanishing gradient problem**.

The deep learning revolution began around 2012 when **Alex Krizhevsky, Ilya Sutskever, and Geoffrey Hinton** (AlexNet) won the ImageNet competition with error rates dramatically lower than all competitors — using a convolutional neural network with ReLU activations and GPU training. The field transformed overnight.

---

## The Concept

### A Single Neuron

A neuron computes: `output = f(w·x + b)` where:
- `x` = input vector
- `w` = weight vector (learned)
- `b` = bias (learned)
- `f` = activation function (introduces nonlinearity)

Without `f` (or with a linear `f`), a multi-layer network is equivalent to a single layer. Nonlinear activations are what make deep networks powerful.

```python
import numpy as np

def sigmoid(z): return 1 / (1 + np.exp(-z))
def relu(z):    return np.maximum(0, z)
def tanh(z):    return np.tanh(z)
```

**Sigmoid**: output ∈ (0,1), saturates for large |z| (gradient vanishes). Used in output layer for binary classification.

**ReLU (Rectified Linear Unit)**: `max(0, z)`. Does not saturate for positive z. Sparse activation (many zeros). The dominant activation for hidden layers since ~2012.

**Leaky ReLU**: `z if z>0 else 0.01*z` — prevents "dead neurons" (neurons that always output 0).

**Softmax**: converts a vector of scores to probabilities that sum to 1. Used in output layer for multi-class classification.

### Multi-Layer Perceptron (MLP)

A fully-connected network with L layers:

```python
class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases  = []
        for i in range(len(layer_sizes) - 1):
            n_in, n_out = layer_sizes[i], layer_sizes[i+1]
            # He initialisation for ReLU networks
            W = np.random.randn(n_in, n_out) * np.sqrt(2.0 / n_in)
            b = np.zeros(n_out)
            self.weights.append(W)
            self.biases.append(b)

    def forward(self, X):
        self.activations = [X]
        A = X
        for i, (W, b) in enumerate(zip(self.weights, self.biases)):
            Z = A @ W + b
            # ReLU for hidden layers, identity for last (or softmax)
            A = relu(Z) if i < len(self.weights) - 1 else Z
            self.activations.append(A)
        return A
```

**Dimensions for a 3-layer network on MNIST (784 inputs, 256, 128, 10):**
- Input: (batch_size, 784)
- W₁: (784, 256), b₁: (256,) → Layer 1 output: (batch_size, 256)
- W₂: (256, 128), b₂: (128,) → Layer 2 output: (batch_size, 128)
- W₃: (128, 10),  b₃: (10,)  → Output: (batch_size, 10)
- Total parameters: 784×256 + 256 + 256×128 + 128 + 128×10 + 10 = 234,378

### Loss Functions

**For regression**: Mean Squared Error (MSE):
```python
def mse_loss(y_pred, y_true):
    return np.mean((y_pred - y_true) ** 2)
```

**For binary classification**: Binary Cross-Entropy:
```python
def bce_loss(y_pred, y_true, eps=1e-15):
    y_pred = np.clip(y_pred, eps, 1-eps)
    return -np.mean(y_true * np.log(y_pred) + (1-y_true) * np.log(1-y_pred))
```

**For multi-class classification**: Categorical Cross-Entropy:
```python
def softmax(Z):
    exp_Z = np.exp(Z - Z.max(axis=1, keepdims=True))
    return exp_Z / exp_Z.sum(axis=1, keepdims=True)

def ce_loss(logits, y_true):
    probs = softmax(logits)
    n = len(y_true)
    return -np.mean(np.log(probs[np.arange(n), y_true] + 1e-15))
```

### Backpropagation (Forward Look)

Backpropagation (detailed in Module 11.5) computes gradients of the loss with respect to every weight via the chain rule:

```python
def backward(self, y_true, loss_grad):
    # Reverse pass through layers
    dA = loss_grad
    grads_W, grads_b = [], []
    for i in reversed(range(len(self.weights))):
        A_in = self.activations[i]
        dZ = dA * relu_derivative(self.activations[i+1]) if i < len(self.weights)-1 else dA
        dW = A_in.T @ dZ / len(y_true)
        db = dZ.mean(axis=0)
        dA = dZ @ self.weights[i].T
        grads_W.insert(0, dW)
        grads_b.insert(0, db)
    return grads_W, grads_b
```

### Training Loop

```python
def train(net, X_train, y_train, epochs=100, lr=0.01, batch_size=32):
    n = len(X_train)
    for epoch in range(epochs):
        # Shuffle
        idx = np.random.permutation(n)
        X_train, y_train = X_train[idx], y_train[idx]

        total_loss = 0
        for i in range(0, n, batch_size):
            Xb = X_train[i:i+batch_size]
            yb = y_train[i:i+batch_size]

            # Forward pass
            logits = net.forward(Xb)
            loss   = ce_loss(logits, yb)
            total_loss += loss

            # Backward pass (gradient computation)
            probs = softmax(logits)
            probs[np.arange(len(yb)), yb] -= 1   # dL/dZ for softmax + CE
            grads_W, grads_b = net.backward(yb, probs / len(yb))

            # Update weights (SGD)
            for j in range(len(net.weights)):
                net.weights[j] -= lr * grads_W[j]
                net.biases[j]  -= lr * grads_b[j]

        print(f"Epoch {epoch+1}/{epochs}: Loss = {total_loss/(n/batch_size):.4f}")
```

### Using PyTorch

In practice, automatic differentiation makes this much simpler:

```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 128),
    nn.ReLU(),
    nn.Linear(128, 10)
)

optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

for epoch in range(10):
    for Xb, yb in dataloader:
        optimizer.zero_grad()
        logits = model(Xb)
        loss   = criterion(logits, yb)
        loss.backward()      # automatic differentiation
        optimizer.step()     # update weights
```

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Single Neuron Visualiser**
- Set weights and bias for a single neuron
- Adjust activation function: sigmoid, ReLU, tanh
- See how the output changes with different inputs

**Tool 2 — MLP Training on XOR**
- A 2-2-1 network trained to compute XOR
- Watch weights update in real time as the network learns
- See the decision boundary evolve from linear to curved

**Tool 3 — Loss Landscape**
- A 2D slice through the weight space
- Visualise the loss surface
- Watch gradient descent follow the slope downward

---

## Going Deeper

**Convolutional Neural Networks (CNNs)**: instead of fully connecting every pixel to every neuron (which would require enormous parameter counts for images), CNNs use small, sliding **convolutional filters** that learn local patterns (edges, textures, shapes). Each filter produces one feature map. Stacking convolutions builds hierarchical features: edges → curves → parts → objects. AlexNet (2012), VGG, ResNet (2015) all use this architecture.

**Batch normalisation**: normalise the inputs to each layer within a mini-batch. Dramatically stabilises and speeds up training by reducing internal covariate shift. Now standard in almost all deep networks. Invented by Sergey Ioffe and Christian Szegedy at Google in 2015.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Implement a 2-layer neural network from scratch in NumPy that learns XOR (no autograd), compute the number of parameters for a given network architecture, trace the forward pass for one example through a 3-layer network showing all matrix dimensions, and explain why ReLU networks can approximate any continuous function (universal approximation theorem intuition).
