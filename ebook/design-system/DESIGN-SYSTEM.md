# AoPS Publishing Design System
## Art of Problem Solving — Ebook Series

**Version:** 1.0  
**Theme:** Minimalistic Japanese Zen Garden  
**Scope:** All AoPS ebook levels (Level 0 through Level 12)

---

## Philosophy

The AoPS design system is built on three principles drawn from *wabi-sabi* and Japanese minimalism:

1. **Ma (間) — Negative Space is Structure.** Whitespace is not emptiness. It is the breath between ideas. Generous margins and leading create the calm that lets technical content breathe.

2. **Shibui (渋い) — Understated Beauty.** No decoration for decoration's sake. Every visual element — a rule, a tint, an indent — must earn its place by serving comprehension.

3. **Mono no Aware (物の哀れ) — Respect for Impermanence.** The content is primary. The design frame holds it with dignity but never competes with it.

---

## 1. Color Palette

### Primary Palette

| Token | Hex | Name | Usage |
|-------|-----|------|-------|
| `--ink` | `#1C1C1C` | Sumi Ink | Body text, headings, rules |
| `--paper` | `#F5F4EF` | Washi Paper | Page background |
| `--warm` | `#EEECE4` | Aged Parchment | Code blocks, callout fills |
| `--bone` | `#E8E5DC` | Bone White | Sidebar fills, subtle rules |
| `--ghost` | `#D4D0C4` | Stone Dust | Borders, dividers, captions |

### Accent Palette

| Token | Hex | Name | Usage |
|-------|-----|------|-------|
| `--indigo` | `#1C2D42` | Deep Indigo | Chapter numbers, key terms, links |
| `--lacquer` | `#C82A2A` | Lacquer Red | Alerts, important callouts, page numbers |
| `--gold` | `#8B6914` | Antique Gold | Success notes, completion markers |
| `--sage` | `#3D5B3F` | Bamboo Sage | Historical notes, going deeper callouts |
| `--slate` | `#4A5568` | Ink Wash | Secondary text, captions |

### Tint System (10% alpha overlays)

| Token | Value | Usage |
|-------|-------|-------|
| `--indigo-tint` | `rgba(28,45,66,0.08)` | Chapter opener wash |
| `--lacquer-tint` | `rgba(200,42,42,0.07)` | Warning/important fills |
| `--gold-tint` | `rgba(139,105,20,0.08)` | Key insight fills |
| `--sage-tint` | `rgba(61,91,63,0.07)` | Historical note fills |

### Forbidden Colors
Never use: neon, electric blue, bright green, hot pink, pure white backgrounds.  
Never use `#FFFFFF` as a page background — always `--paper` (`#F5F4EF`).

---

## 2. Typography Hierarchy

### Font Families

```css
/* Display / Chapter titles */
--font-display: 'Noto Serif JP', 'Noto Serif', Georgia, serif;

/* Body text */
--font-body: 'EB Garamond', 'Libre Baskerville', Georgia, serif;

/* Labels, captions, UI chrome */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

/* Code, technical, monospace */
--font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
```

### Type Scale

| Level | Element | Font | Size | Weight | Leading | Tracking |
|-------|---------|------|------|--------|---------|---------|
| T1 | Book Title | Display | 48–56px | 300 | 1.05 | −0.03em |
| T2 | Book Subtitle | Display | 22px | 300 | 1.3 | 0.08em + uppercase |
| T3 | Part Title | Display | 36px | 300 | 1.1 | −0.02em |
| T4 | Chapter Number | Sans | 11px | 600 | 1.0 | 0.20em + uppercase |
| T5 | Chapter Title | Display | 32px | 300 | 1.15 | −0.01em |
| T6 | Chapter Subtitle | Sans | 13px | 400 | 1.4 | 0.12em + uppercase |
| T7 | Section Head (H2) | Display | 22px | 400 | 1.2 | −0.01em |
| T8 | Sub-section (H3) | Sans | 13px | 600 | 1.3 | 0.1em + uppercase |
| T9 | Body Text | Body | 16–17px | 400 | 1.75 | 0 |
| T10 | Lead/Opening Para | Body | 18px | 400 italic | 1.7 | 0.01em |
| T11 | Caption | Sans | 12px | 400 | 1.5 | 0.02em |
| T12 | Figure Label | Mono | 11px | 500 | 1.3 | 0.1em + uppercase |
| T13 | Code / Inline | Mono | 14px | 400 | 1.6 | 0 |
| T14 | Code Block | Mono | 13px | 400 | 1.7 | 0 |
| T15 | Footnote | Sans | 11px | 300 | 1.55 | 0 |
| T16 | Running Head | Sans | 10px | 500 | 1.0 | 0.18em + uppercase |
| T17 | Page Number | Mono | 11px | 400 | 1.0 | 0.05em |

