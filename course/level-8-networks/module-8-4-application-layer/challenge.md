# Challenge 8.4 — Application Layer: DNS and HTTP

**Type:** Trace + analysis + implementation  
**Estimated time:** 40–50 minutes  
**Tools needed:** pen and paper

---

## Part A — DNS Resolution Walk

Trace the complete DNS resolution for `api.github.com` from a client with no cached entries. The client's recursive resolver is `8.8.8.8`.

1. List every query and response in order:
   - Who queries whom?
   - What is the exact query (qname, qtype)?
   - What does the response contain?
   
   There should be at least 4 distinct queries before the final answer arrives.

2. The final answer is an **A record** with TTL=60. The recursive resolver caches it. If the same query is made again 30 seconds later, how many network queries occur? After 90 seconds?

3. `api.github.com` may return a **CNAME** before the final A record. What does a CNAME mean? How many DNS lookups does a CNAME chain of length 3 require?

4. DNS uses **UDP port 53** for most queries. Under what circumstances does DNS fall back to TCP? What is the size limit that triggers this?

---

## Part B — HTTP Response Decoding

Given this raw HTTP response (headers only):

```
HTTP/1.1 301 Moved Permanently
Location: https://www.example.com/page
Content-Type: text/html; charset=utf-8
Content-Length: 153
Cache-Control: max-age=3600
Date: Wed, 10 Sep 2026 22:00:00 GMT
Server: nginx/1.24.0
X-Request-ID: abc-123-def
Connection: keep-alive
```

5. What HTTP status code is this? What action should the client take?

6. What does `max-age=3600` mean? When can the cached response be used without re-validation?

7. If the client sends `GET /page HTTP/1.1\r\nIf-Modified-Since: Wed, 10 Sep 2026 20:00:00 GMT\r\n\r\n` and the page hasn't changed, what status code and response body does the server return?

8. The `Connection: keep-alive` header means the server will not close the TCP connection after this response. What are the performance implications for loading a web page with 20 sub-resources (images, CSS, JS)?

---

## Part C — HTTP Methods and REST Semantics

For a `/users/{id}` endpoint:

9. Which HTTP method is **idempotent but not safe**? What does this mean practically?

10. Difference between `PUT /users/42` and `PATCH /users/42`: if the user has fields `{name, email, role, created_at}` and you send `{name: "Alice"}`:
    - What does the PUT version do to the other fields?
    - What does the PATCH version do?

11. A client sends `DELETE /users/42` twice. The first returns 204 No Content. What should the second return: 404 Not Found or 204 again? Justify with idempotency reasoning.

---

## Part D — DNS Cache Poisoning

12. Describe a **DNS cache poisoning** attack: how does an attacker trick a recursive resolver into caching a false IP address for `bank.com`?

13. How does **DNSSEC** prevent this attack? What does it add to DNS responses?

14. **DNS-over-HTTPS (DoH)** sends DNS queries inside HTTPS connections. What eavesdropping attack does this prevent that DNSSEC does not?

---

## Part E — HTTP Caching Challenge

A web page at `https://news.example.com/article/42` has:
- `Cache-Control: no-cache` (must revalidate, but can cache)
- `ETag: "v7-2026-09-10"`

15. A client loads the page and caches it. On the next visit, what request does the browser send? Show the exact request headers used for conditional revalidation.

16. Server responds with `304 Not Modified`. What does the browser do? What is transmitted over the wire vs served from cache?

17. Difference between `no-cache` and `no-store`: when would you use each? Give one real-world example for each.

---

## Rubric

| Part | Points |
|---|---|
| A DNS walk | 24 |
| B HTTP response | 20 |
| C HTTP methods | 18 |
| D DNS security | 18 |
| E caching | 20 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1 — DNS resolution trace</summary>

1. Client → 8.8.8.8: `api.github.com A?`
2. 8.8.8.8 → root server: `api.github.com A?` → Response: NS records for `.com` zone
3. 8.8.8.8 → .com TLD server: `api.github.com A?` → Response: NS records for `github.com`
4. 8.8.8.8 → github.com authoritative server: `api.github.com A?` → Response: A record (or CNAME)
5. 8.8.8.8 → Client: final A record answer

If CNAME is returned, additional A record lookups follow.
</details>

<details>
<summary>Part B.5–8</summary>

5. 301 Moved Permanently. Client should follow the Location header and make a new GET request to `https://www.example.com/page`. Future requests should go directly to the new URL.

6. max-age=3600: cache this response for 3600 seconds (1 hour). Response can be served from cache without revalidation until 1 hour from the Date header.

7. 304 Not Modified. No body — zero bytes of content transmitted. Browser uses its cached copy.

8. With keep-alive, the browser can pipeline 20 resource requests over the same TCP connection (or a small pool of connections). Without keep-alive, each resource requires a separate TCP handshake (~1 RTT each). For 20 resources × 50ms RTT = 1 second saved just in connection setup.
</details>

<details>
<summary>Part C.10 — PUT vs PATCH</summary>

PUT is a **replace** operation: sends the complete new representation. `PUT {name: "Alice"}` would set name=Alice and remove/null all other fields.

PATCH is a **partial update**: only the specified fields are changed. `PATCH {name: "Alice"}` updates the name field only; email, role, created_at are unchanged.
</details>

<details>
<summary>Part E.15 — conditional request</summary>

```
GET /article/42 HTTP/1.1
Host: news.example.com
If-None-Match: "v7-2026-09-10"
```

Server checks: does the current ETag match? If yes → 304 Not Modified, no body. Browser serves cached copy. Only headers transmitted (~200 bytes vs potentially hundreds of KB for the full page).
</details>
