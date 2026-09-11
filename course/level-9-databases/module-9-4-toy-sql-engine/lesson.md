# Module 9.4 — Building a Toy SQL Engine

---

## The Problem

> SQL is a declarative language: you describe *what* you want.
> Someone has to figure out *how* to get it.
>
> That someone is the SQL engine — the software that takes your query,
> parses it, plans an execution strategy, and retrieves the data.
>
> Building a minimal SQL engine from scratch is one of the most educational
> programming projects in computer science.
> It requires understanding: parsing, query planning, B-tree indexes,
> join algorithms, aggregation, and storage formats.

---

## The Story

### SQLite — The World's Most Deployed Database

D. Richard Hipp wrote SQLite in 2000 for use on US Navy destroyers — embedded systems that needed a database without a server. SQLite is serverless, zero-configuration, and self-contained in a single ~750 KB C file.

Today, SQLite is embedded in: every Android device, every iOS device, every Mac and Windows machine, every Firefox browser, every Chrome browser. Over one trillion SQLite databases are in active use. It is almost certainly the most widely deployed software library in history.

SQLite's source code is public domain and is one of the best-documented database implementations ever written. Reading it is a masterclass in systems programming.

Our toy engine will be a fraction of SQLite's complexity but will hit the same fundamental concepts: parsing SQL text, executing against an in-memory table store, and producing results.

---

## The Concept

### The SQL Engine Pipeline

```
SQL string input
      ↓ Tokeniser (Lexer)
Token stream: SELECT, *, FROM, users, WHERE, id, =, 5
      ↓ Parser
Abstract Syntax Tree (AST)
      ↓ Query Planner / Optimiser
Execution Plan: SeqScan → Filter → Project
      ↓ Executor
Result rows
```

### Step 1: Tokeniser

```python
import re

def tokenise(sql):
    token_patterns = [
        ('KEYWORD',  r'\b(SELECT|FROM|WHERE|INSERT|INTO|VALUES|UPDATE|SET|DELETE|AND|OR|NOT|CREATE|TABLE|INT|TEXT|PRIMARY|KEY|JOIN|ON|AS)\b'),
        ('NUMBER',   r'\d+(\.\d+)?'),
        ('STRING',   r"'[^']*'"),
        ('IDENT',    r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('OP',       r'[=<>!]+|[,;()*]'),
        ('WHITESPACE', r'\s+'),
    ]
    combined = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns)
    tokens = []
    for m in re.finditer(combined, sql, re.IGNORECASE):
        if m.lastgroup != 'WHITESPACE':
            tokens.append((m.lastgroup, m.group()))
    return tokens

tokenise("SELECT name, age FROM users WHERE id = 5")
# [('KEYWORD','SELECT'), ('IDENT','name'), ('OP',','), ('IDENT','age'),
#  ('KEYWORD','FROM'), ('IDENT','users'), ('KEYWORD','WHERE'),
#  ('IDENT','id'), ('OP','='), ('NUMBER','5')]
```

### Step 2: Parser — Building an AST

```python
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos    = 0

    def peek(self): return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    def consume(self): t = self.tokens[self.pos]; self.pos += 1; return t
    def expect(self, kind, val=None):
        t = self.consume()
        if t[0] != kind or (val and t[1].upper() != val.upper()):
            raise SyntaxError(f"Expected {kind} {val}, got {t}")
        return t

    def parse_select(self):
        self.expect('KEYWORD', 'SELECT')
        columns = self.parse_column_list()
        self.expect('KEYWORD', 'FROM')
        table = self.consume()[1]
        where  = None
        if self.peek() and self.peek()[1].upper() == 'WHERE':
            self.consume()
            where = self.parse_condition()
        return {'type': 'SELECT', 'columns': columns, 'table': table, 'where': where}

    def parse_column_list(self):
        cols = []
        t = self.peek()
        if t and t[1] == '*': self.consume(); return ['*']
        cols.append(self.consume()[1])
        while self.peek() and self.peek()[1] == ',':
            self.consume(); cols.append(self.consume()[1])
        return cols

    def parse_condition(self):
        left  = self.consume()[1]
        op    = self.consume()[1]
        right = self.consume()[1].strip("'")
        return {'left': left, 'op': op, 'right': right}
```

### Step 3: In-Memory Storage Engine

```python
class Table:
    def __init__(self, name, schema):
        # schema: [(col_name, col_type), ...]
        self.name   = name
        self.schema = schema
        self.rows   = []       # list of dicts
        self.next_id = 1

    def insert(self, row_dict):
        if 'id' not in row_dict:
            row_dict['id'] = self.next_id; self.next_id += 1
        self.rows.append(row_dict)

    def scan(self):
        return iter(self.rows)

class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, name, schema):
        self.tables[name] = Table(name, schema)

    def get_table(self, name):
        if name not in self.tables:
            raise NameError(f"Table '{name}' not found")
        return self.tables[name]
```

