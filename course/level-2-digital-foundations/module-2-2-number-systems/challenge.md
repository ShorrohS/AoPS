# Challenge 2.2 — Number Systems

**Type:** Conversion + arithmetic + analysis  
**Estimated time:** 35–45 minutes  
**Tools needed:** `simulation.html` + pen and paper

---

## Part A — Base Conversions

Show all working. Do not use a calculator — these must be done by hand, then verified in the simulator.

### Decimal → Binary
1. Convert 173 to binary
2. Convert 255 to binary
3. Convert 1024 to binary (shortcut exists!)

### Binary → Decimal
4. Convert `0b10110101` to decimal
5. Convert `0b11111111` to decimal
6. Convert `0b1000000000000000` to decimal (count the zeros carefully)

### Binary → Hex (group in fours)
7. Convert `0b10101111` to hex
8. Convert `0b1100101001011110` to hex

### Hex → Binary (expand each digit to 4 bits)
9. Convert `0xDEAD` to binary
10. Convert `0xFF` to binary and then to decimal

### Decimal → Hex (via binary is fine)
11. Convert 255 to hex
12. Convert 4096 to hex

---

## Part B — Two's Complement

Work in **8 bits** throughout this part.

1. Write +47 in 8-bit binary.
2. Find the two's complement (negative) of 47. Show the invert-and-add-1 steps.
3. Verify: add your +47 and −47 representations. Do they sum to 00000000?
4. What is the 8-bit two's complement representation of −1? (Work it out: invert 00000001, add 1.)
5. What is the range of values representable in 8-bit two's complement?

### Overflow detection
6. Add `0b01100000` + `0b01100000` in 8-bit two's complement. What is the mathematical result? What does the 8-bit machine actually produce? Is this correct?
7. Add `0b10000001` + `0b11111111` in 8-bit. What is the result? Is there overflow?

---

## Part C — Hexadecimal in Practice

1. A web colour is `#3A7FCC`. What are the decimal values of the R, G, B components?
2. An x86 instruction is encoded as `0x48 0x89 0xE5`. Convert each byte to binary.
3. A memory address is `0xBEEF`. What decimal address is this?
4. You see a value `0xDEADBEEF` in a debugger. Convert it to decimal. (Use the simulator for this one.)

---

## Part D — Binary Arithmetic

Perform these in binary. Show all carries. Then verify in decimal.

1. `0b01001101 + 0b00110101`
2. `0b11010101 - 0b01001100` (use two's complement: negate second operand, then add)
3. `0b1111 + 0b0001` (4-bit: what happens? Why?)

---

## Rubric

| Part | Points |
|------|--------|
| A conversions (12 problems) | 36 |
| B two's complement | 28 |
| C hex in practice | 16 |
| D binary arithmetic | 20 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A</summary>

1. 173 = 128+32+8+4+1 = `10101101`
2. 255 = `11111111` (all 8 bits set)
3. 1024 = 2¹⁰ = `10000000000` (1 followed by 10 zeros)
4. `10110101` = 128+32+16+4+1 = **181**
5. `11111111` = 255
6. `1000000000000000` = 2¹⁵ = **32,768**
7. `1010 1111` → A F → **0xAF**
8. `1100 1010 0101 1110` → C A 5 E → **0xCA5E**
9. D=1101, E=1110, A=1010, D=1101 → **1101111010101101**
10. `0xFF` = `11111111` = **255**
11. 255 = `FF` hex = **0xFF**
12. 4096 = 2¹² = `0x1000`
</details>

<details>
<summary>Part B</summary>

1. 47 = 32+8+4+2+1 = `00101111`
2. Invert: `11010000`, Add 1: `11010001` = −47
3. `00101111` + `11010001` = `100000000` (9 bits) → keep 8 bits = `00000000` ✓
4. −1: invert `00000001` → `11111110`, add 1 → `11111111`
5. 8-bit two's complement: **−128 to +127**
6. `01100000` + `01100000` = `11000000`. Mathematical result = 96+96=192. In signed: `11000000` = −64. **OVERFLOW** (two positives summed to a negative — the sign bit flipped incorrectly).
7. `10000001` (= −127) + `11111111` (= −1) = `10000000` (= −128). Correct, no overflow.
</details>

<details>
<summary>Part C</summary>

1. `#3A7FCC`: R=0x3A=58, G=0x7F=127, B=0xCC=204
2. `0x48`=`01001000`, `0x89`=`10001001`, `0xE5`=`11100101`
3. `0xBEEF` = 11×4096 + 14×256 + 14×16 + 15 = 45056+3584+224+15 = **48,879**
4. `0xDEADBEEF` = 3,735,928,559
</details>
