# Module 3.4 — Input/Output: Connecting to the World

---

## The Problem

> You have a CPU that fetches, decodes, and executes instructions.
> You have memory that stores programs and data.
>
> But a computer that can only read from and write to its own memory is useless.
> How does it accept input from a keyboard?
> How does it send output to a screen?
> How does it read a file from disk?
>
> The answer is **Input/Output (I/O)** — the mechanisms by which a CPU communicates with the world outside its own chip.

Without I/O, a computer is a sealed box performing calculations no one can see and responding to nothing. I/O is what connects the silicon to the world.

---

## The Story

### The First I/O: Punch Cards and Lights

The earliest computers had no keyboard, no screen. Programs were loaded via **punched cards** fed into a card reader — a mechanical device that detected holes and converted them to electrical signals. Output was printed on paper or displayed as patterns of lights on a front panel.

The operator's interaction with the computer was entirely through these physical media. A program could take minutes to load and hours to run. Output was not real-time — it was retrieved after the job completed.

The concept of **interactive computing** — where a human types and the computer responds immediately — did not exist until the 1960s. The development of time-sharing operating systems and terminals made it possible. This was considered revolutionary.

---

### Three I/O Methods

**Method 1 — Programmed I/O (Polling)**

The CPU directly controls the I/O device by reading and writing specific addresses. To check if a key has been pressed, the CPU reads a "status register" address and tests a bit. If not ready, it reads it again. And again. And again.

```
loop:
  READ status_register → A
  AND A, 0x01          ; test the "data ready" bit
  JZ loop              ; if not ready, keep polling
  READ data_register → B  ; now read the actual data
```

This is called **polling** or **busy-waiting**. It works, but the CPU wastes 100% of its time checking — it can do nothing else while waiting for I/O.

Analogy: standing at the front door staring at the letterbox, checking every second if a letter has arrived.

**Method 2 — Interrupts**

The CPU continues executing its program normally. When an I/O device has data ready, it sends an **interrupt signal** to the CPU.

The CPU:
1. Finishes the current instruction
2. Saves the current PC and registers to the stack
3. Jumps to an **Interrupt Service Routine (ISR)** — a special function that handles the event
4. The ISR reads the data from the I/O device
5. The ISR restores registers and returns to the interrupted program

The CPU can do useful work between I/O events. The keyboard only interrupts when a key is actually pressed — perhaps 10 times per second, consuming a tiny fraction of CPU time.

Analogy: put a doorbell on the front door. You do your work. The doorbell rings when a letter arrives.

**Method 3 — Direct Memory Access (DMA)**

For high-bandwidth I/O (disk, network, video), even interrupt-driven I/O is too slow — the CPU would spend all its time copying bytes from the I/O device into memory.

DMA gives the I/O device direct access to memory **without involving the CPU**:

1. CPU programs the DMA controller: "copy 4096 bytes from disk to address 0x8000"
2. CPU continues executing other code
3. DMA controller handles all the data transfer autonomously
4. When done, DMA controller interrupts the CPU
5. CPU reads the data at 0x8000 — already there

Modern SSDs, GPUs, and network cards all use DMA. Without it, a CPU reading a 1 GB file would spend nearly all its time doing memory copies instead of useful computation.

---

### Memory-Mapped I/O

How does the CPU "talk to" an I/O device? There are two approaches:

**Port-mapped I/O**: separate IN/OUT instructions with a separate I/O address space (x86 uses this historically).
```nasm
IN  al, 0x60   ; read from keyboard port 0x60
OUT 0x61, al   ; write to speaker port 0x61
```

**Memory-mapped I/O (MMIO)**: I/O devices appear at specific memory addresses. Reading from or writing to those addresses communicates with the device — no special instructions needed.

```
Address 0xFFFF0000: keyboard status register
Address 0xFFFF0001: keyboard data register
Address 0xFFFF0010: screen framebuffer start
```

When the CPU writes to 0xFFFF0010, the value doesn't go to RAM — it goes to the video controller, which displays it on screen.

**Modern practice**: almost all modern systems use MMIO. ARM processors use MMIO exclusively. Memory-mapped I/O makes device drivers simpler — they just use regular memory read/write operations.

