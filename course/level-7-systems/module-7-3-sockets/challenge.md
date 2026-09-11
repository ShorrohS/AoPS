# Challenge 7.3 — Network Sockets from Scratch

**Type:** Implementation + trace + reasoning  
**Estimated time:** 45–55 minutes  
**Tools needed:** Python

---

## Part A — TCP Echo Server and Client

1. Implement a TCP **echo server** that:
   - Listens on port 9000
   - Accepts one connection at a time
   - Reads up to 1024 bytes from the client
   - Sends the same bytes back (echo)
   - Closes the connection and accepts the next one
   - Runs until interrupted

2. Implement a TCP **echo client** that:
   - Connects to `127.0.0.1:9000`
   - Sends the string "Hello, server!"
   - Reads the response and prints it
   - Closes the connection

3. Why do you need `server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)` after creating the server socket? What error occurs without it when you restart the server quickly?

---

## Part B — Multi-Client Server

4. Extend your echo server to handle **multiple simultaneous clients** using threads. Each accepted connection should be handled in a new thread.

5. What is the maximum number of concurrent clients this threaded server can handle? What limits it?

6. Rewrite the multi-client server using Python's `selectors` module (I/O multiplexing, no threads). Register the server socket and each client socket with the selector. Show the event loop.

---

## Part C — TCP Handshake

Trace the **three-way TCP handshake** for a connection from `127.0.0.1:54321` to `127.0.0.1:9000`.

7. Fill in the sequence numbers and flags for each packet:

| Step | Direction | Flags | Seq | Ack |
|------|-----------|-------|-----|-----|
| 1    | Client → Server | ? | x | — |
| 2    | Server → Client | ? | y | ? |
| 3    | Client → Server | ? | ? | ? |

8. After the handshake, the client sends "Hello" (5 bytes). What are the sequence and acknowledgement numbers in the client's data segment and the server's ACK?

9. What is the purpose of the initial sequence number (ISN)? Why is it random rather than always starting at 0?

---

## Part D — UDP vs TCP

10. Implement a UDP **echo server** and **client**. Note the differences: no `accept()`, no `connect()` required, use `recvfrom()` and `sendto()`.

11. Send 10 messages from the UDP client. On a local loopback interface, all 10 arrive. Over an unreliable network, some may be lost. Modify the client to detect lost messages by: adding a sequence number to each message, waiting 0.5 seconds for each reply, retrying up to 3 times if no reply arrives.

12. Compare TCP and UDP for these applications:
    - Video streaming (YouTube)
    - Online gaming (position updates 60/s)
    - File transfer
    - DNS lookup

---

## Part E — Protocol Design

13. Design a simple binary protocol for sending messages over a TCP stream. The protocol must handle:
    - Messages of variable length (0–65535 bytes)
    - A message type identifier (1 byte)
    - Reliable delivery (TCP handles this)

    Define the header format (which fields, how many bytes each).

14. Implement `send_message(sock, msg_type, data)` and `recv_message(sock)` using your protocol. Why is it important to keep reading until you have all expected bytes (using a loop) rather than assuming one `recv()` call returns a complete message?

15. Why does TCP need framing (your protocol) while UDP does not?

---

## Rubric

| Part | Points |
|---|---|
| A TCP echo (3 questions) | 20 |
| B multi-client (3 questions) | 24 |
| C handshake trace | 20 |
| D UDP (3 questions) | 22 |
| E protocol design | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1+2 — TCP echo server and client</summary>

```python
# Server
import socket, threading

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 9000))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)
        if data: conn.sendall(data)
        conn.close()

# Client
import socket

def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 9000))
    s.sendall(b'Hello, server!')
    response = s.recv(1024)
    print(response.decode())
    s.close()
```

SO_REUSEADDR allows binding to a port that is in TIME_WAIT state from a previous connection. Without it, you get "Address already in use" for ~60 seconds after the server closes.
</details>

<details>
<summary>Part E.14 — protocol framing</summary>

```python
import struct

# Header: [msg_type: 1B][length: 2B] = 3 bytes total
HEADER_FMT = '!BH'   # big-endian: unsigned byte + unsigned short

def send_message(sock, msg_type, data):
    if isinstance(data, str): data = data.encode()
    header = struct.pack(HEADER_FMT, msg_type, len(data))
    sock.sendall(header + data)

def recv_exact(sock, n):
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk: raise ConnectionError("Connection closed")
        buf += chunk
    return buf

def recv_message(sock):
    header = recv_exact(sock, 3)
    msg_type, length = struct.unpack(HEADER_FMT, header)
    data = recv_exact(sock, length)
    return msg_type, data
```

TCP is a byte stream — `recv(1024)` may return 1 byte or 500 bytes regardless of how much was sent. You must loop until you have the exact bytes you need.

UDP sends and receives whole datagrams — one `sendto()` = one `recvfrom()` (or the datagram is lost entirely). No partial datagrams.
</details>
