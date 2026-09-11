# Module 7.2 — Mutexes, Semaphores, and Deadlocks

---

## The Problem

> Module 7.1 introduced race conditions and the basic mutex.
> But real concurrent systems have more complex coordination needs:
>
> - Allow up to N threads to access a resource simultaneously (database connection pool)
> - Signal that an event has occurred (producer notifies consumer)
> - Prevent a circular wait where threads block each other forever
>
> These needs require richer synchronisation primitives —
> and the coordination bugs they prevent are replaced by a new class of bugs
> that are often harder to detect: **deadlocks**, **livelocks**, and **starvation**.

---

## The Story

### Dijkstra's Semaphore

Edsger Dijkstra introduced the **semaphore** in his 1965 paper "Solution of a Problem in Concurrent Programming Control." He was solving the mutual exclusion problem: how can N processes share a resource safely?

A semaphore is an integer with two atomic operations:
- **P (proberen/wait)**: decrement, block if result is negative
- **V (verhogen/signal)**: increment, wake a blocked thread if any

Dijkstra was also the first to formally describe the **dining philosophers problem** (1965): five philosophers sit at a round table, each alternating between thinking and eating. To eat, a philosopher needs both the left and right fork. If all pick up their left fork simultaneously and wait for the right, they deadlock — a simple model of circular waiting.

This single thought experiment has driven 60 years of research into deadlock avoidance, lock ordering, and concurrent algorithm design.

---

## The Concept

### Mutex (Revisited)

A mutex is a binary semaphore with ownership semantics: only the thread that locked it can unlock it. Used for mutual exclusion — one thread in the critical section at a time.

```python
import threading
lock = threading.Lock()

with lock:              # acquire
    # critical section
    pass               # release on exit (even on exception)
```

**Reentrant mutex (RLock)**: a thread can acquire the same lock multiple times without deadlocking. Must release the same number of times.

```python
rlock = threading.RLock()
with rlock:
    with rlock:    # safe with RLock, deadlock with Lock
        pass
```

### Semaphores — Counting Synchronisation

A semaphore with initial value N allows up to N threads to be in the critical section simultaneously:

```python
sem = threading.Semaphore(3)   # allow 3 concurrent accesses

def access_database():
    with sem:          # acquire (blocks when count reaches 0)
        # use database connection (max 3 simultaneous)
        query_db()
    # release: another thread can now enter
```

**Binary semaphore** (initial=1): equivalent to a mutex, but any thread can release it — useful for signalling.

**Signalling with semaphores** — producer/consumer:
```python
filled = threading.Semaphore(0)   # how many items available to consume
empty  = threading.Semaphore(10)  # how many spaces available to produce
mutex  = threading.Semaphore(1)   # protect buffer

def producer():
    while True:
        item = produce()
        empty.acquire()    # wait for empty slot
        mutex.acquire()
        buffer.append(item)
        mutex.release()
        filled.release()   # signal: item is available

def consumer():
    while True:
        filled.acquire()   # wait for item
        mutex.acquire()
        item = buffer.pop()
        mutex.release()
        empty.release()    # signal: slot freed
        consume(item)
```

### Condition Variables

A condition variable allows threads to wait for a specific condition while atomically releasing a mutex:

```python
lock = threading.Lock()
condition = threading.Condition(lock)
buffer = []

def producer():
    while True:
        item = produce()
        with condition:
            buffer.append(item)
            condition.notify()   # wake one waiting consumer

def consumer():
    while True:
        with condition:
            while not buffer:    # spurious wakeup protection
                condition.wait() # release lock, block, re-acquire on wake
            item = buffer.pop(0)
        consume(item)
```

The key operations:
- `wait()`: atomically release lock + block thread + re-acquire lock on wake
- `notify()`: wake one waiting thread
- `notify_all()`: wake all waiting threads

### Deadlock — The Circular Wait

