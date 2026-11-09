#!/usr/bin/env python3
"""Convert Blender PNG renders into the WebP files the game uses.

Usage examples (run from the repo root):
  python tools/convert_assets.py words   ./incoming/words          # one sub-folder per word
  python tools/convert_assets.py letters ./incoming/letters        # a/, b/ ... or flat a_idle.png
  python tools/convert_assets.py upper   ./incoming/letters_upper
  python tools/convert_assets.py num     ./incoming/num
  python tools/convert_assets.py objects ./incoming/objects
  python tools/convert_assets.py garden  ./incoming/garden
  python tools/convert_assets.py mascot  ./incoming/mascot
  python tools/convert_assets.py bosses  ./incoming/bosses
  python tools/convert_assets.py dino    ./incoming/dino           # dinos: {name}_idle/_walk_###/_roar_###, egg_s0..s3, egg_hatch_###
  python tools/convert_assets.py scenes  ./incoming/scenes

Input naming: {name}_idle.png, {name}_sleep.png, {name}_{action}_001.png ... (24 or 12 frames).
Output: assets/<kind>/{name}_{state}.webp  (animations become animated WebP, 24 fps).
All states of one character share ONE crop box (union of alpha bboxes) so sizes line up.
After converting words, run with --update-art to refresh the ART map inside index.html.
"""
import os, re, sys, glob, json
from PIL import Image
from concurrent.futures import ProcessPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, 'assets')
HEIGHT = {'words':384,'letters':176,'upper':176,'num':224,'objects':160,'garden':128,'mascot':288,'bosses':512,'dino':384}
DEST   = {'words':'words','letters':'letters','upper':'letters_upper','num':'num','objects':'objects','garden':'garden','mascot':'mascot','bosses':'bosses','dino':'dino'}
PAD = 6

def bbox(paths):
    bb = None
    for p in paths:
        a = Image.open(p).convert('RGBA').getchannel('A').getbbox()
        if a: bb = a if bb is None else (min(bb[0],a[0]),min(bb[1],a[1]),max(bb[2],a[2]),max(bb[3],a[3]))
    if bb is None: return None
    w,h = Image.open(paths[0]).size
    return (max(0,bb[0]-PAD),max(0,bb[1]-PAD),min(w,bb[2]+PAD),min(h,bb[3]+PAD))

def prep(p,bb,h):
    im = Image.open(p).convert('RGBA').crop(bb); s = h/im.height
    return im.resize((max(1,round(im.width*s)),h), Image.LANCZOS)

def convert_one(args):
    name, files, h, outdir, capsmall = args
    os.makedirs(outdir, exist_ok=True)
    allf = [f for v in files.values() for f in (v if isinstance(v,list) else [v])]
    bb = bbox(allf)
    if bb is None: return name+' (empty)'
    if capsmall and (bb[3]-bb[1]) < 256: h = min(h, int((bb[3]-bb[1])*1.5))   # don't blow up tiny renders
    for state, v in files.items():
        out = f'{outdir}/{name}_{state}.webp'
        if isinstance(v, list):
            fr = [prep(f,bb,h) for f in v]
            fr[0].save(out, save_all=True, append_images=fr[1:], duration=42 if len(v)>12 else 60, loop=0, quality=80, method=4)
        else:
            prep(v,bb,h).save(out, quality=82, method=4)
    return name

def collect(folder, name):
    """Group files of one character: stills -> state, sequences -> state (list)."""
    files = {}
    for f in sorted(os.listdir(folder)):
        if not f.endswith('.png') or not f.startswith(name+'_'): continue
        rest = f[len(name)+1:-4]
        m = re.match(r'(.+)_(\d{3})$', rest)
        if m:
            st = m.group(1)
            if isinstance(files.get(st), str) and st+'_anim' not in files: files[st+'_anim'] = []   # still + sequence share a name: sequence -> {state}_anim
            key = st+'_anim' if st+'_anim' in files else st
            files.setdefault(key, []).append(os.path.join(folder,f))
        elif isinstance(files.get(rest), list): files[rest+'_anim'] = files.pop(rest); files[rest] = os.path.join(folder,f)
        else: files[rest] = os.path.join(folder,f)
    # the game expects the word animation to be called "anim" and animals' motion "move"
    return files

def main():
    if len(sys.argv) < 3: print(__doc__); sys.exit(1)
    kind, src = sys.argv[1], sys.argv[2]
    update_art = '--update-art' in sys.argv
    if kind == 'scenes':
        os.makedirs(f'{OUT}/scenes', exist_ok=True)
        for f in sorted(glob.glob(f'{src}/*.png')):
            name = os.path.basename(f)[:-4]
            if name.endswith('_fg'):   # foreground layer: keep transparency
                Image.open(f).convert('RGBA').save(f'{OUT}/scenes/{name}.webp', quality=82, method=4)
            else:
                Image.open(f).convert('RGB').save(f'{OUT}/scenes/{name}.webp', quality=78, method=4)
            print('scene', name)
        return
    h, outdir = HEIGHT[kind], f'{OUT}/{DEST[kind]}'
    jobs, art = [], {}
    # characters may live in sub-folders (words/dog/dog_idle.png) or flat (num/n3_idle.png)
    names = set()
    for f in glob.glob(f'{src}/**/*.png', recursive=True):
        b = os.path.basename(f)
        m = re.match(r'(op_[a-z]+|mascot_xmas|[A-Za-z0-9]+)_[a-z0-9]+(?:_\d{3})?\.png$', b)
        if m and 'sheet' not in b and 'preview' not in f: names.add((os.path.dirname(f), m.group(1)))
    for folder, name in sorted(names):
        files = collect(folder, name)
        if kind == 'words':
            seqs = [k for k,v in files.items() if isinstance(v,list)]
            if seqs:
                art[name] = seqs[0]; files['anim'] = files.pop(seqs[0])
        if kind == 'garden':
            seqs = [k for k,v in files.items() if isinstance(v,list)]
            for k in seqs: files['move'] = files.pop(k)
        jobs.append((name, files, h, outdir, kind=='words'))
    with ProcessPoolExecutor() as ex:
        for r in ex.map(convert_one, jobs): print('ok', r)
    if kind == 'words' and update_art and art:
        idx = os.path.join(ROOT,'index.html'); s = open(idx, encoding='utf-8').read()
        cur = re.search(r"const ART=(\{.*?\});", s).group(1)
        d = json.loads(cur.replace("'",'"')); d.update(art)
        s = s.replace(cur, json.dumps(d, separators=(',',':')).replace('"',"'"))
        open(idx,'w',encoding='utf-8').write(s); print('ART map updated with', art)
    print('\nNow bump VERSION in sw.js, then git add/commit/push.')

if __name__ == '__main__': main()
