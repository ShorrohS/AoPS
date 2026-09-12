"""Build Chapter 4: Babbage and Ada — The First Programmers"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from pathlib import Path

BASE = Path(r"c:\Users\NDH01061\Desktop\Kiro - Project\AoPS")
c1 = (BASE / "ebook/level-0/chapter-1/chapter-1.html").read_text("utf-8", errors="replace")
CSS = re.search(r"<style>(.*?)</style>", c1, re.DOTALL).group(1)
FONTS = "https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@200;300;400;600&family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500&display=swap"
FIG_CSS = """
.fig-block{margin:var(--space-2xl) 0;max-width:var(--text-width);}
.fig-block.wide{max-width:100%;}
.fig-label{display:block;font-family:var(--font-mono);font-size:10.5px;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:var(--indigo);margin-bottom:6px;}
.fig-rule{display:block;height:1px;background:var(--ghost);margin-bottom:14px;}
.fig-frame{border:1px solid var(--ghost);background:var(--warm);border-radius:2px;overflow:hidden;margin-bottom:10px;}
.fig-frame svg{display:block;width:100%;height:auto;}
.fig-caption{font-family:var(--font-sans);font-size:12px;font-style:italic;color:var(--slate);line-height:1.6;}
.fig-caption strong{font-style:normal;font-weight:500;color:var(--ink);display:block;margin-bottom:3px;}
"""

def get_figs(p):
    html = Path(p).read_text("utf-8", errors="replace")
    svgs = re.findall(r'<svg[^>]+viewBox[^>]*>.*?</svg>', html, re.DOTALL)
    ids   = re.findall(r'class="fig-id"[^>]*>\s*([^<]+)\s*<', html)
    titles= re.findall(r'class="fig-title"[^>]*>\s*([^<]+)\s*<', html)
    caps_raw = re.findall(r'class="fig-caption"[^>]*>(.*?)</div>', html, re.DOTALL)
    caps  = [re.sub(r'<[^>]+>','',c).strip() for c in caps_raw]
    return [{"svg":svgs[i],"id":ids[i],"title":titles[i],"cap":caps[i] if i<len(caps) else ""} for i in range(min(len(svgs),len(ids)))]

def e(s): return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def fig(f, num, wide=False):
    slug = num.replace(".","_")
    w = ' wide' if wide else ''
    return f"""
      <figure class="fig-block{w}" id="fig-{slug}" aria-labelledby="fig-{slug}-title">
        <span class="fig-label">Figure {e(num)}</span>
        <span class="fig-rule" role="separator"></span>
        <div class="fig-frame">{f["svg"]}</div>
        <figcaption class="fig-caption">
          <strong id="fig-{slug}-title">Figure {e(num)} &mdash; {e(f["title"])}</strong> {e(f["cap"])}
        </figcaption>
      </figure>"""

def sb():
    return """
      <div class="section-break" role="separator" aria-hidden="true">
        <div class="sb-line"></div><div class="sb-dot"></div><div class="sb-dot"></div><div class="sb-dot"></div><div class="sb-line"></div>
      </div>"""

figs = get_figs(BASE / "illustrations/level-0/module-0-4-babbage-ada.html")
print(f"Chapter 4 figs: {len(figs)}")

h = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AoPS &mdash; Chapter Four: Babbage and Ada</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="{FONTS}" rel="stylesheet">
<style>{CSS}{FIG_CSS}</style>
</head>
<body>
<article class="book-page">
  <header class="running-header" role="banner">
    <span>Volume 0 &mdash; Before Computers</span>
    <span class="rh-chapter">Chapter Four</span>
  </header>

  <div class="chapter-opener" role="heading" aria-level="1">
    <svg class="opener-motif" viewBox="0 0 720 320" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" preserveAspectRatio="xMidYMid slice">
      <!-- Difference Engine register columns -->
      <g stroke="#F5F4EF" opacity="0.15">
        <!-- Column shafts -->
        <g stroke-width="0.8">
          <line x1="60"  y1="30" x2="60"  y2="240"/>
          <line x1="110" y1="30" x2="110" y2="240"/>
          <line x1="160" y1="30" x2="160" y2="240"/>
          <line x1="210" y1="30" x2="210" y2="240"/>
          <line x1="260" y1="30" x2="260" y2="240"/>
        </g>
        <!-- Wheel discs on each column -->
        <g stroke-width="1">
          <circle cx="60"  cy="80"  r="16"/><circle cx="60"  cy="80"  r="8"/>
          <circle cx="60"  cy="130" r="16"/><circle cx="60"  cy="130" r="8"/>
          <circle cx="60"  cy="180" r="16"/><circle cx="60"  cy="180" r="8"/>
          <circle cx="110" cy="90"  r="16"/><circle cx="110" cy="90"  r="8"/>
          <circle cx="110" cy="145" r="16"/><circle cx="110" cy="145" r="8"/>
          <circle cx="110" cy="200" r="16"/><circle cx="110" cy="200" r="8"/>
          <circle cx="160" cy="75"  r="16"/><circle cx="160" cy="75"  r="8"/>
          <circle cx="160" cy="130" r="16"/><circle cx="160" cy="130" r="8"/>
          <circle cx="210" cy="85"  r="16"/><circle cx="210" cy="85"  r="8"/>
          <circle cx="210" cy="140" r="16"/><circle cx="210" cy="140" r="8"/>
          <circle cx="260" cy="95"  r="16"/><circle cx="260" cy="95"  r="8"/>
        </g>
        <!-- Digit labels on wheels -->
        <g fill="#F5F4EF" opacity="0.4" font-family="JetBrains Mono, monospace" font-size="9" text-anchor="middle">
          <text x="60"  y="84">7</text><text x="60"  y="134">2</text><text x="60"  y="184">0</text>
          <text x="110" y="94">4</text><text x="110" y="149">1</text><text x="110" y="204">3</text>
          <text x="160" y="79">9</text><text x="160" y="134">6</text>
          <text x="210" y="89">5</text><text x="210" y="144">8</text>
          <text x="260" y="99">2</text>
        </g>
        <!-- Carry rods (horizontal connections) -->
        <g stroke-width="0.5" opacity="0.5">
          <line x1="60" y1="128" x2="110" y2="128"/>
          <line x1="110" y1="143" x2="160" y2="143"/>
          <line x1="160" y1="128" x2="210" y2="128"/>
        </g>
      </g>
      <!-- Difference table (right) — Ada's algorithm -->
      <g stroke="#F5F4EF" stroke-width="0.5" opacity="0.12">
        <line x1="340" y1="50"  x2="660" y2="50"/>
        <line x1="340" y1="80"  x2="660" y2="80"/>
        <line x1="340" y1="110" x2="660" y2="110"/>
        <line x1="340" y1="140" x2="660" y2="140"/>
        <line x1="340" y1="170" x2="660" y2="170"/>
        <line x1="340" y1="200" x2="660" y2="200"/>
        <line x1="380" y1="40"  x2="380" y2="220"/>
        <line x1="460" y1="40"  x2="460" y2="220"/>
        <line x1="540" y1="40"  x2="540" y2="220"/>
        <line x1="620" y1="40"  x2="620" y2="220"/>
      </g>
      <!-- Lacquer accent — diff values -->
      <g fill="#C82A2A" opacity="0.4">
        <circle cx="380" cy="65"  r="3"/><circle cx="460" cy="50"  r="3"/>
        <circle cx="540" cy="65"  r="3"/><circle cx="620" cy="50"  r="3"/>
      </g>
      <g fill="#F5F4EF" opacity="0.3" font-family="JetBrains Mono, monospace" font-size="8" text-anchor="middle">
        <text x="380" y="68">41</text><text x="380" y="98">43</text><text x="380" y="128">47</text>
        <text x="460" y="68">2</text><text x="460" y="98">4</text><text x="460" y="128">6</text>
        <text x="540" y="68">2</text><text x="540" y="98">2</text>
      </g>
      <text x="155" y="265" font-family="JetBrains Mono, monospace" font-size="8" fill="#F5F4EF" opacity="0.25" text-anchor="middle">Difference Engine registers</text>
      <text x="500" y="265" font-family="JetBrains Mono, monospace" font-size="8" fill="#F5F4EF" opacity="0.25" text-anchor="middle">finite differences &mdash; Ada's algorithm</text>
    </svg>
    <div class="chapter-ghost-num" aria-hidden="true">04</div>
    <p class="chapter-num-label">Module 0.4 &nbsp;&middot;&nbsp; Level 0 &mdash; Before Computers</p>
    <div class="chapter-rule" role="separator"></div>
    <h1 class="chapter-title">Babbage and Ada:<br>The First Programmers</h1>
    <p class="chapter-subtitle">The design of a general-purpose computer, a century before electronics</p>
  </div>

  <figure class="chapter-illustration" aria-label="Decorative: Difference Engine register columns with finite differences table">
    <svg viewBox="0 0 672 140" fill="none" xmlns="http://www.w3.org/2000/svg" width="672" height="140" aria-hidden="true">
      <defs>
        <linearGradient id="fl4" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="#EEECE4" stop-opacity="1"/><stop offset="12%" stop-color="#EEECE4" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="fr4" x1="0" y1="0" x2="1" y2="0">
          <stop offset="88%" stop-color="#EEECE4" stop-opacity="0"/><stop offset="100%" stop-color="#EEECE4" stop-opacity="1"/>
        </linearGradient>
      </defs>
      <!-- Register columns -->
      <g stroke="#1C2D42" stroke-width="0.5" opacity="0.15">
        <line x1="70"  y1="15" x2="70"  y2="130"/><line x1="110" y1="15" x2="110" y2="130"/>
        <line x1="150" y1="15" x2="150" y2="130"/><line x1="190" y1="15" x2="190" y2="130"/>
        <line x1="230" y1="15" x2="230" y2="130"/>
      </g>
      <g stroke="#1C2D42" stroke-width="0.8" opacity="0.2" fill="none">
        <circle cx="70"  cy="40" r="12"/><circle cx="70"  cy="80" r="12"/><circle cx="70"  cy="115" r="12"/>
        <circle cx="110" cy="50" r="12"/><circle cx="110" cy="90" r="12"/>
        <circle cx="150" cy="40" r="12"/><circle cx="150" cy="85" r="12"/>
        <circle cx="190" cy="55" r="12"/><circle cx="230" cy="45" r="12"/>
      </g>
      <!-- Difference table right -->
      <g stroke="#1C2D42" stroke-width="0.4" opacity="0.12">
        <line x1="300" y1="25" x2="600" y2="25"/><line x1="300" y1="50" x2="600" y2="50"/>
        <line x1="300" y1="75" x2="600" y2="75"/><line x1="300" y1="100" x2="600" y2="100"/>
        <line x1="300" y1="125" x2="600" y2="125"/>
        <line x1="335" y1="18" x2="335" y2="132"/><line x1="415" y1="18" x2="415" y2="132"/>
        <line x1="495" y1="18" x2="495" y2="132"/><line x1="575" y1="18" x2="575" y2="132"/>
      </g>
      <g fill="#1C2D42" opacity="0.28" font-family="JetBrains Mono, monospace" font-size="9" text-anchor="middle">
        <text x="335" y="40">41</text><text x="335" y="65">43</text><text x="335" y="90">47</text><text x="335" y="115">53</text>
        <text x="415" y="40">2</text><text x="415" y="65">4</text><text x="415" y="90">6</text>
        <text x="495" y="40">2</text><text x="495" y="65">2</text>
      </g>
      <g fill="#C82A2A" opacity="0.45">
        <circle cx="335" cy="25" r="2.5"/><circle cx="495" cy="25" r="2.5"/>
      </g>
      <text x="150"  y="132" font-family="JetBrains Mono, monospace" font-size="8" fill="#1C2D42" opacity="0.35" text-anchor="middle">Difference Engine, 1822</text>
      <text x="455"  y="132" font-family="JetBrains Mono, monospace" font-size="8" fill="#1C2D42" opacity="0.35" text-anchor="middle">finite differences &mdash; constant second diff = 2</text>
      <rect x="0"   y="0" width="60"  height="140" fill="url(#fl4)"/>
      <rect x="612" y="0" width="60"  height="140" fill="url(#fr4)"/>
    </svg>
  </figure>

  <main class="chapter-body">

    <section aria-labelledby="sect-prob4">
      <h2 class="section-head" id="sect-prob4" style="border-top:none;padding-top:0;margin-top:0;">The Problem</h2>
      <p class="lead drop-cap">You are an astronomer in 1820. You need a table of logarithms accurate to twenty decimal places. The only way to produce it: hire a room full of human computers to calculate each value by hand and have another room check their work.</p>
      <p class="body no-indent">Charles Babbage receives such a table, sits down to check it, and finds error after error. He slams it on the desk and says to his colleague:</p>
      <p class="body no-indent" style="font-family:var(--font-display);font-size:19px;font-weight:300;font-style:italic;color:var(--indigo);text-indent:0;margin:var(--space-lg) 0;">&ldquo;I wish to God these calculations had been executed by steam.&rdquo;</p>
      <p class="body no-indent">That frustration launched forty years of obsessive work &mdash; and produced the first complete design of a general-purpose programmable computer, a century before electronics made it practical.</p>
    </section>

    <section aria-labelledby="sect-story4">
      <h2 class="section-head" id="sect-story4">The Story</h2>

      <h3 class="sub-head">The Difference Engine &mdash; 1822</h3>
      <p class="body no-indent">Babbage&rsquo;s first machine, the <strong>Difference Engine</strong>, was designed to compute polynomial functions using the method of <strong>finite differences</strong>.</p>
      <p class="body">Almost every useful mathematical table &mdash; logarithms, trigonometric functions, astronomical positions &mdash; can be approximated by a polynomial. Polynomials have a beautiful property: if you take successive differences of their values, you eventually reach a constant. For <em>f</em>(<em>n</em>) = <em>n</em>&sup2; + <em>n</em> + 41 at <em>n</em> = 0, 1, 2, 3&hellip;: the values are 41, 43, 47, 53, 61, 71&hellip; The first differences are 2, 4, 6, 8, 10&hellip; The second differences are always 2.</p>
      <p class="body">So to compute the <em>next</em> value of <em>f</em>(<em>n</em>), you only ever need to <strong>add</strong> &mdash; no multiplication required. Babbage&rsquo;s Difference Engine encoded this: columns of gear wheels, each representing one &ldquo;order&rdquo; of difference. Turn a crank; the next value computes automatically.</p>
"""

