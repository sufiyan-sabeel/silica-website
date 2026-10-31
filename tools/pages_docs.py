"""Documentation pages for the Silica website.

Every code block comes from tools/snippets.py, which is executed against the
real implementation before the site is built.
"""

import json
import os

from site_chrome import (DOC_PAGES, GITHUB, VERSION, callout, code_block,
                         icon, output_block)
from snippets import SNIPPETS

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "snippet_output.json"), encoding="utf-8") as _fh:
    OUTPUTS = json.load(_fh)


def src(name):
    return SNIPPETS[name]["code"]


def out(name):
    return OUTPUTS.get(name, {}).get("output") or ""


def code(name, filename=None, label=None):
    return code_block(src(name), filename or SNIPPETS[name]["file"], label=label)


def code_out(name, filename="output"):
    text = out(name)
    if not text:
        return ""
    return output_block(text, filename)


def table(headers, rows):
    """A table that scrolls inside its own box on narrow screens."""
    head = "".join('<th scope="col">%s</th>' % h for h in headers)
    body = "".join(
        "<tr>%s</tr>" % "".join("<td>%s</td>" % cell for cell in row)
        for row in rows
    )
    return ('<div class="table-wrap" tabindex="0" role="region" aria-label="Table">'
            "<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>"
            % (head, body))


def h2(text, anchor):
    return '<h2 id="%s">%s</h2>' % (anchor, text)


# --------------------------------------------------------------------------
def getting_started():
    return """
<p>Silica is a Python package with one console command, <code>silica</code>.
This page takes you from nothing to a running program, then to bytecode and the
in-browser IDE.</p>

%(req)s

%(h_install)s
<p>The installer downloads the release wheel for the current version, verifies
its SHA-256 against <code>SHA256SUMS.txt</code> from the same release, and installs
it into an isolated environment at <code>~/.local/share/silica/venv</code> with a
launcher in <code>~/.local/bin</code> (or <code>$PREFIX/bin</code> on Termux).</p>

%(install_code)s

<p>If <code>silica</code> is not found afterwards, the installer prints the exact
line to add to your shell profile. In short:
<code>export PATH="$HOME/.local/bin:$PATH"</code>.</p>

<p>Other ways in — Termux, <code>pip install</code> from a checkout, a system-wide
install — are on the <a href="installation.html">Installation</a> page.</p>

%(h_first)s
<p>A Silica program lives in a <code>.sc</code> file. Every program needs a
<code>main</code> function; that is where execution starts.</p>

%(hello_code)s
%(hello_out)s

<p>Run it:</p>

%(run_code)s

%(h_check)s
<p><code>check</code> parses and type-checks without producing bytecode, which is
the fastest way to find a mistake. It exits non-zero when it finds one.</p>

%(check_code)s

<p>A diagnostic always names the file, line and column, and usually suggests a
fix:</p>

%(error_code)s

%(h_repl)s
<p>Run <code>silica</code> with no arguments for the interactive interpreter.
Globals and functions persist between entries.</p>

%(repl_code)s

%(h_bytecode)s
<p>Compiling writes a versioned <code>.sbc</code> file: a magic number, format
version, CRC-32, constant pool, function metadata and a line table. The loader
verifies it before anything executes.</p>

%(compile_code)s

%(h_ide)s
<p>The Script Mode IDE is a local editor and runner for <code>.sc</code> files. It
serves a page on <code>127.0.0.1</code> and requires the session token it prints.
The Run button executes the real toolchain in a subprocess.</p>

%(ide_code)s

%(h_next)s
<ul>
  <li><a href="syntax.html">Syntax</a> — keywords, statements and operators.</li>
  <li><a href="variables-and-data-types.html">Variables and Data Types</a> — the
  eight types Silica checks.</li>
  <li><a href="built-in-functions.html">Built-in Functions</a> — the standard
  library that exists today.</li>
  <li><a href="cli-reference.html">CLI Reference</a> — every command and flag.</li>
</ul>
""" % {
        "req": callout(
            "<strong>Requirement:</strong> Python 3.9 or newer. The core language "
            "has no third-party dependencies, so nothing else is needed to run "
            "Silica programs."
        ),
        "h_install": h2("1. Install", "install"),
        "install_code": code_block(
            "curl -fsSL https://raw.githubusercontent.com/sufiyan-sabeel/silica/main/install.sh | sh\n"
            "silica --version\n"
            "silica %s" % VERSION,
            "bash", show_copy=True, label="Terminal",
        ),
        "h_first": h2("2. Your first program", "first-program"),
        "hello_code": code("hello", "hello.sc"),
        "hello_out": code_out("hello"),
        "run_code": code_block(
            "$ silica run hello.sc\nHello from Silica\n\n"
            "$ silica hello.sc        # the same thing\nHello from Silica",
            "bash", label="Terminal",
        ),
        "h_check": h2("3. Check before you run", "check"),
        "check_code": code_block(
            "$ silica check hello.sc\n"
            "$ echo $?\n0",
            "bash", label="Terminal",
        ),
        "error_code": code_block(
            "app.sc:2:18: type error: cannot initialise Int with a value of type String\n"
            "  hint: convert explicitly with int(value)",
            "output", show_copy=False, label="Real diagnostic",
        ),
        "h_repl": h2("4. The interactive interpreter", "repl"),
        "repl_code": code_block(
            "$ silica\nSilica 0.9.0 — Ctrl+D to exit\n> sprint(\"hello\")\nhello\n"
            "> let x: Int = 2\n> sprint(x * 21)\n42",
            "bash", label="Terminal",
        ),
        "h_bytecode": h2("5. Compile to bytecode", "bytecode"),
        "compile_code": code_block(
            "$ silica compile hello.sc -o hello.sbc\n"
            "$ silica run hello.sbc\nHello from Silica",
            "bash", label="Terminal",
        ),
        "h_ide": h2("6. Try the Script Mode IDE", "ide"),
        "ide_code": code_block(
            "$ silica ide --root ~/scripts\n"
            "Silica Script Mode\n"
            "  workspace : /home/you/scripts\n"
            "  listening : 127.0.0.1:8080\n"
            "  open      : http://127.0.0.1:8080/?token=<session-token>",
            "bash", label="Terminal",
        ),
        "h_next": h2("Next steps", "next"),
    }


