"""All website copy and data. Edit this file to change the site, then run `python3 build.py`.

Rules for copy (keep the site credible):
  * Only state facts we can stand behind. Mark mock-ups as ILLUSTRATIVE.
  * Product status must match reality: Live, Launching, Pilot, Early access, Service.
  * Numbers in STATS are real portfolio figures. Update them, don't round them up.
"""

SITE = {
    "url": "https://buildfromideas.ai",
    "name": "Buildd From Ideas",
    "short": "BYLD",
    "tagline": "Ideas, buildd.",
    # TODO(owner): confirm the public inbox. Used for the contact form and footer.
    "email": "hello@buildfromideas.com",
    "address": {
        "street": "1207 Delaware Avenue, #1292",
        "city": "Wilmington",
        "region": "DE",
        "postal": "19806",
        "country": "US",
    },
    "portal": "https://portal.buildfromideas.ai/login?redirect=%2Fportal_home",
    "pms_login": "https://login.buildfromideas.com/#/login",
    "pricing_explainer": "https://portal.buildfromideas.ai/pricing_works.html",
    "saleslock_demo": "https://portal.buildfromideas.ai/saleslock_demo.html",
    "description": (
        "BYLD gives hotels more than a franchise does, without franchise fees: a PMS, "
        "AI pricing approved by a human revenue manager, comp-set intelligence, owner reporting, "
        "OTA payout recovery, your own loyalty program, group sales and reputation."
    ),
}

# Real portfolio figures. Shown as plain text (search engines read them).
STATS = [
    {"value": "32", "label": "Hotels live", "note": "on the BYLD platform"},
    {"value": "$40.6M", "label": "Revenue managed", "note": "annually, across our hotels"},
    {"value": "+62%", "label": "Year-over-year growth", "note": "in revenue at the hotels we manage"},
    {"value": "57", "label": "Nights priced ahead", "note": "for every room category, every day"},
]

BRANDS = ["Red Roof", "Sonesta", "Choice Hotels", "Wyndham", "Hilton", "Marriott", "IHG", "Independent hotels"]

