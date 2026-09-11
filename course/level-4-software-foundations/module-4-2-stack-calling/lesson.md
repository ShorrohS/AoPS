# Module 4.2 — The Stack and Calling Conventions

---

## The Problem

> You can write assembly instructions.
> You know how to jump to a label.
>
> But how do functions work at the machine level?
> How does a function receive its arguments?
> How does it return a value?
> How does it return to *exactly where it was called from* — even when functions call other functions?
>
> The answer is the **stack** — and the rules that govern its use are the **calling convention**.

Without the stack, you cannot have functions. Without functions, you cannot have programs longer than a few dozen lines. The stack is the structural foundation on which all procedural programming rests.

---

## The Story

### The Problem of Return Addresses

Suppose function A calls function B, which calls function C. Each call must eventually return to exactly the right place. How?

The naive solution: store the return address in a fixed register. But if B calls C, B's return address gets overwritten. The solution to nested calls is a **stack** — a last-in, first-out structure that grows as calls nest and shrinks as they return.

The stack was invented independently by several people in the early 1950s. **Friedrich Bauer** and **Klaus Samelson** in Germany, **Charles Leonard Hamblin** in Australia, and others all recognised that a pushdown automaton could solve the nested-call problem elegantly. By the late 1950s, the call stack was universal.

---

### The Stack in Hardware

The x86-64 stack is a region of memory that grows **downward** (toward lower addresses). Two registers manage it:

**RSP (Stack Pointer)** — always points to the current top of the stack (the most recently pushed value). Lower RSP = more stack used.

**RBP (Base Pointer / Frame Pointer)** — points to the base of the **current stack frame**. Fixed while a function executes, allowing stable access to local variables and parameters regardless of what RSP does.

**PUSH instruction:**
```nasm
push rax     ; RSP -= 8; memory[RSP] = rax
```

**POP instruction:**
```nasm
pop rbx      ; rbx = memory[RSP]; RSP += 8
```

The stack is not a special hardware structure — it is ordinary memory, accessed through a convention. Any memory region could be a stack if you use it this way.

---

### The CALL and RET Instructions

**CALL target:**
```nasm
; equivalent to:
push rip + instruction_size   ; save return address (next instruction)
jmp target                    ; jump to function
```

**RET:**
```nasm
; equivalent to:
pop rip       ; restore return address
; (CPU resumes execution at the saved address)
```

This is how nested calls work. Each CALL pushes a return address. Each RET pops and jumps to it. They interleave correctly because of LIFO order:

```
main calls A    → stack: [main_ret]
A    calls B    → stack: [main_ret, A_ret]
B    calls C    → stack: [main_ret, A_ret, B_ret]
C    returns    → pops B_ret, resumes in B
B    returns    → pops A_ret, resumes in A
A    returns    → pops main_ret, resumes in main
```

---

### The Stack Frame

When a function is called, it creates a **stack frame** — a region of the stack containing:
1. The saved return address (pushed by CALL)
2. The saved RBP (pushed by the function prologue)
3. Local variables (allocated by subtracting from RSP)
4. Saved registers (if the function uses callee-saved registers)

**Standard function prologue (x86-64):**
```nasm
push rbp          ; save caller's frame pointer
mov  rbp, rsp     ; set frame pointer to current stack top
sub  rsp, N       ; allocate N bytes for locals
```

**Standard function epilogue:**
```nasm
mov  rsp, rbp     ; restore stack pointer (deallocate locals)
pop  rbp          ; restore caller's frame pointer
ret               ; pop return address and jump
```

After the prologue, local variables live at negative offsets from RBP:
```
[rbp - 4]  → local int a
[rbp - 8]  → local int b
[rbp - 12] → local int c
```

And the saved return address and caller's RBP live above RBP:
```
[rbp + 8]  → return address (pushed by CALL)
[rbp + 0]  → saved RBP (pushed by prologue)
[rbp - 4]  → first local variable
```

---

### Calling Conventions — The Rules Everyone Agrees On

