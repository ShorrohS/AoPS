"""
AoPS Review Edition PDF Generator v2
Produces: AoPS_Review_Edition_v1.pdf
Robust build: no multiBuild ToC, direct story construction.
"""

import os, re, sys, json
from pathlib import Path
from datetime import datetime

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import markdown

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, Preformatted
)

# ── Paths ──────────────────────────────────────────────────────────────────
BASE        = Path(__file__).resolve().parent
COURSE_DIR  = BASE / "course"
ILLUS_DIR   = BASE / "illustrations"
OUT_PDF     = BASE / "AoPS_Review_Edition_v1.pdf"

# ── Palette ────────────────────────────────────────────────────────────────
C_INK    = colors.HexColor("#2C2C2C")
C_STONE  = colors.HexColor("#6E6E6E")
C_BAMBOO = colors.HexColor("#728C69")
C_INDIGO = colors.HexColor("#2E4057")
C_RED    = colors.HexColor("#C82A2A")
C_GOLD   = colors.HexColor("#8B6914")
C_SAND   = colors.HexColor("#F4EFE6")
C_PAPER  = colors.HexColor("#F4F3EF")
C_BORDER = colors.HexColor("#D8D6CE")
C_WHITE  = colors.white
C_LITE   = colors.HexColor("#EEECE6")

PAGE_W, PAGE_H = A4
ML = 22*mm;  MR = 22*mm
MT = 26*mm;  MB = 38*mm   # extra bottom for footer
TW = PAGE_W - ML - MR     # text width

DRAFT = "DRAFT REVIEW EDITION"

# ── Report accumulator ─────────────────────────────────────────────────────
RPT = {
    "levels": [], "modules": [], "figure_count": 0,
    "missing_lessons": [], "missing_illustrations": [], "missing_challenges": []
}

# ── Style factory ──────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

STYLES = {
    # Cover
    "ctitle":   S("ctitle",   fontName="Helvetica-Bold",   fontSize=34, textColor=C_INDIGO, alignment=TA_CENTER, leading=40, spaceAfter=8),
    "csub":     S("csub",     fontName="Helvetica",         fontSize=15, textColor=C_STONE,  alignment=TA_CENTER, leading=20, spaceAfter=6),
    "cmeta":    S("cmeta",    fontName="Helvetica",         fontSize=10, textColor=C_STONE,  alignment=TA_CENTER, leading=14),
    "cdraft":   S("cdraft",   fontName="Helvetica-Bold",    fontSize=11, textColor=C_RED,    alignment=TA_CENTER, leading=14),
    # Level page
    "lnum":     S("lnum",     fontName="Helvetica-Bold",    fontSize=10, textColor=C_WHITE,  alignment=TA_CENTER, leading=14),
    "ltitle":   S("ltitle",   fontName="Helvetica-Bold",    fontSize=28, textColor=C_WHITE,  alignment=TA_CENTER, leading=34, spaceBefore=4),
    "lsub":     S("lsub",     fontName="Helvetica",         fontSize=12, textColor=colors.HexColor("#BBBBB5"), alignment=TA_CENTER, leading=18, spaceBefore=8),
    # Module
    "mcode":    S("mcode",    fontName="Helvetica-Bold",    fontSize=9,  textColor=C_GOLD,   leading=12, spaceBefore=2),
    "mtitle":   S("mtitle",   fontName="Helvetica-Bold",    fontSize=20, textColor=C_INDIGO, leading=26, spaceAfter=2),
    # Headings
    "h2":       S("h2",       fontName="Helvetica-Bold",    fontSize=14, textColor=C_INDIGO, leading=18, spaceBefore=14, spaceAfter=4),
    "h3":       S("h3",       fontName="Helvetica-Bold",    fontSize=11, textColor=C_INK,    leading=16, spaceBefore=10, spaceAfter=3),
    "h4":       S("h4",       fontName="Helvetica-Bold",    fontSize=10, textColor=C_STONE,  leading=14, spaceBefore=6,  spaceAfter=2),
    # Body
    "body":     S("body",     fontName="Helvetica",         fontSize=10, textColor=C_INK,    leading=15, spaceAfter=5, alignment=TA_JUSTIFY),
    # Code
    "code":     S("code",     fontName="Courier",           fontSize=8.5, textColor=C_INK,   leading=12, backColor=colors.HexColor("#F8F7F3"),
                              leftIndent=10, rightIndent=10, spaceBefore=4, spaceAfter=4),
    # Special
    "figid":    S("figid",    fontName="Helvetica-Bold",    fontSize=8,  textColor=C_GOLD,   leading=11, spaceAfter=1),
    "figcap":   S("figcap",   fontName="Helvetica",         fontSize=8.5,textColor=C_STONE,  leading=12, spaceBefore=2, spaceAfter=6, alignment=TA_JUSTIFY),
    "ph":       S("ph",       fontName="Helvetica-Oblique", fontSize=9,  textColor=C_STONE,  leading=13, spaceBefore=3, spaceAfter=3),
    "chlabel":  S("chlabel",  fontName="Helvetica-Bold",    fontSize=8.5,textColor=C_WHITE,  leading=12, leftIndent=8),
    "chbody":   S("chbody",   fontName="Helvetica",         fontSize=9.5,textColor=C_INK,    leading=14, leftIndent=8, spaceAfter=4, alignment=TA_JUSTIFY),
    "simlabel": S("simlabel", fontName="Helvetica-Bold",    fontSize=8.5,textColor=C_WHITE,  leading=12, leftIndent=8),
    "simbody":  S("simbody",  fontName="Helvetica",         fontSize=9,  textColor=C_INK,    leading=14, leftIndent=8, spaceAfter=3),
    "toc0":     S("toc0",     fontName="Helvetica-Bold",    fontSize=11, textColor=C_INDIGO, leading=16, spaceAfter=2, leftIndent=0),
    "toc1":     S("toc1",     fontName="Helvetica",         fontSize=9.5,textColor=C_INK,    leading=14, spaceAfter=1, leftIndent=14),
    "footer":   S("footer",   fontName="Helvetica",         fontSize=7.5,textColor=C_STONE,  leading=10),
}