# --------------------------------------------------------------------------
def installation():
    return """
<p>There are four ways to get Silica, in order of how much you should trust them.
All of them install the same thing: a Python package named
<code>silica-lang</code>, importable as <code>silica</code>, with one console
script.</p>

%(summary)s

%(h_installer)s
<p>The installer is the supported path on Linux and Termux. It detects the
platform and architecture, finds Python 3.9+, downloads the release wheel and its
checksum file, and refuses to continue if the checksum does not match.</p>

%(installer_code)s

<p>What it does, in order: detects Termux or desktop Linux and the CPU
architecture; finds Python and checks the <code>venv</code> module; downloads the
wheel and <code>SHA256SUMS.txt</code>; installs into
<code>~/.local/share/silica/venv</code>; writes a launcher to
<code>~/.local/bin</code> (or <code>$PREFIX/bin</code>); prints the line to add to
your shell profile if needed; and records what it created so the uninstaller can
remove exactly that.</p>

<p>It never runs <code>sudo</code> unless you ask for it, never writes outside
those directories, and is safe to run twice — a second run is an upgrade.</p>

%(h_version)s
<p>The version must exist as a published release with the wheel and checksum
attached. The installer does not fall back to <code>main</code> if a version is
missing; it stops and says the release could not be found.</p>

%(version_code)s

%(h_uninstall)s
%(uninstall_code)s

<p>The uninstaller reads the manifest written at install time and removes only
those paths. It refuses to delete a launcher it did not create, and refuses to
delete a virtual environment outside the Silica home directory.</p>

%(h_termux)s
<p>Silica runs natively in Termux. Do not use <code>proot-distro</code> and do not
expect <code>sudo</code> to work — Termux is not a Linux distribution with root.</p>

%(termux_code)s

%(termux_note)s

%(h_source)s
<p>The most auditable route, and the right one if you want to read exactly what
you run.</p>

%(source_code)s

%(h_system)s
<p>The only path that uses root. It installs to <code>/opt/silica</code> and links
<code>/usr/local/bin/silica</code>.</p>

%(system_code)s

%(h_verify)s
%(verify_code)s

%(h_platforms)s
%(platform_table)s

%(h_trouble)s
%(trouble_table)s

%(trust)s
""" % {
        "summary": table(
            ["Method", "Best for", "Needs"],
            [
                ["Installer script", "Linux and Termux users who want the release build",
                 "<code>curl</code>, Python 3.9+"],
                ["Termux native", "Android through Termux", "<code>pkg install python</code>"],
                ["From source", "Reading the code you run",
                 "<code>git</code>, Python 3.9+"],
                ["System-wide", "Every user on one machine", "root"],
            ],
        ),
        "h_installer": h2("1. The installer", "installer"),
        "installer_code": code_block(
            "curl -fsSL https://raw.githubusercontent.com/sufiyan-sabeel/silica/main/install.sh | sh",
            "bash", label="Terminal",
        ),
        "h_version": h2("2. Pinning or upgrading", "version"),
        "version_code": code_block(
            "SILICA_VERSION=%s sh install.sh   # install or upgrade to a version\n"
            "SILICA_VERSION=0.8.0 sh install.sh  # roll back" % VERSION,
            "bash", label="Terminal",
        ),
        "h_uninstall": h2("3. Uninstalling", "uninstall"),
        "uninstall_code": code_block(
            "curl -fsSL https://raw.githubusercontent.com/sufiyan-sabeel/silica/main/uninstall.sh | sh",
            "bash", label="Terminal",
        ),
        "h_termux": h2("4. Termux (Android)", "termux"),
        "termux_code": code_block(
            "pkg update\npkg install python git curl\n"
            "curl -fsSL https://raw.githubusercontent.com/sufiyan-sabeel/silica/main/install.sh | sh",
            "bash", label="Terminal",
        ),
        "termux_note": callout(
            "<strong>Honest status:</strong> the installer's Termux branch is "
            "covered by automated tests that set the environment variables Termux "
            "sets (<code>TERMUX_VERSION</code>, <code>PREFIX</code>) and assert the "
            "launcher lands in <code>$PREFIX/bin</code>, but it has not been run on "
            "a real Android device as part of this work. Treat it as a strong "
            "expectation, not a verified claim.",
            kind="warn",
        ),
        "h_source": h2("5. From source", "source"),
        "source_code": code_block(
            "git clone https://github.com/sufiyan-sabeel/silica.git\n"
            "cd silica\n\n"
            "python3 -m venv .venv\n"
            ". .venv/bin/activate\n"
            "pip install .\n\n"
            "silica --version\n\n"
            "# or run straight from the checkout, with no install at all\n"
            "python3 -m silica examples/hello.sc",
            "bash", label="Terminal",
        ),
        "h_system": h2("6. System-wide", "system"),
        "system_code": code_block(
            "curl -fsSL https://raw.githubusercontent.com/sufiyan-sabeel/silica/main/install.sh \\\n"
            "  | sudo SILICA_SYSTEM=1 sh",
            "bash", label="Terminal",
        ),
        "h_verify": h2("Verifying an installation", "verify"),
        "verify_code": code_block(
            "silica --version        # silica %s\n"
            "silica examples/hello.sc   # Hello from Silica\n"
            "silica                  # the interpreter; Ctrl+D to leave" % VERSION,
            "bash", label="Terminal",
        ),
        "h_platforms": h2("Platforms", "platforms"),
        "platform_table": table(
            ["Platform", "Status"],
            [
                ["Debian / Ubuntu (x86_64, aarch64)", "Tested in CI and by hand"],
                ["Other Linux with Python 3.9+",
                 "Expected to work — the installer checks only <code>uname</code> and Python"],
                ["Termux (Android, aarch64)",
                 "Termux code path tested; <strong>not run on a device</strong>"],
                ["macOS",
                 "<code>install.sh</code> exits early; <code>pip install .</code> should work"],
                ["Windows", "No installer and no testing"],
            ],
        ),
        "h_trouble": h2("Troubleshooting", "troubleshooting"),
        "trouble_table": table(
            ["Symptom", "Cause and fix"],
            [
                ["<code>silica: command not found</code>",
                 "The launcher directory is not on <code>PATH</code>. Add "
                 "<code>export PATH=\"$HOME/.local/bin:$PATH\"</code> to your shell profile."],
                ["<code>error: Python 3.9+ not found</code>",
                 "Install Python, and on Debian/Ubuntu also "
                 "<code>python3-venv</code>: <code>sudo apt install python3 python3-venv</code>."],
                ["<code>error: the Python venv module is missing</code>",
                 "<code>sudo apt install python3-venv</code> on Debian/Ubuntu, "
                 "<code>pkg install python</code> on Termux."],
                ["<code>error: checksum mismatch</code>",
                 "The download was corrupted or altered. Re-run; if it persists, do "
                 "not install and verify the release yourself."],
                ["<code>silica ide</code> says <code>No module named silica</code>",
                 "You are running from a checkout without <code>PYTHONPATH</code>. "
                 "Use <code>python3 -m silica ide</code>."],
                ["The REPL prints <code>&gt; </code> instead of <code>¢</code>",
                 "Your terminal is not UTF-8. Set <code>LANG=C.UTF-8</code>."],
            ],
        ),
        "trust": callout(
            "<strong>The trust model, stated plainly.</strong> Piping a script into "
            "a shell means you trust that script and whatever it fetches. "
            "<code>install.sh</code> is short and readable; it downloads only from "
            "this repository's releases over HTTPS and verifies the wheel's SHA-256 "
            "against <code>SHA256SUMS.txt</code> from the same release. That "
            "protects against a corrupt or tampered download, not against a "
            "compromised GitHub account. If you need more than that, install from a "
            "source archive you verify yourself.",
            kind="warn",
        ),
    }


