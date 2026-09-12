# AoPS — Art of Problem Solving
## Master Autonomous Agent Guide & Unified Steering Document

> **Document Version:** 1.0.0  
> **Last Updated:** 2026-09-12  
> **Target Audience:** All AI Agents, Autonomous Subagents, and Human Collaborators  
> **Primary Workspace:** `c:\Users\ssro2\OneDrive\Desktop\Projects\eBooks\AoPS`  
> **Companion Workspace:** `c:\Users\ssro2\OneDrive\Desktop\Projects\eBooks\AoPS_Young_Explorers`  
> **Rule of Engagement:** **THIS IS THE LIVING MASTER GUIDE.** Every AI agent working on this repository MUST read this file first, follow its standards, execute tasks against its roadmap, and update this file's status tracker and changelog before finishing work.

---

## Table of Contents

1. [Executive Summary & Multi-Track Architecture](#1-executive-summary--multi-track-architecture)
2. [Complete Repository Map & Current State](#2-complete-repository-map--current-state)
3. [Integrated Steering & Core Philosophies](#3-integrated-steering--core-philosophies)
   - [3.1 Pedagogical Philosophy & 5 Golden Rules](#31-pedagogical-philosophy--5-golden-rules)
   - [3.2 The Japanese Zen Minimalist Simulation Design System](#32-the-japanese-zen-minimalist-simulation-design-system)
   - [3.3 The Ebook Publishing & Typesetting System](#33-the-ebook-publishing--typesetting-system)
   - [3.4 The Young Explorers Storybook Transformation Framework](#34-the-young-explorers-storybook-transformation-framework)
4. [Master Curriculum & Module Directory (Levels 0–12)](#4-master-curriculum--module-directory-levels-012)
5. [Operational Roadmap — What We Are Doing and How](#5-operational-roadmap--what-we-are-doing-and-how)
   - [Track A: Technical Curriculum & Simulation Polish](#track-a-technical-curriculum--simulation-polish)
   - [Track B: Publishing Pipeline & PDF Generation Engine](#track-b-publishing-pipeline--pdf-generation-engine)
   - [Track C: Ebook Digital Edition Production](#track-c-ebook-digital-edition-production)
   - [Track D: Young Explorers Children's Picture Book Series](#track-d-young-explorers-childrens-picture-book-series)
6. [AI Agent Standard Operating Procedures (SOPs)](#6-ai-agent-standard-operating-procedures-sops)
   - [SOP-01: How to Pick Up a Task](#sop-01-how-to-pick-up-a-task)
   - [SOP-02: Simulation Development & Design System Adherence](#sop-02-simulation-development--design-system-adherence)
   - [SOP-03: Lesson & Challenge Authoring](#sop-03-lesson--challenge-authoring)
   - [SOP-04: Illustration Production](#sop-04-illustration-production)
   - [SOP-05: Running the PDF Engine](#sop-05-running-the-pdf-engine)
   - [SOP-06: Updating the Master Guide](#sop-06-updating-the-master-guide)
7. [Living Progress Matrix & Status Tracker](#7-living-progress-matrix--status-tracker)
8. [Agent Changelog & Contribution History](#8-agent-changelog--contribution-history)

---

## 1. Executive Summary & Multi-Track Architecture

The **AoPS (Art of Problem Solving)** project is an end-to-end, first-principles Computer Science educational initiative. Its premise:

> *"We don't teach computing. We rebuild it from scratch, one problem at a time."*

From the earliest mechanical counters (Napier's Bones, Jacquard Loom) to modern Transistors, Operating Systems, Compilers, Distributed Systems, and Advanced Generative AI/Agents, the project reconstructs the intellectual history of computing without hand-waving or skipping layers of abstraction.

The overall initiative operates across **four interconnected production tracks**:

```
                                 ┌────────────────────────────────────────────────────────┐
                                 │                 AoPS SOURCE CURRICULUM                 │
                                 │          13 Levels | 70 Modules | 70 Lessons           │
                                 └───────────────────────────┬────────────────────────────┘
                                                             │
                    ┌────────────────────────────────────────┼────────────────────────────────────────┐
                    ▼                                        ▼                                        ▼
   ┌─────────────────────────────────┐      ┌─────────────────────────────────┐      ┌─────────────────────────────────┐
   │    TRACK A: SIMULATIONS &       │      │   TRACK B: PUBLISHING & PDF     │      │   TRACK C & D: ADAPTATION &     │
   │    INTERACTIVE LABORATORY       │      │   Automated compilation via     │      │   YOUNG EXPLORERS STORYBOOKS    │
   │ 70 Browser-based HTML5/JS tools │      │   generate_pdf.py & ReportLab   │      │ 13 Children's Picture Books     │
   │ Zen Minimalist Design System    │      │   Complete Review Edition PDF   │      │ Ages 5–10, Character Bible,     │
   │ Bento Box Layout, zero install  │      │   Ebook HTML/CSS front/covers   │      │ Metaphorical Story Spreads      │
   └─────────────────────────────────┘      └─────────────────────────────────┘      └─────────────────────────────────┘
```

---

## 2. Complete Repository Map & Current State

The workspace is organized into clear domain directories:

```
AoPS/
├── MASTER_GUIDE.md                  ← [THIS FILE] Unified master guide for all agents & tasks
├── README.md                        ← Public overview of the technical curriculum
├── AoPS_PDF_Summary.json            ← Compilation manifest of latest PDF build
├── AoPS_Review_Edition_v1.pdf       ← Compiled 800+ KB PDF review edition (13 levels, 70 modules)
├── generate_pdf.py                  ← ReportLab automation script assembling the full course PDF
├── New_TMTB_Prompt.md               ← Creative brief for the "Young Explorers" 13-book adaptation
├── .kiro/
│   └── steering/
│       ├── aops-course-guide.md     ← Foundational curriculum & pedagogical guidelines
│       └── design-system.md         ← Japanese Zen Minimalist UI rules for interactive simulations
├── course/                          ← Core technical curriculum: 13 Levels (0 through 12)
│   ├── level-0-before-computers/    ← 5 modules (Jacquard, Babbage, Hollerith, etc.)
│   ├── level-1-physical-computing/  ← 6 modules (Relays, Vacuum tubes, Transistors, Moore's Law)
│   ├── level-2-digital-foundations/ ← 6 modules (Binary, Logic gates, Adders, Sequential, ALU)
│   ├── level-3-machine-architecture/← 5 modules (Memory hierarchy, FDE cycle, Toy ISA, Bus, I/O)
│   ├── level-4-software-foundations/← 5 modules (Assembly, Stack, OS kernels, Virtual memory, FS)
│   ├── level-5-programming/         ← 6 modules (C close-to-metal, Python, Data models)
│   ├── level-6-dsa/                 ← 8 modules (Arrays, Trees, Graphs, Sorting, DP)
│   ├── level-7-systems/             ← 5 modules (Concurrency, Sockets, Tiny Shell, HTTP)
│   ├── level-8-networks/            ← 6 modules (OSI/TCP-IP, DNS, Routing, TLS/SSL)
│   ├── level-9-databases/           ← 4 modules (B-Trees, Relational, ACID, Toy SQL engine)
│   ├── level-10-web/                ← 4 modules (DOM, Rendering engines, REST, Web apps)
│   ├── level-11-ai-ml/              ← 5 modules (Linear algebra, Neural nets, Backprop, Transformers)
│   └── level-12-advanced-ai/        ← 5 modules (LLMs, Embeddings, RAG, AI Agents, Ethics)
│       *(Every module contains: lesson.md, simulation.html, and challenge.md)*
├── illustrations/                   ← 78 standalone interactive SVG/HTML visual explanation files
│   ├── index.html                   ← Visual gallery / showcase of all course illustrations
│   └── level-0/ ... level-12/       ← Module-by-module interactive visual assets (220+ figures)
├── ebook/                           ← Digital ebook and print typesetting assets
│   ├── covers/                      ← Volume covers (volume-0-cover.html, etc.)
│   ├── design-system/               ← Book design system (DESIGN-SYSTEM.md, preview, aops-book.css)
│   ├── front-matter/                ← Title page, Copyright, Dedication, Preface, TOC
│   └── level-0/chapter-1/           ← Chapter-level responsive book layouts (chapter-1.html, md)
└── [External Sibling Repo]
    └── ../AoPS_Young_Explorers/     ← The children's picture book production repository
        ├── 00-series-bible/         ← Character bible, design system, style guide, synopses
        └── book-00-before-computers/← Book 00 manuscript, illustration briefs, prototype
```

---

## 3. Integrated Steering & Core Philosophies

*(Synthesizing `.kiro/steering/aops-course-guide.md`, `.kiro/steering/design-system.md`, `ebook/design-system/DESIGN-SYSTEM.md`, and `New_TMTB_Prompt.md`)*

### 3.1 Pedagogical Philosophy & 5 Golden Rules

1. **The "Why First" Rule:** Every lesson opens with the human crisis, bottleneck, or historical tension that forced an invention into existence (e.g., the 1880 census taking 8 years leading to Hollerith's tabulating machine). Never present an abstraction before the pain point is felt.
2. **Hands-On is Non-Negotiable:** Every lesson must have an interactive browser simulation and a practical, graded challenge. No passive reading allowed.
3. **Precision Over Breadth:** Deep mastery of fundamental mechanisms (e.g., how voltage levels represent truth values, or how flip-flops latch state) precedes high-level conveniences.
4. **Physical Simulations for Hardware:** Relays, vacuum tubes, flip-flops, and transistor switches must be interactively modeled in browser-native code. Hand-waving is strictly prohibited.
5. **Progressive Complexity & Naming Abstractions:** Each layer builds upon the prior. When introducing an abstraction (e.g., a function call, a virtual memory page table, or an HTTP socket), agents must explicitly identify the lower-level hardware/software mechanics being hidden.

#### Standard Module Structure (`lesson.md`)
Every `lesson.md` across all 70 modules must follow this exact template:
```markdown
# Module X.Y — [Title]

## The Problem
> What human need, physical limitation, or frustration drove this invention?

## The Story
Historical and narrative context (vivid, concise, character-driven).

## The Concept
Precise technical explanation with architectural diagrams.

## Hands-On Exercise
Step-by-step guided walkthrough using the accompanying simulation.html.

## Going Deeper
One layer below the abstraction (hardware physics, machine code, or mathematical proof).

## Challenge
Measurable problem with verification criteria. (Detailed in challenge.md).
```

---

### 3.2 The Japanese Zen Minimalist Simulation Design System

All simulations (`simulation.html`) must use the **Japanese Zen Minimalist** aesthetic archetype (*Wabi-Sabi Precision*).

#### Core Aesthetic Tenets
- **Ma (間) — Negative Space:** Whitespace is active structure. Let circuits, numbers, and diagrams breathe.
- **Wabi-Sabi Surfaces:** Warm stone and unbleached washi paper tones (`#F4F3EF`, `#FDFDFD`) rather than blinding white or generic neon dark modes.
- **Sumi Ink Precision:** Hairline rules (`1px solid #1C1C1C` or `#D8D6CE`) mimicking sumi brushstrokes on parchment.
- **Lacquer & Indigo Accents:** Deep Indigo (`#1C2D42`) for structure and charts; Lacquer Red (`#C82A2A`) for active states, current flow, and triggers; Antique Gold (`#8B6914`) for success/solved states.
- **Bento Box Layout:** Standard 2-zone layout: 65% left canvas (visual simulation) + 35% right panel (controls, telemetry, logs).

#### Mandatory CSS Design Tokens
All `simulation.html` files must declare these tokens in `:root`:

```css
:root {
  /* Surfaces */
  --bg-paper:      #F4F3EF;   /* Warm Stone — page base */
  --bg-washi:      #FDFDFD;   /* Pure Washi — panel & card surface */
  --bg-warm:       #EEECE6;   /* Deeper warm tone — hover/active */
  --bg-canvas:     #F8F7F3;   /* Simulation canvas base */

  /* Sumi Ink Typography */
  --text-sumi:     #1C1C1C;   /* Near-black primary text */
  --text-body:     #3A3A3A;   /* High-contrast body text */
  --text-muted:    #888880;   /* Secondary metadata */
  --text-ghost:    #BBBBB5;   /* Disabled / placeholder */

  /* Accents */
  --accent-red:    #C82A2A;   /* Lacquer Red — active/current */
  --accent-indigo: #1C2D42;   /* Deep Indigo — structural */
  --accent-gold:   #8B6914;   /* Antique Gold — success/clock */
  --accent-ink:    #1C1C1C;   /* Sumi Ink — interactive */

  /* Borders & Radii */
  --border-hair:   #1C1C1C;   /* Primary hairline (1px solid) */
  --border-light:  #D8D6CE;   /* Separators & grid */
  --border-paper:  #E8E6DF;   /* Subtle structural edges */
  --radius-xs:     2px;       /* Sharp, hard-edged minimalist */
  --radius-sm:     4px;

  /* Animation Easing */
  --ease-out:      cubic-bezier(0.16, 1, 0.3, 1);
  --t-fast:        120ms;
  --t-med:         240ms;
}
```

#### Canvas Direct Color Palette
In `<canvas>` 2D rendering contexts where CSS variables cannot be resolved, use these literal hex codes:
- Background: `#F8F7F3`
- Active Wires / Signal High: `#C82A2A` (Lacquer Red)
- Inactive Wires / Low: `#D8D6CE` (Hairline Grey)
- Logic Gates / Nodes: `#1C1C1C` (Sumi Ink)
- Clock Pulse / Success: `#8B6914` (Antique Gold)
- Electron Dots / Particles: `#1C2D42` (Indigo)

---

### 3.3 The Ebook Publishing & Typesetting System

For print (A5 / Hardcover) and high-end digital formats (`ebook/`):
- **Page Dimensions:** A5 Standard (148 × 210mm). Inner gutter 20mm, outer margin 28mm (thumb zone + margin notes), top 18mm, bottom 16mm.
- **Typography Scale:**
  - Book Title: `Noto Serif JP` (Light 300, 48–56px)
  - Chapter Heading: `Noto Serif JP` (32px, leading 1.15)
  - Body Text: `EB Garamond` / `Libre Baskerville` (16–17px, leading 1.75, sumi ink `#1C1C1C`)
  - Metadata & Labels: `Inter` (10–12px uppercase, tracking 0.12em)
  - Code & Registers: `JetBrains Mono` (12–13px, padded warm parchment fill `#EEECE4`)
- **Rules:** First paragraph after heading has zero indent; subsequent paragraphs carry `text-indent: 1.4em`. Chapter openings feature a 3-line drop cap in Deep Indigo.

---

### 3.4 The Young Explorers Storybook Transformation Framework

For the companion children's edition (Ages 5–10):
- **Core Ratio:** 70–80% visual storytelling, 20–30% text (20–80 words per spread).
- **Format:** 13 standalone hardcover picture books (Books 00 through 12).
- **Atmosphere:** Evoking *Rosie Revere, Engineer*, *Ada Twist, Scientist*, and *Ten Minutes to Bed*. Warm, painterly, whimsical, timeless.
- **Recurring Cast of Characters:**
  1. **Mira:** South Asian girl explorer, teal vest, amber glasses. The reader's stand-in.
  2. **Cog:** Small brass clockwork automaton companion who remembers every journey.
  3. **Professor Hollis:** Scholarly mentor with two pocket watches and endless curiosity.
  4. **Volt:** Energetic electricity sprite who can never sit still.
  5. **Bit & Bob:** The binary twin sprites (one white, one midnight-blue).
  6. **Wren:** The memory elephant with glasses perched on her trunk.
  7. **Finn:** The logic fox with a chalkboard of IF/THEN decisions.
  8. **Percy:** The packet pigeon flying messages across stormy digital seas.
  9. **Sage:** The great library dragon who categorizes all human knowledge.
  10. **Echo:** The gentle learning machine helper discovering how to understand human speech.

---

## 4. Master Curriculum & Module Directory (Levels 0–12)

The curriculum consists of **13 Levels, 70 Modules, 70 Lessons, 70 Simulations, and 70 Challenges**:

| Level | Title | Modules | Theme / Key Breakthroughs |
|:-----:|:------|:-------:|:--------------------------|
| **0** | Before Computers | 5 | Census crisis, Napier's bones, Pascaline, Jacquard loom, Babbage Difference Engine, Hollerith tabulator |
| **1** | Physical Computing | 6 | Electrons & circuits, Relays, Relay logic gates, Vacuum tubes, Transistors, Moore's Law |
| **2** | Digital Foundations | 6 | Noise immunity, Binary/Octal/Hex, Boolean algebra & NAND, Ripple-carry adders, Flip-flops, 4-bit ALU |
| **3** | Machine Architecture | 5 | SRAM/DRAM memory hierarchy, Fetch-Decode-Execute cycle, Toy 8-instruction ISA, Memory-mapped I/O, System bus |
| **4** | Software Foundations | 5 | x86-64 assembly & NASM, Call stack & frames, OS kernel & syscalls, Virtual memory & TLB, File system inodes |
| **5** | Programming | 6 | C memory model & pointers, Compilation pipeline, Python runtime, OOP data model, Dynamic typing |
| **6** | Data Structures & Algorithms | 8 | Arrays/Lists, Hash table collision resolution, Trees (BST/AVL), Heaps, Graphs (Dijkstra/A*), Sorting, DP |
| **7** | Systems Programming | 5 | Threads & mutexes, Race conditions, POSIX sockets, Tiny Unix shell, Barebones HTTP web server |
| **8** | Networks & Protocols | 6 | OSI & TCP/IP stack, Ethernet frames, IP routing, TCP handshakes & flow control, DNS resolution, TLS 1.3 |
| **9** | Databases | 4 | Relational algebra, B-Trees & indexing, ACID transactions & WAL, Building a toy SQL engine |
| **10** | Web Development | 4 | HTML DOM tree, CSS layout & repaint pipeline, JavaScript event loop & V8, REST APIs & Full-stack |
| **11** | AI & Machine Learning | 5 | Matrix transformations, Gradient descent, Multilayer perceptrons, Backprop derivation, CNNs & Attention |
| **12** | Advanced AI | 5 | Transformer LLM architecture, Vector embeddings, Retrieval-Augmented Generation (RAG), AI Agents, Ethics |

---

## 5. Operational Roadmap — What We Are Doing and How

### Track A: Technical Curriculum & Simulation Polish
1. **Audit All 70 Simulations:** Ensure all simulations conform strictly to the Zen Minimalist design system (`:root` tokens, `#F4F3EF` background, `#1C1C1C` borders, Noto Serif JP + Inter + JetBrains Mono typography).
2. **Interactive Polish:** Verify that every simulation includes:
   - Interactive slider/switch controls with instantaneous canvas redraw.
   - Real-time telemetry readouts (`.zen-stat-val`).
   - Terminal log pane (`.zen-log`) detailing internal state transitions.
   - Functional `Reset` and `Preset` buttons.
3. **Cross-Browser Verification:** Verify responsiveness and layout fidelity across mobile and desktop viewports.

### Track B: Publishing Pipeline & PDF Generation Engine
1. **Hardening `generate_pdf.py`:**
   - Eliminate hardcoded user paths (`c:\Users\NDH01061\...`) by replacing them with dynamic relative paths: `BASE = Path(__file__).resolve().parent`.
   - Ensure ReportLab handles Unicode symbols and code formatting cleanly.
2. **Review Edition Builds:** Maintain `AoPS_Review_Edition_v1.pdf` and `AoPS_PDF_Summary.json` as release artifacts, verifying 0 missing lessons, 0 missing challenges, and 0 missing illustrations.

### Track C: Ebook Digital Edition Production
1. **Expand Front Matter & Chapters:** Complete HTML chapter editions in `ebook/level-X/` mirroring the styling defined in `ebook/design-system/DESIGN-SYSTEM.md` and `aops-book.css`.
2. **Interactive EPUB / Web Book Output:** Package chapters into an interconnected static reading interface.

### Track D: Young Explorers Children's Picture Book Series
1. **Series Bible Sync:** Maintain strict alignment between `AoPS` and `AoPS_Young_Explorers/00-series-bible/`.
2. **Book Production (00 through 12):**
   - Translate each module's technical core into storybook scenes.
   - Produce 20–28 full-spread illustration briefs and image generation prompts per book.
   - Create read-aloud manuscripts featuring Mira, Cog, and domain companions.
   - Build interactive story prototypes (e.g., `book-00-before-computers/module-0-1-prototype/prototype.html`).

---

## 6. AI Agent Standard Operating Procedures (SOPs)

Whenever an AI agent is invoked to work on any task in this repository, the agent **MUST** follow these procedures:

### SOP-01: How to Pick Up a Task
1. **Read `MASTER_GUIDE.md` First:** Inspect this file to understand the architecture, design tokens, and current module status.
2. **Inspect Existing Files:** Always read the targeted module's `lesson.md`, `simulation.html`, and `challenge.md` before making modifications. Never rewrite from scratch if existing work can be improved.
3. **Preserve Educational Intent:** Maintain the "Why First" rule and conceptual rigor.

### SOP-02: Simulation Development & Design System Adherence
1. **Single-File Native HTML:** Simulations must run directly in the browser with no build step, no npm install, and no external framework.
2. **Mandatory Fonts:** Include Google Fonts `<link>` for `Noto Serif JP`, `Inter`, and `JetBrains Mono`.
3. **CSS Tokens:** Import or inline the complete `:root` tokens from Section 3.2. Never use pure black `#000000` or sterile white `#FFFFFF`.
4. **Bento Grid:** Structure the container with `.zen-canvas-wrap` (left 60–70%) and `.zen-ctrl` (right 30–40%).
5. **No Broken Controls:** Every slider, button, and input must be hooked up to an event listener that updates the visualization immediately.

### SOP-03: Lesson & Challenge Authoring
1. **Adhere to the Universal Template:** Use the 6 standard headers (The Problem, The Story, The Concept, Hands-On Exercise, Going Deeper, Challenge).
2. **Concrete Challenges:** Challenges must have specific input test cases, expected outputs, and step-by-step rubrics.

### SOP-04: Illustration Production
1. **Location:** Store module illustrations in `illustrations/level-X/module-X-Y-[name].html`.
2. **Format:** Use responsive vector SVG embedded within Zen Minimalist preview containers.
3. **Gallery Registration:** Register every new illustration module in `illustrations/index.html`.

### SOP-05: Running the PDF Engine
1. **Run Command:**
   ```powershell
   python generate_pdf.py
   ```
2. **Verify Output:** Inspect `AoPS_PDF_Summary.json` to ensure:
   - `missing_lessons`: 0
   - `missing_challenges`: 0
   - `missing_illustrations`: 0
   - File size and page count are healthy.

### SOP-06: Updating the Master Guide
1. **MANDATORY FINAL STEP:** Before completing any agent interaction that alters files, updates modules, or advances a track, the agent **MUST edit Section 7 (Progress Matrix) and Section 8 (Changelog)** of this `MASTER_GUIDE.md` file.

---

## 7. Living Progress Matrix & Status Tracker

*Legend: ✅ Complete & Validated | 🟡 In Polish / Retrofit | 🔵 In Progress | ⚪ Planned*

| Level | Module | Module Title | Technical Lesson | Interactive Simulation | Challenge Rubric | Illustration Page | Ebook HTML | Young Explorers Book |
|:-----:|:------:|:-------------|:----------------:|:----------------------:|:----------------:|:-----------------:|:----------:|:--------------------:|
| **0** | **0.1** | Why Did Humans Need to Compute? | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | 🟡 Prototype Spread |
| **0** | **0.2** | Early Mechanical Computation | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **0** | **0.3** | The Loom That Taught Computers | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **0** | **0.4** | Babbage & Ada: First Programmers | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **0** | **0.5** | Hollerith & Punch Card Era | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **1** | **1.1** | What is Electricity? | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **1** | **1.2** | Switches: The Atom of Computing | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **1** | **1.3** | Relay Logic: Metal Decisions | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **1** | **1.4** | Vacuum Tubes: Faster Switching | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **1** | **1.5** | The Transistor Revolution | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **1** | **1.6** | From Transistors to Chips: Moore | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **2** | **2.1** | Why Binary? Physics of Two States | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **2** | **2.2** | Number Systems: Bin, Oct, Hex | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **2** | **2.3** | Boolean Algebra & Logic Gates | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **2** | **2.4** | Combinational Circuits | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **2** | **2.5** | Sequential Circuits & Memory | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **2** | **2.6** | From Gates to a Simple ALU | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **3** | **3.1** | Memory: How Machines Remember | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **3** | **3.2** | Fetch-Decode-Execute Cycle | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **3** | **3.3** | Instruction Set Architecture | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **3** | **3.4** | Input/Output: Connecting World | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **3** | **3.5** | The Bus: Moving Data Around | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **4** | **4.1** | Machine Code & Assembly | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **4** | **4.2** | Stack & Calling Conventions | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **4** | **4.3** | Operating System Concepts | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **4** | **4.4** | Memory Management & Paging | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **4** | **4.5** | File Systems & Inodes | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **5** | **5.1** | C: Close to the Metal | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **5** | **5.2** | Python: High-Level Abstraction | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **5** | **5.3** | Compilation vs Interpretation | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **5** | **5.4** | Functions, Scope & Lifetimes | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **5** | **5.5** | Memory Allocation & Heap | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **5** | **5.6** | Debugging & Profiling | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **6** | **6.1** | Arrays & Contiguous Memory | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **6** | **6.2** | Linked Lists & Pointers | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **6** | **6.3** | Stacks & Queues | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **6** | **6.4** | Hash Tables & Collisions | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **6** | **6.5** | Trees & Binary Search | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **6** | **6.6** | Priority Queues & Heaps | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **6** | **6.7** | Graphs & Pathfinding | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **6** | **6.8** | Dynamic Programming | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **7** | **7.1** | Processes & Threads | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **7** | **7.2** | Concurrency & Mutexes | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **7** | **7.3** | Sockets & IPC | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **7** | **7.4** | Building a Tiny Shell | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **7** | **7.5** | Building a Tiny HTTP Server | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **8** | **8.1** | Physical & Data Link Layers | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **8** | **8.2** | IP Addressing & Routing | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **8** | **8.3** | TCP & Reliable Streams | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **8** | **8.4** | UDP & Real-Time Media | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **8** | **8.5** | DNS & Name Resolution | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **8** | **8.6** | TLS/SSL & Secure Channels | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **9** | **9.1** | The Relational Model & SQL | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **9** | **9.2** | B-Trees & Storage Engines | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **9** | **9.3** | Transactions & ACID | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **9** | **9.4** | Building a Toy SQL Database | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **10** | **10.1** | How Browsers Render Pages | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **10** | **10.2** | Modern CSS Layout & Flex/Grid | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **10** | **10.3** | JavaScript Event Loop & Async | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **10** | **10.4** | Building a Full-Stack Web App | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **11** | **11.1** | Linear Algebra for ML | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **11** | **11.2** | Gradient Descent & Optimizers | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **11** | **11.3** | Neural Networks from Scratch | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **11** | **11.4** | Backpropagation Derived | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **11** | **11.5** | Convolution & Attention | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **12** | **12.1** | LLM Architecture & Tokens | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **12** | **12.2** | Vector Embeddings & Similarity | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **12** | **12.3** | Retrieval-Augmented Generation | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **12** | **12.4** | Autonomous AI Agents | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |
| **12** | **12.5** | AI Alignment, Safety & Ethics | ✅ | ✅ Zen Styled | ✅ | ✅ | ✅ Complete | ⚪ |

---

## 8. Agent Changelog & Contribution History

Every agent making changes in the codebase must append an entry here describing what was done, files touched, and resulting status.

| Timestamp (UTC/Local) | Agent / Subagent | Scope / Files Touched | Description of Work Performed |
|:----------------------|:-----------------|:----------------------|:------------------------------|
| 2026-09-12 16:35 IST | Master Agent | `MASTER_GUIDE.md`, `README.md` | Created comprehensive master autonomous agent guide unifying steering rules, curriculum map (all 70 modules), design system, publishing engine, Young Explorers roadmap, and agent SOPs. |
| 2026-09-12 16:45 IST | Master Agent | `ebook/level-0-ebook.html`, `MASTER_GUIDE.md` | Conducted automated quality audit on Level 0 assets (100% pass) and compiled full publication-grade HTML eBook (`ebook/level-0-ebook.html`) with Cover, Front Matter, Prologue, Modules 0.1–0.5, 24 embedded vector SVGs, Simulation cards, Challenges, and Epilogue. |
| 2026-09-12 18:00 IST | Master Agent | `ebook/level-1-ebook.html` through `ebook/level-12-ebook.html`, `MASTER_GUIDE.md` | Compiled all remaining 12 curriculum volumes (Levels 1–12) into publication-grade, self-contained HTML eBooks under Japanese Zen Minimalist design system. Total 13 volumes (70 chapters, 246 vector SVGs, 3.75 MB) now 100% complete and visually validated in browser. |