# ── Page decoration ────────────────────────────────────────────────────────
def on_page(canv, doc):
    w, h = A4
    canv.saveState()
    # top hairline
    canv.setStrokeColor(C_BORDER); canv.setLineWidth(0.4)
    canv.line(ML, h - MT + 4*mm, w - MR, h - MT + 4*mm)
    # bottom rule
    canv.line(ML, MB - 8*mm, w - MR, MB - 8*mm)
    # footer text
    canv.setFont("Helvetica", 7.5); canv.setFillColor(C_STONE)
    canv.drawString(ML, MB - 13*mm, DRAFT)
    canv.drawString(ML, MB - 20*mm, "Art of Problem Solving — Computer Science Course")
    canv.setFont("Helvetica-Bold", 7.5)
    canv.drawRightString(w - MR, MB - 13*mm, f"Page {doc.page}")
    canv.restoreState()


# ── Markdown parser ────────────────────────────────────────────────────────
def safe_para(text, style):
    """Return Paragraph, falling back to plain text on XML error."""
    text = (text or "").strip()
    if not text:
        return None
    try:
        return Paragraph(text, style)
    except Exception:
        clean = re.sub(r"<[^>]+>", "", text)
        try:
            return Paragraph(clean, style)
        except Exception:
            return Paragraph("...", style)


def escape_xml(t):
    return (t.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))


