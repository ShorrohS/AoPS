# Module 8.1 — Physical and Data Link Layers

---

## The Problem

> Two computers. A wire between them.
> How do bits get from one to the other?
> And if the wire is shared by 100 computers, how does each
> computer know which bits were meant for it?
>
> These questions are answered at the two lowest layers of the network stack:
> the **Physical Layer** (turning bits into signals)
> and the **Data Link Layer** (framing, addressing, and access control).

---

## The Story

### From Morse Code to Ethernet

The physical layer problem is as old as electrical communication. Samuel Morse's telegraph (1844) was a one-bit physical layer: key down = 1, key up = 0. The modulation scheme (dots and dashes) was a data link layer that enabled human-readable encoding.

**Ethernet** was invented at Xerox PARC in 1973 by Robert Metcalfe and David Boggs. The name comes from "ether" — the medium through which light was once thought to propagate. The core problem Metcalfe solved was how to share a single cable among multiple computers without a central controller — the **CSMA/CD** (Carrier Sense Multiple Access with Collision Detection) protocol.

The 10Base5 "thick Ethernet" cable of the 1970s literally connected computers through a shared coaxial cable — any computer could listen to any other's transmissions. Modern Ethernet uses switches, but the addressing scheme (MAC addresses) and framing format are essentially unchanged from 1980.

---

## The Concept

### Layer 1: The Physical Layer

The physical layer is responsible for transmitting a sequence of bits over a physical medium. It is not concerned with what the bits mean — only with reliably transferring each 0 and 1.

**Encoding schemes:**
- **NRZ (Non-Return to Zero)**: 1 = high voltage, 0 = low voltage. Problem: long strings of same bit lose clock synchronisation.
- **Manchester encoding**: each bit includes a transition: 1 = low-to-high, 0 = high-to-low. Used in early Ethernet. Reliable but uses 2× bandwidth.
- **4B/5B**: encode every 4 bits as a 5-bit code chosen to prevent long runs of zeros. Used in 100Base-TX (Fast Ethernet).
- **PAM-4** (4-level pulse amplitude modulation): four voltage levels encode 2 bits per symbol. Used in 25G, 100G, 400G Ethernet.

**Physical media:**
- **Twisted pair copper** (Cat5e, Cat6, Cat7): standard for LAN. Pairs twisted to reduce electromagnetic interference. Up to 10 Gbps for Cat6A at 55m.
- **Fibre optic**: light pulses in glass or plastic fibre. Single-mode: 100 km+ at 400 Gbps. Multi-mode: shorter distances, cheaper. Used for all long-distance and data centre interconnects.
- **802.11 (Wi-Fi)**: radio waves. Physical layer uses OFDM (Orthogonal Frequency Division Multiplexing) — simultaneously transmit on many sub-carriers. Wi-Fi 6 (802.11ax): up to 9.6 Gbps theoretical.

### Layer 2: The Data Link Layer

The data link layer takes raw bits and organises them into **frames** — logical units with headers, payload, and error checking.

**Ethernet frame format** (IEEE 802.3):
```
Preamble (7B) | SFD (1B) | Dst MAC (6B) | Src MAC (6B) | EtherType (2B) | Payload (46-1500B) | FCS (4B)
```
- **Preamble + SFD**: synchronisation — `10101010...10101011` lets the receiver lock onto the clock
- **Destination MAC**: 6-byte hardware address of the intended recipient
- **Source MAC**: sender's hardware address
- **EtherType**: what protocol is in the payload (`0x0800` = IPv4, `0x0806` = ARP, `0x86DD` = IPv6)
- **Payload**: 46–1500 bytes (the MTU — maximum transmission unit — is 1500 bytes for standard Ethernet)
- **FCS (Frame Check Sequence)**: CRC-32 checksum to detect transmission errors

**MAC Addresses**:
Every network interface has a globally unique 48-bit MAC address burned in at manufacture. Format: `AA:BB:CC:DD:EE:FF`. First 24 bits = OUI (Organisationally Unique Identifier, assigned to the manufacturer). Last 24 bits = device-specific.

Special addresses:
- `FF:FF:FF:FF:FF:FF` = broadcast (all devices on the local segment receive it)
- `01:00:5E:xx:xx:xx` = IPv4 multicast

**MAC addresses are local**: they only matter within a single network segment (broadcast domain). The IP address is what matters for routing between networks.

### CSMA/CD — Ethernet's Collision Protocol

Early Ethernet (bus topology — all computers on one shared cable) used CSMA/CD:

1. **Carrier Sense**: before transmitting, listen if someone else is already transmitting. If so, wait.
2. **Multiple Access**: multiple computers share the same medium.
3. **Collision Detection**: while transmitting, listen. If what you hear differs from what you're sending, a collision occurred (two computers started transmitting simultaneously). Both stop, wait a **random backoff** time (exponential backoff), and retry.

Modern switched Ethernet is **full-duplex point-to-point** — each cable connects one computer to one switch port. No shared medium, no collisions possible. CSMA/CD is not used but is still specified by the standard.

### Switches — The Data Link Layer Device

A **network switch** operates at Layer 2. It:
1. **Learns** MAC addresses: when a frame arrives on a port, it associates the source MAC with that port in its **MAC address table** (CAM table).
2. **Forwards** frames: looks up the destination MAC; if found, sends only to that port; if not, **floods** to all ports except the source.
3. Creates **collision domains** per port: each port is a separate collision domain — no more shared medium.

A 24-port switch with all links active gives each device its full bandwidth (unlike a hub, where all devices share the bandwidth).

**VLANs** (Virtual LANs): divide a physical switch into multiple logical segments. Frames carry a **VLAN tag** (IEEE 802.1Q, 4 bytes added to the frame) identifying which VLAN they belong to. Frames from different VLANs cannot communicate directly — they must be routed (Layer 3).

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Manchester Encoding**
- Enter a bit sequence (e.g., `10110010`)
- Watch it converted to a Manchester-encoded waveform
- See how clock transitions enable synchronisation

**Tool 2 — Ethernet Frame Builder**
- Set source MAC, destination MAC, EtherType, and payload
- Watch the frame assembled byte by byte
- Compute the CRC-32 FCS

**Tool 3 — Switch Learning and Forwarding**
- A small network: 4 computers, 1 switch
- Send frames and watch the MAC address table fill
- See the difference between unicast forwarding and flooding

---

## Going Deeper

**Spanning Tree Protocol (STP)**: in real networks, redundant switch paths prevent single points of failure but create loops. Without loop prevention, a broadcast frame would circulate forever (broadcast storm). STP detects loops and blocks redundant links, creating a loop-free tree topology. RSTP (Rapid STP) and MSTP are modern successors used in production networks.

**CRC (Cyclic Redundancy Check)**: the Frame Check Sequence is a 32-bit CRC computed over the entire frame content. CRC is a polynomial division in GF(2) — efficient to compute in hardware (a shift register with XOR feedback). It detects all single-bit errors, all burst errors of length ≤ 32 bits, and most random errors. It does not correct errors — frames with bad FCS are silently discarded and must be retransmitted by higher layers.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Decode a Manchester-encoded waveform, calculate the time to transmit a 1500-byte Ethernet frame on a 100 Mbps link, trace the switch MAC table after 5 frame transmissions between 3 computers, and explain why CSMA/CD is unnecessary on a modern switched full-duplex network.
