"""Build the Silica website into ./site.

    python3 tools/verify_snippets.py /path/to/silica   # verify code first
    python3 tools/build_site.py                        # then build

The output is plain static HTML/CSS/JS with no build step at serve time, so it
can be served by GitHub Pages directly.
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
from site_chrome import (BASE_URL, DOC_PAGES, GITHUB, VERSION, footer, head,  # noqa: E402
                         header, icon)

ROOT = os.path.dirname(HERE)
OUT = ROOT   # the site is built in place at the repository root
TODAY = datetime.date.today().isoformat()

DOC_GROUPS = [
    ("Start here", ["getting-started", "installation"]),
    ("Language", ["syntax", "variables-and-data-types", "functions",
                  "control-flow", "strings"]),
    ("Reference", ["built-in-functions", "cli-reference", "examples", "faq"]),
]


def org_json_ld():
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
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": BASE_URL + "/#website",
                "url": BASE_URL + "/",
                "name": "Silica Programming Language",
                "description": "The official website of Silica, an open-source "
                               "high-level general-purpose programming language.",
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
            org_json_ld(),
        ],
    }
    return data


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
                     "item": "%s/docs/getting-started.html" % BASE_URL},
                    {"@type": "ListItem", "position": 3, "name": title,
                     "item": "%s/docs/%s.html" % (BASE_URL, slug)},
                ],
            },
            org_json_ld(),
        ],
    }


def script_tag(data):
    return ('<script type="application/ld+json">%s</script>\n'
            % json.dumps(data, indent=2, ensure_ascii=False))


def build_toc(body):
    """An "On this page" list from the page's own h2 headings."""
    items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S)
    if len(items) < 2:
        return ""
    links = []
    for anchor, text in items:
        label = re.sub(r"<[^>]+>", "", text).strip()
        links.append('<li><a href="#%s">%s</a></li>' % (anchor, label))
    return ('<nav class="toc" aria-label="On this page">'
            '<p class="toc__title">On this page</p><ul>%s</ul></nav>'
            % "".join(links))


def docs_nav(current):
    groups = []
    for name, slugs in DOC_GROUPS:
        links = []
        for slug in slugs:
            label = dict((s, l) for s, l, _ in DOC_PAGES)[slug]
            current_attr = ' aria-current="page"' if slug == current else ""
            links.append('<li><a href="%s.html"%s>%s</a></li>'
                         % (slug, current_attr, label))
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
        parts.append('<a class="prev" href="%s.html">%s%s</a>'
                     % (prev_slug, '<span>Previous</span>', labels[prev_slug]))
    if index < len(slugs) - 1:
        next_slug = slugs[index + 1]
        parts.append('<a class="next" href="%s.html">%s%s</a>'
                     % (next_slug, '<span>Next</span>', labels[next_slug]))
    return '<div class="pager">%s</div>' % "".join(parts)


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as handle:
        handle.write(text)
    return full


def build_home():
    page = {
        "title": "Silica Programming Language — an open-source language built to create",
        "description": "Silica is an open-source, high-level general-purpose "
                       "programming language with its own syntax, a checked "
                       "compiler, versioned bytecode and a capability-based "
                       "security model. Created by Umaiz Sufiyan.",
        "canonical": BASE_URL + "/",
        "root": "",
        "json_ld": script_tag(home_json_ld()),
    }
    document = (head(page) + header("") + '<main id="main">' + pages_home.body()
                + "</main>" + footer(""))
    return write("index.html", document)


