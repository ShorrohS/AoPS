# Level 1 — Physical Computing: From Electricity to Logic

> *The gear gave way to the electron. Everything else followed.*

---

## What This Level Is About

Level 0 showed that humans needed machines to compute and that information could be stored in physical media — holes in cards, gear positions, ink on paper. But gears are slow, heavy, and wear out. The real revolution came when we replaced mechanical motion with **electrical switching**.

This level traces that journey — from the basic physics of electricity, through telegraph relays and vacuum tubes, to the transistor and the integrated circuit. Every step reduces the physical size of a "switch" while increasing its speed by orders of magnitude.

By the end of Level 1, you will understand:
- What electricity is and how it flows through circuits
- Why a switch is the fundamental atom of all computation
- How relay circuits implement logical decisions (AND, OR, NOT)
- Why vacuum tubes replaced relays, and why transistors replaced vacuum tubes
- What Moore's Law is, why it held for 50 years, and where it's going

---

## Modules

| Module | Title | Core Idea |
|--------|-------|-----------|
| [1.1](./module-1-1-electricity/lesson.md) | What is Electricity? | Voltage, current, resistance — the water analogy |
| [1.2](./module-1-2-switches/lesson.md) | Switches: The Atom of Computing | On/off is binary; relays are electrical switches |
| [1.3](./module-1-3-relay-logic/lesson.md) | Relay Logic: Building Decisions from Metal | AND, OR, NOT from physical relays |
| [1.4](./module-1-4-vacuum-tubes/lesson.md) | Vacuum Tubes: Faster Switching | Electrons in glass replace mechanical contacts |
| [1.5](./module-1-5-transistor/lesson.md) | The Transistor: Revolution in a Grain of Sand | Semiconductor switching at atomic scale |
| [1.6](./module-1-6-moores-law/lesson.md) | From Transistors to Chips: Moore's Law | Doubling density, halving cost, every two years |

---

## The Speed Ladder

One of the most important ideas in this level is **switching speed** — how fast a device can go from OFF to ON and back. Watch this number change as you progress:

| Technology | Era | Switching Speed | Typical Size |
|-----------|-----|----------------|--------------|
| Mechanical relay | 1840s | ~10 ms (100 ops/sec) | 5 cm |
| Vacuum triode | 1906 | ~1 µs (1M ops/sec) | 3 cm |
| Discrete transistor | 1947 | ~1 ns (1G ops/sec) | 1 cm |
| Integrated circuit transistor | 1958 | ~0.1 ns | 100 µm |
| Modern MOSFET (2024) | today | ~0.01 ns (100G ops/sec) | 3–5 nm |

Each row in this table represents an improvement of roughly **1000×** in speed and **1000×** in size reduction. Understanding *why* each leap happened is the entire story of Level 1.

---

## Prerequisites

**Level 0 — Before Computers** (complete).

You should understand:
- Why mechanical computation was needed
- What "stored instructions" means
- How information can be encoded as physical state (holes, gear positions)

---

## What Comes Next

**Level 2 — Digital Foundations** takes the transistor switches from Level 1 and combines them into logic gates (AND, OR, NOT), then combines those gates into circuits that can add, store, and decide. The transistor is the atom; Level 2 builds the molecules.
