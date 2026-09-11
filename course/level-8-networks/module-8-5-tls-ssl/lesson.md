# Module 8.5 — TLS/SSL from First Principles

---

## The Problem

> HTTP sends all data in plaintext.
> Any router between your laptop and the server can read your password,
> your bank balance, your private messages.
>
> Three security properties are needed:
> 1. **Confidentiality** — only sender and recipient can read the data
> 2. **Integrity** — data cannot be modified in transit without detection
> 3. **Authentication** — you are really talking to google.com, not an impostor
>
> TLS (Transport Layer Security) provides all three.
> It is the protocol behind the padlock icon in your browser.

---

## The Story

### From SSL to TLS

Netscape Communications invented **SSL** (Secure Sockets Layer) in 1994 to secure e-commerce on the early web. Taher Elgamal was the primary designer. SSL 2.0 was the first public release; SSL 3.0 (1996) fixed critical vulnerabilities.

The IETF standardised **TLS 1.0** (1999) based on SSL 3.0. TLS 1.2 (2008) remains widely deployed. **TLS 1.3** (2018) was a major redesign — removing obsolete cryptography (RC4, MD5, SHA-1, RSA key exchange, DH < 1024 bits), reducing handshake latency from 2 RTTs to 1 RTT, and achieving **0-RTT** (zero round-trip) for session resumption.

As of 2024: TLS 1.3 is used by ~70% of HTTPS connections. TLS 1.2 handles most of the rest. TLS 1.0 and 1.1 are deprecated.

---

## The Concept

### The Cryptographic Building Blocks

**Symmetric encryption**: one key, used for both encryption and decryption. Fast. Problems: key distribution (how do you securely share the key?). Examples: **AES-256-GCM** (the dominant cipher in TLS 1.3).

**Asymmetric encryption (public-key cryptography)**: two mathematically related keys — a public key anyone can know, and a private key only you know. Data encrypted with the public key can only be decrypted with the private key. Slow (1000× slower than AES for bulk data). Examples: **RSA**, **ECDH** (Elliptic Curve Diffie-Hellman).

**Hash functions**: one-way transformation. Given input, produces a fixed-size digest. Computationally infeasible to reverse or find two inputs with the same digest. Examples: **SHA-256**, **SHA-384**.

**MACs (Message Authentication Codes)**: like a hash but keyed. Only someone with the key can compute or verify a MAC. Proves both integrity and authenticity. Example: **HMAC-SHA256**.

**Digital signatures**: a private key signs data; anyone with the public key can verify it was signed by the private key holder. Used in certificates to prove identity.

### The TLS 1.3 Handshake

TLS 1.3 completes the handshake in **one round trip** (1-RTT):

```
Client                              Server
  |                                   |
  |── ClientHello ──────────────────>|
  |   (supported cipher suites,       |
  |    key share: ECDH public key,    |
  |    random nonce)                  |
  |                                   |
  |<──────────── ServerHello ─────────|
  |   (chosen cipher suite,           |
  |    key share: server ECDH key,    |
  |    random nonce)                  |
  |<────────── {Certificate} ─────────|
  |   (server's X.509 certificate)    |
  |<────── {CertificateVerify} ───────|
  |   (signature over handshake hash) |
  |<──────────── {Finished} ──────────|
  |   (HMAC over handshake transcript)|
  |                                   |
  |── {Finished} ─────────────────── >|
  |── {Application Data} ───────────>|  ← encrypted traffic begins
  |<── {Application Data} ────────────|
```

`{}` indicates the message is **encrypted** with handshake keys derived during the handshake.

### Key Exchange — ECDH

**Elliptic Curve Diffie-Hellman** allows two parties to agree on a shared secret over an insecure channel without ever transmitting the secret:

