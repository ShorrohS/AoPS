# Challenge 2.1 — Why Binary?

**Type:** Calculation + simulation + written analysis  
**Estimated time:** 25–35 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Noise Margin Calculations

A **5V CMOS** logic family has these specifications:
- Output HIGH guaranteed: ≥ 4.5V
- Output LOW guaranteed: ≤ 0.5V
- Input HIGH minimum: 3.5V
- Input LOW maximum: 1.5V

A **3.3V LVTTL** logic family has:
- Output HIGH guaranteed: ≥ 2.4V
- Output LOW guaranteed: ≤ 0.4V
- Input HIGH minimum: 2.0V
- Input LOW maximum: 0.8V

1. Calculate the **HIGH noise margin** for both families:  
   `NM_H = V_OH(min) − V_IH(min)`

2. Calculate the **LOW noise margin** for both families:  
   `NM_L = V_IL(max) − V_OL(max)`

3. Which family tolerates more noise? By how much?

4. A signal passes through **50 gates in series**. Each gate adds an average of 5mV of noise. Does either logic family survive? Show your working.

---

## Part B — Precision: Analog vs Digital

An **analog computer** represents a 10-digit decimal number as a voltage between 0V and 10V. Each decimal digit requires a distinct voltage level (0.0V, 1.0V, 2.0V… 9.0V for a 1-digit machine).

1. For 10 voltage levels (1 decimal digit): how much voltage separates adjacent levels?

2. If the circuit adds ±0.3V of noise, which voltage levels can be confused? How many misreads are possible?

3. A **binary** system encodes the same decimal range using 4 bits (0000 to 1001 = 0–9). Each bit uses the 5V CMOS thresholds above. What is the noise margin for each bit?

4. Which system is more reliable? Quantify the comparison (noise margin ÷ level separation).

---

## Part C — Bit Counting (Simulation)

Using the **Bit Counter** tool in the simulation:

1. Find the binary representation of: 42, 127, 200, 255
2. How many bits does each require?
3. What is the largest decimal value representable with exactly 8 bits (unsigned)?
4. With 8 bits signed (two's complement), what is the range? *(Hint: one bit is the sign bit)*
5. Your friend says "I need to store numbers up to 1,000,000. What's the minimum number of bits I need?" Calculate and verify in the simulator.

---

## Part D — Signal Regeneration (Simulation)

Using the **Signal Noise Demonstrator**:

1. Set noise to 20%. How many analog readings are misidentified vs binary?
2. Increase noise to 40%. At what noise level does the binary system first produce errors?
3. Set up a chain of 5 "amplifier stages" with 10% noise each. Compare accumulated noise in analog vs binary systems.

---

## Part E — Written Analysis

1. **Why not decimal?** ENIAC was a decimal machine (10-state ring counters per digit). It required approximately 10 transistors per digit. A binary machine uses 1 transistor per bit, and 4 bits can represent 16 values (more than a decimal digit). How many transistors does a binary machine need per decimal digit's worth of range? Is binary more efficient?

2. **The regeneration argument**: A message is copied through 100 relay stations. In an analog relay system, each station amplifies both signal AND noise. In a digital system, each relay regenerates the signal. If each relay adds 1% noise (in analog), what is the signal-to-noise ratio after 100 relays? In binary? (Qualitative comparison is fine.)

3. **Why does flash memory use multi-level cells but CPUs don't?** Explain the trade-off that makes MLC practical for storage but not for compute logic.

---

## Rubric

| Part | Points |
|------|--------|
| A noise margin calculations | 20 |
| B analog vs digital precision | 20 |
| C bit counting | 15 |
| D simulation observations | 15 |
| E written analysis (3 questions) | 30 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A</summary>

**5V CMOS:**  
NM_H = 4.5 − 3.5 = **1.0V**  
NM_L = 1.5 − 0.5 = **1.0V**

**3.3V LVTTL:**  
NM_H = 2.4 − 2.0 = **0.4V**  
NM_L = 0.8 − 0.4 = **0.4V**

5V CMOS tolerates **2.5× more noise** (1.0V vs 0.4V).

50 gates × 5mV = 250mV total noise. 5V CMOS: 1000mV margin → **survives**. 3.3V LVTTL: 400mV margin → **barely survives** (250mV < 400mV).
</details>

<details>
<summary>Part B</summary>

1. 10V ÷ 10 levels = **1.0V** separation between analog levels.

2. ±0.3V noise means any reading could be off by 0.3V. Adjacent levels (1.0V apart) need >0.3V margin on each side — total margin is 0.4V. **0.3V noise makes adjacent level confusion possible** (e.g., 2.7V–3.3V overlaps both "3.0V" and nearby levels).

3. Binary bits use 5V CMOS: noise margin = **1.0V per bit** — dramatically better than the 0.4V analog margin.

4. Binary is 1.0/0.5 = **2.5× more reliable** per level-separation-unit.
</details>

<details>
<summary>Part C</summary>

1. 42 = `00101010`, 127 = `01111111`, 200 = `11001000`, 255 = `11111111`
2. All fit in 8 bits.
3. 8-bit unsigned max = 2⁸ − 1 = **255**
4. 8-bit signed: −128 to +127
5. 1,000,000 < 2²⁰ = 1,048,576. Need **20 bits** minimum.
</details>
