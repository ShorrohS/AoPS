# Module 4.3 — Operating System Concepts

---

## The Problem

> You have a CPU that can execute programs.
> You have memory that stores them.
> You have I/O devices to communicate with the world.
>
> Now run *two programs at once*.
>
> How do you prevent program A from reading program B's memory?
> Who decides which program gets the CPU, and for how long?
> What happens when a program wants to write to disk — does it get direct access to the hardware?
>
> These are the problems the **operating system** exists to solve.

An OS is not magic. It is a program — but a privileged one, with exclusive access to hardware, that manages resources on behalf of all other programs and enforces the boundaries between them.

---

## The Story

### Early Computers Had No OS

On early computers, one program ran at a time. The programmer submitted a job (usually a deck of punch cards), the operator loaded it, it ran, and the output was collected. If the program crashed or ran forever, the operator killed it manually.

The **batch OS** (late 1950s) automated job sequencing: when one program finished, the OS automatically loaded the next. Still one program at a time, but no human required between jobs.

**Time-sharing** (1960s) was the revolution: multiple users sharing one computer simultaneously. The OS rapidly switched between programs, giving each a short burst of CPU time. Each user felt they had a dedicated machine. **CTSS** (MIT, 1961), **Multics** (1965–1969), and **Unix** (1969–1973) emerged from this era.

Unix's influence dominates to this day. Linux, macOS, Android, iOS, and BSD are all Unix-descended systems. Even Windows NT borrowed heavily from Unix/VMS concepts.

---

### Kernel vs User Space

The operating system enforces a hardware-enforced boundary between two privilege levels:

**Kernel space**: where the OS kernel runs. Direct access to hardware, memory, all CPU instructions. A bug here crashes the entire system.

**User space**: where all applications run. Cannot directly access hardware. Cannot access another process's memory. Cannot execute privileged CPU instructions. A crash here only kills that one process.

The CPU enforces this via **privilege rings** (or protection levels). x86 has 4 rings (0–3); modern OSes use only ring 0 (kernel) and ring 3 (user). ARM uses EL0 (user) through EL3 (firmware).

The boundary exists for security and stability: a buggy or malicious user program cannot crash the system or access another program's data. Without this boundary, every program crash would bring down the whole machine — which is exactly what happened on early unprotected systems.

---

### System Calls — The Bridge

User programs cannot access hardware directly. But they need to — to read files, write to screen, open network connections, allocate memory. The mechanism is the **system call** (syscall).

A system call is a controlled transition from user space to kernel space:

1. User program places syscall number in `rax` and arguments in `rdi, rsi, rdx, ...`
2. User program executes the `syscall` instruction
3. CPU switches to ring 0, jumps to the kernel's syscall handler
4. Kernel validates arguments, performs the requested operation
5. Kernel places result in `rax`, returns to user space (ring 3)

```nasm
; Linux x86-64 — write "hello" to stdout
mov rax, 1          ; syscall #1 = write
mov rdi, 1          ; fd = 1 (stdout)
mov rsi, msg_ptr    ; pointer to message
mov rdx, 5          ; length = 5
syscall             ; enter kernel
; rax now holds number of bytes written (or negative error code)
```

**Common Linux syscalls:**

| Number | Name | Description |
|---|---|---|
| 0 | `read` | Read from file descriptor |
| 1 | `write` | Write to file descriptor |
| 2 | `open` | Open a file |
| 3 | `close` | Close a file descriptor |
| 9 | `mmap` | Map memory |
| 11 | `munmap` | Unmap memory |
| 12 | `brk` | Adjust heap break |
| 60 | `exit` | Terminate process |
| 57 | `fork` | Create child process |
| 59 | `execve` | Execute new program |

The C standard library (`libc`) wraps syscalls in convenient functions: `printf()` calls `write()`, `malloc()` calls `brk()` or `mmap()`, `fopen()` calls `open()`. You use these every day without thinking about the syscall layer beneath.

---

### Processes and Context Switching

