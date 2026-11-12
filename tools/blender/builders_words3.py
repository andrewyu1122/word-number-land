# Reader vocabulary (139 picture words). Same style as builders_words2: rounded subsurf shapes + metaball animals. Face -Y, stand on z=0.
exec(open(PIPE + "/builders_words2.py", encoding="utf-8").read().rsplit(chr(10) + "BUILD = {k[2:]", 1)[0])
for _k in [k for k in list(globals()) if k.startswith("b_")]: del globals()[_k]      # only this file's words
PAL.update(dict(skin2=(0.78, 0.56, 0.4), skin3=(0.55, 0.36, 0.24), hairb=(0.25, 0.15, 0.08), blonde=(0.95, 0.8, 0.35), ginger=(0.85, 0.42, 0.15),
                grass=(0.45, 0.75, 0.3), water=(0.3, 0.65, 0.95), brick=(0.8, 0.4, 0.3), roof=(0.75, 0.25, 0.2), bean=(0.62, 0.16, 0.16), stone=(0.7, 0.7, 0.74)))
def surf_y(x, z, fallback):
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    hit, loc, nrm, idx, ob, mw = scene.ray_cast(dg, Vector((x, -8.0, z)), Vector((0, 1, 0)))
    return loc.y if hit else fallback
def sface(z, spread=0.2, r=0.11, x=0.0, mouth_dz=None, mr=None, tongue=True, parent=None, fb=-0.5):
    """face glued onto whatever surface is in front at height z"""
    f = Vector((0, -1, 0))
    for sx in (-1, 1):
        p = Vector((x + sx*spread, surf_y(x + sx*spread, z, fb) + r*0.42, z))
        EYES.extend([S(r, p, (1, 0.5, 1), "white", parent, name="Eye"), S(r*0.55, p + f*(r*0.6), (1, 0.5, 1), "black", parent, name="Pupil", seg=16, ring=10),
                     S(r*0.18, p + f*(r*0.95) + Vector((-r*0.25, 0, r*0.35)), (1, 1, 1), "white", parent, name="Shine", seg=10, ring=6)])
        LIDS.append((p + f*(r*0.4), parent, r))
    mz = z - (mouth_dz if mouth_dz is not None else r*2.2)
    smile(mz, surf_y(x, mz, fb) - 0.015, mr if mr else r, parent, x, tongue)
def person(shirt, pants=None, hair="hairb", skin="peach", style="short", shoes="dkbrown", sleeves=None, arm=15):
    """the shared round-headed little person; clothes / props tell them apart"""
    RB((0, 0, 0.75), (0.75, 0.6, 0.7), shirt, lv=2)
    S(0.42, (0, 0, 1.4), (1, 1, 1), skin)
    for sx in (-1, 1):
        RC(0.08, 0.5, (sx*0.45, -0.05, 0.75), sleeves or shirt, (0, rad(sx*arm), 0), lv=1); S(0.1, (sx*0.52, -0.08, 0.48), (1, 1, 1), skin)
        S(0.09, (sx*0.41, 0.02, 1.38), (0.5, 1, 1), skin)
    legs2(pants or shirt, 0, 0.3, 0.09, 0.2, foot=shoes)
    if style != "bald": S(0.44, (0, 0.07, 1.5), (1, 1, 0.85), hair)
    if style == "long":
        S(0.42, (0, 0.2, 1.25), (1.0, 0.7, 1.15), hair)
        for sx in (-1, 1): S(0.2, (sx*0.38, 0.1, 1.15), (0.7, 0.9, 1.5), hair)
    if style == "bun": S(0.18, (0, 0.12, 1.92), (1, 1, 1), hair)
    if style == "pony": S(0.16, (0, 0.5, 1.5), (0.8, 1, 1.6), hair, rot=(rad(-30), 0, 0))
    face(1.42, -0.4, 0.15, 0.09, mouth_dz=0.26, mr=0.08)
def chain(p0, p1, r0, r1, n=6):
    a = Vector(p0); b = Vector(p1)
    return [((a+(b-a)*(k/(n-1))).to_tuple(), r0+(r1-r0)*k/(n-1), None) for k in range(n)]
def BX(loc, scale, c, parent=None, rot=None, bevel=0.05): return B(loc, scale, c, parent, rot, bevel)
def base(w, d, c="grass", h=0.2): return BX((0, 0, h/2), (w, d, h), c, bevel=0.07)
def fit(h=2.0, maxw=2.4):
    """scale the whole model to a standard size (and keep the sleep lids in the right place)"""
    k = normalize_height(h, maxw)
    for i, (p, parent, r) in enumerate(LIDS): LIDS[i] = (Vector(p)*k if parent is None else p, parent, r*k if parent is None else r)
    return k
def house(x, y, w, d, h, c, rc="roof", door="dkbrown", rh=0.45):
    BX((x, y, h/2 + 0.2), (w, d, h), c); Fp([(-w*0.6, 0), (w*0.6, 0), (0, rh)], (x, y, h + 0.2), d*1.1, rc)
    if door: BX((x, y - d/2, 0.2 + h*0.25), (w*0.25, 0.05, h*0.5), door, bevel=0.02)
