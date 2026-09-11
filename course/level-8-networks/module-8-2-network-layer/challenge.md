# Challenge 8.2 — Network Layer: IP and Routing

**Type:** Calculation + trace + reasoning  
**Estimated time:** 40–50 minutes  
**Tools needed:** pen and paper

---

## Part A — Subnet Calculations

For each of the following, compute: network address, broadcast address, first and last usable host address, number of usable hosts.

1. `192.168.10.50/24`
2. `10.0.5.130/25`
3. `172.16.0.200/20`

4. How many /27 subnets can you create from a single /24 network? How many usable hosts does each /27 provide?

5. You have the block `10.10.0.0/22`. Divide it into exactly 4 equal subnets. List the network address and prefix length for each.

---

## Part B — Longest Prefix Match

A router has this routing table:

| Destination | Prefix | Next Hop |
|---|---|---|
| 192.168.1.0/24 | | Router A |
| 192.168.1.128/25 | | Router B |
| 192.168.0.0/16 | | Router C |
| 10.0.0.0/8 | | Router D |
| 0.0.0.0/0 | | ISP Gateway |

For each destination IP, identify which route is used and why:

6. `192.168.1.200`
7. `192.168.1.100`
8. `192.168.2.5`
9. `10.255.255.255`
10. `8.8.8.8`

---

## Part C — TTL and traceroute

11. A packet is sent with TTL=3. It traverses routers R1→R2→R3→R4 before reaching the destination. At which router is the packet dropped? What ICMP message is sent back, and to whom?

12. **traceroute** sends probes with TTL=1, 2, 3, ... to map the path to a destination. Explain:
    - What response does TTL=1 produce (and from whom)?
    - What response does the final TTL (reaching the destination) produce?
    - Why does traceroute send 3 probes per TTL?

13. A traceroute shows `* * *` at hop 3 (three timeouts). What are three possible reasons? Does this mean the path is broken?

---

## Part D — NAT Trace

A home network has NAT router at public IP `203.0.113.1`. Internal hosts use `192.168.1.0/24`.

14. Internal host `192.168.1.5` sends a DNS query to `8.8.8.8:53`. The source port is `54321`. Complete the NAT translation table entry and show the translated packet headers.

15. The DNS response arrives at the router addressed to `203.0.113.1:54321`. How does the router know to deliver it to `192.168.1.5`?

16. Two internal hosts (`192.168.1.5:54321` and `192.168.1.10:54321`) both send packets to `8.8.8.8:53` at the same time. How does NAT handle the port collision? What appears in the NAT table?

---

## Part E — IPv6

17. An IPv6 address is `2001:0db8:0000:0000:0000:8a2e:0370:7334`. Compress it using:
    - Leading zero omission
    - `::` for the longest run of consecutive all-zero groups

18. IPv6 eliminates the need for NAT. Why? What property of IPv6 addressing makes NAT unnecessary?

19. The IPv6 header is **simpler** than IPv4 despite having larger addresses. Name two fields that were removed from IPv4 and explain why each was removed.

---

## Rubric

| Part | Points |
|---|---|
| A subnet calculations | 24 |
| B longest prefix match | 20 |
| C TTL and traceroute | 20 |
| D NAT trace | 22 |
| E IPv6 | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1–3</summary>

1. `192.168.10.50/24`: Network=192.168.10.0, Broadcast=192.168.10.255, Hosts=192.168.10.1–254, Count=254.

2. `10.0.5.130/25`: Mask=255.255.255.128. 130 ≥ 128 → second half. Network=10.0.5.128, Broadcast=10.0.5.255, Hosts=10.0.5.129–254, Count=126.

3. `172.16.0.200/20`: Mask=255.255.240.0. 200/256 in 3rd octet → 0.0 block. Network=172.16.0.0, Broadcast=172.16.15.255, Hosts=172.16.0.1–172.16.15.254, Count=4094.
</details>

<details>
<summary>Part B.6–10</summary>

6. `192.168.1.200`: matches /24 AND /25 (200 ≥ 128 → in 192.168.1.128/25). **Longest prefix wins: Router B (/25)**.
7. `192.168.1.100`: matches /24 only (100 < 128). **Router A (/24)**.
8. `192.168.2.5`: matches /16 only. **Router C**.
9. `10.255.255.255`: matches /8. **Router D**.
10. `8.8.8.8`: no specific match. **ISP Gateway (default route 0.0.0.0/0)**.
</details>

<details>
<summary>Part C.11</summary>

TTL=3: decremented at R1 (→2), R2 (→1), R3 (→0). R3 drops the packet and sends **ICMP Time Exceeded (Type 11, Code 0)** back to the original sender's IP address.
</details>
