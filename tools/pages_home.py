"""Homepage body for the Silica website."""

import html
import json
import os

from site_chrome import (BASE_URL, CREATOR_GITHUB, DOC_PAGES, GITHUB,
                         INSTAGRAM, VERSION, callout, code_block, icon,
                         output_block)
from snippets import SNIPPETS

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "snippet_output.json"), encoding="utf-8") as _fh:
    OUTPUTS = json.load(_fh)


def src(name):
    return SNIPPETS[name]["code"]


def out(name):
    value = OUTPUTS.get(name, {}).get("output")
    return value if value else ""


def hero():
    return """
<section class="hero">
  <div class="wrap">
    <div>
      <div class="hero-mark">
        <img src="assets/img/mark-dark.png" alt="Silica logo" class="logo-dark" width="44" height="56">
        <img src="assets/img/mark-light.png" alt="Silica logo" class="logo-light" width="44" height="56">
        <span>Silica %(version)s · open source · MIT</span>
      </div>
      <h1>Meet Silica.<br>A Language Built to <em>Create.</em></h1>
      <p class="lede">Silica is an open-source, high-level general-purpose
      programming language designed to make writing code feel more natural,
      expressive, and approachable.</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="#what">%(arrow)s Explore Silica</a>
        <a class="btn btn--ghost" href="%(github)s" rel="noopener">%(gh)s View on GitHub</a>
      </div>
      <div class="hero-meta">
        <span class="pill pill--accent"><span class="pill__dot"></span>v%(version)s released</span>
        <span class="pill">Python 3.9+</span>
        <span class="pill">bytecode VM</span>
        <span class="pill">no runtime dependencies</span>
      </div>
    </div>
    <div>
      %(code)s
      %(output)s
    </div>
  </div>
</section>
""" % {
        "version": VERSION,
        "arrow": icon("arrow-right"),
        "gh": icon("github"),
        "github": GITHUB,
        "code": code_block(src("hero"), "hello.sc"),
        "output": output_block(out("hero"), "terminal", "Output"),
    }


