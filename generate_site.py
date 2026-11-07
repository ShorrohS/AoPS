#!/usr/bin/env python3
"""
AoPS GitHub Pages Site Generator
Builds:
  1. Standalone responsive HTML for every lesson (70 modules)
  2. Standalone responsive HTML for every challenge (70 modules)
  3. Master course index (index.html) with direct links, filters, and mobile UX
  4. Universal dynamic markdown reader (reader.html)
  5. .nojekyll for GitHub Pages
"""

import os
import re
import json
import html
from pathlib import Path
from markdown_it import MarkdownIt

# Initialize Markdown processor
md_parser = MarkdownIt("commonmark", {"html": True, "breaks": True, "typographer": True}).enable(["table"])

BASE_DIR = Path(__file__).resolve().parent

LEVELS_META = [
    {
        "id": "level-0-before-computers",
        "num": 0,
        "name": "Level 0",
        "title": "Before Computers",
        "category": "hardware",
        "theme": "Census crisis, Napier bones, Pascaline, Jacquard loom, Babbage, Hollerith",
        "desc": "How humans computed before electricity: counting, mechanical gears, punched cards, and algorithmic logic.",
        "ebook": "ebook/level-0-ebook.html",
        "illustrations": "illustrations/index.html#level-0"
    },
    {
        "id": "level-1-physical-computing",
        "num": 1,
        "name": "Level 1",
        "title": "Physical Computing",
        "category": "hardware",
        "theme": "Electricity, switches, relay logic, vacuum tubes, transistors, Moore's Law",
        "desc": "From physical electrons to logic gates: relays, thermionic valves, semiconductors, and silicon lithography.",
        "ebook": "ebook/level-1-ebook.html",
        "illustrations": "illustrations/index.html#level-1"
    },
    {
        "id": "level-2-digital-foundations",
        "num": 2,
        "name": "Level 2",
        "title": "Digital Foundations",
        "category": "hardware",
        "theme": "Binary physics, number systems, logic gates, combinational & sequential circuits, ALU",
        "desc": "How binary noise immunity enables digital logic: Boolean algebra, adders, flip-flops, registers, and the ALU.",
        "ebook": "ebook/level-2-ebook.html",
        "illustrations": "illustrations/index.html#level-2"
    },
    {
        "id": "level-3-machine-architecture",
        "num": 3,
        "name": "Level 3",
        "title": "Machine Architecture",
        "category": "architecture",
        "theme": "Memory hierarchy, Fetch-Decode-Execute cycle, Toy ISA, Memory-mapped I/O, Bus",
        "desc": "The Von Neumann engine in motion: SRAM/DRAM caches, program counter, instruction decoding, and data buses.",
        "ebook": "ebook/level-3-ebook.html",
        "illustrations": "illustrations/index.html#level-3"
    },
    {
        "id": "level-4-software-foundations",
        "num": 4,
        "name": "Level 4",
        "title": "Software Foundations",
        "category": "architecture",
        "theme": "Machine code, assembly, stack frames, OS kernel, virtual memory & paging, file systems",
        "desc": "From bare metal to an operating system: x86-64 assembly, stack frames, supervisor mode, paging, and inodes.",
        "ebook": "ebook/level-4-ebook.html",
        "illustrations": "illustrations/index.html#level-4"
    },
    {
        "id": "level-5-programming",
        "num": 5,
        "name": "Level 5",
        "title": "Programming & Runtimes",
        "category": "software",
        "theme": "C close-to-metal, compilation, Python object model, recursion, memory & heaps, debugging",
        "desc": "Close to the metal vs interpreted languages: memory pointers, compilation pipelines, Python objects, and heap allocation.",
        "ebook": "ebook/level-5-ebook.html",
        "illustrations": "illustrations/index.html#level-5"
    },
    {
        "id": "level-6-dsa",
        "num": 6,
        "name": "Level 6",
        "title": "Data Structures & Algorithms",
        "category": "software",
        "theme": "Arrays, linked lists, stacks, queues, hash tables, trees, heaps, graphs, sorting, DP",
        "desc": "Mastering computational efficiency: cache-conscious structures, graph traversal, balanced trees, and dynamic programming.",
        "ebook": "ebook/level-6-ebook.html",
        "illustrations": "illustrations/index.html#level-6"
    },
    {
        "id": "level-7-systems",
        "num": 7,
        "name": "Level 7",
        "title": "Systems Programming",
        "category": "systems",
        "theme": "Processes, multithreading, mutexes & sync, sockets & IPC, tiny shell, HTTP server",
        "desc": "Concurrent and networked computing: POSIX threads, synchronization primitives, socket programming, and building a web server.",
        "ebook": "ebook/level-7-ebook.html",
        "illustrations": "illustrations/index.html#level-7"
    },
    {
        "id": "level-8-networks",
        "num": 8,
        "name": "Level 8",
        "title": "Networks & Protocols",
        "category": "systems",
        "theme": "Physical layer, Ethernet, IP routing, TCP streams, UDP, DNS resolution, TLS 1.3",
        "desc": "Connecting global computers: packet framing, subnet routing, reliable byte streams, DNS, and cryptographic handshakes.",
        "ebook": "ebook/level-8-ebook.html",
        "illustrations": "illustrations/index.html#level-8"
    },
    {
        "id": "level-9-databases",
        "num": 9,
        "name": "Level 9",
        "title": "Databases & Storage",
        "category": "data",
        "theme": "Relational model, B-Trees, transactions & ACID/WAL, building a toy SQL engine",
        "desc": "Persistent data at scale: relational algebra, disk B-Trees, transaction concurrency, write-ahead logs, and query parsers.",
        "ebook": "ebook/level-9-ebook.html",
        "illustrations": "illustrations/index.html#level-9"
    },
    {
        "id": "level-10-web",
        "num": 10,
        "name": "Level 10",
        "title": "Web & App Development",
        "category": "data",
        "theme": "HTML/CSS/JS DOM, browser rendering engine, REST APIs & async, fullstack app",
        "desc": "The modern application canvas: DOM layouts, render pipelines, asynchronous event loops, REST contracts, and fullstack architectures.",
        "ebook": "ebook/level-10-ebook.html",
        "illustrations": "illustrations/index.html#level-10"
    },
    {
        "id": "level-11-ai-ml",
        "num": 11,
        "name": "Level 11",
        "title": "AI & Machine Learning",
        "category": "aiml",
        "theme": "Search, linear algebra, regression & gradient descent, neural nets, backpropagation",
        "desc": "From symbolic rules to learning systems: multidimensional vectors, gradient optimization, loss landscapes, and backprop derivation.",
        "ebook": "ebook/level-11-ebook.html",
        "illustrations": "illustrations/index.html#level-11"
    },
    {
        "id": "level-12-advanced-ai",
        "num": 12,
        "name": "Level 12",
        "title": "Advanced AI & Frontiers",
        "category": "aiml",
        "theme": "Transformer architecture, vector embeddings, RAG, autonomous AI agents, AI safety & alignment",
        "desc": "The modern intelligence frontier: self-attention mechanisms, semantic embeddings, retrieval augmentation, agentic tool use, and safety.",
        "ebook": "ebook/level-12-ebook.html",
        "illustrations": "illustrations/index.html#level-12"
    }
]

