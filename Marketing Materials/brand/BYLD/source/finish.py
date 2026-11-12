#!/usr/bin/env python3
"""Build favicon.ico from the rendered PNGs and zip the pack. Run after render.js."""
import pathlib, zipfile
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
fav = ROOT / "favicon"
imgs = [Image.open(fav / f"favicon-{s}.png").convert("RGBA") for s in (16, 32, 48)]
imgs[-1].save(fav / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=imgs[:-1])

zpath = ROOT.parent / "BYLD-logo-pack.zip"
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(ROOT.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            z.write(f, pathlib.Path("BYLD-logo-pack") / f.relative_to(ROOT))
print("wrote", zpath.name, f"{zpath.stat().st_size // 1024} KB")
