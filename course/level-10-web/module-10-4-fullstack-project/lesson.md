# Module 10.4 — Full-Stack Project

---

## The Problem

> You have learned:
> - HTML, CSS, JavaScript (frontend)
> - HTTP and REST APIs (communication layer)
> - Databases and SQL (data persistence)
> - Sockets and servers (networking)
>
> But these skills in isolation do not make a working application.
> A real application is these layers **working together**:
> a user clicks a button in the browser →
> JavaScript sends an HTTP request →
> a server receives and validates it →
> queries a database →
> returns structured data →
> JavaScript renders the result on screen.
>
> This module integrates everything by building a complete,
> working application from scratch.

---

## The Story

### The Full Stack Emerges

The term "full stack" was popularised around 2008–2012 as web applications became increasingly complex. The LAMP stack (Linux, Apache, MySQL, PHP) was an early full-stack: PHP generated HTML server-side, MySQL stored data.

**AJAX** (Asynchronous JavaScript and XML, named ~2005) changed the model: instead of the server rendering complete HTML pages, JavaScript would fetch data (via XMLHttpRequest) and update the page dynamically. Google Maps (2005) demonstrated this spectacularly — panning a map didn't reload the page.

Modern full-stack typically means: a JavaScript or TypeScript **frontend** (React, Vue, Angular), a **backend API** (Node.js, Python, Go, Java), and a **database** (PostgreSQL, MySQL, MongoDB). The frontend and backend communicate via JSON REST APIs or GraphQL.

---

## The Concept

### Application Architecture

A modern full-stack web application has three tiers:

```
┌─────────────────────────────────────────────────────┐
│   BROWSER (Client)                                  │
│   HTML/CSS/JavaScript                               │
│   React / Vue / plain JS                            │
│   Fetches data from API                             │
└──────────────────────────┬──────────────────────────┘
                           │ HTTP/REST (JSON)
┌──────────────────────────▼──────────────────────────┐
│   WEB SERVER (Backend)                              │
│   Python/Flask, Node.js/Express, etc.              │
│   Handles requests, applies business logic         │
│   Authentication, validation, authorisation        │
└──────────────────────────┬──────────────────────────┘
                           │ SQL / ORM
┌──────────────────────────▼──────────────────────────┐
│   DATABASE                                          │
│   PostgreSQL / MySQL / SQLite                      │
│   Persistent data storage                          │
└─────────────────────────────────────────────────────┘
```

### The Project: A Task Manager

Build a simple but complete task manager app:
- Create tasks with title, description, and due date
- Mark tasks as complete
- Filter by status (all / pending / completed)
- Persist tasks in a database

### Backend: Flask + SQLite

