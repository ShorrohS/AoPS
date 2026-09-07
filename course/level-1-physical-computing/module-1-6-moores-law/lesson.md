# Module 1.6 — From Transistors to Chips: Moore's Law

---

## The Problem

> The transistor was invented in 1947. It was a breakthrough. But each transistor was still a separate component — you bought them individually, wired them together by hand, soldered connections one at a time.
>
> A computer with 1,000 transistors meant 1,000 separate parts, thousands of hand-soldered joints, and a reliability nightmare (every solder joint could fail). Building a computer with a million transistors by hand was practically impossible.
>
> The question: **can we build the entire circuit — transistors, resistors, connections — all at once on a single piece of silicon?**

The answer came from two people independently in 1958–1959, and it launched the modern world.

---

## The Story

### The Integrated Circuit — 1958

**Jack Kilby** at Texas Instruments built the first working integrated circuit in 1958. Using germanium, he placed a transistor, resistors, and capacitors on a single chip and connected them with fine gold wires. It was messy, but it worked.

**Robert Noyce** at Fairchild Semiconductor independently invented a cleaner approach in 1959: use deposited aluminium traces on top of silicon dioxide insulation to connect components without physical wires. This **planar process** is the foundation of every chip made since.

Both Kilby and Noyce are credited as co-inventors of the IC. Kilby won the Nobel Prize in Physics in 2000 (Noyce had died in 1990).

**Why the IC was revolutionary:**
- All components and connections fabricated simultaneously in one process
- Reliability improved: no hand-soldered joints to fail
- Size: the entire circuit is photolithographically patterned — smaller than any hand assembly
- Cost: manufacturing cost scales with chip area, not with number of components
- The same photomask that makes 1 transistor can make 1 million in the same process step

---

### Moore's Law — 1965

Gordon Moore, co-founder of Fairchild and later Intel, observed in 1965 that the number of transistors on an integrated circuit had been doubling roughly every year since the IC's invention. He predicted this would continue for at least 10 more years.

In 1975 he revised the prediction: doubling every **two years**.

This became **Moore's Law**: *the number of transistors on a chip doubles approximately every two years.*

| Year | Chip | Transistors |
|------|------|-------------|
| 1971 | Intel 4004 | 2,300 |
| 1974 | Intel 8080 | 4,500 |
| 1978 | Intel 8086 | 29,000 |
| 1982 | Intel 286 | 134,000 |
| 1985 | Intel 386 | 275,000 |
| 1989 | Intel 486 | 1,200,000 |
| 1993 | Pentium | 3,100,000 |
| 2000 | Pentium 4 | 42,000,000 |
| 2006 | Core 2 Duo | 291,000,000 |
| 2012 | Ivy Bridge | 1,400,000,000 |
| 2020 | Apple M1 | 16,000,000,000 |
| 2023 | Apple M3 | 25,000,000,000 |
| 2024 | Apple M4 | 28,000,000,000 |

From 2,300 to 28 billion in 53 years. That's a factor of **12 million**.

---

### How Chips Are Made: Photolithography

The magic of ICs is **photolithography** — printing circuit patterns onto silicon using light.

1. **Start with a silicon wafer** — a disc of highly pure silicon, 300mm in diameter
2. **Grow oxide**: heat the wafer to grow a thin layer of SiO₂ on the surface
3. **Apply photoresist**: coat the wafer with a light-sensitive chemical
4. **Expose through a mask**: shine UV light through a photomask (like a film negative) — where light hits, photoresist becomes soluble
5. **Develop**: wash away the exposed photoresist — the pattern remains
6. **Etch or dope**: etch away the exposed oxide, or implant dopant atoms into the exposed silicon
7. **Repeat**: each chip layer requires multiple lithography-etch cycles (modern chips have 100+ layers)
8. **Deposit metal**: aluminium or copper traces connect transistors

The minimum feature size — the width of the smallest line that can be printed — is the **process node** (or technology node). This is the number you see: 90nm, 45nm, 14nm, 7nm, 5nm, 3nm.

**Shrinking the node** by 2× means:
- Each transistor occupies 4× less area (2D shrink)
- 4× more transistors fit on the same chip area
- Transistors are closer together → signals travel shorter distances → faster switching
- Smaller transistors have less capacitance → less energy per switch → lower power

This is the physical mechanism behind Moore's Law: **photolithography precision doubling every ~18 months**.

---

### Why Moore's Law Is Slowing

By the early 2010s, shrinking transistors was running into fundamental physical limits:

**The quantum tunnelling problem**: When a transistor gate is only a few atoms thick, electrons can **quantum tunnel** through the gate oxide even when the transistor is supposed to be OFF. This causes leakage current — the transistor can't fully shut off, wasting power and causing errors. At 2nm, the gate is roughly 10 atoms wide.

