# Module 11.2 — Linear Algebra for Machine Learning

---

## The Problem

> A dataset has 10,000 images, each 28×28 pixels.
> A neural network layer has 512 neurons, each connected to all 784 pixels.
> Training involves computing 10,000 × 784 multiplications and additions — simultaneously.
>
> Without linear algebra, this is incomprehensible.
> With linear algebra, it is one matrix multiplication.
>
> Machine learning is, at its mathematical core, applied linear algebra.
> Understanding vectors, matrices, and the operations on them
> is the prerequisite for understanding every ML algorithm that matters.

---

## The Story

### Linear Algebra Was Always About Computation

Linear algebra — the study of linear equations, vectors, and matrices — was developed over centuries. **Gauss** solved systems of linear equations with what we now call Gaussian elimination (early 19th century). **Arthur Cayley** introduced matrix notation in 1858.

But the connection to machine learning is direct: a linear model is literally a linear function (y = Wx + b), a neural network layer is a matrix multiplication followed by a nonlinearity, and most ML optimisation involves computing gradients of scalar loss functions with respect to matrices of parameters.

**Sanjoy Mahajan's** observation: "In applied mathematics, everything is a matrix." Training a model is computing W ← W - α∇W (gradient descent in matrix form). Understanding what ∇W means requires linear algebra.

---

## The Concept

### Vectors

A **vector** is an ordered list of numbers — a point in n-dimensional space.

```python
import numpy as np

# 3D vector
v = np.array([1.0, 2.0, 3.0])

# Operations
u = np.array([4.0, 5.0, 6.0])
print(u + v)          # [5, 7, 9]  — element-wise addition
print(2 * v)          # [2, 4, 6]  — scalar multiplication
print(np.dot(u, v))   # 4+10+18 = 32 — dot product
print(np.linalg.norm(v))   # √(1+4+9) = √14 ≈ 3.74 — L2 norm
```

**Dot product**: `u·v = Σᵢ uᵢvᵢ = |u| |v| cos(θ)` — measures similarity (angle between vectors). At the heart of every linear model.

**Cosine similarity**: `cos(θ) = u·v / (|u||v|)` — 1 = identical direction, 0 = perpendicular, -1 = opposite. Used for comparing word embeddings, document similarity.

### Matrices

A **matrix** is a 2D array of numbers — a linear transformation.

```python
# 3×2 matrix (3 rows, 2 columns)
A = np.array([[1, 2],
              [3, 4],
              [5, 6]])

print(A.shape)          # (3, 2)
print(A.T)              # transpose: shape (2, 3)
print(A[1, :])          # row 1: [3, 4]
print(A[:, 0])          # column 0: [1, 3, 5]
```

**Matrix multiplication** — the fundamental operation:

```python
A = np.array([[1,2],[3,4],[5,6]])   # shape (3,2)
B = np.array([[7,8,9],[10,11,12]])  # shape (2,3)

C = A @ B    # shape (3,3) — matrix multiplication
# C[i,j] = dot product of row i of A with column j of B
```

Rule: `(m×k) @ (k×n) = (m×n)` — the inner dimensions must match.

**Why matrix multiplication matters for ML**: a neural network layer transforms an input vector x (shape: n) to output z (shape: m) via:
```
z = W @ x + b
```
Where W is a weight matrix (shape: m×n) and b is a bias vector (shape: m). One operation transforms every input dimension to every output dimension.

For a **batch** of N examples: stack them as rows in X (shape: N×n). Then:
```python
Z = X @ W.T + b    # shape: (N, m) — all N examples transformed simultaneously
```

This is why GPUs are essential for ML: matrix multiplication is massively parallelisable.

### Special Matrix Operations

**Inverse**: A⁻¹ such that A⁻¹A = I (identity). Exists only for square, non-singular matrices. Expensive to compute (O(n³)); avoid when possible.

**Eigenvectors and eigenvalues**:
```
A v = λ v
```
An eigenvector `v` is unchanged in direction by the matrix `A` — only scaled by eigenvalue `λ`.

Eigendecomposition is the basis of:
- **PCA (Principal Component Analysis)**: find the directions of maximum variance in data — the eigenvectors of the covariance matrix
- **Spectral clustering**: cluster data using eigenvectors of the graph Laplacian
- **PageRank**: rank web pages using the dominant eigenvector of the link matrix

**SVD (Singular Value Decomposition)**: any matrix A = UΣVᵀ. The generalisation of eigendecomposition to non-square matrices. Basis of: recommender systems (matrix factorisation), dimensionality reduction, pseudo-inverse.

### NumPy for ML

NumPy is the foundation of all Python ML:

```python
import numpy as np

# Create and manipulate data
X = np.random.randn(1000, 20)    # 1000 examples, 20 features
y = np.random.randint(0, 2, 1000) # binary labels

# Normalise features (zero mean, unit variance)
X_mean = X.mean(axis=0)          # mean of each feature
X_std  = X.std(axis=0)
X_norm = (X - X_mean) / X_std

# Linear model forward pass
W = np.random.randn(20, 10) * 0.01   # weight matrix
b = np.zeros(10)                       # bias
Z = X_norm @ W + b                     # (1000, 10)

# Softmax for multi-class classification
def softmax(Z):
    exp_Z = np.exp(Z - Z.max(axis=1, keepdims=True))  # stable softmax
    return exp_Z / exp_Z.sum(axis=1, keepdims=True)

probs = softmax(Z)    # (1000, 10) — probabilities for each class
```

### Gradient Computation

Backpropagation (Module 11.5) relies on matrix calculus. Key identities:

**Scalar loss L, weight matrix W, input X:**
- Forward: `Z = XW + b`, `L = loss(Z, y)`
- Backward: `∂L/∂W = Xᵀ @ ∂L/∂Z`, `∂L/∂b = sum(∂L/∂Z, axis=0)`, `∂L/∂X = ∂L/∂Z @ Wᵀ`

These matrix operations are the core of training every neural network.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Vector Operations**
- Enter two 2D or 3D vectors
- Visualise addition, subtraction, scalar multiplication
- Compute and visualise dot product (angle between vectors)

**Tool 2 — Matrix Multiplication**
- Enter two matrices
- Watch the element-by-element computation
- See shape rules validated or violated

**Tool 3 — PCA Visualiser**
- A 2D dataset
- Compute the covariance matrix and its eigenvectors
- Watch PCA rotate the coordinate system to align with maximum variance directions

---

## Going Deeper

**Tensors**: generalisation of matrices to arbitrary dimensions. A rank-0 tensor = scalar, rank-1 = vector, rank-2 = matrix, rank-3 = stack of matrices (e.g., a batch of images: N × H × W × C). PyTorch and TensorFlow are built around tensor operations on GPUs.

**Matrix decompositions in ML**: QR decomposition for solving least squares efficiently; Cholesky decomposition for multivariate Gaussian sampling; LU decomposition for solving linear systems. Each has O(n³) time but different numerical stability properties.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Implement matrix multiplication from scratch (without NumPy), compute PCA on a 3-feature dataset reducing to 2 dimensions, prove that `(AB)ᵀ = BᵀAᵀ` for arbitrary compatible matrices A and B, and explain what it means geometrically when a matrix has a zero eigenvalue.