def tree_s(x, y, s=1.0, c="green"):
    RC(0.08*s, 0.6*s, (x, y, 0.2 + 0.3*s), "brown", lv=1); S(0.42*s, (x, y, 0.2 + 0.85*s), (1, 1, 1), c); S(0.28*s, (x + 0.2*s, y, 0.2 + 1.15*s), (1, 1, 1), c)
# ---------------------------------------------------------------- level 1
def b_dad():
    person("blue", "navy", "hairb")
    RK(0.07, 0.36, (0, -0.33, 0.82), "red", (math.pi, 0, 0), lv=1); S(0.06, (0, -0.33, 1.03), (1, 0.6, 0.8), "red")
    for sx in (-1, 1): To(0.115, 0.016, (sx*0.15, -0.44, 1.43), "black", (R90, 0, 0)); S(0.08, (sx*0.08, -0.41, 1.24), (1.5, 0.5, 0.55), "hairb")
    Cy(0.012, 0.1, (0, -0.45, 1.44), "black", (0, R90, 0), verts=6); return {}
def b_mom():
    person("hotpink", "hotpink", "brown", style="long", shoes="red")
    RK(0.58, 0.55, (0, 0, 0.5), "hotpink", lv=2, r2=0.3); To(0.2, 0.025, (0, -0.06, 1.08), "gold")
    for sx in (-1, 1): S(0.05, (sx*0.44, -0.02, 1.26), (1, 1, 1), "gold")
    S(0.09, (0.25, -0.3, 1.72), (1.3, 0.6, 1), "yellow"); return {}
def b_gym():
    base(2.4, 2.0, "blue"); BX((0, 0.3, 0.9), (1.9, 1.1, 1.4), "orange"); BX((0, 0.3, 1.66), (2.05, 1.25, 0.14), "white")
    BX((0.6, -0.27, 0.5), (0.4, 0.06, 0.6), "navy", bevel=0.02); BX((-0.6, -0.27, 0.6), (0.45, 0.06, 0.4), "glass", bevel=0.02)
    RC(0.06, 1.3, (0, 0.3, 2.05), "dkgrey", (0, R90, 0), lv=1)
    for sx in (-1, 1): Cy(0.32, 0.16, (sx*0.6, 0.3, 2.05), "red", (0, R90, 0)); Cy(0.24, 0.12, (sx*0.76, 0.3, 2.05), "charcoal", (0, R90, 0))
    S(0.2, (0.95, -0.7, 0.4), (1, 1, 0.9), "charcoal"); To(0.11, 0.035, (0.95, -0.7, 0.62), "charcoal", (R90, 0, 0))
    S(0.22, (-0.9, -0.7, 0.42), (1, 1, 1), "orange"); To(0.22, 0.012, (-0.9, -0.7, 0.42), "black", (R90, 0, 0))
    face(1.25, -0.27, 0.2, 0.11, mouth_dz=0.26, mr=0.1); fit(); return {}
def b_mat():
    RB((0, 0.4, 0.07), (1.5, 1.7, 0.1), "purple", lv=1); RC(0.33, 1.5, (0, -0.5, 0.36), "purple", (0, R90, 0), lv=1)
    for sx in (-1, 1): To(0.22, 0.025, (sx*0.83, -0.5, 0.36), "lavender", (0, R90, 0)); To(0.1, 0.02, (sx*0.83, -0.5, 0.36), "lavender", (0, R90, 0))
    for y in (0.0, 0.5, 1.0): RB((0, y, 0.125), (1.4, 0.08, 0.02), "lavender", lv=1)
    sface(0.44, 0.2, 0.1, mouth_dz=0.2, mr=0.08); return {}
def b_ox():
    h = quad_meta((0.72, 0.5, 0.3), (0.86, 0.7, 0.5), (0.92, 0.8, 0.62), (0.25, 0.15, 0.08), ear="round", tail="long", snout_len=0.08)
    for sx in (-1, 1):
        RC(0.08, 0.7, (sx*0.55, -0.55, 1.88), "ivory", (rad(-10), rad(sx*72), 0), lv=1); RK(0.09, 0.3, (sx*0.9, -0.6, 2.1), "ivory", (0, rad(sx*15), 0), lv=1)
    RB((0, -0.2, 1.52), (1.1, 0.22, 0.16), "wood", lv=1); S(0.12, (0, -0.8, 0.82), (1, 1, 1.1), "gold"); return h
