---
inclusion: always
---

# 🎨 AoPS Design System — Modern Minimalist (HTML Simulations & Mockups)

> **Project Target:** End-to-End Practical Computer Science Course Platform (Static HTML Mockups)
> **Aesthetic Archetype:** Modern Linear Minimalist (Developer/IDE-inspired, High-Contrast Dark Mode, Precision Utility)
> **Primary Objective:** Generate production-ready, hyper-clean static HTML/CSS/JS simulations with fluid micro-interactions, smooth CSS state transitions, responsive component logic, and zero visual clutter.

---

## 1. Core Visual Philosophy

- **Elevated Utility:** Interface aesthetics draw from developer tools (Vercel, Linear, Raycast) combined with premium docs (Stripe, Tailwind).
- **Typography-Driven Hierarchy:** Structure through font sizes, weights, and monospace accenting — not decorative containers.
- **Tactile & Fluid:** Every hover, click, drawer collapse, and tab switch uses GPU-accelerated CSS transitions.
- **Content-First Dark Precision:** High contrast, deep canvas tones optimised for code readability and interactive simulations.

---

## 2. Global CSS Design Tokens — REQUIRED IN EVERY HTML FILE

Every simulation.html and mockup must define and use these root variables. Do NOT use hardcoded colour values. Do NOT use the old colour palette (`#1a1a2e`, `#16213e`, `#0f3460`, `#53d8fb`, `#4ecca3`, `#f9ca24`).

```css
:root {
  /* Canvas & Surface Colors */
  --bg-primary: #090A0F;
  --bg-secondary: #12141C;
  --bg-tertiary: #1A1D27;
  --bg-glass: rgba(18, 20, 28, 0.75);

  /* Text & Content Hierarchy */
  --text-primary: #F3F4F6;
  --text-secondary: #9CA3AF;
  --text-muted: #4B5563;

  /* Brand Accents & Interactive States */
  --accent-primary: #6366F1;
  --accent-hover: #4F46E5;
  --accent-glow: rgba(99, 102, 241, 0.15);

  /* Status Colors */
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-danger: #EF4444;
  --color-code-bg: #0D0E15;

  /* Borders & Shadows */
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-active: rgba(99, 102, 241, 0.4);
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --blur-glass: blur(12px);
  --shadow-soft: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
  --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.2);

  /* Animation Timings */
  --transition-fast: 150ms cubic-bezier(0.16, 1, 0.3, 1);
  --transition-smooth: 300ms cubic-bezier(0.16, 1, 0.3, 1);
  --transition-bounce: 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## 3. Typography Rules

- **Primary Sans-Serif:** `'Inter'`, `-apple-system`, `BlinkMacSystemFont`, `sans-serif`
- **Code / Monospace:** `'JetBrains Mono'`, `'Fira Code'`, `'SF Mono'`, `monospace`

| Style | Size | Weight | Usage |
|-------|------|--------|-------|
| Display Header | 36–48px | 700 | Hero titles, module splash |
| Section Header | 20–24px | 600 | Lesson headers, section titles |
| Body Text | 15–16px | 400 | Explanations, guides |
| Code / Logs | 13–14px | 400–500 | IDE, terminal, snippets |
| Label / Badge | 11–12px | 600 | Uppercase tags, metadata |

Load Inter and JetBrains Mono from Google Fonts in every file:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

## 4. Interaction & Motion Rules

### Button & Card Hover
```css
.card:hover {
  transform: translateY(-2px);
  border-color: var(--border-active);
  box-shadow: var(--shadow-glow);
  transition: all var(--transition-smooth);
}
```

### Tabs — Active Indicator
Use a sliding underline or filled pill background shift, never a hard border swap. The active tab gets `background: var(--accent-glow); border-bottom: 2px solid var(--accent-primary);`

### Buttons
- Primary CTA: `background: var(--accent-primary)`, `color: white`, `border-radius: var(--radius-md)`, hover shifts to `var(--accent-hover)` with `var(--shadow-glow)`
- Secondary: `background: transparent`, `border: 1px solid var(--border-subtle)`, hover shifts to `border-color: var(--border-active)`
- Danger: `background: var(--color-danger)`
- Success: `background: var(--color-success)`, `color: #000`

### Simulations & Animations
- Use CSS `@keyframes` for data flow, particle movement, state changes
- Status changes must transition smoothly — never instant colour jumps
- Canvas-based simulations: dark canvas (`var(--color-code-bg)` or `var(--bg-primary)`), draw colours from the token set

---

## 5. Structural Layout Templates

