# Challenge 11.4 — Neural Networks from Scratch

**Type:** Implementation + trace + analysis  
**Estimated time:** 55–65 minutes  
**Tools needed:** Python + NumPy

---

## Part A — XOR from Scratch

XOR is not linearly separable: no single line can separate (0,0)→0, (1,1)→0 from (0,1)→1, (1,0)→1.

1. Prove XOR is not linearly separable: for any line `w₁x₁ + w₂x₂ + b = 0`, show that no choice of w₁, w₂, b correctly classifies all four points simultaneously.

2. A 2-2-1 network (2 inputs, 2 hidden neurons with sigmoid, 1 output with sigmoid) CAN learn XOR. Implement this network in NumPy with:
   - Manual weight initialisation
   - Forward pass
   - MSE loss
   - Backpropagation
   - 10,000 training iterations

3. After training, verify: `predict(0,0)≈0`, `predict(0,1)≈1`, `predict(1,0)≈1`, `predict(1,1)≈0`. Plot (describe) the loss curve over training iterations.

---

## Part B — Network Architecture

4. A network processes 28×28 grayscale images (MNIST) into 10 class probabilities. The architecture is: `784 → 256 → 128 → 10`. Calculate:
   - Total parameters (weights + biases) for each layer
   - Total parameters for the whole network

5. Why does adding a 4th hidden layer of 64 neurons (`784 → 256 → 128 → 64 → 10`) sometimes **not** improve accuracy? Name two reasons.

6. **Universal approximation theorem**: a single hidden layer with enough neurons can approximate any continuous function. Does this mean one hidden layer is always best? What are the trade-offs of depth vs width?

---

## Part C — Activation Functions

7. For `z = [-3, -1, 0, 1, 3]`, compute the output of:
   - sigmoid(z)
   - tanh(z)
   - relu(z)
   - leaky_relu(z, alpha=0.01)

8. **Dead ReLU problem**: a neuron with negative bias might have z < 0 for all training examples. Its ReLU output is always 0, gradient is always 0, and it never learns. How do Leaky ReLU and PReLU address this?

9. Why is tanh generally preferred over sigmoid for hidden layers? (Hint: consider the output range and its effect on gradient flow.)

---

## Part D — Weight Initialisation

10. A 3-layer network with 1000 neurons per layer. All weights initialised to `0`. What is the output of every hidden neuron? What is the gradient? Why does this fail?

11. All weights initialised to `0.01` (small random). Explain the problem for a 10-layer network: what happens to the activation magnitudes and gradients as you go deeper?

12. **He initialisation** for ReLU: `W ~ N(0, 2/n_in)`. For a layer with 256 inputs, what is the standard deviation? Why is the factor 2 (not 1) used for ReLU?

13. Implement and compare three initialisations for a 5-layer ReLU network: zeros, uniform(0,1), He. Record the mean activation magnitude at each layer for a forward pass on random input.

---

## Part E — PyTorch Comparison

14. Rewrite your XOR network from Part A using PyTorch (`nn.Sequential`, `nn.Linear`, `nn.Sigmoid`, `optim.Adam`, `nn.MSELoss`). Compare:
    - Lines of code: NumPy vs PyTorch
    - Training speed: NumPy vs PyTorch on 10,000 epochs
    - Code readability

15. What does `optimizer.zero_grad()` do and why is it needed before every backward pass?

---

## Rubric

| Part | Points |
|---|---|
| A XOR from scratch | 28 |
| B network architecture | 18 |
| C activation functions | 20 |
| D weight initialisation | 22 |
| E PyTorch comparison | 12 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1 — XOR not linearly separable</summary>

For a line `w₁x₁ + w₂x₂ + b = 0`:
- (0,0)→0: b < 0
- (1,1)→0: w₁+w₂+b < 0 → w₁+w₂ < -b
- (0,1)→1: w₂+b > 0 → w₂ > -b
- (1,0)→1: w₁+b > 0 → w₁ > -b

From constraints 3 and 4: w₁+w₂ > -2b.
But constraint 2 says w₁+w₂ < -b.
So: -2b < -b → -b > 0 → b < 0.
And b < 0 from constraint 1. OK so far.
But w₁+w₂ > -2b and w₁+w₂ < -b: need -2b < -b → b > 0. **Contradiction** with b < 0.
No such w₁, w₂, b exists. ∎
</details>

<details>
<summary>Part B.4 — parameter count</summary>

Layer 1 (784→256): 784×256 + 256 = 200,960 + 256 = 201,216 params
Layer 2 (256→128): 256×128 + 128 = 32,768 + 128 = 32,896 params
Layer 3 (128→10): 128×10 + 10 = 1,280 + 10 = 1,290 params
Total: **235,402 parameters**
</details>

<details>
<summary>Part D.10 — zero initialisation failure</summary>

All weights = 0: every hidden neuron computes `z = 0 × x₁ + 0 × x₂ + ... + b`. If b=0 too, every neuron outputs sigmoid(0)=0.5. Every neuron is identical. The gradient for all neurons is the same. All neurons update identically every step — they stay identical forever. The network has effectively one neuron at each layer. This is the "symmetry breaking" problem: weights must be different to learn different features.
</details>
