# Horse Ranch builders — ONE parametric base horse (metaball body + separate neck / head / jaw / legs / tail pivots),
# 16 colour + feature variants, the barn door "egg", and the horse actions (walk, happy, eat, sleep, run).
# Runs on top of the Dino Island helpers (body_blob, head_unit, quad_legs, chain ...).
import random
exec(open(PIPE + "/builders_dino.py", encoding="utf-8").read().split("# ------------------------------------------------------------------ the 16 dinos")[0])

WHITE = (0.97, 0.97, 0.95); BLACKC = (0.045, 0.045, 0.055); HOOF = (0.2, 0.13, 0.08)

def surf(o, d=(0, 1, 0)):
    """first surface hit from point o along d (world space)"""
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    hit, loc, nrm, idx, ob, mw = scene.ray_cast(dg, Vector(o), Vector(d))
    return Vector(loc) if hit else None
def paint(o, fn):
    """re-colour polygons: fn(world centre, world normal) -> colour or None (keep)"""
    bpy.context.view_layer.update(); M = o.matrix_world.copy(); Nm = M.to_3x3(); me = o.data; idx = {}
    for p in me.polygons:
        c = fn(M @ p.center, (Nm @ p.normal).normalized())
        if c is None: continue
        if c not in idx: me.materials.append(mat(c)); idx[c] = len(me.materials) - 1
        p.material_index = idx[c]
def cellspot(c, cell, r, seed=0):
    """True when c is within r of the jittered point of a lattice cell (round spots scattered in 3D)"""
    ix, iy, iz = (math.floor(v / cell) for v in c)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                rr = random.Random((ix + dx) * 7349 + (iy + dy) * 9151 + (iz + dz) * 3571 + seed * 101)
                p = Vector(((ix + dx + 0.2 + 0.6 * rr.random()) * cell, (iy + dy + 0.2 + 0.6 * rr.random()) * cell, (iz + dz + 0.2 + 0.6 * rr.random()) * cell))
                if (Vector(c) - p).length < r: return True
    return False

