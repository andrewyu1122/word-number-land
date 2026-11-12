# 52 new word characters (batch 4). Rounded (subsurf) + metaball animals. Face -Y, stand on z=0.
_SP = PIPE + "/"
for _f in ("builders_words.py", "builders_subsurf.py", "builders_meta.py"):
    exec(open(_SP + _f, encoding="utf-8").read().split("BUILD = {k[2:]")[0])
PAL.update(dict(coral=(1.0,0.45,0.35), aqua=(0.3,0.8,0.85), rust=(0.8,0.35,0.15), ivory=(0.98,0.95,0.85), lgreen=(0.55,0.85,0.35), violet=(0.45,0.3,0.85), sand=(0.95,0.88,0.6), plum=(0.6,0.2,0.5), charcoal=(0.15,0.15,0.18)))
def wheelset(body, pts, r=0.3, w=0.26, c="black", hub="lgrey"):
    ws = []
    for (x, y, z) in pts:
        p = E((x, y, z), body); Cy(r, w, (x, y, z), c, (0, R90, 0), p); Cy(r*0.55, w+0.03, (x, y, z), hub, (0, R90, 0), p, verts=16); ws.append(p)
    return ws
# ---------------------------------------------------------------- level 1
def b_van():
    body = E((0, 0, 0))
    RB((0, 0.25, 1.05), (1.5, 2.4, 1.3), "white", body, lv=1); RB((0, -1.0, 0.95), (1.45, 0.8, 1.0), "white", body, lv=1)
    RB((0, 0.1, 1.0), (1.56, 2.3, 0.3), "blue", body, lv=1); RB((0, -0.2, 0.45), (1.55, 2.9, 0.3), "dkgrey", body, lv=1)
    RB((0, -1.36, 1.15), (1.15, 0.06, 0.5), "glass", body, lv=1)
    for sx in (-1, 1): RB((sx*0.76, 0.3, 1.25), (0.06, 0.8, 0.45), "glass", body, lv=1); S(0.13, (sx*0.5, -1.36, 0.8), (1, 0.5, 1), "yellow", body)
    RB((0, -1.4, 0.5), (1.3, 0.1, 0.18), "lgrey", body, lv=1); RB((0, 0.3, 1.72), (0.9, 1.4, 0.12), "blue", body, lv=1)
    ws = wheelset(body, [(sx*0.78, y, 0.35) for sx in (-1, 1) for y in (-0.8, 0.9)], 0.33, 0.28)
    face(1.15, -1.39, 0.3, 0.13, parent=body, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.85, -1.42, 0.13, parent=body); return {"body": body, "wheels": ws}
def b_log():
    RC(0.5, 2.2, (0, 0, 0.5), "brown", (0, R90, 0), lv=2)
    for sx in (-1, 1): Cy(0.46, 0.08, (sx*1.14, 0, 0.5), "tan", (0, R90, 0), verts=24); To(0.3, 0.025, (sx*1.19, 0, 0.5), "wood", (0, R90, 0)); To(0.15, 0.02, (sx*1.19, 0, 0.5), "wood", (0, R90, 0))
    for k in range(6): RB((-0.8+0.32*k, -0.1*(k % 2)+0.05, 0.98), (0.18, 0.1, 0.07), "dkbrown", lv=1)
    RB((0.3, 0.3, 1.05), (0.1, 0.1, 0.45), "dkbrown", lv=1); S(0.18, (0.3, 0.3, 1.32), (1.3, 0.5, 0.8), "green", rot=(0, 0, rad(30)))
    face(0.62, -0.5, 0.22, 0.11, mouth_dz=0.3, mr=0.1); return {}
def b_gem():
    Co(0.7, 0.7, (0, 0, 0.35), "aqua", (math.pi, 0, 0), verts=6); Co(0.7, 0.55, (0, 0, 0.97), "aqua", (0, 0, 0), verts=6, r2=0.3)
    Cy(0.3, 0.02, (0, 0, 1.25), "white", verts=6)
    for k in range(6): a = k*TAU/6; Cy(0.012, 0.56, (0.35*math.cos(a), 0.35*math.sin(a), 0.97), "white", (0, rad(-48), a), verts=6)
    for sx in (-1, 1): S(0.06, (sx*0.18, -0.5, 1.05), (1, 0.4, 1), "white")
    face(0.75, -0.6, 0.18, 0.1, mouth_dz=0.28, mr=0.09); return {}
def b_pot():
    RC(0.75, 0.9, (0, 0, 0.5), "navy", lv=2); Cy(0.78, 0.08, (0, 0, 0.95), "lgrey", verts=32); RK(0.78, 0.32, (0, 0, 1.12), "navy", lv=2, r2=0.3); S(0.1, (0, 0, 1.32), (1, 1, 0.8), "lgrey")
    for sx in (-1, 1): To(0.14, 0.035, (sx*0.82, 0, 0.75), "lgrey", (0, R90, 0))
    for k in range(3): S(0.07, (-0.2+0.2*k, 0, 1.45+0.15*k), (1, 1, 1.4), "lgrey")
    face(0.65, -0.72, 0.22, 0.12, mouth_dz=0.3, mr=0.1); return {}
