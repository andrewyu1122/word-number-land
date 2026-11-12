# 10 achievement medals: gold disc on a coloured ribbon, a different emblem each. Action "spin" = one turn + a sparkle flash.
exec(open(PIPE + "/builders_words3.py", encoding="utf-8").read().rsplit(chr(10) + "BUILD = {k[2:]", 1)[0])
for _k in [k for k in list(globals()) if k.startswith("b_")]: del globals()[_k]
Z0 = 0.85; YF = -0.1                      # disc centre height, front surface
def medal(rib1, rib2, emblem):
    gold = mat((1.0, 0.76, 0.12), 0.35, 0.0); o = Cy(0.8, 0.16, (0, 0, Z0), "gold", (R90, 0, 0), verts=64); o.data.materials[0] = gold
    for sy in (-1, 1): To(0.74, 0.05, (0, sy*0.08, Z0), "yellow", (R90, 0, 0)); Cy(0.62, 0.02, (0, sy*0.085, Z0), (0.95, 0.62, 0.08), (R90, 0, 0), verts=48)
    To(0.13, 0.04, (0, 0, Z0 + 0.86), "gold", (R90, 0, 0))
    for sx in (-1, 1):
        Fp([(0, 0), (0.34, 0), (0.34 + 0.42, 0.95), (0.42, 0.95)] if sx == 1 else [(0, 0), (-0.34, 0), (-0.34 - 0.42, 0.95), (-0.42, 0.95)], (sx*-0.17 + (0.17 if sx == 1 else -0.17) - sx*0.17, 0.02*sx, Z0 + 0.9), 0.06, rib1)
        Fp([(0.1, 0), (0.24, 0), (0.24 + 0.42, 0.95), (0.52, 0.95)] if sx == 1 else [(-0.1, 0), (-0.24, 0), (-0.24 - 0.42, 0.95), (-0.52, 0.95)], (sx*-0.17 + (0.17 if sx == 1 else -0.17) - sx*0.17, 0.02*sx - 0.012, Z0 + 0.9), 0.06, rib2)
    emblem()
    sp = []
    for (x, z, r) in [(0.62, Z0 + 0.55, 0.3), (-0.6, Z0 - 0.45, 0.22), (0.35, Z0 - 0.62, 0.16)]:
        e = E((x, YF - 0.12, z), name="Spark"); m = mat((1.0, 1.0, 0.85), 0.3, 3.0)
        for rot in (0, R90): q = S(r, (x, YF - 0.12, z), (1, 0.12, 0.16), "white", e, rot=(0, rot, 0)); q.data.materials[0] = m
        e.scale = (0.001, 0.001, 0.001); sp.append(e)
    return {"spark": sp, "gold": gold}
def medal_spin(h):
    n = NFRAMES
    for f in range(1, n + 2):
        u = min(1.0, (f - 1)/18.0); u = (1 - math.cos(math.pi*u))/2
        ROOT.rotation_euler = (0, 0, TAU*u); kf(ROOT, "rotation_euler", f)
        k = max(0.0, math.sin(math.pi*min(1.0, max(0.0, (f - 18.5)/6.0)))) if f < n + 1 else 0.0
        for i, e in enumerate(h["spark"]): v = max(0.001, 1.25*k*(1 - 0.15*i)); e.scale = (v, v, v); kf(e, "scale", f); e.rotation_euler = (0, rad(40)*k, 0); kf(e, "rotation_euler", f)
        inp = h["gold"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]; h["gold"].node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (1.0, 0.85, 0.3, 1)
        inp.default_value = 0.9*k; inp.keyframe_insert("default_value", frame=f)
ACTS["spin"] = medal_spin
def book(x, z, w=0.62, hh=0.46, c="blue", rot=0.0):
    BX((x, YF - 0.05, z), (w, 0.1, hh), c, rot=(0, rad(rot), 0), bevel=0.03); BX((x + 0.03, YF - 0.06, z), (w - 0.08, 0.1, hh - 0.1), "white", rot=(0, rad(rot), 0), bevel=0.01); BX((x - w*0.38, YF - 0.11, z), (0.06, 0.02, hh), c, rot=(0, rad(rot), 0), bevel=0.0)
def crown(x, z, s=1.0):
    BX((x, YF - 0.05, z), (0.5*s, 0.1, 0.14*s), "red", bevel=0.02)
    Fp([(-0.25*s, 0), (0.25*s, 0), (0.3*s, 0.3*s), (0.12*s, 0.14*s), (0, 0.34*s), (-0.12*s, 0.14*s), (-0.3*s, 0.3*s)], (x, YF - 0.05, z + 0.06*s), 0.1, "red")
    for dx in (-0.3, 0, 0.3): S(0.045*s, (x + dx*s, YF - 0.06, z + (0.36 if dx else 0.4)*s), (1, 1, 1), "white")
def b_medal_words50(): return medal("blue", "sky", lambda: book(0, Z0, 0.8, 0.6))
def b_medal_words100(): return medal("red", "yellow", lambda: (book(0, Z0 - 0.26, 0.82, 0.22, "red"), book(0.03, Z0, 0.76, 0.22, "green"), book(-0.03, Z0 + 0.26, 0.7, 0.22, "blue")))
def b_medal_words200(): return medal("purple", "gold", lambda: (book(0, Z0 - 0.16, 0.76, 0.46, "purple"), crown(0, Z0 + 0.16, 0.9)))
def b_medal_math(): return medal("green", "lime", lambda: T3("123", 0.62, (0, YF - 0.03, Z0), "navy", depth=0.05))
def b_medal_hunt():
    def em():
        To(0.3, 0.07, (-0.08, YF - 0.06, Z0 + 0.1), "navy", (R90, 0, 0)); Cy(0.26, 0.04, (-0.08, YF - 0.04, Z0 + 0.1), "sky", (R90, 0, 0)); S(0.06, (-0.18, YF - 0.07, Z0 + 0.2), (1.6, 0.3, 0.8), "white", rot=(0, rad(40), 0))
        RC(0.065, 0.42, (0.3, YF - 0.06, Z0 - 0.3), "brown", (0, rad(-45), 0), lv=1)
    return medal("orange", "yellow", em)
