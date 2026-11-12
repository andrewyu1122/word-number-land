# Metaball -> mesh -> proportional pulls -> Subdivision Surface(2) -> Shade Smooth. Faces -Y, stands on z=0.
def metachar(elems, pulls, mats, region, res=0.085, lv=2, thresh=0.4, rs=1.3):
    mb = bpy.data.metaballs.new("mb"); mb.resolution = res; mb.threshold = thresh
    mo = bpy.data.objects.new("mbo", mb); scene.collection.objects.link(mo)
    for e in elems:
        el = mb.elements.new(); el.co = e[0]; el.radius = e[1] * rs
        if len(e) > 2 and e[2]:
            el.type = 'ELLIPSOID'; el.size_x, el.size_y, el.size_z = e[2]
        el.stiffness = e[3] if len(e) > 3 else 2.0
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(mo.evaluated_get(dg)); bpy.data.objects.remove(mo, do_unlink=True)
    o = bpy.data.objects.new("Body", me); scene.collection.objects.link(o)
    for (center, direction, radius, strength) in pulls:      # proportional-editing style pull (smooth falloff)
        c = Vector(center); dv = Vector(direction)
        for v in me.vertices:
            d = (v.co - c).length
            if d < radius: v.co += dv * strength * (1 - (d / radius) ** 2) ** 2
    for cname in mats: me.materials.append(mat(cname))
    for p in me.polygons: p.material_index = region(p.center, p.normal)
    m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = lv; m.render_levels = lv
    smooth(o); par(o, ROOT); return o
def quad_meta(body_c, belly_c, muzzle_c, feet_c, ear="round", tail="short", size=1.0, extra_elems=(), extra_pulls=(), spots=None, mane=False, leg_h=0.0, snout_len=0.0, stripes=False):
    s = size; E = []; P = []
    E.append(((0, 0.05*s, 0.85*s), 0.62*s, (1.0, 1.5, 0.95)))
    E.append(((0, -0.62*s, 1.38*s), 0.5*s, None))
    E.append(((0, -1.0*s, 1.22*s), 0.26*s, None))                        # snout
    for (x, y) in [(-0.3, -0.42), (0.3, -0.42), (-0.3, 0.45), (0.3, 0.45)]:
        E.append(((x*s, y*s, (0.42+leg_h)*s), 0.24*s, None)); E.append(((x*s, y*s - 0.03, 0.14*s), 0.22*s, None))
    if tail == "short": E.append(((0, 0.9*s, 1.0*s), 0.18*s, None))
    elif tail == "bushy": E.append(((0.15*s, 1.0*s, 1.0*s), 0.3*s, (0.8, 1.3, 0.8))); E.append(((0.25*s, 1.3*s, 1.3*s), 0.2*s, None))
    elif tail == "long": E += [((0.15*s, 0.9*s, 0.95*s), 0.2*s, None), ((0.3*s, 1.1*s, 1.2*s), 0.17*s, None), ((0.42*s, 1.22*s, 1.45*s), 0.17*s, None), ((0.5*s, 1.3*s, 1.65*s), 0.2*s, None)]
    if mane:
        for k in range(12):
            a = k*TAU/12; E.append(((0.62*s*math.cos(a), -0.42*s, 1.38*s + 0.62*s*math.sin(a)), 0.27*s, None))
    E += list(extra_elems)
    if ear == "round":
        for sx in (-1, 1): E.append(((sx*0.36*s, -0.58*s, 1.82*s), 0.17*s, None))
    elif ear == "point":
        for sx in (-1, 1): P.append(((sx*0.3*s, -0.6*s, 1.8*s), (sx*0.25, -0.05, 1.0), 0.3*s, 0.42*s))
    elif ear == "floppy":
        for sx in (-1, 1): E.append(((sx*0.5*s, -0.6*s, 1.55*s), 0.14*s, (0.6, 0.9, 1.3)))
    P.append(((0, -1.26*s, 1.22*s), (0, -1, 0), 0.28*s, (0.12 + snout_len)*s))     # nose pull
    P += list(extra_pulls)
    def region(c, n):
        if c.z < 0.26*s: return 3
        if c.y < -1.05*s and 0.95*s < c.z < 1.5*s: return 2
        if stripes and c.z > 0.5*s and c.y > -0.35*s and int((c.y + 3.0) * 5.5) % 2 == 0: return 3
        if stripes and c.y < -0.35*s and c.z > 1.05*s and abs(c.x) < 0.5*s and int((c.z + 3.0) * 7) % 2 == 0 and c.y > -0.95*s: return 3
        if mane and (Vector((c.x, 0, c.z)) - Vector((0, 0, 1.38*s))).length > 0.5*s and -0.75*s < c.y < -0.1*s and c.z > 0.75*s: return 4
        if spots and c.z > 1.1*s and -0.35*s < c.y < 0.75*s and n.z > 0.45:
            for (x, y) in [(-0.28, 0.1), (0.3, 0.35), (0.05, -0.15), (-0.2, 0.55), (0.3, -0.25), (-0.05, 0.3)]:
                if (Vector((c.x, c.y)) - Vector((x*s, y*s))).length < 0.12*s: return 1
        if n.z < -0.55 and 0.3*s < c.z < 0.9*s and -0.7*s < c.y < 0.55*s and abs(c.x) < 0.45*s: return 1
        if n.y < -0.75 and c.y < -0.85*s and 0.45*s < c.z < 1.05*s and abs(c.x) < 0.35*s: return 1
        return 0
    mats = [body_c, belly_c, muzzle_c, feet_c] + (["brown"] if mane else [])
    metachar(E, P, mats, region)
    S(0.085*s, (0, -1.4*s, 1.27*s), (1.2, 0.8, 0.8), "black", name="Nose")
    face(1.47*s, -1.1*s, 0.19*s, 0.1*s, mouth_dz=0.3*s, mr=0.09*s)
    return {}
