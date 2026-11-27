#!/usr/bin/env python3
"""Build the BYLD website into public/.

    python3 build.py

No dependencies beyond Pillow (for image optimisation). Copy lives in content.py.
"""
import hashlib, html, json, pathlib, shutil
from datetime import date

from content import (SITE, STATS, BRANDS, PRODUCTS, GROUPS, COMING, FRANCHISE_ROWS, AI_HUMAN, STEPS,
                     DATA_FLOW, PARTNERS, HOME_FAQ, FRANCHISE_FAQ)

import interactive as ix

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "public"
STATIC = ROOT / "static"
TODAY = date.today().isoformat()
BY_SLUG = {p["slug"]: p for p in PRODUCTS}
e = html.escape

# ----------------------------------------------------------------------------- helpers
ICON = {
    "arrow": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>',
    "check": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="10" r="8.2" opacity=".25"/><path d="M6.5 10.2l2.3 2.3 4.7-4.9"/></svg>',
    "minus": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="10" cy="10" r="8.2" opacity=".35"/><path d="M6.5 10h7"/></svg>',
    "chev": '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M3 4.5l3 3 3-3"/></svg>',
    "menu": '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M3 6h14M3 14h14"/></svg>',
    "mail": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="2.5" y="4.5" width="15" height="11" rx="2"/><path d="M3 5.5l7 5 7-5"/></svg>',
    "pin": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M10 18s6-5.2 6-10a6 6 0 10-12 0c0 4.8 6 10 6 10z"/><circle cx="10" cy="8" r="2.2"/></svg>',
    "key": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="6.5" cy="13.5" r="3.5"/><path d="M9 11l7-7M14 6l2 2M12 8l1.5 1.5"/></svg>',
}
PICONS = {  # one glyph per product, 20x20, stroke
    "bfis-pms": '<rect x="3" y="4" width="14" height="12" rx="2"/><path d="M3 8h14M8 8v8"/>',
    "pricecortex": '<path d="M3 15l4-5 3 3 7-8"/><path d="M13 5h4v4"/>',
    "compmatrix": '<path d="M4 16V9M10 16V4M16 16v-5"/>',
    "foliolens": '<circle cx="9" cy="9" r="5"/><path d="M13 13l4 4M7 10l1.5-2 1.5 1.5L11.5 7"/>',
    "revvitals": '<path d="M2 10h3l2-5 3 10 2-6 1.5 1H18"/>',
    "otarecon365": '<path d="M16 7a7 7 0 10.8 5"/><path d="M17 3v4h-4"/><path d="M10 7v3l2 1.5"/>',
    "goldkey-rewards": '<circle cx="6.5" cy="13.5" r="3.5"/><path d="M9 11l7-7M14 6l2 2M12 8l1.5 1.5"/>',
    "saleslock": '<rect x="4" y="9" width="12" height="8" rx="2"/><path d="M7 9V6.5a3 3 0 016 0V9"/>',
    "askrank": '<circle cx="9" cy="9" r="5.5"/><path d="M13 13l4 4"/>',
    "pulsepilot": '<path d="M10 16.5s-6-3.6-6-8.2A3.3 3.3 0 0110 6a3.3 3.3 0 016 2.3c0 4.6-6 8.2-6 8.2z"/>',
    "direct-booking": '<circle cx="10" cy="10" r="7"/><path d="M3 10h14M10 3c2 2.2 2.8 4.5 2.8 7s-.8 4.8-2.8 7c-2-2.2-2.8-4.5-2.8-7S8 5.2 10 3z"/>',
}

def picon(slug):
    return f'<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{PICONS[slug]}</svg>'

def pname(p, plain=False):
    """Product name with the trademark sign after the first word."""
    name = p["name"]
    if not p.get("tm"):
        return name if plain else e(name)
    first, _, rest = name.partition(" ")
    if plain:
        return f"{first}™" + (f" {rest}" if rest else "")
    return f'{e(first)}<span class="tm">™</span>' + (f" {e(rest)}" if rest else "")

def nav_name(p):
    return e(p["nav_name"]) if p.get("nav_name") else pname(p)

def badge(status):
    s = status.lower()
    cls = "live" if s == "live" else "soon" if s.startswith("launch") else "svc" if s == "service" else "pilot"
    return f'<span class="badge {cls}">{e(status)}</span>'

def href(target):
    """CTA target: a SITE key (external) or a site path."""
    if target in SITE:
        return SITE[target], True
    return target, False

def a_btn(label, target, cls="btn-primary", arrow=True):
    url, ext = href(target)
    rel = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="btn {cls}" href="{e(url)}"{rel}>{e(label)}{ICON["arrow"] if arrow else ""}</a>'

IMG_SIZES = {}

def picture(name, alt, sizes="(max-width: 980px) 100vw, 640px", eager=False):
    w, h = IMG_SIZES[name]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/webp" srcset="/img/{name}.webp"><img src="/img/{name}.jpg" '
            f'width="{w}" height="{h}" alt="{e(alt)}" {load} sizes="{sizes}"></picture>')

def window(inner, bar, live=True, label="Live product"):
    em = f'<em>{label}</em>' if live else '<em style="color:#8A92A6">Illustrative</em>'
    return f'<div class="window"><div class="window-bar"><i></i><i></i><i></i><span>{e(bar)}</span>{em}</div>{inner}</div>'

