# Challenge 1.3 — Relay Logic and Boolean Algebra

**Type:** Simulation circuit building + Boolean algebra + truth tables  
**Estimated time:** 35–45 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Boolean Algebra Manipulation

Simplify each expression using Boolean algebra identities. Show every step.

1. `A AND (A OR B)`  
   *(Hint: Absorption law — A AND (A OR B) = ?)*

2. `(A AND B) OR (A AND NOT B)`  
   *(Factor out A)*

3. `NOT (NOT A AND NOT B)`  
   *(Apply De Morgan's Law)*

4. `(A OR B) AND (A OR NOT B)`  
   *(Distribute, then simplify)*

5. Verify De Morgan's Law for the case A=1, B=0:  
   Show that `NOT (A AND B) = (NOT A) OR (NOT B)` evaluates to the same value on both sides.

---

## Part B — Truth Tables

Complete the truth tables for these expressions:

### Expression 1: `(A AND B) OR (NOT A AND NOT B)`

| A | B | A AND B | NOT A | NOT B | NOT A AND NOT B | Result |
|---|---|---------|-------|-------|-----------------|--------|
| 0 | 0 |         |       |       |                 |        |
| 0 | 1 |         |       |       |                 |        |
| 1 | 0 |         |       |       |                 |        |
| 1 | 1 |         |       |       |                 |        |

**What logic function does this implement?** (Hint: when is the output 1?)

### Expression 2: XOR from primitives: `(A OR B) AND NOT(A AND B)`

| A | B | A OR B | A AND B | NOT(A AND B) | Result |
|---|---|--------|---------|--------------|--------|
| 0 | 0 |        |         |              |        |
| 0 | 1 |        |         |              |        |
| 1 | 0 |        |         |              |        |
| 1 | 1 |        |         |              |        |

---

## Part C — Half Adder (Simulation)

Using the **Half Adder** tab in the simulation:

1. Test all 4 input combinations and verify the Sum and Carry outputs match this table:

| A | B | Sum (XOR) | Carry (AND) |
|---|---|-----------|-------------|
| 0 | 0 |     ?     |      ?      |
| 0 | 1 |     ?     |      ?      |
| 1 | 0 |     ?     |      ?      |
| 1 | 1 |     ?     |      ?      |

2. If you connected two half adders together (to add 3 bits instead of 2), what would you call the result? Describe what additional input it would need and what it would output.  
*(This is a preview of the Full Adder you'll build in Module 2.4)*

---

## Part D — Build a 1-Bit Comparator

A **1-bit comparator** outputs 1 when inputs A and B are equal (both 0 or both 1), and 0 when they differ.

1. Look at the truth table from Part B, Expression 1. What is the relationship between that expression and the comparator function?

2. Write the Boolean expression for the comparator in two ways:
   - As a sum-of-products (OR of AND terms)
   - As a simplified form (using XOR or XNOR)

3. Using the **Boolean Expression Evaluator** in the simulation, enter your expression and verify it produces the correct truth table.

4. How many relay contacts would you need to implement this comparator in hardware? Count them.

---

## Part E — Shannon's Impact (Written)

Answer each question in 2–4 sentences:

1. **Before Shannon (1937)**, Boolean algebra and relay circuits were separate fields. Describe what gap Shannon's thesis bridged, and why that gap had existed for 83 years.

2. **The Zuse Z3** ran at 5.3 Hz. A modern CPU runs at 5 GHz. Express this as a ratio and explain what physical change made this improvement possible (not just "transistors are faster" — explain *why* they're faster).

3. **The Mark I** had 800 km of wire. Why does miniaturization matter beyond just saving space? Describe at least two computing advantages that come from physically smaller components (hint: think about signal travel time and power).

---

## Rubric

| Part | Points | What we're looking for |
|------|--------|------------------------|
| A1–A5 simplifications | 25 | Correct steps, correct identities named |
| B truth tables | 20 | All 8 entries correct per table |
| B — function identification | 5 | Correctly names XNOR/equivalence |
| C half adder verification | 10 | All 4 rows correct |
| C full adder description | 10 | Correct: carry-in input, sum + carry-out outputs |
| D comparator design | 15 | Correct expression + relay count |
| E written questions | 15 | Precise, historically grounded |

**Total: 100 points**

---

## Hints

<details>
<summary>Hint — Part A1 (Absorption)</summary>
A AND (A OR B): distribute → (A AND A) OR (A AND B) → A OR (A AND B) → A.
The result is just A. A "absorbs" the OR expression.
</details>

<details>
<summary>Hint — Part A3 (De Morgan)</summary>
NOT(NOT A AND NOT B) = NOT(NOT A) OR NOT(NOT B) = A OR B
</details>

<details>
<summary>Hint — Part B Expression 1</summary>
The output is 1 when A and B are both 0 OR both 1. That is: when A equals B. This is the XNOR function (equivalence).
</details>

<details>
<summary>Hint — Part D relay count</summary>
XNOR = NOT(XOR). XOR needs: 1 OR-relay pair (parallel) + 1 NAND-relay pair (series NC) + 1 AND connecting them. XNOR adds a NOT (1 NC contact). Count the contacts.
</details>

---

## Solutions

<details>
<summary>Part A Solutions</summary>

1. `A AND (A OR B) = (A AND A) OR (A AND B) = A OR (A AND B) = A`  
   (Absorption: A AND (A OR B) = A)

2. `(A AND B) OR (A AND NOT B) = A AND (B OR NOT B) = A AND 1 = A`

3. `NOT(NOT A AND NOT B) = NOT(NOT A) OR NOT(NOT B) = A OR B`  
   (De Morgan + double negation)

4. `(A OR B) AND (A OR NOT B) = A OR (B AND NOT B) = A OR 0 = A`  
   (Distributive law + contradiction)

5. A=1, B=0: `NOT(1 AND 0) = NOT(0) = 1`  
   `(NOT 1) OR (NOT 0) = 0 OR 1 = 1` ✓ Both sides equal 1.
</details>

<details>
<summary>Part B Solutions</summary>

**Expression 1 — XNOR:**

| A | B | A AND B | NOT A | NOT B | NOT A AND NOT B | Result |
|---|---|---------|-------|-------|-----------------|--------|
| 0 | 0 | 0 | 1 | 1 | 1 | **1** |
| 0 | 1 | 0 | 1 | 0 | 0 | **0** |
| 1 | 0 | 0 | 0 | 1 | 0 | **0** |
| 1 | 1 | 1 | 0 | 0 | 0 | **1** |

This is **XNOR** (equivalence): output 1 when A equals B.

**Expression 2 — XOR:**

| A | B | A OR B | A AND B | NOT(A AND B) | Result |
|---|---|--------|---------|--------------|--------|
| 0 | 0 | 0 | 0 | 1 | **0** |
| 0 | 1 | 1 | 0 | 1 | **1** |
| 1 | 0 | 1 | 0 | 1 | **1** |
| 1 | 1 | 1 | 1 | 0 | **0** |
</details>

<details>
<summary>Part D Solution</summary>

The comparator = XNOR = `(A AND B) OR (NOT A AND NOT B)`

Sum-of-products: `(A AND B) OR (NOT A AND NOT B)`  
Simplified: `NOT (A XOR B)` = XNOR(A, B)

Relay count for XNOR via `(A AND B) OR (NOT A AND NOT B)`:
- A AND B: 2 NO contacts in series = 2 contacts
- NOT A AND NOT B: 2 NC contacts in series = 2 contacts
- OR: parallel paths (no extra contacts needed — just wire junction)
- Total: **4 relay contacts**

In a real relay implementation, each relay has one coil and one contact, so 4 relays minimum. A NOT requires a NC contact on a relay already driven by the signal, so with careful sharing you can do it in 4 relays (2 driven by A, 2 driven by B, with NO and NC contacts on each).
</details>
