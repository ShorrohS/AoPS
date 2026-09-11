# Challenge 8.1 — Physical and Data Link Layers

**Type:** Calculation + trace + reasoning  
**Estimated time:** 40–50 minutes  
**Tools needed:** pen and paper

---

## Part A — Manchester Encoding

1. Encode the bit sequence `10110010` using Manchester encoding (1 = low-to-high transition, 0 = high-to-low transition). Draw the resulting waveform showing voltage levels over time.

2. Decode this Manchester-encoded waveform back to bits: starting HIGH, the transitions are: ↓ ↑ ↓ ↑ ↑ ↓ ↓ ↑ (each pair = one bit). What is the decoded sequence?

3. Manchester encoding uses 2× the bandwidth of NRZ for the same bit rate. Why is this trade-off considered worthwhile for early Ethernet?

4. Compare Manchester encoding vs 4B/5B + NRZ-I: 4B/5B maps every 4 bits to a 5-bit code (20% overhead vs 100% for Manchester). Why did Fast Ethernet (100Base-TX) switch to 4B/5B?

---

## Part B — Ethernet Frame

5. Calculate the time to transmit one **maximum-size Ethernet frame** (1518 bytes including header, no FCS) on:
   - 10 Mbps (10Base-T)
   - 100 Mbps (Fast Ethernet)
   - 1 Gbps
   - 10 Gbps

   Show all calculations. Express in microseconds.

6. An Ethernet frame has this structure: `[Preamble 7B][SFD 1B][Dst MAC 6B][Src MAC 6B][EtherType 2B][Payload 46–1500B][FCS 4B]`. What is the minimum frame size? Why does the minimum exist (hint: CSMA/CD collision detection)?

7. The source MAC is `AA:BB:CC:DD:EE:FF`. Write this in binary for the first byte only (`AA`). Is the LSB or MSB transmitted first on the wire?

---

## Part C — Switch MAC Table

A switch with 4 ports starts with an empty MAC address table. Trace the following events:

```
t=1: Frame from MAC=A arrives on port 1, destined for MAC=C
t=2: Frame from MAC=B arrives on port 2, destined for MAC=A
t=3: Frame from MAC=C arrives on port 3, destined for MAC=A
t=4: Frame from MAC=A arrives on port 1, destined for MAC=D (unknown)
```

8. After each event, show: (a) the MAC table state, (b) what the switch does with the frame (flood/forward/filter).

9. At t=4, MAC=D is unknown. The switch **floods** the frame to all ports except the source. Which ports receive the flood?

10. Why does a switch **not** forward a frame back out the port it arrived on, even during flooding?

---

## Part D — CRC Error Detection

11. The CRC-32 polynomial detects all burst errors of length ≤ 32 bits. A frame is 1500 bytes (12,000 bits). If a single random bit flips, what is the probability that CRC-32 fails to detect it? What about a 2-bit error?

12. CRC is an error **detection** code, not an error **correction** code. Why doesn't Ethernet try to correct errors (retransmit instead)? What layer handles retransmission?

13. A received frame has a bad FCS (checksum doesn't match). What does the switch do with it? What does the receiving NIC do with it?

---

## Part E — CSMA/CD Analysis

14. On a 10Base5 (10 Mbps, 500m cable) network, the propagation delay is 5µs for the full segment. The minimum frame size (64 bytes) takes 51.2µs to transmit. Why must the minimum frame be at least 51.2µs? Show the calculation relating minimum frame time to 2× propagation delay.

15. Two stations 500m apart both start transmitting at t=0. At what time does each detect the collision? What is the **slot time** (minimum time to detect any collision)?

16. After a collision, stations use **exponential backoff**: after the k-th collision, wait a random number of slot times in [0, 2^min(k,10) − 1]. After 3 collisions, what is the range of possible backoff values?

---

## Rubric

| Part | Points |
|---|---|
| A encoding | 20 |
| B Ethernet frame | 22 |
| C switch MAC table | 20 |
| D CRC | 18 |
| E CSMA/CD | 20 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part B.5 — frame transmission times</summary>

1518 bytes = 12,144 bits.
- 10 Mbps: 12,144 / 10,000,000 = **1,214.4 µs**
- 100 Mbps: 12,144 / 100,000,000 = **121.44 µs**
- 1 Gbps: 12,144 / 1,000,000,000 = **12.144 µs**
- 10 Gbps: 12,144 / 10,000,000,000 = **1.2144 µs**
</details>

<details>
<summary>Part C.8 — switch trace</summary>

t=1: Learn A→port1. Flood to ports 2,3,4 (C unknown). Table: {A:1}
t=2: Learn B→port2. Forward to port1 (A known). Table: {A:1, B:2}
t=3: Learn C→port3. Forward to port1 (A known). Table: {A:1, B:2, C:3}
t=4: A already on port1 (no relearn needed). D unknown → flood to ports 2,3,4.
</details>

<details>
<summary>Part E.14 — minimum frame calculation</summary>

For collision detection to work: the transmitting station must still be sending when the collision signal returns. Round-trip time = 2 × propagation delay = 2 × 5µs = 10µs. At 10 Mbps, 10µs = 100 bits. But the standard uses 512 bits (64 bytes) to provide margin. Transmission time for 64 bytes at 10 Mbps = 64 × 8 / 10,000,000 = 51.2µs >> 10µs. The 64-byte minimum provides ample time to detect any collision on the segment.
</details>
