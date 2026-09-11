# Challenge 2.5 — Sequential Circuits

**Type:** State tracing + design + written analysis  
**Estimated time:** 40–50 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — SR Latch State Trace

Trace the SR latch through this sequence of inputs. Start with Q=0.

| Step | S | R | Q (before) | Q (after) | Action |
|------|---|---|------------|-----------|--------|
| 1    | 0 | 0 | 0 | ? | |
| 2    | 1 | 0 | ? | ? | |
| 3    | 0 | 0 | ? | ? | |
| 4    | 0 | 1 | ? | ? | |
| 5    | 0 | 0 | ? | ? | |
| 6    | 1 | 0 | ? | ? | |
| 7    | 1 | 1 | ? | ? | FORBIDDEN |
| 8    | 0 | 0 | ? | ? | |

1. Fill in the Q column.
2. What happens at step 7? Why is S=R=1 forbidden?
3. What happens at step 8 after the forbidden state? What is the problem?

---

## Part B — D Flip-Flop Clock Trace

A D flip-flop captures D on each rising clock edge. Trace Q through these clock cycles.

| Clock edge | D (before edge) | Q (after edge) |
|-----------|-----------------|----------------|
| Rise 1 | 1 | ? |
| Rise 2 | 0 | ? |
| Rise 3 | 0 | ? |
| Rise 4 | 1 | ? |
| Rise 5 | 1 | ? |

Between Rise 3 and Rise 4, D is changed from 0 → 1 → 0 → 1 three times rapidly. What is Q after Rise 4?

*(Key insight: only the value of D immediately before the rising edge matters.)*

---

## Part C — 4-Bit Synchronous Counter

A 4-bit synchronous counter starts at `0000`. Write out the first 20 states it passes through (continuing past 1111).

| Clock | Q3 Q2 Q1 Q0 | Decimal |
|-------|-------------|---------|
| 0     | 0 0 0 0     | 0       |
| 1     | ? | 1 |
| 2     | ? | 2 |
| ... | | |
| 15    | 1 1 1 1 | 15 |
| 16    | ? | ? |
| 17    | ? | ? |

What happens after count 15? Why?

---

## Part D — Design: Modulo-6 Counter

Design a counter that counts: 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, ...  
(It resets to 0 after reaching 5.)

1. A standard 3-bit binary counter counts 0–7. You need 0–5.
2. Which state triggers the reset? What does the reset condition look like in Boolean logic?  
   *(Hint: 6 = `110`. Which bits are both 1 in state 6?)*
3. Write the reset condition as a Boolean expression.
4. How would you wire this to the counter's synchronous reset input?
5. Run this in the simulation's counter tool and verify it counts 0→5→0.

---

## Part E — Written Questions

1. **Combinational vs Sequential**: Explain in 2–3 sentences the fundamental difference between a combinational circuit and a sequential circuit. Give one example of each from this course.

2. **Why clock edges?** A D latch is "transparent" when enabled. Why does this cause problems in cascaded circuits? How does edge-triggering solve it?

3. **Setup and hold time**: A flip-flop has setup time = 100ps and hold time = 20ps, and propagation delay = 200ps. The combinational logic between two flip-flops has a worst-case delay of 150ps. What is the minimum clock period? What is the maximum clock frequency?

4. **Registers as memory**: A CPU has 16 registers, each 64 bits wide. How many D flip-flops does that require? How many bits of total register file storage is that?

---

## Rubric

| Part | Points |
|------|--------|
| A SR latch trace | 20 |
| B DFF clock trace | 15 |
| C counter sequence | 15 |
| D modulo-6 design | 25 |
| E written questions | 25 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A</summary>

| Step | S | R | Q before | Q after | |
|------|---|---|----------|---------|---|
| 1 | 0 | 0 | 0 | **0** | Hold |
| 2 | 1 | 0 | 0 | **1** | Set |
| 3 | 0 | 0 | 1 | **1** | Hold |
| 4 | 0 | 1 | 1 | **0** | Reset |
| 5 | 0 | 0 | 0 | **0** | Hold |
| 6 | 1 | 0 | 0 | **1** | Set |
| 7 | 1 | 1 | 1 | **undefined** | Both outputs go 0 in NOR latch |
| 8 | 0 | 0 | undefined | **unpredictable** | Race condition |
</details>

<details>
<summary>Part B</summary>

Rise 1: Q=1, Rise 2: Q=0, Rise 3: Q=0, Rise 4: Q=1 (captures the D=1 just before edge 4), Rise 5: Q=1.

The rapid D changes between Rise 3 and 4 are irrelevant — only the value of D at the moment of the clock edge matters.
</details>

<details>
<summary>Part D</summary>

Reset condition: count reaches 6 = `0110`. Q2=1 AND Q1=1 → reset expression: `RESET = Q2 AND Q1`. Wire this to the synchronous clear input of the counter.
</details>

<details>
<summary>Part E.3</summary>

Minimum clock period = propagation delay + setup time = 200ps + 100ps = **300ps**.  
Maximum clock frequency = 1/300ps = **~3.33 GHz**.
</details>
