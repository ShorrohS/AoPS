"""Build Chapter 5: Hollerith and the Punch Card Era"""
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

figs = get_figs(BASE / "illustrations/level-0/module-0-5-hollerith.html")
print(f"Chapter 5 figs: {len(figs)}")

h = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AoPS &mdash; Chapter Five: Hollerith and the Punch Card Era</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="{FONTS}" rel="stylesheet">
<style>{CSS}{FIG_CSS}</style>
</head>
<body>
<article class="book-page">
  <header class="running-header" role="banner">
    <span>Volume 0 &mdash; Before Computers</span>
    <span class="rh-chapter">Chapter Five</span>
  </header>

  <div class="chapter-opener" role="heading" aria-level="1">
    <svg class="opener-motif" viewBox="0 0 720 320" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" preserveAspectRatio="xMidYMid slice">
      <!-- Hollerith card grid (12 rows × 80 columns, abstracted) -->
      <g stroke="#F5F4EF" stroke-width="0.4" opacity="0.12">
        <!-- Card outline -->
        <rect x="30" y="40" width="280" height="200" rx="3"/>
        <!-- Row lines (12 rows) -->
        <line x1="30"  y1="57"  x2="310" y2="57"/>
        <line x1="30"  y1="74"  x2="310" y2="74"/>
        <line x1="30"  y1="91"  x2="310" y2="91"/>
        <line x1="30"  y1="108" x2="310" y2="108"/>
        <line x1="30"  y1="125" x2="310" y2="125"/>
        <line x1="30"  y1="142" x2="310" y2="142"/>
        <line x1="30"  y1="159" x2="310" y2="159"/>
        <line x1="30"  y1="176" x2="310" y2="176"/>
        <line x1="30"  y1="193" x2="310" y2="193"/>
        <line x1="30"  y1="210" x2="310" y2="210"/>
        <!-- Column markers (compressed) -->
        <g opacity="0.5">
          <line x1="55" y1="40" x2="55" y2="240"/><line x1="80" y1="40" x2="80" y2="240"/>
          <line x1="105" y1="40" x2="105" y2="240"/><line x1="130" y1="40" x2="130" y2="240"/>
          <line x1="155" y1="40" x2="155" y2="240"/><line x1="180" y1="40" x2="180" y2="240"/>
          <line x1="205" y1="40" x2="205" y2="240"/><line x1="230" y1="40" x2="230" y2="240"/>
          <line x1="255" y1="40" x2="255" y2="240"/><line x1="280" y1="40" x2="280" y2="240"/>
        </g>
      </g>
      <!-- Punched holes (census data encoded) -->
      <g fill="#F5F4EF" opacity="0.45">
        <!-- Age: 34 → punch row 3 col zone, row 4 -->
        <ellipse cx="55"  cy="91"  rx="4.5" ry="6"/>
        <ellipse cx="55"  cy="108" rx="4.5" ry="6"/>
        <!-- Occupation: Farmer -->
        <ellipse cx="80"  cy="57"  rx="4.5" ry="6"/>
        <ellipse cx="80"  cy="125" rx="4.5" ry="6"/>
        <!-- Birthplace: Virginia -->
        <ellipse cx="105" cy="74"  rx="4.5" ry="6"/>
        <ellipse cx="105" cy="159" rx="4.5" ry="6"/>
        <!-- Family: 6 -->
        <ellipse cx="130" cy="91"  rx="4.5" ry="6"/>
        <!-- More scattered punches -->
        <ellipse cx="155" cy="57"  rx="4.5" ry="6"/>
        <ellipse cx="180" cy="108" rx="4.5" ry="6"/>
        <ellipse cx="205" cy="74"  rx="4.5" ry="6"/>
        <ellipse cx="230" cy="142" rx="4.5" ry="6"/>
        <ellipse cx="255" cy="57"  rx="4.5" ry="6"/>
        <ellipse cx="280" cy="91"  rx="4.5" ry="6"/>
      </g>
      <!-- Tabulator wheels (right) — counters incrementing -->
      <g stroke="#F5F4EF" opacity="0.14">
        <circle cx="430" cy="90"  r="32" stroke-width="1"/>
        <circle cx="430" cy="90"  r="20" stroke-width="0.6"/>
        <circle cx="430" cy="90"  r="6"  stroke-width="0.6"/>
        <circle cx="510" cy="90"  r="32" stroke-width="1"/>
        <circle cx="510" cy="90"  r="20" stroke-width="0.6"/>
        <circle cx="510" cy="90"  r="6"  stroke-width="0.6"/>
        <circle cx="590" cy="90"  r="32" stroke-width="1"/>
        <circle cx="590" cy="90"  r="20" stroke-width="0.6"/>
        <circle cx="590" cy="90"  r="6"  stroke-width="0.6"/>
        <!-- Tick marks on wheels -->
        <g stroke-width="1.2">
          <line x1="430" y1="55"  x2="430" y2="48"/>
          <line x1="462" y1="64"  x2="467" y2="58"/>
          <line x1="465" y1="90"  x2="463" y2="82"/>
          <line x1="430" y1="125" x2="430" y2="132"/>
          <line x1="395" y1="90"  x2="398" y2="82"/>
          <line x1="510" y1="55"  x2="510" y2="48"/>
          <line x1="542" y1="90"  x2="543" y2="82"/>
          <line x1="590" y1="55"  x2="590" y2="48"/>
        </g>
        <!-- Digit windows -->
        <rect x="418" y="82" width="24" height="16" rx="2" stroke-width="0.8"/>
        <rect x="498" y="82" width="24" height="16" rx="2" stroke-width="0.8"/>
        <rect x="578" y="82" width="24" height="16" rx="2" stroke-width="0.8"/>
      </g>
      <!-- Digits in windows -->
      <g fill="#F5F4EF" opacity="0.5" font-family="JetBrains Mono, monospace" font-size="11" text-anchor="middle">
        <text x="430" y="94">7</text>
        <text x="510" y="94">2</text>
        <text x="590" y="94">8</text>
      </g>
      <!-- Lacquer accent — electrical connection lines -->
      <g stroke="#C82A2A" stroke-width="1.2" opacity="0.35">
        <line x1="80"  y1="57"  x2="390" y2="57"  stroke-dasharray="4,3"/>
        <line x1="55"  y1="91"  x2="390" y2="86"  stroke-dasharray="4,3"/>
        <line x1="105" y1="74"  x2="390" y2="78"  stroke-dasharray="4,3"/>
      </g>
      <text x="170" y="260" font-family="JetBrains Mono, monospace" font-size="8" fill="#F5F4EF" opacity="0.25" text-anchor="middle">Hollerith card &mdash; 80 col &times; 12 row</text>
      <text x="510" y="145" font-family="JetBrains Mono, monospace" font-size="8" fill="#F5F4EF" opacity="0.25" text-anchor="middle">mechanical counter wheels</text>
    </svg>
    <div class="chapter-ghost-num" aria-hidden="true">05</div>
    <p class="chapter-num-label">Module 0.5 &nbsp;&middot;&nbsp; Level 0 &mdash; Before Computers</p>
    <div class="chapter-rule" role="separator"></div>
    <h1 class="chapter-title">Hollerith and the<br>Punch Card Era</h1>
    <p class="chapter-subtitle">From the 1890 census to the birth of IBM &mdash; data processing at scale</p>
  </div>

  <figure class="chapter-illustration" aria-label="Decorative: Hollerith card grid with encoded holes and counter wheel dials">
    <svg viewBox="0 0 672 140" fill="none" xmlns="http://www.w3.org/2000/svg" width="672" height="140" aria-hidden="true">
      <defs>
        <linearGradient id="fl5" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="#EEECE4" stop-opacity="1"/><stop offset="12%" stop-color="#EEECE4" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="fr5" x1="0" y1="0" x2="1" y2="0">
          <stop offset="88%" stop-color="#EEECE4" stop-opacity="0"/><stop offset="100%" stop-color="#EEECE4" stop-opacity="1"/>
        </linearGradient>
      </defs>
      <!-- Card outline -->
      <g stroke="#1C2D42" opacity="0.12">
        <rect x="50" y="18" width="220" height="110" rx="3" stroke-width="0.7"/>
        <!-- Row lines -->
        <line x1="50"  y1="28"  x2="270" y2="28" stroke-width="0.4"/>
        <line x1="50"  y1="38"  x2="270" y2="38" stroke-width="0.4"/>
        <line x1="50"  y1="48"  x2="270" y2="48" stroke-width="0.4"/>
        <line x1="50"  y1="58"  x2="270" y2="58" stroke-width="0.4"/>
        <line x1="50"  y1="68"  x2="270" y2="68" stroke-width="0.4"/>
        <line x1="50"  y1="78"  x2="270" y2="78" stroke-width="0.4"/>
        <line x1="50"  y1="88"  x2="270" y2="88" stroke-width="0.4"/>
        <line x1="50"  y1="98"  x2="270" y2="98" stroke-width="0.4"/>
        <line x1="50"  y1="108" x2="270" y2="108" stroke-width="0.4"/>
        <!-- Column lines (compressed) -->
        <line x1="75"  y1="18" x2="75"  y2="128" stroke-width="0.3" opacity="0.5"/>
        <line x1="95"  y1="18" x2="95"  y2="128" stroke-width="0.3" opacity="0.5"/>
        <line x1="115" y1="18" x2="115" y2="128" stroke-width="0.3" opacity="0.5"/>
        <line x1="135" y1="18" x2="135" y2="128" stroke-width="0.3" opacity="0.5"/>
        <line x1="155" y1="18" x2="155" y2="128" stroke-width="0.3" opacity="0.5"/>
        <line x1="175" y1="18" x2="175" y2="128" stroke-width="0.3" opacity="0.5"/>
        <line x1="195" y1="18" x2="195" y2="128" stroke-width="0.3" opacity="0.5"/>
        <line x1="215" y1="18" x2="215" y2="128" stroke-width="0.3" opacity="0.5"/>
        <line x1="235" y1="18" x2="235" y2="128" stroke-width="0.3" opacity="0.5"/>
        <line x1="255" y1="18" x2="255" y2="128" stroke-width="0.3" opacity="0.5"/>
      </g>
      <!-- Punched holes -->
      <g fill="#1C2D42" opacity="0.3">
        <ellipse cx="75"  cy="33" rx="4" ry="5.5"/><ellipse cx="75"  cy="53" rx="4" ry="5.5"/>
        <ellipse cx="95"  cy="28" rx="4" ry="5.5"/><ellipse cx="95"  cy="78" rx="4" ry="5.5"/>
        <ellipse cx="115" cy="43" rx="4" ry="5.5"/><ellipse cx="135" cy="63" rx="4" ry="5.5"/>
        <ellipse cx="155" cy="33" rx="4" ry="5.5"/><ellipse cx="175" cy="88" rx="4" ry="5.5"/>
        <ellipse cx="195" cy="48" rx="4" ry="5.5"/><ellipse cx="215" cy="28" rx="4" ry="5.5"/>
        <ellipse cx="235" cy="68" rx="4" ry="5.5"/><ellipse cx="255" cy="43" rx="4" ry="5.5"/>
      </g>
      <!-- Counter wheels right -->
      <g stroke="#1C2D42" opacity="0.18" fill="none">
        <circle cx="365" cy="65" r="28" stroke-width="0.8"/>
        <circle cx="365" cy="65" r="17" stroke-width="0.5"/>
        <circle cx="365" cy="65" r="5"  stroke-width="0.5"/>
        <circle cx="435" cy="65" r="28" stroke-width="0.8"/>
        <circle cx="435" cy="65" r="17" stroke-width="0.5"/>
        <circle cx="435" cy="65" r="5"  stroke-width="0.5"/>
        <circle cx="505" cy="65" r="28" stroke-width="0.8"/>
        <circle cx="505" cy="65" r="17" stroke-width="0.5"/>
        <circle cx="505" cy="65" r="5"  stroke-width="0.5"/>
        <!-- Windows -->
        <rect x="354" y="57" width="22" height="16" rx="2" stroke-width="0.7"/>
        <rect x="424" y="57" width="22" height="16" rx="2" stroke-width="0.7"/>
        <rect x="494" y="57" width="22" height="16" rx="2" stroke-width="0.7"/>
      </g>
      <g fill="#1C2D42" opacity="0.35" font-family="JetBrains Mono, monospace" font-size="11" text-anchor="middle">
        <text x="365" y="70">6</text><text x="435" y="70">2</text><text x="505" y="70">9</text>
      </g>
      <!-- Electrical connection dots -->
      <g fill="#C82A2A" opacity="0.5">
        <circle cx="95"  cy="28" r="2.5"/>
        <circle cx="155" cy="33" r="2.5"/>
        <circle cx="215" cy="28" r="2.5"/>
      </g>
      <!-- Labels -->
      <text x="160"  y="135" font-family="JetBrains Mono, monospace" font-size="8" fill="#1C2D42" opacity="0.35" text-anchor="middle">Hollerith card &mdash; 1890</text>
      <text x="435"  y="107" font-family="JetBrains Mono, monospace" font-size="8" fill="#1C2D42" opacity="0.35" text-anchor="middle">tabulator counters</text>
      <rect x="0"   y="0" width="60"  height="140" fill="url(#fl5)"/>
      <rect x="612" y="0" width="60"  height="140" fill="url(#fr5)"/>
    </svg>
  </figure>

  <main class="chapter-body">

    <section aria-labelledby="sect-prob5">
      <h2 class="section-head" id="sect-prob5" style="border-top:none;padding-top:0;margin-top:0;">The Problem</h2>
      <p class="lead drop-cap">It is 1887. The US Census Bureau is staring at the results of the 1880 census &mdash; still being compiled, eight years later. The 1890 census is three years away and will count even more people. At the current rate, the results will still be coming in when the 1900 census begins.</p>
      <p class="body no-indent">A young statistician named Herman Hollerith has an idea. He watched a train conductor punch passenger tickets to record seat, destination, and fare. He remembered Jacquard&rsquo;s loom. He had worked briefly at the Census Bureau himself.</p>
      <p class="body">What if you could encode a person&rsquo;s census data as holes in a card &mdash; and have a machine read, sort, and tally those cards automatically?</p>
      <p class="body">Hollerith&rsquo;s answer to this question didn&rsquo;t just solve the census problem. It invented the data processing industry, gave birth to <abbr title="International Business Machines">IBM</abbr>, and established the punch card as the dominant data storage medium for the next century.</p>
    </section>

    <section aria-labelledby="sect-story5">
      <h2 class="section-head" id="sect-story5">The Story</h2>

      <h3 class="sub-head">The Hollerith Machine &mdash; Three Components</h3>
      <p class="body no-indent">Hollerith&rsquo;s tabulating system had three components working in sequence: a punch, a tabulator, and a sorter.</p>
      <p class="body"><strong>The Pantograph Punch.</strong> An operator sat with the completed paper census form and used a hand punch to create holes in a card at positions corresponding to each answer. Age 34 &rarr; punch position 34. Occupation &ldquo;Farmer&rdquo; &rarr; punch position in the occupations zone. Foreign-born &rarr; punch a specific position. Each card represented one person. The presence or absence of a hole at each position encoded that person&rsquo;s attributes as binary data.</p>
      <p class="body"><strong>The Tabulator.</strong> The card was placed in a press. A grid of spring-loaded pins descended onto the card. Where there was a hole, the pin passed through into a small cup of mercury, completing an electrical circuit. Where there was no hole, the pin was blocked. Each completed circuit incremented a mechanical counter by 1 &mdash; a small gear wheel, driven by an electromagnet rather than a human hand.</p>
      <p class="body">This is the critical link: <strong>a hole in a card &rarr; electrical signal &rarr; counter increments</strong>. The physical hole becomes an electrical event becomes a counted datum.</p>
      <p class="body"><strong>The Sorter.</strong> A separate device sorted cards into bins based on which circuit fired. This allowed operators to group cards by any attribute &mdash; all farmers, all immigrants, all people over 65 &mdash; without manual searching.</p>