# ---------------------------------------------------------------------------------------------
# Products. `slug` becomes /products/<slug>. Order here is the order on the site.
# visual: "shot" uses a real screenshot from static/img; otherwise a named HTML mock in build.py.
# ---------------------------------------------------------------------------------------------
PRODUCTS = [
    {
        "slug": "bfis-pms",
        "name": "BFIS PMS",
        "tm": False,
        "group": "Foundation",
        "verb": "Run",
        "status": "Live",
        "short": "Cloud property management system with a live tape chart, room status and folios.",
        "tagline": "Where every revenue decision starts.",
        "title": "BFIS PMS: Cloud Hotel Property Management",
        "meta": "BFIS PMS is a cloud hotel property management system: live tape chart, room status, front desk folios and multi-property login, feeding pricing and reporting.",
        "intro": "Our cloud property management system, running live hotels today. The tape chart shows every room, every night and every guest at a glance, with room status, folios, rates and reports one click away. Its data flows straight into pricing, reporting and loyalty, so every decision uses the same numbers.",
        "features": [
            ("Tape chart", "Every room by night, with occupancy and availability for each day, tooltips, rates and room locks."),
            ("Live room status", "Vacant or occupied, clean, dirty or in maintenance, so the front desk and housekeeping work from the same screen."),
            ("Front desk and folios", "New folios, check-ins, cashiering, guest messages and reports, all from the top bar."),
            ("Multi-property", "Switch hotels from one login. Data feeds PriceCortex, FolioLens and GoldKey automatically."),
        ],
        "visual": {"type": "shot", "src": "pms-tape-chart", "bar": "pms.buildfromideas.com · Tape chart",
                   "alt": "BFIS PMS tape chart showing rooms by night, room status legend and occupancy per day",
                   "caption": "Real BFIS PMS screen. Guest names hidden."},
        "cta": ("BFIS PMS login", "pms_login"),
        "faq": [
            ("Do I have to switch to BFIS PMS to work with BYLD?", "No. BFIS PMS is our own system and the fastest route, but we also connect to the PMS you already run, including ASI, G6 and IHG feeds."),
            ("Can one login cover several hotels?", "Yes. BFIS PMS is multi-property: owners and managers switch between hotels from a single login."),
        ],
        "related": ["pricecortex", "foliolens", "goldkey-rewards"],
    },
    {
        "slug": "pricecortex",
        "name": "PriceCortex",
        "tm": True,
        "group": "Price & compete",
        "verb": "Price",
        "status": "Live",
        "badge": "AI + human RM",
        "short": "AI rate recommendations for every room category, 57 nights ahead, approved by your revenue manager.",
        "tagline": "The right rate for every room, 57 nights ahead.",
        "title": "PriceCortex: AI Hotel Pricing, Human-Approved",
        "meta": "PriceCortex reads your booking pace, comp set and market daily and recommends a rate per room category, 57 nights ahead. A human revenue manager approves.",
        "intro": "Every day, for every hotel, PriceCortex reads where the books are against where they should be, checks the market, and recommends a rate for each room category. Your revenue manager reviews the reasoning and approves. Nothing reaches your guests without a person signing off.",
        "features": [
            ("On the books vs target vs last year", "Rooms sold today, the target from your booking curve, and last year's final on the same day of the week."),
            ("Pace against the booking curve", "How many rooms ahead or behind you are, so price moves are driven by real demand."),
            ("A rate per room category, inside your limits", "Always between a floor and a ceiling, with each band showing where it came from: your rule, your listing, your PMS rate or the market."),
            ("RevPAR and demand pressure", "Recent RevPAR against target and last year, plus a 1-to-5 demand-pressure score."),
        ],
        "visual": {"type": "shot", "src": "pricecortex-today-card", "bar": "PriceCortex · Today",
                   "alt": "PriceCortex today card with on-the-books, pace, recommended rates per room category and RevPAR",
                   "caption": "Real PriceCortex screen."},
        "cta": ("See how PriceCortex prices", "pricing_explainer"),
        "faq": [
            ("Does PriceCortex change my rates automatically?", "No. PriceCortex recommends; a named human revenue manager reviews the reasoning and approves before anything goes live. Floors and ceilings you set can never be crossed."),
            ("How far ahead does it price?", "57 nights ahead, for every room category, every day."),
            ("Can I see why a rate was recommended?", "Yes. Every recommendation carries its audit trail: the pace signal, the competitor position and the guardrail that applied."),
        ],
        "related": ["compmatrix", "foliolens", "bfis-pms"],
    },
    {
        "slug": "compmatrix",
        "name": "CompMatrix",
        "tm": True,
        "group": "Price & compete",
        "verb": "Compete",
        "status": "Live",
        "short": "Your rate against your whole comp set for the next 30 days, refreshed daily.",
        "tagline": "Know where you stand, every night.",
        "title": "CompMatrix: Hotel Comp Set Rate Shopping",
        "meta": "CompMatrix compares your rate with your whole comp set for the next 30 days, refreshed daily, built on 1.4M+ competitor rates with like-for-like rooms.",
        "intro": "Your rate against your whole comp set for the next 30 days, refreshed daily and built on a deep history of more than 1.4 million competitor rates. Room types are matched like for like, so you compare suites with suites, not just the cheapest room.",
        "features": [
            ("Best Available Rate", "The cheapest plan per day, across all room types, for every hotel in the set."),
            ("Daily rank", "Each night coloured by who is first, second and third cheapest."),
            ("Room Matrix", "Like-for-like room categories compared, not just the cheapest room."),
            ("Comp movement on WhatsApp", "Changes in your comp set sent to your team every day."),
        ],
        "visual": {"type": "shot", "src": "compmatrix-bar", "bar": "CompMatrix · Best Available Rate",
                   "alt": "CompMatrix chart comparing best available rate for the hotel and its comp set over 30 days",
                   "caption": "Real CompMatrix screen."},
        "cta": ("Open CompMatrix", "portal"),
        "faq": [
            ("How much rate history does CompMatrix use?", "More than 1.4 million competitor rates, refreshed daily."),
            ("Does it compare only the cheapest room?", "No. The Room Matrix compares like-for-like room categories across your comp set."),
        ],
        "related": ["pricecortex", "foliolens", "revvitals"],
    },
    {
        "slug": "foliolens",
        "name": "FolioLens",
        "tm": True,
        "group": "Report & improve",
        "verb": "Report",
        "status": "Live",
        "short": "Owner reporting: actual vs plan, last year and your market, with a weekly brief.",
        "tagline": "Performance, without building a report.",
        "title": "FolioLens: Hotel Owner Reporting and STR",
        "meta": "FolioLens shows owners actual vs plan vs last year, CoStar STR benchmarks (occupancy, ADR, RevPAR, RGI) and a self-checking weekly performance brief.",
        "intro": "The owner's view of each hotel: actual against plan and last year, against the market, and a weekly brief that checks itself before it sends. No spreadsheets to build, no report to chase.",
        "features": [
            ("Actual vs plan vs last year", "Month to date, last week and the next 7 days of pace."),
            ("You vs your market", "Occupancy, ADR, RevPAR and RGI from CoStar STR, with a two-line AI verdict."),
            ("Analysis tab", "This year vs last year vs a market-adjusted last year, month by month, plus quarterly performance reviews."),
            ("Weekly Performance Brief", "Delivered by email and quality-checked automatically before it sends."),
        ],
        "visual": {"type": "mock", "name": "foliolens"},
        "cta": ("Open FolioLens", "portal"),
        "faq": [
            ("Where does the market data come from?", "Monthly CoStar STR market reports, compared with your own PMS data."),
            ("How often do owners hear from us?", "Owners can log in any time, and get a Weekly Performance Brief by email that is checked automatically before it sends."),
        ],
        "related": ["pricecortex", "revvitals", "compmatrix"],
    },
    {
        "slug": "revvitals",
        "name": "RevVitals",
        "tm": False,
        "group": "Report & improve",
        "verb": "Improve",
        "status": "Live",
        "short": "A full revenue and OTA marketing health check, turned into a tracked action plan.",
        "tagline": "A health check, then the follow-through.",
        "title": "RevVitals: Hotel Revenue and OTA Health Check",
        "meta": "RevVitals reviews hotel pricing, distribution, OTA marketing on Expedia, Booking.com and Agoda, and market position, then tracks every action to done.",
        "intro": "A full revenue health review of each hotel, including its digital marketing on the OTAs, turned into a tracked list of actions, so recommendations don't stop at a slide deck.",
        "features": [
            ("OTA marketing levers", "Expedia Accelerator and promotions, Booking.com Genius and Booster, Agoda deals, a promotions calendar, content, photos and parity."),
            ("Hotel-by-hotel review", "Distribution, content, pricing and market position, reviewed for each property."),
            ("Action tracker", "Every recommendation followed through: done, in progress, awaiting the property, awaiting your approval or not started."),
            ("Proof it worked", "Before-and-after channel scores, the OTA team's live working sheets and quarterly OTA reviews in your owner portal."),
        ],
        "visual": {"type": "mock", "name": "revvitals"},
        "cta": ("See a sample report", "/revvitals-sample"),
        "faq": [
            ("What does a RevVitals review cover?", "Pricing, distribution, content, market position and OTA marketing on Expedia, Booking.com and Agoda, each graded and turned into actions."),
            ("Can I see an example?", "Yes. We publish an anonymised RevVitals report from a real engagement."),
        ],
        "related": ["foliolens", "askrank", "otarecon365"],
    },
    {
        "slug": "otarecon365",
        "name": "OTARecon365",
        "tm": True,
        "group": "Recover & retain",
        "verb": "Recover",
        "status": "Live",
        "short": "Every OTA payout audited booking by booking, and missing money recovered.",
        "tagline": "Collect what you're owed.",
        "title": "OTARecon365: OTA Payout Audit and Recovery",
        "meta": "OTARecon365 audits every Booking.com and Expedia payout booking by booking, tracks virtual cards before they expire and recovers missing money.",
        "intro": "Every OTA payout audited booking by booking across its full collection window, and the missing money chased until it lands in your account. You only pay on what we find.",
        "features": [
            ("Full-window audit", "Up to 365 days on Booking.com and 180 on Expedia, to find bookings never paid or under-paid."),
            ("Virtual cards tracked", "Pending virtual cards tracked against each OTA's charge deadline, so none expire uncollected."),
            ("Your money, your account", "Cards are charged through Stripe to the hotel's own account. We never see a card number."),
            ("Performance-based", "Our fee is a percentage of the recoverable amount we find, invoiced per hotel."),
        ],
        "visual": {"type": "mock", "name": "otarecon"},
        "cta": ("Open OTARecon365", "portal"),
        "faq": [
            ("How far back does OTARecon365 look?", "Up to 365 days on Booking.com and 180 days on Expedia."),
            ("Does BYLD handle card numbers?", "No. Cards are charged through Stripe to the hotel's own account and we never see a card number."),
            ("How is it priced?", "Performance-based: a percentage of the recoverable amount we find, invoiced per hotel."),
        ],
        "related": ["revvitals", "foliolens", "goldkey-rewards"],
    },
    {
        "slug": "goldkey-rewards",
        "name": "GoldKey Rewards",
        "tm": False,
        "group": "Recover & retain",
        "verb": "Retain",
        "status": "Launching",
        "short": "A loyalty program with your hotel's name on it that drives direct bookings.",
        "tagline": "Guests who come back, and book direct.",
        "title": "GoldKey Rewards: Your Own Hotel Loyalty Program",
        "meta": "GoldKey Rewards gives your hotel its own loyalty program: QR sign-up, member cards, four tiers, free nights and restaurant credit, on direct bookings only.",
        "intro": "A loyalty program with your hotel's name on it: “[Your Hotel] GoldKey Rewards”. Guests join at the front desk, get a personal welcome and a metal-look member card, and come back through your own booking engine instead of an OTA. No per-stay brand loyalty fees.",
        "features": [
            ("30-second sign-up", "By QR code at the front desk or the restaurant table."),
            ("A welcome that feels personal", "Your hotel's photo, their name, their member card and their reward, by email."),
            ("Rewards matched to the stay", "15% off the next direct stay, free nights, or a restaurant credit."),
            ("Direct bookings only", "Verified by staff, so rewards can't be shared or abused."),
            ("One membership across your group", "Stays at your hotels count together, and free nights work at any of them."),
            ("Four tiers", "Core, Platinum (10 nights), Executive (30 nights) and Black (by invitation)."),
        ],
        "visual": {"type": "mock", "name": "goldkey"},
        "cta": ("Talk to us about GoldKey", "/contact"),
        "faq": [
            ("Whose brand is on the program?", "Yours. Members join “[Your Hotel] GoldKey Rewards”, with your hotel's photo and name."),
            ("Can rewards be used on OTA bookings?", "No. Member codes work only on your own booking engine, which is the point: members come back direct."),
            ("Does it work across several hotels?", "Yes. Stays at your hotels count together, and free nights work at any of them."),
        ],
        "related": ["direct-booking", "pulsepilot", "bfis-pms"],
    },
    {
        "slug": "saleslock",
        "name": "SalesLock Concierge",
        "tm": True,
        "group": "Sell & be seen",
        "verb": "Sell groups",
        "status": "Pilot · Jan 2027",
        "short": "Group and RFP leads captured, approved by phone and answered before the deadline.",
        "tagline": "Never miss an RFP deadline.",
        "title": "SalesLock: Hotel Group Sales and RFP Response",
        "meta": "SalesLock captures group and RFP leads with their deadlines, gets one-tap rate approval from your Director of Sales and escalates until every reply is sent.",
        "intro": "Group and RFP enquiries come with deadlines, and they often arrive after hours. SalesLock starts the clock the moment a lead lands, puts it in front of your Director of Sales for a one-tap decision, and escalates until the response is in.",
        "features": [
            ("Every lead in one pipeline", "Captured from RFP platforms and email, each with its deadline."),
            ("One-tap approvals by phone", "Your Director of Sales approves the rate; if they're away, the GM steps in."),
            ("Escalating reminders", "Reminders get louder as each deadline gets closer, and your Remote Sales Manager submits every response."),
            ("One number that matters", "Missed RFPs: 0. Answers come fast because they're pre-filled from a property questionnaire."),
        ],
        "visual": {"type": "mock", "name": "saleslock"},
        "cta": ("See the SalesLock demo", "saleslock_demo"),
        "faq": [
            ("When is SalesLock available?", "SalesLock Concierge is in pilot from January 2027."),
            ("Who submits the RFP responses?", "Your Remote Sales Manager submits every response once the rate is approved."),
        ],
        "related": ["askrank", "pricecortex", "foliolens"],
    },
    {
        "slug": "askrank",
        "name": "AskRank",
        "tm": False,
        "group": "Sell & be seen",
        "verb": "Be found",
        "status": "Pilot starting",
        "short": "Search, listing and AI-assistant visibility, run for you and reported in your portal.",
        "tagline": "Be found first, on every screen that sells rooms.",
        "title": "AskRank: Hotel Search and AI Visibility",
        "meta": "AskRank runs your Google Business Profile, Expedia, Hotels.com and Tripadvisor sponsored listings, with every monthly budget approved by you.",
        "intro": "Your hotel's search, listing and AI visibility, run for you. We propose a monthly plan and budget, you approve it, and our team runs the campaigns and reports the return in your owner portal.",
        "features": [
            ("Visibility audit", "Where you rank, branded vs discovery searches, and the keywords you're missing."),
            ("Campaigns we run", "Google Business Profile, Expedia and Hotels.com sponsored listings, and Tripadvisor sponsored placements."),
            ("You stay in control", "Nothing runs until you approve the month's plan and budget."),
            ("Reported in your portal", "Spend, return on ad spend and rankings against your starting point. AI-assistant visibility is next."),
        ],
        "visual": {"type": "mock", "name": "askrank"},
        "cta": ("Ask about the AskRank pilot", "/contact"),
        "faq": [
            ("Does AskRank spend money without approval?", "No. Nothing runs until you approve the month's plan and budget."),
            ("What is AI visibility?", "How often AI assistants such as ChatGPT and Gemini recommend your hotel when travellers ask. Tracking it is the next AskRank module."),
        ],
        "related": ["revvitals", "direct-booking", "pulsepilot"],
    },
    {
        "slug": "pulsepilot",
        "name": "PulsePilot",
        "tm": True,
        "group": "Sell & be seen",
        "verb": "Protect reputation",
        "status": "Early access",
        "short": "In-stay guest feedback by QR, GM alerts in real time, and more Google reviews.",
        "tagline": "Hear it first. Fix it before checkout.",
        "title": "PulsePilot: In-Stay Guest Feedback and Reviews",
        "meta": "PulsePilot collects guest feedback by QR during the stay, alerts the GM in time to fix problems before checkout, and invites happy guests to review on Google.",
        "intro": "Guests scan a QR card at the front desk, in their room or at breakfast and tell you how their stay is going. Problems reach your GM privately while there's still time to fix them, and every guest is invited to share their stay on Google.",
        "features": [
            ("QR cards everywhere guests are", "Front desk, rooms and breakfast, printed with your hotel's logo."),
            ("Feedback with detail", "Star ratings for room, service, cleanliness and location, plus comments and photos."),
            ("GM alerts for every issue", "So it's handled the same day, not discovered in a one-star review."),
            ("Owner dashboard", "See, resolve and track every message, and download your QR codes."),
        ],
        "visual": {"type": "mock", "name": "pulsepilot"},
        "cta": ("Request early access", "/contact"),
        "faq": [
            ("When do guests give feedback?", "During their stay, by scanning a QR card, so problems can be fixed before checkout."),
            ("Does it help with online reviews?", "Yes. Every guest is invited to share their stay on Google."),
        ],
        "related": ["goldkey-rewards", "askrank", "revvitals"],
    },
    {
        "slug": "direct-booking",
        "name": "Website, Booking Engine & Photography",
        "nav_name": "Web, Booking & Photo",
        "tm": False,
        "group": "Sell & be seen",
        "verb": "Book direct",
        "status": "Service",
        "short": "A fast hotel website, a booking engine connected to any PMS in about a week, and pro photos.",
        "tagline": "Look as good online as you do in person.",
        "title": "Hotel Websites, Booking Engine and Photography",
        "meta": "Fast, search-friendly hotel websites, a direct booking engine connected to any PMS in about a week, and professional photography for your site and OTAs.",
        "intro": "Direct bookings start with how your hotel shows up online. We build the website, connect the booking engine to your PMS and shoot the photos, so guests find you, trust you and book with you, not through an OTA.",
        "features": [
            ("Website development", "A fast, mobile-first hotel website, search-friendly and AI-search ready, on your brand and your domain."),
            ("Booking engine integrated in about a week", "Connected to any PMS, typically within a week, with rates and availability kept in sync."),
            ("Member and promo codes", "Direct-only offers, including GoldKey member rates and free nights."),
            ("Professional photography", "Rooms, lobby, exterior and amenities, edited for your website and every OTA, to lift content scores."),
        ],
        "visual": {"type": "mock", "name": "booking"},
        "cta": ("Plan your website", "/contact"),
        "faq": [
            ("Which PMS can the booking engine connect to?", "Any PMS. Integration typically takes about a week."),
            ("Do I own the website and domain?", "Yes. It's your brand, your content and your domain."),
        ],
        "related": ["goldkey-rewards", "askrank", "bfis-pms"],
    },
]

