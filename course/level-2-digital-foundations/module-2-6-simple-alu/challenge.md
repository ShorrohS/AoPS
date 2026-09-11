# Challenge 2.6 — The Simple ALU (Level 2 Capstone)

**Type:** ALU execution + flag analysis + design + capstone  
**Estimated time:** 50–60 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — ALU Operations by Hand

Execute each operation on the 4-bit ALU. Inputs are 4-bit unsigned. Predict results AND flags before simulating.

The ALU operations: ADD, SUB (using two's complement), AND, OR, XOR, NOT A.

| A    | B    | Operation | Result (binary) | Decimal | Z | C | N | V |
|------|------|-----------|-----------------|---------|---|---|---|---|
| 0101 | 0011 | ADD       | ? | ? | ? | ? | ? | ? |
| 1001 | 0111 | ADD       | ? | ? | ? | ? | ? | ? |
| 1010 | 0110 | SUB (A-B) | ? | ? | ? | ? | ? | ? |
| 0011 | 0011 | SUB (A-B) | ? | ? | ? | ? | ? | ? |
| 1111 | 1010 | AND       | ? | ? | ? | ? | — | — |
| 0000 | 1111 | OR        | ? | ? | ? | ? | — | — |
| 1010 | 1010 | XOR       | ? | ? | ? | ? | — | — |
| 0110 | —    | NOT A     | ? | ? | ? | ? | — | — |

---

## Part B — Flag Deep Dive

For each scenario, explain which flags fire and why.

1. ALU computes `7 + 7` in a **4-bit signed** (two's complement) system. Both operands are positive. The result in 4 bits is... what? What flag fires?

2. ALU computes `9 + 9` in 4-bit **unsigned**. What is the result? What flag fires?

3. ALU computes `0101 - 0101`. What are Z, N, C, V?

4. ALU computes `0000 - 0001` (0 minus 1) in 4-bit two's complement. The result is −1 = `1111`. What flags fire?

5. **Carry vs Overflow — explain the difference** in 3 sentences. When does Carry fire but not Overflow? When does Overflow fire but not Carry? (Hint: think unsigned vs signed.)

---

## Part C — ALU Mini-Program

Write a sequence of ALU operations to compute this formula:  
`result = (A AND B) + C` where A = `0110`, B = `1011`, C = `0011`

Step through it:
1. Operation 1: ?  Inputs: ?, ?  Result: ?  Store in accumulator
2. Operation 2: ?  Inputs: accumulator, ?  Result: ?

Verify: AND(0110, 1011) = ? Then + 0011 = ?

---

## Part D — ALU Design Extension

Extend the 4-bit ALU to add two new operations:

1. **Arithmetic shift right (ASR)**: shifts A right by 1, copies MSB into new MSB.  
   Example: `1010` → `1101` (sign-preserving divide by 2)  
   Example: `0110` → `0011` (divide by 2)  
   Describe the circuit: what gates/connections are needed?

2. **Increment (INC)**: A + 1  
   How would you implement this using the existing adder with a fixed B=0001 input? What control signals select it?

---

## Part E — Level 2 Capstone Essay

Write 4–6 sentences for each question.

**E1 — The abstraction ladder**  
You started this level with transistors (Module 2.1). You ended it with an ALU (Module 2.6). Name every abstraction layer you passed through. What did each layer hide, and what did it expose?

**E2 — Why binary arithmetic works**  
Explain why the same adder circuit correctly handles both addition and subtraction (via two's complement). What is the mathematical insight that makes this possible?

**E3 — The stored-program connection**  
The ALU computes. Registers hold values. A counter tracks position. Connecting these three things gives you a computer. Describe in your own words how these three components from Level 2 will combine in Level 3 (Machine Architecture) to form a CPU that can execute programs.

---

## Rubric

| Part | Points |
|------|--------|
| A ALU operations (8 rows) | 24 |
| B flag analysis | 20 |
| C mini-program | 16 |
| D design extension | 15 |
| E capstone essays | 25 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A — Key rows</summary>

- `0101+0011` = 1000 = 8, Z=0, C=0, N=1, V=1 (5+3=8, but in 4-bit signed max is 7 → overflow!)
- `1001+0111` = 10000 → keep 4 bits = 0000 = 0, Z=1, C=1, N=0, V=0
- `1010-0110` = 1010 + 1001 + 1 = 10100 → 0100 = 4 (10−6=4 ✓), Z=0, C=1, N=0, V=0
- `0011-0011` = 0011 + 1100 + 1 = 10000 → 0000 = 0 (3−3=0 ✓), Z=1, C=1, N=0, V=0
- `1111 AND 1010` = 1010, Z=0, C=0, N=1
- `0000 OR 1111` = 1111, Z=0, N=1
- `1010 XOR 1010` = 0000, Z=1
- `NOT 0110` = 1001, Z=0, N=1
</details>

<details>
<summary>Part B.5 — Carry vs Overflow</summary>

**Carry** indicates unsigned overflow — the result exceeded the maximum value representable as an unsigned n-bit integer. **Overflow** indicates signed overflow — the result has the wrong sign for a two's complement interpretation (two positives summed to a negative, or two negatives summed to a positive).

Carry fires without overflow when: `1001 + 1000` = unsigned 9+8=17 > 15, but in signed this is −7 + (−8) = −15, which fits in 4-bit signed (range −8 to +7)... actually this IS signed overflow too. A clear case: `1111 + 0001` = carry set (unsigned 15+1=16), no signed overflow (−1+1=0).

Overflow fires without carry: `0111 + 0001` = no carry (8 fits in 4 bits), but in signed: 7+1=8 exceeds the max of 7 → overflow.
</details>

<details>
<summary>Part C</summary>

Step 1: AND(0110, 1011) = 0010  
Step 2: ADD(0010, 0011) = 0101 = 5  
Verify: (6 AND 11) = (0110 AND 1011) = 0010 = 2. Then 2 + 3 = 5 ✓
</details>