"""

h += fig(figs[0], "5.1", wide=True) if len(figs) > 0 else ""
h += fig(figs[2], "5.2") if len(figs) > 2 else ""

h += sb()

h += """
      <h3 class="sub-head">The 1890 Census &mdash; By the Numbers</h3>
"""

h += fig(figs[3], "5.3") if len(figs) > 3 else ""

h += """
      <span class="table-label">Table 5.1</span>
      <div class="table-wrap">
        <table class="book-table" role="table" aria-label="1880 manual census vs 1890 Hollerith census comparison">
          <thead><tr><th scope="col">Metric</th><th scope="col">1880 (manual)</th><th scope="col">1890 (Hollerith)</th></tr></thead>
          <tbody>
            <tr><td>Population counted</td><td class="mono">50,189,209</td><td class="mono">62,979,766</td></tr>
            <tr><td>Time to basic count</td><td class="mono">~2.5 years</td><td class="mono" style="color:var(--sage);font-weight:500">6 weeks</td></tr>
            <tr><td>Time to full tabulation</td><td class="mono">8 years</td><td class="mono">~2.5 years</td></tr>
            <tr><td>Error rate</td><td class="mono">~5%</td><td class="mono">&lt;1%</td></tr>
            <tr class="highlight"><td>Cost</td><td class="mono">~$11.5M</td><td class="mono">~$5M</td></tr>
          </tbody>
        </table>
      </div>
      <p class="table-caption">Table 5.1 &mdash; The 1890 census delivered results in six weeks rather than eight years &mdash; and did so for a larger population at lower cost and with fewer errors. The machine did not just save time. It changed what data was <em>usable for</em>.</p>

      <div class="callout callout-insight" role="note" aria-label="Key Insight">
        <div class="callout-label"><span aria-hidden="true">&#9670;</span> Key Insight</div>
        <p>Six weeks versus eight years is not an optimisation. It is a phase transition. Census data that arrives eight years late cannot influence the policy decisions it was meant to inform &mdash; by then, a new census is needed. Data that arrives in six weeks is <em>actionable</em>. The speed difference changed what the data was good for. This pattern &mdash; where quantitative improvement in speed or scale produces qualitative change in utility &mdash; recurs throughout computing history.</p>
      </div>"""

h += sb()

h += """
      <h3 class="sub-head">The Birth of IBM</h3>
      <p class="body no-indent">Hollerith founded the <strong>Tabulating Machine Company</strong> in 1896 to lease his equipment to businesses. The census had proven the concept; now he applied it to payroll processing, freight statistics, and insurance accounting. The machines were leased, not sold &mdash; the software-as-a-service model of its day.</p>
      <p class="body">In 1911, the company merged with two others to form the Computing-Tabulating-Recording Company (<abbr title="Computing-Tabulating-Recording Company">CTR</abbr>). In 1924, <abbr title="Computing-Tabulating-Recording Company">CTR</abbr> was renamed by its new president, Thomas J. Watson Sr.:</p>
      <p class="body no-indent" style="font-family:var(--font-display);font-size:20px;font-weight:300;color:var(--indigo);text-indent:0;margin:var(--space-md) 0 var(--space-lg);">International Business Machines &mdash; <abbr title="International Business Machines">IBM</abbr>.</p>
      <p class="body no-indent">The 80-column <abbr title="International Business Machines">IBM</abbr> punch card that became standard by 1928 was a direct evolution of Hollerith&rsquo;s original design. It remained the dominant data input medium for computers until the early 1980s &mdash; nine decades of continuous use.</p>
    </section>

    <section aria-labelledby="sect-concept5">
      <h2 class="section-head" id="sect-concept5">The Concept &mdash; Data Encoding</h2>
      <p class="body no-indent">Every data encoding scheme answers the same question: <strong>how do we represent information as a physical state that a machine can read?</strong></p>
      <p class="body">Hollerith&rsquo;s answers: information unit = one census attribute; physical carrier = a stiff card; encoding method = hole position = attribute value; reading method = electrical continuity through hole = 1, blocked = 0; processing = electrical signal drives mechanical counter.</p>