# ----------------------------------------------------------------------------- mocks
MOCKS = {
"foliolens": ("FolioLens · Month to date", '''<div class="mock">
<div class="row"><span class="lbl">Month to date · vs plan</span><span class="tag ok">Ahead of plan</span></div>
<div class="kpis"><div><b>78%</b><small>Occupancy</small></div><div><b>$132</b><small>ADR</small></div><div><b>$103</b><small>RevPAR</small></div></div>
<svg class="spark" viewBox="0 0 300 90" preserveAspectRatio="none" aria-hidden="true"><path d="M0 70 L30 64 60 66 90 52 120 55 150 40 180 44 210 30 240 34 270 22 300 18" fill="none" stroke="#0A7BD1" stroke-width="2.5"/><path d="M0 62 L300 30" fill="none" stroke="#7C8CFF" stroke-width="1.5" stroke-dasharray="5 5"/><path d="M0 76 L30 72 60 74 90 66 120 68 150 58 180 62 210 52 240 55 270 46 300 44" fill="none" stroke="#B4BAC8" stroke-width="1.5"/></svg>
<div class="row" style="font-size:12px;color:#5E6679"><span><b style="color:#0A7BD1">━</b> Actual &nbsp; <b style="color:#7C8CFF">┅</b> Plan &nbsp; <b style="color:#B4BAC8">━</b> Last year</span></div>
<div class="row"><span>RGI vs CoStar STR market</span><b>112.4</b></div>
<div class="row"><span>Weekly Performance Brief</span><span class="tag ok">Checked · sent Mon 7:00</span></div>
<div class="note">ILLUSTRATIVE</div></div>'''),
"revvitals": ("RevVitals · Health check", '''<div class="mock">
<span class="lbl">Health check</span>
<div class="grades"><div><b style="color:#0E8F63">A</b><small>Pricing</small></div><div><b style="color:#9A6205">B−</b><small>Distribution</small></div><div><b style="color:#C2334A">C+</b><small>OTA marketing</small></div><div><b style="color:#0E8F63">B+</b><small>Market</small></div></div>
<div class="row"><span>Expedia Accelerator</span><span class="tag ok">Active</span></div>
<div class="row"><span>Booking.com Genius</span><span class="tag ok">Active</span></div>
<div class="row"><span>Visibility Booster</span><span class="tag info">Recommended</span></div>
<div class="row"><span>Refresh OTA photos</span><span class="tag ok">Done</span></div>
<div class="row"><span>Last-minute deal on Expedia</span><span class="tag warn">Awaiting approval</span></div>
<div class="note">ILLUSTRATIVE</div></div>'''),
"otarecon": ("OTARecon365 · Recovery queue", '''<div class="mock">
<div class="row"><span class="lbl">Recovered this month</span><span class="tag ok">Live queue</span></div>
<div class="big" style="margin:6px 0 10px">$4,812</div>
<div class="row"><span>OTA 1 · Virtual card not charged<br><small style="color:#8A92A6">$412</small></span><span class="tag ok">Recovered</span></div>
<div class="row"><span>OTA 2 · Payout short vs folio<br><small style="color:#8A92A6">$186</small></span><span class="tag info">Claimed</span></div>
<div class="row"><span>OTA 1 · No-show fee unpaid<br><small style="color:#8A92A6">$129</small></span><span class="tag info">Claimed</span></div>
<div class="row"><span>OTA 3 · Cancelled, card expiring<br><small style="color:#8A92A6">$94</small></span><span class="tag bad">Expires in 2 days</span></div>
<div class="note">ILLUSTRATIVE</div></div>'''),
"goldkey": ("GoldKey Rewards · Member card", '''<div class="mock" style="background:linear-gradient(160deg,#141833,#0B0E24);color:#fff">
<div class="gk-card"><div class="t"><span>GOLDKEY</span><span>CORE</span></div><div class="nm">ALEX MORGAN</div><div class="ft"><span>MEMBER NO. 1001</span><span>MEMBER SINCE 2026</span></div></div>
<div class="gk-tiers" style="color:#fff"><div style="border-color:rgba(255,255,255,.12)"><b>Core</b>On joining</div><div style="border-color:rgba(255,255,255,.12)"><b>Platinum</b>10 nights</div><div style="border-color:rgba(255,255,255,.12)"><b>Executive</b>30 nights</div><div style="border-color:rgba(255,255,255,.12)"><b>Black</b>Invitation</div></div>
<div class="note" style="color:#8790AE">ILLUSTRATIVE</div></div>'''),
"saleslock": ("SalesLock · Group pipeline", '''<div class="mock">
<div class="row"><span class="lbl">Group pipeline</span><span class="tag ok">Missed RFPs: 0</span></div>
<div class="pipe">
<div><span class="lbl">New</span><div class="lead">Wedding block<small>12 rooms · Jun</small></div><div class="lead">Construction crew<small>8 rooms · 6 wks</small></div></div>
<div><span class="lbl">Quoted</span><div class="lead">Youth sports team<small>15 rooms · Mar</small></div></div>
<div><span class="lbl">Negotiating</span><div class="lead">Corporate training<small>10 rooms · 3 nts</small></div></div>
<div><span class="lbl">Won</span><div class="lead">Church retreat<small>18 rooms · $6.8K</small></div></div>
</div><div class="note">ILLUSTRATIVE</div></div>'''),
"askrank": ("AskRank · Visibility", '''<div class="mock">
<span class="lbl">Ask an AI assistant</span>
<div class="chat" style="margin:10px 0 14px">“Best place to stay near downtown for a work trip?”</div>
<div class="row"><span>ChatGPT visibility</span><b>78</b></div><div class="bar"><i style="width:78%"></i></div>
<div class="row" style="margin-top:8px"><span>Gemini visibility</span><b>64</b></div><div class="bar"><i style="width:64%"></i></div>
<div class="row" style="margin-top:8px"><span>Google Business Profile</span><span class="tag ok">Campaign live</span></div>
<div class="row"><span>Expedia sponsored listing</span><span class="tag warn">Awaiting budget approval</span></div>
<div class="note">AI VISIBILITY COMING NEXT · ILLUSTRATIVE</div></div>'''),
"pulsepilot": ("PulsePilot · Guest feedback", '''<div class="mock">
<div class="row"><span class="lbl">Guest feedback</span><span class="tag ok">Live</span></div>
<div class="fb"><div class="row" style="padding:0;border:0"><span class="lbl">Room QR</span><span class="stars">★★☆☆☆</span></div><p>AC in room 214 is noisy. Photo attached.</p><span class="tag bad">GM alerted 9:42 pm</span> <span class="tag ok">Resolved before checkout</span></div>
<div class="fb"><div class="row" style="padding:0;border:0"><span class="lbl">Breakfast QR</span><span class="stars">★★★★★</span></div><p>Fresh waffles and a really friendly team.</p><span class="tag info">Invited to Google</span></div>
<div class="note">ILLUSTRATIVE</div></div>'''),
"booking": ("yourhotel.com · Book direct", '''<div class="mock">
<div class="row"><span class="lbl">Book direct · best rate</span><span class="tag ok">Synced with PMS</span></div>
<div class="kpis"><div><small>Check in</small><b style="font-size:17px">Fri 12</b></div><div><small>Check out</small><b style="font-size:17px">Sun 14</b></div><div><small>Guests</small><b style="font-size:17px">2</b></div></div>
<div class="row"><span><b>King Room</b><br><small style="color:#8A92A6">Free cancellation</small></span><b>$144</b></div>
<div class="row"><span><b>King Room · GoldKey member</b><br><small style="color:#8A92A6">Code applied: 15% off</small></span><b style="color:#0E8F63">$122</b></div>
<div class="row"><span><b>Two Queen Suite</b></span><b>$189</b></div>
<div class="note">ILLUSTRATIVE</div></div>'''),
}

def product_visual(p, eager=False):
    v = p["visual"]
    if v["type"] == "shot":
        return window(picture(v["src"], v["alt"], eager=eager), v["bar"], label=v.get("label", "Live product"))
    bar, inner = MOCKS[v["name"]]
    return window(inner, bar, live=False)

