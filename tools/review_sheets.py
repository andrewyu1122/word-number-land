"""Build contact sheets of every asset family + metrics for the review report.
  python tools/review_sheets.py            -> tools/review/*.png, tools/review/metrics.json
Sheets: words_1..N (6x6), letters, numbers, dino, sea, objects, garden, bosses, scenes.
Metrics: coverage of the 160px cell, idle-vs-sleep difference, frame1-vs-frame12 animation difference.
"""
import os, re, glob, json, math
from PIL import Image, ImageDraw, ImageFont, ImageChops
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, 'assets'); OUT = os.path.join(ROOT, 'tools', 'review'); os.makedirs(OUT, exist_ok=True)
CELL = 160; LABEL = 18
try: FONT = ImageFont.truetype("arial.ttf", 12)
except Exception: FONT = ImageFont.load_default()
SEA = "clownfish seahorse jellyfish starfish turtle octopus crab dolphin whale shark pufferfish lobster seal penguin narwhal manta seaegg".split()

def first_frame(p):
    im = Image.open(p); im.seek(0); return im.convert('RGBA')
def frame(p, i):
    im = Image.open(p); n = getattr(im, 'n_frames', 1); im.seek(min(i, n-1)); return im.convert('RGBA')
def coverage(im):
    bb = im.getchannel('A').getbbox()
    if not bb: return 0.0, None
    return max((bb[2]-bb[0])/im.width, (bb[3]-bb[1])/im.height), bb
def diff(a, b):
    """mean abs RGB difference over the union of alpha masks, 0..1"""
    import numpy as np
    if a.size != b.size: b = b.resize(a.size)
    A_ = np.asarray(a, dtype=np.int16); B_ = np.asarray(b, dtype=np.int16)
    m = np.maximum(A_[..., 3], B_[..., 3]) > 10
    if not m.any(): return 0.0
    d = np.abs(A_[..., :3] - B_[..., :3]).mean(axis=2)
    return float(d[m].mean() / 255.0)
