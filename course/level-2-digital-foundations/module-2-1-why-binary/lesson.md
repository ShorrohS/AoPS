# Module 2.1 — Why Binary? The Physics of Two States

---

## The Problem

> You have a circuit carrying voltage. You want to represent the number 7. The obvious approach: use 7 volts. Store a number as its voltage.
>
> The problem: real-world circuits are noisy. A "7V" signal might arrive as 6.8V. Is that 6 or 7? A "3V" signal in a noisy environment might read as 2.6V, 3.1V, or 3.4V. You've built a calculator that can't be trusted to read its own numbers.
>
> The 1940s engineers trying to build reliable computers faced this exact crisis. The solution was counterintuitive: **use less information, not more.**

Instead of representing a number as a precise voltage level, represent it as a *region*: anything above 2.5V is a 1. Anything below 0.5V is a 0. A 0.5V–2.5V "no-man's-land" is forbidden — the circuit is designed to push signals to one extreme or the other.

This is binary. Its superiority over analog representation isn't mathematical elegance — it's **noise immunity**.

---

## The Story

### The Analog Disaster

Early computing attempts in the 1930s and 1940s tried analog computers — machines where voltage levels directly encoded values. They could solve differential equations faster than any human. But they had a fundamental problem: every component added noise.

A resistor adds thermal noise (electrons jiggling from heat). A wire acts as an antenna and picks up electromagnetic interference. Capacitors leak. Amplifiers amplify noise alongside signal. Chain together a hundred components and you've amplified the noise a hundred times.

Analog computers were accurate to perhaps 3–4 decimal places under ideal conditions. That's fine for controlling a gun turret. It's catastrophically wrong for financial calculations or scientific tables where you need 10+ digits of precision.

**Shannon's information theory (1948)** put this on rigorous mathematical footing: you can transmit information reliably over a noisy channel if and only if you have error correction — and the simplest error-correcting code is binary, because there are only two valid values to distinguish between.

---

### Why Two States Win

Compare three approaches to encoding the digit 5 in electronics:

**Analog (10 voltage levels, 0–9V):**
- Each level is 1V apart
- Noise margin: ±0.5V before misread
- Chain 20 amplifiers: noise accumulates, levels blur together
- Precision: ~3–4 decimal digits maximum

**Decimal (10 discrete levels):**
- Tried! The ENIAC used decimal ring counters — 10 flip-flops per digit
- A decimal digit required 10 transistors
- A binary digit requires 1 transistor
- 10× less efficient in hardware

**Binary (2 levels: 0 and 1):**
- 0V = 0, 5V = 1 (for a 5V logic family)
- Noise margin: ±2V before misread — 4× better than analog
- Every transistor is either saturated (fully on) or cut off (fully off)
- After every gate, the signal is *regenerated* to full swing — noise resets
- Precision: unlimited (just use more bits)

The binary system transforms *analog noise* into a *digital decision*. At each gate boundary, a comparator decides: is this above the threshold? If yes, drive the output to +5V. If no, drive it to 0V. The noise is erased. Precision is restored.

---

### Bits, Bytes, and Words

**Bit**: one binary digit — 0 or 1. The smallest unit of information.  
One bit encodes one of 2 possibilities.

**Byte**: 8 bits. Encodes one of 2⁸ = 256 possibilities.  
Chosen historically to represent one character (ASCII uses 7 bits; the 8th allows error checking or extended characters).

**Word**: the natural integer width of a processor. Was 8-bit (8086 era), then 16, 32, and now 64 bits. A 64-bit processor can represent integers from 0 to 2⁶⁴−1 = 18,446,744,073,709,551,615.

**Nibble** (yes, really): 4 bits = one hexadecimal digit. Used constantly in practice.

---

### The Threshold and Noise Margin

In a 5V CMOS logic family (common from the 1970s–1990s):
- Input LOW: 0V to 1.5V → read as 0
- Input HIGH: 3.5V to 5V → read as 1
- Forbidden zone: 1.5V to 3.5V (output should never be in this range)
- Output LOW: guaranteed ≤ 0.5V
- Output HIGH: guaranteed ≥ 4.5V

**Noise margin** = (guaranteed output) − (minimum acceptable input) = 4.5 − 3.5 = 1.0V  
This means up to 1V of noise on any wire before a logical error occurs.

Modern 1.8V and 1.2V logic (used in current chips) has tighter margins, which is one reason modern chips require extremely clean power supplies and careful layout.

---

### Binary and Power of 2

With n bits you can represent 2ⁿ distinct values.

| Bits | Values | Range (unsigned) | Common name |
|------|--------|-----------------|-------------|
| 1 | 2 | 0–1 | bit |
| 4 | 16 | 0–15 | nibble |
| 8 | 256 | 0–255 | byte |
| 16 | 65,536 | 0–65,535 | word |
| 32 | 4,294,967,296 | 0–4.3 billion | double word |
| 64 | 1.8×10¹⁹ | 0–18.4 quintillion | quad word |

The reason computers count in powers of 2 isn't arbitrary — it falls directly out of the physics of switches.

---

## The Concept: Regeneration

The single most important property of digital systems is **signal regeneration**.

In an analog system: noise accumulates indefinitely as signals pass through components.

In a digital system: each logic gate acts as a threshold detector. It receives a potentially noisy input, makes a binary decision, and drives a fresh, noise-free output. The noise resets to zero at every gate.

This is why digital audio doesn't degrade when copied. Why a file sent across the internet is bit-for-bit identical at the destination. Why your computer gives the same answer to 7+8 a billion times in a row without ever computing 15.0001.

**Analog computes with voltages. Digital computes with decisions.**

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

Three tools:

**Tool 1 — Signal Noise Demonstrator**
- Drag an "analog" signal (sine wave representing a value 0–9)
- Add noise using the noise slider
- Watch analog values blur and misread at realistic noise levels
- Switch to binary: same noise, zero misreads

**Tool 2 — Threshold Visualiser**
- See a 5V CMOS logic family's input/output thresholds
- Drag a signal through the forbidden zone — watch the output snap to 0 or 5V
- Adjust noise level and observe when the system fails

**Tool 3 — Bit Counter**
- Enter a decimal number
- Watch it decompose into bits, one by one
- See the binary representation animate
- Understand which bits are "on" (1) and which are "off" (0)

---

## Going Deeper

The threshold-based binary system seems wasteful — why use only two states when a wire could in principle carry many voltage levels? This is the question behind **multi-level cell (MLC) flash memory**, which stores 2, 3, or 4 bits per cell by distinguishing 4, 8, or 16 voltage levels in a capacitor. The cost: each level requires more precision, more careful voltage control, and more error-correction circuitry. MLC flash requires powerful error-correcting codes running constantly just to be trustworthy.

For compute logic — gates, ALUs, CPUs — the overhead makes multi-level impractical. For storage (where you read once, correct errors, and don't chain thousands of stages), it's economically worthwhile. This is why your SSD stores 3 bits per cell but your CPU operates purely binary.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

You'll calculate noise margins for different logic families, convert between analog and digital precision, and explain in writing why signal regeneration makes digital computers more reliable than analog ones.
