# Module 5.1 — C: Close to the Metal

---

## The Problem

> Assembly language gives you full control over the hardware.
> But assembly is architecture-specific: x86-64 assembly won't run on ARM.
> Writing an operating system, a compiler, or a database in pure assembly means rewriting it for every CPU.
>
> In 1972, Dennis Ritchie at Bell Labs asked:
> *Can we have a language that is portable across hardware but still compiles down to efficient machine code with no hidden overhead?*
>
> The answer was **C** — and it changed computing permanently.

C sits at the exact boundary between human-readable and machine-executable. Every concept in C maps directly to a small number of machine instructions. There is no garbage collector, no runtime, no virtual machine. If you write `x++`, the CPU executes one instruction. This is why C is called "portable assembly."

---

## The Story

### Why C Was Invented

Before C, operating systems were written in assembly. The PDP-7 version of Unix (1969) was written entirely in assembly. Porting it to a new machine meant rewriting every line.

Ritchie's predecessor language, **B** (1969), was portable but too slow for OS work — it had no types, so every operation treated data as machine words, requiring extra work to handle bytes or floats.

C added:
- **Types**: `int`, `char`, `float`, `struct` — the compiler uses type information to generate correct machine code without programmer overhead
- **Structs**: group related data into a single compound type
- **Pointers**: explicit memory addresses — full hardware access
- **Arrays**: contiguous memory blocks with typed access

In 1973, the Unix kernel was rewritten in C. This was the first major operating system written in a high-level language. It could now be ported to new hardware in weeks instead of years. This single decision — rewriting Unix in C — is why C became universal.

---

### The Compilation Pipeline (Review)

```
Source (.c)  →  Preprocessor  →  Compiler  →  Assembler  →  Linker  →  Executable
```

**Preprocessor** (`cpp`): expands `#include`, `#define`, `#ifdef`. Produces pure C.  
**Compiler** (`cc1`): translates C to assembly. Performs optimisation.  
**Assembler** (`as`): translates assembly to object code (`.o`).  
**Linker** (`ld`): combines object files, resolves symbols, produces final binary.

Understanding this pipeline explains why a missing semicolon in `foo.c` can produce an error message referencing `foo.h` — the preprocessor merged them first.

---

## The Concept

### Pointers — The Core of C

A **pointer** is a variable that holds a memory address.

```c
int  x = 42;      // x is an int stored at some address
int *p = &x;      // p holds the address of x (& = "address of")
int  y = *p;      // y = the value at address p (* = "dereference")
*p = 100;         // write 100 to the address p points to → x is now 100
```

This is not abstraction — this is exactly what the CPU does. `p` contains a 64-bit integer that happens to be a memory address. The dereference `*p` compiles to a single `MOV` instruction using an indirect addressing mode.

**Why pointers matter:**
- Pass large data to functions without copying (pass by reference)
- Build dynamic data structures (linked lists, trees) that grow at runtime
- Interface with hardware registers (embedded systems)
- Implement your own memory allocator

**Common pointer mistakes:**
- **Null pointer dereference**: `int *p = NULL; *p = 5;` → segfault
- **Dangling pointer**: pointer to memory that has been freed
- **Buffer overrun**: writing past the end of an array via pointer arithmetic
- **Memory leak**: allocating with `malloc()` without ever calling `free()`

### Memory Allocation

C has two kinds of memory:

**Stack** — automatic, managed by the compiler:
```c
void fn() {
    int x = 5;      // allocated on stack when fn() called
    char buf[64];   // 64 bytes on stack
}                   // all freed when fn() returns
```

**Heap** — manual, managed by the programmer:
```c
int *arr = malloc(100 * sizeof(int));  // allocate 400 bytes
if (arr == NULL) { /* handle error */ }
arr[0] = 42;        // use it
free(arr);          // you must free it — no garbage collector
arr = NULL;         // good practice: clear the pointer after free
```

This manual memory management is what makes C fast and dangerous simultaneously. No GC pause, but also no safety net.

### Structs — User-Defined Types

```c
struct Point {
    int x;
    int y;
};

struct Point p1;
p1.x = 10;
p1.y = 20;

struct Point *pp = &p1;
pp->x = 30;          // arrow operator: (*pp).x = 30
```

Structs are laid out contiguously in memory. `struct Point` occupies 8 bytes: 4 for x, 4 for y. The compiler may add **padding bytes** to ensure alignment rules are met, which is why `sizeof(struct)` can surprise you.

### Functions and the Call Stack

C functions map directly to the calling convention from Module 4.2:

```c
int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(3, 4);  // a→rdi, b→rsi; return→rax
    return 0;
}
```

Recursion works naturally because each call gets its own stack frame:

```c
int factorial(int n) {
    if (n <= 1) return 1;         // base case
    return n * factorial(n - 1);  // recursive case
}
```

### Building a Memory Allocator

To truly understand C, you build a simplified `malloc()`. The core idea:

```c
// A minimal slab allocator — conceptual sketch
static char heap[65536];  // 64 KB of pretend heap
static int  top = 0;      // current allocation pointer

void *my_malloc(int size) {
    if (top + size > sizeof(heap)) return NULL;  // out of memory
    void *ptr = &heap[top];
    top += size;
    return ptr;
}
// (No free() in this sketch — a real allocator needs a free list)
```

A real `malloc()` implementation (like `ptmalloc` in glibc) manages a free list of blocks, coalesces adjacent free blocks, and calls `brk()`/`mmap()` to request more memory from the OS when needed.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Pointer Visualiser**
- Declare variables and take their addresses
- Watch memory addresses appear in the pointer variable
- Dereference pointers and observe the value change at the target address

**Tool 2 — Stack vs Heap**
- Call a function and watch local variables appear on the stack
- Call `malloc()` and watch a heap block get allocated
- Call `free()` and watch it get released
- Introduce a memory leak — observe that freed status shows the block is still in memory

**Tool 3 — Build a Linked List**
- Use `malloc()` to allocate nodes
- Link them together using pointer fields
- Traverse the list following pointers
- Free them one by one and watch heap usage drop

---

## Going Deeper

**undefined behaviour**: C has a large category of operations that are "undefined behaviour" (UB) — the language standard makes no guarantee about what happens. Signed integer overflow, reading uninitialised memory, modifying a string literal: all UB. The compiler is allowed to assume UB never happens, which means it can and does optimise away code that would prevent UB from being exploited. This is a major source of security vulnerabilities. Tools like AddressSanitizer and UBSanitizer catch UB at runtime during development.

**C in 2024**: Despite being 50+ years old, C is still the primary language for operating system kernels (Linux, Windows, macOS, iOS), embedded systems (microcontrollers), and anywhere that raw performance and minimal runtime overhead are required. Every Python interpreter, every JavaScript engine, every database is written substantially in C or C++.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace pointer operations through memory, find and fix a memory leak, implement `strlen()` without any library functions, and reason about struct padding.
