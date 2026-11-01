"""Shared chrome, SEO head, icons and the Silica syntax highlighter.

Keyword and type tables are imported from the language implementation, so a
token cannot be highlighted unless Silica actually has it.
"""

import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("SILICA_REPO", "/scratch/work/silica-0.9.3")

if REPO not in sys.path:
    sys.path.insert(0, REPO)

try:  # the real tables; a missing checkout falls back to a literal copy
    from silica.tokens import BUILTIN_TYPES, KEYWORDS  # noqa: E402
except Exception:  # pragma: no cover
    KEYWORDS = {
        "sprint", "dit", "input", "oui", "nein", "und", "ou", "non", "si",
        "sino", "tant", "per", "in", "break", "continue", "fin", "halt",
        "sfn", "ret", "use", "let", "const", "struct",
    }
    BUILTIN_TYPES = {"Int", "Float", "Bool", "String", "Unit", "List", "Map", "Any"}

# --- repository facts, captured by tools/fetch_repo_status.py ---------------
STATUS_PATH = os.path.join(HERE, "repo_status.json")
try:
    with open(STATUS_PATH, encoding="utf-8") as _fh:
        STATUS = json.load(_fh)
except Exception:  # pragma: no cover
    STATUS = {}

RELEASE = (STATUS.get("latest_release") or {}).get("tag") or "v0.9.3"
VERSION = RELEASE.lstrip("v")
BUILT = (STATUS.get("fetched_at") or "")[:10]

SITE_NAME = "Silica"

# --- asset versioning -------------------------------------------------------
# Every asset URL carries a short hash of the files it depends on, so a visitor
# who cached the previous build (including the corrupt logo that shipped once)
# gets the current bytes without clearing anything.
def _asset_version():
    import hashlib
    digest = hashlib.sha256()
    for relative in ("assets/css/site.css", "assets/js/site.js",
                     "assets/js/crystal.js", "assets/img/logo-dark.png",
                     "assets/img/logo-light.png", "assets/img/mark-dark.png",
                     "assets/img/mark-light.png"):
        path = os.path.join(os.path.dirname(HERE), relative)
        try:
            with open(path, "rb") as handle:
                digest.update(handle.read())
        except OSError:
            digest.update(relative.encode())
    return digest.hexdigest()[:8]


ASSET_V = _asset_version()


def asset(root, relative):
    """A versioned URL for a file under assets/."""
    return "%sassets/%s?v=%s" % (root, relative, ASSET_V)
BASE_URL = "https://sufiyan-sabeel.github.io/silica-website"
GITHUB = "https://github.com/sufiyan-sabeel/silica"
CREATOR_GITHUB = "https://github.com/sufiyan-sabeel"
INSTAGRAM = "https://www.instagram.com/umaizsufiyan.78/"
LICENSE = "MIT"

MODULE_NAMES = {
    "math", "string", "collections", "json", "fs", "ui", "tui", "gui",
    "speech", "voice", "core", "colors", "lib",
}
CORE_CALLS = {
    "sprint", "dit", "input", "type_of", "assert", "str", "int", "float",
    "len", "range", "push", "keys", "values", "has",
}


