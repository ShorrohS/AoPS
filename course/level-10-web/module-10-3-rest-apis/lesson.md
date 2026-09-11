# Module 10.3 — REST APIs and JSON

---

## The Problem

> A mobile app, a web frontend, a desktop app, and a third-party service
> all need to share the same data and functionality.
>
> You cannot share code — they run on different platforms.
> You cannot share a database — that would be a security nightmare.
>
> You need a standard way for these different systems to communicate.
> A contract that says: send this request, get that response.
>
> That contract is the **API** (Application Programming Interface),
> and for web services, the dominant style is **REST** using **JSON**.

---

## The Story

### REST: A Style, Not a Standard

Roy Fielding defined REST (Representational State Transfer) in his 2000 PhD dissertation at UC Irvine. Fielding was one of the primary authors of HTTP/1.1; REST was his architectural analysis of why the web worked so well and how to apply those same principles to designing APIs.

REST is not a protocol or a specification — it is a set of architectural constraints. An API that follows these constraints is called "RESTful."

Before REST, web services typically used **SOAP** (Simple Object Access Protocol) — XML-based, rigid, complex, with extensive tooling requirements. SOAP dominated enterprise software in the early 2000s. REST replaced it because it was simpler: use HTTP verbs and URLs you already understand, and JSON instead of XML.

**JSON** (JavaScript Object Notation) was popularised by Douglas Crockford around 2001. It was not invented — it was discovered as a subset of JavaScript that worked as a data interchange format. Simpler than XML (no closing tags), directly parseable by JavaScript, and human-readable.

---

## The Concept

### JSON — Data Format

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "age": 30,
  "address": {
    "street": "123 Main St",
    "city": "New York",
    "country": "US"
  },
  "tags": ["developer", "python", "aws"],
  "active": true,
  "score": 98.5,
  "deleted_at": null
}
```

**JSON data types**: string (double quotes), number (int or float), boolean (true/false), null, object ({}), array ([]).

**JSON in Python:**
```python
import json

# Parse JSON string → Python dict
data = json.loads('{"name": "Alice", "age": 30}')
print(data['name'])      # Alice

# Serialize Python → JSON string
obj = {'name': 'Bob', 'scores': [95, 87, 92]}
text = json.dumps(obj, indent=2)
# {
#   "name": "Bob",
#   "scores": [95, 87, 92]
# }
```

### REST Architectural Constraints

1. **Client-Server**: separate concerns — client handles UI, server handles data
2. **Stateless**: each request contains all information needed; server stores no session state per client
3. **Cacheable**: responses indicate whether they can be cached
4. **Uniform Interface**: consistent URLs and HTTP methods (the key constraint)
5. **Layered System**: client doesn't know if it's talking to the real server or a load balancer/cache
6. **Code on Demand** (optional): server can send executable code (JavaScript)

### RESTful API Design

**Resources** (nouns) map to URLs. **HTTP methods** (verbs) define the action:

```
GET    /users           → list all users
GET    /users/42        → get user 42
POST   /users           → create a new user
PUT    /users/42        → replace user 42 entirely
PATCH  /users/42        → partially update user 42
DELETE /users/42        → delete user 42

GET    /users/42/orders → list orders for user 42
POST   /users/42/orders → create an order for user 42
GET    /orders/7        → get a specific order (can also go here)
```

**URL design rules:**
- Use nouns, not verbs: `/users/42` not `/getUser?id=42`
- Use plural nouns: `/users` not `/user`
- Nest for relationships: `/users/42/orders`
- Keep it flat when possible: `/orders?user_id=42` is fine
- Versioning: `/api/v1/users` or `Accept: application/vnd.api+json;version=1`

### Request and Response Format

**Creating a user (POST):**

Request:
```http
POST /api/v1/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...

{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "role": "admin"
}
```

Response:
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/users/43

{
  "id": 43,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "role": "admin",
  "created_at": "2026-09-10T22:00:00Z"
}
```

**Error response (validation failure):**
```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "error": "validation_failed",
  "message": "Request validation failed",
  "details": [
    {"field": "email", "code": "already_exists", "message": "Email already in use"},
    {"field": "name", "code": "too_short", "message": "Name must be at least 2 characters"}
  ]
}
```

### Building a REST API with Python (Flask)

```python
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# In-memory store (use a database in production)
users = {1: {'id':1,'name':'Alice','email':'alice@example.com'}}
next_id = 2

@app.route('/api/v1/users', methods=['GET'])
def list_users():
    return jsonify(list(users.values()))

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user: abort(404, description=f"User {user_id} not found")
    return jsonify(user)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        abort(400, description="name and email are required")
    user = {'id': next_id, 'name': data['name'], 'email': data['email']}
    users[next_id] = user
    next_id += 1
    return jsonify(user), 201

@app.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users: abort(404)
    del users[user_id]
    return '', 204

@app.errorhandler(404)
def not_found(e): return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e): return jsonify(error=str(e)), 400
```

### Authentication

**API Keys**: simplest form. Include in header: `Authorization: ApiKey abc123`. No expiry, hard to revoke per-user.

**JWT (JSON Web Token)**: a signed token containing claims (user ID, roles, expiry). The server can verify the token without database lookup — stateless authentication.

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
    return jwt.decode(token, SECRET, algorithms=['HS256'])
```

**OAuth 2.0**: industry standard for delegated authorisation. "Login with Google" — the user grants your app limited access to their Google data without sharing their password.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — REST API Explorer**
- Pre-built mock API with users and orders endpoints
- Make GET, POST, PUT, DELETE requests from the UI
- See the full request (headers, body) and response (status code, headers, body)

**Tool 2 — JSON Schema Validator**
- Define a JSON schema for a resource
- Enter JSON payloads — see which pass and which fail
- Understand required vs optional fields, type validation, format validation

**Tool 3 — API Design Exercise**
- Given a problem (e.g., a library book system)
- Design the URL structure and HTTP methods
- Compare your design to best practices

---

## Going Deeper

**GraphQL**: an alternative to REST invented by Facebook (2015). Instead of multiple endpoints, there is one endpoint (`/graphql`) and you specify exactly what data you want in the request body. Benefits: no over-fetching (getting more data than needed) or under-fetching (needing multiple requests to get all needed data). Trade-offs: more complex server implementation, harder caching, N+1 query problems. Used heavily in modern frontend apps.

**OpenAPI (Swagger)**: a specification format for describing REST APIs. An `openapi.yaml` file describes all endpoints, parameters, request/response schemas, and authentication. From this file: generate client SDKs in any language, generate interactive documentation (Swagger UI), validate requests and responses automatically. Most production REST APIs publish an OpenAPI spec.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Design a REST API for a library system (books, members, loans), implement the `/books` and `/loans` endpoints in Python with Flask, write authentication middleware using JWT, and identify three REST design mistakes in a given poorly-designed API URL structure.
