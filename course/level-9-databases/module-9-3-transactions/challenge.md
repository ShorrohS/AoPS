# Challenge 9.3 — Transactions, ACID, and Isolation

**Type:** SQL + trace + reasoning  
**Estimated time:** 45–55 minutes  
**Tools needed:** pen and paper

---

## Part A — ACID Properties

Classify each scenario and explain which ACID property it violates:

1. A bank transfer: `UPDATE accounts SET balance = balance - 100 WHERE id = 1`. The system crashes before `UPDATE accounts SET balance = balance + 100 WHERE id = 2` runs. Which property fails without transactions?

2. Two transactions read the same account balance simultaneously, both compute `new_balance = old_balance + interest`, and both write the new value. One update is lost. Which property does this violate?

3. A transaction adds 500 rows to an `orders` table. After `COMMIT`, the database crashes and restarts. The 500 rows are gone. Which property does this violate?

4. A foreign key constraint (`orders.customer_id` references `customers.id`) is violated by a transaction. The transaction commits anyway. Which property does this violate?

---

## Part B — Write-Ahead Log

A transaction performs these operations:

```
BEGIN
UPDATE products SET stock = stock - 1 WHERE id = 101  -- stock was 10, now 9
UPDATE orders SET status = 'processing' WHERE id = 5   -- was 'pending'
COMMIT
```

5. Write out the **WAL entries** this transaction would generate, including:
   - BEGIN marker
   - For each UPDATE: before-image, after-image, affected row
   - COMMIT marker

6. The system crashes after the COMMIT marker is written to the WAL but before the data pages are updated on disk. What happens during recovery? Does the transaction commit or roll back?

7. The system crashes after the first UPDATE is written to the WAL but before COMMIT. What happens during recovery?

---

## Part C — Isolation Levels

Two transactions run concurrently. Session A reads account balance; Session B updates it.

```
Time  Session A                           Session B
 1:   BEGIN                               BEGIN
 2:   SELECT balance FROM acct WHERE id=1  -- reads 1000
 3:                                       UPDATE acct SET balance=1200 WHERE id=1
 4:                                       COMMIT
 5:   SELECT balance FROM acct WHERE id=1  -- reads ?
 6:   COMMIT
```

8. At **Read Committed** isolation: what does Session A read at t=2 and t=5?

9. At **Repeatable Read** isolation: what does Session A read at t=5?

10. At **Serializable** isolation: can both transactions complete if Session A also writes (not just reads)?

11. Describe the **phantom read** anomaly. Which isolation level prevents it but is not prevented by Repeatable Read?

---

## Part D — Preventing Double-Booking

A hotel room booking system must prevent two users from booking the same room on the same night.

12. Write a transaction using `SELECT ... FOR UPDATE` that:
    - Checks if room 101 is available on 2026-09-15
    - If available, creates a booking
    - Ensures no other transaction can book the same room simultaneously

```sql
BEGIN;
-- Step 1: lock the availability row
-- Step 2: check if room is available
-- Step 3: if yes, insert booking
-- Step 4: update availability
COMMIT;
```

13. What isolation level is required for this to work correctly? Explain why Read Committed is insufficient.

14. If `SELECT FOR UPDATE` is not available, what alternative pessimistic locking mechanism could you use? Describe an optimistic locking alternative using a version counter.

---

## Part E — Two-Phase Commit

A distributed purchase spans two databases: the payment database (deduct $50) and the inventory database (decrement stock by 1).

15. Describe the **two-phase commit** protocol for this transaction. What happens if the payment database replies "ready" but the inventory database crashes before responding?

16. What is the **blocking problem** with 2PC? Under what conditions is a participant blocked indefinitely?

17. Modern databases like **CockroachDB** use Paxos consensus instead of 2PC for distributed transactions. What property does Paxos provide that makes it non-blocking?

---

## Rubric

| Part | Points |
|---|---|
| A ACID scenarios | 20 |
| B WAL trace | 22 |
| C isolation levels | 24 |
| D double-booking | 22 |
| E 2PC | 12 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part B.5 — WAL entries</summary>

```
LSN 1001: BEGIN txn#42
LSN 1002: UPDATE products id=101 [before: stock=10] [after: stock=9]
LSN 1003: UPDATE orders id=5 [before: status='pending'] [after: status='processing']
LSN 1004: COMMIT txn#42
```

6. Crash after COMMIT written: recovery replays LSNs 1002 and 1003 (redo). Transaction commits. Data pages updated. ✓

7. Crash after LSN 1002 but before COMMIT: no COMMIT in WAL. Recovery applies undo for LSN 1002 (stock back to 10). Transaction rolled back. ✓
</details>

<details>
<summary>Part C.8–9</summary>

8. Read Committed: t=2 reads 1000 (B hasn't committed). t=5 reads 1200 (B committed between t=2 and t=5). This is a **non-repeatable read**.

9. Repeatable Read: t=5 still reads 1000. The transaction's snapshot is taken at BEGIN (or first read). Changes committed by other transactions after the snapshot are invisible within this transaction.
</details>

<details>
<summary>Part D.12</summary>

```sql
BEGIN;
SELECT * FROM availability 
WHERE room_id = 101 AND date = '2026-09-15' AND available = true
FOR UPDATE;  -- locks the row; other transactions wait

-- application checks if row was found
-- if found:
INSERT INTO bookings (room_id, date, guest_id) VALUES (101, '2026-09-15', 99);
UPDATE availability SET available = false WHERE room_id = 101 AND date = '2026-09-15';
COMMIT;
```
</details>