def inline_fmt(t):
    """Apply basic inline markdown formatting."""
    t = escape_xml(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    t = re.sub(r"`(.+?)`", lambda m: f"<font name='Courier'>{escape_xml(m.group(1))}</font>", t)
    return t


def md_to_story(text, max_chars=7000):
    """Convert markdown text to list of reportlab flowables."""
    if not text:
        return []
    text = text[:max_chars]
    flow = []
    lines = text.split("\n")
    buf = []
    in_code = False
    code_buf = []

    def flush():
        if not buf:
            return
        joined = " ".join(l.strip() for l in buf if l.strip())
        buf.clear()
        if not joined:
            return
        p = safe_para(inline_fmt(joined), STYLES["body"])
        if p:
            flow.append(p)

    for line in lines:
        if line.startswith("```"):
            flush()
            if in_code:
                flow.append(Preformatted("\n".join(code_buf), STYLES["code"]))
                code_buf.clear(); in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue

        # Headings
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            flush()
            lvl = len(m.group(1))
            txt = inline_fmt(m.group(2).strip())
            sty = {1:"h2",2:"h2",3:"h3",4:"h4"}.get(lvl,"h3")
            p = safe_para(txt, STYLES[sty])
            if p: flow.append(p)
            continue

        # Blockquote
        if line.startswith("> "):
            flush()
            p = safe_para(f"<i>{inline_fmt(line[2:].strip())}</i>", STYLES["body"])
            if p: flow.append(p)
            continue

        # List items
        if re.match(r"^[-*+]\s", line):
            flush()
            p = safe_para("&bull; " + inline_fmt(line[2:].strip()), STYLES["body"])
            if p: flow.append(p)
            continue
        if re.match(r"^\d+\.\s", line):
            flush()
            content = re.sub(r"^\d+\.\s*", "", line)
            p = safe_para(inline_fmt(content.strip()), STYLES["body"])
            if p: flow.append(p)
            continue

        # HR
        if re.match(r"^[-_*]{3,}$", line.strip()):
            flush()
            flow.append(HRFlowable(width="100%", thickness=0.4, color=C_BORDER, spaceAfter=4))
            continue

        # Empty line
        if not line.strip():
            flush()
            continue

        buf.append(line)

    flush()
    if in_code and code_buf:
        flow.append(Preformatted("\n".join(code_buf), STYLES["code"]))

    return flow


# ── Level metadata ─────────────────────────────────────────────────────────
LEVEL_META = {
    "level-0-before-computers":  ("00","Before Computers","The Human Problem that Forced Computation into Existence"),
    "level-1-physical-computing":("01","Physical Computing","From Electricity to Logic — The Birth of Electronic Computation"),
    "level-2-digital-foundations":("02","Digital Foundations","Binary, Boolean Algebra, and the Language of Machines"),
    "level-3-machine-architecture":("03","Machine Architecture","How CPUs Fetch, Decode, and Execute Instructions"),
    "level-4-software-foundations":("04","Software Foundations","From Machine Code to Operating Systems"),
    "level-5-programming":        ("05","Programming","C, Python, Algorithms, and Computational Thinking"),
    "level-6-dsa":                ("06","Data Structures & Algorithms","Organising Information for Efficient Computation"),
    "level-7-systems":            ("07","Systems Programming","Concurrency, Sockets, Shells, and HTTP Servers"),
    "level-8-networks":           ("08","Networks & Protocols","From Bits on Wire to HTTPS — The Internet Layer by Layer"),
    "level-9-databases":          ("09","Databases","Relational Models, B-Trees, Transactions, and SQL Engines"),
    "level-10-web":               ("10","Web & Application Dev","HTML, Browsers, REST APIs, and Full-Stack Architecture"),
    "level-11-ai-ml":             ("11","AI & Machine Learning","Search, Neural Networks, Backpropagation, and Learning Theory"),
    "level-12-advanced-ai":       ("12","Advanced AI","LLMs, Embeddings, RAG, Agents, Ethics, and Safety"),
}

ILLUS_LEVEL_MAP = {
    "level-0-before-computers":"level-0","level-1-physical-computing":"level-1",
    "level-2-digital-foundations":"level-2","level-3-machine-architecture":"level-3",
    "level-4-software-foundations":"level-4","level-5-programming":"level-5",
    "level-6-dsa":"level-6","level-7-systems":"level-7","level-8-networks":"level-8",
    "level-9-databases":"level-9","level-10-web":"level-10",
    "level-11-ai-ml":"level-11","level-12-advanced-ai":"level-12",
}


# ── Cover ──────────────────────────────────────────────────────────────────
def make_cover():
    s = []
    s.append(Spacer(1, 55*mm))
    s.append(safe_para("AoPS", STYLES["ctitle"]))
    s.append(safe_para("Art of Problem Solving", STYLES["csub"]))
    s.append(Spacer(1, 4*mm))
    s.append(HRFlowable(width="50%", thickness=1, color=C_INDIGO, hAlign="CENTER", spaceAfter=4))
    s.append(Spacer(1, 4*mm))
    s.append(safe_para("Computer Science Course", STYLES["csub"]))
    s.append(Spacer(1, 10*mm))
    s.append(safe_para("Review Edition &mdash; Volume I", STYLES["cmeta"]))
    s.append(safe_para("Levels 0 &ndash; 12 &bull; Complete Course Content", STYLES["cmeta"]))
    s.append(Spacer(1, 8*mm))
    s.append(safe_para(DRAFT, STYLES["cdraft"]))
    s.append(Spacer(1, 6*mm))
    s.append(safe_para(f"Generated {datetime.now().strftime('%B %Y')} &bull; Internal Review Only", STYLES["cmeta"]))
    s.append(PageBreak())
    return s


# ── ToC page ───────────────────────────────────────────────────────────────
def make_toc_page(toc_entries):
    """Build a static ToC page from collected entries."""
    s = []
    s.append(safe_para("Table of Contents", STYLES["h2"]))
    s.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER, spaceAfter=6))
    s.append(Spacer(1, 4*mm))
    for entry_type, text in toc_entries:
        if entry_type == 0:
            p = safe_para(text, STYLES["toc0"])
            if p: s.append(p)
        else:
            p = safe_para(text, STYLES["toc1"])
            if p: s.append(p)
    s.append(PageBreak())
    return s


