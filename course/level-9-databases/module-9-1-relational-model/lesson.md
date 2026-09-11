# Module 9.1 — The Relational Model and SQL

---

## The Problem

> A company stores customer data in one file, orders in another, products in a third.
> To find all orders placed by customers in New York for products that are currently out of stock,
> you write a custom program that opens all three files, reads every line, and applies filters.
>
> Every new question requires a new program.
> When the file format changes, every program breaks.
>
> In 1970, Edgar Codd published a paper that solved all of these problems at once.
> The solution: a **relational model** — data organised as tables,
> accessed through a declarative language that describes *what* you want,
> not *how* to get it.

---

## The Story

### E.F. Codd and the Relational Revolution

Edgar Codd was a computer scientist at IBM's San Jose Research Lab. In 1970, he published "A Relational Model of Data for Large Shared Data Banks" — one of the most influential papers in computer science history.

Codd's insight: store data in **relations** (tables), and access it using **relational algebra** — a mathematical framework with operations like selection, projection, and join. The query language would be *declarative*: describe what data you want, let the database figure out how to retrieve it.

IBM built System R (1974–1979) to prove the concept, developing the **SEQUEL** query language (later renamed **SQL**). Don Chamberlin and Ray Boyce designed SQL to be readable by non-programmers — like English with structure.

Oracle Corporation (founded 1977 by Larry Ellison) shipped the first commercial SQL database in 1979. PostgreSQL (1986, open source), MySQL (1995, open source), SQLite (2000, embedded) followed. Today, relational databases power virtually every financial system, e-commerce platform, and enterprise application in the world.

---

## The Concept

### Tables, Rows, Columns

A **relation** is a table with:
- **Schema**: column names and types (defined once)
- **Rows** (tuples): individual records
- **Primary key**: one or more columns that uniquely identify each row

```sql
CREATE TABLE users (
    id          INTEGER PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(255) UNIQUE NOT NULL,
    city        VARCHAR(100),
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    user_id     INTEGER REFERENCES users(id),
    amount      DECIMAL(10,2) NOT NULL,
    status      VARCHAR(20) DEFAULT 'pending',
    created_at  TIMESTAMP DEFAULT NOW()
);
```

A **foreign key** (`user_id REFERENCES users(id)`) enforces referential integrity: you cannot create an order for a non-existent user, and you cannot delete a user who has orders.

### SQL — The Four Core Operations

**SELECT — Query data:**
```sql
-- Basic selection and projection
SELECT name, email FROM users WHERE city = 'New York';

-- Aggregate functions
SELECT city, COUNT(*) as user_count, AVG(amount) as avg_order
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed'
GROUP BY city
HAVING COUNT(*) > 10
ORDER BY user_count DESC
LIMIT 5;
```

**INSERT — Add data:**
```sql
INSERT INTO users (name, email, city) VALUES ('Alice', 'alice@example.com', 'NYC');
INSERT INTO orders (user_id, amount) SELECT id, 99.99 FROM users WHERE city = 'NYC';
```

**UPDATE — Modify data:**
```sql
UPDATE orders SET status = 'shipped' WHERE id = 1234;
UPDATE users SET city = 'New York' WHERE city = 'NYC';  -- normalise data
```

**DELETE — Remove data:**
```sql
DELETE FROM orders WHERE created_at < NOW() - INTERVAL '1 year' AND status = 'cancelled';
```

### JOINs — Combining Tables

The JOIN operation is the heart of relational databases:

```sql
-- INNER JOIN: only rows where condition matches in both tables
SELECT u.name, o.amount, o.status
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN: all users, even those with no orders
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Self-join: find users who share a city
SELECT a.name, b.name, a.city
FROM users a
JOIN users b ON a.city = b.city AND a.id < b.id;
```

**Types of joins:**
- **INNER JOIN**: intersection — rows matching in both tables
- **LEFT JOIN**: all from left table + matching from right (NULLs where no match)
- **RIGHT JOIN**: all from right + matching from left
- **FULL OUTER JOIN**: all rows from both tables
- **CROSS JOIN**: Cartesian product — every combination (rarely used)

### Normalisation — Eliminating Redundancy

**First Normal Form (1NF)**: every column holds atomic values (no lists, no nested tables). Each row is unique.

**Second Normal Form (2NF)**: in addition to 1NF, every non-key attribute depends on the whole primary key (no partial dependencies). Relevant when the key is composite.

**Third Normal Form (3NF)**: in addition to 2NF, no transitive dependencies — non-key attributes do not depend on other non-key attributes.

**Example — violation and fix:**
```sql
-- BAD: city depends on zip, not on customer_id + order_id
orders(customer_id, order_id, customer_name, customer_zip, customer_city, product_name, quantity)

-- GOOD: separate tables, each fact stored once
customers(customer_id, name, zip, city)       -- city depends only on zip → 3NF issue
zip_codes(zip, city, state)                   -- extract the dependency
customers(customer_id, name, zip)             -- zip is FK to zip_codes
orders(order_id, customer_id, product_id, quantity)
products(product_id, name, price)
```

Denormalisation is sometimes done intentionally for read performance: store redundant data to avoid joins.

### Indexes — Making Queries Fast

Without an index, every query scans every row (O(n)). With an index (B+tree, Module 9.2):

```sql
-- Slow: full table scan
SELECT * FROM orders WHERE user_id = 12345;

-- Add index: O(log n) lookup
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Composite index: useful for queries filtering on both columns
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Covering index: all queried columns in the index → no table lookup
CREATE INDEX idx_orders_covering ON orders(user_id, status, amount, created_at);

-- Check if index is being used:
EXPLAIN SELECT * FROM orders WHERE user_id = 12345;
```

**When indexes help**: equality lookups, range queries, ORDER BY, GROUP BY on indexed columns, JOINs on indexed foreign keys.

**When indexes hurt**: INSERT, UPDATE, DELETE are slower (must maintain all indexes), full table scans on small tables (index lookup overhead exceeds full scan cost).

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — SQL Query Executor**
- Pre-loaded tables: users, orders, products
- Run SELECT queries with WHERE, JOIN, GROUP BY, ORDER BY
- See execution plans and row counts

**Tool 2 — JOIN Visualiser**
- Two small tables side by side
- Select INNER, LEFT, RIGHT, FULL OUTER JOIN
- Watch the result set build: matching rows highlighted, nulls shown

**Tool 3 — Index Impact**
- Run a query on an un-indexed column: watch the full table scan
- Add an index: run the same query, see the B+tree lookup
- Compare execution times

---

## Going Deeper

**Query optimiser**: SQL is declarative — the database engine decides how to execute it. The query optimiser generates multiple execution plans, estimates their cost (using table statistics), and chooses the cheapest. A JOIN between two tables could be executed as a nested loop (O(n×m)), hash join (O(n+m)), or sort-merge join (O(n log n + m log m)). The optimiser picks based on table sizes, available indexes, and selectivity estimates. Understanding the optimiser explains why `EXPLAIN ANALYZE` output is a core DBA skill.

**Window functions**: a powerful SQL feature for analytical queries — compute running totals, rank rows within groups, calculate moving averages, all without subqueries:
```sql
SELECT name, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
       SUM(salary) OVER (PARTITION BY department) as dept_total
FROM employees;
```

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Write SQL to find the top 5 users by total order value (only counting completed orders), normalise a given denormalised table to 3NF, explain why `SELECT * FROM large_table` is sometimes faster without an index than with one, and trace what query execution steps happen for a JOIN between a 1M-row and 100K-row table.
