# Module 10.2 — How Browsers Render Pages

---

## The Problem

> You type a URL.
> 0.5 seconds later, a fully-rendered web page appears.
> What happened?
>
> Between the DNS lookup and the pixels on screen,
> the browser does an enormous amount of work:
> network requests, parsing, style calculation,
> layout, painting, and compositing.
> Understanding this pipeline explains why some pages feel instant
> and others feel sluggish — and how to make the difference.

---

## The Story

### Browsers as the World's Most Complex Applications

The first graphical web browser, **NCSA Mosaic** (1993), was revolutionary but simple. It downloaded an HTML file, parsed it sequentially, and drew text and images on screen.

Modern browsers — Chrome, Firefox, Safari, Edge — are among the most complex software systems ever built. Chrome has over 35 million lines of code. The rendering engine alone (Blink, forked from WebKit in 2013) handles HTML5, CSS3, JavaScript ES2022, WebGL, WebAssembly, WebRTC, service workers, and hundreds of other standards.

The performance of rendering directly affects user experience. Google's research showed a 100ms delay in search results caused a 0.2% reduction in searches. Amazon found every 100ms increase in page load time cost 1% in revenue. This commercial pressure drove massive investment in browser performance optimisation.

---

## The Concept

### The Critical Rendering Path

```
1. DNS lookup
2. TCP connection + TLS handshake
3. HTTP request/response
4. Receive HTML bytes
       ↓
5. Parse HTML → DOM tree
6. Parse CSS → CSSOM tree
       ↓
7. Combine → Render Tree
       ↓
8. Layout (Reflow) — calculate position and size
       ↓
9. Paint — draw pixels for each element
       ↓
10. Composite — layer pixels onto screen
```

### Step 1–3: Network

The browser resolves the hostname via DNS, opens a TCP connection, performs a TLS handshake (for HTTPS), and sends an HTTP GET request. First byte arrives after 1–2 RTTs minimum.

**Time to First Byte (TTFB)**: how long until the browser receives the first byte of the response. Optimised by CDNs (serve from geographically closer servers) and server-side caching.

### Step 4–6: Parsing

**HTML parsing → DOM**:
The browser parses HTML incrementally as bytes arrive — it does not wait for the entire document. Parsing is deliberately error-tolerant (browsers handle malformed HTML without crashing):

```
<html><body><h1>Title</h1><p>Text</p></body></html>
```
↓
```
Document
  └── html
        └── body
              ├── h1
              │    └── "Title"
              └── p
                   └── "Text"
```

**CSS parsing → CSSOM**:
CSS is **render-blocking**: the browser cannot render any part of the page until all CSS is loaded and parsed. Why? Because any element might be affected by any CSS rule — the browser cannot start rendering until it knows the complete styles.

```css
h1 { color: red; font-size: 2rem; }
p  { color: #333; margin: 16px 0; }
```
↓
```
CSSStyleSheet
  ├── Rule: h1 → {color:red, font-size:2rem}
  └── Rule: p  → {color:#333, margin:16px 0}
```

**JavaScript is also render-blocking** (unless marked `async` or `defer`): when the HTML parser encounters a `<script>` tag, it stops parsing HTML, downloads the script, executes it, then resumes. JavaScript can modify the DOM and CSSOM, so the browser must pause to maintain consistency.

```html
<!-- Blocking: parser stops until script downloads and executes -->
<script src="app.js"></script>

<!-- async: download in parallel, execute immediately when ready -->
<script src="analytics.js" async></script>

<!-- defer: download in parallel, execute after HTML parsed -->
<script src="app.js" defer></script>
```

### Step 7: Render Tree

The render tree combines DOM + CSSOM. It includes only visible elements:
- `display: none` elements are excluded
- `visibility: hidden` elements are included (space reserved, but invisible)
- Pseudo-elements (`::before`, `::after`) are added

Each node in the render tree knows its computed styles.

### Step 8: Layout (Reflow)

The browser calculates the exact position and size of every element in the render tree. This involves:
- Computing text flow (line breaking, word wrapping)
- Resolving percentage widths relative to parent
- Computing margins, paddings, borders
- Handling flexbox/grid layout algorithms

Layout is **expensive and cascading**: changing the width of a parent may require re-laying out all its descendants. This is called **reflow**. Operations that trigger reflow include:
- Changing any CSS property that affects size or position
- Inserting or removing DOM elements
- Reading `offsetWidth`, `scrollTop`, `getBoundingClientRect()` — forces synchronous layout ("layout thrashing")

### Step 9: Paint

The browser creates drawing commands for each visible element — backgrounds, borders, text, shadows, images. This creates a list of painting operations but does not yet produce pixels.

**Layers**: elements that need to be painted independently (due to animations, `will-change`, `position: fixed`, `overflow: scroll`, etc.) are promoted to their own **compositor layer** — drawn once and cached as a texture.

### Step 10: Composite

The GPU composites (combines) all layers into the final frame. Operations handled entirely by the compositor (no layout or paint triggered):
- CSS `transform: translate/rotate/scale`
- CSS `opacity`
- CSS `filter`

This is why CSS animations of `transform` and `opacity` are smooth (60 fps) while animating `top`, `left`, or `margin` causes jank (triggers layout on every frame).

### Performance: 60fps and the 16ms Budget

The human eye perceives motion as smooth at 60 frames per second. Each frame must be rendered in **16.67ms** (1000ms ÷ 60). For a smooth animation:

- JavaScript execution: < 10ms
- Rendering pipeline: < 6ms

If JavaScript takes longer than ~50ms, users notice jank. Profile with Chrome DevTools → Performance tab.

**Key optimisations:**
- Minimise reflows: batch DOM reads and writes, use `requestAnimationFrame`
- Avoid layout thrashing: don't read and write layout properties in a loop
- Use `transform` and `opacity` for animations (compositor only)
- Use `will-change: transform` to promote elements to their own layer
- Load JavaScript `defer`red or `async`; load CSS in `<head>`

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Rendering Pipeline Visualiser**
- A sample page with HTML, CSS, and JS
- Step through: DOM construction, CSSOM construction, render tree, layout, paint, composite
- See how adding `async` to a script unblocks parsing

**Tool 2 — Reflow vs Repaint**
- Change different CSS properties on an element
- Green: compositor-only (no layout or paint)
- Yellow: repaint only (no layout)
- Red: reflow (triggers layout cascade)

**Tool 3 — Layer Inspector**
- A page with `position: fixed`, `overflow: scroll`, and `transform` elements
- See which elements get their own compositor layer and why

---

## Going Deeper

**Service Workers**: a script that runs in the background, separate from the web page, intercepting network requests. Can cache resources and serve them from cache even offline. The foundation of Progressive Web Apps (PWAs). A service worker acts as a proxy between the browser and the network — it can return cached responses, generate synthetic responses, or pass through to the real network.

**WebAssembly (WASM)**: a binary instruction format that runs in browsers at near-native speed. C, C++, Rust, and Go programs can be compiled to WASM and run in browsers — enabling applications like Figma, Google Earth, and Doom to run in the browser without plugins. WASM does not replace JavaScript — they work together. WASM handles compute-intensive tasks; JavaScript handles DOM manipulation and web APIs.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Identify which operations in a given code snippet cause layout thrashing and rewrite them to batch reads then writes, explain why `opacity` animation is faster than `height` animation, trace the full critical rendering path for loading a page with one CSS file, one JS file, and one image, and calculate the number of frames per second possible if each frame takes 20ms to render.