# Canonical titles dictionary from MASTER_GUIDE to ensure 100% clean nomenclature
CANONICAL_MODULES = {
    "module-0-1-why-compute": ("0.1", "Why Did Humans Need to Compute?"),
    "module-0-2-mechanical": ("0.2", "Early Mechanical Computation"),
    "module-0-3-loom": ("0.3", "The Loom That Taught Computers"),
    "module-0-4-babbage-ada": ("0.4", "Babbage & Ada: The First Programmers"),
    "module-0-5-hollerith": ("0.5", "Hollerith & The Punch Card Era"),
    "module-1-1-electricity": ("1.1", "What is Electricity?"),
    "module-1-2-switches": ("1.2", "Switches: The Atom of Computing"),
    "module-1-3-relay-logic": ("1.3", "Relay Logic: Metal Decisions"),
    "module-1-4-vacuum-tubes": ("1.4", "Vacuum Tubes: Faster Switching"),
    "module-1-5-transistor": ("1.5", "The Transistor Revolution"),
    "module-1-6-moores-law": ("1.6", "From Transistors to Chips: Moore's Law"),
    "module-2-1-why-binary": ("2.1", "Why Binary? The Physics of Two States"),
    "module-2-2-number-systems": ("2.2", "Number Systems: Bin, Oct, Hex & Two's Complement"),
    "module-2-3-logic-gates": ("2.3", "Boolean Algebra & Logic Gates"),
    "module-2-4-combinational-circuits": ("2.4", "Combinational Circuits"),
    "module-2-5-sequential-circuits": ("2.5", "Sequential Circuits: Memory from Gates"),
    "module-2-6-simple-alu": ("2.6", "From Gates to a Simple ALU"),
    "module-3-1-memory": ("3.1", "Memory: How Machines Remember"),
    "module-3-2-fetch-decode-execute": ("3.2", "The Fetch-Decode-Execute Cycle"),
    "module-3-3-isa": ("3.3", "Instruction Set Architecture"),
    "module-3-4-io": ("3.4", "Input/Output: Connecting to the World"),
    "module-3-5-bus": ("3.5", "The Bus: Moving Data Around"),
    "module-4-1-machine-code": ("4.1", "Machine Code & Assembly"),
    "module-4-2-stack-calling": ("4.2", "The Stack & Calling Conventions"),
    "module-4-3-os-concepts": ("4.3", "Operating System Concepts"),
    "module-4-4-memory-management": ("4.4", "Memory Management & Paging"),
    "module-4-5-file-systems": ("4.5", "File Systems & Inodes"),
    "module-5-1-c-language": ("5.1", "C: Close to the Metal"),
    "module-5-2-python": ("5.2", "Python: High-Level Abstraction"),
    "module-5-3-algorithms-intro": ("5.3", "Compilation vs Interpretation"),
    "module-5-4-recursion": ("5.4", "Functions, Scope & Recursion"),
    "module-5-5-sorting": ("5.5", "Memory Allocation & Heap"),
    "module-5-6-searching": ("5.6", "Debugging & Profiling"),
    "module-6-1-arrays-linked-lists": ("6.1", "Arrays & Contiguous Memory"),
    "module-6-2-stacks-queues": ("6.2", "Linked Lists, Stacks & Queues"),
    "module-6-3-hash-tables": ("6.3", "Hash Tables & Collisions"),
    "module-6-4-trees": ("6.4", "Trees & Binary Search"),
    "module-6-5-heaps": ("6.5", "Priority Queues & Heaps"),
    "module-6-6-graphs": ("6.6", "Graphs & Pathfinding"),
    "module-6-7-sorting-advanced": ("6.7", "Advanced Sorting Algorithms"),
    "module-6-8-dynamic-programming": ("6.8", "Dynamic Programming"),
    "module-7-1-multithreading": ("7.1", "Processes & Multithreading"),
    "module-7-2-sync-primitives": ("7.2", "Concurrency, Locks & Mutexes"),
    "module-7-3-sockets": ("7.3", "Sockets & Network IPC"),
    "module-7-4-shell": ("7.4", "Building a Tiny Shell"),
    "module-7-5-http-server": ("7.5", "Building a Tiny HTTP Server"),
    "module-8-1-physical-datalink": ("8.1", "Physical & Data Link Layers"),
    "module-8-2-network-layer": ("8.2", "IP Addressing & Packet Routing"),
    "module-8-3-transport-layer": ("8.3", "TCP & Reliable Byte Streams"),
    "module-8-4-application-layer": ("8.4", "UDP & Real-Time Protocols"),
    "module-8-5-tls-ssl": ("8.5", "DNS & Name Resolution"),
    "module-8-6-packet-analyzer": ("8.6", "TLS/SSL & Cryptographic Channels"),
    "module-9-1-relational-model": ("9.1", "The Relational Model & SQL"),
    "module-9-2-btrees": ("9.2", "B-Trees & Storage Engines"),
    "module-9-3-transactions": ("9.3", "Transactions, ACID & WAL"),
    "module-9-4-toy-sql-engine": ("9.4", "Building a Toy SQL Database"),
    "module-10-1-html-css-js": ("10.1", "How Browsers Render Pages"),
    "module-10-2-how-browsers-render": ("10.2", "Modern CSS Layout & Flex/Grid"),
    "module-10-3-rest-apis": ("10.3", "JavaScript Event Loop & REST APIs"),
    "module-10-4-fullstack-project": ("10.4", "Building a Full-Stack Web App"),
    "module-11-1-search-intelligence": ("11.1", "Search & Symbolic Intelligence"),
    "module-11-2-linear-algebra-ml": ("11.2", "Linear Algebra for Machine Learning"),
    "module-11-3-regression-classification": ("11.3", "Gradient Descent & Optimizers"),
    "module-11-4-neural-networks": ("11.4", "Neural Networks from Scratch"),
    "module-11-5-backpropagation": ("11.5", "Backpropagation Derived"),
    "module-12-1-llm-architecture": ("12.1", "Transformer & LLM Architecture"),
    "module-12-2-embeddings": ("12.2", "Vector Embeddings & Semantic Search"),
    "module-12-3-rag": ("12.3", "Retrieval-Augmented Generation (RAG)"),
    "module-12-4-ai-agents": ("12.4", "Autonomous AI Agents"),
    "module-12-5-ethics-safety": ("12.5", "AI Alignment, Safety & Ethics"),
}