# --------------------------------------------------------------------------
# icons (Lucide, ISC licence — inlined so the site needs no icon CDN)
# --------------------------------------------------------------------------
def icon(name, cls=""):
    paths = {
        "github": '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.4 5.4 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/>',
        "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
        "arrow-left": '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
        "arrow-up-right": '<path d="M7 17 17 7"/><path d="M7 7h10v10"/>',
        "chevron-down": '<path d="m6 9 6 6 6-6"/>',
        "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
        "book": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/>',
        "terminal": '<polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/>',
        "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
        "braces": '<path d="M8 3H7a2 2 0 0 0-2 2v5a2 2 0 0 1-2 2 2 2 0 0 1 2 2v5c0 1.1.9 2 2 2h1"/><path d="M16 21h1a2 2 0 0 0 2-2v-5c0-1.1.9-2 2-2a2 2 0 0 1-2-2V5a2 2 0 0 0-2-2h-1"/>',
        "box": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
        "palette": '<circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/>',
        "layers": '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
        "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
        "cpu": '<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>',
        "zap": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
        "gauge": '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
        "file-text": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
        "copy": '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
        "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
        "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
        "menu": '<line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/>',
        "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
        "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
        "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
        "check": '<path d="M20 6 9 17l-5-5"/>',
        "sparkles": '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>',
        "instagram": '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>',
        "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
        "git-branch": '<line x1="6" x2="6" y1="3" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/>',
        "git-commit": '<circle cx="12" cy="12" r="3"/><line x1="3" x2="9" y1="12" y2="12"/><line x1="15" x2="21" y1="12" y2="12"/>',
        "star": '<path d="M11.5 2.9a.6.6 0 0 1 1 0l2.4 4.9 5.4.8a.6.6 0 0 1 .3 1l-3.9 3.8.9 5.4a.6.6 0 0 1-.9.6L12 17.9l-4.8 2.5a.6.6 0 0 1-.9-.6l.9-5.4L3.3 9.6a.6.6 0 0 1 .3-1l5.4-.8Z"/>',
        "package": '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
        "compass": '<path d="m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z"/><circle cx="12" cy="12" r="10"/>',
        "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
    }
    body = paths.get(name, paths["info"])
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true" focusable="false"%s>%s</svg>'
        % (' class="%s"' % cls if cls else "", body)
    )


# --------------------------------------------------------------------------
# syntax highlighting
# --------------------------------------------------------------------------
_OPERATORS = set("+-*/%=<>(){}[],:.;!")


def highlight(source):
    out = []
    i = 0
    n = len(source)
    while i < n:
        ch = source[i]

        if ch == "#" or (ch == "/" and source[i:i + 2] == "//"):
            end = source.find("\n", i)
            end = n if end == -1 else end
            out.append('<span class="tok-com">%s</span>' % html.escape(source[i:end]))
            i = end
            continue

        triple = source[i:i + 3]
        if triple in ('"""', "'''"):
            end = source.find(triple, i + 3)
            end = n if end == -1 else end + 3
            out.append('<span class="tok-str">%s</span>' % html.escape(source[i:end]))
            i = end
            continue

        if ch in ('"', "'"):
            j = i + 1
            while j < n:
                if source[j] == "\\":
                    j += 2
                    continue
                if source[j] == ch or source[j] == "\n":
                    break
                j += 1
            end = min(j + 1, n)
            out.append('<span class="tok-str">%s</span>' % html.escape(source[i:end]))
            i = end
            continue

        if ch.isdigit():
            j = i
            while j < n and (source[j].isdigit() or source[j] == "."):
                j += 1
            out.append('<span class="tok-num">%s</span>' % html.escape(source[i:j]))
            i = j
            continue

        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (source[j].isalnum() or source[j] == "_"):
                j += 1
            word = source[i:j]
            rest = source[j:j + 1]
            if word in KEYWORDS:
                cls = "tok-kw"
            elif word in BUILTIN_TYPES:
                cls = "tok-type"
            elif word in MODULE_NAMES:
                cls = "tok-mod"
            elif rest == "(" or word in CORE_CALLS:
                cls = "tok-fn"
            else:
                out.append(html.escape(word))
                i = j
                continue
            out.append('<span class="%s">%s</span>' % (cls, html.escape(word)))
            i = j
            continue

        if ch in _OPERATORS:
            out.append('<span class="tok-op">%s</span>' % html.escape(ch))
            i += 1
            continue

        out.append(html.escape(ch))
        i += 1

    return "".join(out)


# --------------------------------------------------------------------------
# HTML builders
# --------------------------------------------------------------------------
_block_ids = {}


