# Challenge 4.2 — The Stack and Calling Conventions

**Type:** Trace + layout + reasoning + security  
**Estimated time:** 50–60 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Setup

Stack grows downward. Initial RSP = 0x7FFF0000. Each push decrements RSP by 8 (64-bit). Each pop increments RSP by 8. All values are 64-bit (8 bytes).

---

## Part A — Stack Trace

Trace the stack contents after each instruction sequence. Show RSP value and what is at each stack address.

```nasm
; Initial: RSP = 0x7FFF0000

push  rax      ; rax = 0x0000000A (10)
push  rbx      ; rbx = 0x00000005 (5)
push  rcx      ; rcx = 0x00000003 (3)
pop   rdx
pop   rsi
```

1. After all 5 instructions, what is: RSP? rdx? rsi? What remains on the stack?

2. After `call function_A` (which pushes the return address 0x401020), what is RSP? What is at that address?

3. Inside function_A:
```nasm
push  rbp           ; save caller's rbp (rbp = 0x7FFF0100)
mov   rbp, rsp
sub   rsp, 16       ; allocate 2 × 8 bytes for locals
```
Draw the stack layout after these three instructions. Label every 8-byte slot with its address and content.

---

## Part B — Frame Layout

A function has this signature and local variables:
```c
int compute(int a, int b, int c) {
    int x = a + b;
    int y = x * c;
    return y;
}
```

Assume Linux x86-64 ABI. The function's prologue:
```nasm
push rbp
mov  rbp, rsp
sub  rsp, 16        ; room for x and y (both 4-byte ints, padded to 16)
```

4. Which registers contain a, b, and c when the function starts (before prologue)?

5. At which offset from RBP are x and y stored? Write out `[rbp - ?]` for each.

6. After the epilogue (`mov rsp, rbp` / `pop rbp` / `ret`), what happens to x and y? Are they "deleted"? What actually happens to those memory addresses?

7. A caller calls `compute(10, 20, 30)`. Show the register state at the moment `compute` begins executing (just before `push rbp`).

---

## Part C — Callee vs Caller Saved

Linux x86-64: callee-saved = {rbx, rbp, r12–r15}. Caller-saved = {rax, rcx, rdx, rsi, rdi, r8–r11}.

8. Function `outer` stores a critical value in `rbx` before calling `inner`. After `inner` returns, can `outer` trust that `rbx` still holds the same value? Why?

9. Function `outer` stores a value in `rdi` before calling `inner`. After `inner` returns, can it trust `rdi`? Why?

10. `outer` needs to preserve the value of `r9` across a call to `inner`. What must `outer` do? Write the assembly instructions.

11. `inner` uses `r12` internally. It did not save and restore it. `outer` had a value in `r12` before calling `inner`. What happens? Is this a bug in `inner` or in `outer`? Explain.

---

## Part D — Call Chain Trace

Three functions: `main` calls `factorial(5)`, which recursively calls `factorial(4)`, ..., `factorial(1)`.

Each call frame is 32 bytes (prologue + one local variable + saved rbp + return address).

12. How many stack frames are on the stack when `factorial(1)` is executing?

13. If the initial RSP is 0x7FFF8000, what is RSP when `factorial(1)` begins? (Each frame = 32 bytes)

