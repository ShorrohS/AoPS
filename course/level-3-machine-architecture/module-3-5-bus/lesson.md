# Module 3.5 — The Bus: Moving Data Around

---

## The Problem

> The CPU computes. Memory stores. I/O devices communicate.
>
> But how do these components actually *talk to each other*?
> The CPU is a chip on a motherboard. Memory is another chip. The GPU is a third.
>
> They cannot communicate by thought. They need a shared pathway — a physical medium, a protocol, and a set of rules for who talks when.
>
> That pathway is the **bus**.

A bus is a shared communication channel — a set of wires connecting multiple components, plus the protocol that governs who uses those wires and when.

---

## The Story

### The Early Bus: Everything Shared One Wire

The earliest computers wired components point-to-point: the CPU had a dedicated wire to memory, another to the printer, another to the card reader. Every new device required new wires and new control logic. Adding a device to a computer was a hardware engineering project.

The invention of the **shared bus** — a common set of wires that all components connect to — was transformative. Now adding a device meant plugging it into the existing bus. The protocol managed who could talk and when.

The **Intel 8086 (1978)** used a 16-bit data bus and 20-bit address bus. The **IBM PC (1981)** standardised the ISA bus (not to be confused with Instruction Set Architecture — the same acronym used for different purposes). **PCI (1992)** replaced ISA. **PCIe (2003)** replaced PCI with a point-to-point switched fabric that looks like a bus to software but is physically very different.

---

### The Three Sub-Buses

A classical system bus consists of three logically separate groups of signals:

**Address Bus**
- Carries the address of the memory location or I/O device being accessed
- Unidirectional: CPU → memory/devices
- Width determines addressable space: 32-bit → 4 GB, 64-bit → 16 EB
- Example: CPU places 0x0000_1000 on address bus → selects address 4096

**Data Bus**
- Carries the actual data being read or written
- Bidirectional: CPU ↔ memory/devices
- Width determines how much data moves per transfer: 8, 16, 32, or 64 bits
- A 64-bit data bus moves 8 bytes per bus cycle

**Control Bus**
- Carries control signals that coordinate the operation
- Signals include:
  - `READ` / `WRITE` — direction of transfer
  - `MEMORY_SELECT` / `IO_SELECT` — is this a memory or I/O access?
  - `CLOCK` — timing signal
  - `INTERRUPT_REQUEST` — device requests CPU attention
  - `BUS_GRANT` / `BUS_REQUEST` — bus arbitration
  - `RESET` — system reset

All three buses operate simultaneously, coordinated by the clock.

---

### Bus Arbitration

A bus is a **shared resource**. Only one device can use it at a time. When multiple components want to use the bus simultaneously, someone must decide who goes first. This is **bus arbitration**.

**Daisy-chain arbitration**: devices are chained in priority order. A bus grant signal passes down the chain — the first device in the chain that wants the bus takes it. Simple but unfair to low-priority devices.

**Centralised arbitration**: a dedicated **bus arbiter** receives requests from all devices and grants access based on a scheduling policy (round-robin, priority, etc.). Fairer but requires extra hardware.

**Distributed arbitration**: devices use a shared wire and a collision-detection protocol (similar to early Ethernet). Each device can "bid" for the bus simultaneously; the highest-priority wins based on wire-OR logic.

Modern systems like PCIe avoid shared-bus arbitration entirely by using **point-to-point switched connections** — each device has its own dedicated link to a switch (like Ethernet vs a hub). But the software model still looks like a bus.

---

### Von Neumann vs Harvard Architecture

**Von Neumann architecture**: instructions and data share the same memory and the same bus. The CPU fetches an instruction, then fetches data — both using the same path. This creates the **Von Neumann bottleneck**: the bus bandwidth limits performance because the same resource is contended for both code and data.

Almost all general-purpose computers (x86, ARM application cores) use Von Neumann architecture.

**Harvard architecture**: separate memory and separate buses for instructions and data. The CPU can fetch an instruction and read data simultaneously — no contention. Simpler to implement but more expensive (two separate memory systems).

Used in: microcontrollers (PIC, AVR), DSPs, many embedded systems.