def b_pan():
    RC(0.8, 0.3, (0, 0, 0.3), "charcoal", lv=2); Cy(0.68, 0.04, (0, 0, 0.44), "dkgrey", verts=32)
    RC(0.07, 1.1, (1.25, 0, 0.42), "charcoal", (0, R90, 0), lv=1); RC(0.09, 0.5, (1.65, 0, 0.42), "wood", (0, R90, 0), lv=1)
    S(0.22, (-0.15, 0.1, 0.5), (1, 1, 0.3), "white"); S(0.12, (-0.15, 0.1, 0.52), (1, 1, 0.5), "yellow")
    face(0.3, -0.78, 0.2, 0.1, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.12, -0.8, 0.1); return {}
def b_net():
    RC(0.05, 1.5, (0, 0, 0.75), "wood", lv=1); To(0.55, 0.035, (0, 0, 1.75), "lgrey", (R90, 0, 0))
    o = S(0.5, (0, 0.25, 1.7), (1, 1.1, 0.95), "white"); o.data.materials[0] = mat((1, 1, 1), 0.9); o.scale = (1, 0.9, 0.9)
    for k in range(5): To(0.5-0.1*k, 0.012, (0, 0.12+0.12*k, 1.75), "lgrey", (R90, 0, 0))
    for a in range(8): Cy(0.012, 0.9, (0.5*math.cos(a*TAU/8), 0.4, 1.75+0.5*math.sin(a*TAU/8)), "lgrey", (R90, 0, 0), verts=6)
    face(1.85, -0.55, 0.16, 0.09, mouth_dz=0.25, mr=0.08); return {}
def b_tub():
    RB((0, 0, 0.55), (1.9, 1.1, 0.75), "white", lv=2); RB((0, 0, 0.9), (1.6, 0.8, 0.12), "sky", lv=1)
    for (x, y) in [(-0.7, -0.35), (0.7, -0.35), (-0.7, 0.35), (0.7, 0.35)]: S(0.14, (x, y, 0.12), (1, 1, 0.8), "gold")
    Cy(0.04, 0.5, (0.75, 0, 1.15), "lgrey"); Cy(0.04, 0.3, (0.75, -0.12, 1.38), "lgrey", (R90, 0, 0))
    for k in range(6): o = S(0.1+0.04*(k % 3), (-0.6+0.25*k, 0.1*math.sin(k), 1.1+0.15*(k % 3)), (1, 1, 1), "white"); o.data.materials[0] = mat((0.85, 0.95, 1.0), 0.2)
    face(0.6, -0.56, 0.3, 0.13, mouth_dz=0.3, mr=0.12); return {}
def b_jar():
    o = RC(0.55, 1.2, (0, 0, 0.62), "glass", lv=2); o.data.materials[0] = mat((0.75, 0.9, 1.0), 0.15)
    RC(0.42, 0.25, (0, 0, 1.32), "gold", lv=1); Cy(0.45, 0.06, (0, 0, 1.46), "gold", verts=24)
    for k in range(5): S(0.16, (0.22*math.cos(k*1.26), 0.22*math.sin(k*1.26), 0.35+0.22*(k % 3)), (1, 1, 0.55), "tan")
    face(0.85, -0.5, 0.2, 0.11, mouth_dz=0.3, mr=0.1); return {}
def b_axe():
    RC(0.08, 1.9, (0, 0, 0.95), "wood", lv=1)
    RB((-0.45, 0, 1.55), (0.9, 0.2, 0.7), "lgrey", lv=2); RB((-0.85, 0, 1.55), (0.14, 0.24, 0.95), "silver", lv=1)
    RB((0.12, 0, 1.6), (0.3, 0.26, 0.4), "dkgrey", lv=1); To(0.1, 0.02, (0, 0, 1.15), "red", (0, 0, 0))
    face(1.65, -0.11, 0.17, 0.1, x=-0.45, mouth_dz=0.26, mr=0.09); return {}
def b_bow():
    for sx in (-1, 1):
        RK(0.45, 0.95, (sx*0.6, 0, 1.1), "hotpink", (0, rad(sx*-90), 0), lv=2); RK(0.28, 0.7, (sx*0.6, -0.08, 1.1), "pink", (0, rad(sx*-90), 0), lv=2)
        RB((sx*0.32, 0.0, 0.45), (0.28, 0.14, 0.9), "hotpink", rot=(0, rad(sx*12), 0), lv=2)
    RB((0, -0.05, 1.1), (0.4, 0.34, 0.46), "hotpink", lv=2)
    face(1.15, -0.25, 0.1, 0.07, mouth_dz=0.18, mr=0.06); return {}
def b_saw():
    Fp([(-1.1, 0.55), (1.1, 0.35), (1.1, 0.0), (-1.1, 0.0)], (0.15, 0, 0.9), 0.05, "silver")
    for k in range(11): Fp([(0, 0), (0.18, 0), (0.09, -0.16)], (1.15-0.2*k, 0, 0.9), 0.05, "silver")
    RB((-1.25, 0, 1.0), (0.3, 0.3, 0.9), "wood", lv=2); RB((-1.25, 0, 1.0), (0.14, 0.34, 0.45), "dkbrown", lv=1)
    face(1.2, -0.05, 0.2, 0.1, x=0.3, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.95, -0.06, 0.1, x=0.3); return {}
