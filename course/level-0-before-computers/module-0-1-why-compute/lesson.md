# Module 0.1 — Why Did Humans Need to Compute?

---

## The Problem

> Imagine you are the United States government in 1880. You need to count 50 million people, record their ages, occupations, birthplaces, and family sizes — and you need to do it accurately enough to redraw congressional districts and allocate federal funding.
>
> You have pencils, paper, and humans.
>
> It takes **8 years**.
>
> By the time you finish, the next census is already 2 years away.

This wasn't a failure of effort. It was a failure of **scale**. Human brains are remarkable, but they break down when asked to do the same arithmetic operation millions of times without error.

That breakdown is exactly why computing had to be invented.

---

## The Story

### Problem 1: The Census Crisis

The 1880 US Census employed hundreds of clerks who hand-tallied results on paper. The final count was published in 1888 — 8 years after the census was taken. The US Constitution requires a census every 10 years. The math was terrifying: **the 1890 census was going to be even bigger**, and at the current rate, it might not be finished before the 1900 census began.

Congress was alarmed. A competition was held to find a faster method. A young engineer named Herman Hollerith won it — but that's Module 0.5's story.

The point here is simpler: **large-scale counting broke human capacity**.

---

### Problem 2: Navigation and the Cost of Arithmetic Errors

In the 17th and 18th centuries, a ship's navigator used printed mathematical tables to find their position at sea. These tables — logarithms, trigonometric values, astronomical positions — were computed by hand and typeset by hand.

Hand computation means human error. Typesetting means more human error.

In 1628, the Swedish warship *Vasa* sank on its maiden voyage partly due to a design calculation error. Navigation errors sent ships onto rocks. Artillery fired at incorrect trajectories killed friendly troops.

The British government commissioned **Mathematical Tables** projects employing teams of human "computers" — people whose job title was literally *computer* — to calculate and cross-check these values. Errors still crept in.

**The problem**: arithmetic at the scale required for navigation and engineering was too error-prone for humans alone.

---

### Problem 3: Artillery and Wartime Calculation

During World War 1 and World War 2, artillery crews needed **firing tables** — books of pre-calculated values telling gunners how to aim based on distance, wind speed, shell weight, and air pressure. Each table required thousands of calculations.

At Aberdeen Proving Ground in the US, teams of (human) computers — many of them women, including those who would later program ENIAC — spent days computing a single trajectory by hand. During WW2, the demand for new firing tables outpaced what humans could calculate.

This bottleneck directly funded the construction of ENIAC, the first general-purpose electronic computer, completed in 1945.

**The problem**: the speed of human calculation was a strategic military liability.

---

## The Pattern

Look at these three problems together:

| Problem | Scale | Consequence of slowness |
|---------|-------|------------------------|
| Census counting | 50 million people | Government dysfunction |
| Navigation tables | Millions of arithmetic ops | Ships lost, lives lost |
| Artillery trajectories | Thousands of ballistic calc | Military disadvantage |

In every case, the bottleneck was the same: **humans doing repetitive arithmetic at scale**.

The solution was always the same direction: **offload repetitive computation to a machine**.

---

## The Concept: What is Computation?

Computation, at its core, is the manipulation of symbols according to rules.

- **Symbol**: any representation of information (a number, a letter, a hole in a card)
- **Rule**: a defined operation (add these two numbers, shift this value left)
- **Manipulation**: applying the rule to the symbol to produce a new symbol

That's it. A human doing long division is computing. A gear turning in a calculating machine is computing. A transistor switching in a chip is computing.

The difference between a human computer and an electronic computer is:
- **Speed**: milliseconds vs nanoseconds
- **Reliability**: humans make errors; circuits don't (unless broken)
- **Tirelessness**: humans get tired; machines don't

---

## What "Stored Instructions" Means (Preview)

The next major leap wasn't just making machines faster — it was making them **programmable**. A machine that can only add is limited. A machine that can follow a *sequence of instructions* — and change what it does based on previous results — is general-purpose.

The idea of storing instructions (a program) alongside data is the single most important idea in computing. You'll see it born in Module 0.3 with Jacquard's loom, formalized in Module 0.4 with Babbage, and industrialized in Module 0.5 with Hollerith.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

The simulation puts you in the role of a human "computer" from 1880. You are given a census tally sheet and must manually count and sum demographic data across multiple districts.

**What to do:**
1. Open `simulation.html` in your browser
2. You'll see a table of raw census records — names, ages, occupations
3. Your task: tally the totals for each category by clicking to count
4. Notice how errors accumulate as the dataset grows
5. Toggle to "machine mode" to see the same task done instantly

**What to observe:**
- How long does the human tally take vs the machine?
- Where do errors appear in your manual count?
- What would this feel like at 50 million records?

---

## Going Deeper

The humans employed as "computers" before electronic machines were a real profession. Between 1930 and 1945, the US government's Mathematical Tables Project employed over 450 people as computers. Many were women with mathematics degrees who couldn't get other professional employment due to discrimination — the same women who would later program ENIAC.

For a deep dive: *Hidden Figures* by Margot Lee Shetterly covers the NASA human computers in detail.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

You will calculate the time required to complete the 1880 census manually versus with automation, then estimate how many human-computer-hours were saved by Hollerith's machine.

This is a math problem. Show your working.
