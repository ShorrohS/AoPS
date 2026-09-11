# Module 4.4 — Memory Management

---

## The Problem

> A 64-bit CPU can address 16 exabytes of memory.
> A typical machine has 16 gigabytes of RAM.
>
> Every program believes it has its own private address space starting at 0x0000.
> Two different programs can both have a variable at address 0x4000 — and they never interfere.
>
> How?
>
> And how does a 4 GB program run on a machine with only 8 GB of RAM when other programs are also running?

These two mysteries have the same answer: **virtual memory** — one of the most elegant engineering solutions in the history of computing.

---

## The Story

### The Problem of Running Multiple Programs

On early computers, programs ran at fixed physical addresses. Loading two programs simultaneously was impossible — they would overwrite each other. The programmer had to know exactly where in physical RAM the program would be placed and write addresses accordingly.

**Relocation** (1950s) was the first solution: a hardware register held the base address of the current program. Every memory access added this base. Programs could move anywhere in RAM without being rewritten. But they still shared the same physical address space — a bug in one program could corrupt another's memory.

**Segmentation** (1960s, Multics) added boundaries: each program had a base and a limit. Hardware enforced that no access exceeded the limit. But segments were variable-size, leading to fragmentation.

**Paging** (late 1960s) solved fragmentation: divide all memory into fixed-size **pages** (typically 4 KB). Give each process its own mapping from virtual pages to physical pages. This is the system used today in every general-purpose OS.

---

### Virtual vs Physical Addresses

Every user-space program uses **virtual addresses**. These are what the program sees — addresses starting at 0x0000_0000_0000_0000 and extending to 0xFFFF_FFFF_FFFF_FFFF (on 64-bit, though only 48 bits are used in practice).

**Physical addresses** are the actual locations in RAM chips. The CPU's **Memory Management Unit (MMU)** translates every virtual address into a physical address on the fly, for every memory access.

```
Virtual address  →  [MMU / Page Table Walk]  →  Physical address
0x00007FFF_1000          translation              0x0000_1A40_3000
```

Two processes can both use virtual address 0x401000 — they map to different physical addresses. Neither can see the other's memory. The OS controls the mapping.

---

### Pages, Frames, and Page Tables

**Page**: a fixed-size block of virtual memory. Typically 4 KB (4096 bytes).  
**Frame**: a fixed-size block of physical memory. Same size as a page.  
**Page table**: a data structure mapping virtual page numbers to physical frame numbers.

For a 32-bit address space with 4 KB pages:
- Virtual address = 20-bit page number + 12-bit page offset
- 2²⁰ = 1,048,576 possible virtual pages
- Each page table entry (PTE) = 4 bytes → 4 MB page table per process!

That is too large. The solution: **multi-level page tables**.

A 2-level page table for 32-bit systems:
```
Virtual address: [10 bits dir] [10 bits table] [12 bits offset]
                     ↓                ↓               ↓
               Page Directory → Page Table → Physical Frame + Offset
```

x86-64 uses a **4-level page table**:
```
Virtual address: [9 bits PML4] [9 bits PDP] [9 bits PD] [9 bits PT] [12 bits offset]
```

Only page directories that are actually in use need to exist. A sparse address space uses very little memory for its page table.

---

### Page Table Entries (PTEs)

Each PTE contains:
- **Physical frame number** — which RAM frame this page maps to
- **Present bit (P)** — 1 = this mapping exists; 0 = page not in memory (triggers page fault)
- **Writable bit (W)** — 0 = read-only; 1 = writable. Enforces code section immutability.
- **User bit (U)** — 0 = kernel only; 1 = user space accessible
- **Accessed bit (A)** — set by hardware when the page is read. Used by page replacement algorithms.
- **Dirty bit (D)** — set by hardware when the page is written. Used to know if a page needs to be written back to disk before reclaiming.
- **NX bit (No-Execute)** — prevents code execution from this page. Makes data pages non-executable — critical for stack/heap security.

---

### The TLB — Translation Lookaside Buffer

A page table walk requires up to 4 memory accesses (on x86-64). That would make every memory access 5× slower. The solution: the **TLB** — a small, fast cache of recent virtual→physical translations.

- Capacity: 64–4096 entries (tiny)
- Speed: 1 cycle (same as L1 cache)
- Hit rate: >99% for well-behaved programs (due to temporal and spatial locality)