GROUPS = ["Foundation", "Price & compete", "Report & improve", "Recover & retain", "Sell & be seen"]

COMING = [
    ("Halo™", "In design", "An AI revenue assistant in your owner portal: ask about pricing and our products in plain English, or pass a message to your revenue manager. Answers from your own hotel data will follow."),
    ("Signal™", "In development", "Demand signals from the wider market, layered onto pricing decisions."),
    ("AI booking concierge", "Exploring", "Chat and phone agents on your direct booking engine that answer guests, take bookings and apply GoldKey member rates and free nights."),
]

# ---------------------------------------------------------------------------------------------
# Franchise comparison. Left column describes the typical franchise model in general terms.
# ---------------------------------------------------------------------------------------------
FRANCHISE_ROWS = [
    ("Fees", "Royalty, marketing, reservation and loyalty fees, charged as a share of room revenue, every month.",
     "No royalty and no brand-marketing levy on your room revenue."),
    ("Revenue management", "Often an optional extra-cost program, or a shared remote team covering many hotels.",
     "A named revenue manager plus AI pricing for every room category, 57 nights ahead."),
    ("Loyalty", "Guests join the brand's program, and you pay for qualifying stays.",
     "Your own program, “[Your Hotel] GoldKey Rewards”, built to win direct bookings."),
    ("Direct booking", "The brand's website and reservation system, on the brand's terms.",
     "Your website on your domain, with a booking engine connected to your PMS in about a week."),
    ("Owner reporting", "Brand portals and separate STR reports to reconcile.",
     "FolioLens: actual vs plan vs last year vs market, and a weekly brief."),
    ("OTA payout audit", "Rarely part of the package.",
     "OTARecon365 audits every payout, up to 365 days back."),
    ("Group and RFP sales", "Shared brand sales channels.",
     "SalesLock: every RFP captured, approved by phone and answered before the deadline."),
    ("Guest feedback", "Brand surveys, after the guest has left.",
     "PulsePilot: feedback during the stay, fixed before checkout."),
    ("Systems", "Brand-mandated PMS and vendors.",
     "BFIS PMS, or keep the PMS you already run."),
]