# ----------------------------------------------------------------------------- chrome
def header(active=""):
    cols = []
    for g in GROUPS:
        items = "".join(
            f'<a href="/products/{p["slug"]}"><b>{nav_name(p)}</b><span>{e(p["short"])}</span></a>'
            for p in PRODUCTS if p["group"] == g)
        cols.append((g, items))
    # 3 columns: [Foundation + Price&compete], [Report&improve + Recover&retain], [Sell & be seen]
    col = lambda *gs: '<div>' + "".join(f'<h6>{e(g)}</h6>{dict(cols)[g]}' for g in gs) + '</div>'
    mega = (col("Foundation", "Price & compete") + col("Report & improve", "Recover & retain") + col("Sell & be seen")
            + f'<div class="mega-foot"><span>One platform. One owner portal. A named revenue manager.</span><a class="link" href="/platform">See the whole platform {ICON["arrow"]}</a></div>')
    cur = lambda k: ' aria-current="page"' if active == k else ""
    mob = "".join(f'<h6>{e(g)}</h6><div class="sub">' + "".join(
        f'<a href="/products/{p["slug"]}">{nav_name(p)}</a>' for p in PRODUCTS if p["group"] == g) + '</div>' for g in GROUPS)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap hdr-in">
  <a class="logo" href="/" aria-label="BYLD, Buildd From Ideas, home"><img src="/img/byld-logo.svg" alt="BYLD" width="70" height="22"><span>Buildd From Ideas</span></a>
  <nav class="nav" aria-label="Main">
    <div class="dd"><button type="button" aria-expanded="false" aria-haspopup="true">Platform{ICON["chev"]}</button><div class="mega">{mega}</div></div>
    <a href="/why-byld"{cur("why")}>Why BYLD</a>
    <a href="/how-it-works"{cur("how")}>How it works</a>
    <a href="/partners"{cur("partners")}>Partners</a>
    <a href="/revvitals-sample">Sample report</a>
  </nav>
  <div class="hdr-cta">
    <button class="theme-btn" type="button" data-theme-toggle aria-label="Switch to light theme" title="Light / dark"><svg class="i-moon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16.5 12.3A7 7 0 017.7 3.5a7 7 0 108.8 8.8z"/></svg><svg class="i-sun" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="10" cy="10" r="3.6"/><path d="M10 1.8v2M10 16.2v2M1.8 10h2M16.2 10h2M4.2 4.2l1.4 1.4M14.4 14.4l1.4 1.4M4.2 15.8l1.4-1.4M14.4 5.6l1.4-1.4"/></svg></button>
    <a class="login" href="{SITE["portal"]}" target="_blank" rel="noopener">Owner login</a>
    <a class="btn btn-primary btn-sm" href="/contact">Book a revenue review</a>
  </div>
  <div class="burger-wrap"><button class="theme-btn" type="button" data-theme-toggle aria-label="Switch to light theme" title="Light / dark"><svg class="i-moon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16.5 12.3A7 7 0 017.7 3.5a7 7 0 108.8 8.8z"/></svg><svg class="i-sun" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="10" cy="10" r="3.6"/><path d="M10 1.8v2M10 16.2v2M1.8 10h2M16.2 10h2M4.2 4.2l1.4 1.4M14.4 14.4l1.4 1.4M4.2 15.8l1.4-1.4M14.4 5.6l1.4-1.4"/></svg></button><button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mnav">{ICON["menu"]}</button></div>
</div></header>
<div class="mnav" id="mnav">
  <a href="/platform">Platform overview</a><a href="/why-byld">Why BYLD</a><a href="/how-it-works">How it works</a><a href="/partners">Partners</a><a href="/revvitals-sample">Sample report</a>
  {mob}
  <h6>Log in</h6><div class="sub"><a href="{SITE["portal"]}" target="_blank" rel="noopener">Owner portal</a><a href="{SITE["pms_login"]}" target="_blank" rel="noopener">BFIS PMS</a></div>
  <a class="btn btn-primary" href="/contact">Book a revenue review</a>
</div>'''

def footer():
    a = SITE["address"]
    prod = "".join(f'<li><a href="/products/{p["slug"]}">{nav_name(p)}</a></li>' for p in PRODUCTS[:6])
    prod2 = "".join(f'<li><a href="/products/{p["slug"]}">{nav_name(p)}</a></li>' for p in PRODUCTS[6:])
    return f'''<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
  <div><a class="logo" href="/"><img src="/img/byld-logo.svg" alt="BYLD" width="76" height="24"></a>
    <p class="about">Buildd From Ideas runs hotel revenue operations on one platform. More than a franchise gives you, without the franchise fees.</p>
    <p class="about" style="margin-top:14px">{e(a["street"])}<br>{e(a["city"])}, {e(a["region"])} {e(a["postal"])}</p></div>
  <div><h5>Platform</h5><ul>{prod}</ul></div>
  <div><h5>&nbsp;</h5><ul>{prod2}</ul></div>
  <div><h5>Company</h5><ul><li><a href="/why-byld">Why BYLD</a></li><li><a href="/how-it-works">How it works</a></li><li><a href="/partners">Partners</a></li><li><a href="/revvitals-sample">Sample report</a></li><li><a href="/contact">Contact</a></li></ul></div>
  <div><h5>Log in</h5><ul><li><a href="{SITE["portal"]}" target="_blank" rel="noopener">Owner portal</a></li><li><a href="{SITE["pms_login"]}" target="_blank" rel="noopener">BFIS PMS</a></li><li><a href="{SITE["pricing_explainer"]}" target="_blank" rel="noopener">How PriceCortex prices</a></li></ul></div>
</div>
<div class="ftr-bot"><span>© {date.today().year} Buildd From Ideas · BYLD · {e(SITE["tagline"])}</span><span>BFIS, PriceCortex, CompMatrix, FolioLens, RevVitals, OTARecon365, GoldKey, SalesLock, AskRank, PulsePilot, Halo and Signal are trademarks of Buildd From Ideas.</span></div>
</div></footer>'''

ORG_LD = {
    "@type": "Organization", "@id": SITE["url"] + "/#org", "name": SITE["name"], "alternateName": "BYLD",
    "url": SITE["url"], "logo": SITE["url"] + "/img/byld-icon-512.png", "slogan": SITE["tagline"],
    "description": SITE["description"],
    "address": {"@type": "PostalAddress", "streetAddress": SITE["address"]["street"], "addressLocality": SITE["address"]["city"],
                "addressRegion": SITE["address"]["region"], "postalCode": SITE["address"]["postal"], "addressCountry": SITE["address"]["country"]},
    "email": SITE["email"],
    "knowsAbout": ["Hotel revenue management", "Hotel property management systems", "Hotel dynamic pricing", "OTA distribution",
                   "Hotel loyalty programs", "Hotel group sales", "Hotel reputation management", "Hotel franchise alternatives"],
}

def crumbs_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE["url"] + u} for i, (n, u) in enumerate(trail)]}

def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

PAGES = []  # (path, priority) for the sitemap

def page(path, title, desc, body, *, active="", ld=None, og=None, priority="0.7", noindex=False):
    url = SITE["url"] + ("" if path == "/" else path)
    full_title = title if "BYLD" in title else f"{title} | BYLD"
    graph = [ORG_LD, {"@type": "WebSite", "@id": SITE["url"] + "/#site", "url": SITE["url"], "name": "BYLD · Buildd From Ideas", "publisher": {"@id": SITE["url"] + "/#org"}}]
    graph += ld or []
    og_img = SITE["url"] + "/og/" + (og or "default") + ".png"
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    doc = f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{robots}
<meta name="theme-color" content="#080B1F">
<meta property="og:type" content="website"><meta property="og:site_name" content="BYLD · Buildd From Ideas">
<meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{og_img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(full_title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{og_img}">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300..700&family=Geist+Mono:wght@400;500;600&display=swap">
<script>try{{var t=localStorage.getItem('byld-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<link rel="stylesheet" href="/css/site.css?v={ASSET_V}">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
<script>document.documentElement.classList.remove('no-js')</script>
</head>
<body>
{header(active)}
<div class="sprog" aria-hidden="true"></div>
<main id="main">
{body}
</main>
{footer()}
{ix.video_dialog()}
<script src="/js/site.js?v={ASSET_V}" defer></script>
</body>
</html>
'''
    target = OUT / ("index.html" if path == "/" else path.strip("/") + ".html")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc, encoding="utf-8")
    if not noindex:
        PAGES.append((path, priority))
    name = og or "default"
    if not noindex and name not in {j["name"] for j in OG_JOBS}:
        OG_JOBS.append({"name": name, "title": title.split(":")[0] if og else "More than a franchise. Without the franchise fees.",
                        "sub": (title.split(":", 1)[1].strip() if og and ":" in title else desc)})