def horse(coat, mane, belly=None, muzzle=None, hoof=HOOF, legz=0.85, legr=0.125, dx=0.3, dy=0.5, br=0.5, bs=(0.95, 1.45, 0.9), nr=(0.3, 0.23), nl=1.0,
          head=0.39, snout=(0.47, 0.25), eye=(0.17, 0.25), ears=0.38, earw=0.115, mane_style="normal", mane_cols=None, tail="low", tail_cols=None, forelock=True,
          pattern=None, gloss=None, wings=False, horn=False, feather=None, star=False, blaze=False, rear=30, legamp=26, inner_ear="pink"):
    muzzle = muzzle or tuple(v * 0.72 for v in coat); belly = belly or coat
    mcols = mane_cols or [mane]; tcols = tail_cols or mcols
    bz = legz + 0.3
    body = body_blob(coat, belly, [((0, 0.08, bz), br, bs), ((0, 0.52, bz + 0.05), br * 0.82, None), ((0, -0.4, bz + 0.06), br * 0.78, None)], bz=bz, chest=False)
    legs = quad_legs(coat, dx=dx, dy=dy, z=legz, r=legr, foot_c=hoof, nails=False)
    # neck (own mesh, pivots at the shoulders) + head on top of it
    nb = Vector((0, -0.4, bz + 0.18)); ax = Vector((0, -0.5, 0.86)).normalized(); back = Vector((0, 0.86, 0.5)); nt = nb + ax * nl
    npv = E(tuple(nb), name="NeckPiv")
    neck = metachar(chain(nb - ax * 0.12, nt, nr[0], nr[1], 6), [], [coat], lambda c, n: 0, res=0.065); par(neck, npv)
    hpos = nt + Vector((0, -0.06, 0.1))
    hp, jp = head_unit(tuple(hpos), coat, r=head, snout=snout, hs=(1.0, 1.05, 0.95), eye=eye, jaw=True)
    par(hp, npv)
    hmesh = [o for o in hp.children if o.type == 'MESH' and o.name.startswith("Body")][0]
    hy, hz = hpos.y, hpos.z
    paint(hmesh, lambda c, n: muzzle if c.y < hy - snout[0] * 0.8 else None)
    for o in jp.children:
        if o.name.split('.')[0] == "Jaw": o.data.materials[0] = mat(muzzle)
    for sx in (-1, 1):                                                   # nostrils
        p = surf((sx * 0.09, hy - 3, hz + 0.03))
        if p: S(0.04, tuple(p + Vector((0, 0.01, 0))), (1, 0.5, 1.3), "ink", hp, name="Nostril", seg=12, ring=8)
    top = surf((0.2, hy + 0.02, hz + 3), (0, 0, -1)); tz = top.z if top else hz + 0.4
    for sx in (-1, 1):                                                   # ears
        Co(earw, ears, (sx * 0.2, hy + 0.04, tz + ears * 0.36), coat, (rad(-6), rad(sx * 16), 0), hp, 0.02, 12, name="Ear")
        Co(earw * 0.6, ears * 0.72, (sx * 0.2, hy - 0.025, tz + ears * 0.34), inner_ear, (rad(-6), rad(sx * 16), 0), hp, 0.012, 10, name="EarIn")
    ctop = surf((0, hy - 0.16, hz + 3), (0, 0, -1)); cz = ctop.z if ctop else hz + 0.4
    # ---- mane along the back of the neck (follows the neck pivot) + forelock on the head
    def mpt(t, off=0.0): return nb + ax * (nl * t) + back * ((nr[0] + (nr[1] - nr[0]) * t) * 0.78 + off)
    if mane_style in ("normal", "rainbow"):
        for k in range(8):
            t = 0.12 + 0.95 * k / 7; S(0.15, tuple(mpt(t, 0.02)), (0.62, 1.0, 1.2), mcols[k % len(mcols)], npv, (rad(-30), 0, 0), name="Mane")
            S(0.11, tuple(mpt(t, -0.06) + Vector((-0.13, 0, -0.08))), (0.7, 1.0, 1.5), mcols[k % len(mcols)], npv, (rad(-30), rad(-20), 0), name="Mane")
    elif mane_style == "fluffy":
        for k in range(8):
            t = 0.08 + 1.0 * k / 7; c = mcols[k % len(mcols)]
            S(0.23, tuple(mpt(t, 0.06)), (0.95, 1.0, 1.15), c, npv, name="Mane")
            for sx in (-1, 1): S(0.19, tuple(mpt(t, -0.1) + Vector((sx * 0.2, 0, -0.14))), (0.8, 1.0, 1.6), c, npv, (0, rad(sx * 22), 0), name="Mane")
    elif mane_style == "short":
        for k in range(7): t = 0.2 + 0.85 * k / 6; S(0.1, tuple(mpt(t, 0.0)), (0.6, 1.0, 1.0), mcols[k % len(mcols)], npv, name="Mane")
    elif mane_style == "wild":
        rr = random.Random(5)
        for k in range(9):
            t = 0.1 + 1.0 * k / 8; c = mcols[k % len(mcols)]
            S(0.15, tuple(mpt(t, 0.0)), (0.7, 1.0, 1.1), c, npv, name="Mane")
            Co(0.11, 0.5 + 0.2 * rr.random(), tuple(mpt(t, 0.2) + Vector((rr.uniform(-0.08, 0.08), 0.1, 0.05))), c, (rad(-58 - 30 * rr.random()), rad(rr.uniform(-25, 25)), 0), npv, 0.01, 10, name="Mane")
    elif mane_style == "roach":
        for k in range(9):
            t = 0.12 + 0.98 * k / 8; B(tuple(mpt(t, 0.05)), (0.11, 0.13, 0.26), mcols[k % len(mcols)], npv, (rad(-30), 0, 0), bevel=0.03, name="Mane")
    if forelock:
        fc = mcols[0]
        if mane_style == "fluffy":
            S(0.24, (0, hy - 0.1, cz + 0.06), (1.2, 1.1, 0.85), fc, hp, name="Forelock"); S(0.17, (-0.1, hy - 0.3, cz - 0.02), (1, 1, 1.2), fc, hp, name="Forelock")
        elif mane_style == "roach": B((0, hy - 0.02, cz + 0.07), (0.11, 0.16, 0.2), fc, hp, bevel=0.03, name="Forelock")
        elif mane_style == "wild":
            for k, a in enumerate((-35, 0, 30)): Co(0.1, 0.42, (0.06 * (k - 1), hy - 0.12, cz + 0.1), fc, (rad(40), rad(a), 0), hp, 0.01, 10, name="Forelock")
            S(0.15, (0, hy - 0.05, cz + 0.02), (1, 1, 0.8), fc, hp, name="Forelock")
        elif mane_style == "short": S(0.1, (0, hy - 0.08, cz + 0.03), (1, 1, 0.9), fc, hp, name="Forelock")
        else:
            S(0.16, (0, hy - 0.1, cz + 0.03), (1.0, 1.1, 0.8), fc, hp, name="Forelock"); S(0.11, (-0.07, hy - 0.26, cz - 0.03), (0.9, 1, 1.2), mcols[-1], hp, name="Forelock")
    # ---- tail on its own pivot
    bk = surf((0, 3, bz + 0.16), (0, -1, 0)); by = (bk.y if bk else 1.0) - 0.06
    tp = E((0, by, bz + 0.16), name="TailPiv")
    def tpt(d): return (0, by + d[0], bz + 0.16 + d[1])
    if tail in ("low", "fluffy"):
        k_ = 1.35 if tail == "fluffy" else 1.0
        for i, (d, r) in enumerate([((0.08, -0.02), 0.13), ((0.2, -0.2), 0.16), ((0.27, -0.45), 0.17), ((0.3, -0.7), 0.15), ((0.3, -0.92), 0.11)]):
            if bz + 0.16 + d[1] - r * k_ * 1.3 < 0.12: continue
            S(r * k_, tpt(d), (0.9, 0.9, 1.3), tcols[i % len(tcols)], tp, name="Tail")
    elif tail == "high":                                                 # carried high, then falls in an arc
        for i, (d, r) in enumerate([((0.1, 0.1), 0.12), ((0.27, 0.27), 0.14), ((0.48, 0.3), 0.15), ((0.66, 0.16), 0.15), ((0.76, -0.08), 0.14), ((0.8, -0.34), 0.11)]):
            S(r, tpt(d), (0.85, 1.1, 1.1), tcols[i % len(tcols)], tp, name="Tail")
    elif tail == "tuft":                                                 # thin tail + tuft (zebra, donkey)
        Cy(0.05, 0.66, tpt((0.12, -0.28)), coat, (rad(22), 0, 0), tp, 10, name="Tail")
        S(0.14, tpt((0.25, -0.66)), (0.9, 0.9, 1.5), tcols[0], tp, name="Tail")
    h = {"head": hp, "jaw": jp, "legs": legs, "neck": npv, "tail": tp, "rear": rear, "legamp": legamp, "legz": legz, "wings": []}
    # ---- extras
    if feather:                                                          # long hair around the ankles (clydesdale)
        for l in legs:
            x, y = l.location.x, l.location.y
            for k in range(6):
                a = k * TAU / 6; S(legr * 0.8, (x + legr * 0.75 * math.cos(a), y + legr * 0.75 * math.sin(a), 0.2), (1, 1, 1.6), feather, l, name="Feather")
            S(legr * 1.3, (x, y, 0.34), (1, 1, 0.9), feather, l, name="Feather")
    if horn:
        hb = surf((0, hy - 0.2, hz + 3), (0, 0, -1)) or Vector((0, hy - 0.2, hz + 0.4))
        o = Co(0.085, 0.62, (0, hb.y - 0.11, hb.z + 0.24), "gold", (rad(22), 0, 0), hp, 0.012, 16, name="Horn"); o.data.materials[0] = mat("gold", 0.3, 0.5)
        for k in range(4): To(0.075 - 0.014 * k, 0.018, (0, hb.y - 0.035 - 0.05 * k, hb.z + 0.06 + 0.12 * k), (1.0, 0.9, 0.45), (rad(22), 0, 0), hp, name="HornRing")
    if star:
        sp = surf((0, hy - 0.2, hz + 3), (0, 0, -1)) or Vector((0, hy - 0.2, hz + 0.4))
        st = Fp(starpts(0.27, 0.12), (0, sp.y - 0.03, sp.z + 0.015), 0.06, "white", hp, (rad(-58), 0, 0), name="Star")   # lies on the forehead, facing up and forward
    if blaze:
        for k in range(5):
            yy = hy - 0.12 - 0.13 * k; sp = surf((0, yy, hz + 3), (0, 0, -1))
            if sp: S(0.1, (0, yy, sp.z - 0.035), (1.0 - 0.06 * k, 1.1, 0.5), "white", hp, name="Blaze")
    if wings:
        for sx in (-1, 1):
            piv = E((sx * 0.3, 0.02, bz + 0.3), name="WingPiv"); h["wings"].append(piv)
            pts = [(0, 0.16), (sx * 0.45, 0.5), (sx * 1.05, 0.66), (sx * 1.5, 0.56), (sx * 1.5, 0.26), (sx * 1.22, 0.2), (sx * 1.2, -0.04), (sx * 0.9, -0.02), (sx * 0.84, -0.26),
                   (sx * 0.56, -0.2), (sx * 0.46, -0.42), (sx * 0.2, -0.3), (0, -0.3)]
            w = Fp(pts if sx > 0 else pts[::-1], (sx * 0.3, 0.02, bz + 0.3), 0.09, "white", piv, name="Wing"); m = w.modifiers.new("Sub", 'SUBSURF'); m.levels = 2; smooth(w)
            for k in range(4):                                           # feather tips in soft blue
                S(0.17, (sx * (0.62 + 0.26 * k) + sx * 0.3, 0.0, bz + 0.3 - 0.12 + 0.11 * k), (1.0, 0.3, 1.5), (0.72, 0.86, 1.0), piv, (0, rad(sx * 12), 0), name="WingTip")
            S(0.2, (sx * 0.34, 0.02, bz + 0.34), (1.2, 0.8, 1), "white", piv, name="WingRoot")
            piv.rotation_euler = (0, rad(-sx * 34), rad(sx * 8)); piv.scale = (0.88, 0.88, 0.88)
    # ---- coat patterns
    parts = [(body, "body"), (neck, "neck"), (hmesh, "head")] + [(o, "leg") for o in bpy.data.objects if o.name.split('.')[0] in ("Leg", "Hip")]
    if pattern:
        ctx = dict(bz=bz, hy=hy, hz=hz, nb=nb, ax=ax, legz=legz, snout=snout)
        for o, part in parts: paint(o, lambda c, n, part=part: pattern(c, n, part, ctx))
    if gloss is not None:
        for m in bpy.data.materials:
            b = m.node_tree.nodes.get("Principled BSDF") if m.node_tree else None
            if b and tuple(round(v, 3) for v in b.inputs["Base Color"].default_value[:3]) == tuple(round(v, 3) for v in coat):
                b.inputs["Roughness"].default_value = gloss
                for k in ("Specular IOR Level", "Specular"):
                    if k in b.inputs: b.inputs[k].default_value = 0.6
    return h

