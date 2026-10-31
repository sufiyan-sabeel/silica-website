"""Run every website snippet through the real Silica implementation.

    python3 tools/verify_snippets.py /path/to/silica

Each snippet is checked with `silica check` and executed with `silica run`.
Snippets marked `expect_error` must fail with the expected message, and snippets
marked `expect_exit` must exit with that status. The exact stdout (or the exact
diagnostic) is written to tools/snippet_output.json for the site build, so the
documentation cannot drift from the language.

Exits non-zero if any snippet does not behave as recorded.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from snippets import SNIPPETS  # noqa: E402


def run(args, repo, stdin=""):
    return subprocess.run(
        [sys.executable, "-m", "silica"] + args,
        cwd=repo, capture_output=True, text=True, timeout=90, input=stdin,
    )


def diagnostic(result):
    text = (result.stderr or result.stdout).strip()
    lines = [line for line in text.splitlines() if line.strip()]
    return "\n".join(lines[:2])


def main(argv):
    repo = argv[1] if len(argv) > 1 else "/scratch/work/silica"
    work = os.path.join(HERE, ".snippet_work")
    os.makedirs(work, exist_ok=True)

    results = {}
    failures = []

    for name, entry in SNIPPETS.items():
        path = os.path.join(work, entry["file"])
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(entry["code"] + "\n")

        expected_error = entry.get("expect_error")
        check = run(["check", path], repo)

        if expected_error:
            if check.returncode != 0:
                message = diagnostic(check)
                if expected_error in message:
                    results[name] = {"output": message, "status": "compile error"}
                else:
                    failures.append((name, "check", "wrong message: " + message))
                continue
            # not a compile error: it must be a runtime one
            executed = run(["run", path], repo)
            message = diagnostic(executed)
            if executed.returncode != 0 and expected_error in message:
                results[name] = {"output": message, "status": "runtime error"}
            else:
                failures.append((name, "run", "expected an error, got: %r"
                                 % (executed.stdout or message)))
            continue

        if check.returncode != 0:
            failures.append((name, "check", diagnostic(check)))
            continue

        if entry.get("skip_run"):
            results[name] = {"output": None, "status": "checked only"}
            continue

        executed = run(["run", path], repo)
        expected_exit = entry.get("expect_exit", 0)
        if executed.returncode != expected_exit:
            failures.append((name, "run", "exit %d, expected %d: %s"
                             % (executed.returncode, expected_exit,
                                diagnostic(executed))))
            continue
        results[name] = {"output": executed.stdout.rstrip("\n"), "status": "ran"}

    out = os.path.join(HERE, "snippet_output.json")
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2, ensure_ascii=False)

    for name, stage, message in failures:
        print("FAIL %-22s %s: %s" % (name, stage, message))
    print("\n%d snippets: %d verified, %d failed"
          % (len(SNIPPETS), len(results), len(failures)))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