# ── Preface ────────────────────────────────────────────────────────────────
def make_preface():
    s = []
    s.append(safe_para("About This Review Document", STYLES["h2"]))
    s.append(safe_para(
        "This is a draft review edition of the Art of Problem Solving (AoPS) Computer Science Course, "
        "covering all 13 levels from Level 0 (Before Computers) through Level 12 (Advanced AI). "
        "It is produced for internal quality review, structural assessment, and content completeness checking.",
        STYLES["body"]))
    s.append(Spacer(1,3*mm))
    s.append(safe_para("Document Structure", STYLES["h3"]))
    s.append(safe_para(
        "Each level opens with a separator page. Each module contains: the lesson narrative, "
        "hands-on simulation summary, illustration figures, and a challenge question. "
        "Illustrations are embedded as figure descriptions referencing the SVG source files. "
        "Interactive simulations are summarised with a description box.",
        STYLES["body"]))
    s.append(safe_para(
        "Placeholders indicate sections that exist as interactive HTML content (JavaScript "
        "simulations, animations) which cannot be rendered in static PDF. These are expected "
        "and do not indicate missing content.",
        STYLES["body"]))
    s.append(Spacer(1,3*mm))
    s.append(safe_para("Figure Numbering", STYLES["h3"]))
    s.append(safe_para(
        "Figures are numbered sequentially across the entire document. "
        "Each figure references its source illustration file for the full interactive version.",
        STYLES["body"]))
    s.append(PageBreak())
    return s


# ── Level separator ────────────────────────────────────────────────────────
def make_level_page(lvl_dir, num, title, subtitle):
    s = []
    inner = [
        [safe_para(f"LEVEL {num}", STYLES["lnum"])],
        [Spacer(1, 3*mm)],
        [safe_para(title, STYLES["ltitle"])],
        [Spacer(1, 4*mm)],
        [safe_para(subtitle, STYLES["lsub"])],
    ]
    flat_inner = [row[0] for row in inner]
    t = Table([[flat_inner]], colWidths=[TW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), C_INDIGO),
        ("TOPPADDING",    (0,0),(-1,-1), 44),
        ("BOTTOMPADDING", (0,0),(-1,-1), 44),
        ("LEFTPADDING",   (0,0),(-1,-1), 24),
        ("RIGHTPADDING",  (0,0),(-1,-1), 24),
    ]))
    s.append(t)

    # README summary
    readme = lvl_dir / "README.md"
    if readme.exists():
        s.append(Spacer(1, 6*mm))
        text = readme.read_text(encoding="utf-8", errors="replace")
        # skip H1 (already in banner)
        body = re.sub(r"^#[^#].*\n?", "", text, count=1).strip()
        s += md_to_story(body[:1200])

    s.append(PageBreak())
    return s