14. Each frame holds the return address (8B), saved RBP (8B), and local `n` (8B) + padding (8B). Draw the stack layout showing all 6 frames (main's frame + 5 factorial frames) with addresses and contents.

15. When `factorial(1)` returns, trace the next 4 RET instructions. What value does RSP have after each one?

---

## Part E — Buffer Overflow Analysis

A function contains:
```c
void read_input(char* user_data) {
    char buffer[16];           // 16-byte local buffer on stack
    strcpy(buffer, user_data); // NO bounds checking!
    printf("Got: %s\n", buffer);
}
```

Stack layout inside `read_input` (grows downward from RBP):
```
[rbp - 16]  buffer[0..15]   ← 16 bytes
[rbp +  0]  saved RBP       ← 8 bytes
[rbp +  8]  return address  ← 8 bytes
```

The attacker passes a 32-byte string: 16 bytes of 'A', then 8 bytes of 'B', then the 8-byte value 0xDEADBEEFCAFEBABE.

16. What happens to the saved RBP? What is its new value?

17. What happens to the return address? What address does execution jump to when `read_input` returns?

18. What is a **stack canary**? Where is it placed in the stack frame? How does it detect this overflow?

19. What is **ASLR** (Address Space Layout Randomisation)? Why does it make buffer overflow exploits harder even if an attacker can overflow the return address?

---

## Rubric

| Part | Points |
|------|--------|
| A stack trace | 18 |
| B frame layout | 20 |
| C callee/caller saved | 20 |
| D call chain | 22 |
| E buffer overflow | 20 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A</summary>

After all 5 instructions:

```
push rax (10): RSP = 0x7FFEFFEC, mem[0x7FFEFFEC] = 10
push rbx  (5): RSP = 0x7FFEFFE4, mem[0x7FFEFFE4] = 5
push rcx  (3): RSP = 0x7FFEFFDC, mem[0x7FFEFFDC] = 3
pop rdx:       rdx = 3, RSP = 0x7FFEFFE4
pop rsi:       rsi = 5, RSP = 0x7FFEFFEC
```

RSP = 0x7FFEFFEC. rdx = 3. rsi = 5. Stack still has 10 at 0x7FFEFFEC.

2. After CALL (pushes 0x401020): RSP = 0x7FFEFFE4. mem[0x7FFEFFE4] = 0x401020.

3. Stack after prologue (RSP started at 0x7FFEFFEC − 8 = 0x7FFEFFE4 after CALL):

```
Addr           Content
0x7FFEFFDC     [rbp - 16] local b (uninit)
0x7FFEFFD0     [rbp -  8] local a (uninit)  ← RSP after sub rsp,16
0x7FFEFFC8     [rbp +  0] saved rbp = 0x7FFF0100  ← RBP now points here
0x7FFEFFC0     [rbp +  8] return address = 0x401020
```
(Exact addresses depend on initial RSP; the relative layout is what matters.)
</details>

<details>
<summary>Part C answers</summary>

8. Yes — `rbx` is **callee-saved**. The ABI requires `inner` to preserve it. If `inner` used rbx, it must push it at entry and pop it before returning.

9. No — `rdi` is **caller-saved**. `outer` has no guarantee. If `outer` needs the value in `rdi` after calling `inner`, it must save it (push it to the stack, or move to a callee-saved register) before the call.

10. Outer must save r9 before the call and restore it after:
```nasm
push r9         ; save r9
call inner
pop  r9         ; restore r9
```

11. This is a **bug in `inner`**. r12 is callee-saved: every function that uses it must preserve it. By not saving/restoring r12, inner violates the ABI contract and corrupts outer's data.
</details>

<details>
<summary>Part E — buffer overflow</summary>

16. The 8 bytes of 'B' (0x4242424242424242) overwrite the saved RBP. The saved RBP is corrupted.

17. The 8 bytes 0xDEADBEEFCAFEBABE overwrite the return address. When `read_input` returns, the CPU pops this value as the return address and jumps to 0xDEADBEEFCAFEBABE — almost certainly a segfault, or an exploit if the attacker chose a valid code address.

18. A **stack canary** is a random value placed between the local variables and the saved RBP/return address at function entry:
```
[buffer 16 bytes]
[canary 8 bytes]    ← checked before RET
[saved RBP]
[return address]
```
Before returning, the function checks that the canary matches its original value. A linear overflow of `buffer` must overwrite the canary before reaching the return address. If the canary changed, the program terminates instead of returning to the corrupted address.

19. **ASLR** randomises the base addresses of the stack, heap, and libraries at every run. An attacker who overwrites the return address needs to know a valid code address to jump to. With ASLR, they cannot predict those addresses (they change each execution). This turns a reliable exploit into a guessing attack with astronomically low probability.
</details>