AI_HUMAN = [
    ("AI and ML models", "Machine", "Read your PMS pace, booking curves, competitor rates and market data, then forecast demand and recommend rates for every room."),
    ("Guardrails", "Rules you set", "Floors, ceilings and your business rules are enforced on every recommendation. No model can cross them."),
    ("Human revenue manager", "Your RM", "Reviews each recommendation with its full reasoning, adjusts where judgement says so, and approves, in the portal or on WhatsApp."),
    ("Live and measured", "Results", "Approved rates go live. Every decision is logged and scored afterwards, so the models and the team keep learning."),
]

STEPS = [
    ("Discovery", "We review your hotels, systems and goals, and show you where revenue is being left behind."),
    ("Connect", "BFIS PMS or your current PMS connected, comp sets agreed, booking engine integrated in about a week."),
    ("Calibrate", "The AI runs alongside your revenue manager before anything changes, so you see the recommendations first."),
    ("Go live", "Owner portal and WhatsApp desk for your team; weekly performance briefs to owners."),
]

DATA_FLOW = {
    "in": ["Your PMS data: BFIS PMS, ASI, G6, IHG and other feeds", "Competitor rates from Booking.com", "CoStar STR market reports, monthly", "Your settings: floors, ceilings and targets"],
    "engine": ["AI and ML models forecast and recommend", "Guardrails enforced on every number", "Revenue manager reviews and approves", "Daily data-freshness checks"],
    "out": ["Owner portal: each person sees only their hotels", "Daily pricing on WhatsApp", "Weekly Performance Brief by email", "Recovery, loyalty, sales and guest-feedback reporting"],
}