OG_JOBS = []

# ----------------------------------------------------------------------------- sections
def stats_html():
    return '<div class="stats">' + "".join(
        f'<div class="stat"><b data-count>{e(s["value"])}</b><span>{e(s["label"])}</span><em>{e(s["note"])}</em></div>' for s in STATS) + '</div>'

def brands_html():
    return f'<div class="brands"><p>Hotels we run revenue for</p>{ix.marquee(BRANDS)}</div>'

def vs_table(rows=FRANCHISE_ROWS):
    hd = f'<div class="vs-row vs-hd"><div></div><div>Typical franchise</div><div class="us">BYLD</div></div>'
    body = "".join(
        f'<div class="vs-row"><div class="k">{e(k)}</div><div class="them">{ICON["minus"]}<span><i class="mlbl">Typical franchise</i>{e(t)}</span></div><div class="us">{ICON["check"]}<span><i class="mlbl">BYLD</i>{e(u)}</span></div></div>'
        for k, t, u in rows)
    return f'<div class="vs rv" role="table" aria-label="Typical hotel franchise compared with BYLD">{hd}{body}</div>'

def flow_html():
    out = []
    for i, (h, who, p) in enumerate(AI_HUMAN):
        cls = ' class="human"' if "human" in h.lower() else ""
        out.append(f'<div{cls}><div class="n"><span>0{i+1}</span><em>{e(who)}</em></div><h3>{e(h)}</h3><p>{e(p)}</p></div>')
    return '<div class="flow rv">' + "".join(out) + '</div>'

def pillars_html():
    items = ["Floor and ceiling locks", "Approval before go-live", "Full audit trail", "Every decision scored"]
    return '<div class="pillars rv">' + "".join(f'<div>{ICON["check"]}{e(t)}</div>' for t in items) + '</div>'

def steps_html():
    return '<ol class="steps">' + "".join(
        f'<li class="rv"><span class="n">0{i+1}</span><h3>{e(h)}</h3><p>{e(p)}</p></li>' for i, (h, p) in enumerate(STEPS)) + '</ol>'

def faq_html(items, title="Questions owners ask", sub="Straight answers. If yours isn't here, ask us."):
    qs = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in items)
    return f'''<section class="sec"><div class="wrap faq-grid">
<div><div class="kicker">FAQ</div><h2 class="h2">{e(title)}</h2><p class="sub">{e(sub)}</p>
<div class="cta-row"><a class="btn btn-dark" href="/contact">Talk to our team{ICON["arrow"]}</a></div></div>
<div class="faq">{qs}</div></div></section>'''

def cta_band(title="See what your hotels are leaving on the table.", sub="Book a free revenue review. We'll look at pricing, distribution, OTA payouts and direct booking, and show you exactly where the money is."):
    return f'''<section class="dark glow gridlines cta-band"><div class="wrap">
<h2>{e(title)}</h2><p>{e(sub)}</p>
<div class="cta-row"><a class="btn btn-primary" href="/contact">Book a revenue review{ICON["arrow"]}</a><a class="btn btn-ghost" href="/revvitals-sample">See a sample report</a></div>
</div></section>'''

def card(p, cls="span2", feature=False, peek=False):
    f = " feature" if feature else ""
    pk = f'<div class="peek">{product_visual(p)}</div>' if peek else ""
    return f'''<a class="card {cls}{f} rv" href="/products/{p["slug"]}">
<div class="top"><div class="ico">{picon(p["slug"])}</div>{badge(p["status"])}</div>
<span class="verb">{e(p["verb"])}</span><h3>{pname(p) if not p.get("nav_name") else e(p["nav_name"])}</h3><p>{e(p["short"])}</p>
<span class="more">Learn more {ICON["arrow"]}</span>{pk}</a>'''

def bento():
    P = BY_SLUG
    return '<div class="bento">' + "".join([
        card(P["pricecortex"], "span3 wide-m", feature=True),
        card(P["bfis-pms"], "span3"),
        card(P["compmatrix"]), card(P["foliolens"]), card(P["revvitals"]),
        card(P["otarecon365"]), card(P["goldkey-rewards"]), card(P["saleslock"]),
        card(P["askrank"]), card(P["pulsepilot"]), card(P["direct-booking"]),
    ]) + '</div>'

def spotlight(p, flip=False, lead=None, extra=""):
    feats = "".join(f'<li>{ICON["check"]}<span><b>{e(h)}.</b> {e(t)}</span></li>' for h, t in p["features"][:4])
    label, target = p["cta"]
    v = p["visual"]
    cap = f'<figcaption>{e(v["caption"])}</figcaption>' if v["type"] == "shot" else ""
    return f'''<div class="spot{" flip" if flip else ""}">
<div class="rv"><div class="meta" style="display:flex;gap:10px;align-items:center"><span class="kicker" style="margin:0">{e(p["verb"])}</span>{badge(p["status"])}</div>
<h3>{pname(p)}: {e(p["tagline"])}</h3><p class="lead">{e(lead or p["intro"])}</p>
<ul class="checks">{feats}</ul>
<div class="acts"><a class="btn btn-dark" href="/products/{p["slug"]}">Explore {pname(p, plain=True)}{ICON["arrow"]}</a>{extra}</div></div>
<figure class="spot-media media rv" style="margin:0">{product_visual(p)}{cap}</figure></div>'''

def whatsapp_html():
    return f'''<section class="sec dark glow"><div class="wrap wa-grid">
<div class="rv"><div class="kicker">WhatsApp revenue desk</div>
<h2 class="h2">Your revenue team, <span class="muted">where you already talk.</span></h2>
<p class="sub">No new app to learn. Your revenue manager shares the daily pricing and comp-set movement on WhatsApp, explains what's changing and why, and gets your go-ahead in a reply. Every detail and every decision is also in the owner portal.</p>
<ul class="checks" style="margin-top:30px">
<li style="color:#fff">{ICON["check"]}<span>Daily pricing and comp-set movement, ready to read on a phone.</span></li>
<li style="color:#fff">{ICON["check"]}<span>Approve with a reply, or ask your revenue manager a question.</span></li>
<li style="color:#fff">{ICON["check"]}<span>Full detail and history in the owner portal.</span></li></ul></div>
<div class="phone rv" aria-label="Example WhatsApp conversation with a BYLD revenue manager"><div class="phone-in">
<div class="wa-top"><img src="/img/byld-icon.svg" alt="" width="36" height="36"><div><b>BYLD Revenue Desk</b><span>Your revenue manager · online</span></div></div>
<div class="wa-body" data-chat>
<div class="msg">Good morning! Daily pricing for <b>Your Hotel</b> 🌅<table><tr><td>Fri King</td><td>$129 → $144</td></tr><tr><td>Sat Suite</td><td>$189 hold</td></tr><tr><td>Sun King</td><td>$119 → $109</td></tr></table><small>8:02</small></div>
<div class="msg">Comps moved up $12 for Friday and pace is ahead of last year. Sunday is soft, so a small drop to pick up weekend stays.<small>8:03</small></div>
<div class="msg me">Looks good. Can we keep Sunday at $115?<small>8:15</small></div>
<div class="msg">Done ✅ Sunday set to $115, everything else live. I'll watch Sunday's pickup.<small>8:17</small></div>
</div></div></div></div></section>'''

