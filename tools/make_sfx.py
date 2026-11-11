# Synthesizes every sound effect (assets/sfx/*.mp3) and the three music loops (assets/music/*.mp3).
# Pure additive synthesis with numpy, encoded with ffmpeg. Run from the repo root:
#   python tools/make_sfx.py                 # everything
#   python tools/make_sfx.py sfx | music     # one half
#   python tools/make_sfx.py pop DIR         # write the three pop candidates (wav) into DIR and print metrics
import numpy as np, wave, subprocess, os, sys, tempfile
SR = 44100
PEAK = 10 ** (-3 / 20)          # -3 dB
POP = "a"                       # chosen pop candidate (see pop_variants)
rng = np.random.default_rng(7)

# ---------- building blocks ----------
def tone(f, dur, parts, attack=0.003, bend=None):
    """Sum of decaying sine partials. parts = [(freq ratio, amp, decay tau s)]. bend = (start ratio, tau)."""
    n = int(dur * SR); t = np.arange(n) / SR
    ft = np.full(n, float(f)) if bend is None else f * (1 + (bend[0] - 1) * np.exp(-t / bend[1]))
    ph = 2 * np.pi * np.cumsum(ft) / SR
    y = np.zeros(n)
    for r, a, tau in parts:
        if f * r < 15000: y += a * np.sin(r * ph) * np.exp(-t / tau)
    return y * np.minimum(1, t / attack)

def marimba(f): return [(1, 1, .30 * (523 / f) ** .5), (4, .30, .06), (10, .05, .012)]
def glock(f):   return [(1, 1, .45), (2.76, .30, .22), (5.4, .10, .09), (8.9, .03, .04)]
def softbell(f):return [(1, 1, .60), (2, .20, .30), (3, .06, .15)]
def pluck(f):   return [(k, 1 / k ** 1.3, .55 / k ** .8) for k in range(1, 8)]
def bass(f):    return [(1, 1, .45), (2, .5, .30), (3, .12, .18)]

def noise(n, lo, hi):
    """White noise band-limited with smooth (Butterworth-like) skirts."""
    X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR); f[0] = 1e-6
    X *= 1 / np.sqrt(1 + (lo / f) ** 6) / np.sqrt(1 + (f / hi) ** 6)
    y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)

def svf_bp(x, fc, q=2.0):
    """Time-varying band-pass (state variable filter); fc is an array in Hz."""
    low = band = 0.0; out = np.empty(len(x)); k = 2 * np.sin(np.pi * np.minimum(fc, SR / 6.5) / SR)
    for i in range(len(x)):
        high = x[i] - low - band / q; band += k[i] * high; low += k[i] * band; out[i] = band
    return out

def put(buf, t0, y, g=1.0):
    i = int(t0 * SR); e = min(len(buf), i + len(y))
    if e > i: buf[i:e] += g * y[:e - i]

def finish(y, dur):
    """Trim leading silence, cut to dur, fade the ends, normalize to -3 dB."""
    thr = np.abs(y).max() * 1e-3; y = y[np.argmax(np.abs(y) > thr):]
    n = int(dur * SR); y = np.pad(y, (0, max(0, n - len(y))))[:n]
    fo = int(min(.03, dur / 4) * SR); y[-fo:] *= np.cos(np.linspace(0, np.pi / 2, fo)) ** 2
    fi = int(.0005 * SR); y[:fi] *= np.linspace(0, 1, fi)
    return y * PEAK / np.abs(y).max()

def hz(m): return 440 * 2 ** ((m - 69) / 12)
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def midi(s): return 12 * (int(s[-1]) + 1) + NOTE[s[0]] + ('#' in s)

def shimmer(dur, count, lo=84, amp=.3):
    """Random soft glockenspiel sparkles on a C pentatonic, drifting upward."""
    y = np.zeros(int(dur * SR)); pent = [0, 2, 4, 7, 9, 12, 14, 16]
    for i in range(count):
        m = lo + pent[min(7, int(i / count * 6 + rng.integers(0, 3)))]
        put(y, i / count * dur * .75 + rng.uniform(0, .03), tone(hz(m), .5, glock(hz(m))), amp * rng.uniform(.6, 1))
    return y

# ---------- sound effects ----------
def pop_variants():
    f = 523.25
    return {
        "a": tone(f, .15, [(1, 1, .045), (4, .30, .012), (10, .05, .004)]),                  # marimba
        "b": tone(f, .15, [(1, 1, .035), (3, .35, .012), (6.2, .10, .005)]),                 # xylophone
        "c": tone(f, .15, [(1, 1, .050), (2, .18, .020), (4, .10, .008)], bend=(1.06, .012)),# round "bloop"
    }
def s_pop(): return pop_variants()[POP]

