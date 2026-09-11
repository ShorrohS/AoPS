# Challenge 9.4 — Building a Toy SQL Engine

**Type:** Implementation + trace + extension  
**Estimated time:** 50–60 minutes  
**Tools needed:** Python

---

## Part A — Extend the Parser

The toy engine from the lesson supports: `SELECT`, `INSERT`, `WHERE` (single condition).

1. Extend the tokeniser to recognise `ORDER`, `BY`, `ASC`, `DESC`, `LIMIT`, `GROUP`, `COUNT`, `AND`, `OR`.

2. Extend `parse_select` to handle:
   ```sql
   SELECT name, age FROM users WHERE city = 'NYC' ORDER BY age DESC LIMIT 5
   ```
   What new fields does the AST need?

3. Extend the executor to apply `ORDER BY` and `LIMIT`. Show the implementation and trace on the query above given a table with 8 rows.

---

## Part B — Add GROUP BY and COUNT

4. Extend the engine to support:
   ```sql
   SELECT city, COUNT(*) as cnt FROM users GROUP BY city
   ```
   
   Implement `execute_group_by(table, group_col, agg_col)`. Show the result for a 10-row users table.

5. What data structure do you use to accumulate groups? Write the implementation.

6. Extend to support `HAVING COUNT(*) > 2` (filter after aggregation).

---

## Part C — Hash Join

7. Implement a nested loop JOIN (O(n×m)):
   ```sql
   SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id
   ```

8. Implement a **hash join** (O(n+m)):
   - Phase 1 (build): hash the smaller table on the join key
   - Phase 2 (probe): scan the larger table; for each row, look up in the hash table

9. For a users table with 1000 rows and an orders table with 50,000 rows:
   - Nested loop: how many comparisons?
   - Hash join: how many hash table operations?

---

## Part D — Execution Trace

Trace every step of executing:
```sql
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.city = 'London'
GROUP BY u.name
ORDER BY order_count DESC
LIMIT 3
```

10. List the execution plan stages in order. For each stage, describe its input and output.

11. If `users` has 500 rows and `orders` has 5000 rows, how many rows pass through each stage?

---

## Part E — Query Optimiser

12. The toy engine executes: `SELECT * FROM users WHERE city = 'London' AND age > 25`. Without indexes, it scans every row. What is the naive execution order?

13. If there is an index on `city` but not `age`, propose an optimised execution plan: use the index for the `city` filter, then apply the `age` filter to the reduced result set.

14. Implement a simple `has_index(table_name, column)` check and modify the executor to use an index scan when available instead of a full table scan.

15. What is the **rule-based optimiser** vs the **cost-based optimiser**? Give one example of a query transformation that is always safe to apply (rule-based) and one that requires statistics (cost-based).

---

## Rubric

| Part | Points |
|---|---|
| A parser extension | 22 |
| B GROUP BY and COUNT | 22 |
| C hash join | 22 |
| D execution trace | 18 |
| E query optimiser | 16 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.3 — ORDER BY + LIMIT</summary>

```python
def execute_select(db, ast):
    table = db.get_table(ast['table'])
    results = []
    for row in table.scan():
        if evaluate_condition(row, ast.get('where')):
            cols = ast['columns']
            results.append({c: row.get(c) for c in cols} if cols != ['*'] else dict(row))

    if ast.get('order_by'):
        col, direction = ast['order_by']
        results.sort(key=lambda r: (r.get(col) is None, r.get(col)),
                     reverse=(direction.upper() == 'DESC'))

    if ast.get('limit') is not None:
        results = results[:ast['limit']]

    return results
```
</details>

<details>
<summary>Part B.5 — GROUP BY implementation</summary>

```python
from collections import defaultdict

def execute_group_by(table, group_col, agg_col='*', having_count=None):
    groups = defaultdict(list)
    for row in table.scan():
        key = row.get(group_col)
        groups[key].append(row)

    results = []
    for key, rows in groups.items():
        count = len(rows)
        if having_count is None or count > having_count:
            results.append({group_col: key, 'count': count})

    return results
```
</details>

<details>
<summary>Part C.8 — hash join</summary>

```python
def hash_join(left_rows, right_rows, left_key, right_key):
    # Phase 1: build hash table from smaller (left) table
    ht = defaultdict(list)
    for row in left_rows:
        ht[row[left_key]].append(row)

    # Phase 2: probe
    results = []
    for row in right_rows:
        for match in ht.get(row[right_key], []):
            results.append({**match, **row})

    return results
```

Nested loop: 1000 × 50,000 = 50,000,000 comparisons.
Hash join: 1000 inserts + 50,000 lookups = 51,000 operations. ~1000× fewer.
</details>