**Modified Harvard**: use separate L1 instruction cache and L1 data cache (effectively separate buses at the cache level), but share memory at L2 and beyond. This gives most of Harvard's performance benefit while keeping one unified address space. Used by: modern x86-64, ARM Cortex-A. This is why L1 is listed as "L1i" (instruction) and "L1d" (data) in CPU specs.

---

### Bus Bandwidth and Latency

**Bandwidth**: how much data can flow per second.
```
Bandwidth = (bus width in bytes) × (bus clock frequency)
Example: 64-bit bus at 100 MHz = 8 bytes × 100 MHz = 800 MB/s
DDR4-3200: 64-bit × 1,600 MHz (double-pumped) × 2 channels = 51.2 GB/s
```

**Latency**: how long until the first data byte arrives after a request.
```
Latency = (bus request overhead) + (memory access time)
Typical DRAM latency: 60–80 ns regardless of bus bandwidth
```

Bandwidth and latency are independent. A high-bandwidth bus can still have high latency. Latency dominates for small random accesses; bandwidth dominates for large sequential transfers.

**Bus width vs bus speed**: doubling bus width doubles bandwidth but requires more pins/wires (expensive). Doubling clock speed doubles bandwidth but increases power and electromagnetic interference. Real systems balance both.

---

### PCIe: The Modern "Bus"

PCIe (Peripheral Component Interconnect Express) is the dominant high-speed interconnect in modern PCs. Technically it is not a shared bus — it is a **switched point-to-point serial fabric**.

- Each device has a **dedicated serial link** (lane) to the PCIe root complex (in the CPU or chipset)
- Each lane is 2 differential pairs: one transmit, one receive
- ×1, ×4, ×8, ×16 slot configurations (1, 4, 8, or 16 lanes)
- PCIe 5.0: 4 GB/s per lane → ×16 = 64 GB/s bidirectional

But from the software perspective, PCIe devices appear in the system address space, are configured via memory-mapped registers, and use the same read/write semantics as any bus. The abstraction holds.

---

## The Concept: The Bus as Shared Protocol

The bus is the physical embodiment of the computing contract: any component that implements the protocol can participate in the system. This is why standards matter. The PCI bus standard let any manufacturer build cards that worked in any PCI motherboard. USB lets any peripheral connect to any host. PCIe lets any GPU or NVMe drive work in any compatible system.

Without standardised bus protocols, the computer industry would be a fragmented ecosystem of incompatible proprietary interfaces — which is exactly what it was before the IBM PC standardised the ISA bus in 1981.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Bus Transaction Animator**
- A visual system with CPU, RAM, and two I/O devices sharing a bus
- Click "Read" or "Write" to initiate a bus transaction
- Watch: address bus lights up with the address, control bus signals activate, data flows on the data bus
- Each sub-bus is colour-coded (address=blue, data=red, control=gold)

**Tool 2 — Bus Arbitration**
- Three devices simultaneously request the bus
- Try different arbitration schemes: fixed priority, round-robin, FCFS
- Observe which device waits, and for how long
- Calculate bus utilisation percentage

**Tool 3 — Von Neumann vs Harvard**
- Two toy CPUs execute the same program: one Von Neumann, one Harvard
- Von Neumann: instruction fetch and data access contend on the same bus
- Harvard: both happen in parallel
- Compare instruction throughput

---

## Going Deeper

**Cache coherency**: when multiple CPU cores share memory, each has its own L1/L2 cache. If Core 0 writes to address X and Core 1 has X cached, Core 1's cache is now stale (incoherent). The **MESI protocol** (Modified, Exclusive, Shared, Invalid) maintains coherency: cache lines carry state tags, and bus transactions notify other caches when a write occurs. Without coherency, multiprocessor programs would produce incorrect results silently.

**Memory-mapped I/O vs port-mapped I/O revisited**: on x86, both exist. The CPU has separate IN/OUT instructions for port-mapped I/O (64K I/O ports) and uses regular MOV for MMIO. Linux drivers almost exclusively use MMIO via `ioremap()`. Port I/O is relegated to legacy devices (PS/2 keyboard, COM ports, legacy DMA).

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Calculate bus bandwidth for different configurations, trace bus transactions through a Von Neumann system, compare arbitration strategies, and design a memory map for a small embedded system.
