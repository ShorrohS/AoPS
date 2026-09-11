# Challenge 4.3 — Operating System Concepts

**Type:** Scheduling + syscall tracing + privilege reasoning  
**Estimated time:** 45–55 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Process Scheduling

Four processes arrive at time 0. A Round Robin scheduler uses a time quantum of 4 ms. Context switch overhead = 1 ms (deducted from the quantum of the switching-out process).

| PID | Burst time (ms) | Arrival | Priority |
|-----|----------------|---------|----------|
| P1  | 12             | 0       | 2 |
| P2  | 6              | 0       | 4 (highest) |
| P3  | 8              | 0       | 1 |
| P4  | 4              | 0       | 3 |

1. **Round Robin (no priority)**: create a Gantt chart showing execution order. Calculate:
   - Completion time for each process
   - Average waiting time
   - Average turnaround time

2. **Priority preemptive (no quantum)**: process with highest priority number runs first. If a tie, FCFS. P2 runs to completion first, then P4, then P1, then P3. Calculate completion times and average waiting time.

3. Which schedule gives better average turnaround time? Which is "fairer" to all processes?

4. A new process P5 arrives at t=8 ms with burst=2 ms and the highest priority (5). It preempts whatever is running. In the priority schedule from question 2, which process is interrupted, and what effect does this have on P2's completion time? (Hint: P2 finishes before t=8.)

---

## Part B — Syscall Sequence

A C program executes these library calls:
```c
int fd = open("data.txt", O_RDONLY);
char buf[64];
int n = read(fd, buf, 64);
write(1, buf, n);   // write to stdout
close(fd);
exit(0);
```

5. List the Linux syscall number for each of these five operations. (Use the table from the lesson.)

6. For the `write(1, buf, n)` call: what values are in `rax`, `rdi`, `rsi`, `rdx` just before the `syscall` instruction executes?

7. The `read()` call returns −1. What does a negative return value from a syscall mean in the Linux convention? What would `errno` be set to if `data.txt` does not exist?

8. Why can't the program call the disk hardware directly to open `data.txt`? What would happen if user programs had direct hardware access?

---

## Part C — Process States

A process transitions through states: **New → Ready → Running → Waiting → Ready → Running → Terminated**

9. What event causes a process to transition from **Running → Waiting**? Give two specific examples.

10. What event causes a process to transition from **Waiting → Ready**? Who triggers this transition?

11. A process is in the **Running** state on a single-core CPU. Can another process also be **Running** simultaneously? What is the correct term for what appears to be simultaneous execution?

12. The scheduler puts a process back in the **Ready** queue after its time quantum expires. Is this a voluntary or involuntary transition? What hardware mechanism forces it?

---

## Part D — strace Output

The following is partial `strace` output from running `cat hello.txt`:

```
execve("/bin/cat", ["cat", "hello.txt"], ...) = 0
brk(NULL) = 0x55a3b0c45000
openat(AT_FDCWD, "hello.txt", O_RDONLY) = 3
fstat(3, {st_size=13, ...}) = 0
mmap(NULL, 131072, PROT_READ|PROT_WRITE, ...) = 0x7f8a...
read(3, "Hello, World!\n", 13) = 13
write(1, "Hello, World!\n", 13) = 13
close(3) = 0
exit_group(0) = ?
```

13. What is file descriptor 3? Why does `openat` return 3 rather than 0, 1, or 2?

14. `brk(NULL)` is called at startup. What is its purpose here (with NULL argument)?

15. `mmap` allocates 131072 bytes (128 KB) even though the file is only 13 bytes. Why might `cat` allocate much more memory than needed?

16. The `read` call uses fd 3 and `write` uses fd 1. What is the OS-level mechanism that makes `cat hello.txt | grep Hello` work — specifically, what changes about fd 1 in the piped case?

---

## Part E — Kernel vs User Space

17. A program executes `mov cr3, rax` (which loads the page table register — a privileged operation). The program is running in user space (ring 3). What happens?