def b_sky():
    RB((0, 0, 1.0), (1.9, 0.55, 1.7), "sky", lv=2)
    for (x, z, s) in [(-0.5, 1.5, 1.0), (0.55, 0.45, 0.85)]:
        for (dx, dz, r) in [(0, 0, 0.22), (-0.22, -0.04, 0.16), (0.22, -0.04, 0.17), (0.08, 0.1, 0.15)]: S(r*s, (x + dx*s, -0.3, z + dz*s), (1, 0.5, 1), "white")
    S(0.24, (0.55, -0.3, 1.5), (1, 0.4, 1), "yellow")
    for k in range(8): a = k*TAU/8; S(0.05, (0.55 + 0.34*math.cos(a), -0.3, 1.5 + 0.34*math.sin(a)), (1, 0.5, 1), "yellow")
    face(1.0, -0.29, 0.24, 0.12, mouth_dz=0.3, mr=0.11); return {}
def b_toe():
    RB((0.45, 0.35, 0.22), (2.1, 1.0, 0.42), "peach", lv=2)
    RC(0.48, 1.25, (-0.35, 0, 0.72), "peach", lv=2); S(0.28, (-0.35, -0.42, 1.2), (1, 0.3, 0.85), "pink")
    for (x, r, hh) in [(0.42, 0.28, 0.75), (0.92, 0.24, 0.62), (1.35, 0.2, 0.5)]: RC(r, hh, (x, 0.05, hh/2 + 0.1), "peach", lv=2); S(r*0.55, (x, -r*0.85 + 0.05, hh*0.85), (1, 0.3, 0.8), "pink")
    sface(0.72, 0.17, 0.1, x=-0.35, mouth_dz=0.28, mr=0.09); return {}
# ---------------------------------------------------------------- level 2
def b_band():
    base(2.5, 1.6, "wood", 0.24)
    RC(0.45, 0.5, (0, 0, 0.56), "red", lv=1); Cy(0.47, 0.05, (0, 0, 0.84), "cream", verts=32); To(0.46, 0.03, (0, 0, 0.84), "gold"); To(0.46, 0.03, (0, 0, 0.3), "gold")
    for sx in (-1, 1): RC(0.025, 0.6, (sx*0.25, -0.1, 1.05), "wood", (rad(20), rad(sx*35), 0), lv=1); S(0.05, (sx*0.42, -0.2, 1.28), (1, 1, 1), "wood")
    S(0.3, (-0.9, 0.1, 0.6), (1, 0.4, 1.15), "orange", rot=(0, rad(-12), 0)); S(0.1, (-0.9, -0.03, 0.6), (1, 0.4, 1), "dkbrown"); RC(0.05, 0.85, (-1.02, 0.1, 1.25), "dkbrown", (0, rad(-12), 0), lv=1); RB((-1.12, 0.1, 1.72), (0.16, 0.08, 0.22), "dkbrown", lv=1)
    RC(0.03, 1.1, (0.9, 0.0, 0.78), "dkgrey", lv=1); S(0.13, (0.9, -0.03, 1.4), (1, 1, 1.1), "charcoal"); Cy(0.2, 0.04, (0.9, 0, 0.26), "dkgrey")
    for (x, z) in [(0.35, 1.75), (-0.35, 1.95)]: S(0.1, (x, 0, z), (1.2, 0.6, 0.9), "black"); Cy(0.02, 0.4, (x + 0.1, 0, z + 0.2), "black", verts=8); S(0.07, (x + 0.17, 0, z + 0.36), (1.4, 0.5, 0.7), "black")
    face(0.6, -0.47, 0.18, 0.1, mouth_dz=0.24, mr=0.09); fit(2.0, 2.5); return {}
def b_bank():
    base(2.3, 1.9, "lgrey"); BX((0, 0.15, 0.85), (1.9, 1.2, 1.3), "cream"); BX((0, 0.1, 1.53), (2.15, 1.5, 0.12), "stone")
    Fp([(-1.05, 0), (1.05, 0), (0, 0.55)], (0, 0.1, 1.59), 1.5, "stone")
    for x in (-0.82, -0.56, 0.56, 0.82): Cy(0.085, 1.26, (x, -0.55, 0.84), "white", verts=16)
    BX((0, -0.75, 0.24), (1.9, 0.3, 0.1), "stone"); Cy(0.2, 0.07, (0, -0.68, 1.8), "gold", (R90, 0, 0)); Cy(0.13, 0.08, (0, -0.69, 1.8), "yellow", (R90, 0, 0))
    face(1.0, -0.46, 0.2, 0.11, mouth_dz=0.3, mr=0.1); fit(); return {}
def b_bean():
    metachar([((0.1, 0, 0.5), 0.46, (1, 0.8, 1)), ((-0.12, 0, 0.95), 0.4, (0.9, 0.8, 1)), ((0.1, 0, 1.4), 0.44, (1, 0.8, 1))], [], ["bean"], lambda c, n: 0, res=0.06)
    S(0.1, (0.3, -0.25, 1.62), (1, 0.4, 0.7), (0.85, 0.4, 0.4))
    sface(1.3, 0.16, 0.1, x=0.08, mouth_dz=0.26, mr=0.09); return {}
