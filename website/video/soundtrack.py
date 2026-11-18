#!/usr/bin/env python3
"""Original soundtrack for the BYLD product film, scored to its scenes (100 BPM).

    python3 video/soundtrack.py timeline.json out.wav

timeline.json comes from render.js: {"duration": s, "scenes": [{"id", "start", "dur", "prod"}, ...]}.
Pure numpy. Everything is synthesized here, so there is nothing to license.
Arrangement: hook (word hits) → lockup (impact, pad bloom) → platform (build) → products (full groove,
a hit on every title card) → WhatsApp (groove) → next (breakdown) → outro (impact, final chord, fade).
"""
import json, sys, wave
import numpy as np

SR = 44100
BEAT = 0.6
rng = np.random.default_rng(11)
tl = json.load(open(sys.argv[1]))
END = tl["duration"]; N = int((END + 0.3) * SR)
L = np.zeros(N); R = np.zeros(N)
sc = {s["id"]: s for s in tl["scenes"]}
prods = [s for s in tl["scenes"] if s.get("prod")]
T_LOCK, T_PLAT, T_PROD = sc["lockup"]["start"], sc["platform"]["start"], prods[0]["start"]
T_WA, T_NEXT, T_OUT = sc["wa"]["start"], sc["next"]["start"], sc["outro"]["start"]
TC = 1.2

def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def env_adsr(n, a, r):
    t = np.arange(n) / SR; T = n / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.clip((T - t) / max(r, 1e-4), 0, 1)
def add(sig, at, g=1.0, pan=0.0):
    i = int(round(at * SR))
    if i >= N or i + len(sig) <= 0: return
    if i < 0: sig = sig[-i:]; i = 0
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * g * np.sqrt((1 - pan) / 2) * 1.414
    R[i:i + len(sig)] += sig * g * np.sqrt((1 + pan) / 2) * 1.414

def saw_voice(f, n, cutoff, detunes=(-0.008, -0.003, 0.003, 0.008)):
    """Band-limited saw stack with a soft low-pass: harmonics above `cutoff` Hz roll off."""
    t = np.arange(n) / SR; out = np.zeros(n)
    hmax = int(min(40, (SR / 2.2) / f))
    for d in detunes:
        ff = f * (1 + d); ph = rng.uniform(0, 2 * np.pi)
        for h in range(1, hmax + 1):
            fh = ff * h
            a = (1 / h) / (1 + (fh / cutoff) ** 4)
            if a < 1e-4: break
            out += a * np.sin(2 * np.pi * fh * t + ph * h)
    return out / len(detunes)

