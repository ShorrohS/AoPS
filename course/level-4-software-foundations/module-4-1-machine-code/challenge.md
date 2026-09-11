# Challenge 4.1 — Machine Code and Assembly Language

**Type:** Translation + encoding + trace + reasoning  
**Estimated time:** 45–55 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — C to Assembly

Translate each C snippet into assembly using the toy ISA from Level 3 (or simplified x86-like pseudocode). Show register assignments and every instruction required.

1. `int x = 10; int y = 4; int z = x - y;` → Translate to assembly. Where is z stored?

2. `if (a > b) { result = a; } else { result = b; }` — Translate to assembly. Use CMP and conditional jumps. (This is `max(a, b)`.)

3. The following loop: `int sum = 0; for (int i = 1; i <= 5; i++) { sum += i; }` — Translate to assembly. Which register holds sum, which holds i?

4. A function call: `int square(int n) { return n * n; }` — In which register does the argument arrive (Linux x86-64 ABI)? In which register must the result be placed before RET?

---

## Part B — Encode to Hex

Using this simplified encoding table:

| Mnemonic | Encoding |
|---|---|
| MOV reg, imm | 0xB8 + reg_num, then 4-byte little-endian immediate |
| ADD reg, reg | 0x01, ModRM byte |
| SUB reg, reg | 0x29, ModRM byte |
| CMP reg, imm | 0x83 reg_ext/7, ModRM, imm8 |
| JMP rel8 | 0xEB, signed offset byte |
| JE  rel8 | 0x74, signed offset byte |
| JNE rel8 | 0x75, signed offset byte |
| CALL rel32 | 0xE8, 4-byte signed offset |
| RET | 0xC3 |
| NOP | 0x90 |

5. Encode: `MOV eax, 5` (reg_num for eax = 0)
6. Encode: `RET` then `NOP` then `NOP`
7. Encode: `JMP +3` (jump forward 3 bytes from the byte after the JMP instruction)
8. Why does x86 store multi-byte immediates in **little-endian** order? What would `MOV eax, 0x0000_0005` look like in little-endian hex?

---

## Part C — Two-Pass Assembler Trace

The following assembly program is fed to a two-pass assembler. Address counter starts at 0x00. Assume all instructions are 3 bytes except JMP (2 bytes) and HALT (1 byte).

```
start:  LOAD A, 10      ; 3 bytes
        LOAD B, 3       ; 3 bytes
        SUB  A, B       ; 3 bytes
loop:   ADD  A, 1       ; 3 bytes
        JMP  done       ; 2 bytes — forward reference!
        ADD  A, 99      ; 3 bytes  (dead code, never reached)
done:   HALT            ; 1 byte
```

9. **Pass 1**: Build the symbol table. What address does each label map to?

10. **Pass 2**: The `JMP done` instruction is at address 0x0C. `done` is at address 0x12. The JMP encoding uses a **relative** offset: offset = target_address − (JMP_address + 2). Calculate the offset byte that gets encoded into the JMP instruction.

11. What is a **forward reference**? Why does the two-pass approach solve it?

12. If the assembler made only **one pass**, how could it handle the `JMP done` forward reference? What is the common technique used?

---

## Part D — Linker and Object Files

Two object files are produced:

**math.o** exports the symbol `add_two` at local address 0x00.  
**main.o** imports `add_two` (uses it with a CALL instruction) at its local address 0x10.

The linker places `main.o` starting at 0x1000 and `math.o` starting at 0x2000.

13. What is the final (linked) address of `add_two`?

14. The CALL instruction in `main.o` used a placeholder address of 0x00000000. What value does the linker patch it to? (CALL uses a relative offset on x86: offset = target − (call_site + 5))

    The CALL instruction is at linked address 0x1010.

15. What is a **symbol table** in an object file? What is a **relocation table**? How do they work together during linking?

---

## Part E — Disassembly

Decode these x86-64 hex bytes into mnemonics. Use the encoding table from Part B.

```
B8 07 00 00 00    ; ?
B9 03 00 00 00    ; ?
90                ; ?
C3                ; ?
```

16. What value is in `eax` after the first instruction? In `ecx` after the second?
17. B8 = MOV eax, ...; B9 = MOV ecx, .... The register number is encoded in the low 3 bits of the opcode. B8 = 0xB8 + 0 (eax). What opcode would `MOV ebx, 7` use? (ebx = register 3)
18. What does a disassembler do that an assembler does not? Why is disassembly always possible for machine code but **compilation** from assembly to C is not?

