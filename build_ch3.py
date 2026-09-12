"""Build Chapter 3: The Loom That Taught Computers"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from pathlib import Path

BASE = Path(r"c:\Users\NDH01061\Desktop\Kiro - Project\AoPS")
c1 = (BASE / "ebook/level-0/chapter-1/chapter-1.html").read_text("utf-8", errors="replace")
CSS = re.search(r"<style>(.*?)</style>", c1, re.DOTALL).group(1)
FONTS = "https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@200;300;400;600&family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500&display=swap"

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
          <strong id="fig-{slug}-title">Figure {e(num)} — {e(f["title"])}</strong> {e(f["cap"])}
        </figcaption>
      </figure>"""

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

def head(title, ch):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AoPS — {e(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="{FONTS}" rel="stylesheet">
<style>{CSS}{FIG_CSS}</style>
</head>
<body>
<article class="book-page">
  <header class="running-header" role="banner">
    <span>Volume 0 — Before Computers</span>
    <span class="rh-chapter">Chapter {ch}</span>
  </header>
"""

def sb(): return """
      <div class="section-break" role="separator" aria-hidden="true">
        <div class="sb-line"></div><div class="sb-dot"></div><div class="sb-dot"></div><div class="sb-dot"></div><div class="sb-line"></div>
      </div>"""

def foot(pg, prev_num, prev_title, next_num, next_title):
    return f"""
    <div class="chapter-nav">
      <div class="nav-prev"><p class="nav-label">Previous — Module {e(prev_num)}</p><p class="nav-title">&larr; {e(prev_title)}</p></div>
      <div class="nav-next"><p class="nav-label">Next — Module {e(next_num)}</p><p class="nav-title">{e(next_title)} &rarr;</p></div>
    </div>
  </main>
  <footer class="page-footer" role="contentinfo">
    <span class="page-footer-series">AoPS — Volume 0</span>
    <span class="page-num">{pg}</span>
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
  if(arr)arr.textContent=open?'↑':'↓';
}}
</script>
</body>
</html>"""

# ══════════════════════════════════════════════════════════════════════
# CHAPTER 3
# ══════════════════════════════════════════════════════════════════════
figs = get_figs(BASE / "illustrations/level-0/module-0-3-loom.html")
print(f"Chapter 3 figs: {len(figs)}")

h = head("Chapter Three — The Loom That Taught Computers", "Three")

# Chapter opener with unique warp/weft motif
h += """
  <div class="chapter-opener" role="heading" aria-level="1">
    <svg class="opener-motif" viewBox="0 0 720 320" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" preserveAspectRatio="xMidYMid slice">
      <!-- Warp threads (vertical) — dense left, dissolving right -->
      <g stroke="#F5F4EF" stroke-linecap="round">
        <g stroke-width="1" opacity="0.22">
          <line x1="40"  y1="20" x2="40"  y2="230"/><line x1="64"  y1="20" x2="64"  y2="230"/>
          <line x1="88"  y1="20" x2="88"  y2="230"/><line x1="112" y1="20" x2="112" y2="230"/>
          <line x1="136" y1="20" x2="136" y2="230"/><line x1="160" y1="20" x2="160" y2="230"/>
          <line x1="184" y1="20" x2="184" y2="230"/><line x1="208" y1="20" x2="208" y2="230"/>
        </g>
        <!-- Weft threads (horizontal) crossing warp -->
        <g stroke-width="0.9" opacity="0.18">
          <line x1="30" y1="50"  x2="240" y2="50"/>
          <line x1="30" y1="80"  x2="240" y2="80"/>
          <line x1="30" y1="110" x2="240" y2="110"/>
          <line x1="30" y1="140" x2="240" y2="140"/>
          <line x1="30" y1="170" x2="240" y2="170"/>
          <line x1="30" y1="200" x2="240" y2="200"/>
        </g>
        <!-- Lifted warp threads (pattern) — highlighted -->
        <g stroke-width="2.5" opacity="0.5">
          <line x1="40"  y1="20" x2="40"  y2="50"/>
          <line x1="88"  y1="20" x2="88"  y2="50"/>
          <line x1="136" y1="20" x2="136" y2="50"/>
          <line x1="184" y1="20" x2="184" y2="50"/>
          <line x1="64"  y1="20" x2="64"  y2="80"/>
          <line x1="112" y1="20" x2="112" y2="80"/>
          <line x1="160" y1="20" x2="160" y2="80"/>
          <line x1="208" y1="20" x2="208" y2="80"/>
        </g>
      </g>
      <!-- Card chain (right) -->
      <g stroke="#F5F4EF" opacity="0.14">
        <rect x="360" y="50"  width="120" height="70" rx="2" stroke-width="0.8"/>
        <rect x="370" y="60"  width="100" height="50" rx="1" stroke-width="0.5"/>
        <rect x="360" y="130" width="120" height="70" rx="2" stroke-width="0.8"/>
        <rect x="370" y="140" width="100" height="50" rx="1" stroke-width="0.5"/>
        <rect x="360" y="210" width="120" height="50" rx="2" stroke-width="0.8" opacity="0.5"/>
        <!-- Holes in cards -->
        <g fill="#F5F4EF" opacity="0.5">
          <circle cx="390" cy="78" r="4"/><circle cx="415" cy="78" r="4"/>
          <circle cx="440" cy="78" r="4"/><circle cx="390" cy="97" r="4"/>
          <circle cx="415" cy="97" r="4"/>
          <circle cx="390" cy="158" r="4"/><circle cx="440" cy="158" r="4"/>
          <circle cx="415" cy="175" r="4"/><circle cx="465" cy="175" r="4"/>
        </g>
        <!-- Chain links -->
        <line x1="420" y1="120" x2="420" y2="130" stroke-width="2"/>
        <line x1="420" y1="200" x2="420" y2="210" stroke-width="2"/>
      </g>
      <!-- Lacquer accent — needles sensing holes -->
      <g fill="#C82A2A" opacity="0.45">
        <circle cx="390" cy="50" r="2.5"/>
        <circle cx="415" cy="50" r="2.5"/>
        <circle cx="440" cy="50" r="2.5"/>
      </g>
      <text x="125" y="260" font-family="JetBrains Mono, monospace" font-size="8" fill="#F5F4EF" opacity="0.28" text-anchor="middle">warp/weft pattern</text>
      <text x="420" y="280" font-family="JetBrains Mono, monospace" font-size="8" fill="#F5F4EF" opacity="0.28" text-anchor="middle">card chain — stored instructions</text>
    </svg>
    <div class="chapter-ghost-num" aria-hidden="true">03</div>
    <p class="chapter-num-label">Module 0.3 &nbsp;&middot;&nbsp; Level 0 &mdash; Before Computers</p>
    <div class="chapter-rule" role="separator"></div>
    <h1 class="chapter-title">The Loom That<br>Taught Computers</h1>
    <p class="chapter-subtitle">How holes in cards became stored instructions</p>
  </div>

  <!-- Illustration band -->
  <figure class="chapter-illustration" aria-label="Decorative: warp threads and punch card chain abstracting to binary encoding">
    <svg viewBox="0 0 672 140" fill="none" xmlns="http://www.w3.org/2000/svg" width="672" height="140" aria-hidden="true">
      <defs>
        <linearGradient id="fl3" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="#EEECE4" stop-opacity="1"/>
          <stop offset="12%" stop-color="#EEECE4" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="fr3" x1="0" y1="0" x2="1" y2="0">
          <stop offset="88%" stop-color="#EEECE4" stop-opacity="0"/>
          <stop offset="100%" stop-color="#EEECE4" stop-opacity="1"/>
        </linearGradient>
      </defs>
      <!-- Warp threads left -->
      <g stroke="#1C2D42" stroke-width="0.5" opacity="0.15">
        <line x1="50" y1="15" x2="50" y2="130"/><line x1="70" y1="15" x2="70" y2="130"/>
        <line x1="90" y1="15" x2="90" y2="130"/><line x1="110" y1="15" x2="110" y2="130"/>
        <line x1="130" y1="15" x2="130" y2="130"/><line x1="150" y1="15" x2="150" y2="130"/>
        <line x1="170" y1="15" x2="170" y2="130"/><line x1="190" y1="15" x2="190" y2="130"/>
        <!-- Weft -->
        <line x1="42" y1="35"  x2="210" y2="35"/>
        <line x1="42" y1="55"  x2="210" y2="55"/>
        <line x1="42" y1="75"  x2="210" y2="75"/>
        <line x1="42" y1="95"  x2="210" y2="95"/>
        <line x1="42" y1="115" x2="210" y2="115"/>
      </g>
      <!-- Lifted threads -->
      <g fill="#1C2D42" opacity="0.25">
        <rect x="44" y="28" width="12" height="12"/><rect x="84" y="28" width="12" height="12"/>
        <rect x="124" y="28" width="12" height="12"/><rect x="164" y="28" width="12" height="12"/>
        <rect x="64" y="48" width="12" height="12"/><rect x="104" y="48" width="12" height="12"/>
        <rect x="144" y="48" width="12" height="12"/><rect x="184" y="48" width="12" height="12"/>
        <rect x="44" y="68" width="12" height="12"/><rect x="84" y="68" width="12" height="12"/>
        <rect x="124" y="68" width="12" height="12"/>
      </g>
      <!-- Punch card right -->
      <g stroke="#1C2D42" opacity="0.15">
        <rect x="280" y="20" width="100" height="65" rx="2" stroke-width="0.8"/>
        <rect x="290" y="30" width="80" height="45" rx="1" stroke-width="0.5"/>
        <rect x="280" y="98" width="100" height="65" rx="2" stroke-width="0.8"/>
        <rect x="290" y="108" width="80" height="45" rx="1" stroke-width="0.5"/>
      </g>
      <!-- Holes -->
      <g fill="#1C2D42" opacity="0.3">
        <circle cx="305" cy="45" r="4.5"/><circle cx="325" cy="45" r="4.5"/>
        <circle cx="345" cy="45" r="4.5"/><circle cx="305" cy="62" r="4.5"/>
        <circle cx="345" cy="62" r="4.5"/>
        <circle cx="305" cy="123" r="4.5"/><circle cx="345" cy="123" r="4.5"/>
        <circle cx="325" cy="140" r="4.5"/>
      </g>
      <!-- Binary readout far right -->
      <g stroke="#1C2D42" stroke-width="0.4" opacity="0.12">
        <line x1="430" y1="25" x2="610" y2="25"/><line x1="430" y1="45" x2="610" y2="45"/>
        <line x1="430" y1="65" x2="610" y2="65"/><line x1="430" y1="85" x2="610" y2="85"/>
        <line x1="430" y1="105" x2="610" y2="105"/>
      </g>
      <g fill="#1C2D42" opacity="0.25">
        <circle cx="448" cy="35" r="4"/><circle cx="478" cy="25" r="4"/>
        <circle cx="508" cy="45" r="4"/><circle cx="538" cy="35" r="4"/>
        <circle cx="568" cy="25" r="4"/><circle cx="598" cy="55" r="4"/>
        <circle cx="448" cy="75" r="4"/><circle cx="508" cy="65" r="4"/>
      </g>
      <g fill="#C82A2A" opacity="0.45">
        <circle cx="448" cy="25" r="2.5"/><circle cx="508" cy="25" r="2.5"/>
        <circle cx="568" cy="45" r="2.5"/>
      </g>
      <text x="130" y="132" font-family="JetBrains Mono, monospace" font-size="8" fill="#1C2D42" opacity="0.35" text-anchor="middle">warp/weft — Lyon, 1804</text>
      <text x="490" y="132" font-family="JetBrains Mono, monospace" font-size="8" fill="#1C2D42" opacity="0.35" text-anchor="middle">card chain → binary encoding</text>
      <rect x="0"   y="0" width="60"  height="140" fill="url(#fl3)"/>
      <rect x="612" y="0" width="60"  height="140" fill="url(#fr3)"/>
    </svg>
  </figure>

  <main class="chapter-body">

    <section aria-labelledby="sect-prob3">
      <h2 class="section-head" id="sect-prob3" style="border-top:none;padding-top:0;margin-top:0;">The Problem</h2>
      <p class="lead drop-cap">You own a silk weaving factory in Lyon, France, in 1800. Your most valuable product is fabric woven in complex patterns &mdash; flowers, birds, geometric designs that wealthy clients pay a fortune for.</p>
      <p class="body no-indent">Each pattern requires a master weaver to manually control which warp threads rise and which stay down on every single pass of the shuttle. One wrong move breaks the pattern. A skilled weaver takes years to train. They are expensive, they tire, they make mistakes, and they can only hold one pattern sequence in their memory at a time.</p>
      <p class="body">How do you separate the <em>knowledge of the pattern</em> from the <em>act of weaving</em>? This is not a question about fabric. It is the question that gave birth to the concept of <strong>stored instructions</strong>: the idea that a procedure can be written down and executed by a machine without a human in the decision loop.</p>
    </section>

    <section aria-labelledby="sect-story3">
      <h2 class="section-head" id="sect-story3">The Story</h2>

      <h3 class="sub-head">Bouchon and Falcon &mdash; First Steps (1725&ndash;1728)</h3>
      <p class="body no-indent">Basile Bouchon made the crucial first step in 1725. He fed a roll of paper with holes punched in it past a row of needles. Where there was a hole, the needle passed through and lifted a thread hook. Where there was no hole, the needle was blocked.</p>
      <p class="body"><strong>The profound shift</strong>: the pattern was no longer in a person&rsquo;s head. It was encoded as holes in paper &mdash; a physical, durable, reproducible medium. This is the first time in history that data was stored externally to a human mind and read by a machine.</p>
      <p class="body">Jean-Baptiste Falcon improved the idea three years later by replacing the paper roll with a chain of stiff punched cards. Cards could be detached and rearranged. The pattern became not just storable but <em>editable</em>.</p>