def b_bush():
    for (x, y, z, r) in [(0, 0, 0.6, 0.65), (-0.65, 0.05, 0.48, 0.5), (0.65, 0.05, 0.5, 0.52), (-0.3, 0.1, 1.1, 0.45), (0.35, 0.05, 1.05, 0.42), (0, 0.4, 0.7, 0.55)]: S(r, (x, y, z), (1, 1, 0.95), "green")
    for (x, y, z, r) in [(-0.75, -0.3, 0.75, 0.2), (0.75, -0.3, 0.8, 0.2), (0.05, -0.1, 1.45, 0.22)]: S(r, (x, y, z), (1, 1, 1), "lgreen")
    for (x, z) in [(-0.85, 0.45), (-0.45, 1.3), (0.5, 1.28), (0.95, 0.5), (0.0, 0.2)]: S(0.07, (x, surf_y(x, z, -0.4) + 0.02, z), (1, 1, 1), "red")
    sface(0.72, 0.2, 0.11, mouth_dz=0.28, mr=0.1); return {}
def b_chef():
    person("white", "white", "hairb", shoes="charcoal")
    RC(0.36, 0.3, (0, 0.02, 1.86), "white", lv=1)
    for (x, y) in [(-0.2, 0), (0.2, 0), (0, -0.15), (0, 0.2)]: S(0.26, (x, y + 0.02, 2.12), (1, 1, 0.9), "white")
    RB((0, -0.28, 1.04), (0.3, 0.1, 0.1), "red", lv=1)
    for z in (0.62, 0.8): S(0.04, (-0.12, -0.31, z), (1, 0.5, 1), "dkgrey"); S(0.04, (0.12, -0.31, z), (1, 0.5, 1), "dkgrey")
    RC(0.03, 0.6, (0.62, -0.12, 0.72), "wood", (0, rad(12), 0), lv=1); S(0.11, (0.68, -0.12, 1.08), (1, 0.5, 1.3), "wood"); return {}
def b_clam():
    S(0.85, (0, 0, 0.42), (1, 0.9, 0.48), "lavender"); p = E((0, 0.65, 0.55))
    S(0.85, (0, 0, 0.95), (1, 0.9, 0.48), "lavender", p); p.rotation_euler = (rad(-28), 0, 0)
    for k in range(5): a = rad(-50 + 25*k); S(0.09, (0.78*math.sin(a), -0.72*math.cos(a), 0.42), (1, 1, 0.8), "purple")
    S(0.7, (0, 0.05, 0.6), (1, 0.85, 0.35), "pink"); S(0.2, (0.38, -0.3, 0.78), (1, 1, 1), "white")
    face(0.82, -0.52, 0.17, 0.11, x=-0.12, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.62, -0.72, 0.1, x=-0.12, tongue=False); return {"lid": p}
def coin(c, r, rim=None, emblem=None, z=None):
    z = z or r + 0.05; Cy(r, 0.16, (0, 0, z), c, (R90, 0, 0), verts=48); To(r*0.92, 0.04, (0, -0.07, z), rim or c, (R90, 0, 0)); To(r*0.92, 0.04, (0, 0.07, z), rim or c, (R90, 0, 0))
    if emblem: emblem(z)
    face(z + r*0.12, -0.09, r*0.3, r*0.15, mouth_dz=r*0.42, mr=r*0.14)
def b_dime():
    coin("silver", 0.7, emblem=lambda z: [S(0.05, (0.5*math.cos(k*TAU/12), -0.09, z + 0.5*math.sin(k*TAU/12)), (1, 0.4, 1), "lgrey") for k in range(12)]); return {}
def b_dirt():
    S(0.95, (0, 0, 0.3), (1.25, 1.0, 0.75), "brown"); S(0.5, (-0.6, 0.2, 0.55), (1, 1, 0.8), "dkbrown"); S(0.45, (0.65, 0.1, 0.5), (1, 1, 0.8), "dkbrown"); S(0.4, (0.1, 0.2, 0.9), (1, 1, 0.8), "brown")
    for (x, y, z) in [(-0.9, -0.6, 0.1), (0.8, -0.7, 0.08), (1.1, -0.2, 0.1), (-1.2, 0.0, 0.1)]: S(0.12, (x, y, z), (1.2, 1, 0.7), "stone")
    RC(0.07, 0.5, (0.7, -0.2, 0.95), "pink", (0, rad(25), 0), lv=1); S(0.08, (0.82, -0.2, 1.2), (1, 1, 1), "pink")
    RC(0.03, 0.35, (-0.5, 0.1, 1.05), "green", lv=1); S(0.12, (-0.4, 0.1, 1.25), (1.4, 0.6, 0.5), "lgreen"); S(0.12, (-0.6, 0.1, 1.22), (1.4, 0.6, 0.5), "lgreen")
    sface(0.45, 0.2, 0.11, mouth_dz=0.24, mr=0.1); return {}
