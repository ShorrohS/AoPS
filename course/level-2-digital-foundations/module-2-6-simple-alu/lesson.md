# Module 2.6 — From Gates to a Simple ALU

---

## The Problem

> You have:
> - Logic gates that compute AND, OR, NOT, XOR
> - Adders that add binary numbers
> - Multiplexers that select between signals
>
> Now: how do you combine these into a single unit that can perform any arithmetic or logical operation on demand?
>
> The answer is the **Arithmetic Logic Unit (ALU)** — the computational core of every processor ever built.

The ALU is the machine that executes the instructions of every program ever written. When Python evaluates `x + 1`, the compiler translates this to an ADD instruction, the CPU fetches it, decodes it, and routes the operands through the ALU. The ALU computes the result in one clock cycle.

Understanding the ALU is the bridge between Level 2 (circuits) and Level 3 (machine architecture). Once you have an ALU, you have a machine that can compute. Add memory, a program counter, and control logic — and you have a CPU.

---

## The Story

### What an ALU Must Do

A minimal ALU for a real processor needs to support at least:

**Arithmetic operations:**
- ADD: A + B
- SUB: A − B (= A + (−B) = A + two's complement of B)
- INC: A + 1
- DEC: A − 1

**Logical operations:**
- AND: A AND B
- OR: A OR B
- XOR: A XOR B
- NOT: NOT A (bitwise invert)

**Comparison (produces flags, not data):**
- Zero flag: result = 0?
- Carry flag: unsigned overflow?
- Negative flag: most significant bit = 1?
- Overflow flag: signed overflow?

**Shifts (often included):**
- LSR: logical shift right (divide by 2)
- LSL: logical shift left (multiply by 2)

All of these from gates, adders, and multiplexers.

---

### Building the 4-Bit ALU

**Step 1: Arithmetic unit**

ADD and SUB use the same adder. For SUB, we negate B using two's complement (invert B and set Cin=1).

Control signal: `sub` (0=add, 1=subtract)
```
B_effective = B XOR sub  (when sub=1, inverts B)
Cin = sub                (when sub=1, adds 1 to complete two's complement)
Result = A + B_effective + Cin
```

One 4-bit adder handles both ADD and SUB. This is elegant: subtraction is free once you have addition and XOR.

**Step 2: Logic unit**

For each bit position i, compute:
```
AND_result[i]  = A[i] AND B[i]
OR_result[i]   = A[i] OR  B[i]
XOR_result[i]  = A[i] XOR B[i]
NOT_result[i]  = NOT A[i]
```

All four computed simultaneously — no selection yet.

**Step 3: Multiplexer selects the operation**

A 2-bit **operation select** (op[1:0]) controls a 4-to-1 multiplexer:
```
op = 00 → select AND result
op = 01 → select OR result
op = 10 → select XOR result  
op = 11 → select NOT result
```

**Step 4: Arithmetic/Logic mode select**

A 1-bit `mode` signal selects between arithmetic unit output and logic unit output:
```
mode = 0 → arithmetic (ADD/SUB)
mode = 1 → logic (AND/OR/XOR/NOT)
```

**Combined control word: 3 bits (sub, mode, op[1:0])**

| mode | sub | op | Operation |
|------|-----|----|-----------|
| 0    | 0   | — | ADD |
| 0    | 1   | — | SUB |
| 1    | 0   | 00 | AND |
| 1    | 0   | 01 | OR |
| 1    | 0   | 10 | XOR |
| 1    | 0   | 11 | NOT A |

---

### Flags

The ALU doesn't just produce a result — it also produces **status flags** that the control unit reads to make decisions (for branch instructions like `if`, `while`, comparisons).

**Zero flag (Z):**
```
Z = NOR(result[3], result[2], result[1], result[0])
Z = 1 when all result bits are 0
```
Application: `JZ` (jump if zero) — the basis of all equality tests.

**Carry flag (C):**
```
C = carry-out of the most significant adder stage
C = 1 when unsigned result overflowed (exceeded 15 for 4-bit)
```
Application: multi-precision arithmetic — add 64-bit numbers as two 32-bit adds using the carry from the first.

**Negative flag (N):**
```
N = result[3]  (most significant bit)
N = 1 when result is negative in two's complement
```
Application: `JN` (jump if negative) — signed comparisons.

**Overflow flag (V):**
Signed overflow — result's sign is wrong.
```
V = Cout XOR Cin_of_MSB
V = 1 when adding two positives gives a negative (or two negatives gives a positive)
```
Application: detecting signed arithmetic errors.

---

### Real-World ALU: Intel x86-64 EFLAGS

The x86-64 processor's EFLAGS register contains all four flags plus more:
- **CF** — Carry Flag
- **ZF** — Zero Flag
- **SF** — Sign Flag (= Negative flag)
- **OF** — Overflow Flag
- **PF** — Parity Flag (count of 1 bits in result)
- **AF** — Auxiliary Carry (carry from bit 3 to bit 4, used in BCD arithmetic)

Every arithmetic instruction sets these flags. Conditional jump instructions (JE, JNE, JL, JG, etc.) test these flags and branch accordingly. Your `if (x == 0)` in C compiles to a CMP + JE — the ALU does the comparison, sets ZF, and the JE checks it.

---

### Putting It All Together

Here is the complete datapath for our 4-bit ALU:

```
Input: A[3:0], B[3:0], control[2:0] = {mode, sub, op[1:0]}

                    B ──[XOR sub]──┐
                                   │
A ──────────────────[4-bit adder]──┤── arith_result ──┐
        Cin = sub ──┘               │                  │
                                   │                  [MUX]── result
A ──[AND]──┐                       │    sub ──────────┘
B ──┘      ├── logic_results ──────┘
A ──[OR]───┤
B ──┘      │                    Z = NOR(result)
A ──[XOR]──┤                    C = carry_out
B ──┘      │                    N = result[3]
A ──[NOT]──┘                    V = overflow
```

This 4-bit ALU uses approximately 100 gates. A modern CPU's 64-bit ALU uses thousands. The structure is identical — wider data paths, more operations, more flags.

---

## The Concept: One Hardware, Many Operations

The ALU's elegance is that it contains **multiple computation paths running simultaneously**. The ADD path is always computing A+B. The AND path is always computing A AND B. The XOR path is always computing A XOR B.

The **multiplexer** at the output selects which result to forward based on the instruction opcode. The "unused" computation results are simply discarded.

This is a form of **spatial parallelism** — computing multiple things at once and selecting the needed result. It's faster and simpler than sequentially deciding what to compute.

The same principle scales up: modern CPUs have multiple ALUs running in parallel (superscalar execution), and GPU shader cores have thousands of ALUs.

---

## Level 2 Capstone

You have now completed Level 2. You can:
1. Explain why binary beats analog (Module 2.1)
2. Convert between binary, hex, octal, and decimal; negate using two's complement (Module 2.2)
3. Write truth tables, apply Boolean algebra, build circuits from expressions (Module 2.3)
4. Build a half adder, full adder, and 4-bit ripple-carry adder (Module 2.4)
5. Explain SR latches, D flip-flops, registers, and counters (Module 2.5)
6. Design a simple ALU with arithmetic, logic, and flag outputs (Module 2.6)

This is the complete **digital foundations** layer. Everything above it — CPU architecture, instruction sets, operating systems, programming languages — is built on what you now understand.

**Level 3 — Machine Architecture** assembles these components into a CPU: an ALU + registers + program counter + memory bus + control unit = a machine that can execute instructions.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — 4-Bit ALU**
- Enter A and B as 4-bit numbers
- Select operation (ADD, SUB, AND, OR, XOR, NOT)
- Watch the result and all four flags update
- Step through the ADD/SUB mux and logic unit visually

**Tool 2 — Flag Explorer**
- Set specific A and B values
- Observe when each flag lights up
- Understand: when does Carry fire vs Overflow?

**Tool 3 — ALU Program**
- Write a 5-step "program" using ALU operations
- Execute step by step — accumulate a result across operations
- Preview of Level 3: this is the ALU stage of fetch-decode-execute

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Execute ALU operations by hand, predict flags before running, write a mini-program using only ALU operations, and explain the difference between carry and overflow.