# ------------------------------------------------------------------ coat patterns
BRN = (0.5, 0.26, 0.1)
def pat_pinto(c, n, part, x):
    bz = x['bz']
    P = [((-0.42, 0.5, bz + 0.2), 0.5), ((-0.35, -0.3, bz - 0.02), 0.34), ((0.42, 0.0, bz + 0.15), 0.48), ((-0.12, -0.72, bz + 0.72), 0.3), ((-0.26, x['hy'] - 0.06, x['hz'] + 0.2), 0.3),
         ((-0.3, 0.5, 0.62), 0.3), ((0.3, -0.5, 0.75), 0.3), ((0.25, 0.75, bz + 0.3), 0.3)]
    for p, r in P:
        if (Vector(c) - Vector(p)).length < r: return BRN
    return None
def pat_appaloosa(c, n, part, x):
    bz = x['bz']
    if part in ("body", "leg") and c.y > 0.22 + 0.5 * max(0, bz - c.z) and c.z > bz - 0.5:
        return (0.12, 0.07, 0.04) if cellspot(c, 0.3, 0.12, 3) else WHITE
    return None
def pat_dapple(c, n, part, x):
    if part in ("body", "neck", "leg") and c.z > 0.55 and cellspot(c, 0.33, 0.105, 8): return (0.88, 0.89, 0.93)
    if part == "leg" and c.z < 0.5: return (0.3, 0.31, 0.36)
    return None
