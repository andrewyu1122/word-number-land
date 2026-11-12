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
    e = E((0, 0, 0)); n0 = len(LIDS)
    BX((0, 0, 0.85), (2.3, 0.14, 1.5), "brown", e, bevel=0.05); BX((0, -0.03, 0.85), (2.05, 0.14, 1.25), "straw", e, bevel=0.03)
    for k in range(5): BX((0, -0.045, 0.37 + 0.24*k), (2.05, 0.14, 0.1), "red" if k % 2 == 0 else "green", e, bevel=0.01)
    for sx in (-1, 1):
        for k in range(9): BX((sx*1.2, 0, 0.2 + 0.16*k), (0.12, 0.08, 0.05), "straw", e, bevel=0.01)
    face(0.95, -0.11, 0.2, 0.1, parent=e, mouth_dz=0.22, mr=0.09)
    e.rotation_euler = (rad(-62), 0, 0); e.location = (0, -0.6, 0.02); bpy.context.view_layer.update()
    M = e.matrix_world
    for i in range(n0, len(LIDS)): pp, parent, r = LIDS[i]; LIDS[i] = (M @ Vector(pp), parent, r)
    return {}
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
    RB((0.35, 0.55, 0.3), (2.3, 1.5, 0.58), "peach", lv=2)                                # front half of the foot
    S(0.8, (-0.6, -0.45, 0.78), (1, 1.1, 0.98), "peach"); S(0.5, (-0.6, -0.5, 1.42), (1, 1.05, 0.4), "red", rot=(rad(-22), 0, 0)); S(0.12, (-0.8, -0.7, 1.56), (1.5, 0.8, 0.3), "white", rot=(rad(-22), 0, 0))
    for k, (x, r) in enumerate([(0.22, 0.3), (0.72, 0.27), (1.15, 0.23), (1.5, 0.19)]):
        y = -0.25 + 0.14*k; S(r, (x, y, r*0.95), (1, 1.15, 0.95), "peach"); S(r*0.55, (x, y - r*0.2, r*1.75), (1, 1.1, 0.35), "pink", rot=(rad(-14), 0, 0))
    sface(0.85, 0.24, 0.13, x=-0.6, mouth_dz=0.32, mr=0.11, fb=-1.2); return {}
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
def T3(txt, size, loc, c, depth=0.04):
    """extruded text standing up, facing the camera side (-Y)"""
    bpy.ops.object.text_add(location=loc, rotation=(R90, 0, 0)); o = bpy.context.active_object
    o.data.body = txt; o.data.size = size; o.data.extrude = depth; o.data.align_x = 'CENTER'; o.data.align_y = 'CENTER'
    try: o.data.font = bpy.data.fonts.load("C:/Windows/Fonts/arialbd.ttf", check_existing=True)
    except Exception: pass
    o.data.materials.append(mat(c)); par(o, ROOT); return o
def coin(c, r, thick, rim, txt, tc, ridges=False):
    z = r + 0.05; Cy(r, thick, (0, 0, z), c, (R90, 0, 0), verts=64)
    for sy in (-1, 1): To(r*0.93, 0.045, (0, sy*thick/2, z), rim, (R90, 0, 0))
    if ridges:
        for k in range(48): a = k*TAU/48; BX((r*1.01*math.cos(a), 0, z + r*1.01*math.sin(a)), (0.06, thick, 0.035), rim, rot=(0, -a, 0), bevel=0.0)
    yf = -thick/2 - 0.03
    T3(txt, r*(1.15 if len(txt) < 3 else 0.84), (0, yf, z + r*0.22), tc, depth=0.05)
    face(z - r*0.48, yf + 0.02, r*0.19, r*0.1, mouth_dz=r*0.2, mr=r*0.09)
def b_dime(): coin("silver", 0.6, 0.09, "lgrey", "10¢", (0.12, 0.13, 0.2)); return {}
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
def lizard(c, belly, spot=None, tail=(0.45, 1.75, 0.22), hr=0.34):
    EL = [((0, 0.1, 0.42), 0.36, (0.85, 1.7, 0.75)), ((0, -0.75, 0.52), hr, (1.05, 1.05, 0.8))] + chain((0, 0.6, 0.38), tail, 0.26, 0.09, 6)
    for sx in (-1, 1): EL += [((sx*0.45, -0.3, 0.22), 0.16, None), ((sx*0.62, -0.42, 0.1), 0.13, (1.2, 1.3, 0.6)), ((sx*0.45, 0.55, 0.22), 0.16, None), ((sx*0.62, 0.62, 0.1), 0.13, (1.2, 1.3, 0.6))]
    def region(cc, n): return 1 if (n.z < -0.3 and cc.z < 0.4) else 0
    metachar(EL, [], [c, belly], region, res=0.06)
    if spot:
        for (x, y) in [(-0.15, 0.0), (0.12, 0.3), (-0.1, 0.6), (0.15, 0.95), (0.25, 1.3), (0.0, -0.4)]: S(0.07, (x, y, 0.66 if y < 0.7 else 0.5), (1, 1, 0.4), spot)
    sface(0.66, 0.17, 0.1, mouth_dz=0.2, mr=0.09, fb=-1.0)
def b_newt(): lizard("orange", "yellow", "charcoal"); return {}
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
    C = "orange"
    pts = [(-0.75, 0.12), (0.75, 0.12), (0.8, 1.05), (0.56, 1.22), (0.5, 1.6), (0.62, 1.98), (0.3, 2.0), (0, 1.15), (-0.3, 2.0), (-0.62, 1.98), (-0.5, 1.6), (-0.56, 1.22), (-0.8, 1.05)]
    o = Fp(pts, (0, 0, 0), 0.36, C); bevel(o, 0.05)
    BX((0, 0.16, 1.0), (1.35, 0.06, 1.7), "navy", bevel=0.03); Fp([(-0.36, 1.98), (0.36, 1.98), (0.3, 1.5), (-0.3, 1.5)], (0, 0.14, 0), 0.1, "navy")
    for sx in (-1, 1):
        Fp([(sx*0.3, 2.0), (sx*0.0, 1.15), (sx*0.1, 1.12), (sx*0.42, 1.98)], (0, -0.19, 0), 0.03, "yellow")
        for z in (0.35, 0.6, 0.85): S(0.06, (sx*0.14, -0.2, z), (1, 0.5, 1), "white")
        BX((sx*0.45, -0.19, 0.36), (0.36, 0.03, 0.08), "yellow", bevel=0.01)
    BX((0, -0.19, 0.6), (0.03, 0.02, 1.0), "rust", bevel=0.0)
    eyes(1.3, -0.2, 0.42, 0.095); smile(1.02, -0.2, 0.0001, x=0) if False else None
    S(0.001, (0, 0, 1), (1, 1, 1), C).hide_render = True; smile(0.16 + 0.9, -0.21, 0.085, x=0.42, tongue=False); return {}
def b_wind():
    for (x, z, r) in [(0, 1.2, 0.6), (-0.6, 1.1, 0.42), (0.55, 1.15, 0.45), (-0.2, 1.6, 0.4), (0.3, 1.58, 0.38)]: S(r, (x, 0, z), (1, 0.75, 1), (0.82, 0.92, 1.0))
    for (x, z, R_) in [(1.25, 1.0, 0.3), (1.75, 1.35, 0.22), (1.3, 0.45, 0.2)]:
        To(R_, 0.055, (x, 0, z), "sky", (R90, 0, 0)); RC(0.055, 0.7, (x - 0.35, 0, z - R_), "sky", (0, R90, 0), lv=1)
    for (x, z) in [(1.85, 0.7), (2.0, 1.75)]: S(0.1, (x, 0, z), (1.6, 0.4, 0.7), "lgreen", rot=(0, rad(30), 0))
    for sx in (-1, 1): S(0.12, (sx*0.36, -0.42, 1.02), (1, 0.4, 0.8), "pink")
    eyes(1.3, -0.45, 0.2, 0.11); S(0.1, (0.12, -0.5, 0.98), (1, 0.5, 1), "mouth"); fit(2.0, 2.6); return {}
# ---------------------------------------------------------------- level 3
def placed(fn, loc, sc=1.0):
    """build something with fn() at the origin, then move / scale it as a group"""
    before = {o.name for o in ROOT.children}; n0 = len(LIDS); fn()
    e = E((0, 0, 0))
    for o in [o for o in ROOT.children if o.name not in before and o is not e]: par(o, e)
    e.location = loc; e.scale = (sc, sc, sc); bpy.context.view_layer.update()
    for i in range(n0, len(LIDS)):
        pp, parent, r = LIDS[i]
        if parent is None: LIDS[i] = (Vector(pp)*sc + Vector(loc), None, r*sc)
    return e
def bird(c, belly=None, beak="orange", s=1.0, legh=0.55, legc="orange", beak_len=0.3, beak_r=0.08, neck=0.0, wing=None, wl=0.6, tail=True, crest=None):
    bz = legh + 0.5*s
    S(0.4*s, (0, 0.05, bz), (0.9, 1.3, 0.85), c)
    if belly: S(0.3*s, (0, -0.12, bz - 0.06*s), (0.85, 1.1, 0.8), belly)
    hz = bz + 0.35*s + neck; hy = -0.42*s - neck*0.25
    if neck: RC(0.11*s, neck + 0.3*s, (0, (hy - 0.2*s)/2, (bz + hz)/2), c, (rad(14), 0, 0), lv=1)
    S(0.3*s, (0, hy, hz), (1, 1, 1), c); Co(beak_r*s, beak_len*s, (0, hy - 0.26*s - beak_len*s/2, hz - 0.04*s), beak, (R90, 0, 0))
    if tail:
        for k in range(3): S(0.11*s, (0.1*s*(k-1), 0.6*s, bz - 0.05*s), (0.4, 1.2, 1.4), c, rot=(rad(-35), 0, rad(k*12-12)))
    if crest: S(0.1*s, (0, hy + 0.05*s, hz + 0.3*s), (0.5, 1, 1.2), crest)
    legs2(legc, 0, legh, 0.03*max(s, 0.8), 0.12*s, foot=legc); eyes(hz + 0.08*s, hy - 0.2*s, 0.13*s, 0.08*s)
    return {"wings": wingpair(0.0, bz + 0.1*s, wing or c, wl*s, "oval", 0.35*s), "flap": 35}
def shape(pts, c, c2, thick=0.3):
    o = Fp(pts, (0, 0, 0), thick, c); bm = o.modifiers.new("Bevel", 'BEVEL'); bm.width = 0.05; bm.segments = 3
    cx = sum(x for x, z in pts)/len(pts); cz = sum(z for x, z in pts)/len(pts)
    Fp([(cx + (x - cx)*0.72, cz + (z - cz)*0.72) for x, z in pts], (0, -0.02, 0), thick, c2)
    return cx, cz
def b_beach():
    BX((0, 0, 0.1), (2.6, 2.2, 0.2), "sand", bevel=0.08); BX((0, 0.8, 0.13), (2.6, 0.6, 0.22), "water", bevel=0.06); BX((0, 0.48, 0.2), (2.6, 0.08, 0.06), "white", bevel=0.03)
    RC(0.04, 1.5, (-0.4, 0.0, 0.9), "wood", (0, rad(8), 0), lv=1); Co(0.85, 0.5, (-0.3, 0, 1.75), "red", (0, rad(8), 0), verts=10)
    for k in range(5): a = k*TAU/5; S(0.1, (-0.3 + 0.8*math.cos(a), 0.8*math.sin(a), 1.52), (1, 1, 1), "white")
    BX((0.7, -0.35, 0.22), (0.6, 0.95, 0.04), "hotpink", bevel=0.02, rot=(0, 0, rad(12)))
    S(0.26, (0.85, 0.2, 0.46), (1, 1, 1), "white"); S(0.262, (0.85, 0.2, 0.46), (1, 0.35, 1), "blue"); S(0.262, (0.85, 0.2, 0.46), (0.35, 1, 1), "yellow")
    RC(0.16, 0.26, (-1.0, -0.65, 0.33), "blue", lv=1); S(0.1, (0.1, -0.85, 0.24), (1.4, 0.8, 0.6), "coral")
    sface(1.72, 0.2, 0.1, x=-0.3, mouth_dz=0.0, mr=0.01, tongue=False); fit(); return {}
def b_beetle():
    S(0.7, (0, 0.15, 0.6), (1.0, 1.2, 0.75), "green"); S(0.42, (0, -0.7, 0.55), (1.1, 0.9, 0.8), "charcoal")
    BX((0, 0.2, 1.1), (0.04, 1.3, 0.06), "dkgreen", bevel=0.02)
    for (x, y) in [(-0.35, -0.1), (0.35, -0.1), (-0.4, 0.45), (0.4, 0.45), (-0.25, 0.85), (0.25, 0.85)]: S(0.1, (x, y, 1.02 - abs(y - 0.2)*0.25), (1, 1, 0.4), "lgreen")
    for sx in (-1, 1):
        for k in range(3): RC(0.045, 0.55, (sx*0.75, -0.3 + 0.45*k, 0.28), "charcoal", (0, rad(sx*-50), rad(sx*(k-1)*-18)), lv=1)
        RC(0.025, 0.5, (sx*0.2, -1.05, 1.0), "charcoal", (rad(40), rad(sx*20), 0), lv=1); S(0.05, (sx*0.26, -1.22, 1.2), (1, 1, 1), "charcoal")
    sface(0.62, 0.18, 0.1, mouth_dz=0.22, mr=0.09, fb=-1.0); return {}
def b_berry():
    import random; random.seed(3)
    S(0.62, (0, 0, 0.75), (1, 1, 1.15), "hotpink")
    for k in range(46):
        a = random.uniform(0, TAU); b_ = random.uniform(0.25, 2.9); S(0.17, (0.6*math.cos(a)*math.sin(b_), 0.6*math.sin(a)*math.sin(b_), 0.75 + 0.7*math.cos(b_)), (1, 1, 1), "hotpink" if k % 3 else (0.85, 0.15, 0.4))
    for k in range(5): a = k*TAU/5; S(0.2, (0.25*math.cos(a), 0.25*math.sin(a), 1.5), (1.3, 0.6, 0.35), "green", rot=(0, rad(-20), a))
    RC(0.04, 0.3, (0, 0, 1.65), "dkgreen", lv=1); sface(0.85, 0.2, 0.11, mouth_dz=0.28, mr=0.1); return {}
