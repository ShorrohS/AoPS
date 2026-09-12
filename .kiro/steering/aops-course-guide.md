---
inclusion: always
---

# AoPS — Art of Problem Solving: Complete Computer Science Course Guide

## Course Philosophy

**Learn by Doing. Always.**

Every concept in this course — from the very first electric signal to training a neural network — is taught through the lens of *why it was needed* and *what problem it solved*. Theory lives inside practice, not above it.

> "We don't teach computing. We rebuild it from scratch, one problem at a time."

---

## Guiding Principles for Every Lesson

### 1. The "Why First" Rule
Every lesson must open with the **human problem that forced this invention into existence**. Students must understand the itch before they see the scratch.

### 2. Hands-On is Non-Negotiable
Every single lesson — without exception — must contain:
- **At least one practical exercise** (simulation, code, circuit builder, or physical model)
- **At least one challenge question** at the end (simulation-based or code-based)

### 3. Precision Over Breadth
Cover fewer things deeply rather than many things shallowly. A student who truly understands binary addition is more valuable than one who has skimmed 10 topics.

### 4. Simulations for Physical Concepts
When a concept requires physical hardware (punch cards, relay circuits, vacuum tubes, transistors), an **interactive browser-based simulation** must be built or referenced. No hand-waving allowed.

### 5. Progressive Complexity
Each module builds on the previous. Introduce new abstractions only when the lower-level reality is understood. Never skip a layer.

---

## Course Architecture

```
LEVEL 0 — Before Computers (The Why)
LEVEL 1 — Physical Computing (Electricity → Logic)
LEVEL 2 — Digital Foundations (Binary → Gates → Circuits)
LEVEL 3 — Machine Architecture (CPU, Memory, I/O)
LEVEL 4 — Software Foundations (Assembly → OS Concepts)
LEVEL 5 — Programming (C → Python → Algorithms)
LEVEL 6 — Data Structures & Algorithms
LEVEL 7 — Systems Programming
LEVEL 8 — Networks & Protocols
LEVEL 9 — Databases
LEVEL 10 — Web & Application Development
LEVEL 11 — Artificial Intelligence & Machine Learning
LEVEL 12 — Advanced AI (Deep Learning, LLMs, Agents)
```

---

## Full Course Content Map

---

### LEVEL 0 — Before Computers: The Human Problem

**Module 0.1 — Why Did Humans Need to Compute?**
- The census problem (1880 US Census took 8 years)
- Astronomical tables and navigation errors
- Artillery trajectory calculations in WW1/WW2
- Lesson: Computation is a necessity born from scale

**Module 0.2 — Early Mechanical Computation**
- Abacus and counting boards
- Napier's Bones (1617)
- Pascal's Pascaline (1642) — first mechanical calculator
- Leibniz's Stepped Reckoner
- 🛠 **Simulation**: Interactive virtual Pascaline — add two numbers mechanically
- 🎯 **Challenge**: Calculate 347 × 6 using simulated Napier's Bones

**Module 0.3 — The Loom That Taught Computers**
- Joseph Jacquard's loom (1804) — holes in cards control patterns
- The concept of *stored instructions*
- How Babbage saw the connection
- 🛠 **Simulation**: Interactive punched card pattern designer — design a weave pattern
- 🎯 **Challenge**: Encode a 4-row pattern as a punch card sequence

**Module 0.4 — Babbage and Ada: The First Programmers**
- The Difference Engine and Analytical Engine
- Ada Lovelace's Note G — the first algorithm
- Why Babbage's machine was never finished (funding, precision)
- 🛠 **Simulation**: Difference Engine stepping through polynomial calculation
- 🎯 **Challenge**: Write out Ada's Bernoulli number algorithm in plain steps

**Module 0.5 — Hollerith and the Punch Card Era**
- Herman Hollerith's tabulating machine (1890 census: 6 weeks!)
- How punch cards encode data (rows, columns, holes)
- IBM's birth from the Tabulating Machine Company
- 🛠 **Simulation**: Interactive punch card encoder/decoder (text → holes → decode)
- 🎯 **Challenge**: Encode your name in Hollerith code and decode a mystery card

---

### LEVEL 1 — Physical Computing: From Electricity to Logic

**Module 1.1 — What is Electricity? (Only What We Need)**
- Electrons, voltage, current, resistance (intuitive, not mathematical)
- The water analogy for circuits
- Open vs closed circuits
- 🛠 **Simulation**: Circuit sandbox — build a simple light bulb circuit
- 🎯 **Challenge**: Build a circuit that lights two bulbs in series vs parallel and observe the difference