def code_block(source, filename=None, block_id=None, show_copy=True,
               label=None, extra_class="", line_numbers=True):
    key = filename or "snippet"
    _block_ids[key] = _block_ids.get(key, 0) + 1
    if block_id is None:
        block_id = "code-%s-%d" % (key.replace(".", "-").replace(" ", "-"),
                                   _block_ids[key])

    body_class = "" if line_numbers else " code--plain"
    parts = ['<div class="code %s%s">' % (extra_class, body_class)]
    parts.append('<div class="code__bar"><span class="code__dots"><i></i><i></i><i></i></span>')
    if filename:
        parts.append('<span class="code__name">%s</span>' % html.escape(filename))
    if show_copy:
        parts.append(
            '<button class="code__copy" type="button" data-copy="%s" '
            'aria-label="Copy code to clipboard">%s<span>copy</span></button>'
            % (block_id, icon("copy"))
        )
    parts.append("</div>")
    if label:
        parts.append('<div class="code__label">%s</div>' % html.escape(label))

    if line_numbers:
        count = source.count("\n") + 1
        numbers = "\n".join(str(n) for n in range(1, count + 1))
        parts.append(
            '<div class="code__body">'
            '<div class="code__lines" aria-hidden="true">%s</div>'
            '<pre id="%s" tabindex="0"><code>%s</code></pre>'
            "</div>" % (numbers, block_id, highlight(source))
        )
    else:
        parts.append(
            '<div class="code__body"><pre id="%s" tabindex="0"><code>%s</code></pre></div>'
            % (block_id, highlight(source))
        )

    parts.append("</div>")
    return "".join(parts)


def output_block(text, filename="output", label="Output"):
    return code_block(text, filename=filename, show_copy=False, label=label,
                      extra_class="code--out", line_numbers=False)


def callout(body, kind="info"):
    icon_name = "alert" if kind == "warn" else "info"
    cls = "callout callout--warn" if kind == "warn" else "callout"
    return '<div class="%s">%s<p>%s</p></div>' % (cls, icon(icon_name), body)


# --------------------------------------------------------------------------
# page registry
# --------------------------------------------------------------------------
DOC_PAGES = [
    ("introduction", "Introduction",
     "What Silica is, why it exists, and what it can and cannot do today."),
    ("getting-started", "Getting Started",
     "Install Silica, run your first program, check it, compile it, and open the "
     "in-browser IDE."),
    ("installation", "Installation",
     "Every supported way to install Silica — the installer, Termux, pip, and "
     "running from a checkout — with troubleshooting."),
    ("syntax", "Language Syntax",
     "Keywords, statements, expressions, operators and block rules, with the "
     "grammar the current parser accepts."),
    ("variables-and-data-types", "Variables and Data Types",
     "let and const, type annotations, inference, and the types Silica checks."),
    ("functions", "Functions",
     "Declaring functions with sfn, parameters, return types, recursion, and how "
     "Silica reports errors."),
    ("control-flow", "Control Flow",
     "si/sino, tant, per, break, continue and halt, with the short-circuit "
     "operators und, ou and non."),
    ("strings", "Strings",
     "Four string delimiter forms, escapes, indexing, concatenation and the "
     "string module."),
    ("structs", "Structs",
     "Named records with typed fields: declaration, construction, field access, "
     "mutability, equality and nesting."),
    ("built-in-functions", "Built-in Functions",
     "The core, math, string, collections, json, colors and fs modules, with "
     "real output for every example."),
    ("cli-reference", "CLI Reference",
     "Every silica command and flag: run, check, compile, repl, fmt, test, ide, "
     "voice, capabilities."),
    ("examples", "Examples",
     "Runnable Silica programs, each verified against the current release."),
    ("faq", "FAQ",
     "Straight answers about performance, completeness, platforms and licensing."),
]


def nav_links(root):
    return [
        ("Overview", root + "index.html#overview"),
        ("Features", root + "index.html#features"),
        ("Documentation", root + "docs/introduction.html"),
        ("Playground", root + "index.html#playground"),
        ("Roadmap", root + "index.html#roadmap"),
        ("About", root + "index.html#creator"),
    ]