def what():
    return """
<section id="what">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">What is Silica</p>
      <h2>A small language with a complete pipeline behind it.</h2>
      <p class="lede">Silica is not a wrapper around another language and not a
      teaching sketch. Source code goes through a lexer, a parser, a static type
      checker, a bytecode compiler, a verifier and a stack virtual machine —
      each stage its own module, each stage testable on its own.</p>
    </div>

    <div class="split">
      <div class="reveal">
        <h3>Why it exists</h3>
        <p>Most of us learn to <em>use</em> programming languages. Silica started
        from the other question: what does it take to build one? It is an
        independent attempt to design a language with its own identity — its own
        keywords, its own type rules, its own bytecode format — rather than
        another layer on top of an existing toolchain.</p>

        <h3>What makes the syntax distinctive</h3>
        <p>Silica does not borrow Python's or JavaScript's keywords. A function is
        <code>sfn</code>, printing is <code>sprint</code>, conditionals are
        <code>si</code> / <code>sino</code>, booleans are <code>oui</code> /
        <code>nein</code>, loops are <code>tant</code> (while) and
        <code>per</code> (for), and logic reads as <code>und</code>,
        <code>ou</code>, <code>non</code>. Braces are mandatory, a newline ends a
        statement, and every block is explicit.</p>

        <h3>Philosophy</h3>
        <p>Check before running, fail with a located diagnostic, and never
        pretend something works. Programs are untrusted by default: the
        capability set starts empty, so a program cannot read a file, open a
        window or use the terminal unless the person running it grants exactly
        that.</p>
      </div>

      <div class="reveal">
        %(pipeline)s
        <div class="grid grid--2" style="margin-top:1rem">
          <div class="card">
            <div class="card__icon">%(cpu)s</div>
            <h3>Checked, then compiled</h3>
            <p>Type errors are reported before any bytecode exists, with the file,
            line and column that caused them.</p>
          </div>
          <div class="card">
            <div class="card__icon">%(shield)s</div>
            <h3>Deny by default</h3>
            <p>Filesystem, terminal and window access each need an explicit
            capability granted on the command line.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid--3" style="margin-top:2.5rem">
      <div class="card reveal">
        <div class="card__icon">%(layers)s</div>
        <h3>Versioned bytecode</h3>
        <p><code>.sbc</code> format 1.0 with a magic number, a CRC-32 and a
        verifier that rejects malformed input before it runs.</p>
      </div>
      <div class="card reveal">
        <div class="card__icon">%(package)s</div>
        <h3>Zero runtime dependencies</h3>
        <p>The language, CLI, standard library, terminal UI and IDE are pure
        Python standard library. Nothing to install but Python.</p>
      </div>
      <div class="card reveal">
        <div class="card__icon">%(file)s</div>
        <h3>Honest documentation</h3>
        <p>Every limitation is written down: no generics, no structs, no
        closures, no network, and it is not fast. The docs say so.</p>
      </div>
    </div>

    <div class="reveal" style="margin-top:2.5rem">
      %(status)s
    </div>
  </div>
</section>
""" % {
        "cpu": icon("cpu"),
        "shield": icon("shield"),
        "layers": icon("layers"),
        "package": icon("package"),
        "file": icon("file-text"),
        "pipeline": code_block(
            "source .sc\n"
            "  \u2192 lexer        tokens + comments\n"
            "  \u2192 parser       AST\n"
            "  \u2192 checker      names, scopes, arities, static types\n"
            "  \u2192 compiler     bytecode chunk\n"
            "  \u2192 verifier     magic, CRC-32, jump targets, stack discipline\n"
            "  \u2192 vm           stack machine, explicit call frames",
            "pipeline.txt", show_copy=False, label="The pipeline"),
        "status": callout(
            "<strong>Current status: v%s, an early release.</strong> The language, "
            "compiler, bytecode format and core standard library are implemented "
            "and tested. Silica is <em>not</em> production-ready, <em>not</em> "
            "self-hosting, and <em>not</em> faster than Python — the VM is a "
            "Python loop. See the <a href=\"#roadmap\">roadmap</a> and the "
            "<a href=\"docs/faq.html\">FAQ</a>." % VERSION,
            kind="warn",
        ),
    }


def story():
    return """
<section id="story" style="border-top:1px solid var(--border-soft)">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Why I built Silica</p>
        <h2>A journey of building something from an idea.</h2>
        <blockquote class="quote">Instead of only learning how to use
        programming languages, I wanted to understand how to build one.</blockquote>
      </div>
      <div class="story reveal">
        <p>I built Silica because I wanted to explore programming beyond simply
        using existing languages.</p>
        <p>As a student and developer, I became interested in how programming
        languages work internally: how code is written, interpreted, executed,
        and transformed into something a computer can understand.</p>
        <p>Instead of only learning how to use programming languages, I wanted to
        understand how to build one. That curiosity became Silica.</p>
        <p>I started this project with the ambition to create a language with its
        own identity, syntax, tools, and ecosystem. I wanted to experiment, solve
        real development challenges, and learn the engineering behind language
        design.</p>
        <p>Silica is not just a coding project for me. It represents curiosity,
        experimentation, independent learning, and the belief that developers can
        create their own tools instead of always depending on existing ones.</p>
        <p>I am continuously learning, improving, testing, and developing Silica
        as an open-source project. This is a journey of building something from an
        idea.</p>
        <div class="signature">
          <img src="assets/img/mark-dark.png" alt="" class="logo-dark" width="40" height="51">
          <img src="assets/img/mark-light.png" alt="" class="logo-light" width="40" height="51">
          <p><strong>Umaiz Sufiyan</strong>Creator of Silica</p>
        </div>
      </div>
    </div>
  </div>
</section>
"""