# ── Illustrations ──────────────────────────────────────────────────────────
def find_illus(lvl_name, mod_name):
    illus_lvl = ILLUS_LEVEL_MAP.get(lvl_name,"")
    if not illus_lvl:
        return None
    ldir = ILLUS_DIR / illus_lvl
    m = re.match(r"(module-\d+-\d+)", mod_name)
    if m:
        for f in ldir.glob(f"{m.group(1)}*.html"):
            return f
    return None


def make_illus(illus_path):
    if not illus_path or not illus_path.exists():
        return []
    try:
        html = illus_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    fig_ids    = re.findall(r'class="fig-id"[^>]*>\s*([^<]+)\s*<', html)
    fig_titles = re.findall(r'class="fig-title"[^>]*>\s*([^<]+)\s*<', html)
    fig_caps   = re.findall(r'class="fig-caption"[^>]*>(.*?)</div>', html, re.DOTALL)

    flow = []
    for i, (fid, ftitle) in enumerate(zip(fig_ids, fig_titles)):
        RPT["figure_count"] += 1
        gnum = RPT["figure_count"]
        fid   = fid.strip(); ftitle = ftitle.strip()
        cap   = re.sub(r"<[^>]+>","", fig_caps[i] if i < len(fig_caps) else "").strip()
        cap   = re.sub(r"\s+"," ", cap)[:600]

        ph_text = (f"Illustration: {fid} | {ftitle[:70]}"
                   f"  [SVG diagram — see {illus_path.name}]")

        fig_block = [
            safe_para(f"Figure {gnum} &bull; {escape_xml(fid)}", STYLES["figid"]),
            safe_para(escape_xml(ftitle), STYLES["h4"]),
            Table(
                [[safe_para(escape_xml(ph_text), STYLES["ph"])]],
                colWidths=[TW - 4*mm], rowHeights=[22*mm]
            ),
        ]
        if cap:
            fig_block.append(safe_para(escape_xml(cap), STYLES["figcap"]))

        box = Table([[fig_block]], colWidths=[TW])
        box.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), C_SAND),
            ("LINEBEFORE",    (0,0),(0,-1), 2, C_GOLD),
            ("LINEBELOW",     (0,0),(-1,-1), 0.4, C_BORDER),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
            ("LEFTPADDING",   (0,0),(-1,-1), 10),
            ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ]))
        flow.append(box)
        flow.append(Spacer(1, 4*mm))
    return flow


# ── Challenge box ──────────────────────────────────────────────────────────
def make_challenge(text):
    if not text.strip():
        return []
    # grab the first challenge block
    body = re.sub(r"#+ ", "", text)
    body = re.sub(r"[^\x20-\x7E\n]", "", body)  # ASCII only for safety
    body = body.strip()[:600]

    t = Table([
        [[safe_para("CHALLENGE", STYLES["chlabel"])]],
        [[safe_para(escape_xml(body), STYLES["chbody"])]],
    ], colWidths=[TW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,0), C_RED),
        ("BACKGROUND",    (0,1),(0,1), colors.HexColor("#FDF5F5")),
        ("BOX",           (0,0),(-1,-1), 0.5, C_RED),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
    ]))
    return [t, Spacer(1, 4*mm)]


