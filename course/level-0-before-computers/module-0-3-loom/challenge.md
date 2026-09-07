# Challenge 0.3 — Program the Loom

**Type:** Simulation design + binary encoding + pattern decoding  
**Estimated time:** 30–40 minutes  
**Tools needed:** `simulation.html` open in your browser + pen and paper

---

## Part A — Design and Weave (Simulation)

Using the **Punch Card Designer** in the simulation, design card chains to produce the following patterns. For each, take note of your card design (which holes you punched).

The loom has **8 threads** (columns) and you can use up to **8 cards** (rows).

### Pattern 1 — Checkerboard
Row 1: threads 1,3,5,7 UP  
Row 2: threads 2,4,6,8 UP  
Row 3: threads 1,3,5,7 UP  
Row 4: threads 2,4,6,8 UP  

Punch this pattern, weave it, and confirm the checkerboard appears in the fabric preview.

### Pattern 2 — Horizontal Stripes
Design a pattern that produces **two thick horizontal stripes** — a dark band of 3 rows, then a light band of 3 rows (or similar alternating blocks). Define your own hole pattern to achieve this.

### Pattern 3 — Your Initials
Try to weave the first letter of your name. Use all 8 rows. Describe the pattern you're going for and how you encoded it.

---

## Part B — Binary Encoding

A punch card row can be written as a binary number. We use this convention:

- Column 1 = most significant bit (leftmost, bit 7)
- Column 8 = least significant bit (rightmost, bit 0)
- Hole = **1**, No hole = **0**

### Task

Write out your **8-card chain for the Checkerboard pattern** (Part A, Pattern 1) as:
1. A binary string for each row (8 bits)
2. The decimal equivalent of each row
3. The hexadecimal equivalent of each row

Use this table format:

| Card | Binary | Decimal | Hex |
|------|--------|---------|-----|
| 1    | `????` | ??      | 0x?? |
| 2    | `????` | ??      | 0x?? |
| 3    | `????` | ??      | 0x?? |
| 4    | `????` | ??      | 0x?? |

---

## Part C — Decode the Mystery Pattern

Below is a card chain encoded as binary. Decode it to answer: **what pattern does this weave?**

| Card | Binary     | Your decoding (which threads are UP?) |
|------|------------|--------------------------------------|
| 1    | `11100000` | ? |
| 2    | `10010000` | ? |
| 3    | `10010000` | ? |
| 4    | `11100000` | ? |
| 5    | `10010000` | ? |
| 6    | `10010000` | ? |
| 7    | `11100000` | ? |
| 8    | `00000000` | ? |

1. Fill in which threads are UP for each row (thread 1=leftmost bit)
2. Sketch the resulting pattern on graph paper (or describe it precisely)
3. What letter of the alphabet does this pattern most closely resemble?

---

## Part D — The Big Idea Question

Answer these in writing (2–4 sentences each):

1. **Before Jacquard**, how did the weaver know which threads to raise? What were the limitations of this approach?

2. **After Jacquard**, what changed? Who or what now holds the "knowledge" of the pattern?

3. **The connection to software**: Explain in your own words why the punch card principle is the conceptual foundation of software. Use the phrase "separation of program from machine" in your answer.

4. **Trade-off**: The Jacquard system made mass production of complex patterns easy. But what capability did weavers *lose* that a skilled hand-weaver had? (Hint: think about what a human can do that a card cannot.)

---

## Rubric

| Part | Points | What we're looking for |
|------|--------|------------------------|
| A — 3 patterns woven correctly | 30 | Patterns match description; simulation used |
| B — Binary/Hex encoding table | 25 | Correct bit mapping and conversions |
| C — Mystery decode + letter ID | 20 | Correct thread decode; letter identified |
| D1–D4 — Written answers | 25 | Precise, thoughtful, uses correct vocabulary |

**Total: 100 points**

---

## Hints

<details>
<summary>Hint — Part B conversion</summary>
For binary to decimal: weight each bit by its power of 2 from right.
`10101010` = 128+0+32+0+8+0+2+0 = 170 = 0xAA
</details>

<details>
<summary>Hint — Part C mystery letter</summary>
Draw an 8×8 grid. Shade the cells where the bit is 1. Look at the shape from a distance.
</details>

<details>
<summary>Hint — Part D trade-off</summary>
Think about what happens when a weaver makes a mistake mid-pattern on a Jacquard loom vs by hand.
</details>

---

## Solutions

<details>
<summary>Part B — Checkerboard Encoding Solution</summary>

Threads 1,3,5,7 UP = columns 1,3,5,7 = bits 7,5,3,1 = `10101010`  
Threads 2,4,6,8 UP = columns 2,4,6,8 = bits 6,4,2,0 = `01010101`

| Card | Binary     | Decimal | Hex   |
|------|------------|---------|-------|
| 1    | `10101010` | 170     | 0xAA  |
| 2    | `01010101` | 85      | 0x55  |
| 3    | `10101010` | 170     | 0xAA  |
| 4    | `01010101` | 85      | 0x55  |

Note: 0xAA and 0x55 are the classic alternating-bit byte patterns used in memory testing to this day.
</details>

<details>
<summary>Part C — Mystery Decode Solution</summary>

```
Card 1: 11100000 → threads 1,2,3 UP      ███░░░░░
Card 2: 10010000 → threads 1,4 UP         █░░█░░░░
Card 3: 10010000 → threads 1,4 UP         █░░█░░░░
Card 4: 11100000 → threads 1,2,3 UP      ███░░░░░
Card 5: 10010000 → threads 1,4 UP         █░░█░░░░
Card 6: 10010000 → threads 1,4 UP         █░░█░░░░
Card 7: 11100000 → threads 1,2,3 UP      ███░░░░░
Card 8: 00000000 → no threads UP          ░░░░░░░░
```

The pattern is the letter **P** (or B depending on interpretation).  
The top three rows form the top curve of a P/B; rows 4–7 are the bottom bulge; row 8 is the baseline.

</details>

<details>
<summary>Part D — Sample Answers</summary>

**D1:** Before Jacquard, the weaver (or drawboy) held the pattern in memory and manually raised threads by hand or with pulled cords. Limitations: prone to error, couldn't run unattended, new patterns required new training, couldn't run faster than the weaver could think.

**D2:** After Jacquard, the "knowledge" of the pattern moved into the card chain. The loom reads the cards and acts mechanically. No human memory is required during operation — just card loading and maintenance.

**D3:** Software is the separation of instructions from the machine that executes them. Before the punch card, a loom could only weave what its physical structure determined. After the punch card, the same loom could weave any pattern — all that changed was the cards. Similarly, a computer's hardware stays fixed; only the software (program) changes. The punch card proved that instructions can be encoded, stored, and loaded separately from the executing mechanism. That is the definition of a program.

**D4:** A skilled hand-weaver could *adapt* in real-time — they could improvise, correct errors mid-row, make creative decisions on the fly, or adjust to a broken thread. A Jacquard loom follows the card chain literally. It cannot decide, adapt, or improvise. A error on card 47 in a 2,000-card chain runs identically every time until a human intervenes and replaces the card.

</details>
