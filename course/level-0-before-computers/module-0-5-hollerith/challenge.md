# Challenge 0.5 — The Hollerith Tabulator

**Type:** Simulation use + encoding + data analysis + Level 0 capstone questions  
**Estimated time:** 40–50 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Encode and Punch

Using the **Card Puncher** in the simulation, encode the following 5 census respondents as punch cards. For each person, record which column positions are punched.

| # | Name | Age | Occupation | Birthplace | Family Size |
|---|------|-----|------------|------------|-------------|
| 1 | John Hayes | 34 | Farmer | Ireland | 5 |
| 2 | Clara Schmidt | 28 | Teacher | Germany | 2 |
| 3 | Marcus Freeman | 45 | Laborer | Virginia | 7 |
| 4 | Mei Lin | 22 | Seamstress | China | 3 |
| 5 | Robert Walsh | 61 | Merchant | New York | 1 |

After punching, write down the binary representation (hole=1, no hole=0) for the **Age field** of each card.

---

## Part B — Tally with the Tabulator

Using the **Tabulator** tool, run all 5 cards through. Then answer:

1. How many people are aged **under 35**?
2. How many are **foreign-born** (not born in a US state)?
3. What is the most common **occupation** in your deck?
4. What is the **average family size** across all 5 records?

---

## Part C — Sort and Analyze

Using the **Card Sorter**, sort the 5 cards by **occupation**.

1. List which cards end up in each occupation bin.
2. Now sort by **age group** (under 30 / 30–49 / 50+). List the bins.
3. In the real 1890 census, the sorter could group 65 cards per minute. If you had 62,979,766 cards and 100 sorters, how many minutes would it take to do one full sort pass? Convert to hours. (Show your working.)

---

## Part D — Decode the Mystery Deck

The simulation's Mystery Deck tab contains 8 pre-punched cards. Run them through the tabulator and sorter, then answer:

1. How many people are in the mystery deck?
2. What are the distinct occupations represented?
3. What is the most common birthplace?
4. Based on age distribution, is this deck likely from a rural farming community or an urban industrial area? Justify your answer in 2–3 sentences using the data you gathered.

---

## Part E — Level 0 Capstone

Answer each question in **3–5 sentences**. This is your graduation from Level 0.

**E1 — The Thread Through All Five Modules**

Trace a single continuous idea from the Jacquard loom (Module 0.3) through to the Hollerith tabulator (Module 0.5). How does the concept of "a hole as an instruction" evolve into "a hole as data"? What stays the same? What changes?

**E2 — The Abstraction Stack**

By the end of Level 0, we have these layers:
- Human problem (census, navigation, artillery)
- Physical encoding (holes in cards, gear positions)
- Mechanical/electrical reading (pins, mercury cups, counters)
- Tallied output (numbers on counters)

Name each of these layers using one word each. Then predict: what layer will we add in Level 1 (Physical Computing)?

**E3 — What Computing Still Can't Do (Yet)**

By 1890, Hollerith's machine could tally and sort. Name **two things** it could NOT do that a modern computer can, and explain why each limitation existed given the technology of the time.

**E4 — The Bit's Ancestor**

Modern computers store data as bits (0s and 1s). In your own words, trace the lineage: what physical thing was a "1" in a Hollerith card? What physical thing is a "1" in a modern DRAM chip? What stayed the same across 130 years?

---

## Rubric

| Part | Points | What we're looking for |
|------|--------|------------------------|
| A — 5 cards encoded, binary age fields | 20 | Correct positional encoding, binary correct |
| B — 4 tally questions | 15 | Correct counts from simulation |
| C1–C2 — Sort bins | 10 | Correct card groupings |
| C3 — Sort time calculation | 10 | Correct math: 62,979,766 ÷ (65×100) |
| D — Mystery deck analysis | 15 | Correct tallies + reasoned community guess |
| E1–E4 — Capstone essays | 30 | Precise, historical accuracy, correct terminology |

**Total: 100 points**

---

## Hints

<details>
<summary>Hint — Part C3 calculation</summary>
Cards per minute (total) = 65 × 100 = 6,500 cards/min.
Total minutes = 62,979,766 ÷ 6,500. Then divide by 60 for hours.
</details>

<details>
<summary>Hint — Part E2 layer names</summary>
Think: Problem → Representation → Mechanism → Result.
The Level 1 addition: electricity replacing mechanical motion.
</details>

<details>
<summary>Hint — Part E3</summary>
Think about: can Hollerith's machine make decisions based on results? Can it do arithmetic beyond counting? Can it store a program?
</details>

---

## Solutions

<details>
<summary>Part C3 Solution</summary>

Cards per minute (all 100 sorters): 65 × 100 = 6,500 cards/min  
Total minutes: 62,979,766 ÷ 6,500 ≈ **9,689 minutes**  
Total hours: 9,689 ÷ 60 ≈ **161.5 hours ≈ 6.7 days**

For a single sort pass on the entire census, 100 machines working non-stop would take about a week. With multiple passes needed for complex cross-tabulations, the 6-week figure for full tabulation makes perfect sense.
</details>

<details>
<summary>Part E — Sample Answers</summary>

**E1:** Both the Jacquard loom and the Hollerith tabulator use holes in stiff cards as binary signals. In the loom, a hole means "lift this thread" — it is an *instruction* that controls machine behavior. In Hollerith's system, a hole means "this attribute is true for this person" — it is *data* that describes reality. What stays the same: hole = 1, no hole = 0; sequential card reading; position determines meaning. What changes: the machine's response shifts from mechanical actuation (thread lifting) to electrical switching (counter incrementing), and the *purpose* shifts from procedure control to data recording.

**E2:** Problem → Representation → Mechanism → Result. Level 1 adds: *Signal* — the electrical signal that replaces mechanical linkage between representation and mechanism. Instead of a pin physically touching mercury, a transistor switching on a voltage.

**E3:** (1) Hollerith's machine could not *branch* — it could not take a different action based on a computed result. Every card was processed identically; there was no conditional logic. This required a *stored program* and a conditional mechanism (Babbage's "conditional lever"), which didn't exist in Hollerith's electromechanical design. (2) It could not do arithmetic beyond counting and simple accumulation. Multiplication, division, and function evaluation required separate human steps. The Mill (processor) of Babbage's Analytical Engine was missing — Hollerith's machine was a tabulator, not a calculator.

**E4:** In a Hollerith card, a "1" was a physical hole — an absence of material that allowed a metal pin to pass through and contact liquid mercury, completing a circuit. In a modern DRAM chip, a "1" is a charged capacitor — a tiny reservoir of electrons holding a voltage above a threshold. What stays the same: the *binary logic* (present/absent, charged/uncharged, high/low). What changes: the physical medium (paper → silicon), the reading mechanism (pin + mercury → voltage sense amplifier), and the size (a card hole is ~1mm; a DRAM cell is ~10nm — 100,000 times smaller).
</details>
