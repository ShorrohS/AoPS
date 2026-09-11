# Module 7.3 — Network Sockets from Scratch

---

## The Problem

> Two programs. Different machines. Possibly different continents.
> How do they exchange data?
>
> The answer — at every layer above bare hardware — is sockets.
> A socket is the API that Unix and Windows expose for network communication.
> Every web server, every game server, every chat application,
> every database client ultimately calls socket(), bind(), listen(), accept(), send(), recv().
>
> Understanding sockets means understanding how *every networked application* is built.

---

## The Story

### The Birth of the Socket API

The Berkeley Software Distribution (BSD) Unix at UC Berkeley introduced the **socket API** in 1983 (4.2BSD). The goal was to create a uniform interface for network communication that abstracted over different network protocols (TCP/IP, Xerox NS, UNIX domain sockets).

The BSD socket API was so well-designed that it was adopted by every Unix-like system, then by Windows (as WinSock, 1993), and is now the standard network API on every major platform. It has been essentially unchanged for 40 years.

The core insight: a socket is a **file descriptor** — it behaves like a file. You `open()` it (socket()), you `read()` from it (recv()), you `write()` to it (send()), you `close()` it. The "everything is a file" Unix philosophy (Module 4.3) applied to networking.

---

## The Concept

### TCP Socket — Client-Server Model

**Server side:**
```python
import socket

# 1. Create socket — IPv4, TCP (stream)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Allow reuse of address immediately after process ends
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 3. Bind to address and port
server.bind(('0.0.0.0', 8080))

# 4. Listen for incoming connections (backlog = 5)
server.listen(5)
print("Server listening on port 8080")

while True:
    # 5. Accept a new connection (blocks until client connects)
    conn, addr = server.accept()
    print(f"Connection from {addr}")

    # 6. Receive data (up to 1024 bytes)
    data = conn.recv(1024)
    print(f"Received: {data.decode()}")

    # 7. Send response
    conn.send(b"Hello from server!")

    # 8. Close this connection
    conn.close()
```

**Client side:**
```python
import socket

# 1. Create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Connect to server
client.connect(('127.0.0.1', 8080))

# 3. Send data
client.send(b"Hello from client!")

# 4. Receive response
data = client.recv(1024)
print(f"Received: {data.decode()}")

# 5. Close
client.close()
```

### The TCP Handshake (Behind the Scenes)

When `client.connect()` is called, the OS performs the TCP three-way handshake:
1. Client sends SYN (synchronise) to server
2. Server replies SYN-ACK (synchronise-acknowledge)
3. Client sends ACK (acknowledge)
4. Connection established — bidirectional byte stream ready

This handshake takes one round trip (~10 ms on a LAN, ~50–100 ms across the internet). HTTPS adds TLS handshake on top: 1–2 more round trips. Modern TLS 1.3 reduces this to 1 round trip.

### UDP Sockets — Fire and Forget

UDP is connectionless — no handshake, no guarantee of delivery or ordering.

```python
# UDP server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 9090))
data, addr = server.recvfrom(1024)   # returns data + sender address
server.sendto(b"ACK", addr)          # reply (optional)

# UDP client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"Hello", ('127.0.0.1', 9090))   # no connect() needed
```

UDP is used when: low latency matters more than reliability (gaming, video streaming, DNS lookups), or when the application handles its own reliability (QUIC, DTLS).

### Handling Multiple Clients

A single-threaded server handles clients one at a time. For concurrent connections, three approaches:

**1. Threaded server** (one thread per connection):
```python
import threading

def handle_client(conn, addr):
    data = conn.recv(1024)
    conn.send(b"Hello " + data)
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 8080)); server.listen()
while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
```

Scales to ~1,000 clients (memory/thread overhead). Does not scale to 10,000+ connections (C10K problem).

**2. select/poll/epoll** — I/O multiplexing. One thread monitors many sockets simultaneously:
```python
import selectors
sel = selectors.DefaultSelector()
# Register multiple sockets
# sel.select() blocks until any socket is ready
# No threads — one event loop handles all connections
```

This is how nginx handles 50,000+ concurrent connections on one thread — the **event-driven** model.

**3. asyncio** (Python's event-driven networking):
```python
import asyncio

async def handle_client(reader, writer):
    data = await reader.read(1024)
    writer.write(b"Echo: " + data)
    await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8080)
    async with server:
        await server.serve_forever()

asyncio.run(main())
```

### Building a Tiny HTTP Server

HTTP/1.0 is just text over a TCP socket. A minimal server:

```python
import socket, os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 8080)); server.listen(5)

while True:
    conn, _ = server.accept()
    request = conn.recv(4096).decode()
    first_line = request.split('\r\n')[0]  # e.g., "GET /index.html HTTP/1.0"
    path = first_line.split(' ')[1]        # e.g., "/index.html"

    filename = '.' + path
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            body = f.read()
        response = (b"HTTP/1.0 200 OK\r\n"
                   b"Content-Type: text/html\r\n\r\n" + body)
    else:
        response = b"HTTP/1.0 404 Not Found\r\n\r\nNot Found"

    conn.send(response)
    conn.close()
```

This ~20-line server serves static files. A production server (nginx, Apache) is this same concept with: non-blocking I/O, TLS, HTTP/2 multiplexing, gzip compression, virtual hosting, and hundreds of configuration options.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — TCP Handshake Visualiser**
- Click "Connect" and watch SYN, SYN-ACK, ACK packets travel between client and server
- See the sequence numbers, acknowledgement numbers, and state machine

**Tool 2 — Send/Receive Data**
- A virtual client connected to a virtual server
- Type messages and send them
- Watch the TCP segment: headers (source/dest port, seq/ack, flags) + payload

**Tool 3 — Multi-Client Server**
- Launch 3 virtual clients simultaneously
- Compare: single-threaded server (clients queue up), threaded server (all handled simultaneously), event-loop server (all handled with one thread)

---

## Going Deeper

**TCP internals — flow control and congestion control**: TCP ensures neither end overwhelms the other. The **receive window** (advertised by the receiver) limits how much data can be in flight. **Congestion control** (TCP Reno, CUBIC, BBR) detects network congestion and backs off. Understanding these mechanisms explains why a 1 Gbps connection to a server 100ms away achieves much less than 1 Gbps — the bandwidth-delay product limits throughput.

**QUIC**: Google's QUIC protocol (now standardised as RFC 9000, used in HTTP/3) runs over UDP and implements its own reliability, ordering, and multiplexing without the TCP stack. Benefits: 0-RTT connection establishment on repeat connections, no head-of-line blocking, connection migration (change IP without reconnecting). Chrome and most Google services use HTTP/3.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Write a TCP echo server and a matching client, extend the server to handle 3 simultaneous clients using threads, trace a three-way TCP handshake with sequence numbers, and identify the minimum code changes to convert the TCP server to UDP.