"""

h += sb()
h += """
      <h3 class="sub-head">Jacquard&rsquo;s Loom &mdash; Complete Automation (1804)</h3>
      <p class="body no-indent">Joseph Marie Jacquard synthesised and perfected these ideas into a complete automated system in 1804. His attachment sat on top of a standard loom and fully automated thread selection for the first time in history.</p>
      <p class="body">A chain of stiff punched cards passes over a square cylinder. On each pass of the shuttle, the next card is pressed against a row of spring-loaded needles. Where there is a hole: the needle passes through, lifts its corresponding warp thread &mdash; thread is <strong>UP</strong>. Where there is no hole: the needle is blocked &mdash; thread is <strong>DOWN</strong>. The shuttle passes through the gap created by the raised threads. The next card advances. The next row of the pattern executes.</p>
      <p class="body">The complete pattern &mdash; potentially thousands of rows &mdash; lives in the card chain. The loom executes it automatically, row by row, without any human decision-making during operation. A Jacquard loom could execute a pattern requiring 24,000 cards in sequence. A single weaver could then produce complex silk damask at the rate a simple loom produced plain cloth.</p>
"""

h += fig(figs[0], "3.1", wide=True) if len(figs) > 0 else ""

h += """
      <div class="callout callout-historical" role="note" aria-label="Historical Note">
        <div class="callout-label"><span aria-hidden="true">&oplus;</span> Historical Note</div>
        <p>The impact was immediate and violent. Lyon&rsquo;s weavers rioted. Jacquard was attacked in the street. His looms were burned. The city council confiscated the machines. Then economics won. By 1812, Napoleon had ordered 11,000 Jacquard looms installed across France. By 1833, there were 30,000 in Lyon alone. The weavers who had opposed the machine now operated it.</p>
      </div>"""

h += sb()

h += """
      <h3 class="sub-head">Babbage Sees It</h3>
      <p class="body no-indent">Charles Babbage visited a weaving exhibition in London in the 1830s and saw a portrait of Jacquard himself &mdash; woven in silk on a Jacquard loom, using 24,000 punch cards. The portrait had the photographic detail of an engraving.</p>
      <p class="body">Babbage later wrote: <em>&ldquo;The Jacquard loom is capable of weaving any design which the imagination of man may conceive.&rdquo;</em></p>
      <p class="body">He immediately grasped that the same principle &mdash; instructions stored on cards, read sequentially by a machine &mdash; could control a calculating engine. Not just weaving, but any computation. This insight is the direct intellectual link between the Jacquard loom and the Analytical Engine (Chapter 4), and by extension, to every computer ever built.</p>
    </section>

    <section aria-labelledby="sect-concept3">
      <h2 class="section-head" id="sect-concept3">The Concept &mdash; What a Punch Card Actually Is</h2>
      <p class="body no-indent">A punch card is a <strong>binary encoding of instructions</strong>.</p>
      <p class="body">Each position on the card can be either: <strong>Hole</strong> (1 &mdash; do this: lift this thread); or <strong>No hole</strong> (0 &mdash; don&rsquo;t do this: leave thread down). A row of eight positions gives eight binary decisions. That is one byte. IBM&rsquo;s 80-column punch cards, used until the 1980s, encoded exactly 80 characters of data per card using a binary hole/no-hole scheme &mdash; the direct industrial descendant of Jacquard&rsquo;s system.</p>
