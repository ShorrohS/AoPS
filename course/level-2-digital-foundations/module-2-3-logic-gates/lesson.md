# Module 2.3 — Boolean Algebra and Logic Gates

---

## The Problem

> You have transistors. Each one is a switch: on or off, 1 or 0.
>
> You have Boolean algebra: a complete mathematical system for manipulating true/false values.
>
> Claude Shannon's 1937 thesis proved they're the same thing.
>
> Now: how do you turn that equivalence into a practical engineering toolkit?

The answer is **logic gates** — standardised circuit symbols that hide the transistor implementation and expose only the logical behaviour. A designer drawing a CPU schematic doesn't draw transistors; they draw gates. The gates abstract away the physics and let you reason in pure logic.

This module is where abstraction happens for the first time. You'll stop thinking about voltages and start thinking about truth.

---

## The Story

### George Boole's Algebra of Thought (1854)

George Boole was a self-taught English mathematician who published *An Investigation of the Laws of Thought* in 1854. He proposed that logical reasoning could be reduced to algebra where variables take only two values (TRUE/FALSE) and three operations (AND, OR, NOT) are sufficient to express any logical statement.

He had no application in mind. It was pure mathematics.

83 years later, Claude Shannon — reading Boole as a graduate student — realised that relay circuits behaved identically to Boolean algebra. The paper he wrote became the theoretical foundation of all digital electronics.

---

## The Seven Gates

Every digital circuit is built from combinations of these seven elementary gates:

### NOT (Inverter)
- **Symbol:** triangle with a bubble
- **Truth table:** output is the opposite of input
- **Boolean:** `Y = Ā` (A-bar)
- **Transistors needed:** 1 (CMOS uses 2: one NMOS + one PMOS)

| A | Y |
|---|---|
| 0 | 1 |
| 1 | 0 |

### AND
- **Symbol:** D-shape, flat on input side
- **Truth table:** output 1 only when ALL inputs are 1
- **Boolean:** `Y = A · B` (dot means AND)
- **Transistors:** 4 (CMOS)

| A | B | Y |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

### OR
- **Symbol:** curved on both sides, pointed output
- **Truth table:** output 1 when ANY input is 1
- **Boolean:** `Y = A + B` (plus means OR)
- **Transistors:** 4

| A | B | Y |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

### NAND (NOT-AND)
- **Symbol:** AND gate + output bubble
- **Truth table:** opposite of AND — output 0 only when ALL inputs are 1
- **Boolean:** `Y = A̅·̅B̅` = `NOT(A AND B)`
- **Transistors:** 4 — actually **simpler** than AND in CMOS!

| A | B | Y |
|---|---|---|
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

**NAND is the universal gate.** Any Boolean function can be implemented using only NAND gates. Every logic function — NOT, AND, OR, XOR, everything — can be constructed from NANDs alone. This is why real chips use NAND-based logic internally: one gate type is all you need to manufacture.

### NOR (NOT-OR)
- **Symbol:** OR gate + output bubble
- **Boolean:** `Y = NOT(A OR B)`
- Also universal — NOR alone can implement everything

### XOR (Exclusive OR)
- **Symbol:** OR gate with extra curved line on input
- **Truth table:** output 1 when inputs are DIFFERENT
- **Boolean:** `Y = A ⊕ B`
- Key application: **binary addition** (the sum bit of a half adder)

| A | B | Y |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

### XNOR (Exclusive NOR)
- Output 1 when inputs are the SAME
- Boolean: `Y = NOT(A ⊕ B)` = `A ⊙ B`
- Application: **equality comparator** (is A = B?)

---

## Boolean Algebra Laws

These identities let you simplify circuits — fewer gates, less cost, less power.

### Basic identities
```
A · 0 = 0          A + 0 = A
A · 1 = A          A + 1 = 1
A · A = A          A + A = A
A · Ā = 0          A + Ā = 1
NOT(NOT A) = A
```

### Commutative
```
A · B = B · A
A + B = B + A
```

### Associative
```
A · (B · C) = (A · B) · C
A + (B + C) = (A + B) + C
```

### Distributive
```
A · (B + C) = (A · B) + (A · C)
A + (B · C) = (A + B) · (A + C)
```

### De Morgan's Laws ← memorise these
```
NOT(A AND B) = (NOT A) OR  (NOT B)
NOT(A OR  B) = (NOT A) AND (NOT B)
```
In words: to negate a product, negate each factor and change AND↔OR.

**Why De Morgan's matters:** it lets you convert between AND-based and OR-based implementations. NAND universality comes directly from De Morgan — `NOT(NOT(A AND B)) = A AND B`, so you can build AND from two NANDs.

### Absorption and Simplification
```
A · (A + B) = A          (absorption)
A + (A · B) = A          (absorption)
(A + B)(A + C) = A + BC  (factoring)
```

---

## From Truth Table to Gate Circuit

Given any truth table, you can mechanically derive a circuit using **Sum of Products (SoP)** or **Product of Sums (PoS)**.

**Sum of Products:** 
1. Write one AND term for every row where output = 1
2. In each AND term, include each input: as-is if input = 1, inverted if input = 0
3. OR all the AND terms together

**Example:** build a circuit that is 1 when A=1, B=0, C=1 OR when A=1, B=1, C=0:

```
Term 1: A=1, B=0, C=1  →  A · B̄ · C
Term 2: A=1, B=1, C=0  →  A · B · C̄
Output: Y = (A · B̄ · C) + (A · B · C̄)
       = A · (B̄ · C + B · C̄)       ← factor out A
       = A · (B ⊕ C)                  ← that's XOR!
```

Three gates (one AND + one XOR) instead of two three-input ANDs and one OR. Simplification saves hardware.

---

## NAND-Only Implementations

Since NAND is universal:

**NOT from NAND:** `NOT A = NAND(A, A)`  
**AND from NAND:** `A AND B = NOT(NAND(A,B)) = NAND(NAND(A,B), NAND(A,B))`  
**OR from NAND:** `A OR B = NAND(NOT A, NOT B) = NAND(NAND(A,A), NAND(B,B))`

This is how real chip logic libraries work — everything compiled down to NAND trees.

---

## Gate Delay and Propagation

Gates are not instantaneous. In a 5nm process (2022), a typical gate switches in about 10–20 picoseconds. The time from input change to stable output is the **propagation delay** (`t_pd`).

When you chain gates, delays add:
```
Chain of 10 gates: 10 × 20ps = 200ps
Maximum clock frequency: 1 / 200ps = 5 GHz
```

Real CPUs spend enormous engineering effort minimising the number of gates in series on the **critical path** — the longest logic chain between any two flip-flops. The critical path determines the maximum clock speed.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

Three tools:

**Tool 1 — Logic Gate Sandbox**
- Place any of the 7 gates
- Connect them with wires
- Toggle inputs — outputs update instantly
- Truth table fills automatically

**Tool 2 — Boolean Expression Builder**
- Type any Boolean expression
- Simulator draws the circuit automatically
- Generates and verifies the truth table
- Simplification suggestions shown

**Tool 3 — NAND-Only Challenge**
- Given a target function, implement it using only NAND gates
- Counter shows how many NANDs you've used
- Compare to minimum

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Build truth tables, simplify Boolean expressions using De Morgan's laws and absorption, and implement XOR and a 2-to-1 multiplexer using only NAND gates.
