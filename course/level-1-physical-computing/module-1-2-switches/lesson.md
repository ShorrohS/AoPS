# Module 1.2 — Switches: The Atom of Computing

---

## The Problem

> We now know electricity flows through circuits and obeys Ohm's Law. We know a switch opens or closes a circuit. Simple enough.
>
> But here is the question that changes everything:
>
> **What if the switch itself is controlled by electricity — not by a human hand?**
>
> If a tiny electrical signal can open and close a much larger circuit, you have a device that can make decisions automatically. You have a device that can respond to one electrical condition and change another. You have, in principle, the ability to build any logical operation from pure electricity.
>
> That single idea — the electrically-controlled switch — is the atom from which all computing is built.

---

## The Story

### The Telegraph and the Relay — 1837

Samuel Morse's telegraph (1837) sent electrical pulses down a wire to ring a bell at the other end. But there was a problem: over long distances, the signal weakened. After a few hundred kilometres, it was too faint to ring the bell.

The solution was a **relay station**: a box placed along the wire that used the weak incoming signal to switch a fresh, strong local battery into the line. The weak signal didn't drive the bell directly — it controlled a switch that let a strong local current drive the next segment.

This device was called a **relay** because it "relayed" the signal forward. And it was the first electrically-controlled switch.

**How a relay works:**

1. A weak current flows through a coil of wire wrapped around an iron core
2. The coil becomes an **electromagnet**
3. The electromagnet attracts a metal arm (the **armature**)
4. The armature moves, closing (or opening) a separate set of electrical contacts
5. Those contacts switch a completely separate circuit — which can carry much more current

The key insight: **the control circuit and the switched circuit are electrically isolated**. A tiny signal (5mA) can switch a circuit carrying amperes. The relay is an electrical amplifier of control.

---

### Binary Is the Natural Language of Switches

A switch has exactly two stable states:
- **Closed** (contacts touching) — current flows — call this **1**
- **Open** (contacts separated) — no current flows — call this **0**

There is no "half-closed" switch. There is no "37% closed." A switch is binary by nature.

This is why digital computing uses binary — not because binary is mathematically elegant (though it is), but because **the physical devices we use to build computers have exactly two stable states**. We could have built computers around three-state devices (ternary logic), and some researchers have tried. But binary won because every switch ever made — mechanical, relay, vacuum tube, transistor — naturally has two states.

The connection from Module 0.3 completes here: Jacquard's card had hole (1) or no hole (0). Hollerith's card had hole (electrical contact) or no hole (blocked). Relay contacts are closed (1) or open (0). Transistors are on (1) or off (0). The binary digit — the bit — is the universal language of switching.

---

### The Telegraph's Hidden Contribution

The telegraph didn't just send messages. It established the entire vocabulary of digital communication:

| Telegraph concept | Modern computing equivalent |
|------------------|-----------------------------|
| Dot / dash pulse | Bit (0 / 1) |
| Start / stop bits | Framing in serial communication |
| Relay amplification | Signal regeneration / buffering |
| Code (Morse) | Encoding (ASCII, Unicode) |
| Transmission line | Network cable / optical fibre |
| Repeater station | Network router / amplifier |

Morse code is, literally, a binary encoding: each letter is a sequence of short pulses (dots = 0) and long pulses (dashes = 1). Telegraph operators were the first data encoders.

---

### Relay Characteristics

Understanding what a relay can and cannot do sets up the entire story of why vacuum tubes and transistors were needed.

**What relays do well:**
- Electrically isolate control from output (safety, noise immunity)
- Switch high currents with tiny control signals
- Physically robust — relay contacts can carry 10A+
- Visible and audible (click!) — easy to debug

**What relays do poorly:**
- **Speed**: A relay's armature is a mechanical part. It takes 5–50 milliseconds to move. That limits switching to ~100–1000 times per second.
- **Size**: A relay is centimetres long — you can't pack many of them together
- **Power**: The electromagnet consumes power continuously while held closed
- **Wear**: Mechanical contacts eventually erode — relays have a finite lifespan

