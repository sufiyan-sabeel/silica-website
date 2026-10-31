"""Measure the rendered page at real viewport widths.

For each width this loads the page in headless Chromium, lets the scripts run,
and reads back a report written into document.title by an injected probe:

    <width>x<scrollWidth>|<overflowing elements>|<js errors>|<hero gap>

An element counts as overflowing when its right edge passes the viewport, which
is what actually produces a horizontal scrollbar on a phone.

    python3 tools/responsive_check.py [page]
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BROWSER = "chromium-headless-shell"
WIDTHS = [320, 360, 390, 430, 768, 1024, 1440]

with open(os.path.join(HERE, "probe.js"), encoding="utf-8") as _fh:
    PROBE = "<script>" + _fh.read() + "</script>"


def build_temp(page_path):
    with open(page_path, encoding="utf-8") as handle:
        html = handle.read()
    html = html.replace("</body>", PROBE + "</body>")
    # the probe file lives next to the page so relative asset URLs still resolve
    name = ".probe-" + os.path.basename(page_path)
    out = os.path.join(os.path.dirname(page_path), name)
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(html)
    return out


def measure(path, width):
    result = subprocess.run(
        [BROWSER, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
         "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
         "--virtual-time-budget=4000", "--window-size=%d,900" % width,
         "--dump-dom", "file://" + path],
        capture_output=True, text=True, timeout=120,
    )
    match = re.search(r"<title>(.*?)</title>", result.stdout, re.S)
    return " ".join(match.group(1).split()) if match else "(no probe captured)"


def main(argv):
    page = os.path.abspath(argv[1]) if len(argv) > 1 else os.path.join(ROOT, "index.html")
    temp = build_temp(page)
    label = os.path.basename(page)
    problems = 0
    try:
        print("measuring %s\n" % label)
        for width in WIDTHS:
            report = measure(temp, width)
            if "x" not in report.split("|")[0]:
                print("%-5d %s" % (width, report))
                continue
            vw, docw = report.split("|")[0].split("x")
            overflow = int(docw) - int(vw)
            flag = "ok " if overflow <= 0 else "OVERFLOW"
            print("%-5d %-8s doc=%s  %s" % (width, flag, docw, report.split("|", 1)[1]))
            if overflow > 0:
                problems += 1
    finally:
        os.remove(temp)
    print("\n%d of %d widths overflow" % (problems, len(WIDTHS)))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