### Step 4: Executor

```python
def evaluate_condition(row, cond):
    if cond is None: return True
    left_val  = row.get(cond['left'])
    right_val = cond['right']
    # Try numeric comparison
    try: left_val = float(left_val); right_val = float(right_val)
    except (TypeError, ValueError): pass
    ops = {'=': lambda a,b: a==b, '!=': lambda a,b: a!=b,
           '<': lambda a,b: a<b,  '>': lambda a,b: a>b,
           '<=':lambda a,b: a<=b, '>=':lambda a,b: a>=b}
    return ops[cond['op']](left_val, right_val)

def execute(db, ast):
    if ast['type'] == 'SELECT':
        table = db.get_table(ast['table'])
        results = []
        for row in table.scan():
            if evaluate_condition(row, ast['where']):
                if ast['columns'] == ['*']:
                    results.append(dict(row))
                else:
                    results.append({c: row.get(c) for c in ast['columns']})
        return results

    if ast['type'] == 'INSERT':
        table = db.get_table(ast['table'])
        row = dict(zip(ast['columns'], ast['values']))
        table.insert(row)
        return [{'affected': 1}]
```

### Step 5: Tying It Together

```python
def query(db, sql):
    tokens = tokenise(sql)
    parser = Parser(tokens)
    keyword = tokens[0][1].upper()
    if keyword == 'SELECT':
        ast = parser.parse_select()
    elif keyword == 'INSERT':
        ast = parser.parse_insert()
    else:
        raise NotImplementedError(f"Unsupported: {keyword}")
    return execute(db, ast)

# Demo:
db = Database()
db.create_table('users', [('id','INT'), ('name','TEXT'), ('age','INT')])
query(db, "INSERT INTO users (name, age) VALUES ('Alice', 30)")
query(db, "INSERT INTO users (name, age) VALUES ('Bob', 25)")
query(db, "INSERT INTO users (name, age) VALUES ('Carol', 35)")
result = query(db, "SELECT name, age FROM users WHERE age > 28")
# [{'name': 'Alice', 'age': 30}, {'name': 'Carol', 'age': 35}]
```

### Extending the Engine

**Add ORDER BY:**
```python
if ast.get('order_by'):
    col, direction = ast['order_by']
    results.sort(key=lambda r: r.get(col), reverse=(direction=='DESC'))
```

**Add GROUP BY + COUNT:**
```python
if ast.get('group_by'):
    from itertools import groupby
    col = ast['group_by']
    results.sort(key=lambda r: r[col])
    grouped = []
    for key, rows in groupby(results, key=lambda r: r[col]):
        group_rows = list(rows)
        grouped.append({col: key, 'count': len(group_rows)})
    results = grouped
```

**Add a nested loop JOIN:**
```python
if ast.get('join'):
    right_table = db.get_table(ast['join']['table'])
    joined = []
    for left_row in results:
        for right_row in right_table.scan():
            if left_row[ast['join']['left_key']] == right_row[ast['join']['right_key']]:
                joined.append({**left_row, **right_row})
    results = joined
```

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — SQL Engine Step-Through**
- Enter a SQL query
- Step through: tokenise → parse → plan → execute
- See the AST as a tree diagram, the execution plan, and the result rows

**Tool 2 — Query Planner**
- A table with and without an index
- Run the same WHERE query; see two execution plans:
  - Without index: Sequential Scan → Filter
  - With index: B+tree Lookup → Fetch

**Tool 3 — Join Algorithm Comparison**
- Run a JOIN on two small tables
- Compare: Nested Loop, Hash Join, Sort-Merge Join
- Count operations for each; see why each is preferred in different scenarios

---

## Going Deeper

**WAL and crash recovery**: our toy engine is memory-only. A real engine writes to disk with WAL (Module 9.3). Implementing WAL means: before modifying a page, write the change to the log; on startup after a crash, replay the log. SQLite's WAL mode is one of the cleanest implementations to study.

**MVCC in the query engine**: multi-version concurrency control (Module 9.3) affects the executor: instead of locking rows, each scan checks each row's visibility — is this row's version visible to this transaction's snapshot? Implementing MVCC makes the executor significantly more complex but enables much higher concurrency.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Extend the toy engine to support `ORDER BY col DESC`, add a `LIMIT n` clause, implement a simple hash join for two tables, and trace all execution steps for `SELECT u.name, COUNT(o.id) FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.name`.