def extract_problem_statement(lpath, default_title):
    if os.path.exists(lpath):
        with open(lpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            pm = re.search(r"##\s+The Problem\s*\n+([^\n#]+)", content)
            if pm:
                text = pm.group(1).strip().lstrip("> ").strip()
                if len(text) > 15:
                    return text
    return f"First-principles exploration of computing mechanics, trade-offs, and systems in {default_title}."

def get_module_info(lvl_dir_name, mod_dir_name):
    if mod_dir_name in CANONICAL_MODULES:
        return CANONICAL_MODULES[mod_dir_name]
    m = re.match(r"module-(\d+)-(\d+)-(.*)", mod_dir_name)
    if m:
        num = f"{m.group(1)}.{m.group(2)}"
        clean_name = m.group(3).replace("-", " ").title()
        return num, clean_name
    return "", mod_dir_name

def parse_curriculum():
    levels = []
    flat_modules = []
    for meta in LEVELS_META:
        lvl_dir = BASE_DIR / "course" / meta["id"]
        mods = sorted([m for m in os.listdir(lvl_dir) if (lvl_dir / m).is_dir() and not m.startswith(".")])
        module_entries = []
        for m in mods:
            mpath = lvl_dir / m
            lpath = mpath / "lesson.md"
            cpath = mpath / "challenge.md"
            spath = mpath / "simulation.html"
            
            num_str, name_str = get_module_info(meta["id"], m)
            problem = extract_problem_statement(lpath, name_str)
            
            entry = {
                "level_id": meta["id"],
                "level_num": meta["num"],
                "level_title": meta["title"],
                "level_name": meta["name"],
                "dir": m,
                "num": num_str,
                "name": name_str,
                "problem": problem,
                "lesson_md": f"course/{meta['id']}/{m}/lesson.md",
                "lesson_html": f"course/{meta['id']}/{m}/lesson.html",
                "challenge_md": f"course/{meta['id']}/{m}/challenge.md" if cpath.exists() else None,
                "challenge_html": f"course/{meta['id']}/{m}/challenge.html" if cpath.exists() else None,
                "simulation_html": f"course/{meta['id']}/{m}/simulation.html" if spath.exists() else None,
                "ebook_html": meta["ebook"],
            }
            module_entries.append(entry)
            flat_modules.append(entry)
            
        meta_copy = dict(meta)
        meta_copy["modules"] = module_entries
        levels.append(meta_copy)
    return levels, flat_modules

COMMON_CSS = """
:root {
  --paper:        #F5F4EF;
  --paper-warm:   #EEECE4;
  --washi:        #FFFFFF;
  --bone:         #E8E5DC;
  --ghost:        #D4D0C4;
  --border-hair:  #1C1C1C;
  --border-light: #D8D6CE;
  --border-paper: #E8E6DF;
  --ink:          #1C1C1C;
  --text-body:    #2E2E2E;
  --slate:        #4A5568;
  --muted:        #787670;
  --indigo:       #1C2D42;
  --indigo-deep:  #0F1E2E;
  --lacquer:      #C82A2A;
  --gold:         #8B6914;
  --sage:         #3D5B3F;
  --card-bg:      #FFFFFF;
  --code-bg:      #EBE8DF;
  --callout-bg:   #FAF8F5;
  
  --font-display: 'Noto Serif JP', Georgia, serif;
  --font-body:    'EB Garamond', Georgia, serif;
  --font-sans:    'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
  
  --shadow-sm:    0 1px 3px rgba(0,0,0,0.06);
  --shadow-md:    0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg:    0 12px 28px rgba(0,0,0,0.12);
  --radius-xs:    2px;
  --radius-sm:    4px;
  --radius-md:    8px;
}

[data-theme="dark"] {
  --paper:        #141619;
  --paper-warm:   #1A1D21;
  --washi:        #1E2227;
  --bone:         #2B3038;
  --ghost:        #3B424D;
  --border-hair:  #4A5260;
  --border-light: #2D333D;
  --border-paper: #22272E;
  --ink:          #E6EDF3;
  --text-body:    #C9D1D9;
  --slate:        #8B949E;
  --muted:        #8B949E;
  --indigo:       #58A6FF;
  --indigo-deep:  #161B22;
  --lacquer:      #FF7B72;
  --gold:         #D29922;
  --sage:         #7EE787;
  --card-bg:      #1C2128;
  --code-bg:      #21262D;
  --callout-bg:   #1F242C;
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  scroll-behavior: smooth;
  -webkit-text-size-adjust: 100%;
}

body {
  background: var(--paper);
  color: var(--text-body);
  font-family: var(--font-body);
  font-size: 1.125rem;
  line-height: 1.75;
  -webkit-font-smoothing: antialiased;
  min-height: 100vh;
}

a {
  color: var(--indigo);
  text-decoration: none;
  transition: color 0.15s ease, border-color 0.15s ease;
}

a:hover {
  text-decoration: underline;
}

code, kbd, samp, pre {
  font-family: var(--font-mono);
  font-size: 0.9em;
}

pre {
  background: var(--code-bg);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-sm);
  padding: 1rem 1.25rem;
  overflow-x: auto;
  margin: 1.5rem 0;
  line-height: 1.5;
}

code:not(pre code) {
  background: var(--code-bg);
  border: 1px solid var(--border-light);
  padding: 0.15em 0.4em;
  border-radius: 3px;
  font-size: 0.88em;
  color: var(--ink);
}

/* Zen Progress Bar */
#zen-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--lacquer);
  width: 0%;
  z-index: 999;
  transition: width 0.1s linear;
}

/* Header & Top Bar */
.zen-topbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--paper);
  border-bottom: 1px solid var(--border-light);
  backdrop-filter: blur(8px);
  padding: 0.6rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.zen-topbar-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 0;
}

.zen-topbar-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.btn-icon {
  background: var(--washi);
  border: 1px solid var(--border-light);
  color: var(--ink);
  padding: 0.4rem 0.75rem;
  border-radius: var(--radius-sm);
  font-family: var(--font-sans);
  font-size: 0.85rem;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
}

.btn-icon:hover {
  background: var(--paper-warm);
  border-color: var(--border-hair);
  text-decoration: none;
}

.btn-primary {
  background: var(--indigo);
  color: #FFFFFF !important;
  border-color: var(--indigo);
}

.btn-primary:hover {
  background: var(--indigo-deep);
  color: #FFFFFF !important;
}

.btn-accent {
  background: var(--lacquer);
  color: #FFFFFF !important;
  border-color: var(--lacquer);
}

.btn-accent:hover {
  filter: brightness(0.9);
  color: #FFFFFF !important;
}
"""

def generate_lesson_html(module_entry, prev_mod, next_mod):
    lpath = BASE_DIR / module_entry["lesson_md"]
    if not lpath.exists():
        return
    with open(lpath, "r", encoding="utf-8", errors="ignore") as f:
        md_text = f.read()

    rendered_body = md_parser.render(md_text)

    # Relative paths from course/level-X/module-Y/ to root
    root_rel = "../../../"
    ebook_rel = f"{root_rel}{module_entry['ebook_html']}"
    sim_link = f"./simulation.html" if module_entry["simulation_html"] else ""
    chal_link = f"./challenge.html" if module_entry["challenge_html"] else ""
    md_link = f"./lesson.md"

    prev_button = ""
    if prev_mod:
        if prev_mod["level_id"] == module_entry["level_id"]:
            p_rel = f"../{prev_mod['dir']}/lesson.html"
        else:
            p_rel = f"../../{prev_mod['level_id']}/{prev_mod['dir']}/lesson.html"
        prev_button = f'<a href="{p_rel}" class="btn-icon">← Prev: M {prev_mod["num"]}</a>'

    next_button = ""
    if next_mod:
        if next_mod["level_id"] == module_entry["level_id"]:
            n_rel = f"../{next_mod['dir']}/lesson.html"
        else:
            n_rel = f"../../{next_mod['level_id']}/{next_mod['dir']}/lesson.html"
        next_button = f'<a href="{n_rel}" class="btn-icon btn-primary">Next: M {next_mod["num"]} →</a>'

    sim_button = ""
    if sim_link:
        sim_button = f'<a href="{sim_link}" class="btn-icon btn-accent" title="Open Interactive Sandbox">⚡ Launch Lab</a>'

    chal_button = ""
    if chal_link:
        chal_button = f'<a href="{chal_link}" class="btn-icon" title="View Challenge Rubric">🎯 Challenge</a>'

    doc_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="zen">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>Module {module_entry['num']} — {html.escape(module_entry['name'])} | AoPS</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300;400;600&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-light.min.css" id="hljs-theme">
  <style>
    {COMMON_CSS}

    .article-wrap {{
      max-width: 760px;
      margin: 0 auto;
      padding: 2rem 1.25rem 6rem;
    }}

    .article-header {{
      margin-bottom: 2.5rem;
      border-bottom: 1px solid var(--border-light);
      padding-bottom: 1.5rem;
    }}

    .article-level-tag {{
      display: inline-block;
      font-family: var(--font-sans);
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--indigo);
      background: var(--paper-warm);
      border: 1px solid var(--border-light);
      padding: 0.2rem 0.6rem;
      border-radius: var(--radius-xs);
      margin-bottom: 0.75rem;
    }}

    .article-title {{
      font-family: var(--font-display);
      font-size: 2.1rem;
      line-height: 1.25;
      color: var(--ink);
      font-weight: 400;
      letter-spacing: -0.01em;
      margin-bottom: 0.75rem;
    }}

    .article-meta-row {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.75rem;
      font-family: var(--font-sans);
      font-size: 0.85rem;
      color: var(--muted);
    }}

    /* Markdown styling */
    .prose h1, .prose h2, .prose h3, .prose h4 {{
      font-family: var(--font-display);
      color: var(--ink);
      font-weight: 400;
      margin-top: 2.25rem;
      margin-bottom: 0.75rem;
      line-height: 1.3;
    }}

    .prose h2 {{
      font-size: 1.55rem;
      border-bottom: 1px solid var(--border-light);
      padding-bottom: 0.35rem;
    }}

    .prose h3 {{
      font-size: 1.25rem;
    }}

    .prose p {{
      margin: 1.1rem 0;
      font-size: 1.125rem;
      line-height: 1.8;
      color: var(--text-body);
    }}

    .prose blockquote {{
      border-left: 3px solid var(--lacquer);
      background: var(--callout-bg);
      padding: 1rem 1.25rem;
      margin: 1.5rem 0;
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      font-style: italic;
      color: var(--ink);
    }}

    .prose blockquote p {{
      margin: 0.4rem 0;
      font-size: 1.05rem;
    }}

    .prose ul, .prose ol {{
      margin: 1rem 0 1rem 1.5rem;
      padding-left: 0.5rem;
    }}

    .prose li {{
      margin: 0.4rem 0;
    }}

    .prose table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
      font-family: var(--font-sans);
      font-size: 0.95rem;
    }}

    .prose th, .prose td {{
      border: 1px solid var(--border-light);
      padding: 0.6rem 0.8rem;
      text-align: left;
    }}

    .prose th {{
      background: var(--paper-warm);
      color: var(--ink);
      font-weight: 600;
    }}

    .prose hr {{
      border: none;
      border-top: 1px solid var(--border-light);
      margin: 2.5rem 0;
    }}

    .zen-footer-nav {{
      margin-top: 4rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border-light);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
    }}

    @media (max-width: 600px) {{
      .article-title {{
        font-size: 1.65rem;
      }}
      .zen-topbar-left span.full-title {{
        display: none;
      }}
    }}
  </style>
