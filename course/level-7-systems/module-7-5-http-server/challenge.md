# Challenge 7.5 — Building a Tiny HTTP Server

**Type:** Implementation + trace + extension  
**Estimated time:** 50–60 minutes  
**Tools needed:** Python

---

## Part A — HTTP Request Parsing

Given this raw HTTP request as bytes:

```
POST /api/users HTTP/1.1\r\n
Host: localhost:8080\r\n
Content-Type: application/json\r\n
Content-Length: 27\r\n
Authorization: Bearer abc123\r\n
\r\n
{"name":"Alice","age":30}
```

1. Parse this request into a dict with keys: `method`, `path`, `version`, `headers` (dict), `body` (string). Show your `parse_request` function.

2. What is the significance of the blank line `\r\n\r\n`? What does the `Content-Length` header tell the server?

3. The server receives data in chunks (TCP is a byte stream). Write a loop that reads until it has received the complete request (headers + body), using `Content-Length` to know when the body is complete.

---

## Part B — Router Implementation

4. Implement a router that maps `(method, path_pattern)` → handler function. Support:
   - Exact matches: `GET /health`
   - Path parameters: `GET /users/{id}` — capture the `{id}` value

```python
router = Router()

@router.route("GET", "/health")
def health(req): ...

@router.route("GET", "/users/{id}")
def get_user(req, id): ...

@router.route("POST", "/users")
def create_user(req): ...
```

5. Implement `Router.dispatch(request)` that finds the matching route, extracts path parameters, and calls the handler.

6. What HTTP status code should be returned if:
   - No route matches the path at all?
   - The path matches but the method is wrong?

---

## Part C — Static File Server

7. Implement a static file handler that:
   - Serves files from a `./static/` directory
   - Sets correct `Content-Type` using the file extension
   - Returns 404 if the file doesn't exist
   - Prevents directory traversal (e.g., `/../../etc/passwd`)

8. Add **gzip compression**: if the request has `Accept-Encoding: gzip` and the file is larger than 1 KB, compress the response body and add `Content-Encoding: gzip`.

```python
import gzip

def maybe_gzip(body, request_headers):
    if 'gzip' in request_headers.get('accept-encoding', ''):
        if len(body) > 1024:
            return gzip.compress(body), {'Content-Encoding': 'gzip'}
    return body, {}
```

---

## Part D — HTTP/1.1 Features

9. Implement **keep-alive**: after serving a response, instead of closing the connection, wait for the next request on the same socket. Use the `Connection` header to determine whether to keep alive.

10. Implement a `/time` route that returns the current UTC time as JSON: `{"time": "2026-09-10T22:00:00Z", "timestamp": 1757523600}`.

11. Implement **rate limiting**: allow at most 100 requests per minute per IP address. Return HTTP 429 Too Many Requests with a `Retry-After: 60` header when exceeded. Use an in-memory dict: `{ip: [timestamps...]}`.

---

## Part E — Full Request Trace

Trace the complete lifecycle of this HTTP request through your server:
`GET /static/hello.txt HTTP/1.1\r\nHost: localhost:8080\r\n\r\n`

12. List every step from `server.accept()` to the final `conn.close()`:
    - Receive raw bytes
    - Parse request
    - Router lookup
    - File system access
    - Build response
    - Send response
    - Decision: close or keep-alive?

13. What is the minimum number of system calls (socket operations) to handle this request?

---

## Rubric

| Part | Points |
|---|---|
| A request parsing | 20 |
| B router | 22 |
| C static file server | 22 |
| D HTTP/1.1 features | 22 |
| E full trace | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part B.4 — Router implementation</summary>

```python
import re

class Router:
    def __init__(self):
        self._routes = []

    def route(self, method, pattern):
        def decorator(fn):
            regex = re.sub(r'\{(\w+)\}', r'(?P<\1>[^/]+)', pattern) + '$'
            self._routes.append((method, re.compile(regex), fn))
            return fn
        return decorator

    def dispatch(self, req):
        for method, regex, fn in self._routes:
            if req['method'] != method: continue
            m = regex.match(req['path'])
            if m:
                return fn(req, **m.groupdict())
        # Check if path matches but method doesn't
        for _, regex, _ in self._routes:
            if regex.match(req['path']):
                return build_response(405, {}, b'Method Not Allowed')
        return build_response(404, {}, b'Not Found')
```
</details>

<details>
<summary>Part D.11 — rate limiter</summary>

```python
import time
from collections import defaultdict

rate_limit = defaultdict(list)
LIMIT = 100
WINDOW = 60

def check_rate_limit(ip):
    now = time.time()
    # Keep only timestamps within the last 60 seconds
    rate_limit[ip] = [t for t in rate_limit[ip] if now - t < WINDOW]
    if len(rate_limit[ip]) >= LIMIT:
        return False   # rate limited
    rate_limit[ip].append(now)
    return True

# In request handler:
ip = addr[0]
if not check_rate_limit(ip):
    return build_response(429, {'Retry-After': '60'}, b'Too Many Requests')
```
</details>
