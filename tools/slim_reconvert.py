#!/usr/bin/env python3
"""Re-convert every character that still has its original PNG renders, using the current settings in convert_assets.py.

  python tools/slim_reconvert.py <png root> [<png root> ...] [--dry]

A character is only re-converted when one of the PNG folders found under the given roots reproduces the WebP that is
committed right now (same pixel size at the OLD height, near-identical first image). That way an outdated render can
never replace newer art, and nothing is ever re-compressed from an existing WebP. Everything else is left untouched.
"""
import os, re, sys, glob
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import convert_assets as ca
OLD_HEIGHT = dict(ca.HEIGHT, words=384, dino=384, bosses=512)       # what the committed files were made with
KINDS = ['words', 'letters', 'upper', 'num', 'objects', 'garden', 'mascot', 'bosses', 'dino']
NAME_RE = re.compile(r'(op_[a-z]+|mascot_xmas|medal_[a-z0-9]+|[A-Za-z0-9]+)_[a-z0-9]+(?:_\d{3})?\.png$')

def states_for(kind, folder, name):
    files = ca.collect(folder, name)
    if kind == 'words':
        seqs = [k for k, v in files.items() if isinstance(v, list)]
        if seqs: files['anim'] = files.pop(seqs[0])
    if kind == 'garden':
        for k in [k for k, v in files.items() if isinstance(v, list)]: files['move'] = files.pop(k)
    return files

def check(args):
    """does this PNG folder reproduce the committed WebPs of (kind, name)?  -> (kind, name, folder, ok, why)"""
    kind, name, folder = args
    out = f'{ca.OUT}/{ca.DEST[kind]}'
    try:
        files = states_for(kind, folder, name)
        if not files: return (kind, name, folder, False, 'no files')
        for st in files:
            if not os.path.exists(f'{out}/{name}_{st}.webp'): return (kind, name, folder, False, f'state {st} not in assets')
        allf = [f for v in files.values() for f in (v if isinstance(v, list) else [v])]
        bb = ca.bbox(allf)
        if bb is None: return (kind, name, folder, False, 'empty')
        h = OLD_HEIGHT[kind]
        if kind == 'words' and (bb[3]-bb[1]) < 256: h = min(h, int((bb[3]-bb[1])*1.5))
        st = 'idle' if 'idle' in files else sorted(files)[0]
        v = files[st]; src = ca.prep(v[0] if isinstance(v, list) else v, bb, h)
        cur = Image.open(f'{out}/{name}_{st}.webp'); cur.seek(0); cur = cur.convert('RGBA')
        if cur.size != src.size: return (kind, name, folder, False, f'size {src.size} vs committed {cur.size}')
        a = np.asarray(src, dtype=np.int16); b = np.asarray(cur, dtype=np.int16); m = a[..., 3] > 32
        d = float(np.abs(a[..., :3] - b[..., :3])[m].mean()) if m.any() else 0.0
        da = float(np.abs(a[..., 3] - b[..., 3]).mean())
        if d > 6 or da > 4: return (kind, name, folder, False, f'pixels differ ({d:.1f}/{da:.1f})')
        return (kind, name, folder, True, '')
    except Exception as e:
        return (kind, name, folder, False, 'error ' + str(e)[:80])

def convert(args):
    kind, name, folder = args
    ca.convert_one((name, states_for(kind, folder, name), ca.HEIGHT[kind], f'{ca.OUT}/{ca.DEST[kind]}', kind == 'words'))
    return (kind, name)

def main():
    roots = [a for a in sys.argv[1:] if not a.startswith('--')]; dry = '--dry' in sys.argv
    src = {}                                       # name -> [folders], newest first
    for r in roots:
        for f in glob.glob(f'{r}/**/*.png', recursive=True):
            m = NAME_RE.match(os.path.basename(f))
            if m and 'sheet' not in f and 'preview' not in f and '_test' not in f: src.setdefault(m.group(1), set()).add(os.path.dirname(f))
    jobs = []
    for kind in KINDS:
        names = sorted({re.match(r'(.+)_[a-z0-9]+(?:_anim)?\.webp$', os.path.basename(p)).group(1) for p in glob.glob(f'{ca.OUT}/{ca.DEST[kind]}/*.webp')})
        cand = set(names)
        for n in names:                             # names with underscores (medal_x, mascot_xmas, op_plus, chest, egg_s0 ...)
            for k in src:
                if n.startswith(k + '_') or n == k: cand.add(k)
        for n in sorted(cand):
            for folder in sorted(src.get(n, []), key=lambda d: -os.path.getmtime(d)): jobs.append((kind, n, folder))
    chosen = {}; why = {}
    with ProcessPoolExecutor() as ex:
        for kind, name, folder, ok, msg in ex.map(check, jobs, chunksize=4):
            if ok and (kind, name) not in chosen: chosen[(kind, name)] = folder
            elif not ok: why.setdefault((kind, name), []).append(msg)
    for kind in KINDS:
        got = sorted(n for (k, n) in chosen if k == kind)
        allc = {os.path.basename(p) for p in glob.glob(f'{ca.OUT}/{ca.DEST[kind]}/*.webp')}
        cov = {f for f in allc if any(f.startswith(n + '_') for n in got)}
        print(f'{kind:8s} re-convert {len(got):3d} characters ({len(cov)}/{len(allc)} files); untouched files: {len(allc) - len(cov)}')
        left = sorted({re.match(r'(.+?)_(idle|sleep|anim|jump|move|walk|roar|swim|happy|eat|run|no|spin)', f).group(1) for f in allc - cov if re.match(r'(.+?)_(idle|sleep|anim|jump|move|walk|roar|swim|happy|eat|run|no|spin)', f)})
        if left: print('   no matching PNGs:', ' '.join(left)[:600])
    if dry: return
    with ProcessPoolExecutor() as ex:
        n = sum(1 for _ in ex.map(convert, [(k, nm, f) for (k, nm), f in chosen.items()], chunksize=2))
    print('converted', n)

if __name__ == '__main__': main()
