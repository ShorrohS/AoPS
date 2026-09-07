# Challenge 1.1 — Ohm's Law and Circuit Basics

**Type:** Calculation + simulation observation + written explanation  
**Estimated time:** 25–35 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Ohm's Law Calculations

Solve each problem. Show your working. Use `V = I × R`.

1. A 9V battery is connected to a 180Ω resistor. What current flows?

2. A circuit carries 50mA of current through a 220Ω resistor. What is the voltage across the resistor?

3. A 12V power supply produces 0.5A of current. What is the resistance of the load?

4. An LED needs exactly 20mA to operate safely. You have a 5V supply. What resistor value do you need in series with the LED? *(Assume the LED itself drops 2V, so the resistor must handle 3V.)*

5. A resistor dissipates 0.5W of power when 100mA flows through it. What is its resistance? *(Hint: P = I² × R)*

---

## Part B — Series vs Parallel (Simulation)

Open the simulation and use the **Series vs Parallel** tool.

**Series experiment:**
1. Start with one bulb — note its brightness (call it "100%")
2. Add a second identical bulb in series — how does brightness change?
3. Add a third — what happens?
4. Now open (break) the middle bulb — what happens to the others?

Record your observations for each step.

**Parallel experiment:**
1. Start with one bulb in parallel — brightness at "100%"
2. Add a second bulb in parallel — how does each bulb's brightness change?
3. Add a third — what happens to each?
4. Now open the middle bulb — what happens to the others?

**Questions:**
5. Why does each bulb get *dimmer* when you add more in series, but *stays the same* when you add more in parallel?
6. Why do houses use parallel wiring instead of series wiring? Answer in terms of what you observed.

---

## Part C — Circuit Design

Using the **Circuit Sandbox**, build and describe:

1. A circuit with a 9V battery, a switch, and a bulb. Describe what happens when you open and close the switch.

2. A circuit with two switches where **both** must be closed for the bulb to light. Draw the circuit topology (series or parallel switches?) and explain why.

3. A circuit where **either** switch can light the bulb independently. Draw the topology and explain.

*(Note: You'll build these exact circuits as logic gates in Module 1.3 — you're previewing AND and OR logic right now.)*

---

## Part D — The Semiconductor Preview

Answer in writing (2–3 sentences each):

1. A material has a resistance of 10,000Ω normally, but only 100Ω when a small voltage is applied to a control terminal. Is this more useful as a wire, an insulator, or a switch? Explain.

2. This is exactly what a transistor does. In terms of Ohm's Law, explain what a transistor is doing when it "switches on" — what quantity is changing, and what effect does that have on current flow?

---

## Rubric

| Part | Points | What we're looking for |
|------|--------|------------------------|
| A1–A5 calculations | 30 | Correct formula use, working shown, units |
| B series/parallel observations | 20 | Accurate descriptions of brightness changes |
| B5–B6 explanations | 15 | Correct reasoning (V splits in series, constant in parallel) |
| C circuit designs | 20 | Correct topologies described/built |
| D semiconductor preview | 15 | Correct transistor concept in Ohm's Law terms |

**Total: 100 points**

---

## Hints

<details>
<summary>Hint — A4 (LED resistor)</summary>
The resistor drops 3V (5V supply − 2V LED). Current must be 0.02A.
R = V/I = 3/0.02 = ?
</details>

<details>
<summary>Hint — A5 (power formula)</summary>
P = I²×R → R = P/I² = 0.5 / (0.1)² = ?
</details>

<details>
<summary>Hint — B5 series brightness</summary>
In series, the same current flows through all bulbs, but the voltage is divided. Each bulb gets less voltage → less power → dimmer.
</details>

<details>
<summary>Hint — C2 (both switches)</summary>
If both must be closed for current to flow, the switches must be in series — current has to pass through both.
</details>

---

## Solutions

<details>
<summary>Part A Solutions</summary>

1. `I = V/R = 9/180 = 0.05A = 50mA`
2. `V = I×R = 0.05 × 220 = 11V`
3. `R = V/I = 12/0.5 = 24Ω`
4. `R = V/I = 3/0.02 = 150Ω`
5. `R = P/I² = 0.5/(0.1²) = 0.5/0.01 = 50Ω`
</details>

<details>
<summary>Part B Solutions</summary>

**Series:** Each added bulb splits the available voltage further. Two identical bulbs in series each get half the voltage → half the power → noticeably dimmer. Three bulbs get one-third each. Breaking one bulb opens the circuit → all go dark.

**Parallel:** Each bulb is connected directly across the full battery voltage. Adding more bulbs doesn't change voltage across any individual bulb → brightness unchanged. Breaking one bulb only opens that branch → others stay at full brightness.

**B5:** Series divides voltage; parallel maintains full voltage for each component.  
**B6:** Houses use parallel so each outlet/appliance gets the full 120V, and one appliance failing doesn't cut power to everything else.
</details>

<details>
<summary>Part D Solutions</summary>

1. A material whose resistance changes dramatically with a control signal is most useful as a **switch** — it can be in a high-resistance (OFF) state or a low-resistance (ON) state, controlled by an external signal. This is far more useful than a fixed wire or insulator.

2. When a transistor switches on, its **resistance drops dramatically** (from thousands of ohms to near zero). By Ohm's Law (I = V/R), when R drops while V stays roughly constant, current spikes — allowing a large current to flow through the transistor's main terminals. The transistor acts as a resistance-controlled valve: a tiny control voltage sets R, which determines how much current flows.
</details>