def b_bunny():
    EL = [((0, 0.15, 0.62), 0.62, (1.0, 1.1, 1.0)), ((0, -0.2, 1.35), 0.5, None), ((0, -0.5, 1.22), 0.26, (1.2, 1, 0.8))]
    metachar(EL, [], ["white", "cream"], lambda cc, n: 1 if (n.y < -0.4 and cc.z < 0.95 and abs(cc.x) < 0.4) else 0, res=0.06)
    for sx in (-1, 1):
        RC(0.14, 1.35, (sx*0.24, -0.1, 2.45), "white", (rad(-4), rad(sx*5), 0), lv=2); RC(0.075, 1.05, (sx*0.24, -0.215, 2.45), "pink", (rad(-4), rad(sx*5), 0), lv=2)
        S(0.24, (sx*0.42, -0.5, 0.14), (0.9, 1.7, 0.55), "white"); S(0.14, (sx*0.22, -0.52, 0.72), (1, 1, 1.2), "white")
        for k in range(3): Cy(0.008, 0.36, (sx*0.36, -0.68, 1.2 + 0.05*k), "lgrey", (0, rad(sx*80 + k*8), 0), verts=6)
        BX((sx*0.045, -0.77, 1.05), (0.08, 0.03, 0.12), "white", bevel=0.01)
    S(0.3, (0.3, 0.72, 0.55), (1, 1, 1), "white"); S(0.08, (0, -0.78, 1.26), (1.3, 0.8, 0.9), "hotpink")
    sface(1.48, 0.2, 0.1, mouth_dz=0.0, mr=0.01, tongue=False); smile(1.14, surf_y(0, 1.14, -0.7) - 0.015, 0.07, tongue=False); return {}
def b_camera():
    BX((0, 0, 0.72), (1.7, 0.75, 1.05), "charcoal", bevel=0.1); BX((0, 0, 0.72), (1.72, 0.77, 0.3), "lgrey", bevel=0.03)
    Cy(0.4, 0.3, (0, -0.48, 0.68), "dkgrey", (R90, 0, 0), verts=32); Cy(0.3, 0.32, (0, -0.5, 0.68), "black", (R90, 0, 0), verts=32); S(0.24, (0, -0.6, 0.68), (1, 0.35, 1), "glass"); S(0.06, (-0.08, -0.68, 0.76), (1, 0.4, 1), "white")
    BX((-0.5, 0, 1.33), (0.4, 0.3, 0.16), "red", bevel=0.04); BX((0.2, 0, 1.36), (0.6, 0.5, 0.22), "dkgrey", bevel=0.05)
    fl = BX((0.55, -0.39, 1.05), (0.4, 0.05, 0.22), "white", bevel=0.02); gm = mat((1.0, 0.95, 0.7), 0.3, 1.2); fl.data.materials[0] = gm
    eyes(1.08, -0.39, 0.0, 0.0) if False else None
    for sx in (-1, 1):
        pass
    face(1.05, -0.39, 0.16, 0.085, x=-0.5, mouth_dz=0.0, mr=0.01, tongue=False); smile(0.24, -0.39, 0.09, x=-0.5); return {"glow": [gm]}
def b_canoe():
    S(1.0, (0, 0, 0.38), (1.5, 0.48, 0.42), "rust"); S(0.9, (0, 0, 0.52), (1.5, 0.42, 0.22), "dkbrown")
    for x in (-0.55, 0.55): BX((x, 0, 0.62), (0.16, 0.75, 0.05), "wood", bevel=0.02)
    To(0.0, 0.0, (0, 0, 0), "rust") if False else None
    for (x, r) in [(-0.2, 62), (0.3, 118)]:
        RC(0.035, 1.5, (x, -0.25, 0.95), "wood", (0, rad(r - 90), 0), lv=1)
    S(0.2, (-0.85, -0.25, 1.28), (0.6, 0.3, 1.3), "wood", rot=(0, rad(-28), 0)); S(0.2, (0.95, -0.25, 1.26), (0.6, 0.3, 1.3), "wood", rot=(0, rad(28), 0))
    sface(0.36, 0.22, 0.11, mouth_dz=0.2, mr=0.09); return {}
def b_celery():
    for (x, y, hh, t) in [(-0.3, 0.05, 1.5, -6), (0, -0.05, 1.7, 0), (0.3, 0.05, 1.45, 6)]:
        RC(0.17, hh, (x, y, hh/2 + 0.05), "lgreen", (0, rad(t), 0), lv=1)
        for k in range(3): Cy(0.012, hh*0.8, (x - 0.08 + 0.08*k + t*0.004, y - 0.165, hh/2), "green", (0, rad(t), 0), verts=6)
        tx = x + math.sin(rad(t))*hh*0.55
        for (dx, dz, r) in [(0, 0.15, 0.24), (-0.2, 0.0, 0.18), (0.2, 0.02, 0.18)]: S(r, (tx + dx, y, hh + dz), (1, 0.7, 1), "green")
    RC(0.36, 0.2, (0, 0, 0.12), (0.85, 0.92, 0.7), lv=1); sface(0.8, 0.14, 0.085, mouth_dz=0.22, mr=0.07); return {}
def b_chair():
    BX((0, 0, 0.85), (1.2, 1.1, 0.14), "wood", bevel=0.04)
    for (x, y) in [(-0.5, -0.45), (0.5, -0.45), (-0.5, 0.45), (0.5, 0.45)]: BX((x, y, 0.4), (0.13, 0.13, 0.8), "brown", bevel=0.03)
    for sx in (-1, 1): BX((sx*0.5, 0.48, 1.45), (0.13, 0.13, 1.2), "brown", bevel=0.03)
    BX((0, 0.48, 1.6), (1.0, 0.1, 0.6), "wood", bevel=0.04); BX((0, 0.48, 2.0), (1.15, 0.14, 0.14), "brown", bevel=0.04)
    BX((0, -0.02, 0.95), (1.0, 0.9, 0.1), "red", bevel=0.05)
    face(1.68, 0.42, 0.2, 0.1, mouth_dz=0.26, mr=0.09); return {}
def b_cheese():
    o = Fp([(-1.1, 0), (1.1, 0), (1.1, 0.95), (-1.1, 0.45)], (0, 0, 0.02), 1.1, "yellow"); bm = o.modifiers.new("Bevel", 'BEVEL'); bm.width = 0.06; bm.segments = 3
    for (x, z, r) in [(-0.7, 0.22, 0.12), (0.75, 0.25, 0.14), (0.15, 0.18, 0.09), (0.8, 0.68, 0.1)]: S(r, (x, -0.55, z), (1, 0.3, 1), "gold")
    for (x, y, r) in [(-0.4, 0.1, 0.13), (0.4, -0.15, 0.1), (0.7, 0.25, 0.12)]: S(r, (x, y, 0.47 + (x + 1.1)*0.227 + 0.01), (1, 1, 0.3), "gold", rot=(0, rad(-12.8), 0))
    face(0.52, -0.56, 0.2, 0.1, x=0.15, mouth_dz=0.24, mr=0.09); return {}
def b_chick():
    S(0.55, (0, 0.05, 0.75), (1, 1.1, 0.95), "yellow"); S(0.42, (0, -0.25, 1.35), (1, 1, 1), "yellow"); Co(0.1, 0.22, (0, -0.72, 1.3), "orange", (R90, 0, 0))
    for sx in (-1, 1): S(0.22, (sx*0.52, 0.1, 0.8), (0.4, 1, 0.8), "gold", rot=(0, rad(sx*-15), 0))
    for k in range(3): S(0.07, (0.06*(k-1), -0.2, 1.8), (0.6, 0.6, 1.5), "yellow", rot=(0, rad((k-1)*25), 0))
    S(0.14, (0, 0.6, 0.85), (0.6, 1, 1.2), "gold", rot=(rad(-40), 0, 0))
    legs2("orange", 0, 0.3, 0.035, 0.18, foot="orange"); eyes(1.45, -0.6, 0.17, 0.09); return {}
def b_circle():
    Cy(0.9, 0.3, (0, 0, 0.95), "blue", (R90, 0, 0), verts=64); Cy(0.68, 0.34, (0, 0, 0.95), "sky", (R90, 0, 0), verts=64)
    face(1.05, -0.18, 0.22, 0.12, mouth_dz=0.32, mr=0.11); return {}
def b_coach():
    person("red", "navy", "hairb", shoes="white", sleeves="red")
    S(0.45, (0, 0.04, 1.52), (1, 1, 0.8), "blue"); BX((0, -0.42, 1.6), (0.5, 0.35, 0.05), "blue", bevel=0.02, rot=(rad(12), 0, 0)); S(0.05, (0, 0.04, 1.89), (1, 1, 0.6), "white")
    for sx in (-1, 1): BX((sx*0.39, -0.02, 0.75), (0.04, 0.5, 0.6), "white", bevel=0.01)
    To(0.22, 0.015, (0, -0.1, 1.05), "black", (rad(50), 0, 0)); S(0.07, (0, -0.36, 0.86), (1.3, 0.8, 1), "silver")
    BX((0.62, -0.2, 0.62), (0.34, 0.05, 0.44), "wood", bevel=0.02); BX((0.62, -0.23, 0.6), (0.27, 0.02, 0.33), "white", bevel=0.01); return {}
def b_crayon():
    Cy(0.25, 1.5, (0, 0, 0.8), "red", verts=32); Co(0.25, 0.45, (0, 0, 1.77), "red", r2=0.07, verts=32); S(0.07, (0, 0, 2.0), (1, 1, 0.8), "red"); Cy(0.265, 0.9, (0, 0, 0.75), (1.0, 0.45, 0.45), verts=32)
    for z in (0.42, 1.08): To(0.265, 0.02, (0, 0, z), "black");
    for k in range(7): a = k*TAU/7; S(0.035, (0.27*math.cos(a), 0.27*math.sin(a), 1.08 - 0.06 - 0.03*(k % 2)), (1, 1, 1), "black")
    sface(0.82, 0.11, 0.07, mouth_dz=0.2, mr=0.06); return {}
def b_desert():
    BX((0, 0, 0.1), (2.6, 2.2, 0.2), "sand", bevel=0.08); S(0.7, (-0.45, 0.45, 0.15), (1.2, 1, 0.45), "straw"); S(0.7, (0.75, 0.6, 0.15), (1.2, 1, 0.45), "sand")
    RC(0.24, 1.3, (0.1, -0.1, 0.85), "green", lv=2)
    for sx, z, hh in [(-1, 0.85, 0.5), (1, 1.05, 0.45)]: RC(0.12, 0.45, (0.1 + sx*0.4, -0.1, z), "green", (0, R90, 0), lv=1); RC(0.12, hh, (0.1 + sx*0.55, -0.1, z + hh/2), "green", lv=2)
    S(0.09, (0.1, -0.1, 1.58), (1, 1, 0.7), "hotpink")
    for (x, y, r) in [(-1.0, -0.7, 0.16), (0.95, -0.75, 0.2), (1.1, -0.45, 0.11)]: S(r, (x, y, 0.2 + r*0.5), (1.2, 1, 0.7), "rust")
    S(0.28, (-0.9, -0.2, 0.4), (1, 1, 0.9), "lgreen"); S(0.06, (-0.9, -0.2, 0.68), (1, 1, 1), "yellow")
    sface(1.0, 0.1, 0.075, x=0.1, mouth_dz=0.2, mr=0.07); fit(); return {}
def b_doctor():
    person("white", "aqua", "hairb", skin="skin2", shoes="white")
    BX((0, -0.3, 0.9), (0.2, 0.04, 0.4), "aqua", bevel=0.01); To(0.24, 0.022, (0, -0.08, 1.05), "charcoal", (rad(55), 0, 0)); Cy(0.015, 0.3, (0.12, -0.34, 0.8), "charcoal", verts=6); S(0.07, (0.12, -0.36, 0.63), (1, 0.4, 1), "silver")
    BX((-0.2, -0.31, 0.62), (0.16, 0.03, 0.14), "white", bevel=0.01); To(0.44, 0.02, (0, 0, 1.6), "lgrey", (rad(-12), 0, 0)); Cy(0.13, 0.03, (0, -0.4, 1.7), "silver", (rad(78), 0, 0)); return {}
def b_dollar():
    G = (0.45, 0.72, 0.42)
    BX((0, 0, 1.0), (2.1, 0.1, 1.05), G, bevel=0.04); BX((0, -0.01, 1.0), (1.9, 0.1, 0.85), (0.72, 0.88, 0.66), bevel=0.02); S(0.38, (0, -0.04, 1.0), (1.1, 0.12, 1.1), G)
    for sx in (-1, 1):
        for sz in (-1, 1): S(0.1, (sx*0.78, -0.05, 1.0 + sz*0.28), (1, 0.3, 1), G)
    face(1.06, -0.085, 0.14, 0.08, mouth_dz=0.2, mr=0.07); return {}
def b_eraser():
    o = Fp([(-0.95, 0), (0.75, 0), (1.0, 0.7), (-0.7, 0.7)], (0, 0, 0.02), 0.7, "pink"); bm = o.modifiers.new("Bevel", 'BEVEL'); bm.width = 0.06; bm.segments = 3
    Fp([(-0.25, -0.01), (0.8, -0.01), (1.05, 0.71), (0.0, 0.71)], (0, 0, 0.02), 0.74, "blue"); Fp([(0.1, 0.25), (0.55, 0.25), (0.62, 0.45), (0.17, 0.45)], (0, -0.36, 0.02), 0.04, "white")
    face(0.45, -0.36, 0.14, 0.085, x=-0.5, mouth_dz=0.2, mr=0.07); return {}