def dataflow_html():
    col = lambda k, cls, t: f'<div class="{cls} rv"><h4>{t}</h4><ul>' + "".join(f"<li>{e(x)}</li>" for x in DATA_FLOW[k]) + '</ul></div>'
    return '<div class="dflow">' + col("in", "", "Data in") + col("engine", "mid", "AI + human revenue manager") + col("out", "", "Results out") + '</div>'

def partners_html(dark=False):
    out = []
    for cat, name, desc, chips in PARTNERS:
        ch = "".join(f'<span class="badge svc">{e(c)}</span>' for c in chips)
        out.append(f'<div class="tile rv"><span class="cat">{e(cat)}</span><h3>{e(name)}</h3><p>{e(desc)}</p>{f"<div class=chips>{ch}</div>" if ch else ""}</div>')
    return '<div class="tiles">' + "".join(out) + '</div>'

def coming_html():
    return '<div class="tiles">' + "".join(
        f'<div class="tile rv"><span class="badge pilot">{e(s)}</span><h3>{e(n)}</h3><p>{e(d)}</p></div>' for n, s, d in COMING) + '</div>'

# ----------------------------------------------------------------------------- pages
def build_home():
    hero = f'''<section class="dark hero hero-x" data-hero><canvas class="aurora" aria-hidden="true"></canvas><div class="hero-grid-fx" aria-hidden="true"></div><div class="wrap">
<div class="hero-grid">
<div class="hero-copy">
  <span class="eyebrow"><i></i>AI-powered, human-guarded hotel revenue</span>
  <h1>{ix.hero_words("More than a franchise.")} <span class="nowrap-m">{ix.hero_words("Without the franchise fees.", "grad")}</span></h1>
  <p class="lede">BYLD runs your hotel's entire revenue engine on one platform: <strong>PMS, AI pricing, comp-set intelligence, owner reporting, OTA payout recovery, your own loyalty program, group sales, reputation and direct booking.</strong> A named revenue manager approves every rate.</p>
  <div class="cta-row"><a class="btn btn-primary" data-magnetic href="/contact">Book a revenue review{ICON["arrow"]}</a>{ix.play_button()}</div>
  <div class="trust"><div class="av">RM</div><div><b>Every rate has a human owner.</b> AI recommends, your revenue manager approves.</div></div>
</div>
<div class="hero-demo" data-tilt>{ix.command_center()}</div>
</div>
{stats_html()}
{brands_html()}
</div></section>'''

    franchise = f'''<section class="sec"><div class="wrap">
<div class="head-row"><div class="head"><div class="kicker">The franchise math</div>
<h2 class="h2">Franchises charge for the flag. <span class="muted">We deliver the revenue engine.</span></h2>
<p class="sub">Royalties, marketing levies, reservation and loyalty fees come off your top line every month. Run your own numbers, then see what BYLD gives you instead.</p></div>
<a class="link" href="/why-byld">Full comparison {ICON["arrow"]}</a></div>
{ix.fee_calculator()}
<div style="margin-top:20px">{vs_table(FRANCHISE_ROWS[:6])}</div>
<p class="vs-note">Franchise column describes common franchise arrangements in general terms; individual agreements vary.</p>
</div></section>'''

    tour = [BY_SLUG[s] for s in ["bfis-pms", "pricecortex", "compmatrix", "foliolens", "otarecon365", "goldkey-rewards"]]
    platform = f'''<section class="sec soft"><div class="wrap">
<div class="head-row"><div class="head"><div class="kicker">The platform</div>
<h2 class="h2">Every revenue task. <span class="muted">One partner, one portal.</span></h2>
<p class="sub">Most hotels piece revenue together from a PMS, a pricing tool, a rate shopper, a BI dashboard, an OTA agency, a reputation tool and spreadsheets. We run the whole cycle on one data foundation, so every decision uses the same numbers.</p></div>
<a class="btn btn-line" href="/platform">All 11 products{ICON["arrow"]}</a></div>
{ix.story(tour, product_visual, pname)}
</div></section>'''

    ai = f'''<section class="sec dark glow"><div class="wrap">
<div class="head"><div class="kicker">AI + human oversight</div>
<h2 class="h2">Machine-learning speed. <span class="muted">Human judgement on every rate.</span></h2>
<p class="sub">Our models read thousands of signals and recommend. Guardrails keep every number inside your limits. A dedicated revenue manager reviews the reasoning and approves before anything reaches your guests.</p></div>
{flow_html()}
<div style="margin-top:20px">{ix.pricing_sim()}</div>
</div></section>'''

    more = f'''<section class="sec"><div class="wrap">
<div class="head-row"><div class="head"><div class="kicker">And more</div><h2 class="h2">Built in-house. <span class="muted">Growing every quarter.</span></h2></div>
<a class="link" href="/platform">See the whole platform {ICON["arrow"]}</a></div>
<div class="bento">{"".join(card(BY_SLUG[k], "span2") for k in ["revvitals", "saleslock", "askrank", "pulsepilot", "direct-booking"])}
<a class="card span2 feature rv" href="/platform#next"><div class="top"><div class="ico">{picon("revvitals")}</div><span class="badge pilot">Coming</span></div><span class="verb">Next</span><h3>Halo™ and Signal™</h3><p>An AI revenue assistant in your owner portal, and market demand signals layered onto pricing.</p><span class="more">What's next {ICON["arrow"]}</span></a>
</div></div></section>'''

    start = f'''<section class="sec soft"><div class="wrap">
<div class="head-row"><div class="head"><div class="kicker">Getting started</div><h2 class="h2">Live in weeks, <span class="muted">not a brand conversion.</span></h2>
<p class="sub">No property improvement plan, no re-flag. Your booking engine can be connected to any PMS in about a week.</p></div>
<a class="link" href="/how-it-works">How it works {ICON["arrow"]}</a></div>
{steps_html()}</div></section>'''

    partners = f'''<section class="sec tight"><div class="wrap">
<div class="head-row"><div class="head"><div class="kicker">Beyond revenue</div><h2 class="h2">Partners for every part of ownership.</h2></div><a class="link" href="/partners">Our partners {ICON["arrow"]}</a></div>
{partners_html()}</div></section>'''

    body = hero + ix.video_section() + franchise + platform + ai + whatsapp_html() + more + start + partners + faq_html(HOME_FAQ) + cta_band()
    page("/", "BYLD: Hotel Revenue Management Without Franchise Fees",
         "More than a franchise, without the fees: PMS, AI pricing approved by a human revenue manager, owner reporting, OTA recovery, loyalty and direct booking.",
         body, ld=[faq_ld(HOME_FAQ), ix.video_ld(SITE["url"])], priority="1.0")

