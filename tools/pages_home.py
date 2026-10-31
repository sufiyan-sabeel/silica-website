"""Homepage body for the Silica website."""

import html
import json
import os

import crystal_svg
from site_chrome import (BASE_URL, BUILT, CREATOR_GITHUB, DOC_PAGES, GITHUB,
                         INSTAGRAM, LICENSE, RELEASE, STATUS, VERSION, callout,
                         code_block, icon, output_block)
from snippets import SNIPPETS

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "snippet_output.json"), encoding="utf-8") as _fh:
    OUTPUTS = json.load(_fh)

STARS = STATUS.get("stars", 0)
FORKS = STATUS.get("forks", 0)
ISSUES = STATUS.get("open_issues", 0)
PUSHED = (STATUS.get("pushed_at") or BUILT)[:10]
LAST_COMMIT = STATUS.get("last_commit") or {}
RELEASES = STATUS.get("releases") or []


def src(name):
    return SNIPPETS[name]["code"]


def out(name):
    return OUTPUTS.get(name, {}).get("output") or ""


def hero():
    return """
<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <p class="hero-label">
        <img src="assets/img/mark-dark.png" alt="" class="logo-dark" width="18" height="23">
        <img src="assets/img/mark-light.png" alt="" class="logo-light" width="18" height="23">
        Open-source programming language
      </p>
      <h1>A Language Built to <em>Create.</em></h1>
      <p class="lede">Meet Silica — a modern, high-level, general-purpose programming
      language built around expressive syntax, practical development, and the
      freedom to create.</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="#overview">%(arrow)s Explore Silica</a>
        <a class="btn btn--ghost" href="%(github)s" rel="noopener">%(gh)s View GitHub</a>
      </div>
      <div class="hero-meta">
        <span class="pill pill--accent"><span class="pill__dot"></span>%(release)s released</span>
        <span class="pill">Python 3.9+</span>
        <span class="pill">bytecode VM</span>
        <span class="pill">no runtime dependencies</span>
      </div>
    </div>

    <div>
      <div class="stage" data-stage>
        <div class="stage__frame"></div>
        %(crystal)s
        <canvas width="720" height="720" aria-hidden="true"></canvas>
        <p class="stage__caption">Rendered live · no model files</p>
      </div>
    </div>
  </div>
</section>

<div class="status-strip" data-repo-status data-built="%(built)s">
  <div class="wrap status-strip__inner">
    <span class="status-strip__label"><span class="status-dot"></span>Repository</span>
    <ul class="status-grid">
      <li>%(star)s <strong data-repo="stars">%(stars)s</strong> %(star_word)s</li>
      <li>%(branch)s <strong data-repo="forks">%(forks)s</strong> %(fork_word)s</li>
      <li>%(issues)s <strong data-repo="issues">%(issues_count)s</strong> %(issue_word)s</li>
      <li>latest release <a data-repo="release-link" href="%(github)s/releases"><strong data-repo="release">%(release)s</strong></a></li>
      <li>last push <strong data-repo="updated">%(pushed)s</strong></li>
    </ul>
    <span class="status-strip__time" data-status-time>as of %(built)s</span>
  </div>
</div>
""" % {
        "arrow": icon("arrow-right"),
        "gh": icon("github"),
        "github": GITHUB,
        "release": RELEASE,
        "crystal": crystal_svg.build(),
        "built": BUILT,
        "stars": STARS,
        "forks": FORKS,
        "issues_count": ISSUES,
        "pushed": PUSHED,
        "star_word": "star" if STARS == 1 else "stars",
        "fork_word": "fork" if FORKS == 1 else "forks",
        "issue_word": "open issue" if ISSUES == 1 else "open issues",
        "star": icon("star"),
        "branch": icon("git-branch"),
        "issues": icon("git-commit"),
    }


