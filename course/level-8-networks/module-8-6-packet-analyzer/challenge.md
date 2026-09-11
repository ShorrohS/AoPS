# Challenge 8.6 — Building a Packet Analyzer

**Type:** Decode + implementation + reasoning  
**Estimated time:** 45–55 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — Manual Packet Decode

Decode this raw packet (hex bytes). It is a complete Ethernet/IPv4/TCP frame.

```
FF FF FF FF FF FF  AA BB CC DD EE FF  08 00
45 00 00 3C 1A 2B 40 00 40 06 00 00
C0 A8 01 05  08 08 08 08
C3 50  01 BB  00 00 00 01  00 00 00 00
50 02  20 00  00 00  00 00
```

1. Parse the Ethernet header (bytes 0–13):
   - Destination MAC
   - Source MAC
   - EtherType

2. Parse the IPv4 header (bytes 14–33):
   - Version and IHL
   - Total length
   - TTL
   - Protocol
   - Source IP
   - Destination IP

3. Parse the TCP header (bytes 34–53):
   - Source port
   - Destination port
   - Sequence number
   - Flags (identify which flags are set)

4. Based on your decode: what kind of packet is this? Where is it going? What is the application?

---

## Part B — Python Decoder

5. Implement `parse_ethernet(frame_bytes)` that returns a dict with `dst_mac`, `src_mac`, `ethertype`, and `payload`.

6. Implement `parse_ipv4(ip_bytes)` that returns a dict with `version`, `ihl`, `ttl`, `protocol`, `src_ip`, `dst_ip`, and `payload`.

7. Implement `parse_tcp(tcp_bytes)` that returns a dict with `src_port`, `dst_port`, `seq`, `ack`, `flags` (as a set of strings: `{'SYN', 'ACK'}` etc.), and `payload`.

8. Chain the three parsers: write `decode_frame(raw_bytes)` that calls each in turn and returns the full decoded structure as a nested dict.

---

## Part C — DNS Packet

A DNS query packet (UDP payload only, 29 bytes):

```
AB CD 01 00 00 01 00 00 00 00 00 00
03 77 77 77 06 67 69 74 68 75 62 03 63 6F 6D 00
00 01 00 01
```

9. Parse the DNS header (bytes 0–11): transaction ID, flags, QDCOUNT (question count), ANCOUNT, NSCOUNT, ARCOUNT.

10. Parse the question section (bytes 12–28): decode the DNS name encoding (length-prefixed labels). What domain name is being queried? What query type (byte 27–28) and class?

11. Write `decode_dns_name(data, offset)` that decodes the length-prefixed label format into a dotted-string domain name.

---

## Part D — BPF Filters

12. Translate these tcpdump/BPF filter expressions into English descriptions:
    - `tcp port 443`
    - `src host 192.168.1.5 and dst port 80`
    - `icmp and not src host 127.0.0.1`
    - `udp and port 53`

13. Write a Python function `matches_filter(packet, filter_spec)` that takes a decoded packet (as returned by your decoder) and a simple filter spec dict, and returns True/False:

```python
filter_spec = {
    'protocol': 'tcp',     # optional
    'src_ip': '...',       # optional
    'dst_port': 443,       # optional
}
```

---

## Part E — Promiscuous Mode and Ethics

14. What is **promiscuous mode**? Why does a NIC normally discard frames not addressed to it? What does promiscuous mode change?

15. Why does capturing packets on a network interface require **root/admin privileges** on most operating systems?

16. Is it legal to run a packet analyzer on:
    - Your own computer
    - Your company's network with IT permission
    - A public Wi-Fi network (capturing other users' traffic)
    - A network you do not own or have permission to monitor
    
    Briefly explain the legal and ethical considerations for each.

---

## Rubric

| Part | Points |
|---|---|
| A manual decode | 28 |
| B Python decoder | 24 |
| C DNS packet | 20 |
| D BPF filters | 16 |
| E ethics | 12 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A — decoded packet</summary>

Ethernet: Dst=FF:FF:FF:FF:FF:FF (broadcast), Src=AA:BB:CC:DD:EE:FF, EtherType=0x0800 (IPv4).

IPv4: Ver=4, IHL=5 (20 bytes), TotalLen=0x003C=60, TTL=0x40=64, Protocol=0x06=TCP, Src=192.168.1.5, Dst=8.8.8.8.

TCP: SrcPort=0xC350=50000, DstPort=0x01BB=443 (HTTPS), Seq=1, Ack=0, Flags=0x02=SYN.

This is a TCP SYN packet from 192.168.1.5 initiating a connection to 8.8.8.8:443 (Google DNS HTTPS). This is the first packet of a TLS/HTTPS connection.
</details>

<details>
<summary>Part B.5–7 — decoders</summary>

```python
import struct

def fmt_mac(b): return ':'.join(f'{x:02X}' for x in b)
def fmt_ip(b):  return '.'.join(str(x) for x in b)

def parse_ethernet(frame):
    return {
        'dst_mac': fmt_mac(frame[0:6]),
        'src_mac': fmt_mac(frame[6:12]),
        'ethertype': struct.unpack('!H', frame[12:14])[0],
        'payload': frame[14:]
    }

def parse_ipv4(ip):
    ihl = (ip[0] & 0x0F) * 4
    ttl, proto = ip[8], ip[9]
    return {
        'version': ip[0] >> 4, 'ihl': ihl,
        'ttl': ttl, 'protocol': proto,
        'src_ip': fmt_ip(ip[12:16]),
        'dst_ip': fmt_ip(ip[16:20]),
        'payload': ip[ihl:]
    }

def parse_tcp(tcp):
    sp, dp = struct.unpack('!HH', tcp[0:4])
    seq, ack = struct.unpack('!II', tcp[4:12])
    off = (tcp[12] >> 4) * 4
    flags = tcp[13]
    flag_names = {0x01:'FIN',0x02:'SYN',0x04:'RST',0x08:'PSH',0x10:'ACK',0x20:'URG'}
    return {
        'src_port': sp, 'dst_port': dp, 'seq': seq, 'ack': ack,
        'flags': {n for m,n in flag_names.items() if flags & m},
        'payload': tcp[off:]
    }
```
</details>

<details>
<summary>Part C.10 — DNS name decode</summary>

Bytes 12–28: 03 77 77 77 = label length 3 + "www"; 06 67 69 74 68 75 62 = length 6 + "github"; 03 63 6F 6D = length 3 + "com"; 00 = end. Domain: "www.github.com". Type 0x0001 = A record. Class 0x0001 = IN (Internet).
</details>