def b_jam():
    RC(0.55, 1.0, (0, 0, 0.52), "red", lv=2); o = RC(0.58, 1.1, (0, 0, 0.56), "glass", lv=2); o.data.materials[0] = mat((0.9, 0.95, 1.0), 0.1); o.scale = (1.02, 1.02, 1.0)
    RC(0.52, 0.22, (0, 0, 1.18), "red", lv=1); RB((0, 0, 1.3), (1.3, 1.3, 0.1), "white", lv=2)
    for k in range(8): a = k*TAU/8; S(0.06, (0.4*math.cos(a), 0.4*math.sin(a), 1.36), (1, 1, 0.5), "red")
    S(0.12, (0.25, -0.62, 0.7), (1, 0.4, 1.2), "red"); S(0.06, (0.25, -0.68, 0.84), (1.4, 0.4, 0.7), "green")
    face(0.75, -0.58, 0.2, 0.11, x=-0.1, mouth_dz=0.3, mr=0.1); return {}
def b_ham():
    o = S(0.7, (0, 0.1, 0.75), (1.0, 1.3, 0.95), "pink"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2
    RK(0.45, 1.0, (0, -0.95, 0.9), "pink", (rad(-80), 0, 0), lv=2); RC(0.1, 0.5, (0, -1.5, 1.0), "white", (R90, 0, 0), lv=1); S(0.17, (0, -1.75, 1.0), (1, 0.8, 1.2), "white")
    for k in range(5): a = k*1.1; RB((0.5*math.cos(a), 0.3+0.3*math.sin(a), 1.2), (0.16, 0.16, 0.05), "tan", lv=1)
    face(1.05, -0.45, 0.24, 0.12, mouth_dz=0.3, mr=0.11); return {}
def b_bun():
    o = S(0.8, (0, 0, 0.55), (1.0, 1.0, 0.75), "tan"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2
    RC(0.78, 0.25, (0, 0, 0.14), "straw", lv=1)
    for k in range(9): a = k*0.7; S(0.05, (0.4*math.cos(a), 0.4*math.sin(a), 1.1), (1.6, 0.8, 0.5), "cream", rot=(0, 0, a))
    face(0.7, -0.72, 0.22, 0.11, mouth_dz=0.3, mr=0.1); return {}
def b_mug():
    RC(0.55, 1.2, (0, 0, 0.62), "blue", lv=2); Cy(0.5, 0.04, (0, 0, 1.2), "chocolate", verts=24); RB((0, 0, 1.22), (1.05, 1.05, 0.08), "blue", lv=2)
    To(0.3, 0.09, (0.68, 0, 0.65), "blue", (R90, 0, 0)); RB((0, 0, 0.25), (1.1, 1.1, 0.15), "navy", lv=1)
    for k in range(3): S(0.07, (-0.15+0.15*k, 0, 1.4+0.15*k), (1, 1, 1.5), "lgrey")
    face(0.85, -0.55, 0.2, 0.11, mouth_dz=0.3, mr=0.1); return {}
def b_pin():
    Cy(0.03, 1.0, (0, 0, 0.5), "silver", verts=12); Co(0.03, 0.12, (0, 0, 0.06), "silver", (math.pi, 0, 0), verts=12)
    RC(0.35, 0.55, (0, 0, 1.25), "red", lv=2); RK(0.42, 0.3, (0, 0, 1.6), "red", lv=2, r2=0.2); RC(0.55, 0.15, (0, 0, 1.0), "red", lv=1)
    face(1.3, -0.38, 0.16, 0.09, mouth_dz=0.25, mr=0.08); return {}
def b_elf():
    RB((0, 0, 0.75), (0.75, 0.6, 0.7), "green", lv=2); RB((0, 0, 0.42), (0.8, 0.62, 0.15), "red", lv=1); S(0.07, (0, -0.32, 0.42), (1, 0.5, 1), "gold")
    S(0.42, (0, 0, 1.4), (1, 1, 1), "peach"); RK(0.46, 0.9, (0, 0.05, 2.0), "green", lv=2); S(0.11, (0, 0.15, 2.45), (1, 1, 1), "white"); RC(0.5, 0.12, (0, 0, 1.68), "red", lv=1)
    for sx in (-1, 1): RK(0.1, 0.35, (sx*0.48, 0.0, 1.45), "peach", (0, rad(sx*95), 0), lv=1)
    for sx in (-1, 1): RC(0.08, 0.5, (sx*0.45, -0.05, 0.75), "green", (0, rad(sx*15), 0), lv=1); S(0.1, (sx*0.52, -0.08, 0.48), (1, 1, 1), "peach")
    legs2("green", 0, 0.3, 0.09, 0.2, foot="red"); face(1.45, -0.4, 0.15, 0.09, mouth_dz=0.28, mr=0.08); return {}
def b_ape():
    RB((0, 0, 0.85), (1.2, 0.9, 1.0), "dkbrown", lv=2); RB((0, -0.4, 0.75), (0.7, 0.3, 0.6), "tan", lv=2)
    S(0.45, (0, -0.15, 1.6), (1, 0.9, 0.95), "dkbrown"); S(0.3, (0, -0.42, 1.5), (1.1, 0.6, 0.85), "tan"); S(0.2, (0, -0.52, 1.72), (1.4, 0.5, 0.6), "tan")
    for sx in (-1, 1): S(0.12, (sx*0.46, -0.15, 1.62), (0.6, 1, 1), "dkbrown"); S(0.07, (sx*0.5, -0.17, 1.62), (0.5, 1, 1), "tan")
    for sx in (-1, 1): RC(0.13, 1.0, (sx*0.72, -0.1, 0.6), "dkbrown", (0, rad(sx*8), 0), lv=1); S(0.18, (sx*0.78, -0.15, 0.12), (1.2, 1.4, 0.6), "tan")
    legs2("dkbrown", 0, 0.35, 0.15, 0.3, foot="tan"); face(1.65, -0.55, 0.16, 0.09, mouth_dz=0.3, mr=0.1)
    for sx in (-1, 1): S(0.03, (sx*0.06, -0.73, 1.45), (1, 0.6, 1.4), "dkbrown")
    return {}
def b_emu():
    o = S(0.6, (0, 0.1, 1.1), (1.0, 1.25, 0.9), "brown"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2
    for k in range(10): a = k*0.63; S(0.16, (0.55*math.cos(a), 0.1+0.65*math.sin(a), 1.1+0.3*math.cos(a*1.7)), (1, 1, 1.5), "dkbrown" if k % 2 else "brown")
    RC(0.12, 1.0, (0, -0.4, 1.75), "tan", (rad(-15), 0, 0), lv=1); S(0.26, (0, -0.55, 2.3), (1, 1.1, 0.95), "tan")
    Co(0.07, 0.3, (0, -0.85, 2.25), "dkgrey", (R90, 0, 0)); S(0.05, (0, -0.5, 2.55), (1, 1, 1.6), "dkbrown")
    legs2("dkgrey", 0, 0.7, 0.05, 0.22, foot="dkgrey"); face(2.38, -0.72, 0.12, 0.08, mouth_dz=0.0, mr=0.0, tongue=False); return {}
def b_yak():
    h = quad_meta((0.35, 0.22, 0.12), (0.5, 0.35, 0.2), (0.55, 0.4, 0.25), (0.2, 0.12, 0.06), ear="round", tail="bushy", snout_len=0.05)
    for k in range(12): a = k*0.52; S(0.2, (0.6*math.cos(a), 0.05+0.7*math.sin(a)*0.8, 0.45), (1, 1, 1.8), (0.3, 0.18, 0.1), name="Hair")
    for sx in (-1, 1): RC(0.07, 0.6, (sx*0.45, -0.55, 1.85), "ivory", (0, rad(sx*55), 0), lv=1); S(0.08, (sx*0.7, -0.55, 2.05), (1, 1, 1), "ivory")
    for k in range(4): S(0.12, (-0.2+0.13*k, -0.72, 1.82), (1, 1, 1.4), (0.3, 0.18, 0.1), name="Fringe")
    return h
# ---------------------------------------------------------------- level 2
def b_sock():
    RC(0.42, 1.2, (0, 0.2, 0.95), "red", lv=2); RC(0.42, 0.95, (0, -0.3, 0.42), "red", (R90, 0, 0), lv=2); S(0.43, (0, -0.75, 0.42), (1, 1, 1), "white")
    RC(0.46, 0.25, (0, 0.2, 1.5), "white", lv=1); S(0.4, (0, 0.45, 0.42), (1, 0.9, 1), "white"); To(0.44, 0.04, (0, 0.2, 1.3), "white"); To(0.44, 0.04, (0, 0.2, 1.15), "white")
    face(0.95, -0.2, 0.17, 0.1, mouth_dz=0.28, mr=0.09); return {}
def b_lamp():
    g = [mat((1.0, 0.8, 0.3), 0.5, 0.25)]
    RC(0.5, 0.15, (0, 0, 0.08), "navy", lv=1); RC(0.06, 1.1, (0, 0, 0.65), "gold", lv=1)
    o = RK(0.8, 0.75, (0, 0, 1.5), "yellow", (0, 0, 0), lv=1, r2=0.4); o.data.materials[0] = g[0]
    o = S(0.18, (0, 0, 1.2), (1, 1, 1.3), "white"); o.data.materials[0] = mat((1, 0.95, 0.7), 0.3, 1.5); g.append(o.data.materials[0])
    face(1.55, -0.62, 0.2, 0.11, mouth_dz=0.3, mr=0.1); return {"glow": g}
def b_door():
    RB((0, 0.1, 1.15), (1.3, 0.25, 2.3), "navy", lv=1); RB((0, 0.0, 1.15), (1.1, 0.12, 2.1), "brown", lv=1)
    RB((0, -0.08, 1.65), (0.75, 0.05, 0.6), "wood", lv=1); RB((0, -0.08, 0.6), (0.75, 0.05, 0.7), "wood", lv=1)
    S(0.08, (0.4, -0.12, 1.1), (1, 1, 1), "gold"); RB((0, 0, 2.38), (1.4, 0.3, 0.16), "navy", lv=1)
    S(0.3, (0, -0.1, 1.95), (1, 0.3, 0.7), "glass"); face(1.72, -0.12, 0.18, 0.1, mouth_dz=0.0, mr=0.0, tongue=False); smile(1.48, -0.13, 0.1); return {}
def b_lock():
    RB((0, 0, 0.7), (1.3, 0.7, 1.2), "gold", lv=2); To(0.42, 0.1, (0, 0, 1.45), "silver", (R90, 0, 0)); RB((0, 0, 1.2), (1.05, 0.5, 0.35), "gold", lv=1)
    S(0.1, (0, -0.37, 0.65), (1, 0.4, 1), "charcoal"); RB((0, -0.37, 0.45), (0.08, 0.04, 0.3), "charcoal", lv=1)
    face(1.0, -0.37, 0.2, 0.11, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.85, -0.38, 0.08); return {}
def b_nest():
    To(0.75, 0.3, (0, 0, 0.35), "brown", scale=(1, 1, 0.8)); Cy(0.6, 0.1, (0, 0, 0.35), "dkbrown", verts=24)
    import random; random.seed(3)
    for k in range(26): a = random.uniform(0, TAU); RC(0.025, random.uniform(0.5, 0.9), (0.78*math.cos(a), 0.78*math.sin(a), 0.4+random.uniform(-0.1, 0.15)), ["tan", "wood", "straw"][k % 3], (rad(random.uniform(60, 120)), 0, a+rad(random.uniform(-30, 30))), lv=0)
    for (x, y, c) in [(-0.25, -0.1, "sky"), (0.25, -0.05, "mint"), (0, 0.3, "pink")]: S(0.22, (x, y, 0.6), (1, 1, 1.25), c)
    face(0.5, -0.95, 0.22, 0.11, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.3, -0.98, 0.1); return {}
def b_shoe():
    RB((0, 0, 0.18), (1.1, 2.2, 0.3), "white", lv=2); RB((0, 0.1, 0.6), (0.95, 1.7, 0.7), "red", lv=2); RB((0, -0.75, 0.42), (0.9, 0.7, 0.4), "white", lv=2)
    RB((0, 0.55, 0.95), (0.6, 0.6, 0.35), "red", lv=2); RB((0, 0.9, 0.95), (0.62, 0.25, 0.45), "white", lv=1)
    for k in range(3): RB((0, -0.15+0.25*k, 0.98-0.05*k), (0.5, 0.06, 0.06), "white", lv=1)
    RB((0.47, 0.2, 0.55), (0.06, 0.6, 0.2), "white", lv=1, rot=(0, 0, rad(-20)))
    face(0.7, -0.6, 0.18, 0.1, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.5, -0.82, 0.1); return {}
def b_boot():
    RC(0.42, 1.3, (0, 0.15, 1.0), "brown", lv=2); RB((0, -0.3, 0.3), (0.95, 1.6, 0.5), "brown", lv=2); RB((0, -0.2, 0.08), (1.0, 1.75, 0.16), "dkbrown", lv=1)
    RC(0.46, 0.2, (0, 0.15, 1.65), "tan", lv=1); RB((0, -0.3, 0.6), (0.3, 0.6, 0.12), "tan", lv=1); To(0.1, 0.03, (0, 0.55, 1.72), "tan", (R90, 0, 0))
    face(1.15, -0.28, 0.16, 0.09, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.92, -0.3, 0.09); return {}
def b_coat():
    RB((0, 0, 1.0), (1.3, 0.6, 1.6), "blue", lv=2); RB((0, 0, 0.3), (1.4, 0.65, 0.3), "blue", lv=2)
    for sx in (-1, 1): RC(0.2, 1.2, (sx*0.78, 0, 1.15), "blue", (0, rad(sx*8), 0), lv=2); RC(0.21, 0.15, (sx*0.85, 0, 0.6), "navy", lv=1); RB((sx*0.45, -0.3, 0.55), (0.35, 0.05, 0.3), "navy", lv=1)
    for sx in (-1, 1): RB((sx*0.3, -0.32, 1.7), (0.4, 0.06, 0.35), "navy", rot=(0, rad(sx*-30), 0), lv=1)
    for k in range(3): S(0.07, (0, -0.32, 1.45-0.35*k), (1, 0.5, 1), "gold")
    face(1.2, -0.32, 0.2, 0.11, x=0, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.98, -0.34, 0.09); return {}
def b_hand():
    RB((0, 0, 0.9), (1.2, 0.4, 1.1), "peach", lv=2)
    for i, (x, h, z) in enumerate([(-0.45, 0.6, 1.6), (-0.15, 0.8, 1.7), (0.15, 0.75, 1.68), (0.45, 0.55, 1.6)]): RC(0.14, h, (x, 0, z), "peach", lv=2)
    RC(0.15, 0.6, (-0.75, -0.05, 1.0), "peach", (0, rad(-35), 0), lv=2); RC(0.3, 0.5, (0, 0, 0.3), "peach", lv=2); RC(0.32, 0.2, (0, 0, 0.1), "sky", lv=1)
    face(1.0, -0.22, 0.2, 0.11, mouth_dz=0.3, mr=0.1); return {}
def b_foot():
    RB((0, 0.2, 0.3), (0.95, 1.6, 0.45), "peach", lv=2); RC(0.32, 0.6, (0, 0.6, 0.65), "peach", lv=2)
    for i, (x, r) in enumerate([(-0.33, 0.14), (-0.12, 0.11), (0.06, 0.1), (0.22, 0.09), (0.36, 0.08)]): S(r, (x, -0.75-(0.05*i if i else 0), r), (1, 1.1, 0.9), "peach"); S(r*0.6, (x, -0.8-r*0.5, r*1.3), (1, 1, 0.5), "pink")
    face(0.5, -0.55, 0.2, 0.1, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.3, -0.62, 0.09); return {}
def b_nose():
    o = S(0.55, (0, 0, 0.9), (0.9, 1.1, 1.0), "peach"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2
    RB((0, 0.2, 1.4), (0.5, 0.5, 0.9), "peach", lv=2); S(0.5, (0, -0.1, 0.65), (1.2, 1.0, 0.75), "peach")
    for sx in (-1, 1): S(0.1, (sx*0.26, -0.4, 0.45), (1, 0.8, 0.6), "pink")
    S(0.14, (-0.15, -0.5, 1.05), (1, 0.6, 1), "white"); face(1.6, -0.3, 0.2, 0.11, mouth_dz=0.0, mr=0.0, tongue=False); smile(1.35, -0.35, 0.1); return {}
def b_wave():
    pts = [(-1.3, 0), (1.3, 0), (1.3, 0.3), (1.0, 0.9), (0.5, 1.5), (0.0, 1.85), (-0.6, 1.9), (-0.9, 1.6), (-0.8, 1.35), (-0.55, 1.4), (-0.45, 1.6), (-0.6, 1.72), (-0.4, 1.75), (-0.1, 1.55), (0.3, 1.2), (0.6, 0.7), (0.6, 0.3), (-1.3, 0.3)]
    o = Fp(pts, (0, 0, 0), 0.9, "blue"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2; smooth(o)
    for (x, z, r) in [(-0.9, 1.65, 0.22), (-0.55, 1.95, 0.2), (-0.15, 1.9, 0.17), (0.3, 1.65, 0.15), (-1.0, 1.3, 0.12)]: S(r, (x, 0, z), (1, 1, 1), "white")
    S(0.1, (-1.3, -0.2, 1.1), (1, 1, 1), "white"); S(0.08, (-1.5, -0.1, 1.4), (1, 1, 1), "white")
    face(1.0, -0.46, 0.22, 0.11, x=0.3, mouth_dz=0.3, mr=0.1); return {"sway": 5, "yawaxis": 1}
def b_road():
    body = E((0, 0, 0))
    RB((0, 0, 0.3), (1.8, 2.8, 0.45), "dkgrey", body, lv=1); RB((0, 0, 0.1), (2.0, 3.0, 0.2), "grey", body, lv=1)
    for k in range(4): RB((0, -1.0+0.7*k, 0.55), (0.14, 0.4, 0.04), "yellow", body, lv=1)
    for sx in (-1, 1): RB((sx*0.8, 0, 0.55), (0.1, 2.7, 0.04), "white", body, lv=1)
    RC(0.04, 1.0, (0.75, -0.9, 0.9), "lgrey", parent=body, lv=1); RB((0.75, -0.9, 1.45), (0.4, 0.06, 0.4), "red", body, lv=1); S(0.14, (0.75, -0.94, 1.45), (1, 0.4, 1), "white", body)
    face(0.45, -1.42, 0.3, 0.13, parent=body, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.2, -1.44, 0.12, parent=body); return {"body": body}
def b_bone():
    RC(0.2, 1.6, (0, 0, 1.0), "ivory", (0, R90, 0), lv=2)
    for sx in (-1, 1):
        for dz in (-0.25, 0.25): S(0.3, (sx*0.9, 0, 1.0+dz), (1, 1, 1), "ivory")
    face(1.12, -0.2, 0.18, 0.1, mouth_dz=0.26, mr=0.09); return {}
def b_soap():
    RB((0, 0, 0.45), (1.5, 1.0, 0.7), "pink", lv=2); RB((0, 0, 0.75), (0.9, 0.5, 0.12), "hotpink", lv=1)
    for k in range(6): o = S(0.08+0.05*(k % 3), (-0.5+0.22*k, -0.2+0.15*math.sin(k), 1.0+0.25*(k % 3)), (1, 1, 1), "white"); o.data.materials[0] = mat((0.9, 0.95, 1.0), 0.15)
    face(0.5, -0.5, 0.25, 0.12, mouth_dz=0.3, mr=0.11); return {}
def b_salt():
    RC(0.45, 1.1, (0, 0, 0.6), "white", lv=2); RC(0.42, 0.3, (0, 0, 1.3), "silver", lv=2)
    for k in range(7): a = k*TAU/7; S(0.035, (0.22*math.cos(a), 0.22*math.sin(a), 1.47), (1, 1, 0.6), "charcoal")
    S(0.04, (0, 0, 1.47), (1, 1, 0.6), "charcoal"); RB((0, -0.44, 0.55), (0.5, 0.05, 0.4), "sky", lv=1)
    face(0.8, -0.45, 0.17, 0.1, mouth_dz=0.28, mr=0.09); return {}
def b_rice():
    RK(0.7, 0.6, (0, 0, 0.3), "white", (math.pi, 0, 0), lv=2, r2=0.5); To(0.7, 0.05, (0, 0, 0.6), "red")
    o = S(0.6, (0, 0, 0.6), (1, 1, 0.75), "ivory"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 1
    for k in range(14): a = k*0.9; S(0.06, (0.4*math.cos(a)*(1-0.05*k), 0.4*math.sin(a)*(1-0.05*k), 0.95+0.08*math.cos(k)), (1.6, 0.8, 0.7), "white", rot=(0, 0, a))
    for sx in (-1, 1): RC(0.03, 1.2, (0.35+sx*0.08, 0.1, 1.2), "wood", (rad(-20), rad(sx*5), 0), lv=1)
    face(0.35, -0.7, 0.2, 0.1, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.15, -0.72, 0.09); return {}
def b_soup():
    RK(0.75, 0.6, (0, 0, 0.32), "red", (math.pi, 0, 0), lv=2, r2=0.55); To(0.76, 0.06, (0, 0, 0.62), "red"); Cy(0.68, 0.04, (0, 0, 0.62), "orange", verts=32)
    for (x, y, c) in [(-0.25, 0.1, "green"), (0.2, -0.15, "yellow"), (0.1, 0.3, "green")]: S(0.09, (x, y, 0.66), (1, 1, 0.4), c)
    RC(0.04, 1.2, (0.4, 0.2, 1.1), "silver", (rad(-25), rad(20), 0), lv=1); S(0.16, (0.65, 0.42, 1.6), (1, 1.3, 0.4), "silver")
    for k in range(3): S(0.07, (-0.2+0.2*k, 0, 0.95+0.2*k), (1, 1, 1.5), "lgrey")
    face(0.38, -0.74, 0.22, 0.11, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.18, -0.76, 0.1); return {}
def b_pear():
    o = S(0.6, (0, 0, 0.6), (1, 1, 0.95), "lime"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2
    o = S(0.42, (0, 0, 1.3), (1, 1, 1.1), "lime"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2
    RC(0.035, 0.4, (0.05, 0, 1.85), "brown", (0, rad(8), 0), lv=1); S(0.2, (0.3, 0, 1.95), (1.4, 0.3, 0.6), "green", rot=(0, rad(-20), 0))
    S(0.07, (-0.3, -0.5, 1.4), (1, 0.4, 1.3), "white"); face(0.85, -0.55, 0.2, 0.11, mouth_dz=0.3, mr=0.1); return {}
def b_kiwi():
    Cy(0.8, 0.5, (0, 0, 0.8), "brown", (R90, 0, 0), verts=32); Cy(0.74, 0.52, (0, 0, 0.8), "lgreen", (R90, 0, 0), verts=32); Cy(0.25, 0.54, (0, 0, 0.8), "cream", (R90, 0, 0), verts=24)
    for k in range(14): a = k*TAU/14; S(0.035, (0.38*math.cos(a), -0.28, 0.8+0.38*math.sin(a)), (1, 0.6, 1.6), "charcoal", rot=(0, a, 0))
    face(1.15, -0.28, 0.2, 0.1, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.95, -0.3, 0.1); return {}
def b_taco():
    for sy in (-1, 1): h = halfdisc((0, sy*0.28, 0.75), 0.75, 0.1, "yellow", flip=True, segs=24); h.rotation_euler = (rad(sy*-10), 0, 0)
    RB((0, 0, 0.35), (1.4, 0.55, 0.3), "yellow", lv=1)
    for (x, c, r) in [(-0.4, "green", 0.16), (-0.15, "red", 0.14), (0.1, "orange", 0.15), (0.35, "green", 0.14), (0.5, "red", 0.1), (-0.5, "yellow", 0.1)]: S(r, (x, 0, 1.3+0.1*math.sin(x*5)), (1, 1, 0.7), c)
    face(0.75, -0.45, 0.22, 0.11, mouth_dz=0.0, mr=0.0, tongue=False); smile(0.55, -0.48, 0.1); return {}
def b_crow():
    S(0.4, (0, 0.05, 1.05), (0.9, 1.3, 0.85), "charcoal"); S(0.3, (0, -0.42, 1.4), (1, 1, 1), "charcoal"); Co(0.08, 0.3, (0, -0.78, 1.36), "dkgrey", (R90, 0, 0))
    for k in range(3): S(0.11, (0.1*(k-1), 0.6, 1.0), (0.4, 1.2, 1.4), "charcoal", rot=(rad(-35), 0, rad(k*12-12)))
    legs2("dkgrey", 0, 0.55, 0.03, 0.12, foot="dkgrey"); eyes(1.48, -0.6, 0.13, 0.08); smile(1.18, -0.7, 0.07, tongue=False)
    return {"wings": wingpair(0.0, 1.15, "charcoal", 0.6, "oval", 0.35), "flap": 35}
def b_dove():
    S(0.4, (0, 0.05, 1.05), (0.9, 1.3, 0.85), "white"); S(0.28, (0, -0.45, 1.38), (1, 1, 1), "white"); Co(0.06, 0.22, (0, -0.75, 1.34), "orange", (R90, 0, 0))
    for k in range(3): S(0.1, (0.1*(k-1), 0.6, 1.0), (0.4, 1.2, 1.4), "white", rot=(rad(-35), 0, rad(k*12-12)))
    RC(0.025, 0.6, (0.15, -0.85, 1.25), "dkgreen", (0, R90, 0), lv=0)
    for k in range(4): S(0.07, (-0.1+0.17*k, -0.86, 1.3+0.05*(k % 2)), (1.3, 0.3, 0.6), "green")
    legs2("orange", 0, 0.5, 0.025, 0.1, foot="orange"); face(1.45, -0.62, 0.12, 0.08, mouth_dz=0.3, mr=0.0, tongue=False)
    return {"wings": wingpair(0.0, 1.15, "white", 0.6, "oval", 0.35), "flap": 35}
def b_bull():
    h = quad_meta((0.35, 0.2, 0.12), (0.45, 0.28, 0.18), (0.5, 0.32, 0.22), (0.2, 0.1, 0.05), ear="round", tail="long", snout_len=0.1)
    for sx in (-1, 1): RC(0.07, 0.55, (sx*0.42, -0.55, 1.85), "ivory", (rad(-20), rad(sx*60), 0), lv=1); S(0.08, (sx*0.68, -0.62, 2.0), (1, 1, 1), "ivory")
    To(0.08, 0.025, (0, -1.5, 1.12), "gold", (R90, 0, 0)); return h
def b_lamb():
    h = quad_meta("white", "cream", "peach", (0.3, 0.25, 0.25), ear="floppy", tail="short", size=0.95)
    import random; random.seed(5)
    for k in range(22): a = random.uniform(0, TAU); b = random.uniform(0.3, 2.6); S(0.17, (0.55*math.cos(a)*math.sin(b), 0.05+0.75*math.sin(a)*math.sin(b), 0.85+0.5*math.cos(b)), (1, 1, 1), "white", name="Wool")
    for k in range(5): S(0.13, (-0.2+0.1*k, -0.6, 1.85+0.05*math.sin(k)), (1, 1, 1), "white", name="Fringe")
    return h
def b_pony():
    h = quad_s((0.95, 0.75, 0.85), "cream", ear="point", tail="long", snout=((0.95, 0.75, 0.85), "pink"), legs_c=(0.95, 0.75, 0.85))
    cols = ["red", "orange", "yellow", "green", "blue", "purple"]
    for k in range(6): RB((0, -0.55+0.14*k, 1.75-0.03*k), (0.16, 0.16, 0.4), cols[k], lv=1); RB((0.42, 1.05, 1.1+0.02*k), (0.14, 0.14, 0.14), cols[k], lv=1)
    for k in range(6): S(0.09, (0.45+0.03*k, 1.1+0.08*k, 1.45-0.16*k), (1, 1, 1.5), cols[k])
    return {"legs": [], **h}
def b_toad():
    EL = [((0, 0, 0.6), 0.62, (1.15, 1.0, 0.7)), ((0, -0.45, 0.75), 0.42, (1.0, 0.8, 0.7))]
    for sx in (-1, 1):
        EL.append(((sx*0.33, -0.45, 1.12), 0.2, None)); EL.append(((sx*0.62, -0.3, 0.3), 0.23, (0.9, 1.0, 0.7))); EL.append(((sx*0.85, -0.5, 0.15), 0.2, (1.1, 1.3, 0.5)))
        EL.append(((sx*0.55, 0.45, 0.35), 0.25, None)); EL.append(((sx*0.72, 0.6, 0.15), 0.18, (1.1, 1.2, 0.5)))
    def region(c, n):
        if n.z < -0.35 and c.z < 0.6 and abs(c.x) < 0.5: return 1
        if c.y < -0.55 and c.z < 0.75 and abs(c.x) < 0.45 and n.y < -0.4: return 1
        return 0
    metachar(EL, [], [(0.55, 0.4, 0.2), "sand"], region)
    for k in range(9): a = k*0.75; S(0.08, (0.45*math.cos(a), 0.1+0.4*math.sin(a), 1.0+0.1*math.cos(k)), (1, 1, 0.7), (0.4, 0.28, 0.12), name="Wart")
    eyes(1.22, -0.62, 0.33, 0.14); smile(0.6, -0.8, 0.26, tongue=False); return {}
def b_hawk():
    S(0.42, (0, 0.05, 1.1), (0.9, 1.3, 0.9), "brown"); S(0.32, (0, -0.05, 0.95), (0.7, 0.9, 0.7), "cream"); S(0.3, (0, -0.42, 1.48), (1, 1, 1), "brown")
    Co(0.07, 0.22, (0, -0.72, 1.42), "yellow", (rad(100), 0, 0)); S(0.05, (0, -0.8, 1.36), (1, 1, 1), "yellow")
    for sx in (-1, 1): S(0.08, (sx*0.14, -0.6, 1.6), (1.3, 0.6, 0.5), "dkbrown")
    for k in range(3): S(0.12, (0.1*(k-1), 0.65, 1.05), (0.4, 1.2, 1.4), "rust", rot=(rad(-35), 0, rad(k*12-12)))
    legs2("yellow", 0, 0.55, 0.035, 0.14, foot="yellow"); eyes(1.55, -0.62, 0.13, 0.08); smile(1.28, -0.68, 0.05, tongue=False)
    return {"wings": wingpair(0.0, 1.2, "brown", 0.7, "oval", 0.38), "flap": 32}
def b_moth():
    RC(0.12, 0.8, (0, 0, 1.0), "tan", lv=2); S(0.15, (0, 0, 1.45), (1, 1, 1), "tan"); wings = []
    for k in range(5): S(0.1, (0, 0, 1.05+0.12*k), (1.3, 1.3, 0.5), "beige", name="Fuzz")
    for sx in (-1, 1):
        p = E((sx*0.06, 0, 1.1)); wings.append(p)
        S(0.42, (sx*0.45, 0, 1.2), (1, 0.15, 0.85), "beige", p, rot=(0, rad(sx*-12), 0)); S(0.3, (sx*0.35, 0, 0.72), (1, 0.15, 0.8), "tan", p, rot=(0, rad(sx*10), 0))
        S(0.12, (sx*0.5, -0.05, 1.25), (1, 0.3, 1), "brown", p); S(0.06, (sx*0.5, -0.08, 1.25), (1, 0.3, 1), "cream", p)
        for k in range(5): S(0.03, (sx*0.1, -0.02, 1.62+0.06*k), (1, 1, 1), "brown", rot=None); Cy(0.01, 0.3, (sx*0.12, 0, 1.65), "brown", (0, rad(sx*-30), 0))
    face(1.48, -0.13, 0.07, 0.05, mouth_dz=0.1, mr=0.04, tongue=False); return {"wings": wings, "flap": 40}
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}
