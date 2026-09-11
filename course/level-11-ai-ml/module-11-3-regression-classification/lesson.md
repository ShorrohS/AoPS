# Module 11.3 — Regression and Classification

---

## The Problem

> You have data: 1,000 house prices with their square footage, number of bedrooms, and location.
> You want to predict the price of a new house.
> This is **regression** — predicting a continuous value.
>
> You have 10,000 emails labelled "spam" or "not spam."
> You want to automatically label new emails.
> This is **classification** — predicting a discrete category.
>
> These are the two most fundamental machine learning tasks.
> Every supervised learning algorithm is solving one of them.

---

## The Story

### Galton, Pearson, and the Origin of Regression

Francis Galton coined the term "regression" in 1886 studying the heights of children relative to their parents — tall parents tend to have children shorter than themselves, short parents tend to have children taller than themselves. Galton called this "regression to the mean." Karl Pearson extended this work, developing the correlation coefficient and linear regression as statistical tools.

The perceptron — the first classification algorithm learned from data — was invented by Frank Rosenblatt in 1958, inspired by McCulloch and Pitts' model of a neuron. The perceptron is still the conceptual foundation of neural networks today.

Logistic regression (despite the name, a classification algorithm) was developed in the 1940s–50s for medical statistics. It remains one of the most widely used algorithms in industry — interpretable, fast, and effective for binary classification with clean features.

---

## The Concept

### Linear Regression

**Problem**: given training data `{(x₁,y₁), ..., (xₙ,yₙ)}`, find parameters `w` (weights) and `b` (bias) such that `ŷ = w·x + b` minimises prediction error.

**Model**: `ŷ = w₁x₁ + w₂x₂ + ... + wₙxₙ + b = Xw + b`

**Loss function** (Mean Squared Error):
```
MSE = (1/n) Σᵢ (yᵢ - ŷᵢ)²
```

**Gradient descent**: iteratively move parameters in the direction that reduces loss.

```python
import numpy as np

def linear_regression_gd(X, y, lr=0.01, epochs=1000):
    n, d = X.shape
    w = np.zeros(d)
    b = 0.0

    for epoch in range(epochs):
        y_pred = X @ w + b                 # forward pass
        error  = y_pred - y

        # Gradients
        dw = (2/n) * X.T @ error
        db = (2/n) * np.sum(error)

        # Update parameters
        w -= lr * dw
        b -= lr * db

        if epoch % 100 == 0:
            loss = np.mean(error**2)
            print(f"Epoch {epoch}: MSE = {loss:.4f}")

    return w, b
```

**Closed-form solution** (Normal Equation):
```python
# ŵ = (XᵀX)⁻¹ Xᵀy  — works for small datasets
w = np.linalg.lstsq(X, y, rcond=None)[0]
```

**Regularisation** prevents overfitting:
- **Ridge (L2)**: loss += λ Σ wᵢ² — penalises large weights, keeps all features
- **Lasso (L1)**: loss += λ Σ |wᵢ| — drives some weights to exactly zero (feature selection)

### Classification: Logistic Regression

For binary classification (y ∈ {0,1}), we need to predict a probability. The **sigmoid function** squashes any value to [0, 1]:

```
σ(z) = 1 / (1 + e^(-z))
```

**Model**: `P(y=1|x) = σ(w·x + b)`

**Decision**: if `P(y=1|x) > 0.5` → predict class 1; else predict class 0.

**Loss function** (Binary Cross-Entropy):
```
BCE = -(1/n) Σᵢ [yᵢ log(ŷᵢ) + (1-yᵢ) log(1-ŷᵢ)]
```

```python
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def logistic_regression(X, y, lr=0.01, epochs=1000):
    n, d = X.shape
    w = np.zeros(d)
    b = 0.0

    for _ in range(epochs):
        z      = X @ w + b
        y_pred = sigmoid(z)
        error  = y_pred - y

        dw = (1/n) * X.T @ error
        db = (1/n) * np.sum(error)

        w -= lr * dw
        b -= lr * db

    return w, b

def predict(X, w, b, threshold=0.5):
    return (sigmoid(X @ w + b) >= threshold).astype(int)
```