# Dmaj9 · Bm9 · Gmaj7 · A6sus, two bars each
CHORDS = [[50, 57, 61, 64, 66], [47, 54, 57, 61, 66], [43, 50, 54, 59, 66], [45, 52, 57, 62, 64]]
BAR = BEAT * 4
def chord_at(t): return CHORDS[int(t // (BAR * 2)) % 4]

# ---------------- pad bed: cutoff opens and closes with the arrangement ----------------
def cutoff_at(t):
    if t < T_LOCK: return 500
    if t < T_PLAT: return 1400
    if t < T_PROD: return 1400 + 2200 * (t - T_PLAT) / (T_PROD - T_PLAT)
    if t < T_NEXT: return 3200
    if t < T_OUT: return 900
    return 4200
seg = BAR * 2; t = 0.0
while t < END:
    ch = chord_at(t + 0.01); n = int((seg + 1.6) * SR)
    cut = cutoff_at(t + seg / 2)
    gain = 0.035 if t < T_LOCK else 0.05
    for j, m in enumerate(ch):
        v = saw_voice(mtof(m), n, cut) * env_adsr(n, 0.9, 1.4)
        add(v, t, gain, pan=(-0.6 + 1.2 * j / 4))
    # sub bass on the root
    tt = np.arange(n) / SR; f = mtof(ch[0] - 24)
    sub = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * env_adsr(n, 0.05, 0.6)
    add(sub, t, 0.0 if t < T_LOCK else (0.12 if t < T_PROD else 0.2))
    t += seg

# ---------------- drums ----------------
def kick(g=1.0):
    n = int(0.5 * SR); tt = np.arange(n) / SR
    f = 44 + 140 * np.exp(-tt / 0.035)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.2)
    click = rng.standard_normal(n) * np.exp(-tt / 0.003) * 0.25
    return np.tanh(1.6 * (body + click)) * g
def clap():
    n = int(0.35 * SR); tt = np.arange(n) / SR; x = rng.standard_normal(n)
    hp = x - np.convolve(x, np.ones(12) / 12, 'same'); bp = np.convolve(hp, np.ones(3) / 3, 'same')
    e = np.zeros(n)
    for o in (0, 0.011, 0.022): e += (tt >= o) * np.exp(-np.clip(tt - o, 0, None) / 0.012)
    e += (tt >= 0.03) * np.exp(-np.clip(tt - 0.03, 0, None) / 0.11) * 0.7
    return bp * e
def hat(open_=False):
    n = int((0.25 if open_ else 0.06) * SR); tt = np.arange(n) / SR; x = rng.standard_normal(n)
    hp = x - np.convolve(x, np.ones(4) / 4, 'same')
    return hp * np.exp(-tt / (0.07 if open_ else 0.014))

pump = np.ones(N)
def duck(at, depth=0.55, rel=0.16):
    i = int(at * SR); m = min(N, i + int(0.45 * SR))
    if i < N: pump[i:m] = np.minimum(pump[i:m], 1 - depth * np.exp(-np.arange(m - i) / SR / rel))

b = 0
while b * BEAT < END - 1.2:
    at = b * BEAT; beat_in_bar = b % 4
    if T_PLAT <= at < T_NEXT or (T_OUT <= at < T_OUT + BAR * 1):
        build = at < T_PROD
        add(kick(), at, 0.32 if build else 0.42); duck(at)
        if not build:
            if beat_in_bar in (1, 3): add(clap(), at, 0.16, pan=0.05)
            add(hat(), at + BEAT / 2, 0.045, pan=0.35)
            add(hat(), at + BEAT / 4, 0.015, pan=-0.35); add(hat(), at + 3 * BEAT / 4, 0.018, pan=-0.35)
            if b % 8 == 7: add(hat(True), at + BEAT / 2, 0.05, pan=0.2)
    b += 1
# snare-roll build into the first product
roll_start = T_PROD - BAR
k = 0
while roll_start + k * BEAT / 4 < T_PROD:
    x = roll_start + k * BEAT / 4; prog = (x - roll_start) / BAR
    add(clap(), x, 0.04 + 0.12 * prog ** 2, pan=0.1 * np.sin(k)); k += 1

# ---------------- arpeggio (dotted-eighth echo), products through WhatsApp ----------------
def pluck(f):
    n = int(0.45 * SR); tt = np.arange(n) / SR
    s = saw_voice(f, n, 2600, detunes=(-0.002, 0.002))
    return s * np.exp(-tt / 0.11) * np.minimum(1, tt / 0.003)
pat = [0, 2, 4, 3, 1, 3, 4, 2]; i = 0; x = T_LOCK + BAR
while x < T_NEXT + (T_OUT - T_NEXT) * 0.7:
    ch = chord_at(x); m = ch[pat[i % 8] % len(ch)] + 12
    g = 0.03 if x < T_PROD else (0.045 if x < T_NEXT else 0.03)
    p = pluck(mtof(m)); add(p, x, g, pan=0.4 * np.sin(i * 0.9)); add(p, x + BEAT * 0.75, g * 0.45, pan=-0.45 * np.sin(i * 0.9))
    x += BEAT / 2; i += 1

# ---------------- hits, risers, whooshes, impacts ----------------
def noise_sweep(length, rising=True, g=1.0):
    n = int(length * SR); x = rng.standard_normal(n); cs = np.concatenate([[0], np.cumsum(x)])
    w = np.linspace(40, 2, n) if rising else np.linspace(2, 40, n); w = w.astype(int)
    idx = np.arange(n); y = (cs[idx + 1] - cs[np.maximum(0, idx + 1 - w)]) / w
    e = (idx / n) ** 2 if rising else (1 - idx / n) ** 2
    return y * e * g
def impact(g=1.0, tail=2.2):
    n = int(tail * SR); tt = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(34 + 90 * np.exp(-tt / 0.07)) / SR) * np.exp(-tt / 0.7)
    x = rng.standard_normal(n); hp = x - np.convolve(x, np.ones(6) / 6, 'same')
    return (np.tanh(1.5 * boom) + hp * np.exp(-tt / 0.5) * 0.12) * g
