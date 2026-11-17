# Revitals repo: notes for Claude

This repo holds Buildd From Ideas (BYLD) marketing work. BYLD runs hotel revenue operations: BFIS PMS,
PriceCortex™, CompMatrix™, FolioLens™, RevVitals, OTARecon365™, GoldKey Rewards, SalesLock™ Concierge,
AskRank, PulsePilot™, websites/booking engine/photography, a WhatsApp revenue desk and partners.

## The website (`website/`)

The owner has asked Claude to own and continuously improve buildfromideas.com. Read `website/README.md`.

- All copy lives in `website/content.py`. Templates and SEO in `website/build.py`.
- After any change: `cd website && python3 build.py` (and `node og.js` if titles changed). Commit `public/` too.
- Positioning: **"More than a franchise. Without the franchise fees."** BYLD gives hotels the revenue engine a
  franchise promises (revenue management, loyalty, direct booking, reporting, sales) without royalties.
  Works for independents (franchise alternative) and branded hotels (the revenue team the brand doesn't provide).
- Every rate is approved by a named human revenue manager. Never describe pricing as fully automatic.
- Do not invent customers, testimonials, numbers or certifications. Mark mock-ups as illustrative.
- When products change elsewhere in the owner's projects, update `PRODUCTS` status and copy to match.
- Keep each `<title>` ≤ 60 characters (including " | BYLD") and each meta description ≤ 160.

## Older material

`Marketing Materials/brochure/` is the original single-page brochure (still useful as an emailable file).
`Marketing Materials/brand/BYLD/` is the logo pack and brand guide.
