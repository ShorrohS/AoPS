# Module 8.4 — Application Layer: DNS and HTTP

---

## The Problem

> TCP gives you a reliable byte stream between two ports.
> But no one navigates to `172.217.14.238:443`.
> People navigate to `google.com`.
>
> And once you have a connection, how do you ask for a specific resource?
> How does a single IP address serve thousands of different websites?
>
> These are application-layer problems:
> **DNS** translates names to addresses,
> **HTTP** defines how to request and serve resources.

---

## The Story

### DNS: The Phone Book of the Internet

In the early ARPANET, there were fewer than 1,000 machines. A single file — `HOSTS.TXT` — maintained at Stanford Research Institute listed every machine and its address. Administrators emailed updates; the file was downloaded regularly. As the ARPANET grew, this system became untenable.

**Paul Mockapetris** designed the Domain Name System (DNS) in 1983 (RFC 882/883). The key innovation: a distributed, hierarchical, delegated database. No single server holds all names. Instead, authority for each zone is delegated to nameservers — Google is responsible for `google.com`, Amazon for `amazon.com`, and so on. The root servers (13 groups, lettered A–M) sit at the top and delegate to top-level domain (TLD) servers (`.com`, `.org`, `.uk`), which delegate to domain nameservers.

DNS became operational in 1985. Today it handles trillions of queries per day — every web request, every email, every API call begins with a DNS lookup.

### HTTP: The Protocol That Built the Web

Tim Berners-Lee designed HTTP at CERN in 1989 (Module 7.5). HTTP/1.1 (RFC 2616, 1997) is still the most widely deployed version. HTTP/2 (2015) improved performance with multiplexing. HTTP/3 (2022) runs over QUIC instead of TCP.

The web as we know it — every website, web app, REST API, and web service — is built on HTTP.

---

## The Concept

### DNS Hierarchy

```
                    . (root)
                   /   |   \
                .com  .org  .uk
               /    \
           google  amazon
           /    \
         www    mail
```

**Types of DNS servers:**
- **Root nameservers**: 13 groups (a–m.root-servers.net), replicated globally via anycast. Know the TLD servers.
- **TLD nameservers**: operated by registries (Verisign for `.com`). Know authoritative nameservers for each domain.
- **Authoritative nameservers**: operated by domain owners (or their DNS provider). Hold actual DNS records.
- **Recursive resolvers**: operated by ISPs or public DNS (8.8.8.8, 1.1.1.1). Cache results and perform the full lookup on behalf of clients.

### DNS Resolution Process

When you type `www.google.com` in a browser:

1. **Local cache check**: browser checks its own DNS cache. Found? Done (sub-millisecond).
2. **OS resolver cache**: OS checks its cache and `/etc/hosts`. Found? Done.
3. **Recursive resolver** (e.g., `8.8.8.8`): OS sends query to configured DNS server.
4. **Root query**: resolver asks a root server for `.com` TLD server address.
5. **TLD query**: resolver asks `.com` TLD server for `google.com` nameserver address.
6. **Authoritative query**: resolver asks Google's nameserver for `www.google.com`.
7. **Answer**: authoritative server returns `A` record: `172.217.14.238`.
8. **Cache**: resolver caches the result for TTL (e.g., 300 seconds).
9. **Return**: resolver returns the IP to the client.

A cold lookup (nothing cached) typically takes 50–200ms. Subsequent lookups hit the cache: < 1ms.

### DNS Record Types

| Type | Purpose | Example |
|---|---|---|
| `A` | IPv4 address | `www.example.com → 93.184.216.34` |
| `AAAA` | IPv6 address | `www → 2606:2800:220:1:248:1893:25c8:1946` |
| `CNAME` | Alias (canonical name) | `blog.example.com → example.com` |
| `MX` | Mail server, with priority | `example.com → mail.example.com (priority 10)` |
| `NS` | Authoritative nameserver | `example.com → ns1.example.com` |
| `TXT` | Arbitrary text | SPF, DKIM, domain verification |
| `SOA` | Start of Authority | Zone metadata, serial number |
| `PTR` | Reverse lookup (IP → name) | `34.216.184.93.in-addr.arpa → www.example.com` |

