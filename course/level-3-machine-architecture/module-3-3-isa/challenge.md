# Challenge 3.3 — Instruction Set Architecture

**Type:** Programming + encoding + design + analysis  
**Estimated time:** 50–60 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Setup — The Toy ISA (same as Module 3.2)

| Opcode | Mnemonic | Format | Description |
|--------|----------|--------|-------------|
| 0x01 | LOAD | 01 rr vv | Load immediate vv into register rr |
| 0x02 | LOAD_MEM | 02 rr aa | Load memory[aa] into register rr |
| 0x03 | STORE | 03 rr aa | Store register rr to memory[aa] |
| 0x10 | ADD | 10 r1 r2 | r1 ← r1 + r2 |
| 0x11 | SUB | 11 r1 r2 | r1 ← r1 − r2 |
| 0x20 | JMP | 20 aa | PC ← aa |
| 0x21 | JZ | 21 rr aa | If rr=0: PC ← aa |
| 0xFF | HALT | FF | Stop |

Registers: A=0x00, B=0x01, C=0x02, D=0x03

---

## Part A — Decode These Instructions

Decode each hex sequence into a mnemonic instruction:

1. `01 00 0A` → ?
2. `10 00 01` → ?
3. `03 00 0F` → ?
4. `21 02 06` → ?
5. `11 01 02` → ?
6. `20 00` → ?

---

## Part B — Encode These Instructions

Encode each mnemonic into hex bytes:

7. `LOAD B, 255`
8. `ADD C, D`
9. `STORE D, 0x08`
10. `JZ A, 0x02`
11. `LOAD_MEM C, 0x0A`

---

## Part C — Write a Program

**Program 1:** Write a toy ISA program that computes `1 + 2 + 3 + 4 + 5` and stores the result (15) at address 0x0F. Use a loop — do not just add five LOAD/ADD instructions manually.

Write it as hex bytes, starting at address 0x00. Then trace the first 4 FDE cycles.

**Program 2:** Write a program that finds the maximum of two values (stored at addresses 0x0C and 0x0D) and stores the result at 0x0E.

*Hint: max(A, B) — load both, subtract B from A. If result is negative (or zero and B was larger), B is max. If positive, A is max. JZ can help.*

---

## Part D — RISC vs CISC Analysis

A CISC CPU has a single instruction: `ADD_MEM [addr1], [addr2]` — adds the value at addr1 to the value at addr2 and stores the result at addr1. This is 1 instruction, 5 bytes.

A RISC CPU must do this with 3 instructions:
```
LOAD_MEM A, addr1    ; 3 bytes
LOAD_MEM B, addr2    ; 3 bytes
ADD A, B             ; 3 bytes
STORE A, addr1       ; 3 bytes
```
That is 4 instructions, 12 bytes.

12. What is the code size advantage of the CISC approach? (bytes saved per operation)

13. The RISC CPU runs at 2 GHz and executes each instruction in 1 cycle. The CISC CPU runs at 1.5 GHz and the complex instruction takes 4 cycles to complete. Which finishes the operation faster? Show the calculation.

14. The RISC pipeline can be 8 stages deep (no instruction takes more than 1 cycle to pass through any stage). The CISC pipeline can only be 3 stages deep (the complex instruction has a multi-cycle execute stage). Both processors need 100 of these ADD_MEM operations. Estimate the throughput advantage of the RISC pipeline once it is full.

15. In 3–4 sentences: why did ARM (RISC) win in mobile/embedded computing, while x86-64 (CISC) still dominates desktops and servers? What does each architecture optimise for?

---

## Part E — Design a New Instruction

You need to add a **MUL (multiply)** instruction to the toy ISA.

16. Design the encoding: what opcode, format, and byte length?

17. What hardware does the control unit need to activate that ADD does not? (Consider: the ALU in Module 2.6 had no multiply. What new circuit is required?)

18. A RISC purist argues: "Don't add MUL — just use repeated ADD in a loop." For 8-bit numbers, what is the worst case? (What is the maximum number of additions needed?) Is this a reasonable argument?

---

## Rubric

| Part | Points |
|------|--------|
| A decode (6 instructions) | 18 |
| B encode (5 instructions) | 15 |
| C Program 1 (loop) | 20 |
| C Program 2 (max) | 15 |
| D analysis (4 questions) | 20 |
| E design (3 questions) | 12 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A — Decoded</summary>

1. `01 00 0A` → `LOAD A, 10`
2. `10 00 01` → `ADD A, B`
3. `03 00 0F` → `STORE A, 0x0F`
4. `21 02 06` → `JZ C, 0x06`
5. `11 01 02` → `SUB B, C`
6. `20 00` → `JMP 0x00`
</details>

<details>
<summary>Part B — Encoded</summary>

7. `LOAD B, 255` → `01 01 FF`
8. `ADD C, D` → `10 02 03`
9. `STORE D, 0x08` → `03 03 08`
10. `JZ A, 0x02` → `21 00 02`
11. `LOAD_MEM C, 0x0A` → `02 02 0A`
</details>

<details>
<summary>Part D answers</summary>

12. CISC saves 7 bytes per operation (12 − 5 = 7 bytes).

13. RISC: 4 instructions at 2 GHz = 4 × 0.5 ns = **2.0 ns**. CISC: 4 cycles at 1.5 GHz = 4 × 0.667 ns = **2.67 ns**. RISC is faster despite needing more instructions.

14. RISC pipeline depth 8: throughput ≈ 1 instruction/cycle after fill. 400 RISC instructions ÷ 1 per cycle = 400 cycles (ignoring fill). CISC pipeline depth 3: 1 complex instruction per 1 cycle (once pipelined), but only 3-deep so fill overhead is less. However at 2 GHz vs 1.5 GHz: 100 RISC ops take 100 + 7 fill = 107 ns / (2 GHz / 4 ops/complex) ≈ better throughput for RISC. The exact answer depends on assumptions — the key insight is: deeper pipeline × higher clock >> fewer instructions.

15. ARM won in mobile because RISC's simplicity means smaller, cooler, more power-efficient chips — crucial when running on a battery. x86-64 dominates desktops/servers because of the 40-year software investment and backward compatibility — every Windows program expects x86-64. Intel and AMD have also poured billions into making x86-64 fast, offsetting the inherent inefficiency of the CISC ISA.
</details>