---

## Rubric

| Part | Points |
|------|--------|
| A C→assembly (4 questions) | 24 |
| B hex encoding (4 questions) | 20 |
| C two-pass trace (4 questions) | 24 |
| D linker (3 questions) | 18 |
| E disassembly (3 questions) | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A answers</summary>

**A1:**
```
MOV eax, 10    ; x = 10
MOV ebx, 4     ; y = 4
SUB eax, ebx   ; eax = x - y = 6 → z
MOV [z], eax   ; store z in memory
```

**A2 (max function):**
```
CMP eax, ebx    ; compare a, b
JLE else_branch ; if a ≤ b, goto else
MOV [result], eax ; result = a
JMP done
else_branch:
MOV [result], ebx ; result = b
done:
```

**A3 (loop):**
```
MOV eax, 0     ; sum = 0
MOV ecx, 1     ; i = 1
loop_start:
CMP ecx, 5     ; i <= 5?
JG  loop_end
ADD eax, ecx   ; sum += i
INC ecx        ; i++
JMP loop_start
loop_end:
; eax = 15
```

**A4:** Argument `n` arrives in `rdi` (Linux x86-64 ABI, first argument). Result must be in `rax` before `RET`.
```
; square(n): n in rdi
MOV rax, rdi    ; rax = n
IMUL rax, rdi   ; rax = n * n
RET             ; return rax
```
</details>

<details>
<summary>Part B answers</summary>

5. `MOV eax, 5`: B8 05 00 00 00 (opcode 0xB8+0=0xB8, then 5 in 4 bytes LE = 05 00 00 00)

6. `RET NOP NOP`: C3 90 90

7. `JMP +3`: EB 03 (offset = 3, jumps 3 bytes past the byte after JMP)

8. Little-endian stores the **least significant byte first**. `MOV eax, 5` = B8 **05 00 00 00** — the 05 (value 5) is at the lowest address. This matches x86's memory byte ordering. A big-endian encoding would be B8 00 00 00 05.
</details>

<details>
<summary>Part C — two-pass trace</summary>

**Pass 1 — symbol table:**
```
start → 0x00  (LOAD A,10 starts at 0)
        0x03  (LOAD B,3)
        0x06  (SUB A,B)
loop  → 0x09  (ADD A,1)
        0x0C  (JMP done) ← 2 bytes
        0x0E  (ADD A,99)
done  → 0x11  (HALT)
```

10. Offset = 0x11 − (0x0C + 2) = 0x11 − 0x0E = 0x03. The JMP encodes as `JMP 0x03` meaning "jump 3 bytes forward from the next instruction."

11. A forward reference is a label used before it is defined (e.g., jumping to `done` before the assembler has seen `done:`). Two-pass: Pass 1 records all labels and their addresses. Pass 2 can resolve all references because the symbol table is complete.

12. **Backpatching**: in a single pass, the assembler emits a placeholder (e.g., 0x00) for unknown forward references, records the location, and patches it after the whole file is processed. Functionally equivalent to two-pass but more complex to implement correctly.
</details>

<details>
<summary>Part D — linker</summary>

13. `add_two` is at math.o local 0x00, placed at 0x2000 → **final address: 0x2000**

14. CALL at linked 0x1010. Offset = target − (call_site + 5) = 0x2000 − (0x1010 + 5) = 0x2000 − 0x1015 = **0x0FEB**. Linker patches the 4-byte placeholder with 0xEB 0x0F 0x00 0x00 (little-endian).

15. **Symbol table**: maps exported names to their local addresses in the object file. **Relocation table**: lists locations in the code that contain addresses needing adjustment when the file is placed at its final linked address. During linking: the linker places all object files at their final addresses, then uses each relocation entry to patch the corresponding address in the code with the correct final value.
</details>

<details>
<summary>Part E</summary>

16. `B8 07 00 00 00` → `MOV eax, 7` → eax = **7**. `B9 03 00 00 00` → `MOV ecx, 3` → ecx = **3**.

17. `MOV ebx, 7`: ebx is register 3. Opcode = 0xB8 + 3 = **0xBB**. Full: `BB 07 00 00 00`.

18. A disassembler decodes bytes back to mnemonics — this always works because the encoding is deterministic and complete. **Decompilation** (machine code → C) is not reliably possible because: variable names, type information, high-level control structures, and comments are all destroyed during compilation. Multiple C programs can compile to identical machine code. Disassembly is lossless in structure; decompilation is not.
</details>
