# Module 1.1 — What is Electricity? (Only What We Need)

---

## The Problem

> Gears work. The Pascaline proved it. The Difference Engine proved it. But gears have a hard limit: to go faster, you need to move mass faster. Moving mass requires force. Force creates friction, heat, and wear.
>
> By 1900, the fastest mechanical calculators could do a few operations per second. The 1890 census used Hollerith's electromechanical machines — the mechanical counters still moved physical gear wheels, just driven by electricity rather than hand-cranking.
>
> To reach a million operations per second — let alone a billion — you need something that has almost no mass to move. You need **electrons**.

Before we can understand how transistors and circuits work, we need to understand what electricity actually is — not as a mysterious force, but as the movement of charged particles through a material, governed by three simple relationships.

---

## The Story

### What Is Electricity?

Everything around you is made of atoms. Atoms have a nucleus (protons and neutrons) surrounded by electrons in orbits. Electrons carry a **negative charge**; protons carry a **positive charge**.

In most materials, electrons are tightly bound to their atoms. But in **conductors** — metals like copper, gold, and silver — the outermost electrons are loosely bound. They can drift from atom to atom through the material.

**Electric current** is the flow of these loosely-bound electrons through a conductor. Think of a copper wire as a tube packed with electrons. Push on one end (apply a voltage), and electrons drift through the tube from one end to the other.

One important convention: by historical accident, electric current is defined as flowing **from positive to negative** — the opposite direction from electron flow. We stick with this convention because it's universal, but always remember electrons actually move the other way.

---

### The Three Quantities: A Water Analogy

The best way to build intuition about electricity is through water flowing in pipes.

**Voltage (V) — Water Pressure**

Voltage is the "pressure" that pushes electrons through a circuit. A higher voltage means a stronger push. Measured in **Volts (V)**.

- A AA battery: 1.5V
- A phone charger: 5V
- A household outlet: 120V (US) / 230V (EU)
- A lightning bolt: ~300,000,000V

No voltage → no flow. Voltage is always measured *between two points* — it's a difference in electrical potential, like measuring the height difference between two water tanks.

**Current (I) — Water Flow Rate**

Current is how many electrons actually flow past a point per second. Measured in **Amperes (A)** — 1 Amp = 6.24 × 10¹⁸ electrons per second passing a point.

- An LED: ~0.02A (20 milliamps)
- A phone charging: ~1–2A
- A household circuit: 15–20A
- A lightning bolt: ~30,000A (briefly)

**Resistance (R) — Pipe Narrowness**

Resistance is how much a material opposes the flow of electrons. A narrow pipe resists water flow; a thin wire resists electron flow. Measured in **Ohms (Ω)**.

- A human body (dry): ~100,000 Ω
- A piece of copper wire (1m): ~0.017 Ω
- A 60W light bulb filament: ~240 Ω
- An open circuit (air gap): essentially infinite Ω

---

### Ohm's Law: The Fundamental Relationship

These three quantities are connected by one of the most important equations in physics:

```
V = I × R
```

**Voltage = Current × Resistance**

Rearranged:
- `I = V / R` — more voltage or less resistance → more current
- `R = V / I` — measure voltage and current to find resistance

This single equation predicts the behavior of most simple circuits. Every resistor, every LED, every transistor bias calculation starts here.

**Example:** A 5V battery connected to a 250Ω resistor:
```
I = V / R = 5 / 250 = 0.02A = 20mA
```
That's exactly the right current for a standard LED. This is why resistors are always paired with LEDs.

---

### Open vs Closed Circuits

A circuit needs to be a **complete loop** for current to flow.

- **Closed circuit**: the path from + terminal, through components, back to − terminal is unbroken → current flows
- **Open circuit**: the path is broken somewhere (a switch is open, a wire is cut) → no current flows
- **Short circuit**: the + and − terminals are connected directly with no resistance → enormous current flows, generating heat (dangerous)

A **switch** is simply a device that opens or closes a circuit on demand. When the switch is closed, the circuit is complete and current flows. When it's open, current stops.

This is the key connection to computing: **a switch is a binary device**. Closed = 1. Open = 0. Everything in digital electronics is built from switches.

---

### Series vs Parallel

**Series circuit**: components connected end-to-end in a single path.
- The same current flows through all components
- Voltages add up: `V_total = V1 + V2 + V3`
- Resistances add up: `R_total = R1 + R2 + R3`
- If one component fails (opens), the entire circuit stops (old Christmas lights)

**Parallel circuit**: components connected side-by-side, sharing the same two endpoints.
- The same voltage appears across all components
- Currents add up: `I_total = I1 + I2 + I3`
- Total resistance is *less* than any individual resistor: `1/R_total = 1/R1 + 1/R2 + 1/R3`
- If one component fails, others keep working (modern Christmas lights, house wiring)

---

### Power: The Heat Problem

Power is the rate at which a circuit consumes energy:

```
P = V × I     (also P = I²×R = V²/R)
```

Measured in **Watts (W)**. Every electron pushed through a resistance generates heat. This is why:
- Your phone gets warm while charging
- Early computers (vacuum tube era) required massive cooling systems
- Modern CPUs have heat sinks and fans
- Power consumption is one of the central engineering constraints of chip design

The transistor's dominance over vacuum tubes came partly from power: a vacuum tube might dissipate 1–5 watts; a modern transistor dissipates picowatts (10⁻¹² W). A billion transistors at a picowatt each = 1mW total — manageable.

---

### Conductors, Insulators, and Semiconductors

| Material | Resistance | Examples | Why it matters |
|----------|-----------|----------|----------------|
| Conductor | Very low | Copper, gold, aluminum | Wires, circuit traces |
| Insulator | Very high | Glass, rubber, air | Wire coating, PCB substrate |
| Semiconductor | In between, controllable | Silicon, germanium | Transistors, diodes |

**Semiconductors** are the key. Their resistance can be controlled — made higher or lower — by adding tiny amounts of impurities (a process called **doping**) or by applying a voltage. This controllable resistance is what makes transistors possible.

Pure silicon is a poor conductor. Dope it with phosphorus → extra electrons → **N-type** silicon (carries negative charge). Dope it with boron → electron holes → **P-type** silicon (carries positive charge). Put N-type and P-type together → a **P-N junction** → a diode. Two junctions → a transistor. This is Module 1.5's story.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

The simulation has three interactive tools:

**Tool 1 — Circuit Sandbox**
- Drag a battery, resistors, bulbs, and switches onto the canvas
- Connect components with wires
- Watch current flow animate through the circuit (moving dots = electrons)
- The bulb glows brighter with more current

**Tool 2 — Ohm's Law Calculator**
- Set any two of V, I, R — the third calculates automatically
- Slide voltage up: watch current increase proportionally
- Slide resistance up: watch current decrease

**Tool 3 — Series vs Parallel**
- Pre-built series and parallel circuits
- Open one bulb in each — see which circuit survives

**What to observe:**
- What happens to brightness when you add a second bulb in series?
- What happens to brightness when you add a second bulb in parallel?
- What happens when you short-circuit the battery (connect + to − directly)?

---

## Going Deeper

The water analogy breaks down in one important way: water flow is continuous, but electric current is quantized — it moves in discrete electron jumps. At the scale of circuit design this doesn't matter, but at the scale of individual transistors (where gates are just a few atoms thick), quantum effects become dominant and classical circuit models fail. This is part of why Moore's Law is slowing down (Module 1.6).

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

You'll apply Ohm's Law to calculate circuit values, predict what happens when components are rearranged, and explain the water analogy in your own words.
