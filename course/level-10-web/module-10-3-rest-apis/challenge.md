# Challenge 10.3 — REST APIs and JSON

**Type:** Design + implementation + analysis  
**Estimated time:** 45–55 minutes  
**Tools needed:** Python + pen and paper

---

## Part A — REST API Design

Design a REST API for a **library management system** with resources: books, members, and loans (a loan = one member borrowing one book).

1. Design the URL structure for all CRUD operations on all three resources. List at least 8 endpoints with their HTTP methods.

2. For the loan resource: a member can borrow a book (create a loan) and return it (update or delete). Which HTTP method is more semantically correct for "return a book": `DELETE /loans/{id}` or `PATCH /loans/{id}` with `{status: "returned"}`? Justify your choice.

3. Design the JSON schema for a `GET /books/{id}` response. Include: id, title, author, isbn, available_copies, publication_year, genres (array). What HTTP status code if the book doesn't exist?

---

## Part B — Implementation

Implement these two endpoints in Flask:

4. `GET /api/books` — list all books, with optional query parameters:
   - `?genre=fiction` — filter by genre
   - `?available=true` — only books with available_copies > 0
   - `?sort=title` or `?sort=year`

5. `POST /api/loans` — borrow a book:
   - Request body: `{member_id, book_id}`
   - Validation: member must exist, book must exist, book must have available copies
   - On success: decrement `available_copies`, create loan record, return 201
   - On failure: return 422 with error details

---

## Part C — Authentication and JWT

6. The library API needs authentication. Implement login:
   ```
   POST /api/auth/login
   Body: {"email": "...", "password": "..."}
   Returns: {"token": "eyJ..."}
   ```
   
   The JWT payload should include: `user_id`, `role` ('member' or 'librarian'), `exp`.

7. A librarian can see all loans; a member can only see their own. Implement the `GET /api/loans` endpoint that uses the JWT role to filter results.

8. Token expiry: what HTTP status code should be returned when a JWT is expired? What header should the response include to tell the client to re-authenticate?

---

## Part D — Error Design

9. Design consistent error responses for the library API. Define the JSON structure for:
   - 400 Bad Request (missing required field)
   - 404 Not Found
   - 422 Validation Error (book not available)
   - 429 Too Many Requests
   
   Your error format should be consistent across all error types and include at minimum: `error` code, `message`, and optionally `details`.

10. A client calls `POST /api/loans` with a valid member_id but a book_id that doesn't exist. Write the exact HTTP response (status line, Content-Type header, and JSON body).

---

## Part E — API Evolution

11. Your API is `v1`. You need to add a breaking change (rename `available_copies` to `copies_available`). How do you handle this without breaking existing clients? Describe two versioning strategies.

12. **Rate limiting** for the library API: members can borrow at most 5 books per month (tracked in the database). Where should this logic live — in the database (constraint), in the API handler, or in a separate rate-limiting middleware? What are the trade-offs?

---

## Rubric

| Part | Points |
|---|---|
| A REST design | 22 |
| B implementation | 24 |
| C authentication | 20 |
| D error design | 18 |
| E API evolution | 16 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1 — URL structure</summary>

```
GET    /api/books              — list all books
POST   /api/books              — add a book (librarian)
GET    /api/books/{id}         — get book details
PUT    /api/books/{id}         — update book (librarian)
DELETE /api/books/{id}         — remove book (librarian)
GET    /api/members            — list members (librarian)
POST   /api/members            — register member
GET    /api/members/{id}       — member profile
GET    /api/members/{id}/loans — all loans for a member
GET    /api/loans              — all active loans (librarian)
POST   /api/loans              — borrow a book
PATCH  /api/loans/{id}         — return a book (update status)
DELETE /api/loans/{id}         — cancel/delete loan
```
</details>

<details>
<summary>Part B.4 — GET /api/books</summary>

```python
@app.route('/api/books')
def list_books():
    genre     = request.args.get('genre')
    available = request.args.get('available')
    sort      = request.args.get('sort', 'title')

    books_list = list(books.values())

    if genre:
        books_list = [b for b in books_list if genre in b.get('genres', [])]
    if available == 'true':
        books_list = [b for b in books_list if b.get('available_copies', 0) > 0]

    valid_sorts = {'title', 'year'}
    if sort in valid_sorts:
        books_list.sort(key=lambda b: b.get(sort, ''))

    return jsonify(books_list)
```
</details>

<details>
<summary>Part D.9 — error format</summary>

```json
{
  "error": "book_not_available",
  "message": "The requested book has no available copies",
  "details": {
    "book_id": 42,
    "available_copies": 0,
    "next_return_expected": "2026-09-20"
  }
}
```
HTTP 422. All error responses use this same structure with `error` (machine-readable code), `message` (human-readable), and optional `details`.
</details>
