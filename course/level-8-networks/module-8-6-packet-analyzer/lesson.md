# Module 8.6 — Building a Packet Analyzer

---

## The Problem

> You've studied the network stack from physical to application layer.
> Theory is one thing. Seeing real bytes on the wire is another.
>
> A packet analyzer — a program that captures and decodes network packets —
> is the most powerful tool for understanding how networks actually work.
> Wireshark, tcpdump, and tshark are the professionals' tools.
> Building a minimal version teaches you every header and field you've studied,
> as real hex bytes.

---

## The Story

### Wireshark and Packet Capture

**tcpdump** was written by Van Jacobson and others at Lawrence Berkeley National Laboratory in 1988. It is still the primary command-line tool for packet capture on Unix systems, running on every Linux and macOS system.

**Ethereal** (later renamed **Wireshark**, 2006) was written by Gerald Combs starting in 1997. It added a GUI, protocol dissectors for hundreds of protocols, and became the de facto standard tool for network analysis. Used by security researchers, network engineers, protocol developers, and system administrators worldwide.

Both tools use **libpcap** (Linux: pcap, Windows: Npcap) to capture packets from network interfaces at the OS level. The OS kernel copies arriving packets into a ring buffer accessible to capture programs — without disrupting normal packet processing.

---

## The Concept

### Raw Sockets and libpcap

To capture all packets on a network interface (not just those addressed to this machine), you need a **raw socket** with promiscuous mode enabled:

```python
import socket, struct

# Raw socket — requires root/admin privileges
sock = socket.socket(socket.AF_PACKET,   # Linux: packet-level access
                     socket.SOCK_RAW,
                     socket.htons(0x0003))  # ETH_P_ALL: capture all protocols

while True:
    raw_data, addr = sock.recvfrom(65535)
    parse_ethernet(raw_data)
```

### Parsing Ethernet Frames

```python
def parse_ethernet(frame):
    # Ethernet header: 6B dst, 6B src, 2B ethertype
    dst_mac = format_mac(frame[0:6])
    src_mac = format_mac(frame[6:12])
    ethertype = struct.unpack('!H', frame[12:14])[0]   # big-endian unsigned short

    print(f"Ethernet: {src_mac} → {dst_mac}  EtherType: 0x{ethertype:04X}")

    if ethertype == 0x0800:    # IPv4
        parse_ipv4(frame[14:])
    elif ethertype == 0x0806:  # ARP
        parse_arp(frame[14:])
    elif ethertype == 0x86DD:  # IPv6
        parse_ipv6(frame[14:])

def format_mac(b):
    return ':'.join(f'{x:02X}' for x in b)
```

### Parsing IPv4

```python
def parse_ipv4(packet):
    version_ihl = packet[0]
    ihl = (version_ihl & 0x0F) * 4          # header length in bytes
    ttl = packet[8]
    protocol = packet[9]
    src_ip = '.'.join(str(b) for b in packet[12:16])
    dst_ip = '.'.join(str(b) for b in packet[16:20])

    print(f"  IPv4: {src_ip} → {dst_ip}  TTL={ttl}  Proto={protocol}")

    payload = packet[ihl:]
    if protocol == 6:    # TCP
        parse_tcp(payload)
    elif protocol == 17: # UDP
        parse_udp(payload)
    elif protocol == 1:  # ICMP
        parse_icmp(payload)

def ip_to_str(b):
    return '.'.join(str(x) for x in b)
```

### Parsing TCP

```python
def parse_tcp(segment):
    src_port = struct.unpack('!H', segment[0:2])[0]
    dst_port = struct.unpack('!H', segment[2:4])[0]
    seq      = struct.unpack('!I', segment[4:8])[0]
    ack      = struct.unpack('!I', segment[8:12])[0]
    offset   = (segment[12] >> 4) * 4    # data offset (header length)
    flags    = segment[13]

    flag_str = ''.join([
        'SYN ' if flags & 0x02 else '',
        'ACK ' if flags & 0x10 else '',
        'FIN ' if flags & 0x01 else '',
        'RST ' if flags & 0x04 else '',
        'PSH ' if flags & 0x08 else '',
    ])

    print(f"    TCP: {src_port} → {dst_port}  seq={seq}  ack={ack}  [{flag_str.strip()}]")
    payload = segment[offset:]
    if payload:
        parse_application(src_port, dst_port, payload)

def parse_udp(segment):
    src_port = struct.unpack('!H', segment[0:2])[0]
    dst_port = struct.unpack('!H', segment[2:4])[0]
    length   = struct.unpack('!H', segment[4:6])[0]
    print(f"    UDP: {src_port} → {dst_port}  len={length}")
    if dst_port == 53 or src_port == 53:
        parse_dns(segment[8:])
```

