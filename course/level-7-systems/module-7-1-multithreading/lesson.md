# Module 7.1 — Multithreading and Concurrency

---

## The Problem

> A web server must handle 10,000 simultaneous connections.
> A video game must update physics, render frames, and play audio simultaneously.
> A data pipeline must download, process, and store data in parallel.
>
> A single-threaded program does one thing at a time.
> The world does not.
>
> **Concurrency** is about dealing with multiple things happening at the same time.
> **Parallelism** is about doing multiple things at the same time.
> They are related but distinct — and confusing them leads to bugs that are nearly impossible to reproduce.

---

## The Story

### From Sequential to Concurrent

The earliest computers were strictly sequential: one program ran, finished, then the next ran. Time-sharing (Module 4.3) created the *illusion* of concurrency by rapidly context-switching between processes.

**Threads** (1960s–70s) took this further: lightweight "processes" sharing the same address space. Switching between threads in the same process is cheaper than between processes (no address space switch). Threads share heap memory, file descriptors, and global variables — enabling communication at the cost of coordination complexity.

**Dijkstra** formalised many of the synchronisation problems in the 1960s: the mutual exclusion problem (1965), semaphores (1965), the dining philosophers problem (1965). These problems, posed 60 years ago, are still the foundational examples taught in every operating systems course.

Intel's **Hyper-Threading** (2002) put two logical CPU cores on one physical core, enabling true thread-level parallelism within a single chip. Modern CPUs have 8–32 physical cores, each with hardware multithreading. Writing correct parallel code became a survival skill for systems programmers.

---

## The Concept

### Processes vs Threads

| Property | Process | Thread |
|---|---|---|
| Address space | Own (isolated) | Shared with other threads |
| Memory | Own heap, stack, data | Own stack; shared heap, data |
| Communication | IPC (pipes, sockets, shared mem) | Direct memory access |
| Context switch cost | High (TLB flush, page table switch) | Low (same address space) |
| Failure isolation | Crash doesn't affect others | Crash kills all threads in process |
| Creation cost | High (`fork` + `exec`) | Low (1–10 µs) |

In Python:
```python
import threading

def worker(n):
    print(f"Thread {n} running")
    # compute something
    print(f"Thread {n} done")

threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
for t in threads: t.start()
for t in threads: t.join()   # wait for all threads to finish
```

### The Race Condition

The fundamental problem of concurrent programs:

```python
counter = 0   # shared variable

def increment():
    global counter
    for _ in range(100_000):
        counter += 1   # NOT atomic!

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)
t1.start(); t2.start()
t1.join(); t2.join()
print(counter)   # Expected: 200,000. Actual: some random smaller number!
```

`counter += 1` compiles to three machine instructions:
1. LOAD counter into register
2. ADD 1 to register
3. STORE register back to counter

If two threads interleave between any of these steps, one thread's increment is lost. This is a **race condition** — the outcome depends on timing, making it non-deterministic and nearly impossible to reproduce consistently.

### Critical Sections and Mutual Exclusion

A **critical section** is any code that accesses a shared resource and must not be executed by two threads simultaneously.

**Mutex (Mutual Exclusion Lock)**: only one thread can hold the lock at a time. Others block until the holder releases it.

```python
import threading

counter = 0
lock = threading.Lock()

def safe_increment():
    global counter
    for _ in range(100_000):
        with lock:           # acquire on entry, release on exit
            counter += 1    # critical section — only one thread at a time

t1 = threading.Thread(target=safe_increment)
t2 = threading.Thread(target=safe_increment)
t1.start(); t2.start()
t1.join(); t2.join()
print(counter)   # Always 200,000
```

The `with lock:` context manager ensures the lock is always released, even if an exception occurs.

### Thread Safety Patterns

**Immutable objects**: if shared data never changes, no synchronisation is needed. Pure functions and immutable data structures are inherently thread-safe.

**Thread-local storage**: data stored per-thread, not shared. Each thread has its own copy.

```python
import threading
local_data = threading.local()

def worker():
    local_data.x = threading.current_thread().name   # each thread writes its own
    print(local_data.x)   # each thread reads its own, no conflict
```

**Producer-Consumer pattern**: producers add work to a queue; consumers take from it.

```python
from queue import Queue

q = Queue(maxsize=10)

def producer():
    for i in range(20):
        q.put(i)           # blocks if queue full
    q.put(None)            # sentinel: no more work

def consumer():
    while True:
        item = q.get()     # blocks if queue empty
        if item is None: break
        process(item)

threading.Thread(target=producer).start()
threading.Thread(target=consumer).start()
```

Python's `queue.Queue` is thread-safe — all operations are internally synchronised.

### The GIL and True Parallelism in Python

Python's **Global Interpreter Lock (GIL)** prevents multiple threads from executing Python bytecode simultaneously. This means:
- Python threads are concurrent (interleaved) but not truly parallel for CPU-bound code
- For CPU-bound parallelism, use `multiprocessing` (separate processes, no GIL)
- For I/O-bound tasks (network, disk), threads work fine — the GIL is released during I/O

```python
# For CPU-bound parallel work:
from multiprocessing import Pool

def compute(x):
    return x * x

with Pool(processes=4) as pool:
    results = pool.map(compute, range(1_000_000))
```

### Async/Await — Cooperative Concurrency

For I/O-bound tasks with thousands of concurrent operations, threads waste memory (each thread has a ~8 MB stack). **Asyncio** uses a single thread with cooperative multitasking:

```python
import asyncio

async def fetch(url):
    # When awaiting I/O, control returns to the event loop
    await asyncio.sleep(1)   # simulate network request
    return f"data from {url}"

async def main():
    # Launch 1000 concurrent "requests" with one thread
    tasks = [fetch(f"http://example.com/{i}") for i in range(1000)]
    results = await asyncio.gather(*tasks)

asyncio.run(main())
```

One thread handles thousands of concurrent I/O operations by switching between them when each is waiting. Memory: ~1 KB per coroutine vs ~8 MB per thread.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Race Condition Demonstrator**
- Two threads incrementing a shared counter simultaneously (no lock)
- Watch the lost updates happen — final value is less than expected
- Enable the lock — result is always correct
- See the interleaving that causes lost updates

**Tool 2 — Thread State Visualiser**
- Multiple threads with blocked/running/waiting states
- Watch a context switch: one thread yields, another resumes
- See the mutex queue: threads waiting to acquire a lock

**Tool 3 — Producer-Consumer**
- A bounded buffer of 5 slots
- Producer and consumer threads run at different speeds
- Watch the buffer fill (producer blocks when full) and drain (consumer blocks when empty)

---

## Going Deeper

**Memory model and visibility**: on a multi-core CPU, each core has its own cache. One thread writing to `counter` may not be immediately visible to another thread reading it — the value might be in the writing thread's cache only. CPU memory models (x86's TSO, ARM's weakly-ordered model) define exactly what ordering guarantees exist. The C++ `std::atomic` and Java `volatile` keyword ensure proper memory visibility without full mutex overhead.

**Lock-free data structures**: using CPU atomic compare-and-swap (CAS) instructions to update shared data without acquiring a lock. Lock-free queues, stacks, and hash tables can outperform lock-based ones under high contention. But they are extremely difficult to write correctly — even experts make mistakes. See Module 6.2 (Going Deeper) for Michael-Scott lock-free queue.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Identify the race condition in a given code snippet, add a mutex to fix it, implement a thread-safe bounded counter using a Lock, design a producer-consumer system with 2 producers and 3 consumers, and explain why Python's GIL does not protect against race conditions.