# --------------------------------------------------------------------------
def syntax():
    return """
<p>This page describes the grammar the v%(version)s parser actually accepts. Where
the grammar cannot express a rule — for example that <code>break</code> is only
legal inside a loop — the checker enforces it instead.</p>

%(h_keywords)s
<p>These are the only reserved words. They cannot be used as identifiers.</p>
%(keyword_table)s

%(h_program)s
<p>A program is a sequence of imports, function declarations and global
declarations. Braces are mandatory for every block; there is no
single-statement body form.</p>
%(program_code)s
%(program_out)s

%(h_statements)s
%(statement_table)s

%(h_newlines)s
<ul>
  <li>A newline ends a statement. Inside <code>(</code> … <code>)</code> and
  <code>[</code> … <code>]</code> newlines are ignored, so a long expression can be
  wrapped in parentheses.</li>
  <li><code>;</code> is accepted as an optional statement separator, but a newline
  is the idiomatic terminator.</li>
  <li><code>fin</code> may appear as an explicit end-of-block marker. It is
  accepted and never required.</li>
  <li>Comments run from <code>#</code> or <code>//</code> to the end of the
  line.</li>
</ul>

%(h_operators)s
<p>From loosest to tightest binding:</p>
%(operator_table)s

<p><code>und</code> and <code>ou</code> short-circuit: the right-hand side is not
evaluated when the result is already known.</p>
%(logic_code)s

%(h_expressions)s
<p>A <code>{</code> in expression position starts a map literal; a <code>{</code>
after a statement header starts a block. The parser decides by position, so the
two never conflict.</p>
%(expr_code)s
%(expr_out)s

%(h_grammar)s
<p>The EBNF for the accepted grammar, abridged to the parts most often
asked about:</p>
%(grammar_code)s

%(h_types)s
<p>Type annotations are optional in <code>let</code>, <code>const</code> and
parameter lists. Where they are given, the checker enforces them.</p>
%(type_note)s
""" % {
        "version": VERSION,
        "h_keywords": h2("Keywords", "keywords"),
        "keyword_table": table(
            ["Keyword", "Meaning"],
            [
                ["<code>sfn</code>", "declare a function"],
                ["<code>ret</code>", "return a value (or nothing)"],
                ["<code>let</code> / <code>const</code>", "mutable / immutable binding"],
                ["<code>si</code> / <code>sino</code>", "if / else"],
                ["<code>tant</code>", "while loop"],
                ["<code>per</code> … <code>in</code>", "for each loop"],
                ["<code>break</code> / <code>continue</code>",
                 "leave the innermost loop / start its next iteration"],
                ["<code>halt</code>", "terminate the program, optionally with an exit code"],
                ["<code>fin</code>", "optional explicit end-of-block marker"],
                ["<code>oui</code> / <code>nein</code>", "true / false"],
                ["<code>und</code> / <code>ou</code> / <code>non</code>",
                 "logical and / or / not"],
                ["<code>sprint</code> / <code>dit</code>", "print with / without a newline"],
                ["<code>input</code>", "read one line of stdin as a String"],
                ["<code>use</code>", "import a standard-library module"],
            ],
        ),
        "h_program": h2("Program structure", "structure"),
        "program_code": code("structure", "structure.sc"),
        "program_out": code_out("structure"),
        "h_statements": h2("Statements", "statements"),
        "statement_table": table(
            ["Form", "Example"],
            [
                ["binding", "<code>let count: Int = 3</code> · <code>const name: String = \"Silica\"</code>"],
                ["assignment", "<code>count = count + 1</code> (only for <code>let</code>)"],
                ["conditional", "<code>si cond { … } sino { … }</code>"],
                ["while", "<code>tant cond { … }</code>"],
                ["for each", "<code>per item in list { … }</code>"],
                ["return", "<code>ret value</code> · <code>ret</code>"],
                ["loop control", "<code>break</code> · <code>continue</code>"],
                ["terminate", "<code>halt(2)</code> · <code>halt</code>"],
                ["expression", "<code>sprint(x)</code> · <code>push(items, 1)</code>"],
            ],
        ),
        "h_newlines": h2("Newlines, blocks and comments", "newlines"),
        "h_operators": h2("Operators", "operators"),
        "operator_table": table(
            ["Level", "Operators"],
            [
                ["logical or", "<code>ou</code>"],
                ["logical and", "<code>und</code>"],
                ["equality", "<code>==</code> <code>!=</code>"],
                ["comparison", "<code>&lt;</code> <code>&lt;=</code> <code>&gt;</code> <code>&gt;=</code>"],
                ["additive", "<code>+</code> <code>-</code>"],
                ["multiplicative", "<code>*</code> <code>/</code> <code>%</code>"],
                ["unary", "<code>non</code> <code>-</code>"],
                ["postfix", "call <code>()</code>, index <code>[]</code>, member <code>.</code>"],
            ],
        ),
        "logic_code": code_block(
            "si ready und non blocked {\n"
            "    sprint(\"Ready\")\n"
            "}",
            "logic.sc", show_copy=False, label="Short-circuit logic",
        ),
        "h_expressions": h2("Literals and expressions", "expressions"),
        "expr_code": code("literals", "literals.sc"),
        "expr_out": code_out("literals"),
        "h_grammar": h2("Grammar", "grammar"),
        "grammar_code": code_block(
            "program        = { NEWLINE | use-decl | func-decl | global-decl } EOF ;\n"
            "func-decl      = \"sfn\" IDENT \"(\" [ param { \",\" param } ] \")\"\n"
            "                 [ \"->\" type ] block ;\n"
            "block          = \"{\" { NEWLINE | stmt } [ \"fin\" ] \"}\" ;\n"
            "if-stmt        = \"si\" expr block [ \"sino\" block ] ;\n"
            "while-stmt     = \"tant\" expr block ;\n"
            "for-stmt       = \"per\" IDENT \"in\" expr block ;\n"
            "let-stmt       = (\"let\" | \"const\") IDENT [ \":\" type ] \"=\" expr NEWLINE ;\n"
            "type           = \"Int\" | \"Float\" | \"Bool\" | \"String\" | \"Unit\"\n"
            "               | \"List\" | \"Map\" | \"Any\" ;",
            "grammar.ebnf", show_copy=False,
        ),
        "h_types": h2("Types in the grammar", "types"),
        "type_note": callout(
            "There are exactly eight type names: <code>Int</code>, "
            "<code>Float</code>, <code>Bool</code>, <code>String</code>, "
            "<code>Unit</code>, <code>List</code>, <code>Map</code> and "
            "<code>Any</code>. There are no user-defined types and no generic "
            "parameters in %s — <a href=\"variables-and-data-types.html\">Variables "
            "and Data Types</a> explains what that means in practice." % VERSION
        ),
    }