def s_wrong():      # gentle boing: falling pitch with a wobble
    n = int(.3 * SR); t = np.arange(n) / SR
    f = 150 + 90 * np.exp(-t / .09) + 14 * np.sin(2 * np.pi * 17 * t) * np.exp(-t / .2)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + .35 * np.sin(2 * ph) + .12 * np.sin(3 * ph)) * np.exp(-t / .11) * np.minimum(1, t / .006)

def s_win():        # C E G C glockenspiel arpeggio
    y = np.zeros(SR)
    for i, m in enumerate([72, 76, 79, 84]): put(y, i * .1, tone(hz(m), .9, glock(hz(m))), .8 if i < 3 else 1)
    return y

def s_whoosh():
    n = int(.3 * SR); t = np.arange(n) / SR
    fc = 500 + 1500 * np.sin(np.pi * t / .3) ** 2
    return svf_bp(noise(n, 200, 5000), fc, 1.6) * np.sin(np.pi * t / .3) ** 1.5

def s_combo():      # rising run + little bell
    y = np.zeros(int(1.2 * SR))
    for i, m in enumerate([72, 74, 76, 79, 81, 84, 86, 88]):
        put(y, i * .075, tone(hz(m), .5, marimba(hz(m))), .5 + i * .04)
        put(y, i * .075, tone(hz(m), .5, glock(hz(m))), .18)
    for m, g in [(91, .8), (96, .45)]: put(y, .64, tone(hz(m), .56, glock(hz(m))), g)
    return y

def tap_burst(g=1.0):   # one eggshell tick
    n = int(.05 * SR); t = np.arange(n) / SR
    return g * (noise(n, 1500, 4500) * np.exp(-t / .005) * .8 + tone(950, .05, [(1, 1, .012), (2.3, .35, .006)]) * .6)

def s_crack():
    y = np.zeros(int(.25 * SR))
    for t0, g in [(0, 1), (.055, .55), (.1, .8), (.13, .4)]: put(y, t0, tap_burst(g))
    return y

def s_hatch():
    y = np.zeros(int(1.5 * SR))
    for t0, g in [(0, .7), (.11, .5), (.2, .8), (.27, .6), (.36, 1)]: put(y, t0, tap_burst(g), .8)
    put(y, .38, tone(330, .2, [(1, 1, .05), (2, .3, .03)], bend=(1.6, .03)), .7)       # soft "pop" as it opens
    put(y, .42, shimmer(1.08, 14, amp=.32))
    for m in (84, 88, 91): put(y, .95, tone(hz(m), .55, glock(hz(m))), .3)
    return y

def s_chest():
    y = np.zeros(SR); tt = 0.0
    while tt < .42:                                             # creak = slow stick-slip pulses on wood resonances
        f = 480 + 500 * tt + rng.uniform(-30, 30)
        put(y, tt, tone(f, .04, [(1, 1, .010), (2.1, .5, .006), (3.4, .2, .004)], attack=.001), .5 * np.sin(np.pi * tt / .42) + .15)
        tt += 1 / (22 + 45 * tt) * rng.uniform(.85, 1.15)
    put(y, .44, tone(170, .2, [(1, 1, .05), (2, .4, .03)]), .9)   # lid thunk
    for i, m in enumerate([79, 84, 88, 91]): put(y, .48 + i * .07, tone(hz(m), .5, glock(hz(m))), .45)
    put(y, .5, shimmer(.5, 6, lo=91, amp=.15))
    return y

def s_star():
    y = np.zeros(int(.3 * SR))
    put(y, 0, tone(hz(88), .3, [(1, 1, .09), (2.76, .25, .04)]), 1); put(y, .035, tone(hz(95), .26, [(1, 1, .08), (2.76, .2, .03)]), .6)
    return y

def s_tap(): return tone(1100, .08, [(1, 1, .010), (.5, .5, .014)], attack=.001)

def s_roar():       # friendly "rawr": voiced harmonics through vowel formants, light growl
    n = int(.8 * SR); t = np.arange(n) / SR
    f0 = np.interp(t, [0, .18, .5, .8], [270, 440, 390, 230]) * (1 + .012 * np.sin(2 * np.pi * 31 * t))
    ph = 2 * np.pi * np.cumsum(f0) / SR; y = np.zeros(n)
    f1 = np.interp(t, [0, .2, .8], [500, 850, 600]); f2 = np.interp(t, [0, .2, .8], [1000, 1350, 950])
    for k in range(1, 13):
        fk = k * f0
        g = np.exp(-((fk - f1) / 260) ** 2) + .6 * np.exp(-((fk - f2) / 320) ** 2) + .12 * np.exp(-((fk - 2500) / 500) ** 2) + (.25 if k == 1 else 0)
        y += g * np.sin(k * ph) / k ** .4
    y *= 1 - .3 * (.5 + .5 * np.sin(2 * np.pi * 31 * t))
    return y * np.minimum(1, t / .05) * np.minimum(1, (.8 - t) / .28)