def b_family():
    def kid(): person("yellow", "blue", "ginger", shoes="red"); S(0.07, (0.3, -0.1, 1.85), (1, 1, 1), "ginger")
    placed(lambda: person("blue", "navy", "hairb"), (-0.72, 0.15, 0), 1.0); placed(lambda: (person("hotpink", "hotpink", "brown", style="long", shoes="red"), RK(0.58, 0.55, (0, 0, 0.5), "hotpink", lv=2, r2=0.3)), (0.72, 0.15, 0), 0.95)
    placed(kid, (0, -0.3, 0), 0.68); fit(2.0, 2.6); return {}
def b_farmer():
    person("red", "blue", "ginger", shoes="dkbrown")
    BX((0, -0.3, 0.72), (0.5, 0.06, 0.5), "blue", bevel=0.03)
    for sx in (-1, 1): BX((sx*0.2, -0.26, 1.02), (0.08, 0.1, 0.3), "blue", bevel=0.02); S(0.04, (sx*0.2, -0.34, 0.93), (1, 0.5, 1), "gold")
    Cy(0.7, 0.05, (0, 0.02, 1.72), "straw", (rad(-6), 0, 0), verts=32); RC(0.36, 0.3, (0, 0.04, 1.86), "straw", lv=1); To(0.38, 0.03, (0, 0.03, 1.78), "red", (rad(-6), 0, 0))
    RC(0.03, 1.5, (0.62, -0.12, 0.85), "wood", lv=1); BX((0.62, -0.12, 1.6), (0.36, 0.04, 0.05), "dkgrey", bevel=0.01)
    for k in (-1, 0, 1): RC(0.02, 0.32, (0.62 + k*0.15, -0.12, 1.78), "dkgrey", lv=1)
    return {}
def b_field():
    BX((0, 0, 0.1), (2.6, 2.2, 0.2), "grass", bevel=0.08)
    for r in range(4):
        y = 0.75 - 0.42*r; BX((-0.3, y, 0.21), (1.9, 0.26, 0.04), "brown", bevel=0.02)
        for k in range(7): x = -1.1 + 0.27*k; RC(0.02, 0.4, (x, y, 0.42), "lgreen", lv=1); S(0.07, (x, y, 0.68), (0.8, 0.8, 1.7), "gold")
    for k in range(4): BX((1.15, -0.85 + 0.55*k, 0.42), (0.08, 0.08, 0.45), "wood", bevel=0.02)
    for z in (0.38, 0.56): BX((1.15, 0, z), (0.05, 1.9, 0.06), "wood", bevel=0.01)
    RC(0.34, 0.6, (0.3, -0.75, 0.55), "straw", (0, R90, 0), lv=1)
    for sx in (-1, 1): To(0.345, 0.02, (0.3 + sx*0.15, -0.75, 0.55), "wood", (0, R90, 0))
    sface(0.6, 0.13, 0.085, x=0.3, mouth_dz=0.2, mr=0.07); fit(1.5, 2.5); return {}
def b_finger():
    RB((0, 0, 0.75), (1.25, 0.75, 1.0), "peach", lv=2)                                   # fist
    for k in range(3): S(0.2, (0.02 + 0.3*k, -0.3, 1.2 - 0.03*k), (1, 1, 0.9), "peach"); RC(0.15, 0.4, (0.02 + 0.3*k, -0.36, 0.98 - 0.03*k), "peach", lv=2)
    RC(0.17, 0.75, (0.15, -0.42, 0.6), "peach", (0, rad(72), 0), lv=2); S(0.12, (-0.2, -0.52, 0.72), (1, 0.4, 0.8), "pink")
    RC(0.23, 1.25, (-0.38, -0.05, 1.75), "peach", lv=2); S(0.17, (-0.38, -0.25, 2.2), (1, 0.3, 1.15), "pink")     # index finger pointing up
    for z in (1.55, 1.9): To(0.235, 0.012, (-0.38, -0.05, z), (0.9, 0.62, 0.5))
    RC(0.5, 0.35, (0, 0, 0.2), "blue", lv=1); To(0.56, 0.04, (0, 0, 0.36), "white")
    sface(0.72, 0.0, 0.0) if False else None
    face(0.86, surf_y(0.3, 0.86, -0.4) - 0.0, 0.17, 0.095, x=0.32, mouth_dz=0.0, mr=0.01, tongue=False); smile(0.42, surf_y(0.3, 0.42, -0.4) - 0.015, 0.09, x=0.32); return {}
def arch(R, r, loc, c, rotz=0.0, zs=1.0, parent=None):
    """half torus standing up (an arch) in the XZ plane, feet at loc.z"""
    import bmesh
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, major_segments=32, minor_segments=12)
    o = bpy.context.active_object; bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y < -0.001], context='VERTS'); bm.to_mesh(o.data); bm.free()
    o.scale = (1, zs, 1); return _fin(o, c, parent, (R90, 0, rotz), "Arch")
def dome(r, loc, c, zs=1.0, parent=None):
    import bmesh
    o = S(r, loc, (1, 1, zs), c, parent); bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.001], context='VERTS'); bm.to_mesh(o.data); bm.free(); return o
def b_forest():
    BX((0, 0, 0.1), (2.6, 2.2, 0.2), "grass", bevel=0.08)
    def pine(x, y, sc, c="dkgreen"):
        RC(0.08*sc, 0.5*sc, (x, y, 0.2 + 0.25*sc), "brown", lv=1)
        for k in range(3): Co((0.5 - 0.11*k)*sc, 0.6*sc, (x, y, 0.2 + (0.65 + 0.38*k)*sc), c, verts=16)
    pine(-0.8, 0.5, 1.3); pine(0.75, 0.6, 1.1, "green"); pine(0.0, 0.75, 1.6, (0.2, 0.55, 0.3)); pine(-1.0, -0.4, 0.8, "green"); pine(1.0, -0.2, 0.9)
    tree_s(0.1, -0.3, 1.5, "green")
    for (x, y, c) in [(-0.45, -0.8, "red"), (0.7, -0.85, "red")]: RC(0.04, 0.14, (x, y, 0.27), "cream", lv=1); S(0.1, (x, y, 0.38), (1, 1, 0.6), c)
    sface(1.5, 0.19, 0.105, x=0.1, mouth_dz=0.26, mr=0.1); fit(); return {}
def b_fruit():
    Cy(1.0, 0.08, (0, 0, 0.06), "white", verts=48); To(0.95, 0.05, (0, 0, 0.1), "sky")
    S(0.55, (-0.1, -0.1, 0.65), (1, 1, 0.92), "red"); RC(0.03, 0.2, (-0.1, -0.1, 1.2), "brown", lv=1); S(0.12, (0.03, -0.1, 1.25), (1.5, 0.6, 0.4), "green")
    S(0.42, (0.62, 0.2, 0.52), (1, 1, 1), "orange"); S(0.05, (0.62, 0.2, 0.94), (1, 1, 0.5), "green")
    for k in range(7): a = k*0.9; S(0.15, (-0.65 + 0.14*math.cos(a), 0.35 + 0.14*math.sin(a), 0.25 + 0.09*k), (1, 1, 1), "purple")
    for k in range(6): a = rad(-50 + 20*k); S(0.14, (-0.75 - 0.05 + 0.75*math.cos(a)*0.0 + 0.0, -0.55, 0.0) , (1, 1, 1), "yellow") if False else S(0.15, (0.25 + 0.55*math.sin(a), -0.72, 0.2 + 0.25*(1 - math.cos(a))), (1.3, 1, 1), "yellow")
    sface(0.72, 0.18, 0.1, x=-0.1, mouth_dz=0.26, mr=0.09); return {}
def b_glove():
    RB((0, 0, 0.95), (1.2, 0.45, 1.0), "blue", lv=2)
    for (x, hh, z) in [(-0.42, 0.6, 1.6), (-0.14, 0.78, 1.7), (0.14, 0.72, 1.67), (0.42, 0.55, 1.58)]: RC(0.14, hh, (x, 0, z), "blue", lv=2)
    RC(0.15, 0.6, (-0.75, -0.05, 1.0), "blue", (0, rad(-35), 0), lv=2); RC(0.42, 0.4, (0, 0, 0.3), "red", lv=1)
    for z in (0.18, 0.3, 0.42): To(0.47, 0.03, (0, 0, z), "roof")
    face(1.05, -0.24, 0.2, 0.11, mouth_dz=0.3, mr=0.1); return {}
def b_goose(): h = bird("white", None, "orange", s=1.3, legh=0.45, neck=0.55, beak_len=0.32, beak_r=0.1); return {}
def b_heron(): return bird((0.62, 0.7, 0.8), "white", "yellow", s=1.05, legh=1.0, legc="dkgrey", neck=0.6, beak_len=0.7, beak_r=0.06, crest="navy", wl=0.75)
def b_hotdog():
    for sy in (-1, 1): RC(0.3, 1.9, (0, sy*0.24, 0.42), "tan", (0, R90, 0), lv=2)
    RC(0.24, 2.3, (0, 0, 0.68), "rust", (0, R90, 0), lv=2)
    for k in range(13): S(0.07, (-0.9 + 0.15*k, 0.09*(1 if k % 2 else -1), 0.93), (1.3, 1, 0.7), "yellow")
    sface(0.44, 0.2, 0.1, mouth_dz=0.2, mr=0.08); return {}
def b_igloo():
    dome(1.0, (0, 0.15, 0), "white", 0.95); RC(0.42, 0.7, (0, -0.85, 0.36), "white", (R90, 0, 0), lv=1); Cy(0.3, 0.05, (0, -1.24, 0.34), "navy", (R90, 0, 0), verts=24); pass
    for z, r in [(0.3, 0.955), (0.6, 0.8), (0.82, 0.55)]: To(r, 0.012, (0, 0.15, z), "sky")
    for k in range(10): a = k*TAU/10; Cy(0.012, 0.32, (0.9*math.cos(a), 0.15 + 0.9*math.sin(a), 0.15), "sky", verts=6)
    for k in range(8): a = k*TAU/8 + 0.3; Cy(0.012, 0.3, (0.72*math.cos(a), 0.15 + 0.72*math.sin(a), 0.72), "sky", (rad(40*math.sin(a)), rad(-40*math.cos(a)), 0), verts=6)
    BX((0, -0.1, 0.02), (2.3, 2.6, 0.04), (0.9, 0.95, 1.0), bevel=0.01)
    sface(0.82, 0.2, 0.1, mouth_dz=0.0, mr=0.01, tongue=False); fit(1.25, 2.4); return {}
def b_iguana():
    lizard("green", "lgreen", None, tail=(0.4, 1.9, 0.2), hr=0.38)
    for k in range(9): y = -0.55 + 0.26*k; Co(0.07, 0.24 - 0.012*k, (0.0 + max(0, y - 0.6)*0.38, y, (0.86 if y < 0.6 else 0.86 - (y - 0.6)*0.36)), "dkgreen", verts=8)
    S(0.16, (0, -0.8, 0.25), (0.5, 1, 1), "lime"); return {}
def b_insect():
    S(0.34, (0, -0.55, 1.0), (1, 1, 1), "purple"); S(0.36, (0, -0.05, 0.95), (1, 1.1, 0.95), "violet"); S(0.3, (0, 0.6, 0.9), (0.9, 1.6, 0.85), "purple")
    for k in range(3): To(0.27 - 0.03*k, 0.03, (0, 0.4 + 0.25*k, 0.9), "yellow", (R90, 0, 0))
    for sx in (-1, 1):
        RC(0.02, 0.4, (sx*0.14, -0.75, 1.4), "charcoal", (rad(25), rad(sx*20), 0), lv=1); S(0.05, (sx*0.2, -0.84, 1.6), (1, 1, 1), "charcoal")
        for k in range(3): RC(0.025, 0.6, (sx*0.36, -0.25 + 0.25*k, 0.55), "charcoal", (0, rad(sx*-35), 0), lv=1)
    eyes(1.08, -0.84, 0.14, 0.09); smile(0.88, -0.87, 0.07, tongue=False)
    w = wingpair(-0.05, 1.2, "sky", 0.75, "oval", 0.25); return {"wings": w, "flap": 40}
def b_jaguar():
    h = quad_meta("gold", "cream", "cream", (0.75, 0.5, 0.1), ear="round", tail="long", snout_len=0.06)
    for (x, y) in [(-0.3, 0.0), (0.3, 0.15), (0.0, 0.35), (-0.3, 0.6), (0.3, 0.7), (0.0, -0.2), (0.5, -0.1), (-0.5, 0.3), (0.52, 0.45), (-0.55, -0.05), (-0.6, 0.6), (0.6, 0.75), (0.0, 0.75), (-0.62, -0.4), (0.62, -0.4)]:
        bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); hit, loc, nrm, idx, ob, mw = scene.ray_cast(dg, Vector((x*1.6, y, 3.0)), Vector((-x*0.5, 0, -1)).normalized())
        if hit: S(0.1, tuple(loc), (1, 1, 0.3), "dkbrown", rot=tuple(nrm.to_track_quat('Z', 'Y').to_euler()))
    return h
def b_juice():
    BX((0, 0, 0.75), (1.0, 0.7, 1.4), "orange", bevel=0.06); BX((0, 0, 1.4), (1.02, 0.72, 0.16), "white", bevel=0.04); BX((0, -0.01, 0.3), (1.02, 0.7, 0.3), "green", bevel=0.04)
    RC(0.04, 0.8, (0.25, 0.1, 1.75), "red", (0, rad(12), 0), lv=1); RC(0.04, 0.3, (0.45, 0.1, 2.12), "red", (0, rad(75), 0), lv=1)
    Cy(0.2, 0.03, (-0.2, -0.36, 0.55), (1.0, 0.7, 0.2), (R90, 0, 0), verts=24); Cy(0.16, 0.035, (-0.2, -0.365, 0.55), "yellow", (R90, 0, 0), verts=24); S(0.12, (0.25, -0.36, 0.5), (1, 0.3, 1.2), "sky")
    face(1.05, -0.36, 0.2, 0.1, mouth_dz=0.24, mr=0.09); return {}