1. Both agree on a public curve and generator point G
2. Client chooses random private key `a`, sends public key `A = a×G`
3. Server chooses random private key `b`, sends public key `B = b×G`
4. Client computes shared secret: `S = a×B = a×b×G`
5. Server computes: `S = b×A = b×a×G`
6. Both have `S = a×b×G` — the shared secret — without it ever being transmitted

An eavesdropper sees `A` and `B` but cannot compute `S` without solving the **elliptic curve discrete logarithm problem** — computationally infeasible for 256-bit curves.

The shared secret is then used to derive symmetric keys for encrypting the actual data (AES-256-GCM in TLS 1.3).

### Certificates and the PKI

Authentication answers: "Is the server I'm talking to really `google.com`?" Without it, an attacker could intercept the connection and use their own keys (man-in-the-middle attack).

A **X.509 certificate** binds a public key to an identity:
```
Subject: CN=www.google.com, O=Google LLC, C=US
Issuer: CN=GTS CA 1C3, O=Google Trust Services LLC
Validity: Not Before: Aug 19 2026, Not After: Nov 11 2026
Public Key: [ECDSA P-256 public key]
Subject Alternative Names: www.google.com, *.google.com
Signature: [signed by GTS CA 1C3]
```

The certificate is signed by a **Certificate Authority (CA)**. Your browser trusts a pre-installed set of ~150 root CAs (Mozilla, Google, Apple, Microsoft maintain lists). The chain of trust:

```
Root CA (trusted by browser, self-signed)
   ↓ signs
Intermediate CA certificate
   ↓ signs
Server certificate (www.google.com)
```

The browser verifies the signature chain up to a trusted root. If valid, and the domain in the certificate matches the URL, authentication succeeds.

### After the Handshake — Record Protocol

All application data is encrypted using the symmetric key established during the handshake:

```
TLS Record:
[content type (1B)] [version (2B)] [length (2B)] [encrypted payload + auth tag]
```

**AES-256-GCM** provides both encryption and authentication in one operation:
- Encrypts data with AES-256 in Galois/Counter Mode
- Produces a 128-bit authentication tag
- Any modification to the ciphertext invalidates the tag — detected immediately

The **sequence number** is included in the authentication (as "additional data"), preventing replay attacks (copying a valid record and sending it again).

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — TLS 1.3 Handshake Trace**
- Animated step-by-step handshake between a browser and server
- See each message's content (cipher suite, key shares, certificate)
- Watch the key derivation: master secret → handshake keys → application keys

**Tool 2 — ECDH Key Exchange**
- Two parties (Alice and Bob) exchange ECDH public keys
- Watch the shared secret computation on both sides
- Verify both parties arrive at the same secret
- Confirm an eavesdropper (Eve) cannot compute it from the public keys alone

**Tool 3 — Certificate Chain**
- A server certificate signed by an intermediate CA signed by a root CA
- Walk the chain: verify each signature, check validity period and domain name
- Observe what happens when one certificate in the chain is expired or untrusted

---

## Going Deeper

**Perfect Forward Secrecy (PFS)**: TLS 1.3 mandates ECDHE (ephemeral) key exchange. "Ephemeral" means new ECDH keys are generated for every session — the private keys are discarded after use. Consequence: even if the server's long-term private key is compromised in the future, an attacker who recorded past traffic cannot decrypt it (they'd need the ephemeral private key, which no longer exists). TLS 1.2 with RSA key exchange did NOT have PFS — compromising the server key could decrypt all past sessions.

**Certificate Transparency (CT)**: a Google-led initiative requiring all publicly-trusted certificates to be logged in public, append-only CT logs. Any certificate for a domain can be audited. This prevents CAs from issuing fraudulent certificates undetected. Browser vendors now require CT compliance for certificates to be trusted.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Explain why an eavesdropper who captures a TLS 1.3 session cannot decrypt it even if they later obtain the server's private key, trace the certificate chain for a real website describing each step of verification, identify what "TLS_AES_128_GCM_SHA256" means (break down the cipher suite name), and describe a man-in-the-middle attack on a connection without TLS.
