"""Shared chrome, SEO head and the Silica syntax highlighter for the site.

The highlighter uses the real keyword and type tables from the language
implementation, so a keyword cannot be highlighted unless Silica has it.
"""

import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("SILICA_REPO", "/scratch/work/silica")

if REPO not in sys.path:
    sys.path.insert(0, REPO)

try:  # the real tables; a missing repo falls back to a literal copy
    from silica.tokens import BUILTIN_TYPES, KEYWORDS  # noqa: E402
except Exception:  # pragma: no cover
    KEYWORDS = {
        "sprint", "dit", "input", "oui", "nein", "und", "ou", "non", "si",
        "sino", "tant", "per", "in", "break", "continue", "fin", "halt",
        "sfn", "ret", "use", "let", "const",
    }
    BUILTIN_TYPES = {"Int", "Float", "Bool", "String", "Unit", "List", "Map", "Any"}

SITE_NAME = "Silica"
BASE_URL = "https://sufiyan-sabeel.github.io/silica-website"
VERSION = "0.9.0"
GITHUB = "https://github.com/sufiyan-sabeel/silica"
CREATOR_GITHUB = "https://github.com/sufiyan-sabeel"
INSTAGRAM = "https://www.instagram.com/umaizsufiyan.78/"
LICENSE = "MIT"

MODULE_NAMES = {
    "math", "string", "collections", "json", "fs", "ui", "tui", "gui",
    "speech", "voice", "core", "lib",
}
CORE_CALLS = {
    "sprint", "dit", "input", "type_of", "assert", "str", "int", "float",
    "len", "range", "push", "keys", "values", "has",
}


# --------------------------------------------------------------------------
# icons (Lucide, ISC licence — inlined so the site needs no CDN)
# --------------------------------------------------------------------------
def icon(name, cls=""):
    paths = {
        "github": '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.4 5.4 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/>',
        "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
        "arrow-left": '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
        "book": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/>',
        "terminal": '<polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/>',
        "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
        "layers": '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
        "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
        "cpu": '<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>',
        "zap": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
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
        "package": '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
        "compass": '<path d="m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z"/><circle cx="12" cy="12" r="10"/>',
        "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    }
    body = paths.get(name, paths["info"])
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.75" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true" focusable="false"%s>%s</svg>'
        % (' class="%s"' % cls if cls else "", body)
    )


# --------------------------------------------------------------------------
# syntax highlighting
# --------------------------------------------------------------------------
_OPERATORS = set("+-*/%=<>(){}[],:.;!")


def highlight(source):
    """Return HTML with Silica tokens wrapped in span classes."""
    out = []
    i = 0
    n = len(source)
    while i < n:
        ch = source[i]

        # comments
        if ch == "#" or (ch == "/" and source[i:i + 2] == "//"):
            end = source.find("\n", i)
            end = n if end == -1 else end
            out.append('<span class="tok-com">%s</span>'
                       % html.escape(source[i:end]))
            i = end
            continue

        # strings: triple quotes first, then single/double
        triple = source[i:i + 3]
        if triple in ('"""', "'''"):
            end = source.find(triple, i + 3)
            end = n if end == -1 else end + 3
            out.append('<span class="tok-str">%s</span>'
                       % html.escape(source[i:end]))
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
            out.append('<span class="tok-str">%s</span>'
                       % html.escape(source[i:end]))
            i = end
            continue

        # numbers
        if ch.isdigit():
            j = i
            while j < n and (source[j].isdigit() or source[j] == "."):
                j += 1
            out.append('<span class="tok-num">%s</span>'
                       % html.escape(source[i:j]))
            i = j
            continue

        # identifiers and keywords
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
# small HTML builders
# --------------------------------------------------------------------------
_block_ids = {}


def code_block(source, filename=None, block_id=None, show_copy=True,
               label=None, extra_class=""):
    """A styled code window with pre-highlighted Silica source."""
    if block_id is None:
        _block_ids[filename or "x"] = _block_ids.get(filename or "x", 0) + 1
        block_id = "code-%s-%d" % ((filename or "snippet").replace(".", "-"),
                                   _block_ids[filename or "x"])

    parts = ['<div class="code %s">' % extra_class]
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
    parts.append('<pre id="%s" tabindex="0"><code>%s</code></pre>'
                 % (block_id, highlight(source)))
    parts.append("</div>")
    return "".join(parts)


def output_block(text, filename="output", label="Output"):
    return code_block(text, filename=filename, show_copy=False, label=label,
                      extra_class="code--out")


def callout(body, kind="info"):
    icon_name = "alert" if kind == "warn" else "info"
    cls = "callout callout--warn" if kind == "warn" else "callout"
    return '<div class="%s">%s<p>%s</p></div>' % (cls, icon(icon_name), body)