def b_kitten(): return quad_meta("orange", "cream", "white", (0.8, 0.4, 0.1), ear="point", tail="long", size=0.8, stripes=True)
def b_marker():
    Cy(0.3, 1.3, (0, 0, 0.7), "white", verts=32); Cy(0.305, 0.5, (0, 0, 0.75), "blue", verts=32); Cy(0.32, 0.5, (0, 0, 1.55), "blue", verts=32); RC(0.2, 0.2, (0, 0, 1.85), "blue", lv=1); BX((0.3, 0, 1.55), (0.06, 0.12, 0.45), "navy", bevel=0.02)
    Cy(0.31, 0.06, (0, 0, 0.06), "blue", verts=32); sface(1.2, 0.12, 0.075, mouth_dz=0.0, mr=0.01, tongue=False); smile(0.75, -0.32, 0.08); return {}
def b_museum():
    base(2.5, 1.9, "lgrey"); BX((0, 0.15, 0.8), (2.1, 1.2, 1.2), "sand"); BX((0, 0.1, 1.43), (2.3, 1.45, 0.12), "stone"); dome(0.55, (0, 0.15, 1.49), "aqua", 0.9); S(0.07, (0, 0.15, 2.02), (1, 1, 1.5), "gold")
    for x in (-0.9, -0.62, 0.62, 0.9): Cy(0.08, 1.16, (x, -0.52, 0.79), "white", verts=16)
    for k in range(3): BX((0, -0.72 - 0.12*k, 0.32 - 0.06*k), (2.0 + 0.1*k, 0.14, 0.06), "stone", bevel=0.01)
    for sx, c in ((-1, "red"), (1, "blue")): BX((sx*0.76, -0.47, 0.85), (0.14, 0.03, 0.75), c, bevel=0.01)
    face(0.95, -0.46, 0.2, 0.11, mouth_dz=0.3, mr=0.1); fit(); return {}
def b_nickel(): coin((0.7, 0.71, 0.75), 0.85, 0.3, "grey", "5¢", (0.12, 0.13, 0.2)); return {}
def b_nurse():
    person("sky", "sky", "blonde", style="bun", shoes="white")
    BX((0, -0.31, 0.72), (0.5, 0.04, 0.55), "white", bevel=0.03); BX((0, -0.335, 0.8), (0.16, 0.02, 0.05), "red", bevel=0.0); BX((0, -0.335, 0.8), (0.05, 0.02, 0.16), "red", bevel=0.0)
    BX((0, -0.2, 1.8), (0.55, 0.3, 0.22), "white", bevel=0.05); BX((0, -0.36, 1.8), (0.14, 0.02, 0.045), "red", bevel=0.0); BX((0, -0.36, 1.8), (0.045, 0.02, 0.14), "red", bevel=0.0)
    BX((0.62, -0.2, 0.62), (0.34, 0.05, 0.44), "wood", bevel=0.02); BX((0.62, -0.23, 0.6), (0.27, 0.02, 0.33), "white", bevel=0.01); return {}
def b_olive():
    S(0.6, (0, 0, 0.8), (1, 1, 1.2), (0.45, 0.55, 0.15)); S(0.2, (0, 0, 1.48), (1, 1, 0.5), "red"); RC(0.025, 2.2, (0, 0, 0.9), "wood", (0, rad(35), 0), lv=1)
    sface(0.9, 0.2, 0.11, mouth_dz=0.28, mr=0.1); return {}
def b_otter():
    Bc = (0.45, 0.3, 0.2); L = (0.85, 0.75, 0.6)
    S(1.0, (0.15, 0, 0.1), (2.0, 1.15, 0.1), "water"); To(1.25, 0.03, (0.15, 0, 0.18), "white", scale=(1.45, 0.85, 1)); To(0.8, 0.025, (0.15, 0, 0.19), "sky", scale=(1.45, 0.85, 1))
    EL = chain((-0.55, 0, 0.5), (0.95, 0, 0.42), 0.4, 0.3, 6) + [((-1.05, 0, 0.72), 0.4, None)] + chain((1.0, 0, 0.4), (1.9, 0, 0.3), 0.24, 0.12, 4)
    metachar(EL, [], [Bc, L], lambda cc, n: 1 if (n.z > 0.55 and -0.75 < cc.x < 0.8 and abs(cc.y) < 0.28) else 0, res=0.06)
    S(0.3, (1.75, 0, 0.3), (1.5, 0.75, 0.3), Bc)                                           # flat tail
    S(0.24, (-1.12, -0.3, 0.66), (1, 0.8, 0.8), L); S(0.07, (-1.15, -0.5, 0.74), (1.2, 0.8, 0.8), "black")
    for sx in (-1, 1): S(0.1, (-1.05 + sx*0.26, 0.05, 1.08), (1, 0.6, 1), Bc)
    for sy in (-1, 1):
        for k in range(3): Cy(0.01, 0.42, (-1.12 + sy*0.26, -0.42, 0.6 + 0.05*k), "white", (0, rad(sy*78 + k*7), 0), verts=6)
    S(0.24, (-0.15, 0, 0.98), (1.05, 0.9, 0.35), (1.0, 0.82, 0.8))                          # shell on the tummy
    for k in range(5): a = rad(-50 + 25*k); RC(0.02, 0.4, (-0.15 + 0.12*math.sin(a), -0.1, 1.05), (1.0, 0.62, 0.6), (R90, 0, a), lv=1)
    for sy in (-1, 1): RC(0.09, 0.45, (-0.3, sy*0.3, 0.82), Bc, (rad(sy*55), 0, 0), lv=1); S(0.11, (-0.25, sy*0.16, 0.98), (1, 1, 0.8), Bc)
    for sy in (-1, 1): S(0.16, (1.0, sy*0.22, 0.72), (0.7, 1, 1.2), Bc)
    eyes(0.86, -0.38, 0.0, 0.0) if False else None
    sface(0.9, 0.15, 0.085, x=-1.08, mouth_dz=0.0, mr=0.01, tongue=False, fb=-0.4); smile(0.56, -0.5, 0.07, x=-1.12, tongue=False); return {}
def b_penny(): coin((0.82, 0.47, 0.25), 0.75, 0.14, (0.66, 0.34, 0.16), "1¢", (0.3, 0.12, 0.04)); return {}
def b_pepper():
    for k in range(4): a = k*TAU/4 + 0.4; S(0.5, (0.28*math.cos(a), 0.28*math.sin(a), 0.75), (1, 1, 1.35), "red")
    S(0.45, (0, 0, 0.9), (1, 1, 1.2), "red"); RC(0.07, 0.4, (0, 0, 1.6), "green", (0, rad(12), 0), lv=1); S(0.22, (0, 0, 1.42), (1, 1, 0.4), "green")
    sface(0.85, 0.2, 0.11, mouth_dz=0.28, mr=0.1); return {}
def b_pilot():
    person("navy", "navy", "hairb", shoes="black")
    S(0.45, (0, 0.03, 1.55), (1, 1, 0.6), "navy"); BX((0, -0.4, 1.6), (0.56, 0.3, 0.05), "black", bevel=0.02, rot=(rad(14), 0, 0)); Cy(0.46, 0.1, (0, 0.03, 1.8), "navy", verts=32); S(0.07, (0, -0.4, 1.72), (1.3, 0.5, 1), "gold")
    RK(0.06, 0.3, (0, -0.33, 0.85), "black", (math.pi, 0, 0), lv=1); BX((0, -0.3, 1.0), (0.3, 0.05, 0.1), "white", bevel=0.02)
    for sx in (-1, 1): To(0.09, 0.02, (sx*0.5, -0.07, 0.6), "gold", (0, rad(sx*15), 0)); S(0.05, (-0.2 + sx*0.07, -0.33, 0.9), (1.4, 0.4, 0.7), "gold")
    for sx in (-1, 1): BX((sx*0.36, 0, 1.08), (0.2, 0.3, 0.05), "gold", bevel=0.02)
    return {}
def b_puppy():
    h = quad_meta("tan", "cream", "cream", "brown", ear="floppy", tail="short", size=0.8)
    S(0.2, (0.2, -0.75, 1.3), (1, 0.6, 1), "brown"); To(0.3, 0.05, (0, -0.4, 0.92), "red", (rad(60), 0, 0)); S(0.07, (0, -0.62, 0.74), (1, 1, 1), "gold"); return h
def b_quail():
    h = bird("brown", "tan", "dkgrey", s=1.05, legh=0.28, legc="dkgrey", beak_len=0.16, beak_r=0.07)
    RC(0.03, 0.3, (0, -0.5, 1.3), "charcoal", (rad(35), 0, 0), lv=1); S(0.08, (0, -0.62, 1.42), (0.7, 1.3, 1), "charcoal")
    for k in range(5): S(0.05, (-0.28, -0.2 + 0.14*k, 0.72 + 0.04*(k % 2)), (1, 1, 1), "cream"); S(0.05, (0.28, -0.2 + 0.14*k, 0.72 + 0.04*(k % 2)), (1, 1, 1), "cream")
    return {}
def b_queen():
    person("purple", "purple", "blonde", style="long", shoes="gold"); RK(0.68, 0.75, (0, 0, 0.42), "purple", lv=2, r2=0.3)
    S(0.6, (0, 0.28, 0.75), (1.05, 0.5, 1.15), "red"); To(0.3, 0.06, (0, -0.02, 1.08), "white")
    Cy(0.3, 0.2, (0, 0.03, 1.9), "gold", verts=24)
    for k in range(6): a = k*TAU/6; Co(0.08, 0.22, (0.27*math.cos(a), 0.03 + 0.27*math.sin(a), 2.08), "gold", verts=8); S(0.045, (0.31*math.cos(a + 0.5), 0.03 + 0.31*math.sin(a + 0.5), 1.9), (1, 1, 1), "red" if k % 2 else "aqua")
    RC(0.03, 1.1, (0.62, -0.12, 0.9), "gold", lv=1); S(0.11, (0.62, -0.12, 1.5), (1, 1, 1), "hotpink")
    To(0.6, 0.05, (0, 0, 0.12), "white"); return {}
def b_quilt():
    BX((0, 0, 1.0), (2.1, 0.22, 1.6), "white", bevel=0.08)
    cols = ["red", "sky", "yellow", "lgreen", "hotpink", "orange", "lavender", "aqua"]
    for i in range(4):
        for j in range(3): BX((-0.75 + 0.5*i, -0.1, 0.5 + 0.5*j), (0.46, 0.06, 0.46), cols[(i*3 + j*5) % 8], bevel=0.04)
    for (i, j) in [(0, 2), (3, 0), (2, 1)]: S(0.1, (-0.75 + 0.5*i, -0.14, 0.5 + 0.5*j), (1, 0.3, 1), "white")
    face(1.08, -0.14, 0.2, 0.1, x=-0.25, mouth_dz=0.24, mr=0.09); return {}
def b_raisin():
    C = (0.36, 0.16, 0.3); S(0.6, (0, 0, 0.62), (1.1, 0.9, 1.0), C)
    for (x, z, r) in [(-0.45, 0.9, 0.3), (0.45, 0.85, 0.32), (-0.4, 0.35, 0.3), (0.42, 0.33, 0.3), (0, 1.05, 0.3)]: S(r, (x, 0.05, z), (1, 0.9, 1), C)
    for k in range(5): To(0.45, 0.035, (0, 0, 0.3 + 0.16*k), (0.27, 0.1, 0.22), (rad(8*(k % 2) - 4), rad(6*(k % 3) - 6), 0), scale=(1.3, 1.05, 1))
    RC(0.03, 0.2, (0, 0, 1.38), "brown", lv=1); sface(0.72, 0.2, 0.11, mouth_dz=0.28, mr=0.1); return {}
def b_river():
    BX((0, 0, 0.1), (2.6, 2.2, 0.2), "grass", bevel=0.08)
    for k in range(9): t = k/8; S(0.42, (-0.9 + 1.7*t + 0.35*math.sin(t*5), 0.95 - 1.9*t, 0.17), (1.1, 1, 0.22), "water")
    for k in range(4): t = 0.15 + 0.22*k; S(0.1, (-0.9 + 1.7*t + 0.35*math.sin(t*5), 0.95 - 1.9*t, 0.26), (1.6, 0.5, 0.15), "white")
    BX((0.05, 0.0, 0.42), (1.3, 0.4, 0.08), "wood", bevel=0.03, rot=(0, 0, rad(35)))
    for sx in (-1, 1): BX((0.05 + sx*0.5, sx*0.35, 0.3), (0.12, 0.42, 0.2), "brown", bevel=0.02, rot=(0, 0, rad(35)))
    tree_s(-0.95, -0.5, 1.0); tree_s(1.0, 0.65, 0.9, "lgreen"); S(0.32, (0.75, -0.75, 0.42), (1.1, 1, 0.9), "stone")
    sface(0.46, 0.12, 0.075, x=0.75, mouth_dz=0.16, mr=0.06); fit(1.6, 2.5); return {}
def b_sandal():
    RB((0, 0, 0.16), (0.95, 2.0, 0.26), "tan", lv=2); RB((0, 0, 0.3), (0.85, 1.85, 0.06), "wood", lv=2)
    arch(0.44, 0.08, (0, -0.45, 0.26), "red", zs=0.85); arch(0.42, 0.07, (0, 0.4, 0.26), "red", zs=0.9)
    RC(0.05, 0.85, (0, -0.02, 0.62), "red", (R90, 0, 0), lv=1); S(0.1, (0, -0.45, 0.66), (1, 1, 1), "yellow")
    face(0.19, -1.0, 0.2, 0.085, mouth_dz=0.0, mr=0.01, tongue=False); return {}