def overview():
    return """
<section id="overview">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Overview</p>
      <h2>More Than Just Another Language.</h2>
      <p class="lede">Silica is not a wrapper around another runtime and not a
      teaching sketch. Source code goes through a lexer, a parser, a static type
      checker, a bytecode compiler, a verifier and a stack virtual machine — each
      stage its own module, each stage testable on its own.</p>
    </div>

    <div class="split">
      <div class="reveal">
        <h3>What it is</h3>
        <p>A general-purpose language implemented in Python, with its own keywords
        rather than Python's: <code>sfn</code> for a function, <code>sprint</code>
        to print, <code>si</code>/<code>sino</code> for if/else,
        <code>oui</code>/<code>nein</code> for true/false, <code>tant</code> and
        <code>per</code> for loops, <code>struct</code> for records.</p>

        <h3>Why it exists</h3>
        <p>Most of us learn to use programming languages. Silica started from the
        other question: what does it take to build one? It is an independent
        attempt to design a language with its own identity — its own keywords, its
        own type rules, its own bytecode format — rather than another layer on an
        existing toolchain.</p>

        <h3>The philosophy</h3>
        <p>Check before running, fail with a located diagnostic, and never pretend
        something works. Programs are untrusted by default: the capability set
        starts empty, so a program cannot read a file, open a window or use the
        terminal unless the person running it grants exactly that.</p>

        <h3>Where it stands</h3>
        <p>%(release)s is an early release with a complete toolchain, a real
        standard library and a test suite of 900+ tests. It is not production-ready,
        not self-hosting, and not fast — the VM is a Python loop. The
        <a href="docs/faq.html">FAQ</a> says so plainly.</p>
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
          <div class="card">
            <div class="card__icon">%(layers)s</div>
            <h3>Versioned bytecode</h3>
            <p><code>.sbc</code> carries a magic number, a CRC-32 and a verifier
            that rejects malformed input before it runs.</p>
          </div>
          <div class="card">
            <div class="card__icon">%(package)s</div>
            <h3>Zero runtime dependencies</h3>
            <p>The language, CLI, standard library, terminal UI and IDE are pure
            Python standard library.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
""" % {
        "release": RELEASE,
        "cpu": icon("cpu"),
        "shield": icon("shield"),
        "layers": icon("layers"),
        "package": icon("package"),
        "pipeline": code_block(
            "source .sc\n"
            "  → lexer        tokens + comments\n"
            "  → parser       AST\n"
            "  → checker      names, scopes, arities, types\n"
            "  → compiler     bytecode chunk\n"
            "  → verifier     magic, CRC-32, jumps, stack discipline\n"
            "  → vm           stack machine, explicit call frames",
            "pipeline.txt", show_copy=False, label="The pipeline",
            line_numbers=False),
    }


def features():
    rows = []

    rows.append("""
    <div class="feature-row reveal">
      <div class="feature-row__text">
        <div class="feature-row__tags"><span class="tag tag--new">new in 0.9.2</span><span class="tag">structs</span></div>
        <h3>Records with typed fields.</h3>
        <p>A struct is a named record with checked fields. Construct it by name or
        by position, read and write fields at any depth, compare by value, and
        print it as it is written. <code>const</code> freezes the whole tree.</p>
        <a class="card__more" href="docs/structs.html">Structs in the documentation %s</a>
      </div>
      <div>%s%s</div>
    </div>""" % (icon("arrow-right"),
                 code_block(src("struct_basic"), "structs.sc"),
                 output_block(out("struct_basic"))))

    rows.append("""
    <div class="feature-row feature-row--flip reveal">
      <div class="feature-row__text">
        <div class="feature-row__tags"><span class="tag tag--new">new in 0.9.1</span><span class="tag">use colors</span></div>
        <h3>A colour system that does not clip.</h3>
        <p>OKLab, OKLCH and Display P3 with real gamut mapping: ask for a teal sRGB
        cannot show and it comes back at a chroma it can, not silently shifted.
        Palettes, themes, WCAG audits and CSS output are part of the same
        29-function module.</p>
        <a class="card__more" href="docs/built-in-functions.html#colors">The colours module %s</a>
      </div>
      <div>%s%s</div>
    </div>""" % (icon("arrow-right"),
                 code_block(src("colors_demo"), "colors.sc"),
                 output_block(out("colors_demo"))))

    rows.append("""
    <div class="feature-row reveal">
      <div class="feature-row__text">
        <div class="feature-row__tags"><span class="tag">types</span><span class="tag">diagnostics</span></div>
        <h3>Checked before anything runs.</h3>
        <p>Eight built-in types plus your struct names, checked at every call
        site. A wrong argument, a missing field or a bad conversion is a compile
        error with a hint, not a surprise at runtime.</p>
        <a class="card__more" href="docs/variables-and-data-types.html">Types and inference %s</a>
      </div>
      <div>%s</div>
    </div>""" % (icon("arrow-right"),
                 code_block(
                     "sfn add(a: Int, b: Int) -> Int {\n"
                     "    ret a + b\n"
                     "}\n"
                     "\n"
                     "sfn main() {\n"
                     "    sprint(add(1))\n"
                     "}",
                     "arity.sc") +
                 output_block("app.sc:5:15: type error: function 'add' expects "
                              "2 argument(s) but got 1",
                              "diagnostic", "The compiler's answer")))

    rows.append("""
    <div class="feature-row feature-row--flip reveal">
      <div class="feature-row__text">
        <div class="feature-row__tags"><span class="tag">control flow</span><span class="tag">recursion</span></div>
        <h3>Loops, logic and recursion in Silica's own words.</h3>
        <p><code>si</code>/<code>sino</code>, <code>tant</code>,
        <code>per … in …</code>, <code>break</code> and <code>continue</code>,
        with short-circuit <code>und</code>, <code>ou</code> and
        <code>non</code>. Calls use explicit VM frames, so recursion is bounded by
        the frame budget, not the host stack.</p>
        <a class="card__more" href="docs/control-flow.html">Control flow %s</a>
      </div>
      <div>%s%s</div>
    </div>""" % (icon("arrow-right"),
                 code_block(src("loop_control"), "loop_control.sc"),
                 output_block(out("loop_control"))))

    rows.append("""
    <div class="feature-row reveal">
      <div class="feature-row__text">
        <div class="feature-row__tags"><span class="tag">security</span><span class="tag">capabilities</span></div>
        <h3>Nothing is granted by default.</h3>
        <p>A Silica program starts with an empty capability set. Reading a file,
        writing one, using the terminal or opening a window each need an explicit
        grant, scoped to a directory, enforced at the VM's native dispatch point
        before any function body runs.</p>
        <a class="card__more" href="docs/cli-reference.html#flags">Capability flags %s</a>
      </div>
      <div>%s</div>
    </div>""" % (icon("arrow-right"),
                 code_block(
                     "$ silica run app.sc --allow-fs-read ./data\n"
                     "\n"
                     "# without the grant:\n"
                     "capability error: 'fs.read' is not granted\n"
                     "  hint: run with --allow-fs-read DIR",
                     "bash", label="Capabilities are granted outside the program",
                     line_numbers=False)))

    return """
<section id="features" class="section--alt">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Language features</p>
      <h2>What is implemented, with the code that proves it.</h2>
      <p class="lede">Every example on this page was executed against %(release)s
      before publication. Nothing here is a mock-up, and nothing unimplemented is
      advertised.</p>
    </div>
    %(rows)s
  </div>
</section>
""" % {"release": RELEASE, "rows": "".join(rows)}


