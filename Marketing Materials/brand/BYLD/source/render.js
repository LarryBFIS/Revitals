// Export PNG and PDF versions of the SVGs, and the brand guide PDF.
// Run after build_logo.py:  node render.js   (needs Playwright + Chromium)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
// The SVG markup goes into the page inline: a blank page may not load file:// images.
const svgText = (n) => fs.readFileSync(path.join(ROOT, 'svg', n), 'utf8');
const frame = (n, w, h, bg) =>
  `<html style="background:${bg}"><head><style>html,body{margin:0;background:${bg}}svg{display:block;width:${w}px;height:${h}px}</style></head><body>${svgText(n)}</body></html>`;
const out = (...p) => { const f = path.join(ROOT, ...p); fs.mkdirSync(path.dirname(f), { recursive: true }); return f; };
const LOGO_RATIO = 124 / 394;
const ON_DARK_RATIO = 224 / 494;

async function png(page, svg, w, h, file) {
  await page.setViewportSize({ width: w, height: h });
  await page.setContent(frame(svg, w, h, 'transparent'));
  await page.screenshot({ path: file, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
}

async function pdf(page, svg, w, h, file) {
  await page.setContent(frame(svg, w, h, 'transparent'));
  await page.pdf({ path: file, width: `${w}px`, height: `${h}px`, printBackground: true, pageRanges: '1' });
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  for (const w of [600, 1200, 2400]) {
    await png(page, 'byld-logo.svg', w, Math.round(w * LOGO_RATIO), out('png', `byld-logo-${w}.png`));
    await png(page, 'byld-logo-white.svg', w, Math.round(w * LOGO_RATIO), out('png', `byld-logo-white-${w}.png`));
    await png(page, 'byld-logo-on-dark.svg', w, Math.round(w * ON_DARK_RATIO), out('png', `byld-logo-on-dark-${w}.png`));
  }
  for (const s of [1024, 512, 256]) await png(page, 'byld-icon.svg', s, s, out('png', `byld-icon-${s}.png`));
  await png(page, 'byld-icon.svg', 180, 180, out('favicon', 'apple-touch-icon.png'));
  for (const s of [16, 32, 48, 64]) await png(page, 'favicon.svg', s, s, out('favicon', `favicon-${s}.png`));
  fs.copyFileSync(path.join(ROOT, 'svg', 'favicon.svg'), out('favicon', 'favicon.svg'));

  await pdf(page, 'byld-logo-on-dark.svg', 988, 448, out('pdf', 'byld-logo-on-dark.pdf'));
  await pdf(page, 'byld-logo.svg', 788, 248, out('pdf', 'byld-logo-transparent.pdf'));
  await pdf(page, 'byld-icon.svg', 400, 400, out('pdf', 'byld-icon.pdf'));

  await page.goto('file://' + path.join(__dirname, 'guide.html'));
  await page.waitForLoadState('networkidle');
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: out('BYLD-Brand-Guide.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });

  await browser.close();
  console.log('Exported PNG, PDF and the brand guide.');
})();