def s_splash():
    n = int(.6 * SR); t = np.arange(n) / SR
    y = svf_bp(noise(n, 250, 5000), 500 + 2200 * np.exp(-t / .12), 1.2) * np.minimum(1, t / .008) * np.exp(-t / .16)
    put(y, 0, tone(140, .2, [(1, 1, .05)], bend=(1.5, .03)), .6)
    for t0 in [.14, .22, .29, .37, .46]:
        f = rng.uniform(450, 800)
        put(y, t0, tone(f, .07, [(1, 1, .03)], attack=.008, bend=(.55, .03)), rng.uniform(.25, .45))
    return y

SFX = {"pop": (s_pop, .15), "wrong": (s_wrong, .3), "win": (s_win, 1.0), "whoosh": (s_whoosh, .3), "combo": (s_combo, 1.2),
       "crack": (s_crack, .25), "hatch": (s_hatch, 1.5), "chest": (s_chest, 1.0), "star": (s_star, .3), "tap": (s_tap, .08),
       "roar": (s_roar, .8), "splash": (s_splash, .6)}

# ---------- music ----------
VOICING = {"C": [60, 64, 67], "Am": [57, 60, 64], "F": [57, 60, 65], "G": [59, 62, 67]}
ROOT = {"C": 36, "Am": 33, "F": 29, "G": 31}
SONGS = {
 "home": dict(bpm=88, prog=["C", "Am", "F", "G"], form="ABA", mel={
  "A": ["E5:1 G5:1 C6:2", "A5:1 G5:1 E5:2", "F5:1 A5:1 C6:1 A5:1", "G5:2 D5:2",
        "E5:1 G5:1 C6:2", "E6:1 D6:1 C6:2", "A5:1 C6:1 A5:1 F5:1", "G5:1 B5:1 D6:2"],
  "B": ["C6:1.5 G5:.5 E5:2", "C6:1.5 A5:.5 E5:2", "F5:.5 G5:.5 A5:1 C6:2", "B5:1 A5:1 G5:2",
        "G5:1 E5:1 G5:1 C6:1", "A5:1 E5:1 A5:1 C6:1", "D6:1 C6:1 A5:1 F5:1", "G5:1 A5:1 B5:2"]}),
 "map": dict(bpm=116, prog=["C", "G", "Am", "F"], form="ABAB", mel={
  "A": ["C5:.5 E5:.5 G5:1 E5:.5 G5:.5 C6:1", "B5:.5 G5:.5 D5:1 G5:.5 B5:.5 D6:1", "C6:.5 A5:.5 E5:1 A5:.5 C6:.5 E6:1", "C6:.5 A5:.5 F5:1 A5:1 -:1",
        "C5:.5 E5:.5 G5:1 E5:.5 G5:.5 C6:1", "D6:.5 B5:.5 G5:1 B5:.5 D6:.5 G6:1", "E6:1 C6:.5 A5:.5 C6:1 E6:1", "F6:.5 E6:.5 D6:.5 C6:.5 A5:1 G5:1"],
  "B": ["G5:1.5 E5:.5 C5:1 E5:1", "G5:1.5 D5:.5 B4:1 D5:1", "A5:1.5 E5:.5 C5:1 E5:1", "A5:.5 G5:.5 F5:1 A5:1 C6:1",
        "E6:1 -:.5 C6:.5 G5:1 C6:1", "D6:1 -:.5 B5:.5 G5:1 B5:1", "C6:1 -:.5 A5:.5 E5:1 A5:1", "C6:.5 A5:.5 F5:.5 A5:.5 G5:1 B5:1"]}),
 "play": dict(bpm=96, prog=["C", "F", "Am", "G"], form="ABA", mel={
  "A": ["E5:2 G5:2", "A5:2 F5:2", "E5:2 C5:2", "D5:2 G5:2", "E5:1 G5:1 C6:2", "A5:1 C6:1 A5:2", "E5:1 A5:1 C6:2", "B5:1 G5:1 D5:2"],
  "B": ["C6:3 G5:1", "A5:3 F5:1", "A5:3 E5:1", "G5:2 B5:2", "G5:1 E5:1 C5:2", "F5:1 A5:1 C6:2", "C6:1 A5:1 E5:2", "D5:1 G5:1 B5:2"]}),
}
_cache = {}
def inst(kind, m, dur=1.6):
    k = (kind, m, dur)
    if k not in _cache:
        f = hz(m); y = tone(f, dur, kind(f), attack=.008 if kind is bass else .003)
        fo = int(.05 * SR); y[-fo:] *= np.linspace(1, 0, fo); _cache[k] = y * min(1, (880 / f) ** .35)
    return _cache[k]

