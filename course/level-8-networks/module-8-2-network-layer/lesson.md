# Module 8.2 — Network Layer: IP and Routing

---

## The Problem

> Ethernet connects computers on the same local segment.
> But your laptop is not on the same cable as a server in Tokyo.
> Billions of machines are connected through an interconnected web of networks.
>
> How does a packet travel from your machine to one in Tokyo
> — through dozens of intermediate routers, different network technologies,
> different countries — and arrive at exactly the right destination?
>
> This is the network layer's problem: **global addressing and routing**.

---

## The Story

### The Internet Is a Network of Networks

The ARPANET (1969) connected four universities. By 1972 it had 40 nodes. By 1975 it was a US government backbone. The challenge: connect different networks — ARPANET, satellite links, radio networks — using a common protocol.

**Vint Cerf and Bob Kahn** designed IP (Internet Protocol) in 1974. The key principle: IP makes no assumptions about the underlying network. It doesn't care if the link is Ethernet, Wi-Fi, dial-up, or carrier pigeon (RFC 1149, 1990 — an actual internet standard). IP provides a common addressing scheme and best-effort delivery. Reliability was left to the transport layer (TCP).

**IPv4** (1981) remains the dominant protocol with 4.3 billion addresses. Address exhaustion, foreseen since the 1980s, forced the development of **IPv6** (1998) with 2¹²⁸ addresses. The internet has been running a simultaneous IPv4/IPv6 transition since the 1990s — still ongoing.

---

## The Concept

### IPv4 Addresses

An IPv4 address is a 32-bit number, written as 4 decimal octets: `192.168.1.100`.

```
192.168.1.100
│   │   │ │
│   │   │ └── Host (100) within the subnet
│   │   └──── Subnet (1)
│   └──────── Network (168)
└──────────── Network (192)
```

**Subnet masks** define the boundary between network and host portions:
- `/24` (255.255.255.0): first 24 bits = network, last 8 bits = host. 256 addresses, 254 usable.
- `/16` (255.255.0.0): first 16 bits = network. 65,536 addresses.
- `/32`: single host.

**CIDR notation** (Classless Inter-Domain Routing): `192.168.1.0/24` means the 256 addresses `192.168.1.0` through `192.168.1.255`.

**Special addresses:**
- `127.0.0.0/8`: loopback (`127.0.0.1` = "this machine")
- `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`: private (not routable on the internet)
- `0.0.0.0/0`: default route (matches everything)
- Broadcast: last address in subnet (e.g., `192.168.1.255` for `/24`)

### IPv4 Packet Header

```
 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Ver=4|IHL| DSCP    |ECN|        Total Length                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      Identification           |Flags| Fragment Offset         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   TTL         |  Protocol     |       Header Checksum         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     Source IP Address                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                  Destination IP Address                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**TTL (Time to Live)**: decremented by each router. Prevents packets looping forever. If TTL reaches 0, packet is dropped and ICMP Time Exceeded is sent back. Starting TTL is typically 64 or 128.

**Protocol**: identifies the transport layer protocol. 6=TCP, 17=UDP, 1=ICMP.

**Fragmentation**: if a packet is larger than a link's MTU, it is split into fragments, each with the same Identification. Reassembled at the destination. Modern practice: use **Path MTU Discovery** instead — discover the smallest MTU on the path and never send packets that need fragmenting.

### Routing

Each router maintains a **routing table** — a set of rules mapping destination prefixes to next-hop routers or output interfaces:

```
Network          Netmask          Gateway        Interface
0.0.0.0          0.0.0.0          10.0.0.1       eth0    ← default route
10.0.0.0         255.255.255.0    0.0.0.0        eth0    ← directly connected
192.168.1.0      255.255.255.0    0.0.0.0        eth1    ← directly connected
```

**Longest prefix match**: when multiple routes match a destination, the most specific (longest prefix) wins. `10.1.2.3` matches both `10.0.0.0/8` and `10.1.0.0/16` — the `/16` wins because it's more specific.

### Routing Protocols

Routers learn routes from each other using routing protocols:

**RIP (Routing Information Protocol)**: distance-vector, hop count as metric. Simple, slow convergence, max 15 hops. Used in small networks.

**OSPF (Open Shortest Path First)**: link-state routing. Each router floods its link state to all others; every router builds a complete topology map and computes shortest paths (Dijkstra's algorithm). Fast convergence, no hop limit. Used in enterprise and ISP networks.

**BGP (Border Gateway Protocol)**: the protocol of the internet. Connects **autonomous systems** (ASes) — networks operated by ISPs, companies, universities. BGP carries policy information (not just cost) — an ISP can prefer routes through certain ASes, avoid others, or limit what routes it advertises. The internet's routing table has ~900,000+ BGP routes.

### NAT — Network Address Translation

Private addresses (`192.168.x.x`) are not routable on the internet. **NAT** (typically on a home router) rewrites source IP and port:

```
Outbound: 192.168.1.5:54321 → 8.8.8.8:53
NAT rewrites to: 203.0.113.1:41234 → 8.8.8.8:53
(203.0.113.1 = public IP of the router)

Return: 8.8.8.8:53 → 203.0.113.1:41234
NAT rewrites back to: 8.8.8.8:53 → 192.168.1.5:54321
```

NAT effectively allows millions of devices to share a few public IP addresses, delaying IPv4 exhaustion for decades. The downside: breaks the end-to-end principle — devices behind NAT cannot easily receive incoming connections.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Subnet Calculator**
- Enter an IP/CIDR (e.g., `192.168.10.0/24`)
- See: network address, broadcast, usable host range, number of hosts, subnet mask in binary and decimal

**Tool 2 — Packet Routing Trace**
- A small internet of 6 routers
- Enter source and destination IPs
- Watch the packet hop from router to router with TTL decrementing
- See the routing table lookup at each hop (longest prefix match)

**Tool 3 — NAT Visualiser**
- 3 private hosts behind a NAT router
- Watch each outbound connection get a NAT entry
- See the reverse translation on reply packets

---

## Going Deeper

**IPv6**: 128-bit addresses written as 8 groups of 4 hex digits: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`. Leading zeros omit-able, consecutive zero groups replaced with `::`. IPv6 eliminates NAT (every device gets a globally unique address), simplifies headers, includes mandatory IPsec, and has stateless address autoconfiguration. Adoption is ~45% of internet traffic as of 2024.

**ICMP**: the Internet Control Message Protocol. Used for diagnostics and error reporting. `ping` uses ICMP Echo Request/Reply. `traceroute` sends packets with TTL=1, 2, 3... — each router that drops a packet (TTL expired) sends ICMP Time Exceeded back, revealing the path. ICMP is essential for network troubleshooting.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Calculate the number of usable hosts for /24, /20, and /28 subnets, trace longest-prefix-match routing for given destination IPs and a routing table, explain what happens when TTL reaches 0 and how traceroute exploits this, and describe one benefit and one downside of NAT.
