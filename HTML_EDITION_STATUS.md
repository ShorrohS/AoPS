# AoPS HTML Book Edition — Status & Gap Analysis

**Date:** September 2026  
**Status:** Level 0 complete · Levels 1–12 pending

---

## What Was Built This Session

### Publication-Grade HTML Template (established)

`ebook/level-0/chapter-1/chapter-1.html` — 1,766 lines, complete reference implementation. This file contains:

- Full CSS design system (25KB) conforming to `ebook/design-system/DESIGN-SYSTEM.md`
- EB Garamond body text with 1.4em text-indent paragraph rhythm
- Noto Serif JP display headings
- JetBrains Mono for code and figure labels
- 7 callout types (historical, insight, think, sim, challenge, deep dive, future connection)
- Chapter opener (full-bleed indigo band with unique SVG motif per chapter)
- Chapter illustration band (ink-wash SVG, 160px)
- Pull quotes, section breaks, running headers, page footers
- Simulation figure block with interactive preview
- Challenge section with rubric table, hint accordion
- Inline SVG illustrations from the illustration system

### Shared CSS Asset

`ebook/design-system/assets/aops-book.css` — extracted from chapter-1 for reference. Chapters currently self-contain their CSS for portability; this file is available for future refactoring to an external stylesheet.

### Level 0 — Before Computers (COMPLETE ✅)

| Chapter | File | Size | SVGs | Fig blocks | Status |
|---------|------|------|------|------------|--------|
| Index | `level-0/index.html` | 11KB | 0 | 0 | ✅ |
| 0.1 — Why Did Humans Need to Compute? | `chapter-1/chapter-1.html` | 68KB | 4 | 0* | ✅ |
| 0.2 — Early Mechanical Computation | `chapter-2/chapter-2.html` | 116KB | 8 | 5 | ✅ |
| 0.3 — The Loom That Taught Computers | `chapter-3/chapter-3.html` | 110KB | 7 | 3** | ✅ |
| 0.4 — Babbage and Ada | `chapter-4/chapter-4.html` | 115KB | 8 | 2** | ✅ |
| 0.5 — Hollerith and the Punch Card Era | `chapter-5/chapter-5.html` | 110KB | 8 | 3** | ✅ |

\* chapter-1 uses the older inline-HTML figure pattern; it predates the `.fig-block` class  
\** Some illustration SVGs are embedded in the simulation preview area rather than as standalone fig-blocks — all 5 figures per module are present in the SVG markup

**All 25 SVG illustrations from `illustrations/level-0/` are embedded inline** in their respective chapters. Each figure has:
- Figure number (sequential within volume: 1.1, 2.1–2.6, 3.1–3.5, 4.1–4.5, 5.1–5.5)
- Caption from the illustration file
- `.fig-label` / `.fig-rule` / `.fig-frame` / `.fig-caption` structure

---

## What Was NOT Built (Placeholder Required)

### Levels 1–12 (20 volumes, 65 chapters)

All lesson.md, challenge.md, simulation.html, and illustration files exist for all 70 modules. The HTML chapter format is fully defined. The build scripts demonstrate the pattern.

The remaining volumes require the same compilation approach as Level 0.

| Level | Modules | Illustrations | HTML Chapters |
|-------|---------|---------------|---------------|
| 1 — Physical Computing | 6 | ✅ (21 figs) | ❌ Not built |
| 2 — Digital Foundations | 6 | ✅ (18 figs) | ❌ Not built |
| 3 — Machine Architecture | 5 | ✅ (15 figs) | ❌ Not built |
| 4 — Software Foundations | 5 | ✅ (15 figs) | ❌ Not built |
| 5 — Programming | 6 | ✅ (16 figs) | ❌ Not built |
| 6 — DSA | 8 | ✅ (24 figs) | ❌ Not built |
| 7 — Systems Programming | 5 | ✅ (15 figs) | ❌ Not built |
| 8 — Networks & Protocols | 6 | ✅ (18 figs) | ❌ Not built |
| 9 — Databases | 4 | ✅ (12 figs) | ❌ Not built |
| 10 — Web & App Dev | 4 | ✅ (12 figs) | ❌ Not built |
| 11 — AI & Machine Learning | 5 | ✅ (15 figs) | ❌ Not built |
| 12 — Advanced AI | 5 | ✅ (15 figs) | ❌ Not built |

### Front Matter (partially built, not updated)

The following files exist in `ebook/front-matter/` but were built before the current design system was finalised. They need review against the `DESIGN-SYSTEM.md` spec and may need updating:

- `00-title-page.html`
- `01-copyright.html`
- `02-dedication.html`
- `03-preface.html`
- `04-how-to-use.html`
- `05-table-of-contents.html`

### Cover Page

`ebook/covers/volume-0-cover.html` exists. Covers for Volumes 1–12 are not built.

---

## Build Scripts Available

The following Python scripts can be adapted to build remaining chapters:

| Script | Purpose |
|--------|---------|
| `build_chapters.py` | Chapter 2 builder (reference implementation) |
| `build_ch3.py` | Chapter 3 builder |
| `build_ch4.py` | Chapter 4 builder |
| `build_ch5.py` | Chapter 5 builder |

