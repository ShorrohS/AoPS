# Module 10.1 — HTML, CSS, and JavaScript from the Ground Up

---

## The Problem

> In 1991, Tim Berners-Lee needed a way to share documents between physicists at CERN.
> He invented three technologies that now power virtually all interactive software:
> a markup language to structure content (HTML),
> a styling language to control appearance (CSS),
> and a scripting language to add behaviour (JavaScript).
>
> Every web page — from a simple blog to a complex trading platform —
> is built from these three technologies, working together.
> Understanding them from first principles reveals
> why the modern web is the way it is, warts and all.

---

## The Story

### HTML, CSS, JavaScript: Three Accidents of History

**HTML** was designed for documents, not applications. The tags (`<h1>`, `<p>`, `<a>`) were meant to describe content structure, not visual layout. The early `<blink>` and `<marquee>` tags for visual effects were embarrassments that browsers eventually stopped supporting.

**CSS** was designed by Håkon Wium Lie (1994) to separate presentation from content. Before CSS, HTML authors used `<font>` tags, `<table>` for layout, and `bgcolor` attributes everywhere — mixing content with presentation in ways that were impossible to maintain.

**JavaScript** was invented by Brendan Eich at Netscape in **10 days** in 1995. The original goal: add simple interactivity to web pages. It was designed quickly, with deliberate Java-like syntax to appeal to Java programmers, but with dynamic typing and prototype-based objects — very different from Java. Every strange corner of JavaScript (type coercion, `this` binding, `var` hoisting) is a direct consequence of that 10-day timeline.

These three technologies were standardised by the W3C and ECMA, evolved separately, and are now deeply intertwined — the foundation of all web development.

---

## The Concept

### HTML — Structure

HTML (HyperText Markup Language) describes the *semantic structure* of content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Page</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <h1>Welcome</h1>
    <nav>
      <a href="/">Home</a>
      <a href="/about">About</a>
    </nav>
  </header>
  <main>
    <article>
      <h2>Article Title</h2>
      <p>First paragraph. <strong>Important word.</strong></p>
      <p>Second paragraph.</p>
    </article>
  </main>
  <footer>
    <p>&copy; 2026</p>
  </footer>
