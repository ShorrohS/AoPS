# AoPS — Art of Problem Solving

**End-to-End Practical Computer Science Course** — from the very first punch card to advanced AI.

> "We don't teach computing. We rebuild it from scratch, one problem at a time."

---

## Course Structure

Every lesson has:
- **lesson.md** — narrative, story-first content
- **simulation.html** — self-contained browser interactive (no install needed)
- **challenge.md** — practical problem with hints and solutions

```
AoPS/
├── .kiro/steering/          ← Course guide + design system rules
├── course/
│   ├── level-0-before-computers/     ← Punch cards → Babbage → Hollerith
│   ├── level-1-physical-computing/   ← Electricity → Relay → Transistor → Moore's Law
│   ├── level-2-digital-foundations/  ← Binary → Logic Gates → ALU (coming soon)
│   └── ...
```

## Levels

| Level | Title | Status |
|-------|-------|--------|
| 0 | Before Computers | ✅ Complete |
| 1 | Physical Computing | ✅ Complete (simulation.html for 1.6 pending) |
| 2–12 | Digital Foundations → Advanced AI | 🔜 In progress |

## Design System

All simulations use the **Modern Minimalist** design system — dark mode, Inter + JetBrains Mono fonts, CSS design tokens. See `.kiro/steering/design-system.md`.

## How to Use

Open any `simulation.html` directly in a browser — no server, no install, no build step.
