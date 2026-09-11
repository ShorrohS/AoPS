# Challenge 6.4 — Trees: BST, AVL, Red-Black

**Type:** Build + trace + implementation + reasoning  
**Estimated time:** 50–60 minutes  
**Tools needed:** pen and paper + Python

---

## Part A — BST Construction and Search

Insert the keys `[8, 3, 10, 1, 6, 9, 14, 4, 7]` into an empty BST in that order.

1. Draw the resulting BST. Verify the BST property: for every node, all left-subtree keys < node key < all right-subtree keys.

2. Trace search for key **7**: list every node visited and the comparison at each step.

3. Trace search for key **11** (not present): list every node visited until you reach a null child.

4. Perform an **in-order traversal** of your tree. What is the output? Why does in-order traversal always produce a sorted sequence from a BST?

---

## Part B — Worst Case BST

5. Insert the keys `[1, 2, 3, 4, 5, 6]` into an empty BST. Draw the result. What is the height? Why is this O(n)?

6. Insert the same six keys in an order that produces the most balanced possible BST. What order minimises height? Draw the result and state the height.

7. What does this demonstrate about BST performance guarantees vs AVL/red-black trees?

---

## Part C — AVL Rotation

Insert `[30, 20, 40, 10, 25, 35, 50, 5]` into an empty AVL tree.

8. After each insertion, compute the balance factor of each node. Show which insertions trigger a rotation.

9. Identify the rotation type (LL, RR, LR, RL) and draw the tree **before and after** the rotation.

10. What is the height of the final AVL tree? Compare to an unbalanced BST with the same keys.

---

## Part D — Tree Traversals

Given the BST from Part A:

11. Write iterative (non-recursive) implementations of in-order, pre-order, and post-order traversal using an explicit stack. No recursion allowed.

12. Write level-order (BFS) traversal using a queue. What is the output for your tree?

13. Given only the **pre-order** and **in-order** traversals of a BST, reconstruct the original tree. Demonstrate with: pre-order = `[8, 3, 1, 6, 4, 7, 10, 9, 14]`, in-order = `[1, 3, 4, 6, 7, 8, 9, 10, 14]`.

---

## Part E — BST as Sorted Map

14. Implement `BST.range_query(lo, hi)` that returns all keys k where `lo ≤ k ≤ hi` in sorted order. What is the time complexity? (O(log n + k) where k = number of results)

15. Why does a BST support range queries efficiently but a hash table does not?

16. A `sorted()` call on a Python list of n elements is O(n log n). If you need to insert elements one at a time and periodically query the k smallest elements, why might a BST be better than sorting the list each time?

---

## Rubric

| Part | Points |
|---|---|
| A BST construction | 24 |
| B worst case | 18 |
| C AVL rotation | 24 |
| D traversals | 22 |
| E sorted map | 12 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.4 — in-order traversal</summary>

In-order (left → root → right) visits: 1, 3, 4, 6, 7, 8, 9, 10, 14. Sorted! Reason: for any node x, all left-subtree nodes < x < all right-subtree nodes. In-order visits left subtree first (all smaller), then x, then right subtree (all larger) — recursively producing sorted order.
</details>

<details>
<summary>Part D.11 — iterative in-order</summary>

```python
def inorder_iterative(root):
    result, stack = [], []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.key)
        curr = curr.right
    return result
```

Pre-order iterative: push root; while stack: node=pop, visit, push right then left (right first so left is processed first).

Post-order iterative: use two stacks, or push root; while stack: pop to result_stack, push left then right; then reverse result_stack.
</details>

<details>
<summary>Part D.13 — reconstruct from pre+in</summary>

Pre-order first element = root = 8.
Find 8 in in-order: position 5. Left of 8 in in-order: [1,3,4,6,7] = left subtree. Right: [9,10,14] = right subtree.

Left subtree pre-order (next 5 elements): [3,1,6,4,7]. Recurse: root=3, in-order left of 3=[1], right=[4,6,7].

Continuing recursively reproduces the original tree.
</details>

<details>
<summary>Part E.14 — range query</summary>

```python
def range_query(node, lo, hi, result):
    if node is None: return
    if node.key > lo:
        range_query(node.left, lo, hi, result)
    if lo <= node.key <= hi:
        result.append(node.key)
    if node.key < hi:
        range_query(node.right, lo, hi, result)
```

O(log n) to find the first element in range, O(k) to collect k results = O(log n + k) total.
</details>