def pat_zebra(c, n, part, x):
    bk = BLACKC
    if part == "body": u = c.y + 0.3 * (c.z - x['bz']); return bk if math.floor((u + 5) / 0.16) % 2 == 0 else None
    if part == "neck": u = (Vector(c) - x['nb']).dot(x['ax']); return bk if math.floor((u + 5) / 0.15) % 2 == 0 else None
    if part == "leg": return bk if math.floor((c.z + 5) / 0.14) % 2 == 0 else None
    if part == "head":
        if c.y < x['hy'] - x['snout'][0] * 0.8: return None
        u = c.y - 0.5 * abs(c.x); return bk if math.floor((u + 5) / 0.12) % 2 == 0 else None
def pat_mustang(c, n, part, x):
    dk = (0.25, 0.14, 0.06)
    if part == "body" and abs(c.x) < 0.085 and n.z > 0.5: return dk
    if part == "leg" and c.z < 0.5: return dk
    return None
def pat_socks(c, n, part, x):
    if part == "leg" and c.z < 0.42: return WHITE
    return None
def pat_bay(c, n, part, x):
    if part == "leg" and c.z < 0.5: return (0.08, 0.06, 0.05)
    return None

# ------------------------------------------------------------------ the 16 horses
def b_chestnut():   return horse((0.66, 0.27, 0.09), (0.3, 0.14, 0.05))
def b_blackhorse(): return horse(BLACKC, (0.02, 0.02, 0.025), muzzle=(0.16, 0.15, 0.17), gloss=0.22, hoof=(0.25, 0.25, 0.28), inner_ear=(0.35, 0.3, 0.33))
def b_whitehorse(): return horse(WHITE, (0.76, 0.77, 0.82), muzzle=(0.93, 0.8, 0.8), hoof=(0.5, 0.48, 0.5))
def b_palomino():   return horse((0.96, 0.7, 0.22), (1.0, 0.95, 0.8), muzzle=(0.82, 0.55, 0.3))
def b_pinto():      return horse(WHITE, (0.4, 0.2, 0.08), muzzle=(0.95, 0.78, 0.76), mane_cols=[(0.4, 0.2, 0.08), WHITE], tail_cols=[WHITE, (0.4, 0.2, 0.08)], pattern=pat_pinto)
def b_appaloosa():  return horse((0.52, 0.3, 0.14), (0.16, 0.09, 0.05), pattern=pat_appaloosa)
def b_dapple():     return horse((0.56, 0.58, 0.65), (0.26, 0.27, 0.32), muzzle=(0.3, 0.3, 0.35), pattern=pat_dapple, hoof=(0.2, 0.2, 0.24))
def b_clydesdale(): return horse((0.5, 0.25, 0.1), (0.05, 0.04, 0.04), legz=0.92, legr=0.175, dx=0.36, dy=0.56, br=0.6, bs=(1.02, 1.42, 0.95), nr=(0.37, 0.29), nl=1.0, head=0.42,
                                 snout=(0.5, 0.28), feather=WHITE, blaze=True, muzzle=(0.95, 0.8, 0.78), rear=24, legamp=22, hoof=(0.3, 0.26, 0.22))
def b_shetland():   return horse((0.4, 0.21, 0.09), (0.98, 0.86, 0.55), legz=0.5, legr=0.14, dy=0.44, br=0.56, bs=(1.02, 1.3, 0.98), nr=(0.33, 0.27), nl=0.72, head=0.42,
                                 snout=(0.4, 0.26), ears=0.2, mane_style="fluffy", tail="fluffy", rear=26)
def b_foal():       return horse((0.88, 0.62, 0.36), (0.5, 0.28, 0.12), legz=1.0, legr=0.095, dx=0.24, dy=0.36, br=0.4, bs=(0.92, 1.3, 0.88), nr=(0.23, 0.19), nl=0.72, head=0.4,
                                 snout=(0.38, 0.23), eye=(0.18, 0.28), ears=0.26, mane_style="short", tail="tuft", tail_cols=[(0.5, 0.28, 0.12)], pattern=pat_socks, legamp=30)
