---
inclusion: always
---

# 🎌 AoPS Design System — Japanese Zen Minimalist

> **Aesthetic Archetype:** Wabi-Sabi Precision — warm paper surfaces, Sumi ink controls, lacquer red accents, hard-edged bento layout
> **Primary Objective:** Premium, calm, distraction-free simulations that feel like beautifully crafted instruments, not software dashboards.

---

## 1. Core Visual Philosophy

- **Ma (間) — Negative Space:** Generous whitespace is structural, not empty. Let elements breathe.
- **Wabi-Sabi Surfaces:** Warm off-white paper tones instead of cold white. Nothing is perfectly sterile.
- **Sumi Ink Precision:** Controls, borders, and text use near-black `#1C1C1C` — like brushstrokes on paper.
- **Lacquer Accent:** The single active/highlight colour is muted Japanese red `#C82A2A` or deep indigo `#1C2D42`. Never neon.
- **Typography as Structure:** Noto Serif JP or similar provides anchor headers. Inter Light carries data readouts.

---

## 2. Global CSS Design Tokens — REQUIRED IN EVERY HTML FILE

```css
:root {
  /* Surface & Background */
  --bg-paper:     #F4F3EF;   /* Warm Stone — workspace base */
  --bg-washi:     #FDFDFD;   /* Pure Washi — component surface */
  --bg-warm:      #EEECE6;   /* Slightly deeper warm tone — hover/active bg */
  --bg-canvas:    #F8F7F3;   /* Simulation canvas base */

  /* Typography */
  --text-sumi:    #1C1C1C;   /* Sumi Ink — primary text & controls */
  --text-body:    #3A3A3A;   /* Body text */
  --text-muted:   #888880;   /* Secondary/metadata */
  --text-ghost:   #BBBBB5;   /* Disabled / placeholder */

  /* Accents */
  --accent-red:   #C82A2A;   /* Lacquer Red — active state, highlights */
  --accent-indigo:#1C2D42;   /* Deep Indigo — charts, secondary accent */
  --accent-gold:  #8B6914;   /* Antique Gold — success / completion */
  --accent-ink:   #1C1C1C;   /* Sumi Ink — interactive elements */

  /* Borders — hairline only */
  --border-hair:  #1C1C1C;   /* Primary hairline (1px solid) */
  --border-light: #D8D6CE;   /* Separator / divider */
  --border-paper: #E8E6DF;   /* Subtle structure border */

  /* Radius — hard-edged, minimal */
  --radius-none:  0px;
  --radius-xs:    2px;
  --radius-sm:    4px;

  /* Motion — deliberate, not snappy */
  --ease-out:     cubic-bezier(0.16, 1, 0.3, 1);
  --ease-inout:   cubic-bezier(0.4, 0, 0.2, 1);
  --t-fast:       120ms;
  --t-med:        240ms;
  --t-slow:       400ms;
}
```

---

## 3. Typography

Load from Google Fonts in every file:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300;400;600&family=Inter:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

| Role | Font | Size | Weight | Usage |
|------|------|------|--------|-------|
| Page Title | `'Noto Serif JP'` | 22–28px | 300 | Module name — light, elegant |
| Section Label | `'Inter'` | 11px | 500 | Uppercase, letter-spaced 0.12em |
| Body / Description | `'Inter'` | 14–15px | 300–400 | Explanatory text |
| Live Data / Numbers | `'JetBrains Mono'` | 24–36px | 300 | Real-time readouts — large, lightweight |
| Code / Log | `'JetBrains Mono'` | 12–13px | 400 | Terminal output |
| Control Labels | `'Inter'` | 12px | 400 | Slider labels, field names |

---

## 4. Layout — Bento Box System

Every simulation uses a **two-zone bento layout**:

```
┌────────────────────────────────────┬──────────────────┐
│                                    │                  │
│     SIMULATION CANVAS (65%)        │  CONTROLS (35%)  │
│     bg: var(--bg-canvas)           │  bg: var(--bg-   │
│     border: none                   │  washi)          │
│                                    │  border-left:    │
│                                    │  1px solid       │
│                                    │  var(--border-   │
│                                    │  light)          │
└────────────────────────────────────┴──────────────────┘
```

- **No border radius on panels** — hard-edged, architectural
- **No box shadows** — only hairline borders `1px solid var(--border-hair)`
- **Generous padding** — 24–32px inside panels

---

## 5. Component Specs

### Body
```css
body {
  background: var(--bg-paper);
  color: var(--text-sumi);
  font-family: 'Inter', -apple-system, sans-serif;
  font-weight: 300;
  min-height: 100vh;
  padding: 32px;
}
```

