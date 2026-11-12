#!/usr/bin/env python3
"""Generate the BYLD logo SVGs from one set of outlined glyph shapes.

Usage:  python3 build_logo.py            -> writes ../svg/*.svg
Then:   node render.js                    -> PNG, PDF and the brand guide (needs Playwright)
        python3 finish.py                 -> favicon.ico and the zip

Every shape is a filled path (no strokes, no fonts), so the files open the
same in Illustrator, Figma, browsers and print RIPs. Units: cap height = 100.
"""
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "svg"

NIGHT, SKY, WHITE = "#12163A", "#5CC0FF", "#FFFFFF"

# Glyphs, each at its own origin (top-left of the cap height).
# B: one outer contour (two bowls meeting at 72.16, 47.78) and two counters.
B = ("M0 0H48A30 30 0 0 1 72.16 47.78A30 30 0 0 1 52 100H0Z "
     "M20 20V40H48A10 10 0 0 0 48 20Z M20 60V80H52A10 10 0 0 0 52 60Z")
Y_STEM = "M6.68 0H29.94L58 47.26V100H38V52.74Z"          # left arm + stem
Y_ARROW = "M42 41.33L76 -4L66.4 -11.2L103.2 -23.6L101.6 15.2L92 8L58 53.33Z"  # rising right arm; base sits flush on the stem edge
L = "M0 0H20V80H72V100H0Z"
D = "M0 0H45A50 50 0 0 1 45 100H0Z M20 20V80H45A30 30 0 0 0 45 20Z"

WORD_POS = {"B": (0, 0), "Y": (98, 0), "L": (210, 0), "D": (298, 0)}
STACK_POS = {"B": (0, 0), "Y": (100, 0), "L": (0, 124), "D": (100, 124)}
SHAPES = {"B": B, "Y": Y_STEM, "L": L, "D": D}


def letters(pos, ink, arrow):
    out = [f'<g fill="{ink}" fill-rule="evenodd">']
    for k in "BYLD":
        x, y = pos[k]
        out.append(f'  <path transform="translate({x} {y})" d="{SHAPES[k]}"/>')
    out.append("</g>")
    x, y = pos["Y"]
    out.append(f'<path fill="{arrow}" transform="translate({x} {y})" d="{Y_ARROW}"/>')
    return "\n".join(out)


def svg(viewbox, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" aria-label="{title}">\n'
            f"<title>{title}</title>\n{body}\n</svg>\n")


WORD_VB = "0 -24 394 124"   # tight to the artwork; the arrow tip rises 24 units above the cap height


def icon(bg, ink, arrow, radius=56):
    return (f'<rect width="200" height="200" rx="{radius}" fill="{bg}"/>'
            f'\n<g transform="translate(49 50) scale(0.5)">\n{letters(STACK_POS, ink, arrow)}\n</g>')


# The brand lives on dark backgrounds only.
# "on-dark" files carry the background and the clear space (half the letter height) built in.
ON_DARK_VB = "-50 -74 494 224"
on_dark = f'<rect x="-50" y="-74" width="494" height="224" fill="{NIGHT}"/>\n' + letters(WORD_POS, WHITE, SKY)

FILES = {
    "byld-logo.svg":         svg(WORD_VB, letters(WORD_POS, WHITE, SKY), "BYLD"),
    "byld-logo-on-dark.svg": svg(ON_DARK_VB, on_dark, "BYLD"),
    "byld-logo-white.svg":   svg(WORD_VB, letters(WORD_POS, WHITE, WHITE), "BYLD"),
    "byld-icon.svg":         svg("0 0 200 200", icon(NIGHT, WHITE, SKY), "BYLD"),
    "favicon.svg":           svg("0 0 200 200", icon(NIGHT, WHITE, SKY, radius=44), "BYLD"),
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, text in FILES.items():
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", (OUT / name).relative_to(HERE.parent))