def b_dish():
    Cy(0.95, 0.1, (0, 0, 1.0), "white", (R90, 0, 0), verts=48); To(0.88, 0.06, (0, -0.03, 1.0), "sky", (R90, 0, 0)); To(0.6, 0.025, (0, -0.05, 1.0), "lgrey", (R90, 0, 0))
    for k in range(10): a = k*TAU/10; S(0.045, (0.74*math.cos(a), -0.06, 1.0 + 0.74*math.sin(a)), (1, 0.4, 1), "blue")
    face(1.08, -0.06, 0.2, 0.11, mouth_dz=0.3, mr=0.1); return {}
def b_doll():
    person("lavender", "lavender", "blonde", shoes="purple"); RK(0.58, 0.55, (0, 0, 0.5), "lavender", lv=2, r2=0.3)
    for sx in (-1, 1):
        S(0.2, (sx*0.52, 0.05, 1.3), (0.8, 0.8, 1.3), "blonde"); S(0.07, (sx*0.45, 0.02, 1.52), (1, 1, 1), "red"); S(0.07, (sx*0.26, -0.37, 1.27), (1, 0.4, 0.8), "pink")
    for sx in (-1, 1): S(0.13, (sx*0.14, -0.12, 1.92), (1.2, 0.6, 1), "red", rot=(0, rad(sx*25), 0))
    S(0.07, (0, -0.12, 1.9), (1, 1, 1), "hotpink")
    for (x, z) in [(-0.2, 0.55), (0.15, 0.4), (0.3, 0.7), (-0.1, 0.85)]: S(0.05, (x, surf_y(x, z, -0.4) + 0.01, z), (1, 1, 1), "white")
    return {}
def b_gate():
    for sx in (-1, 1): BX((sx*1.0, 0, 0.95), (0.26, 0.26, 1.9), "brown"); S(0.17, (sx*1.0, 0, 1.98), (1, 1, 1), "dkbrown")
    for k in range(5):
        x = -0.64 + 0.32*k; hh = 1.25 + 0.18*(2 - abs(k - 2)); BX((x, 0, 0.2 + hh/2), (0.26, 0.1, hh), "wood", bevel=0.03); Fp([(-0.13, 0), (0.13, 0), (0, 0.16)], (x, 0, 0.2 + hh), 0.1, "wood")
    for z in (0.5, 1.15): BX((0, 0.06, z), (1.75, 0.06, 0.12), "brown", bevel=0.02)
    S(0.06, (0.72, -0.08, 0.9), (1, 1, 1), "charcoal"); To(0.07, 0.02, (0.72, -0.1, 0.8), "charcoal", (R90, 0, 0))
    face(1.0, -0.06, 0.2, 0.1, mouth_dz=0.26, mr=0.09); return {}
def b_horn():
    Co(0.62, 0.85, (0, -0.5, 1.0), "gold", (-R90, 0, 0), r2=0.12); To(0.6, 0.05, (0, -0.92, 1.0), "yellow", (R90, 0, 0)); Cy(0.55, 0.02, (0, -0.88, 1.0), "dkbrown", (R90, 0, 0), verts=32)
    RC(0.1, 1.3, (0, 0.45, 1.0), "gold", (R90, 0, 0), lv=1); To(0.32, 0.075, (0, 0.5, 0.72), "gold", (0, R90, 0)); Cy(0.14, 0.14, (0, 1.15, 1.0), "yellow", (R90, 0, 0))
    for k in range(3): Cy(0.06, 0.25, (0, 0.2 + 0.18*k, 1.2), "yellow", verts=12); S(0.07, (0, 0.2 + 0.18*k, 1.34), (1, 1, 0.6), "ivory")
    face(1.08, -0.9, 0.2, 0.11, mouth_dz=0.3, mr=0.1); return {}
def b_lake():
    BX((0, 0, 0.1), (2.6, 2.2, 0.2), "grass", bevel=0.08); S(1.0, (0, 0, 0.2), (1.15, 0.95, 0.42), "water"); S(0.5, (-0.2, 0.1, 0.56), (1.2, 0.8, 0.12), "sky")
    for (x, y) in [(-1.05, 0.7), (-0.95, 0.85), (1.1, 0.6)]: RC(0.03, 0.7, (x, y, 0.55), "green", lv=1); RC(0.06, 0.25, (x, y, 0.95), "brown", lv=1)
    tree_s(1.0, 0.85, 0.8); S(0.16, (0.45, 0.25, 0.68), (1, 1.2, 0.9), "yellow"); S(0.1, (0.45, 0.1, 0.8), (1, 1, 1), "yellow"); Co(0.04, 0.1, (0.45, -0.02, 0.79), "orange", (R90, 0, 0))
    for (x, y) in [(-1.1, -0.8), (0.9, -0.9), (1.15, -0.3)]: S(0.14, (x, y, 0.24), (1.2, 1, 0.7), "stone")
    sface(0.4, 0.22, 0.11, mouth_dz=0.2, mr=0.09); fit(1.6, 2.5); return {}
