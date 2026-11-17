// Render 1200x630 social share images into public/og/ from public/og-jobs.json (written by build.py).
// Usage: node og.js   (needs Playwright + Chromium; run after build.py when titles change)
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');

const root = __dirname;
const jobs = JSON.parse(fs.readFileSync(path.join(root, 'og-jobs.json'), 'utf8'));
const logo = fs.readFileSync(path.join(root, 'static/img/byld-logo.svg'), 'utf8');
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const html = (title, sub) => `<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;600&family=Geist+Mono:wght@500&display=swap" rel="stylesheet">
<style>
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#080B1F;color:#fff;font-family:Geist,sans-serif;position:relative;overflow:hidden;padding:72px 80px;display:flex;flex-direction:column}
body::before{content:"";position:absolute;inset:0;background:radial-gradient(560px 380px at 85% 10%,rgba(92,192,255,.28),transparent 70%),radial-gradient(520px 360px at 5% 0%,rgba(124,140,255,.2),transparent 70%)}
body::after{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);background-size:64px 64px;-webkit-mask-image:radial-gradient(ellipse 80% 80% at 70% 0%,#000 20%,transparent 75%)}
.l{position:relative;z-index:1;height:40px}.l svg{height:40px;width:auto}
h1{position:relative;z-index:1;font-size:${title.length > 40 ? 62 : 74}px;line-height:1.04;letter-spacing:-.035em;font-weight:600;margin-top:auto;max-width:1000px}
p{position:relative;z-index:1;font-size:27px;line-height:1.4;color:#C9D1E6;margin-top:22px;max-width:960px}
.u{position:relative;z-index:1;font:500 20px 'Geist Mono',monospace;color:#5CC0FF;margin-top:34px}
</style></head><body><div class="l">${logo}</div><h1>${esc(title)}</h1><p>${esc(sub)}</p><div class="u">buildfromideas.com</div></body></html>`;

(async () => {
  const out = path.join(root, 'public/og');
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  for (const j of jobs) {
    let sub = j.sub.length > 150 ? j.sub.slice(0, j.sub.lastIndexOf(' ', 147)) + '…' : j.sub;
    await p.setContent(html(j.title, sub), { waitUntil: 'networkidle' });
    await p.screenshot({ path: path.join(out, j.name + '.png') });
  }
  // revvitals sample page share image
  await p.setContent(html('RevVitals sample report', 'An anonymised hotel revenue health check from a real BYLD engagement.'), { waitUntil: 'networkidle' });
  await p.screenshot({ path: path.join(out, 'revvitals-sample.png') });
  await b.close();
  console.log(`Wrote ${jobs.length + 1} images to public/og/`);
})();