A **process** is an instance of a running program. It consists of:
- A **virtual address space** (more on this in Module 4.4)
- A set of open **file descriptors**
- A **process ID (PID)**
- A **program counter** and register state
- A **stack** and **heap**

The OS gives the illusion that multiple processes run simultaneously. In reality (on a single core), only one runs at a time. The OS uses a **timer interrupt** to periodically preempt the running process and switch to another.

**Context switch:**
1. Timer interrupt fires — CPU jumps to kernel
2. Kernel saves all registers of the running process to its **Process Control Block (PCB)**
3. Kernel scheduler selects the next process to run
4. Kernel restores the registers of the new process from its PCB
5. Kernel returns to user space — the new process resumes exactly where it left off

A context switch takes ~1–10 microseconds. A modern system performs thousands per second. This is why time-sharing feels instantaneous to humans, whose perception latency is ~10 milliseconds.

---

### The Scheduler

The **scheduler** decides which process runs next. Key policies:

**Round Robin**: each process gets a fixed time quantum (e.g., 10 ms). Fair but ignores priority.

**Priority scheduling**: higher-priority processes preempt lower-priority ones. Risk: **starvation** — a low-priority process may never run if high-priority ones keep arriving.

**Completely Fair Scheduler (CFS)** — used by Linux: tracks each process's "virtual runtime" (time actually executed, normalised by priority). Always runs the process with the smallest virtual runtime. Achieves fairness without explicit time quanta.

**Real-time scheduling**: hard deadlines. A process must run within a guaranteed time window. Used in embedded systems, audio drivers, industrial control.

---

### Files, Processes, and Everything as Files

Unix's most elegant abstraction: **everything is a file**. A regular file, a directory, a terminal, a network socket, a hardware device — all accessed via the same system calls: `open`, `read`, `write`, `close`.

This uniformity means: a program that reads from stdin (`fd = 0`) can be redirected to read from a file, a network socket, or another program's stdout — without changing a line of the program. This is the foundation of Unix pipes and redirection.

```bash
ls -la | grep ".c" | sort > output.txt
```
Each `|` creates a pipe: a kernel buffer where the stdout of one process is connected to the stdin of the next. Three processes, running concurrently, communicating through the kernel.

---

## The Concept: The OS as a Resource Manager

The OS does three things:
1. **Isolation**: each process believes it owns the whole computer. Hardware enforces this illusion.
2. **Multiplexing**: one CPU, many processes; one disk, many files; one network, many connections.
3. **Abstraction**: expose clean interfaces (files, sockets, processes) that hide messy hardware realities.

Every program you have ever used benefits from all three simultaneously.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Process Scheduler Visualiser**
- A set of processes with different priorities and run states
- Step through scheduler ticks manually or run automatically
- Watch context switches happen — see which process is "running" vs "ready" vs "waiting"
- Compare Round Robin vs Priority scheduling outcomes

**Tool 2 — Syscall Tracer**
- A "Hello World" program executes symbolically
- Every system call is shown: number, arguments, kernel activity, return value
- Observe: even `printf("Hello\n")` requires a syscall chain

**Tool 3 — Kernel/User Space Boundary**
- A process attempts privileged operations
- In user mode: operation blocked, exception raised
- In kernel mode: operation succeeds
- Visualise the ring level of every instruction

---

## Going Deeper

**fork() and exec()**: Unix process creation uses two syscalls. `fork()` creates an exact copy of the current process (child). `exec()` replaces the current process's memory with a new program. The shell uses this pattern constantly: fork a child, exec the requested command in the child, parent waits for the child to finish. This two-step design allows the shell to set up pipes and redirections between fork and exec — before the new program starts.

**Signals**: asynchronous notifications sent to a process. `SIGTERM` asks it to terminate gracefully. `SIGKILL` kills it immediately (cannot be caught). `SIGSEGV` fires when a process accesses invalid memory (segfault). `SIGINT` is sent when you press Ctrl+C. Signal handlers are registered with the kernel and called asynchronously.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace a process through scheduler states, decode syscall sequences, reason about kernel/user privilege, and analyse what strace output tells you about a running program.