18. A kernel module has a bug: it dereferences a null pointer (`*((int*)0) = 5`). What happens? Compare this to the same bug in a user-space program.

19. Why is the syscall interface the **only** legitimate way for user programs to request kernel services? What would be the security implication if any user program could directly jump into the kernel at any address?

20. Describe the sequence of events when a process calls `malloc(1024)` in C. Start from the C library call and trace all the way to what (possibly) happens in the kernel.

---

## Rubric

| Part | Points |
|------|--------|
| A scheduling (4 questions) | 28 |
| B syscall sequence (4 questions) | 22 |
| C process states (4 questions) | 18 |
| D strace (4 questions) | 18 |
| E kernel/user (4 questions) | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A — Round Robin Gantt Chart</summary>

Quantum = 4 ms (effectively 3 ms useful + 1 ms overhead per switch, but typically in exams quantum = CPU time given). Simpler: use quantum=4, no overhead unless specified. 

With 4 ms quantum, no overhead:
- t=0–4: P1 (ran 4/12)
- t=4–8: P2 (ran 4/6)
- t=8–12: P3 (ran 4/8)
- t=12–14: P4 (ran 4/4) → P4 completes at t=14 (only needs 4)
- t=14–18: P1 (ran 8/12)
- t=18–20: P2 (ran 6/6) → P2 completes at t=20
- t=20–24: P3 (ran 8/8) → P3 completes at t=24
- t=24–26: P1 (ran 12/12) → P1 completes at t=26

Completion: P4=14, P2=20, P3=24, P1=26.
Turnaround: P4=14, P2=20, P3=24, P1=26. Average=(14+20+24+26)/4=21 ms.
Waiting: P4=10, P2=14, P3=16, P1=14. Average=13.5 ms.
</details>

<details>
<summary>Part B — Syscalls</summary>

5. open→2 (openat is 257, but open=2 on older kernels; either accepted), read=0, write=1, close=3, exit=60.

6. `write(1, buf, n)`: rax=1, rdi=1, rsi=address of buf, rdx=n (value returned by read).

7. Negative return = error. The actual errno is set by the C library from the absolute value of the return. If file doesn't exist: errno = ENOENT (2).

8. Hardware access requires ring 0. A user process in ring 3 executing a hardware I/O port instruction triggers a protection fault. If user programs had direct access: any program could corrupt any other program's data, crash the system, or bypass security. The kernel acts as a trusted intermediary enforcing access control and isolation.
</details>

<details>
<summary>Part E answers</summary>

17. Privileged instruction in ring 3: the CPU raises a **General Protection Fault** (#GP exception, interrupt 13). The kernel's fault handler runs, determines the process attempted a privileged instruction, and sends it SIGSEGV. The process is terminated.

18. Null pointer in kernel: the kernel accesses address 0, which is not mapped. This triggers a page fault in ring 0 — a **kernel oops** or kernel panic. The entire system may crash (kernel panic) or the offending kernel thread is killed. All user processes lose their OS. A null pointer in user space only kills that one process — the OS remains running.

19. The syscall instruction causes a controlled transition: the CPU jumps to a fixed kernel entry point defined in the `LSTAR` register (set up at boot). Only the OS controls this address. If user programs could jump anywhere in kernel memory, they could execute arbitrary kernel code as ring 0, bypassing all security checks — instant privilege escalation and system compromise.

20. `malloc(1024)`:
1. C library's malloc implementation checks its free list — if a large enough freed block exists, it returns it immediately (no syscall).
2. If not enough free memory: calls `brk(new_break)` or `mmap(NULL, size, ...)` to request more pages from the kernel.
3. Kernel validates the request, updates the process's virtual memory map, returns the new address.
4. The pages are not necessarily physically allocated yet — they are mapped but not backed by physical RAM until actually written (demand paging).
5. malloc returns a pointer to the caller.
</details>
