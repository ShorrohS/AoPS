# Module 3.1 — Memory: How Machines Remember

---

## The Problem

> You have an ALU that can add, subtract, and perform logic operations.
> You have registers that hold values for a single clock cycle.
>
> But here is the problem: where do the values come from before they reach the ALU?
> And where do results go after the ALU produces them?
>
> The answer is **memory** — the system that lets a machine remember anything at all.

Without memory, a processor can only react to its current inputs. It cannot store a result, recall a previous value, or execute a program. Memory is what transforms a calculator into a computer.

---

## The Story

### The Human Analogy

A human performing arithmetic uses two types of memory simultaneously:
- **Working memory** — the few numbers held in mind right now (small, fast, volatile)
- **Long-term memory** — everything learned and stored (large, slow, persistent)

Computer memory works the same way, at every scale from a single chip to an entire data centre. The hierarchy exists because of a fundamental physical tradeoff: **fast memory is expensive and small; slow memory is cheap and large.**

Every computer architecture in history has navigated this tradeoff.

---

### From Flip-Flops to Memory Arrays

In Module 2.5 you built a D flip-flop — a single bit of memory. One flip-flop stores one bit.

Eight flip-flops wired together store one byte. That is a **register**.

Now imagine 256 rows of 8 flip-flops each. That is 256 bytes of **SRAM** — Static Random Access Memory. Add an address decoder to select which row to read or write, and you have a functioning memory array.

This is literally how CPU cache memory works today, scaled to millions of cells.

---

### SRAM vs DRAM

**SRAM (Static RAM)** — each bit stored in a flip-flop (6 transistors per bit)
- Fast: access time ~1 nanosecond
- Expensive: large die area
- Used for: CPU registers, L1/L2/L3 cache

**DRAM (Dynamic RAM)** — each bit stored as charge on a capacitor (1 transistor + 1 capacitor per bit)
- Slower: access time ~50–100 nanoseconds
- Cheap: very small cell, high density
- Problem: capacitors leak — must be **refreshed** every ~64 milliseconds
- Used for: main system RAM (DDR4, DDR5)

The "dynamic" in DRAM refers to this need for constant refreshing. If the refresh circuit fails, all data is lost within milliseconds — even with power connected.

---

### The Memory Hierarchy

Modern systems layer memory into a hierarchy based on speed and capacity:

| Level | Type | Size | Speed | Location |
|-------|------|------|-------|----------|
| L0 | CPU Registers | 16–32 × 64-bit | 1 cycle (~0.3 ns) | On-chip |
| L1 | SRAM Cache | 32–64 KB | 4 cycles (~1 ns) | On-chip |
| L2 | SRAM Cache | 256 KB–1 MB | 12 cycles (~4 ns) | On-chip |
| L3 | SRAM Cache | 4–32 MB | 40 cycles (~12 ns) | On-chip |
| RAM | DRAM | 4–64 GB | ~200 cycles (~60 ns) | Off-chip |
| SSD | Flash | 256 GB–4 TB | ~100,000 ns | Off-chip |
| HDD | Magnetic | 1–20 TB | ~10,000,000 ns | Off-chip |

The CPU operates on data in registers. When it needs data not in registers, it looks in L1 cache. On a miss, it checks L2, then L3, then RAM, then disk. Each level is roughly 10–100× slower than the one above.

This is why **cache locality** matters so much in software performance: a program that accesses memory in sequential, predictable patterns keeps data in fast cache. A program that jumps around randomly keeps forcing expensive cache misses to main RAM.

---

### Address Space and Addressability

Every byte in memory has a unique **address** — a number that identifies its location.

For a 32-bit address space: 2³² = 4,294,967,296 addresses = 4 GB maximum.
For a 64-bit address space: 2⁶⁴ = 18,446,744,073,709,551,616 addresses = 16 exabytes.

**Addressability** refers to what unit each address points to. Most modern architectures are **byte-addressable**: each address identifies one byte. Some older or embedded systems are word-addressable (each address identifies 16 or 32 bits).

**Memory map**: not all addresses point to RAM. A typical x86-64 system uses its address space for:
- RAM (the majority)
- Memory-mapped I/O (peripherals that respond to memory read/write)
- BIOS/UEFI ROM
- Graphics framebuffer
- Reserved regions

---

### How a Read Operation Works

When the CPU issues a **read**:
1. CPU places the **address** on the address bus
2. CPU asserts the **read control signal**
3. Memory decodes the address to select the correct row and column
4. Memory places the **data** on the data bus
5. CPU latches the data from the data bus into a register

For DRAM, step 3–4 involves:
- **Row address strobe (RAS)**: selects the row, copies it into a row buffer
- **Column address strobe (CAS)**: selects the column from the row buffer
- CAS latency (CL) is the key DRAM timing spec (e.g., CL16 = 16 clock cycles)

---

### How a Write Operation Works

When the CPU issues a **write**:
1. CPU places the **address** on the address bus
2. CPU places the **data** on the data bus
3. CPU asserts the **write control signal**
4. Memory decodes the address, stores data at that location

---

## The Concept: Memory as an Addressed Array

Think of memory as a post office with numbered mailboxes. Each mailbox (address) holds a fixed-size value (1 byte for byte-addressable memory). The postmaster (address decoder) routes requests to the correct box. Reading opens the box and copies its contents. Writing replaces its contents.

The key abstractions:
- **Address**: which location
- **Data**: what value
- **Control**: read or write

These three signals — address, data, control — form the **memory bus interface**. Everything from a 1980s microprocessor to a modern server uses this same abstraction.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Memory Array Explorer**
- A 16-byte memory array with addresses 0x00–0x0F
- Click any cell to select it; enter a value (0–255) to write
- Use Read/Write buttons to simulate bus operations
- Watch the address bus, data bus, and control signals light up

**Tool 2 — Cache Simulator**
- A small "CPU" requests memory reads in a configurable pattern
- Watch L1 cache hits vs misses
- Try sequential access vs random access — observe the hit rate difference

**Tool 3 — Hierarchy Visualizer**
- Animate a read request propagating through the memory hierarchy
- See the latency accumulate at each cache miss

---

## Going Deeper

**Write-through vs write-back caches**: When the CPU writes to a cached address, does it immediately write to RAM (write-through) or only update the cache and write to RAM later (write-back)? Write-back is faster but more complex — the cache must track which lines are "dirty" (modified but not yet written back). Modern CPUs use write-back with sophisticated coherency protocols.

**Virtual memory**: Programs don't see physical RAM addresses. The CPU's Memory Management Unit (MMU) translates virtual addresses (what the program uses) to physical addresses (where the data actually lives in RAM). This allows isolation between processes, larger address spaces than physical RAM, and demand paging. Module 4.4 covers this in depth.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Calculate access times across the memory hierarchy, trace read/write operations through an address decoder, write the contents of a simulated 8-byte memory as ASCII values, and analyse cache hit/miss patterns.
