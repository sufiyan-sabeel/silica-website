"""Build the Silica website in place.

    python3 tools/fetch_repo_status.py     # capture live repository facts
    python3 tools/verify_snippets.py PATH  # verify every code example
    python3 tools/build_site.py            # generate the pages

Output is plain static HTML/CSS/JS plus a search index, served directly by
GitHub Pages from the repository root.
"""

import datetime
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pages_docs  # noqa: E402
import pages_home  # noqa: E402
from site_chrome import (BASE_URL, BUILT, DOC_PAGES, GITHUB, LICENSE, RELEASE,  # noqa: E402
                         STATUS, VERSION, footer, head, header, search_dialog)

ROOT = os.path.dirname(HERE)
OUT = ROOT          # built in place: the repository root is the published site
TODAY = datetime.date.today().isoformat()

DOC_GROUPS = [
    ("Start here", ["introduction", "getting-started", "installation"]),
    ("Language", ["syntax", "variables-and-data-types", "functions",
                  "control-flow", "strings", "structs", "generics"]),
    ("Reference", ["built-in-functions", "cli-reference", "examples", "faq"]),
]


# --------------------------------------------------------------------------
# structured data
# --------------------------------------------------------------------------
def person_json_ld():
    return {
        "@type": "Person",
        "@id": BASE_URL + "/#creator",
        "name": "Umaiz Sufiyan",
        "url": "https://github.com/sufiyan-sabeel",
        "jobTitle": "Student Developer and Creator of Silica",
        "sameAs": [
            "https://github.com/sufiyan-sabeel",
            "https://www.instagram.com/umaizsufiyan.78/",
        ],
    }


def home_json_ld():
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": BASE_URL + "/#website",
                "url": BASE_URL + "/",
                "name": "Silica",
                "alternateName": "Silica Programming Language",
                "description": "The official website of Silica, an open-source, "
                               "high-level, general-purpose programming language.",
                "inLanguage": "en",
                "publisher": {"@id": BASE_URL + "/#creator"},
            },
            {
                "@type": "SoftwareSourceCode",
                "@id": BASE_URL + "/#software",
                "name": "Silica",
                "alternateName": "Silica Programming Language",
                "description": "An open-source, high-level general-purpose "
                               "programming language with its own syntax, a "
                               "checked compiler and a versioned bytecode format.",
                "codeRepository": GITHUB,
                "programmingLanguage": {"@type": "ComputerLanguage", "name": "Silica"},
                "runtimePlatform": "Python 3.9+",
                "version": VERSION,
                "license": "https://opensource.org/licenses/MIT",
                "author": {"@id": BASE_URL + "/#creator"},
                "applicationCategory": "DeveloperApplication",
                "operatingSystem": "Linux, Termux",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            },
            {
                "@type": "SoftwareApplication",
                "name": "Silica toolchain",
                "applicationCategory": "DeveloperApplication",
                "operatingSystem": "Linux, Termux",
                "softwareVersion": VERSION,
                "license": "https://opensource.org/licenses/MIT",
                "url": BASE_URL + "/",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            },
            person_json_ld(),
        ],
    }


def doc_json_ld(slug, title, description):
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "headline": title,
                "description": description,
                "url": "%s/docs/%s.html" % (BASE_URL, slug),
                "inLanguage": "en",
                "author": {"@id": BASE_URL + "/#creator"},
                "publisher": {"@id": BASE_URL + "/#creator"},
                "isPartOf": {"@id": BASE_URL + "/#website"},
                "about": {"@id": BASE_URL + "/#software"},
                "proficiencyLevel": "Beginner",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home",
                     "item": BASE_URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Documentation",
                     "item": "%s/docs/introduction.html" % BASE_URL},
                    {"@type": "ListItem", "position": 3, "name": title,
                     "item": "%s/docs/%s.html" % (BASE_URL, slug)},
                ],
            },
            person_json_ld(),
        ],
    }


