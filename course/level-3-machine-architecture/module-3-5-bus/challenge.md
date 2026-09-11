# Challenge 3.5 — The Bus: Moving Data Around

**Type:** Calculation + trace + design  
**Estimated time:** 40–50 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Bus Bandwidth Calculations

1. A system has a **32-bit data bus** running at **66 MHz**. What is the theoretical peak bandwidth in MB/s?

2. A **64-bit data bus** at **133 MHz** (double data rate — transfers on both clock edges): what is the peak bandwidth in MB/s? In GB/s?

3. DDR4-3200 RAM has a 64-bit bus running at 1,600 MHz (double data rate = 3,200 MT/s effective). Calculate the bandwidth in GB/s for a single channel. For a dual-channel configuration.

4. PCIe 4.0 has a per-lane bandwidth of 2 GB/s in each direction. A GPU uses a PCIe ×16 slot. What is the total unidirectional bandwidth? Bidirectional?

5. A CPU's L1 cache has a **512-bit** data bus to the CPU core, running at **3 GHz**. What is its bandwidth in GB/s? How does this compare to DDR4 dual-channel?

---

## Part B — Bus Transaction Trace

A Von Neumann CPU executes this instruction at address 0x0010:
```
LOAD_A_MEM 0x0200   ; Load the byte at address 0x0200 into register A
```

The instruction itself is stored at 0x0010 (opcode) and 0x0011 (address operand).

Trace every bus transaction required to execute this instruction. For each transaction, specify:
- Phase (Fetch/Decode/Execute)
- Address bus value
- Data bus value (or direction of transfer)
- Control bus signals active
- What register/memory changes as a result

There should be **at least 3 distinct bus transactions** to complete this instruction.

---

## Part C — Arbitration Strategies

Three devices (CPU, DMA controller, GPU) share a bus. In one time period, they submit these requests simultaneously:

| Device | Requests | Priority (fixed) |
|--------|----------|-----------------|
| CPU    | 3 bus transactions | Highest (1) |
| DMA    | 5 bus transactions | Medium (2) |
| GPU    | 2 bus transactions | Lowest (3) |

Each bus transaction takes 1 time unit.

6. **Fixed priority**: how many time units until the GPU completes all its transactions? Does the DMA controller have to wait? Show the schedule.

7. **Round-robin** (rotate priority each turn): how many time units until all 10 transactions complete? Show the schedule for the first 6 turns.

8. Which strategy gives better **average waiting time** across all devices? Which gives better **worst-case waiting time** for the lowest-priority device?

9. The CPU needs its 3 transactions completed within 5 time units or a timer fires (system stall). DMA needs its 5 transactions within 8 time units or data is lost. GPU has no deadline. Design a **deadline-aware arbitration policy** that satisfies both constraints.

---

## Part D — Von Neumann vs Harvard

A Von Neumann CPU has a shared bus with these timings:
- Instruction fetch: 4 cycles
- Data read: 4 cycles
- Both use the same bus (cannot run simultaneously)

A Harvard CPU has separate buses:
- Instruction fetch: 4 cycles (dedicated instruction bus)
- Data read: 4 cycles (dedicated data bus)
- Both can run simultaneously

