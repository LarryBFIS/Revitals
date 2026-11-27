#!/usr/bin/env python3
"""Inline assets/ into a single self-contained HTML file for sharing.

Usage:  python3 build.py
Output: dist/BYLD_Revenue_Operations.html
"""
import base64, mimetypes, pathlib, re

here = pathlib.Path(__file__).resolve().parent
html = (here / "index.html").read_text(encoding="utf-8")
cache = {}

def inline(m):
    path = m.group(1)
    if path not in cache:
        f = here / path
        mime = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
        cache[path] = f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()
    return cache[path]

out = re.sub(r"(assets/[\w.\-]+)", inline, html)
# The single file travels on its own (email, upload), so links to sibling pages go to the live site.
SITE = "https://marketing.buildfromideas.ai"
out = out.replace('href="revvitals-sample.html"', f'href="{SITE}/revvitals-sample" target="_blank" rel="noopener"')
out = out.replace('href="keycircle/"', f'href="{SITE}/keycircle" target="_blank" rel="noopener"')
dist = here / "dist"
dist.mkdir(exist_ok=True)
target = dist / "BYLD_Revenue_Operations.html"
target.write_text(out, encoding="utf-8")
print(f"Wrote {target.relative_to(here)} ({target.stat().st_size // 1024} KB, {len(cache)} assets inlined)")