def b_bear():  return quad_meta("brown", "tan", "beige", "dkbrown", ear="round", tail="short")
def b_lion():
    h = quad_meta("tan", "cream", "cream", "brown", ear="round", tail="long", mane=True)
    S(0.2, (0.5, 1.3, 1.72), (1, 1, 1.15), "brown", name="Tuft"); return h
def b_wolf():
    return quad_meta((0.45, 0.55, 0.68), "white", "white", (0.3, 0.38, 0.5), ear="point", tail="bushy", snout_len=0.12)
def b_pig():
    h = quad_meta("pink", "peach", "pink", "hotpink", ear="floppy", tail="short", snout_len=0.08)
    Cy(0.19, 0.06, (0, -1.4, 1.24), "hotpink", (R90, 0, 0), verts=24)
    for sx in (-1, 1): S(0.035, (sx*0.07, -1.44, 1.24), (1, 0.6, 1.3), "mouth")
    sub = To(0.1, 0.035, (0, 1.05, 1.1), "pink", (0, R90, 0)); m = sub.modifiers.new("Sub", 'SUBSURF'); m.levels = 1; return h
def b_deer():
    h = quad_meta((0.72, 0.47, 0.22), "cream", (0.78, 0.55, 0.3), (0.4, 0.25, 0.1), ear="floppy", tail="short", spots=True, leg_h=0.12, size=0.95)
    for sx in (-1, 1):
        for (loc, rot, L) in [((sx*0.22, -0.55, 2.05), (0, rad(sx*12), 0), 0.6), ((sx*0.3, -0.55, 2.15), (0, rad(sx*-55), 0), 0.3), ((sx*0.38, -0.55, 2.32), (0, rad(sx*-40), 0), 0.28)]:
            o = Cy(0.032, L, loc, "dkbrown", rot, verts=10); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 1
    return h
def b_swan():
    E = [((0, 0.15, 0.6), 0.6, (0.9, 1.6, 0.7)), ((0, 0.95, 0.85), 0.22, (0.7, 1.0, 1.0)),
         ((0, -0.5, 0.75), 0.26, None), ((0, -0.68, 1.05), 0.22, None), ((0, -0.76, 1.35), 0.2, None), ((0, -0.72, 1.62), 0.2, None), ((0, -0.6, 1.85), 0.2, None),
         ((0, -0.62, 2.02), 0.3, (1.0, 1.15, 0.9))]
    for sx in (-1, 1): E.append(((sx*0.42, 0.25, 0.85), 0.3, (0.6, 1.3, 0.7)))
    P = [((0, -0.95, 1.98), (0, -1, 0), 0.26, 0.1)]       # slight beak base pull
    def region(c, n):
        if c.y < -0.98 and 1.8 < c.z < 2.15: return 1
        if c.y < -0.85 and 1.85 < c.z < 2.15: return 2
        return 0
    metachar(E, P, ["white", "orange", "black"], region)
    bk = Co(0.11, 0.42, (0, -1.22, 1.97), "orange", (R90, 0, 0), None, 0.04, 14); m = bk.modifiers.new("Sub", 'SUBSURF'); m.levels = 1
    S(0.12, (0, -1.02, 2.0), (1, 0.6, 0.9), "black", name="Mask")
    face(2.1, -0.95, 0.11, 0.065, mouth_dz=0.6, mr=0.0, tongue=False); return {"sway": 3, "yawaxis": 1}