def playground():
    tabs = [
        ("hello", "Hello World", "hello.sc"),
        ("variables", "Variables", "variables.sc"),
        ("functions", "Functions", "functions.sc"),
        ("conditions", "Conditions", "conditionals.sc"),
        ("loops", "Loops", "loops.sc"),
        ("strings", "Strings", "strings.sc"),
        ("struct_basic", "Structs", "structs.sc"),
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
<section id="playground">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Playground</p>
      <h2>Seven programs, and what they actually print.</h2>
      <p class="lede">Switch between them. Each is a complete file, run against
      %(release)s, and the output under each one is the real output.</p>
    </div>

    <div data-tabs>
      <div class="tabs" role="tablist" aria-label="Silica examples">
        %(buttons)s
      </div>
      %(panels)s
    </div>

    <p class="playground-note">%(info)s
      <span>There is no browser-based Silica runtime, so these panels do not
      execute. Save a file and run <code>silica run hello.sc</code> — see
      <a href="docs/getting-started.html">Getting Started</a>.</span>
    </p>
  </div>
</section>
""" % {
        "release": RELEASE,
        "buttons": "\n        ".join(buttons),
        "panels": "\n      ".join(panels),
        "info": icon("info"),
    }


def story():
    return """
<section id="story" class="section--alt">
  <div class="wrap">
    <div class="story">
      <div class="story__aside reveal">
        <p class="eyebrow">Why I built Silica</p>
        <h2>Built From Curiosity.<br>Driven By Creation.</h2>
        <img class="story__mark logo-dark" src="assets/img/mark-dark.png" alt="" width="46" height="59">
        <img class="story__mark logo-light" src="assets/img/mark-light.png" alt="" width="46" height="59">
        <ol class="story__timeline">
          <li><strong>Curiosity</strong>Wanting to know what happens underneath the code.</li>
          <li><strong>Experiment</strong>Syntax, interpreters, runtime architecture, tooling.</li>
          <li><strong>Identity</strong>A language with its own keywords, bytecode and ecosystem.</li>
          <li><strong>Today</strong>%(release)s — an open-source project still being built.</li>
        </ol>
        <div class="signature">
          <img src="assets/img/mark-dark.png" alt="" class="logo-dark" width="32" height="41">
          <img src="assets/img/mark-light.png" alt="" class="logo-light" width="32" height="41">
          <p><strong>Umaiz Sufiyan</strong>Creator of Silica</p>
        </div>
      </div>

      <div class="story__body reveal">
        <p>I started building Silica because I wanted to understand programming at
        a deeper level.</p>
        <p>Learning how to write software was only the beginning. I became curious
        about what happens underneath the code — how programming languages are
        designed, how syntax is interpreted, how execution works, and how
        developers build the tools they use every day.</p>
        <p>I did not want to limit myself to simply using existing programming
        languages. I wanted to explore what it takes to create one.</p>
        <p>That curiosity became Silica.</p>
        <p>I began experimenting with language design, syntax, interpreters,
        runtime architecture, and developer tooling.</p>
        <p>My goal was to build an independent programming language with its own
        identity and ecosystem — something that I could continuously improve,
        experiment with, and share with the developer community.</p>
        <p>Silica is an ongoing journey of learning, engineering, experimentation,
        and creation.</p>
        <p>I believe that curiosity can turn an idea into something real.</p>
        <p>And Silica is my way of proving that.</p>
      </div>
    </div>
  </div>
</section>
""" % {"release": RELEASE}


def architecture():
    stages = [
        ("lexer.py", "Source text becomes tokens with line and column, plus the comments the formatter keeps."),
        ("parser.py", "Recursive descent into an AST. Blocks are braced; a newline ends a statement."),
        ("checker.py", "Scopes, arities, struct fields and static types, with a hint attached to every error."),
        ("compiler.py", "AST to bytecode: locals in numbered slots, jumps patched to absolute offsets."),
        ("bytecode.py", "The .sbc container — magic, version, CRC-32, constant pool, line table — and its verifier."),
        ("vm.py", "A stack machine with explicit call frames, so recursion is bounded by frames, not the host stack."),
    ]
    arrows = ""
    for name, desc in stages:
        arrows += (
            '<div class="arch__stage"><span class="arch__name">%s</span>'
            '<span class="arch__desc">%s</span></div>' % (name, desc)
        )
        arrows += '<div class="arch__arrow">%s</div>' % icon("chevron-down")

    return """
<section id="architecture">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Architecture</p>
        <h2>How the implementation actually works.</h2>
        <p class="lede">Six stages, one direction, no hidden re-parsing at run
        time. Each module is testable on its own, and the bytecode format is
        versioned so a compiled file can be checked before it executes.</p>

        <h3>Around the core</h3>
        <ul>
          <li><code>natives.py</code> — the standard library registry: 25 modules,
          each native declaring the types the checker needs.</li>
          <li><code>capabilities.py</code> — grants, roots and path containment,
          enforced before a native body runs.</li>
          <li><code>optimizer.py</code> — compile-time constant folding
          (<code>SILICA_NO_OPT=1</code> disables it).</li>
          <li><code>cli.py</code> — <code>run</code>, <code>check</code>,
          <code>compile</code>, <code>repl</code>, <code>fmt</code>,
          <code>test</code>, <code>ide</code>, <code>capabilities</code>.</li>
          <li><code>ui/</code>, <code>tui/</code>, <code>gui/</code> — three
          renderers over one theme model.</li>
        </ul>
        <p class="faint small">There is no Rust port, no self-hosting compiler and
        no package manager yet. Those are roadmap items, not shipped features.</p>
      </div>

      <div class="reveal">
        <div class="arch">
          <div class="arch__flow">%(stages)s</div>
          <p class="arch__note">Source <code>.sc</code> → tokens → AST → checked
          tree → chunk → verified <code>.sbc</code> → execution.</p>
        </div>
      </div>
    </div>
  </div>
</section>
""" % {"stages": arrows}


def install():
    return """
<section id="install" class="section--alt">
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
            <h3>Pin a version</h3>
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
            <code>python3 -m silica examples/hello.sc</code> — no install at all.</p>
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
            "troubleshooting is in <a href=\"docs/installation.html\">Installation</a>."
        ),
    }