def script_tag(data):
    return ('<script type="application/ld+json">%s</script>\n'
            % json.dumps(data, indent=2, ensure_ascii=False))


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def strip_tags(markup):
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", markup, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def build_toc(body):
    items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S)
    if len(items) < 2:
        return ""
    links = []
    for anchor, text in items:
        label = strip_tags(text)
        links.append('<li><a href="#%s">%s</a></li>' % (anchor, html.escape(label)))
    return ('<nav class="toc" aria-label="On this page">'
            '<p class="toc__title">On this page</p><ul>%s</ul></nav>'
            % "".join(links))


def build_search_index(rendered):
    """One entry per heading section, so results land on the right paragraph."""
    entries = []
    for slug, label, _description, body in rendered:
        parts = re.split(r'<h2 id="([^"]+)">(.*?)</h2>', body, flags=re.S)
        intro = strip_tags(parts[0])[:520]
        if intro:
            entries.append({
                "page": label,
                "title": label,
                "url": "docs/%s.html" % slug,
                "text": intro,
            })
        for i in range(1, len(parts) - 2, 3):
            anchor, heading, rest = parts[i], parts[i + 1], parts[i + 2]
            text = strip_tags(rest)[:700]
            if not text:
                continue
            entries.append({
                "page": label,
                "title": strip_tags(heading),
                "url": "docs/%s.html#%s" % (slug, anchor),
                "text": text,
            })
    return entries


def docs_nav(current):
    labels = dict((s, l) for s, l, _ in DOC_PAGES)
    groups = []
    for name, slugs in DOC_GROUPS:
        links = []
        for slug in slugs:
            current_attr = ' aria-current="page"' if slug == current else ""
            links.append('<li><a href="%s.html"%s>%s</a></li>'
                         % (slug, current_attr, labels[slug]))
        groups.append(
            '<div class="docs-nav__group"><p class="docs-nav__title">%s</p>'
            "<ul>%s</ul></div>" % (name, "".join(links))
        )
    return ('<nav class="docs-nav" id="docs-nav" aria-label="Documentation">%s</nav>'
            % "".join(groups))


def pager(current):
    slugs = [s for s, _, _ in DOC_PAGES]
    labels = dict((s, l) for s, l, _ in DOC_PAGES)
    index = slugs.index(current)
    parts = []
    if index > 0:
        prev_slug = slugs[index - 1]
        parts.append('<a class="prev" href="%s.html"><span>Previous</span>%s</a>'
                     % (prev_slug, labels[prev_slug]))
    if index < len(slugs) - 1:
        next_slug = slugs[index + 1]
        parts.append('<a class="next" href="%s.html"><span>Next</span>%s</a>'
                     % (next_slug, labels[next_slug]))
    return '<div class="pager">%s</div>' % "".join(parts)


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as handle:
        handle.write(text)
    return full


# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------
def build_home():
    page = {
        "title": "Silica — A Language Built to Create",
        "description": "Silica is an open-source, high-level general-purpose "
                       "programming language created by Umaiz Sufiyan. Explore the "
                       "syntax, features and documentation.",
        "canonical": BASE_URL + "/",
        "root": "",
        "json_ld": script_tag(home_json_ld()),
    }
    document = (
        head(page)
        + header("")
        + search_dialog("")
        + '<main id="main">' + pages_home.body() + "</main>"
        + footer("")
    )
    return write("index.html", document)


