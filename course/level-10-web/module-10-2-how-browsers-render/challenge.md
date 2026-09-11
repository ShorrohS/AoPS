# Challenge 10.2 — How Browsers Render Pages

**Type:** Analysis + optimisation + reasoning  
**Estimated time:** 40–50 minutes  
**Tools needed:** browser DevTools

---

## Part A — Critical Rendering Path

1. A web page loads these resources in `<head>`:
   ```html
   <link rel="stylesheet" href="styles.css">
   <script src="app.js"></script>
   <link rel="stylesheet" href="theme.css">
   ```
   
   In what order do they block/not-block rendering? Draw a timeline showing when each resource is fetched and when rendering can begin.

2. Rewrite the above with optimal loading attributes (`async`, `defer`, `rel="preload"`). Explain what each attribute change does.

3. What is the **FOUC** (Flash of Unstyled Content) and how does CSS loading in `<head>` (render-blocking) prevent it? What would happen if CSS were loaded at the bottom of `<body>` instead?

---

## Part B — Layout Thrashing

This JavaScript code is extremely slow. Identify the problem and fix it.

```javascript
const boxes = document.querySelectorAll('.box');
for (let i = 0; i < boxes.length; i++) {
    const width  = boxes[i].offsetWidth;   // forces layout
    boxes[i].style.height = width + 'px'; // writes to DOM
}
```

4. What is "layout thrashing"? Why does this loop cause it?

5. Rewrite the loop to avoid layout thrashing by separating all reads from all writes.

6. For 1000 `.box` elements, estimate the performance difference between the thrashing version and the optimised version (in terms of layout recalculations).

---

## Part C — CSS Animation Performance

7. For each CSS property, state whether animating it triggers: (a) compositor only, (b) paint only, or (c) layout + paint + composite:
   - `transform: translateX(100px)`
   - `left: 100px`
   - `opacity: 0.5`
   - `width: 200px`
   - `background-color: red`
   - `border-radius: 50%`

8. A card component slides in from the right. Compare these two implementations:
   ```css
   /* Option A */
   .card { left: -300px; transition: left 0.3s; }
   .card.visible { left: 0; }
   
   /* Option B */
   .card { transform: translateX(-300px); transition: transform 0.3s; }
   .card.visible { transform: translateX(0); }
   ```
   Which is faster? Explain the rendering pipeline difference.

---

## Part D — Layer Promotion

9. Explain why `will-change: transform` tells the browser to promote an element to its own compositor layer. What are the costs and benefits?

10. A developer adds `will-change: transform` to every element on the page as a "performance optimisation." Why is this actually harmful?

11. Which of these elements automatically get their own compositor layer (no `will-change` needed)?
    - `position: fixed` navbar
    - `overflow: scroll` container
    - `video` element
    - `<canvas>` element
    - Regular `<div>` with `background-color`

---

## Part E — Measuring Performance

12. The browser renders at 60 fps, giving a budget of 16.67ms per frame. A JavaScript event handler takes 25ms. What visual artifact does the user see?

13. `requestAnimationFrame(callback)` schedules the callback to run just before the next paint. Why is this better than `setTimeout(callback, 16)` for animations?

14. Using the browser Performance tab, you profile a page scroll and see a long bar labelled "Recalculate Style" taking 45ms. What likely caused this? Give two specific CSS properties or operations that are expensive to recalculate.

---

## Rubric

| Part | Points |
|---|---|
| A critical rendering path | 22 |
| B layout thrashing | 22 |
| C CSS animation | 22 |
| D layer promotion | 18 |
| E performance measurement | 16 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part B.5 — fixed loop</summary>

```javascript
const boxes = document.querySelectorAll('.box');

// Phase 1: read all widths (one layout calculation)
const widths = Array.from(boxes).map(b => b.offsetWidth);

// Phase 2: write all heights (no layout recalculation between writes)
boxes.forEach((b, i) => b.style.height = widths[i] + 'px');
```

Thrashing version: 1000 elements × 2 forced layouts = 2000 layout passes. Optimised: 1 layout read + 1 style update = 2 passes total. ~1000× fewer layout recalculations.
</details>

<details>
<summary>Part C.7 — CSS properties</summary>

- `transform`: compositor only ✓ (fastest)
- `left`: layout + paint + composite (slowest — triggers full reflow)
- `opacity`: compositor only ✓ (fastest)
- `width`: layout + paint + composite (reflow)
- `background-color`: paint + composite (no layout, but repaint)
- `border-radius`: paint + composite (no layout if not affecting box model)
</details>

<details>
<summary>Part A.2 — optimal loading</summary>

```html
<link rel="preload" href="styles.css" as="style">
<link rel="stylesheet" href="styles.css">        <!-- render-blocking, but preloaded -->
<link rel="stylesheet" href="theme.css">          <!-- render-blocking -->
<script src="app.js" defer></script>              <!-- defer: fetch in parallel, execute after HTML parsed -->
```

`defer` for scripts ensures they download in parallel without blocking HTML parsing, and execute in order after the DOM is ready. `async` downloads in parallel but executes immediately when downloaded (out of order — dangerous for dependent scripts).
</details>