def stab(ch, g=1.0, cut=3500, length=0.9):
    n = int(length * SR); out = np.zeros(n)
    for m in ch: out += saw_voice(mtof(m + 12), n, cut)
    return out / len(ch) * np.exp(-np.arange(n) / SR / 0.25) * g

# hook: a hit on every word (beats 0, 2, 4, 6)
for j in range(4):
    at = j * BEAT * 2
    add(impact(0.55 if j < 3 else 0.7, 1.4), at, 0.5)
    add(stab(CHORDS[j % 4], 1.0, 1800 + 600 * j), at, 0.22)
    if j: add(noise_sweep(0.5, True, 1.2), at - 0.5, 0.18)
add(noise_sweep(1.2, True, 1.4), T_LOCK - 1.2, 0.3)
add(impact(1.0, 2.8), T_LOCK, 0.62); add(stab(CHORDS[0], 1.0, 4200, 2.4), T_LOCK, 0.2)
add(noise_sweep(2.4, True, 1.5), T_PROD - 2.4, 0.26)
# every product title card: whoosh in, hit on the card, small swell into the demo
for s in prods + [sc["wa"]]:
    add(noise_sweep(0.55, True, 1.2), s["start"] - 0.55, 0.22, pan=0.2)
    add(impact(0.5, 1.2), s["start"], 0.3)
    add(stab(chord_at(s["start"] + 0.01), 1.0, 3800, 0.7), s["start"], 0.12)
    add(noise_sweep(0.35, False, 0.9), s["start"] + TC, 0.08, pan=-0.2)
add(noise_sweep(2.0, False, 1.2), T_NEXT, 0.18)
add(noise_sweep(1.8, True, 1.6), T_OUT - 1.8, 0.34)
add(impact(1.0, 3.5), T_OUT, 0.7)
n = int(6.5 * SR)
for j, m in enumerate(CHORDS[0] + [74]):
    add(saw_voice(mtof(m + 12), n, 5200) * env_adsr(n, 0.02, 5.5) * np.exp(-np.arange(n) / SR / 2.6), T_OUT, 0.05, pan=-0.5 + j / 5)

# ---------------- mix ----------------
L *= pump; R *= pump
def reverb(x, sec=2.8, seed=1, pre=0.02):
    r = np.random.default_rng(seed); n = int(sec * SR); tt = np.arange(n) / SR
    ir = r.standard_normal(n) * np.exp(-tt / (sec / 6)); ir[: int(pre * SR)] = 0
    ir = np.convolve(ir, np.ones(8) / 8, 'same')  # darker tail
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return y / (np.sqrt((ir ** 2).sum()) + 1e-9)
wl, wr = reverb(L, seed=3), reverb(R, seed=4)
L = L + 0.22 * wl; R = R + 0.22 * wr
fade = np.ones(N); fi = int(0.05 * SR); fade[:fi] = np.linspace(0, 1, fi)
fo = int(2.8 * SR); e = int(END * SR); fade[e - fo:e] = np.linspace(1, 0, fo) ** 1.6; fade[e:] = 0
L *= fade; R *= fade
pk = max(np.abs(L).max(), np.abs(R).max())
L = np.tanh(1.8 * L / pk) / np.tanh(1.8); R = np.tanh(1.8 * R / pk) / np.tanh(1.8)
pcm = (np.stack([L, R], 1) * 0.9 * 32767).astype(np.int16)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print(f"wrote {sys.argv[2]} ({END:.1f}s)")
