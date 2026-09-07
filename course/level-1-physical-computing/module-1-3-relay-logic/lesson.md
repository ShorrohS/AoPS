# Module 1.3 — Relay Logic: Building Decisions from Metal

---

## The Problem

> We can light a bulb with a relay. We can even make a relay remember a state. But can we make a relay *compute*?
>
> In 1937, a 21-year-old MIT graduate student named Claude Shannon submitted a master's thesis that answered this question definitively — and in doing so, connected 83 years of Boole's abstract algebra to physical circuits for the first time.
>
> The thesis was titled: *"A Symbolic Analysis of Relay and Switching Circuits."*
>
> Its central claim: **any Boolean logical expression can be implemented directly as a relay circuit.**
>
> Every logic gate in every computer ever built traces its intellectual ancestry to that thesis.

---

## The Story

### Claude Shannon's Thesis — 1937

George Boole had published *An Investigation of the Laws of Thought* in 1854. It described a complete algebra of TRUE/FALSE values with operations AND, OR, NOT. Mathematically elegant, but abstract — nobody had found a physical application for it.

Shannon was repairing a telephone switching network when he noticed that relay circuits — already in widespread use for telephone exchanges — behaved exactly like Boolean expressions:
- A closed contact = TRUE (1)
- An open contact = FALSE (0)
- Contacts in series = AND
- Contacts in parallel = OR
- A normally-closed contact = NOT

He proved that you could take any Boolean expression, however complex, and translate it directly into a relay circuit. And conversely, you could take any relay circuit and describe it as a Boolean expression.

This equivalence meant: **if you can express a computation as logic, you can build it from relays.**

His thesis examiner called it "possibly the most important master's thesis of the 20th century." He was 21.

---

### Boolean Algebra: The Rules

Boolean algebra operates on values that are either 0 (FALSE) or 1 (TRUE). The rules:

**AND (multiplication):**
```
0 AND 0 = 0
0 AND 1 = 0
1 AND 0 = 0
1 AND 1 = 1
```
AND is true only when ALL inputs are true.

**OR (addition):**
```
0 OR 0 = 0
0 OR 1 = 1
1 OR 0 = 1
1 OR 1 = 1
```
OR is true when ANY input is true.

**NOT (complement):**
```
NOT 0 = 1
NOT 1 = 0
```
NOT inverts the value.