def build_docs():
    written = []
    for slug, label, description in DOC_PAGES:
        page = {
            "title": "%s — Silica documentation" % label,
            "description": description,
            "canonical": "%s/docs/%s.html" % (BASE_URL, slug),
            "root": "../",
            "og_type": "article",
            "json_ld": script_tag(doc_json_ld(slug, label, description)),
        }
        body = pages_docs.PAGES[slug]()
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
            + '<a href="getting-started.html">Docs</a><span aria-hidden="true">/</span>'
            + "<span>%s</span></nav>" % html.escape(label)
            + "<h1>%s</h1>" % label
            + body
            + pager(slug)
            + "</article>"
            + build_toc(body)
            + "</div></div></main>"
        )
        written.append(write("docs/%s.html" % slug,
                             head(page) + header("../", "Docs") + article + footer("../")))
    return written


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
        <a class="btn btn--ghost" href="/silica-website/docs/getting-started.html">%(book)s Documentation</a>
      </div>
      %(code)s
    </div>
  </div>
</main>
""" % {
        "home": icon("arrow-right"),
        "book": icon("book"),
        "code": '<div class="code" style="max-width:420px;margin-inline:auto">'
                '<div class="code__bar"><span class="code__dots"><i></i><i></i>'
                '<i></i></span><span class="code__name">404.sc</span></div>'
                '<pre><code><span class="tok-kw">sfn</span> '
                '<span class="tok-fn">main</span>() {\n'
                '    <span class="tok-fn">halt</span>(<span class="tok-num">404</span>)\n'
                "}</code></pre></div>",
    }
    # the 404 page is served from any path, so links are site-absolute
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

    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(entries) + "\n</urlset>\n")
    write("sitemap.xml", sitemap)

    robots = ("User-agent: *\n"
              "Allow: /\n"
              "\n"
              "Sitemap: %s/sitemap.xml\n" % BASE_URL)
    write("robots.txt", robots)

    # GitHub Pages: serve files as-is instead of running Jekyll
    write(".nojekyll", "")
    return sitemap


README = """# Silica website

The official website for [Silica](https://github.com/sufiyan-sabeel/silica), an
open-source general-purpose programming language created by Umaiz Sufiyan.

Live at **https://sufiyan-sabeel.github.io/silica-website/**

## What this is

A static site: plain HTML, one stylesheet, one small script. No framework, no
bundler, no runtime dependency. It is served by GitHub Pages directly from the
`main` branch, so a push is a deploy.

## Layout

```
index.html              homepage
docs/*.html             eleven documentation pages
assets/css/site.css     the whole design system
assets/js/site.js       theme switch, mobile nav, copy buttons, tabs
assets/img/             logo, mark, icons, social card
sitemap.xml robots.txt  search-engine plumbing
404.html                not-found page
tools/                  the generator that produced the pages above
```

The pages are generated, then committed. `python3 tools/build_site.py`
rewrites them in place from `tools/`, so the repository is both the source and
the published output — which is what GitHub Pages serves.

## Editing

Edit the HTML in place, or regenerate it from the generator that produced it:

```
tools/build_site.py       page chrome, docs layout, sitemap
tools/pages_home.py       homepage sections
tools/pages_docs.py       documentation pages
tools/snippets.py         every code example, in one place
tools/verify_snippets.py  runs each example against the real toolchain
```

Every code example on the site is executed against the Silica implementation
before publication, so the documentation cannot drift from the language.

## Accessibility and performance

Semantic landmarks, a skip link, keyboard-operable tabs, visible focus states,
`prefers-reduced-motion` support, a light and dark theme, no web fonts and no
third-party scripts.

## Licence

The website content is MIT licensed, like Silica itself. Copyright (c) 2026
Umaiz Sufiyan.
"""


def main():
    if not os.path.isdir(os.path.join(OUT, "assets")):
        raise SystemExit("missing assets/ — the stylesheet and images must exist "
                         "before building")
    written = [build_home()]
    written += build_docs()
    written.append(build_404())
    build_seo()
    write("README.md", README)

    total = 0
    for path in written:
        total += os.path.getsize(path)
    print("built %d pages, %.1f KB of HTML" % (len(written), total / 1024.0))
    print("output: %s" % OUT)


if __name__ == "__main__":
    main()
