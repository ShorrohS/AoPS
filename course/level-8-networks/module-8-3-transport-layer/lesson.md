# Module 8.3 — Transport Layer: TCP and UDP

---

## The Problem

> IP (Module 8.2) delivers packets between machines.
> But a machine runs hundreds of programs, each communicating simultaneously.
> How does the OS know which packets belong to which program?
> How do we guarantee that data arrives completely and in order?
> How do we prevent a fast sender from overwhelming a slow receiver?
>
> These are the transport layer's problems:
> **multiplexing**, **reliability**, and **flow control**.

---

## The Story

### TCP Was Born from Military Necessity

The ARPANET (1969) used a packet-switched protocol without reliability guarantees. When the US military needed reliable data transfer — routing commands, sensor data, and communications across potentially damaged or intermittent connections — a new protocol was needed.

Vinton Cerf and Robert Kahn published the TCP specification in 1974. The original design had TCP and IP as one protocol. Jon Postel's famous contribution (1978) was separating them — TCP (Transport Control Protocol) handled reliability and ordering; IP handled routing. This separation of concerns enabled the internet to accommodate different transport needs: UDP for simple datagram delivery, TCP for reliable streams.

Cerf and Kahn received the Turing Award in 2004 for this work.

---

## The Concept

### Port Numbers — Multiplexing

A machine has one IP address but hundreds of applications needing network access. **Port numbers** (16-bit, 0–65535) distinguish between applications:

- **Well-known ports** (0–1023): reserved for standard services. HTTP=80, HTTPS=443, SSH=22, DNS=53, FTP=21, SMTP=25.
- **Registered ports** (1024–49151): by application convention. MySQL=3306, PostgreSQL=5432, Redis=6379, MongoDB=27017.
- **Dynamic/ephemeral ports** (49152–65535): assigned by the OS for outbound connections.

A connection is uniquely identified by a **5-tuple**: `(protocol, src_IP, src_port, dst_IP, dst_port)`. Two different browsers can connect to the same server simultaneously because they have different ephemeral source ports.

### UDP — Simple Datagram

UDP adds only port numbers to IP:

```
UDP Header (8 bytes):
[src_port 2B] [dst_port 2B] [length 2B] [checksum 2B]
[payload]
```

**Properties**: connectionless, unreliable (no delivery guarantee), no ordering, no flow control. Fire and forget.

**When to use UDP**:
- **DNS**: a query fits in one packet; if no reply arrives, just retry. TCP overhead is unnecessary.
- **Real-time media** (VoIP, video streaming): a dropped packet is better than a delayed one. Applications handle loss gracefully (video skips a frame, audio conceals the gap).
- **Online games**: low latency matters more than reliability. Games send position updates 60/s — a missed one is just outdated data.
- **QUIC**: uses UDP as a substrate and builds its own reliability mechanism on top.

### TCP — Reliable Byte Stream

TCP provides an ordered, reliable, flow-controlled byte stream between two endpoints.

**TCP Header** (20 bytes minimum):
```
[src_port 2B] [dst_port 2B]
[sequence_number 4B]
[acknowledgement_number 4B]
[flags: SYN ACK FIN RST PSH URG] [window_size 2B]
[checksum 2B] [urgent_pointer 2B]
[options variable] [data variable]
```

### The Three-Way Handshake

Before data transfer, TCP establishes a connection:

```
Client → Server: SYN, seq=x
Server → Client: SYN-ACK, seq=y, ack=x+1
Client → Server: ACK, seq=x+1, ack=y+1
(connection established)
```

`SYN` (synchronise) starts a connection and carries the initial sequence number. The sequence number is a 32-bit counter for tracking byte positions.

**Connection termination** (four-way):
```
Client → Server: FIN, seq=m
Server → Client: ACK, ack=m+1
Server → Client: FIN, seq=n
Client → Server: ACK, ack=n+1
```

Both sides must explicitly close — TCP connections are full-duplex and each direction closes independently.

