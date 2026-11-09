"""Align every number character (n0..n100, nq) so the idle feet and head margins match in the final WebP.
  python tools/align_num.py <src1> [<src2> ...] [--out assets/num] [--hr 0.35] [--pad 0.05]
Per character: box left/right = union of all states (+pad); bottom = idle feet + pad; top = idle top - hr*idle_h - pad
(widened to the union if an animation goes higher, which is reported). Result: identical idle size and feet row for all numbers."""
import os, re, sys, glob
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import convert_assets as ca
args = [a for a in sys.argv[1:] if not a.startswith('--')]
def opt(name, default):
    if f'--{name}' in sys.argv: return type(default)(sys.argv[sys.argv.index(f'--{name}')+1])
    return default
OUT = opt('out', os.path.join(ca.OUT, 'num')); HR = opt('hr', 0.35); PADF = opt('pad', 0.05); H = ca.HEIGHT['num']
os.makedirs(OUT, exist_ok=True)
chars = {}
for src in args:
    for p in glob.glob(os.path.join(src, 'n*_idle.png')):
        n = re.match(r'(n\d+|nq)_idle\.png$', os.path.basename(p))
        if n: chars[n.group(1)] = src
def bb(p): return Image.open(p).convert('RGBA').getchannel('A').getbbox()
report = []
for name in sorted(chars, key=lambda s: (len(s), s)):
    files = ca.collect(chars[name], name)
    allf = [f for v in files.values() for f in (v if isinstance(v, list) else [v])]
    ub = ca.bbox(allf); ib = bb(files['idle']); ih = ib[3]-ib[1]
    W, Hh = Image.open(files['idle']).size
    PAD = max(6, PADF*ih); top = ib[1] - HR*ih - PAD; bottom = ib[3] + PAD
    note = ''
    if ub[1] < top: note = f'anim exceeds headroom by {int(top-ub[1])}px'; top = ub[1]
    if ub[3] > bottom: note += f' anim below feet by {int(ub[3]-bottom)}px'; bottom = ub[3]
    box = (ub[0]-4, int(top), ub[2]+4, int(bottom))   # may extend beyond the 512 frame: PIL pads with transparency
    for state, v in files.items():
        out = f'{OUT}/{name}_{state}.webp'
        if isinstance(v, list):
            fr = [ca.prep(f, box, H) for f in v]; fr[0].save(out, save_all=True, append_images=fr[1:], duration=42 if len(v) > 12 else 60, loop=0, quality=80, method=4)
        else: ca.prep(v, box, H).save(out, quality=82, method=4)
    report.append((name, round(ih/(box[3]-box[1]), 3), note))
for r in report: print(*r)
print('aligned', len(report), 'characters ->', OUT)