---

### The Journey of a Keystroke

Let's trace what happens when you press the 'A' key:

1. **Physical**: the key closes a circuit, sending a voltage signal
2. **Keyboard controller**: detects the closed circuit, generates a scancode (0x1C for 'A' on a standard layout)
3. **Keyboard buffer**: stores the scancode in a small internal buffer
4. **Hardware interrupt**: keyboard controller asserts the IRQ1 interrupt line
5. **CPU**: finishes current instruction, saves state, jumps to keyboard ISR
6. **ISR**: reads the scancode from the keyboard data port, translates to ASCII ('A' = 0x41), stores in OS keyboard buffer
7. **ISR return**: CPU restores state, continues previous program
8. **Application**: calls `read()` system call, OS returns 'A' from the keyboard buffer
9. **Terminal/shell**: receives 'A', echoes it to screen, adds to input line

This entire chain — from key press to character appearing on screen — takes approximately 1–10 milliseconds. Most of that time is in the OS and display pipeline. The hardware interrupt itself is handled in microseconds.

---

### From Punch Cards to USB

**Punch cards (1890s–1970s)**: data encoded as holes; mechanical reader converts holes to signals; output via line printer  
**Serial terminals (1960s–1980s)**: RS-232 serial connection; text only; 110–9600 baud  
**Parallel port (1970s–2000s)**: 8 data lines + control lines; used for printers; up to 1 MB/s  
**PS/2 (1987–present)**: dedicated keyboard/mouse port; synchronous serial protocol  
**USB (1996–present)**: Universal Serial Bus; hot-pluggable; 1.5 Mb/s to 40 Gb/s (USB4); handles keyboard, mouse, storage, audio, video, charging  
**PCIe (2003–present)**: high-speed bus for GPUs, NVMe SSDs, network cards; PCIe 5.0 = 128 GB/s (×16 slot)

Every peripheral you connect to a computer uses one of these protocols to convert physical signals into data the CPU can read.

---

## The Concept: Every Peripheral is a Memory Address

The elegance of MMIO is the reduction: **every I/O operation becomes a memory read or write**. The CPU doesn't need to know whether it's talking to RAM or a GPU or a network card. It just reads and writes addresses. The hardware behind those addresses handles the rest.

This abstraction is what makes device drivers possible. A driver is a program that knows the memory-mapped register layout of a specific device and uses regular memory operations to control it.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Polling vs Interrupts**
- A simulated keyboard generates keystrokes at random intervals
- In Polling mode: watch the CPU loop, burning cycles waiting
- In Interrupt mode: watch the CPU run a "useful computation" program; interrupts fire when keys arrive
- Compare CPU utilisation: polling shows ~0% useful work; interrupt shows ~95%

**Tool 2 — DMA Transfer**
- Simulate copying 256 bytes from a "disk" device to memory
- With DMA off: watch the CPU copy byte by byte (256 separate load/store cycles)
- With DMA on: the DMA controller handles the copy; CPU continues executing code; interrupt fires on completion

**Tool 3 — Memory Map Explorer**
- A visual 64KB memory map showing RAM, MMIO, ROM regions
- Click any region to see which device it controls
- Simulate reading a keypress via MMIO address

---

## Going Deeper

**Interrupt priorities and nested interrupts**: Not all interrupts are equally urgent. A system timer interrupt can wait; a hardware fault cannot. CPUs implement an interrupt priority scheme (IRQ levels). A high-priority interrupt can interrupt the ISR of a low-priority interrupt — creating nested interrupt handling. Real-time operating systems (RTOS) depend on this for guaranteed response times.

**I/O schedulers**: When many processes are reading from disk simultaneously, the OS I/O scheduler decides the order. The classic "elevator algorithm" minimises disk head movement by servicing requests in sweep order (like an elevator going up then down). Modern SSDs don't have a mechanical head, so SSDs use different scheduling strategies optimised for parallelism.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Compare polling vs interrupt CPU utilisation, trace a DMA transfer, write polling and interrupt-driven I/O code in pseudo-assembly, and reason about the memory map of a simple embedded system.
