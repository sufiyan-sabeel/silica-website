"""Validate the generated site: links, assets, metadata, structure.

    python3 tools/check_site.py

Fails loudly on a broken internal link, a missing image, a missing SEO tag, a
stray template placeholder, or unbalanced markup.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = ROOT   # the site is built in place at the repository root

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

REQUIRED_META = [
    ('name="description"', "meta description"),
    ('rel="canonical"', "canonical URL"),
    ('property="og:title"', "Open Graph title"),
    ('property="og:description"', "Open Graph description"),
    ('property="og:image"', "Open Graph image"),
    ('property="og:url"', "Open Graph URL"),
    ('name="twitter:card"', "Twitter card"),
    ('name="twitter:image"', "Twitter image"),
    ('application/ld+json', "structured data"),
]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.images = []
        self.h1 = 0
        self.title = ""
        self._in_title = False
        self.stack = []
        self.errors = []
        self.has_main = False
        self.has_skip = False
        self.img_without_alt = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "img":
            self.images.append(attrs.get("src", ""))
            if attrs.get("alt") is None:
                self.img_without_alt.append(attrs.get("src", ""))
        if tag == "h1":
            self.h1 += 1
        if tag == "main":
            self.has_main = True
        if tag == "a" and "skip-link" in (attrs.get("class") or ""):
            self.has_skip = True
        if tag == "title":
            self._in_title = True
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append("closing </%s> with nothing open" % tag)
            return
        if self.stack[-1] == tag:
            self.stack.pop()
            return
        if tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append("unclosed <%s> before </%s>"
                                   % (self.stack.pop(), tag))
            if self.stack:
                self.stack.pop()
        else:
            self.errors.append("stray </%s>" % tag)

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def main():
    if not os.path.isdir(SITE):
        raise SystemExit("no index.html — run tools/build_site.py first")

    pages = []
    for base, _dirs, files in os.walk(SITE):
        for name in files:
            if name.endswith(".html"):
                pages.append(os.path.join(base, name))

    problems = []
    checked_links = 0

    for path in sorted(pages):
        rel = os.path.relpath(path, SITE)
        raw = open(path, encoding="utf-8").read()
        parser = Page()
        parser.feed(raw)
        parser.close()

        if parser.stack:
            problems.append("%s: unclosed tags at end: %s"
                            % (rel, ", ".join(parser.stack)))
        for error in parser.errors:
            problems.append("%s: %s" % (rel, error))

        if parser.h1 != 1:
            problems.append("%s: expected exactly one <h1>, found %d"
                            % (rel, parser.h1))
        if not parser.title.strip():
            problems.append("%s: empty <title>" % rel)
        if not parser.has_main:
            problems.append("%s: no <main> landmark" % rel)
        if not parser.has_skip:
            problems.append("%s: no skip link" % rel)
        for src in parser.img_without_alt:
            problems.append("%s: <img> without alt: %s" % (rel, src))

        for needle, label in REQUIRED_META:
            if needle not in raw:
                problems.append("%s: missing %s" % (rel, label))

        for placeholder in ("%(", "{{", "}}", "TODO", "Lorem ipsum", "FIXME"):
            if placeholder in raw:
                problems.append("%s: stray placeholder %r" % (rel, placeholder))

        # internal links and images must resolve
        base_dir = os.path.dirname(path)
        for target in parser.links + parser.images:
            if not target or target.startswith(("http://", "https://", "mailto:",
                                                "#", "data:")):
                continue
            parsed = urlparse(target)
            local = parsed.path
            if not local:
                continue
            if local.startswith("/silica-website/"):
                resolved = os.path.normpath(
                    os.path.join(SITE, local[len("/silica-website/"):]))
            else:
                resolved = os.path.normpath(os.path.join(base_dir, local))
            checked_links += 1
            if not os.path.exists(resolved):
                problems.append("%s: broken reference %s" % (rel, target))

    # sitemap
    sitemap = os.path.join(SITE, "sitemap.xml")
    try:
        tree = ET.parse(sitemap)
        urls = [el.text for el in tree.getroot().iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    except Exception as exc:  # noqa: BLE001
        problems.append("sitemap.xml: %s" % exc)
        urls = []

    if len(urls) != len(pages) - 1:  # every page except 404
        problems.append("sitemap.xml lists %d URLs for %d pages"
                        % (len(urls), len(pages) - 1))

    for required in ("robots.txt", ".nojekyll", "assets/css/site.css",
                     "assets/js/site.js", "assets/img/og-cover.jpg"):
        if not os.path.exists(os.path.join(SITE, required)):
            problems.append("missing %s" % required)

    total_bytes = 0
    for base, _dirs, files in os.walk(SITE):
        for name in files:
            total_bytes += os.path.getsize(os.path.join(base, name))

    print("%d pages, %d internal references checked, %.0f KB total"
          % (len(pages), checked_links, total_bytes / 1024.0))
    if problems:
        print("\n%d problem(s):" % len(problems))
        for problem in problems:
            print("  - %s" % problem)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
