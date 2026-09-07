# Module 1.5 — The Transistor: Revolution in a Grain of Sand

---

## The Problem

> ENIAC works. It's fast. But 17,468 tubes, 150kW of power, and a tube failure every few hours is not a scalable path.
>
> Bell Labs in 1945 had a very practical problem: their telephone network used millions of vacuum tube amplifiers in repeater stations along long-distance lines. Each station needed maintenance, cooling, and regular tube replacement. The cost and unreliability were becoming unmanageable.
>
> Bell Labs set up a solid-state physics group with one mission: find a replacement for the vacuum tube. Something smaller, cooler, more reliable. Something that didn't need a glowing hot filament to work.
>
> On December 16, 1947, John Bardeen and Walter Brattain, supervised by William Shockley, made the first working transistor. It was the size of a fingernail and made of germanium. It amplified a signal with no moving parts, no vacuum, and no heater.
>
> It changed everything.

---

## The Story

### What is a Semiconductor?

Recall from Module 1.1: conductors conduct freely, insulators don't conduct. Semiconductors sit in between — and their conductivity can be controlled.

**Silicon** (the element, Si) is the key material. Pure silicon at room temperature is a poor conductor: its four valence electrons form stable covalent bonds with neighbouring atoms, leaving almost no free electrons to carry current.

**Doping** changes this. Adding tiny amounts of impurity atoms alters silicon's conductivity dramatically:

**N-type silicon** (doped with phosphorus or arsenic):
- Phosphorus has 5 valence electrons; silicon needs only 4 to bond
- The extra electron is loosely bound and free to move
- Result: extra free electrons → current carried by negative charges → **N**-type

**P-type silicon** (doped with boron or aluminium):
- Boron has only 3 valence electrons; there's a "hole" where an electron is missing
- Neighbouring electrons can jump into the hole, making it appear to move
- Result: current carried by moving holes (positive charges) → **P**-type

---

### The P-N Junction: The Diode

Put N-type and P-type silicon in contact. At the junction:
- Free electrons from the N-side diffuse across and fill holes on the P-side
- This creates a **depletion region** — a zone with no free carriers, acting as an insulator
- An electric field builds across the junction opposing further diffusion

**Forward bias** (apply + to P-side, − to N-side): the electric field is reduced → carriers flow → current passes.  
**Reverse bias** (apply + to N-side): the field increases → no current flows.

This one-way current is a **diode** — identical function to Fleming's 1904 vacuum diode, but solid-state, small, and durable.

---

### The Bipolar Junction Transistor (BJT)

Add a second junction and you get a transistor. The **NPN transistor** has three layers: N-P-N, with three terminals:

- **Emitter (E)**: the N-region that emits carriers
- **Base (B)**: the thin middle P-region — the control terminal
- **Collector (C)**: the N-region that collects carriers

**How it works:**
1. Apply a small forward-bias voltage to the base-emitter junction (V_BE ≈ 0.6V for silicon)
2. This injects electrons from the emitter into the thin base region
3. Most electrons don't recombine in the thin base — they diffuse across into the strong reverse-biased collector field
4. A small base current (µA range) controls a large collector current (mA range)

**Current gain (β or hFE)**: β = I_C / I_B, typically 50–500.

As a switch:
- Base voltage = 0 → transistor OFF (collector current ≈ 0)
- Base voltage = 0.7V → transistor ON (collector current = V_CC / R_C, limited by load)
- No vacuum needed. No heater. No moving parts.
- Switching time: ~1 nanosecond for early transistors, picoseconds for modern ones.

---

### The MOSFET: The Transistor That Runs the World

The **Metal-Oxide-Semiconductor Field-Effect Transistor (MOSFET)** is the dominant transistor in digital chips today — every CPU, GPU, and memory chip is built from billions of MOSFETs.

Three terminals: **Gate (G)**, **Source (S)**, **Drain (D)**.

An N-channel enhancement-mode MOSFET:
1. A thin layer of silicon dioxide (SiO₂ — glass!) insulates the gate from the silicon
2. Applying voltage to the gate creates an electric field through the oxide
3. This field attracts electrons to the surface of the P-type body, creating an **inversion channel** — a thin conducting path of N-type carriers between source and drain
4. Current flows from drain to source through this channel
5. Remove gate voltage → channel disappears → no current

**Key advantage over BJT for digital logic:**
- Gate is insulated → draws essentially **zero current** (only capacitive charging)
- This means millions of MOSFETs can switch simultaneously without excessive current draw
- Enables the extreme integration density of modern chips

---

### The First Transistor Computer — 1953

The University of Manchester built the first transistor computer in 1953, using 92 point-contact transistors. By 1955, Bell Labs' TRADIC was the first transistor computer to fly in an aircraft.

IBM's first fully transistorized mainframe, the 7090 (1959), replaced the vacuum-tube IBM 709:
- 50× faster
- Smaller
- Used far less power
- Far more reliable

By 1960, vacuum tube computers were obsolete for general computing.

---

### Why Transistors Beat Tubes

| Property | Vacuum Tube | BJT Transistor | MOSFET |
|----------|-------------|----------------|--------|
| Size | ~3 cm | ~1 cm (discrete) | nm scale |
| Power per switch | 1–5 W | 0.01–0.1 W | Picowatts |
| Switching speed | ~1 µs | ~1 ns | <0.1 ns |
| Needs heater | Yes (5–12V) | No | No |
| Fragility | Glass — fragile | Robust | Robust |
| Lifespan | 1,000–10,000 hrs | 10⁹ cycles+ | 10¹²+ cycles |
| Control current | Small (mA) | Small (µA) | Near zero |
| Works at room temp | No (needs heat) | Yes | Yes |

The transistor didn't just replace the tube — it enabled a density of switching that tubes could never approach. You simply cannot pack 10 billion vacuum tubes onto a chip the size of a fingernail.

---

## The Concept: Semiconductor Physics Summary

```
Pure silicon → poor conductor (all electrons in bonds)
    ↓ add phosphorus (N-type)
N-type silicon → free electrons, good conductor
    ↓ add boron (P-type)
P-type silicon → holes act as positive carriers

P-N junction → diode (one-way current)
N-P-N sandwich → BJT transistor (current amplifier/switch)
Gate over P-type + SiO₂ insulator → MOSFET (voltage-controlled switch)

Key operation: small gate/base signal → large drain/collector current
This is amplification. In digital mode: fully off or fully on = binary switch.
```

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

Three tools:

**Tool 1 — P-N Junction Explorer**
- See N-type and P-type silicon side by side
- Slide the bias voltage from reverse to forward
- Watch the depletion region shrink and current flow

**Tool 2 — BJT Switch**
- Adjust base voltage from 0 to 1V
- Watch the transistor switch from cut-off to saturation
- See the current gain live: I_C = β × I_B

**Tool 3 — MOSFET Switch**
- Adjust gate voltage from 0 to 5V
- Watch the inversion channel form and disappear
- Compare power consumption to the BJT and vacuum tube

---

## Going Deeper

The transistor won the 1956 Nobel Prize in Physics for Bardeen, Brattain, and Shockley. Shockley went on to found Shockley Semiconductor in Palo Alto, California. Eight of his employees left to found Fairchild Semiconductor — and later Intel. The neighbourhood became known as Silicon Valley.

The BJT has largely been replaced by the MOSFET for digital logic because of the zero gate current advantage. But BJTs are still used in analog circuits, RF amplifiers, and applications requiring precise current control. Your phone's amplifier chain likely uses BJTs.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Calculate transistor switching power vs tubes, use the MOSFET simulator to find the threshold voltage, and trace how the transistor enabled integrated circuits.