def b_mustang():    return horse((0.82, 0.64, 0.36), (0.2, 0.11, 0.05), mane_style="wild", pattern=pat_mustang, rear=34)
def b_arabian():    return horse((0.33, 0.16, 0.07), (0.03, 0.03, 0.03), legz=0.95, legr=0.105, dx=0.27, br=0.44, bs=(0.92, 1.5, 0.86), nr=(0.25, 0.19), nl=1.12, head=0.36,
                                 snout=(0.46, 0.21), tail="high", star=True, forelock=False, pattern=pat_bay, legamp=30, rear=34)
def b_zebrah():     return horse(WHITE, BLACKC, muzzle=(0.12, 0.1, 0.1), mane_style="roach", mane_cols=[BLACKC, WHITE], tail="tuft", tail_cols=[BLACKC], pattern=pat_zebra,
                                 hoof=(0.1, 0.1, 0.1), ears=0.28, earw=0.12, br=0.52)
def b_donkey():     return horse((0.56, 0.54, 0.56), (0.2, 0.18, 0.18), belly=(0.93, 0.9, 0.84), muzzle=WHITE, legz=0.7, legr=0.12, nl=0.85, head=0.41, snout=(0.44, 0.27),
                                 ears=0.62, earw=0.13, mane_style="roach", tail="tuft", rear=22, hoof=(0.15, 0.13, 0.13))
def b_unicornh():
    RB = [(0.98, 0.3, 0.4), (1.0, 0.6, 0.2), (1.0, 0.88, 0.25), (0.4, 0.82, 0.45), (0.3, 0.65, 1.0), (0.66, 0.42, 0.95)]
    return horse(WHITE, RB[0], muzzle=(1.0, 0.8, 0.85), mane_style="rainbow", mane_cols=RB, tail_cols=RB[::-1], horn=True, hoof=(1.0, 0.75, 0.1), inner_ear=(1.0, 0.7, 0.8))
def b_pegasus():
    return horse(WHITE, (0.55, 0.78, 1.0), muzzle=(0.96, 0.82, 0.84), mane_cols=[(0.55, 0.78, 1.0), (0.78, 0.9, 1.0)], wings=True, hoof=(0.8, 0.84, 0.95), inner_ear=(0.72, 0.86, 1.0))
HORSE_NAMES = ["chestnut", "blackhorse", "whitehorse", "palomino", "pinto", "appaloosa", "dapple", "clydesdale", "shetland", "foal", "mustang", "arabian", "zebrah", "donkey", "unicornh", "pegasus"]

# ------------------------------------------------------------------ horse actions (use helpers from actions.py: crv, _rot, _root, set_body, solve, set_eyes ...)
def _wings(h, f, a):
    for i, wg in enumerate(h.get("wings", [])): _rot(wg, f, dy=a * (1 if i % 2 == 0 else -1))
def h_walk(h):
    PH = (0, math.pi, math.pi + 0.5, 0.5)
    for f in range(1, N + 2):
        t = (f - 1) / N; w = TAU * 2 * t
        _root(f, (0, 0, 0.05 * (1 - math.cos(2 * w)) / 2), (rad(2) * math.sin(2 * w), 0, rad(3) * math.sin(w)))
        for i, l in enumerate(LEGS): _rot(l, f, dx=rad(h["legamp"]) * math.sin(w + PH[i]))
        _rot(h["neck"], f, dx=rad(7) * math.sin(2 * w + 0.6)); _rot(h["head"], f, dx=rad(-5) * math.sin(2 * w + 0.6))
        _rot(h["tail"], f, dx=rad(8) + rad(5) * math.sin(2 * w), dz=rad(16) * math.sin(w))
        _wings(h, f, rad(9) * math.sin(w))
def h_happy(h):       # rear up on the hind legs and neigh
    piv = Vector((0, max(l.y for l in LREST), sum(l.z for l in LREST) / len(LREST)))
    A = [(1, 0), (2, 0), (8, 1), (11, 0.9), (14, 1), (17, 0.9), (22, 0), (25, 0)]
    J = [(1, 0), (6, 0), (8, 1), (10, 0.55), (12, 1), (14, 0.55), (16, 1), (19, 0), (25, 0)]
    for f in range(1, N + 2):
        a = crv(f, A); j = crv(f, J); t = (f - 1) / N
        sw = [(rad(-50) * a + rad(24) * a * math.sin(TAU * 3 * t + math.pi * i)) if i < 2 else rad(6) * a for i in range(len(LEGS))]
        set_body(-rad(h["rear"]) * a, piv, swing=sw, legscale=False, f=f)
        _rot(h["neck"], f, dx=rad(14) * a); _rot(h["head"], f, dx=rad(-16) * a + rad(-5) * j)
        _rot(h["jaw"], f, dx=rad(26) * j)
        _rot(h["tail"], f, dx=rad(24) * a, dz=rad(14) * a * math.sin(TAU * 3 * t))
        _wings(h, f, rad(42) * a + rad(8) * a * math.sin(TAU * 3 * t))
