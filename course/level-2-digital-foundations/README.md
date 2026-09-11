# Level 2 — Digital Foundations: The Language of Machines

> *A transistor switches in nanoseconds. But how does switching fast become thinking?*

---

## What This Level Is About

Level 1 gave you the atom of computing: a switch with two states. Level 2 shows how those switches, combined by the millions, build up into a machine that can perform any calculation ever conceived.

The path: **two physical states → binary digits → Boolean algebra → logic gates → circuits that add → circuits that remember → a simple processor core.**

Every CPU ever made — from the 4004 to the M4 — is built from exactly the ideas in this level, just repeated billions of times with extraordinary precision.

By the end of Level 2, you will be able to:
- Explain why binary is the only practical number system for electronics
- Convert fluently between binary, decimal, octal, and hexadecimal
- Design any logic circuit from truth table to gate diagram
- Build a working 4-bit adder from first principles
- Explain how a flip-flop stores one bit, and how flip-flops chain into counters
- Describe the structure and operation of a simple ALU

---

## Modules

| Module | Title | Core Concept |
|--------|-------|-------------|
| [2.1](./module-2-1-why-binary/lesson.md) | Why Binary? | Physics forces two states; analog fails at scale |
| [2.2](./module-2-2-number-systems/lesson.md) | Number Systems | Binary, Octal, Hex, Two's Complement |
| [2.3](./module-2-3-logic-gates/lesson.md) | Boolean Algebra & Logic Gates | Truth tables, gate symbols, NAND universality |
| [2.4](./module-2-4-combinational-circuits/lesson.md) | Combinational Circuits | Half adder → Full adder → 4-bit ripple carry |
| [2.5](./module-2-5-sequential-circuits/lesson.md) | Sequential Circuits | SR latch → D flip-flop → register → counter |
| [2.6](./module-2-6-simple-alu/lesson.md) | From Gates to a Simple ALU | Arithmetic + Logic Unit: the heart of every CPU |

---

## Prerequisites

**Level 1 — Physical Computing** (complete). You must understand:
- What a transistor is and how it switches
- Why switching can represent binary (0/1)
- That AND, OR, NOT can be built from relay contacts

---

## The Abstraction Stack

Level 2 is where we first build **abstractions**. An abstraction hides the details of the layer below so you can think at a higher level. Name each layer as you build it:

```
Physical layer:     Transistors switching (Level 1)
         ↓
Gate layer:         Logic gates (AND, OR, NOT) — Module 2.3
         ↓
Circuit layer:      Adders, multiplexers — Module 2.4
         ↓
State layer:        Flip-flops, registers — Module 2.5
         ↓
ALU layer:          Arithmetic + Logic Unit — Module 2.6
         ↓
CPU layer:          Fetch-Decode-Execute (Level 3)
```

Each level knows nothing about the one below it — only its interface. This is the principle that makes building a billion-transistor chip possible.

---

## What Comes Next

**Level 3 — Machine Architecture** assembles the ALU from this level with memory and control logic to build a simple but complete CPU: the fetch-decode-execute cycle, registers, program counter, and instruction set.
