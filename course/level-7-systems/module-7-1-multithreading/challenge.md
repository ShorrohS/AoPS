# Challenge 7.1 — Multithreading and Concurrency

**Type:** Code analysis + implementation + reasoning  
**Estimated time:** 45–55 minutes  
**Tools needed:** Python + pen and paper

---

## Part A — Race Condition Identification

```python
import threading

balance = 1000

def withdraw(amount):
    global balance
    current = balance          # (1)
    if current >= amount:      # (2)
        balance = current - amount  # (3)

t1 = threading.Thread(target=withdraw, args=(700,))
t2 = threading.Thread(target=withdraw, args=(700,))
t1.start(); t2.start()
t1.join();  t2.join()
print(balance)
```

1. Identify the race condition. What is the problematic interleaving? Show the exact sequence of operations between t1 and t2 that results in `balance = 300` even though that should be impossible (both withdrawals of 700 from 1000 should not both succeed).

2. Why does the race condition only appear sometimes? What determines whether it manifests?

3. Fix the race condition using `threading.Lock()`. Write the corrected `withdraw` function.

4. Explain why Python's GIL does **not** prevent this race condition, even though it prevents true parallel execution.

---

## Part B — Thread-Safe Counter

5. Implement a `SafeCounter` class that can be safely incremented from multiple threads:

```python
class SafeCounter:
    def __init__(self, initial=0): ...
    def increment(self): ...       # thread-safe
    def get(self): ...             # thread-safe read
    def reset(self): ...           # thread-safe reset
```

6. Write a test: launch 100 threads, each calling `increment()` 1,000 times. Assert that the final count equals 100,000. Without a lock, what range of values might you observe?

7. An alternative to locking is using `threading.local()` for per-thread counters that are summed at the end. Implement this variant. What are the trade-offs vs a shared lock?

---

## Part C — Producer-Consumer

8. Implement a producer-consumer system:
   - One producer thread generates integers 0–99 and puts them in a bounded queue (max size 5)
   - Two consumer threads take items and compute their square
   - All results are collected in a shared list
   - Main thread waits for all items to be processed

```python
from queue import Queue
import threading

results = []
q = Queue(maxsize=5)

def producer(): ...
def consumer(): ...
```

9. What happens if the producer fills the queue and no consumer is running? What mechanism prevents this?

10. How do you signal consumers to stop when production is complete? (Hint: sentinel values)

---

## Part D — Deadlock Analysis

```python
import threading

lock_a = threading.Lock()
lock_b = threading.Lock()

def task_1():
    with lock_a:
        print("T1 acquired A")
        with lock_b:          # waits for B
            print("T1 done")

def task_2():
    with lock_b:
        print("T2 acquired B")
        with lock_a:          # waits for A
            print("T2 done")
```

11. When exactly does deadlock occur? Describe the precise interleaving.

12. Fix using **lock ordering**: always acquire `lock_a` before `lock_b`, in both functions.

13. Fix using **trylock with backoff**: use `lock.acquire(timeout=0.1)`. If acquiring the second lock fails, release the first and retry after a short sleep. Implement this.

14. Which fix is better in a production system? Why?

---

## Part E — asyncio vs Threads

15. Rewrite the following thread-based I/O-bound task using `asyncio`:

```python
# Thread version
import threading, time

def fetch(url):
    time.sleep(0.1)   # simulate network request
    return f"data from {url}"

threads = [threading.Thread(target=fetch, args=(f"url{i}",)) for i in range(100)]
for t in threads: t.start()
for t in threads: t.join()
```

16. For 100 simulated requests of 0.1s each: how long does the thread version take? How long does the asyncio version take? Explain the difference.

17. If the work inside `fetch` were CPU-bound instead of I/O-bound (e.g., computing a hash), would asyncio still help? Why or why not?

---

## Rubric

| Part | Points |
|---|---|
| A race condition | 24 |
| B SafeCounter | 18 |
| C producer-consumer | 22 |
| D deadlock | 22 |
| E asyncio | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A — race condition interleaving</summary>

t1 reads current=1000 (line 1)
t2 reads current=1000 (line 1)
t1 checks 1000 >= 700 (line 2) → True
t2 checks 1000 >= 700 (line 2) → True
t1 sets balance = 1000 - 700 = 300 (line 3)
t2 sets balance = 1000 - 700 = 300 (line 3)
Final: balance=300, but two withdrawals of 700 each "succeeded."
</details>

<details>
<summary>Part A.3 — fixed withdraw</summary>

```python
lock = threading.Lock()

def withdraw(amount):
    global balance
    with lock:
        if balance >= amount:
            balance -= amount
```
</details>

<details>
<summary>Part C.8 — producer-consumer</summary>

```python
from queue import Queue
import threading

results = []
results_lock = threading.Lock()
q = Queue(maxsize=5)

def producer():
    for i in range(100):
        q.put(i)       # blocks if queue full
    q.put(None)        # sentinel per consumer
    q.put(None)

def consumer():
    while True:
        item = q.get()   # blocks if empty
        if item is None: break
        with results_lock:
            results.append(item ** 2)
        q.task_done()

threads = [threading.Thread(target=consumer) for _ in range(2)]
prod = threading.Thread(target=producer)
for t in threads: t.start()
prod.start()
prod.join()
for t in threads: t.join()
assert len(results) == 100
```
</details>

<details>
<summary>Part E.15 — asyncio version</summary>

```python
import asyncio

async def fetch(url):
    await asyncio.sleep(0.1)    # non-blocking sleep
    return f"data from {url}"

async def main():
    tasks = [fetch(f"url{i}") for i in range(100)]
    results = await asyncio.gather(*tasks)
    return results

asyncio.run(main())
```

Threads: ~0.1s (all 100 run concurrently via GIL release during time.sleep). Asyncio: ~0.1s (all coroutines suspended at await, event loop runs other coroutines). Both take ~0.1s for I/O-bound. For CPU-bound: both ~10s because neither truly parallelises CPU work — use multiprocessing for that.
</details>
