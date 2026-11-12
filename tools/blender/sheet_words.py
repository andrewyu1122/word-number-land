# python sheet_words.py <preview dir> <out png> name1,name2,...  -> idle | sleep pairs in a grid
import sys, os
from PIL import Image, ImageDraw
src, out, names = sys.argv[1], sys.argv[2], sys.argv[3].split(','); T = 256; cols = 3
rows = (len(names) + cols - 1) // cols
im = Image.new('RGB', (cols * T * 2, rows * T), (150, 185, 150)); d = ImageDraw.Draw(im)
for i, n in enumerate(names):
    x, y = (i % cols) * T * 2, (i // cols) * T
    for k, st in enumerate(("idle", "sleep")):
        p = f"{src}/{n}_{st}.png"
        if os.path.exists(p): t = Image.open(p).convert('RGBA').resize((T, T)); im.paste(t, (x + k * T, y), t)
    d.text((x + 4, y + 4), n, fill=(0, 0, 0))
im.save(out); print(out, im.size)
