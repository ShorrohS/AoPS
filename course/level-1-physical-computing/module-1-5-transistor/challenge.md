# Challenge 1.5 — The Transistor

**Type:** Calculation + simulation + written analysis  
**Estimated time:** 35–45 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Power Calculations

1. A vacuum tube consumes 2.5W when switched ON. A BJT transistor consumes 50mW when ON. How many times less power does the transistor use?

2. ENIAC had 17,468 tubes at ~2.5W each. A transistor equivalent with the same number of switches at 50mW each would consume how much power? Compare to ENIAC's 150kW.

3. A modern MOSFET in a CPU switches at a power of 1 picowatt (10⁻¹² W) per switching event. A CPU runs at 3 GHz (3×10⁹ switches per second) with 10 billion transistors switching simultaneously on average. Calculate total dynamic power in Watts. Does this match real CPU power ratings (~10–100W)?

4. If you could replace all 17,468 ENIAC tubes with modern MOSFETs running at the same 5,000 operations/second, what would the total power be? How does this compare to a modern LED light bulb (≈10W)?

---

## Part B — The P-N Junction (Simulation)

Using the **P-N Junction** tool:

1. Set bias to 0V (no bias). Describe the depletion region — where is it, what is it made of?
2. Set bias to −5V (reverse bias). What happens to the depletion region? Does current flow?
3. Increase forward bias from 0V to 1V in 0.1V steps. At what voltage does current start flowing significantly? This is the **forward voltage drop** (V_f).
4. Why does a silicon diode have V_f ≈ 0.6–0.7V but a germanium diode has V_f ≈ 0.2–0.3V? (Hint: think about the energy needed to push carriers across the junction — this depends on the semiconductor's band gap.)

---

## Part C — BJT Switch (Simulation)

Using the **BJT Switch** tool:

1. At base voltage = 0V, what is the collector current?
2. Increase base voltage to 0.6V. What happens? What is the collector current?
3. Increase to 0.7V. What is the current gain (β = I_C / I_B)?
4. At what base voltage is the transistor "fully ON" (saturated)?
5. This transistor has β = 100. If the base current is 50µA, what is the collector current?
6. Compare: the base current that turns this transistor on (µA range) vs the grid current in a vacuum tube (~mA range). What does this difference mean for circuit design?

---

## Part D — The Integration Leap

In 1958, Jack Kilby at Texas Instruments built the first **integrated circuit**: multiple transistors, resistors, and capacitors all fabricated on a single piece of semiconductor.

1. Before ICs, each transistor was a separate component wired by hand. A computer with 1,000 transistors needed 1,000 separate hand-soldered connections. What are two reliability problems this creates?

2. An IC puts all connections on the chip itself using deposited metal traces. Why does this dramatically improve reliability?

3. The first IC had 1 transistor + a few passive components. The Intel 4004 (1971) had 2,300. An iPhone's M3 chip (2023) has ~19 billion. This is a factor of ~8 million in 52 years. Assuming Moore's Law (doubling every 2 years), verify: does 2^(52/2) ≈ 8 million? Show the calculation.

---

## Part E — Written Analysis

1. **The key physical difference**: A vacuum tube uses thermionic emission (hot cathode → free electrons in vacuum). A transistor uses semiconductor doping. What does this difference mean for: (a) operating temperature requirements, (b) startup time, (c) mechanical fragility?

2. **Why MOSFET dominates digital**: A BJT requires a base current to stay ON. A MOSFET requires only a voltage (zero current). Explain why zero gate current is crucial when you have 10 billion transistors on one chip.

3. **Silicon Valley's origin**: Shockley's employees left to found Fairchild, which spun out Intel, AMD, and dozens of others — all in one region. Why did this geographic concentration happen, and why does it still matter today?

---

## Rubric

| Part | Points | What we're looking for |
|------|--------|------------------------|
| A power calculations | 25 | Correct arithmetic, units, comparisons |
| B P-N junction | 15 | Correct observations, V_f identified |
| C BJT switch | 20 | Correct current gain, saturation identified |
| D integration leap | 20 | Correct IC reliability reasoning, Moore's Law calc |
| E written analysis | 20 | Precise physical reasoning |

**Total: 100 points**

---

## Hints

<details>
<summary>Hint — A3 dynamic power</summary>
P = power_per_switch × switches_per_second × num_transistors  
= 10⁻¹² W × 3×10⁹ × 10¹⁰ = 30W
Yes, this matches real CPU power consumption!
</details>

<details>
<summary>Hint — D3 Moore's Law check</summary>
52 years / 2 years per doubling = 26 doublings.
2²⁶ = 67,108,864 ≈ 67 million. More than 8 million — because the doubling rate was sometimes faster than 2 years in early decades.
</details>

---

## Solutions

<details>
<summary>Part A Solutions</summary>

1. 2.5W / 0.05W = **50× less power**

2. 17,468 × 0.05W = **873.4W ≈ 0.87kW** vs ENIAC's 150kW. **172× lower power**.

3. P = 10⁻¹² × 3×10⁹ × 10¹⁰ = **30W**. Yes — Apple M1/M3 chips consume 15–40W. Perfect match.

4. 17,468 × 10⁻¹² W × (5000 ops × ~5 switches/op) = ~4.4×10⁻⁷ W = **0.00044mW**.  
   Compared to a 10W LED bulb: the MOSFET version uses 23 billion times less power. A modern LED bulb uses infinitely more power than an equivalent MOSFET circuit.
</details>

<details>
<summary>Part C5</summary>
I_C = β × I_B = 100 × 50µA = **5,000µA = 5mA**
</details>