def build_platform():
    groups = ""
    for g in GROUPS:
        ps = [p for p in PRODUCTS if p["group"] == g]
        cards = "".join(card(p, "span2") for p in ps)
        groups += f'<div style="margin-top:56px"><div class="kicker">{e(g)}</div><div class="bento">{cards}</div></div>'
    body = f'''<section class="dark glow gridlines phero"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span aria-current="page">Platform</span></nav>
<h1>One platform for <span class="grad">every revenue task</span> in your hotel.</h1>
<p class="lede">Eleven products on one data foundation, one owner portal and one WhatsApp desk, run by a named revenue manager. Start with one, or hand us the whole cycle.</p>
<div class="cta-row"><a class="btn btn-primary" href="/contact">Book a revenue review{ICON["arrow"]}</a><a class="btn btn-ghost" href="{SITE["portal"]}" target="_blank" rel="noopener">Owner portal login</a></div>
</div></section>
<section class="sec" style="padding-top:40px"><div class="wrap">{groups}</div></section>
<section class="sec soft"><div class="wrap"><div class="head"><div class="kicker">How it runs</div><h2 class="h2">Connected to your data. <span class="muted">Running while you sleep.</span></h2></div>{dataflow_html()}</div></section>
<section class="sec"><div class="wrap"><div class="head"><div class="kicker">What's next</div><h2 class="h2">Growing with your hotels.</h2><p class="sub">New modules join the same portal as they're ready.</p></div>{coming_html()}</div></section>
{cta_band()}'''
    page("/platform", "Hotel Revenue Platform: PMS, Pricing, Loyalty",
         "Eleven hotel revenue products in one owner portal: PMS, AI pricing, comp sets, owner reporting, OTA recovery, loyalty, group sales, reputation and booking.",
         body, active="platform", ld=[crumbs_ld([("Home", "/"), ("Platform", "/platform")]),
         {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f'{SITE["url"]}/products/{p["slug"]}', "name": pname(p, True)} for i, p in enumerate(PRODUCTS)]}],
         og="platform", priority="0.9")

def build_product(p):
    label, target = p["cta"]
    feats = "".join(f'<div class="feat rv"><span class="n">0{i+1}</span><h3>{e(h)}</h3><p>{e(t)}</p></div>' for i, (h, t) in enumerate(p["features"]))
    rel = "".join(card(BY_SLUG[s], "span2") for s in p["related"])
    v = p["visual"]
    cap = f'<p class="mono" style="font-size:12.5px;color:var(--d-muted);margin-top:12px">{e(v["caption"])}</p>' if v["type"] == "shot" else ""
    extra = ""
    if p["slug"] == "goldkey-rewards":
        shots = "".join(f'<figure>{picture(n, a, sizes="(max-width:900px) 33vw, 330px")}</figure>' for n, a in [
            ("goldkey-signup", "GoldKey Rewards QR sign-up page on a phone"),
            ("goldkey-welcome", "GoldKey Rewards instant welcome with member card"),
            ("goldkey-email", "GoldKey Rewards personal welcome email")])
        extra = f'''<section class="sec soft"><div class="wrap"><div class="head"><div class="kicker">Live screens</div><h2 class="h2">Sign-up, welcome card and email.</h2><p class="sub">Real GoldKey screens. Hotel and guest names hidden.</p></div><div class="gk-shots">{shots}</div></div></section>'''
    if p["slug"] == "revvitals":
        shots = "".join(f'<figure>{window(picture(n, a, sizes="(max-width:900px) 100vw, 560px"), bar, label="Real report")}<figcaption>{e(cap_)}</figcaption></figure>' for n, a, bar, cap_ in [
            ("revvitals-ota-audit", "RevVitals OTA audit comparing Booking.com, Expedia and Agoda metric by metric", "Chapter IV · The OTA audit",
             "Every OTA checked line by line: reviews, content scores, volume, rate, cancellations and promotions."),
            ("revvitals-progress", "RevVitals action tracker showing channel scores before and after and progress on 23 actions", "Chapter V · Action plan",
             "Then the follow-through: actions done and under way, and channel scores before and after.")])
        extra = f'''<section class="sec"><div class="wrap"><div class="head"><div class="kicker">From the real report</div><h2 class="h2">The audit, then the follow-through.</h2><p class="sub">Snapshots from an actual RevVitals report. The hotel name, location and account identifiers have been changed.</p></div><div class="rv-shots">{shots}</div><div class="cta-row" style="margin-top:28px"><a class="btn btn-primary" href="/revvitals-sample">Read the full sample report{ICON["arrow"]}</a></div></div></section>'''
    if p["slug"] == "pricecortex":
        extra = f'''<section class="sec dark glow"><div class="wrap"><div class="head"><div class="kicker">AI + human oversight</div><h2 class="h2">The model recommends. <span class="muted">A person decides.</span></h2></div>{flow_html()}<div style="margin-top:20px">{ix.pricing_sim()}</div></div></section>'''
    body = f'''<section class="dark glow gridlines phero"><div class="wrap prod-hero">
<div class="rv"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/platform">Platform</a><span>/</span><span aria-current="page">{pname(p)}</span></nav>
<div class="meta"><span class="nm">{e(p["group"])}</span>{badge(p["status"])}{f'<span class="badge svc">{e(p["badge"])}</span>' if p.get("badge") else ""}</div>
<h1><span class="pn">{pname(p)}</span><span class="grad">{e(p["tagline"])}</span></h1>
<p class="lede">{e(p["intro"])}</p>
<div class="cta-row">{a_btn(label, target)}<a class="btn btn-ghost" href="/contact">Book a revenue review</a></div></div>
<div class="rv" data-tilt>{product_visual(p, eager=True)}{cap}</div>
</div></section>
<section class="sec"><div class="wrap"><div class="head"><div class="kicker">What it does</div><h2 class="h2">{pname(p)}, <span class="muted">feature by feature.</span></h2></div>
<div class="feat-grid{" three" if len(p["features"]) > 4 else ""}">{feats}</div></div></section>
{extra}
<section class="sec soft"><div class="wrap"><div class="head-row"><div class="head"><div class="kicker">Works with</div><h2 class="h2">Better together on one platform.</h2></div><a class="link" href="/platform">All products {ICON["arrow"]}</a></div><div class="bento">{rel}</div></div></section>
{faq_html(p["faq"], title=f"{pname(p, True)} questions", sub="Anything else, ask your revenue manager or our team.")}
{cta_band()}'''
    ld = [crumbs_ld([("Home", "/"), ("Platform", "/platform"), (pname(p, True), f'/products/{p["slug"]}')]), faq_ld(p["faq"])]
    if p["slug"] == "direct-booking":
        ld.append({"@type": "Service", "name": p["name"], "serviceType": "Hotel website, booking engine and photography", "provider": {"@id": SITE["url"] + "/#org"}, "description": p["meta"], "areaServed": "US"})
    else:
        ld.append({"@type": "SoftwareApplication", "name": pname(p, True), "applicationCategory": "BusinessApplication", "applicationSubCategory": "Hotel revenue management",
                   "operatingSystem": "Web", "description": p["meta"], "publisher": {"@id": SITE["url"] + "/#org"}, "url": f'{SITE["url"]}/products/{p["slug"]}'})
    page(f'/products/{p["slug"]}', p["title"], p["meta"], body, ld=ld, og=p["slug"], priority="0.8")

