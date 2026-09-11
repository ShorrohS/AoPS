# Module 2.4 — Combinational Circuits

---

## The Problem

> You can compute AND, OR, NOT. You can build any logic function from gates.
>
> But the fundamental operation every computer performs millions of times per second is **addition**. How do you add two binary numbers using only logic gates?
>
> And once you can add, how do you chain that addition across multiple bits — from one-bit arithmetic to 4-bit, 8-bit, 32-bit?

This module builds the **adder** — the most important combinational circuit — from first principles, one gate at a time. By the end, you'll have a working 4-bit ripple-carry adder that performs real binary addition, and understand every gate inside it.

**Combinational circuit**: output depends only on current inputs. No memory. No state. Input → output, instantly (within propagation delay).

---

## The Story

### The Half Adder

Adding two 1-bit numbers produces a 2-bit result: a sum bit and a carry bit.

```
0 + 0 = 00  (sum=0, carry=0)
0 + 1 = 01  (sum=1, carry=0)
1 + 0 = 01  (sum=1, carry=0)
1 + 1 = 10  (sum=0, carry=1)
```

Truth table:

| A | B | Sum | Carry |
|---|---|-----|-------|
| 0 | 0 | 0   | 0     |
| 0 | 1 | 1   | 0     |
| 1 | 0 | 1   | 0     |
| 1 | 1 | 0   | 1     |

Looking at the patterns:
- **Sum = A XOR B** — output is 1 when exactly one input is 1
- **Carry = A AND B** — output is 1 only when both inputs are 1

Implementation: **one XOR gate + one AND gate**.

```
    A ─┬─[XOR]─ Sum
       │
    B ─┤
       │
       └─[AND]─ Carry
```

The half adder is "half" because it can't handle an incoming carry from a previous stage. For multi-bit addition, we need the full adder.

---

### The Full Adder

A **full adder** adds three 1-bit inputs: A, B, and Cin (carry-in from the previous stage).

| A | B | Cin | Sum | Cout |
|---|---|-----|-----|------|
| 0 | 0 | 0   | 0   | 0    |
| 0 | 0 | 1   | 1   | 0    |
| 0 | 1 | 0   | 1   | 0    |
| 0 | 1 | 1   | 0   | 1    |
| 1 | 0 | 0   | 1   | 0    |
| 1 | 0 | 1   | 0   | 1    |
| 1 | 1 | 0   | 0   | 1    |
| 1 | 1 | 1   | 1   | 1    |

Derivation:
- **Sum = A XOR B XOR Cin**
- **Cout = (A AND B) OR (Cin AND (A XOR B))**

Implementation: **two half adders + one OR gate** (5 gates total, or 9 gates in NAND-only).

```
    A ─[HA]─ S1 ─[HA]─ Sum
    B ─┘  └Cout1        ↑ Cin also goes in
                        │
         Cout1 ─[OR]─ Cout
         Cout2 ─┘
```

---

### The 4-Bit Ripple Carry Adder

To add two 4-bit numbers A[3:0] and B[3:0], chain four full adders:

```
    A0 B0     A1 B1     A2 B2     A3 B3
     │  │      │  │      │  │      │  │
    [FA0]──C1─[FA1]──C2─[FA2]──C3─[FA3]──Cout
    Cin=0      │         │         │         │
               S0        S1        S2        S3
```

- FA0 gets Cin=0 (no incoming carry for the least significant bit)
- FA0's Cout feeds FA1's Cin
- FA1's Cout feeds FA2's Cin
- FA2's Cout feeds FA3's Cin
- FA3's Cout is the overflow/carry-out of the entire addition

**Example:** 5 + 6 = ?
```
A = 0101  (5)
B = 0110  (6)

Bit 0: 1+0+0=1, Cout=0  → S0=1
Bit 1: 0+1+0=1, Cout=0  → S1=1
Bit 2: 1+1+0=0, Cout=1  → S2=0
Bit 3: 0+0+1=1, Cout=0  → S3=1

Result: 1011 = 11 ✓
```

This is called "ripple carry" because the carry signal **ripples** from bit 0 to bit 3. FA3 cannot compute its result until FA2's carry is ready — which waits for FA1 — which waits for FA0. The critical path is 4 full-adder delays long.

For a 64-bit ripple-carry adder: 64 × (full-adder delay). Too slow for high-speed CPUs!

---

### Carry Lookahead — Fixing the Speed Problem

**Carry lookahead** (invented in the 1950s, still used today) eliminates the ripple wait by computing all carries in parallel.

Define:
- **Generate:** `Gi = Ai AND Bi` — this bit *generates* a carry regardless of Cin
- **Propagate:** `Pi = Ai XOR Bi` — this bit *propagates* an incoming carry

Then:
```
C1 = G0 OR (P0 AND C0)
C2 = G1 OR (P1 AND C1)
   = G1 OR (P1 AND G0) OR (P1 AND P0 AND C0)
C3 = G2 OR (P2 AND G1) OR (P2 AND P1 AND G0) OR (P2 AND P1 AND P0 AND C0)
C4 = G3 OR (P3 AND G2) OR ...
```

Each carry is now a direct function of the original inputs A, B, C0 — no chaining. All carries computed in 2 gate delays instead of n × (full adder delay). This is why modern 64-bit adders run at GHz speeds.

---

### Other Important Combinational Circuits

**Multiplexer (MUX):** selects one of N inputs based on a select signal.
- 2-to-1 MUX: `Y = (S AND B) OR (NOT S AND A)` — if S=0, pass A; if S=1, pass B
- Used everywhere: routing data, implementing registers, building ALU operations

**Demultiplexer (DEMUX):** routes one input to one of N outputs based on select.

**Decoder:** converts n-bit binary input to one of 2ⁿ one-hot outputs.
- Example: 3-bit input → 8 output lines, exactly one high
- Application: memory address decoding, opcode decoding in CPUs

**Encoder:** opposite of decoder — 2ⁿ inputs to n-bit output.

**Comparator:** compares two n-bit numbers, outputs A>B, A=B, A<B.
- `A=B`: XOR each bit pair, NOR all results
- `A>B`: more complex — requires looking at most significant differing bit

---

## The Concept: No State, Just Wires and Gates

A combinational circuit has no memory. Change the inputs, the outputs change (after propagation delay). Remove the inputs, the outputs become undefined. There is no "stored" value.

Everything we've built so far — adders, multiplexers, decoders — is combinational. The next module (2.5) introduces **sequential circuits**: circuits that remember their state. The union of combinational and sequential circuits is everything inside a CPU.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Half Adder**
- Toggle A and B, watch Sum and Carry update
- Gate-level view shows which gates are active

**Tool 2 — Full Adder**
- Toggle A, B, Cin
- Step through the carry propagation
- See both internal half adders working

**Tool 3 — 4-Bit Ripple Carry Adder**
- Enter two 4-bit numbers
- Watch carry ripple from bit 0 to bit 3, one step at a time
- Overflow flag lights up when result exceeds 4 bits

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace a full adder truth table, trace carry propagation through the 4-bit adder, implement subtraction using two's complement, and calculate the critical path delay.