# --------------------------------------------------------------------------
def variables():
    return """
<p>A binding is introduced with <code>let</code> (mutable) or <code>const</code>
(immutable). The type annotation is optional: when it is omitted, the checker
infers the type from the initialiser.</p>

%(bind_code)s
%(bind_out)s

%(h_mutability)s
<p>Assigning to a <code>const</code> is a compile-time error, not a runtime
surprise:</p>
%(const_code)s
%(const_out)s

%(h_types)s
%(type_table)s

%(type_code)s
%(type_out)s

%(h_int)s
<p><code>Int</code> is a signed 64-bit integer that wraps on overflow.
<code>Float</code> is IEEE-754 double precision. Mixing them in arithmetic is a
type error — convert explicitly with <code>float(x)</code> or <code>int(x)</code>.</p>

<p>Integer division truncates toward zero, and <code>%%</code> keeps the sign of
the dividend. Division or modulo by zero is a runtime error for both
<code>Int</code> and <code>Float</code>:</p>
%(zero_code)s
%(zero_out)s

%(h_containers)s
<p><code>List</code> and <code>Map</code> are containers whose element type is
<code>Any</code> in v%(version)s — there are no generics yet, so an element is
accepted whatever it is and checked at runtime. This is a documented limitation,
not an oversight.</p>

<p><code>==</code> compares <code>List</code> and <code>Map</code> structurally, by
value, and scalars by value. Negative indices and missing map keys are runtime
errors rather than silent <code>Unit</code> values.</p>
%(container_code)s
%(container_out)s

%(h_any)s
%(any_note)s

%(h_unit)s
<p>There is no <code>null</code>. A function that returns nothing returns
<code>Unit</code>, and <code>sprint</code> renders it as <code>unit</code>.</p>
%(unit_code)s
%(unit_out)s
""" % {
        "bind_code": code("variables", "variables.sc"),
        "bind_out": code_out("variables"),
        "h_mutability": h2("let, const and assignment", "mutability"),
        "const_code": code("const_error", "const.sc"),
        "const_out": code_out("const_error"),
        "h_types": h2("The eight types", "types"),
        "type_table": table(
            ["Type", "What it is", "Example"],
            [
                ["<code>Int</code>", "signed 64-bit integer, wraps on overflow", "<code>42</code>"],
                ["<code>Float</code>", "IEEE-754 double precision", "<code>3.14159</code>"],
                ["<code>Bool</code>", "<code>oui</code> or <code>nein</code>", "<code>oui</code>"],
                ["<code>String</code>", "UTF-8 text, four delimiter forms", "<code>\"Silica\"</code>"],
                ["<code>Unit</code>", "the absence of a value", "the result of <code>sprint</code>"],
                ["<code>List</code>", "ordered, indexed from 0, mutable", "<code>[1, 2, 3]</code>"],
                ["<code>Map</code>", "string-keyed, mutable", "<code>{\"a\": 1}</code>"],
                ["<code>Any</code>", "accepted by the checker without inspection", "element type of List and Map"],
            ],
        ),
        "type_code": code("types_table", "types.sc"),
        "type_out": code_out("types_table"),
        "h_int": h2("Numbers", "numbers"),
        "zero_code": code("zero_error", "zero.sc"),
        "zero_out": code_out("zero_error"),
        "version": VERSION,
        "h_containers": h2("Lists and maps", "containers"),
        "container_code": code("collections", "collections.sc"),
        "container_out": code_out("collections"),
        "h_any": h2("Why Any appears", "any"),
        "any_note": callout(
            "<strong>No generics in %s.</strong> <code>List</code> and "
            "<code>Map</code> elements check as <code>Any</code>, which is "
            "compatible with every type. The implementation still validates at "
            "runtime and raises a located error on a mismatch, so a wrong element "
            "fails loudly — just later than a static check would." % VERSION,
            kind="warn",
        ),
        "h_unit": h2("Unit", "unit"),
        "unit_code": code("unit_demo", "unit.sc"),
        "unit_out": code_out("unit_demo"),
    }