### HTTP/1.1 Request-Response

A complete HTTP/1.1 exchange (from Module 7.5, extended):

**Request:**
```
GET /search?q=dns HTTP/1.1
Host: www.google.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: text/html,application/xhtml+xml
Accept-Language: en-US,en;q=0.9
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: SID=abc123; HSID=xyz789
```

**Response:**
```
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: gzip
Content-Length: 12453
Cache-Control: private, max-age=0
Set-Cookie: NID=204=...; expires=...; path=/; domain=.google.com; HttpOnly
Transfer-Encoding: chunked
```

### HTTP Status Codes

| Range | Meaning | Key codes |
|---|---|---|
| 1xx | Informational | 100 Continue, 101 Switching Protocols |
| 2xx | Success | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirection | 301 Moved Permanently, 302 Found, 304 Not Modified |
| 4xx | Client error | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests |
| 5xx | Server error | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable |

### HTTP Methods

| Method | Purpose | Body? | Safe? | Idempotent? |
|---|---|---|---|---|
| GET | Retrieve resource | No | Yes | Yes |
| POST | Create / submit | Yes | No | No |
| PUT | Replace resource | Yes | No | Yes |
| PATCH | Partial update | Yes | No | No |
| DELETE | Delete resource | No | No | Yes |
| HEAD | GET without body | No | Yes | Yes |
| OPTIONS | List allowed methods | No | Yes | Yes |

**Safe**: does not modify state. **Idempotent**: calling multiple times has the same effect as calling once.

### HTTP Caching

```
Cache-Control: max-age=3600          # cache for 1 hour
Cache-Control: no-cache              # must revalidate before using cache
Cache-Control: no-store              # never cache (passwords, bank data)
ETag: "abc123"                       # content fingerprint
If-None-Match: "abc123"              # conditional GET: only send if changed
Last-Modified: Wed, 10 Sep 2026 ...
If-Modified-Since: Wed, 10 Sep 2026  # conditional GET: only send if newer
```

A `304 Not Modified` response tells the browser: "use your cached copy — nothing changed." This saves bandwidth and dramatically speeds up page loads.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — DNS Resolver Walk**
- Type a domain name (e.g., `www.github.com`)
- Watch the resolution chain: root → TLD → authoritative → answer
- See the TTL countdown for cached entries

**Tool 2 — HTTP Request Builder**
- Select method (GET, POST, PUT, DELETE)
- Set headers, path, and body
- See the raw HTTP request and response
- Try different status codes: 200, 404, 301, 304

**Tool 3 — Cache Behaviour**
- Request the same resource twice
- First request: full response, cache headers set
- Second request: `If-None-Match` sent, 304 returned — no body transmitted

---

## Going Deeper

**DNSSEC**: DNS was designed with no authentication — any resolver could return fake records (DNS cache poisoning). DNSSEC adds cryptographic signatures to DNS records. A root key signs TLD keys, TLD keys sign domain keys — a chain of trust. However, DNSSEC deployment has been slow and partial; DNS-over-HTTPS (DoH) and DNS-over-TLS (DoT) are the more widely deployed modern solutions, encrypting DNS traffic to prevent eavesdropping and tampering.

**HTTP/2**: solves HTTP/1.1's head-of-line blocking problem. In HTTP/1.1, responses on a keep-alive connection are serialised — a slow response blocks all subsequent responses. HTTP/2 multiplexes multiple streams over one TCP connection. Each request/response is a stream; streams are independent. Also adds: header compression (HPACK), server push (unsolicited resources), and binary framing (more efficient than text).

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Trace a full DNS resolution for `api.github.com` listing every server queried, decode a raw HTTP response (given as text), identify caching headers and calculate when a resource expires, and explain what happens when a CNAME chain creates a loop.