def b_school():
    base(2.6, 1.9, "grass"); BX((0, 0.2, 0.8), (2.2, 1.1, 1.2), "brick"); Fp([(-1.2, 0), (1.2, 0), (1.0, 0.3), (-1.0, 0.3)], (0, 0.2, 1.4), 1.25, "roof")
    BX((0, 0.1, 1.75), (0.6, 0.6, 1.0), "brick"); Fp([(-0.4, 0), (0.4, 0), (0, 0.4)], (0, 0.1, 2.25), 0.7, "roof"); Cy(0.2, 0.04, (0, -0.21, 1.95), "white", (R90, 0, 0)); S(0.1, (0, 0.1, 1.55), (1, 1, 1), "gold")
    BX((0, -0.36, 0.5), (0.5, 0.05, 0.6), "dkbrown", bevel=0.02)
    for sx in (-1, 1): BX((sx*0.7, -0.36, 0.95), (0.4, 0.05, 0.36), "glass", bevel=0.02)
    Cy(0.02, 1.2, (1.15, -0.6, 0.8), "lgrey", verts=8); Fp([(0, 0), (0.4, 0.1), (0, 0.24)], (1.15, -0.6, 1.15), 0.03, "red")
    face(1.08, -0.35, 0.16, 0.085, mouth_dz=0.0, mr=0.01, tongue=False); fit(); return {}
def b_shell():
    S(0.95, (0, 0, 0.95), (1.05, 0.28, 0.95), (1.0, 0.8, 0.75)); BX((0, 0, 0.12), (0.7, 0.3, 0.2), (1.0, 0.7, 0.65), bevel=0.06)
    for k in range(9): a = rad(-64 + 16*k); RC(0.04, 1.45, (0.72*math.sin(a), -0.22 + abs(math.sin(a))*0.08, 0.2 + 0.72*math.cos(a)), (1.0, 0.62, 0.6), (0, a, 0), lv=1)
    sface(0.75, 0.2, 0.11, mouth_dz=0.28, mr=0.1); return {}
def b_shirt():
    BX((0, 0, 0.9), (1.3, 0.42, 1.55), "sky", bevel=0.12)
    for sx in (-1, 1): BX((sx*0.85, 0, 1.38), (0.75, 0.4, 0.48), "sky", rot=(0, rad(sx*30), 0), bevel=0.1); BX((sx*1.13, 0, 1.22), (0.1, 0.42, 0.5), "blue", rot=(0, rad(sx*30), 0), bevel=0.03)
    To(0.28, 0.07, (0, 0, 1.68), "blue", (rad(15), 0, 0))
    for z in (0.4, 0.62): BX((0, 0, z), (1.32, 0.44, 0.1), "white", bevel=0.02)
    S(0.18, (0.32, -0.21, 0.98), (1, 0.2, 1), "yellow"); face(1.25, -0.22, 0.2, 0.1, x=-0.1, mouth_dz=0.24, mr=0.09); return {}
def b_slide():
    o = Fp([(-1.5, 0.1), (-1.2, 0.04), (0.5, 1.3), (0.5, 1.42), (-1.2, 0.2), (-1.5, 0.25)], (0, 0, 0), 0.6, "red")
    for sy in (-1, 1): Fp([(-1.5, 0.25), (-1.2, 0.2), (0.5, 1.42), (0.5, 1.6), (-1.2, 0.38), (-1.5, 0.4)], (0, sy*0.32, 0), 0.05, "yellow")
    BX((0.8, 0, 1.4), (0.65, 0.7, 0.08), "blue", bevel=0.03)
    for sy in (-1, 1):
        for x in (0.52, 1.08): RC(0.04, 1.4, (x, sy*0.3, 0.7), "blue", lv=1)
        RC(0.03, 0.55, (0.8, sy*0.33, 1.9), "yellow", (0, R90, 0), lv=1); RC(0.03, 0.5, (0.52, sy*0.33, 1.66), "yellow", lv=1); RC(0.03, 0.5, (1.08, sy*0.33, 1.66), "yellow", lv=1)
    for k in range(4): Cy(0.03, 0.6, (1.1, 0, 0.25 + 0.3*k), "lgrey", (R90, 0, 0), verts=8)
    BX((0.8, -0.3, 0.7), (0.5, 0.04, 0.9), "yellow", bevel=0.03); face(0.85, -0.32, 0.14, 0.08, x=0.8, mouth_dz=0.2, mr=0.07); fit(2.0, 2.6); return {}
def ball(c, r=0.8):
    return S(r, (0, 0, r), (1, 1, 1), c, seg=48, ring=24)
def b_soccer():
    ball("white")
    import random; random.seed(2)
    dirs = [Vector((0, 0, 1)), Vector((0, 0, -1))] + [Vector((math.cos(k*TAU/5), math.sin(k*TAU/5), 0.45)).normalized() for k in range(5)] + [Vector((math.cos(k*TAU/5 + 0.63), math.sin(k*TAU/5 + 0.63), -0.45)).normalized() for k in range(5)]
    for d in dirs:
        if d.y < -0.75: continue
        Co(0.27, 0.05, tuple(Vector((0, 0, 0.8)) + d*0.785), "black", tuple(d.to_track_quat('Z', 'Y').to_euler()), r2=0.25, verts=5)
    sface(0.9, 0.2, 0.11, mouth_dz=0.28, mr=0.1); return {}
def b_square():
    cx, cz = shape([(-0.85, 0.05), (0.85, 0.05), (0.85, 1.75), (-0.85, 1.75)], "red", (1.0, 0.45, 0.45)); face(cz + 0.1, -0.19, 0.22, 0.12, x=cx, mouth_dz=0.32, mr=0.11); return {}
def b_steps():
    for k in range(4): BX((0, -0.6 + 0.42*k, 0.21*(k + 1)), (1.7, 0.44, 0.42*(k + 1)), "stone", bevel=0.03); BX((0, -0.6 + 0.42*k - 0.01, 0.42*(k + 1) + 0.005), (0.7, 0.44, 0.03), "red", bevel=0.01); BX((0, -0.6 + 0.42*k - 0.225, 0.42*k + 0.21), (0.7, 0.02, 0.42), "red", bevel=0.0)
    for sx in (-1, 1): BX((sx*0.95, 0.05, 1.1), (0.14, 1.75, 0.1), "brown", bevel=0.03, rot=(rad(45), 0, 0)); BX((sx*0.95, -0.75, 0.5), (0.14, 0.14, 1.0), "brown", bevel=0.03)
    eyes(0.3, -0.83, 0.55, 0.085); smile(0.2, -0.83, 0.08, x=-0.55 + 0.0); return {}
def b_street():
    body = E((0, 0, 0))
    BX((0, 0, 0.12), (2.2, 3.0, 0.24), "grey", body, bevel=0.04); BX((0, 0, 0.26), (1.4, 3.0, 0.04), "dkgrey", body, bevel=0.01)
    for k in range(4): BX((0, -1.0 + 0.7*k, 0.285), (0.1, 0.36, 0.01), "yellow", body, bevel=0.0)
    for k in range(5): BX((-0.52 + 0.26*k, -1.25, 0.285), (0.14, 0.4, 0.01), "white", body, bevel=0.0)
    RC(0.04, 1.5, (0.9, -0.6, 1.0), "dkgrey", parent=body, lv=1); S(0.16, (0.9, -0.6, 1.8), (1, 1, 1), "yellow", body); BX((0.9, -0.6, 1.93), (0.3, 0.3, 0.06), "dkgrey", body, bevel=0.02)
    BX((-0.9, 0.6, 0.55), (0.3, 0.3, 0.6), "red", body, bevel=0.05); S(0.17, (-0.9, 0.6, 0.9), (1, 1, 0.6), "red", body)
    BX((-0.9, -0.5, 0.8), (0.04, 0.04, 1.1), "lgrey", body, bevel=0.0); Cy(0.2, 0.04, (-0.9, -0.53, 1.35), "red", (R90, 0, 0), body, verts=8)
    face(0.2, -1.5, 0.3, 0.085, parent=body, mouth_dz=0.0, mr=0.01, tongue=False); return {"body": body}
def b_stripe():
    for k in range(8): Cy(0.36, 0.2, (0, 0.3, 0.75 + 0.2*k), "red" if k % 2 else "white", verts=32)
    RC(0.37, 0.25, (0, 0.3, 2.35), "red", lv=1); S(0.42, (0, 0.2, 0.45), (1, 1.2, 1), "white")
    for k in range(5): S(0.4 - 0.012*k, (0, -0.05 - 0.2*k, 0.4 - 0.01*k), (1, 0.35, 0.95), "red" if k % 2 == 0 else "white")
    S(0.36, (0, -1.0, 0.36), (1, 0.8, 0.95), "red"); sface(1.5, 0.15, 0.09, mouth_dz=0.24, mr=0.08, fb=0.0); return {}
def b_tennis():
    ball((0.8, 0.92, 0.2))
    for sx in (-1, 1): To(0.62, 0.035, (sx*0.52, 0, 0.8), "white", (0, R90, 0))
    sface(0.9, 0.2, 0.11, mouth_dz=0.28, mr=0.1); return {}
def b_violet():
    RC(0.05, 1.0, (0, 0.1, 0.5), "green", lv=1)
    for sx in (-1, 1): S(0.32, (sx*0.35, 0.05, 0.35), (1.3, 0.5, 0.45), "green", rot=(0, rad(sx*-28), 0))
    for k in range(5): a = k*TAU/5 + R90; S(0.38, (0.42*math.cos(a), -0.05, 1.35 + 0.42*math.sin(a)), (1, 0.3, 1), "violet" if k < 2 else "purple")
    S(0.3, (0, -0.12, 1.35), (1, 0.5, 1), "yellow"); face(1.4, -0.26, 0.11, 0.07, mouth_dz=0.16, mr=0.06); return {}
def b_wagon():
    body = E((0, 0, 0))
    BX((0, 0.1, 0.65), (1.3, 2.1, 0.55), "red", body, bevel=0.08); BX((0, 0.1, 0.9), (1.1, 1.9, 0.08), "roof", body, bevel=0.02)
    ws = wheelset(body, [(sx*0.72, y, 0.32) for sx in (-1, 1) for y in (-0.6, 0.8)], 0.32, 0.16, "black", "white")
    RC(0.04, 1.0, (0, -1.38, 0.82), "black", (rad(55), 0, 0), body, lv=1); RC(0.05, 0.4, (0, -1.8, 1.12), "black", (0, R90, 0), body, lv=1)
    S(0.25, (0.2, 0.3, 1.1), (1, 1, 1), "yellow", body); BX((-0.25, 0.6, 1.1), (0.4, 0.4, 0.4), "blue", body, bevel=0.05)
    face(0.72, -0.96, 0.24, 0.11, parent=body, mouth_dz=0.0, mr=0.01, tongue=False); smile(0.5, -0.97, 0.1, parent=body); return {"body": body, "wheels": ws}
def b_walrus():
    Bc = (0.4, 0.25, 0.17); L = (0.55, 0.38, 0.28)
    EL = [((0, 0.25, 0.62), 0.78, (1.0, 1.25, 0.8)), ((0, -0.3, 1.0), 0.58, None), ((0, -0.55, 1.5), 0.45, None), ((0, 1.0, 0.4), 0.4, (0.8, 1.3, 0.7))]
    metachar(EL, [], [Bc, L], lambda cc, n: 1 if (n.y < -0.35 and cc.z < 1.1 and abs(cc.x) < 0.5) else 0, res=0.065)
    for sx in (-1, 1):
        S(0.4, (sx*0.72, -0.55, 0.12), (1.0, 1.5, 0.28), Bc, rot=(0, 0, rad(sx*-28)))        # front flippers
        S(0.36, (sx*0.4, 1.5, 0.1), (1.0, 1.6, 0.25), Bc, rot=(0, 0, rad(sx*30)))           # rear flippers
        S(0.23, (sx*0.19, -0.98, 1.36), (1, 0.75, 0.85), (0.8, 0.66, 0.52))                 # whisker pads
        RK(0.08, 0.85, (sx*0.17, -1.0, 0.86), "white", (math.pi, 0, 0), lv=1)                # tusks
        for k in range(6): a = rad(-30 + 24*k); Cy(0.012, 0.36, (sx*(0.3 + 0.1*math.cos(a)), -1.12, 1.32 + 0.14*math.sin(a) - 0.05), "white", (0, rad(sx*(70 + 8*k)), 0), verts=6)
    S(0.09, (0, -1.05, 1.52), (1.4, 0.8, 0.8), "black")
    sface(1.7, 0.17, 0.09, mouth_dz=0.0, mr=0.01, tongue=False, fb=-0.9); return {}
def b_zipper():
    for sx in (-1, 1): BX((sx*0.42, 0, 1.0), (0.75, 0.16, 1.9), "blue", bevel=0.05); BX((sx*0.1, -0.02, 1.0), (0.12, 0.16, 1.9), "navy", bevel=0.02)
    for k in range(15): BX((0.05*(1 if k % 2 else -1), -0.08, 0.15 + 0.115*k), (0.16, 0.08, 0.07), "silver", bevel=0.02)
    BX((0, -0.14, 1.15), (0.3, 0.1, 0.3), "lgrey", bevel=0.05); BX((0, -0.2, 0.85), (0.16, 0.04, 0.5), "lgrey", bevel=0.03); To(0.07, 0.025, (0, -0.2, 0.62), "lgrey", (R90, 0, 0))
    face(1.3, -0.085, 0.14, 0.085, x=-0.5, mouth_dz=0.2, mr=0.07); return {}
# ---------------------------------------------------------------- level 4
def bevel(o, w=0.05):
    bm = o.modifiers.new("Bevel", 'BEVEL'); bm.width = w; bm.segments = 3; return o