### Decision Trees

A decision tree makes predictions by asking a sequence of yes/no questions:

```
        Is age > 30?
        /          \
      Yes           No
       |             |
Is income > 50k?   Predict: No Purchase
  /         \
Yes          No
 |            |
Predict:   Predict:
Purchase   No Purchase
```

Trees are built by choosing the feature and threshold that best separates the classes at each node. **Gini impurity** or **information gain (entropy)** measure "best":

```
Gini(S) = 1 - Σₖ pₖ²
Information Gain = H(parent) - Σ (|child|/|parent|) × H(child)
```

**Decision trees in Python:**
```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
model = DecisionTreeClassifier(max_depth=3)
model.fit(X, y)
print(model.predict([[5.1, 3.5, 1.4, 0.2]]))   # [0] — Iris setosa
```

**Pros**: interpretable (you can explain each decision), handles mixed feature types, no scaling needed.
**Cons**: prone to overfitting (especially deep trees), unstable (small data changes → very different tree).

**Random Forests**: build many decision trees, each on a random subset of data and features; average their predictions. Dramatically reduces overfitting. One of the most effective and widely used ML algorithms.

### Evaluation Metrics

**For regression:**
- MSE (Mean Squared Error) — penalises large errors heavily
- RMSE (Root MSE) — same units as y
- MAE (Mean Absolute Error) — more robust to outliers
- R² (coefficient of determination) — 1.0 = perfect, 0 = predicts mean, < 0 = worse than mean

**For classification:**
```
              Predicted
              Pos   Neg
Actual  Pos [ TP  | FN ]
        Neg [ FP  | TN ]

Accuracy  = (TP+TN) / (TP+TN+FP+FN)
Precision = TP / (TP+FP)    — of predicted positives, how many are correct?
Recall    = TP / (TP+FN)    — of actual positives, how many did we find?
F1        = 2 × (P × R) / (P + R)
```

When classes are imbalanced (99% negative), accuracy is misleading — a model predicting "always negative" gets 99% accuracy but is useless. Precision, recall, and F1 are more informative.

**ROC curve and AUC**: plot True Positive Rate vs False Positive Rate at all decision thresholds. AUC (Area Under the Curve) = 1.0 is perfect; 0.5 is random. Used to compare classifiers independent of threshold choice.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Linear Regression Fitter**
- Scatter plot of house prices vs size
- Watch gradient descent update the regression line
- See the loss curve decrease over epochs
- Adjust learning rate — observe convergence speed

**Tool 2 — Logistic Regression Decision Boundary**
- 2D classification data (two features)
- Watch the decision boundary line move as training progresses
- See misclassified points
- Change threshold — watch precision/recall tradeoff

**Tool 3 — Decision Tree Builder**
- A dataset with 2 features, 2 classes
- Build a tree step by step: pick the best split at each node
- See Gini impurity calculated for each candidate split

---

## Going Deeper

**Gradient descent variants**: batch gradient descent uses all n examples per step. **Stochastic gradient descent (SGD)** uses 1 example — noisy but fast. **Mini-batch gradient descent** (most common in practice) uses k examples (typically 32–256) — reduces noise while maintaining speed. Neural networks are almost always trained with mini-batch SGD with momentum and adaptive learning rates (Adam, RMSprop).

**Bias-variance tradeoff**: model error = bias² + variance + irreducible noise. High bias = underfitting (model too simple, wrong structure). High variance = overfitting (model too complex, memorises training data). The tradeoff: more complex models have lower bias but higher variance. Cross-validation estimates the variance. Regularisation reduces variance at the cost of slightly higher bias.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Implement linear regression from scratch with gradient descent for a given dataset, calculate precision, recall, and F1 score for a given confusion matrix, build a decision tree by hand for a small dataset (4 examples, 2 features, 2 classes), and explain what happens to a logistic regression model when features are not normalised.