def features():
    implemented = [
        ("Functions with typed parameters and return types",
         "<code>sfn add(a: Int, b: Int) -&gt; Int</code>, recursion, and a checker that "
         "requires a return on every path."),
        ("Variables and constants",
         "<code>let</code> is mutable, <code>const</code> is not, and locals are "
         "type-inferred from their initialiser."),
        ("Conditionals and logic",
         "<code>si</code> / <code>sino</code> with short-circuit <code>und</code>, "
         "<code>ou</code> and <code>non</code>."),
        ("Loops with control transfer",
         "<code>tant</code> (while), <code>per ... in ...</code> (for) over lists, "
         "maps and ranges, plus <code>break</code> and <code>continue</code>."),
        ("Strings in four delimiter forms",
         "single, double, and both triple-quoted forms; escapes including "
         "<code>\\uXXXX</code>; indexing and concatenation."),
        ("Lists and maps",
         "Literals, indexing, <code>len</code>, <code>push</code>, "
         "<code>keys</code>, <code>values</code>, <code>has</code>, and structural "
         "equality."),
        ("Static type checking",
         "Eight types — Int, Float, Bool, String, Unit, List, Map, Any — checked "
         "before anything runs."),
        ("Bytecode compilation and verification",
         "Compile to <code>.sbc</code>, run it later, and trust the verifier to "
         "reject malformed files."),
        ("Capability-based security",
         "Filesystem, terminal, GUI and speech access are granted per root path, "
         "and denied by default."),
        ("Standard library",
         "<code>core</code>, <code>math</code>, <code>string</code>, "
         "<code>collections</code>, <code>json</code> and a capability-gated "
         "<code>fs</code>."),
        ("Toolchain",
         "<code>run</code>, <code>check</code>, <code>compile</code>, "
         "<code>repl</code>, <code>fmt</code>, <code>test</code>, "
         "<code>capabilities</code> and an in-browser Script Mode IDE."),
        ("Interfaces beyond the terminal",
         "A declarative web UI DSL that renders to HTML, a curses terminal UI, and "
         "desktop windows through tkinter."),
    ]

    partial = [
        ("Web UI DSL",
         "Shipped in 0.2.0 with a node tree, themes, breakpoints and events. Other "
         "renderers (Android, iOS, desktop, OS-UI) are specified but not built."),
        ("Terminal and desktop UI",
         "Working, but covered by unit tests rather than by a real terminal or "
         "display in CI."),
        ("Speech and voice",
         "Needs extra packages (<code>numpy</code>, <code>onnxruntime</code>) plus "
         "downloaded models; it is not part of the core install."),
        ("Constant folding optimiser",
         "One measured optimisation. <code>SILICA_NO_OPT=1</code> turns it off; it "
         "is not a general optimiser."),
        ("Script Mode IDE",
         "Edit, save and run real scripts with clickable errors. No search and "
         "replace, folding or autocomplete yet."),
        ("Termux support",
         "The installer's Termux path is tested with Termux's environment "
         "variables, but has not been run on a real device."),
    ]

    planned = [
        ("Generics", "Type parameters, constraints and generic collections. Today "
                     "<code>List</code> and <code>Map</code> elements check as "
                     "<code>Any</code>."),
        ("Structs and classes", "No user-defined types yet; there are no fields, "
                                "methods or constructors."),
        ("First-class functions and closures", "Functions can be called, not "
                                               "passed around."),
        ("Enums and pattern matching", "On the roadmap, not implemented."),
        ("A Result / error type", "Errors abort the program; there is no "
                                  "recoverable error value and no exceptions."),
        ("Package manager", "<code>silica new</code>, <code>add</code>, "
                            "<code>install</code> and <code>build</code> are not "
                            "implemented and say so."),
        ("Networking", "<code>net</code>, <code>http</code> and <code>crypto</code> "
                       "are refused at compile time."),
        ("Concurrency", "No threads, no async, no scheduler in the VM."),
        ("Language server and debugger", "Planned; today there is syntax "
                                         "highlighting for VS Code only."),
        ("Self-hosting and a Rust port", "Silica does not compile itself, and the "
                                         "engine is Python."),
    ]

    def rows(items):
        return "".join(
            '<li><div><strong>%s</strong><span>%s</span></div></li>' % (title, body)
            for title, body in items
        )

    return """
<section id="features" style="border-top:1px solid var(--border-soft);background:var(--bg-elev)">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Language features</p>
      <h2>What is implemented, what is partial, and what is planned.</h2>
      <p class="lede">This list was compiled by reading the v%(version)s source and
      running the test suite. Nothing here is presented as working unless it runs
      today.</p>
    </div>

    <div class="feature-group reveal">
      <h3>Implemented and tested <span class="status status--done">%(check)s shipped</span></h3>
      <ul class="feature-list">%(implemented)s</ul>
    </div>

    <div class="feature-group reveal">
      <h3>Implemented with limits <span class="status status--partial">partial</span></h3>
      <ul class="feature-list">%(partial)s</ul>
    </div>

    <div class="feature-group reveal">
      <h3>Planned, not built <span class="status status--planned">not yet</span></h3>
      <ul class="feature-list">%(planned)s</ul>
    </div>
  </div>
</section>
""" % {
        "version": VERSION,
        "check": icon("check"),
        "implemented": rows(implemented),
        "partial": rows(partial),
        "planned": rows(planned),
    }


