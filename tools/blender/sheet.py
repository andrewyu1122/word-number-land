# python sheet.py <preview dir> <out png> name1,name2,...   -> rows = name x action, cols = frames
import sys, os
from PIL import Image, ImageDraw
src, out, names = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
FR = (1, 4, 7, 10, 13, 16, 19, 22); ACT = ("eat", "sleep", "run"); T = int(sys.argv[4]) if len(sys.argv) > 4 else 150
W = T * len(FR) + 70; H = T * len(ACT) * len(names)
im = Image.new('RGB', (W, H), (150, 185, 150)); d = ImageDraw.Draw(im)
for i, n in enumerate(names):
    for j, a in enumerate(ACT):
        y = (i * len(ACT) + j) * T; d.text((4, y + 4), f"{n}\n{a}", fill=(0, 0, 0))
        d.line([(70, y + int(T * 0.8)), (W, y + int(T * 0.8))], fill=(120, 150, 120))
        for k, f in enumerate(FR):
            p = f"{src}/{n}_{a}_{f:03d}.png"
            if os.path.exists(p):
                t = Image.open(p).convert('RGBA').resize((T, T), Image.LANCZOS); im.paste(t, (70 + k * T, y), t)
im.save(out); print(out, im.size)