def sheet(items, name, cols=6):
    rows = math.ceil(len(items)/cols)
    S = Image.new('RGB', (cols*CELL, rows*(CELL+LABEL)), (235, 235, 238)); dr = ImageDraw.Draw(S)
    for i, (label, path) in enumerate(items):
        r, c = divmod(i, cols); x0, y0 = c*CELL, r*(CELL+LABEL)
        dr.rectangle([x0, y0, x0+CELL-1, y0+CELL-1], outline=(200, 200, 205))
        try:
            im = first_frame(path); im.thumbnail((CELL-4, CELL-4))
            S.paste(im, (x0+(CELL-im.width)//2, y0+(CELL-im.height)//2), im)
        except Exception as e: dr.text((x0+4, y0+4), 'ERR', fill=(200, 0, 0), font=FONT)
        dr.text((x0+3, y0+CELL+2), label[:24], fill=(40, 40, 50), font=FONT)
    S.save(os.path.join(OUT, name+'.png')); print('sheet', name, len(items))

def idles(folder, exclude=()):
    out = []
    for p in sorted(glob.glob(os.path.join(A, folder, '*_idle.webp'))):
        n = os.path.basename(p)[:-10]
        if n in exclude: continue
        out.append((n, p))
    return out

metrics = {'coverage': {}, 'fill': {}, 'sleep_diff': {}, 'anim_diff': {}}
def measure_family(folder, items):
    for n, p in items:
        im = first_frame(p); cov, bb = coverage(im); metrics['coverage'][f'{folder}/{n}'] = round(cov, 3)
        import numpy as np; t = im.copy(); t.thumbnail((CELL, CELL)); metrics['fill'][f'{folder}/{n}'] = round(float((np.asarray(t)[..., 3] > 40).sum())/(CELL*CELL), 3)
        sp = os.path.join(A, folder, n+'_sleep.webp')
        if os.path.exists(sp): metrics['sleep_diff'][f'{folder}/{n}'] = round(diff(im, first_frame(sp)), 4)
        for anim in glob.glob(os.path.join(A, folder, n+'_*.webp')):
            st = os.path.basename(anim)[len(n)+1:-5]
            if st in ('idle', 'sleep') or re.match(r's\d$', st): continue
            try:
                a = Image.open(anim)
                if getattr(a, 'n_frames', 1) > 1: f0 = frame(anim, 0); nf = a.n_frames; metrics['anim_diff'][f'{folder}/{n}_{st}'] = round(max(diff(f0, frame(anim, int(nf*q))) for q in (0.125, 0.25, 0.375, 0.5)), 4)
            except Exception: pass

# ---- words (6x6 pages)
W = idles('words'); measure_family('words', W)
for k in range(0, len(W), 36): sheet(W[k:k+36], f'words_{k//36+1}')
# ---- letters
L = idles('letters') + [(n.upper()+'', p) for n, p in idles('letters_upper')]; measure_family('letters', idles('letters')); measure_family('letters_upper', idles('letters_upper'))
sheet(L, 'letters', 8)
# ---- numbers
N = [(f'n{i}', os.path.join(A, 'num', f'n{i}_idle.webp')) for i in range(0, 101) if os.path.exists(os.path.join(A, 'num', f'n{i}_idle.webp'))]
N += [(n, p) for n, p in idles('num') if not re.match(r'n\d+$', n)]
measure_family('num', N); sheet(N, 'numbers', 10)
# ---- dino / sea
D = [(n, p) for n, p in idles('dino') if n not in SEA]; Sx = [(n, p) for n, p in idles('dino') if n in SEA]
measure_family('dino', D + Sx); sheet(D, 'dino', 6); sheet(Sx, 'sea', 6)
# ---- objects, garden, bosses, mascot
O = idles('objects'); measure_family('objects', O); sheet(O, 'objects', 8)
G = idles('garden') + [(os.path.basename(p)[:-5], p) for p in sorted(glob.glob(os.path.join(A, 'garden', '*_s3.webp')))]; measure_family('garden', idles('garden')); sheet(G, 'garden', 8)
B = idles('bosses') + idles('mascot'); measure_family('bosses', idles('bosses')); measure_family('mascot', idles('mascot')); sheet(B, 'bosses', 6)
# ---- scenes
SC = [(os.path.basename(p)[:-5], p) for p in sorted(glob.glob(os.path.join(A, 'scenes', '*.webp')))]
rows = math.ceil(len(SC)/4); S = Image.new('RGB', (4*300, rows*(188+LABEL)), (235, 235, 238)); dr = ImageDraw.Draw(S)
for i, (n, p) in enumerate(SC):
    r, c = divmod(i, 4); im = Image.open(p).convert('RGB'); im.thumbnail((296, 185)); S.paste(im, (c*300+2, r*(188+LABEL)+2)); dr.text((c*300+3, r*(188+LABEL)+188), n, fill=(40, 40, 50), font=FONT)
S.save(os.path.join(OUT, 'scenes.png')); print('sheet scenes', len(SC))
json.dump(metrics, open(os.path.join(OUT, 'metrics.json'), 'w'), indent=1)
# ---- quick text summaries for the report
cov = sorted(metrics['coverage'].items(), key=lambda kv: kv[1])
print('\nSMALLEST (coverage of cell):'); [print(f'  {k} {v}') for k, v in cov[:30]]
sd = sorted(metrics['sleep_diff'].items(), key=lambda kv: kv[1])
print('\nSLEEP ~ IDLE (smallest diff):'); [print(f'  {k} {v}') for k, v in sd[:25]]
ad = sorted(metrics['anim_diff'].items(), key=lambda kv: kv[1])
print('\nWEAKEST ANIMATION (frame1 vs frame12):'); [print(f'  {k} {v}') for k, v in ad[:25]]