def h_eat(h):         # lower the head to the grass, nibble, then chew
    nk = h["neck"]; hp = h["head"]; jp = h["jaw"]
    piv = Vector((0, max(l.y for l in LREST), sum(l.z for l in LREST) / len(LREST)))
    n0 = SNAP_REST[nk.name][1]; h0 = SNAP_REST[hp.name][1]
    def pose(d, jaw=0.0, wob=0.0, f=None):
        set_body(rad(5) * d, piv, f=f)
        nk.rotation_euler = (n0[0] + rad(84) * d, n0[1], n0[2]); hp.rotation_euler = (h0[0] + rad(8) * d + wob, h0[1], h0[2])
        if f: kf(nk, "rotation_euler", f); kf(hp, "rotation_euler", f); _rot(jp, f, dx=jaw)
    s = solve(pose, FOOT + 0.03)
    D = [(1, 0), (6, 1), (9, 0.82), (12, 1), (17, 0.05), (25, 0)]
    J = [(1, 0), (3.5, 0.8), (6, 0.05), (9, 0.8), (12, 0.05), (15, 0.5), (17, 0.05), (19, 0.5), (21, 0.05), (23, 0.35), (25, 0)]
    for f in range(1, N + 2):
        j = crv(f, J); pose(s * crv(f, D), rad(22) * j, (rad(-4) * j if f > 14 else 0.0), f)
        _rot(h["tail"], f, dz=rad(14) * math.sin(TAU * 2 * (f - 1) / N))
def h_sleep(h):       # lying down, legs tucked under, eyes closed, breathing
    set_eyes(False)
    drop = h["legz"] - 0.2
    for f in range(1, N + 2):
        b = (1 - math.cos(TAU * (f - 1) / N)) / 2; s = 1 + 0.03 * b
        _root(f, (0, 0, -drop + 0.02 * b), (0, 0, 0), (s, s, s))
        for i, l in enumerate(LEGS): _rot(l, f, dx=rad(80) if i < 2 else rad(-82))
        _rot(h["neck"], f, dx=rad(30) - rad(2.5) * b); _rot(h["head"], f, dx=rad(4) + rad(1.5) * b)
        _rot(h["tail"], f, dx=rad(-6))
        _wings(h, f, -rad(52) + rad(3) * b)
def h_run(h):         # gallop in place (pegasus: flying, legs tucked, big wing beats)
    piv = sum(LREST, Vector()) / len(LREST); piv.x = 0
    fly = bool(h.get("wings"))
    for f in range(1, N + 2):
        t = (f - 1) / N; w = TAU * 3 * t
        if fly:
            w = TAU * 2 * t
            sw = [rad(-42) + rad(12) * math.sin(w + 0.5 * i) if i < 2 else rad(40) + rad(12) * math.sin(w + 1 + 0.5 * i) for i in range(len(LEGS))]
            set_body(rad(-7) + rad(3) * math.sin(w), piv, lift=0.42 + 0.1 * math.sin(w - 1.2), swing=sw, legscale=False, f=f)
            _wings(h, f, rad(8) + rad(44) * math.sin(w))
            _rot(h["neck"], f, dx=rad(10)); _rot(h["head"], f, dx=rad(-6) + rad(3) * math.sin(w))
            _rot(h["tail"], f, dx=rad(50) + rad(10) * math.sin(w + 1), dz=rad(8) * math.sin(w))
        else:
            sw = [rad(44) * math.sin(w + ph) for ph in (0, 0.7, math.pi + 0.3, math.pi + 1.0)][:len(LEGS)]
            set_body(rad(3) + rad(6) * math.sin(w + 0.4), piv, lift=0.06 + 0.13 * (1 - math.cos(w - 0.5)) / 2, swing=sw, legscale=False, f=f)
            _rot(h["neck"], f, dx=rad(16) + rad(6) * math.sin(w + 1.4)); _rot(h["head"], f, dx=rad(-9) + rad(-4) * math.sin(w + 1.4))
            _rot(h["tail"], f, dx=rad(58) + rad(12) * math.sin(2 * w), dz=rad(8) * math.sin(w))
            _wings(h, f, 0.0)
HORSE_ACTS = dict(walk=h_walk, happy=h_happy, eat=h_eat, sleep=h_sleep, run=h_run)