def b_mall():
    base(2.6, 1.8, "lgrey"); BX((0, 0.2, 0.95), (2.3, 1.1, 1.5), "sky"); BX((0, 0.2, 1.76), (2.4, 1.2, 0.14), "white")
    BX((0, -0.38, 1.45), (1.5, 0.1, 0.34), "hotpink"); BX((0, -0.4, 0.55), (0.6, 0.06, 0.7), "glass", bevel=0.02)
    for sx in (-1, 1): BX((sx*0.8, -0.37, 0.65), (0.5, 0.06, 0.5), "glass", bevel=0.02); Fp([(-0.3, 0), (0.3, 0), (0.3, 0.14), (-0.3, 0.14)], (sx*0.8, -0.5, 0.92), 0.25, "yellow", rot=(rad(25), 0, 0))
    for k in range(5): S(0.07, (-0.56 + 0.28*k, -0.44, 1.45), (1, 0.5, 1), "white")
    for sx in (-1, 1): S(0.16, (sx*1.15, -0.7, 0.36), (1, 1, 1), "green"); RC(0.1, 0.16, (sx*1.15, -0.7, 0.26), "rust", lv=1)
    face(1.08, -0.36, 0.2, 0.1, mouth_dz=0.2, mr=0.08); fit(); return {}
def b_newt():
    EL = [((0, 0.1, 0.42), 0.36, (0.85, 1.7, 0.75)), ((0, -0.75, 0.52), 0.34, (1.05, 1.05, 0.8))] + chain((0, 0.6, 0.38), (0.45, 1.75, 0.22), 0.26, 0.09, 6)
    for sx in (-1, 1): EL += [((sx*0.45, -0.3, 0.22), 0.16, None), ((sx*0.62, -0.42, 0.1), 0.13, (1.2, 1.3, 0.6)), ((sx*0.45, 0.55, 0.22), 0.16, None), ((sx*0.62, 0.62, 0.1), 0.13, (1.2, 1.3, 0.6))]
    def region(c, n): return 1 if (n.z < -0.3 and c.z < 0.4) else 0
    metachar(EL, [], ["orange", "yellow"], region, res=0.06)
    for (x, y) in [(-0.15, 0.0), (0.12, 0.3), (-0.1, 0.6), (0.15, 0.95), (0.25, 1.3), (0.0, -0.4)]: S(0.07, (x, y, 0.66 if y < 0.7 else 0.5), (1, 1, 0.4), "charcoal")
    sface(0.66, 0.17, 0.1, mouth_dz=0.2, mr=0.09, fb=-1.0); return {}
def b_park():
    BX((0, 0, 0.1), (2.6, 2.2, 0.2), "grass", bevel=0.08); BX((0.2, -0.2, 0.21), (0.5, 2.1, 0.03), "sand", bevel=0.01)
    tree_s(-0.75, 0.4, 1.5); tree_s(1.0, 0.7, 0.9, "lgreen")
    BX((0.85, -0.45, 0.5), (0.7, 0.2, 0.06), "wood", bevel=0.02); BX((0.85, -0.33, 0.7), (0.7, 0.05, 0.25), "wood", bevel=0.02)
    for sx in (-1, 1): BX((0.85 + sx*0.28, -0.42, 0.34), (0.06, 0.18, 0.28), "dkgrey", bevel=0.01)
    for (x, y, c) in [(-0.3, -0.8, "red"), (-0.9, -0.75, "yellow"), (0.6, -0.9, "pink"), (1.1, 0.0, "white")]: RC(0.02, 0.2, (x, y, 0.3), "green", lv=1); S(0.07, (x, y, 0.43), (1, 1, 0.7), c)
    sface(1.55, 0.2, 0.11, x=-0.75, mouth_dz=0.26, mr=0.1); fit(); return {}
def b_pool():
    BX((0, 0, 0.3), (2.5, 1.9, 0.6), "white", bevel=0.08); BX((0, 0, 0.56), (2.15, 1.55, 0.1), "water", bevel=0.03)
    for k in range(3): BX((-0.6 + 0.6*k, 0.1*(k % 2), 0.615), (0.35, 0.05, 0.02), "white", bevel=0.01)
    To(0.26, 0.09, (0.5, 0.2, 0.68), "red", (0, 0, 0)); To(0.26, 0.092, (0.5, 0.2, 0.68), "white", (0, 0, 0), scale=(0.35, 1.02, 1.02))
    for sx in (-1, 1): RC(0.03, 0.6, (-1.0 + sx*0.14, 0.75, 0.85), "lgrey", lv=1)
    for z in (0.75, 0.95): Cy(0.02, 0.28, (-1.0, 0.75, z), "lgrey", (0, R90, 0), verts=8)
    BX((1.0, 0.85, 0.7), (0.5, 0.3, 0.1), "sky", bevel=0.03); BX((1.0, 1.0, 0.45), (0.2, 0.1, 0.5), "lgrey", bevel=0.02)
    face(0.34, -0.96, 0.24, 0.12, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.16, -0.97, 0.1); fit(1.3, 2.5); return {}