### Pattern A — Split-Screen Interactive Lesson (IDE Style)
- Left Panel (35–40%): lesson content, outline, step checklist
- Right Panel (60–65%): tabbed code editor + collapsible terminal drawer

### Pattern B — Module Dashboard / Roadmap
- Grid of interactive module cards
- Progress indicators, difficulty badges, status tags (COMPLETED / IN PROGRESS / LOCKED)
- Hover quick-view drawers

### Every simulation.html must use:
```html
<body class="ds-body">
  <header class="ds-header">...</header>
  <div class="ds-tabs">...</div>
  <main class="ds-main">
    <div class="ds-panel active" id="panel-X">...</div>
  </main>
</body>
```

---

## 6. Component Spec — Standard Elements

### Intro/Info Box
```css
.ds-intro {
  background: var(--bg-secondary);
  border: 1px solid var(--border-subtle);
  border-left: 3px solid var(--accent-primary);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-secondary);
  margin-bottom: 20px;
}
.ds-intro strong { color: var(--color-warning); }
```

### Stat / Metric Box
```css
.ds-stat {
  background: var(--bg-secondary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 14px;
  text-align: center;
}
.ds-stat-val {
  font-size: 1.8rem;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  color: var(--accent-primary);
}
.ds-stat-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: .05em; margin-top: 4px; }
```

### Truth Table
```css
.ds-table { border-collapse: collapse; width: 100%; font-size: 13px; }
.ds-table th { background: var(--bg-tertiary); color: var(--text-muted); padding: 7px 12px; border: 1px solid var(--border-subtle); font-family: 'JetBrains Mono', monospace; }
.ds-table td { padding: 7px 12px; border: 1px solid var(--border-subtle); text-align: center; font-family: 'JetBrains Mono', monospace; }
.ds-table tr.active td { background: var(--accent-glow); color: var(--text-primary); }
.val-1 { color: var(--color-success); font-weight: 700; }
.val-0 { color: var(--color-danger); }
```

### Badge / Status Tag
```css
.ds-badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; letter-spacing: .05em; text-transform: uppercase; }
.ds-badge-success { background: rgba(16,185,129,.15); color: var(--color-success); border: 1px solid rgba(16,185,129,.3); }
.ds-badge-warning { background: rgba(245,158,11,.15); color: var(--color-warning); border: 1px solid rgba(245,158,11,.3); }
.ds-badge-danger  { background: rgba(239,68,68,.15);  color: var(--color-danger);  border: 1px solid rgba(239,68,68,.3);  }
.ds-badge-accent  { background: var(--accent-glow);   color: var(--accent-primary);border: 1px solid var(--border-active); }
```

### Canvas Wrapper
```css
.ds-canvas-wrap {
  background: var(--color-code-bg);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
}
canvas { display: block; width: 100%; }
```

### Log / Terminal Output
```css
.ds-log {
  background: var(--color-code-bg);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  line-height: 1.6;
  color: var(--color-success);
  max-height: 160px;
  overflow-y: auto;
}
.ds-log-info { color: var(--accent-primary); }
.ds-log-warn { color: var(--color-warning); }
.ds-log-err  { color: var(--color-danger); }
```

---

## 7. Retrofit Rule (Applies to All Existing Files)

When regenerating or editing any existing simulation.html:

1. Replace the entire `<style>` block with the new design token system
2. Replace all old colour references with design tokens
3. Keep ALL existing JavaScript logic and canvas drawing intact — only reskin colours and layout
4. Add Google Fonts `<link>` tags to `<head>`
5. Ensure all buttons, cards, tables, tabs match the component specs above
6. Canvas draw calls: replace old palette colours with equivalent token colours:
   - `#1a1a2e` → `var(--bg-primary)` or `#090A0F`
   - `#16213e` → `var(--bg-secondary)` or `#12141C`
   - `#0f3460` → `var(--bg-tertiary)` or `#1A1D27`
   - `#53d8fb` (accent2/cyan) → `#6366F1` (accent-primary) or `#818CF8`
   - `#4ecca3` (green) → `#10B981` (color-success)
   - `#f9ca24` (yellow) → `#F59E0B` (color-warning)
   - `#e94560` (accent/red) → `#EF4444` (color-danger)
   - `#8892a4` (muted) → `#9CA3AF` (text-secondary)
   - `#2a4a7f` (border) → `rgba(255,255,255,0.08)` (border-subtle)

---

## 8. Execution Rule

**Every new simulation.html, mockup, or interactive file created for this course must strictly follow this design system.** The old palette is retired. This file governs all visual output from this point forward.

When this steering file is active, all HTML output must comply with sections 2–7 above without exception.
