# Module 3.3 — Instruction Set Architecture (ISA)

---

## The Problem

> The ALU can add, subtract, AND, OR, XOR.
> The FDE cycle can fetch and execute instructions.
> Memory can store and retrieve bytes.
>
> But how does the CPU know *what to do* with a byte like 0x83?
> How does it distinguish "add these two registers" from "load this value" from "jump to that address"?
>
> The answer is the **Instruction Set Architecture** — the contract between hardware and software that defines every operation a CPU can perform.

The ISA is the most important design decision in computer architecture. It is the interface that software speaks and hardware implements. Every program ever compiled targets a specific ISA. Change the ISA and every program must be recompiled or rewritten.

---

## The Story

### The First ISAs

Early computers had no standard instruction set. Each machine had its own unique set of operations, wired directly into its control unit. Writing a program for one machine meant it ran on nothing else. Moving programs between machines meant rewriting them from scratch.

The **IBM System/360** (1964) was the first family of computers to share a common ISA across machines of different speeds and prices. A program written for the cheapest System/360 would run unchanged on the most powerful one. This was revolutionary: **software became an asset that outlasted hardware**.

The System/360 ISA introduced concepts still present in x86-64 today.

---

### What an ISA Defines

An ISA specifies:
1. **Registers** — how many, how wide, which are special
2. **Data types** — integers (8/16/32/64-bit), floats, vectors
3. **Instructions** — every operation the CPU supports
4. **Addressing modes** — how operands are located (immediate, register, memory, indirect)
5. **Instruction encoding** — how instructions are represented as bits
6. **Memory model** — byte order (endianness), alignment rules
7. **Privilege levels** — which instructions only the OS can use
8. **Exception model** — what happens on errors

---

### RISC vs CISC

Two competing philosophies dominate ISA design:

**CISC — Complex Instruction Set Computer**
- Many instructions, some very complex (string copy, matrix operations)
- Instructions of variable length (1–15 bytes on x86)
- Single instruction can do a memory read, an operation, and a memory write
- Fewer instructions needed in programs → smaller code size
- Complex decoder hardware needed
- Examples: Intel x86-64, AMD64

**RISC — Reduced Instruction Set Computer**
- Few, simple instructions — each does exactly one thing
- Fixed instruction length (typically 32 bits)
- Memory access only via explicit load/store instructions
- More instructions needed for complex operations → larger programs
- Simple decoder → easier to pipeline, easier to optimise
- Examples: RISC-V, ARM (modern), MIPS, SPARC

**The modern reality**: ARM processors (RISC) run almost all smartphones and tablets. x86-64 (CISC) runs almost all desktop/laptop/server computing. Apple's M-series chips (ARM RISC) now run high-performance Macs, challenging x86-64 dominance. RISC-V is an open-source ISA gaining traction in embedded and research systems.

*Interesting nuance*: modern x86-64 CPUs internally translate CISC instructions into simpler micro-operations (μops) that look a lot like RISC. The CISC/RISC distinction has blurred at the implementation level, even if the ISA surface remains different.

---

### Addressing Modes

How does an instruction specify where its data comes from? **Addressing modes** are the answer.

**Immediate**: the value is encoded directly in the instruction.
`LOAD A, 42` — loads the literal value 42 into register A.

**Register**: the value is in a register.
`ADD A, B` — adds the value in register B to register A.

**Direct (absolute)**: the value is at a specific memory address.
`LOAD A, [0x1000]` — loads the byte at memory address 0x1000 into A.

**Indirect**: the address of the value is in a register.
`LOAD A, [B]` — loads the byte from the address stored in register B.

