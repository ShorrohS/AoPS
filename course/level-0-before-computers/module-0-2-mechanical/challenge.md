# Challenge 0.2 — Gears and Carries

**Type:** Simulation use + written mechanical trace  
**Estimated time:** 25–35 minutes  
**Tools needed:** `simulation.html` open in your browser + pen and paper

---

## Part A — Napier's Bones (Simulation)

Use the **Napier's Bones tool** in the simulation to solve these multiplications. For each one, write down:
1. Which rods you selected
2. Which row you read
3. The diagonal values you added
4. The final answer

### Problems

1. `347 × 6`
2. `829 × 7`
3. `1284 × 9`

**After completing each:** verify your answer using regular multiplication. They must match.

---

## Part B — Pascaline Carry Trace (Written + Simulation)

Use the **Pascaline tool** in the simulation and add `798 + 203`.

Watch the animation carefully. Then answer:

1. When the units wheel processes `8 + 3 = 11`, what physically happens to the units wheel? What happens to the tens wheel?

2. When the tens wheel processes `9 + 0 + (carry from units) = 10`, what happens next?

3. When the hundreds wheel processes `7 + 2 + (carry from tens) = 10`, what happens?

4. Write out the full carry trace in this format:
```
Units:    8 + 3 = 11  → write 1, carry 1 to tens
Tens:     9 + 0 + 1 = __ → write ?, carry ? to hundreds
Hundreds: 7 + 2 + ? = __ → write ?, carry ? to thousands
Thousands: 0 + 0 + ? = __  → final result
```

5. What is the final result? Verify: `798 + 203 = ?`

---

## Part C — The Overflow Question

Add `9999 + 1` on the Pascaline simulator.

1. How many wheels move?
2. What is the result displayed?
3. What *should* the result be?
4. This is called **integer overflow**. In one sentence, explain what overflow means in terms of the physical machine.
5. Where will you encounter this same problem again in modern computers? (Hint: think about what happens when a 32-bit counter reaches its maximum value.)

---

## Part D — Design Thinking

Without using any electronics, describe in 3–5 sentences how you would build a mechanical device that automatically multiplies two single-digit numbers (1–9) using only gears and wheels. You don't need to be technically precise — focus on the principle.

*There is no single right answer here. We're looking for mechanical reasoning.*

---

## Rubric

| Part | Points | What we're looking for |
|------|--------|------------------------|
| A — 3 multiplications | 30 | Correct rods, rows, diagonal addition, verified answer |
| B1–B3 | 20 | Correct description of what each wheel does |
| B4 — carry trace | 20 | Correctly filled-in trace table |
| B5 — final result | 5 | 1001 ✓ |
| C1–C4 | 15 | Correct overflow analysis |
| D | 10 | Thoughtful mechanical reasoning |

**Total: 100 points**

---

## Hints

<details>
<summary>Hint — Napier's Bones diagonal addition</summary>
Read each diagonal from top-right to bottom-left. Add the two numbers sharing a diagonal cell. Write down the ones digit, carry the tens digit to the next diagonal left.
</details>

<details>
<summary>Hint — Part B carry trace</summary>
Each wheel can only show 0–9. When the sum exceeds 9, the wheel shows (sum - 10) and sends a carry of 1 to the next wheel.
</details>

<details>
<summary>Hint — Part C overflow</summary>
A 4-wheel Pascaline can only represent 0000–9999. What is 9999 + 1 if you only have 4 digits?
</details>

---

## Solutions

<details>
<summary>Part A Solutions</summary>

**347 × 6:**
- Rods: 3, 4, 7 — Row 6
- Diagonals: `1/8 | 2/4 | 4/2`
- Addition: `1 | (8+2) | (4+4) | 2` = `1 | 10 | 8 | 2`
- Carry the 10: `2 | 0 | 8 | 2` = **2082**

**829 × 7:**
- Rods: 8, 2, 9 — Row 7
- Diagonals: `5/6 | 1/4 | 6/3`
- Addition: `5 | (6+1) | (4+6) | 3` = `5 | 7 | 10 | 3`
- Carry: `5 | 8 | 0 | 3` = **5803**

**1284 × 9:**
- Rods: 1, 2, 8, 4 — Row 9
- Diagonals: `0/9 | 1/8 | 7/2 | 3/6`
- Addition: `0 | (9+1) | (8+7) | (2+3) | 6` = `0 | 10 | 15 | 5 | 6`
- Carry: `1 | 1 | 5 | 5 | 6` = **11556**

</details>

<details>
<summary>Part B Solution</summary>

```
Units:    8 + 3 = 11  → write 1, carry 1 to tens
Tens:     9 + 0 + 1 = 10 → write 0, carry 1 to hundreds
Hundreds: 7 + 2 + 1 = 10 → write 0, carry 1 to thousands
Thousands: 0 + 0 + 1 = 1 → write 1, no carry
```

Final result: **1001** ✓

</details>

<details>
<summary>Part C Solution</summary>

1. All 4 wheels move (a cascade carry through every position)
2. The display shows **0000**
3. The correct result is **10000** — which needs 5 digits
4. Overflow: the machine's physical capacity (4 wheels = max 9999) was exceeded; the result wraps around to 0 because there is no fifth wheel to receive the final carry
5. Same problem in 32-bit integers: max value 4,294,967,295 — add 1 and it wraps to 0. Classic overflow bug.

</details>
