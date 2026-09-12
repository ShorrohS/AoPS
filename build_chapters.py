"""
AoPS HTML Book Builder — Chapters 2–5 (Level 0, Modules 0.2–0.5)
Produces publication-grade HTML following the chapter-1.html design system.
"""
import re, sys, os
from pathlib import Path

BASE = Path(r"c:\Users\NDH01061\Desktop\Kiro - Project\AoPS")

# ── Read shared CSS from chapter-1 ──────────────────────────────────────────
c1_html = (BASE / "ebook/level-0/chapter-1/chapter-1.html").read_text("utf-8", errors="replace")
css_match = re.search(r"<style>(.*?)</style>", c1_html, re.DOTALL)
SHARED_CSS = css_match.group(1) if css_match else ""

def get_svgs(illus_path):
    """Extract SVG, figid, figtitle, figcaption from an illustration HTML file."""
    html = Path(illus_path).read_text("utf-8", errors="replace")
    svgs = re.findall(r'<svg[^>]+viewBox[^>]*>.*?</svg>', html, re.DOTALL)
    figids   = re.findall(r'class="fig-id"[^>]*>\s*([^<]+)\s*<', html)
    figtitles = re.findall(r'class="fig-title"[^>]*>\s*([^<]+)\s*<', html)
    caps_raw = re.findall(r'class="fig-caption"[^>]*>(.*?)</div>', html, re.DOTALL)
    caps = [re.sub(r'<[^>]+>','',c).strip() for c in caps_raw]
    return [{"svg":svgs[i],"id":figids[i],"title":figtitles[i],"caption":caps[i] if i<len(caps) else ""}
            for i in range(min(len(svgs),len(figids)))]

