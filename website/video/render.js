// Render video/tour.html frame by frame, add the synthesized soundtrack, and write public/video/:
//   tour.mp4 (H.264 + AAC), tour.webm (VP9 + Opus), tour-poster.jpg
// Usage: node video/render.js   (needs Playwright, ffmpeg, python3 with numpy). Takes several minutes.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');

const FPS = 30, W = 1920, H = 1080;
const root = path.resolve(__dirname, '..');
const out = path.join(root, 'public/video');
const work = fs.mkdtempSync(path.join(os.tmpdir(), 'byld-tour-'));
const frames = path.join(work, 'f'); fs.mkdirSync(frames);
const ff = args => execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...args], { stdio: 'inherit' });

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.goto('file://' + path.join(__dirname, 'tour.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const { duration, scenes } = await p.evaluate(() => ({ duration: window.__DURATION, scenes: window.__TIMELINE }));
  fs.writeFileSync(path.join(work, 'timeline.json'), JSON.stringify({ duration, scenes }));
  const total = Math.round(FPS * duration);
  for (let i = 0; i < total; i++) {
    await p.evaluate(t => window.__seek(t), i / FPS);
    await p.screenshot({ path: path.join(frames, String(i).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 90 });
    if (i % 300 === 0) console.log(`frame ${i}/${total}`);
  }
  // Poster: the platform map, fully drawn.
  const map = scenes.find(s => s.id === 'map');
  await p.evaluate(t => window.__seek(t), map.start + 3.2);
  await p.screenshot({ path: path.join(out, 'tour-poster.jpg'), type: 'jpeg', quality: 86 });
  await b.close();

  const wav = path.join(work, 'music.wav');
  execFileSync('python3', [path.join(__dirname, 'soundtrack.py'), path.join(work, 'timeline.json'), wav], { stdio: 'inherit' });

  const src = ['-framerate', String(FPS), '-i', path.join(frames, '%05d.jpg'), '-i', wav];
  const audio = ['-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-shortest'];
  ff([...src, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '22', '-preset', 'slow', '-tune', 'animation',
      ...audio, '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', path.join(out, 'tour.mp4')]);
  ff([...src, '-map', '0:v', '-map', '1:a', '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '36', '-row-mt', '1', '-deadline', 'good', '-cpu-used', '2',
      ...audio, '-c:a', 'libopus', '-b:a', '128k', path.join(out, 'tour.webm')]);
  fs.rmSync(work, { recursive: true, force: true });
  for (const f of fs.readdirSync(out)) console.log(f, Math.round(fs.statSync(path.join(out, f)).size / 1024) + ' KB');
  console.log('duration', duration);
})();
