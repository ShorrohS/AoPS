# Module 2.5 — Sequential Circuits: Memory from Gates

---

## The Problem

> The 4-bit adder from Module 2.4 computes the sum of two numbers instantly — as fast as the signals propagate through the gates. Perfect.
>
> Now: what happens after the addition? Where does the result go?
>
> If you wire the output directly to the next operation, the values are gone the moment the inputs change. There is no memory. A computer that can't remember intermediate results can't execute even the simplest program.
>
> You need circuits that **hold a value** — circuits whose output persists even when the input is removed. You need **state**.

State changes everything. A circuit with state is no longer purely combinational — its output depends not only on current inputs but on **history**. This is the distinction between a calculator (combinational) and a computer (sequential).

---

## The Story

### Feedback — The Key Insight

All memory in digital electronics comes from one idea: **feedback**. Route the output of a gate back to its own input. The circuit can now hold a state indefinitely.

Consider two NAND gates cross-coupled:

```
    S ──[NAND]──┬── Q
                │
    R ──[NAND]──┴── Q̄
```

If Q=1 and Q̄=0:
- Top NAND: one input is S, other is Q̄=0. Output Q = NAND(S, 0) = 1 — stable.
- Bottom NAND: one input is R, other is Q=1. Output Q̄ = NAND(R, 1) = NOT R.

Normally S=R=1 (inactive). Then Q̄=0 and Q=1 — stable.
Set S=0: Q becomes 1 (set). Release S: circuit stays Q=1.
Set R=0: Q̄ becomes 1, which feeds back to force Q=0 (reset). Release R: stays at 0.

This is the **SR NAND latch** — the simplest possible 1-bit memory cell. It holds its value indefinitely as long as power is supplied.

---

### The SR Latch

**SR Latch (NOR-based):**

| S | R | Q (next) | Q̄ (next) | Action |
|---|---|----------|-----------|--------|
| 0 | 0 | Q (hold) | Q̄ (hold) | Hold state |
| 0 | 1 | 0        | 1         | Reset |
| 1 | 0 | 1        | 0         | Set |
| 1 | 1 | invalid  | invalid   | Forbidden! |

The forbidden state (S=R=1) forces both outputs to 0, violating the invariant Q≠Q̄. If both inputs then return to 0 simultaneously, the final state is unpredictable — a **race condition**. Real systems must avoid this.

**The SR latch stores 1 bit.** It's the ancestor of every RAM cell in every computer ever built.

---

### The D Latch (Transparent Latch)

The SR latch has the forbidden state problem. The **D latch** solves it with one extra input:

- **D (Data):** the value to store (0 or 1)
- **E (Enable):** when high, output follows D; when low, output is held

Implementation: `S = D AND E`, `R = (NOT D) AND E`

This prevents S=R=1: when E=1, if D=1 then S=1,R=0; if D=0 then S=0,R=1. Never both 1.

**Problem with transparent latches:** when E is high, the output *follows* D continuously — the latch is "transparent." If D is changing (because the output of an adder is rippling), the latch sees every intermediate value. This causes glitches in cascaded circuits.

---

### The D Flip-Flop (Edge-Triggered)

The **D flip-flop** (DFF) solves the transparency problem by only capturing D at the **edge** of a clock signal (either rising edge 0→1 or falling edge 1→0).

Implementation: two D latches in series (master-slave configuration):
- When CLK=0: master latch is transparent, slave is held
- When CLK=1: master is held, slave captures master's output

The net effect: Q updates to D's value at the instant CLK transitions 0→1. After that, Q is held regardless of D changes until the next clock edge.

```
       D ──[master latch]──[slave latch]── Q
                CLK              NOT CLK
```

**Why the edge-triggered flip-flop is the foundation of CPUs:**
- All registers in a CPU are flip-flops
- The clock signal synchronises all flip-flops — they all update at the same moment
- This makes the entire processor operate in lockstep
- Clock frequency = how fast the flip-flops toggle = operations per second

---

### Registers

A **register** is simply N flip-flops connected in parallel, sharing the same clock and enable signals.

- 4 flip-flops → 4-bit register (stores one nibble)
- 8 flip-flops → 8-bit register (byte)
- 64 flip-flops → 64-bit register (modern CPU register width)

A CPU's general-purpose registers (RAX, RBX, etc. in x86-64) are 64-bit D flip-flop arrays clocked at the CPU's operating frequency (3–5 GHz).

---

### Counters — Adding State to Addition

Chain flip-flops together and you get a **counter**: a circuit that increments a binary number on each clock edge.

**Ripple (asynchronous) counter:**
- Each flip-flop's output feeds the clock of the next flip-flop
- Q0 toggles every clock; Q1 toggles when Q0 goes 1→0; Q2 when Q1 goes 1→0…
- Simple but slow — the toggle ripples through stages (like ripple carry)

**Synchronous counter:**
- All flip-flops share the same clock
- Combinational logic computes next state: each bit toggles if all lower bits are 1
- Faster — all bits update simultaneously

**4-bit synchronous counter sequence:**
```
0000 → 0001 → 0010 → 0011 → 0100 → ... → 1111 → 0000 (wraps)
  0  →   1  →   2  →   3  →   4  → ... →  15  →   0
```

Counters appear everywhere: program counters (track which instruction to execute), timer circuits, frequency dividers, and pseudorandom number generators.

---

## The Concept: The Clock

The clock signal is the heartbeat of a synchronous digital system. It's a square wave oscillating between 0 and 1 at a fixed frequency.

```
CLK: ─┐  ┌─┐  ┌─┐  ┌─┐  ┌─
      └──┘  └──┘  └──┘  └──
```

At each rising edge, all flip-flops sample their D inputs and update their Q outputs simultaneously. Between edges, the combinational logic settles to its new values, ready for the next clock edge.

**Setup time** (t_su): D must be stable this long *before* the clock edge  
**Hold time** (t_h): D must be stable this long *after* the clock edge  
**Propagation delay** (t_pd): how long after the clock edge Q is stable

Maximum clock frequency:
```
f_max = 1 / (t_pd_flop + t_pd_logic + t_su)
```

This is the clock constraint every chip designer solves. Increase clock speed → combinational logic has less time to settle → errors. The CPU you're reading this on was carefully engineered to run at exactly its rated frequency under all operating conditions.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — SR Latch**
- Click Set and Reset buttons
- Watch Q and Q̄ update
- Try the forbidden state — see what happens

**Tool 2 — D Flip-Flop**
- Set D to 0 or 1
- Click the clock edge button — watch Q capture D
- Observe: changing D between clocks does NOT change Q

**Tool 3 — 4-Bit Counter**
- Step the clock manually or let it run automatically
- Watch the 4-bit binary count 0000 → 1111 → 0000
- Observe each bit's toggle frequency

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace an SR latch through state sequences, trace a DFF through clock cycles, design a modulo-6 counter, and explain the difference between combinational and sequential circuits in your own words.