"""

h += fig(figs[1], "3.2") if len(figs) > 1 else ""
h += fig(figs[2], "3.3") if len(figs) > 2 else ""

h += """
      <span class="table-label">Table 3.1</span>
      <div class="table-wrap">
        <table class="book-table" role="table" aria-label="Three revolutionary ideas from the Jacquard loom">
          <thead><tr><th scope="col">Idea</th><th scope="col">What it means for computing</th></tr></thead>
          <tbody>
            <tr><td>External instruction storage</td><td>The program lives outside the machine; it can be saved, copied, and edited</td></tr>
            <tr><td>Sequential execution</td><td>Cards are read in order; the machine follows a defined sequence of steps</td></tr>
            <tr class="highlight"><td>Separation of program from machine</td><td>The same loom weaves any pattern; the same computer runs any program. This is the birth of software.</td></tr>
          </tbody>
        </table>
      </div>
      <p class="table-caption">Table 3.1 &mdash; Three ideas introduced by the Jacquard loom that define software to this day. The third is the most profound: it separates what a machine <em>does</em> from what a machine <em>is</em>.</p>

      <div class="pull-quote">
        &ldquo;You don&rsquo;t need a different computer for each program. You need different software. Jacquard understood this about looms in 1804.&rdquo;
      </div>
