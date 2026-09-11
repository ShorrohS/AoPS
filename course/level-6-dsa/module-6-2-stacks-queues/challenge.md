# Challenge 6.2 — Stacks and Queues

**Type:** Implementation + trace + reasoning  
**Estimated time:** 45–55 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — Stack with Two Queues

Implement a stack using only two queues (FIFO structures). The stack must support `push(x)`, `pop()`, and `peek()` using only queue operations: `enqueue(x)`, `dequeue()`, `is_empty()`.

1. Implement `StackFromQueues`. You may make push O(1) and pop O(n), or push O(n) and pop O(1) — choose one approach and implement it.

2. Trace the following sequence on your implementation, showing the state of both queues after each operation:
   `push(1), push(2), push(3), pop(), push(4), peek(), pop()`

3. What is the amortised cost of n push + pop operations using your approach?

---

## Part B — Queue with Two Stacks

Implement a queue using only two stacks. The queue must support `enqueue(x)` and `dequeue()`.

4. Implement `QueueFromStacks`. Use the inbox/outbox pattern: enqueue pushes to inbox; dequeue pops from outbox (moving inbox to outbox if outbox is empty).

5. Trace: `enqueue(1), enqueue(2), enqueue(3), dequeue(), enqueue(4), dequeue(), dequeue()`

6. What is the amortised O(1) dequeue cost? Explain using the accounting method: each enqueue pays for its own future dequeue.

---

## Part C — Parentheses and RPN

7. Use a stack to check if each string has balanced brackets. Show the stack state after each character:
   - `"({[]})"` — balanced or not?
   - `"([)]"` — balanced or not?
   - `"((("` — balanced or not?

8. Evaluate these RPN (Reverse Polish Notation) expressions using a stack. Show the stack state after each token:
   - `"3 4 + 2 *"` → should give 14
   - `"5 1 2 + 4 * + 3 -"` → should give 14

9. Implement `eval_rpn(tokens)` that evaluates an RPN expression given as a list of strings.

---

## Part D — BFS Queue Trace

10. Run BFS starting from node A on this graph (adjacency list):
    ```
    A: [B, C]
    B: [A, D, E]
    C: [A, F]
    D: [B]
    E: [B, F]
    F: [C, E]
    ```
    Show the **queue state** after each dequeue step. List nodes in the order they are first visited.

11. BFS produces the shortest path (by hop count) from A to any node. Extract the shortest path from A to F by maintaining a `parent` dictionary alongside BFS.

12. What is the BFS discovery order if you use a **stack** instead of a queue? What algorithm does this implement?

---

## Part E — Monotonic Stack

13. Given array `[4, 1, 2, 3]`, use a monotonic stack to find the **next greater element** for each position. Show the stack state and result array after each element is processed.

14. Implement `next_greater(arr)` that returns an array where `result[i]` is the next element in `arr` that is greater than `arr[i]`, or -1 if none exists.

15. Why is the monotonic stack approach O(n) rather than O(n²)? Prove that each element is pushed and popped at most once.

---

## Rubric

| Part | Points |
|---|---|
| A stack from queues | 22 |
| B queue from stacks | 18 |
| C parentheses + RPN | 24 |
| D BFS queue trace | 22 |
| E monotonic stack | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A — Stack from Queues (push O(n))</summary>

```python
from collections import deque

class StackFromQueues:
    def __init__(self):
        self.q1 = deque()
        self.q2 = deque()

    def push(self, x):
        self.q2.append(x)           # push to empty q2
        while self.q1:              # move all q1 elements after new one
            self.q2.append(self.q1.popleft())
        self.q1, self.q2 = self.q2, self.q1  # q1 is now the stack

    def pop(self):   return self.q1.popleft()
    def peek(self):  return self.q1[0]
```
</details>

<details>
<summary>Part C.8 — RPN traces</summary>

"3 4 + 2 *":
- push 3: [3]
- push 4: [3, 4]
- +: pop 4,3 → push 7: [7]
- push 2: [7, 2]
- *: pop 2,7 → push 14: [14]
Result: 14 ✓

"5 1 2 + 4 * + 3 -":
- push 5: [5]
- push 1: [5,1]
- push 2: [5,1,2]
- +: [5,3]
- push 4: [5,3,4]
- *: [5,12]
- +: [17]
- push 3: [17,3]
- -: [14]
Result: 14 ✓
</details>

<details>
<summary>Part E.14 — next_greater</summary>

```python
def next_greater(arr):
    result = [-1] * len(arr)
    stack  = []   # stores indices
    for i, x in enumerate(arr):
        while stack and arr[stack[-1]] < x:
            idx = stack.pop()
            result[idx] = x
        stack.append(i)
    return result
```

O(n): each index is pushed exactly once and popped at most once. Total push + pop operations ≤ 2n.
</details>
