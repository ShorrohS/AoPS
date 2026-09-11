# Challenge 9.1 — The Relational Model and SQL

**Type:** SQL writing + analysis + reasoning  
**Estimated time:** 50–60 minutes  
**Tools needed:** pen and paper (or a SQL sandbox)

---

## Setup — Schema

```sql
CREATE TABLE customers (
    id         INTEGER PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    city       VARCHAR(100),
    email      VARCHAR(255) UNIQUE
);

CREATE TABLE products (
    id         INTEGER PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    price      DECIMAL(10,2),
    category   VARCHAR(50),
    stock      INTEGER DEFAULT 0
);

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    product_id  INTEGER REFERENCES products(id),
    quantity    INTEGER NOT NULL,
    status      VARCHAR(20) DEFAULT 'pending',
    created_at  TIMESTAMP DEFAULT NOW()
);
```

---

## Part A — Basic Queries

Write SQL for each requirement:

1. Find all customers in 'New York' or 'London', ordered by name.

2. Find the top 5 most expensive products that are currently in stock (stock > 0).

3. Count the total number of orders for each status ('pending', 'shipped', 'delivered', 'cancelled'). Include statuses with zero orders.

4. Find all customers who have placed more than 3 orders. Return customer name and order count, ordered by order count descending.

5. Find all products that have **never** been ordered.

---

## Part B — JOINs

6. List all orders with customer name, product name, quantity, and total price (quantity × price). Show only completed orders.

7. Find customers who have ordered at least two different product categories. Return customer name and the count of distinct categories.

8. Self-join: find pairs of customers who are in the same city. Return `(customer1_name, customer2_name, city)`. Avoid duplicates (don't show both (A,B) and (B,A)).

---

## Part C — Aggregation and Window Functions

9. Calculate the total revenue per city (sum of quantity × price for all delivered orders), ordered by revenue descending.

10. For each product, show: product name, total units sold, total revenue, and rank by revenue (1 = highest). Use a window function for the rank.

11. Running total: for each customer in `customer_id = 1`, show each order with a running total of their spending. Use a window function (`SUM(...) OVER`).

---

## Part D — Query Plan Analysis

12. Without any indexes, what query execution plan (in plain words) does the database use for:
    ```sql
    SELECT * FROM orders WHERE customer_id = 12345;
    ```
    How many rows does the database examine?

13. After adding `CREATE INDEX idx_customer_id ON orders(customer_id)`:
    - What plan does the database now use?
    - How many rows does it examine for the same query?

14. The following query is slow on a table with 5 million orders:
    ```sql
    SELECT DATE(created_at), COUNT(*)
    FROM orders
    WHERE status = 'delivered'
    GROUP BY DATE(created_at)
    ORDER BY DATE(created_at);
    ```
    Propose an index that would speed this up. Explain why a composite index on `(status, created_at)` would help.

---

## Part E — Normalisation

The following table is denormalised:

```
order_id | customer_name | customer_city | product_name | category | unit_price | quantity
---------|---------------|----------------|--------------|----------|------------|--------
1        | Alice         | New York       | Laptop       | Electronics | 999.99 | 1
2        | Alice         | New York       | Mouse        | Electronics | 29.99  | 2
3        | Bob           | London         | Laptop       | Electronics | 999.99 | 1
```

15. Identify all functional dependencies in this table.

16. Normalise to 3NF. Show all resulting tables with their schemas and primary/foreign keys.

17. After normalisation, what JOIN query reconstructs the original view above?

---

## Rubric

| Part | Points |
|---|---|
| A basic queries | 25 |
| B JOINs | 20 |
| C aggregation | 22 |
| D query plans | 18 |
| E normalisation | 15 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A answers</summary>

```sql
-- 1
SELECT * FROM customers WHERE city IN ('New York','London') ORDER BY name;

-- 2
SELECT * FROM products WHERE stock > 0 ORDER BY price DESC LIMIT 5;

-- 3
SELECT status, COUNT(*) as cnt FROM orders GROUP BY status;
-- For all statuses including zero: LEFT JOIN with a status list or use CASE

-- 4
SELECT c.name, COUNT(o.id) as order_count
FROM customers c JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name HAVING COUNT(o.id) > 3
ORDER BY order_count DESC;

-- 5
SELECT p.* FROM products p
LEFT JOIN orders o ON p.id = o.product_id
WHERE o.id IS NULL;
```
</details>

<details>
<summary>Part B.6</summary>

```sql
SELECT c.name, p.name, o.quantity,
       o.quantity * p.price AS total_price
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products  p ON o.product_id  = p.id
WHERE o.status = 'delivered';
```
</details>

<details>
<summary>Part C.10 — window function</summary>

```sql
SELECT p.name,
       SUM(o.quantity) AS units_sold,
       SUM(o.quantity * p.price) AS revenue,
       RANK() OVER (ORDER BY SUM(o.quantity * p.price) DESC) AS rank
FROM products p
LEFT JOIN orders o ON p.id = o.product_id AND o.status = 'delivered'
GROUP BY p.id, p.name;
```
</details>
