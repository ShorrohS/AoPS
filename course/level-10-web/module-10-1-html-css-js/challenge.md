# Challenge 10.1 — HTML, CSS, and JavaScript from the Ground Up

**Type:** Build + implementation + analysis  
**Estimated time:** 60–75 minutes  
**Tools needed:** browser + text editor

---

## Part A — Semantic HTML

Rewrite this non-semantic HTML using appropriate semantic elements:

```html
<div class="header">
  <div class="nav">
    <div onclick="go('/')">Home</div>
    <div onclick="go('/about')">About</div>
  </div>
</div>
<div class="main">
  <div class="article">
    <div class="title">My First Post</div>
    <div class="meta">Posted on September 10, 2026</div>
    <div class="body">Content here...</div>
    <div class="tags"><div>javascript</div><div>web</div></div>
  </div>
</div>
<div class="footer">© 2026</div>
```

1. Rewrite using: `<header>`, `<nav>`, `<main>`, `<article>`, `<h1>`, `<time>`, `<footer>`, `<a>`, `<ul>`.

2. For each semantic element you used, explain one concrete benefit it provides over a generic `<div>`.

3. Add ARIA labels where needed for accessibility. Which elements need them and why?

---

## Part B — CSS Layout

4. Using only CSS (no JavaScript), create a **3-column card grid** that:
   - Shows 3 columns on desktop (>768px)
   - Shows 2 columns on tablet (480–768px)
   - Shows 1 column on mobile (<480px)
   - Each card has: image, title, description, a "Read more" button
   
   Write the CSS using Grid or Flexbox + media queries.

5. The CSS cascade: given these three rules, what is the final color of a `<p class="text" id="main-para">` element?
   ```css
   p { color: blue; }
   .text { color: green; }
   #main-para { color: red; }
   p.text { color: purple; }
   ```
   Calculate specificity for each rule and determine the winner.

6. Implement a CSS-only **dark mode toggle**: using a checkbox `<input type="checkbox" id="dark-toggle">` and the `:checked` pseudo-class with the `~` sibling selector, toggle all body background and text colors without JavaScript.

---

## Part C — To-Do List (Pure JS)

Build a complete to-do list application using only HTML, CSS, and vanilla JavaScript — no frameworks.

7. Features required:
   - Add a task (text input + button or Enter key)
   - Mark a task as complete (click to toggle)
   - Delete a task (delete button on each item)
   - Filter: All / Active / Completed (three buttons)
   - Show count of remaining active tasks

8. Implement `addTask(text)`, `toggleTask(id)`, `deleteTask(id)`, and `renderTasks(filter)`. Use a JavaScript array as the state.

9. Persist the task list across page refreshes using `localStorage`. What is the serialisation format? Show `saveToStorage()` and `loadFromStorage()`.

---

## Part D — Event Flow

10. For the HTML below, trace the event flow when the `<button>` is clicked:
    ```html
    <div id="outer">
      <div id="middle">
        <button id="btn">Click me</button>
      </div>
    </div>
    ```
    List all elements that receive the event, in what order (capture phase then bubble phase).

11. What does `event.stopPropagation()` do? In the above example, if it's called inside the `#middle` handler, which handlers still fire?

12. What is **event delegation**? Show how to use one event listener on `#outer` to handle clicks on any `<button>` descendant, including buttons added dynamically after the listener is attached.

---

## Part E — JavaScript Internals

13. Explain the output of this code:
    ```javascript
    for (var i = 0; i < 3; i++) {
      setTimeout(() => console.log(i), 0);
    }
    ```
    What is printed? Why? Fix it using `let` and explain why `let` fixes it.

14. Explain the difference between `null`, `undefined`, and an undeclared variable. Give one scenario where each naturally occurs.

15. What does `===` check vs `==`? Give two examples where `==` returns `true` but `===` returns `false`.

---

## Rubric

| Part | Points |
|---|---|
| A semantic HTML | 18 |
| B CSS layout | 22 |
| C to-do list | 28 |
| D event flow | 18 |
| E JS internals | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part B.5 — specificity</summary>

Specificity: (ID, Class, Element)
- `p`: (0,0,1)
- `.text`: (0,1,0)
- `#main-para`: (1,0,0) → wins → **red**
- `p.text`: (0,1,1)

Winner: `#main-para { color: red }`. Final color = **red**.
</details>

<details>
<summary>Part C.8 — core JS</summary>

```javascript
let tasks = [];
let nextId = 1;

function addTask(text) {
    tasks.push({ id: nextId++, text, completed: false });
    saveToStorage();
    renderTasks(currentFilter);
}

function toggleTask(id) {
    const t = tasks.find(t => t.id === id);
    if (t) { t.completed = !t.completed; saveToStorage(); renderTasks(currentFilter); }
}

function deleteTask(id) {
    tasks = tasks.filter(t => t.id !== id);
    saveToStorage();
    renderTasks(currentFilter);
}

function saveToStorage() { localStorage.setItem('tasks', JSON.stringify(tasks)); }
function loadFromStorage() {
    const raw = localStorage.getItem('tasks');
    tasks = raw ? JSON.parse(raw) : [];
    nextId = tasks.reduce((max, t) => Math.max(max, t.id), 0) + 1;
}
```
</details>

<details>
<summary>Part E.13 — var closure bug</summary>

Output: 3, 3, 3. Because `var i` is function-scoped (or global here); all three timeouts close over the same `i`, which is 3 when they run (after the loop completes).

Fix with `let`: `let` is block-scoped — each iteration gets its own `i` binding. The three closures capture separate values 0, 1, 2. Output: 0, 1, 2.
</details>