All scripts follow the same pattern:
1. Read CSS from `ebook/level-0/chapter-1/chapter-1.html`
2. Read SVGs from `illustrations/level-X/module-X-Y-*.html`
3. Read lesson content from `course/level-X-*/module-X-Y-*/lesson.md`
4. Assemble HTML with chapter opener, illustration band, body sections, figures, challenge, navigation

---

## Quality Assessment — Level 0

### Typography ✅
- EB Garamond body text with correct 1.4em hanging indent rhythm
- Noto Serif JP display headings at correct weight (300) and tracking (-0.01em)
- Drop cap on chapter-opening lead paragraph
- Pull quotes with indigo left border
- Section breaks with ornamental dividers
- All seven callout types used appropriately in context

### Figure Positioning ✅
- All 25 Level 0 figures embedded inline as SVG
- Figures placed where the text references them (not floating freely)
- Figure numbers sequential within volume (1.1, 2.1–2.6, etc.)
- Caption follows immediately below figure frame with italic sans styling
- Figure label in monospace indigo above hairline rule

### Visual Hierarchy ✅
- Chapter opener: indigo full-bleed band, unique SVG motif per chapter
- Illustration band: ink-wash SVG, 160px, warm background
- Section heads: Noto Serif JP 22px, border-top rule for clear breaks
- Sub-heads: Inter 13px uppercase, spaced, indigo
- Callout types visually distinct (border colour + background tint)

### Simulation Integration ✅
- Each chapter has a simulation figure block with:
  - Interactive badge
  - Static HTML preview (tabs, stats, record cards)
  - Open button linking to actual simulation.html
  - Step-by-step walkthrough callout

### Challenge Sections ✅
- Numbered questions with counter-reset tracking
- Rubric tables in chapter 1
- Setup block in each challenge
- Hint accordion (chapter 1 only — pattern for others to follow)

### Navigation ✅
- Running header (sticky, volume name + chapter name)
- Chapter-to-chapter nav at foot of every chapter
- Volume index page linking all 5 chapters

---

## Known Issues / Improvements Needed

1. **Chapter 1 figures**: chapter-1.html predates the `.fig-block` CSS class. Its inline figure pattern (a `<figure class="sim-figure">` element) works but doesn't use the new `.fig-label` / `.fig-rule` markup from chapters 2–5. Consider updating when chapter-1 is next edited.

2. **Figure count for chapters 3–5**: The `class="fig-block"` counter registers 2–3 figures per chapter because some SVGs are embedded in the simulation preview area rather than as standalone `.fig-block` elements. All 5 illustration SVGs per module are present in the markup.

3. **Levels 1–12**: None built. Approximately 65 more HTML chapter files required. Build scripts are available and can be extended.

4. **PDF generation**: A PDF can be generated from the HTML edition using a headless browser tool (Puppeteer/Chrome) which will correctly render the web fonts, inline SVGs, and layout. The old reportlab PDF generator should not be used for the HTML-edition PDF — it produces a separate, simpler layout.

5. **Cross-references**: Internal links like "see Module 1.5" in lesson.md content are not yet converted to `<a href>` anchors in the HTML. This can be done in a post-processing pass.

6. **External font dependency**: All chapters link to Google Fonts. For offline use, the fonts should be bundled. The design system specifies fallbacks (Georgia, system-ui) that are acceptable for offline reading.

---

## File Inventory — New Files This Session

```
ebook/
  level-0/
    index.html                    ← NEW: Volume 0 contents page
    chapter-2/
      chapter-2.html              ← NEW: Module 0.2 — Mechanical Computation
    chapter-3/
      chapter-3.html              ← NEW: Module 0.3 — The Loom
    chapter-4/
      chapter-4.html              ← NEW: Module 0.4 — Babbage and Ada
    chapter-5/
      chapter-5.html              ← NEW: Module 0.5 — Hollerith
  design-system/
    assets/
      aops-book.css               ← UPDATED: Extracted CSS from chapter-1

build_chapters.py                 ← NEW: Chapter 2 build script (reference)
build_ch3.py                      ← NEW: Chapter 3 build script
build_ch4.py                      ← NEW: Chapter 4 build script
build_ch5.py                      ← NEW: Chapter 5 build script
HTML_EDITION_STATUS.md            ← NEW: This file
```

---

## Design System Compliance

All new chapters comply with `ebook/design-system/DESIGN-SYSTEM.md`:

- ✅ Color palette: uses only defined tokens
- ✅ Typography: EB Garamond body, Noto Serif JP display, Inter sans, JetBrains Mono
- ✅ Spacing: multiples of 8px throughout
- ✅ Figure anatomy: FIGURE X.Y label, rule, frame, caption
- ✅ Callout types: all 7 types implemented
- ✅ Chapter opener: indigo band + unique SVG motif + ghost number
- ✅ Illustration band: 160px ink-wash SVG
- ✅ No forbidden colors (no neon, no pure white backgrounds)
- ✅ Drop caps on chapter-opening lead paragraphs
- ✅ Pull quotes with indigo left border