def b_hen():
    E = [((0, 0.05, 0.75), 0.55, (0.95, 1.25, 1.0)), ((0, -0.55, 1.35), 0.36, None), ((0, 0.75, 1.05), 0.26, (0.6, 1.0, 1.3)),
         ((0, -0.55, 1.75), 0.11, None), ((0, -0.42, 1.78), 0.1, None), ((0, -0.68, 1.72), 0.1, None), ((0, -0.86, 1.12), 0.1, None)]
    for sx in (-1, 1): E.append(((sx*0.5, 0.05, 0.8), 0.28, (0.5, 1.1, 0.8)))
    P = [((0, -0.95, 1.3), (0, -1, 0), 0.22, 0.1)]
    def region(c, n):
        if c.z > 1.68 and c.y < -0.3: return 1
        if c.y < -0.75 and 0.95 < c.z < 1.25: return 1
        if n.z < -0.5 and c.z < 0.75: return 2
        return 0
    metachar(E, P, ["brown", "red", "tan"], region)
    bk = Co(0.09, 0.3, (0, -1.05, 1.3), "orange", (R90, 0, 0), None, 0.02, 12); m = bk.modifiers.new("Sub", 'SUBSURF'); m.levels = 1
    legs2("orange", 0, 0.3, 0.04, 0.18, foot="orange")
    face(1.42, -0.86, 0.14, 0.085, mouth_dz=0.5, mr=0.0, tongue=False); return {}
def b_bat():
    EL = [((0, 0, 1.05), 0.42, (0.9, 0.8, 1.0)), ((0, -0.12, 1.55), 0.4, None), ((0, -0.05, 0.62), 0.22, None)]
    for sx in (-1, 1): EL.append(((sx*0.26, -0.1, 1.92), 0.15, None))
    PU = [((0, -0.5, 1.45), (0, -1, 0), 0.3, 0.08)]
    def region(c, n):
        if c.y < -0.25 and 0.75 < c.z < 1.25 and abs(c.x) < 0.3: return 1
        return 0
    metachar(EL, PU, ["purple", "lavender"], region)
    wings = []
    for sx in (-1, 1):
        piv = E((sx*0.38, 0.05, 1.2)); wings.append(piv)
        w = Fp([(0,0.3),(sx*0.6,0.45),(sx*1.3,0.35),(sx*1.5,0.0),(sx*1.1,-0.2),(sx*0.7,-0.35),(sx*0.3,-0.25),(0,-0.3)], (sx*0.38, 0.05, 1.2), 0.06, "purple", piv)
        m = w.modifiers.new("Sub", 'SUBSURF'); m.levels = 2; smooth(w)
        for k in range(3): Cy(0.035, 0.5+0.2*k, (sx*(0.6+0.35*k), 0.02, 1.25-0.05*k), "purple", (0, rad(sx*(75-10*k)), 0), piv, 8)
    for sx in (-1, 1): Co(0.035, 0.14, (sx*0.1, -0.5, 1.28), "white", (R90, 0, 0), None, 0.0, 8)
    face(1.58, -0.5, 0.17, 0.1, mouth_dz=0.26, mr=0.1); return {"wings": wings, "flap": 28}
def b_frog():
    EL = [((0, 0, 0.6), 0.6, (1.1, 1.0, 0.72)), ((0, -0.45, 0.75), 0.4, (1.0, 0.8, 0.7))]
    for sx in (-1, 1):
        EL.append(((sx*0.32, -0.45, 1.12), 0.2, None))                              # eye mounds
        EL.append(((sx*0.6, -0.3, 0.3), 0.22, (0.9, 1.0, 0.7))); EL.append(((sx*0.85, -0.5, 0.15), 0.2, (1.1, 1.3, 0.5)))
        EL.append(((sx*0.55, 0.45, 0.35), 0.24, None)); EL.append(((sx*0.7, 0.6, 0.15), 0.18, (1.1, 1.2, 0.5)))
    def region(c, n):
        if n.z < -0.35 and c.z < 0.6 and abs(c.x) < 0.5: return 1
        if c.y < -0.55 and c.z < 0.75 and abs(c.x) < 0.45 and n.y < -0.4: return 1
        return 0
    metachar(EL, [], ["green", "cream"], region)
    eyes(1.2, -0.62, 0.32, 0.14); smile(0.6, -0.78, 0.26, tongue=False); return {}
