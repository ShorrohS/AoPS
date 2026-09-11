# Challenge 7.2 — Mutexes, Semaphores, and Deadlocks

**Type:** Analysis + implementation + trace  
**Estimated time:** 45–55 minutes  
**Tools needed:** Python + pen and paper

---

## Part A — Deadlock Identification

```python
import threading, time

lock1 = threading.Lock()
lock2 = threading.Lock()
lock3 = threading.Lock()

def thread_A():
    with lock1:
        time.sleep(0.01)
        with lock2:           # waits for lock2
            with lock3: pass

def thread_B():
    with lock2:
        time.sleep(0.01)
        with lock3:           # waits for lock3
            with lock1: pass

def thread_C():
    with lock3:
        time.sleep(0.01)
        with lock1:           # waits for lock1
            with lock2: pass
```

1. Draw the **wait-for graph**: each thread is a node, draw an edge from T to L if T is waiting to acquire lock L, and from L to T if T holds lock L. Is there a cycle?

2. Describe the precise interleaving that causes deadlock: which thread acquires which lock in what order?

3. Fix the deadlock using **global lock ordering**: assign each lock a number (lock1=1, lock2=2, lock3=3) and always acquire locks in increasing order. Rewrite all three thread functions.

4. After applying lock ordering, can the three threads still run concurrently? Or does the fix serialise them?

---

## Part B — Semaphore as Resource Pool

5. Implement a **connection pool** using a semaphore: max 3 simultaneous database connections allowed. Write `acquire_connection()` and `release_connection()` functions. Include a context manager.

6. Launch 10 threads that each "use" a connection for 0.1 seconds. Verify using logging that at most 3 threads are in the critical section simultaneously.

7. What happens if a thread acquires a connection but raises an exception before releasing? How do you ensure the semaphore is always released? (Hint: `try/finally` or context manager)

---

## Part C — Condition Variable

8. Implement a **bounded buffer** (producer-consumer with a fixed-size buffer of 5) using a `threading.Condition`:
   - `put(item)`: wait if buffer full, add item, notify consumer
   - `get()`: wait if buffer empty, remove item, notify producer

```python
import threading

class BoundedBuffer:
    def __init__(self, capacity):
        self._buffer   = []
        self._capacity = capacity
        self._cond     = threading.Condition()

    def put(self, item): ...
    def get(self): ...
```

9. Why must the wait condition be checked in a `while` loop, not an `if`? What is a **spurious wakeup** and why does it occur?

10. What is the difference between `notify()` and `notify_all()`? In the bounded buffer, which is more correct to use after `put()` and why?

---

## Part D — Dining Philosophers

11. Implement the dining philosophers problem with **5 philosophers** and **5 forks** (each fork is a Lock). Without any fix, demonstrate that the following naive approach can deadlock:

```python
def philosopher(id, left_fork, right_fork):
    while True:
        left_fork.acquire()
        right_fork.acquire()    # may deadlock here
        eat()
        right_fork.release()
        left_fork.release()
        think()
```

12. Apply the **resource hierarchy fix**: philosopher i always picks up `fork[min(i, (i+1)%5)]` first. Show how this breaks the cycle for all 5 philosophers.

13. Trace the first 3 meal cycles for philosopher 0 with the fix applied. Which forks does each philosopher acquire in what order?

---

## Part E — Livelock

14. Construct a scenario where two threads enter a **livelock** (both active, neither making progress). Use: both try to acquire the other's resource, detect they can't, back off, and retry — in perfect synchrony so they always back off simultaneously.

15. How does **randomised backoff** prevent livelock? What is the expected number of retries before one thread makes progress?

---

## Rubric

| Part | Points |
|---|---|
| A deadlock identification | 24 |
| B semaphore pool | 18 |
| C condition variable | 24 |
| D dining philosophers | 22 |
| E livelock | 12 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part B.5 — connection pool</summary>

```python
import threading, contextlib, time, logging

logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')
sem = threading.Semaphore(3)

@contextlib.contextmanager
def acquire_connection():
    sem.acquire()
    try:
        logging.info("Acquired connection")
        yield
    finally:
        sem.release()
        logging.info("Released connection")

def use_db():
    with acquire_connection():
        time.sleep(0.1)

threads = [threading.Thread(target=use_db) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
```
</details>

<details>
<summary>Part C.8 — BoundedBuffer</summary>

```python
class BoundedBuffer:
    def __init__(self, capacity):
        self._buffer   = []
        self._capacity = capacity
        self._cond     = threading.Condition()

    def put(self, item):
        with self._cond:
            while len(self._buffer) >= self._capacity:
                self._cond.wait()         # releases lock, waits
            self._buffer.append(item)
            self._cond.notify_all()       # wake consumers

    def get(self):
        with self._cond:
            while not self._buffer:
                self._cond.wait()
            item = self._buffer.pop(0)
            self._cond.notify_all()       # wake producers
            return item
```

While loop: spurious wakeups occur when the OS wakes a waiting thread for reasons unrelated to the notify. Without the while check, the thread would proceed even if the condition is still false. With while, it rechecks and waits again if needed.
</details>

<details>
<summary>Part D.12 — resource hierarchy fix</summary>

With 5 philosophers (0–4) and 5 forks (0–4), fork[i] = fork between philosophers i and (i+1)%5:
- Philosopher i picks up fork min(i, (i+1)%5) first, then max.
- Philosopher 4: min(4,0)=0, max=4. Picks fork 0 first.
- Others: min(i,i+1)=i. Pick fork i first, then i+1.

Philosopher 4 now picks up fork 0 first (same as philosopher 0 wants). If philosopher 0 holds fork 0, philosopher 4 must wait — breaking the cycle. Not all can hold their "first" fork simultaneously.
</details>