def head(page):
    title = page["title"]
    description = page["description"]
    canonical = page["canonical"]
    root = page["root"]
    og_image = BASE_URL + "/assets/img/og-cover.png"
    json_ld = page.get("json_ld", "")

    return """<!DOCTYPE html>
<html lang="en" data-theme="dark" data-accent="indigo">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(description)s">
<link rel="canonical" href="%(canonical)s">
<meta name="author" content="Umaiz Sufiyan">
<meta name="robots" content="%(robots)s">
<meta name="theme-color" content="#0b1020">
<meta name="color-scheme" content="dark light">

<meta property="og:type" content="%(og_type)s">
<meta property="og:site_name" content="Silica">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(description)s">
<meta property="og:url" content="%(canonical)s">
<meta property="og:image" content="%(og_image)s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Silica — a language built to create">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(description)s">
<meta name="twitter:image" content="%(og_image)s">

<link rel="icon" type="image/png" sizes="144x144" href="%(root)sfavicon.png">
<link rel="icon" href="%(favicon)s" sizes="32x32">
<link rel="icon" href="%(icon192)s" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="%(icon192)s">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="preload" as="image" href="%(markdark)s" media="(prefers-color-scheme: dark)">
<link rel="preload" as="image" href="%(marklight)s" media="(prefers-color-scheme: light)">
<link rel="stylesheet" href="%(stylesheet)s">
%(json_ld)s</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
""" % {
        "title": title,
        "description": description,
        "canonical": canonical,
        "root": root,
        "og_type": page.get("og_type", "website"),
        "og_image": og_image,
        "robots": page.get("robots", "index, follow, max-image-preview:large"),
        "json_ld": json_ld,
        "stylesheet": asset(root, "css/site.css"),
        "favicon": asset(root, "img/favicon.ico"),
        "icon192": asset(root, "img/icon-192.png"),
        "markdark": asset(root, "img/mark-dark.png"),
        "marklight": asset(root, "img/mark-light.png"),
    }


def search_dialog(root):
    return """<div class="search-dialog" id="search-dialog" data-index="%(root)sassets/search-index.json" hidden>
  <div class="search-panel" role="dialog" aria-modal="true" aria-label="Search the documentation">
    <div class="search-field">
      %(icon)s
      <input type="search" placeholder="Search the documentation…" aria-label="Search the documentation" autocomplete="off" spellcheck="false">
      <button class="search-close" type="button" data-search-close>esc</button>
    </div>
    <p class="search-empty" role="status">Type to search the documentation.</p>
    <ul class="search-results"></ul>
    <div class="search-hint"><span>↑ ↓ to move · Enter to open</span><span>Esc to close</span></div>
  </div>
</div>
""" % {"root": root, "icon": icon("search")}


def header(root, current=None):
    links = []
    for label, href in nav_links(root):
        current_attr = ' aria-current="page"' if current and label == current else ""
        links.append('<a href="%s"%s>%s</a>' % (href, current_attr, label))

    return """<header class="site-header">
  <div class="wrap">
    <a class="brand" href="%(root)sindex.html" aria-label="Silica — home">
      <img src="%(markdark)s" alt="" class="logo-dark" width="22" height="28">
      <img src="%(marklight)s" alt="" class="logo-light" width="22" height="28">
      <span>Silica</span>
    </a>
    <nav class="nav" id="site-nav" aria-label="Primary">
      %(links)s
      <div class="nav-drawer-cta">
        <a class="btn btn--ghost btn--sm" href="%(github)s" rel="noopener">%(github_icon)s GitHub</a>
        <a class="btn btn--primary btn--sm" href="%(root)sdocs/getting-started.html">Get Started</a>
      </div>
    </nav>
    <div class="nav-actions">
      <button class="search-open" type="button" data-search-open aria-label="Search the documentation">
        %(search)s<span>Search</span><kbd>/</kbd>
      </button>
      <button class="icon-btn" type="button" data-theme-toggle aria-label="Switch to light theme">
        %(sun)s
      </button>
      <div class="customizer" data-customizer>
        <button class="icon-btn" type="button" data-customizer-toggle aria-expanded="false" aria-controls="customizer-panel" aria-label="Customise appearance">
          %(palette)s
        </button>
        <div class="customizer__panel" id="customizer-panel" hidden>
          <div class="customizer__group">
            <p class="customizer__title">Accent</p>
            <div class="swatches" role="group" aria-label="Accent colour">
              %(swatches)s
            </div>
          </div>
          <div class="customizer__group">
            <p class="customizer__title">Theme</p>
            <div class="segmented" role="group" aria-label="Theme">
              <button type="button" data-theme-choice="dark" aria-pressed="true">Dark</button>
              <button type="button" data-theme-choice="light" aria-pressed="false">Light</button>
            </div>
          </div>
        </div>
      </div>
      <a class="btn btn--ghost btn--sm" href="%(github)s" rel="noopener">%(github_icon)s<span>GitHub</span></a>
      <a class="btn btn--primary btn--sm" href="%(root)sdocs/getting-started.html">Get Started</a>
      <button class="icon-btn nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
        %(menu)s
      </button>
    </div>
  </div>
  <div class="nav-backdrop" data-nav-backdrop hidden></div>
</header>
""" % {
        "root": root,
        "links": "\n      ".join(links),
        "github": GITHUB,
        "github_icon": icon("github"),
        "search": icon("search"),
        "sun": icon("sun"),
        "menu": icon("menu"),
        "palette": icon("palette"),
        "markdark": asset(root, "img/mark-dark.png"),
        "marklight": asset(root, "img/mark-light.png"),
        "swatches": "".join(
            '<button class="swatch" type="button" data-accent-choice="%s" '
            'aria-pressed="%s"><span style="--sw: %s"></span>%s</button>'
            % (slug, "true" if slug == "indigo" else "false", colour, label)
            for slug, label, colour in (
                ("indigo", "Indigo", "#8b9bff"),
                ("teal", "Teal", "#5fd3c0"),
                ("violet", "Violet", "#b79cff"),
                ("amber", "Amber", "#e8b765"),
                ("rose", "Rose", "#f08c9a"),
            )
        ),
    }


