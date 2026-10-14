"""Method diagrams for CiteBench, the Agentic Development Workflow, and the
Wasted Momentum deployment screening table.

Usage: python scripts/project_diagrams.py OUT_DIR   (requires cairosvg)
Writes citebench, agentic-workflow, and wasted-momentum-screening as
SVG and PNG; the site uses WebP copies in assets/img/projects/.

All render at 1600x1000 (16:10) with large type so they stay legible
when shown at roughly 480px wide on a project card.
"""
import sys
import cairosvg

INK = "#17191b"
MUTED = "#626970"
LINE = "#b8c0c4"
ACCENT = "#315d6b"
ACCENT_SOFT = "#e7eff1"
SURFACE = "#ffffff"
PAPER = "#f7f6f2"
WARN = "#a3542a"
WARN_SOFT = "#f6e9e1"
FONT = "Inter"

W, H = 1600, 1000


def head():
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="{FONT}">'
        f'<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker></defs>'
        f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>'
    )


def box(x, y, w, h, fill=SURFACE, stroke=LINE, sw=3, r=14):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def text(x, y, s, size=38, weight=500, fill=INK, anchor="middle"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" dominant-baseline="middle">{s}</text>')


def arrow(x1, y1, x2, y2, color=ACCENT, sw=4):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}" marker-end="url(#arr)"/>')


def citebench():
    s = [head()]
    s.append(text(60, 70, "Six extraction strategies, one schema, one scorer",
                  size=46, weight=700, anchor="start"))
    # source
    s.append(box(60, 400, 230, 200, fill=PAPER))
    s.append(text(175, 475, "Academic", size=38, weight=600))
    s.append(text(175, 525, "PDF", size=38, weight=600))
    # strategies
    strategies = ["Direct PDF", "Markdown cascade", "Visual page triage",
                  "Full text", "Targeted text", "Hybrid routing"]
    top, step, bh = 140, 130, 100
    sx, sw_ = 400, 420
    for i, name in enumerate(strategies):
        y = top + i * step
        s.append(arrow(290, 500, sx - 6, y + bh / 2, sw=3))
        s.append(box(sx, y, sw_, bh, fill=ACCENT_SOFT, stroke=ACCENT, sw=2))
        s.append(text(sx + sw_ / 2, y + bh / 2, name, size=36, weight=500))
    # schema
    cx = 930
    for i in range(6):
        y = top + i * step + bh / 2
        s.append(arrow(sx + sw_, y, cx - 6, 425 + i * 30, sw=3))
    s.append(box(cx, 400, 260, 200, fill=SURFACE, stroke=ACCENT, sw=4))
    s.append(text(cx + 130, 470, "Shared", size=38, weight=600))
    s.append(text(cx + 130, 530, "schema", size=38, weight=600))
    # scorer
    s.append(arrow(cx + 260, 500, 1284, 500))
    s.append(box(1290, 400, 250, 200, fill=SURFACE, stroke=ACCENT, sw=4))
    s.append(text(1415, 470, "Scored vs", size=36, weight=600))
    s.append(text(1415, 530, "silver labels", size=36, weight=600))
    # caveats
    s.append(box(1000, 680, 540, 120, fill=WARN_SOFT, stroke=WARN, sw=2))
    s.append(text(1270, 718, "Schema-valid is not useful:", size=30, weight=600, fill=WARN))
    s.append(text(1270, 760, "valid output, zero references", size=30, fill=INK))
    s.append(box(1000, 830, 540, 120, fill=WARN_SOFT, stroke=WARN, sw=2))
    s.append(text(1270, 868, "GROBID baseline is circular:", size=30, weight=600, fill=WARN))
    s.append(text(1270, 910, "GROBID also made the labels", size=30, fill=INK))
    s.append(text(60, 960, "705 recorded runs, 11 variants", size=30, fill=MUTED, anchor="start"))
    s.append("</svg>")
    return "".join(s)


def agentic():
    s = [head()]
    s.append(text(60, 70, "Planning and execution split by an approved brief",
                  size=46, weight=700, anchor="start"))
    stages = [
        ("PLANNING.md", "define it", "10 lock conditions"),
        ("PROJECT_BRIEF.md", "lock the scope", "fixed-schema contract"),
        ("EXECUTION.md", "build it", "5 workflows, 8 roles"),
        ("Artifacts", "verify it", "quality gates"),
    ]
    bw, bh, gap = 330, 250, 60
    x0, y0 = 60, 180
    for i, (name, verb, detail) in enumerate(stages):
        x = x0 + i * (bw + gap)
        mid = i in (1,)
        s.append(box(x, y0, bw, bh, fill=ACCENT_SOFT if mid else SURFACE,
                     stroke=ACCENT, sw=4 if mid else 3))
        s.append(text(x + bw / 2, y0 + 70, name, size=29 if len(name) > 13 else 38,
                      weight=700, fill=ACCENT))
        s.append(text(x + bw / 2, y0 + 140, verb, size=38, weight=600))
        s.append(text(x + bw / 2, y0 + 200, detail, size=28, fill=MUTED))
        if i < len(stages) - 1:
            s.append(arrow(x + bw + 4, y0 + bh / 2, x + bw + gap - 6, y0 + bh / 2))
    # human gates
    gy = 640
    s.append(text(60, 570, "Human approval gates", size=38, weight=700, anchor="start"))
    s.append(f'<line x1="80" y1="{gy}" x2="1520" y2="{gy}" stroke="{LINE}" stroke-width="4"/>')
    gates = ["Planning", "Architecture", "Review", "Interpretation", "Release"]
    for i, g in enumerate(gates):
        gx = 140 + i * 330
        s.append(f'<rect x="{gx-22}" y="{gy-22}" width="44" height="44" '
                 f'transform="rotate(45 {gx} {gy})" fill="{ACCENT}"/>')
        s.append(text(gx, gy + 70, g, size=32, weight=500))
    # amendment loop note
    s.append(box(60, 800, 1480, 140, fill=PAPER, stroke=LINE, sw=2))
    s.append(text(800, 850, "Scope changes need a documented, human-approved amendment",
                  size=34, weight=600))
    s.append(text(800, 900, "Reviewer roles run in fresh contexts, so agents do not grade their own work",
                  size=30, fill=MUTED))
    s.append("</svg>")
    return "".join(s)


def screening():
    """Deployment screening table from the Wasted Momentum white paper, section 4.

    Cell shading marks whether each value favors vehicle-hosted compute;
    every cell is also labeled, so the meaning never rests on color alone.
    """
    fav, mid, unf = "#d4e5ea", "#efefeb", WARN_SOFT
    rows = [
        ("Emergency response", [("Absent", fav), ("Tight", fav), ("High", fav), ("High", fav), ("Very high", fav)], "Strong"),
        ("Defense, expeditionary", [("Contested", fav), ("Tight", fav), ("High", fav), ("High", fav), ("Very high", fav)], "Strong"),
        ("Remote inspection", [("Poor", fav), ("Moderate", mid), ("High", fav), ("High", fav), ("High", fav)], "Strong"),
        ("Precision agriculture", [("Poor", fav), ("Moderate", mid), ("High", fav), ("High", fav), ("High", fav)], "Strong"),
        ("Campus fleets", [("Good", unf), ("Loose", unf), ("Moderate", mid), ("Moderate", mid), ("Low", unf)], "Pilot testbed"),
        ("Long-haul logistics", [("Variable", mid), ("Loose", unf), ("Low", unf), ("High", fav), ("Low", unf)], "Conditional"),
        ("Rideshare, consumer", [("Good", unf), ("Loose", unf), ("Low", unf), ("Low", unf), ("Low", unf)], "Weak"),
    ]
    heads = [("Backhaul", "access"), ("Latency", "need"), ("Edge", "data"),
             ("Incidental", "runtime"), ("Alt. infra", "cost")]
    fit_style = {
        "Strong": (ACCENT, SURFACE),
        "Pilot testbed": (mid, INK),
        "Conditional": (mid, INK),
        "Weak": (WARN, SURFACE),
    }
    s = [head()]
    s.append(text(60, 66, "Deployment screening: strongest where connectivity is the constraint",
                  size=40, weight=700, anchor="start"))
    x0, label_w, col_w, fit_w = 60, 410, 172, 230
    y0, head_h, row_h, gap = 130, 104, 92, 6
    for j, (a, b) in enumerate(heads):
        cx = x0 + label_w + j * col_w + col_w / 2
        s.append(text(cx, y0 + 34, a, size=28, weight=600))
        s.append(text(cx, y0 + 70, b, size=28, weight=600))
    fx = x0 + label_w + 5 * col_w + 12
    s.append(text(fx + fit_w / 2, y0 + 52, "Fit", size=30, weight=700))
    for i, (name, cells, fit) in enumerate(rows):
        y = y0 + head_h + i * row_h
        s.append(text(x0, y + row_h / 2 - gap / 2, name, size=31, weight=600, anchor="start"))
        for j, (val, fill) in enumerate(cells):
            cx = x0 + label_w + j * col_w
            s.append(box(cx + gap / 2, y, col_w - gap, row_h - gap, fill=fill, stroke=fill, sw=0, r=8))
            s.append(text(cx + col_w / 2, y + row_h / 2 - gap / 2, val, size=27))
        bg, fg = fit_style[fit]
        s.append(box(fx, y, fit_w, row_h - gap, fill=bg, stroke=bg, sw=0, r=8))
        s.append(text(fx + fit_w / 2, y + row_h / 2 - gap / 2, fit, size=28, weight=700, fill=fg))
    ly = y0 + head_h + len(rows) * row_h + 40
    lx = x0
    for label, fill in (("Favors vehicle compute", fav), ("Mixed", mid), ("Favors centralized compute", unf)):
        s.append(box(lx, ly - 16, 32, 32, fill=fill, stroke=fill, sw=0, r=6))
        s.append(text(lx + 46, ly, label, size=26, fill=MUTED, anchor="start"))
        lx += 46 + len(label) * 14 + 60
    s.append("</svg>")
    return "".join(s)


if __name__ == "__main__":
    out = sys.argv[1]
    for name, fn in (("citebench", citebench), ("agentic-workflow", agentic),
                     ("wasted-momentum-screening", screening)):
        svg = fn()
        open(f"{out}/{name}.svg", "w").write(svg)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=f"{out}/{name}.png",
                         output_width=W)