def docs_section():
    icons = ["compass", "rocket", "terminal", "code", "layers", "braces", "git-branch",
             "file-text", "box", "package", "terminal", "book", "info"]
    cards = []
    for index, (slug, label, description) in enumerate(DOC_PAGES):
        cards.append(
            '<a class="card card--link reveal" href="docs/%s.html">'
            '<div class="card__icon">%s</div>'
            "<h3>%s</h3><p>%s</p>"
            '<span class="card__more">Read %s</span></a>'
            % (slug, icon(icons[index % len(icons)]), label, description,
               icon("arrow-right"))
        )

    return """
<section id="docs">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Documentation</p>
      <h2>Thirteen pages, checked against the parser.</h2>
      <p class="lede">Searchable, with a table of contents on every page, and every
      code example executed against the current release before publication.</p>
    </div>
    <div class="grid grid--3">
      %(cards)s
    </div>
  </div>
</section>
""" % {"cards": "\n      ".join(cards)}


def roadmap():
    columns = [
        ("done", "Implemented", "shipped", [
            "Lexer, parser, AST, type checker",
            "Bytecode compiler, verifier, stack VM",
            "Functions, loops, <code>break</code>/<code>continue</code>",
            "Lists, maps, strings in four delimiter forms",
            "Structs with typed fields (0.9.2)",
            "Capability model with <code>fs</code>",
            "Perceptual colour system (0.9.1)",
            "Terminal UI, desktop GUI, web UI DSL",
            "Script Mode IDE, REPL, formatter, test runner",
        ]),
        ("active", "In development", "unreleased", [
            "Voice profiles and consent records",
            "Colour wired into the TUI and GUI",
            "Bug-fix passes on published wheels",
        ]),
        ("planned", "Planned", "not started", [
            "Generics with real type parameters",
            "Methods and inheritance",
            "Enums and pattern matching",
            "<code>net</code>, <code>http</code>, <code>crypto</code>",
            "Package manager (<code>new</code>, <code>add</code>, <code>build</code>)",
            "Language server and debugger",
            "Self-hosting compiler",
        ]),
        ("experimental", "Experimental", "limited", [
            "Speech and voice (needs models)",
            "Termux path (tested, not run on a device)",
            "Constant folding only — no other optimiser",
            "Script Mode IDE without search or folding",
            "Web UI DSL: one renderer of several planned",
        ]),
    ]

    cols = []
    for state, title, meta, items in columns:
        lis = "".join("<li>%s</li>" % item for item in items)
        cols.append(
            '<div class="roadmap__col" data-state="%s">'
            '<div class="roadmap__head"><h3>%s</h3>'
            '<span class="roadmap__meta">%s</span></div>'
            '<ul class="roadmap__list">%s</ul></div>'
            % (state, title, meta, lis)
        )

    return """
<section id="roadmap" class="section--alt">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Roadmap</p>
      <h2>What is shipped, what is being built, what is only planned.</h2>
      <p class="lede">Taken from the repository's changelog, releases and roadmap.
      "Implemented" means implemented, tested and documented there — not
      announced.</p>
    </div>
    <div class="roadmap">
      %(cols)s
    </div>
    <div style="margin-top:1.5rem">
      <a class="btn btn--ghost btn--sm" href="%(github)s/blob/main/docs/ROADMAP.md" rel="noopener">%(branch)s Full roadmap</a>
    </div>
  </div>
</section>
""" % {
        "cols": "".join(cols),
        "github": GITHUB,
        "branch": icon("git-branch"),
    }


