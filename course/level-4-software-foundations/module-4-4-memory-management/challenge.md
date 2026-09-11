# Challenge 4.4 — Memory Management

**Type:** Calculation + trace + reasoning  
**Estimated time:** 45–55 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Page Address Arithmetic

System: 32-bit virtual addresses, 4 KB pages (2¹² bytes = 4096 bytes).

1. A virtual address is 32 bits: [20-bit page number | 12-bit offset]. Break down virtual address `0x0040_1B8C`:
   - What is the page number (in decimal and hex)?
   - What is the page offset (in decimal and hex)?

2. Physical memory has 256 MB. Page frames are also 4 KB. How many physical frames exist? How many bits are needed for the frame number?

3. A page table entry maps virtual page 1024 to physical frame 512. Virtual address `0x0040_10A0`:
   - What is the page number?
   - Does it map to frame 512? (page 1024 = frame 512)
   - What is the resulting physical address?

4. A process has 16 KB of virtual memory actively used (4 pages). How many bytes does its page table occupy if each PTE is 4 bytes and it uses a flat (single-level) page table for the full 32-bit space?

---

## Part B — Multi-Level Page Table Walk

A simplified 2-level page table for a 32-bit system:
- Virtual address: [10 bits L1 index | 10 bits L2 index | 12 bits offset]
- Page Directory (L1) is at physical address 0x1000
- Each entry is 4 bytes

The Page Directory at 0x1000 contains:
```
Entry 0: 0x2000  (points to page table at 0x2000)
Entry 1: 0x3000  (points to page table at 0x3000)
Entry 2: 0x0000  (not present)
```

The Page Table at 0x2000 contains:
```
Entry 0: frame 0x100  (physical page 0x100000)
Entry 1: frame 0x200  (physical page 0x200000)
Entry 2: frame 0x050  (physical page 0x050000)
```

Translate these virtual addresses:
5. `0x0000_0000` (L1=0, L2=0, offset=0)
6. `0x0000_1000` (L1=0, L2=1, offset=0)
7. `0x0040_0030` (L1=1, L2=0, offset=0x030)
8. `0x0080_0000` (L1=2, ...) — what happens?

---

## Part C — Page Faults

A process accesses these virtual pages in order. The system has **3 physical frames** (very small for illustration). Use **LRU** replacement. Initially all frames empty.

Access sequence: `P1, P2, P3, P4, P1, P2, P5, P1, P2, P3, P4`

9. For each access, state: **Hit or Fault?** Which page is loaded? Is any page evicted (and which)?

10. Calculate the **page fault rate** (faults / total accesses).

11. Now use **FIFO** replacement for the same sequence. What is the fault rate? Is it better or worse than LRU?

12. **Belady's anomaly**: FIFO sometimes gets *more* faults with *more* frames. With 4 frames and the sequence `1,2,3,4,1,2,5,1,2,3,4,5`, how many faults does FIFO produce? Compare to 3 frames. Does LRU exhibit this anomaly?

---

## Part D — Process Isolation

13. Process A is at virtual address `0x4010_0000`. Process B is also at virtual address `0x4010_0000`. Can A read B's data at this address? Why or why not? What mechanism enforces the isolation?

14. `fork()` creates a child process. The parent has 100 MB of heap memory. Using **Copy-on-Write**:
    - How much physical memory is immediately allocated for the child's heap?
    - If the child writes to 10 MB of pages, how much physical memory has been allocated for the child's heap now?
    - What happens at the hardware level when the child writes to a CoW page?

15. A process calls `mmap(NULL, 4096, PROT_READ, MAP_ANONYMOUS, -1, 0)` then tries to write to the returned address. What happens and why?

16. A shared library (`libc.so`) is mapped into 1,000 different processes. The `.text` (code) section is 2 MB. How much physical RAM is used for all 1,000 copies of libc's code section? Explain how this is possible.

---

## Part E — Virtual Memory Layout