h += fig(figs[1], "4.1") if len(figs) > 1 else ""

h += """
      <div class="callout callout-historical" role="note" aria-label="Historical Note">
        <div class="callout-label"><span aria-hidden="true">&oplus;</span> Historical Note</div>
        <p>Babbage began construction in 1823 with British government funding. After a decade and &pound;17,000 (millions in today&rsquo;s money), the machine was abandoned. The manufacturing precision required was beyond what 1830s toolmaking could deliver. Parts didn&rsquo;t fit. The project collapsed. A complete Difference Engine No. 2 was finally built by the Science Museum in London in <strong>1991</strong> using Babbage&rsquo;s original drawings &mdash; and it worked perfectly.</p>
      </div>"""

h += sb()

h += """
      <h3 class="sub-head">The Analytical Engine &mdash; General-Purpose (1837 onward)</h3>
      <p class="body no-indent">Before the Difference Engine was even finished, Babbage&rsquo;s mind had already moved on to something far more ambitious: the <strong>Analytical Engine</strong>, a general-purpose mechanical computer.</p>
      <p class="body">Its design, completed in 1837, included:</p>
"""

h += fig(figs[0], "4.2", wide=True) if len(figs) > 0 else ""

h += """
      <span class="table-label">Table 4.1</span>
      <div class="table-wrap">
        <table class="book-table" role="table" aria-label="Babbage's Analytical Engine vs modern Von Neumann architecture">
          <thead><tr><th scope="col">Component</th><th scope="col">Babbage&rsquo;s name (1837)</th><th scope="col">Modern equivalent</th></tr></thead>
          <tbody>
            <tr><td>Memory for 1,000 numbers of 50 digits</td><td class="mono">The Store</td><td><abbr title="Random Access Memory">RAM</abbr></td></tr>
            <tr><td>Computing unit</td><td class="mono">The Mill</td><td><abbr title="Central Processing Unit">CPU</abbr> / <abbr title="Arithmetic Logic Unit">ALU</abbr></td></tr>
            <tr><td>Input via punch cards</td><td class="mono">Operation + Variable cards</td><td>Instruction + data memory</td></tr>
            <tr><td>Conditional branching</td><td class="mono">Conditional lever</td><td><code>if</code> statement / branch instruction</td></tr>
            <tr><td>Looping</td><td class="mono">Backing up the cards</td><td>Loops / iteration</td></tr>
            <tr class="highlight"><td>Printing output</td><td class="mono">The Printing Apparatus</td><td>Output device</td></tr>
          </tbody>
        </table>
      </div>
      <p class="table-caption">Table 4.1 &mdash; The Analytical Engine&rsquo;s architecture, mapped to modern computing concepts. Babbage designed all of this in 1837. The Von Neumann architecture &mdash; which every computer since 1945 has used &mdash; is structurally identical.</p>

      <p class="body">Point five in the table is the key. A machine that can only follow a fixed sequence is a calculator. A machine that can <em>decide</em> &mdash; take this branch if the result is zero, that branch if it isn&rsquo;t &mdash; is a computer. Babbage designed that decision in 1837. Every <code>if</code> statement you will ever write is the direct descendant of his conditional lever.</p>

      <div class="callout callout-historical" role="note" aria-label="Historical Note">
        <div class="callout-label"><span aria-hidden="true">&oplus;</span> Historical Note</div>
        <p>The Analytical Engine was never built. Babbage couldn&rsquo;t raise funding, couldn&rsquo;t get government support after the Difference Engine debacle, and spent his remaining years revising the design. He died in 1871 with the machine unbuilt. He left behind thousands of engineering drawings and the most sophisticated mechanical computing design in human history.</p>
      </div>"""

