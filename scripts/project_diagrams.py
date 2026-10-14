"""Method diagrams for CiteBench and the Agentic Development Workflow.

Usage: python scripts/project_diagrams.py OUT_DIR   (requires cairosvg)
Writes citebench.{svg,png} and agentic-workflow.{svg,png}; the site uses
WebP copies in assets/img/projects/.

Both render at 1600x1000 (16:10) with large type so they stay legible
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


if __name__ == "__main__":
    out = sys.argv[1]
    for name, fn in (("citebench", citebench), ("agentic-workflow", agentic)):
        svg = fn()
        open(f"{out}/{name}.svg", "w").write(svg)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=f"{out}/{name}.png",
                         output_width=W)