**Module 1.2 — Switches: The Atom of Computing**
- A switch is a binary device: on or off
- Telegraph relays — the first electrically controlled switches
- How a relay works (electromagnet closes a contact)
- 🛠 **Simulation**: Animated relay — click to energize coil, watch contact close
- 🎯 **Challenge**: Wire two relays so that BOTH must be ON to light a bulb (AND logic)

**Module 1.3 — Relay Logic: Building Decisions from Metal**
- Shannon's 1937 thesis — circuits can implement Boolean algebra
- AND, OR, NOT using physical relays
- Building a half adder from relays
- 🛠 **Simulation**: Relay circuit builder — drag and drop relays to build logic gates
- 🎯 **Challenge**: Build an OR gate and a NOT gate from relays in the simulator

**Module 1.4 — Vacuum Tubes: Faster Switching**
- Why relays were too slow and too mechanical
- How a triode vacuum tube amplifies and switches
- ENIAC — 18,000 vacuum tubes (1945)
- Power, heat, and reliability problems
- 🛠 **Simulation**: Virtual vacuum tube — visualize electron flow with grid voltage control
- 🎯 **Challenge**: Compare switching speed: relay (milliseconds) vs tube (microseconds) — calculate how many more operations per second tubes enable

**Module 1.5 — The Transistor: Revolution in a Grain of Sand**
- Bell Labs, 1947 — Shockley, Bardeen, Brattain
- How a transistor switches current with a tiny control signal
- Why transistors beat vacuum tubes (size, heat, speed, reliability)
- From discrete transistors to integrated circuits (Jack Kilby, 1958)
- 🛠 **Simulation**: Transistor switch simulator — control a motor with a small signal
- 🎯 **Challenge**: Calculate how many transistors fit on a 1mm² chip if each is 5nm wide (2024 reality)

**Module 1.6 — From Transistors to Chips: Moore's Law**
- Intel 4004 (1971): 2,300 transistors
- Moore's Law explained and its real-world implications
- Modern chips: billions of transistors
- Why this matters for everything that comes next
- 🛠 **Simulation**: Interactive Moore's Law timeline chart — explore transistor counts across decades
- 🎯 **Challenge**: Predict (with math) when we hit physical limits if transistors halve every 2 years

---

### LEVEL 2 — Digital Foundations: The Language of Machines

**Module 2.1 — Why Binary? The Physics of Two States**
- Noise immunity: why analog fails at scale
- High voltage = 1, Low voltage = 0
- Bits, bytes, words
- 🛠 **Simulation**: Analog vs digital signal noise demonstration
- 🎯 **Challenge**: Convert decimal 255, 42, and 128 to binary by hand then verify

**Module 2.2 — Number Systems: Binary, Octal, Hex**
- Positional notation revisited
- Binary arithmetic (add, subtract)
- Two's complement for negative numbers
- Hex as shorthand for binary
- 🛠 **Simulation**: Interactive base converter with step-by-step working shown
- 🎯 **Challenge**: Add 0b10110111 + 0b01101001 in binary, then verify in decimal

**Module 2.3 — Boolean Algebra and Logic Gates**
- Boole's algebra (1854) applied to circuits
- Truth tables for AND, OR, NOT, NAND, NOR, XOR, XNOR
- Gate symbols and circuit diagrams
- NAND as the universal gate
- 🛠 **Simulation**: Logic gate sandbox — drag gates, wire inputs, watch truth tables fill live
- 🎯 **Challenge**: Implement XOR using only NAND gates (4 gates)

**Module 2.4 — Combinational Circuits**
- Half adder and full adder
- Ripple carry adder (4-bit)
- Multiplexers and demultiplexers
- Encoders and decoders
- 🛠 **Simulation**: 4-bit adder simulator — input two binary numbers, watch carry propagate
- 🎯 **Challenge**: Design a 1-bit full adder truth table and implement it in the gate sandbox

**Module 2.5 — Sequential Circuits: Memory from Gates**
- Feedback loops and state
- SR Latch, D Latch, D Flip-Flop
- Clock signals and synchronous circuits
- Registers (N flip-flops = N bits of storage)
- 🛠 **Simulation**: D flip-flop animator — clock it manually, watch Q change
- 🎯 **Challenge**: Build a 2-bit counter using D flip-flops in the simulator

**Module 2.6 — From Gates to a Simple ALU**
- Arithmetic Logic Unit — the heart of computation
- Adding a control signal: choose ADD or AND
- Flags: zero, carry, overflow
- 🛠 **Simulation**: 4-bit ALU simulator — pick operation, input values, see result and flags
- 🎯 **Challenge**: Use the ALU to compute 13 - 7 using two's complement addition

---

### LEVEL 3 — Machine Architecture