def b_medal_read():
    def em():
        S(0.42, (0, YF - 0.03, Z0 - 0.02), (1.25, 0.14, 0.72), "white"); S(0.2, (0, YF - 0.07, Z0 - 0.02), (1, 0.2, 1), "blue"); S(0.1, (0, YF - 0.1, Z0 - 0.02), (1, 0.2, 1), "black"); S(0.04, (-0.05, YF - 0.12, Z0 + 0.04), (1, 0.3, 1), "white")
        Fp(starpts(0.17, 0.075), (0.36, YF - 0.07, Z0 + 0.4), 0.06, "hotpink"); Fp(starpts(0.1, 0.045), (-0.42, YF - 0.07, Z0 - 0.4), 0.06, "hotpink")
    return medal("hotpink", "white", em)
def b_medal_dino():
    def em():
        S(0.34, (0.08, YF - 0.05, Z0 + 0.05), (1, 0.3, 0.95), "green"); S(0.26, (-0.28, YF - 0.05, Z0 - 0.08), (1.2, 0.3, 0.8), "green"); S(0.07, (0.05, YF - 0.13, Z0 + 0.16), (1, 0.4, 1), "white"); S(0.035, (0.04, YF - 0.16, Z0 + 0.16), (1, 0.4, 1), "black")
        for k in range(3): Fp([(-0.05, 0), (0.05, 0), (0, -0.1)], (-0.42 + 0.12*k, YF - 0.1, Z0 - 0.14), 0.03, "white")
        for k in range(3): Fp([(-0.08, 0), (0.08, 0), (0, 0.14)], (0.02 + 0.14*k, YF - 0.05, Z0 + 0.34 - 0.07*k), 0.06, "dkgreen", rot=(0, rad(22*k), 0))
        S(0.03, (-0.5, YF - 0.11, Z0 - 0.02), (1, 0.4, 1), "dkgreen")
    return medal("green", "orange", em)
def b_medal_sea():
    def em():
        S(0.34, (-0.06, YF - 0.05, Z0), (1.25, 0.3, 0.85), "orange"); Fp([(0, 0), (0.3, 0.24), (0.3, -0.24)], (0.3, YF - 0.05, Z0), 0.08, "orange")
        for x in (-0.12, 0.08): BX((x, YF - 0.11, Z0), (0.07, 0.03, 0.5), "white", bevel=0.01)
        S(0.06, (-0.3, YF - 0.13, Z0 + 0.07), (1, 0.4, 1), "white"); S(0.03, (-0.31, YF - 0.16, Z0 + 0.07), (1, 0.4, 1), "black")
        for (x, z, r) in [(-0.5, Z0 + 0.3, 0.05), (-0.42, Z0 + 0.44, 0.035)]: S(r, (x, YF - 0.06, z), (1, 0.4, 1), "sky")
    return medal("sky", "navy", em)
def b_medal_streak7():
    def em():
        Fp([(0, -0.42), (0.3, -0.3), (0.4, -0.02), (0.3, 0.22), (0.2, 0.1), (0.1, 0.5), (-0.12, 0.2), (-0.2, 0.34), (-0.4, 0.0), (-0.3, -0.3)], (0, YF - 0.04, Z0), 0.08, "red")
        Fp([(0, -0.38), (0.2, -0.28), (0.26, -0.05), (0.14, 0.12), (0.04, 0.3), (-0.1, 0.08), (-0.26, -0.06), (-0.2, -0.28)], (0, YF - 0.06, Z0), 0.08, "orange")
        T3("7", 0.42, (0.0, YF - 0.1, Z0 - 0.14), "white", depth=0.03)
    return medal("red", "orange", em)
def b_medal_map():
    def em():
        o = Fp([(-0.45, -0.3), (-0.15, -0.22), (0.15, -0.3), (0.45, -0.22), (0.45, 0.3), (0.15, 0.22), (-0.15, 0.3), (-0.45, 0.22)], (0, YF - 0.04, Z0 - 0.06), 0.08, "cream")
        for x in (-0.15, 0.15): BX((x, YF - 0.085, Z0 - 0.06), (0.015, 0.01, 0.5), "tan", bevel=0.0)
        for k in range(5): S(0.03, (-0.32 + 0.13*k, YF - 0.09, Z0 - 0.2 + 0.07*math.sin(k*1.4) + 0.04*k), (1, 0.4, 1), "red")
        Cy(0.02, 0.5, (0.28, YF - 0.09, Z0 + 0.22), "brown", verts=8); Fp([(0, 0), (0.26, 0.09), (0, 0.18)], (0.29, YF - 0.09, Z0 + 0.28), 0.03, "red"); BX((0.26, YF - 0.09, Z0 - 0.02), (0.1, 0.02, 0.1), "red", rot=(0, rad(45), 0), bevel=0.0)
    return medal("aqua", "yellow", em)
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}