</head>
<body>
  <div id="zen-progress"></div>

  <!-- Sticky Top Navigation -->
  <header class="zen-topbar">
    <div class="zen-topbar-left">
      <a href="{root_rel}index.html" class="btn-icon" title="Return to Course Index">← Hub</a>
      <span style="font-family:var(--font-sans); font-size:0.85rem; font-weight:600; color:var(--ink);">
        M {module_entry['num']}
      </span>
      <span class="full-title" style="font-family:var(--font-sans); font-size:0.85rem; color:var(--muted); max-width:260px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
        {html.escape(module_entry['name'])}
      </span>
    </div>
    <div class="zen-topbar-right">
      {sim_button}
      {chal_button}
      <button id="theme-btn" class="btn-icon" title="Toggle Dark/Light Mode">🌓</button>
    </div>
  </header>

  <!-- Article Container -->
  <main class="article-wrap">
    <div class="article-header">
      <div class="article-level-tag">{html.escape(module_entry['level_name'])} • {html.escape(module_entry['level_title'])}</div>
      <h1 class="article-title">Module {module_entry['num']} — {html.escape(module_entry['name'])}</h1>
      <div class="article-meta-row">
        <span>📖 Technical Lesson</span>
        <span>•</span>
        <a href="{md_link}" target="_blank" style="color:var(--muted);">Raw Markdown</a>
        <span>•</span>
        <a href="{ebook_rel}" style="color:var(--indigo);">Full Volume eBook</a>
      </div>
    </div>

    <!-- Rendered Markdown Body -->
    <article class="prose">
      {rendered_body}
    </article>

    <!-- Bottom Navigation -->
    <nav class="zen-footer-nav">
      <div>
        {prev_button}
      </div>
      <div style="display:flex; gap:0.5rem;">
        <a href="{root_rel}index.html" class="btn-icon">Course Index</a>
        {next_button}
      </div>
    </nav>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script>
    // Syntax highlighting
    if (typeof hljs !== 'undefined') hljs.highlightAll();

    // Math auto-render
    if (typeof renderMathInElement !== 'undefined') {{
      renderMathInElement(document.body, {{
        delimiters: [
          {{left: '$$', right: '$$', display: true}},
          {{left: '$', right: '$', display: false}},
          {{left: '\\\\(', right: '\\\\)', display: false}},
          {{left: '\\\\[', right: '\\\\]', display: true}}
        ],
        throwOnError: false
      }});
    }}

    // Theme toggle
    const themeBtn = document.getElementById('theme-btn');
    const currentTheme = localStorage.getItem('aops_theme') || 'zen';
    document.documentElement.setAttribute('data-theme', currentTheme);
    const hljsTheme = document.getElementById('hljs-theme');
    if (hljsTheme) {{
      hljsTheme.href = currentTheme === 'dark' 
        ? 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css'
        : 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-light.min.css';
    }}

    themeBtn.addEventListener('click', () => {{
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const nextTheme = isDark ? 'zen' : 'dark';
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem('aops_theme', nextTheme);
      if (hljsTheme) {{
        hljsTheme.href = nextTheme === 'dark'
          ? 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css'
          : 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-light.min.css';
      }}
    }});

    // Reading progress bar
    window.addEventListener('scroll', () => {{
      const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
      document.getElementById('zen-progress').style.width = scrolled + '%';
    }});
  </script>
