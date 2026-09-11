# Challenge 2.4 — Combinational Circuits

**Type:** Circuit tracing + arithmetic + design  
**Estimated time:** 40–50 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Full Adder Truth Table

Complete the full truth table for a full adder (A + B + Cin).

| A | B | Cin | Sum | Cout |
|---|---|-----|-----|------|
| 0 | 0 | 0   |     |      |
| 0 | 0 | 1   |     |      |
| 0 | 1 | 0   |     |      |
| 0 | 1 | 1   |     |      |
| 1 | 0 | 0   |     |      |
| 1 | 0 | 1   |     |      |
| 1 | 1 | 0   |     |      |
| 1 | 1 | 1   |     |      |

Verify that Sum = A XOR B XOR Cin and Cout = (A AND B) OR (Cin AND (A XOR B)).

---

## Part B — 4-Bit Ripple Carry Addition

Perform each addition by tracing through all four full adder stages. Show Cin, Sum, and Cout for every stage.

1. `0101 + 0011` (5 + 3)

| Stage | A_i | B_i | Cin | Sum | Cout |
|-------|-----|-----|-----|-----|------|
| FA0   | 1   | 1   | 0   |     |      |
| FA1   | 0   | 1   |  ↑  |     |      |
| FA2   | 1   | 0   |  ↑  |     |      |
| FA3   | 0   | 0   |  ↑  |     |      |

2. `1001 + 0111` (9 + 7). Be careful — this overflows 4 bits!

3. `1111 + 0001` (15 + 1). Show what happens.

---

## Part C — Subtraction via Two's Complement

A 4-bit ALU implements subtraction as: `A - B = A + (NOT B) + 1`

1. Compute `8 - 5` using this method:
   - A = `1000`, B = `0101`
   - NOT B = ?
   - Cin = 1 (the "+1" for two's complement)
   - Add A + NOT B + 1 using the 4-bit adder
   - What is the result in binary and decimal?

2. Compute `3 - 7` (this should give −4 in two's complement):
   - A = `0011`, B = `0111`
   - Work through the same steps
   - Interpret the result as a signed 4-bit two's complement number

---

## Part D — Multiplexer Design

A **2-to-1 MUX** selects between input A and input B based on select signal S.

1. Write the Boolean expression: `Y = (NOT S AND A) OR (S AND B)`
2. Build the complete truth table (3 inputs: S, A, B)
3. How many gates are needed? (AND, OR, NOT)
4. What does this MUX do when S=0? When S=1?
5. Design a **4-to-1 MUX** (2 select bits S1, S0 choosing between A, B, C, D). How many 2-to-1 MUXes would you need to chain together?

---

## Part E — Critical Path Analysis

A 4-bit ripple-carry adder has the following gate delays:
- XOR gate: 20ps
- AND gate: 15ps
- OR gate: 15ps

The full adder uses:
- Sum = A XOR B XOR Cin (two XOR gates in series)
- Cout = (A AND B) OR (Cin AND (A XOR B)) — uses AND, XOR, AND, OR

1. What is the critical path delay for one full adder? (Consider both Sum and Cout paths.)
2. What is the total carry-chain delay through all 4 stages of a 4-bit adder?
3. At what maximum clock frequency can this 4-bit adder run?

---

## Rubric

| Part | Points |
|------|--------|
| A full adder truth table | 20 |
| B carry trace (3 additions) | 25 |
| C subtraction | 25 |
| D MUX design | 15 |
| E delay analysis | 15 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A</summary>

| A | B | Cin | Sum | Cout |
|---|---|-----|-----|------|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |
</details>

<details>
<summary>Part B.1</summary>

0101 + 0011 = 1000 (8)

| Stage | A | B | Cin | Sum | Cout |
|-------|---|---|-----|-----|------|
| FA0 | 1 | 1 | 0 | 0 | 1 |
| FA1 | 0 | 1 | 1 | 0 | 1 |
| FA2 | 1 | 0 | 1 | 0 | 1 |
| FA3 | 0 | 0 | 1 | 1 | 0 |

Result: **1000** = 8 ✓
</details>

<details>
<summary>Part C.1 (8-5)</summary>

A=1000, B=0101, NOT B=1010, Cin=1  
1000 + 1010 + 1 = 10011 → keep 4 bits → **0011** = 3 ✓ (8−5=3)
</details>
