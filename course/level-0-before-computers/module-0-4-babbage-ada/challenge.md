# Challenge 0.4 — Program the Analytical Engine

**Type:** Simulation use + algorithm tracing + written analysis  
**Estimated time:** 35–45 minutes  
**Tools needed:** `simulation.html` open in your browser + pen and paper

---

## Part A — Difference Engine: Tabulate a Polynomial

Using the **Difference Engine** tab in the simulation, tabulate the polynomial:

**`f(n) = n² + 3n + 2`** for n = 0 through 9

### Step 1 — Calculate by hand first

Fill in this table manually before using the simulator:

| n | f(n) = n²+3n+2 | 1st diff | 2nd diff |
|---|----------------|----------|----------|
| 0 | ? | | |
| 1 | ? | ? | |
| 2 | ? | ? | ? |
| 3 | ? | ? | ? |
| 4 | ? | ? | ? |
| 5 | ? | ? | ? |
| 6 | ? | ? | ? |
| 7 | ? | ? | ? |
| 8 | ? | ? | ? |
| 9 | ? | ? | ? |

**What is the constant value of the 2nd difference?** ___

### Step 2 — Verify with the simulator

Enter your polynomial coefficients into the Difference Engine tab and step through. Do your hand-calculated values match?

### Step 3 — Key question

**Why does the 2nd difference become constant for a degree-2 polynomial?**  
Answer in 2–3 sentences using the concept of "taking differences reduces the degree by one."

---

## Part B — Analytical Engine: Trace an Algorithm

The Analytical Engine emulator uses operation cards. Here is a simple program:

```
LOAD  V0  5       ; Store 5 in variable V0
LOAD  V1  3       ; Store 3 in variable V1
ADD   V2  V0  V1  ; V2 = V0 + V1
MUL   V3  V2  V2  ; V3 = V2 * V2
SUB   V4  V3  V1  ; V4 = V3 - V1
```

### Task 1 — Manual trace

Trace this program through the Store by hand. Fill in the Store state after each operation:

| Step | Operation | V0 | V1 | V2 | V3 | V4 |
|------|-----------|----|----|----|----|-----|
| Start | — | — | — | — | — | — |
| 1 | LOAD V0 5 | ? | — | — | — | — |
| 2 | LOAD V1 3 | ? | ? | — | — | — |
| 3 | ADD V2 V0 V1 | ? | ? | ? | — | — |
| 4 | MUL V3 V2 V2 | ? | ? | ? | ? | — |
| 5 | SUB V4 V3 V1 | ? | ? | ? | ? | ? |

**What is the final value in V4?** ___

**In plain language, what does this program compute?** (Describe mathematically what V4 represents in terms of the original inputs 5 and 3.)

### Task 2 — Verify in the simulator

Enter this program into the Analytical Engine emulator tab and run it. Does your trace match?

---

## Part C — Write Your Own Program

Write an operation card sequence (using LOAD, ADD, SUB, MUL, DIV) for the Analytical Engine emulator that computes:

**The area and perimeter of a rectangle with width = 7 and height = 4**

Requirements:
- Store width in V0, height in V1
- Compute area (width × height) and store in V2
- Compute perimeter (2 × (width + height)) and store in V3
- You may use V4–V9 as scratch variables

Write out your program as operation cards:
```
LOAD  V0  7      ; width
LOAD  V1  4      ; height
[your cards here]
```

Then run it in the simulator and confirm V2 = 28 and V3 = 22.

---

## Part D — Ada's Insight

Answer these questions in writing (2–4 sentences each):

1. **The key distinction**: What is the fundamental difference between the Difference Engine and the Analytical Engine? Use the word "reprogrammable" in your answer.

2. **Conditional branching**: Ada described the Analytical Engine's conditional lever as essential. In your own words, why does the *ability to branch* (make a decision based on a result) distinguish a computer from a calculator?

3. **Ada's prophecy**: Ada wrote that the Engine could work on "other things besides number" — that it could compose music, for example. In 2024, AI generates music, images, and text. Was Ada right? Explain the connection between her insight and modern AI.

4. **The tragedy**: Both the Difference Engine and Analytical Engine were never completed in Babbage's lifetime. Name one practical reason the Difference Engine failed, and one reason that failure was NOT Babbage's fault.

---

## Rubric

| Part | Points | What we're looking for |
|------|--------|------------------------|
| A1 — Hand-calculated table | 20 | All values correct; 2nd diff is constant 2 |
| A3 — Why constant | 10 | Correct reasoning about degree reduction |
| B1 — Manual trace | 20 | Correct store state at each step |
| B — Plain language description | 5 | Identifies the formula (a+b)² - b |
| C — Rectangle program | 20 | Correct program; V2=28 and V3=22 confirmed |
| D1–D4 — Written answers | 25 | Precise, uses correct terms |

**Total: 100 points**

---

## Hints

<details>
<summary>Hint — Part A first differences</summary>
1st diff = f(n+1) - f(n). For n=0: f(1)-f(0) = 6 - 2 = 4.
</details>

<details>
<summary>Hint — Part B final value</summary>
Work through: V0=5, V1=3, V2=8, V3=64, V4=61.
</details>

<details>
<summary>Hint — Part C perimeter</summary>
2*(W+H) = 2*V2_temp. You need to add W+H first, then multiply by 2.
LOAD V4 2 will give you a constant 2 to multiply by.
</details>

<details>
<summary>Hint — Part A why constant</summary>
A degree-2 polynomial has a degree-2 "acceleration." Taking one difference gives degree 1. Taking a second difference gives degree 0 — a constant.
</details>

---

## Solutions

<details>
<summary>Part A — Full Table</summary>

f(n) = n² + 3n + 2

| n | f(n) | 1st diff | 2nd diff |
|---|------|----------|----------|
| 0 | 2    |          |          |
| 1 | 6    | 4        |          |
| 2 | 12   | 6        | 2        |
| 3 | 20   | 8        | 2        |
| 4 | 30   | 10       | 2        |
| 5 | 42   | 12       | 2        |
| 6 | 56   | 14       | 2        |
| 7 | 72   | 16       | 2        |
| 8 | 90   | 18       | 2        |
| 9 | 110  | 20       | 2        |

Constant 2nd difference = **2** (= 2 × leading coefficient of n²)

**Why constant**: Each differencing operation reduces the polynomial degree by 1. A degree-2 polynomial → degree-1 first differences → degree-0 (constant) second differences.
</details>

<details>
<summary>Part B — Trace Solution</summary>

| Step | V0 | V1 | V2 | V3 | V4 |
|------|----|----|----|----|-----|
| Start | — | — | — | — | — |
| 1 | 5 | — | — | — | — |
| 2 | 5 | 3 | — | — | — |
| 3 | 5 | 3 | 8 | — | — |
| 4 | 5 | 3 | 8 | 64 | — |
| 5 | 5 | 3 | 8 | 64 | 61 |

V4 = 61. The program computes **(V0 + V1)² - V1** = (5+3)² - 3 = 64 - 3 = 61.
</details>

<details>
<summary>Part C — Rectangle Solution</summary>

```
LOAD  V0  7      ; width = 7
LOAD  V1  4      ; height = 4
MUL   V2  V0  V1 ; area = 7 × 4 = 28
ADD   V4  V0  V1 ; V4 = width + height = 11
LOAD  V5  2      ; constant 2
MUL   V3  V5  V4 ; perimeter = 2 × 11 = 22
```

V2 = 28 ✓, V3 = 22 ✓
</details>