def playground():
    tabs = [
        ("hello", "Hello World", "hello.sc"),
        ("variables", "Variables", "variables.sc"),
        ("functions", "Functions", "functions.sc"),
        ("conditions", "Conditions", "conditionals.sc"),
        ("loops", "Loops", "loops.sc"),
        ("strings", "Strings", "strings.sc"),
    ]

    buttons = []
    panels = []
    for index, (name, label, filename) in enumerate(tabs):
        selected = index == 0
        buttons.append(
            '<button class="tab" type="button" role="tab" id="tab-%s" '
            'aria-controls="panel-%s" aria-selected="%s" tabindex="%s">%s</button>'
            % (name, name, "true" if selected else "false",
               "0" if selected else "-1", label)
        )
        panels.append(
            '<div class="tabpanel" role="tabpanel" id="panel-%s" '
            'aria-labelledby="tab-%s"%s>\n%s\n%s\n</div>'
            % (name, name, "" if selected else " hidden",
               code_block(src(name), filename),
               output_block(out(name), "output", "Output"))
        )

    return """
<section id="playground" style="border-top:1px solid var(--border-soft)">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Code playground</p>
      <h2>Real Silica programs, and what they actually print.</h2>
      <p class="lede">Every example below is a complete program from the
      repository, run against v%(version)s. The output under each one is the real
      output, not an illustration.</p>
    </div>

    <div data-tabs>
      <div class="tabs" role="tablist" aria-label="Silica examples">
        %(buttons)s
      </div>
      %(panels)s
    </div>

    <p class="playground-note">%(info)s
      <span>There is no browser-based Silica runtime, so these panels do not
      execute. To run any of them, save the file and use
      <code>silica run hello.sc</code> — see
      <a href="docs/getting-started.html">Getting Started</a>.</span>
    </p>
  </div>
</section>
""" % {
        "version": VERSION,
        "buttons": "\n        ".join(buttons),
        "panels": "\n      ".join(panels),
        "info": icon("info"),
    }