# ------------------------------------------------------------------ the barn door (the horses' "egg"): barn_s0..s3 + barn_hatch
def b_barn():
    RED = (0.82, 0.13, 0.1); DRED = (0.62, 0.09, 0.07); TR = (1, 1, 0.97); ROOF = (0.42, 0.3, 0.26)
    W, D, Hh = 2.3, 1.7, 1.45; F = -D / 2
    B((0, 0, Hh / 2), (W, D, Hh), RED, name="Walls")
    gp = [(-W / 2, 0), (W / 2, 0), (W / 2, 0.28), (W * 0.3, 0.86), (0, 1.12), (-W * 0.3, 0.86), (-W / 2, 0.28)]
    Fp(gp, (0, 0, Hh), D, RED, name="Gable")
    for (a, b) in [((W / 2, 0.28), (W * 0.3, 0.86)), ((W * 0.3, 0.86), (0, 1.12)), ((0, 1.12), (-W * 0.3, 0.86)), ((-W * 0.3, 0.86), (-W / 2, 0.28))]:   # roof slabs
        mx, mz = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; L = math.hypot(b[0] - a[0], b[1] - a[1]); ang = math.atan2(b[1] - a[1], b[0] - a[0])
        B((mx - 0.05 * math.sin(ang), 0, Hh + mz + 0.05 * math.cos(ang)), (L + 0.14, D + 0.3, 0.1), ROOF, None, (0, -ang, 0), bevel=0.02, name="Roof")
    for sx in (-1, 1): B((sx * (W / 2 - 0.04), F - 0.02, Hh / 2), (0.1, 0.06, Hh), TR, name="Trim")
    B((0, F - 0.02, Hh + 0.02), (W, 0.06, 0.1), TR, name="Trim")
    Cy(0.2, 0.06, (0, F - 0.02, Hh + 0.6), TR, (R90, 0, 0), name="LoftRim"); Cy(0.15, 0.08, (0, F - 0.03, Hh + 0.6), (0.3, 0.2, 0.15), (R90, 0, 0), name="Loft")
    S(0.3, (-1.0, F - 0.35, 0.2), (1.2, 1, 0.75), "straw", name="Hay"); S(0.2, (-0.75, F - 0.55, 0.13), (1.2, 1, 0.75), (0.9, 0.72, 0.36), name="Hay")
    # doorway: dark inside, glow panel, shadow of "someone" inside
    DW, DH = 1.2, 1.18
    B((0, F - 0.025, DH / 2 + 0.04), (DW + 0.2, 0.07, DH + 0.2), TR, name="Frame")
    inside = B((0, F - 0.05, DH / 2), (DW, 0.04, DH), (0.1, 0.06, 0.05), name="Inside")
    glow = B((0, F - 0.06, DH / 2), (DW, 0.03, DH), (1.0, 0.86, 0.4), name="GlowPanel"); gm = mat((1.0, 0.8, 0.3), 0.5, 2.0).copy(); glow.data.materials[0] = gm
    ginp = gm.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    SH = (0.3, 0.17, 0.05); shadow = []
    shadow.append(S(0.3, (0.08, F - 0.085, 0.42), (1.2, 0.05, 1.0), SH, name="Shadow")); shadow.append(S(0.15, (-0.12, F - 0.085, 0.7), (0.9, 0.05, 1.6), SH, None, (0, rad(-28), 0), name="Shadow"))
    shadow.append(S(0.2, (-0.3, F - 0.085, 0.9), (1.35, 0.05, 0.85), SH, None, (0, rad(25), 0), name="Shadow"))
    for sx in (-1, 1): shadow.append(Co(0.06, 0.2, (-0.2 + sx * 0.08, F - 0.085, 1.1), SH, (0, 0, 0), None, 0.01, 8, name="Shadow"))
    rays = []
    for k in range(7):
        a = rad(-66 + k * 22); o = Co(0.012, 0.6, (0.95 * math.sin(a), F - 0.5, 0.75 + 0.95 * math.cos(a)), (1.0, 0.9, 0.4), (0, a, 0), None, 0.05, 8, name="Ray")
        o.data.materials[0] = mat((1.0, 0.85, 0.3), 0.4, 1.4); rays.append(o)
    # the door: one leaf hinged on the right, swings out towards the viewer; white X brace and a big "?"
    hinge = E((DW / 2, F - 0.1, 0), name="Hinge")
    B((0, F - 0.1, DH / 2), (DW, 0.07, DH), DRED, hinge, name="Door")
    for (loc, sc, r) in [((0, F - 0.14, DH - 0.06), (DW, 0.03, 0.1), 0), ((0, F - 0.14, 0.06), (DW, 0.03, 0.1), 0), ((-DW / 2 + 0.05, F - 0.14, DH / 2), (0.1, 0.03, DH), 0),
                         ((DW / 2 - 0.05, F - 0.14, DH / 2), (0.1, 0.03, DH), 0)]: B(loc, sc, TR, hinge, name="Brace")
    S(0.05, (-DW / 2 + 0.16, F - 0.17, DH / 2), (1, 1, 1), "gold", hinge, name="Knob")
    cu = bpy.data.curves.new("Q", 'FONT'); cu.body = "?"; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.size = 1.45; cu.extrude = 0.03; cu.bevel_depth = 0.012
    q = bpy.data.objects.new("QMark", cu); scene.collection.objects.link(q); q.location = (0, F - 0.15, DH / 2 + 0.01); q.rotation_euler = (R90, 0, 0)
    q.data.materials.append(mat((1.0, 0.86, 0.2), 0.4, 0.25)); par(q, hinge)
    # burst pieces for the hatch
    rr = random.Random(4); hay = []
    for k in range(14):
        a = rad(-80 + 160 * k / 13) + rr.uniform(-0.1, 0.1)
        o = Cy(0.035, rr.uniform(0.34, 0.55), (0.2 * math.sin(a), F - 0.2, 0.6), ("straw" if k % 2 else (0.92, 0.72, 0.3)), (rr.uniform(0, 3), rr.uniform(0, 3), 0), None, 6, name="HayBit")
        hay.append((o, a, rr.uniform(0.8, 1.3)))
    stars = []
    for k in range(9):
        a = rad(-90 + 180 * k / 8); st = Fp(starpts(0.2, 0.085), (0, F - 0.3, 0.7), 0.05, "gold", None, None, name="Star"); st.data.materials[0] = mat("gold", 0.3, 2.5); stars.append((st, a))
    burst = S(0.3, (0, F - 0.2, 0.62), (1, 0.4, 1), (1.0, 0.95, 0.5), name="Burst"); bmat = mat((1.0, 0.95, 0.55), 0.3, 4.0).copy(); burst.data.materials[0] = bmat
    def show(ob, on): ob.hide_render = not on; ob.hide_viewport = not on
    ANG = [0, 13, 44, 74]
    def state(k, tilt=True):
        hinge.rotation_euler = (0, 0, rad(ANG[k]))
        show(inside, True); show(glow, k >= 1); ginp.default_value = (0, 0.55, 0.8, 1.15)[k]
        for o in shadow: show(o, k == 2)
        for o in rays: show(o, k >= 3)
        for o, a, s in hay: show(o, False)
        for st, a in stars: show(st, False)
        show(burst, False)
        ROOT.rotation_euler = (0, rad(4) if (k == 3 and tilt) else 0, 0); ROOT.scale = (1.04, 1.04, 0.96) if (k == 3 and tilt) else (1, 1, 1)
    globals()['EXTRA_STILLS'] = [(f"{PREFIX}_s{k}", (lambda k=k: state(k))) for k in range(4)]
    state(0)
    return dict(hinge=hinge, state=state, show=show, hay=hay, stars=stars, burst=burst, bmat=bmat, rays=rays, ginp=ginp, glow=glow, shadow=shadow)