### Reliability — Sequence Numbers and ACKs

Each byte in the stream has a sequence number. The receiver sends acknowledgements (`ACK`) confirming bytes received.

**Retransmission**: if the sender doesn't receive an ACK within a timeout (RTO — Retransmission Timeout), it resends the unacknowledged data.

**Sliding window**: the sender can have multiple unacknowledged segments in flight (up to the window size). This is essential for performance on high-latency links — waiting for one ACK per segment at 100ms RTT means only 10 round trips per second regardless of bandwidth.

### Flow Control — Receiver Window

The receiver advertises how much buffer space it has (`window_size` in the header). The sender never sends more data than the receiver can buffer.

If the receiver's buffer fills (window=0), the sender stops and periodically probes with a 1-byte segment to check if the window reopened.

### Congestion Control

The network can become congested — routers drop packets when buffers overflow. TCP detects congestion via:
- **Packet loss** (timeout or duplicate ACKs)
- **ECN** (Explicit Congestion Notification): routers mark packets instead of dropping them

TCP's congestion control algorithms:

**Slow Start**: begin with cwnd (congestion window) = 1 MSS (maximum segment size). Double cwnd every RTT. This is "slow" compared to sending immediately at full rate, not actually slow.

**Congestion Avoidance**: when cwnd exceeds ssthresh (slow start threshold), increase linearly by 1 MSS per RTT.

**On packet loss** (Reno): set ssthresh = cwnd/2, reset cwnd = 1 MSS, restart slow start.

**BBR** (Bottleneck Bandwidth and RTT, Google 2016): models the network path's bandwidth and RTT rather than responding to loss. Achieves much better throughput on long-distance links and in data centres. Used by ~50% of TCP traffic on YouTube.

### TCP vs UDP Comparison

| Feature | TCP | UDP |
|---|---|---|
| Connection | Yes (3-way handshake) | No |
| Reliability | Guaranteed delivery | Best effort |
| Ordering | In-order delivery | Out of order possible |
| Flow control | Yes (window) | No |
| Congestion control | Yes | No |
| Overhead | ~20 byte header + state | 8 byte header |
| Latency | Higher (handshake, retransmit) | Lower |
| Use cases | HTTP, email, file transfer, databases | DNS, video, gaming, QUIC |

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — TCP Handshake and State Machine**
- Step through the three-way handshake
- See the sequence/acknowledgement numbers
- Watch the TCP state machine: CLOSED → SYN_SENT → ESTABLISHED → FIN_WAIT → CLOSED

**Tool 2 — Sliding Window**
- A sender with window size 4
- Send 8 segments; watch which are in-flight, which are acknowledged
- Drop one segment — watch retransmission and window stop-and-wait

**Tool 3 — Congestion Control**
- Watch CWND grow: slow start (exponential), congestion avoidance (linear)
- Trigger a loss event — watch CWND drop and recovery

---

## Going Deeper

**TCP Fast Retransmit**: if 3 duplicate ACKs arrive (receiver gets packets 1, 3, 4, 5 but not 2 — so it ACKs packet 1 three times), the sender retransmits packet 2 immediately without waiting for the timeout. This is much faster than waiting for the RTO (~1 second) when a single packet is dropped.

**SCTP and MPTCP**: SCTP (Stream Control Transmission Protocol, 2000) addresses some TCP limitations: multi-homing (failover between network interfaces), multi-streaming (no head-of-line blocking), and message-oriented delivery. MPTCP (Multipath TCP) allows a single connection to use multiple paths simultaneously (e.g., Wi-Fi + cellular) — used in iOS for Siri.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace the sequence numbers in a TCP exchange for a 3-segment file transfer, calculate the maximum throughput for a TCP connection with a 64 KB window over a 100ms RTT link, explain why three duplicate ACKs are a better congestion signal than timeout, and write the UDP and TCP server/client code for a simple echo service.