"""

h += fig(figs[3], "3.4") if len(figs) > 3 else ""

h += """
      <div class="callout callout-future" role="note" aria-label="Future Connection">
        <div class="callout-label"><span aria-hidden="true">&rarr;</span> Future Connection &mdash; Level 3: Machine Architecture</div>
        <p>The Jacquard card chain encodes a fixed sequence of instructions read once, in order. The stored-program computer goes further: the program is stored in the <em>same memory as the data</em>, can be modified at runtime, and can jump to any instruction based on a computed result. The punch card is the conceptual ancestor; the instruction register and program counter are its electronic descendants. You will meet them in Module 3.2: The Fetch-Decode-Execute Cycle.</p>
      </div>
    </section>

    <section aria-labelledby="sect-sim3">
      <h2 class="section-head" id="sect-sim3">Hands-On Exercise</h2>
      <p class="body no-indent">The simulation provides two interconnected tools: a punch card designer and a loom animator. The key observation &mdash; once you design the card chain, the loom executes it identically every time &mdash; should be felt, not just understood. Spend time with the pattern editor before reading on.</p>

      <figure class="sim-figure" aria-labelledby="sim3-cap">
        <span class="sim-figure-badge">Interactive</span>
        <span class="sim-figure-label">Figure 3.5 &mdash; Jacquard Loom Simulator</span>
        <div class="sim-figure-frame">
          <div class="sim-preview-header">
            <div><div class="sim-preview-title">Jacquard Loom Simulator</div><div class="sim-preview-subtitle">Punch card designer &middot; Loom animator &middot; Fabric preview</div></div>
          </div>
          <div class="sim-tabs-preview" aria-hidden="true">
            <div class="sim-tab-p active">Card Designer</div>
            <div class="sim-tab-p">Loom View</div>
            <div class="sim-tab-p">Fabric Preview</div>
          </div>
          <div class="sim-link-row">
            <a href="../../course/level-0-before-computers/module-0-3-loom/simulation.html" class="sim-open-btn" target="_blank" rel="noopener noreferrer">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2 2h8v8M10 2L2 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              Open Simulation
            </a>
            <p class="sim-note">Opens in a new tab &middot; No installation required</p>
          </div>
        </div>
        <figcaption class="sim-figure-caption" id="sim3-cap">Figure 3.5 &mdash; Jacquard Loom Simulator. Card Designer: click cells to punch holes in an 8&times;8 grid; each column controls one warp thread. Loom View: watch threads lift and fall row by row as each card advances. Fabric Preview: the cumulative woven pattern builds up in the panel below.</figcaption>
      </figure>

      <div class="callout callout-sim" role="note" aria-label="Walkthrough">
        <div class="callout-label"><span aria-hidden="true">&#9655;</span> Step-by-Step Walkthrough</div>
        <p><strong>Step 1.</strong> In the Card Designer, punch a checkerboard &mdash; holes in columns 1,3,5,7 on odd rows; holes in 2,4,6,8 on even rows. Press Weave. Observe the alternating lift pattern produce a simple check fabric.</p>
        <p style="margin-top:8px"><strong>Step 2.</strong> Attempt to weave the letter <strong>H</strong>. Notice you must think about the pattern entirely in advance and encode it completely before weaving begins. There is no &ldquo;undo&rdquo; on a moving loom.</p>
        <p style="margin-top:8px"><strong>Step 3.</strong> Change one card in the middle of your H sequence. Only that row changes. The rest of the pattern is unaffected. This modularity &mdash; editing one instruction without rewriting the whole program &mdash; is the fundamental advantage of stored instructions over hardwired mechanisms.</p>
      </div>
    </section>

    <section aria-labelledby="sect-deeper3">
      <h2 class="section-head" id="sect-deeper3">Going Deeper</h2>
      <div class="callout callout-deep" role="note" aria-label="Deep Dive">
        <div class="callout-label"><span aria-hidden="true">&nabla;</span> The Jacquard Lineage</div>
        <p>The Jacquard loom is the ancestor of the entire data-storage technology stack. Piano rolls (1800s) encoded musical performances as holes in paper. Player pianos read those holes mechanically. Teletypes used punched tape for transmitting messages. IBM punch cards stored data for computers until the early 1980s &mdash; nine decades of continuous use. Numerically controlled (<abbr title="Numerically Controlled">NC</abbr>) machine tools were programmed via punched tape. The optical disc &mdash; <abbr title="Compact Disc">CD</abbr>, <abbr title="Digital Versatile Disc">DVD</abbr> &mdash; encodes 0s and 1s as microscopic pits and lands: the same hole-versus-not-hole principle, read by laser instead of needle.</p>
        <p style="margin-top:var(--space-sm)">The hole as instruction is one of humanity&rsquo;s most durable ideas. It survived the transition from silk thread to digital data with its underlying logic intact across two centuries.</p>
      </div>
    </section>

    <section aria-labelledby="challenge-03" class="challenge-section">
      <header class="challenge-header">
        <div class="challenge-num" aria-hidden="true">0.3</div>
        <div class="challenge-title-block">
          <p class="challenge-overline">Challenge</p>
          <h2 class="challenge-title" id="challenge-03">Encoding and Decoding a Pattern</h2>
          <div class="challenge-meta">
            <span class="challenge-meta-item">Binary encoding &amp; design</span>
            <span class="challenge-meta-item">25&ndash;30 minutes</span>
          </div>
        </div>
      </header>
      <div class="challenge-setup">
        <p class="challenge-setup-label">Setup</p>
        <p>An 8-column loom. Each column controls one warp thread. <strong>Hole = thread UP</strong>; <strong>No hole = thread DOWN</strong>. Each row on a card represents one pass of the shuttle.</p>
      </div>
      <div class="challenge-part">
        <p class="challenge-part-label"><span>Part A</span> Encode a Pattern</p>
        <ol class="challenge-questions">
          <li data-sub="1"><p>Design a 4-row card sequence that weaves a diagonal stripe in the &ldquo;/&rdquo; direction across an 8-column fabric. Write each row as an 8-bit binary number (1 = hole, 0 = no hole). Verify in the simulation.</p></li>
          <li data-sub="2"><p>Design a 4-row sequence that produces the letter <strong>I</strong> (a vertical bar in column 4). What is the binary representation of each row?</p></li>
        </ol>
      </div>
      <div class="challenge-part">
        <p class="challenge-part-label"><span>Part B</span> Decode a Mystery</p>
        <ol class="challenge-questions" style="counter-reset: q-counter 2">
          <li data-sub="3"><p>The following card sequence is provided:<br>
          Row 1: <code>10000001</code><br>
          Row 2: <code>01000010</code><br>
          Row 3: <code>00100100</code><br>
          Row 4: <code>00011000</code><br>
          Without the simulation, describe the visual pattern this produces. Then verify.</p></li>
        </ol>
      </div>
    </section>

    <section aria-labelledby="summary-03" class="chapter-summary">
      <h2 class="section-head" id="summary-03" style="border-top:none;padding-top:0;margin-top:0;">Summary</h2>
      <p class="body no-indent">The Jacquard loom solved a problem in textile manufacturing and accidentally solved a problem in computer science: how to store a procedure in a medium that a machine can read.</p>
      <p class="body">Holes in cards are binary. Sequential cards are sequential instructions. The separation of card chain from loom mechanism is the separation of software from hardware. These ideas entered weaving in 1804, computing in the 1830s when Babbage saw the loom, and industry in the 1890s when Hollerith applied them to the census. The next chapter asks: what is the difference between a calculator and a <em>computer</em> &mdash; and who first drew that line?</p>
"""

h += foot(5, "0.2", "Early Mechanical Computation", "0.4", "Babbage and Ada: The First Programmers")

out = BASE / "ebook/level-0/chapter-3/chapter-3.html"
out.write_text(h, "utf-8")
print(f"chapter-3.html: {len(h):,} chars  ({len(h)//1024} KB)")