# --------------------------------------------------------------------------
def functions():
    return """
<p>A function is declared with <code>sfn</code>. Parameters may carry type
annotations, and <code>-&gt; T</code> gives the return type. Without a return type
the function returns <code>Unit</code>.</p>

%(fn_code)s
%(fn_out)s

%(h_params)s
<p>Parameter types are checked at every call site, and so is the number of
arguments:</p>
%(arity_code)s
%(arity_out)s

%(h_return)s
<p>A function with a non-<code>Unit</code> return type must return on every path;
the checker verifies that statically. A <code>Unit</code> function may return
early with a bare <code>ret</code>.</p>

%(h_recursion)s
<p>Recursion is supported. Calls use explicit frames on the VM, so the limit is
the frame budget rather than the host's Python stack.</p>
%(fib_code)s
%(fib_out)s

%(h_unit)s
<p>Functions without a return type are the natural way to write procedures:</p>
%(unit_code)s
%(unit_out)s

%(h_errors)s
<p>Silica has no exceptions and no <code>Result</code> type. Errors are
compile-time diagnostics, or runtime aborts that stop the program with a located
message. Idiomatic Silica returns a sentinel or prints and returns early:</p>
%(err_code)s
%(err_out)s

%(h_limits)s
%(limits_note)s
""" % {
        "fn_code": code("functions", "functions.sc"),
        "fn_out": code_out("functions"),
        "h_params": h2("Parameters and arity", "parameters"),
        "arity_code": code("arity_error", "arity.sc"),
        "arity_out": code_out("arity_error"),
        "h_return": h2("Return types", "return"),
        "h_recursion": h2("Recursion", "recursion"),
        "fib_code": code("recursion", "fibonacci.sc"),
        "fib_out": code_out("recursion"),
        "h_unit": h2("Unit functions", "unit"),
        "unit_code": code("unit_function", "banner.sc"),
        "unit_out": code_out("unit_function"),
        "h_errors": h2("Errors", "errors"),
        "err_code": code("divide", "divide.sc"),
        "err_out": code_out("divide"),
        "h_limits": h2("What functions cannot do yet", "limits"),
        "limits_note": callout(
            "<strong>Functions are not first-class values in %s.</strong> They can be "
            "called, not passed, returned or stored. There are no closures, no "
            "anonymous functions and no methods on user-defined types. Those are "
            "planned, not present — see the <a href=\"../index.html#roadmap\">"
            "roadmap</a>." % VERSION,
            kind="warn",
        ),
    }


# --------------------------------------------------------------------------
def control_flow():
    return """
<p>Control flow is expressed with Silica's own keywords: <code>si</code> /
<code>sino</code> for conditionals, <code>tant</code> for while loops,
<code>per … in …</code> for iteration, and <code>break</code> /
<code>continue</code> inside loops.</p>

%(h_if)s
<p>Braces are required. <code>sino</code> must follow an <code>si</code> block; a
newline between them is fine. There is no <code>sino si</code> chain form, so
nesting is explicit:</p>
%(if_code)s
%(if_out)s
%(nested_code)s
%(nested_out)s

%(h_logic)s
%(logic_code)s
%(logic_out)s

%(h_while)s
<p><code>tant</code> tests its condition before each iteration. The condition must
be a <code>Bool</code>.</p>
%(while_code)s
%(while_out)s

%(h_for)s
<p><code>per</code> iterates a <code>List</code> by value, a <code>Map</code> by
key, and the list produced by <code>range</code>. The loop variable is immutable
inside the body.</p>
%(for_code)s
%(for_out)s

%(h_break)s
<p><code>break</code> leaves the innermost loop and <code>continue</code> starts
its next iteration. Both are compiled to jumps — no new opcode, no change to the
bytecode format — and both are compile-time errors outside a loop.</p>
%(break_code)s
%(break_out)s

%(h_halt)s
<p><code>halt</code> terminates the program immediately. With an argument, that
value becomes the process exit code.</p>
%(halt_code)s
%(halt_out)s

%(h_loops)s
%(loop_full_code)s
%(loop_full_out)s
""" % {
        "h_if": h2("si / sino", "if"),
        "if_code": code("conditions", "conditionals.sc"),
        "if_out": code_out("conditions"),
        "nested_code": code("nested_if", "grades.sc"),
        "nested_out": code_out("nested_if"),
        "h_logic": h2("und, ou, non", "logic"),
        "logic_code": code("logic", "logic.sc"),
        "logic_out": code_out("logic"),
        "h_while": h2("tant — while", "while"),
        "while_code": code("while_loop", "while.sc"),
        "while_out": code_out("while_loop"),
        "h_for": h2("per — for each", "for"),
        "for_code": code("loop_over_list", "loop_list.sc"),
        "for_out": code_out("loop_over_list"),
        "h_break": h2("break and continue", "break"),
        "break_code": code("loop_control", "loop_control.sc"),
        "break_out": code_out("loop_control"),
        "h_halt": h2("halt", "halt"),
        "halt_code": code("halt_demo", "halt.sc"),
        "halt_out": code_out("halt_demo"),
        "h_loops": h2("A complete example", "example"),
        "loop_full_code": code("loops", "loops.sc"),
        "loop_full_out": code_out("loops"),
    }