### Page Header
```css
.zen-header { margin-bottom: 32px; border-bottom: 1px solid var(--border-light); padding-bottom: 20px; }
.zen-title { font-family: 'Noto Serif JP', serif; font-size: 22px; font-weight: 300; color: var(--text-sumi); letter-spacing: -0.01em; margin-bottom: 4px; }
.zen-subtitle { font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.12em; color: var(--text-muted); }
```

### Tabs
```css
.zen-tabs { display: flex; gap: 0; border-bottom: 1px solid var(--border-light); margin-bottom: 0; }
.zen-tab {
  padding: 12px 24px; font-size: 12px; font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--text-muted); cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all var(--t-fast) var(--ease-out);
  background: transparent; border-top: none; border-left: none; border-right: none;
  user-select: none;
}
.zen-tab:hover { color: var(--text-sumi); }
.zen-tab.active {
  color: var(--accent-red);
  border-bottom: 2px solid var(--accent-red);
}
```

### Panels
```css
.zen-panel { display: none; padding: 32px 0; }
.zen-panel.active { display: block; }
```

### Intro / Info Box
```css
.zen-intro {
  border-left: 2px solid var(--accent-red);
  padding: 12px 18px;
  margin-bottom: 28px;
  font-size: 14px; line-height: 1.7;
  color: var(--text-body);
  background: transparent;
}
.zen-intro strong { color: var(--text-sumi); font-weight: 500; }
```

### Section Label (uppercase divider)
```css
.zen-label {
  font-size: 10px; font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.14em;
  color: var(--text-muted);
  margin-bottom: 12px;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--border-paper);
}
```

### Buttons
```css
.zen-btn {
  padding: 10px 24px;
  font-size: 12px; font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.1em;
  border: 1px solid var(--border-hair);
  background: var(--bg-washi);
  color: var(--text-sumi);
  cursor: pointer;
  transition: background var(--t-fast) var(--ease-out),
              color var(--t-fast) var(--ease-out);
  border-radius: var(--radius-xs);
}
.zen-btn:hover { background: var(--accent-ink); color: #FDFDFD; }
.zen-btn.primary { background: var(--accent-ink); color: #FDFDFD; }
.zen-btn.primary:hover { background: #2C2C2C; }
.zen-btn.danger { border-color: var(--accent-red); color: var(--accent-red); }
.zen-btn.danger:hover { background: var(--accent-red); color: #FDFDFD; }
.zen-btn.success { border-color: var(--accent-gold); color: var(--accent-gold); }
.zen-btn.success:hover { background: var(--accent-gold); color: #FDFDFD; }
.zen-btn-row { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin-top: 20px; }
```

### Stat / Metric Box
```css
.zen-stat {
  padding: 16px 20px;
  border: 1px solid var(--border-paper);
  background: var(--bg-washi);
}
.zen-stat-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 2rem; font-weight: 300;
  color: var(--text-sumi); line-height: 1;
  margin-bottom: 4px;
}
.zen-stat-val.accent { color: var(--accent-red); }
.zen-stat-label {
  font-size: 10px; font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--text-muted);
}
```

### Control Panel (right bento column)
```css
.zen-ctrl {
  background: var(--bg-washi);
  border-left: 1px solid var(--border-light);
  padding: 28px 24px;
}
.zen-ctrl-block { margin-bottom: 28px; padding-bottom: 28px; border-bottom: 1px solid var(--border-paper); }
.zen-ctrl-block:last-child { border-bottom: none; margin-bottom: 0; }
```

### Canvas Wrapper
```css
.zen-canvas-wrap {
  background: var(--bg-canvas);
  border: 1px solid var(--border-paper);
  border-radius: var(--radius-xs);
  overflow: hidden;
}
canvas { display: block; width: 100%; }
```

### Progress Bar
```css
.zen-progress-bg {
  height: 4px;
  background: var(--border-paper);
  border-radius: 0;
  overflow: hidden;
}
.zen-progress-fill {
  height: 100%;
  background: var(--accent-red);
  transition: width 0.1s linear;
}
```

### Log / Terminal
```css
.zen-log {
  background: var(--bg-washi);
  border: 1px solid var(--border-paper);
  padding: 14px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; line-height: 1.7;
  color: var(--text-body);
  max-height: 160px; overflow-y: auto;
}
.zen-log .log-ok   { color: var(--accent-gold); }
.zen-log .log-info { color: var(--accent-indigo); }
.zen-log .log-err  { color: var(--accent-red); }
```