def b_ramp():
    Fp([(-1.3, 0), (1.3, 0), (1.3, 1.1), (1.1, 1.1)], (0, 0, 0), 1.3, "orange"); BX((1.2, 0, 1.12), (0.3, 1.34, 0.06), "dkgrey", bevel=0.02)
    for k in range(4): t = 0.2 + 0.2*k; Fp([(-0.06, 0), (0.06, 0), (0.06, 0.03), (-0.06, 0.03)], (-1.3 + 2.4*t, 0, 1.1*t - 0.01), 1.32, "yellow", rot=(0, rad(-24.6), 0))
    b = E((-0.1, 0, 0.62)); BX((-0.1, 0, 0.66), (0.7, 0.24, 0.05), "blue", b, bevel=0.02)
    for sx in (-1, 1): Cy(0.07, 0.3, (-0.1 + sx*0.24, 0, 0.59), "white", (R90, 0, 0), b, verts=12)
    b.rotation_euler = (0, rad(-24.6), 0)
    face(0.42, -0.66, 0.18, 0.1, x=0.55, mouth_dz=0.24, mr=0.09); return {}
def b_room():
    BX((0, 0, 0.08), (2.3, 2.0, 0.16), "wood", bevel=0.04); BX((0, 0.95, 0.95), (2.3, 0.12, 1.7), "cream", bevel=0.04); BX((1.1, 0, 0.95), (0.12, 2.0, 1.7), "sand", bevel=0.04)
    BX((-0.55, 0.88, 1.3), (0.6, 0.05, 0.5), "sky", bevel=0.02); BX((-0.55, 0.86, 1.3), (0.04, 0.04, 0.5), "white", bevel=0.0); BX((-0.55, 0.86, 1.3), (0.6, 0.04, 0.04), "white", bevel=0.0)
    BX((0.5, 0.35, 0.36), (0.9, 1.1, 0.3), "blue", bevel=0.08); BX((0.5, 0.75, 0.56), (0.8, 0.3, 0.14), "white", bevel=0.06); BX((0.5, 0.86, 0.6), (0.95, 0.08, 0.7), "brown", bevel=0.03)
    S(0.45, (-0.5, -0.3, 0.17), (1, 0.8, 0.05), "red"); BX((-0.85, 0.6, 0.4), (0.4, 0.4, 0.5), "brown", bevel=0.03); RC(0.03, 0.3, (-0.85, 0.6, 0.8), "dkgrey", lv=1); Co(0.2, 0.25, (-0.85, 0.6, 1.05), "yellow", r2=0.1)
    face(1.3, 0.87, 0.18, 0.1, x=0.4, mouth_dz=0.24, mr=0.09); fit(); return {}
def b_rope():
    for k in range(5): To(0.62 - 0.03*k, 0.13, (0, 0, 0.14 + 0.22*k), "straw")
    for k in range(5):
        for j in range(14): a = j*TAU/14 + k*0.2; S(0.03, ((0.75 - 0.03*k)*math.cos(a), (0.75 - 0.03*k)*math.sin(a), 0.14 + 0.22*k), (1, 1, 2.5), "wood", rot=(0, 0, a))
    RC(0.12, 0.7, (0.3, 0.1, 1.4), "straw", (0, rad(20), 0), lv=1); S(0.16, (0.42, 0.1, 1.75), (1, 1, 1), "straw"); To(0.13, 0.03, (0.36, 0.1, 1.55), "red", (0, rad(20), 0))
    sface(0.62, 0.2, 0.11, mouth_dz=0.3, mr=0.1); return {}
def b_sail():
    BX((0, 0, 0.18), (1.9, 0.6, 0.3), "wood", bevel=0.1); RC(0.05, 2.1, (-0.1, 0, 1.3), "brown", lv=1)
    Fp([(0, 0), (1.25, 0.1), (0, 1.75)], (-0.02, 0, 0.45), 0.08, "white"); Fp([(0, 0), (-0.7, 0.1), (0, 1.2)], (-0.18, 0, 0.5), 0.08, "red")
    Fp([(0, 0), (0.75, 0.06), (0.5, 0.4), (0, 0.42)], (-0.02, -0.01, 0.45), 0.09, "sky"); Fp([(0, 0), (0.3, -0.1), (0, -0.2)], (-0.1, 0, 2.38), 0.03, "red")
    face(1.2, -0.07, 0.15, 0.09, x=0.33, mouth_dz=0.22, mr=0.08); return {}
