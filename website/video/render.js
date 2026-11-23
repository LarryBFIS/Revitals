// Render the BYLD product film into public/video/: tour.mp4 (H.264 + AAC), tour.webm (VP9 + Opus), tour-poster.jpg.
//
//   node video/render.js            full quality (60 fps capture blended to 30 fps for motion blur)
//   node video/render.js --draft    quick check (30 fps, no blur)
//
// Music: uses video/music.mp3 or video/music.wav if present (e.g. a licensed track), otherwise
// synthesizes the original score with video/soundtrack.py. Needs Playwright, ffmpeg and python3 + numpy.
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');

const DRAFT = process.argv.includes('--draft');
const CAP = DRAFT ? 30 : 60, OUT_FPS = 30, W = 1920, H = 1080;
const root = path.resolve(__dirname, '..');
const out = path.join(root, 'public/video');
const work = fs.mkdtempSync(path.join(os.tmpdir(), 'byld-film-'));
const ff = args => execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...args], { stdio: 'inherit' });

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.goto('file://' + path.join(__dirname, 'tour.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const { duration, scenes } = await p.evaluate(() => ({ duration: window.__DURATION, scenes: window.__TIMELINE }));
  fs.writeFileSync(path.join(work, 'timeline.json'), JSON.stringify({ duration, scenes }));

  // Stream frames straight into ffmpeg: no frames on disk. Motion blur = average of each pair of 60 fps frames.
  const master = path.join(work, 'master.mp4');
  // No film grain: random grain defeats compression (it took the MP4 from ~14 MB to 100 MB).
  const vf = [DRAFT ? null : 'tmix=frames=2:weights=1 1', `fps=${OUT_FPS}`, 'eq=contrast=1.03:saturation=1.06', 'format=yuv420p'].filter(Boolean).join(',');
  const enc = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(CAP), '-c:v', 'mjpeg', '-i', '-',
    '-vf', vf, '-c:v', 'libx264', '-crf', DRAFT ? '20' : '12', '-preset', DRAFT ? 'veryfast' : 'medium', master], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((res, rej) => enc.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg exited ' + c))));
  const total = Math.round(CAP * duration);
  for (let i = 0; i < total; i++) {
    await p.evaluate(t => window.__seek(t), i / CAP);
    const buf = await p.screenshot({ type: 'jpeg', quality: 93 });
    if (!enc.stdin.write(buf)) await new Promise(r => enc.stdin.once('drain', r));
    if (i % (CAP * 10) === 0) console.log(`frame ${i}/${total}`);
  }
  enc.stdin.end();
  // Poster: the platform grid, fully assembled.
  const plat = scenes.find(s => s.id === 'platform');
  await p.evaluate(t => window.__seek(t), plat.start + plat.dur - 0.5);
  await p.screenshot({ path: path.join(out, 'tour-poster.jpg'), type: 'jpeg', quality: 88 });
  await b.close();
  await done;

  let music = ['music.mp3', 'music.wav'].map(f => path.join(__dirname, f)).find(f => fs.existsSync(f));
  if (!music) {
    music = path.join(work, 'music.wav');
    execFileSync('python3', [path.join(__dirname, 'soundtrack.py'), path.join(work, 'timeline.json'), music], { stdio: 'inherit' });
  } else console.log('using music file', path.basename(music));

  const inputs = ['-i', master, '-i', music];
  const audio = ['-af', `loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=out:st=${(duration - 2).toFixed(2)}:d=2`, '-shortest'];
  ff([...inputs, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '23', '-preset', 'slow', '-tune', 'animation', '-profile:v', 'high', '-maxrate', '3M', '-bufsize', '6M',
      ...audio, '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', path.join(out, 'tour.mp4')]);
  ff([...inputs, '-map', '0:v', '-map', '1:a', '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '37', '-row-mt', '1', '-deadline', 'good', '-cpu-used', '4',
      ...audio, '-c:a', 'libopus', '-b:a', '160k', path.join(out, 'tour.webm')]);
  fs.rmSync(work, { recursive: true, force: true });
  for (const f of fs.readdirSync(out)) console.log(f, Math.round(fs.statSync(path.join(out, f)).size / 1024) + ' KB');
  console.log('duration', duration.toFixed(1), 's');
})();