```python
# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # allow browser requests from different origin

DB = 'tasks.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row  # rows as dicts
    return conn

def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                description TEXT,
                due_date    TEXT,
                completed   INTEGER DEFAULT 0,
                created_at  TEXT DEFAULT (datetime('now'))
            )
        ''')

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    status = request.args.get('status')   # ?status=pending or ?status=completed
    with get_db() as db:
        if status == 'pending':
            rows = db.execute('SELECT * FROM tasks WHERE completed=0 ORDER BY created_at DESC').fetchall()
        elif status == 'completed':
            rows = db.execute('SELECT * FROM tasks WHERE completed=1 ORDER BY created_at DESC').fetchall()
        else:
            rows = db.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify(error='title is required'), 400
    with get_db() as db:
        cursor = db.execute(
            'INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)',
            (data['title'], data.get('description'), data.get('due_date'))
        )
        task_id = cursor.lastrowid
        task = dict(db.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone())
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    data = request.get_json()
    with get_db() as db:
        task = db.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone()
        if not task: return jsonify(error='not found'), 404
        if 'completed' in data:
            db.execute('UPDATE tasks SET completed=? WHERE id=?', (int(data['completed']), task_id))
        if 'title' in data:
            db.execute('UPDATE tasks SET title=? WHERE id=?', (data['title'], task_id))
        updated = dict(db.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone())
    return jsonify(updated)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with get_db() as db:
        result = db.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        if result.rowcount == 0: return jsonify(error='not found'), 404
    return '', 204

init_db()
if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Frontend: HTML + Vanilla JavaScript

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Task Manager</title>
  <style>
    * { box-sizing: border-box; }
    body { font-family: Inter, system-ui, sans-serif; max-width: 640px; margin: 40px auto; padding: 0 16px; }
    .task { display: flex; align-items: center; gap: 12px; padding: 12px; border: 1px solid #ddd; border-radius: 6px; margin-bottom: 8px; }
    .task.completed { opacity: 0.5; }
    .task-title { flex: 1; font-size: 15px; }
    .task.completed .task-title { text-decoration: line-through; }
    button { padding: 8px 16px; border: 1px solid #333; background: #fff; cursor: pointer; border-radius: 4px; }
    #add-form { display: flex; gap: 8px; margin-bottom: 24px; }
    #task-input { flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 15px; }
  </style>
</head>
<body>
  <h1>Task Manager</h1>
  <form id="add-form">
    <input id="task-input" placeholder="New task..." required>
    <button type="submit">Add Task</button>
  </form>
  <div id="filter-bar">
    <button onclick="loadTasks()">All</button>
    <button onclick="loadTasks('pending')">Pending</button>
    <button onclick="loadTasks('completed')">Completed</button>
  </div>
  <div id="task-list"></div>

  <script>
    const API = 'http://localhost:5000/api';

    async function loadTasks(status = '') {
      const url = status ? `${API}/tasks?status=${status}` : `${API}/tasks`;
      const res  = await fetch(url);
      const tasks = await res.json();
      renderTasks(tasks);
    }

    function renderTasks(tasks) {
      const list = document.getElementById('task-list');
      list.innerHTML = tasks.map(t => `
        <div class="task ${t.completed ? 'completed' : ''}" id="task-${t.id}">
          <input type="checkbox" ${t.completed ? 'checked' : ''}
            onchange="toggleTask(${t.id}, this.checked)">
          <span class="task-title">${t.title}</span>
          <button onclick="deleteTask(${t.id})">×</button>
        </div>
      `).join('');
    }

    async function toggleTask(id, completed) {
      await fetch(`${API}/tasks/${id}`, {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({completed})
      });
      loadTasks();
    }

    async function deleteTask(id) {
      await fetch(`${API}/tasks/${id}`, { method: 'DELETE' });
      loadTasks();
    }

    document.getElementById('add-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const input = document.getElementById('task-input');
      await fetch(`${API}/tasks`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title: input.value})
      });
      input.value = '';
      loadTasks();
    });

    loadTasks();
  </script>
</body>
</html>
```

### What You Just Built

This application demonstrates the complete stack:
- **Browser** renders HTML/CSS, runs JavaScript
- **JavaScript** makes `fetch()` calls to the REST API
- **Flask** receives HTTP requests, validates input, queries the database
- **SQLite** persists data to disk

This is the same architecture — at different scales and with more components — used by every modern web application.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — API Request Trace**
- Click "Add Task" in the task manager
- Watch the full request: JS → fetch() → HTTP → Flask handler → SQLite → JSON response → DOM update

**Tool 2 — Database Inspector**
- See the SQLite database contents update in real time
- Execute raw SQL and watch the API response change

**Tool 3 — Network Tab**
- A simulated browser DevTools network tab
- See every HTTP request made by the app
- Identify which operations are GET, POST, PATCH, DELETE

---

## Going Deeper

**React and component-based UIs**: plain JavaScript for UIs becomes unmaintainable as complexity grows — you write endless `document.getElementById()` calls and lose track of what state is displayed. React's component model (`function TaskItem({task}) { return <div>...</div>; }`) makes UI logic modular and testable. The virtual DOM handles efficient DOM updates. Understanding why React was invented requires first experiencing the pain of vanilla JS UI code at scale.

**Authentication and sessions**: our app has no authentication. Adding it requires: login endpoint (POST /api/auth/login → JWT), protected endpoints (verify JWT on every request), logout (invalidate token), and refresh tokens (short-lived access tokens + long-lived refresh tokens). This is a non-trivial addition that most production apps need from day one.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Extend the task manager with: due dates displayed and colour-coded (red if overdue), a search endpoint (`GET /api/tasks?q=keyword`), user authentication so each user only sees their own tasks, and a deployment checklist (what would you need to change to deploy this to a public server?).
