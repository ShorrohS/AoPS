# Module 3.2 — The Fetch-Decode-Execute Cycle

---

## The Problem

> You now have:
> - An ALU that performs arithmetic and logic
> - Memory that stores bytes at addresses
> - Registers that hold values temporarily
>
> The missing piece: what makes the CPU actually *do* something?
>
> What starts the process? What decides which operation to perform next?
> What keeps it going, instruction after instruction, without stopping?

The answer is the **Fetch-Decode-Execute cycle** — the three-step loop that has driven every program ever run on every computer ever built.

---

## The Story

### The Problem of Sequential Control

Imagine you have a list of instructions written on paper:
1. Load the number at address 5 into Register A
2. Load the number at address 6 into Register B
3. Add Register A and Register B
4. Store the result at address 7

A human can read this list and execute it. But how does a machine do it?

The machine needs:
- A way to **remember where it is** in the instruction list (the Program Counter)
- A way to **read the next instruction** from memory (the Fetch step)
- A way to **understand what the instruction means** (the Decode step)
- A way to **carry out the instruction** (the Execute step)
- A way to **automatically move to the next instruction** (PC increment)

These five elements, working in a continuous loop, are the CPU.

---

### The Three Registers You Cannot Live Without

**Program Counter (PC)** — holds the address of the *next instruction* to fetch. After each fetch, it automatically increments. A jump instruction sets it to a new value, breaking the sequential flow.

**Instruction Register (IR)** — holds the *current instruction* being decoded and executed. The fetched instruction is copied here and stays until the next fetch.

**Memory Address Register (MAR)** — holds the address being read from or written to memory. When the CPU needs to access memory, it first loads the address here.

**Memory Data Register (MDR)** also called the Memory Buffer Register (MBR) — holds the data traveling to or from memory. Reads store their result here; writes take their data from here.

---

### The Cycle — Step by Step

**FETCH:**
1. Copy PC → MAR (tell memory which address to read)
2. Read memory[MAR] → MDR (get the instruction bytes)
3. Copy MDR → IR (load instruction into the instruction register)
4. Increment PC (point to the next instruction)

**DECODE:**
5. The control unit examines IR
6. It identifies the **opcode** (what operation to perform)
7. It identifies the **operands** (which registers, addresses, or immediate values to use)
8. It activates the correct control signals for the next phase

**EXECUTE:**
9. The identified operation is performed:
   - ALU operation: route operands to ALU, store result
   - Memory read: MAR ← address, MDR ← memory[MAR], register ← MDR
   - Memory write: MAR ← address, MDR ← register, memory[MAR] ← MDR
   - Jump: PC ← new address

10. Return to FETCH.

The cycle repeats forever — or until the machine is powered off or halts.

---

### Why This Is Profound

Every program ever written — every web browser, every game, every operating system — runs on this three-step loop. The loop does not know about Python or JavaScript or databases. It knows only: fetch an instruction, decode it, execute it, repeat.

The sophistication of modern software exists entirely in how instructions are sequenced and what they instruct the hardware to do. The hardware itself is doing nothing more than this ancient, simple cycle.

---

### A Concrete Example — Tracing ADD

Suppose memory contains:
```
Address 0x00: 0x01  ← LOAD_A instruction (load next byte into Register A)
Address 0x01: 0x05  ← operand: value 5
Address 0x02: 0x02  ← LOAD_B instruction
Address 0x03: 0x03  ← operand: value 3
Address 0x04: 0x10  ← ADD instruction (A + B → A)
Address 0x05: 0x30  ← STORE instruction (store A at address 0x08)
Address 0x06: 0x08  ← operand: store address
```

PC starts at 0x00.

**Cycle 1 — LOAD_A 5:**
- Fetch: IR ← 0x01, PC becomes 0x01
- Decode: opcode 0x01 = LOAD_A; operand follows
- Execute: fetch operand (0x05=5), load 5 into Register A; PC becomes 0x02

