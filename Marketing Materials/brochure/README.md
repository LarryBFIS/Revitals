# BYLD Revenue Operations page

Interactive marketing page for Buildd From Ideas (BYLD): BFIS PMS, PriceCortex™, CompMatrix™, FolioLens™,
RevVitals, OTARecon365™, GoldKey Rewards, SalesLock™ Concierge, KeyCircle, AskRank, PulsePilot™,
Web & Photo, the WhatsApp revenue desk and partners.

| Path | What it is |
| --- | --- |
| `index.html` | Source page. Edit this. |
| `assets/` | Logo and real product screenshots referenced by the page. |
| `build.py` | Inlines `assets/` into one self-contained file. |
| `keycircle/index.html` | KeyCircle interactive demo, linked from the KeyCircle chapter. |
| `dist/BYLD_Revenue_Operations.html` | Single-file build to email, upload or share. |

## Edit and preview

Open `index.html` in a browser. Images load from `assets/`.

## Build a shareable single file

```bash
python3 build.py
```

## Adding a screenshot

Save it in `assets/` (JPEG for screenshots, keep it under ~200 KB) and reference it as
`assets/<name>.jpg`. Run `build.py` again before sharing.
