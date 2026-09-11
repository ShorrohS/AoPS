# Module 2.2 — Number Systems: Binary, Octal, Hex, Two's Complement

---

## The Problem

> You've accepted binary. Everything is 0s and 1s. Now you need to check what's stored at memory address 0b0001110101001100.
>
> That's: memory address 7,500. Not hard in decimal. But in binary? Reading 16 bits of binary at a glance takes a trained eye — and you'll need to read thousands of them while debugging.
>
> There is also the problem of negative numbers. Binary naturally represents only non-negative integers. How do you represent −1 in bits?

Both problems have elegant solutions that every computer scientist uses daily: hexadecimal as shorthand for binary, and two's complement for signed integers. Understanding these isn't optional — they appear in every debugger, every disassembler, every network packet, every colour code on a webpage.

---

## The Story

### Positional Notation

Every number system we use is **positional** — the value of a digit depends on its position.

In decimal (base 10):
```
3 4 7
│ │ └── 7 × 10⁰ = 7 × 1   =    7
│ └──── 4 × 10¹ = 4 × 10  =   40
└────── 3 × 10² = 3 × 100 =  300
                            ─────
                              347
```

The *base* tells you how many symbols exist (10: 0–9) and what each position is worth (powers of 10).

The same principle works for any base:

**Binary (base 2):** symbols are 0,1. Positions are powers of 2.
```
1 0 1 1 0 1
│ │ │ │ │ └── 1 × 2⁰ = 1
│ │ │ │ └──── 0 × 2¹ = 0
│ │ │ └────── 1 × 2² = 4
│ │ └──────── 1 × 2³ = 8
│ └────────── 0 × 2⁴ = 0
└──────────── 1 × 2⁵ = 32
                       ──
                       45
```
So `0b101101` = 45 in decimal.

---

### Binary ↔ Decimal Conversions

**Decimal to binary** — repeated division by 2, read remainders bottom to top:
```
45 ÷ 2 = 22 remainder 1   ← LSB (least significant bit)
22 ÷ 2 = 11 remainder 0
11 ÷ 2 =  5 remainder 1
 5 ÷ 2 =  2 remainder 1
 2 ÷ 2 =  1 remainder 0
 1 ÷ 2 =  0 remainder 1   ← MSB (most significant bit)

Reading bottom to top: 101101
```

**Binary to decimal** — sum the positional values of each 1 bit (as shown above).

**Shortcut for powers of 2:**
```
2⁰=1, 2¹=2, 2²=4, 2³=8, 2⁴=16, 2⁵=32, 2⁶=64, 2⁷=128
2⁸=256, 2⁹=512, 2¹⁰=1024, 2¹⁶=65536, 2³²≈4 billion
```
Memorise up to 2¹⁰. The rest follow by doubling.

---

### Hexadecimal — Binary's Shorthand

**Hexadecimal (base 16):** symbols are 0–9 then A–F (where A=10, B=11, C=12, D=13, E=14, F=15).

The key insight: 16 = 2⁴. So **one hex digit encodes exactly 4 binary bits**. This makes conversion trivial:

```
Binary:  1010  1111  0011  1100
Hex:       A     F     3     C
= 0xAF3C
```

To convert any binary number to hex: group bits in fours from the right, convert each group.
To convert hex to binary: expand each digit to 4 bits.

**Why hex is everywhere:**
- Memory addresses: `0x7FFF0000` is much more readable than `0111 1111 1111 1111 0000 0000 0000 0000`
- Colour codes: `#FF5733` = RGB(255, 87, 51) — three bytes in six hex digits
- Machine code: `0x48 0x89 0xE5` is the first instruction of almost every x86-64 function
- Ethernet addresses: `A4:C3:F0:85:AC:2D`
- IPv6: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`

---

### Octal — The Forgotten Sibling

Octal (base 8) groups binary in threes. It was used in old minicomputers and Unix file permissions.

```
Binary: 111 101 100
Octal:    7   5   4
= 0754 (a Unix file permission: rwxr-xr--)
```

Octal has largely been replaced by hex in modern systems, but you'll still encounter it in Unix `chmod` commands.

---

### Binary Arithmetic: Addition

Binary addition follows the same rules as decimal, with carries:

```
Bit addition table:
0 + 0 = 0          (no carry)
0 + 1 = 1          (no carry)
1 + 0 = 1          (no carry)
1 + 1 = 0 carry 1  (like decimal: 9+1=0 carry 1)
1 + 1 + 1 = 1 carry 1

Example: 0101 + 0011
  0101   (5)
+ 0011   (3)
──────
  1000   (8)   ✓
```

The carry propagation rule is exactly what the Pascaline implemented mechanically in 1642 — and what every adder circuit in every CPU implements today.

---

### Two's Complement: Negative Numbers

How do you represent −1 in binary? Several approaches exist; only one is used in practice.

**Sign-magnitude** (naive approach): use the leftmost bit as a sign (0=positive, 1=negative).
- Problem: two representations of zero (0000 and 1000)
- Problem: addition doesn't work normally — need separate add/subtract circuits

**Two's complement** (the universal standard):

**Rule**: to negate a number, invert all bits and add 1.

```
+5 in 8-bit binary:  00000101
Invert all bits:      11111010
Add 1:                11111011
= −5 in two's complement
```

Verify: 5 + (−5) = 0?
```
  00000101   (+5)
+ 11111011   (−5)
──────────
 100000000   = 9 bits, but we only keep 8 → 00000000 = 0 ✓
```

**Two's complement range** for n bits: −2^(n-1) to +2^(n-1)−1
- 8-bit: −128 to +127
- 16-bit: −32,768 to +32,767
- 32-bit: −2,147,483,648 to +2,147,483,647

**Why two's complement wins:**
- Only one representation of zero
- Addition and subtraction work with the **same circuit** — no special cases
- The most significant bit still acts as a sign indicator (1 = negative)
- Hardware is simpler: one adder handles both add and subtract

---

### Overflow

When a result exceeds the representable range, **overflow** occurs.

```
8-bit signed: max positive = 127 = 0111 1111
127 + 1:
  0111 1111
+ 0000 0001
──────────
  1000 0000  = 128 in unsigned, but = −128 in signed!
```

The CPU sets an **overflow flag** when this happens. If you're writing a program and ignore overflow, you get silent corruption — the classic source of security vulnerabilities. The `signed integer overflow` bug has caused spacecraft failures, financial miscalculations, and legendary security exploits.

---

## The Concept: Every Computer Uses These

Every value in your computer right now — every pixel colour, every instruction address, every floating-point number, every timestamp — is encoded in binary and often displayed in hex. Two's complement is how every signed integer works on every mainstream CPU (x86, ARM, MIPS, RISC-V, all of them).

Understanding these representations is the difference between reading machine output as "noise" vs reading it as structured information.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

Three tools:

**Tool 1 — Interactive Base Converter**
- Type any number in any base (decimal, binary, hex, octal)
- See all four representations simultaneously, updating in real time
- Each bit position labelled with its weight (2⁷, 2⁶, etc.)
- Step-by-step conversion working shown

**Tool 2 — Two's Complement Explorer**
- Enter a positive number → see its two's complement negative
- Watch the invert-and-add-1 animation step by step
- Adjust bit width (4, 8, 16 bits)
- Overflow indicator: shows when you've gone past the range

**Tool 3 — Binary Arithmetic Trainer**
- Addition and subtraction problems in binary
- Work through them manually, then check
- Carry/borrow propagation animated

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Convert between all four number systems, perform binary addition and subtraction using two's complement, and identify overflow conditions.