# ── Simulation summary ─────────────────────────────────────────────────────
def make_sim(sim_path):
    if not sim_path or not sim_path.exists():
        return []
    try:
        html = sim_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    title_m = re.search(r"<title>([^<]+)</title>", html)
    title = title_m.group(1).strip()[:80] if title_m else "Interactive Simulation"
    title = re.sub(r"[^\x20-\x7E]", "", title)

    # Get any description text
    sub_m = re.search(r'class="zen-subtitle[^"]*">([^<]+)<', html)
    desc = sub_m.group(1).strip()[:200] if sub_m else ""
    desc = re.sub(r"[^\x20-\x7E]", "", desc)

    body_text = f"{title}"
    if desc:
        body_text += f": {desc}"
    body_text += f"  [Interactive HTML — open {sim_path.name} in browser to run]"

    t = Table([
        [[safe_para("INTERACTIVE SIMULATION", STYLES["simlabel"])]],
        [[safe_para(escape_xml(body_text), STYLES["simbody"])]],
    ], colWidths=[TW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,0), C_BAMBOO),
        ("BACKGROUND",    (0,1),(0,1), colors.HexColor("#F0F5F0")),
        ("BOX",           (0,0),(-1,-1), 0.5, C_BAMBOO),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
    ]))
    return [t, Spacer(1, 4*mm)]


# ── Module ─────────────────────────────────────────────────────────────────
def make_module(lvl_name, mod_dir, toc_entries):
    s = []

    lesson_f    = mod_dir / "lesson.md"
    challenge_f = mod_dir / "challenge.md"
    sim_f       = mod_dir / "simulation.html"

    lesson_text = ""
    if lesson_f.exists():
        lesson_text = lesson_f.read_text(encoding="utf-8", errors="replace")
    else:
        RPT["missing_lessons"].append(mod_dir.name)

    challenge_text = ""
    if challenge_f.exists():
        challenge_text = challenge_f.read_text(encoding="utf-8", errors="replace")
    else:
        RPT["missing_challenges"].append(mod_dir.name)

    # Extract module code + title
    mod_title = mod_dir.name.replace("-"," ").title()
    mod_code  = ""
    if lesson_text:
        h1 = re.search(r"^#\s+(.+)", lesson_text, re.MULTILINE)
        if h1:
            raw = h1.group(1).strip()
            cm = re.match(r"(Module\s+[\d.]+)\s*[--]\s*(.+)", raw)
            if cm:
                mod_code  = cm.group(1).strip()
                mod_title = cm.group(2).strip()
            else:
                mod_title = raw
    mod_title = re.sub(r"[^\x20-\x7E]","",mod_title)
    mod_code  = re.sub(r"[^\x20-\x7E]","",mod_code)

    # ToC entry
    label = f"{mod_code} — {mod_title}" if mod_code else mod_title
    toc_entries.append((1, escape_xml(label[:80])))

    # Heading
    if mod_code:
        p = safe_para(escape_xml(mod_code.upper()), STYLES["mcode"])
        if p: s.append(p)
    p = safe_para(escape_xml(mod_title), STYLES["mtitle"])
    if p: s.append(p)
    s.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER, spaceAfter=5))

    # Lesson content
    if lesson_text:
        body = re.sub(r"^#[^#].*\n?", "", lesson_text, count=1).strip()
        s += md_to_story(body[:6000])
    else:
        s.append(safe_para("[MISSING: lesson.md not found for this module]", STYLES["ph"]))

    s.append(Spacer(1, 5*mm))

    # Illustrations
    illus_f = find_illus(lvl_name, mod_dir.name)
    if illus_f:
        s.append(safe_para("Illustrations", STYLES["h3"]))
        s += make_illus(illus_f)
    else:
        RPT["missing_illustrations"].append(mod_dir.name)
        s.append(safe_para(
            f"[Illustration file not found for {mod_dir.name}]", STYLES["ph"]))

    # Simulation
    if sim_f.exists():
        s.append(safe_para("Hands-On Simulation", STYLES["h3"]))
        s += make_sim(sim_f)

    # Challenge
    if challenge_text:
        s += make_challenge(challenge_text)

    s.append(Spacer(1, 6*mm))
    s.append(HRFlowable(width="100%", thickness=0.3, color=C_BORDER, spaceAfter=8))

    return s


