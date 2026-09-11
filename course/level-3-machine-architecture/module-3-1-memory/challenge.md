# Challenge 3.1 — Memory: How Machines Remember

**Type:** Calculation + trace + hands-on  
**Estimated time:** 40–50 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Memory Hierarchy Calculations

Use the latency table from the lesson.

1. A program runs a loop that accesses the **same 4 values** repeatedly. All 4 fit in L1 cache. If the loop runs 1,000,000 iterations and each iteration does 4 memory reads:
   - How many total memory reads occur?
   - Assuming all reads hit L1 cache (1 ns each), what is the total memory access time?

2. The same loop is rewritten to access **1,000 different values** in random order. None fit in L1 (32 KB full). Every read is a RAM access (60 ns each):
   - How many total memory reads occur? (same 1,000,000 iterations × 4 reads)
   - What is the total memory access time now?
   - What is the **speedup ratio** of the cache-friendly version vs the cache-unfriendly version?

3. A hard disk (10,000,000 ns per access) stores a 512-byte block. An SSD (100,000 ns) stores the same block. How many times faster is the SSD? How many times faster is RAM than the SSD?

---

## Part B — Address Space

4. A processor has a **16-bit address bus**. How many unique addresses can it address? How many bytes of memory can it support?

5. An old 8-bit processor (6502, used in Apple II and NES) had a 16-bit address bus. Its RAM was only 64 KB. Why could it not address more than 64 KB even with a faster CPU?

6. A 32-bit processor running Windows XP had a 4 GB address space limit. A user installed 8 GB of RAM. How much of it could the OS use? What would be needed to use all 8 GB?

7. Calculate the number of bits needed in the address bus to address exactly 1 GB of byte-addressable memory.

---

## Part C — Read/Write Trace

A simple memory array has 8 bytes at addresses 0x00 through 0x07. Initial contents: all zeros.

Execute these operations in order and show the memory state after **each operation**:

```
WRITE 0x03 ← 0xFF
WRITE 0x01 ← 0x41
WRITE 0x06 ← 0x4F
READ  0x03        → result: ?
WRITE 0x03 ← 0x00
READ  0x01        → result: ?
READ  0x07        → result: ?
```

Show the full 8-byte memory array after each write.

---

## Part D — ASCII Memory

8. The ASCII code for 'H' is 72 (0x48), 'E' is 69 (0x45), 'L' is 76 (0x4C), 'O' is 79 (0x4F).

   Write the word **"HELLO"** into addresses 0x00–0x04 of a byte-addressable memory. What value goes at each address?

9. A memory array contains these values at addresses 0x10–0x17:
   ```
   0x10: 0x41   0x11: 0x6F   0x12: 0x50   0x13: 0x53
   0x14: 0x00   0x15: 0x21   0x16: 0x00   0x17: 0x00
   ```
   Decode the ASCII string stored here. (0x00 is the null terminator — end of string)

---

## Part E — Cache Analysis

A small direct-mapped cache has **4 cache lines**, each holding 1 byte. The cache uses the **lowest 2 bits** of the address as the cache index (so address 0x00 maps to line 0, 0x01 to line 1, 0x04 to line 0, etc.)

A program reads these addresses in sequence:
`0x00, 0x01, 0x02, 0x03, 0x04, 0x01, 0x00, 0x05, 0x01, 0x00`

For each access, state: **Hit or Miss?** Which cache line is used? Is anything evicted?

Then calculate the **hit rate** for this access pattern.

---

## Rubric

| Part | Points | What we're looking for |
|------|--------|------------------------|
| A1 | 8 | 4M reads × 1ns = 4ms total |
| A2 | 10 | 4M reads × 60ns = 240ms; speedup = 60× |
| A3 | 7 | SSD 100× faster than HDD; RAM 600× faster than SSD |
| B4 | 5 | 2¹⁶ = 65,536 addresses = 64 KB |
| B5 | 8 | Address bus width caps addressable memory regardless of CPU speed |
| B6 | 7 | PAE (Physical Address Extension) needed to access >4GB on 32-bit |
| B7 | 5 | 2³⁰ = 1GB → 30 address bits |
| C trace | 15 | Correct memory state after each operation |
| D8 | 5 | H=0x48@0x00, E=0x45@0x01, L=0x4C@0x02, L=0x4C@0x03, O=0x4F@0x04 |
| D9 | 5 | "AoPS" (0x41='A', 0x6F='o', 0x50='P', 0x53='S', 0x00=null) |
| E cache | 15 | Correct hit/miss trace; hit rate = 3/10 = 30% |