</body>
</html>
"""
    dest_path = BASE_DIR / module_entry["lesson_html"]
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(doc_html)

def generate_challenge_html(module_entry):
    if not module_entry["challenge_md"]:
        return
    cpath = BASE_DIR / module_entry["challenge_md"]
    if not cpath.exists():
        return
    with open(cpath, "r", encoding="utf-8", errors="ignore") as f:
        md_text = f.read()

    rendered_body = md_parser.render(md_text)

    root_rel = "../../../"
    lesson_link = "./lesson.html"
    sim_link = f"./simulation.html" if module_entry["simulation_html"] else ""

    sim_button = ""
    if sim_link:
        sim_button = f'<a href="{sim_link}" class="btn-icon btn-accent" title="Open Interactive Sandbox">⚡ Launch Lab</a>'

    doc_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="zen">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>Challenge {module_entry['num']} — {html.escape(module_entry['name'])} | AoPS</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300;400;600&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-light.min.css" id="hljs-theme">
  <style>
    {COMMON_CSS}

    .article-wrap {{
      max-width: 760px;
      margin: 0 auto;
      padding: 2rem 1.25rem 6rem;
    }}

    .article-header {{
      margin-bottom: 2.5rem;
      border-bottom: 1px solid var(--border-light);
      padding-bottom: 1.5rem;
    }}

    .article-level-tag {{
      display: inline-block;
      font-family: var(--font-sans);
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--lacquer);
      background: var(--paper-warm);
      border: 1px solid var(--border-light);
      padding: 0.2rem 0.6rem;
      border-radius: var(--radius-xs);
      margin-bottom: 0.75rem;
    }}

    .article-title {{
      font-family: var(--font-display);
      font-size: 2rem;
      line-height: 1.25;
      color: var(--ink);
      font-weight: 400;
      margin-bottom: 0.75rem;
    }}

    /* Markdown styling */
    .prose h1, .prose h2, .prose h3, .prose h4 {{
      font-family: var(--font-display);
      color: var(--ink);
      font-weight: 400;
      margin-top: 2rem;
      margin-bottom: 0.75rem;
    }}

    .prose h2 {{
      font-size: 1.45rem;
      border-bottom: 1px solid var(--border-light);
      padding-bottom: 0.35rem;
    }}

    .prose p {{
      margin: 1.1rem 0;
      font-size: 1.1rem;
      line-height: 1.8;
      color: var(--text-body);
    }}

    .prose table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
      font-family: var(--font-sans);
      font-size: 0.95rem;
    }}

    .prose th, .prose td {{
      border: 1px solid var(--border-light);
      padding: 0.6rem 0.8rem;
      text-align: left;
    }}

    .prose th {{
      background: var(--paper-warm);
      color: var(--ink);
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <header class="zen-topbar">
    <div class="zen-topbar-left">
      <a href="{lesson_link}" class="btn-icon">← Lesson</a>
      <a href="{root_rel}index.html" class="btn-icon">Hub</a>
      <span style="font-family:var(--font-sans); font-size:0.85rem; font-weight:600; color:var(--ink);">
        Challenge {module_entry['num']}
      </span>
    </div>
    <div class="zen-topbar-right">
      {sim_button}
      <button id="theme-btn" class="btn-icon" title="Toggle Theme">🌓</button>
    </div>
  </header>

  <main class="article-wrap">
    <div class="article-header">
      <div class="article-level-tag">🎯 Challenge & Graded Rubric</div>
      <h1 class="article-title">Module {module_entry['num']} Challenge</h1>
      <p style="font-family:var(--font-sans); font-size:0.95rem; color:var(--muted);">
        Hands-on verification problem for {html.escape(module_entry['name'])}.
      </p>
    </div>

    <article class="prose">
      {rendered_body}
    </article>

    <div style="margin-top:3rem; padding-top:1.5rem; border-top:1px solid var(--border-light); display:flex; gap:0.75rem;">
      <a href="{lesson_link}" class="btn-icon btn-primary">← Back to Lesson</a>
      {sim_button}
      <a href="{root_rel}index.html" class="btn-icon">Course Index</a>
    </div>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script>
    if (typeof hljs !== 'undefined') hljs.highlightAll();
    if (typeof renderMathInElement !== 'undefined') {{
      renderMathInElement(document.body, {{
        delimiters: [
          {{left: '$$', right: '$$', display: true}},
          {{left: '$', right: '$', display: false}},
          {{left: '\\\\(', right: '\\\\)', display: false}},
          {{left: '\\\\[', right: '\\\\]', display: true}}
        ],
        throwOnError: false
      }});
    }}

    const themeBtn = document.getElementById('theme-btn');
    const currentTheme = localStorage.getItem('aops_theme') || 'zen';
    document.documentElement.setAttribute('data-theme', currentTheme);
    const hljsTheme = document.getElementById('hljs-theme');
    if (hljsTheme) {{
      hljsTheme.href = currentTheme === 'dark' 
        ? 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css'
        : 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-light.min.css';
    }}

    themeBtn.addEventListener('click', () => {{
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const nextTheme = isDark ? 'zen' : 'dark';
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem('aops_theme', nextTheme);
      if (hljsTheme) {{
        hljsTheme.href = nextTheme === 'dark'
          ? 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css'
          : 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-light.min.css';
      }}
    }});
  </script>
</body>
</html>
"""
    dest_path = BASE_DIR / module_entry["challenge_html"]
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(doc_html)

