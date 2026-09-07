# Module 0.2 — Early Mechanical Computation

---

## The Problem

> You are a 17th-century merchant calculating compound interest on a loan. The calculation requires multiplying large numbers together — numbers with 6, 8, even 10 digits. There are no calculators. There are no computers. There is only you, a quill, and arithmetic rules you learned as a child.
>
> A single multiplication can take **30 minutes**. A mistake means starting over. You need to do dozens of these calculations a day.
>
> What if a machine could do it for you?

Arithmetic at scale was exhausting, slow, and error-prone. Long before electronics, inventors tried to solve this with **gears, levers, and rotating cylinders** — encoding numbers in physical positions and letting mechanical motion do the work.

---

## The Story

### The Abacus — The First Computational Tool (~2400 BC)

The abacus wasn't a calculator — it was a **memory aid**. By moving beads into positions, an operator could hold intermediate results without relying on mental memory alone. The abacus offloaded working memory to a physical object.

Key insight: **externalizing state**. Instead of keeping numbers in your head, you encode them in something physical you can see and manipulate. This idea — state stored in a physical medium — is the seed of all computing.

A skilled abacus user can beat a calculator on simple additions. But an abacus can't carry its own operations. A human must still perform each step.

---

### Napier's Bones — 1617

John Napier, a Scottish mathematician, invented a set of **multiplication rods** in 1617. Each rod was engraved with a multiplication table for a single digit. Laid side by side, they turned multi-digit multiplication into a series of additions that even a non-mathematician could perform.

**How they work:**
1. Pick the rods corresponding to each digit of your multiplicand
2. Lay them side by side
3. Read off the row corresponding to your multiplier
4. Add the diagonal entries to get the product

For `357 × 8`:
- Place rods for 3, 5, 7
- Read row 8: `2/4 | 4/0 | 5/6`
- Add diagonals: `2 | (4+4) | (0+5) | 6` = `2 | 8 | 5 | 6` = 2856

The machine didn't compute — it **encoded multiplication tables** so a human could assemble the answer from simpler lookups. This is a precursor to lookup tables in software.

---

### Schickard's Calculating Clock — 1623

Wilhelm Schickard built the first known mechanical calculator in 1623 — it was called the "calculating clock." It used a set of Napier-like rods for multiplication and a separate set of wheels for addition and subtraction, with an automatic carry mechanism.

The **carry mechanism** was the key innovation: when a digit wheel rolled from 9 to 0, it automatically advanced the next wheel by 1. This is the same principle as the carry in binary addition — the single most important operation in arithmetic.

Schickard's machine was destroyed in a fire and largely forgotten. But the idea survived.

---

### Pascal's Pascaline — 1642

Blaise Pascal, at age 18, built the **Pascaline** to help his father — a tax collector — with tedious addition and subtraction. It was the first mass-produced mechanical calculator (around 50 were built).

**How it works:**
- A series of interlocked gear wheels, each representing one decimal digit (0–9)
- To add 1, you turn the rightmost wheel one notch
- When a wheel completes a full rotation (9 → 0), it advances the next wheel by one notch — the **carry**
- Subtraction was done by a complementary method (adding the 9's complement)

The Pascaline could only add and subtract. It could not multiply or divide directly. Its greatest contribution was the **mechanical carry** — proving that the most difficult part of arithmetic (propagating carries) could be done by gears without human intervention.

**Why it matters:** Pascal proved that **arithmetic rules could be embedded in physical mechanisms**. The law of adding carries isn't just a mental rule — it can be a gear meshing with another gear.

---

### Leibniz's Stepped Reckoner — 1694

Gottfried Wilhelm Leibniz improved on Pascal by adding a **stepped drum** (Leibniz wheel) — a cylinder with 9 teeth of varying length. By sliding the drum, you could engage 1 to 9 teeth, effectively multiplying by any single digit.

This allowed the Stepped Reckoner to **multiply and divide** via repeated addition/subtraction with a crank-operated register — the first calculator to support all four arithmetic operations.

Leibniz was also the inventor of binary arithmetic. He wrote in 1679 about a system using only 0s and 1s, inspired by the Chinese I Ching. He never connected binary to circuits — that took another 258 years — but the mathematics was there.

---

### The Pattern Across All These Machines

| Machine | Year | Operation | Key Innovation |
|---------|------|-----------|---------------|
| Abacus | ~2400 BC | Add/Subtract | External state storage |
| Napier's Bones | 1617 | Multiply | Encoded lookup tables |
| Schickard's Clock | 1623 | Add/Multiply | Mechanical carry |
| Pascaline | 1642 | Add/Subtract | Reliable mechanical carry |
| Stepped Reckoner | 1694 | All four ops | Variable-engagement gear |

Each machine solved a real bottleneck. Each one embedded a rule of arithmetic into a physical mechanism, offloading cognitive work onto metal and motion.

---

## The Concept: Encoding Information in Physical State

Every one of these machines shares a single deep idea: **numbers are encoded as physical positions**.

- A bead's position on a wire = a digit's value
- A gear wheel's rotational position = a digit (0–9)
- A rod's alignment = a multiplication table entry

This is the essence of computing: **representing information as physical state** and **manipulating that state according to rules**.

The shift from mechanical gears to electrical circuits is a shift in *medium*, not in *concept*. A transistor's on/off state is just a gear wheel's position, but a billion times faster and a billion times smaller.

### What "Carrying" Really Means

The mechanical carry — when one wheel overflows and advances the next — is the physical embodiment of the arithmetic rule: "when a column exceeds its base, subtract the base and add 1 to the next column."

You will see this same idea in:
- Binary addition (Module 2.2)
- The ALU carry flag (Module 2.6)
- Computer overflow errors (Module 3.3)

The gear that clicks forward when a wheel hits 9 is the ancestor of every carry bit in every processor ever made.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

The simulation has three interactive tools:

**Tool 1 — Napier's Bones**
- Select rods by clicking digit buttons
- Enter a multiplier (1–9)
- Watch the diagonal addition animate step by step
- Verify the result

**Tool 2 — Virtual Pascaline**
- Click the input wheels to dial in a number
- Hit "Add" to add it to the accumulator
- Watch the carry propagate visually through the gear chain
- Try to cause a multi-digit carry (add 999 + 1)

**What to observe:**
- How does the carry mechanism "know" to advance the next wheel?
- What happens when you overflow the accumulator (exceed 9999)?

---

## Going Deeper

The Pascaline's carry mechanism had a fatal flaw: it used a **sequential carry**, meaning carries propagated one wheel at a time. Adding 999 + 1 caused a chain reaction through all wheels — it took longer than adding 001 + 1.

This "carry chain" problem plagued mechanical calculators and later early electronic computers. The solution — **carry lookahead** — was one of the great innovations of the 1950s and is still used in every modern CPU. You'll build it in Module 2.4.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Use the Napier's Bones simulation to multiply `347 × 6` and `829 × 7`. Then explain in writing how the Pascaline's carry mechanism handles the addition `798 + 203`. Trace every wheel that moves.