17. A program's virtual address layout (simplified):
    - .text starts at 0x400000, size 12 KB
    - .data starts at 0x600000, size 4 KB
    - .bss starts at 0x601000, size 8 KB
    - Heap starts at 0x700000, current size 20 KB
    - Stack top at 0x7FFF_0000, current size 40 KB

    How many virtual pages are used by each segment? (4 KB pages)

18. Why is .text mapped read-only + executable, .data read-write but not executable, and the stack read-write but not executable (on systems with NX/XD bit)?

19. The heap "grows upward" and the stack "grows downward." At some theoretical future point they could meet. On a 32-bit system with 4 GB virtual space, with stack at the top and heap starting at 0x08048000 (typical Linux), how much virtual address space is available for heap+stack combined? What actually limits them before they meet?

---

## Rubric

| Part | Points |
|------|--------|
| A address arithmetic | 20 |
| B page table walk | 20 |
| C page faults / replacement | 25 |
| D process isolation | 20 |
| E virtual layout | 15 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A</summary>

1. `0x0040_1B8C`: Page number = upper 20 bits = `0x00401` = 1025 decimal. Offset = lower 12 bits = `0xB8C` = 2956 decimal.

2. 256 MB / 4 KB = 65,536 frames = 2¹⁶. Need **16 bits** for frame number.

3. Virtual `0x0040_10A0`: page = `0x00401` = 1025. Not page 1024, so it maps to a different frame. If page 1025 mapped to frame 513: physical = 513 × 4096 + 0x0A0 = 0x0020_10A0.

4. Flat page table: 2²⁰ entries × 4 bytes = 4 MB. (This is why multi-level tables exist.)
</details>

<details>
<summary>Part B translations</summary>

5. L1=0→0x2000, L2=0→frame 0x100, offset=0 → physical **0x100_000**
6. L1=0→0x2000, L2=1→frame 0x200, offset=0 → physical **0x200_000**
7. L1=1→0x3000, L2=0→(depends on 0x3000 contents, not given) → need more data; answer is "requires reading page table at 0x3000"
8. L1=2→Entry 2 = 0x0000 (not present) → **Page fault**: kernel must allocate a new page table at L2 level and then handle the access.
</details>

<details>
<summary>Part C — LRU trace</summary>

3 frames. Access: P1, P2, P3, P4, P1, P2, P5, P1, P2, P3, P4

| Access | Frames | Fault? | Evict |
|--------|--------|--------|-------|
| P1 | P1,−,− | Fault | — |
| P2 | P1,P2,− | Fault | — |
| P3 | P1,P2,P3 | Fault | — |
| P4 | P2,P3,P4 | Fault | P1 (LRU) |
| P1 | P3,P4,P1 | Fault | P2 (LRU) |
| P2 | P4,P1,P2 | Fault | P3 (LRU) |
| P5 | P1,P2,P5 | Fault | P4 (LRU) |
| P1 | P1,P2,P5 | **Hit** | — |
| P2 | P1,P2,P5 | **Hit** | — |
| P3 | P2,P5,P3 | Fault | P1 (LRU) |
| P4 | P5,P3,P4 | Fault | P2 (LRU) |

9 faults / 11 accesses = **81.8% fault rate** — LRU.
</details>

<details>
<summary>Part D</summary>

13. No — the MMU maintains separate page tables for each process. Virtual address 0x4010_0000 in process A maps to a different physical frame than in process B. The hardware MMU enforces this with every memory access; there is no software-visible overlap.

14. With CoW: 0 MB immediately allocated (child shares parent's pages, all marked read-only). After writing to 10 MB: 10 MB allocated (one copy per written page). Hardware: on the write attempt, MMU raises a page fault (write to read-only page); kernel handler checks CoW flag, copies the page to a new physical frame, updates both page tables, marks both writable, resumes execution.

15. PROT_READ only: the page is mapped read-only. A write attempt raises a page fault. Kernel checks: write to read-only mapping → SIGSEGV. The process receives a segfault.

16. Only **2 MB** of physical RAM, shared. The `.text` section is mapped with Present=1 and User=1, Writable=0 into all 1,000 processes, all pointing to the same 512 physical frames. No copies — one physical copy, 1,000 virtual mappings. This is why shared libraries use so little memory.
</details>
