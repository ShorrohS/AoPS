# Challenge 1.6 — Moore's Law and the Level 1 Capstone

**Type:** Calculation + simulation + comprehensive written capstone  
**Estimated time:** 45–60 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Moore's Law Mathematics

1. The Intel 4004 (1971) had 2,300 transistors. Moore's Law predicts doubling every 2 years. How many transistors does the model predict for 2023 (52 years later)? Show: `2,300 × 2^(52/2)`

2. The Apple M3 (2023) actually has ~25 billion transistors. How does this compare to your prediction? Express the real count as a percentage of the prediction. What does any deviation tell you about the actual doubling rate?

3. If the doubling period slowed to every 3 years after 2015 (instead of 2 years), recalculate the 2023 prediction starting from the 2015 Intel Broadwell chip (~1.9 billion transistors). How many transistors does this predict vs the M3's actual count?

4. At the current pace of ~20% transistor size reduction per year, a transistor at 2nm (2024) would reach 0.1nm (roughly 1 atom wide) in how many years? Show your calculation. What does this tell us about the physical future of Moore's Law?

---

## Part B — Photolithography Scale (Simulation)

Using the **Photolithography Simulator**:

1. Set feature size to 10µm (early 1970s). How many transistors fit in a 1cm × 1cm chip area?
2. Set feature size to 130nm (2001). How many fit now? What is the density increase factor?
3. Set feature size to 5nm (2020). How many fit?
4. The improvement from 10µm to 5nm is a factor of 2,000 in linear dimension. Since transistors occupy area (2D), what is the density improvement factor? Does this match your simulation results?

---

## Part C — Doubling Calculator (Simulation)

Use the **Doubling Calculator** to answer:

1. Your laptop has 25 billion transistors today. If Moore's Law continues at the historical rate (doubling every 2 years), how many transistors will your 2030 laptop have?

2. If a transistor currently costs 10⁻¹² dollars to manufacture (one picodollar — $0.000000000001), what does a chip with 25 billion transistors cost to manufacture just in transistor cost? *(Hint: don't forget the number of chips per wafer and yield factors — but just use the simple multiplication for this exercise.)*

3. The first transistor (1947) was hand-built and cost approximately $8 in 1947 dollars (~$110 today). A transistor today costs roughly $10⁻¹³. How many orders of magnitude cheaper has the transistor become?

---

## Part D — The Full Story (Level 1 Capstone)

This is your graduation from Level 1. Write a connected narrative (one paragraph per point, ~3–5 sentences each) tracing the complete story from Module 1.1 to 1.6.

### Narrative Arc

**D1 — The Foundation (Module 1.1)**  
Explain why electricity replaced mechanical motion as the medium for computation. What physical property of electrons makes them better than gears for computing?

**D2 — The Binary Atom (Module 1.2)**  
Why is a switch the fundamental unit of computation? Explain the connection: switch → two states → binary digit → bit.

**D3 — Logic from Metal (Module 1.3)**  
How did Shannon connect Boolean algebra to physical circuits? What does it mean that AND, OR, NOT are "functionally complete"?

**D4 — The Speed Leap (Module 1.4)**  
What physical change let vacuum tubes switch 1,000× faster than relays? What was the cost of this speed?

**D5 — The Semiconductor Revolution (Module 1.5)**  
How does a MOSFET improve on a vacuum tube? Focus on: what it replaces (thermionic emission → field effect), and what it eliminates (heater, vacuum, fragility).

**D6 — The Exponential Engine (Module 1.6)**  
What is Moore's Law and what physical mechanism drove it? Connect it to everything that came before: without the transistor's solid-state nature, miniaturisation would have been impossible.

**D7 — The Thread**  
In a single paragraph, describe the single continuous idea that runs from Jacquard's punch card loom (1804) through Shannon's relay circuits (1937) to a modern MOSFET (2024). What has changed? What fundamental idea is the same?

---

## Rubric

| Part | Points | What we're looking for |
|------|--------|------------------------|
| A1–A4 calculations | 25 | Correct math, units, physical reasoning |
| B photolithography | 15 | Correct density calculations |
| C doubling calculator | 10 | Correct projections |
| D1–D6 narrative | 40 | Precise, historically grounded, correct physics |
| D7 thread | 10 | Identifies binary switching as the constant |

**Total: 100 points**

---

## Hints

<details>
<summary>Hint — A1</summary>
2^(52/2) = 2^26. Calculate step by step: 2^10 = 1024, 2^20 ≈ 1 million, 2^26 ≈ 67 million.
Result: 2,300 × 67,108,864 ≈ 154 billion.
</details>

<details>
<summary>Hint — A4 (physical limits)</summary>
Current size: 2nm. Target: 0.1nm. Reduction needed: 2/0.1 = 20× reduction.
Each year: feature size reduces by ~20% → multiply by 0.8 each year.
0.8^n = 1/20 → n × log(0.8) = log(0.05) → n ≈ 14 years from 2024 → ~2038.
</details>

<details>
<summary>Hint — D7 thread</summary>
The constant is: a physical binary state (hole/no-hole, contact/open, tube on/off, transistor on/off) representing 1 or 0, read by a mechanism that can act on that state without human intervention. The medium changes; the logic doesn't.
</details>

---

## Solutions

<details>
<summary>Part A Solutions</summary>

**A1:** 2,300 × 2^26 = 2,300 × 67,108,864 ≈ **154 billion**

**A2:** M3 actual = 25 billion. Prediction = 154 billion.  
25/154 = 16% of prediction.  
The actual count is ~6× lower than the pure Moore's Law prediction. This reflects the slowdown since ~2015 when the doubling period stretched from 2 years to ~2.5–3 years. The law hasn't ended but has clearly decelerated.

**A3:** Starting 2015: 1.9 billion transistors. Years 2015→2023 = 8 years at 3-year doubling = 2.67 doublings.  
1.9B × 2^2.67 ≈ 1.9B × 6.35 ≈ **12 billion**.  
M3 actual: 25 billion — higher, suggesting the pace was still faster than 3 years per doubling in some years.

**A4:** Need: 2nm → 0.1nm = 20× reduction. Rate: 20% per year = multiply by 0.8.  
0.8^n = 0.1/2 = 0.05. n = log(0.05)/log(0.8) ≈ (-2.996)/(-0.097) ≈ **~14 years → around 2038**.  
This is roughly when transistors would be 1 atom wide — physically impossible to shrink further with silicon. This is why the industry is pursuing new materials (III-V semiconductors, carbon nanotubes) and 3D architectures.
</details>

<details>
<summary>Part C3 (cost reduction)</summary>
1947 cost: ~$110 today.  
Today's cost: ~$10⁻¹³.  
Ratio: 110 / 10⁻¹³ = 1.1 × 10¹⁵.  
That's **15 orders of magnitude** cheaper — a quadrillion-fold cost reduction in ~75 years.  
No other manufactured product in history comes close to this cost reduction curve.
</details>