**Module 3.1 — Memory: How Machines Remember**
- SRAM (flip-flop based) vs DRAM (capacitor based)
- Address space and addressability
- The memory hierarchy: registers → cache → RAM → disk
- 🛠 **Simulation**: Visual memory array — write to and read from addresses manually
- 🎯 **Challenge**: Write "HELLO" into a simulated 8-byte memory as ASCII values

**Module 3.2 — The Fetch-Decode-Execute Cycle**
- Instructions as numbers stored in memory
- Program Counter (PC), Instruction Register (IR)
- The three-step cycle that runs every program ever written
- 🛠 **Simulation**: Animated CPU cycle — watch PC increment, instruction load, execute
- 🎯 **Challenge**: Manually trace 5 instructions through the FDE cycle on paper, then verify

**Module 3.3 — Instruction Set Architecture (ISA)**
- What an instruction set is and why it matters
- RISC vs CISC philosophies
- Simple toy ISA: define 8 instructions
- Encoding instructions as binary
- 🛠 **Simulation**: Toy CPU with 8-instruction ISA — write a simple add-and-store program
- 🎯 **Challenge**: Write a program in the toy ISA that computes the sum of 1+2+3+4+5

**Module 3.4 — Input/Output: Connecting to the World**
- Memory-mapped I/O
- Interrupts vs polling
- From punch cards → keyboards → USB
- 🛠 **Simulation**: Toy CPU with a virtual "keyboard" and "display" peripheral
- 🎯 **Challenge**: Write a toy ISA program that reads a number and doubles it to the display

**Module 3.5 — The Bus: Moving Data Around**
- Address bus, data bus, control bus
- Bus arbitration and why it matters
- Von Neumann vs Harvard architecture
- 🛠 **Simulation**: Animated system bus — watch data flow between CPU, RAM, and I/O
- 🎯 **Challenge**: Identify and label all bus transactions in a simple program execution trace

---

### LEVEL 4 — Software Foundations

**Module 4.1 — Machine Code and Assembly Language**
- Binary instructions are unreadable — we need mnemonics
- Assembler: translates text to binary
- Writing real x86-64 assembly (Linux, NASM)
- 🛠 **Hands-On**: Write and run "Hello, World" in assembly (NASM + Linux or online assembler)
- 🎯 **Challenge**: Write assembly that computes the factorial of 5

**Module 4.2 — The Stack and Calling Conventions**
- Stack pointer, base pointer
- push, pop, call, ret
- How function calls work at the machine level
- 🛠 **Hands-On**: Trace a function call in a debugger (GDB or online)
- 🎯 **Challenge**: Write an assembly function that returns the max of two numbers

**Module 4.3 — Operating System Concepts**
- Why we need an OS (resource management, abstraction)
- Kernel vs user space
- System calls: the bridge
- Processes and context switching
- 🛠 **Simulation**: Process scheduler visualizer — watch processes get CPU time
- 🎯 **Challenge**: List all system calls made by a "Hello World" C program using strace

**Module 4.4 — Memory Management**
- Virtual memory and address spaces
- Pages, frames, page tables
- The MMU and TLB
- Segmentation faults explained from hardware up
- 🛠 **Simulation**: Virtual memory translator — enter virtual address, walk page table
- 🎯 **Challenge**: Calculate the physical address for a given virtual address with a 2-level page table

**Module 4.5 — File Systems**
- Files as named byte sequences
- Inodes, directories, links
- FAT vs ext4 vs NTFS (concepts)
- 🛠 **Simulation**: Visual inode explorer — create files, watch inode table update
- 🎯 **Challenge**: Trace what disk reads happen when you open and read /home/user/hello.txt

---

### LEVEL 5 — Programming Languages

**Module 5.1 — C: Close to the Metal**
- Why C was invented (portable assembly)
- Compilation pipeline: preprocessing → compiling → assembling → linking
- Pointers explained from memory addresses up
- 🛠 **Hands-On**: Build a simple memory allocator in C
- 🎯 **Challenge**: Implement strlen() from scratch without using any library functions

**Module 5.2 — Python: Abstraction for Humans**
- Interpreted vs compiled
- Dynamic typing and garbage collection
- The Python data model
- 🛠 **Hands-On**: Implement a linked list in Python from scratch
- 🎯 **Challenge**: Write a Python decorator that times any function it wraps

**Modules 5.3–5.6** — Algorithms, recursion, sorting, searching (detailed in Level 6)

---

### LEVEL 6 — Data Structures & Algorithms

*(Full detail in course files — each topic has simulation + challenge)*

- Arrays, Linked Lists, Stacks, Queues
- Hash Tables (with collision resolution simulations)
- Trees: BST, AVL, Red-Black
- Heaps and Priority Queues
- Graphs: BFS, DFS, Dijkstra, A*
- Sorting: Bubble → Merge → Quick → Radix
- Dynamic Programming
- 🛠 Each has: animated visualizer + coding challenge

