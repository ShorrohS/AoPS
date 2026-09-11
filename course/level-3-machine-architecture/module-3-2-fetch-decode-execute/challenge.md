# Challenge 3.2 — The Fetch-Decode-Execute Cycle

**Type:** Trace + reasoning + design  
**Estimated time:** 45–55 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Setup — The Toy CPU

This challenge uses a toy CPU with:
- 4 general-purpose registers: **A, B, C, D** (each 8 bits, initially 0)
- A **Program Counter (PC)** (initially 0x00)
- 16 bytes of memory (addresses 0x00–0x0F)
- A simple instruction set:

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 0x01 | LOAD_A imm | Load immediate value into A |
| 0x02 | LOAD_B imm | Load immediate value into B |
| 0x03 | LOAD_C imm | Load immediate value into C |
| 0x10 | ADD | A ← A + B |
| 0x11 | SUB | A ← A − B |
| 0x12 | AND | A ← A AND B |
| 0x13 | OR  | A ← A OR B |
| 0x20 | STORE addr | Memory[addr] ← A |
| 0x21 | LOAD_A_MEM addr | A ← Memory[addr] |
| 0x30 | JMP addr | PC ← addr (unconditional jump) |
| 0x31 | JZ addr | If A=0: PC ← addr, else continue |
| 0xFF | HALT | Stop execution |

All instructions that take an operand are 2 bytes: opcode then operand.  
Instructions with no operand (ADD, SUB, etc.) are 1 byte.

---

## Part A — Manual FDE Trace

The following program is loaded into memory starting at 0x00:

```
0x00: 0x01    (LOAD_A)
0x01: 0x0A    (immediate value: 10)
0x02: 0x02    (LOAD_B)
0x03: 0x06    (immediate value: 6)
0x04: 0x11    (SUB — A ← A - B)
0x05: 0x20    (STORE)
0x06: 0x0E    (store address: 0x0E)
0x07: 0xFF    (HALT)
```

For each FDE cycle, fill in this table:

| Cycle | PC (start) | Fetch: IR← | Decode: operation | Execute: result | PC (end) |
|-------|-----------|------------|-------------------|-----------------|----------|
| 1 | 0x00 | ? | ? | ? | ? |
| 2 | ? | ? | ? | ? | ? |
| 3 | ? | ? | ? | ? | ? |
| 4 | ? | ? | ? | ? | ? |

After cycle 4 (HALT), what is in:
- Register A?
- Register B?
- Memory[0x0E]?

---

## Part B — PC Arithmetic

5. After the CPU fetches a **1-byte instruction** (like ADD = 0x10) from address 0x07, what does PC become?

6. After the CPU fetches a **2-byte instruction** (like LOAD_A + operand) starting at address 0x04, what does PC become after the full instruction is processed (both bytes fetched)?

7. A JMP instruction at address 0x09 carries the operand 0x02. After executing the jump:
   - What is the new value of PC?
   - What instruction will be fetched next?

8. A program has a bug: the HALT instruction was accidentally overwritten and the CPU keeps executing past address 0x07 into undefined memory (all 0x00 bytes). What happens? (0x00 is not a valid opcode in our ISA — what would a real CPU do?)

---

## Part C — Write a Program

Write a program in the toy ISA that computes **3 × 4** using only ADD and LOAD instructions (no multiply instruction exists). Store the result at address 0x0F.

Constraints:
- You may use registers A, B, C
- You may use any addresses 0x08–0x0F for data storage
- Use HALT at the end

Write out the full memory contents (opcode + operand for each instruction), and trace at least the first 3 FDE cycles.

*Hint: 3 × 4 = 4 + 4 + 4. Use a loop… or just unroll it.*

---

## Part D — Pipeline Reasoning

A 4-stage pipeline: **Fetch → Decode → Execute → Writeback**

9. A non-pipelined CPU takes 4 cycles to complete 1 instruction. How many cycles to complete 8 instructions?

10. A 4-stage pipelined CPU takes 4 cycles for the first instruction to complete, then 1 additional cycle per instruction after that. How many total cycles for 8 instructions?

