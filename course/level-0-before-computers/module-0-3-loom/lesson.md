# Module 0.3 — The Loom That Taught Computers

---

## The Problem

> You own a silk weaving factory in Lyon, France, in 1800. Your most valuable product is fabric woven in complex patterns — flowers, birds, geometric designs that wealthy clients pay a fortune for.
>
> Each pattern requires a master weaver to manually control which threads go up and which go down on every single pass of the shuttle. One wrong move and the pattern breaks. A skilled weaver takes **years** to learn. They are expensive, they tire, they make mistakes, and they can only work on one pattern at a time.
>
> If a pattern is successful, you want to make thousands of metres of it. But the weaver must essentially re-learn the pattern for every metre — holding the entire sequence in their head.
>
> How do you separate the *knowledge of the pattern* from the *act of weaving*?

This is not a question about fabric. It is the question that gave birth to the concept of **stored instructions** — the idea that a procedure can be written down and executed by a machine without a human in the loop.

---

## The Story

### Weaving Before Jacquard

A loom works by lifting certain warp threads (running lengthwise) while passing a shuttle carrying the weft thread (running crosswise) through the gap. By changing which warp threads are raised on each pass, you create patterns.

In a simple loom, this was done by hand — the weaver manually selected threads. For complex patterns, a **drawboy** sat beside the loom, pulling cords to raise groups of threads according to the weaver's shouted instructions. The drawboy had to memorize or follow a complex sequence. Errors were common. The drawboy had to be trained for each new pattern.

The bottleneck: **the pattern existed only in human memory and voice**.

---

### Basile Bouchon's Paper Roll — 1725

The first attempt to automate pattern control came from Basile Bouchon in 1725. He created a mechanism where a roll of paper with holes punched in it was pressed against a row of needles. Where there was a hole, a needle passed through and lifted a thread hook. Where there was no hole, the needle was blocked.

**The profound shift**: the pattern is no longer in a person's head. It is encoded as **holes in paper** — a physical, durable, reproducible medium.

This is the first time in history that **data was stored externally to a human mind and read by a machine**.

The limitation: Bouchon's roll only controlled a portion of the threads. A human operator still controlled the rest.

---

### Falcon's Punched Cards — 1728

Jean-Baptiste Falcon improved on Bouchon three years later by replacing the paper roll with a **chain of stiff punched cards**, linked together in sequence. Each card controlled one row of the pattern. Cards could be detached and rearranged.

Two key advances:
1. **Discrete units**: each card was a separate instruction (not a continuous roll)
2. **Reordering**: patterns could be modified by rearranging cards

This is the birth of **sequential, discrete instructions** — the ancestor of every program ever written.

---

### Jacquard's Loom — 1804

Joseph Marie Jacquard synthesized and perfected these ideas into a complete automated system in 1804. His attachment sat on top of a standard loom and completely automated the thread selection process.

**How it works:**

1. A chain of stiff punched cards passes over a square cylinder (prism)
2. On each pass of the shuttle, the next card is pressed against a row of spring-loaded needles
3. **Where there is a hole**: the needle passes through, hooks its corresponding thread hook, raises the warp thread → thread is UP
4. **Where there is no hole**: the needle is blocked, the thread is NOT lifted → thread is DOWN
5. The shuttle passes through the gap created by the raised threads
6. The next card advances — the next row of the pattern is set

The complete pattern — potentially thousands of rows — is stored in the card chain. The loom executes it automatically, row by row, without any human decision-making during operation.

**One key number**: A Jacquard loom could execute a pattern requiring 24,000 cards in sequence. A single weaver could then produce complex silk damask at the rate a simple loom produces plain fabric.

---

### The Reaction

The impact was immediate and violent. Lyon's weavers rioted. Jacquard was attacked in the street. His looms were burned. The city council confiscated the machines.

Then economics won. By 1812, Napoleon had ordered 11,000 Jacquard looms installed across France. By 1833, there were 30,000 in Lyon alone. The weavers who once opposed the machine now operated it.

---

### Babbage Sees It

Charles Babbage visited a weaving exhibition in London in the 1830s and saw a portrait of Jacquard himself — **woven in silk on a Jacquard loom**, using 24,000 punch cards. The portrait had the photographic detail of an engraving.

Babbage later wrote: *"The Jacquard loom is capable of weaving any design which the imagination of man may conceive."*

He immediately grasped that the same principle — **instructions stored on cards, read sequentially by a machine** — could control a calculating engine. Not just weaving, but any computation.

This insight is the direct intellectual link between the Jacquard loom and the Analytical Engine (Module 0.4) — and by extension, to every computer ever built.

---

## The Concept: What a Punch Card Actually Is

A punch card is a **binary encoding of instructions**.

Each position on the card can be either:
- **Hole** → 1 (do this: lift this thread / read this data)
- **No hole** → 0 (don't do this: leave thread down / skip)

A row of 8 positions gives you 8 binary decisions. That's 1 byte. A card with 24 rows of 80 positions is 1,920 bits = 240 bytes.

This is not a metaphor. IBM's 80-column punch cards, used until the 1980s, encoded exactly 80 characters of data per card using a binary hole/no-hole scheme — the direct industrial descendant of Jacquard's system.

### The Three Revolutionary Ideas

| Idea | What it meant |
|------|--------------|
| **External instruction storage** | The program lives outside the machine; it can be saved, copied, edited |
| **Sequential execution** | Cards are read in order; the machine follows a defined sequence of steps |
| **Separation of program from machine** | The same loom can weave any pattern; the same computer can run any program |

The third idea is the most profound. Before Jacquard, a machine did one thing. After Jacquard, a machine + a card chain was **general-purpose within its domain**. You didn't need a different loom for each pattern — you needed different cards.

You don't need a different computer for each program. You need different software.

**This is the conceptual birth of software.**

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

The simulation has two interconnected tools:

**Tool 1 — Punch Card Designer**
- A grid of 8 columns × 8 rows
- Click any cell to punch a hole (●) or leave it blank (○)
- Each row represents one pass of the shuttle
- Each column controls one thread (UP if hole, DOWN if no hole)

**Tool 2 — Loom Animator**
- Press "Weave" to execute your card chain row by row
- Watch which threads rise (shown in gold) and which stay down (shown in grey)
- Watch the woven pattern build up, row by row, in the fabric preview

**What to try:**
1. Punch a checkerboard pattern (alternate holes row by row) and weave it
2. Create a diagonal stripe
3. Try to create the letter "H" in the fabric

**Key observation:** Once you've designed the card chain, the loom executes it identically every time. Change one card → only that row changes.

---

## Going Deeper

The Jacquard loom didn't just inspire Babbage. It is the ancestor of:

- **Piano rolls** (1800s): punched paper rolls storing musical performances
- **Player pianos**: reading holes → pressing keys (mechanical music playback)
- **Telegraphs and teletypes**: punched tape for transmitting messages
- **IBM punch cards**: 80-column cards used in mainframes until the 1980s
- **Perforated tape**: used to program early NC (numerically controlled) machine tools
- **CD/DVD pits and lands**: optical discs encode 0s and 1s as microscopic holes (pits) and flat areas (lands) — same principle, laser instead of needle

The hole-as-instruction is one of humanity's most durable ideas.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Design a 4-row punch card sequence that weaves a specific pattern, encode it as binary, then decode a mystery card sequence and identify the pattern it produces.