h += sb()

h += """
      <h3 class="sub-head">Ada Lovelace &mdash; The First Programmer</h3>
      <p class="body no-indent">In 1842, an Italian mathematician named Luigi Menabrea published a paper describing the Analytical Engine in French, based on lectures Babbage gave in Turin. A young English mathematician &mdash; <strong>Augusta Ada King, Countess of Lovelace</strong> &mdash; was asked to translate it.</p>
      <p class="body">Ada did not just translate. She added her own <strong>Notes</strong>, labeled A through G, that were three times longer than the original paper.</p>
      <p class="body"><strong>Note G</strong> is the most famous document in the history of computing. It contains the first published algorithm intended to be executed by a machine: a procedure for computing Bernoulli numbers using the Analytical Engine. It demonstrates a complete understanding of what an algorithm <em>is</em>: a finite sequence of unambiguous steps that can be mechanically followed. And it contains a visionary observation: <em>&ldquo;The Engine might act upon other things besides number&hellip; the Engine might compose elaborate and scientific pieces of music of any degree of complexity or extent.&rdquo;</em></p>
"""

h += fig(figs[2], "4.3") if len(figs) > 2 else ""

h += """
      <p class="body">Ada understood something Babbage never fully articulated: the Engine&rsquo;s operations were not fundamentally about <em>numbers</em> &mdash; they were about <em>symbols</em> that could represent anything. This insight took the field another century to catch up to.</p>

      <div class="callout callout-insight" role="note" aria-label="Key Insight">
        <div class="callout-label"><span aria-hidden="true">&#9670;</span> Key Insight</div>
        <p>Ada&rsquo;s algorithm for Bernoulli numbers uses variables stored in the Store (memory locations), arithmetic operations in the Mill (the <abbr title="Arithmetic Logic Unit">ALU</abbr>), a looping structure (repeating a set of operations), and a sequence of operation cards (the program). It is, by every meaningful definition, a program. The person who wrote it was, by every meaningful definition, a programmer.</p>
      </div>
    </section>

    <section aria-labelledby="sect-concept4">
      <h2 class="section-head" id="sect-concept4">The Concept &mdash; Calculator vs Computer</h2>
      <p class="body no-indent">The Difference Engine was not a computer. It was a sophisticated calculator &mdash; it could do one thing (polynomial tabulation) and could not be redirected to a different task.</p>
      <p class="body">The Analytical Engine <em>was</em> a computer. It had input, storage, processing, output, conditional execution, and loops. The decisive feature is conditional execution: the ability to take different actions based on the result of a computation. That is what separates a machine that follows a fixed path from a machine that can <em>reason about its own output</em>.</p>
"""

