# Challenge 1.2 — Relay Logic and Binary Switching

**Type:** Simulation + truth tables + circuit design  
**Estimated time:** 30–40 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Relay Anatomy

Using the **Relay Anatomy** tool:

1. At what control current percentage does the relay close? Record the threshold.
2. Once closed, lower the current slowly. At what percentage does it open again? Is this the same threshold? (This difference is called **hysteresis** — explain in one sentence why it exists mechanically.)
3. Draw a simple diagram of the relay showing: coil, core, armature, normally-open contacts, normally-closed contacts, and the two separate circuits.

---

## Part B — Truth Tables (Simulation)

Using the **Switch Logic Preview** tool, test each gate and fill in the truth tables:

### NOT Gate
| Input A | Output |
|---------|--------|
| 0       | ?      |
| 1       | ?      |

### AND Gate
| Input A | Input B | Output |
|---------|---------|--------|
| 0       | 0       | ?      |
| 0       | 1       | ?      |
| 1       | 0       | ?      |
| 1       | 1       | ?      |

### OR Gate
| Input A | Input B | Output |
|---------|---------|--------|
| 0       | 0       | ?      |
| 0       | 1       | ?      |
| 1       | 0       | ?      |
| 1       | 1       | ?      |

---

## Part C — Self-Latching Memory

Using the **Self-Latching Relay** tool:

1. Press SET. What state is the output? (0 or 1)
2. Release SET. What state is the output now? Why doesn't it return to 0?
3. Press RESET. What state is the output?
4. This circuit has two stable states. In your own words, explain how it "remembers" which button was last pressed.
5. How many bits of information can this circuit store? Justify.

---

## Part D — Design a NAND Gate

A **NAND gate** outputs 0 only when **both** inputs are 1 — it is AND followed by NOT.

1. Draw (or describe in words) a relay circuit that implements NAND using the AND circuit wired through a normally-closed relay contact.
2. Fill in the NAND truth table:

| Input A | Input B | AND output | NAND output (inverted) |
|---------|---------|------------|------------------------|
| 0       | 0       | ?          | ?                      |
| 0       | 1       | ?          | ?                      |
| 1       | 0       | ?          | ?                      |
| 1       | 1       | ?          | ?                      |

3. Why is NAND called a "universal gate"? (Hint: can you build NOT, AND, and OR from NAND alone? You don't need to prove it — just state whether it's true and why it matters for chip design.)

---

## Part E — Speed Analysis

A relay takes 10ms to close and 8ms to open.

1. What is the maximum number of ON/OFF cycles per second (the switching frequency)?
2. Compare to a modern transistor that switches in 0.1 nanoseconds. How many times faster is the transistor?
3. A 1940s relay computer executes 3 additions per second. A modern CPU runs at 3 GHz (3 × 10⁹ cycles/second). Assuming 1 addition ≈ 1 cycle, how many times faster is the modern CPU?
4. If relay computers had continued improving at the same rate as transistor computers (doubling speed every 2 years), what year would we have reached 3 GHz? Show your working.

---

## Rubric

| Part | Points | What we're looking for |
|------|--------|------------------------|
| A — Relay anatomy | 15 | Correct threshold, hysteresis explanation, diagram |
| B — Truth tables | 25 | All 10 entries correct |
| C — Latch memory | 20 | Correct observations, correct "1 bit" justification |
| D — NAND design | 20 | Correct truth table, correct NAND = universal statement |
| E — Speed analysis | 20 | Correct calculations with units shown |

**Total: 100 points**

---

## Hints

<details>
<summary>Hint — Part A hysteresis</summary>
When the armature is already touching the core, the magnetic gap is smaller, so less magnetic force is needed to keep it closed than to initially pull it closed from a distance.
</details>

<details>
<summary>Hint — Part C latch</summary>
The relay's own contacts are wired in parallel with the SET button. Once closed by SET, the relay provides its own holding current path.
</details>

<details>
<summary>Hint — Part E switching frequency</summary>
Frequency = 1 / (close time + open time) = 1 / (0.010 + 0.008)s
</details>

<details>
<summary>Hint — Part E relay-to-CPU speedup</summary>
3 GHz = 3,000,000,000 ops/sec. Relay = 3 ops/sec. Speedup = ?
</details>

---

## Solutions

<details>
<summary>Part B — Truth Tables</summary>

**NOT:** 0→1, 1→0  
**AND:** 00→0, 01→0, 10→0, 11→1  
**OR:** 00→0, 01→1, 10→1, 11→1
</details>

<details>
<summary>Part D — NAND truth table</summary>

| A | B | AND | NAND |
|---|---|-----|------|
| 0 | 0 |  0  |  1   |
| 0 | 1 |  0  |  1   |
| 1 | 0 |  0  |  1   |
| 1 | 1 |  1  |  0   |

NAND is universal because: NOT A = NAND(A,A); A AND B = NOT(NAND(A,B)); A OR B = NAND(NOT A, NOT B). Any logic function can be expressed with only NAND gates. This matters because chip designers only need to implement one type of gate — then combine them.
</details>

<details>
<summary>Part E Solutions</summary>

1. Frequency = 1/(0.010+0.008) = 1/0.018 ≈ **55.6 Hz** (55 on/off cycles per second)

2. Transistor: 0.1 ns = 1×10⁻¹⁰ s per switch. Relay: 0.010 s = 1×10⁻² s.  
   Speedup = 10⁻² / 10⁻¹⁰ = **100,000,000× (100 million times faster)**

3. CPU speedup vs relay computer: 3×10⁹ / 3 = **1,000,000,000× (one billion times faster)**

4. Starting from 3 ops/sec in 1944, doubling every 2 years to reach 3×10⁹:
   3 × 2ⁿ = 3×10⁹ → 2ⁿ = 10⁹ → n = log₂(10⁹) ≈ 30 doublings
   30 doublings × 2 years = 60 years from 1944 = **year 2004**.
   
   Remarkably, this is close to correct! Intel's Pentium 4 hit ~3 GHz in 2002. The relay-to-transistor path did follow roughly this trajectory because Moore's Law governed transistor improvement too. What the relay path lacked was the ability to continue scaling beyond ~1000 Hz before the mechanical limits were hit — transistors had no such physical ceiling for decades.
</details>