A deadlock occurs when:
1. Thread A holds lock L1 and waits for lock L2
2. Thread B holds lock L2 and waits for lock L1
3. Neither can proceed

```python
lock1 = threading.Lock()
lock2 = threading.Lock()

def thread_a():
    with lock1:              # acquires lock1
        with lock2: pass     # waits for lock2 → DEADLOCK if B holds it

def thread_b():
    with lock2:              # acquires lock2
        with lock1: pass     # waits for lock1 → DEADLOCK if A holds it
```

**The four conditions for deadlock** (Coffman, 1971):
1. **Mutual exclusion**: resources cannot be shared
2. **Hold and wait**: threads hold resources while waiting for more
3. **No preemption**: resources cannot be forcibly taken
4. **Circular wait**: a cycle of threads, each waiting for the next

Breaking any one condition prevents deadlock:

**Lock ordering** (break circular wait): always acquire locks in the same global order. If all threads acquire lock1 before lock2, circular wait is impossible:

```python
def thread_a():
    with lock1:
        with lock2: pass   # same order as thread_b

def thread_b():
    with lock1:            # both acquire lock1 first
        with lock2: pass
```

**Timeout with trylock** (break hold-and-wait):
```python
def safe_acquire(lock1, lock2, timeout=1.0):
    if lock1.acquire(timeout=timeout):
        if lock2.acquire(timeout=timeout):
            return True
        else:
            lock1.release()   # back off — try again later
    return False
```

### Livelock and Starvation

**Livelock**: threads keep responding to each other, constantly changing state, but making no progress. Like two people meeting in a hallway, each stepping aside in the same direction repeatedly.

**Starvation**: a thread never gets CPU time because other threads always have higher priority or are always preferred by the scheduler. A low-priority thread may wait indefinitely — not blocked, just never scheduled.

**Solution**: **aging** — gradually increase priority of waiting threads so every thread eventually gets scheduled.

### The Dining Philosophers — Solutions

**Resource hierarchy** (Dijkstra's solution): number forks 1–5. Each philosopher picks up the lower-numbered fork first. The philosopher who would create the cycle (the one who wants fork 5 then fork 1) picks fork 1 then fork 5 instead — no cycle possible.

**Arbitrator** (waiter solution): a central mutex (the "waiter") that philosophers must acquire before picking up any fork. Only one philosopher eats at a time — correct but serialised.

**Chandy/Misra** (1984): each fork has an owner. A hungry philosopher sends a "request" message. The fork owner sends the fork only if not eating; otherwise defers. Works for distributed systems.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Semaphore Pool**
- 5 threads, 2 semaphore permits (simulating 2 database connections)
- Watch threads queue up and acquire/release semaphore permits
- Observe at most 2 threads active at any time

**Tool 2 — Deadlock Simulator**
- Two threads acquiring two locks in opposite order
- Watch the deadlock form — both threads blocked, no progress
- Apply lock ordering fix — deadlock resolved

**Tool 3 — Dining Philosophers**
- 5 philosophers animated around a table
- Run without any solution — observe deadlock forming
- Enable the resource hierarchy solution — all philosophers eventually eat

---

## Going Deeper

**Read-write locks**: many operations are reads (multiple threads can read simultaneously) and only occasionally writes (exclusive access required). A `threading.RWLock` allows multiple concurrent readers OR one exclusive writer. This dramatically improves throughput for read-heavy workloads.

**Monitors**: a higher-level abstraction combining a mutex and condition variable into a single object. Java's `synchronized` keyword and `wait()`/`notify()` implement a monitor. Every Java object has an intrinsic monitor. Python's `threading.Condition` is effectively a monitor.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Identify the deadlock in a given lock acquisition sequence, fix it using lock ordering, implement a bounded buffer using condition variables with proper spurious wakeup handling, and trace the dining philosophers deadlock step by step with 5 philosophers showing exactly who holds and waits for what.