def build_docs():
    written = []
    rendered = []

    for slug, label, description in DOC_PAGES:
        body = pages_docs.PAGES[slug]()
        rendered.append((slug, label, description, body))

        page = {
            "title": "%s — Silica documentation" % label,
            "description": description,
            "canonical": "%s/docs/%s.html" % (BASE_URL, slug),
            "root": "../",
            "og_type": "article",
            "json_ld": script_tag(doc_json_ld(slug, label, description)),
        }

        article = (
            '<main id="main"><div class="wrap"><div class="docs">'
            + '<div class="docs-menu" data-docs-menu>'
            + '<button class="docs-menu__toggle" type="button" data-docs-toggle '
              'aria-expanded="true" aria-controls="docs-nav">Documentation menu</button>'
            + docs_nav(slug)
            + "</div>"
            + '<article class="article">'
            + '<nav class="breadcrumbs" aria-label="Breadcrumb">'
            + '<a href="../index.html">Home</a><span aria-hidden="true">/</span>'
            + '<a href="introduction.html">Documentation</a>'
            + '<span aria-hidden="true">/</span>'
            + "<span>%s</span></nav>" % html.escape(label)
            + "<h1>%s</h1>" % label
            + body
            + pager(slug)
            + "</article>"
            + build_toc(body)
            + "</div></div></main>"
        )
        written.append(write(
            "docs/%s.html" % slug,
            head(page) + header("../", "Documentation") + search_dialog("../")
            + article + footer("../"),
        ))

    index = build_search_index(rendered)
    write("assets/search-index.json",
          json.dumps(index, ensure_ascii=False, separators=(",", ":")))
    return written, index


def build_404():
    page = {
        "title": "Page not found — Silica",
        "description": "That page does not exist on the Silica website.",
        "canonical": BASE_URL + "/404.html",
        "root": "/silica-website/",
        "robots": "noindex, follow",
        "json_ld": script_tag({
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Page not found",
            "url": BASE_URL + "/404.html",
            "isPartOf": {"@id": BASE_URL + "/#website"},
            "inLanguage": "en",
        }),
    }
    body = """
<main id="main">
  <div class="wrap error-page">
    <div>
      <p class="eyebrow" style="justify-content:center">Error 404</p>
      <h1>This page is not in the bytecode.</h1>
      <p class="lede" style="margin-inline:auto">The address you followed does not
      exist here. The documentation index is the best place to pick up again.</p>
      <div class="btn-row" style="justify-content:center">
        <a class="btn btn--primary" href="/silica-website/index.html">%(home)s Home</a>
        <a class="btn btn--ghost" href="/silica-website/docs/introduction.html">%(book)s Documentation</a>
      </div>
      %(code)s
    </div>
  </div>
</main>
""" % {
        "home": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>',
        "book": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/></svg>',
        "code": '<div class="code code--plain" style="max-width:420px;margin-inline:auto">'
                '<div class="code__bar"><span class="code__dots"><i></i><i></i>'
                '<i></i></span><span class="code__name">404.sc</span></div>'
                '<div class="code__body"><pre><code><span class="tok-kw">sfn</span> '
                '<span class="tok-fn">main</span>() {\n'
                '    <span class="tok-fn">halt</span>(<span class="tok-num">404</span>)\n'
                "}</code></pre></div></div>",
    }
    return write("404.html", head(page) + header("/silica-website/") + body
                 + footer("/silica-website/"))