def b_camel():
    EL = [((0, 0.1, 1.0), 0.5, (0.9, 1.5, 0.8)), ((0, 0.0, 1.5), 0.36, None), ((0, 0.45, 1.5), 0.34, None),
          ((0, -0.75, 1.3), 0.26, None), ((0, -0.85, 1.7), 0.24, None), ((0, -0.8, 2.05), 0.3, (1.0, 1.2, 0.85))]
    for (x, y) in [(-0.3, -0.45), (0.3, -0.45), (-0.3, 0.5), (0.3, 0.5)]:
        EL.append(((x, y, 0.55), 0.2, None)); EL.append(((x, y, 0.15), 0.2, None))
    EL.append(((0, 0.95, 1.1), 0.14, None))
    PU = [((0, -1.15, 1.98), (0, -1, 0), 0.28, 0.14)]
    for sx in (-1, 1): PU.append(((sx*0.28, -0.78, 2.32), (sx*0.2, 0, 1.0), 0.2, 0.22))
    def region(c, n):
        if c.z < 0.3: return 1
        if c.y < -1.0 and 1.8 < c.z < 2.1: return 2
        return 0
    metachar(EL, PU, ["tan", "brown", "beige"], region)
    S(0.07, (0, -1.3, 2.0), (1.2, 0.8, 0.7), "black", name="Nose"); face(2.12, -1.1, 0.16, 0.09, mouth_dz=0.3, mr=0.08); return {}
def b_zebra():
    h = quad_meta("white", "white", "lgrey", "black", ear="point", tail="long", snout_len=0.1, stripes=True)
    for k in range(5): B((0, -0.15+k*0.17, 1.38), (0.08, 0.1, 0.16), "black", ROOT)
    return h
def b_monkey():
    h = quad_meta("brown", "tan", "tan", "dkbrown", ear="round", tail="long", snout_len=0.05)
    for sx in (-1,1): S(0.17, (sx*0.46, -0.6, 1.5), (0.6, 1, 1), "brown", name="BigEar"); S(0.1, (sx*0.5, -0.64, 1.5), (0.5, 1, 1), "tan", name="BigEarIn")
    S(0.32, (0, -0.88, 1.35), (1.0, 0.45, 0.8), "tan", name="FacePatch"); return h
def b_hamster():
    EL = [((0, 0.05, 0.62), 0.62, (1.0, 1.1, 0.95)), ((0, -0.5, 0.85), 0.42, None), ((0, -0.85, 0.75), 0.2, None)]
    for sx in (-1,1): EL.append(((sx*0.3, -0.45, 1.3), 0.14, None)); EL.append(((sx*0.32, -0.6, 0.72), 0.2, None)); EL.append(((sx*0.25, -0.75, 0.18), 0.17, None)); EL.append(((sx*0.3, 0.35, 0.18), 0.17, None))
    def region(c, n):
        if n.z < -0.4 and c.z < 0.5: return 1
        if c.y < -0.75 and 0.45 < c.z < 1.0: return 1
        if c.z > 0.95 and -0.7 < c.y < 0.4 and n.z > 0.3: return 2
        return 0
    metachar(EL, [], ["orange", "cream", "tan"], region)
    S(0.06, (0, -1.08, 0.8), (1.2, 0.8, 0.7), "pink", name="Nose"); face(0.98, -0.85, 0.17, 0.09, mouth_dz=0.26, mr=0.07); return {}
def b_horse():
    h = quad_meta((0.72, 0.42, 0.15), (0.95, 0.85, 0.7), (0.95, 0.85, 0.7), (0.35, 0.2, 0.08), ear="point", tail="long", snout_len=0.18, leg_h=0.1)
    for k in range(7): RBm = S(0.14, (0, -0.55+k*0.13, 1.72-k*0.04), (1, 1, 1.4), "white", name="Mane")
    S(0.12, (0, -0.95, 1.8), (1, 1, 1.3), "white", name="Fringe"); S(0.22, (0.5, 1.32, 1.62), (1, 1, 1.5), "white", name="TailHair")
    return h
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}