def b_alligator():
    G = (0.3, 0.55, 0.25)
    EL = [((0, 0.1, 0.42), 0.38, (0.9, 1.8, 0.75)), ((0, -0.8, 0.5), 0.36, (1.0, 1.0, 0.8)), ((0, -1.35, 0.42), 0.26, (0.9, 1.7, 0.6))] + chain((0, 0.7, 0.38), (0.5, 2.0, 0.2), 0.3, 0.09, 7)
    for sx in (-1, 1): EL += [((sx*0.5, -0.3, 0.22), 0.17, None), ((sx*0.68, -0.42, 0.1), 0.14, (1.2, 1.3, 0.6)), ((sx*0.5, 0.6, 0.22), 0.17, None), ((sx*0.68, 0.68, 0.1), 0.14, (1.2, 1.3, 0.6))]
    metachar(EL, [], [G, "lgreen"], lambda cc, n: 1 if (n.z < -0.3 and cc.z < 0.4) else 0, res=0.06)
    for k in range(7): y = -0.3 + 0.3*k; S(0.08, (-0.14, y, 0.72 - max(0, y - 0.6)*0.2), (1, 1, 0.8), "dkgreen"); S(0.08, (0.14 + max(0, y - 0.9)*0.2, y, 0.72 - max(0, y - 0.6)*0.2), (1, 1, 0.8), "dkgreen")
    for sx in (-1, 1):
        for k in range(4): Co(0.035, 0.1, (sx*0.2, -1.2 - 0.15*k, 0.3), "white", (math.pi, 0, 0), verts=6)
        S(0.04, (sx*0.08, -1.82, 0.52), (1, 1, 1), "dkgreen"); S(0.14, (sx*0.19, -0.82, 0.8), (1, 1, 1), G)
    eyes(0.84, -0.9, 0.19, 0.085); return {}
def b_apartment():
    base(1.9, 1.6, "lgrey"); BX((0, 0.1, 1.2), (1.5, 1.0, 2.0), (0.6, 0.7, 0.85)); BX((0, 0.1, 2.24), (1.6, 1.1, 0.1), "stone"); RC(0.2, 0.3, (0.35, 0.2, 2.45), "wood", lv=1)
    for r in range(3):
        for c in range(3):
            if r == 2 and c == 1: continue
            BX((-0.46 + 0.46*c, -0.41, 0.85 + 0.5*r), (0.28, 0.04, 0.3), "glass" if (r + c) % 3 else "yellow", bevel=0.02)
    BX((0, -0.41, 0.42), (0.3, 0.05, 0.44), "dkbrown", bevel=0.02); BX((0, -0.5, 0.68), (0.5, 0.2, 0.05), "red", bevel=0.02)
    face(1.88, -0.4, 0.13, 0.08, mouth_dz=0.0, mr=0.01, tongue=False); smile(1.74, -0.41, 0.06); fit(2.2, 2.2); return {}
def b_aquarium():
    BX((0, 0, 0.8), (2.0, 0.9, 1.3), "water", bevel=0.04); BX((0, 0, 0.12), (2.1, 1.0, 0.24), "charcoal", bevel=0.04); BX((0, 0, 1.5), (2.1, 1.0, 0.14), "charcoal", bevel=0.04)
    BX((0, -0.44, 0.33), (1.9, 0.04, 0.18), "sand", bevel=0.02)
    for (x, hh) in [(-0.8, 0.6), (-0.65, 0.45), (0.85, 0.55)]: RC(0.04, hh, (x, -0.46, 0.3 + hh/2), "green", (0, rad(8), 0), lv=1)
    S(0.2, (-0.3, -0.46, 0.85), (1.3, 0.3, 0.9), "orange"); Fp([(0, 0), (0.25, 0.18), (0.25, -0.18)], (-0.08, -0.46, 0.85), 0.05, "orange"); S(0.03, (-0.42, -0.52, 0.9), (1, 1, 1), "black")
    for (x, z, r) in [(-0.7, 1.1, 0.05), (-0.62, 1.25, 0.035), (0.2, 0.6, 0.04)]: S(r, (x, -0.46, z), (1, 0.4, 1), "white")
    face(1.0, -0.46, 0.17, 0.095, x=0.5, mouth_dz=0.24, mr=0.085); return {}
def b_baseball():
    ball("white")
    for sx in (-1, 1): To(0.62, 0.03, (sx*0.52, 0, 0.8), "red", (0, R90, 0))
    for sx in (-1, 1):
        for k in range(9): a = rad(-60 + 15*k) + math.pi; S(0.035, (sx*(0.52 - 0.62*0.0) - sx*0.0, 0.62*math.cos(a)*1.0, 0.8 + 0.62*math.sin(a)), (1.8, 0.6, 0.6), "red")
    sface(0.9, 0.2, 0.11, mouth_dz=0.28, mr=0.1); return {}
def b_brother():
    person("lgreen", "blue", "ginger", shoes="red")
    S(0.45, (0, 0.05, 1.53), (1, 1, 0.75), "red"); BX((0, 0.45, 1.5), (0.5, 0.3, 0.05), "red", bevel=0.02, rot=(rad(-10), 0, 0))
    BX((0, 0.34, 0.8), (0.6, 0.25, 0.65), "orange", bevel=0.08)
    for sx in (-1, 1): BX((sx*0.28, -0.05, 0.9), (0.08, 0.6, 0.5), "orange", bevel=0.02)
    S(0.2, (0.62, -0.15, 0.3), (1, 1, 1), "white"); S(0.202, (0.62, -0.15, 0.3), (0.3, 1, 1), "red")
    for sx in (-1, 1): S(0.04, (sx*0.24, -0.38, 1.3), (1, 0.4, 1), "ginger")
    return {}
def b_caterpillar():
    for k in range(6):
        x = 0.95 - 0.36*k; z = 0.4 + 0.12*abs(math.sin(k*1.2)); S(0.3, (x, 0.1, z), (1, 1, 1), "lgreen" if k % 2 else "green")
        for sy in (-1, 1): S(0.07, (x, 0.1 + sy*0.2, 0.08), (1, 1, 0.8), "dkgreen")
        S(0.07, (x, 0.1, z + 0.3), (1, 1, 1), "yellow")
    S(0.42, (-1.15, 0.0, 0.62), (1, 1, 1), "green")
    for sx in (-1, 1): RC(0.02, 0.35, (-1.15 + sx*0.14, 0.0, 1.15), "dkgreen", (0, rad(sx*18), 0), lv=1); S(0.06, (-1.15 + sx*0.2, 0.0, 1.33), (1, 1, 1), "hotpink")
    for sx in (-1, 1): S(0.08, (-1.15 + sx*0.3, -0.3, 0.52), (1, 0.4, 0.8), "pink")
    sface(0.7, 0.16, 0.1, x=-1.15, mouth_dz=0.24, mr=0.09); return {}
def b_classroom():
    BX((0, 0, 0.08), (2.4, 2.0, 0.16), "wood", bevel=0.04); BX((0, 0.95, 0.95), (2.4, 0.12, 1.7), "cream", bevel=0.04); BX((1.15, 0, 0.95), (0.12, 2.0, 1.7), "sand", bevel=0.04)
    BX((-0.2, 0.87, 1.15), (1.5, 0.06, 0.8), "brown", bevel=0.03); BX((-0.2, 0.85, 1.15), (1.36, 0.06, 0.66), (0.2, 0.45, 0.3), bevel=0.02); BX((-0.2, 0.8, 0.78), (1.3, 0.1, 0.04), "lgrey", bevel=0.01)
    Cy(0.16, 0.04, (0.85, 0.87, 1.5), "white", (R90, 0, 0));
    for (x, y) in [(-0.6, -0.1), (0.3, -0.1), (-0.6, -0.65), (0.3, -0.65)]:
        BX((x, y, 0.5), (0.55, 0.36, 0.06), "tan", bevel=0.02)
        for sx in (-1, 1): BX((x + sx*0.22, y, 0.33), (0.05, 0.3, 0.34), "dkgrey", bevel=0.01)
        BX((x, y + 0.3, 0.36), (0.3, 0.26, 0.05), ["red", "blue", "yellow", "green"][int((x > 0)*2 + (y < -0.3))], bevel=0.02)
    S(0.1, (0.85, 0.3, 0.6), (1, 1, 1), "red"); BX((0.85, 0.3, 0.38), (0.4, 0.5, 0.4), "brown", bevel=0.03)
    face(1.25, 0.81, 0.18, 0.1, x=-0.2, mouth_dz=0.24, mr=0.09); fit(); return {}
def b_cracker():
    C = (0.9, 0.72, 0.42); BX((0, 0, 0.95), (1.7, 0.2, 1.7), C, bevel=0.06)
    for k in range(8):
        for (dx, dz) in [(-0.86 + 0.245*k, 0.86), (-0.86 + 0.245*k, -0.86), (0.86, -0.86 + 0.245*k), (-0.86, -0.86 + 0.245*k)]: S(0.11, (dx, 0, 0.95 + dz), (1, 0.9, 1), C)
    for i in range(3):
        for j in range(3):
            if (i, j) != (1, 1) and (i, j) != (0, 1) and (i, j) != (2, 1): S(0.05, (-0.5 + 0.5*i, -0.1, 0.45 + 0.5*j), (1, 0.4, 1), (0.7, 0.5, 0.25))
    for (x, z) in [(-0.3, 1.5), (0.4, 0.4), (0.65, 1.3), (-0.6, 0.7)]: S(0.03, (x, -0.11, z), (1, 1, 1), "white")
    face(1.05, -0.11, 0.22, 0.11, mouth_dz=0.3, mr=0.1); return {}
def b_cucumber():
    G = (0.2, 0.5, 0.2); RC(0.34, 1.7, (-0.2, 0, 0.95), G, (0, rad(-8), 0), lv=2)
    import random; random.seed(4)
    for k in range(16): a = random.uniform(0, TAU); z = random.uniform(0.3, 1.6); S(0.04, (-0.2 + 0.36*math.cos(a) - (z - 0.95)*0.14, 0.36*math.sin(a), z), (1, 1, 1), "green")
    Cy(0.36, 0.1, (0.65, -0.1, 0.38), G, (R90, 0, rad(-20)), verts=32); Cy(0.31, 0.11, (0.65, -0.1, 0.38), (0.75, 0.9, 0.6), (R90, 0, rad(-20)), verts=32)
    for k in range(6): a = k*TAU/6; S(0.035, (0.65 + 0.14*math.cos(a)*0.95, -0.17 - 0.14*math.cos(a)*0.34, 0.38 + 0.14*math.sin(a)), (1, 0.4, 1.6), "cream", rot=(0, a, 0))
    sface(1.1, 0.13, 0.08, x=-0.22, mouth_dz=0.22, mr=0.07); return {}
def b_diamond():
    C = (0.72, 0.9, 1.0); Co(0.9, 0.9, (0, 0, 0.47), C, (math.pi, 0, 0), verts=8); Co(0.9, 0.5, (0, 0, 1.17), C, (0, 0, 0), verts=8, r2=0.5); Cy(0.5, 0.02, (0, 0, 1.43), "white", verts=8)
    for k in range(8): a = k*TAU/8 + TAU/16; Cy(0.012, 0.66, (0.7*math.cos(a), 0.7*math.sin(a), 1.17), "white", (0, rad(-38), a), verts=6)
    To(0.9, 0.015, (0, 0, 0.92), "white")
    for (x, z) in [(1.0, 1.6), (-0.95, 1.5), (0.8, 0.5)]: S(0.06, (x, -0.2, z), (0.4, 0.4, 2.2), "white"); S(0.06, (x, -0.2, z), (2.2, 0.4, 0.4), "white")
    sface(1.15, 0.18, 0.1, mouth_dz=0.0, mr=0.01, tongue=False); smile(0.8, surf_y(0, 0.8, -0.5) - 0.015, 0.09); return {}
def b_eggplant():
    P_ = (0.4, 0.15, 0.5); S(0.62, (0, 0, 0.65), (1, 1, 1), P_); S(0.45, (0.08, 0, 1.25), (1, 1, 1.1), P_)
    for k in range(5): a = k*TAU/5; S(0.2, (0.1 + 0.26*math.cos(a), 0.26*math.sin(a), 1.68), (1.2, 0.6, 0.4), "green", rot=(0, rad(25), a))
    RC(0.06, 0.35, (0.14, 0, 1.9), "dkgreen", (0, rad(15), 0), lv=1); S(0.14, (0.3, -0.35, 0.95), (1, 0.3, 1.6), (0.6, 0.35, 0.7))
    sface(0.75, 0.2, 0.11, mouth_dz=0.28, mr=0.1); return {}
def b_envelope():
    BX((0, 0, 0.9), (2.1, 0.12, 1.35), "white", bevel=0.04)
    Fp([(-1.02, 0.65), (1.02, 0.65), (0, -0.1)], (0, -0.05, 0.9), 0.06, (0.9, 0.92, 0.97))
    for sx in (-1, 1): BX((sx*0.52, -0.065, 0.48), (1.25, 0.02, 0.025), "lgrey", rot=(0, rad(sx*33), 0), bevel=0.0)
    S(0.14, (-0.07, -0.1, 0.84), (1, 0.4, 1), "red"); S(0.14, (0.07, -0.1, 0.84), (1, 0.4, 1), "red"); Fp([(-0.2, 0), (0.2, 0), (0, -0.24)], (0, -0.1, 0.8), 0.07, "red")
    face(0.52, -0.07, 0.3, 0.09, mouth_dz=0.0, mr=0.01, tongue=False); smile(0.38, -0.07, 0.08); return {}
def b_feather():
    RC(0.03, 2.2, (0, 0, 1.15), "cream", (0, rad(18), 0), lv=1)
    S(0.75, (0.12, 0, 1.35), (0.55, 0.1, 1.15), "sky", rot=(0, rad(18), 0)); S(0.5, (0.3, -0.01, 1.75), (0.5, 0.1, 0.9), "white", rot=(0, rad(18), 0))
    for k in range(7): BX((-0.12 + 0.07*k, -0.075, 0.65 + 0.22*k), (0.5 - 0.02*k, 0.01, 0.015), "blue", rot=(0, rad(18 + 55), 0), bevel=0.0)
    sface(1.3, 0.13, 0.085, x=0.1, mouth_dz=0.22, mr=0.075); return {}