# --------------------------------------------------------------------------
def strings():
    return """
<p>A <code>String</code> is UTF-8 text. Silica accepts four delimiter forms, and
the triple-quoted ones may span lines.</p>

%(delim_code)s
%(delim_out)s

%(h_escapes)s
%(escape_table)s

%(h_ops)s
<p><code>+</code> concatenates two strings; mixing a string and a number is a type
error, so convert with <code>str()</code>, <code>int()</code> or
<code>float()</code> first. Indexing with <code>s[i]</code> returns a one-character
string, indexed from zero; <code>len(s)</code> gives the length in characters.</p>
%(ops_code)s
%(ops_out)s

%(h_module)s
<p>The <code>string</code> module must be imported with <code>use string</code>.
Calling it without the import is a compile-time error that says so.</p>
%(module_code)s
%(module_out)s

%(h_functions)s
%(function_table)s

%(h_limits)s
%(limits_note)s
""" % {
        "delim_code": code("string_delimiters", "delimiters.sc"),
        "delim_out": code_out("string_delimiters"),
        "h_escapes": h2("Escape sequences", "escapes"),
        "escape_table": table(
            ["Escape", "Meaning"],
            [
                ["<code>\\n</code>", "newline"],
                ["<code>\\t</code>", "tab"],
                ["<code>\\r</code>", "carriage return"],
                ["<code>\\0</code>", "null"],
                ["<code>\\\\</code>", "backslash"],
                ["<code>\\\"</code> / <code>\\'</code>", "quote"],
                ["<code>\\uXXXX</code>", "a Unicode code point"],
            ],
        ),
        "h_ops": h2("Concatenation, indexing and length", "operations"),
        "ops_code": code("string_concat", "concat.sc"),
        "ops_out": code_out("string_concat"),
        "h_module": h2("The string module", "module"),
        "module_code": code("strings", "strings.sc"),
        "module_out": code_out("strings"),
        "h_functions": h2("Functions in the string module", "functions"),
        "function_table": table(
            ["Function", "Returns", "Notes"],
            [
                ["<code>string.split(s, sep)</code>", "<code>List</code>", "splits on a separator"],
                ["<code>string.join(list, sep)</code>", "<code>String</code>", "joins list elements"],
                ["<code>string.trim(s)</code>", "<code>String</code>", "removes surrounding whitespace"],
                ["<code>string.replace(s, from, to)</code>", "<code>String</code>", "replaces every occurrence"],
                ["<code>string.contains(s, part)</code>", "<code>Bool</code>", "substring test"],
                ["<code>string.starts_with(s, prefix)</code>", "<code>Bool</code>", "prefix test"],
                ["<code>string.ends_with(s, suffix)</code>", "<code>Bool</code>", "suffix test"],
                ["<code>string.upper(s)</code>", "<code>String</code>", "uppercase"],
                ["<code>string.lower(s)</code>", "<code>String</code>", "lowercase"],
            ],
        ),
        "h_limits": h2("What strings cannot do", "limits"),
        "limits_note": callout(
            "There is no string interpolation and no template syntax in %s: build "
            "text with <code>+</code> and <code>str()</code>. There are also no "
            "regular expressions — <code>regex</code> is a planned module that "
            "currently fails to import with an explicit message." % VERSION,
            kind="warn",
        ),
    }


# --------------------------------------------------------------------------
def builtins():
    return """
<p>Silica's standard library is a set of native functions grouped into modules.
<code>core</code> is always in scope; everything else needs a
<code>use</code> statement. Types in the tables below are the ones the static
checker enforces.</p>

%(h_core)s
%(core_table)s
<p>Example — <code>type_of</code>, <code>str</code> and <code>len</code>:</p>
%(core_code)s
%(core_out)s

%(h_math)s
<p>Import with <code>use math</code>. <code>math.pi</code>, <code>math.e</code> and
<code>math.tau</code> are constants, not functions.</p>
%(math_table)s
%(math_code)s
%(math_out)s

%(h_string)s
<p>Import with <code>use string</code>. The full list is on the
<a href="strings.html">Strings</a> page.</p>

%(h_collections)s
<p>Import with <code>use collections</code>.</p>
%(collections_table)s
%(collections_code)s
%(collections_out)s

%(h_json)s
<p>Import with <code>use json</code>. The mapping is deliberate:
<code>oui</code>/<code>nein</code> become <code>true</code>/<code>false</code>,
<code>null</code> parses to <code>Unit</code>, and errors carry a position.</p>
%(json_table)s
%(json_code)s
%(json_out)s

%(h_fs)s
<p>Import with <code>use fs</code>. Every function is behind a capability, and
nothing is granted by default:</p>
%(fs_table)s
%(fs_code)s

%(h_modules)s
%(module_table)s

%(h_planned)s
%(planned_note)s
""" % {
        "h_core": h2("core — always available", "core"),
        "core_table": table(
            ["Function", "Signature", "What it does"],
            [
                ["<code>sprint(x)</code>", "<code>Any → Unit</code>", "print with a newline"],
                ["<code>dit(x)</code>", "<code>Any → Unit</code>", "print without a newline"],
                ["<code>input(prompt)</code>", "<code>String → String</code>", "read one line of stdin"],
                ["<code>type_of(x)</code>", "<code>Any → String</code>", "the runtime type name"],
                ["<code>assert(cond, message)</code>", "<code>Bool, String → Unit</code>", "abort if false"],
                ["<code>str(x)</code> / <code>int(x)</code> / <code>float(x)</code>",
                 "<code>Any → String / Int / Float</code>", "explicit conversion"],
                ["<code>len(x)</code>", "<code>Any → Int</code>", "length of a string, list or map"],
                ["<code>range(a, b, step)</code>", "<code>Int… → List</code>", "1–3 arguments"],
                ["<code>push(list, value)</code>", "<code>List, Any → Unit</code>", "append in place"],
                ["<code>keys(map)</code> / <code>values(map)</code>", "<code>Map → List</code>", "map contents"],
                ["<code>has(container, key)</code>", "<code>Any, Any → Bool</code>", "key or membership test"],
            ],
        ),
        "core_code": code("core_demo", "core.sc"),
        "core_out": code_out("core_demo"),
        "h_math": h2("math", "math"),
        "math_table": table(
            ["Function", "Returns"],
            [
                ["<code>math.abs(x)</code>", "same type as the argument"],
                ["<code>math.min(a, b)</code> / <code>math.max(a, b)</code>", "the smaller / larger value"],
                ["<code>math.sqrt(x)</code>", "<code>Float</code>"],
                ["<code>math.pow(a, b)</code>", "<code>Float</code>"],
                ["<code>math.floor(x)</code> / <code>math.ceil(x)</code> / <code>math.round(x)</code>", "<code>Int</code>"],
            ],
        ),
        "math_code": code("math", "math_demo.sc"),
        "math_out": code_out("math"),
        "h_string": h2("string", "string"),
        "h_collections": h2("collections", "collections"),
        "collections_table": table(
            ["Function", "Returns", "Notes"],
            [
                ["<code>collections.sort(list)</code>", "<code>List</code>", "a sorted copy"],
                ["<code>collections.reverse(list)</code>", "<code>List</code>", "a reversed copy"],
                ["<code>collections.index_of(list, value)</code>", "<code>Int</code>", "position, or -1"],
                ["<code>collections.sum(list)</code>", "<code>Any</code>", "numeric total"],
            ],
        ),
        "collections_code": code("collections", "collections.sc"),
        "collections_out": code_out("collections"),
        "h_json": h2("json", "json"),
        "json_table": table(
            ["Function", "Signature", "Notes"],
            [
                ["<code>json.parse(text)</code>", "<code>String → Any</code>", "errors report a position"],
                ["<code>json.stringify(value)</code>", "<code>Any → String</code>", "compact form"],
                ["<code>json.stringify(value, indent)</code>", "<code>Any, Int → String</code>", "pretty-printed"],
            ],
        ),
        "json_code": code("json", "json_demo.sc"),
        "json_out": code_out("json"),
        "h_fs": h2("fs — behind capabilities", "fs"),
        "fs_table": table(
            ["Function", "Capability required"],
            [
                ["<code>fs.read_text(path)</code>", "<code>fs.read</code>"],
                ["<code>fs.write_text(path, text)</code>", "<code>fs.write</code>"],
                ["<code>fs.list_dir(path)</code>", "<code>fs.list</code>"],
                ["<code>fs.exists(path)</code>", "none — metadata only"],
            ],
        ),
        "fs_code": code_block(
            "$ silica run app.sc --allow-fs-read ./data --allow-fs-write ./out\n"
            "\n"
            "# without the grant:\n"
            "# capability error: 'fs.read' is not granted\n"
            "#   hint: run with --allow-fs-read DIR",
            "bash", label="Granting a capability",
        ),
        "h_modules": h2("Modules", "modules"),
        "module_table": table(
            ["Module", "Import", "Status"],
            [
                ["<code>core</code>", "always in scope", "implemented"],
                ["<code>math</code>", "<code>use math</code>", "implemented"],
                ["<code>string</code>", "<code>use string</code>", "implemented"],
                ["<code>collections</code>", "<code>use collections</code>", "implemented"],
                ["<code>json</code>", "<code>use json</code>", "implemented"],
                ["<code>fs</code>", "<code>use fs</code>", "implemented, capability-gated"],
                ["<code>ui</code>, <code>tui</code>, <code>gui</code>, <code>speech</code>",
                 "<code>use ui</code> …", "implemented; UI namespaces are separate"],
                ["<code>path</code>, <code>time</code>, <code>random</code>, "
                 "<code>regex</code>, <code>http</code>, <code>net</code>, "
                 "<code>crypto</code>", "—", "planned; importing is a compile error"],
            ],
        ),
        "h_planned": h2("Importing something that does not exist", "planned"),
        "planned_note": callout(
            "A planned module is refused at compile time with a message that names "
            "it — it never pretends to load. For example, "
            "<code>use net</code> reports that the module is planned and not "
            "implemented. The list of planned modules is fixed in the source, so "
            "the message cannot drift from reality."
        ),
    }