### Typographic Rules

- **First paragraph** after a heading: no text-indent, no paragraph spacing above
- **Subsequent paragraphs**: `text-indent: 1.4em`; no margin between paragraphs (hanging indent method)
- **Maximum line length**: 68–72 characters (680px at 17px body)
- **Widow/orphan control**: minimum 2 lines at top/bottom of column
- **Drop cap**: first letter of each chapter opening — 3 lines tall, Noto Serif JP, indigo color
- **Small caps**: used for abbreviations (CPU, IBM, HTML), person names on first mention, and running headers

---

## 3. Margin System

### Print/PDF Layout (A5: 148 × 210mm)

```
Top margin:      18mm
Bottom margin:   16mm
Inner margin:    20mm (gutter)
Outer margin:    28mm (for thumb + notes)
Header area:     8mm
Footer area:     8mm
```

### Digital/HTML Layout

```css
/* Page container */
max-width: 720px;
margin: 0 auto;
padding: 48px 64px;   /* desktop */
padding: 32px 24px;   /* tablet */
padding: 24px 16px;   /* mobile */
```

### Column Grid

```
Single column (body text):      640px max
Wide (figures, tables):         720px max
Full bleed (chapter openers):   100% viewport
Pull quote offset:              −40px left margin
```

### Spacing Scale

```css
--space-xs:   4px
--space-sm:   8px
--space-md:  16px
--space-lg:  32px
--space-xl:  64px
--space-2xl: 96px
--space-3xl: 128px
```

### Vertical Rhythm

Base unit: **8px**. All spacing, padding, and margins must be multiples of 8px.  
Body line-height: **28px** at 16px font size = 1.75.  
All measurements snap to the 28px baseline grid.

---

## 4. Chapter Opening Layout

### Structure

Every chapter opens with a dedicated page following this exact sequence:

```
[Chapter Number label — 11px sans, indigo, uppercase, letter-spaced]

[Horizontal rule — 1px, ghost color, full width]

[Chapter Title — 32px Noto Serif JP, weight 300, ink color]

[Chapter Subtitle / Epigraph — 13px sans, slate, italic, uppercase]

[Opening vignette illustration — described below]

[Opening paragraph — 18px body, italic, drop cap on first letter]

[Rule — 40px wide, 1px, centered, gold color]
```

### Chapter Number Format

```
CHAPTER ONE
───────────────────────────────────────────────
```
Use written-out ordinals: ONE, TWO, THREE, etc.  
Color: `--indigo`

### Chapter Opener Illustration

A full-width abstract ink-wash band (max height 160px) rendered as:
- Horizontal gradient from `--indigo-tint` to transparent
- Sparse Japanese-ink-style line motif (SVG, inline)
- Each chapter has a unique motif tied to its theme:
  - Ch.1 (Census): Tally marks dissolving into order
  - Ch.2 (Mechanical): Interlocking gear teeth
  - Ch.3 (Loom): Warp/weft grid pattern
  - Ch.4 (Babbage/Ada): Difference register columns
  - Ch.5 (Hollerith): Punch card hole pattern

---

## 5. Figure Styling

### Figure Anatomy