def b_sand():
    S(1.15, (0, 0, 0.05), (1.2, 1.0, 0.3), "sand"); BX((0, 0.1, 0.65), (1.3, 0.9, 0.8), "sand", bevel=0.08)
    for sx in (-1, 1):
        RC(0.3, 1.2, (sx*0.7, 0.1, 0.8), "sand", lv=1); Co(0.34, 0.4, (sx*0.7, 0.1, 1.62), "straw")
        for k in range(4): a = k*TAU/4 + 0.4; BX((sx*0.7 + 0.27*math.cos(a), 0.1 + 0.27*math.sin(a), 1.42), (0.14, 0.14, 0.14), "sand", bevel=0.03)
    for k in range(4): BX((-0.42 + 0.28*k, -0.3, 1.1), (0.16, 0.16, 0.16), "sand", bevel=0.03)
    Cy(0.02, 0.6, (0.7, 0.1, 2.1), "brown", verts=8); Fp([(0, 0), (0.35, 0.1), (0, 0.22)], (0.7, 0.1, 2.15), 0.03, "red")
    Fp([(-0.16, 0), (0.16, 0), (0.16, 0.3), (0, 0.42), (-0.16, 0.3)], (0, -0.36, 0.3), 0.06, "dkbrown")
    RC(0.2, 0.34, (-1.1, -0.6, 0.27), "red", lv=1); To(0.2, 0.02, (-1.1, -0.6, 0.5), "yellow", (R90, 0, 0)); S(0.1, (1.0, -0.7, 0.12), (1.4, 0.8, 0.6), "pink")
    face(0.82, -0.36, 0.2, 0.1, mouth_dz=0.0, mr=0.0, tongue=False); fit(); return {}
def b_tire():
    To(0.68, 0.3, (0, 0, 1.0), "charcoal", (R90, 0, 0)); Cy(0.42, 0.3, (0, 0, 1.0), "lgrey", (R90, 0, 0), verts=32); Cy(0.12, 0.34, (0, 0, 1.0), "dkgrey", (R90, 0, 0))
    for k in range(18): a = k*TAU/18; BX((0.97*math.cos(a), 0, 1.0 + 0.97*math.sin(a)), (0.1, 0.5, 0.07), "black", rot=(0, -a + R90, 0), bevel=0.02)
    for k in range(5): a = k*TAU/5 + 0.3; S(0.045, (0.28*math.cos(a), -0.16, 1.0 + 0.28*math.sin(a)), (1, 0.5, 1), "dkgrey")
    face(1.08, -0.16, 0.15, 0.085, mouth_dz=0.2, mr=0.07); return {}
def b_town():
    BX((0, 0, 0.1), (2.7, 2.0, 0.2), "grass", bevel=0.08); BX((0, -0.65, 0.21), (2.7, 0.5, 0.03), "dkgrey", bevel=0.01)
    for k in range(4): BX((-0.9 + 0.6*k, -0.65, 0.23), (0.25, 0.05, 0.01), "white", bevel=0.0)
    house(-0.85, 0.2, 0.7, 0.7, 0.8, "yellow", "roof"); house(0.85, 0.25, 0.7, 0.7, 1.0, "sky", "navy"); house(0, 0.1, 0.8, 0.8, 1.3, "coral", "brown", door="dkbrown")
    BX((0.85, 0.6, 1.6), (0.14, 0.14, 0.3), "brick", bevel=0.02); tree_s(-1.15, -0.2, 0.6); tree_s(1.2, -0.25, 0.55, "lgreen")
    face(1.15, -0.31, 0.16, 0.09, mouth_dz=0.2, mr=0.07); fit(); return {}
def b_vest():
    RB((0, 0, 0.9), (1.3, 0.5, 1.45), "red", lv=1)
    Fp([(-0.3, 0), (0.3, 0), (0, -0.75)], (0, -0.3, 1.72), 0.1, "cream"); BX((0, -0.33, 0.75), (0.05, 0.04, 0.9), "roof", bevel=0.01)
    for sx in (-1, 1): S(0.2, (sx*0.6, 0, 1.3), (0.45, 0.9, 1.2), "roof"); BX((sx*0.3, -0.33, 0.45), (0.3, 0.05, 0.1), "roof", bevel=0.02)
    for z in (0.5, 0.75, 1.0): S(0.05, (0.12, -0.36, z), (1, 0.5, 1), "gold")
    face(1.25, -0.31, 0.3, 0.1, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.75, -0.34, 0.09, x=-0.25); return {}
def b_wind():
    for (x, z, r) in [(0, 1.2, 0.6), (-0.6, 1.1, 0.42), (0.55, 1.15, 0.45), (-0.2, 1.6, 0.4), (0.3, 1.58, 0.38)]: S(r, (x, 0, z), (1, 0.75, 1), (0.82, 0.92, 1.0))
    for (x, z, R_) in [(1.25, 1.0, 0.3), (1.75, 1.35, 0.22), (1.3, 0.45, 0.2)]:
        To(R_, 0.055, (x, 0, z), "sky", (R90, 0, 0)); RC(0.055, 0.7, (x - 0.35, 0, z - R_), "sky", (0, R90, 0), lv=1)
    for (x, z) in [(1.85, 0.7), (2.0, 1.75)]: S(0.1, (x, 0, z), (1.6, 0.4, 0.7), "lgreen", rot=(0, rad(30), 0))
    for sx in (-1, 1): S(0.12, (sx*0.36, -0.42, 1.02), (1, 0.4, 0.8), "pink")
    eyes(1.3, -0.45, 0.2, 0.11); S(0.1, (0.12, -0.5, 0.98), (1, 0.5, 1), "mouth"); fit(2.0, 2.6); return {}
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}