"""

h += fig(figs[1], "5.4") if len(figs) > 1 else ""

h += """
      <h3 class="sub-head">What a Record Is</h3>
      <p class="body no-indent">Hollerith invented the concept of a <strong>record</strong>: a fixed-format collection of fields that together describe one entity &mdash; one person, one transaction, one event.</p>
      <p class="body">Each card = one record. Each column zone = one field. Each hole = one attribute value. This is identical to a row in a database table. A <abbr title="Structured Query Language">SQL</abbr> <code>SELECT&nbsp;*&nbsp;FROM&nbsp;census&nbsp;WHERE&nbsp;occupation='Farmer'</code> is the direct intellectual descendant of Hollerith&rsquo;s card sorter.</p>

      <div class="pull-quote">
        &ldquo;The hole is gone. The bit remains.&rdquo;
      </div>

      <div class="callout callout-future" role="note" aria-label="Future Connection">
        <div class="callout-label"><span aria-hidden="true">&rarr;</span> Future Connection &mdash; Level 2: Digital Foundations; Level 9: Databases</div>
        <p>Hollerith&rsquo;s encoding &mdash; binary position encoding a character &mdash; is the ancestor of <abbr title="American Standard Code for Information Interchange">ASCII</abbr> (1963), the character encoding system still used in every computer today. His record concept is the ancestor of every database table in every relational database system. And his electrical reading mechanism &mdash; presence or absence of a hole closing a circuit &mdash; is the direct ancestor of the transistor switch: present state = 1, absent state = 0.</p>
      </div>
    </section>

    <section aria-labelledby="sect-sim5">
      <h2 class="section-head" id="sect-sim5">Hands-On Exercise</h2>
      <p class="body no-indent">The simulation provides three interconnected tools: a card puncher, a tabulator, and a sorter. Work through the card puncher first to build an intuition for positional encoding, then feed your cards into the tabulator and observe the counter increment in real time.</p>

      <figure class="sim-figure" aria-labelledby="sim5-cap">
        <span class="sim-figure-badge">Interactive</span>
        <span class="sim-figure-label">Figure 5.5 &mdash; Hollerith Tabulating System</span>
        <div class="sim-figure-frame">
          <div class="sim-preview-header">
            <div><div class="sim-preview-title">Hollerith Tabulating System</div><div class="sim-preview-subtitle">Card puncher &middot; Tabulator &middot; Sorter</div></div>
          </div>
          <div class="sim-tabs-preview" aria-hidden="true">
            <div class="sim-tab-p active">Card Puncher</div>
            <div class="sim-tab-p">Tabulator</div>
            <div class="sim-tab-p">Sorter</div>
          </div>