def install():
    return """
<section id="install" style="border-top:1px solid var(--border-soft);background:var(--bg-elev)">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Installation</p>
        <h2>One command, and a checksum that must match.</h2>
        <p class="lede">Silica is a Python package with no runtime dependencies.
        The installer downloads the release wheel, verifies its SHA-256, and puts
        it in an isolated virtual environment under your home directory.</p>

        <div class="terminal" style="margin-top:1.75rem">
          <div class="terminal__bar"><span>bash</span></div>
          <pre><span class="prompt">$</span> curl -fsSL https://raw.githubusercontent.com/sufiyan-sabeel/silica/main/install.sh | sh
<span class="comment"># then</span>
<span class="prompt">$</span> silica --version
silica %(version)s
<span class="prompt">$</span> silica run examples/hello.sc
Hello from Silica</pre>
        </div>

        <div class="btn-row">
          <a class="btn btn--ghost" href="docs/installation.html">%(book)s All install options</a>
        </div>
      </div>

      <div class="reveal">
        <div class="grid grid--2">
          <div class="card">
            <h3>Requirements</h3>
            <p>Python 3.9 or newer. Nothing else for the core language — no
            compiled extensions, no third-party packages.</p>
          </div>
          <div class="card">
            <h3>Upgrade or pin</h3>
            <p><code>SILICA_VERSION=%(version)s sh install.sh</code> installs or
            rolls back to a specific published release.</p>
          </div>
          <div class="card">
            <h3>Termux</h3>
            <p><code>pkg install python git curl</code>, then the same installer.
            The launcher lands in <code>$PREFIX/bin</code>.</p>
          </div>
          <div class="card">
            <h3>From source</h3>
            <p><code>git clone</code>, then
            <code>python3 -m silica examples/hello.sc</code> — no install at
            all.</p>
          </div>
        </div>

        <div style="margin-top:1rem">
          %(trouble)s
        </div>
      </div>
    </div>
  </div>
</section>
""" % {
        "version": VERSION,
        "book": icon("book"),
        "trouble": callout(
            "<strong><code>silica: command not found</code></strong> — the "
            "installer prints the exact line to add. In short: "
            "<code>export PATH=\"$HOME/.local/bin:$PATH\"</code>. Full "
            "troubleshooting is in <a href=\"docs/installation.html\">Installation</a>.",
        ),
    }


def docs_section():
    cards = []
    icons = ["compass", "terminal", "code", "layers", "git-branch", "zap",
             "file-text", "package", "terminal", "book", "info"]
    for index, (slug, label, description) in enumerate(DOC_PAGES):
        cards.append(
            '<a class="card reveal" href="docs/%s.html" style="text-decoration:none">'
            '<div class="card__icon">%s</div>'
            "<h3>%s</h3><p>%s</p></a>"
            % (slug, icon(icons[index % len(icons)]), label, description)
        )

    return """
<section id="docs" style="border-top:1px solid var(--border-soft)">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Documentation</p>
      <h2>Everything written down, checked against the parser.</h2>
      <p class="lede">The documentation is written from the implementation and
      tested: every code example on this site is run against the real Silica
      toolchain before it is published.</p>
    </div>
    <div class="grid grid--3">
      %(cards)s
    </div>
  </div>
</section>
""" % {"cards": "\n      ".join(cards)}