**Base + offset**: address = register + constant.
`LOAD A, [B + 4]` — loads from the address (B's value + 4). Used for array indexing and struct field access.

**PC-relative**: address = PC + offset. Used for branch instructions.
`JMP +8` — jump forward 8 bytes from the current PC. Produces position-independent code.

---

### Instruction Encoding

Every instruction must be represented as a pattern of bits. Two main approaches:

**Fixed-length** (RISC): every instruction is exactly 32 bits.
```
RISC-V R-type (32-bit):
[31:25] funct7  [24:20] rs2  [19:15] rs1  [14:12] funct3  [11:7] rd  [6:0] opcode
```
Simple decoder: always knows exactly where each field is.

**Variable-length** (CISC): instructions range from 1 to 15 bytes.
```
x86-64 examples:
NOP:           0x90           (1 byte)
INC  eax:      0xFF 0xC0      (2 bytes)
MOV  rax, imm: 0x48 0xB8 + 8-byte immediate  (10 bytes)
```
Complex decoder: must figure out instruction length before it can decode it. One reason x86 decoders are expensive in silicon area.

---

### Our Toy ISA — 8 Instructions

For this module, we design and use a minimal ISA:

| Opcode (hex) | Mnemonic | Format | Description |
|---|---|---|---|
| 0x01 | LOAD imm | 0x01 rr vv | Load immediate value vv into register rr |
| 0x02 | LOAD_MEM | 0x02 rr aa | Load from memory[aa] into register rr |
| 0x03 | STORE | 0x03 rr aa | Store register rr to memory[aa] |
| 0x10 | ADD | 0x10 r1 r2 | r1 ← r1 + r2 |
| 0x11 | SUB | 0x11 r1 r2 | r1 ← r1 − r2 |
| 0x20 | JMP | 0x20 aa | PC ← aa (unconditional) |
| 0x21 | JZ | 0x21 rr aa | If rr=0: PC ← aa |
| 0xFF | HALT | 0xFF | Stop |

Register encoding: A=0x00, B=0x01, C=0x02, D=0x03

**Example — sum of 1+2+3+4+5:**
```
Address: Bytes:   Meaning:
0x00:    01 00 01  LOAD A, 1        ; accumulator = 1
0x03:    01 01 06  LOAD B, 6        ; loop limit (stop before adding 6)
0x06:    01 02 02  LOAD C, 2        ; next value to add
0x09:    11 01 02  SUB B, C         ; B = B - C (check if done)
0x0C:    21 01 14  JZ B, 0x14       ; if B=0: jump to HALT
0x0F:    10 00 02  ADD A, C         ; A = A + C (accumulate)
0x12:    20 09    JMP 0x09          ; loop back
0x14:    FF       HALT
```

---

### Real ISA: x86-64 Subset

The actual instruction set your computer uses for every program you run:

```nasm
; Load values
MOV rax, 5          ; rax = 5 (immediate)
MOV rbx, [0x1000]   ; rbx = memory[0x1000] (direct)
MOV rcx, [rax]      ; rcx = memory[rax] (indirect)
MOV rdx, [rax + 8]  ; rdx = memory[rax + 8] (base+offset)

; Arithmetic
ADD rax, rbx        ; rax = rax + rbx
SUB rax, 1          ; rax = rax - 1
IMUL rax, rbx       ; rax = rax * rbx (signed multiply)
IDIV rcx            ; rax = rax / rcx, rdx = rax mod rcx

; Comparison and control flow
CMP rax, 0          ; sets flags based on rax - 0 (doesn't modify rax)
JE  label           ; jump if equal (ZF=1)
JNE label           ; jump if not equal
JL  label           ; jump if less (signed)
JMP label           ; unconditional jump
CALL function       ; push PC, jump to function
RET                 ; pop PC (return from function)
```

Every C/C++/Rust/Go program you compile becomes sequences of these instructions.

---

## The Concept: The ISA as Contract

The ISA is the most stable interface in computing. Intel has maintained backward compatibility with the 8086 ISA (1978) through every generation of x86 processor to this day. A program compiled in 1985 for DOS can still run on a 2024 Core i9 (in compatibility mode). This backward compatibility is both a massive commercial advantage (all old software keeps working) and an engineering burden (carrying 46 years of design decisions forward).

ARM's decision to design a clean, simple RISC ISA in the 1980s is why ARM cores are so efficient — they don't carry the weight of 40 years of complexity.

RISC-V represents a third path: a completely open, free ISA designed with modern knowledge, with no legacy baggage. Its adoption in research, embedded systems, and potentially data centres is growing rapidly.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Toy ISA CPU**
- Full implementation of the 8-instruction toy ISA
- Write programs directly in the memory editor (hex opcodes)
- Step through execution or run at speed
- Observe register states and memory after each instruction

**Tool 2 — Instruction Encoder**
- Type a mnemonic instruction (e.g., `ADD A, B`)
- See the binary/hex encoding
- Understand how the CPU's decoder would parse each field

**Tool 3 — Sum 1–5 Challenge**
- Pre-loaded program that computes 1+2+3+4+5
- Step through it and verify each register state
- Modify it to compute 1+2+3+4+5+6+7 instead

---

## Going Deeper

**The ABI (Application Binary Interface)**: Beyond the ISA, software needs conventions for how programs interact. Which register holds the first function argument? How is the stack organised? What is the calling convention? These rules, defined by the platform ABI (e.g., System V AMD64 ABI on Linux), are as important as the ISA itself for software compatibility.

**ISA extensions**: Modern x86-64 CPUs implement dozens of ISA extensions beyond the base set: SSE, AVX, AVX-512 (SIMD vector operations), AES-NI (hardware encryption), SHA extensions. A compiler detects which extensions the target CPU supports and emits the fastest instructions available.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Write and trace programs in the toy ISA, encode instructions into binary, design a new instruction, and reason about RISC vs CISC trade-offs.