def barn_hatch(h):
    show = h["show"]; hinge = h["hinge"]
    def vis(ob, on, f): show(ob, on); ob.keyframe_insert("hide_render", frame=f); ob.keyframe_insert("hide_viewport", frame=f)
    h["state"](3, tilt=False)
    # the door rattles, then bangs wide open and bounces; the barn squashes and jumps with it
    keys(hinge, "rotation_euler", [(f, (0, 0, rad(a))) for f, a in [(1, 74), (2, 62), (3, 78), (4, 58), (5, 80), (6, 54), (7, 40), (9, 126), (11, 108), (13, 120), (15, 113), (17, 116), (25, 116)]])
    keys(ROOT, "rotation_euler", [(1, (0, 0, 0)), (2, (0, rad(5), 0)), (3, (0, rad(-5), 0)), (4, (0, rad(6), 0)), (5, (0, rad(-6), 0)), (6, (0, rad(4), 0)), (7, (0, 0, 0)), (25, (0, 0, 0))])
    keys(ROOT, "scale", [(1, (1, 1, 1)), (6, (1.05, 1.05, 0.93)), (7, (1.08, 1.08, 0.88)), (9, (0.93, 0.93, 1.12)), (12, (1.04, 1.04, 0.97)), (15, (1, 1, 1)), (25, (1, 1, 1))])
    keys(ROOT, "location", [(1, (0, 0, 0)), (7, (0, 0, 0)), (10, (0, 0, 0.22)), (13, (0, 0, 0)), (25, (0, 0, 0))])
    for f, v in [(1, 1.15), (7, 1.3), (9, 2.2), (14, 1.3), (25, 1.0)]: h["ginp"].default_value = v; h["ginp"].keyframe_insert("default_value", frame=f)
    for o in h["rays"]: vis(o, True, 1); vis(o, False, 8); vis(o, True, 9); vis(o, False, 15)
    F = -1.7 / 2
    for o, a, s in h["hay"]:
        vis(o, False, 1); vis(o, True, 8); vis(o, False, 23)
        d = Vector((math.sin(a) * 0.8, -0.6, math.cos(a) * 0.8)) * s; p0 = Vector((0.2 * math.sin(a), F - 0.2, 0.6))
        o.location = p0; kf(o, "location", 8); o.location = p0 + d * 0.75 + Vector((0, 0, 0.25)); kf(o, "location", 13)
        o.location = p0 + d * 1.1 + Vector((0, 0, -0.1)); kf(o, "location", 18); o.location = Vector((p0.x + d.x * 1.25, p0.y + d.y * 1.2, 0.05)); kf(o, "location", 23)
        r0 = tuple(o.rotation_euler); kf(o, "rotation_euler", 8); o.rotation_euler = (r0[0] + rad(300), r0[1] + rad(200), r0[2]); kf(o, "rotation_euler", 23)
    for st, a in h["stars"]:
        vis(st, False, 1); vis(st, True, 9); vis(st, False, 21)
        st.location = (0, F - 0.3, 0.7); kf(st, "location", 9); st.location = (math.sin(a) * 1.25, F - 0.7, 0.8 + math.cos(a) * 1.15); kf(st, "location", 20)
        st.scale = (0.3, 0.3, 0.3); kf(st, "scale", 9); st.scale = (1.4, 1.4, 1.4); kf(st, "scale", 14); st.scale = (0.2, 0.2, 0.2); kf(st, "scale", 20)
        st.rotation_euler = (0, 0, 0); kf(st, "rotation_euler", 9); st.rotation_euler = (0, rad(200), 0); kf(st, "rotation_euler", 20)
    b = h["burst"]; vis(b, False, 1); vis(b, True, 8); vis(b, False, 16)
    keys(b, "scale", [(8, (0.4, 0.2, 0.4)), (11, (2.0, 0.4, 2.0)), (15, (2.6, 0.4, 2.6))])
    inp = h["bmat"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    for f, v in [(8, 2.2), (12, 1.4), (15, 0.6)]: inp.default_value = v; inp.keyframe_insert("default_value", frame=f)
ACTS["hatch"] = barn_hatch
BUILD = {k: globals()["b_" + k] for k in HORSE_NAMES + ["barn"]}