**Key identities (you'll use these constantly):**
```
A AND 0 = 0          (anything ANDed with false is false)
A AND 1 = A          (anything ANDed with true is itself)
A OR 0 = A           (anything ORed with false is itself)
A OR 1 = 1           (anything ORed with true is true)
A AND A = A          (idempotent)
A AND (NOT A) = 0    (contradiction)
A OR (NOT A) = 1     (tautology)
NOT (NOT A) = A      (double negation)
```

**De Morgan's Laws** (extremely important):
```
NOT (A AND B) = (NOT A) OR (NOT B)
NOT (A OR B)  = (NOT A) AND (NOT B)
```
De Morgan's Laws let you convert between AND-circuits and OR-circuits with inversions. This is how NAND-only and NOR-only chip designs work.

---

### Building a Half Adder

The half adder is the simplest arithmetic circuit. It adds two 1-bit numbers and produces a 2-bit result: a **Sum** bit and a **Carry** bit.

Truth table:
```
A  B  | Sum  Carry
0  0  |  0     0
0  1  |  1     0
1  0  |  1     0
1  1  |  0     1
```

Look carefully:
- **Carry = A AND B** — you only get a carry when both inputs are 1
- **Sum = A XOR B** — the sum is 1 when exactly one input is 1 (not both, not neither)

XOR (exclusive OR) is the key operation. How do you build XOR from AND, OR, NOT?

```
A XOR B = (A OR B) AND NOT(A AND B)
        = (A OR B) AND (NOT A OR NOT B)  ← De Morgan applied
```

In relay terms:
1. One relay per input (A, B)
2. OR path: contacts in parallel → fire if either A or B is high
3. NOT-AND path: normally-closed contacts in series → open only when BOTH are high (NAND)
4. AND the OR-result with the NAND-result → XOR

This is four relays. In 1940s relay computers, every XOR took four physical relay devices. A 16-bit adder needed hundreds of relays just for the sum logic. ENIAC's equivalent in vacuum tubes was already faster by orders of magnitude.

---

### Shannon's Minimization

Shannon also showed how to **minimize** logic circuits — reduce the number of gates needed to implement a function. This is the origin of **Karnaugh maps** and **Boolean minimization** algorithms used in every chip design tool today.

The principle: two relay networks that always produce the same output for every input are equivalent, even if they look different. The simpler one is preferable. Finding the simplest equivalent circuit is an optimization problem Shannon formalized.

Example: `(A AND B) OR (A AND C)` can be simplified to `A AND (B OR C)` — one fewer AND operation, saving one relay.

This kind of algebraic simplification is what synthesis tools (like those that compile Verilog/VHDL to chip layouts) do billions of times per chip design.

---

### The Zuse Z3 — First Programmable Computer (1941)

Konrad Zuse, working in his parents' living room in Berlin, built the **Z3** in 1941 — the world's first fully operational programmable computer. It used **2,600 telephone relays** and could execute programs stored on perforated film.

Key specs:
- Clock speed: ~5.3 Hz (5.3 relay switching cycles per second)
- Word length: 22-bit floating point
- Memory: 64 words
- Operations: Add, subtract, multiply, divide, square root
- Program input: punched 35mm film strip

The Z3 could multiply two 22-bit floating-point numbers in about 3 seconds. Impressive for relays — but the machine had fundamental speed limits. Each instruction required multiple relay switching cycles, each cycle took ~190ms.

The Z3 was destroyed in a 1943 Allied bombing raid. A working replica exists in the Deutsches Museum, Munich.

---

### The Mark I — Electromechanical Computing at Scale

Harvard's IBM Automatic Sequence Controlled Calculator (**Mark I**), completed in 1944, was the first large-scale electromechanical computer in the US. It had:
- 765,000 components
- ~3,000 electromechanical relays
- 800 km of wire
- 15 metres long, 2.4 metres tall
- Weight: 4,500 kg

It could do one multiplication per 6 seconds. Grace Hopper programmed it and wrote its operating manual. The "first computer bug" — an actual moth — was found in a relay here on September 9, 1945.

The Mark I made clear both what relay computers could do and why they couldn't go much further. The US Navy used it for ballistic calculations throughout WW2, but it was already being overtaken by ENIAC before it was finished.

---

## The Concept: Logic is Physical

Shannon's insight bridges the entire philosophical gap between Boole's abstract mathematics and Babbage's mechanical vision:

```
Boolean algebra (Boole, 1854)
    ↓ 83 years
Shannon's thesis (1937): Boolean algebra = relay circuit topology
    ↓
Every logic gate, every CPU, every chip:
    a physical implementation of Boolean algebra
```

When a modern CPU executes `if (x > 0 && y < 10)`, it is evaluating a Boolean expression using billions of transistors arranged in exactly the same logical pattern Shannon described with relays in 1937. The medium changed. The logic did not.

**The three primitives that suffice for all computation:**
| Gate | Boolean | Relay implementation |
|------|---------|---------------------|
| AND  | A · B   | Series contacts |
| OR   | A + B   | Parallel contacts |
| NOT  | Ā       | Normally-closed contact |

These three, combined, can implement any computable function. This is a proved mathematical fact (functional completeness of {AND, OR, NOT}).

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

The simulation is a **relay logic circuit builder** with three tools:

**Tool 1 — Gate Builder**
- Drag relay symbols onto the canvas
- Connect them in series (AND) or parallel (OR)
- Toggle a relay type between normally-open (NO) and normally-closed (NC)
- Test the circuit with input toggles

**Tool 2 — Half Adder**
- Pre-built half adder circuit (Sum + Carry)
- Toggle inputs A and B
- Watch the XOR (Sum) and AND (Carry) outputs respond
- See the Boolean expressions update live

**Tool 3 — Boolean Expression Evaluator**
- Type a Boolean expression (e.g., `(A AND B) OR (NOT C)`)
- The simulator builds the corresponding relay circuit automatically
- Test all combinations and verify the truth table

**What to try:**
1. Build XOR manually in the Gate Builder — can you do it in 4 relays?
2. In the Half Adder, confirm all 4 rows of the truth table
3. Enter `NOT (A AND B)` in the expression evaluator — is it the same as `(NOT A) OR (NOT B)`? (De Morgan's Law)

---

## Going Deeper

The telephone exchange was the original motivation for relay logic. A telephone switching system must connect any caller to any of thousands of possible destinations. Each connection is a relay closure. A switching fabric of N inputs to M outputs required (N × M) relay contacts in the worst case — quickly reaching millions of relays for a city-scale exchange.

Shannon's minimization theory directly reduced the number of relays needed, saving AT&T enormous hardware costs. This is why AT&T's Bell Labs — not a university — funded so much of the foundational computer science research of the 20th century, including the transistor (1947) and Unix (1969).

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Build XOR from primitive gates, minimize a Boolean expression using the identities, and wire a relay circuit that implements a 1-bit comparator (outputs 1 when A equals B).
