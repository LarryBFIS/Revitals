#!/usr/bin/env python3
"""Synthesize an original soundtrack for the product tour, timed to its scenes.

    python3 video/soundtrack.py timeline.json out.wav

timeline.json is written by render.js: {"duration": seconds, "scenes": [{"id", "start", "dur"}, ...]}.
Only numpy is needed. Everything is generated here, so there are no licensing questions.
"""
import json, sys, wave
import numpy as np

SR = 44100
BPM = 100
BEAT = 60 / BPM
rng = np.random.default_rng(7)

tl = json.load(open(sys.argv[1]))
DUR = tl["duration"] + 0.5
N = int(DUR * SR)
t = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
scenes = {s["id"]: s for s in tl["scenes"]}
first_prod = next(s["start"] for s in tl["scenes"] if s["id"].startswith("prod"))
next_start = scenes["next"]["start"]; outro = scenes["outro"]["start"]; map_start = scenes["map"]["start"]

def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N: return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * gain * (1 - pan) ** 0.5
    R[i:i + len(sig)] += sig * gain * (1 + pan) ** 0.5

# ---- chords: Dmaj9, Bm9, Gmaj7, Asus ----
CHORDS = [[50, 57, 61, 64, 66], [47, 54, 57, 61, 62], [43, 50, 54, 59, 64], [45, 52, 57, 62, 64]]
CH_LEN = BEAT * 8  # two bars

def pad_note(freq, length):
    n = int(length * SR); tt = np.arange(n) / SR
    sig = np.zeros(n)
    for det in (-0.006, 0.0, 0.0065):
        f = freq * (1 + det)
        for h in range(1, 8):
            sig += np.sin(2 * np.pi * f * h * tt + rng.uniform(0, 6.28)) / h ** 1.7
    env = np.minimum(1, tt / 1.4) * np.minimum(1, (length - tt) / 1.2).clip(0)
    trem = 1 + 0.08 * np.sin(2 * np.pi * 0.23 * tt)
    return sig * env * trem / 3

k = 0; start = 0.0
while start < DUR:
    ch = CHORDS[k % 4]
    length = CH_LEN + 1.4
    for j, m in enumerate(ch):
        add(pad_note(mtof(m), length), start, 0.055, pan=(-0.5 + j / 4) * 0.8)
    # sub bass on the root, an octave down
    n = int(length * SR); tt = np.arange(n) / SR
    f = mtof(ch[0] - 12)
    sub = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt)) * np.minimum(1, tt / 0.3) * np.minimum(1, (length - tt) / 0.8).clip(0)
    add(sub, start, 0.16 if start >= map_start - 0.1 else 0.06)
    start += CH_LEN; k += 1

# ---- drums: in from the map, full from the first product, break for "next", back for the outro ----
def kick():
    n = int(0.45 * SR); tt = np.arange(n) / SR
    f = 46 + 110 * np.exp(-tt / 0.045)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.16)

def hat():
    n = int(0.06 * SR); x = rng.standard_normal(n)
    x = np.diff(np.concatenate([[0], x]))  # crude high-pass
    return x * np.exp(-np.arange(n) / SR / 0.012)

K, H = kick(), hat()
beat_t = np.arange(0, DUR, BEAT)
pump = np.ones(N)
for bt in beat_t:
    in_break = next_start <= bt < outro
    if bt < map_start or in_break or bt > tl["duration"] - 2.5:
        continue
    g = 0.22 if bt < first_prod else 0.38
    add(K, bt, g)
    i = int(bt * SR); m = min(N, i + int(0.35 * SR))
    pump[i:m] = np.minimum(pump[i:m], 1 - 0.45 * np.exp(-np.arange(m - i) / SR / 0.11))
    if bt >= first_prod:
        add(H, bt + BEAT / 2, 0.05, pan=0.3)
        add(H, bt + BEAT * 0.75, 0.025, pan=-0.3)

# ---- arpeggio from the first product to the break ----
def pluck(freq):
    n = int(0.5 * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * tt) + 0.35 * np.sin(4 * np.pi * freq * tt) + 0.12 * np.sin(6 * np.pi * freq * tt)
    return s * np.exp(-tt / 0.13) * np.minimum(1, tt / 0.004)

pattern = [0, 2, 3, 4, 3, 2, 1, 2]
step = BEAT / 2
x = first_prod; i = 0
while x < next_start - 0.2:
    ch = CHORDS[int(x // CH_LEN) % 4]
    m = ch[pattern[i % 8] % len(ch)] + 24
    p = pluck(mtof(m))
    add(p, x, 0.05, pan=0.35 * np.sin(i * 0.7))
    add(p, x + BEAT * 0.75, 0.022, pan=-0.4 * np.sin(i * 0.7))  # dotted-eighth echo
    x += step; i += 1

# ---- whooshes into each scene, riser into the map, impact on the outro ----
def whoosh(length=0.7, bright=1.0):
    n = int(length * SR); x = rng.standard_normal(n)
    out = np.zeros(n); win = np.linspace(28, 3, n).astype(int)  # darker to brighter
    cs = np.cumsum(np.concatenate([[0], x]))
    for a in range(0, n, 256):
        w = win[a]; b = min(n, a + 256); idx = np.arange(a, b)
        out[a:b] = (cs[idx + 1] - cs[np.maximum(0, idx + 1 - w)]) / w
    env = (np.arange(n) / n) ** 2.2
    return out * env * bright

for s in tl["scenes"][1:]:
    add(whoosh(0.75), max(0, s["start"] - 0.7), 0.5, pan=0.2)
riser = whoosh(2.6, 1.3)
add(riser, map_start - 2.5, 0.16)
add(whoosh(1.6, 1.2), outro - 1.5, 0.55)

n = int(3.5 * SR); tt = np.arange(n) / SR
boom = np.sin(2 * np.pi * np.cumsum(38 + 80 * np.exp(-tt / 0.08)) / SR) * np.exp(-tt / 0.9)
crash = rng.standard_normal(n); crash = np.diff(np.concatenate([[0], crash])) * np.exp(-tt / 1.1)
add(boom, outro, 0.38); add(crash, outro, 0.035)
for m in CHORDS[0]:
    add(pad_note(mtof(m + 12), 6.5), outro, 0.04)

# ---- mix: sidechain pump on the pad bed, reverb, soft clip, fades ----
L *= pump; R *= pump
def reverb(x, seconds=2.6, seed=1):
    r = np.random.default_rng(seed)
    n = int(seconds * SR); tt = np.arange(n) / SR
    ir = r.standard_normal(n) * np.exp(-tt / (seconds / 5))
    ir[: int(0.012 * SR)] = 0
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return y / (np.abs(ir).sum() ** 0.5)
wetL, wetR = reverb(L, seed=1), reverb(R, seed=2)
L = L + 0.32 * wetL / (np.abs(wetL).max() + 1e-9) * np.abs(L).max()
R = R + 0.32 * wetR / (np.abs(wetR).max() + 1e-9) * np.abs(R).max()

fade = np.ones(N)
fi = int(1.2 * SR); fade[:fi] = np.linspace(0, 1, fi) ** 2
fo = int(3.0 * SR); end = int(tl["duration"] * SR)
fade[end - fo:end] = np.linspace(1, 0, fo) ** 1.5; fade[end:] = 0
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = np.tanh(1.4 * L / peak) / np.tanh(1.4), np.tanh(1.4 * R / peak) / np.tanh(1.4)
pcm = (np.stack([L, R], 1) * 0.89 * 32767).astype(np.int16)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print(f"wrote {sys.argv[2]} ({DUR:.1f}s)")