10. A simple program has this pattern: Fetch, Fetch+Data, Fetch, Fetch+Data, Fetch (some instructions need a data read, some don't). How many cycles does each architecture take?

11. For a program where **every** instruction requires exactly one data read, what is the throughput ratio of Harvard vs Von Neumann?

12. Modern x86-64 uses "modified Harvard" with separate L1i and L1d caches but a unified L2. When does the Von Neumann bottleneck still appear?

---

## Part E — Memory Map Design

You are designing a small embedded system with these requirements:
- 32 KB of RAM for program and data
- 8 KB of ROM for bootloader (read-only)
- 3 memory-mapped I/O devices:
  - LED controller: 4 bytes
  - UART serial port: 8 bytes
  - Timer: 4 bytes
- 16-bit address bus (64 KB total space)

13. Design a memory map: assign each region a start and end address. Show the full 64 KB layout, marking any unused regions.

14. How many address bits does the address decoder need to distinguish between RAM and I/O regions?

15. The ROM bootloader runs at power-on. It needs to copy itself into RAM and then jump to the RAM copy. Why would you want the bootloader in ROM rather than RAM? What would happen if the bootloader were in RAM at power-on?

---

## Rubric

| Part | Points |
|------|--------|
| A bandwidth (5 calculations) | 25 |
| B bus transaction trace | 20 |
| C arbitration (4 questions) | 20 |
| D Von Neumann vs Harvard | 15 |
| E memory map design | 20 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A</summary>

1. 32 bits = 4 bytes × 66 MHz = **264 MB/s**
2. 64 bits = 8 bytes × 133 MHz × 2 (DDR) = **2,128 MB/s ≈ 2.08 GB/s**
3. 64 bits = 8 bytes × 1,600 MHz × 2 (DDR) = 25.6 GB/s single channel. Dual channel: **51.2 GB/s**
4. PCIe 4.0 ×16: 2 GB/s/lane × 16 = **32 GB/s unidirectional, 64 GB/s bidirectional**
5. 512 bits = 64 bytes × 3 GHz = **192 GB/s** — roughly 4× DDR4 dual-channel, showing why cache bandwidth must far exceed RAM bandwidth
</details>

<details>
<summary>Part B — Transaction trace</summary>

**Transaction 1 — Fetch opcode (Fetch phase):**
- Address bus: 0x0010
- Control: MEMORY_SELECT, READ
- Data bus: 0x02 (LOAD_MEM opcode) → loaded into IR
- PC: 0x0010 → 0x0011

**Transaction 2 — Fetch operand (Fetch phase continued):**
- Address bus: 0x0011
- Control: MEMORY_SELECT, READ
- Data bus: 0x0200 (address operand) → loaded into MAR
- PC: 0x0011 → 0x0012

**Transaction 3 — Execute: read data (Execute phase):**
- Address bus: 0x0200
- Control: MEMORY_SELECT, READ
- Data bus: value at 0x0200 (e.g., 0x42) → loaded into Register A
</details>

<details>
<summary>Part C — Arbitration</summary>

6. Fixed priority schedule: CPU goes 3× first (turns 1–3), DMA next 5× (turns 4–8), GPU last 2× (turns 9–10). GPU waits until turn 9 → **completes at t=10**. DMA waits until turn 4.

7. Round-robin (CPU→DMA→GPU→CPU→DMA→...): Turn 1:CPU, 2:DMA, 3:GPU, 4:CPU, 5:DMA, 6:GPU, 7:CPU, 8:DMA, 9:DMA, 10:DMA. All done at t=10 in this case (same total, better distribution).

8. Round-robin gives better **average waiting time** and much better worst-case for low-priority devices. Fixed priority can starve low-priority devices entirely if high-priority devices keep requesting.

9. Give CPU and DMA higher priority for the first 8 time units (CPU's 3 + DMA's 5 = 8 transactions fit within deadlines). GPU uses remaining slots. Or: use earliest-deadline-first — DMA deadline (8) < CPU deadline (5)... wait, CPU has tighter deadline, so: CPU first 3 turns, DMA next 5 turns, GPU remaining.
</details>

<details>
<summary>Part E — Memory map example</summary>

One valid mapping:
```
0x0000 – 0x7FFF: RAM (32 KB)
0x8000 – 0x9FFF: ROM bootloader (8 KB)
0xA000 – 0xA003: LED controller (4 bytes)
0xA004 – 0xA00B: UART serial port (8 bytes)
0xA00C – 0xA00F: Timer (4 bytes)
0xA010 – 0xFFFF: Unused / reserved (23.98 KB)
```

The address decoder needs to distinguish RAM (bit 15 = 0), ROM (bits 15:13 = 100), and I/O (bits 15:12 = 1010) — roughly **4 high address bits** are sufficient to decode all regions.

ROM at power-on: RAM contents are undefined at power-on (DRAM must be initialised). ROM retains its contents without power. If the bootloader were in RAM, there would be nothing valid to execute at reset. The bootloader in ROM copies itself (or the main firmware) to RAM for faster execution, then jumps there.
</details>
