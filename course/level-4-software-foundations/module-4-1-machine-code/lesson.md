# Module 4.1 — Machine Code and Assembly Language

---

## The Problem

> You can now build a CPU and execute instructions from memory.
> The CPU understands binary — 0x01 0x05 means "load the value 5 into register A."
>
> But nobody writes programs in hex bytes.
>
> How did programmers get from "a CPU that reads binary" to "a Python script you can write in plain English"?
>
> The first step up from raw binary is **assembly language** — and the tool that bridges them is the **assembler**.

Every high-level program you will ever write sits atop a chain of translations. Understanding the first link in that chain — from human-readable mnemonics to machine binary — is essential for understanding everything above it.

---

## The Story

### The First Programmers Had No Language

ENIAC (1945) was programmed by physically rewiring the machine. There were no instructions in memory — the circuit topology *was* the program. Changing the program meant changing the hardware.

The stored-program computer (1948–1949) was the breakthrough: programs could be loaded into memory as data. But the first stored programs were still written as raw binary numbers. Programmers kept notebooks mapping opcodes to numbers. A single typo in a binary string produced a program that crashed silently or produced wrong results with no indication of where.

**Kathleen Booth** (1947) and **David Wheeler** (1949) at Cambridge are among the earliest people credited with writing what we would today recognise as assembly language — symbolic mnemonics like `ADD` and `JMP` that a secondary program (the assembler) would translate into binary.

The insight was simple but profound: **let the computer do the translation**. Write in symbols; let a program convert them to numbers.

---

### The Compilation Pipeline

Modern programs go through multiple translation stages before the CPU can execute them:

```
Source code (.c, .py, .rs)
       ↓  Preprocessor
Preprocessed source
       ↓  Compiler
Assembly code (.s / .asm)
       ↓  Assembler
Object code (.o / .obj)  ← machine code + relocation metadata
       ↓  Linker
Executable (.exe / ELF binary)  ← ready to load
       ↓  Loader (OS)
Process in memory  ← CPU executes this
```

**Preprocessor** — expands macros, includes header files, strips comments  
**Compiler** — translates high-level code to assembly (register allocation, optimisation)  
**Assembler** — translates assembly mnemonics to binary machine code  
**Linker** — combines multiple object files, resolves symbol references, produces one executable  
**Loader** — the OS reads the executable, allocates memory, copies segments into place, sets PC to entry point

---

### What Machine Code Looks Like

x86-64 machine code is variable-length. Here is the same simple computation in three representations:

```c
// C source
int x = 5;
int y = 3;
int z = x + y;
```

```nasm
; x86-64 Assembly (AT&T syntax)
movl  $5, -4(%rbp)      ; x = 5  (store 5 at stack slot)
movl  $3, -8(%rbp)      ; y = 3
movl  -4(%rbp), %eax    ; load x into eax
addl  -8(%rbp), %eax    ; eax = eax + y
movl  %eax, -12(%rbp)   ; z = eax
```

```
; Machine code (hex bytes)
C7 45 FC 05 00 00 00    ; movl $5, -4(%rbp)
C7 45 F8 03 00 00 00    ; movl $3, -8(%rbp)
8B 45 FC                ; movl -4(%rbp), %eax
03 45 F8                ; addl -8(%rbp), %eax
89 45 F4                ; movl %eax, -12(%rbp)
```

The CPU executes the bottom representation. The middle is what a human can read. The top is what an application programmer writes.

---

### Anatomy of an Assembly Instruction

```
label:    mnemonic    operand1, operand2    ; comment
```

**Label** — optional name for this address. Used as jump targets and function names.  
**Mnemonic** — the instruction name: MOV, ADD, SUB, JMP, CALL, RET, etc.  
**Operands** — what the instruction operates on:
  - Immediate: `$5` (literal value)
  - Register: `%rax`, `%rbx` (CPU register)
  - Memory: `-4(%rbp)` (address = rbp − 4)

**Two syntax flavours:**
- **Intel syntax** (Windows, NASM): `mov rax, 5` — destination first
- **AT&T syntax** (Linux, GAS): `movq $5, %rax` — source first, register prefixed with %

---

### Real x86-64 Registers

