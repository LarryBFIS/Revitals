"""Interactive and animated sections for the BYLD site. Each function returns HTML; behaviour lives in static/js/site.js.

Everything labelled ILLUSTRATIVE uses example numbers, never client data.
"""
import html

e = html.escape

ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
PLAY = '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M6.5 4.6v10.8a.8.8 0 001.2.7l8.6-5.4a.8.8 0 000-1.4L7.7 3.9a.8.8 0 00-1.2.7z"/></svg>'
LOCK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 015 0v2"/></svg>'

VIDEO = {"mp4": "/video/tour.mp4", "webm": "/video/tour.webm", "poster": "/video/tour-poster.jpg", "seconds": 76}


def hero_words(text, cls=""):
    """Split a headline into words that animate in one after another."""
    words = text.split(" ")
    return " ".join(f'<span class="w {cls}" style="--i:{i}">{e(w)}</span>' for i, w in enumerate(words))


def play_button(label="Watch the product tour"):
    return f'<button class="btn btn-ghost btn-play" type="button" data-video-open>{PLAY}<span>{e(label)}</span></button>'


# ----------------------------------------------------------------------------- hero command center
def command_center():
    """Auto-cycling, tabbed product demo in the hero. Pure HTML/SVG; animated by site.js + CSS."""
    tabs = [("price", "Price", "PriceCortex™"), ("compete", "Compete", "CompMatrix™"),
            ("report", "Report", "FolioLens™"), ("recover", "Recover", "OTARecon365™")]
    tab_html = "".join(
        f'<button type="button" role="tab" class="cc-tab" data-tab="{k}" aria-selected="{str(i == 0).lower()}"><b>{e(t)}</b><span>{e(n)}</span><i class="cc-prog"></i></button>'
        for i, (k, t, n) in enumerate(tabs))

    price = f'''<div class="cc-panel" data-panel="price">
  <div class="cc-hd"><span>PriceCortex · Fri · King room</span><span class="cc-pill">Demand 4/5</span></div>
  <div class="cc-rate"><div><small>Recommended rate</small><b>$<span data-tick data-from="129" data-to="144">144</span></b><em class="up">▲ $15 vs today</em></div>
    <div class="cc-guard"><span>{LOCK} Floor $99</span><span>{LOCK} Ceiling $189</span></div></div>
  <svg class="cc-chart" viewBox="0 0 400 120" preserveAspectRatio="none" aria-hidden="true">
    <rect x="0" y="18" width="400" height="84" class="band"/>
    <path class="curve" d="M0 104 C80 96 150 80 220 62 S340 30 400 22"/>
    <path class="pace draw" d="M0 108 C60 100 110 88 170 70 S300 34 400 16"/>
    <circle class="dot" cx="400" cy="16" r="5"/>
  </svg>
  <div class="cc-legend"><span><i class="l1"></i>On the books</span><span><i class="l2"></i>Booking curve</span><span><i class="l3"></i>Guardrails</span></div>
  <div class="cc-rows"><div><span>Pace vs curve</span><b class="pos">+8 rooms</b></div><div><span>Comp set median</span><b>$139 <em class="up">+$12</em></b></div></div>
  <div class="cc-approve"><div class="av">RM</div><div><b>Approved by your revenue manager</b><span>Live on all channels · 8:15 am</span></div><i>✓</i></div>
</div>'''

    hotels = [("Comp hotel A", 152), ("Your hotel", 144), ("Comp hotel B", 139), ("Comp hotel C", 131), ("Comp hotel D", 118)]
    bars = "".join(
        f'<div class="cc-bar{" me" if n == "Your hotel" else ""}" style="--w:{int(r / 160 * 100)}%;--i:{i}"><span>{e(n)}</span><i></i><b>${r}</b></div>'
        for i, (n, r) in enumerate(hotels))
    compete = f'''<div class="cc-panel" data-panel="compete">
  <div class="cc-hd"><span>CompMatrix · Best available rate · Fri</span><span class="cc-pill">Rank #2 of 5</span></div>
  <div class="cc-bars">{bars}</div>
  <div class="cc-heat" aria-hidden="true">{"".join(f'<i style="--d:{i};--c:{c}"></i>' for i, c in enumerate([1,2,1,3,2,1,1,2,3,1,2,2,1,1,3,2,1,2,1,1,2]))}</div>
  <div class="cc-legend"><span><i class="h1"></i>1st cheapest</span><span><i class="h2"></i>2nd</span><span><i class="h3"></i>3rd</span><span>Next 21 nights</span></div>
</div>'''

    report = f'''<div class="cc-panel" data-panel="report">
  <div class="cc-hd"><span>FolioLens · Month to date</span><span class="cc-pill ok">Ahead of plan</span></div>
  <div class="cc-kpis"><div><small>Occupancy</small><b><span data-tick data-from="0" data-to="78">78</span>%</b></div><div><small>ADR</small><b>$<span data-tick data-from="0" data-to="132">132</span></b></div><div><small>RevPAR</small><b>$<span data-tick data-from="0" data-to="103">103</span></b></div></div>
  <svg class="cc-chart" viewBox="0 0 400 110" preserveAspectRatio="none" aria-hidden="true">
    <path class="ly" d="M0 92 L40 88 80 90 120 80 160 82 200 72 240 76 280 66 320 68 360 60 400 58"/>
    <path class="plan" d="M0 84 L400 44"/>
    <path class="pace draw" d="M0 86 L40 78 80 80 120 64 160 67 200 50 240 54 280 38 320 42 360 28 400 22"/>
  </svg>
  <div class="cc-legend"><span><i class="l1"></i>Actual</span><span><i class="l2"></i>Plan</span><span><i class="l4"></i>Last year</span></div>
  <div class="cc-rows"><div><span>RGI vs CoStar STR market</span><b class="pos"><span data-tick data-from="100" data-to="112.4" data-dec="1">112.4</span></b></div><div><span>Weekly brief</span><b>Checked · sent Mon 7:00</b></div></div>
</div>'''

    items = [("Virtual card not charged", "OTA 1", 412, "ok", "Recovered"), ("Payout short vs folio", "OTA 2", 186, "info", "Claimed"),
             ("No-show fee unpaid", "OTA 1", 129, "info", "Claimed"), ("Cancelled, card expiring", "OTA 3", 94, "bad", "Expires in 2 days")]
    q = "".join(f'<div class="cc-q" style="--i:{i}"><div><b>{e(t)}</b><span>{e(o)} · ${a}</span></div><em class="t-{c}">{e(s)}</em></div>' for i, (t, o, a, c, s) in enumerate(items))
    recover = f'''<div class="cc-panel" data-panel="recover">
  <div class="cc-hd"><span>OTARecon365 · Recovery queue</span><span class="cc-pill">365-day audit</span></div>
  <div class="cc-rate"><div><small>Found this month</small><b>$<span data-tick data-from="0" data-to="821">821</span></b><em class="up">across 4 bookings</em></div></div>
  <div class="cc-queue">{q}</div>
</div>'''

    return f'''<div class="cc" data-cc aria-label="Interactive product preview">
<div class="cc-glow" aria-hidden="true"></div>
<div class="cc-frame">
  <div class="cc-top"><i></i><i></i><i></i><span>portal.buildfromideas.ai</span><em>Illustrative</em></div>
  <div class="cc-tabs" role="tablist">{tab_html}</div>
  <div class="cc-body">{price}{compete}{report}{recover}</div>
</div>
</div>'''