def b_firefighter():
    person((0.85, 0.65, 0.15), (0.85, 0.65, 0.15), "hairb", shoes="charcoal")
    for z in (0.52, 0.95): BX((0, 0, z), (0.78, 0.63, 0.07), "lgrey", bevel=0.02)
    for sx in (-1, 1): To(0.09, 0.025, (sx*0.5, -0.07, 0.62), "lgrey", (0, rad(sx*15), 0))
    S(0.46, (0, 0.03, 1.55), (1, 1.05, 0.75), "red"); Cy(0.55, 0.05, (0, 0.1, 1.56), "red", (rad(-8), 0, 0), verts=32); BX((0, 0.0, 1.9), (0.08, 0.6, 0.08), "red", bevel=0.03)
    Fp([(-0.1, 0), (0.1, 0), (0.1, 0.16), (0, 0.24), (-0.1, 0.16)], (0, -0.43, 1.62), 0.04, "gold")
    RC(0.03, 1.0, (0.64, -0.12, 0.8), "wood", lv=1); Fp([(0, 0), (0.3, 0.12), (0.3, -0.12)], (0.64, -0.12, 1.25), 0.06, "red"); Fp([(0, 0.05), (-0.14, 0.0), (0, -0.05)], (0.64, -0.12, 1.25), 0.06, "lgrey"); return {}
def b_fountain():
    Cy(1.1, 0.4, (0, 0, 0.2), "stone", verts=40); wm = mat((0.15, 0.38, 0.72), 0.2, 0.8); o = Cy(0.98, 0.42, (0, 0, 0.21), "water", verts=40); o.data.materials[0] = wm
    RC(0.14, 0.9, (0, 0, 0.8), "stone", lv=1); Cy(0.5, 0.12, (0, 0, 1.22), "stone", verts=32); o2 = Cy(0.43, 0.13, (0, 0, 1.23), "water", verts=32); o2.data.materials[0] = wm
    RC(0.07, 0.4, (0, 0, 1.45), "stone", lv=1)
    for k in range(6):
        a = k*TAU/6
        for j in range(5): t = j/4; q = S(0.07 - 0.008*j, (math.cos(a)*(0.1 + 0.42*t), math.sin(a)*(0.1 + 0.42*t), 1.7 + 0.35*math.sin(math.pi*min(1, t*1.15)) - 0.5*t*t), (1, 1, 1.3), "water"); q.data.materials[0] = wm
    q = S(0.12, (0, 0, 1.78), (1, 1, 1.4), "water"); q.data.materials[0] = wm
    face(0.24, -1.1, 0.22, 0.1, mouth_dz=0.0, mr=0.01, tongue=False); return {"glow": [wm]}
def b_grasshopper():
    G = (0.45, 0.75, 0.2); S(0.36, (0, 0.2, 0.75), (0.8, 1.9, 0.75), G); S(0.33, (0, -0.6, 0.95), (0.9, 0.9, 1.1), G); S(0.3, (0, 0.35, 0.92), (0.6, 1.7, 0.4), "lgreen")
    for sx in (-1, 1):
        RC(0.08, 0.95, (sx*0.42, 0.45, 0.85), "green", (rad(-42), 0, 0), lv=1); RC(0.04, 1.0, (sx*0.45, 0.72, 0.6), "dkgreen", (rad(38), 0, 0), lv=1); S(0.07, (sx*0.45, 0.42, 0.06), (1, 1.8, 0.6), "dkgreen")
        for k in range(2): RC(0.03, 0.6, (sx*0.3, -0.45 + 0.35*k, 0.35), "dkgreen", (0, rad(sx*-25), 0), lv=1)
        RC(0.015, 0.7, (sx*0.12, -0.75, 1.5), "dkgreen", (rad(30), rad(sx*14), 0), lv=1)
    eyes(1.08, -0.82, 0.17, 0.1); smile(0.82, -0.86, 0.08, tongue=False); return {}
def b_houseboat():
    o = Fp([(-1.4, 0.55), (1.4, 0.55), (1.1, 0.0), (-1.1, 0.0)], (0, 0, 0.02), 1.0, "brown"); bevel(o, 0.06); BX((0, 0, 0.6), (2.9, 1.1, 0.08), "wood", bevel=0.03)
    BX((0.1, 0.05, 1.05), (1.5, 0.8, 0.85), "yellow"); Fp([(-0.9, 0), (0.9, 0), (0.6, 0.3), (-0.6, 0.3)], (0.1, 0.05, 1.47), 0.95, "roof"); BX((0.5, 0.1, 1.85), (0.14, 0.14, 0.3), "brick", bevel=0.02)
    BX((0.55, -0.36, 1.0), (0.26, 0.04, 0.55), "dkbrown", bevel=0.02); BX((-0.35, -0.36, 1.15), (0.5, 0.04, 0.3), "glass", bevel=0.02)
    To(0.16, 0.06, (-1.05, -0.52, 0.42), "red", (R90, 0, 0));
    for x in (-1.25, 1.3): RC(0.025, 0.4, (x, -0.5, 0.82), "lgrey", lv=1)
    Cy(0.015, 2.55, (0.02, -0.5, 1.0), "lgrey", (0, R90, 0), verts=6)
    face(1.3, -0.36, 0.0, 0.0, mouth_dz=0.0, mr=0.01, tongue=False) if False else None
    face(0.34, -0.51, 0.22, 0.1, x=0.2, mouth_dz=0.0, mr=0.01, tongue=False); fit(2.0, 2.6); return {}
def b_invitation():
    BX((0, 0, 1.0), (1.5, 0.1, 1.9), "cream", bevel=0.04); BX((0, -0.02, 1.0), (1.3, 0.1, 1.7), "white", bevel=0.02)
    for (x, z, c) in [(-0.35, 1.55, "red"), (0, 1.68, "yellow"), (0.35, 1.55, "blue")]: S(0.17, (x, -0.08, z), (1, 0.3, 1.2), c); Cy(0.008, 0.35, (x*0.6, -0.08, z - 0.35), "dkgrey", (0, rad(-x*40), 0), verts=6)
    for k in range(3): BX((0, -0.075, 0.55 - 0.14*k), (0.9 - 0.2*k, 0.01, 0.04), "lgrey", bevel=0.0)
    for (x, z) in [(-0.5, 0.25), (0.5, 0.25), (-0.52, 1.1), (0.52, 1.1)]: Fp(starpts(0.09, 0.04), (x, -0.08, z), 0.02, "gold")
    face(1.0, -0.075, 0.17, 0.09, mouth_dz=0.22, mr=0.08); return {}
def b_janitor():
    person((0.4, 0.5, 0.62), (0.4, 0.5, 0.62), "hairb", skin="skin3", shoes="charcoal")
    S(0.45, (0, 0.04, 1.52), (1, 1, 0.8), "navy"); BX((0, -0.42, 1.6), (0.5, 0.35, 0.05), "navy", bevel=0.02, rot=(rad(12), 0, 0))
    BX((-0.18, -0.31, 0.88), (0.2, 0.03, 0.12), "white", bevel=0.01); To(0.1, 0.012, (0.25, -0.33, 0.52), "gold", (R90, 0, 0))
    RC(0.03, 1.7, (0.66, -0.12, 0.95), "wood", lv=1)
    for k in range(7): RC(0.04, 0.35, (0.66 + 0.06*(k - 3), -0.12 + 0.04*(k % 2), 0.2), "white", (0, rad((k - 3)*7), 0), lv=1)
    RC(0.22, 0.34, (-0.72, -0.15, 0.2), "yellow", lv=1); o = Cy(0.19, 0.02, (-0.72, -0.15, 0.37), "water", verts=24); return {}
def b_library():
    base(2.6, 1.9, "grass"); BX((0, 0.2, 0.85), (2.2, 1.1, 1.3), "tan"); BX((0, 0.2, 1.55), (2.35, 1.25, 0.12), "brown")
    BX((0, -0.36, 0.5), (0.5, 0.05, 0.6), "dkbrown", bevel=0.02)
    for sx in (-1, 1):
        BX((sx*0.72, -0.36, 0.85), (0.55, 0.04, 0.7), "cream", bevel=0.02)
        for r in range(3):
            for k in range(5): BX((sx*0.72 - 0.2 + 0.1*k, -0.385, 0.62 + 0.22*r), (0.08, 0.02, 0.17), ["red", "blue", "yellow", "green", "purple"][(k + r*2) % 5], bevel=0.0)
    BX((0, -0.25, 1.82), (0.75, 0.12, 0.5), "blue", bevel=0.03); BX((0, -0.31, 1.82), (0.65, 0.03, 0.4), "white", bevel=0.01); BX((0, -0.33, 1.82), (0.03, 0.03, 0.42), "blue", bevel=0.0)
    for k, c in enumerate(["red", "green", "yellow"]): BX((1.05, -0.7, 0.26 + 0.11*k), (0.4, 0.3, 0.1), c, bevel=0.02, rot=(0, 0, rad(12*k)))
    face(1.28, -0.35, 0.16, 0.085, mouth_dz=0.0, mr=0.01, tongue=False); fit(); return {}
def b_lightning():
    gm = mat((1.0, 0.85, 0.1), 0.4, 1.2)
    o = Fp([(0.25, 1.75), (-0.5, 0.95), (-0.05, 0.95), (-0.4, 0.1), (0.55, 1.15), (0.1, 1.15), (0.65, 1.75)], (0, 0, 0), 0.3, "yellow"); o.data.materials[0] = gm; bevel(o, 0.04)
    for (x, z, r) in [(0.1, 2.0, 0.42), (-0.4, 1.95, 0.32), (0.6, 1.95, 0.34), (0.3, 2.25, 0.3), (-0.15, 2.22, 0.28)]: S(r, (x, 0.05, z), (1, 0.8, 1), (0.5, 0.52, 0.62))
    face(2.0, -0.33, 0.16, 0.09, x=0.1, mouth_dz=0.2, mr=0.08); return {"glow": [gm]}
def b_nectarine():
    S(0.72, (0, 0, 0.75), (1, 1, 0.95), (0.95, 0.35, 0.2)); S(0.55, (-0.3, -0.25, 0.9), (1, 1, 1), (1.0, 0.65, 0.2)); S(0.72, (0.06, 0.02, 0.75), (0.2, 1.0, 0.94), (0.8, 0.25, 0.15))
    RC(0.03, 0.2, (0, 0, 1.5), "brown", lv=1); S(0.18, (0.2, 0, 1.52), (1.5, 0.6, 0.35), "green", rot=(0, rad(-20), 0))
    sface(0.85, 0.2, 0.11, mouth_dz=0.28, mr=0.1); return {}
def b_pelican():
    h = bird("white", None, "orange", s=1.25, legh=0.4, neck=0.35, beak_len=0.75, beak_r=0.12, wl=0.7)
    hz = 0.4 + 0.5*1.25 + 0.35*1.25 + 0.35; hy = -0.42*1.25 - 0.35*0.25
    S(0.22, (0, hy - 0.6, hz - 0.2), (0.7, 1.7, 0.8), "yellow"); return h
def b_playground():
    BX((0, 0, 0.1), (2.7, 2.2, 0.2), "grass", bevel=0.08); S(0.7, (0.5, -0.4, 0.17), (1.2, 1, 0.12), "sand")
    for sx in (-1, 1):
        for sy in (-1, 1): RC(0.035, 1.5, (-0.75 + sx*0.5, 0.5 + sy*0.2, 0.9), "blue", (rad(sy*14), 0, 0), lv=1)
    RC(0.04, 1.1, (-0.75, 0.5, 1.62), "blue", (0, R90, 0), lv=1)
    for x in (-0.95, -0.55): Cy(0.012, 0.95, (x, 0.5, 1.15), "dkgrey", verts=6); BX((x, 0.5, 0.66), (0.26, 0.14, 0.04), "red", bevel=0.01)
    Fp([(-0.85, 0.02), (-0.65, 0.0), (0.25, 0.75), (0.25, 0.85), (-0.65, 0.12), (-0.85, 0.14)], (0.5, -0.35, 0.2), 0.36, "red"); BX((0.95, -0.35, 0.6), (0.45, 0.4, 0.8), "yellow", bevel=0.04)
    BX((0.9, 0.7, 0.42), (1.1, 0.14, 0.05), "orange", bevel=0.02, rot=(0, rad(-12), 0)); Fp([(-0.14, 0), (0.14, 0), (0, 0.22)], (0.9, 0.7, 0.2), 0.2, "purple")
    face(0.72, -0.56, 0.11, 0.07, x=0.95, mouth_dz=0.17, mr=0.06); fit(1.9, 2.6); return {}
def b_pretzel():
    C = (0.6, 0.33, 0.12); To(0.78, 0.13, (0, 0, 0.95), C, (R90, 0, 0), scale=(1, 1, 0.9))
    for sx in (-1, 1): RC(0.12, 1.25, (sx*0.22, -0.02, 0.9), C, (0, rad(sx*33), 0), lv=1); S(0.16, (sx*0.55, -0.02, 0.38), (1, 1, 1), C)
    S(0.2, (0, -0.05, 1.22), (1, 1, 1), C)
    import random; random.seed(6)
    for k in range(22): a = random.uniform(0, TAU); S(0.03, (0.78*math.cos(a), -0.12, 0.95 + 0.7*math.sin(a)), (1, 1, 1), "white")
    face(1.26, -0.2, 0.09, 0.06, mouth_dz=0.14, mr=0.05); return {}
def b_quarter(): coin("silver", 1.0, 0.16, "lgrey", "25¢", (0.12, 0.13, 0.2), ridges=True); return {}
def b_raccoon():
    h = quad_meta((0.55, 0.55, 0.6), (0.8, 0.8, 0.82), "white", (0.2, 0.2, 0.24), ear="point", tail="bushy", snout_len=0.08, size=0.9)
    for sx in (-1, 1): S(0.2, (sx*0.2, surf_y(sx*0.2, 1.32, -0.9) + 0.04, 1.32), (1.15, 0.3, 0.8), "charcoal")
    for k in range(3): To(0.2 - 0.02*k, 0.06, (0.16 + 0.07*k, 0.95 + 0.14*k, 1.0 + 0.16*k), "charcoal", (rad(-35), 0, 0))
    return h
