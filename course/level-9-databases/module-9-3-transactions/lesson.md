# Module 9.3 — Transactions, ACID, and Isolation

---

## The Problem

> Two people simultaneously book the last seat on a flight.
> Both checks show the seat is available.
> Both bookings succeed.
> Two passengers arrive, one seat exists.
>
> A bank transfers £100 from account A to account B.
> The system crashes after deducting from A but before adding to B.
> £100 vanishes.
>
> These are **concurrency** and **durability** problems in databases.
> Transactions and ACID properties exist specifically to prevent them.

---

## The Story

### The Problem of Bank Transfers

The canonical example of why transactions exist: a funds transfer. Conceptually: `UPDATE accounts SET balance = balance - 100 WHERE id = 1` followed by `UPDATE accounts SET balance = balance + 100 WHERE id = 2`. These are two separate operations. Without transactions, a crash between them leaves the database in an inconsistent state — money lost.

Jim Gray formalised transaction processing in the 1970s while at IBM working on System R. His 1981 paper "The Transaction Concept: Virtues and Limitations" defined the ACID properties. Gray received the Turing Award in 1998 for his work on transaction processing and database systems.

The ideas from Gray's work are now universal: every relational database, most NoSQL databases, and many distributed systems implement some form of transactional guarantees.

---

## The Concept

### ACID Properties

**Atomicity**: a transaction either completes entirely or has no effect. No partial execution. "All or nothing."

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;   -- both updates persist
-- If crash occurs before COMMIT: neither update persists (rollback)
```

**Consistency**: a transaction takes the database from one valid state to another. All integrity constraints (foreign keys, check constraints, unique constraints) hold after every committed transaction.

**Isolation**: concurrent transactions behave as if they executed serially. One transaction's intermediate state is invisible to others.

**Durability**: once committed, a transaction's effects survive crashes. Achieved via **write-ahead logging (WAL)**: changes are written to a durable log before being applied to data pages.

### The Write-Ahead Log (WAL)

Before any data page is modified, the change is recorded in the WAL (also called redo log in MySQL, journal in SQLite):

```
LSN 1001: BEGIN TRANSACTION txn#42
LSN 1002: UPDATE accounts SET balance=900 WHERE id=1  [old=1000, new=900]
LSN 1003: UPDATE accounts SET balance=200 WHERE id=2  [old=100,  new=200]
LSN 1004: COMMIT txn#42
```

On crash recovery:
- WAL entries with COMMIT are **replayed** (redo): any changes not yet on disk are re-applied
- WAL entries without COMMIT are **rolled back** (undo): any partial changes are reversed

The WAL is append-only — the fastest possible write pattern on both HDDs and SSDs.

### Isolation Levels and Concurrency Anomalies

Perfect isolation is expensive — it requires full serialisation. Most databases offer weaker isolation levels for better performance:

**Read Uncommitted**: a transaction can read uncommitted changes from other transactions.
→ Allows **dirty reads**: read data that another transaction will roll back.

**Read Committed** (PostgreSQL default): only committed data is visible.
→ Prevents dirty reads. Allows **non-repeatable reads**: re-reading the same row yields different results if another transaction committed between reads.

**Repeatable Read** (MySQL InnoDB default): all reads within a transaction see a consistent snapshot from transaction start.
→ Prevents dirty reads and non-repeatable reads. Allows **phantom reads**: a range query executed twice may return different rows if another transaction inserted rows matching the range.

**Serializable**: full isolation — transactions execute as if sequential.
→ Prevents all anomalies. Most expensive. Uses locks or MVCC + predicate locking.

### MVCC — Multi-Version Concurrency Control

Most modern databases (PostgreSQL, Oracle, MySQL InnoDB) use **MVCC** rather than locks for read isolation:

- Each row has a **transaction ID range** indicating which transactions can see it
- When a transaction starts, it gets a snapshot timestamp
- Reads see the latest version of each row **committed before the transaction's snapshot**
- Writes create a **new version** of the row rather than modifying in-place
- Old versions are cleaned up by a background process (VACUUM in PostgreSQL)

Benefits:
- Readers never block writers, writers never block readers
- Long-running queries don't stall updates

Costs:
- Extra storage for multiple versions
- Vacuum/cleanup overhead

### Deadlocks in Databases

```sql
-- Session 1                  -- Session 2
BEGIN;                         BEGIN;
UPDATE accounts                UPDATE accounts
  SET bal=bal-100              SET bal=bal-100
  WHERE id=1;                  WHERE id=2;   -- acquires lock on row 2
                               UPDATE accounts
                                 SET bal=bal+100
                                 WHERE id=1; -- waits for lock on row 1
UPDATE accounts
  SET bal=bal+100
  WHERE id=2;  -- waits for    -- DEADLOCK
  lock on row 2
```

The database detects deadlocks (cycle in the wait-for graph) and aborts one transaction with an error. The application should retry the aborted transaction.

**Lock ordering** prevents deadlocks: always acquire locks in the same order. Many applications implement this by sorting the rows to update by primary key before executing.

### Two-Phase Commit (2PC)

For distributed transactions spanning multiple databases:

**Phase 1 (Prepare)**: coordinator asks all participants "are you ready to commit?" Each participant flushes its changes to WAL and responds "yes/no."

**Phase 2 (Commit/Abort)**: if all said yes, coordinator sends COMMIT to all. If any said no, sends ROLLBACK to all.

2PC provides distributed ACID but is blocking: if the coordinator crashes after phase 1, participants hold locks indefinitely. Modern distributed databases (Google Spanner, CockroachDB) use Paxos/Raft for fault-tolerant distributed transactions.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — ACID Demonstration**
- A bank transfer that crashes halfway
- Without transaction: see the inconsistent state
- With transaction + WAL: crash recovery restores consistency

**Tool 2 — Isolation Levels**
- Two concurrent transactions running simultaneously
- Switch between Read Committed, Repeatable Read, Serializable
- See what each transaction can read at each step

**Tool 3 — Deadlock Visualiser**
- Two transactions acquiring locks in opposite order
- Watch the wait-for graph build into a cycle
- See the database detect the deadlock and abort one transaction

---

## Going Deeper

**Serializable Snapshot Isolation (SSI)**: PostgreSQL's serializable isolation uses SSI — detecting serialisation conflicts at commit time rather than blocking immediately. This allows much higher concurrency than traditional 2PL (two-phase locking) while still guaranteeing full serializability. The key insight: track read-write conflicts between transactions and abort any that could produce a non-serializable outcome.

**BASE vs ACID**: many NoSQL databases (Cassandra, DynamoDB, MongoDB) relax ACID for higher availability and performance. BASE (Basically Available, Soft state, Eventually consistent) allows replicas to temporarily diverge — reads may return stale data, but the system converges to consistency eventually. Understanding the CAP theorem (Consistency, Availability, Partition tolerance: choose two) is essential for distributed database design.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Write a transaction for a hotel room booking that prevents double-booking using SELECT FOR UPDATE, trace the WAL entries for a 3-statement transaction, identify which isolation level would prevent the phantom read in a given scenario, and explain why you cannot detect a deadlock with a simple timeout (what other issues does timeout cause?).