h += fig(figs[3], "4.4", wide=True) if len(figs) > 3 else ""

h += """
      <h3 class="sub-head">What &ldquo;Algorithm&rdquo; Means</h3>
      <p class="body no-indent">Ada used this word &mdash; from al-Khwarizmi, the ninth-century Persian mathematician whose name gave us &ldquo;algorithm&rdquo; &mdash; to describe a precise, finite, unambiguous sequence of steps that can be followed mechanically to produce a result.</p>
      <p class="body">An algorithm is: <strong>finite</strong> (it terminates); <strong>precise</strong> (each step is unambiguous); <strong>general</strong> (it works for any valid input, not just one specific case); and <strong>effective</strong> (each step can actually be carried out). This definition has not changed in 185 years. Every function you will ever write is an algorithm.</p>

      <div class="pull-quote">
        &ldquo;The Analytical Engine has no power of originating anything. It can only do what we know how to order it to perform.&rdquo;
        <cite>&mdash; Ada Lovelace, Note G, 1843</cite>
      </div>

      <div class="callout callout-future" role="note" aria-label="Future Connection">
        <div class="callout-label"><span aria-hidden="true">&rarr;</span> Future Connection &mdash; Level 3: Machine Architecture</div>
        <p>Babbage&rsquo;s Store + Mill + conditional branch is the Von Neumann architecture (1945), a century before Von Neumann wrote it down. When you study Module 3.2 (The Fetch-Decode-Execute Cycle), you will be learning the electronic implementation of what Babbage drew in mechanical gears. The architecture did not change &mdash; only the medium.</p>
      </div>
    </section>

    <section aria-labelledby="sect-sim4">
      <h2 class="section-head" id="sect-sim4">Hands-On Exercise</h2>
      <p class="body no-indent">The simulation implements a simplified virtual Analytical Engine with two tools: a Difference Engine that steps through polynomial calculations, and a minimal Analytical Engine emulator with a Store, Mill, and operation card editor. Ada&rsquo;s Bernoulli algorithm is pre-loaded as an example.</p>

      <figure class="sim-figure" aria-labelledby="sim4-cap">
        <span class="sim-figure-badge">Interactive</span>
        <span class="sim-figure-label">Figure 4.5 &mdash; Virtual Analytical Engine</span>
        <div class="sim-figure-frame">
          <div class="sim-preview-header">
            <div><div class="sim-preview-title">Virtual Analytical Engine</div><div class="sim-preview-subtitle">Difference Engine &middot; Analytical Engine emulator &middot; Ada&rsquo;s algorithm</div></div>
          </div>
          <div class="sim-tabs-preview" aria-hidden="true">
            <div class="sim-tab-p active">Difference Engine</div>
            <div class="sim-tab-p">Analytical Engine</div>
            <div class="sim-tab-p">Ada&rsquo;s Algorithm</div>
          </div>
"""