def generate_dynamic_reader():
    """Generates reader.html capable of rendering any markdown file passed via ?src="""
    doc_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="zen">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>AoPS Universal Markdown Reader</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300;400;600&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <!-- Marked.js for fast client-side markdown rendering -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    {COMMON_CSS}

    .article-wrap {{
      max-width: 760px;
      margin: 0 auto;
      padding: 2rem 1.25rem 6rem;
    }}

    .prose h1, .prose h2, .prose h3 {{
      font-family: var(--font-display);
      color: var(--ink);
      font-weight: 400;
      margin-top: 2.25rem;
      margin-bottom: 0.75rem;
    }}

    .prose p {{
      margin: 1.1rem 0;
      font-size: 1.125rem;
      line-height: 1.8;
      color: var(--text-body);
    }}

    .prose blockquote {{
      border-left: 3px solid var(--lacquer);
      background: var(--callout-bg);
      padding: 1rem 1.25rem;
      margin: 1.5rem 0;
      font-style: italic;
    }}

    .prose table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
    }}

    .prose th, .prose td {{
      border: 1px solid var(--border-light);
      padding: 0.6rem 0.8rem;
    }}

    .prose th {{
      background: var(--paper-warm);
    }}

    #status-msg {{
      font-family: var(--font-sans);
      font-size: 0.95rem;
      padding: 2rem;
      text-align: center;
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <div id="zen-progress"></div>

  <header class="zen-topbar">
    <div class="zen-topbar-left">
      <a href="index.html" class="btn-icon">← Hub</a>
      <span id="doc-title" style="font-family:var(--font-sans); font-size:0.85rem; font-weight:600; color:var(--ink);">
        AoPS Reader
      </span>
    </div>
    <div class="zen-topbar-right">
      <a id="sim-btn" href="#" class="btn-icon btn-accent" style="display:none;">⚡ Lab</a>
      <a id="raw-btn" href="#" class="btn-icon" target="_blank" style="display:none;">📄 Source</a>
      <button id="theme-btn" class="btn-icon">🌓</button>
    </div>
  </header>

  <main class="article-wrap">
    <div id="status-msg">Loading document...</div>
    <article id="content" class="prose"></article>
  </main>

  <script>
    // Theme toggle
    const themeBtn = document.getElementById('theme-btn');
    const currentTheme = localStorage.getItem('aops_theme') || 'zen';
    document.documentElement.setAttribute('data-theme', currentTheme);
    themeBtn.addEventListener('click', () => {{
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const nextTheme = isDark ? 'zen' : 'dark';
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem('aops_theme', nextTheme);
    }});

    // Reading progress
    window.addEventListener('scroll', () => {{
      const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
      document.getElementById('zen-progress').style.width = scrolled + '%';
    }});

    // Fetch and render markdown from query string ?src=path/to/file.md
    const params = new URLSearchParams(window.location.search);
    const src = params.get('src') || 'README.md';

    const statusEl = document.getElementById('status-msg');
    const contentEl = document.getElementById('content');
    const docTitle = document.getElementById('doc-title');
    const rawBtn = document.getElementById('raw-btn');
    const simBtn = document.getElementById('sim-btn');

    rawBtn.href = src;
    rawBtn.style.display = 'inline-flex';

    // If it's a course lesson, check for simulation.html in the same folder
    if (src.includes('course/') && src.endsWith('lesson.md')) {{
      const simUrl = src.replace('lesson.md', 'simulation.html');
      simBtn.href = simUrl;
      simBtn.style.display = 'inline-flex';
    }}

    docTitle.textContent = src.split('/').pop();

    fetch(src)
      .then(res => {{
        if (!res.ok) throw new Error('HTTP ' + res.status + ' ' + res.statusText);
        return res.text();
      }})
      .then(markdown => {{
        statusEl.style.display = 'none';
        contentEl.innerHTML = marked.parse(markdown);
        // Try to update title from first h1
        const h1 = contentEl.querySelector('h1');
        if (h1) {{
          document.title = h1.textContent + ' | AoPS';
          docTitle.textContent = h1.textContent;
        }}
      }})
      .catch(err => {{
        statusEl.innerHTML = '<p style="color:var(--lacquer); font-weight:600;">Failed to load ' + src + '</p><p>' + err.message + '</p><p><a href="index.html" class="btn-icon" style="margin-top:1rem;">← Return to Index</a></p>';
      }});
  </script>
