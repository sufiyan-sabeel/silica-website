"""Build the search-result favicon.

Google picks a favicon that is a square multiple of 48px (48, 96, 144, …) from a
stable, crawlable URL, and it renders it on a light background. The site's mark
is a light glyph for dark chrome, which would disappear there, so this draws the
mark on a rounded Midnight tile instead: readable on white, on black, and at
16px in a browser tab.

    python3 tools/make_favicon.py

Writes favicon.png (144x144) at the repository root.
"""

import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SIZE = 144
TILE = (11, 16, 32, 255)        # --bg from the site palette
RADIUS = 30


def build():
    tile = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tile)
    draw.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=RADIUS, fill=TILE)

    mark = Image.open(os.path.join(ROOT, "assets", "img", "mark-dark.png")).convert("RGBA")
    # the mark is taller than it is wide; fit it inside a square with margin
    target_h = int(SIZE * 0.66)
    target_w = int(mark.size[0] * target_h / mark.size[1])
    mark = mark.resize((target_w, target_h), Image.LANCZOS)

    tile.alpha_composite(
        mark,
        ((SIZE - target_w) // 2, (SIZE - target_h) // 2),
    )
    return tile


def main():
    icon = build()
    out = os.path.join(ROOT, "favicon.png")
    icon.save(out, optimize=True)
    print("wrote %s (%dx%d, %d bytes)" % (out, icon.size[0], icon.size[1], os.path.getsize(out)))

    # a 48px and a 96px copy for anyone who wants the exact sizes Google lists
    for size in (48, 96):
        small = icon.resize((size, size), Image.LANCZOS)
        small.save(os.path.join(ROOT, "favicon-%d.png" % size), optimize=True)
        print("wrote favicon-%d.png" % size)

    preview = Image.new("RGBA", (SIZE * 2 + 40, SIZE + 20), (255, 255, 255, 255))
    preview.alpha_composite(icon, (10, 10))
    dark = Image.new("RGBA", (SIZE, SIZE), (32, 33, 36, 255))
    dark.alpha_composite(icon)
    preview.paste(dark.convert("RGB"), (SIZE + 30, 10))
    preview.save("/scratch/work/favicon-preview.png")
    print("preview: /scratch/work/favicon-preview.png (light and dark background)")


if __name__ == "__main__":
    main()
