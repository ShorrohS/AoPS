# Challenge 11.3 — Regression and Classification

**Type:** Implementation + analysis + calculation  
**Estimated time:** 50–60 minutes  
**Tools needed:** Python + NumPy

---

## Part A — Linear Regression from Scratch

Dataset: house prices. `X = [500, 750, 1000, 1250, 1500]` (sq ft), `y = [150, 200, 250, 325, 400]` (thousands).

1. Implement `linear_regression_gd(X, y, lr=0.0001, epochs=1000)` using gradient descent. Normalise X first (zero mean, unit variance). Return `(w, b)`.

2. What is the learned equation `y = w*x_norm + b`? Convert back to original scale.

3. Predict the price for a 1100 sq ft house. How close is it to the linear interpolation?

4. Compute the **R² score** for your model on the training data. What does R²=0.95 mean in plain language?

---

## Part B — Logistic Regression

Binary classification: predict whether a student passes (1) or fails (0) based on hours studied.

```python
X = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
y = np.array([0,   0,   0,   0,   1,   0,   1,   1,   1,   1  ])
```

5. Implement logistic regression using gradient descent. Use the binary cross-entropy loss and the sigmoid activation.

6. After training, plot (conceptually — describe) the sigmoid curve and the decision boundary at threshold=0.5. At what number of study hours does the model predict a 50% probability of passing?

7. Compute **precision**, **recall**, and **F1** on the training data with threshold=0.5. Show the confusion matrix.

8. Lower the threshold to 0.3. How does this change precision and recall? When would you want lower threshold (higher recall, lower precision)?

---

## Part C — Decision Tree by Hand

Build a decision tree for this dataset:

| Age | Income | Bought |
|-----|--------|--------|
| Young | High | Yes |
| Young | Low | No |
| Middle | High | Yes |
| Middle | Low | Yes |
| Senior | High | No |
| Senior | Low | No |

9. Calculate **Gini impurity** for the entire dataset: `Gini(S) = 1 - Σ pᵢ²`.

10. Calculate the Gini impurity for splitting on **Age** (3 values) vs splitting on **Income** (2 values). Show all calculations.

11. Which split is better? Draw the first level of the decision tree after the best split.

12. After the first split, one branch might be pure (all same class). Which branch? Does it need further splitting?

---

## Part D — Evaluation Metrics

13. A cancer screening model on 10,000 patients: 100 have cancer, 9,900 don't. The model predicts "no cancer" for everyone. Calculate accuracy, precision, recall, and F1. Why is accuracy misleading here?

14. A model has: TP=80, FP=20, FN=20, TN=9880 (on the same 10,000 patients).
    Calculate precision, recall, F1. Which metric matters most for cancer screening? Why?

15. Explain the **ROC curve**: what does the area under the curve (AUC=0.5 vs AUC=1.0) represent? For the cancer model in question 14, would you expect a high or low AUC?

---

## Part E — Bias-Variance Tradeoff

16. A polynomial regression model of degree 10 fits the training data perfectly (R²=1.0) but performs poorly on test data (R²=0.3). What is this called? What is the fix?

17. A linear model fits training data with R²=0.6 and test data with R²=0.58. What is this called? What are two fixes?

18. Explain regularisation (Ridge/L2) as a mechanism that reduces variance at the cost of slight bias increase. If λ=0, what happens? If λ→∞?

---

## Rubric

| Part | Points |
|---|---|
| A linear regression | 22 |
| B logistic regression | 24 |
| C decision tree | 22 |
| D evaluation metrics | 18 |
| E bias-variance | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.4 — R² definition</summary>

R² = 1 - SS_res / SS_tot, where SS_res = Σ(y - ŷ)² (residuals) and SS_tot = Σ(y - ȳ)² (total variance). R²=0.95 means the model explains 95% of the variance in y. The remaining 5% is unexplained by the linear fit.
</details>

<details>
<summary>Part B.7 — confusion matrix</summary>

With threshold 0.5, the boundary is around hours_studied ≈ 2.5. Predicting:
- 0.5,1.0,1.5,2.0 → 0 (correct: all are 0)
- 2.5 → 0.5 ≈ threshold boundary (depends on trained w,b)
- 3.0,3.5,4.0,4.5,5.0 → 1 (one false negative at 3.0 which is labeled 0)

Approximate CM: TP≈4, FP≈0, FN≈1, TN≈5. Precision=4/4=1.0, Recall=4/5=0.8, F1=2×(1×0.8)/(1.8)≈0.89.
</details>

<details>
<summary>Part C.9–10 — Gini calculations</summary>

Dataset: 4 Yes, 2 No. Gini(root) = 1 - (4/6)² - (2/6)² = 1 - 0.444 - 0.111 = **0.444**.

Split on Income (2 branches):
- High (3 rows: YYN): Gini = 1-(2/3)²-(1/3)² = 0.444
- Low (3 rows: NYY): Gini = 1-(2/3)²-(1/3)² = 0.444
- Weighted: 0.5×0.444 + 0.5×0.444 = 0.444

Split on Age (3 branches):
- Young (YN): Gini = 1-0.5²-0.5² = 0.5
- Middle (YY): Gini = 0 (pure!)
- Senior (NN): Gini = 0 (pure!)
- Weighted: (2/6)×0.5 + (2/6)×0 + (2/6)×0 = 0.167

Age split Gini (0.167) < Income split Gini (0.444). **Age is the better first split.**
</details>
