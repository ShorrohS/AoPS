# Challenge 10.4 — Full-Stack Project

**Type:** Implementation + extension + reasoning  
**Estimated time:** 60–90 minutes  
**Tools needed:** Python, Flask, browser

---

## Part A — Feature Extensions

Starting from the task manager from the lesson:

1. **Due dates with colour coding**: modify the frontend to display each task's due date. Tasks overdue (past due date) should be shown with a red border; tasks due today should be orange; others normal.

2. **Search endpoint**: implement `GET /api/tasks?q=keyword` that returns tasks where the title or description contains the keyword (case-insensitive). Show the SQL query with `LIKE` and the JavaScript that calls it when the user types in a search box.

3. **Priority field**: add a `priority` field (values: 'low', 'medium', 'high') to the tasks table. Update the API and frontend to:
   - Set priority on create
   - Change priority via a dropdown on each task
   - Sort by priority (high first) when filtering

---

## Part B — Authentication

4. Add a `users` table and `user_id` foreign key to `tasks`. Implement:
   ```
   POST /api/auth/register   — create a new user account
   POST /api/auth/login      — return a JWT on success
   GET  /api/tasks           — return only this user's tasks (verify JWT)
   ```

5. Implement JWT creation and verification:
   ```python
   import jwt, datetime
   SECRET = 'your-secret-key'
   
   def create_token(user_id): ...
   def verify_token(token): ...    # raises jwt.InvalidTokenError if invalid
   ```

6. Write a Flask decorator `@require_auth` that extracts the JWT from the `Authorization: Bearer <token>` header, verifies it, and passes the `user_id` to the handler. If the token is missing or invalid, return 401.

---

## Part C — API Design Review

The following API has three design problems. Identify each and propose the correct REST-compliant design:

```
GET  /getTasks?userId=42
POST /createTask
GET  /deleteTask?id=99
PUT  /tasks/update/5
```

7. Problem 1: __________. Correct: __________
8. Problem 2: __________. Correct: __________
9. Problem 3: __________. Correct: __________

---

## Part D — Deployment Checklist

You want to deploy this Flask app to a public server. For each item, explain what needs to change from the development version:

10. **Debug mode**: `app.run(debug=True)`. What security risk does debug mode create in production? What should it be set to?

11. **Database**: SQLite file at `./tasks.db`. What problem does this create if you run 2+ worker processes? What database should you use instead?

12. **CORS**: `CORS(app)` allows requests from any origin. What should you restrict this to in production?

13. **SECRET_KEY**: the JWT secret `'your-secret-key'`. How should this be stored and loaded in production?

14. **HTTPS**: your server currently uses plain HTTP. What do you need to add to serve HTTPS? Name the tool/component.

---

## Part E — Tracing a Full Request

Trace the complete lifecycle of clicking "Mark as complete" on task #42:

15. List every step from the click to the database update and DOM update, identifying:
    - JavaScript event handler
    - HTTP request (method, URL, headers, body)
    - Flask route handler
    - SQL query
    - JSON response
    - DOM mutation

16. How many network round trips does this operation require? How could you reduce it to 0 (optimistic update)?

---

## Rubric

| Part | Points |
|---|---|
| A feature extensions | 24 |
| B authentication | 24 |
| C API design review | 12 |
| D deployment checklist | 20 |
| E full trace | 20 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part B.5 — JWT</summary>

```python
import jwt, datetime

SECRET = 'your-secret-key'

def create_token(user_id):
    return jwt.encode({
        'sub': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }, SECRET, algorithm='HS256')

def verify_token(token):
    return jwt.decode(token, SECRET, algorithms=['HS256'])  # raises on invalid

def require_auth(fn):
    from functools import wraps
    from flask import request, jsonify
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify(error='Unauthorized'), 401
        try:
            payload = verify_token(auth[7:])
            return fn(*args, user_id=payload['sub'], **kwargs)
        except jwt.InvalidTokenError:
            return jsonify(error='Invalid token'), 401
    return wrapper
```
</details>

<details>
<summary>Part C.7–9</summary>

7. `/getTasks` uses a verb in the URL — REST uses nouns. Correct: `GET /tasks?user_id=42`
8. `GET /deleteTask?id=99` uses GET for a destructive action — deletes should use DELETE method. Correct: `DELETE /tasks/99`
9. `/tasks/update/5` uses a verb "update" in the path. Correct: `PUT /tasks/5` (the method expresses the action, not the URL)
</details>

<details>
<summary>Part E.15 — full trace</summary>

1. User clicks checkbox → JavaScript `change` event fires
2. `toggleTask(42, true)` called
3. `fetch('/api/tasks/42', {method:'PATCH', body: JSON.stringify({completed:true})})`
4. HTTP request: `PATCH /api/tasks/42\r\nContent-Type: application/json\r\n\r\n{"completed":true}`
5. Flask routes to `update_task(42)` → reads JSON body
6. SQL: `UPDATE tasks SET completed=1 WHERE id=42`
7. SQL: `SELECT * FROM tasks WHERE id=42` (return updated task)
8. Flask returns 200 JSON `{"id":42,"completed":1,...}`
9. JavaScript receives response → calls `loadTasks()` → re-fetches entire list
10. DOM re-rendered with updated state

1 round trip for the PATCH, 1 for the re-fetch = 2 total.
Optimistic: update DOM immediately before fetch, revert on error = 0 perceived latency.
</details>