```
┌────────────────────────────────────────────────────────────────┐
│  [FIGURE LABEL: FIGURE 3.2]                                    │
│  ─────────────────────────────────────────────────────         │
│                                                                 │
│  [Figure content: screenshot, diagram, or illustration]        │
│                      600px max width                           │
│                                                                 │
│  ─────────────────────────────────────────────────────         │
│  [Figure Title: bold, 13px sans]                               │
│  [Caption: 12px sans, slate, max 600px, italic description]    │
└────────────────────────────────────────────────────────────────┘
```

### Figure Label Format

```
FIGURE 3.2
```
- Font: `--font-mono`, 11px, `--indigo`, uppercase
- Tracking: 0.12em
- Margin below: 6px

### Figure Border

```css
border: 1px solid var(--ghost);
border-radius: 2px;
background: var(--warm);
padding: 16px;
```

### Figure Caption Format

```
Figure 3.2 — The Jacquard loom reading a punch card chain.
Each hole in the card admits a needle, which raises the
corresponding warp thread. The pattern is the program.
```

- Font: `--font-sans`, 12px, `--slate`
- Style: italic
- Max-width: 600px
- Margin above: 10px

### Figure Numbering

Format: `Chapter.Figure` — e.g., Figure 1.1, Figure 3.4  
Figures are numbered sequentially within each chapter.  
Reset at each chapter.

### Simulation Figures (Special)

Simulation screenshots receive an additional `[INTERACTIVE]` badge:

```css
.fig-badge {
  font-family: var(--font-mono);
  font-size: 9px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--indigo);
  border: 1px solid var(--indigo);
  padding: 2px 8px;
  border-radius: 2px;
  margin-bottom: 8px;
  display: inline-block;
}
```

---

## 6. Callout Styling

Seven callout types. Each has a left border, tinted fill, icon, label, and body.

### Callout Anatomy

```
│ [ICON] [LABEL — 10px mono, uppercase, letter-spaced]
│
│ Body text — 14px body font, normal weight
│ Can contain inline code, bold, italic.
```

### Callout Specifications

#### 1. Historical Note 📜
```css
border-left: 3px solid var(--sage);
background: var(--sage-tint);
label-color: var(--sage);
icon: ⊕  (or custom SVG scroll)
```

#### 2. Key Insight 💡
```css
border-left: 3px solid var(--gold);
background: var(--gold-tint);
label-color: var(--gold);
icon: ◆
```

#### 3. Think About It 🤔
```css
border-left: 3px solid var(--indigo);
background: var(--indigo-tint);
label-color: var(--indigo);
icon: ◇
```

#### 4. Try It Yourself ⚙️
```css
border-left: 3px solid var(--slate);
background: var(--bone);
label-color: var(--slate);
icon: ▷
```

#### 5. Challenge 🎯
```css
border-left: 3px solid var(--lacquer);
background: var(--lacquer-tint);
label-color: var(--lacquer);
icon: ✦
```

#### 6. Deep Dive 🔬
```css
border-left: 3px solid var(--indigo);
background: var(--warm);
label-color: var(--indigo);
font: italic body
icon: ∇
```

#### 7. Future Connection 🔗
```css
border-left: 3px solid var(--gold);
background: var(--warm);
label-color: var(--gold);
icon: →
```

### Callout Spacing

```
margin-top: 32px
margin-bottom: 32px
padding: 20px 24px
```

---

## 7. Illustration Standards

### Inline Diagrams

- All diagrams rendered as **inline SVG** — no raster images for diagrams
- Stroke color: `--ink` or `--ghost` only
- Fill colors: only palette tints defined above
- Stroke width: 1px for fine lines, 1.5px for primary lines, 2px for emphasis
- Font in SVG: same as `--font-mono` for labels
- No drop shadows on diagrams

### Historical Reproductions

- Rendered as **sepia-toned** with `filter: sepia(0.4) contrast(1.05)`
- Border: 1px solid `--ghost`
- Background: `--warm`
- Caption required

### Conceptual Illustrations (Per Chapter)

Each chapter has one full-width conceptual illustration — an ink-wash style SVG placed after the chapter opener:

- Max height: 200px
- Colors: only `--ink`, `--ghost`, `--indigo`, with opacity transitions
- Style: horizontal brushstroke bands, sparse geometry, negative space dominant
- No shading gradients — flat regions with hairline borders only