# --------------------------------------------------------------------------
def cli():
    return """
<p>One command, <code>silica</code>, with a small set of subcommands. Run
<code>silica --help</code> for the same list on your machine.</p>

%(h_commands)s
%(command_table)s

%(h_flags)s
<p>Capability flags apply to <code>run</code> and to running a file directly.
Nothing is granted by default.</p>
%(flag_table)s

%(h_usage)s
%(usage_code)s

%(h_exit)s
%(exit_table)s

%(h_missing)s
%(missing_note)s
""" % {
        "h_commands": h2("Commands", "commands"),
        "command_table": table(
            ["Command", "What it does"],
            [
                ["<code>silica &lt;file.sc&gt;</code>", "run a source file directly"],
                ["<code>silica &lt;file.sbc&gt;</code>", "run verified bytecode"],
                ["<code>silica</code>", "start the interactive interpreter"],
                ["<code>silica run &lt;file&gt;</code>", "compile if needed, then execute"],
                ["<code>silica check &lt;file.sc&gt;</code>", "parse and type-check only"],
                ["<code>silica compile &lt;file.sc&gt; [-o out.sbc]</code>", "compile to versioned bytecode"],
                ["<code>silica repl</code>", "interactive session"],
                ["<code>silica fmt &lt;file.sc&gt; [--check]</code>", "rewrite in canonical style, or verify it"],
                ["<code>silica test [dir]</code>", "run <code>*_test.sc</code> files under a directory"],
                ["<code>silica ide [--root DIR] [--port N] [--host H]</code>",
                 "Script Mode IDE in your browser"],
                ["<code>silica voice &lt;subcommand&gt;</code>", "speech: list, install, speak, transcribe"],
                ["<code>silica capabilities [flags]</code>", "print the effective capability set"],
                ["<code>silica --version</code> / <code>--help</code>", "version or usage"],
            ],
        ),
        "h_flags": h2("Capability flags", "flags"),
        "flag_table": table(
            ["Flag", "Effect"],
            [
                ["<code>--allow-fs-read DIR</code>", "allow reading files under DIR"],
                ["<code>--allow-fs-write DIR</code>", "allow writing files under DIR"],
                ["<code>--allow-fs-list DIR</code>", "allow listing directories under DIR"],
                ["<code>--allow-tui</code>", "allow terminal applications"],
                ["<code>--allow-gui</code>", "allow desktop windows"],
                ["<code>--deny-fs-read</code>, <code>--deny-fs-write</code>, <code>--deny-fs-list</code>",
                 "remove a capability a config file granted — a denial always wins"],
                ["<code>--capabilities FILE</code>", "read grants from a TOML <code>[capabilities]</code> table"],
            ],
        ),
        "h_usage": h2("Worked example", "usage"),
        "usage_code": code_block(
            "$ silica --version\n"
            "silica %(v)s\n"
            "\n"
            "$ silica check examples/fibonacci.sc\n"
            "\n"
            "$ silica compile examples/fibonacci.sc -o fib.sbc\n"
            "$ silica run fib.sbc\n"
            "0 1 1 2 3 5 8 13 21 34 55\n"
            "\n"
            "$ silica test tests\n"
            "5/5 test files passed" % {"v": VERSION},
            "bash", label="Terminal",
        ),
        "h_exit": h2("Exit codes", "exit-codes"),
        "exit_table": table(
            ["Situation", "Exit code"],
            [
                ["the program finished normally", "0"],
                ["<code>halt(n)</code>", "n"],
                ["a compile or runtime error", "non-zero"],
                ["<code>silica check</code> found a problem", "1"],
            ],
        ),
        "h_missing": h2("Not implemented", "not-implemented"),
        "missing_note": callout(
            "<code>new</code>, <code>add</code>, <code>remove</code>, "
            "<code>install</code> and <code>build</code> belong to the packaging "
            "milestone and are not implemented. Running them reports that they are "
            "not implemented rather than failing obscurely — the CLI does not fake "
            "a package manager.",
            kind="warn",
        ),
    }


