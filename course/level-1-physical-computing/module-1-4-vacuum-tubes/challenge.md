# Challenge 1.4 — Vacuum Tubes and Switching Speed

**Type:** Calculation + simulation + written analysis  
**Estimated time:** 30–40 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — ENIAC Reliability Math

ENIAC had 17,468 vacuum tubes. Each tube had a mean lifetime of approximately 2,500 hours under normal operating conditions.

1. If all tubes were installed at the same time and had exactly equal lifetimes, how many hours until the first tube fails? (This is the ideal case — in reality, lifetimes vary.)

2. In reality, lifetimes follow a statistical distribution. If you model failures as random events with an average rate of (17,468 tubes ÷ 2,500 hours), how many tube failures do you expect **per hour**?

3. ENIAC ran approximately 8 hours per day in active use. How many tubes would you expect to fail **per day**?

4. A technician can replace one tube in about 15 minutes. How many technicians would you need working simultaneously to keep up with the failure rate during operation?

5. At $10 per tube (1945 price), what was the annual tube replacement cost just from wear-out failures? (Assume 250 operating days per year.)

---

## Part B — Speed Comparison

A relay takes 15ms to close. A vacuum tube switches in 1µs.

1. How many times faster is the tube than the relay? Express as a ratio.

2. A relay computer does 3 arithmetic operations per second. If you replaced every relay with a vacuum tube (same circuit design, just faster switches), how many operations per second could it do?

3. ENIAC actually ran at about 5,000 additions per second. Why is this lower than the theoretical maximum from question B2? Name two reasons.

4. Modern CPUs switch at ~100 picoseconds (0.1 ns). How many times faster is a modern CPU transistor than a 1945 vacuum tube? Express your answer as a power of 10.

---

## Part C — Triode Characteristic Curves (Simulation)

Using the **Triode Anatomy** tool:

1. Set grid voltage to −5V. Record plate current.
2. Increase grid voltage in 1V steps from −5V to +2V. Record plate current at each step.
3. Plot your results as a simple table:

| Grid Voltage (V) | Plate Current (mA) |
|------------------|--------------------|
| −5 | ? |
| −4 | ? |
| −3 | ? |
| −2 | ? |
| −1 | ? |
| 0  | ? |
| +1 | ? |
| +2 | ? |

4. At what grid voltage does the tube switch from "effectively OFF" to "effectively ON"? This is the **threshold voltage**.
5. Is the relationship between grid voltage and plate current linear? Describe the shape.

---

## Part D — The Heat Problem

ENIAC consumed 150,000 Watts (150 kW) of power.

1. A typical house uses about 1.5 kW on average. How many houses could ENIAC's power supply run?
2. Virtually all of ENIAC's power was converted to heat. ENIAC occupied 167 m². What was the heat output per square metre? (Express in W/m²)
3. A modern Apple M3 chip runs at about 22W in a 120mm² package. What is its power density in W/mm²? Compare this to ENIAC's W/m².
4. Why does lower power consumption matter beyond just electricity costs? Describe two engineering consequences of high heat in a computing system.

---

## Part E — Written Analysis

1. **The key advance**: In one paragraph, explain what physical property of the vacuum tube made it 1,000× faster than a relay. Be specific about what is moving in each device and why one is faster.

2. **The key limitation**: Why did vacuum tubes eventually have to be replaced? Name the two most important limitations and connect each to a physical property of tubes.

3. **The reliability paradox**: As computers got larger (more tubes), they became more powerful but also less reliable. Explain this trade-off and why it was fundamentally unavoidable with vacuum tube technology.

---

## Rubric

| Part | Points | What we're looking for |
|------|--------|------------------------|
| A1–A5 reliability calculations | 25 | Correct arithmetic with units |
| B1–B4 speed comparison | 20 | Correct ratios and reasoning |
| C characteristic curve | 20 | Correct table, threshold identified, shape described |
| D heat problem | 15 | Correct calculations, two engineering consequences |
| E written analysis | 20 | Precise physical explanations |

**Total: 100 points**

---

## Hints

<details>
<summary>Hint — A2 failure rate</summary>
Rate = total tubes / average lifetime = 17,468 / 2,500 = failures per hour. This assumes all tubes fail at their average lifetime (Poisson approximation).
</details>

<details>
<summary>Hint — B3 why slower than theoretical</summary>
Think about: (1) each operation requires multiple switching cycles, not just one; (2) other bottlenecks like memory access and I/O slow the pipeline.
</details>

<details>
<summary>Hint — D modern chip comparison</summary>
Convert units carefully: ENIAC is W/m², modern chip is W/mm². 1 m² = 1,000,000 mm².
</details>

---

## Solutions

<details>
<summary>Part A Solutions</summary>

1. Ideal: all fail at 2,500 hours → first failure at **2,500 hours** (104 days).

2. Failure rate = 17,468 / 2,500 = **~6.99 ≈ 7 tube failures per hour**

3. Per day (8 hours): 7 × 8 = **~56 tube failures per day**

4. 56 failures × 15 min each = 840 min/day = 14 hours of repair work per day.  
   With an 8-hour shift: 14/8 ≈ **2 technicians needed continuously**  
   (ENIAC actually had 6 technicians for maintenance)

5. 56 failures/day × 250 days × $10/tube = **$140,000/year** just in tube replacement
</details>

<details>
<summary>Part B Solutions</summary>

1. 15ms / 1µs = 15×10⁻³ / 1×10⁻⁶ = **15,000× faster**

2. 3 ops/sec × 15,000 = **45,000 operations/second** (theoretical)

3. Actual was ~5,000/sec because: (1) each arithmetic operation requires many tube switching cycles (a multiply might need 20+ steps); (2) the machine used decimal (not binary) arithmetic with 10-state ring counters, which was slower than pure binary.

4. Tube: 1µs = 10⁻⁶s. Modern: 0.1ns = 10⁻¹⁰s.  
   Speedup = 10⁻⁶ / 10⁻¹⁰ = **10,000× = 10⁴ times faster**
</details>

<details>
<summary>Part D Solutions</summary>

1. 150,000W / 1,500W = **100 houses**

2. 150,000W / 167m² = **~898 W/m²** ≈ 900 W/m²

3. 22W / 120mm² = **0.183 W/mm²** = 183,000 W/m²  
   Modern chip: ~183,000 W/m². ENIAC: ~900 W/m².  
   Modern chip runs at ~200× higher power density than ENIAC — but it's tiny and has a massive heatsink relative to its size.

4. High heat: (1) **requires active cooling** (fans, heat sinks, sometimes liquid cooling), adding cost, size, and failure points; (2) **accelerates component aging** — heat causes thermal stress and electromigration, shortening component lifetimes.
</details>