A **calling convention** is the agreement between caller and callee about:
- Which registers hold function arguments
- Which register holds the return value
- Which registers the callee must preserve (callee-saved)
- Which registers the callee may destroy (caller-saved)
- How the stack must be aligned

**Linux x86-64 (System V AMD64 ABI):**

| Purpose | Registers |
|---|---|
| Integer arguments 1–6 | `rdi, rsi, rdx, rcx, r8, r9` |
| Floating-point args 1–8 | `xmm0–xmm7` |
| Return value | `rax` (integer), `xmm0` (float) |
| Callee-saved | `rbx, rbp, r12–r15` (must restore) |
| Caller-saved | `rax, rcx, rdx, rsi, rdi, r8–r11` (may be destroyed) |
| Stack alignment | RSP must be 16-byte aligned at CALL site |

**Windows x64 ABI (different!):**
- First 4 integer args: `rcx, rdx, r8, r9`
- 32-byte "shadow space" on stack required by callee
- Different callee/caller-saved register split

This is why Windows DLLs and Linux shared libraries are binary-incompatible even on the same CPU.

---

### A Complete Function Call Example

```c
// C
int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(3, 4);
    return 0;
}
```

```nasm
; Linux x86-64 — what the compiler generates

add:
    push rbp
    mov  rbp, rsp
    ; a is in edi (first arg), b is in esi (second arg)
    mov  eax, edi       ; eax = a
    add  eax, esi       ; eax = a + b
    pop  rbp
    ret                 ; return value is in eax

main:
    push rbp
    mov  rbp, rsp
    sub  rsp, 16        ; allocate space for local 'result'
    mov  edi, 3         ; first arg = 3
    mov  esi, 4         ; second arg = 4
    call add            ; call add(3, 4)
    mov  [rbp-4], eax   ; result = return value
    mov  eax, 0         ; return 0
    pop  rbp
    ret
```

---

### Stack Overflow and Buffer Overflows

**Stack overflow**: when recursive function calls nest so deeply that RSP runs out of stack space and crashes into other memory. Default stack size is typically 1–8 MB. An infinite recursive function will always stack overflow.

**Buffer overflow**: when a local array on the stack is written past its end, corrupting adjacent stack data — potentially overwriting the saved return address. If an attacker controls what the return address is overwritten with, they can redirect execution to arbitrary code. This is one of the oldest and most dangerous classes of security vulnerabilities. Modern defences: stack canaries, ASLR, non-executable stack (NX bit).

---

## The Concept: The Stack Enforces Scope

The stack's LIFO property naturally enforces the nesting of function calls. A function's local variables appear when it is called and disappear when it returns — exactly corresponding to lexical scope in high-level languages.

This is why local variables in C are "on the stack" and go away when the function returns. It is not a design decision — it is a direct consequence of how the call stack works.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Stack Frame Visualiser**
- Watch the stack grow and shrink as functions are called and returned
- Step through a main→add→multiply call chain
- See RSP and RBP update, local variables appear and disappear

**Tool 2 — Calling Convention Explorer**
- Enter a function signature (arguments + return type)
- See which registers receive which arguments per Linux ABI
- Observe what happens when a 7th argument is needed (goes on stack)

**Tool 3 — Stack Overflow Demonstrator**
- A recursive function with no base case
- Watch the stack grow frame by frame until it crashes
- Observe how a stack canary would detect the overflow

---

## Going Deeper

**Tail call optimisation (TCO)**: if a function's last action is a call to another function, the compiler can reuse the current stack frame instead of creating a new one. This makes certain recursive algorithms (tail-recursive) use O(1) stack space instead of O(n). Functional languages (Scheme, Haskell) rely on TCO for their looping idioms.

**Debugging with stack traces**: when a crash occurs, the debugger walks the chain of saved RBP values to reconstruct the sequence of function calls that led to the crash. This is the "stack trace" or "backtrace" you see in error messages. Frame pointers (RBP) are essential for reliable stack unwinding — which is why performance-sensitive code that omits them (`-fomit-frame-pointer`) makes debugging harder.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace function call sequences through the stack, compute frame layouts, identify callee/caller-saved registers, and analyse a buffer overflow scenario.