# --------------------------------------------------------------------------
# page registry
# --------------------------------------------------------------------------
DOC_PAGES = [
    ("getting-started", "Getting Started",
     "Install Silica and run your first program: the toolchain, the REPL and the "
     "first five things to try."),
    ("installation", "Installation",
     "Every supported way to install Silica 0.9.0 — the installer, Termux, pip, "
     "and running from a checkout — with troubleshooting."),
    ("syntax", "Syntax",
     "Silica's keywords, statements, expressions, operators and block rules, "
     "with the grammar the v0.9.0 parser actually accepts."),
    ("variables-and-data-types", "Variables and Data Types",
     "let and const, type annotations, inference, and the eight types Silica "
     "checks: Int, Float, Bool, String, Unit, List, Map, Any."),
    ("functions", "Functions",
     "Declaring functions with sfn, parameters, return types, recursion, and how "
     "Silica reports errors."),
    ("control-flow", "Control Flow",
     "si/sino, tant, per, break, continue and halt — with the short-circuit "
     "operators und, ou and non."),
    ("strings", "Strings",
     "Four string delimiter forms, escapes, indexing, concatenation and the "
     "string module."),
    ("built-in-functions", "Built-in Functions",
     "The core, math, string, collections, json and fs modules, with real "
     "output for every example."),
    ("cli-reference", "CLI Reference",
     "Every silica command and flag: run, check, compile, repl, fmt, test, ide, "
     "voice, capabilities."),
    ("examples", "Examples",
     "Runnable Silica programs from the repository, each verified against the "
     "v0.9.0 implementation."),
    ("faq", "FAQ",
     "Straight answers about performance, completeness, platforms, licensing "
     "and where Silica is going."),
]


def nav_links(root):
    return [
        ("Features", root + "index.html#features"),
        ("Playground", root + "index.html#playground"),
        ("Docs", root + "docs/getting-started.html"),
        ("Install", root + "index.html#install"),
        ("Roadmap", root + "index.html#roadmap"),
    ]


def head(page):
    """page: dict with title, description, path (relative), url (absolute)."""
    title = page["title"]
    description = page["description"]
    canonical = page["canonical"]
    root = page["root"]
    og_image = BASE_URL + "/assets/img/og-cover.jpg"
    json_ld = page.get("json_ld", "")

    return """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(description)s">
<link rel="canonical" href="%(canonical)s">
<meta name="author" content="Umaiz Sufiyan">
<meta name="robots" content="%(robots)s">
<meta name="theme-color" content="#0b0d10">
<meta name="color-scheme" content="dark light">

<meta property="og:type" content="%(og_type)s">
<meta property="og:site_name" content="Silica Programming Language">
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

<link rel="icon" href="%(root)sassets/img/favicon.ico" sizes="32x32">
<link rel="icon" href="%(root)sassets/img/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="%(root)sassets/img/icon-192.png">
<link rel="stylesheet" href="%(root)sassets/css/site.css">
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
    }


def header(root, current=None):
    links = []
    for label, href in nav_links(root):
        current_attr = ""
        if current and label == current:
            current_attr = ' aria-current="page"'
        links.append('<a href="%s"%s>%s</a>' % (href, current_attr, label))

    return """<header class="site-header">
  <div class="wrap">
    <a class="brand" href="%(root)sindex.html" aria-label="Silica home">
      <img src="%(root)sassets/img/mark-dark.png" alt="" class="logo-dark" width="24" height="31">
      <img src="%(root)sassets/img/mark-light.png" alt="" class="logo-light" width="24" height="31">
      <span>Silica</span>
    </a>
    <nav class="nav" id="site-nav" aria-label="Primary">
      %(links)s
    </nav>
    <div class="nav-actions">
      <button class="icon-btn" type="button" data-theme-toggle aria-label="Switch to light theme">
        <svg class="icon-sun" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
      </button>
      <a class="btn btn--ghost btn--sm" href="%(github)s" rel="noopener">
        %(github_icon)s<span>GitHub</span>
      </a>
      <button class="icon-btn nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>
      </button>
    </div>
  </div>
</header>
""" % {
        "root": root,
        "links": "\n      ".join(links),
        "github": GITHUB,
        "github_icon": icon("github"),
    }


def footer(root):
    doc_links = "\n        ".join(
        '<li><a href="%sdocs/%s.html">%s</a></li>' % (root, slug, label)
        for slug, label, _ in DOC_PAGES[:8]
    )
    return """<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="%(root)sassets/img/logo-dark.png" alt="Silica" class="logo-dark" width="132" height="52">
        <img src="%(root)sassets/img/logo-light.png" alt="Silica" class="logo-light" width="132" height="52">
        <p>An open-source, high-level general-purpose programming language with its
        own syntax, a checked compiler and a versioned bytecode format.
        Created by Umaiz Sufiyan.</p>
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
          <li><a href="%(github)s/issues" rel="noopener">Issues</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Creator</h4>
        <ul>
          <li><a href="%(creator)s" rel="noopener">Umaiz Sufiyan</a></li>
          <li><a href="%(instagram)s" rel="noopener">Instagram</a></li>
          <li><a href="%(root)sindex.html#creator">About the creator</a></li>
          <li><a href="%(github)s/blob/main/LICENSE" rel="noopener">MIT licence</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p style="margin:0">© 2026 Umaiz Sufiyan. Silica is released under the MIT licence.</p>
      <p style="margin:0">Designed and developed with curiosity by Umaiz Sufiyan.</p>
    </div>
  </div>
</footer>
<script src="%(root)sassets/js/site.js" defer></script>
</body>
</html>
""" % {
        "root": root,
        "doc_links": doc_links,
        "github": GITHUB,
        "creator": CREATOR_GITHUB,
        "instagram": INSTAGRAM,
    }
