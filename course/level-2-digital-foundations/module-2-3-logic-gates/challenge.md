# Challenge 2.3 — Boolean Algebra and Logic Gates

**Type:** Truth tables + algebra + circuit design  
**Estimated time:** 40–50 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Truth Tables

Build the complete truth table for each expression.

1. `Y = A AND (NOT B)`

| A | B | NOT B | Y |
|---|---|-------|---|
| 0 | 0 | | |
| 0 | 1 | | |
| 1 | 0 | | |
| 1 | 1 | | |

2. `Y = (A OR B) AND (NOT A OR C)` — 3 variables, 8 rows

3. `Y = NOT (A XOR B)` — what common gate is this?

---

## Part B — Boolean Algebra Simplification

Simplify each expression. Show every step and name the law used.

1. `Y = A AND (A OR B)`

2. `Y = (A AND B) OR (A AND NOT B) OR (NOT A AND B)`

3. `Y = NOT(NOT A AND NOT B)` — apply De Morgan's

4. `Y = A OR (NOT A AND B)` — *hint: distributive, then complementation*

5. Prove that `XOR` can be written as: `A ⊕ B = (A OR B) AND NOT(A AND B)`  
   Verify by building the truth table for both sides.

---

## Part C — Implement from Truth Table

This truth table defines a circuit. Your job: find the minimal gate implementation.

| A | B | C | Y |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 |
| 1 | 1 | 1 | 1 |

1. Write the Sum of Products expression (one AND term per output-1 row)
2. Simplify it — what is the minimal expression?
3. How many gates does the minimal circuit need?
4. Build it in the simulation and verify.

---

## Part D — NAND-Only Implementation

Implement the following using **only NAND gates**. Draw the circuit (or describe gate connections precisely).

1. `NOT A` — how many NANDs?
2. `A AND B` — how many NANDs?
3. `A OR B` — how many NANDs? *(hint: De Morgan)*
4. `A XOR B` — minimum NANDs is 4. Find the implementation.
5. A **2-to-1 MUX**: `Y = (NOT S AND A) OR (S AND B)`  
   Implement with only NANDs. How many do you need?

---

## Part E — Gate Delay Analysis

A full adder's critical path goes through:
- 2 XOR gates in series (for Sum)
- 2 AND gates + 1 OR gate in series (for Carry)

Assume each gate has a propagation delay of 20ps.

1. What is the critical path delay for one full adder?
2. A 16-bit ripple-carry adder chains 16 full adders. What is the total carry-chain delay?
3. At what maximum frequency can this 16-bit adder theoretically run?
4. A modern CPU runs at 4 GHz. Does a ripple-carry adder fit? What would a designer need to do differently?

---

## Rubric

| Part | Points |
|------|--------|
| A truth tables | 20 |
| B simplifications | 25 |
| C from truth table | 20 |
| D NAND-only | 20 |
| E delay analysis | 15 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1</summary>

| A | B | NOT B | Y = A AND NOT B |
|---|---|-------|-----------------|
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 |
</details>

<details>
<summary>Part B solutions</summary>

1. `A AND (A OR B) = A` — Absorption law
2. `(AB) OR (A·NOT B) OR (NOT A·B) = A(B+NOT B) OR NOT A·B = A OR (NOT A·B)`. Apply: `A OR (NOT A·B) = (A OR NOT A)(A OR B) = 1·(A OR B) = A OR B`
3. `NOT(NOT A AND NOT B)` — De Morgan: `= A OR B`
4. `A OR (NOT A AND B) = (A OR NOT A)(A OR B) = A OR B`
</details>

<details>
<summary>Part C</summary>

SoP: `(NOT A·NOT B·C) OR (NOT A·B·C) OR (A·NOT B·C) OR (A·B·C)`  
Factor out C: `C·(NOT A·NOT B + NOT A·B + A·NOT B + A·B) = C·1 = C`  
Minimal expression: **Y = C**. One wire, zero gates!
</details>

<details>
<summary>Part D.4 XOR from 4 NANDs</summary>

```
G1 = NAND(A, B)
G2 = NAND(A, G1)
G3 = NAND(B, G1)
G4 = NAND(G2, G3) = A XOR B
```
</details>

<details>
<summary>Part E</summary>

1. Critical path: XOR chain = 2×20ps = **40ps** for Sum; AND-AND-OR = 3×20ps = **60ps** for Carry. Critical path = **60ps per full adder**.
2. 16 full adders: 16 × 60ps = **960ps**
3. f_max = 1/960ps = **~1.04 GHz** — a 16-bit ripple carry barely exceeds 1 GHz.
4. A 4 GHz CPU needs the carry computed in 250ps. A ripple adder can't do it. Solution: **carry lookahead** — compute all carries in parallel in 2 gate delays (~40ps), then the full 64-bit add fits in 4 GHz timing.
</details>