**TLB miss**: the hardware page table walker reads the page table hierarchy, loads the translation into the TLB, and retries. On x86, this is done entirely by hardware (hardware page table walker). On ARM, software can handle TLB misses.

**TLB shootdown**: when the OS modifies a process's page table (e.g., unmaps a page), it must invalidate the corresponding TLB entries on *all* CPU cores. On a multiprocessor system, this requires an inter-processor interrupt (IPI) to each core. TLB shootdowns are expensive and a significant performance cost of shared-memory multiprocessors.

---

### Demand Paging and the Page Fault

A process does not need all its pages in physical RAM simultaneously. The OS uses **demand paging**: pages are loaded into RAM only when first accessed.

When a process accesses a virtual address whose PTE has Present=0:
1. The CPU raises a **page fault** exception
2. The kernel's page fault handler runs
3. It checks: is this a valid virtual address for this process?
   - Yes: load the page from disk (swap space / file), update PTE, return
   - No: invalid access → send SIGSEGV to the process (segmentation fault)
4. The process resumes, unaware that it paused

**Copy-on-Write (CoW)**: when `fork()` creates a child process, the OS does not immediately copy the parent's memory. Instead, both parent and child share the same physical pages, marked read-only. When either process writes to a shared page, a page fault fires, the kernel copies just that page, and the write proceeds. This makes `fork()` nearly free even for large processes.

---

### Swap Space

When RAM is full and a new page must be loaded, the OS must **evict** an existing page. If the page is dirty (modified), it is written to **swap space** on disk before eviction. If clean (matches the disk copy), it can be silently discarded.

**Page replacement algorithms:**
- **LRU (Least Recently Used)**: evict the page accessed longest ago. Optimal in practice but expensive to implement precisely.
- **Clock algorithm (Second Chance)**: approximates LRU using the Accessed bit. Scan pages in circular order; if A=1, clear it and give a second chance; if A=0, evict.
- **LFU (Least Frequently Used)**: evict the page accessed fewest times. Suffers from outdated frequency counts.

Modern Linux uses variants of the clock algorithm plus separate active/inactive page lists.

---

### Process Memory Layout

A typical Linux process's virtual address space (64-bit):

```
0xFFFFFFFF_FFFFFFFF  ┐
                     │  Kernel space (user cannot access)
0xFFFF8000_00000000  ┘
        ...
0x00007FFF_FFFFFFFF  ┐
                     │  Stack (grows downward)
0x00007FFE_XXXXXXXX  ┘  ← RSP here
        ...
        [random ASLR gap]
        ...
                        Heap (grows upward) ← sbrk/mmap
                     ┐
                     │  .bss (uninitialised globals, zeroed)
                     │  .data (initialised globals)
0x00000000_00401000  │  .text (code, read+execute, not writable)
0x00000000_00400000  ┘  ← ELF header
```

---

## The Concept: The MMU Makes Every Process Think It Owns All of Memory

This is the central illusion of modern operating systems. Each process has a complete, private virtual address space. The physical RAM is shared invisibly. The OS and MMU cooperate to maintain the illusion seamlessly — except when debugging, when the illusion's mechanics become visible and useful.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Virtual Address Translator**
- Enter a virtual address
- Step through the 4-level x86-64 page table walk
- See which physical address it maps to
- Toggle the Present bit to trigger a page fault

**Tool 2 — Page Fault Handler**
- A process accesses pages in a specific sequence
- Watch pages being loaded from "disk" into available frames
- See the page replacement algorithm evict pages when RAM is full

**Tool 3 — Process Memory Map**
- A visual representation of a process's virtual address space
- Show .text, .data, .bss, heap, stack regions
- Toggle ASLR to see how base addresses shift between runs

---

## Going Deeper

**Huge pages**: using 4 KB pages for large memory workloads (databases, JVMs, ML models) generates enormous TLB pressure. Huge pages (2 MB on x86) reduce TLB misses by 512× for the same memory coverage. Linux supports transparent huge pages (THP), which tries to merge small pages automatically.

**mmap and memory-mapped files**: `mmap()` maps a file directly into a process's virtual address space. Reading from the mapped region reads from the file. Writing to it (if MAP_SHARED) writes back to the file. This is how database files, executable files, and shared libraries are loaded — the dynamic linker mmap's the ELF file sections into the process's address space.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Walk a page table manually, calculate physical addresses, trace page faults, and reason about copy-on-write and process isolation.