def build_why():
    body = f'''<section class="dark glow gridlines phero"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span aria-current="page">Why BYLD</span></nav>
<h1>Everything a franchise promises your revenue. <span class="grad">None of the franchise fees.</span></h1>
<p class="lede">A flag brings a name, a reservation system and a loyalty program, and takes a slice of every room night for them. BYLD brings the revenue engine itself: the systems, the data and a named revenue manager working your hotel every day.</p>
<div class="cta-row"><a class="btn btn-primary" href="/contact">Book a revenue review{ICON["arrow"]}</a><a class="btn btn-ghost" href="/platform">See the platform</a></div>
</div></section>
<section class="sec"><div class="wrap">
<div class="head"><div class="kicker">Side by side</div><h2 class="h2">What you get, <span class="muted">and what you stop paying for.</span></h2></div>
{ix.fee_calculator()}
<div style="margin-top:20px">{vs_table()}</div>
<p class="vs-note">The franchise column describes common franchise arrangements in general terms; individual agreements vary.</p>
<div class="save">
<div class="rv"><b>Keep your top line</b><p>No royalty and no brand-marketing levy taken as a share of your room revenue.</p></div>
<div class="rv"><b>Own your guests</b><p>Your loyalty program, your booking engine, your website and your data. Members come back direct.</p></div>
<div class="rv"><b>Keep your choices</b><p>Run BFIS PMS or keep your current system. No mandated vendors to swap in.</p></div>
</div></div></section>
<section class="sec soft"><div class="wrap"><div class="head"><div class="kicker">Two ways to work with us</div><h2 class="h2">Independent or flagged, <span class="muted">we make the numbers move.</span></h2></div>
<div class="feat-grid">
<div class="feat rv"><span class="n">INDEPENDENT HOTELS</span><h3>The franchise toolkit, without the franchise.</h3><p>Distribution, loyalty and a revenue team are what independents usually miss. We bring a booking engine connected to your PMS in about a week, OTA marketing through RevVitals and AskRank, your own GoldKey Rewards program, and a named revenue manager backed by PriceCortex.</p></div>
<div class="feat rv"><span class="n">BRANDED HOTELS</span><h3>The revenue team your brand doesn't provide.</h3><p>Our portfolio flies Red Roof, Sonesta, Choice, Wyndham, Hilton, Marriott and IHG flags. The brand supplies the name; we supply daily pricing, comp-set tracking, owner reporting, OTA payout recovery, group sales and reputation work.</p></div>
</div></div></section>
<section class="sec dark glow"><div class="wrap">{stats_html()}</div></section>
{faq_html(FRANCHISE_FAQ, title="BYLD vs franchise")}
{cta_band("Run the numbers on your hotel.", "We'll compare what you pay today with what BYLD would deliver, property by property.")}'''
    page("/why-byld", "Hotel Franchise Alternative: No Franchise Fees",
         "Compare a hotel franchise with BYLD: revenue management, your own loyalty program, direct booking and owner reporting, without royalties or brand fees.",
         body, active="why", ld=[crumbs_ld([("Home", "/"), ("Why BYLD", "/why-byld")]), faq_ld(FRANCHISE_FAQ)], og="why-byld", priority="0.9")

def build_how():
    body = f'''<section class="dark glow gridlines phero"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span aria-current="page">How it works</span></nav>
<h1>AI does the heavy lifting. <span class="grad">A person you can call owns every decision.</span></h1>
<p class="lede">Here's how BYLD connects to your hotel, how the models and your revenue manager work together, and how you stay in the loop without learning a new tool.</p>
</div></section>
<section class="sec dark" style="padding-top:0"><div class="wrap">{flow_html()}{pillars_html()}<div style="margin-top:20px">{ix.pricing_sim()}</div></div></section>
<section class="sec"><div class="wrap"><div class="head"><div class="kicker">Under the hood</div><h2 class="h2">Connected to your data. <span class="muted">Running while you sleep.</span></h2>
<p class="sub">Every morning the platform pulls your PMS, the comp set and the market, checks the data is fresh, and has recommendations waiting for your revenue manager.</p></div>{dataflow_html()}</div></section>
{whatsapp_html()}
<section class="sec soft"><div class="wrap"><div class="head"><div class="kicker">Getting started</div><h2 class="h2">Four steps to live.</h2><p class="sub">Nothing changes at your hotel until you've seen the recommendations and agreed with them.</p></div>{steps_html()}</div></section>
{faq_html(HOME_FAQ[1:4])}
{cta_band()}'''
    page("/how-it-works", "How BYLD Works: AI Pricing, Human Revenue Managers",
         "Your PMS, comp set and STR data feed AI models; guardrails and a named revenue manager approve every rate; results reach you in the portal and on WhatsApp.",
         body, active="how", ld=[crumbs_ld([("Home", "/"), ("How it works", "/how-it-works")]), faq_ld(HOME_FAQ[1:4])], og="how-it-works", priority="0.8")

def build_partners():
    body = f'''<section class="dark glow gridlines phero"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span aria-current="page">Partners</span></nav>
<h1>Beyond revenue: <span class="grad">partners for every part of ownership.</span></h1>
<p class="lede">Capital, management and accounting from specialists we trust, so owners have one place to start for everything their hotels need.</p>
</div></section>
<section class="sec"><div class="wrap">{partners_html()}</div></section>
{cta_band("Need more than revenue?", "Tell us what you're working on, from an acquisition to a management change, and we'll make the right introduction.")}'''
    page("/partners", "Hotel Ownership Partners: Capital, Management, Tax",
         "Partners for hotel owners: fundraising and equity, full-service management from LHM Hospitality (Hilton, Marriott, IHG approved) and NPV Prime accounting.",
         body, active="partners", ld=[crumbs_ld([("Home", "/"), ("Partners", "/partners")])], og="partners", priority="0.6")