| Register | 64-bit | 32-bit | Purpose |
|---|---|---|---|
| Accumulator | `rax` | `eax` | Return values, arithmetic |
| Base | `rbx` | `ebx` | General purpose |
| Counter | `rcx` | `ecx` | Loop counter |
| Data | `rdx` | `edx` | I/O, multiply/divide |
| Stack Pointer | `rsp` | `esp` | Top of stack |
| Base Pointer | `rbp` | `ebp` | Stack frame base |
| Instruction Pointer | `rip` | `eip` | Current instruction address |
| Source Index | `rsi` | `esi` | String source |
| Dest Index | `rdi` | `edi` | String dest, arg 1 (Linux ABI) |
| R8–R15 | — | — | General purpose (64-bit only) |

---

### Hello World in Assembly (x86-64 Linux)

```nasm
; hello.asm — NASM syntax, x86-64 Linux
section .data
    msg db "Hello, World!", 10   ; 10 = newline character
    len equ $ - msg              ; length = current position minus msg label

section .text
    global _start

_start:
    ; write(1, msg, len)  — syscall number 1 = write
    mov rax, 1          ; syscall: write
    mov rdi, 1          ; fd: stdout (1)
    mov rsi, msg        ; pointer to message
    mov rdx, len        ; length of message
    syscall             ; invoke kernel

    ; exit(0)  — syscall number 60 = exit
    mov rax, 60         ; syscall: exit
    mov rdi, 0          ; exit code: 0 (success)
    syscall
```

This is the bedrock. Every `print("Hello")` in Python eventually produces a sequence of operations equivalent to this — layers of abstraction translate the readable to the executable.

---

### The Assembler's Job

An assembler makes two passes through the source:

**Pass 1 — Symbol table construction:**
- Record the address of every label
- Compute the size of every instruction
- Build a table: `{label → address}`

**Pass 2 — Code generation:**
- For each instruction, look up the opcode encoding
- Substitute label references with actual addresses
- Emit the binary bytes

The output is an **object file** — machine code with *relocation entries*: placeholders that the linker will fill in when it knows the final layout of all combined object files.

---

## The Concept: Every High-Level Construct Has an Assembly Equivalent

```c
// if statement
if (x > 0) { y = 1; }

; Assembly equivalent
cmp   eax, 0          ; compare x (in eax) with 0
jle   skip            ; jump if x ≤ 0 (skip the body)
mov   [y], 1          ; y = 1
skip:
```

```c
// for loop
for (int i = 0; i < 10; i++) { sum += i; }

; Assembly equivalent
mov   ecx, 0          ; i = 0
loop_start:
cmp   ecx, 10         ; i < 10?
jge   loop_end        ; if not, exit
add   eax, ecx        ; sum += i
inc   ecx             ; i++
jmp   loop_start
loop_end:
```

Every `if`, `for`, `while`, function call, and return in every language compiles to this style of pattern. The patterns are universal; only the syntax differs between architectures.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Assembly to Machine Code**
- Enter x86-like assembly mnemonics (simplified set)
- Watch the assembler produce hex bytes, one instruction at a time
- See the two-pass process: symbol table then code

**Tool 2 — Compilation Pipeline Visualiser**
- Input a short C snippet
- Step through: C source → preprocessed → assembly → machine code bytes
- Observe which compiler transformations happen at each stage

**Tool 3 — Disassembler**
- Enter hex bytes
- Watch them get decoded back into mnemonics
- Understand that machine code is always reversible to assembly (the data is all there)

---

## Going Deeper

**Calling conventions and the ABI**: Assembly doesn't enforce any rules about how functions pass arguments or return values. The **Application Binary Interface (ABI)** is the platform convention that everyone agrees to follow. On Linux x86-64: first 6 integer arguments go in `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`. Return value in `rax`. Stack 16-byte aligned at `CALL`. These rules let code compiled by different compilers (and different languages) call each other. Module 4.2 covers this in depth.

**Inline assembly in C**: Sometimes a programmer needs to write assembly inside a C program — for hardware-specific operations, maximum performance, or features the compiler can't generate. In GCC: `asm("instruction" : outputs : inputs : clobbers);`. Widely used in OS kernels.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Translate C snippets to assembly, encode assembly instructions to hex, trace the two-pass assembler, and identify what the linker does with unresolved symbols.