### Diagram Grid

All circuit diagrams, flowcharts, and schematics follow:
- Grid unit: 16px
- Connection lines: L-shaped (no diagonal wires)
- Component boxes: min 48×32px, `--warm` fill, 1px `--ghost` border
- Signal paths: 1.5px stroke, `--ink` when active, `--ghost` when inactive

---

## 8. TOC Styling

### Table of Contents Layout

```
[Book Title — T1 size, centered]
[Subtitle — T2 size, centered]
[Rule]

CONTENTS
────────────────────────────────────────────

Preface ................................. xi
Introduction ........................... xv

PART ONE: BEFORE THE MACHINE

  Chapter One
  Why Humans Compute .................... 3

  Chapter Two
  Gears and Levers ....................... 29
  
  ...
```

### TOC Typography Rules

- Part headers: `--font-sans`, 10px, uppercase, letter-spaced, `--slate`
- Chapter numbers: `--font-sans`, 11px, uppercase, `--indigo`
- Chapter titles: `--font-display`, 14px, weight 300, `--ink`
- Page numbers: `--font-mono`, 12px, `--slate`, right-aligned with dot leaders
- Dot leaders: `content: " · · · · · · · · · "`, `--ghost` color

---

## 9. Cover Styling

### Cover Layout (A5 Portrait)

```
┌─────────────────────────────────────────────┐
│                                             │
│  [TOP: 80px indigo band]                    │
│  [AoPS logotype — white, Noto Serif JP]     │
│                                             │
│  [MAIN AREA: paper background]              │
│                                             │
│       Art of Problem Solving                │ ← T1
│                                             │
│       ─────────────                         │ ← 40px rule, indigo
│                                             │
│       Before Computers                      │ ← T3 size
│                                             │
│       The Origins of Computation            │ ← T6 size, slate
│                                             │
│  [CENTER ILLUSTRATION:                      │
│   Ink-wash abstraction of gears,            │
│   punch cards, and abacus beads             │
│   dissolving into binary dots]              │
│                                             │
│  [BOTTOM BAND: 60px warm]                   │
│  [LEVEL 0]  ←mono→  [Series Name]          │
└─────────────────────────────────────────────┘
```

### Cover Color Rules

- Background: `--paper`
- Top band: `--indigo`
- Bottom band: `--warm`
- Title: `--ink`
- Subtitle: `--indigo`
- Level badge: `--lacquer` text, `--lacquer-tint` background

### Cover Spine (Print)

- Background: `--indigo`
- Text: white, 12px Noto Serif JP
- Rotated: reading bottom-to-top
- Content: "AoPS | Before Computers | Level 0"

---

## 10. PDF Layout Rules

### Page Setup

```
Paper size: A5 (148mm × 210mm)
Bleed: 3mm all sides
Safe zone: 8mm from trim edge
Two-page spread: mirrored margins
```

### Running Headers

```
Recto (right) page: Chapter title — 10px sans, uppercase, slate, right-aligned
Verso (left) page:  Book title — 10px sans, uppercase, slate, left-aligned
Rule below header: 0.5pt, ghost color
```

### Page Numbers

```
Position: centered in footer, 12mm from bottom trim
Font: --font-mono, 11px, --slate
Format: Arabic numerals (1, 2, 3...)
Front matter: lowercase Roman (i, ii, iii...)
No page number on chapter openers, full-bleed pages
```

### Paragraph Rules

```css
/* Body text */
font-size: 10.5pt;       /* 14px equivalent in print */
line-height: 15.75pt;    /* 1.5 × 10.5 */
text-align: justify;
text-indent: 1em;        /* all but first para after heading */
hyphenation: auto;
orphans: 2;
widows: 2;
```

### Print Color