</body>
</html>
```

**Semantic HTML**: use the right element for the right content. `<article>` for self-contained content. `<nav>` for navigation. `<button>` for buttons (not `<div>`). `<input type="email">` for email fields. Semantic HTML improves:
- **Accessibility**: screen readers use semantics to navigate
- **SEO**: search engines weight headings and semantic elements
- **Maintainability**: clear meaning for developers

**The DOM (Document Object Model)**: the browser parses HTML and creates a tree of objects. JavaScript can read and modify this tree, dynamically updating the page.

### CSS — Presentation

CSS (Cascading Style Sheets) controls visual appearance through selectors and declarations:

```css
/* Selector: element */
h1 { color: #1C1C1C; font-size: 2rem; }

/* Selector: class */
.card { background: white; border-radius: 8px; padding: 16px; }

/* Selector: ID */
#main-nav { display: flex; gap: 24px; }

/* Selector: pseudo-class */
a:hover { text-decoration: underline; }

/* Selector: descendant */
.card p { color: #666; font-size: 0.9rem; }
```

**The Box Model**: every HTML element is a rectangular box:
```
┌─────────────────────────────────────────┐
│                 MARGIN                  │
│  ┌───────────────────────────────────┐  │
│  │             BORDER                │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │           PADDING           │  │  │
│  │  │  ┌────────────────────┐     │  │  │
│  │  │  │      CONTENT       │     │  │  │
│  │  │  └────────────────────┘     │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**Flexbox** — one-dimensional layout:
```css
.container {
  display: flex;
  justify-content: space-between;  /* horizontal distribution */
  align-items: center;             /* vertical alignment */
  gap: 16px;
}
```

**CSS Grid** — two-dimensional layout:
```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);  /* 3 equal columns */
  grid-template-rows: auto;
  gap: 24px;
}
```

**Cascade and Specificity**: when multiple rules target the same element, the most specific wins:
- Inline style: `style="color:red"` (specificity: 1000)
- ID selector: `#id` (specificity: 100)
- Class selector: `.class` (specificity: 10)
- Element selector: `p` (specificity: 1)
- `!important` overrides everything (use sparingly)

### JavaScript — Behaviour

JavaScript makes pages interactive. Core concepts:

```javascript
// Variables
let count = 0;           // block-scoped, reassignable
const PI = 3.14159;      // block-scoped, not reassignable
var legacy = "avoid";    // function-scoped, hoisted (legacy)

// Functions
function add(a, b) { return a + b; }
const multiply = (a, b) => a * b;   // arrow function

// DOM manipulation
const btn = document.querySelector('#submit-btn');
btn.addEventListener('click', function(event) {
  event.preventDefault();             // stop form submission
  const input = document.querySelector('#name');
  const message = document.querySelector('#message');
  message.textContent = `Hello, ${input.value}!`;
  message.style.color = 'green';
});

// Fetch API — HTTP requests from JavaScript
async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
  return data;
}
```

**Event-driven model**: JavaScript runs in an event loop. No blocking I/O. Events (clicks, timers, network responses) are queued and handled one at a time. This is the same model as Node.js on the server.

**Promises and async/await**:
```javascript
// Old way: callback hell
fetchUser(1, function(user) {
  fetchOrders(user.id, function(orders) {
    renderPage(user, orders);
  });
});

// Modern way: async/await
async function loadPage() {
  try {
    const user   = await fetchUser(1);
    const orders = await fetchOrders(user.id);
    renderPage(user, orders);
  } catch (err) {
    showError(err.message);
  }
}
```

### How the Three Work Together

```html
<!-- HTML: structure -->
<button id="counter-btn" class="btn-primary">
  Clicked <span id="count">0</span> times
</button>
```

```css
/* CSS: appearance */
.btn-primary {
  background: #1C2D42;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}
.btn-primary:hover { background: #2a3f5c; }
```

```javascript
// JavaScript: behaviour
let count = 0;
const btn  = document.getElementById('counter-btn');
const span = document.getElementById('count');

btn.addEventListener('click', () => {
  count++;
  span.textContent = count;
});
```

Separation of concerns: HTML defines what is there, CSS defines how it looks, JavaScript defines what it does.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — HTML/CSS/JS Live Editor**
- Three panes: HTML, CSS, JavaScript
- Changes reflect instantly in a preview pane
- Pre-loaded examples: a card component, a navigation bar, a form

**Tool 2 — DOM Inspector**
- Click any element in the preview
- See its HTML, computed CSS styles, and position in the DOM tree
- Modify values live and watch the page update

**Tool 3 — Event Flow**
- Click a nested element (button inside div inside section)
- Watch the event bubble up the DOM tree
- See how `stopPropagation()` prevents further bubbling

---

## Going Deeper

**Virtual DOM**: React, Vue, and other frameworks don't directly modify the real DOM — they maintain a virtual representation in JavaScript objects, diff it when state changes, and apply only the minimal set of real DOM changes. This is faster because DOM operations are expensive (they trigger browser layout and paint). Understanding why the virtual DOM was invented requires experiencing the performance problems of naive DOM manipulation.

**CSS preprocessors and modern tooling**: writing raw CSS for large applications is painful — no variables (before CSS custom properties), no nesting, no modules. SASS and LESS added these features as preprocessors. Modern CSS has custom properties (`--color: #1C2D42;`), nesting (in newer browsers), and `@layer` for cascade management. PostCSS transforms future CSS syntax for current browsers. Understanding the gap between what developers write and what browsers receive is essential for modern frontend work.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Build a to-do list with HTML structure, CSS styling (light/dark mode toggle), and JavaScript for add/complete/delete functionality. Implement it without any frameworks — pure HTML, CSS, and JS.