**Cycle 2 — LOAD_B 3:**
- Fetch: IR ← 0x02, PC becomes 0x03
- Decode: opcode 0x02 = LOAD_B; operand follows
- Execute: fetch operand (0x03=3), load 3 into Register B; PC becomes 0x04

**Cycle 3 — ADD:**
- Fetch: IR ← 0x10, PC becomes 0x05
- Decode: opcode 0x10 = ADD; uses Reg A and Reg B
- Execute: ALU computes A + B = 8; result stored in Register A

**Cycle 4 — STORE:**
- Fetch: IR ← 0x30, PC becomes 0x06
- Decode: opcode 0x30 = STORE; address follows
- Execute: fetch address (0x08); write Register A (8) to memory[0x08]

After 4 cycles, memory[0x08] = 8. The computation 5 + 3 = 8 is complete.

---

### The Role of the Control Unit

The **Control Unit (CU)** is the conductor of this orchestra. It:
- Generates all timing and control signals
- Tells the ALU which operation to perform
- Opens and closes the gates that route data between registers and memory
- Manages the PC increment and jump logic
- Handles exceptions (invalid instruction, division by zero, memory fault)

The CU does not compute. It directs the components that do.

Two implementations: **hardwired control** (logic gates implementing the state machine — fast, inflexible) and **microprogrammed control** (a small internal ROM of microinstructions — slower, but easy to modify and extend).

---

### Clock Speed and IPC

The FDE cycle is driven by a clock. Modern CPUs run at 3–6 GHz — 3 to 6 billion clock cycles per second. But a single instruction often takes multiple cycles (memory accesses are slow). The key performance metric is not just clock speed but **IPC — Instructions Per Clock**.

Modern superscalar CPUs execute multiple instructions per clock using **pipelining**: while one instruction is in the Execute stage, the next is in Decode, and the one after is being Fetched — simultaneously. A 4-stage pipeline theoretically achieves 4× throughput.

This is why modern CPUs have performance figures like "4.5 GHz × 6 IPC = 27 billion instruction-equivalents per second."

---

## The Concept: State Drives Computation

The FDE cycle is a **finite state machine**. The state is:
- The contents of all registers (PC, IR, MAR, MDR, general-purpose registers)
- The contents of memory
- The current phase (Fetch / Decode / Execute)

Given any state, the next state is completely determined by the current instruction and the control unit's logic. There is no randomness, no ambiguity — just deterministic state transitions at clock speed.

This determinism is what makes debugging possible, what makes programs reliable, and what makes the behaviour of software predictable from its source code.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Single-Step FDE Tracer**
- A toy CPU with 4 registers (A, B, C, PC) and 16 bytes of memory
- A small program is pre-loaded into memory
- Click "Step" to execute one FDE cycle at a time
- Watch PC, IR, registers, and memory update in real time
- Each step shows which sub-phase is active (Fetch / Decode / Execute)

**Tool 2 — Write Your Own Program**
- Enter opcodes and operands directly into the memory array
- Run your program step by step or in auto mode
- Observe how instruction sequencing controls the flow

**Tool 3 — Pipeline Visualiser**
- See 4 instructions flowing through a 4-stage pipeline simultaneously
- Observe how a branch instruction causes a pipeline flush
- Compare throughput: pipelined vs non-pipelined

---

## Going Deeper

**Exceptions and interrupts**: What happens if an instruction is invalid, or a divide-by-zero occurs? The control unit detects the fault, saves the current PC, and jumps to a **fault handler** — a special piece of code that decides how to respond. This is how operating systems catch and handle program errors.

**Branch prediction**: Jump instructions are a problem for pipelining — the CPU doesn't know the next instruction until it executes the jump. Modern CPUs **predict** the branch direction and speculatively fetch instructions along the predicted path. If the prediction is wrong, the pipeline is flushed and the CPU restarts from the correct address. Good branch predictors achieve >99% accuracy.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Manually trace a 6-instruction program through the FDE cycle, predict register and memory states at each step, answer questions about the Program Counter, and identify what goes wrong when a branch misprediction occurs.