### Table
```css
.zen-table { border-collapse: collapse; width: 100%; font-size: 13px; }
.zen-table th {
  background: var(--bg-warm); color: var(--text-muted);
  padding: 8px 14px; border: 1px solid var(--border-paper);
  font-family: 'Inter', sans-serif; font-size: 10px;
  text-transform: uppercase; letter-spacing: 0.1em; font-weight: 500;
  text-align: center;
}
.zen-table td {
  padding: 8px 14px; border: 1px solid var(--border-paper);
  text-align: center; font-family: 'JetBrains Mono', monospace;
  color: var(--text-body); font-size: 13px;
}
.zen-table tr.hl td { background: rgba(200, 42, 42, 0.06); color: var(--text-sumi); }
.val-1 { color: var(--accent-indigo); font-weight: 500; }
.val-0 { color: var(--text-muted); }
```

### Slider
```css
input[type=range] {
  -webkit-appearance: none; appearance: none;
  width: 100%; height: 1px;
  background: var(--border-hair); cursor: pointer; margin: 14px 0;
}
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 14px; height: 14px;
  background: var(--accent-ink);
  border-radius: 50%; cursor: grab;
  transition: background var(--t-fast) var(--ease-out);
}
input[type=range]::-webkit-slider-thumb:active { cursor: grabbing; background: var(--accent-red); }
input[type=range]:focus { outline: none; }
select, input[type=text], input[type=number] {
  background: var(--bg-washi);
  border: 1px solid var(--border-hair);
  border-radius: var(--radius-xs);
  color: var(--text-sumi);
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px; padding: 7px 10px;
}
select:focus, input:focus { outline: none; border-color: var(--accent-indigo); }
```

### Card (record, bin, deck item)
```css
.zen-card {
  background: var(--bg-washi);
  border: 1px solid var(--border-paper);
  padding: 14px;
  cursor: pointer;
  transition: border-color var(--t-fast) var(--ease-out),
              background var(--t-fast) var(--ease-out);
  border-radius: var(--radius-xs);
}
.zen-card:hover { border-color: var(--accent-ink); }
.zen-card.active { border-color: var(--accent-red); background: rgba(200,42,42,0.04); }
.zen-card.done   { border-color: var(--accent-gold); background: rgba(139,105,20,0.04); }
```

### CSS Animations
```css
@keyframes zen-fade-in {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes zen-pulse-red {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}
@keyframes zen-slide-in {
  from { transform: translateX(-8px); opacity: 0; }
  to   { transform: translateX(0);    opacity: 1; }
}
@keyframes zen-count-tick {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.08); color: var(--accent-red); }
  100% { transform: scale(1); }
}
.animate-in { animation: zen-fade-in var(--t-med) var(--ease-out) forwards; }
.animate-tick { animation: zen-count-tick 300ms var(--ease-out); }
```

---

## 6. Canvas Draw Colour Map

When drawing on HTML canvas in JavaScript, use these literal hex values (CSS variables are not accessible inside canvas):

| Semantic role | Hex value |
|--------------|-----------|
| Canvas background | `#F8F7F3` |
| Primary lines / wires (active) | `#1C1C1C` |
| Secondary wires (inactive) | `#D8D6CE` |
| Accent / highlight | `#C82A2A` |
| Success / completed | `#8B6914` |
| Particle / electron dots | `#1C2D42` |
| Panel background | `#FDFDFD` |
| Grid / tick lines | `#E8E6DF` |

---

## 7. Retrofit Colour Map (Old → New)

When converting existing files:

| Old value | New value |
|-----------|-----------|
| `#090A0F` / `#1a1a2e` (dark bg) | `#F4F3EF` |
| `#12141C` / `#16213e` (panel) | `#FDFDFD` |
| `#1A1D27` / `#0f3460` (card) | `#EEECE6` |
| `#818CF8` / `#6366F1` / `#53d8fb` (accent blue/indigo) | `#1C2D42` |
| `#10B981` / `#4ecca3` (green success) | `#8B6914` |
| `#F59E0B` / `#f9ca24` (yellow warning) | `#C82A2A` |
| `#EF4444` / `#e94560` (red danger) | `#C82A2A` |
| `#9CA3AF` / `#8892a4` (muted) | `#888880` |
| `rgba(255,255,255,0.08)` / `#2a4a7f` (border) | `#D8D6CE` |
| `#0D0E15` / `#0a0f1e` (code bg) | `#F8F7F3` |

---

## 8. Execution Rule

All Level 0 simulations use this Japanese Zen Minimalist system. Level 1+ will follow once Level 0 is confirmed. All JavaScript logic stays intact — only CSS and canvas colour strings change.
