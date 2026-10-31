# Silica website

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