- All text: `--ink` (#1C1C1C) — prints as near-black
- Accents (`--indigo`, `--lacquer`, `--gold`, `--sage`) print in color on color print, greyscale on B&W
- B&W fallback: callout fills use 8% black tint, borders use 30% black

### Chapter Break

Each chapter begins on a recto (right-hand, odd-numbered) page.  
If preceding chapter ends on recto, insert a blank verso page.

---

## 11. Code Block Styling

```css
.code-block {
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.7;
  background: var(--warm);
  border: 1px solid var(--ghost);
  border-left: 3px solid var(--indigo);
  padding: 16px 20px;
  border-radius: 2px;
  overflow-x: auto;
  color: var(--ink);
}
```

### Inline Code

```css
code {
  font-family: var(--font-mono);
  font-size: 0.88em;
  background: var(--bone);
  border: 1px solid var(--ghost);
  padding: 1px 5px;
  border-radius: 2px;
  color: var(--indigo);
}
```

---

## 12. Table Styling

```css
.book-table {
  border-collapse: collapse;
  width: 100%;
  font-size: 14px;
  margin: 32px 0;
}
.book-table th {
  font-family: var(--font-sans);
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--slate);
  background: var(--warm);
  padding: 10px 14px;
  border-top: 1.5px solid var(--ink);
  border-bottom: 1px solid var(--ghost);
  text-align: left;
}
.book-table td {
  padding: 9px 14px;
  border-bottom: 1px solid var(--bone);
  color: var(--ink);
  vertical-align: top;
}
.book-table tr:last-child td {
  border-bottom: 1.5px solid var(--ink);
}
```

---

## 13. Pull Quote Styling

Large, impactful quotations pulled from body text.

```css
.pull-quote {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 300;
  font-style: italic;
  line-height: 1.45;
  color: var(--indigo);
  border-left: 4px solid var(--indigo);
  padding: 8px 0 8px 28px;
  margin: 48px 0 48px -4px;
}
.pull-quote cite {
  display: block;
  font-family: var(--font-sans);
  font-size: 11px;
  font-style: normal;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--slate);
  margin-top: 12px;
}
```

---

## 14. Accessibility Standards

- **Minimum contrast ratio:** 4.5:1 for body text, 3:1 for large text
- `--ink` (#1C1C1C) on `--paper` (#F5F4EF): contrast ratio 15.8:1 ✓
- `--indigo` (#1C2D42) on `--paper`: contrast ratio 12.4:1 ✓
- `--lacquer` (#C82A2A) on `--paper`: contrast ratio 5.9:1 ✓
- `--gold` (#8B6914) on `--paper`: contrast ratio 5.2:1 ✓
- Alt text required for all figures
- Semantic HTML required: `<figure>`, `<figcaption>`, `<blockquote>`, `<cite>`
- EPUB: WCAG 2.1 AA compliance

---

## 15. Design Token Quick Reference

```css
:root {
  /* Colors */
  --ink:           #1C1C1C;
  --paper:         #F5F4EF;
  --warm:          #EEECE4;
  --bone:          #E8E5DC;
  --ghost:         #D4D0C4;
  --indigo:        #1C2D42;
  --lacquer:       #C82A2A;
  --gold:          #8B6914;
  --sage:          #3D5B3F;
  --slate:         #4A5568;
  --indigo-tint:   rgba(28,45,66,0.08);
  --lacquer-tint:  rgba(200,42,42,0.07);
  --gold-tint:     rgba(139,105,20,0.08);
  --sage-tint:     rgba(61,91,63,0.07);

  /* Fonts */
  --font-display:  'Noto Serif JP', Georgia, serif;
  --font-body:     'EB Garamond', Georgia, serif;
  --font-sans:     'Inter', system-ui, sans-serif;
  --font-mono:     'JetBrains Mono', monospace;

  /* Spacing */
  --space-xs:  4px;
  --space-sm:  8px;
  --space-md:  16px;
  --space-lg:  32px;
  --space-xl:  64px;
  --space-2xl: 96px;
  --space-3xl: 128px;

  /* Typography */
  --text-body:     17px;
  --text-small:    14px;
  --text-caption:  12px;
  --text-label:    11px;
  --text-mono:     14px;

  /* Layout */
  --content-width:  720px;
  --text-width:     640px;
  --line-height:    1.75;
  --border-radius:  2px;
}
```