# ── Main ───────────────────────────────────────────────────────────────────
def generate():
    print("=== AoPS Review Edition PDF Generator ===")
    print(f"Output: {OUT_PDF}")

    story = []
    toc_entries = []   # (level, text)  built during story construction

    # Cover
    story += make_cover()

    # Preface
    story += make_preface()

    # Placeholder for ToC — will be replaced after scan
    toc_placeholder_idx = len(story)
    story.append(Spacer(1, 1))  # replaced later

    # Content
    def level_sort_key(d):
        # extract numeric prefix: level-0-..., level-10-... → 0, 10
        m = re.match(r"level-(\d+)", d.name)
        return int(m.group(1)) if m else 99
    level_dirs = sorted([d for d in COURSE_DIR.iterdir() if d.is_dir()], key=level_sort_key)

    for lvl_dir in level_dirs:
        lvl_name = lvl_dir.name
        if lvl_name not in LEVEL_META:
            continue

        num, title, subtitle = LEVEL_META[lvl_name]
        RPT["levels"].append(lvl_name)
        print(f"  Level {num}: {title}")

        # Level separator
        story += make_level_page(lvl_dir, num, title, subtitle)

        # ToC level entry
        toc_entries.append((0, f"Level {num} -- {title}"))

        # Modules
        mod_dirs = sorted([d for d in lvl_dir.iterdir() if d.is_dir()], key=lambda d: d.name)
        for mod_dir in mod_dirs:
            has_content = any([
                (mod_dir/"lesson.md").exists(),
                (mod_dir/"challenge.md").exists(),
                (mod_dir/"simulation.html").exists()
            ])
            if not has_content:
                continue
            RPT["modules"].append(mod_dir.name)
            print(f"    {mod_dir.name}")
            story += make_module(lvl_name, mod_dir, toc_entries)

        story.append(PageBreak())

    # Replace ToC placeholder with real ToC
    toc_pages = make_toc_page(toc_entries)
    story[toc_placeholder_idx:toc_placeholder_idx+1] = toc_pages

    # Build PDF
    print("\nBuilding PDF...")
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        leftMargin=ML, rightMargin=MR,
        topMargin=MT, bottomMargin=MB,
        title="AoPS CS Course Review Edition",
        author="AoPS Course Team",
        subject="Draft Review",
    )
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

    # Summary
    pdf_mb = OUT_PDF.stat().st_size / (1024*1024)
    print(f"\nPDF written: {OUT_PDF.name}  ({pdf_mb:.1f} MB)")

    print("\n" + "="*56)
    print("GENERATION SUMMARY")
    print("="*56)
    print(f"  Output file         : {OUT_PDF.name}")
    print(f"  File size           : {pdf_mb:.1f} MB")
    print(f"  Levels included     : {len(RPT['levels'])}")
    print(f"  Modules included    : {len(RPT['modules'])}")
    print(f"  Figures embedded    : {RPT['figure_count']}")
    print(f"  Missing lessons     : {len(RPT['missing_lessons'])}")
    print(f"  Missing challenges  : {len(RPT['missing_challenges'])}")
    print(f"  Missing illus.      : {len(RPT['missing_illustrations'])}")
    if RPT["missing_illustrations"]:
        for x in RPT["missing_illustrations"][:8]:
            print(f"    - {x}")
    print("="*56)

    # JSON summary
    summary = {
        "file": "AoPS_Review_Edition_v1.pdf",
        "size_mb": round(pdf_mb, 2),
        "levels_included": len(RPT["levels"]),
        "modules_included": len(RPT["modules"]),
        "figures_embedded": RPT["figure_count"],
        "missing_lessons": RPT["missing_lessons"],
        "missing_challenges": RPT["missing_challenges"],
        "missing_illustrations": RPT["missing_illustrations"],
        "generated": datetime.now().isoformat(),
    }
    sj = BASE / "AoPS_PDF_Summary.json"
    sj.write_text(json.dumps(summary, indent=2))
    print(f"\n  Summary JSON        : {sj.name}")
    print("="*56)


if __name__ == "__main__":
    generate()
