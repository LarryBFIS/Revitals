// Render video/tour.html frame by frame into public/video/tour.mp4, tour.webm, a 12s hero loop and posters.
// Usage: node video/render.js   (needs Playwright + ffmpeg). Takes a few minutes.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');

const FPS = 30, DURATION = 36, W = 1280, H = 720;
const root = path.resolve(__dirname, '..');
const out = path.join(root, 'public/video');
const frames = fs.mkdtempSync(path.join(os.tmpdir(), 'byld-tour-'));

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.goto('file://' + path.join(__dirname, 'tour.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => document.getAnimations().forEach(a => a.pause()));
  const total = FPS * DURATION;
  for (let i = 0; i < total; i++) {
    const ms = (i / FPS) * 1000;
    await p.evaluate(t => document.getAnimations().forEach(a => { a.currentTime = t; }), ms);
    await p.screenshot({ path: path.join(frames, String(i).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 92 });
    if (i % 150 === 0) process.stdout.write(`frame ${i}/${total}\n`);
  }
  await b.close();
  const src = ['-y', '-framerate', String(FPS), '-i', path.join(frames, '%05d.jpg')];
  const ff = args => execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', ...args], { stdio: 'inherit' });
  ff([...src, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '24', '-preset', 'slow', '-movflags', '+faststart', path.join(out, 'tour.mp4')]);
  ff([...src, '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '38', '-row-mt', '1', path.join(out, 'tour.webm')]);
  // Poster frames: title card and the end card.
  fs.copyFileSync(path.join(frames, String(FPS * 3).padStart(5, '0') + '.jpg'), path.join(out, 'tour-poster.jpg'));
  fs.rmSync(frames, { recursive: true, force: true });
  for (const f of fs.readdirSync(out)) console.log(f, Math.round(fs.statSync(path.join(out, f)).size / 1024) + ' KB');
})();