---

### LEVEL 7 — Systems Programming

- Multithreading and concurrency
- Mutexes, semaphores, deadlocks
- Network sockets from scratch
- Building a tiny shell
- Building a tiny HTTP server

---

### LEVEL 8 — Networks & Protocols

- Physical layer → Data Link → Network → Transport → Application
- Ethernet, IP, TCP, UDP, DNS, HTTP/HTTPS
- TLS/SSL from first principles
- 🛠 Build a packet analyzer in Python

---

### LEVEL 9 — Databases

- Relational model and SQL
- B-trees and why databases use them
- Transactions, ACID, isolation levels
- Building a toy SQL engine

---

### LEVEL 10 — Web & Application Development

- HTML/CSS/JS from ground up
- How browsers render pages
- REST APIs and JSON
- Full-stack project

---

### LEVEL 11 — Artificial Intelligence & Machine Learning

- What is intelligence? Search and constraint satisfaction
- Linear algebra for ML (with visual simulations)
- Regression, classification, neural networks from scratch
- Backpropagation derived and implemented
- CNNs, RNNs, Transformers

---

### LEVEL 12 — Advanced AI

- Large Language Models: architecture and training
- Embeddings and vector databases
- Retrieval-Augmented Generation
- AI Agents: planning, tool use, memory
- Ethics and safety

---

## Lesson Template (Every Lesson Must Follow This)

```markdown
# Module X.Y — [Title]

## The Problem
> What human need or frustration drove this invention?

## The Story
Historical/narrative context (concise, vivid)

## The Concept
Precise technical explanation

## Hands-On Exercise
[Simulation link or code exercise]
Step-by-step guided walkthrough

## Going Deeper
One layer below the abstraction (optional but encouraged)

## Challenge
[Simulation-based or code-based]
Specific, measurable problem to solve
Hints available on request
Solution revealed only after attempt
```

---

## Simulation Standards

All simulations built in this course must:
- Run in the browser (HTML/CSS/JavaScript — no install required)
- Be self-contained single-file or minimal-file implementations
- Have clear controls with labels
- Show intermediate state (not just input → output)
- Be mobile-friendly where feasible
- Include a "Reset" button

---

## Progression Rules

| Rule | Detail |
|------|--------|
| No skipping levels | A student must demonstrate the previous level's challenge before advancing |
| Simulation before code | Physical concepts get a simulation before any code is written |
| Name the abstraction | When introducing an abstraction, always name what it hides |
| Build before use | Build a simplified version of every major tool before using the real one |

---

## File & Folder Convention

```
AoPS/
├── .kiro/steering/aops-course-guide.md   ← This file
├── course/
│   ├── level-0-before-computers/
│   ├── level-1-physical-computing/
│   ├── level-2-digital-foundations/
│   ├── level-3-machine-architecture/
│   ├── level-4-software-foundations/
│   ├── level-5-programming/
│   ├── level-6-dsa/
│   ├── level-7-systems/
│   ├── level-8-networks/
│   ├── level-9-databases/
│   ├── level-10-web/
│   ├── level-11-ai-ml/
│   └── level-12-advanced-ai/
└── simulations/
    ├── level-0/
    ├── level-1/
    └── ...
```

Each level folder contains:
- `README.md` — level overview
- `module-X-Y/` — one folder per module
  - `lesson.md` — the lesson content
  - `simulation.html` — the hands-on simulation (self-contained)
  - `challenge.md` — the challenge question and rubric

---

## Current Status & Master Steering

> **Note for AI Agents & Collaborators:**  
> The centralized master guide governing all active tracks, design systems, module directories, and agent SOPs is maintained in **[MASTER_GUIDE.md](file:///c:/Users/ssro2/OneDrive/Desktop/Projects/eBooks/AoPS/MASTER_GUIDE.md)** at the root of this repository.

- [x] Steering files created
- [x] Level 0 — Before Computers (complete — 5 modules)
- [x] Level 1 — Physical Computing (complete — 6 modules)
- [x] Levels 2–12 — Digital Foundations through Advanced AI (complete — 59 modules)
- [x] All 70 Modules: 70 Lessons, 70 Simulations, 70 Challenges, 78 Illustration Pages
- [x] Automated Review Edition PDF generation engine (`generate_pdf.py`)
- [ ] Active: Japanese Zen Minimalist design system polish across all simulations
- [ ] Active: Young Explorers 13-Book Picture Book Series adaptation

---

*This document governs all content created under the AoPS course. Every lesson, simulation, and challenge must conform to the standards above and in MASTER_GUIDE.md.*