def roadmap():
    items = [
        ("done", "Milestone A — front end",
         "Lexer with source locations, AST, recursive-descent parser, located "
         "diagnostics, integers, strings, <code>let</code>/<code>const</code>, "
         "<code>sprint</code>, <code>sfn</code>, <code>ret</code>."),
        ("done", "Milestone B — semantics and engine",
         "Scopes and symbol resolution, static type checker with inference, "
         "conditionals, short-circuit logic, loops, functions and recursion, "
         "bytecode compiler and stack VM."),
        ("done", "Milestone C — CLI, bytecode, tests, docs",
         "The command set, the versioned <code>.sbc</code> format with CRC-32, the "
         "bytecode verifier, the REPL, the formatter, examples and the "
         "documentation set."),
        ("done", "Milestone D — standard library (partly)",
         "<code>core</code>, <code>math</code>, <code>string</code>, "
         "<code>collections</code>, the capability model, <code>fs</code> and "
         "<code>json</code>. Still missing: <code>path</code>, <code>time</code>, "
         "<code>random</code>, <code>regex</code>, <code>log</code>."),
        ("done", "Milestone F — Silica UI (web renderer only)",
         "The web UI DSL, themes with WCAG contrast validation, responsive "
         "breakpoints, scrolling, sticky headers and animations. Other renderers "
         "are not built; self-hosting has not started."),
        ("done", "Milestone G — loop control (0.9.0)",
         "<code>break</code> and <code>continue</code> compiled to jumps, with no "
         "new opcode and no change to the <code>.sbc</code> format."),
        ("next", "Milestone E — packaging and release engineering",
         "<code>silica new / add / remove / install / build</code> with lockfiles "
         "and checksums, a package registry, release artifacts and, eventually, a "
         "Rust port of the engine. Not started."),
    ]

    rows = []
    for state, title, body in items:
        badge = ""
        if state == "done":
            badge = '<span class="status status--done">done</span>'
        else:
            badge = '<span class="status status--planned">not started</span>'
        rows.append(
            '<li data-state="%s"><h3>%s %s</h3><p>%s</p></li>'
            % (state, title, badge, body)
        )

    return """
<section id="roadmap" style="border-top:1px solid var(--border-soft);background:var(--bg-elev)">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Roadmap</p>
      <h2>Current functionality, and what is still ambition.</h2>
      <p class="lede">Taken from the repository's own roadmap. "Done" means
      implemented, tested and documented in the repository — nothing here is
      aspirational.</p>
    </div>

    <div class="split">
      <ul class="timeline reveal">
        %(rows)s
      </ul>
      <div class="reveal">
        <div class="card">
          <h3>Known limitations in v%(version)s</h3>
          <p>No generics — <code>List</code> and <code>Map</code> elements check as
          <code>Any</code>. No first-class functions, closures, methods or
          user-defined types. No exceptions. <code>per</code> loop variables are
          immutable. No negative indexing and no element assignment. No labelled
          <code>break</code>. The REPL recompiles each entry from scratch. The
          formatter refuses files with comments.</p>
        </div>
        <div class="card" style="margin-top:1rem">
          <h3>Performance, stated plainly</h3>
          <p>On the repository's four benchmarks, Silica ran 38–101× slower than
          CPython when measured on 2026-10-28 (Linux x86_64, CPython 3.12.13,
          Silica %(version)s), because the VM is a Python loop. Constant folding
          cut one hot loop by 39%%.</p>
        </div>
        <div style="margin-top:1rem">
          <a class="btn btn--ghost btn--sm" href="%(github)s/blob/main/docs/ROADMAP.md" rel="noopener">%(branch)s Full roadmap</a>
        </div>
      </div>
    </div>
  </div>
</section>
""" % {
        "rows": "\n        ".join(rows),
        "version": VERSION,
        "github": GITHUB,
        "branch": icon("git-branch"),
    }


def creator():
    return """
<section id="creator" style="border-top:1px solid var(--border-soft)">
  <div class="wrap">
    <div class="creator reveal">
      <div class="creator-grid">
        <div>
          <p class="eyebrow">Meet the creator</p>
          <h2>Umaiz Sufiyan</h2>
          <p class="muted" style="margin-bottom:1rem">Student Developer and
          Creator of Silica</p>
          <p>Umaiz Sufiyan is an independent student developer interested in
          programming languages, software engineering, developer tools, and
          artificial intelligence. Silica is one of his efforts to explore
          language design and build something of his own.</p>
          <div class="creator-links">
            <a href="%(creator)s" rel="noopener">%(user)s GitHub</a>
            <a href="%(github)s" rel="noopener">%(gh)s Silica repository</a>
            <a href="%(instagram)s" rel="noopener">%(ig)s Instagram</a>
          </div>
          <p class="attribution">Designed and developed with curiosity by Umaiz
          Sufiyan.</p>
        </div>
        <div>
          %(card)s
        </div>
      </div>
    </div>
  </div>
</section>
""" % {
        "creator": CREATOR_GITHUB,
        "github": GITHUB,
        "instagram": INSTAGRAM,
        "user": icon("user"),
        "gh": icon("github"),
        "ig": icon("instagram"),
        "card": code_block(src("creator_card"), "creator.sc", show_copy=False),
    }


def body():
    return "".join([
        hero(), what(), story(), features(), playground(), install(),
        docs_section(), roadmap(), creator(),
    ])