"""

if len(figs) > 4:
    h += f'          <div style="margin:10px 0;border:1px solid var(--ghost);border-radius:2px;overflow:hidden;">{figs[4]["svg"]}</div>\n'

h += """
          <div class="sim-link-row">
            <a href="../../course/level-0-before-computers/module-0-5-hollerith/simulation.html" class="sim-open-btn" target="_blank" rel="noopener noreferrer">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2 2h8v8M10 2L2 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              Open Simulation
            </a>
            <p class="sim-note">Opens in a new tab &middot; No installation required</p>
          </div>
        </div>
        <figcaption class="sim-figure-caption" id="sim5-cap">Figure 5.5 &mdash; Hollerith Tabulating System. Card Puncher: enter a person&rsquo;s census attributes and watch them encoded as holes at specific column positions on the card. Tabulator: feed cards through the press and watch counter wheels increment as each circuit closes. Sorter: load a deck of 10 pre-punched cards, choose a sort key, and observe cards sorted into bins by attribute.</figcaption>
      </figure>

      <div class="callout callout-sim" role="note" aria-label="Walkthrough">
        <div class="callout-label"><span aria-hidden="true">&#9655;</span> Step-by-Step Walkthrough</div>
        <p><strong>Step 1 &mdash; Card Puncher.</strong> Enter your own census data (your age, a occupation, a birthplace). Observe which column positions receive holes. Notice that position is meaning &mdash; the machine has no notion of &ldquo;age&rdquo;; it only knows that a hole in column range 20&ndash;99 corresponds to an age value.</p>
        <p style="margin-top:8px"><strong>Step 2 &mdash; Tabulator.</strong> Feed your card through the virtual press. Watch the spring-loaded pins descend. Observe which circuits close (holes) and which are blocked (no holes). Watch the corresponding counters increment.</p>
        <p style="margin-top:8px"><strong>Step 3 &mdash; Sorter.</strong> Load the pre-punched deck. Sort by occupation. Then sort by age group. Notice: the cards did not change. The sort key changed. The machine reads the same physical data through a different interpretive lens each time.</p>
      </div>
    </section>

    <section aria-labelledby="sect-deeper5">
      <h2 class="section-head" id="sect-deeper5">Going Deeper</h2>
      <div class="callout callout-deep" role="note" aria-label="Deep Dive">
        <div class="callout-label"><span aria-hidden="true">&nabla;</span> The Legacy: From Holes to Bits</div>
        <p>Trace the lineage from Jacquard to Hollerith to modern computing:</p>
        <p style="margin-top:var(--space-sm);font-family:var(--font-mono);font-size:12px;line-height:2;color:var(--ink);">
          Jacquard loom (1804): hole in card &rarr; thread lifts &rarr; stored weaving instructions<br>
          Hollerith tabulator (1890): hole in card &rarr; electrical circuit closes &rarr; counter increments<br>
          IBM punch cards (1928&ndash;1980s): 80 &times; 12 = 960 bit positions per card<br>
          Magnetic storage (1950s): magnetic domain = bit<br>
          Semiconductor memory (1970s): transistor state = bit
        </p>
        <p style="margin-top:var(--space-sm)">The hole is gone. The bit remains. And the bit is the hole in Jacquard&rsquo;s card, abstracted through two centuries of technology changes.</p>
      </div>
    </section>

    <!-- Level 0 Capstone Review -->
    <section aria-labelledby="sect-capstone" style="margin-top:var(--space-2xl);padding-top:var(--space-xl);border-top:1.5px solid var(--ink);max-width:var(--text-width);">
      <h2 class="section-head" id="sect-capstone" style="border-top:none;padding-top:0;margin-top:0;">Level 0 Capstone &mdash; What You Can Now Answer</h2>
      <p class="body no-indent">Before moving to Level 1, you should be able to answer these questions from memory:</p>
      <ol style="margin: var(--space-md) 0 var(--space-md) var(--space-xl); max-width: var(--text-width); list-style: decimal;">
        <li style="font-family:var(--font-body);font-size:17px;line-height:1.78;color:var(--ink);margin-bottom:10px;">Why did mechanical computation become necessary? (Chapter 1)</li>
        <li style="font-family:var(--font-body);font-size:17px;line-height:1.78;color:var(--ink);margin-bottom:10px;">How did mechanical devices encode numbers in physical state? (Chapter 2)</li>
        <li style="font-family:var(--font-body);font-size:17px;line-height:1.78;color:var(--ink);margin-bottom:10px;">What does &ldquo;stored instructions&rdquo; mean, and where did the concept come from? (Chapter 3)</li>
        <li style="font-family:var(--font-body);font-size:17px;line-height:1.78;color:var(--ink);margin-bottom:10px;">What is the difference between a calculator and a computer? (Chapter 4)</li>
        <li style="font-family:var(--font-body);font-size:17px;line-height:1.78;color:var(--ink);">How does a hole in a card become a counted datum? (Chapter 5)</li>
      </ol>
      <div class="callout callout-future" role="note" aria-label="Next Level">
        <div class="callout-label"><span aria-hidden="true">&rarr;</span> Next &mdash; Level 1: Physical Computing</div>
        <p>Gear gave way to the electron. Level 1 traces the path from basic electricity to the transistor: voltage as information, switches as binary devices, and the relay, vacuum tube, and transistor as successive answers to the same question &mdash; how do you build a switch that is faster, smaller, cheaper, and more reliable than the one before it? Each generation was approximately 1,000 times faster <em>and</em> 1,000 times smaller than its predecessor. You will follow that exponential trajectory step by step.</p>
      </div>
    </section>

    <section aria-labelledby="challenge-05" class="challenge-section">
      <header class="challenge-header">
        <div class="challenge-num" aria-hidden="true">0.5</div>
        <div class="challenge-title-block">
          <p class="challenge-overline">Challenge</p>
          <h2 class="challenge-title" id="challenge-05">Encoding, Tabulating, and Decoding</h2>
          <div class="challenge-meta">
            <span class="challenge-meta-item">Simulation exercise</span>
            <span class="challenge-meta-item">25&ndash;30 minutes</span>
          </div>
        </div>
      </header>
      <div class="challenge-setup">
        <p class="challenge-setup-label">Setup</p>
        <p>Five census records are provided below. Use the simulation to punch, tabulate, and sort them.</p>
        <p>Records: Thomas, age 42, Farmer, Virginia, family 6 &middot; Mary, age 29, Seamstress, Poland, family 4 &middot; James, age 55, Blacksmith, Ireland, family 3 &middot; Sarah, age 34, Teacher, New York, family 2 &middot; Eli, age 67, Retired, Germany, family 1.</p>
      </div>
      <div class="challenge-part">
        <p class="challenge-part-label"><span>Part A</span> Encode and Tabulate</p>
        <ol class="challenge-questions">
          <li data-sub="1"><p>Punch all five records. For Thomas&rsquo;s card, write the column positions that receive holes (age zone, occupation zone, birthplace zone).</p></li>
          <li data-sub="2"><p>Run the tabulator on all five cards. What do the counters show for: total records, total farmers, foreign-born count?</p></li>
        </ol>
      </div>
      <div class="challenge-part">
        <p class="challenge-part-label"><span>Part B</span> Sort and Interpret</p>
        <ol class="challenge-questions" style="counter-reset: q-counter 2">
          <li data-sub="3"><p>Sort the deck by occupation. Which bin contains the most cards? Which bins are empty?</p></li>
          <li data-sub="4"><p>Sort by age group (under 35, 35&ndash;55, over 55). How does the distribution change compared to the occupation sort?</p></li>
          <li data-sub="5"><p>In two sentences: why is sorting by a different attribute faster than manually searching through paper census forms? What physical property of the machine enables this?</p></li>
        </ol>
      </div>
    </section>

    <section aria-labelledby="summary-05" class="chapter-summary">
      <h2 class="section-head" id="summary-05" style="border-top:none;padding-top:0;margin-top:0;">Summary</h2>
      <p class="body no-indent">Hollerith&rsquo;s tabulating machine closes the loop that Jacquard opened.</p>
      <p class="body">Jacquard proved that instructions could be stored in holes and read by a machine. Hollerith proved that <em>data</em> could be stored in holes and processed by a machine. Together, they established the foundation of information processing: encode information as binary physical states, read those states electrically, and use the resulting signals to drive mechanical or electronic operations.</p>
      <p class="body">The census of 1890 was not merely faster than the census of 1880. It was the first demonstration at industrial scale that data processing was a separable activity &mdash; something that could be done by a machine, not just by a human mind. Every spreadsheet, every database query, every data pipeline in the modern world is the descendant of Hollerith&rsquo;s press, his mercury cups, and the 62 million cards punched for the United States Census of 1890.</p>
      <div class="section-break" role="separator" aria-hidden="true"><div class="sb-line"></div><div class="sb-dot"></div><div class="sb-dot"></div><div class="sb-dot"></div><div class="sb-line"></div></div>
      <div class="chapter-nav">
        <div class="nav-prev"><p class="nav-label">Previous &mdash; Module 0.4</p><p class="nav-title">&larr; Babbage and Ada</p></div>
        <div class="nav-next"><p class="nav-label">Next &mdash; Level 1, Module 1.1</p><p class="nav-title">What is Electricity? &rarr;</p></div>
      </div>
    </section>

  </main>
  <footer class="page-footer" role="contentinfo">
    <span class="page-footer-series">AoPS &mdash; Volume 0</span>
    <span class="page-num">7</span>
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

out = BASE / "ebook/level-0/chapter-5/chapter-5.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(h, "utf-8")
print(f"chapter-5.html: {len(h):,} chars  ({len(h)//1024} KB)")