def build_seo():
    urls = [(BASE_URL + "/", "1.0")]
    for slug, _, _ in DOC_PAGES:
        urls.append(("%s/docs/%s.html" % (BASE_URL, slug), "0.8"))

    entries = []
    for loc, priority in urls:
        entries.append(
            "  <url>\n"
            "    <loc>%s</loc>\n"
            "    <lastmod>%s</lastmod>\n"
            "    <changefreq>monthly</changefreq>\n"
            "    <priority>%s</priority>\n"
            "  </url>" % (loc, TODAY, priority)
        )

    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "\n".join(entries) + "\n</urlset>\n")

    write("robots.txt",
          "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE_URL)
    write(".nojekyll", "")
    return urls


README = """<p align="center">
  <a href="https://gitdiagram.com/sufiyan-sabeel/silica?utm_source=readme&amp;utm_medium=badge">
    <img src="https://gitdiagram.com/diagram-badge.svg" alt="Architecture diagram">
  </a>
</p>

# Silica — official website

The official website for [Silica](https://github.com/sufiyan-sabeel/silica), an
open-source general-purpose programming language created by Umaiz Sufiyan.

**Live at https://sufiyan-sabeel.github.io/silica-website/**
**Language repository: https://github.com/sufiyan-sabeel/silica**

## What this is

A static site served by GitHub Pages straight from `main`: plain HTML, one
stylesheet, two small scripts, no framework and no bundler. A push is a deploy.

```
index.html                 homepage (hero 3D, features, playground, roadmap, …)
docs/*.html                thirteen documentation pages
assets/css/site.css        the whole design system ("Silica Midnight")
assets/js/site.js          theme, nav, tabs, copy, search, live repo status
assets/js/crystal.js       the hero crystal — hand-written WebGL, no library
assets/img/                logo, mark, icons, social card
assets/search-index.json   generated index for the documentation search
sitemap.xml robots.txt     search-engine plumbing
404.html                   not-found page
tools/                     the generator that produced everything above
```

## The 3D hero

`assets/js/crystal.js` draws an icosahedron with raw WebGL: two translucent
shells (back faces, then front faces), an inner solid, and edge lines, lit by a
key light plus a fresnel rim. No three.js, no model file, no network request.

It is deliberately defensive: device pixel ratio capped at 2, rendering stops
when the canvas leaves the viewport or the tab is hidden, `prefers-reduced-motion`
renders one still frame, and if WebGL is unavailable the inline SVG fallback in
`index.html` stays on screen. `tools/crystal_svg.py` generates that fallback from
the same geometry, so the two views are the same object.

## Live repository status

The homepage carries a status board: latest release, last commit, stars, forks and
open issues, read from the public GitHub API in the visitor's browser. The build
bakes the same values in as a fallback, so the page is correct with JavaScript
disabled and honest when the API is rate-limited.

`tools/fetch_repo_status.py` captures stars, forks, open issues, the latest
release and the last push into `tools/repo_status.json`. The build bakes those
values into the page, and `site.js` refreshes them from the public GitHub API on
load — no token, no backend. If the API is rate-limited the baked values and their
timestamp stand.

## Editing

Edit the HTML in place, or regenerate it:

```
tools/build_site.py        page chrome, docs layout, search index, sitemap
tools/pages_home.py        homepage sections
tools/pages_docs.py        documentation pages
tools/snippets.py          every code example, in one place
tools/verify_snippets.py   runs each example against the real toolchain
tools/crystal_svg.py       the SVG fallback for the hero
tools/check_site.py        links, metadata, structure, overflow
```

Every code example on the site is executed against the Silica implementation
before publication, so the documentation cannot drift from the language.

## Accessibility and performance

Semantic landmarks, a skip link, keyboard-operable tabs and search, visible focus
states, `prefers-reduced-motion` support, a light and dark theme, no layout shift
from the canvas, and no third-party scripts. Inter and JetBrains Mono are loaded
from Google Fonts with `display=swap`; the design falls back to the system stack
if that request fails.

## Licence

MIT, like Silica itself. Copyright (c) 2026 Umaiz Sufiyan.
"""


def main():
    if not os.path.isdir(os.path.join(OUT, "assets")):
        raise SystemExit("missing assets/ — the stylesheet and images must exist")

    written = [build_home()]
    docs_written, index = build_docs()
    written += docs_written
    written.append(build_404())
    urls = build_seo()
    write("README.md", README)

    total = sum(os.path.getsize(path) for path in written)
    print("built %d pages (%d documentation), %.1f KB of HTML"
          % (len(written), len(docs_written), total / 1024.0))
    print("search index: %d entries" % len(index))
    print("sitemap: %d urls" % len(urls))
    print("release: %s (captured %s)" % (RELEASE, BUILT))


if __name__ == "__main__":
    main()