The first electromechanical computers — Zuse's Z3 (1941), Harvard Mark I (1944) — used relays. The Z3 had 2,600 relays and could do about 3 additions per second. ENIAC (1945), with vacuum tubes, could do 5,000 additions per second. Same logic, 1,000× faster.

---

### The Relay as a Binary Memory

Here's something surprising: a relay can remember a state. Consider this circuit:

1. Press button A → relay closes → contacts latch (hold) closed
2. Release button A → relay stays closed (the latch current flows through its own contacts)
3. Only pressing a separate "reset" button opens the circuit

This is called **self-latching** — a relay that holds its own state. It's the first mechanical implementation of a **flip-flop**: a device with two stable states that can be set and reset. This is the fundamental memory cell. Every RAM bit in every computer is a more sophisticated version of this circuit.

---

### From Relay to Every Switch That Followed

The relay established the template that every subsequent switching technology follows:

```
Control input  →  [switching device]  →  Output circuit

Relay:         Control coil current   →  Armature movement    →  Contact closure
Vacuum tube:   Grid voltage           →  Electron stream      →  Plate current
Transistor:    Base/gate current      →  Semiconductor state  →  Collector/drain current
```

Same structure. Shrinking size. Increasing speed. Decreasing power. This is the entire story of Level 1.

---

## The Concept: The Switch as a Logic Element

Once you have an electrically-controlled switch, you can build logic:

**NOT (Inverter)**: Wire a relay so that the contacts are **normally closed** (touching when no current flows). Apply a control signal → electromagnet pulls armature → contacts open → output turns OFF. The input being ON makes the output be OFF. That's NOT.

**AND**: Wire two relays in **series** on the output circuit. Both electromagnets must be energised for current to flow through both contact sets. Both inputs must be 1 for the output to be 1. That's AND.

**OR**: Wire two relays in **parallel** on the output circuit. Either electromagnet closes its contacts → current flows. Either input being 1 produces output 1. That's OR.

You've seen this before in Module 1.1's challenge — series switches give AND behaviour, parallel switches give OR behaviour. The same topology, now driven electrically rather than manually.

These three operations — AND, OR, NOT — are sufficient to build any logic circuit that exists. This was proven by George Boole in 1854 and connected to circuits by Claude Shannon in 1937. You will build them in Module 1.3.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

The simulation has three tools:

**Tool 1 — Relay Anatomy**
- An interactive cross-section of a relay
- Slide the control current from 0 to 100%
- Watch the electromagnet energise, the armature move, and the contacts close
- See the control circuit and output circuit separately coloured

**Tool 2 — Self-Latching Relay**
- Two buttons: SET and RESET
- Press SET → relay latches (holds state even after releasing)
- Press RESET → relay releases
- This is your first 1-bit memory cell

**Tool 3 — Switch Logic Preview**
- Three circuits: NOT, AND, OR — each built from relay symbols
- Toggle the inputs; watch the output respond
- Truth tables fill automatically as you test each combination

**What to observe:**
- What is the minimum control current needed to close the relay?
- After latching, what happens if you remove all input signals?
- Can you find all 4 rows of the AND truth table by toggling the inputs?

---

## Going Deeper

The Harvard Mark I (1944) had 765,000 components and 3,000+ relays. It was 15 metres long and weighed 4,500 kg. Its operators could hear it computing — a rhythmic clicking of thousands of relays. Grace Hopper, one of its first programmers, found a moth stuck in a relay causing a malfunction. She taped it into the logbook with the note: "First actual case of bug being found." The term "debugging" comes from this literal event.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Wire up AND, OR, and NOT logic using the relay simulator. Fill in complete truth tables. Then design a relay circuit that implements XOR (either input but not both) and explain how it works.
