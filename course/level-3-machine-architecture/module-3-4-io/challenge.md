# Challenge 3.4 — Input/Output: Connecting to the World

**Type:** Calculation + trace + code + reasoning  
**Estimated time:** 40–50 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Polling vs Interrupts: Cost Analysis

A CPU runs at 1 GHz (1 cycle = 1 ns). A keyboard generates keypresses at an average rate of **10 per second** (once every 100 ms). The polling loop checks the keyboard status register every **1,000 cycles** (1 µs).

1. How many times does the CPU check the status register per second?

2. How many of those checks actually find a keypress waiting? (Assume a keypress takes exactly 1 check to detect once it arrives.)

3. What percentage of CPU time is **wasted** on polling? (Wasted cycles = total checks × 1,000 cycles/check, minus the ~10 "useful" checks per second that actually found data.)

4. Now switch to interrupt-driven I/O. The interrupt handler takes **500 cycles** to execute. The keyboard fires 10 interrupts per second. What percentage of CPU time is now spent on keyboard I/O?

5. What is the **efficiency ratio** of interrupts vs polling for this scenario?

---

## Part B — DMA Transfer

A disk sector is 512 bytes. Without DMA, the CPU must copy each byte individually: LOAD from device register (2 cycles) + STORE to memory (2 cycles) = 4 cycles/byte.

6. How many cycles does a non-DMA 512-byte sector read consume?

7. The CPU runs at 3 GHz. How long in nanoseconds does the non-DMA copy take?

8. A DMA controller handles the same transfer. Once programmed, it takes 200 cycles to set up, then runs the transfer autonomously. The CPU is free during the transfer (512 × 4 cycles of DMA activity). When done, it fires an interrupt taking 500 cycles. What is the total CPU overhead for a DMA-assisted 512-byte read?

9. What percentage of the transfer time is the CPU **free** to do other work with DMA?

---

## Part C — MMIO Programming

A simple embedded system has this memory map:
```
0x0000 – 0x0FFF: RAM (4 KB)
0x1000:          LED control register (bit 0 = LED on/off)
0x1001:          Button status register (bit 0 = button pressed)
0x1002:          Timer counter register (read-only, increments each ms)
```

Write a **polling-based** pseudo-assembly program that:
- Turns the LED on when the button is pressed
- Turns it off when the button is released
- Runs forever

Then write an **interrupt-driven** version:
- The button press fires interrupt vector 1
- The interrupt handler toggles the LED

Use the toy ISA from Module 3.3 (extended with MMIO addresses).

---

## Part D — Interrupt Trace

A CPU is executing a program. At cycle 1,000, it receives an interrupt from the keyboard. The interrupt handler (ISR) is at address 0x0200.

10. List the exact sequence of steps the CPU takes from the moment it detects the interrupt to the moment it returns to the interrupted program. (Minimum 6 steps.)

11. The CPU was in the middle of a 3-cycle ADD instruction when the interrupt arrived (2 cycles complete, 1 remaining). Does the CPU handle the interrupt immediately, or does it finish ADD first? Why does this matter for correctness?

12. A second, higher-priority interrupt (timer tick) arrives while the keyboard ISR is running. Describe what happens. What data must the ISR save before it is interrupted?

---

## Part E — I/O Bus Bandwidth

13. A USB 3.0 connection transfers at 5 Gbits/s. An NVMe SSD connected via PCIe 4.0 ×4 transfers at 64 Gbits/s. How many times faster is the SSD interface than USB 3.0?

14. A 4K video stream requires 3.82 GB/s sustained throughput. Can USB 3.0 handle it? Can PCIe 4.0 ×4 handle it? Show calculations (convert Gbits/s to GB/s for comparison).

15. A network card receives packets at 10 Gbits/s. Each packet is 1,500 bytes (maximum Ethernet frame). How many packets per second arrive? If the CPU must handle each packet individually via polling (1,000 cycles per packet at 3 GHz), what fraction of the CPU is consumed? What does this imply about why DMA is essential for high-speed networking?

---

## Rubric

| Part | Points |
|------|--------|
| A polling analysis (5 questions) | 25 |
| B DMA calculations (4 questions) | 20 |
| C MMIO code (polling + interrupt) | 25 |
| D interrupt trace (3 questions) | 18 |
| E bandwidth (3 questions) | 12 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A</summary>

1. 1,000,000 checks/second (1 GHz / 1,000 cycles/check)
2. 10 useful checks/second (one per keypress)
3. Wasted: (1,000,000 − 10) checks × 1,000 cycles = ~999,990,000 cycles/second ≈ **99.999% waste**
4. Interrupts: 10 interrupts × 500 cycles = 5,000 cycles/second = **0.0005% of CPU time**
5. Efficiency ratio: ~200,000× more efficient with interrupts
</details>

<details>
<summary>Part B</summary>

6. 512 bytes × 4 cycles/byte = **2,048 cycles**
7. 2,048 cycles ÷ 3 GHz = **682 ns**
8. CPU overhead = 200 (setup) + 500 (interrupt) = **700 cycles total**. The DMA runs for 2,048 cycles autonomously — CPU is free for that entire period.
9. CPU free time = 2,048 ÷ (200 + 2,048 + 500) = 2,048 ÷ 2,748 ≈ **74.5%** of the transfer time
</details>

<details>
<summary>Part E</summary>

13. PCIe 4.0 ×4 (64 Gbits/s) ÷ USB 3.0 (5 Gbits/s) = **12.8× faster**

14. 4K stream = 3.82 GB/s = 3.82 × 8 = 30.56 Gbits/s. USB 3.0 at 5 Gbits/s = 0.625 GB/s — **cannot handle it**. PCIe 4.0 ×4 at 64 Gbits/s = 8 GB/s — **yes, easily**.

15. 10 Gbits/s ÷ (1,500 × 8 bits) = 10,000,000,000 ÷ 12,000 ≈ **833,333 packets/second**. At 1,000 cycles/packet × 3 GHz: 833,333,000 cycles/second ÷ 3,000,000,000 = **27.8% of CPU**. At 10 Gbps that's just one interface — a server handles multiple. Without DMA, I/O processing would consume the entire CPU.
</details>