def footer(root):
    doc_links = "\n        ".join(
        '<li><a href="%sdocs/%s.html">%s</a></li>' % (root, slug, label)
        for slug, label, _ in DOC_PAGES[:7]
    )
    stars = STATUS.get("stars", 0)
    forks = STATUS.get("forks", 0)
    issues = STATUS.get("open_issues", 0)

    return """<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="%(logodark)s" alt="Silica" class="logo-dark" width="120" height="48" loading="lazy" decoding="async">
        <img src="%(logolight)s" alt="Silica" class="logo-light" width="120" height="48" loading="lazy" decoding="async">
        <p>An open-source, high-level general-purpose programming language with its
        own syntax, a checked compiler and a versioned bytecode format.</p>
        <div class="footer-meta">
          <span class="pill"><span class="pill__dot"></span><span data-version-label>%(release)s</span></span>
          <span class="pill">%(license)s licence</span>
          <span class="pill">Python 3.9+</span>
        </div>
      </div>
      <div class="footer-col">
        <h4>Documentation</h4>
        <ul>
        %(doc_links)s
        </ul>
      </div>
      <div class="footer-col">
        <h4>Project</h4>
        <ul>
          <li><a href="%(github)s" rel="noopener">Source on GitHub</a></li>
          <li><a href="%(github)s/releases" rel="noopener">Releases</a></li>
          <li><a href="%(github)s/blob/main/CHANGELOG.md" rel="noopener">Changelog</a></li>
          <li><a href="%(github)s/blob/main/docs/LANGUAGE_SPEC.md" rel="noopener">Language spec</a></li>
          <li><a href="%(github)s/issues" rel="noopener">Issues (%(issues)s)</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Creator</h4>
        <ul>
          <li><a href="%(creator)s" rel="noopener">Umaiz Sufiyan</a></li>
          <li><a href="%(instagram)s" rel="noopener">Instagram</a></li>
          <li><a href="%(root)sindex.html#creator">About the creator</a></li>
          <li><a href="%(github)s/blob/main/LICENSE" rel="noopener">%(license)s licence</a></li>
          <li><a href="%(root)sdocs/faq.html">FAQ</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 Umaiz Sufiyan. Silica is released under the %(license)s licence.</p>
      <p>Created by Umaiz Sufiyan.</p>
    </div>
  </div>
</footer>
<script src="%(scripts)s" defer></script>
%(extra_script)s</body>
</html>
""" % {
        "root": root,
        "doc_links": doc_links,
        "github": GITHUB,
        "creator": CREATOR_GITHUB,
        "instagram": INSTAGRAM,
        "release": RELEASE,
        "license": LICENSE,
        "issues": issues,
        "logodark": asset(root, "img/logo-dark.png"),
        "logolight": asset(root, "img/logo-light.png"),
        "scripts": asset(root, "js/site.js"),
        "extra_script": "",
    }