PARTNERS = [
    ("Fundraising and equity", "Fundraising & Equity Partner", "Capital raising and equity partnerships for acquisitions and growth.", []),
    ("Management company", "LHM Hospitality Management LLC", "Full-service hotel management.", ["Hilton approved", "Marriott approved", "IHG approved"]),
    ("Accounting and taxation", "NPV Prime Advisors Inc.", "Hotel accounting, bookkeeping and tax services.", []),
]

HOME_FAQ = [
    ("How is BYLD different from a hotel franchise?",
     "A franchise gives you a flag and charges a share of room revenue for it. BYLD gives you the revenue engine behind the flag: a PMS, AI pricing approved by a named revenue manager, comp-set intelligence, owner reporting, OTA payout recovery, your own loyalty program, group sales, reputation and a direct booking website, without royalties or brand-marketing fees. Already flagged? We work alongside your brand and do the revenue work it doesn't."),
    ("Do I need to change my PMS?",
     "No. You can run BFIS PMS, our cloud PMS, or keep your current system. We already take feeds from ASI, G6, IHG and others, and can connect a direct booking engine to any PMS in about a week."),
    ("Does AI set my prices on its own?",
     "Never. Our models forecast and recommend, guardrails keep every number inside your floors and ceilings, and a named human revenue manager approves every rate before it goes live."),
    ("What kinds of hotels do you work with?",
     "Branded and independent hotels. Our portfolio includes properties flying Red Roof, Sonesta, Choice, Wyndham, Hilton, Marriott and IHG flags, as well as independents."),
    ("Who can see my hotel's data?",
     "Only the people you choose. In the owner portal each person sees only their own hotels, and OTARecon365 charges virtual cards through Stripe to your own account without us ever seeing a card number."),
    ("How do we get started?",
     "Book a revenue review. We look at your hotels, systems and goals, connect your PMS, run the AI alongside your revenue manager to calibrate, then go live with the owner portal and WhatsApp desk."),
]

FRANCHISE_FAQ = [
    ("Is BYLD a franchise?",
     "No. BYLD is a revenue operations partner. You keep your name, your guests and your data, and you don't pay royalties on room revenue."),
    ("I already have a brand. Is BYLD still for me?",
     "Yes. Many of our hotels fly major flags. Brands supply the name and the reservation system; BYLD supplies the daily revenue work that drives the numbers: pricing, comp-set tracking, owner reporting, OTA recovery, group sales and reputation."),
    ("What do independents lose without a franchise, and how do you replace it?",
     "Mainly distribution, loyalty and a revenue team. BYLD replaces them with a booking engine connected to your PMS in about a week, OTA marketing through RevVitals and AskRank, your own GoldKey Rewards program, and a named revenue manager backed by PriceCortex."),
]