**Total: 90 points**

---

## Hints

<details>
<summary>Hint — Part A speedup</summary>
Total time = number of reads × latency per read. The speedup ratio is simply time_slow ÷ time_fast. The 60× figure should match the ratio of RAM latency to L1 latency from the lesson table.
</details>

<details>
<summary>Hint — Part B7</summary>
You need 2^n = 1,073,741,824. Solve for n: log₂(1,073,741,824) = 30. So 30 address bits.
</details>

<details>
<summary>Hint — Part E cache mapping</summary>
The cache index = address mod 4 (lowest 2 bits). Address 0x00 → index 0. Address 0x04 → also index 0 (evicts whatever was in line 0). Address 0x05 → index 1. Track what each cache line contains after each access.
</details>

---

## Solution

<details>
<summary>Part A</summary>

**A1:** 1,000,000 × 4 = 4,000,000 reads × 1 ns = **4 ms**

**A2:** 4,000,000 reads × 60 ns = **240 ms**. Speedup = 240/4 = **60×**

**A3:** SSD is 10,000,000 ÷ 100,000 = **100× faster** than HDD. RAM is 100,000 ÷ 60 ≈ **1,667× faster** than SSD.
</details>

<details>
<summary>Part B</summary>

**B4:** 2¹⁶ = 65,536 addresses = **64 KB**

**B5:** The address bus has 16 bits → maximum 2¹⁶ = 64 KB addressable. No matter how fast the CPU is, it physically cannot generate more than 65,536 distinct addresses. Adding more RAM beyond that is invisible to the processor.

**B6:** With a 32-bit address space, the OS can only address **4 GB**. The other 4 GB of installed RAM is inaccessible. Solution: **PAE (Physical Address Extension)** — a CPU feature that extends the physical address bus to 36 bits while keeping 32-bit virtual addresses per process, allowing the OS to map more than 4 GB total (though each process still sees only 4 GB).

**B7:** 2³⁰ = 1,073,741,824 bytes = 1 GiB. Need **30 address bits**.
</details>

<details>
<summary>Part C trace</summary>

Initial: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07] = [00, 00, 00, 00, 00, 00, 00, 00]

After WRITE 0x03 ← 0xFF: [00, 00, 00, **FF**, 00, 00, 00, 00]  
After WRITE 0x01 ← 0x41: [00, **41**, 00, FF, 00, 00, 00, 00]  
After WRITE 0x06 ← 0x4F: [00, 41, 00, FF, 00, 00, **4F**, 00]  
READ 0x03 → **0xFF**  
After WRITE 0x03 ← 0x00: [00, 41, 00, **00**, 00, 00, 4F, 00]  
READ 0x01 → **0x41**  
READ 0x07 → **0x00** (never written)
</details>

<details>
<summary>Part D</summary>

**D8:** 0x00=0x48('H'), 0x01=0x45('E'), 0x02=0x4C('L'), 0x03=0x4C('L'), 0x04=0x4F('O')

**D9:** 0x41='A', 0x6F='o', 0x50='P', 0x53='S', 0x00=null terminator → **"AoPS"**
</details>

<details>
<summary>Part E cache trace</summary>

Cache lines 0–3, initially empty (cold start):

| Access | Address | Index | Cache line | Hit/Miss | Evicts |
|--------|---------|-------|------------|----------|--------|
| 1 | 0x00 | 0 | 0 | Miss | — |
| 2 | 0x01 | 1 | 1 | Miss | — |
| 3 | 0x02 | 2 | 2 | Miss | — |
| 4 | 0x03 | 3 | 3 | Miss | — |
| 5 | 0x04 | 0 | 0 | Miss | 0x00 evicted |
| 6 | 0x01 | 1 | 1 | **Hit** | — |
| 7 | 0x00 | 0 | 0 | Miss | 0x04 evicted |
| 8 | 0x05 | 1 | 1 | Miss | 0x01 evicted |
| 9 | 0x01 | 1 | 1 | Miss | 0x05 evicted |
| 10 | 0x00 | 0 | 0 | **Hit** | — |

Hits: 2 out of 10. **Hit rate = 20%**

Note: access 10 (0x00) hits because 0x00 was loaded at step 7 and line 0 hasn't been evicted since.
</details>
