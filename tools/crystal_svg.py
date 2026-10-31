"""Generate the static SVG crystal used as the hero's no-WebGL fallback.

It is the same icosahedron the WebGL scene draws, projected with the same camera
and shaded with the same palette, so the fallback is the same object rather than
a different picture. Emitted inline by the page builder: no extra request, no
layout shift, sharp at any size, and it inherits the theme's CSS variables.
"""

import math

# --- geometry (identical to assets/js/crystal.js) ---------------------------
T = (1 + math.sqrt(5)) / 2
RAW = [
    (-1, T, 0), (1, T, 0), (-1, -T, 0), (1, -T, 0),
    (0, -1, T), (0, 1, T), (0, -1, -T), (0, 1, -T),
    (T, 0, -1), (T, 0, 1), (-T, 0, -1), (-T, 0, 1),
]
FACES = [
    (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
    (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
    (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
    (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1),
]

VERTICES = []
for x, y, z in RAW:
    length = math.sqrt(x * x + y * y + z * z)
    VERTICES.append((x / length, y / length, z / length))


def rotate(point, rx, ry):
    x, y, z = point
    cx, sx = math.cos(rx), math.sin(rx)
    y, z = y * cx - z * sx, y * sx + z * cx
    cy, sy = math.cos(ry), math.sin(ry)
    x, z = x * cy + z * sy, -x * sy + z * cy
    return (x, y, z)


def project(point, size=100.0, distance=2.72, fov=0.72):
    """Perspective projection into a 0..size square."""
    x, y, z = point
    z = z + distance
    f = 1.0 / math.tan(fov / 2.0)
    scale = size * 0.42
    px = (x * f / z) * scale
    py = (-y * f / z) * scale
    return (size / 2 + px, size / 2 + py)


def face_normal(a, b, c):
    """Outward normal. The faces are wound clockwise seen from outside, so the
    cross product of (c - a) and (b - a) points away from the centre."""
    u = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    v = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    length = math.sqrt(sum(c * c for c in n)) or 1.0
    return (n[0] / length, n[1] / length, n[2] / length)


def _shell(rx, ry, scale, size):
    """Projected facets of the icosahedron at a given rotation and scale."""
    rotated = [rotate(v, rx, ry) for v in VERTICES]
    rotated = [(x * scale, y * scale, z * scale) for x, y, z in rotated]
    out = []
    for face in FACES:
        a, b, c = (rotated[i] for i in face)
        centre = tuple((a[i] + b[i] + c[i]) / 3.0 for i in range(3))
        normal = face_normal(a, b, c)
        # the camera sits at (0, 0, -distance) in this space; project() adds the
        # distance, so the view vector has to include that offset
        view = (-centre[0], -centre[1], -2.72 - centre[2])
        vlen = math.sqrt(sum(c * c for c in view)) or 1.0
        view = tuple(c / vlen for c in view)
        facing = sum(normal[i] * view[i] for i in range(3))
        key = max(0.0, sum(normal[i] * k for i, k in enumerate((-0.45, 0.75, 0.65))))
        out.append({
            "points": [project(p, size) for p in (a, b, c)],
            "depth": sum(p[2] for p in (a, b, c)) / 3.0,
            "facing": facing,
            "key": key,
        })
    return out


def build(rx=-0.22, ry=0.55, size=100.0):
    parts = [
        '<svg class="stage__fallback" viewBox="0 0 %d %d" role="img" '
        'aria-label="A translucent crystalline icosahedron: the Silica mark in three dimensions" '
        'xmlns="http://www.w3.org/2000/svg">' % (size, size),
        "<defs>",
        '<radialGradient id="cr-halo" cx="50%" cy="46%" r="50%">',
        '<stop offset="0%" stop-color="var(--accent)" stop-opacity="0.22"/>',
        '<stop offset="55%" stop-color="var(--accent)" stop-opacity="0.06"/>',
        '<stop offset="100%" stop-color="var(--accent)" stop-opacity="0"/>',
        "</radialGradient>",
        '<linearGradient id="cr-face" x1="18%" y1="6%" x2="82%" y2="96%">',
        '<stop offset="0%" stop-color="var(--accent-strong)"/>',
        '<stop offset="48%" stop-color="var(--accent)"/>',
        '<stop offset="100%" stop-color="var(--violet)"/>',
        "</linearGradient>",
        '<linearGradient id="cr-core" x1="20%" y1="10%" x2="80%" y2="90%">',
        '<stop offset="0%" stop-color="var(--accent-strong)"/>',
        '<stop offset="100%" stop-color="var(--violet)"/>',
        "</linearGradient>",
        "</defs>",
        '<circle cx="%g" cy="%g" r="%g" fill="url(#cr-halo)"/>'
        % (size / 2, size / 2, size * 0.5),
    ]

    # inner solid: gives the object depth behind the translucent shell
    inner = _shell(rx + 0.1, ry * -0.7, 0.5, size)
    inner.sort(key=lambda f: f["depth"])
    for facet in inner:
        if facet["facing"] <= 0.02:
            continue
        points = " ".join("%.2f,%.2f" % p for p in facet["points"])
        parts.append(
            '<polygon points="%s" fill="url(#cr-core)" fill-opacity="%.3f"/>'
            % (points, 0.42 + facet["key"] * 0.34)
        )

    # outer shell: translucent facets, back to front
    outer = _shell(rx, ry, 1.0, size)
    outer.sort(key=lambda f: f["depth"])
    for facet in outer:
        if facet["facing"] <= 0.0:
            continue
        points = " ".join("%.2f,%.2f" % p for p in facet["points"])
        parts.append(
            '<polygon points="%s" fill="url(#cr-face)" fill-opacity="%.3f" '
            'stroke="var(--accent-strong)" stroke-opacity="%.3f" stroke-width="0.22"/>'
            % (points, 0.16 + facet["key"] * 0.34, 0.1 + facet["key"] * 0.22)
        )

    # silhouette: the outline of the whole solid, so the shape always reads
    silhouette = [p for p in (project(rotate(v, rx, ry), size) for v in VERTICES)]
    hull = _convex_hull(silhouette)
    parts.append(
        '<polygon points="%s" fill="none" stroke="var(--accent-strong)" '
        'stroke-opacity="0.6" stroke-width="0.5" stroke-linejoin="round"/>'
        % " ".join("%.2f,%.2f" % p for p in hull)
    )

    parts.append("</svg>")
    return "".join(parts)


def _convex_hull(points):
    """Andrew's monotone chain — the silhouette of the projected vertices."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


if __name__ == "__main__":
    import sys
    out = build()
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as handle:
            handle.write(out)
        print("wrote %s (%d bytes)" % (sys.argv[1], len(out)))
    else:
        print(out)