def b_racecar():
    body = E((0, 0, 0))
    RB((0, 0.15, 0.5), (1.2, 2.6, 0.5), "red", body, lv=2); RB((0, -1.25, 0.42), (0.7, 1.0, 0.3), "red", body, lv=2); RB((0, 0.3, 0.85), (0.75, 0.9, 0.4), "glass", body, lv=2)
    BX((0, 1.45, 1.05), (1.5, 0.3, 0.06), "charcoal", body, bevel=0.02)
    for sx in (-1, 1): BX((sx*0.55, 1.45, 0.85), (0.06, 0.2, 0.4), "charcoal", body, bevel=0.01)
    BX((0, -1.72, 0.3), (1.3, 0.25, 0.06), "charcoal", body, bevel=0.02); BX((0, 0.15, 0.76), (0.2, 2.6, 0.02), "white", body, bevel=0.0)
    for sx in (-1, 1): Cy(0.2, 0.03, (sx*0.61, 0.2, 0.52), "white", (0, R90, 0), body)
    ws = wheelset(body, [(sx*0.78, y, 0.36) for sx in (-1, 1) for y in (-1.05, 1.0)], 0.36, 0.34, "black", "yellow")
    face(0.5, -1.74, 0.2, 0.1, parent=body, mouth_dz=0.0, mr=0.01, tongue=False); smile(0.42, -1.76, 0.07, parent=body); return {"body": body, "wheels": ws}
def b_rectangle():
    cx, cz = shape([(-1.15, 0.05), (1.15, 0.05), (1.15, 1.35), (-1.15, 1.35)], "purple", "lavender"); face(cz + 0.1, -0.19, 0.22, 0.12, x=cx, mouth_dz=0.32, mr=0.11); return {}
def b_restaurant():
    base(2.6, 1.9, "lgrey"); BX((0, 0.25, 0.9), (2.1, 1.0, 1.4), "cream"); BX((0, 0.25, 1.66), (2.2, 1.1, 0.12), "roof")
    for k in range(8): BX((-0.91 + 0.26*k, -0.45, 1.2), (0.26, 0.5, 0.05), "red" if k % 2 else "white", rot=(rad(-28), 0, 0), bevel=0.0)
    BX((0.6, -0.26, 0.55), (0.4, 0.05, 0.7), "dkbrown", bevel=0.02); BX((-0.45, -0.26, 0.7), (0.9, 0.05, 0.5), "glass", bevel=0.02)
    Cy(0.3, 0.06, (0, -0.2, 1.95), "white", (R90, 0, 0)); Cy(0.2, 0.07, (0, -0.21, 1.95), "sky", (R90, 0, 0))
    for sx in (-1, 1): BX((sx*0.42, -0.22, 1.95), (0.035, 0.04, 0.45), "silver", bevel=0.01)
    Cy(0.26, 0.04, (-0.85, -0.75, 0.55), "red", verts=24); RC(0.03, 0.35, (-0.85, -0.75, 0.37), "dkgrey", lv=1)
    for sx in (-1, 1): BX((-0.85 + sx*0.36, -0.75, 0.36), (0.16, 0.16, 0.3), "wood", bevel=0.02)
    face(0.78, -0.24, 0.15, 0.085, x=-0.45, mouth_dz=0.0, mr=0.01, tongue=False); fit(); return {}
def b_sailboat():
    S(1.0, (0, 0, 0.42), (1.45, 0.5, 0.42), "blue"); BX((0, 0, 0.62), (2.3, 0.75, 0.08), "white", bevel=0.03); BX((0.5, 0, 0.82), (0.6, 0.45, 0.35), "white", bevel=0.05); S(0.07, (0.5, -0.24, 0.85), (1, 0.4, 1), "sky")
    RC(0.045, 2.0, (-0.1, 0, 1.6), "brown", lv=1); Fp([(0, 0), (1.15, 0.1), (0, 1.75)], (-0.03, 0, 0.78), 0.06, "white"); Fp([(0, 0), (-0.85, 0.1), (0, 1.35)], (-0.17, 0, 0.82), 0.06, "yellow")
    Fp([(0, 0), (0.3, -0.1), (0, -0.2)], (-0.1, 0, 2.65), 0.03, "red"); To(0.5, 0.02, (0, 0, 0.0), "white") if False else None
    sface(0.4, 0.22, 0.11, x=-0.2, mouth_dz=0.2, mr=0.09); fit(2.2, 2.6); return {}
def b_salamander(): lizard("charcoal", "yellow", "yellow"); return {}
def b_starfish():
    C = (1.0, 0.5, 0.35); o = Fp(starpts(1.0, 0.5), (0, 0, 1.0), 0.36, C); bevel(o, 0.1); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2; smooth(o)
    for k in range(5):
        a = R90 + k*TAU/5
        for j in range(3): S(0.05, (0.3*math.cos(a)*(1 + j*0.7), -0.17, 1.0 + 0.3*math.sin(a)*(1 + j*0.7)), (1, 0.5, 1), (1.0, 0.75, 0.6))
    face(1.08, -0.17, 0.15, 0.09, mouth_dz=0.24, mr=0.08); return {}
def b_sunglasses():
    for sx in (-1, 1):
        Cy(0.48, 0.08, (sx*0.58, 0, 1.0), "charcoal", (R90, 0, 0), verts=40); To(0.48, 0.06, (sx*0.58, 0, 1.0), "red", (R90, 0, 0))
        BX((sx*1.08, 0.55, 1.05), (0.07, 1.1, 0.1), "red", bevel=0.03); S(0.08, (sx*1.08, 1.1, 0.98), (1, 1, 1.4), "red"); S(0.1, (sx*0.72, -0.05, 1.2), (1.6, 0.3, 0.6), "lgrey", rot=(0, rad(35), 0))
    RC(0.05, 0.3, (0, 0, 1.08), "red", (0, R90, 0), lv=1)
    eyes(0.98, -0.05, 0.58, 0.14); smile(0.62, 0.0, 0.1); return {}
def b_sweater():
    C = "purple"; BX((0, 0, 0.9), (1.25, 0.45, 1.4), C, bevel=0.12); RC(0.28, 0.28, (0, 0, 1.72), "lavender", lv=1)
    for sx in (-1, 1): RC(0.2, 1.1, (sx*0.82, 0, 1.0), C, (0, rad(sx*-22), 0), lv=2); RC(0.21, 0.16, (sx*1.02, 0, 0.5), "lavender", (0, rad(sx*-22), 0), lv=1)
    BX((0, 0, 0.24), (1.27, 0.47, 0.18), "lavender", bevel=0.05)
    for z in (0.48, 0.62): BX((0, 0, z), (1.27, 0.47, 0.06), "yellow" if z < 0.5 else "hotpink", bevel=0.01)
    face(1.3, -0.235, 0.2, 0.1, mouth_dz=0.26, mr=0.09); return {}
def b_teacher():
    person("green", "dkbrown", "brown", style="bun", skin="skin2", shoes="charcoal")
    for sx in (-1, 1): To(0.115, 0.016, (sx*0.15, -0.44, 1.43), "red", (R90, 0, 0))
    Cy(0.012, 0.1, (0, -0.45, 1.44), "red", (0, R90, 0), verts=6); BX((0, -0.3, 0.8), (0.22, 0.04, 0.6), "white", bevel=0.01)
    BX((-0.6, -0.2, 0.62), (0.32, 0.1, 0.42), "blue", bevel=0.03); BX((-0.6, -0.26, 0.62), (0.26, 0.02, 0.36), "white", bevel=0.01)
    RC(0.02, 0.9, (0.7, -0.15, 0.95), "wood", (0, rad(25), 0), lv=1); S(0.1, (0.3, -0.25, 0.25), (1, 1, 0.9), "red") if False else None
    return {}
def b_television():
    gm = mat((0.14, 0.36, 0.55), 0.3, 1.0)
    BX((0, 0, 1.0), (2.0, 0.5, 1.35), "charcoal", bevel=0.08); sc = BX((-0.15, -0.24, 1.0), (1.45, 0.06, 1.05), "sky", bevel=0.05); sc.data.materials[0] = gm
    for k in range(3): S(0.07, (0.8, -0.26, 1.35 - 0.25*k), (1, 0.5, 1), "red" if k == 0 else "lgrey")
    for sx in (-1, 1): BX((sx*0.6, 0, 0.2), (0.14, 0.4, 0.4), "dkgrey", bevel=0.03, rot=(0, rad(sx*-15), 0)); RC(0.02, 0.8, (sx*0.25, 0, 2.0), "lgrey", (0, rad(sx*28), 0), lv=1); S(0.05, (sx*0.44, 0, 2.35), (1, 1, 1), "lgrey")
    face(1.1, -0.27, 0.22, 0.12, x=-0.15, mouth_dz=0.3, mr=0.1); return {"glow": [gm]}
def b_triangle():
    cx, cz = shape([(-1.0, 0.05), (1.0, 0.05), (0, 1.75)], "green", "lgreen"); face(0.75, -0.19, 0.2, 0.11, x=0, mouth_dz=0.28, mr=0.1); return {}
def b_underwear():
    o = Fp([(-0.95, 1.4), (0.95, 1.4), (0.95, 0.85), (0.28, 0.2), (-0.28, 0.2), (-0.95, 0.85)], (0, 0, 0), 0.5, "white"); bevel(o, 0.08)
    BX((0, 0, 1.36), (1.95, 0.54, 0.2), "blue", bevel=0.05)
    for (x, z) in [(-0.6, 1.0), (0.6, 1.0), (0, 0.45), (-0.3, 0.75), (0.3, 0.75), (0, 1.1)]: S(0.07, (x, -0.26, z), (1, 0.3, 1), "red")
    face(0.95, -0.27, 0.36, 0.1, mouth_dz=0.0, mr=0.01, tongue=False); smile(0.75, -0.27, 0.09); return {}
def b_vegetable():
    RC(0.75, 0.6, (0, 0, 0.35), "wood", lv=1)
    for z in (0.2, 0.4, 0.6): To(0.82, 0.04, (0, 0, z), "brown")
    Co(0.2, 0.9, (-0.4, 0.05, 1.0), "orange", (rad(180), rad(-12), 0)); S(0.16, (-0.48, 0.05, 1.5), (1, 1, 1.5), "green")
    RC(0.12, 0.5, (0.35, 0.15, 0.95), "lgreen", lv=1)
    for (dx, dz, r) in [(0, 0.45, 0.28), (-0.22, 0.32, 0.22), (0.22, 0.34, 0.22), (0, 0.3, 0.24)]: S(r, (0.35 + dx, 0.15 - 0.05*(dz < 0.31), 0.95 + dz), (1, 1, 1), "green")
    S(0.3, (0.05, -0.3, 0.85), (1, 1, 0.9), "red"); S(0.08, (0.05, -0.3, 1.12), (1.5, 1.5, 0.4), "green")
    S(0.22, (-0.05, 0.35, 0.9), (1, 1, 1.2), "purple")
    face(0.42, -0.84, 0.2, 0.1, mouth_dz=0.0, mr=0.01, tongue=False); smile(0.24, -0.85, 0.09); return {}
def b_vulture():
    s_ = 1.2; h = bird("charcoal", "dkgrey", (0.9, 0.8, 0.5), s=s_, legh=0.5, legc="lgrey", neck=0.3, beak_len=0.3, beak_r=0.1, wl=0.85)
    hz = 0.5 + 0.5*s_ + 0.35*s_ + 0.3; hy = -0.42*s_ - 0.3*0.25
    S(0.31*s_, (0, hy + 0.01, hz + 0.01), (1, 1, 1), "pink"); To(0.22, 0.09, (0, hy + 0.2, hz - 0.36), "white", (rad(14), 0, 0)); Co(0.05, 0.14, (0, hy - 0.6, hz - 0.13), (0.9, 0.8, 0.5), (math.pi, 0, 0))
    return h
def b_waterfall():
    gm = mat((0.16, 0.4, 0.72), 0.2, 0.8)
    BX((0, 0, 0.1), (2.6, 2.2, 0.2), "grass", bevel=0.08); BX((0, 0.6, 1.0), (2.2, 0.9, 1.7), "stone", bevel=0.12); BX((-0.75, 0.45, 0.7), (0.7, 0.9, 1.1), (0.6, 0.6, 0.65), bevel=0.12)
    w = BX((0.25, 0.12, 1.05), (0.75, 0.12, 1.75), "water", bevel=0.05); w.data.materials[0] = gm; w2 = BX((0.25, 0.5, 1.87), (0.75, 0.9, 0.08), "water", bevel=0.03); w2.data.materials[0] = gm
    S(0.8, (0.25, -0.45, 0.17), (1.1, 0.8, 0.2), "water")
    for k in range(6): S(0.13 + 0.03*(k % 2), (-0.15 + 0.16*k, -0.05, 0.3), (1, 1, 0.8), "white")
    tree_s(-0.8, 0.7, 0.9); tree_s(0.95, 0.75, 0.7, "lgreen"); S(0.2, (-0.95, -0.6, 0.32), (1.2, 1, 0.8), "stone")
    face(0.75, 0.0, 0.14, 0.085, x=-0.75, mouth_dz=0.2, mr=0.07); fit(); return {"glow": [gm]}
def b_watermelon():
    halfdisc((0, 0, 1.15), 1.1, 0.5, "green"); halfdisc((0, 0, 1.151), 1.0, 0.52, "white"); halfdisc((0, 0, 1.152), 0.93, 0.54, "red")
    for (x, z) in [(-0.6, 0.85), (0.6, 0.85), (-0.3, 0.5), (0.3, 0.5), (0, 0.35), (-0.75, 1.05), (0.75, 1.05)]: S(0.05, (x, -0.275, z), (0.7, 0.4, 1.3), "black")
    face(0.92, -0.275, 0.2, 0.11, mouth_dz=0.26, mr=0.1); return {}
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}