def build_contact():
    opts = "".join(f"<option>{pname(p, True)}</option>" for p in PRODUCTS)
    a = SITE["address"]
    body = f'''<section class="dark glow gridlines phero"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span aria-current="page">Contact</span></nav>
<h1>Book a <span class="grad">revenue review.</span></h1>
<p class="lede">Tell us about your hotels. We'll review pricing, distribution, OTA payouts and direct booking, and come back with where the money is, whether or not you work with us.</p>
</div></section>
<section class="sec"><div class="wrap contact-grid">
<div><div class="kicker">What happens next</div><h2 class="h2" style="font-size:36px">A conversation, then a plan.</h2>
<ol class="steps" style="grid-template-columns:1fr;margin-top:32px;gap:28px">{"".join(f'<li><span class="n">0{i+1}</span><h3>{e(h)}</h3><p>{e(p)}</p></li>' for i, (h, p) in enumerate(STEPS[:2]))}</ol>
<ul class="contact-list" style="margin-top:40px">
<li>{ICON["mail"]}<div><b>Email</b><a class="link" href="mailto:{SITE["email"]}">{SITE["email"]}</a></div></li>
<li>{ICON["pin"]}<div><b>Office</b>{e(a["street"])}, {e(a["city"])}, {e(a["region"])} {e(a["postal"])}</div></li>
<li>{ICON["key"]}<div><b>Already a client?</b><a class="link" href="{SITE["portal"]}" target="_blank" rel="noopener">Owner portal</a> · <a class="link" href="{SITE["pms_login"]}" target="_blank" rel="noopener">BFIS PMS</a></div></li>
</ul></div>
<form class="form" id="contact" data-to="{SITE["email"]}">
<div class="two"><div><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-email">Work email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div></div>
<div class="two"><div><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
<div><label for="f-hotels">Number of hotels</label><select id="f-hotels" name="hotels"><option>1</option><option>2–5</option><option>6–15</option><option>16+</option></select></div></div>
<label for="f-type">Your hotels are</label><select id="f-type" name="type"><option>Branded / franchised</option><option>Independent</option><option>A mix of both</option><option>Planning an acquisition</option></select>
<label for="f-interest">Most interested in</label><select id="f-interest" name="interest"><option>The full platform</option>{opts}</select>
<label for="f-msg">Anything we should know?</label><textarea id="f-msg" name="message" rows="4" placeholder="PMS, markets, what's not working today…"></textarea>
<button class="btn btn-primary" type="submit">Request my revenue review{ICON["arrow"]}</button>
<small>We reply within one business day. We never share your details.</small>
</form></div></section>'''
    page("/contact", "Book a Hotel Revenue Review", "Book a free hotel revenue review with BYLD: pricing, distribution, OTA payouts and direct booking, with a clear plan for where the money is.",
         body, ld=[crumbs_ld([("Home", "/"), ("Contact", "/contact")]), {"@type": "ContactPage", "url": SITE["url"] + "/contact"}], og="contact", priority="0.8")

def build_404():
    body = f'''<section class="dark glow gridlines phero" style="padding:140px 0"><div class="wrap">
<span class="eyebrow"><i></i>404</span><h1 style="margin-top:20px">This page checked out early.</h1>
<p class="lede">The page you're looking for has moved or never existed.</p>
<div class="cta-row"><a class="btn btn-primary" href="/">Back to home{ICON["arrow"]}</a><a class="btn btn-ghost" href="/platform">See the platform</a></div></div></section>'''
    page("/404", "Page not found", "This page could not be found.", body, noindex=True)

def build_sample():
    """Carry over the RevVitals sample report, with SEO head and site-relative assets."""
    src = ROOT.parent / "Marketing Materials" / "brochure" / "revvitals-sample.html"
    if not src.exists():
        return
    t = src.read_text(encoding="utf-8")
    t = t.replace('href="assets/byld-icon.svg"', 'href="/favicon.svg"').replace('src="assets/', 'src="/img/').replace('href="index.html"', 'href="/"')
    extra = (f'<link rel="canonical" href="{SITE["url"]}/revvitals-sample">\n'
             f'<meta property="og:title" content="RevVitals Sample Report | BYLD"><meta property="og:image" content="{SITE["url"]}/og/revvitals-sample.png">\n')
    t = t.replace("<title>RevVitals Sample Report</title>", "<title>RevVitals Sample Report | BYLD</title>\n" + extra, 1)
    # Dark by default like the rest of the site; honours a visitor's saved light choice.
    theme = ("<script>try{var t=localStorage.getItem('byld-theme');"
             "if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>\n"
             '<meta name="theme-color" content="#080B1F">\n')
    t = t.replace("<head>", "<head>\n" + theme, 1)
    t = t.replace("</head>", f'<link rel="stylesheet" href="/css/report-dark.css?v={ASSET_V}">\n</head>', 1)
    (OUT / "revvitals-sample.html").write_text(t, encoding="utf-8")
    PAGES.append(("/revvitals-sample", "0.6"))

# ----------------------------------------------------------------------------- assets & SEO files
def copy_static():
    global ASSET_V
    if OUT.exists():
        for child in OUT.iterdir():
            if child.name in ("og", "video"):  # generated separately by og.mjs; keep between builds
                continue
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    OUT.mkdir(exist_ok=True)
    for sub in ["css", "js", "img"]:
        shutil.copytree(STATIC / sub, OUT / sub, dirs_exist_ok=True)
    for f in (STATIC / "root").iterdir():
        shutil.copy(f, OUT / f.name)
    h = hashlib.sha1((STATIC / "css/site.css").read_bytes() + (STATIC / "js/site.js").read_bytes()).hexdigest()[:8]
    ASSET_V = h
    # optimise screenshots: jpg (quality 82) + webp, record intrinsic sizes for width/height attrs
    from PIL import Image
    for src in sorted((ROOT / "assets").glob("*.jpg")):
        im = Image.open(src).convert("RGB")
        IMG_SIZES[src.stem] = im.size
        im.save(OUT / "img" / f"{src.stem}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
        im.save(OUT / "img" / f"{src.stem}.webp", "WEBP", quality=80, method=6)

def seo_files():
    urls = "".join(f'<url><loc>{SITE["url"]}{"" if p == "/" else p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>' for p, pr in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")
    lines = [f"# BYLD · Buildd From Ideas", "", f"> {SITE['description']}", "",
             "BYLD is a hotel revenue operations partner. AI and machine-learning models recommend; a named human revenue manager approves every rate. "
             "It positions itself as offering more than a hotel franchise does, without franchise fees.", "",
             "## Portfolio", *[f"- {s['label']}: {s['value']} ({s['note']})" for s in STATS], "",
             "## Products", *[f"- [{pname(p, True)}]({SITE['url']}/products/{p['slug']}): {p['short']} Status: {p['status']}." for p in PRODUCTS], "",
             "## Pages", f"- [Why BYLD vs a franchise]({SITE['url']}/why-byld)", f"- [How it works]({SITE['url']}/how-it-works)",
             f"- [Partners]({SITE['url']}/partners)", f"- [RevVitals sample report]({SITE['url']}/revvitals-sample)", f"- [Contact]({SITE['url']}/contact)", ""]
    (OUT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")
    (ROOT / "og-jobs.json").write_text(json.dumps(OG_JOBS, indent=1), encoding="utf-8")

ASSET_V = "0"

def main():
    copy_static()
    build_home(); build_platform()
    for p in PRODUCTS:
        build_product(p)
    build_why(); build_how(); build_partners(); build_contact(); build_404(); build_sample()
    seo_files()
    print(f"Built {len(PAGES)} indexable pages into {OUT.relative_to(ROOT.parent)}/")

if __name__ == "__main__":
    main()
