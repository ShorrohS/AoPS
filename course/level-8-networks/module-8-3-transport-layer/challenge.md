# Challenge 8.3 — Transport Layer: TCP and UDP

**Type:** Calculation + trace + implementation  
**Estimated time:** 45–55 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — TCP Sequence Numbers

A TCP connection transfers a 2,000-byte file. The initial sequence number (ISN) is 100. Each TCP segment carries 500 bytes of data.

1. Fill in the sequence and acknowledgement numbers for all segments and ACKs:

| # | Direction | Seq | Ack | Bytes | Notes |
|---|---|---|---|---|---|
| 1 | C→S | SYN, x=100 | — | 0 | Handshake |
| 2 | S→C | SYN-ACK, y=500 | ? | 0 | |
| 3 | C→S | ACK | ? | 0 | |
| 4 | C→S | Data | ? | 500 | Segment 1 |
| 5 | S→C | ACK | ? | 0 | |
| 6 | C→S | Data | ? | 500 | Segment 2 |
| 7 | C→S | Data | ? | 500 | Segment 3 |
| 8 | C→S | Data | ? | 500 | Segment 4 |
| 9 | S→C | ACK | ? | 0 | Cumulative ACK for 6,7,8 |

2. Segment 3 (row 7) is lost in transit. The server receives segments 1, 2, and 4 out of order. What ACKs does the server send? What does the client do after receiving 3 duplicate ACKs?

3. What is the maximum TCP throughput (in bytes/second) for a connection with:
   - Window size = 65,535 bytes
   - Round-trip time = 100ms
   Show the calculation: throughput = window / RTT.

---

## Part B — Congestion Control

Starting with `cwnd = 1 MSS` (MSS = 1460 bytes) and `ssthresh = 16 MSS`:

4. Trace the TCP slow start phase: how many MSS can be sent after each ACK round? Fill in:

| Round | cwnd (MSS) | Can send |
|---|---|---|
| 1 | 1 | 1 MSS |
| 2 | 2 | 2 MSS |
| 3 | ? | ? |
| 4 | ? | ? |
| 5 | ? | ? |

Stop when `cwnd = ssthresh`. What phase begins at that point?

5. A packet loss event occurs when `cwnd = 20 MSS`. Under **TCP Reno**:
   - What is the new `ssthresh`?
   - What is the new `cwnd`?
   - Does the connection enter slow start or congestion avoidance?

6. Under **TCP BBR**, is packet loss used as the primary congestion signal? What does BBR use instead?

---

## Part C — UDP Echo Implementation

7. Implement a UDP echo server that:
   - Listens on port 9001
   - Echoes every received datagram back to the sender
   - Prints the sender address and data for each datagram

8. Implement a UDP echo client that:
   - Sends 5 messages ("message 1" through "message 5")
   - Waits 0.5 seconds for each reply
   - Reports if a reply times out
   - Reports round-trip time for each successful reply

9. On a local loopback, UDP datagrams are never lost. Artificially introduce packet loss in the client: randomly drop 30% of received replies. Observe and report how many messages are "lost."

---

## Part D — TCP vs UDP Decision

For each application, choose TCP or UDP and justify:

10. A multiplayer game sending player position updates 60 times per second. The game can tolerate missed frames but not latency.

11. A file synchronisation client uploading changed files to a cloud server.

12. A live video stream where viewers can tolerate occasional artefacts but not freezing.

13. A financial transaction system where every order must be confirmed.

14. A DNS resolver sending queries to a recursive server.

---

## Part E — Window and Throughput

15. A TCP connection over a satellite link has RTT = 600ms and packet loss rate = 0.1%. Using the Mathis formula: `throughput ≈ MSS / (RTT × √(loss))`, calculate the maximum achievable throughput with MSS = 1460 bytes.

16. Compare: for the same link, what window size would a single TCP connection need to fully utilise a 100 Mbps link? (throughput = window / RTT)

---

## Rubric

| Part | Points |
|---|---|
| A sequence numbers | 26 |
| B congestion control | 22 |
| C UDP implementation | 22 |
| D TCP vs UDP | 16 |
| E window/throughput | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1 — sequence numbers</summary>

| # | Seq | Ack | Notes |
|---|---|---|---|
| 1 | 100 | — | SYN |
| 2 | 500 | 101 | SYN-ACK (ack = ISN+1 = 101) |
| 3 | 101 | 501 | ACK |
| 4 | 101 | 501 | Data bytes 101–600 |
| 5 | 501 | 601 | ACK (expects byte 601) |
| 6 | 601 | 501 | Data bytes 601–1100 |
| 7 | 1101 | 501 | Data bytes 1101–1600 (lost → 501?) wait |
| 8 | 1601 | 501 | Data bytes 1601–2100 |
| 9 | 501 | 1101 | Cumulative ACK: got 601–1100, expects 1101 |

(Adjusted: after segments 6,7,8 arrive with segment 7 lost: server acks up to what it received in order.)
</details>

<details>
<summary>Part B.4 — slow start</summary>

| Round | cwnd | Can send |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 4 | 4 |
| 4 | 8 | 8 |
| 5 | 16 | 16 = ssthresh → congestion avoidance begins |
</details>

<details>
<summary>Part C.7+8 — UDP server/client</summary>

```python
# Server
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 9001))
while True:
    data, addr = s.recvfrom(1024)
    print(f"From {addr}: {data.decode()}")
    s.sendto(data, addr)

# Client with timeout
import socket, time
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.settimeout(0.5)
for i in range(1, 6):
    msg = f"message {i}".encode()
    t0 = time.perf_counter()
    c.sendto(msg, ('127.0.0.1', 9001))
    try:
        data, _ = c.recvfrom(1024)
        rtt = (time.perf_counter() - t0) * 1000
        print(f"Reply {i}: {data.decode()}, RTT={rtt:.2f}ms")
    except socket.timeout:
        print(f"Message {i}: TIMEOUT")
```
</details>

<details>
<summary>Part E.15 — Mathis formula</summary>

throughput ≈ MSS / (RTT × √loss) = 1460 / (0.6 × √0.001) = 1460 / (0.6 × 0.0316) = 1460 / 0.01897 ≈ **76,962 bytes/s ≈ 615 Kbps**.

For 100 Mbps: window = throughput × RTT = 12,500,000 bytes/s × 0.6s = **7,500,000 bytes ≈ 7.5 MB**. A 16-bit window field (max 65,535 bytes) would limit throughput to ~872 Kbps — hence TCP Window Scaling (RFC 7323) which multiplies the window by 2^scale, enabling multi-MB windows.
</details>