# ----------------------------------------------------------------------------- video
def video_section():
    v = VIDEO
    return f'''<section class="sec vsec" id="tour"><div class="wrap">
<div class="head center"><div class="kicker">Product tour</div><h2 class="h2">Eleven products. <span class="muted">One platform, in 76 seconds.</span></h2>
<p class="sub">BFIS PMS, PriceCortex™, CompMatrix™, FolioLens™, RevVitals, OTARecon365™, GoldKey Rewards, SalesLock™ Concierge, AskRank, PulsePilot™ and direct booking, then the WhatsApp desk and what's next. Screens marked "Real screen" are live product; the rest are illustrative.</p></div>
<div class="vframe rv">
  <video class="vinline" muted loop playsinline preload="none" poster="{v["poster"]}" data-autoplay aria-label="BYLD product tour">
    <source src="{v["webm"]}" type="video/webm"><source src="{v["mp4"]}" type="video/mp4"></video>
  <button class="vplay" type="button" data-video-open aria-label="Play the tour with sound and controls"><span>{PLAY}</span><b>Play with sound</b></button>
</div></div></section>'''


def video_dialog():
    v = VIDEO
    return f'''<dialog class="vmodal" id="vmodal" aria-label="BYLD product tour">
<button class="vclose" type="button" data-video-close aria-label="Close video">✕</button>
<video controls playsinline preload="none" poster="{v["poster"]}"><source src="{v["webm"]}" type="video/webm"><source src="{v["mp4"]}" type="video/mp4"></video>
</dialog>'''


def video_ld(site_url):
    return {"@type": "VideoObject", "name": "BYLD product tour", "description": "A 76-second tour of every BYLD product: BFIS PMS, PriceCortex, CompMatrix, FolioLens, RevVitals, OTARecon365, GoldKey Rewards, SalesLock Concierge, AskRank, PulsePilot, websites and booking engine, and the WhatsApp revenue desk.",
            "thumbnailUrl": site_url + VIDEO["poster"], "contentUrl": site_url + VIDEO["mp4"], "uploadDate": "2026-11-18", "duration": f"PT{VIDEO['seconds']}S"}


