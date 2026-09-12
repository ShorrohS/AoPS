# AoPS — Art of Problem Solving

**End-to-End Practical Computer Science Course** — from the very first punch card to advanced AI.

> "We don't teach computing. We rebuild it from scratch, one problem at a time."

---

> **📖 Autonomous Agent & Contributor Guide:**  
> All AI agents, contributors, and subagents must consult [MASTER_GUIDE.md](file:///c:/Users/ssro2/OneDrive/Desktop/Projects/eBooks/AoPS/MASTER_GUIDE.md) for the unified steering rules, curriculum map, Japanese Zen Minimalist design tokens, publishing engine instructions, and living status tracker.

---

## Course Structure

Every lesson has:
- **lesson.md** — narrative, story-first content
- **simulation.html** — self-contained browser interactive (no install needed)
- **challenge.md** — practical problem with hints and solutions

```
AoPS/
├── MASTER_GUIDE.md               ← Master autonomous agent guide & unified steering
├── .kiro/steering/               ← Course guide + design system rules
├── course/                       ← 13 Levels (0–12), 70 Modules, 70 Lessons, 70 Simulations
│   ├── level-0-before-computers/
│   ├── level-1-physical-computing/
│   ├── ...
│   └── level-12-advanced-ai/
├── illustrations/                ← 78 interactive SVG/HTML visual explanation files & gallery
├── ebook/                        ← Digital book typesetting, front matter, and volume covers
└── generate_pdf.py               ← Automated ReportLab review edition PDF generator
```

## Levels (All 13 Levels / 70 Modules Complete)

| Level | Title | Modules | Status |
|:-----:|:------|:-------:|:------:|
| 0 | Before Computers | 5 | ✅ Complete |
| 1 | Physical Computing | 6 | ✅ Complete |
| 2 | Digital Foundations | 6 | ✅ Complete |
| 3 | Machine Architecture | 5 | ✅ Complete |
| 4 | Software Foundations | 5 | ✅ Complete |
| 5 | Programming | 6 | ✅ Complete |
| 6 | Data Structures & Algorithms | 8 | ✅ Complete |
| 7 | Systems Programming | 5 | ✅ Complete |
| 8 | Networks & Protocols | 6 | ✅ Complete |
| 9 | Databases | 4 | ✅ Complete |
| 10 | Web & Application Development | 4 | ✅ Complete |
| 11 | Artificial Intelligence & ML | 5 | ✅ Complete |
| 12 | Advanced AI & Agents | 5 | ✅ Complete |

## Design System

All simulations use the **Japanese Zen Minimalist** design system (*Wabi-Sabi Precision*) — warm paper background, Sumi ink controls, Lacquer Red / Deep Indigo accents, and hard-edged Bento Box layout. See `.kiro/steering/design-system.md` and [MASTER_GUIDE.md](file:///c:/Users/ssro2/OneDrive/Desktop/Projects/eBooks/AoPS/MASTER_GUIDE.md).

## How to Use

- **Interactive Simulations:** Open any `simulation.html` directly in a browser — no server, no install, no build step.
- **Visual Illustrations:** Open `illustrations/index.html` to explore the complete visual diagram gallery.
- **Review Edition PDF:** Check `AoPS_Review_Edition_v1.pdf` or compile via `python generate_pdf.py`.