def esc(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def make_figure_html(fig, fig_num_str):
    """Render a figure block in the ebook style."""
    svg_clean = fig["svg"].replace(' style="height:', ' aria-hidden="false" style="max-width:100%;height:')
    return f"""
      <!-- ── FIGURE {esc(fig["id"])} ── -->
      <figure class="fig-block" id="fig-{fig_num_str.replace('.','-').lower()}" aria-labelledby="fig-{fig_num_str.replace('.','-').lower()}-title">
        <span class="fig-label">Figure {esc(fig_num_str)}</span>
        <span class="fig-rule" role="separator"></span>
        <div class="fig-frame">
          {fig["svg"]}
        </div>
        <figcaption class="fig-caption">
          <strong id="fig-{fig_num_str.replace('.','-').lower()}-title">Figure {esc(fig_num_str)} — {esc(fig["title"])}</strong> {esc(fig["caption"])}
        </figcaption>
      </figure>"""

def chapter_head(title, module_label, volume_label, fonts_url, css):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AoPS — {esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="{fonts_url}" rel="stylesheet">
<style>
{css}

/* ── Figure block — publication style ────────────────────────────── */
.fig-block {{
  margin: var(--space-2xl) 0;
  max-width: var(--text-width);
}}
.fig-label {{
  display: block;
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--indigo);
  margin-bottom: 6px;
}}
.fig-rule {{
  display: block;
  height: 1px;
  background: var(--ghost);
  margin-bottom: 14px;
}}
.fig-frame {{
  border: 1px solid var(--ghost);
  background: var(--warm);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 10px;
}}
.fig-frame svg {{
  display: block;
  width: 100%;
  height: auto;
}}
.fig-caption {{
  font-family: var(--font-sans);
  font-size: 12px;
  font-weight: 400;
  font-style: italic;
  color: var(--slate);
  line-height: 1.6;
  max-width: 100%;
}}
.fig-caption strong {{
  font-style: normal;
  font-weight: 500;
  color: var(--ink);
  display: block;
  margin-bottom: 3px;
}}

/* ── Wide figure (full text-column width) ── */
.fig-block.wide {{
  max-width: 100%;
}}
</style>
</head>
<body>
"""

FONTS_URL = "https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@200;300;400;600&family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500&display=swap"

# ═══════════════════════════════════════════════════════════════════════════
# CHAPTER 2 — Early Mechanical Computation (Module 0.2)
# ═══════════════════════════════════════════════════════════════════════════

def build_chapter_2():
    figs = get_svgs(BASE / "illustrations/level-0/module-0-2-mechanical.html")

    html = chapter_head(
        "Chapter Two — Early Mechanical Computation",
        "Module 0.2", "Volume 0 — Before Computers",
        FONTS_URL, SHARED_CSS
    )

    html += """
<article class="book-page" aria-label="Chapter Two — Early Mechanical Computation">

  <!-- ── Running header ── -->
  <header class="running-header" role="banner">
    <span>Volume 0 — Before Computers</span>
    <span class="rh-chapter">Chapter Two</span>
  </header>

  <!-- ══════════════════════════════════════════
       CHAPTER OPENER
  ══════════════════════════════════════════ -->
  <div class="chapter-opener" role="heading" aria-level="1">

    <!-- Motif: interlocking gear teeth dissolving into binary columns -->
    <svg class="opener-motif" viewBox="0 0 720 320" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" preserveAspectRatio="xMidYMid slice">
      <!-- Gear circle abstraction — left half -->
      <g stroke="#F5F4EF" opacity="0.14">
        <!-- Large gear outline -->
        <circle cx="160" cy="160" r="100" stroke-width="1"/>
        <circle cx="160" cy="160" r="70"  stroke-width="0.7"/>
        <!-- Gear teeth (24 teeth) -->
        <g stroke-width="1.5" stroke-linecap="square">
          <line x1="160" y1="55"  x2="160" y2="38"/>
          <line x1="189" y1="60"  x2="196" y2="44"/>
          <line x1="214" y1="74"  x2="224" y2="60"/>
          <line x1="231" y1="96"  x2="244" y2="84"/>
          <line x1="240" y1="122" x2="256" y2="114"/>
          <line x1="238" y1="150" x2="256" y2="147"/>
          <line x1="226" y1="177" x2="244" y2="178"/>
          <line x1="206" y1="199" x2="220" y2="206"/>
          <line x1="182" y1="213" x2="192" y2="223"/>
          <line x1="155" y1="218" x2="160" y2="230"/>
          <line x1="128" y1="212" x2="128" y2="226"/>
          <line x1="104" y1="198" x2="98"  y2="211"/>
          <line x1="86"  y1="177" x2="75"  y2="185"/>
          <line x1="76"  y1="149" x2="63"  y2="152"/>
          <line x1="77"  y1="120" x2="62"  y2="116"/>
          <line x1="90"  y1="94"  x2="77"  y2="85"/>
          <line x1="110" y1="74"  x2="100" y2="62"/>
          <line x1="134" y1="60"  x2="128" y2="46"/>
        </g>
        <!-- Smaller meshing gear -->
        <circle cx="285" cy="130" r="42"  stroke-width="0.8"/>
        <circle cx="285" cy="130" r="28"  stroke-width="0.5"/>
        <g stroke-width="1.2" stroke-linecap="square">
          <line x1="285" y1="85"  x2="285" y2="73"/>
          <line x1="305" y1="90"  x2="311" y2="79"/>
          <line x1="320" y1="105" x2="329" y2="96"/>
          <line x1="327" y1="124" x2="338" y2="121"/>
          <line x1="323" y1="144" x2="334" y2="145"/>
          <line x1="309" y1="162" x2="318" y2="167"/>
          <line x1="290" y1="172" x2="294" y2="182"/>
          <line x1="270" y1="172" x2="268" y2="183"/>
          <line x1="253" y1="162" x2="245" y2="169"/>
          <line x1="241" y1="145" x2="231" y2="147"/>
          <line x1="241" y1="124" x2="230" y2="121"/>
          <line x1="249" y1="104" x2="241" y2="95"/>
          <line x1="264" y1="89"  x2="259" y2="78"/>
        </g>
        <!-- Axle dots -->
        <circle cx="160" cy="160" r="8" stroke-width="1"/>
        <circle cx="285" cy="130" r="5" stroke-width="0.8"/>
        <!-- Connecting shaft -->
        <line x1="160" y1="160" x2="285" y2="130" stroke-width="0.6"/>
      </g>

      <!-- Transition: gear teeth → digit columns (right half) -->
      <g stroke="#F5F4EF" stroke-width="0.5" opacity="0.1">
        <line x1="380" y1="40"  x2="680" y2="40"/>
        <line x1="380" y1="70"  x2="680" y2="70"/>
        <line x1="380" y1="100" x2="680" y2="100"/>
        <line x1="380" y1="130" x2="680" y2="130"/>
        <line x1="380" y1="160" x2="680" y2="160"/>
        <line x1="380" y1="190" x2="680" y2="190"/>
        <line x1="380" y1="220" x2="680" y2="220"/>
        <!-- Columns -->
        <line x1="420" y1="30"  x2="420" y2="240"/>
        <line x1="470" y1="30"  x2="470" y2="240"/>
        <line x1="520" y1="30"  x2="520" y2="240"/>
        <line x1="570" y1="30"  x2="570" y2="240"/>
        <line x1="620" y1="30"  x2="620" y2="240"/>
        <line x1="670" y1="30"  x2="670" y2="240"/>
      </g>
      <!-- Digit wheels (circles in columns) -->
      <g stroke="#F5F4EF" stroke-width="0.8" opacity="0.18">
        <circle cx="420" cy="100" r="14"/>
        <circle cx="470" cy="130" r="14"/>
        <circle cx="520" cy="70"  r="14"/>
        <circle cx="570" cy="160" r="14"/>
        <circle cx="620" cy="100" r="14"/>
        <circle cx="670" cy="130" r="14"/>
      </g>
      <!-- Lacquer carry accent -->
      <g fill="#C82A2A" opacity="0.4">
        <circle cx="420" cy="40"  r="3"/>
        <circle cx="470" cy="40"  r="3"/>
        <circle cx="520" cy="40"  r="3"/>
      </g>
      <text x="400" y="268" font-family="JetBrains Mono, monospace" font-size="9" fill="#F5F4EF" opacity="0.3" text-anchor="middle">carry propagation</text>

      <!-- Divider -->
      <line x1="358" y1="30" x2="358" y2="240" stroke="#F5F4EF" stroke-width="0.6" opacity="0.12"/>
    </svg>

    <div class="chapter-ghost-num" aria-hidden="true">02</div>

    <p class="chapter-num-label">Module 0.2 &nbsp;·&nbsp; Level 0 — Before Computers</p>
    <div class="chapter-rule" role="separator"></div>
    <h1 class="chapter-title">Early Mechanical<br>Computation</h1>
    <p class="chapter-subtitle">When arithmetic became a machine's job</p>

  </div>

  <!-- ══════════════════════════════════════════
       ILLUSTRATION BAND
  ══════════════════════════════════════════ -->
  <figure class="chapter-illustration" aria-label="Decorative illustration: gear wheels and digit columns representing mechanical calculators">
    <svg viewBox="0 0 672 140" fill="none" xmlns="http://www.w3.org/2000/svg" width="672" height="140" aria-hidden="true">
      <defs>
        <linearGradient id="fade-l2" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%"   stop-color="#EEECE4" stop-opacity="1"/>
          <stop offset="12%"  stop-color="#EEECE4" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="fade-r2" x1="0" y1="0" x2="1" y2="0">
          <stop offset="88%"  stop-color="#EEECE4" stop-opacity="0"/>
          <stop offset="100%" stop-color="#EEECE4" stop-opacity="1"/>
        </linearGradient>
      </defs>

      <!-- Gear abstraction -->
      <g stroke="#1C2D42" opacity="0.16">
        <circle cx="80"  cy="70" r="50" stroke-width="0.8"/>
        <circle cx="80"  cy="70" r="35" stroke-width="0.5"/>
        <circle cx="80"  cy="70" r="5"  stroke-width="0.6" fill="none"/>
        <!-- teeth -->
        <g stroke-width="1.4" stroke-linecap="square">
          <line x1="80"  y1="17"  x2="80"  y2="8"/>
          <line x1="104" y1="23"  x2="110" y2="15"/>
          <line x1="123" y1="40"  x2="131" y2="34"/>
          <line x1="132" y1="62"  x2="142" y2="60"/>
          <line x1="128" y1="85"  x2="138" y2="88"/>
          <line x1="112" y1="104" x2="119" y2="112"/>
          <line x1="90"  y1="115" x2="93"  y2="124"/>
          <line x1="66"  y1="115" x2="63"  y2="125"/>
          <line x1="45"  y1="104" x2="38"  y2="111"/>
          <line x1="29"  y1="83"  x2="20"  y2="86"/>
          <line x1="27"  y1="60"  x2="17"  y2="58"/>
          <line x1="36"  y1="38"  x2="27"  y2="31"/>
          <line x1="55"  y1="22"  x2="49"  y2="13"/>
        </g>
        <!-- Second meshing gear -->
        <circle cx="178" cy="80" r="35" stroke-width="0.8"/>
        <circle cx="178" cy="80" r="23" stroke-width="0.5"/>
        <circle cx="178" cy="80" r="4"  stroke-width="0.6" fill="none"/>
        <g stroke-width="1.2" stroke-linecap="square">
          <line x1="178" y1="42"  x2="178" y2="33"/>
          <line x1="196" y1="47"  x2="202" y2="39"/>
          <line x1="208" y1="61"  x2="216" y2="56"/>
          <line x1="213" y1="78"  x2="222" y2="77"/>
          <line x1="208" y1="95"  x2="216" y2="98"/>
          <line x1="195" y1="107" x2="201" y2="114"/>
          <line x1="178" y1="113" x2="178" y2="122"/>
          <line x1="161" y1="108" x2="156" y2="115"/>
          <line x1="149" y1="95"  x2="141" y2="99"/>
          <line x1="144" y1="78"  x2="134" y2="78"/>
          <line x1="148" y1="60"  x2="140" y2="55"/>
          <line x1="160" y1="47"  x2="154" y2="39"/>
        </g>
        <line x1="80" y1="70" x2="178" y2="80" stroke-width="0.5"/>
      </g>

      <!-- Digit columns — right side -->
      <g stroke="#1C2D42" stroke-width="0.5" opacity="0.12">
        <line x1="260" y1="20" x2="620" y2="20"/>
        <line x1="260" y1="45" x2="620" y2="45"/>
        <line x1="260" y1="70" x2="620" y2="70"/>
        <line x1="260" y1="95" x2="620" y2="95"/>
        <line x1="260" y1="120" x2="620" y2="120"/>
        <line x1="295" y1="15" x2="295" y2="130"/>
        <line x1="345" y1="15" x2="345" y2="130"/>
        <line x1="395" y1="15" x2="395" y2="130"/>
        <line x1="445" y1="15" x2="445" y2="130"/>
        <line x1="495" y1="15" x2="495" y2="130"/>
        <line x1="545" y1="15" x2="545" y2="130"/>
        <line x1="595" y1="15" x2="595" y2="130"/>
      </g>
      <!-- Wheel circles in columns -->
      <g stroke="#1C2D42" stroke-width="0.7" opacity="0.2" fill="none">
        <circle cx="295" cy="70" r="12"/>
        <circle cx="345" cy="45" r="12"/>
        <circle cx="395" cy="95" r="12"/>
        <circle cx="445" cy="70" r="12"/>
        <circle cx="495" cy="45" r="12"/>
        <circle cx="545" cy="95" r="12"/>
        <circle cx="595" cy="70" r="12"/>
      </g>
      <!-- Carry highlights -->
      <g fill="#C82A2A" opacity="0.45">
        <circle cx="295" cy="20" r="2.5"/>
        <circle cx="345" cy="20" r="2.5"/>
        <circle cx="395" cy="20" r="2.5"/>
      </g>
      <!-- Label -->
      <text x="450" y="115" font-family="JetBrains Mono, monospace" font-size="9" fill="#1C2D42" opacity="0.35" text-anchor="middle">mechanical carry — Pascal, 1642</text>

      <rect x="0"   y="0" width="60"  height="140" fill="url(#fade-l2)"/>
      <rect x="612" y="0" width="60"  height="140" fill="url(#fade-r2)"/>
    </svg>
  </figure>

  <!-- ══════════════════════════════════════════
       CHAPTER BODY
  ══════════════════════════════════════════ -->
  <main class="chapter-body">

    <!-- ── THE PROBLEM ── -->
    <section aria-labelledby="section-problem">
      <h2 class="section-head" id="section-problem" style="border-top:none;padding-top:0;margin-top:0;">The Problem</h2>

      <p class="lead drop-cap">You are a seventeenth-century merchant calculating compound interest on a substantial loan. The calculation requires multiplying numbers with six, eight, even ten digits. There are no calculators, no tables, no aids — only you, a quill, and arithmetic rules you memorised as a child.</p>

      <p class="body no-indent">A single multiplication can take thirty minutes. A mistake means starting again. You need to perform dozens of these calculations each day.</p>

      <p class="body">That frustration — routine arithmetic as an exhausting, error-prone, time-consuming labour — was the seed of mechanical computation. Long before electricity, inventors tried to solve it with <strong>gears, levers, and rotating cylinders</strong>, encoding numbers in physical positions and letting mechanical motion do the work.</p>

    </section>

    <!-- ── THE STORY ── -->
    <section aria-labelledby="section-story">
      <h2 class="section-head" id="section-story">The Story</h2>

      <h3 class="sub-head">The Abacus — External State Storage (~2400 <abbr title="Before Common Era">BC</abbr>)</h3>

      <p class="body no-indent">The abacus is not a calculator — it is a <strong>memory aid</strong>. By moving beads into positions, an operator holds intermediate results without relying on mental memory alone. The abacus offloads working memory to a physical object.</p>

      <p class="body">This idea — <em>externalising state</em>, encoding numbers in something physical that can be seen and manipulated — is the seed of all computing. Every register in a modern processor is a high-speed abacus: a device that holds a value in a physical state, readable and writeable by a mechanism.</p>

      <p class="body">A skilled abacus user can outperform a calculator on simple additions. But the abacus cannot carry its own operations. A human must perform each step. The machine holds the state; the person applies the rules.</p>

      <div class="section-break" role="separator" aria-hidden="true">
        <div class="sb-line"></div>
        <div class="sb-dot"></div><div class="sb-dot"></div><div class="sb-dot"></div>
        <div class="sb-line"></div>
      </div>

      <h3 class="sub-head">Napier's Bones — Encoded Lookup Tables (1617)</h3>

      <p class="body no-indent">John Napier, a Scottish mathematician, invented a set of multiplication rods in 1617. Each rod was engraved with a multiplication table for a single digit. Laid side by side, they reduced multi-digit multiplication to a series of additions that even a non-mathematician could perform.</p>

      <p class="body">For <code>357 × 6</code>: place rods for 3, 5, 7. Read row 6. Add the diagonal entries to get the product: 2,142. The physical arrangement of rods embeds the multiplication table in a form the human eye can assemble without mental arithmetic.</p>

      <div class="callout callout-insight" role="note" aria-label="Key Insight">
        <div class="callout-label"><span aria-hidden="true">◆</span> Key Insight</div>
        <p>Napier's Bones do not compute — they <em>encode</em> computation. The multiplication table is baked into the rods; the human assembles a pre-computed result. This is the conceptual ancestor of the lookup table — a fundamental optimisation in software. When your CPU computes a sine function using a stored table rather than evaluating the Taylor series, it is doing what Napier's Bones did in 1617.</p>
      </div>

"""

    # Insert Figure 0.2-C (Napier's Bones) here
    if len(figs) > 2:
        html += make_figure_html(figs[2], "2.1")
        html += "\n"

    html += """
      <div class="section-break" role="separator" aria-hidden="true">
        <div class="sb-line"></div>
        <div class="sb-dot"></div><div class="sb-dot"></div><div class="sb-dot"></div>
        <div class="sb-line"></div>
      </div>

      <h3 class="sub-head">Schickard's Calculating Clock — Mechanical Carry (1623)</h3>

      <p class="body no-indent">Wilhelm Schickard built the first known mechanical calculator in 1623. His "calculating clock" combined Napier-style multiplication rods with a set of wheels for addition and subtraction, including an <strong>automatic carry mechanism</strong>.</p>

      <p class="body">The carry mechanism was the critical innovation: when a digit wheel rolled from 9 to 0, it automatically advanced the next wheel by 1. This is the same principle as the carry in binary addition — the single most important operation in arithmetic, and the operation that had never before been performed by a machine without human intervention.</p>

      <p class="body">Schickard's machine was destroyed in a fire and largely forgotten. The carry mechanism survived.</p>

      <div class="section-break" role="separator" aria-hidden="true">
        <div class="sb-line"></div>
        <div class="sb-dot"></div><div class="sb-dot"></div><div class="sb-dot"></div>
        <div class="sb-line"></div>
      </div>

      <h3 class="sub-head">Pascal's Pascaline — Reliable Mechanical Carry (1642)</h3>

      <p class="body no-indent">Blaise Pascal, aged eighteen, built the <strong>Pascaline</strong> to assist his father — a tax collector overwhelmed with tedious addition and subtraction. Approximately fifty machines were built — the first mechanical calculators produced in significant quantity.</p>

      <p class="body">A series of interlocked gear wheels, each representing one decimal digit, encoded the accumulator. Turning the rightmost wheel advances it by 1. When a wheel completes a full rotation — crossing from 9 to 0 — it advances the next wheel by one notch. The carry propagates mechanically, without any human intervention, through as many wheels as necessary.</p>

      <div class="callout callout-historical" role="note" aria-label="Historical Note">
        <div class="callout-label"><span aria-hidden="true">⊕</span> Historical Note</div>
        <p>Pascal's proof was not merely mathematical — it was <em>philosophical</em>. His contemporaries believed that arithmetic required a human mind to understand what it was doing. Pascal demonstrated that a gear could add without understanding. The law of arithmetic is not in the mind — it is in the relationship between teeth. This was, in its time, a deeply unsettling insight, and Pascal knew it. He wrote about the machine in terms that anticipate arguments about artificial intelligence three centuries later.</p>
      </div>

"""

    # Insert Figure 0.2-B (carry mechanism)
    if len(figs) > 1:
        html += make_figure_html(figs[1], "2.2")
        html += "\n"

    # Insert Figure 0.2-E (Pascaline 999+1)
    if len(figs) > 4:
        html += make_figure_html(figs[4], "2.3")
        html += "\n"

    html += """
      <div class="section-break" role="separator" aria-hidden="true">
        <div class="sb-line"></div>
        <div class="sb-dot"></div><div class="sb-dot"></div><div class="sb-dot"></div>
        <div class="sb-line"></div>
      </div>

      <h3 class="sub-head">Leibniz's Stepped Reckoner — All Four Operations (1694)</h3>

      <p class="body no-indent">Gottfried Wilhelm Leibniz improved on Pascal by adding a <strong>stepped drum</strong> — a cylinder with nine teeth of varying length. By sliding the drum, you could engage one to nine teeth, effectively multiplying by any single digit via repeated addition.</p>

      <p class="body">This allowed the Stepped Reckoner to multiply and divide through repeated addition and subtraction, making it the first mechanical calculator to support all four arithmetic operations with a single cranking mechanism.</p>

      <p class="body">Leibniz had another insight that would take another 258 years to become useful: binary arithmetic. He wrote in 1679 about a system using only 0 and 1, inspired by the Chinese <em>I Ching</em>. He never connected binary to circuits. But the mathematics was there, waiting.</p>

    </section>

    <!-- ── THE CONCEPT ── -->
    <section aria-labelledby="section-concept">
      <h2 class="section-head" id="section-concept">The Concept — State and Rules in Metal</h2>

      <p class="body no-indent">Every machine in this chapter shares a single deep idea: <strong>numbers are encoded as physical positions</strong>.</p>

      <p class="body">A bead's position on a wire is a digit's value. A gear wheel's rotational position is a digit (0–9). The relationship between two meshing gears implements the addition rule. The carry mechanism implements the overflow rule. The machine does not understand addition — it <em>is</em> addition, built from metal.</p>

"""

    # Insert Figure 0.2-A (hero — two machines side by side)
    if len(figs) > 0:
        html += make_figure_html(figs[0], "2.4")
        html += "\n"

    html += """
      <p class="body">The shift from mechanical gears to electrical circuits — which happens in Level 1 — is a shift in <em>medium</em>, not in concept. A transistor's on/off state is just a gear wheel's rotational position, a billion times faster and a billion times smaller. The abstraction is identical.</p>

      <h3 class="sub-head">What Carrying Really Means</h3>

      <p class="body no-indent">The mechanical carry — when one wheel overflows and advances the next — is the physical embodiment of an arithmetic rule: when a column exceeds its base, subtract the base and add 1 to the column on the left.</p>

      <p class="body">You will encounter this rule again:</p>

      <ul style="margin: var(--space-md) 0 var(--space-md) var(--space-xl); max-width: var(--text-width); list-style: disc;">
        <li style="font-family:var(--font-body);font-size:17px;line-height:1.78;color:var(--ink);margin-bottom:8px;">In binary addition, when two 1-bits add to produce a 1-bit carry (Module 2.2)</li>
        <li style="font-family:var(--font-body);font-size:17px;line-height:1.78;color:var(--ink);margin-bottom:8px;">In the ALU carry flag, recording whether the last addition overflowed (Module 2.6)</li>
        <li style="font-family:var(--font-body);font-size:17px;line-height:1.78;color:var(--ink);">In computer overflow errors, when the result of an addition cannot fit in the available bits (Module 3.3)</li>
      </ul>

      <p class="body">The gear that clicks forward when a wheel hits 9 is the ancestor of every carry bit in every processor ever made.</p>

"""

    # Insert Figure 0.2-D (lineage table)
    if len(figs) > 3:
        html += make_figure_html(figs[3], "2.5")
        html += "\n"

    html += """
      <div class="pull-quote">
        "The shift from gears to electrons is a shift in medium, not in meaning. Computation was already there — in the teeth of a gear, in the position of a wheel."
      </div>

      <div class="callout callout-future" role="note" aria-label="Future Connection">
        <div class="callout-label"><span aria-hidden="true">→</span> Future Connection — Level 2: Digital Foundations</div>
        <p>The Pascaline's carry chain had a fatal flaw: carries propagated sequentially, one wheel at a time. Adding 999 + 1 was slower than adding 001 + 1 because each wheel had to wait for the previous carry to resolve. This "carry ripple" problem was solved in the 1950s by <strong>carry-lookahead</strong> logic — computing all carries simultaneously using Boolean algebra. You will build it in Module 2.4: Combinational Circuits.</p>
      </div>

    </section>

    <!-- ── SIMULATION ── -->
    <section aria-labelledby="section-simulation">
      <h2 class="section-head" id="section-simulation">Hands-On Exercise</h2>

      <p class="body no-indent">The simulation provides three interactive tools, corresponding to the three mechanical devices covered in this chapter. Work through them in order — the conceptual progression from lookup tables to adding machines to the carry mechanism is the same progression the field took between 1617 and 1694.</p>

      <figure class="sim-figure" aria-labelledby="sim-fig-02-caption">
        <span class="sim-figure-badge">Interactive</span>
        <span class="sim-figure-label">Figure 2.6 — Mechanical Calculator Simulator</span>

        <div class="sim-figure-frame">
          <div class="sim-preview-header">
            <div>
              <div class="sim-preview-title">Mechanical Calculator Simulator</div>
              <div class="sim-preview-subtitle">Napier's Bones · Virtual Pascaline · Stepped Reckoner</div>
            </div>
          </div>
          <div class="sim-tabs-preview" aria-hidden="true">
            <div class="sim-tab-p active">Napier's Bones</div>
            <div class="sim-tab-p">Virtual Pascaline</div>
            <div class="sim-tab-p">Stepped Reckoner</div>
          </div>
          <div class="sim-stat-row" aria-hidden="true">
            <div class="sim-stat"><div class="sim-stat-val">357</div><div class="sim-stat-label">Multiplicand</div></div>
            <div class="sim-stat"><div class="sim-stat-val">6</div><div class="sim-stat-label">Multiplier</div></div>
            <div class="sim-stat"><div class="sim-stat-val">2,142</div><div class="sim-stat-label">Product</div></div>
            <div class="sim-stat"><div class="sim-stat-val" style="font-size:14px">3 steps</div><div class="sim-stat-label">Diagonal adds</div></div>
          </div>
          <div class="sim-link-row">
            <a href="../../course/level-0-before-computers/module-0-2-mechanical/simulation.html"
               class="sim-open-btn" target="_blank" rel="noopener noreferrer"
               aria-label="Open the Mechanical Calculator Simulator">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                <path d="M2 2h8v8M10 2L2 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              Open Simulation
            </a>
            <p class="sim-note">Opens in a new tab · No installation required</p>
          </div>
        </div>

        <figcaption class="sim-figure-caption" id="sim-fig-02-caption">
          Figure 2.6 — The Mechanical Calculator Simulator. Napier's Bones: interactive rods for multiplication by diagonal addition. Virtual Pascaline: animated gear wheels with visible carry propagation. Stepped Reckoner: variable-engagement drum demonstrating all four operations.
        </figcaption>
      </figure>

      <div class="callout callout-sim" role="note" aria-label="Walkthrough">
        <div class="callout-label"><span aria-hidden="true">▷</span> Step-by-Step Walkthrough</div>
        <p><strong>Step 1 — Napier's Bones.</strong> Select rods 3, 5, 7. Read row 6. Observe the diagonal addition: 1/8 + 3/0 + 4/2 → 2,142. Verify with a different multiplier.</p>
        <p style="margin-top:8px"><strong>Step 2 — Virtual Pascaline.</strong> Dial in 999. Press Add(1). Watch the carry chain propagate from the units wheel leftward through all three wheels simultaneously. Note how all three wheels move in response to a single input.</p>
        <p style="margin-top:8px"><strong>Step 3.</strong> Add 001 to 998 in the same Pascaline and compare. The single-wheel carry is instant; the triple-wheel carry takes measurably longer. This is the carry-chain delay problem that would occupy engineers for three more centuries.</p>
      </div>

    </section>

    <!-- ── GOING DEEPER ── -->
    <section aria-labelledby="section-deeper">
      <h2 class="section-head" id="section-deeper">Going Deeper</h2>

      <div class="callout callout-deep" role="note" aria-label="Deep Dive">
        <div class="callout-label"><span aria-hidden="true">∇</span> The Carry-Chain Problem</div>
        <p>The Pascaline's carry mechanism was <em>sequential</em>: carries propagated one wheel at a time. This meant that the worst-case addition — 999,999 + 1 — took six times as long as the best case. In a six-digit machine with twenty-millisecond carry propagation per digit, the worst case took 120 milliseconds. In a modern 64-bit adder with nanosecond gates, an unoptimised ripple-carry would take 64 nanoseconds — acceptable by human standards, but too slow for a processor running at four gigahertz.</p>
        <p style="margin-top:var(--space-sm)">The solution was <strong>carry-lookahead</strong>, developed in the late 1950s: instead of waiting for each carry to ripple through, compute all carries simultaneously using combinational logic. A carry-lookahead adder computes the sum of two 64-bit numbers in two gate delays, regardless of the values. You will build it in Module 2.4.</p>
      </div>

    </section>

    <!-- ── FUTURE CONNECTION ── -->
    <div class="callout callout-future" role="note" aria-label="Future Connection">
      <div class="callout-label"><span aria-hidden="true">→</span> Future Connection — Module 0.3: The Loom That Taught Computers</div>
      <p>All the machines in this chapter had one limitation: they were <em>single-purpose</em>. The Pascaline added and subtracted. The Stepped Reckoner extended this to four operations. But neither could be programmed — neither could be redirected to a different task without hardware modification. The next chapter asks: how do you store the <em>instructions themselves</em> in a physical medium, separate from the machine that executes them?</p>
    </div>

    <!-- ── CHALLENGE ── -->
    <section aria-labelledby="challenge-heading-02" class="challenge-section">

      <header class="challenge-header">
        <div class="challenge-num" aria-hidden="true">0.2</div>
        <div class="challenge-title-block">
          <p class="challenge-overline">Challenge</p>
          <h2 class="challenge-title" id="challenge-heading-02">Gears, Bones, and Carries</h2>
          <div class="challenge-meta">
            <span class="challenge-meta-item">Calculation &amp; tracing</span>
            <span class="challenge-meta-item">20–25 minutes</span>
          </div>
        </div>
      </header>

      <div class="challenge-setup">
        <p class="challenge-setup-label">Setup</p>
        <p>Use the simulation for Parts A and B. Part C is pen-and-paper only.</p>
      </div>

      <div class="challenge-part">
        <p class="challenge-part-label"><span>Part A</span> Napier's Bones</p>
        <ol class="challenge-questions">
          <li data-sub="1"><p>Use the Napier's Bones simulation to compute <strong>347 × 6</strong>. Write out the three diagonal sums. What is the final product?</p></li>
          <li data-sub="2"><p>Compute <strong>829 × 7</strong> the same way. Verify by standard multiplication. Where (if anywhere) does the diagonal method produce more or fewer steps than the standard algorithm?</p></li>
        </ol>
      </div>

      <div class="challenge-part">
        <p class="challenge-part-label"><span>Part B</span> Pascaline Carry Trace</p>
        <ol class="challenge-questions" style="counter-reset: q-counter 2">
          <li data-sub="3"><p>In the Pascaline simulation, add <strong>798 + 203</strong>. Trace every wheel that moves. Which wheels carry, and in what sequence?</p></li>
          <li data-sub="4"><p>Now add <strong>999 + 1</strong>. How many carry events occur? Compare this to the number of carries in 001 + 1. What does this tell you about worst-case and best-case addition times?</p></li>
        </ol>
      </div>

      <div class="challenge-part">
        <p class="challenge-part-label"><span>Part C</span> The Abstraction</p>
        <ol class="challenge-questions" style="counter-reset: q-counter 4">
          <li data-sub="5"><p>In your own words (two to three sentences): what is the shared abstract structure of the Abacus, Napier's Bones, and the Pascaline? What problem does each solve, and what distinguishes them from one another?</p></li>
        </ol>
      </div>

    </section>

    <!-- ── SUMMARY ── -->
    <section aria-labelledby="summary-02" class="chapter-summary">
      <h2 class="section-head" id="summary-02" style="border-top:none;padding-top:0;margin-top:0;">Summary</h2>

      <p class="body no-indent">Four machines, four centuries, one trajectory.</p>

      <p class="body">The abacus externalised state. Napier encoded multiplication tables. Schickard automated the carry. Pascal made the carry reliable. Leibniz extended to all four operations. Each machine embedded one more rule of arithmetic into a physical mechanism, moving one step further from "human does the calculation" toward "machine does the calculation."</p>

      <p class="body">The limit they could not cross was programmability. Every machine in this chapter was purpose-built — it could perform one category of arithmetic and nothing else. The next question is not "can a machine compute?" — these machines answered that. The next question is "can a machine be <em>told what to compute</em>?" The answer comes, unexpectedly, from a silk weaving factory in Lyon.</p>

      <div class="section-break" role="separator" aria-hidden="true">
        <div class="sb-line"></div>
        <div class="sb-dot"></div><div class="sb-dot"></div><div class="sb-dot"></div>
        <div class="sb-line"></div>
      </div>

      <div class="chapter-nav">
        <div class="nav-prev">
          <p class="nav-label">Previous — Module 0.1</p>
          <p class="nav-title">← Why Did Humans Need to Compute?</p>
        </div>
        <div class="nav-next">
          <p class="nav-label">Next — Module 0.3</p>
          <p class="nav-title">The Loom That Taught Computers →</p>
        </div>
      </div>

    </section>

  </main>

  <footer class="page-footer" role="contentinfo">
    <span class="page-footer-series">AoPS — Volume 0</span>
    <span class="page-num">4</span>
  </footer>

</article>

<script>
function toggleHint(btn) {
  const id = btn.getAttribute('aria-controls');
  const box = document.getElementById(id);
  if (!box) return;
  const isOpen = box.classList.toggle('open');
  btn.setAttribute('aria-expanded', isOpen);
  const arrow = btn.querySelector('.hint-toggle-arrow');
  if (arrow) arrow.textContent = isOpen ? '↑' : '↓';
}
</script>
</body>
</html>"""

    return html

# ── Write chapter 2 ──────────────────────────────────────────────────────
out_dir = BASE / "ebook/level-0/chapter-2"
out_dir.mkdir(parents=True, exist_ok=True)
chapter2 = build_chapter_2()
(out_dir / "chapter-2.html").write_text(chapter2, "utf-8")
print(f"chapter-2.html: {len(chapter2):,} chars")
print("Done.")
