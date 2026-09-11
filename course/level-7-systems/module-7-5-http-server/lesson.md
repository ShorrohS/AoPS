# Module 7.5 — Building a Tiny HTTP Server

---

## The Problem

> Every website you visit is served by an HTTP server.
> nginx, Apache, Express, Django, Flask — they all do the same core job:
> listen on a port, accept TCP connections, parse HTTP requests, return HTTP responses.
>
> When you understand how a tiny HTTP server works from the socket layer up,
> every web framework becomes transparent.
> You understand what Flask's `@app.route` is doing underneath.
> You understand what "middleware" means mechanically.
> You understand why HTTP/1.1 keep-alive matters for performance.

---

## The Story

### HTTP Was Designed on a Napkin

Tim Berners-Lee invented HTTP at CERN in 1989. The original HTTP/0.9 was extraordinarily simple: one command (`GET /path`) over a TCP connection, response is the file content, connection closes. No headers, no status codes, no response format.

HTTP/1.0 (1996) added headers, status codes (200, 404, etc.), and support for content types — enabling images, not just text. Each request required a new TCP connection.

HTTP/1.1 (1997, still dominant) added keep-alive (reuse connections for multiple requests), chunked transfer encoding, host headers (enabling virtual hosting — multiple websites on one IP), and caching directives. It is the protocol powering the majority of the web today.

HTTP/2 (2015) added multiplexing (multiple requests per connection, no head-of-line blocking), header compression, and server push. HTTP/3 (2022) runs over QUIC instead of TCP.

A working understanding of HTTP/1.1 is sufficient to understand everything built on top of it.

---

## The Concept

### HTTP Request Format

An HTTP/1.1 request is plain text over a TCP connection:

```
GET /index.html HTTP/1.1\r\n
Host: www.example.com\r\n
User-Agent: Mozilla/5.0\r\n
Accept: text/html\r\n
\r\n
```

Structure:
- **Request line**: `METHOD PATH HTTP/VERSION`
- **Headers**: `Name: Value` pairs, each ending `\r\n`
- **Blank line**: `\r\n` marks end of headers
- **Optional body**: for POST/PUT requests (e.g., form data, JSON)

### HTTP Response Format

```
HTTP/1.1 200 OK\r\n
Content-Type: text/html; charset=utf-8\r\n
Content-Length: 138\r\n
Connection: keep-alive\r\n
\r\n
<html>...</html>
```

Structure:
- **Status line**: `HTTP/VERSION STATUS_CODE REASON_PHRASE`
- **Headers**: content type, length, caching, cookies, etc.
- **Blank line**
- **Body**: the actual content

### Parsing an HTTP Request

```python
def parse_request(raw: bytes) -> dict:
    text  = raw.decode('utf-8', errors='replace')
    lines = text.split('\r\n')

    # Request line
    method, path, version = lines[0].split(' ', 2)

    # Headers
    headers = {}
    i = 1
    while i < len(lines) and lines[i] != '':
        key, _, value = lines[i].partition(': ')
        headers[key.lower()] = value
        i += 1

    # Body (everything after the blank line)
    body = '\r\n'.join(lines[i+1:]) if i+1 < len(lines) else ''

    return {
        'method':  method,
        'path':    path,
        'version': version,
        'headers': headers,
        'body':    body,
    }
```

### Building the Server — Step by Step

