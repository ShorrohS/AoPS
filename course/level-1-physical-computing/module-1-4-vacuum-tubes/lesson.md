# Module 1.4 — Vacuum Tubes: Faster Switching

---

## The Problem

> Relay computers work. The logic is sound. The Z3 runs. The Mark I calculates.
>
> But a relay takes 5–50 milliseconds to switch — 100 to 1,000 operations per second at best. The US military needed firing tables for hundreds of artillery configurations, each requiring thousands of trajectory calculations. At relay speeds, one complete firing table took days.
>
> The question was brutally practical: **can we switch faster without moving any metal?**
>
> The answer already existed in every radio receiver in the world — a glass tube with no moving parts that could switch a million times per second. The vacuum tube.

---

## The Story

### The Edison Effect — 1883

Thomas Edison, experimenting with his lightbulb in 1883, noticed something odd: a small current flowed between the hot filament and a metal plate sealed inside the bulb even though they weren't touching. He had no explanation, patented it as a curiosity, and moved on. It became known as the "Edison effect."

The explanation: **electrons were boiling off the hot filament** and drifting through the vacuum to the metal plate. This is **thermionic emission** — heat gives surface electrons enough energy to escape the metal.

### Fleming's Diode — 1904

British physicist John Ambrose Fleming connected the dots in 1904. If the plate is positive, emitted electrons (negative charge) are attracted to it — current flows. If the plate is negative, electrons are repelled — no current flows.

This one-way current flow made Fleming's **diode** perfect for detecting radio waves (rectifying the alternating signal into a detectable direct current). But a diode is not an amplifier and not a switch — it has no control input.

### De Forest's Triode — 1906

Lee de Forest added a third element in 1906: a wire mesh between cathode and plate called the **grid**. This created the **triode** — the device that changed everything.

**How a triode works:**

```
CATHODE (heated) → emits electrons → [GRID controls flow] → PLATE collects current
```

- Apply **negative voltage to grid**: repels electrons → almost no plate current → tube is **OFF**
- Apply **zero or positive voltage to grid**: electrons flow freely → large plate current → tube is **ON**
- The grid transition between these states takes **microseconds**, not milliseconds

A small voltage change on the grid produces a large current change at the plate — this is **amplification**. The ratio of plate voltage swing to grid voltage swing is the **amplification factor (µ)**, typically 20–100.

As a switch: the tube is either saturated (full current, ON=1) or cut off (no current, OFF=0). No moving parts. No mechanical wear. Switching time: ~1 microsecond.

### ENIAC — 18,000 Tubes, 1945

The Electronic Numerical Integrator and Computer (ENIAC) was the first general-purpose electronic computer, completed in 1945 at the University of Pennsylvania.

| Specification | Value |
|--------------|-------|
| Vacuum tubes | 17,468 |
| Resistors | 70,000 |
| Weight | 27,000 kg |
| Power | 150 kW |
| Floor space | 167 m² |
| Speed | ~5,000 additions/second |
| Cost (1945) | ~$400,000 |

ENIAC was **1,000× faster than the Mark I**. Calculations that took the relay-based Mark I days took ENIAC minutes.

**The reliability problem**: With 17,468 tubes, one failed every few hours on average. A team of operators patrolled ENIAC continuously, replacing burned-out tubes. Running a long computation without failure required luck. This fragility was the tube's fundamental limitation — and the motivation for the transistor.

---

## The Concept: Thermionic Emission and Electron Control

**Why do electrons leave the cathode?**

In a metal, outermost electrons are only loosely bound. At room temperature, they don't have enough energy to escape. But heating the metal to ~1000°C gives electrons enough thermal energy to overcome the surface barrier — they literally boil off. This is **thermionic emission**.

**Why does the grid control the current?**

The grid is a mesh of fine wire sitting in the electron stream between cathode and plate. It creates an electric field:

- Negative grid → field points away from plate → electrons decelerate → most turn back → low current
- Positive grid → field points toward plate → electrons accelerate → all reach plate → high current

The grid needs only millivolts to milliamps to exert this control — while the plate circuit can handle volts and amps. **Small control energy, large output energy: this is amplification.**

**Why vacuum?**

Electrons scatter off air molecules. At atmospheric pressure, an electron travels only nanometres before colliding. A vacuum of 10⁻⁶ torr or better lets electrons travel centimetres without collision — essential for cathode-to-plate transit.

---

## Tube vs Relay: The Scorecard

| Property | Relay | Vacuum Tube | Winner |
|----------|-------|-------------|--------|
| Switching speed | 5–50 ms | 0.1–1 µs | Tube (×10,000) |
| Moving parts | Yes | None | Tube |
| Power per switch | ~0.1 W | 1–5 W | Relay |
| Size | ~5 cm | ~3–8 cm | Roughly equal |
| Lifespan | Millions of cycles | 1,000–10,000 hrs | Relay |
| Fragility | Robust | Glass — fragile | Relay |
| Heat generated | Low | Very high | Relay |
| Control isolation | Complete | Partial | Relay |

The tube wins on speed decisively. It loses on power, heat, and reliability. This is precisely why it was replaced by the transistor — which kept the speed while fixing the other problems.

---

## The Williams Tube — First Electronic Memory, 1946

A key unsolved problem in early computers was memory. Paper tape and punch cards were slow. The Williams tube (1946, Manchester) used a cathode ray tube — normally a display device — as memory:

- Write a 1: fire the electron beam at a spot → leaves a positive charge on the phosphor
- Write a 0: don't fire (or fire differently) → no charge
- Read: scan the spot with a low-energy beam → the charge either absorbs or reflects the scan → detect the difference

A Williams tube held ~1,024 bits. Manchester's Small-Scale Experimental Machine (Baby), the first stored-program computer, ran its first program on June 21, 1948, using Williams tubes for memory.

This connects directly to Module 1.2's self-latching relay: the Williams tube was an electronic latch — state stored as charge, reading and writing using the same electron beam that Hollerith's pins had done with holes in cards.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

The simulation has three tools:

**Tool 1 — Triode Anatomy**
- Adjust the cathode temperature (heater current)
- Adjust the grid voltage (negative = cut off, positive = saturated)
- Watch the electron cloud density change
- See plate current on the output meter
- The characteristic curves (plate current vs grid voltage) plot live

**Tool 2 — Tube as Switch**
- Set grid voltage to cut-off (−5V) or saturation (0V)
- See switching between ON and OFF states
- Compare switching time to a relay (animated side-by-side)

**Tool 3 — ENIAC Scale Visualizer**
- See 17,468 tubes represented as a grid
- Click "Simulate failure rate" — random tubes fail over simulated time
- Watch how quickly the machine would go down without maintenance
- See how many tube-swaps per day were needed

---

## Going Deeper

The triode was so valuable that AT&T's Bell Labs spent years trying to replace it with something smaller and more reliable. The result, in 1947, was the transistor (Module 1.5). Ironically, the transistor was invented partly because Bell needed millions of tubes for its telephone network, and keeping them all working was becoming impossible.

The vacuum tube didn't disappear entirely. **Magnetrons** (high-power microwave tubes) are still in every microwave oven. **Klystrons** are used in particle accelerators and radar. **Traveling-wave tubes** amplify signals in satellites. For extreme power and frequency applications, tubes still outperform transistors.

And audiophiles still swear by tube amplifiers — the "warm" sound is a real phenomenon caused by the even-order harmonic distortion tubes produce, which many listeners find more pleasant than the odd-order distortion of transistor amplifiers.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Calculate ENIAC's tube failure statistics, compare relay vs tube switching speeds with real numbers, and use the triode simulator to map out a characteristic curve.