# ----------------------------------------------------------------------------- franchise fee calculator
def fee_calculator():
    def field(id_, label, val, mn, mx, step, pre="", suf=""):
        return f'''<div class="calc-f"><div class="calc-l"><label for="{id_}">{e(label)}</label><output for="{id_}" data-out="{id_}">{pre}{val}{suf}</output></div>
<input type="range" id="{id_}" min="{mn}" max="{mx}" step="{step}" value="{val}" data-pre="{pre}" data-suf="{suf}"></div>'''
    return f'''<div class="calc rv" data-calc>
<div class="calc-in">
  <div class="kicker" style="margin-bottom:6px">Franchise fee calculator</div>
  <h3>What does the flag cost you?</h3>
  {field("c-rooms", "Rooms", 100, 20, 400, 1)}
  {field("c-adr", "Average daily rate", 120, 60, 400, 1, "$")}
  {field("c-occ", "Occupancy", 70, 30, 95, 1, "", "%")}
  {field("c-fee", "Total franchise fees, % of room revenue", 12, 4, 20, 0.5, "", "%")}
  <p class="calc-note">Use the total from your own agreement: royalty, marketing, reservation, loyalty and technology fees. Estimate only; no growth assumed.</p>
</div>
<div class="calc-out">
  <div><small>Annual room revenue</small><b data-r="rev">$3,066,000</b></div>
  <div class="hl"><small>Paid to the brand every year</small><b data-r="fee">$367,920</b></div>
  <div><small>Over a 10-year agreement</small><b data-r="ten">$3,679,200</b></div>
  <div class="calc-bar" aria-hidden="true"><i data-r="bar" style="width:12%"></i></div>
  <p>BYLD charges no royalty on your room revenue. Ask us what the same budget delivers when it goes into revenue, distribution and loyalty you own.</p>
  <a class="btn btn-primary" href="/contact">Compare it for my hotel{ARROW}</a>
</div></div>'''


# ----------------------------------------------------------------------------- pricing simulator
def pricing_sim():
    def rng(id_, label, val, mn, mx, step, fmt):
        return f'''<div class="calc-f"><div class="calc-l"><label for="{id_}">{e(label)}</label><output data-out="{id_}">{fmt}</output></div>
<input type="range" id="{id_}" min="{mn}" max="{mx}" step="{step}" value="{val}"></div>'''
    return f'''<div class="sim rv" data-sim>
<div class="sim-in">
  <div class="kicker">Try it</div>
  <h3>Move the market. Watch the rate.</h3>
  {rng("s-pace", "Pace vs booking curve", 8, -20, 20, 1, "+8 rooms")}
  {rng("s-comp", "Comp set median rate", 139, 80, 220, 1, "$139")}
  {rng("s-dem", "Demand pressure", 4, 1, 5, 1, "4 of 5")}
  <div class="sim-locks"><span>{LOCK} Floor $99</span><span>{LOCK} Ceiling $189</span><span>Set by you. No model can cross them.</span></div>
</div>
<div class="sim-out">
  <small>Recommended rate · Friday · King</small>
  <div class="sim-rate"><span>$<b data-s="rate">154</b></span><em data-s="clamp"></em></div>
  <div class="gauge" aria-hidden="true"><div class="g-band" style="left:15%;right:9.17%"></div><div class="g-needle" data-s="needle"></div><span style="left:15%">$99</span><span style="left:90.83%">$189</span></div>
  <ul class="sim-why" data-s="why"></ul>
  <button class="btn btn-primary" type="button" data-s="send">Send to my revenue manager{ARROW}</button>
  <div class="sim-chat" data-s="chat" hidden></div>
  <p class="sim-note">Simplified illustration. The real PriceCortex model reads far more signals, and a person approves every rate.</p>
</div></div>'''


# ----------------------------------------------------------------------------- scrollytelling platform tour
def story(products, visual_fn, pname):
    steps, stage = [], []
    for i, p in enumerate(products):
        feats = "".join(f"<li>{e(h)}</li>" for h, _ in p["features"][:3])
        steps.append(f'''<div class="story-step" data-step="{i}">
<span class="kicker">{i + 1:02d} · {e(p["verb"])}</span><h3>{pname(p)}</h3><p class="lead">{e(p["tagline"])} {e(p["short"])}</p>
<ul class="story-list">{feats}</ul><a class="link" href="/products/{p["slug"]}">Explore {pname(p, plain=True)} {ARROW}</a>
<div class="story-inline">{visual_fn(p)}</div></div>''')
        stage.append(f'<div class="story-vis{" on" if i == 0 else ""}" data-vis="{i}">{visual_fn(p)}</div>')
    dots = "".join(f'<i data-dot="{i}"{" class=on" if i == 0 else ""}></i>' for i in range(len(products)))
    return f'''<div class="story" data-story>
<div class="story-steps">{"".join(steps)}</div>
<div class="story-stage"><div class="story-sticky"><div class="story-frame">{"".join(stage)}</div><div class="story-dots">{dots}</div></div></div>
</div>'''


def marquee(items):
    row = "".join(f"<li>{e(b)}</li>" for b in items)
    return f'<div class="marquee" aria-label="Brands in our portfolio"><ul>{row}</ul><ul aria-hidden="true">{row}</ul></div>'