```python
import socket, os, mimetypes
from pathlib import Path

STATIC_ROOT = Path('./static')

STATUS = {200: 'OK', 404: 'Not Found', 405: 'Method Not Allowed',
          500: 'Internal Server Error'}

def build_response(status, headers, body=b''):
    header_lines = f"HTTP/1.1 {status} {STATUS[status]}\r\n"
    for k, v in headers.items():
        header_lines += f"{k}: {v}\r\n"
    return header_lines.encode() + b"\r\n" + body

def handle_request(raw):
    try:
        req = parse_request(raw)
    except Exception:
        return build_response(400, {'Content-Length': 0})

    if req['method'] not in ('GET', 'HEAD'):
        return build_response(405, {'Allow': 'GET, HEAD', 'Content-Length': 0})

    # Resolve path (security: prevent directory traversal)
    rel_path = req['path'].lstrip('/')
    if not rel_path: rel_path = 'index.html'
    file_path = (STATIC_ROOT / rel_path).resolve()

    # Security: ensure file is inside STATIC_ROOT
    if not str(file_path).startswith(str(STATIC_ROOT.resolve())):
        return build_response(403, {'Content-Length': 0})

    if not file_path.exists():
        return build_response(404, {'Content-Type': 'text/plain',
                                    'Content-Length': str(len(b'Not Found'))}, b'Not Found')

    body = b'' if req['method'] == 'HEAD' else file_path.read_bytes()
    mime = mimetypes.guess_type(str(file_path))[0] or 'application/octet-stream'
    return build_response(200, {
        'Content-Type': mime,
        'Content-Length': str(len(body)),
        'Connection': 'close',
    }, body)

def run_server(host='', port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Serving on http://localhost:{port}")
    while True:
        conn, addr = server.accept()
        raw = b''
        while b'\r\n\r\n' not in raw:
            chunk = conn.recv(4096)
            if not chunk: break
            raw += chunk
        response = handle_request(raw)
        conn.sendall(response)
        conn.close()
```

### Adding a Router

A router maps URL patterns to handler functions — this is exactly what Flask's `@app.route` does:

```python
routes = {}

def route(path):
    def decorator(fn):
        routes[path] = fn
        return fn
    return decorator

@route('/hello')
def hello(req):
    body = b'<h1>Hello, World!</h1>'
    return build_response(200, {'Content-Type': 'text/html',
                                'Content-Length': str(len(body))}, body)

@route('/echo')
def echo(req):
    body = req['body'].encode()
    return build_response(200, {'Content-Type': 'text/plain',
                                'Content-Length': str(len(body))}, body)

def handle_request(raw):
    req = parse_request(raw)
    handler = routes.get(req['path'])
    if handler:
        return handler(req)
    # ... fall through to static file serving
```

### Middleware

A middleware is a function that wraps a handler — adding behaviour before and after:

```python
def logging_middleware(handler):
    def wrapper(req):
        print(f"→ {req['method']} {req['path']}")
        response = handler(req)
        status = response[:15].decode()
        print(f"← {status}")
        return response
    return wrapper

# Apply to all routes:
for path, fn in routes.items():
    routes[path] = logging_middleware(fn)
```

This is the exact pattern used by Express.js middleware, Django middleware, and Flask `before_request` hooks.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — HTTP Request Parser**
- Paste a raw HTTP request
- Watch it get parsed: method, path, version, each header, body
- See what happens with malformed requests

**Tool 2 — Request-Response Trace**
- Send simulated requests to the virtual server
- Watch the server look up the route, call the handler, and build the response
- Try 200, 404, 405 responses

**Tool 3 — Middleware Chain**
- Add middleware: logging, authentication check, rate limiting
- See each middleware called in order before the handler
- Observe how middleware can short-circuit and return early (e.g., 401 if not authenticated)

---

## Going Deeper

**Keep-alive connections**: HTTP/1.1 by default keeps TCP connections open for multiple requests (`Connection: keep-alive`). Without this, every image, stylesheet, and script requires a new TCP handshake — dramatically slowing page loads. A production server must handle multiple requests per connection efficiently.

**WebSockets**: HTTP can be "upgraded" to a persistent, bidirectional connection using the WebSocket protocol. After the upgrade handshake (an HTTP request with `Upgrade: websocket`), the connection becomes a raw TCP stream with a simple framing protocol. Used for real-time chat, live dashboards, collaborative editing, and multiplayer games.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Extend the server with a `/time` route that returns the current time, add a `Content-Encoding: gzip` response for files > 1KB, identify and fix the directory traversal vulnerability (what if path = `../../etc/passwd`?), and trace a full HTTP/1.1 request-response cycle for `GET /images/logo.png HTTP/1.1`.
