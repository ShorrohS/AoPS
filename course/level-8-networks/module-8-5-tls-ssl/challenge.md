# Challenge 8.5 — TLS/SSL from First Principles

**Type:** Reasoning + calculation + trace  
**Estimated time:** 40–50 minutes  
**Tools needed:** pen and paper

---

## Part A — TLS 1.3 Handshake

1. Draw the TLS 1.3 handshake message sequence between Client and Server. Label each message and indicate which are encrypted (use `{}` notation).

2. The handshake takes **1 RTT** in TLS 1.3. In TLS 1.2, it took **2 RTTs**. For a user with 100ms RTT to a server, calculate the total connection setup time:
   - DNS: 1 RTT
   - TCP handshake: 1 RTT
   - TLS 1.2: 2 RTTs
   - TLS 1.3: 1 RTT
   
   How many milliseconds does TLS 1.3 save per new connection vs TLS 1.2?

3. TLS 1.3 supports **0-RTT** for session resumption. What data can be sent in 0-RTT? What security property is sacrificed compared to full 1-RTT? (Hint: replay attacks)

---

## Part B — ECDH Key Exchange

Alice and Bob agree on the elliptic curve P-256 and a generator point G.

Alice chooses private key `a = 7`.  
Bob chooses private key `b = 11`.  

For illustration, use a simplified discrete logarithm over integers mod 23 (not a real elliptic curve): `G = 5`, multiplication is repeated addition mod 23.

4. Calculate Alice's public key: `A = a × G mod 23 = 7 × 5 mod 23`.
5. Calculate Bob's public key: `B = b × G mod 23 = 11 × 5 mod 23`.
6. Calculate the shared secret: Alice computes `a × B mod 23`, Bob computes `b × A mod 23`. Do they get the same value?
7. Eve observes A=12 and B=9 and knows G=5, p=23. She must find `a` such that `a×5 ≡ 12 (mod 23)`. This is the **discrete logarithm problem**. Try all values a=1..22. How long did it take? Why is this infeasible for 256-bit curves?

---

## Part C — Certificate Chain

8. A certificate chain for `www.bank.com`:
   - Root CA: "Global Root CA" (self-signed, in browser's trust store)
   - Intermediate CA: "Bank SSL CA" (signed by Global Root CA)
   - End-entity cert: "www.bank.com" (signed by Bank SSL CA)
   
   List the verification steps the browser performs, in order.

9. The end-entity certificate has `NotBefore: 2025-01-01` and `NotAfter: 2026-01-01`. Today is 2026-09-10. What does the browser do?

10. You access `https://www.bank.com` but receive a certificate for `www.b4nk.com`. What does the browser show? What attack does this prevent against?

---

## Part D — Perfect Forward Secrecy

11. In TLS 1.2 with **RSA key exchange** (no PFS): the client encrypts the session key with the server's public key. The server decrypts with its private key. If an attacker records the TLS session and later obtains the server's private key, can they decrypt the recorded session? Why?

12. In TLS 1.3 with **ECDHE** (ephemeral key exchange): the server generates a fresh ECDH key pair for every session and discards the private key after the session. If an attacker records the session and later obtains the server's long-term private key, can they decrypt it? Why not?

13. This property is called **Perfect Forward Secrecy**. What is the cost of PFS in terms of server computation compared to static RSA key exchange?

---

## Part E — Cipher Suite Decoding

14. Decode this TLS 1.3 cipher suite string: `TLS_AES_256_GCM_SHA384`. What does each component mean?

15. TLS 1.3 removed many cipher suites that were in TLS 1.2. Name two removed components and why each was removed (e.g., RC4, MD5, RSA key exchange, CBC mode).

---

## Rubric

| Part | Points |
|---|---|
| A TLS 1.3 handshake | 22 |
| B ECDH key exchange | 24 |
| C certificate chain | 22 |
| D perfect forward secrecy | 22 |
| E cipher suite | 10 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part B.4–6 — ECDH numbers</summary>

A = 7 × 5 mod 23 = 35 mod 23 = **12**  
B = 11 × 5 mod 23 = 55 mod 23 = **9**  
Alice: 7 × 9 mod 23 = 63 mod 23 = **17**  
Bob:  11 × 12 mod 23 = 132 mod 23 = 132 - 5×23 = 132 - 115 = **17** ✓  
Shared secret = 17.
</details>

<details>
<summary>Part C.8 — certificate verification steps</summary>

1. Check the end-entity cert's signature using the Intermediate CA's public key → valid?
2. Check the Intermediate CA cert's signature using the Root CA's public key → valid?
3. Check the Root CA cert is in the browser's trusted store → yes?
4. Check each cert's validity period (NotBefore ≤ today ≤ NotAfter)
5. Check no cert has been revoked (OCSP or CRL check)
6. Check the Subject Alternative Name (SAN) in the end-entity cert matches the URL hostname
</details>

<details>
<summary>Part D.11–12 — PFS explanation</summary>

RSA key exchange (no PFS): the pre-master secret is encrypted with the server's long-term RSA public key. A recorded session + compromised private key → decrypt the pre-master secret → derive all session keys → decrypt all past traffic. Yes, they can.

ECDHE (PFS): the session key is derived from ephemeral ECDH values that are deleted after the session. The long-term private key is used only for authentication (signing), not for key derivation. An attacker who compromises the long-term key later cannot compute the ephemeral ECDH private key that was already deleted. Past sessions remain secure.
</details>

<details>
<summary>Part E.14 — cipher suite</summary>

TLS_AES_256_GCM_SHA384:
- TLS: protocol
- AES_256: symmetric cipher, AES with 256-bit key
- GCM: mode of operation (Galois/Counter Mode — provides both encryption and authentication)
- SHA384: hash function used in the HKDF key derivation function (384-bit output)
</details>