11. The 5th instruction in the sequence is a conditional jump (JZ). The CPU predicts "not taken" and continues fetching the next 3 instructions speculatively. The jump is actually taken. What happens to those 3 speculatively-fetched instructions? How many cycles are wasted?

12. In your own words: why does branch prediction matter more at higher clock speeds and deeper pipelines?

---

## Part E — Control Unit Design

The control unit for our toy CPU must generate control signals based on the decoded opcode. For each instruction below, list which hardware components receive an active control signal:

| Instruction | ALU? | Memory Read? | Memory Write? | PC Change? | Which registers involved? |
|-------------|------|--------------|---------------|------------|--------------------------|
| LOAD_A imm  |      |              |               |            |                          |
| ADD         |      |              |               |            |                          |
| STORE addr  |      |              |               |            |                          |
| JMP addr    |      |              |               |            |                          |
| HALT        |      |              |               |            |                          |

---

## Rubric

| Part | Points |
|------|--------|
| A trace (4 cycles) | 28 |
| B PC arithmetic (4 questions) | 20 |
| C program + trace | 25 |
| D pipeline (4 questions) | 17 |
| E control signals | 10 |

**Total: 100 points**

---

## Hints

<details>
<summary>Hint — Part A: how to handle 2-byte instructions</summary>
For LOAD_A: Cycle 1 fetches the opcode (0x01) at PC=0x00, PC becomes 0x01. The execute phase then fetches the operand byte from PC=0x01, PC becomes 0x02. So a 2-byte instruction consumes 2 PC increments. The whole LOAD_A + operand is one "logical" instruction but touches two memory addresses.
</details>

<details>
<summary>Hint — Part C: multiplication by repeated addition</summary>
Load 4 into A. Load 4 into B. ADD (A=8). ADD (A=12). STORE. Or: Load 4 into B three times and ADD three times. Or load 4 once and add it three times using a loop structure (JZ + counter in C).
</details>

---

## Solution

<details>
<summary>Part A — Full Trace</summary>

| Cycle | PC start | IR fetch | Operation | Result | PC end |
|-------|----------|----------|-----------|--------|--------|
| 1 | 0x00 | 0x01, 0x0A | LOAD_A 10 | A ← 10 | 0x02 |
| 2 | 0x02 | 0x02, 0x06 | LOAD_B 6  | B ← 6  | 0x04 |
| 3 | 0x04 | 0x11       | SUB       | A ← 10−6 = 4 | 0x05 |
| 4 | 0x05 | 0x20, 0x0E | STORE 0x0E | Mem[0x0E] ← 4 | 0x07 |

Cycle 5: HALT — execution stops.

Final state: A=4, B=6, Memory[0x0E]=4
</details>

<details>
<summary>Part D answers</summary>

9. Non-pipelined: 8 × 4 = **32 cycles**

10. Pipelined: 4 + (8−1) × 1 = **11 cycles**

11. The 3 speculatively-fetched instructions are **flushed** (discarded). The pipeline restarts from the jump target. **3 cycles wasted** (one per flushed instruction stage).

12. A deeper pipeline means more in-flight instructions at any moment. A misprediction wastes not 3 cycles but potentially 15–20 cycles (for a 15–20 stage pipeline like modern x86). At 5 GHz, 20 wasted cycles = 4 nanoseconds. Multiply by millions of branches per second and the performance impact is enormous. This is why branch predictors in modern CPUs are extremely sophisticated — some use machine learning.
</details>

<details>
<summary>Part E — Control signals</summary>

| Instruction | ALU? | Mem Read? | Mem Write? | PC Change? | Registers |
|-------------|------|-----------|------------|------------|-----------|
| LOAD_A imm  | No | Yes (operand) | No | +2 | A (dest), PC |
| ADD | Yes (ADD) | No | No | +1 | A, B (src), A (dest) |
| STORE addr | No | Yes (address) | Yes | +2 | A (src), MAR, MDR |
| JMP addr | No | Yes (address) | No | Set to operand | PC |
| HALT | No | No | No | No | None |
</details>