</body>
</html>
"""
    with open(BASE_DIR / "reader.html", "w", encoding="utf-8") as f:
        f.write(doc_html)

def generate_index_html(levels, flat_modules):
    """Generates the master index.html portal."""
    
    # Pre-render level navigation chips
    chips_html = []
    for lvl in levels:
        chips_html.append(f'<a href="#{lvl["id"]}" class="zen-chip">L{lvl["num"]}</a>')
    chips_bar = "\n".join(chips_html)

    # Pre-render level sections
    sections_html = []
    for lvl in levels:
        mod_cards = []
        for m in lvl["modules"]:
            sim_btn = f'<a href="{m["simulation_html"]}" class="btn-icon btn-accent" title="Interactive Simulation Sandbox">⚡ Lab</a>' if m["simulation_html"] else ""
            chal_btn = f'<a href="{m["challenge_html"]}" class="btn-icon" title="Challenge Rubric">🎯 Challenge</a>' if m["challenge_html"] else ""
            lesson_btn = f'<a href="{m["lesson_html"]}" class="btn-icon btn-primary" title="Read Standalone Lesson">📖 Lesson</a>'
            raw_btn = f'<a href="{m["lesson_md"]}" class="btn-icon" title="Raw Markdown Source">📄 .md</a>'
            
            card = f"""
            <article class="zen-card" data-category="{lvl['category']}" data-keywords="{m['num']} {html.escape(m['name']).lower()} {html.escape(lvl['title']).lower()}">
              <div class="zen-card-top">
                <span class="zen-badge-num">M {m['num']}</span>
                <span class="zen-badge-status">Interactive</span>
              </div>
              <h3 class="zen-card-title">
                <a href="{m['lesson_html']}">{html.escape(m['name'])}</a>
              </h3>
              <p class="zen-card-problem">{html.escape(m['problem'])}</p>
              <div class="zen-card-actions">
                {lesson_btn}
                {sim_btn}
                {chal_btn}
                {raw_btn}
              </div>
            </article>
            """
            mod_cards.append(card)

        grid_html = "\n".join(mod_cards)

        sec = f"""
        <section id="{lvl['id']}" class="zen-level-section">
          <div class="zen-level-header">
            <div class="zen-level-header-left">
              <span class="zen-level-pill">Level {lvl['num']}</span>
              <h2 class="zen-level-title">{html.escape(lvl['title'])}</h2>
              <p class="zen-level-desc">{html.escape(lvl['desc'])}</p>
            </div>
            <div class="zen-level-header-right">
              <a href="{lvl['ebook']}" class="btn-icon" title="Read Complete Volume eBook">📚 Volume {lvl['num']} Book</a>
              <span class="zen-level-count">{len(lvl['modules'])} Modules</span>
            </div>
          </div>
          <div class="zen-cards-grid">
            {grid_html}
          </div>
        </section>
        """
        sections_html.append(sec)

    all_sections = "\n".join(sections_html)

    doc_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="zen">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>AoPS — Art of Problem Solving | Master Course Hub</title>
  <meta name="description" content="Rebuilding Computer Science from First Principles across 13 Levels, 70 Modules, and 70 Interactive Labs.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300;400;600&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    {COMMON_CSS}

    /* Portal Layout */
    .zen-container {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 0 1.25rem 5rem;
    }}

    /* Hero Banner */
    .zen-hero {{
      padding: 3.5rem 0 2.5rem;
      border-bottom: 1px solid var(--border-light);
      margin-bottom: 2rem;
    }}

    .zen-brand {{
      display: inline-flex;
      align-items: center;
      gap: 0.6rem;
      font-family: var(--font-sans);
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--indigo);
      margin-bottom: 0.75rem;
    }}

    .zen-stamp {{
      background: var(--lacquer);
      color: #FFFFFF;
      width: 26px;
      height: 26px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 2px;
      font-family: var(--font-display);
      font-size: 0.85rem;
      line-height: 1;
    }}

    .zen-hero-title {{
      font-family: var(--font-display);
      font-size: clamp(2rem, 5vw, 3.25rem);
      line-height: 1.15;
      font-weight: 400;
      color: var(--ink);
      letter-spacing: -0.02em;
      margin-bottom: 1rem;
    }}

    .zen-hero-subtitle {{
      font-size: clamp(1.1rem, 2.5vw, 1.35rem);
      color: var(--muted);
      max-width: 780px;
      line-height: 1.6;
      margin-bottom: 1.75rem;
    }}

    .zen-stats-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 1.5rem;
      padding: 1.25rem 1.5rem;
      background: var(--card-bg);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-sm);
      margin-bottom: 2rem;
    }}

    .zen-stat-item {{
      display: flex;
      flex-direction: column;
    }}

    .zen-stat-val {{
      font-family: var(--font-mono);
      font-size: 1.5rem;
      font-weight: 600;
      color: var(--ink);
      line-height: 1.2;
    }}

    .zen-stat-lbl {{
      font-family: var(--font-sans);
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--muted);
    }}

    /* Filter & Search Bar */
    .zen-controls-wrap {{
      position: sticky;
      top: 50px;
      z-index: 90;
      background: var(--paper);
      padding: 0.75rem 0;
      border-bottom: 1px solid var(--border-light);
      margin-bottom: 2rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }}

    .zen-search-row {{
      display: flex;
      gap: 0.75rem;
      align-items: center;
    }}

    .zen-search-input {{
      flex: 1;
      padding: 0.65rem 1rem;
      font-family: var(--font-sans);
      font-size: 0.95rem;
      background: var(--card-bg);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-sm);
      color: var(--ink);
      outline: none;
      transition: border-color 0.15s ease;
    }}

    .zen-search-input:focus {{
      border-color: var(--indigo);
    }}

    .zen-chips-scroller {{
      display: flex;
      gap: 0.4rem;
      overflow-x: auto;
      padding-bottom: 0.25rem;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
    }}

    .zen-chips-scroller::-webkit-scrollbar {{
      display: none;
    }}

    .zen-chip {{
      font-family: var(--font-sans);
      font-size: 0.8rem;
      font-weight: 600;
      padding: 0.35rem 0.75rem;
      background: var(--card-bg);
      border: 1px solid var(--border-light);
      border-radius: 999px;
      color: var(--ink);
      white-space: nowrap;
      transition: all 0.15s ease;
    }}

    .zen-chip:hover, .zen-chip.active {{
      background: var(--indigo);
      color: #FFFFFF;
      border-color: var(--indigo);
      text-decoration: none;
    }}

    /* Level Section */
    .zen-level-section {{
      margin-bottom: 3.5rem;
      scroll-margin-top: 130px;
    }}

    .zen-level-header {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-end;
      gap: 1rem;
      padding-bottom: 1rem;
      border-bottom: 2px solid var(--border-hair);
      margin-bottom: 1.5rem;
    }}

    .zen-level-pill {{
      display: inline-block;
      font-family: var(--font-sans);
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--lacquer);
      margin-bottom: 0.25rem;
    }}

    .zen-level-title {{
      font-family: var(--font-display);
      font-size: 1.85rem;
      color: var(--ink);
      font-weight: 400;
      line-height: 1.2;
    }}

    .zen-level-desc {{
      font-family: var(--font-body);
      font-size: 1.05rem;
      color: var(--muted);
      max-width: 650px;
      margin-top: 0.35rem;
    }}

    .zen-level-header-right {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}

    .zen-level-count {{
      font-family: var(--font-mono);
      font-size: 0.85rem;
      color: var(--muted);
    }}

    /* Bento Cards Grid */
    .zen-cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.25rem;
    }}

    .zen-card {{
      background: var(--card-bg);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-sm);
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
    }}

    .zen-card:hover {{
      transform: translateY(-2px);
      border-color: var(--border-hair);
      box-shadow: var(--shadow-md);
    }}

    .zen-card-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }}

    .zen-badge-num {{
      font-family: var(--font-mono);
      font-size: 0.8rem;
      font-weight: 600;
      background: var(--paper-warm);
      border: 1px solid var(--border-light);
      color: var(--ink);
      padding: 0.15rem 0.5rem;
      border-radius: var(--radius-xs);
    }}

    .zen-badge-status {{
      font-family: var(--font-sans);
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--sage);
      font-weight: 600;
    }}

    .zen-card-title {{
      font-family: var(--font-display);
      font-size: 1.25rem;
      font-weight: 400;
      line-height: 1.35;
      margin-bottom: 0.65rem;
      color: var(--ink);
    }}

    .zen-card-title a {{
      color: inherit;
    }}

    .zen-card-problem {{
      font-family: var(--font-body);
      font-size: 0.95rem;
      line-height: 1.55;
      color: var(--slate);
      flex: 1;
      margin-bottom: 1.25rem;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    .zen-card-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
      border-top: 1px solid var(--border-light);
      padding-top: 0.85rem;
    }}

    /* Mobile Quick Nav */
    @media (max-width: 600px) {{
      .zen-cards-grid {{
        grid-template-columns: 1fr;
      }}
      .zen-hero {{
        padding: 2rem 0 1.5rem;
      }}
      .zen-stats-bar {{
        gap: 1rem;
        padding: 1rem;
      }}
      .zen-level-header {{
        flex-direction: column;
        align-items: flex-start;
      }}
    }}
  </style>
</head>
<body>
  <!-- Global Top Bar -->
  <header class="zen-topbar">
    <div class="zen-topbar-left">
      <span class="zen-stamp">解</span>
      <span style="font-family:var(--font-sans); font-size:0.9rem; font-weight:700; color:var(--ink); letter-spacing:0.04em;">
        AoPS
      </span>
      <span style="font-family:var(--font-sans); font-size:0.8rem; color:var(--muted); display:inline-block;">
        Art of Problem Solving
      </span>
    </div>
    <div class="zen-topbar-right">
      <a href="illustrations/index.html" class="btn-icon" title="Illustration Gallery">🎨 Gallery</a>
      <a href="AoPS_Review_Edition_v1.pdf" class="btn-icon" target="_blank" title="Download Complete 800-Page PDF">📄 PDF</a>
      <a href="https://github.com/ShorrohS/AoPS" class="btn-icon" target="_blank" rel="noopener">🐙 GitHub</a>
      <button id="theme-btn" class="btn-icon" title="Toggle Theme">🌓</button>
    </div>
  </header>

  <div class="zen-container">
    <!-- Hero Section -->
    <section class="zen-hero">
      <div class="zen-brand">
        <span class="zen-stamp">解</span>
        <span>First-Principles Computer Science Architecture</span>
      </div>
      <h1 class="zen-hero-title">
        We don't teach computing.<br>
        We rebuild it from scratch.
      </h1>
      <p class="zen-hero-subtitle">
        From ancient counting and mechanical punch cards, through relays, transistors, operating systems, and network protocols, all the way to neural networks and autonomous AI agents.
      </p>

      <!-- Stats Bar -->
      <div class="zen-stats-bar">
        <div class="zen-stat-item">
          <span class="zen-stat-val">13</span>
          <span class="zen-stat-lbl">Levels</span>
        </div>
        <div class="zen-stat-item">
          <span class="zen-stat-val">70</span>
          <span class="zen-stat-lbl">Lessons</span>
        </div>
        <div class="zen-stat-item">
          <span class="zen-stat-val">70</span>
          <span class="zen-stat-lbl">Web Labs</span>
        </div>
        <div class="zen-stat-item">
          <span class="zen-stat-val">70</span>
          <span class="zen-stat-lbl">Challenges</span>
        </div>
        <div class="zen-stat-item">
          <span class="zen-stat-val">240+</span>
          <span class="zen-stat-lbl">Vector SVGs</span>
        </div>
      </div>
    </section>

    <!-- Search & Sticky Level Scroller -->
    <div class="zen-controls-wrap">
      <div class="zen-search-row">
        <input type="search" id="module-search" class="zen-search-input" placeholder="🔍 Search 70 modules (e.g. b-tree, transistor, backprop, assembly, mutex, tcp)...">
        <span id="search-counter" style="font-family:var(--font-mono); font-size:0.8rem; color:var(--muted); white-space:nowrap;">70 / 70</span>
      </div>
      <div class="zen-chips-scroller">
        <a href="#all" class="zen-chip active" data-filter="all">All Levels</a>
        {chips_bar}
      </div>
    </div>

    <!-- Levels and Modules Content -->
    <main id="levels-container">
      {all_sections}
    </main>

    <!-- Footer -->
    <footer style="margin-top:6rem; padding-top:2rem; border-top:1px solid var(--border-light); font-family:var(--font-sans); font-size:0.85rem; color:var(--muted); text-align:center;">
      <p style="margin-bottom:0.5rem; font-weight:600; color:var(--ink);">AoPS — The Art of Problem Solving in Computer Science</p>
      <p>Published on GitHub Pages • Mobile Optimized • Zero Dependencies</p>
    </footer>
  </div>

  <script>
    // Theme toggle
    const themeBtn = document.getElementById('theme-btn');
    const currentTheme = localStorage.getItem('aops_theme') || 'zen';
    document.documentElement.setAttribute('data-theme', currentTheme);
    themeBtn.addEventListener('click', () => {{
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const nextTheme = isDark ? 'zen' : 'dark';
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem('aops_theme', nextTheme);
    }});

    // Live search filter
    const searchInput = document.getElementById('module-search');
    const cards = document.querySelectorAll('.zen-card');
    const counter = document.getElementById('search-counter');
    const sections = document.querySelectorAll('.zen-level-section');

    searchInput.addEventListener('input', (e) => {{
      const q = e.target.value.trim().toLowerCase();
      let visibleCount = 0;

      cards.forEach(card => {{
        const kw = card.getAttribute('data-keywords') || '';
        const problem = card.querySelector('.zen-card-problem').textContent.toLowerCase();
        const match = !q || kw.includes(q) || problem.includes(q);
        card.style.display = match ? 'flex' : 'none';
        if (match) visibleCount++;
      }});

      // Hide empty sections during search
      sections.forEach(sec => {{
        const visibleInSec = sec.querySelectorAll('.zen-card[style="display: flex;"]').length;
        sec.style.display = (q && visibleInSec === 0) ? 'none' : 'block';
      }});

      counter.textContent = visibleCount + ' / 70';
    }});
  </script>
</body>
</html>
"""
    with open(BASE_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(doc_html)

def main():
    print("=" * 60)
    print("AoPS GitHub Pages Site Generator")
    print("=" * 60)
    
    levels, flat_modules = parse_curriculum()
    print(f"Parsed {len(levels)} levels and {len(flat_modules)} total modules.")

    # 1. Create .nojekyll
    nojekyll_path = BASE_DIR / ".nojekyll"
    if not nojekyll_path.exists():
        nojekyll_path.touch()
        print("Created .nojekyll")

    # 2. Generate lesson.html and challenge.html for every module
    print("Generating standalone lesson and challenge HTML files...")
    for idx, mod in enumerate(flat_modules):
        prev_m = flat_modules[idx - 1] if idx > 0 else None
        next_m = flat_modules[idx + 1] if idx < len(flat_modules) - 1 else None
        generate_lesson_html(mod, prev_m, next_m)
        generate_challenge_html(mod)

    print(f"Generated 70 lesson.html and 70 challenge.html files.")

    # 3. Generate reader.html
    generate_dynamic_reader()
    print("Generated universal reader.html")

    # 4. Generate master index.html
    generate_index_html(levels, flat_modules)
    print("Generated master index.html")

    print("Build complete!")

if __name__ == "__main__":
    main()