def song(name):
    S = SONGS[name]; beat = 60 / S["bpm"]; bars = [b for sec in S["form"] for b in S["mel"][sec]]
    L = int(round(len(bars) * 4 * beat * SR)); buf = np.zeros((L + 4 * SR, 2)); r = np.random.default_rng(3)
    def add(b, y, g, pan=.5):
        i = int(round(b * beat * SR)); g *= r.uniform(.9, 1.05)
        buf[i:i + len(y), 0] += g * np.cos(pan * np.pi / 2) * y; buf[i:i + len(y), 1] += g * np.sin(pan * np.pi / 2) * y
    for bi, bar in enumerate(bars):
        b0 = bi * 4; ch = S["prog"][bi % 4]; v = VOICING[ch]; root = ROOT[ch] + 12; second = bi >= 16; pos = 0.0
        for tok in bar.split():                                   # melody
            nm, d = tok.split(":"); d = float(d)
            if nm != "-":
                m = midi(nm)
                add(b0 + pos, inst(softbell if name == "play" else marimba, m), .50, .42)
                if second or name == "map": add(b0 + pos, inst(glock, m), .07 if not second else .11, .30)
            pos += d
        if name == "home":
            add(b0, inst(bass, root, 2.0), .42); add(b0 + 2, inst(bass, root + 7, 2.0), .30)
            for i, m in enumerate([v[0], v[1], v[2], v[1]] * 2): add(b0 + i * .5, inst(pluck, m), .16 if i % 2 else .20, .64)
        elif name == "map":
            add(b0, inst(bass, root, .9), .46); add(b0 + 2, inst(bass, root + 7, .9), .36); add(b0 + 3.5, inst(bass, root + 7, .5), .2)
            for b, g in [(1, .2), (3, .2), (1.5, .11), (2.5, .09)]:
                for j, m in enumerate(v + [v[0] + 12]): add(b0 + b + j * .012 / beat, inst(pluck, m, .8), g, .66)
            for i in range(8):                                    # whisper-quiet shaker
                n = int(.05 * SR); add(b0 + i * .5, noise(n, 3500, 7500) * np.exp(-np.arange(n) / SR / .012), .035 if i % 2 else .02, .55)
        else:
            add(b0, inst(bass, root, 3.0), .36)
            for i, m in enumerate([v[0], v[2], v[1], v[2]] * 2): add(b0 + i * .5, inst(marimba, m - 0, 1.0), .15 if i % 4 else .20, .62)
    buf[:4 * SR] += buf[L:]; buf = buf[:L]                        # wrap note tails round -> seamless loop
    buf = buf + .14 * np.roll(buf[:, ::-1], int(.085 * SR), 0) + .07 * np.roll(buf, int(.19 * SR), 0)   # circular echo for width
    return buf * PEAK / np.abs(buf).max()

# ---------- output ----------
def write_wav(path, y):
    y = np.atleast_2d(y.T).T if y.ndim == 2 else y[:, None]
    with wave.open(path, "wb") as w:
        w.setnchannels(y.shape[1]); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype("<i2").tobytes())

def encode(y, out, kbps):
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "x.wav"); write_wav(wav, y)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-ar", str(SR), "-b:a", f"{kbps}k", out], check=True)

def metrics(y):
    y = y if y.ndim == 1 else y.mean(1); X = np.abs(np.fft.rfft(y)) ** 2; f = np.fft.rfftfreq(len(y), 1 / SR)
    return dict(dur=round(len(y) / SR, 2), peak_db=round(20 * np.log10(np.abs(y).max()), 1), rms_db=round(10 * np.log10(np.mean(y ** 2)), 1),
                centroid_hz=int((X * f).sum() / X.sum()), above4k_pct=round(100 * X[f > 4000].sum() / X.sum(), 2),
                max_step=round(float(np.abs(np.diff(y)).max()), 3))

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what == "pop":
        os.makedirs(sys.argv[2], exist_ok=True)
        for k, y in pop_variants().items():
            y = finish(y, .15); write_wav(os.path.join(sys.argv[2], f"pop_{k}.wav"), y); print("pop_" + k, metrics(y))
        sys.exit()
    if what in ("all", "sfx"):
        os.makedirs("assets/sfx", exist_ok=True)
        for name, (fn, dur) in SFX.items():
            y = finish(fn(), dur); encode(y, f"assets/sfx/{name}.mp3", 96); print(name, metrics(y))
    if what in ("all", "music"):
        os.makedirs("assets/music", exist_ok=True)
        for name in SONGS:
            y = song(name); encode(y, f"assets/music/{name}.mp3", 112)
            print(name, metrics(y), "loop seam step", round(float(np.abs(y[0] - y[-1]).max()), 4), os.path.getsize(f"assets/music/{name}.mp3") // 1024, "KB")