# --------------------------------------------------------------------------
def examples():
    gallery = [
        ("hello", "Hello World", "The smallest complete program."),
        ("loops", "Loops", "Sum 1–10 with <code>per</code>, then count down with "
                           "<code>tant</code>."),
        ("conditions", "Conditionals", "<code>si</code> / <code>sino</code>."),
        ("logic", "Logic", "Short-circuit <code>und</code>, <code>ou</code> and "
                           "<code>non</code>."),
        ("recursion", "Recursion", "Fibonacci, computed by calling itself."),
        ("collections", "Collections", "Lists and maps with the collections "
                                       "module."),
        ("strings", "Strings", "Split, join, replace and index."),
        ("json", "JSON", "Parse and re-emit a document, compact and pretty."),
        ("math", "Math", "The math module and its constant <code>pi</code>."),
    ]

    blocks = []
    for name, title, description in gallery:
        blocks.append(
            '<div class="reveal" style="margin-bottom:3rem">'
            "<h3>%s</h3><p>%s</p>\n%s\n%s\n</div>"
            % (title, description, code(name, SNIPPETS[name]["file"]),
               code_out(name))
        )

    return """
<p>Every program on this page is a file from the repository, or an equivalent
written for the documentation, and every one was executed against v%(version)s
before publication. The output shown is the real output.</p>

%(gallery)s

%(h_more)s
<p>The repository ships more examples that need a capability, a display or
stdin:</p>
%(extra_table)s
%(note)s
""" % {
        "version": VERSION,
        "gallery": "\n".join(blocks),
        "h_more": h2("Examples that need more than a terminal", "more"),
        "extra_table": table(
            ["File", "Needs"],
            [
                ["<code>examples/calculator.sc</code>", "stdin"],
                ["<code>examples/json_demo.sc</code>", "nothing"],
                ["<code>examples/fs_demo.sc</code>", "<code>--allow-fs-read</code> / <code>--allow-fs-write</code>"],
                ["<code>examples/tui_demo.sc</code>", "<code>--allow-tui</code> and a real terminal"],
                ["<code>examples/gui_demo.sc</code>", "<code>--allow-gui</code> and a display"],
                ["<code>examples/ui_hello.sc</code>", "the web UI renderer"],
            ],
        ),
        "note": callout(
            "Run any of them with <code>silica run examples/&lt;name&gt;.sc</code>. "
            "The full set, with what each one demonstrates, is in the "
            "<a href=\"%s/tree/main/examples\">repository's examples directory</a>." % GITHUB
        ),
    }


# --------------------------------------------------------------------------
def faq():
    items = [
        ("Is Silica fast?",
         "No. On the repository's four benchmarks it ran 38–101× slower than CPython "
         "when measured on 2026-10-28, because the VM is a Python loop. Constant "
         "folding cut one hot loop by 39%. Speed is not the current goal; "
         "correctness and clarity are."),
        ("Is it production-ready?",
         "No. It is an early 0.x release with a small standard library, no "
         "concurrency, no networking and no package manager. Use it to learn, to "
         "experiment, and to build small tools."),
        ("Can Silica compile itself?",
         "Not yet. Self-hosting is a staged plan in the repository's bootstrap "
         "document, not a finished feature."),
        ("Does it have classes, structs or generics?",
         "No. There are no user-defined types, no fields or methods, and no generic "
         "parameters — <code>List</code> and <code>Map</code> elements check as "
         "<code>Any</code>. These are on the roadmap."),
        ("Are there closures or first-class functions?",
         "No. Functions can be called but not passed, returned or stored."),
        ("Does it support exceptions or a Result type?",
         "No. A type error is caught before anything runs; a runtime error stops the "
         "program with a located message. Recoverable errors are written by hand, "
         "for example by returning a sentinel value."),
        ("Can it make HTTP requests or run a web server?",
         "No. <code>net</code>, <code>http</code> and <code>crypto</code> are planned "
         "modules; importing one is a compile error that says so."),
        ("Which platforms work?",
         "Linux x86_64 is the tested platform. Termux's code path is tested with its "
         "environment variables but has not been run on a device. macOS and Windows "
         "are not supported by the installer; <code>pip install .</code> should work "
         "because there are no compiled parts, but that is an expectation, not a "
         "verified claim."),
        ("Why does it need a capability to read a file?",
         "Because Silica programs are untrusted by default. A program cannot read, "
         "write, open a window or use the terminal unless you grant exactly that "
         "capability, scoped to a directory. It is the same idea as a browser "
         "permission prompt, applied to a language."),
        ("Is it free? Can I use it commercially?",
         "Yes. Silica is MIT licensed — Copyright (c) 2026 Umaiz Sufiyan. You may "
         "use, modify and redistribute it, including commercially, provided the "
         "copyright notice and permission notice are included."),
        ("How is it tested?",
         "The repository runs its suite with <code>python3 -m unittest discover -s "
         "tests -t .</code>; on the audited commit that is 803 tests. CI runs it on "
         "Python 3.9, 3.11 and 3.12. Silica also has its own test runner for "
         "<code>*_test.sc</code> files: <code>silica test tests</code>."),
        ("Who made Silica?",
         "Umaiz Sufiyan, an independent student developer. The project is developed "
         "in the open on GitHub, and contributions are welcome."),
        ("Why are the keywords not English?",
         "Because the language was designed to have its own identity rather than "
         "imitate another one. <code>si</code>/<code>sino</code>, "
         "<code>tant</code>/<code>per</code> and <code>oui</code>/<code>nein</code> "
         "are the language's own vocabulary, and they are reserved words."),
    ]

    blocks = []
    for question, answer in items:
        blocks.append(
            "<details><summary>%s</summary><p>%s</p></details>" % (question, answer)
        )

    return """
<p>Short answers to the questions that come up most, including the ones where the
answer is "no".</p>

<div class="faq">
%(blocks)s
</div>

%(h_more)s
<p>Still stuck? Open an <a href="%(github)s/issues">issue on GitHub</a>. Questions
that turn into useful answers get added to this page.</p>
""" % {
        "blocks": "\n".join(blocks),
        "h_more": h2("Something else", "more"),
        "github": GITHUB,
    }


PAGES = {
    "getting-started": getting_started,
    "installation": installation,
    "syntax": syntax,
    "variables-and-data-types": variables,
    "functions": functions,
    "control-flow": control_flow,
    "strings": strings,
    "built-in-functions": builtins,
    "cli-reference": cli,
    "examples": examples,
    "faq": faq,
}