def creator():
    return """
<section id="creator">
  <div class="wrap">
    <div class="creator reveal">
      <div class="creator-grid">
        <div>
          <p class="eyebrow">The creator</p>
          <h2>The Mind Behind Silica.</h2>
          <p class="muted" style="margin-bottom:1rem">Umaiz Sufiyan · Student
          Developer &amp; Creator of Silica</p>
          <p>Umaiz Sufiyan is an independent student developer interested in
          programming languages, software engineering, artificial intelligence, and
          developer tools.</p>
          <p>Through Silica, he explores programming language design and the
          engineering involved in building software from the ground up.</p>
          <p>His vision is to keep learning, experimenting, and creating tools that
          make a meaningful contribution to the developer ecosystem.</p>
          <div class="creator-links">
            <a href="%(creator)s" rel="noopener">%(user)s GitHub</a>
            <a href="%(github)s" rel="noopener">%(gh)s Silica repository</a>
            <a href="%(instagram)s" rel="noopener">%(ig)s Instagram</a>
          </div>
          <p class="attribution">Created by Umaiz Sufiyan.</p>
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


def cta():
    return """
<section class="section--flush">
  <div class="wrap" style="padding-block:clamp(2.5rem,6vw,5rem)">
    <div class="cta reveal">
      <p class="eyebrow" style="justify-content:center">Start here</p>
      <h2>Your Next Idea Deserves a Language.</h2>
      <p>Explore Silica, discover its syntax, and follow the journey of an
      independently built programming language.</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="docs/getting-started.html">%(book)s Explore Documentation</a>
        <a class="btn btn--ghost" href="%(github)s" rel="noopener">%(star)s Star on GitHub</a>
      </div>
    </div>
  </div>
</section>
""" % {"book": icon("book"), "star": icon("star"), "github": GITHUB}


def body():
    return "".join([
        hero(), overview(), features(), playground(), story(), architecture(),
        install(), docs_section(), roadmap(), creator(), cta(),
    ])
