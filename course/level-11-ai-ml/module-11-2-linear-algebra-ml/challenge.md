# Challenge 11.2 — Linear Algebra for Machine Learning

**Type:** Calculation + implementation + proof  
**Estimated time:** 45–55 minutes  
**Tools needed:** NumPy + pen and paper

---

## Part A — Matrix Multiplication

1. Multiply these matrices by hand:
   ```
   A = [[1, 2, 3],    B = [[7,  8],
        [4, 5, 6]]         [9, 10],
                           [11, 12]]
   ```
   Show the calculation for C[0][0] and C[1][1] explicitly.

2. A neural network layer: input X has shape (32, 784) — 32 examples, 784 features each. The weight matrix W has shape (784, 256). What is the shape of the output XW? What does each row of XW represent?

3. Implement matrix multiplication from scratch in pure Python (no NumPy). Then verify your result matches `np.dot(A, B)`.

---

## Part B — Vector Operations

4. Compute the **cosine similarity** between `u = [1, 2, 3]` and `v = [4, 5, 6]`. Show all steps: dot product, norms, final similarity.

5. Normalise both vectors to unit length. What is the dot product of the normalised vectors? How does it relate to your cosine similarity?

6. Two word embeddings: `king = [0.8, 0.3, -0.1]`, `queen = [0.7, 0.4, -0.2]`. Compute their cosine similarity. Are they semantically similar according to this metric?

---

## Part C — Matrix Properties

7. Prove algebraically that `(AB)ᵀ = BᵀAᵀ` for 2×2 matrices:
   ```
   A = [[a, b],   B = [[e, f],
        [c, d]]        [g, h]]
   ```
   Compute both sides and show they're equal.

8. What does it mean geometrically for a 2×2 matrix to be **singular** (non-invertible)? Compute the determinant of:
   ```
   M1 = [[2, 4],    M2 = [[2, 3],
          [1, 2]]          [4, 6]]
   ```
   Which is singular? What does this mean about the linear system Mx = b?

---

## Part D — PCA by Hand

Given the 4-point dataset: `[(1,2), (2,4), (3,3), (4,5)]`

9. Compute the **mean** of each dimension. Center the data.

10. Compute the **2×2 covariance matrix** of the centered data.

11. The eigenvectors of the covariance matrix are the principal components. Without computing eigenvectors (hard to do by hand), describe qualitatively: in which direction does the data have the most variance? That direction is PC1.

12. Implement PCA using NumPy: `pca(X, n_components=2)` that:
    - Centers X
    - Computes covariance matrix
    - Computes eigenvalues and eigenvectors (`np.linalg.eig`)
    - Returns the top n_components eigenvectors and the projected data

---

## Part E — Gradient in Matrix Form

For a single-layer linear model `ŷ = XW + b` with MSE loss `L = (1/n)||ŷ - y||²`:

13. Write out `∂L/∂W` in matrix form. The answer is `(2/n) Xᵀ(ŷ - y)`. Verify the shapes match: X is (n,d), W is (d,m), ŷ and y are (n,m). What shape is `∂L/∂W`?

14. Implement one gradient descent step on random data:
    ```python
    n, d, m = 100, 10, 1
    X = np.random.randn(n, d)
    y = np.random.randn(n, m)
    W = np.zeros((d, m))
    b = np.zeros(m)
    lr = 0.01
    # compute gradient and update W and b
    ```

---

## Rubric

| Part | Points |
|---|---|
| A matrix multiplication | 22 |
| B vector operations | 18 |
| C matrix properties | 20 |
| D PCA | 24 |
| E gradient | 16 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1 — matrix multiply</summary>

A is (2,3), B is (3,2). C = AB has shape (2,2).

C[0][0] = 1×7 + 2×9 + 3×11 = 7 + 18 + 33 = 58
C[0][1] = 1×8 + 2×10 + 3×12 = 8 + 20 + 36 = 64
C[1][0] = 4×7 + 5×9 + 6×11 = 28 + 45 + 66 = 139
C[1][1] = 4×8 + 5×10 + 6×12 = 32 + 50 + 72 = **154**
</details>

<details>
<summary>Part B.4 — cosine similarity</summary>

u·v = 1×4 + 2×5 + 3×6 = 4 + 10 + 18 = 32
|u| = √(1+4+9) = √14 ≈ 3.742
|v| = √(16+25+36) = √77 ≈ 8.775
cosine = 32 / (3.742 × 8.775) = 32 / 32.83 ≈ **0.975** (very similar direction)
</details>

<details>
<summary>Part E.14 — gradient step</summary>

```python
y_hat = X @ W + b                    # (n,m)
error = y_hat - y                    # (n,m)
dW = (2/n) * X.T @ error             # (d,m) ✓
db = (2/n) * error.mean(axis=0)      # (m,)
W  -= lr * dW
b  -= lr * db
```
</details>