**Heat density**: Transistors have always generated heat. Smaller transistors generate less heat each, but you can pack so many more of them that total heat density has hit a ceiling. Most CPUs can't exceed ~100W/cm² without exotic cooling.

**Economic limits**: Each new fab (semiconductor fabrication facility) costs $10–20 billion to build. The number of companies that can afford leading-edge fabs has shrunk to: TSMC, Samsung, Intel. Each process node requires completely new equipment.

**The industry response:**
- **3D stacking**: stack multiple die layers (memory on top of logic) — going vertical instead of lateral
- **Heterogeneous integration**: combine specialized chips (CPU + GPU + memory) in one package
- **New transistor designs**: FinFET (2011), Gate-All-Around (2022) — new 3D transistor geometries instead of flat planar devices
- **Specialized hardware**: GPUs for graphics, TPUs for AI — don't need a general CPU for everything

---

### What Moore's Law Actually Enabled

Moore's Law isn't just an interesting observation. It's the engine behind every major computing development since 1965:

| What changed | Because of Moore's Law |
|--------------|----------------------|
| Personal computers (1980s) | Chips cheap enough for individuals |
| Internet (1990s) | Routers, servers affordable at scale |
| Smartphones (2007+) | PC-power in pocket-size, battery-powered form |
| Social media (2010s) | Data centres with millions of cores |
| Deep learning / AI (2010s+) | GPUs with billions of transistors for matrix math |
| Large language models (2020s) | Trillion-parameter models require trillion-op/sec chips |

Every computer science topic from Level 2 onward exists because transistors got small enough, cheap enough, and fast enough.

---

## The Concept: Exponential Growth

Moore's Law is an **exponential process**: each doubling multiplies the previous value by 2.

Starting at 2,300 (Intel 4004, 1971), doubling every 2 years:
```
2,300 × 2^n where n = years_elapsed / 2

After 52 years (2023): 2,300 × 2^(52/2) = 2,300 × 2^26 = 2,300 × 67,108,864 ≈ 154 billion
```

The M3 chip has 19 billion transistors — roughly in line (the doubling rate has slowed somewhat since 2015).

**The intuition pump**: a checkerboard with grains of rice doubling each square. The first 32 squares fill a bag. The last 32 squares require more rice than has ever been grown on Earth. Moore's Law has been running on the second half of that board for 20 years.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

Three tools:

**Tool 1 — Moore's Law Timeline**
- Interactive log-scale chart of transistor counts 1971–2024
- Hover over any chip to see specs
- Toggle "actual data" vs "ideal Moore's Law" to see where the curve bent

**Tool 2 — Doubling Calculator**
- Enter a start value, doubling period, and number of years
- See the exponential growth plotted
- Explore: what if phones kept getting bigger instead of chips getting smaller?

**Tool 3 — Photolithography Simulator**
- Drag a UV mask over a silicon surface
- Watch the pattern expose, develop, and etch
- Scale the feature size from 10µm (1970s) to 3nm (2022) and see how many transistors fit

---

## Going Deeper

The 2nm process node (in production at TSMC and Samsung in 2024–2025) uses **Gate-All-Around (GAA)** transistors — nanosheet FETs where the gate wraps entirely around a thin ribbon of silicon. This is fundamentally different from the planar MOSFET described in Module 1.5, though the operating principle (voltage-controlled channel) is the same.

Intel's answer is **Intel 18A** (scheduled for 2025), using its own GAA variant called RibbonFET. The competition between TSMC, Samsung, and Intel is now measured in angstroms (tenths of nanometres) — dimensions approaching individual atomic spacings.

---

## Level 1 Capstone

You have now completed Level 1. Before advancing to Level 2, you should be able to answer:

1. What are the three quantities in Ohm's Law and what does each mean physically? (Module 1.1)
2. Why is a switch binary, and why does this connect to digital computing? (Module 1.2)
3. How do relay contacts implement AND, OR, and NOT? (Module 1.3)
4. What physical property makes vacuum tubes 1,000× faster than relays? (Module 1.4)
5. What is the difference between a BJT and a MOSFET, and why does MOSFET dominate digital logic? (Module 1.5)
6. What is Moore's Law, and what physical process drove it for 50 years? (Module 1.6)

If you can answer all six, you are ready for **Level 2: Digital Foundations** — where transistors become logic gates, gates become circuits, and circuits become the building blocks of every processor ever made.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Calculate Moore's Law projections, estimate when physical limits will be hit, and trace the full path from Jacquard's punch card to a modern MOSFET in one continuous narrative.