if len(figs) > 4:
    h += f'          <div style="margin:10px 0;border:1px solid var(--ghost);border-radius:2px;overflow:hidden;">{figs[4]["svg"]}</div>\n'

h += """
          <div class="sim-link-row">
            <a href="../../course/level-0-before-computers/module-0-4-babbage-ada/simulation.html" class="sim-open-btn" target="_blank" rel="noopener noreferrer">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2 2h8v8M10 2L2 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              Open Simulation
            </a>
            <p class="sim-note">Opens in a new tab &middot; No installation required</p>
          </div>
        </div>
        <figcaption class="sim-figure-caption" id="sim4-cap">Figure 4.5 &mdash; Virtual Analytical Engine. Difference Engine tab: enter polynomial coefficients and step through successive differences. Analytical Engine tab: write operation card sequences and watch the Store update step by step. Ada&rsquo;s Algorithm tab: run the pre-loaded Bernoulli number program and observe each Store variable change.</figcaption>
      </figure>

      <div class="callout callout-sim" role="note" aria-label="Walkthrough">
        <div class="callout-label"><span aria-hidden="true">&#9655;</span> Step-by-Step Walkthrough</div>
        <p><strong>Step 1 &mdash; Difference Engine.</strong> Enter coefficients for <em>f</em>(<em>n</em>) = <em>n</em>&sup2; (a = 1, b = 0, c = 0). Step through the calculation. Observe that after two steps, the second differences are always 2 &mdash; the engine computes the next value using only addition from that point on.</p>
        <p style="margin-top:8px"><strong>Step 2 &mdash; Analytical Engine.</strong> The Store has 10 variables (V0&ndash;V9). Write a simple two-instruction program: ADD V0 V1 &rarr; V2 (add V0 and V1 and store in V2). Set V0=5, V1=7. Run. Verify V2=12.</p>
        <p style="margin-top:8px"><strong>Step 3.</strong> Observe the critical difference: the Difference Engine computed only what its initial setup determined. The Analytical Engine can be <em>reprogrammed</em> by changing the operation cards. That is the difference between a calculator and a computer.</p>
      </div>
    </section>

    <section aria-labelledby="sect-deeper4">
      <h2 class="section-head" id="sect-deeper4">Going Deeper</h2>
      <div class="callout callout-deep" role="note" aria-label="Deep Dive">
        <div class="callout-label"><span aria-hidden="true">&nabla;</span> Why the Analytical Engine Matters Despite Never Being Built</div>
        <p>Babbage&rsquo;s machine was never built. So why does it matter? First: it proved the concept was coherent. When the Science Museum built the Difference Engine from Babbage&rsquo;s drawings in 1991, it worked. The Analytical Engine would have worked too &mdash; just extremely slowly and at enormous cost.</p>
        <p style="margin-top:var(--space-sm)">Second: it established the architecture. The Store + Mill + input/output + conditional branch is the Von Neumann architecture, a century before Von Neumann wrote it down. Every computer you have ever used is a descendant of this structure.</p>
        <p style="margin-top:var(--space-sm)">Third: Ada named the abstraction. By writing the first algorithm and articulating that the Engine worked on symbols (not just numbers), she defined programming as a discipline separate from hardware construction. The first person to understand what software <em>is</em> understood it in 1843, about a punch-card-driven mechanical engine that was never built.</p>
      </div>
    </section>

    <section aria-labelledby="challenge-04" class="challenge-section">
      <header class="challenge-header">
        <div class="challenge-num" aria-hidden="true">0.4</div>
        <div class="challenge-title-block">
          <p class="challenge-overline">Challenge</p>
          <h2 class="challenge-title" id="challenge-04">Differences and Operation Cards</h2>
          <div class="challenge-meta">
            <span class="challenge-meta-item">Calculation + emulator exercise</span>
            <span class="challenge-meta-item">25&ndash;30 minutes</span>
          </div>
        </div>
      </header>
      <div class="challenge-setup">
        <p class="challenge-setup-label">Setup</p>
        <p>Use the simulation for Part B. Part A is pen-and-paper.</p>
      </div>
      <div class="challenge-part">
        <p class="challenge-part-label"><span>Part A</span> Finite Differences</p>
        <ol class="challenge-questions">
          <li data-sub="1"><p>For <em>f</em>(<em>n</em>) = 2<em>n</em>&sup2; + 3<em>n</em> + 1, compute values at <em>n</em> = 0, 1, 2, 3, 4. Then compute first differences and second differences. At what order do the differences become constant?</p></li>
          <li data-sub="2"><p>Use the Difference Engine simulation to tabulate the same polynomial. Does the machine match your manual calculation?</p></li>
        </ol>
      </div>
      <div class="challenge-part">
        <p class="challenge-part-label"><span>Part B</span> Operation Cards</p>
        <ol class="challenge-questions" style="counter-reset: q-counter 2">
          <li data-sub="3"><p>In the Analytical Engine emulator, write a 5-step operation card sequence that computes <em>a</em>&sup2; + <em>b</em>&sup2; given <em>a</em> and <em>b</em> stored in V0 and V1. Hint: you will need MUL and ADD operations. Trace the Store state after each step.</p></li>
          <li data-sub="4"><p>In two sentences: what does Ada&rsquo;s observation &mdash; &ldquo;the Engine might act upon other things besides number&rdquo; &mdash; mean in modern terms? Give one example of a non-numerical computation.</p></li>
        </ol>
      </div>
    </section>

    <section aria-labelledby="summary-04" class="chapter-summary">
      <h2 class="section-head" id="summary-04" style="border-top:none;padding-top:0;margin-top:0;">Summary</h2>
      <p class="body no-indent">Babbage designed a general-purpose computer in 1837. Ada programmed it in 1843. Neither could build it. But the ideas were complete.</p>
      <p class="body">Store, Mill, conditional branch, loop, output: these five concepts define a computer. Every processor since 1945 implements them. The names have changed. The architecture has not. When you write <code>if</code>, <code>while</code>, a variable assignment, and a function call, you are using Babbage&rsquo;s Analytical Engine &mdash; built from silicon rather than brass, executing in nanoseconds rather than minutes, but structurally the same machine.</p>
      <div class="section-break" role="separator" aria-hidden="true"><div class="sb-line"></div><div class="sb-dot"></div><div class="sb-dot"></div><div class="sb-dot"></div><div class="sb-line"></div></div>
      <div class="chapter-nav">
        <div class="nav-prev"><p class="nav-label">Previous &mdash; Module 0.3</p><p class="nav-title">&larr; The Loom That Taught Computers</p></div>
        <div class="nav-next"><p class="nav-label">Next &mdash; Module 0.5</p><p class="nav-title">Hollerith and the Punch Card Era &rarr;</p></div>
      </div>
    </section>

  </main>
  <footer class="page-footer" role="contentinfo">
    <span class="page-footer-series">AoPS &mdash; Volume 0</span>
    <span class="page-num">6</span>
  </footer>
</article>
<script>
function toggleHint(btn){{
  const id=btn.getAttribute('aria-controls');
  const box=document.getElementById(id);
  if(!box)return;
  const open=box.classList.toggle('open');
  btn.setAttribute('aria-expanded',open);
  const arr=btn.querySelector('.hint-toggle-arrow');
  if(arr)arr.textContent=open?'&uarr;':'&darr;';
}}
</script>
</body>
</html>"""

out = BASE / "ebook/level-0/chapter-4/chapter-4.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(h, "utf-8")
print(f"chapter-4.html: {len(h):,} chars  ({len(h)//1024} KB)")