### Parsing HTTP (Application Layer)

```python
def parse_application(src_port, dst_port, payload):
    try:
        text = payload.decode('utf-8', errors='replace')
    except: return

    if dst_port == 80 or src_port == 80:
        lines = text.split('\r\n')
        if lines[0].startswith(('GET ','POST ','HTTP/')):
            print(f"      HTTP: {lines[0]}")
```

### DNS Parsing

```python
def parse_dns(data):
    tx_id    = struct.unpack('!H', data[0:2])[0]
    flags    = struct.unpack('!H', data[2:4])[0]
    qr       = (flags >> 15) & 1    # 0=query, 1=response
    q_count  = struct.unpack('!H', data[4:6])[0]

    # Parse the first question (simplified)
    i = 12   # skip header
    name_parts = []
    while i < len(data) and data[i] != 0:
        length = data[i]; i += 1
        name_parts.append(data[i:i+length].decode('ascii','replace'))
        i += length
    name = '.'.join(name_parts)

    qtype = struct.unpack('!H', data[i+1:i+3])[0]
    type_str = {1:'A', 28:'AAAA', 15:'MX', 2:'NS', 5:'CNAME'}.get(qtype, str(qtype))
    print(f"      DNS: {'Response' if qr else 'Query'} id={tx_id:#06x} "
          f"{'reply' if qr else f'{name} {type_str}'}")
```

### Putting It Together

A complete, functional packet analyzer in ~100 lines of Python. Add:
- **Filtering**: only show TCP on port 443, or only DNS, or only packets from a specific IP
- **Statistics**: packet count per protocol, bytes per second, top talkers
- **Flow reconstruction**: reassemble TCP streams to reconstruct HTTP transactions
- **File output**: write to pcap format for later analysis with Wireshark

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Hex Packet Decoder**
- Paste a raw packet as hex bytes
- Watch each field parsed: Ethernet → IPv4 → TCP/UDP → payload
- Colour-code each layer (Layer 2 = gold, Layer 3 = blue, Layer 4 = red)

**Tool 2 — Live Capture Replay**
- Pre-recorded packet captures (HTTP request, DNS query, TCP handshake)
- Step through each packet; see decoded fields
- Reconstruct the HTTP conversation from the packet sequence

**Tool 3 — Build Your Filter**
- Enter a BPF-like filter expression (e.g., `tcp port 80`, `src host 192.168.1.1`)
- See which packets in the capture match the filter
- Understand how display filters and capture filters differ

---

## Going Deeper

**BPF (Berkeley Packet Filter)**: the filtering language used by tcpdump, Wireshark, and seccomp. BPF expressions are compiled to a tiny virtual machine that runs inside the kernel — packets are filtered before being copied to user space, dramatically reducing overhead. eBPF (extended BPF) is a modern evolution that allows arbitrary programs to run in the kernel for tracing, security monitoring, and network processing. eBPF is one of the most significant additions to the Linux kernel in the last decade.

**Wireshark dissectors**: Wireshark's protocol understanding comes from "dissectors" — plugins that parse specific protocols. There are 3,000+ dissectors. Writing a Wireshark dissector for a proprietary protocol (a common task in network engineering) requires understanding exactly the byte layout at every layer.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Decode a given 60-byte raw Ethernet/IPv4/TCP packet (as hex) by hand, identifying every field and its value. Then: write a Python filter that captures only DNS queries (UDP port 53), parse a DNS response packet and extract the answer IP addresses, and explain what "promiscuous mode" means and why you need root privileges to capture packets.
