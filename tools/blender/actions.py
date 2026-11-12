# eat / sleep / run for the Dino Island + Coral Reef collections.
# exec'd inside the wb.py globals AFTER the builders, BEFORE BUILD[NAME]().  Needs KIND ("dino"|"sea").
import numpy as np
from mathutils import Euler, Matrix
IS_DINO = (KIND == "dino")
N = NFRAMES
# screen axes of the fixed 3/4 camera (ortho, so only the orientation matters)
_q = (Vector((0, 0, 1.2)) - Vector((-9, -9, 6.8))).to_track_quat('-Z', 'Y')
UP = np.array(_q @ Vector((0, 1, 0))); RIGHT = np.array(_q @ Vector((1, 0, 0)))

MOUTH = []
_sm_orig = smile
def smile(*a, **k):
    before = {o.name for o in bpy.data.objects}; _sm_orig(*a, **k)
    MOUTH.extend([o for o in bpy.data.objects if o.name not in before])

def crv(f, pts):
    """cosine-eased curve through (frame, value) points"""
    if f <= pts[0][0]: return pts[0][1]
    for (f0, v0), (f1, v1) in zip(pts, pts[1:]):
        if f <= f1:
            u = (f - f0) / (f1 - f0); u = (1 - math.cos(math.pi * u)) / 2; return v0 + (v1 - v0) * u
    return pts[-1][1]
def vis_meshes(): return [o for o in scene.objects if o.type == 'MESH' and not o.hide_render]
def descendants(o):
    out = []; st = list(o.children)
    while st:
        c = st.pop(); out.append(c); st.extend(c.children)
    return out
def world_pts(objs):
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); out = []
    for ob in objs:
        ev = ob.evaluated_get(dg); me = ev.to_mesh(); n = len(me.vertices)
        if n:
            co = np.empty(n * 3, dtype=np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3).astype(np.float64)
            M = np.array(ev.matrix_world); out.append(co @ M[:3, :3].T + M[:3, 3])
        ev.to_mesh_clear()
    return np.concatenate(out) if out else np.zeros((1, 3))
def sbox(objs):
    """exact screen-space box (xmin, xmax, ymin, ymax) of the evaluated meshes"""
    w = world_pts(objs); sx = w @ RIGHT; sy = w @ UP
    return (float(sx.min()), float(sx.max()), float(sy.min()), float(sy.max()))
def minz(objs): return float(world_pts(objs)[:, 2].min())
def set_eyes(open_):
    for e in EYES: e.hide_render = not open_; e.hide_viewport = not open_
    for l in LIDOBJ: l.hide_render = open_; l.hide_viewport = open_

# ------------------------------------------------------------------ neck rig for the long-necked dinos
NECK = dict(brachiosaurus=((0, -0.5, 1.35), (0, -0.82, 2.95)), diplodocus=((0, -0.55, 1.15), (0, -2.0, 1.85)), plesiosaurus=((0, -0.6, 0.95), (0, -1.45, 2.25)))
NB = 8
NW = [0.22, 0.19, 0.16, 0.13, 0.11, 0.08, 0.06, 0.05]
NECKARM = None; NSG = 1
def neck_rig(h):
    g = globals(); p0, p1 = map(Vector, NECK[NAME]); hp = h["head"]
    body = bpy.data.objects["Body"]
    ad = bpy.data.armatures.new("NeckArm"); arm = bpy.data.objects.new("NeckArm", ad); scene.collection.objects.link(arm)
    for o in bpy.context.selected_objects: o.select_set(False)
    bpy.context.view_layer.objects.active = arm; arm.select_set(True); bpy.ops.object.mode_set(mode='EDIT')
    eb = ad.edit_bones.new("base"); eb.head = (0, 0.6, 0.4); eb.tail = (0, 0.6, 0.8)
    prev = None
    for k in range(NB):
        b = ad.edit_bones.new(f"n{k}"); b.head = p0 + (p1 - p0) * (k / NB); b.tail = p0 + (p1 - p0) * ((k + 1) / NB); b.roll = 0
        if prev: b.parent = prev; b.use_connect = True
        prev = b
    bpy.ops.object.mode_set(mode='OBJECT'); arm.select_set(False)
    par(arm, ROOT)
    me = body.data; ax = p1 - p0; Ln = ax.length; axn = ax / Ln
    names = ["base"] + [f"n{k}" for k in range(NB)]
    vg = {nm: body.vertex_groups.new(name=nm) for nm in names}
    for v in me.vertices:
        d = v.co - p0; al = d.dot(axn); s = al / Ln * NB; rr = (d - axn * al).length
        mask = 1.0 if s > 2.0 else max(0.0, min(1.0, (0.62 - rr) / 0.2))
        c = s - 0.5; i0 = math.floor(c); fr = c - i0
        w = {}
        def add(i, x):
            i = max(-1, min(NB - 1, i)); w[i] = w.get(i, 0.0) + x
        add(i0, (1 - fr) * mask); add(i0 + 1, fr * mask); add(-1, 1 - mask)
        for i, x in w.items():
            if x > 1e-4: vg[names[i + 1]].add([v.index], x, 'REPLACE')
    am = body.modifiers.new("Arm", 'ARMATURE'); am.object = arm
    body.modifiers.move(len(body.modifiers) - 1, 0)
    bpy.context.view_layer.update()
    xa = ad.bones["n0"].matrix_local.col[0]
    assert abs(xa.x) > 0.9, ("neck bone roll", tuple(xa))
    g['NSG'] = 1 if xa.x > 0 else -1
    for pb in arm.pose.bones: pb.rotation_mode = 'XYZ'
    ne = bpy.data.objects.new("NeckEnd", None); scene.collection.objects.link(ne)
    ne.parent = arm; ne.parent_type = 'BONE'; ne.parent_bone = f"n{NB-1}"
    bpy.context.view_layer.update(); ne.matrix_world = Matrix.Translation(hp.matrix_world.translation); bpy.context.view_layer.update()
    hp.parent = ne; hp.matrix_parent_inverse = ne.matrix_world.inverted(); bpy.context.view_layer.update()
    g['NECKARM'] = arm
def set_neck(phi, f=None):
    if not NECKARM: return
    for k in range(NB):
        pb = NECKARM.pose.bones[f"n{k}"]; pb.rotation_euler = (NSG * phi * NW[k], 0, 0)
        if f: pb.keyframe_insert("rotation_euler", frame=f)

# ------------------------------------------------------------------ rig discovery (after BUILD)
LIDOBJ = []; LEGS = []; LREST = []; HEADOBJS = []; BODYOBJS = []; DKIND = None
def setup_rig(h):
    g = globals()
    for e in EYES: e.hide_viewport = True
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    cols = []
    for (p, parent, r) in LIDS:                           # skin colour behind each eye (ray from the front)
        hit, loc, nrm, idx, ob, mw = scene.ray_cast(dg, Vector(p) + Vector((0, -3.0, 0)), Vector((0, 1, 0)))
        col = (0.5, 0.5, 0.5)
        if not hit: hit, loc, nrm, idx, ob, mw = scene.ray_cast(dg, Vector(p) + Vector((0, r * 0.4, 0)), Vector((0, 0, -1)))
        if hit and ob.data.materials:
            mi = ob.data.polygons[idx].material_index if idx < len(ob.data.polygons) else 0
            m = ob.data.materials[min(mi, len(ob.data.materials) - 1)]
            col = tuple(m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value[:3])
        cols.append(tuple(round(v * 0.82, 4) for v in col))
    for e in EYES: e.hide_viewport = False
    for (p, parent, r), col in zip(LIDS, cols):           # closed eye = skin-coloured lid + dark lash line
        pe = Vector(p) + Vector((0, r * 0.4, 0))
        LIDOBJ.append(S(r * 1.05, tuple(pe), (1, 0.5, 1), col, parent, name="Lid"))
        LIDOBJ.append(B(tuple(pe + Vector((0, -r * 0.5, -r * 0.12))), (r * 1.5, r * 0.22, r * 0.2), "ink", parent, name="Lash"))
    for l in LIDOBJ: l.hide_render = True; l.hide_viewport = True
    for o in bpy.data.objects:
        if o.name.split('.')[0] in ("MouthLine", "Pout"): MOUTH.append(o)
    if IS_DINO:
        LEGS.extend(sorted([o for o in bpy.data.objects if o.name.startswith("LegPiv")], key=lambda o: o.name))
        LREST.extend([Vector(l.location) for l in LEGS])
    if NAME in NECK: neck_rig(h)
    bpy.context.view_layer.update()
    hp = h.get("head")
    if hp: HEADOBJS.extend([o for o in descendants(hp) if o.type == 'MESH' and not o.hide_render])
    g['FOOT'] = sbox(vis_meshes())[2]                 # idle foot line on screen
    if IS_DINO:
        skip = {o.name for o in HEADOBJS}
        for l in LEGS: skip.update(o.name for o in descendants(l))
        BODYOBJS.extend([o for o in vis_meshes() if o.name not in skip])
        g['BODY_MINZ'] = minz(BODYOBJS)
        g['DKIND'] = 'biped' if len(LEGS) == 2 else ('quad' if len(LEGS) == 4 else 'swim')
    print("RIG", NAME, "legs", len(LEGS), "kind", DKIND, "mouth", len(MOUTH), "lids", len(LIDOBJ), "foot %.3f" % FOOT, flush=True)

# ------------------------------------------------------------------ dino body helper
def set_body(theta, piv, drop=0.0, lift=0.0, yaw=0.0, swing=None, legscale=True, us=1.0, f=None):
    """pitch the body by theta about `piv` (stays put), lower it by drop; legs stay upright and reach the ground"""
    R = Euler((theta, 0, yaw), 'XYZ').to_matrix()
    loc = piv - R @ (piv * us) + Vector((0, 0, lift - drop))
    ROOT.location = loc; ROOT.rotation_euler = (theta, 0, yaw); ROOT.scale = (us, us, us)
    if f: kf(ROOT, "location", f); kf(ROOT, "rotation_euler", f); kf(ROOT, "scale", f)
    for i, l in enumerate(LEGS):
        L = LREST[i]; hz = (loc + R @ (L * us)).z
        l.rotation_euler = (-theta + (swing[i] if swing else 0.0), 0, 0)
        k = max(0.3, min(1.1, hz / (L.z * us))) if legscale else 1.0
        l.scale = (1, 1, k)
        if f: kf(l, "rotation_euler", f); kf(l, "scale", f)
DOVR = dict(brachiosaurus=dict(eat=(12, 175, 60), sleep=(0, 160, 15)), diplodocus=dict(eat=(10, 95, 50), sleep=(0, 85, 10)),
            plesiosaurus=dict(eat=(0, 150, 55), sleep=(0, 135, 12)))
def dcfg():
    hipc = (sum(LREST, Vector()) / len(LREST)) if LREST else Vector((0, 0.2, 0.4)); hipc.x = 0
    c = dict(kind=DKIND, piv=hipc, peck=NAME in ("pterodactyl", "archaeopteryx"))
    if DKIND == 'biped': c.update(eat=(50, 0, 88), eatpiv=hipc, sleep=(6, 0, 46), lean=14)
    elif DKIND == 'quad': c.update(eat=(12, 0, 64), eatpiv=Vector((0, max(l.y for l in LREST), hipc.z)), sleep=(0, 0, 32), lean=5)
    else: c.update(eat=(0, 0, 50), eatpiv=hipc, sleep=(0, 0, 20), lean=5)
    c.update(DOVR.get(NAME, {})); return c
def head_low(): return sbox(HEADOBJS)[2]
def solve(fn, target, it=14):
    """largest s in [0,1] whose pose keeps the head above the screen foot line"""
    fn(1.0)
    if head_low() >= target: return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(it):
        mid = (lo + hi) / 2; fn(mid)
        if head_low() >= target: lo = mid
        else: hi = mid
    return lo

def dino_eat(h):
    c = dcfg(); hp = h["head"]; jp = h.get("jaw"); eb, en, eh = c['eat']; piv = c['eatpiv']
    def pose(d, jaw=0.0, wob=0.0, f=None):
        thb = rad(eb) * d; ph = rad(en) * d; hw = rad(eh) * d
        set_body(thb, piv, f=f); set_neck(ph, f)
        hp.rotation_euler = (hw - thb - ph + wob, 0, 0)
        if f: kf(hp, "rotation_euler", f)
        if jp:
            jp.rotation_euler = (jaw, 0, 0)
            if f: kf(jp, "rotation_euler", f)
    s = solve(pose, FOOT + 0.03)
    if c['peck']:
        D = [(1, 0), (4, 1), (7, 0.35), (10, 1), (13, 0.35), (16, 1), (20, 0), (25, 0)]
        J = [(1, 0), (2.5, 0.5), (4, 0), (7, 0.6), (10, 0), (13, 0.6), (16, 0), (19, 0.45), (21, 0.05), (23, 0.35), (25, 0)]
    else:
        D = [(1, 0), (6, 1), (9, 0.7), (12, 1), (17, 0.06), (25, 0)]
        J = [(1, 0), (3.5, 0.9), (6, 0.05), (9, 0.85), (12, 0.05), (15, 0.5), (17, 0.05), (19, 0.45), (21, 0.05), (23, 0.3), (25, 0)]
    for f in range(1, N + 2):
        j = crv(f, J)
        pose(s * crv(f, D), rad(27) * j, (rad(-5) * j if f > 14 else 0.0), f)
    for i, w in enumerate(h.get("wings", [])):
        sx = -1 if i % 2 == 0 else 1
        for f in range(1, N + 2): w.rotation_euler = (0, -rad(14) * sx * crv(f, D), 0); kf(w, "rotation_euler", f)

def dino_sleep(h):
    c = dcfg(); hp = h["head"]; jp = h.get("jaw"); sb, sn, sh = c['sleep']; piv = c['piv']
    set_eyes(False)
    hipz = piv.z if LEGS else 1.0
    drop = max(0.0, min(BODY_MINZ - 0.04, 0.62 * hipz)) if LEGS else 0.0
    st = dict(lift=0.0, s=1.0)
    def pose(s, b=0.0, f=None):
        thb = rad(sb) - rad(1.0) * b
        set_body(thb, piv, drop=drop, lift=st['lift'] + 0.025 * b, us=1 + 0.03 * b, f=f); set_neck(rad(sn) * s, f)
        hp.rotation_euler = (rad(sh) * s - thb - rad(sn) * s, 0, 0)
        if f: kf(hp, "rotation_euler", f)
        for i, w in enumerate(h.get("wings", [])):
            w.rotation_euler = (0, (rad(h.get("flap", 30) * 0.5) - rad(3) * b) * (-1 if i % 2 == 0 else 1), 0)
            if f: kf(w, "rotation_euler", f)
    for _ in range(3):                                   # rest the head on the foot line, never let anything sink below it
        st['s'] = solve(pose, FOOT + 0.02); pose(st['s'])
        m = sbox(vis_meshes())[2]
        if m >= FOOT - 0.002: break
        st['lift'] += (FOOT - m) / UP[2] + 0.004
    for f in range(1, N + 2):
        b = (1 - math.cos(TAU * (f - 1) / N)) / 2
        pose(st['s'], b, f)
    for i, fl in enumerate(h.get("flippers", [])):
        sx = -1 if i % 2 == 0 else 1
        for f in range(1, N + 2):
            b = (1 - math.cos(TAU * (f - 1) / N)) / 2; fl.rotation_euler = (0, rad(5) * b * -sx, 0); kf(fl, "rotation_euler", f)

def dino_run(h):
    c = dcfg(); hp = h["head"]; jp = h.get("jaw"); kind = c['kind']; lean = rad(c['lean']); piv = c['piv']
    hover = bool(h.get("hover"))
    for f in range(1, N + 2):
        t = (f - 1) / N; w = TAU * 3 * t
        bounce = (0.12 if kind != 'swim' else 0.08) * (1 - math.cos(2 * w)) / 2
        th = lean + rad(3) * math.sin(2 * w + 0.6); yaw = rad(6) * math.sin(w)
        if kind == 'biped': sw = [rad(46 if not hover else 16) * math.sin(w + math.pi * i) for i in range(len(LEGS))]
        else: sw = [rad(38) * math.sin(w + ph) for ph in (0, 0.8, math.pi + 0.4, math.pi + 1.2)][:len(LEGS)]
        lift = bounce + (0.5 * math.sin(lean) if kind == 'quad' else 0.0) + (0.22 + 0.1 * math.sin(w) if hover else 0.0)
        set_body(th, piv, lift=lift, yaw=yaw, swing=sw, legscale=False, f=f)
        nk = (rad(9) + rad(5) * math.sin(2 * w + 1.2)) if NECKARM else 0.0
        set_neck(nk, f)
        hp.rotation_euler = (-0.75 * lean - nk + rad(6) * math.sin(2 * w + 2.0), 0, rad(4) * math.sin(w + math.pi)); kf(hp, "rotation_euler", f)
        if jp: jp.rotation_euler = (rad(15) + rad(6) * math.sin(w), 0, 0); kf(jp, "rotation_euler", f)
        for i, wg in enumerate(h.get("wings", [])):
            sx = -1 if i % 2 == 0 else 1; a = rad(14) + rad(h.get("flap", 30) * 1.4) * math.sin(w + 0.5)
            wg.rotation_euler = (0, -a * sx, 0); kf(wg, "rotation_euler", f)
        for i, fl in enumerate(h.get("flippers", [])):
            fl.rotation_euler = (0, rad(42) * (-1 if i % 2 == 0 else 1) * math.sin(w + math.pi * (i // 2)), 0); kf(fl, "rotation_euler", f)

# ------------------------------------------------------------------ sea creatures
SKIND = dict(clownfish='fish', shark='fish', pufferfish='fish', dolphin='fish', whale='fish', narwhal='fish', seahorse='seahorse', jellyfish='jelly',
             octopus='jelly', starfish='star', crab='crab', lobster='crab', turtle='turtle', seal='seal', penguin='penguin', manta='manta')
SFLOAT = {'clownfish', 'shark', 'pufferfish', 'dolphin', 'whale', 'narwhal', 'seahorse', 'jellyfish', 'turtle', 'manta'}
def _rest(o): return SNAP_REST[o.name]
def _mouth(m, f):
    for o in MOUTH:
        s0 = SNAP_REST[o.name][2]; big = o.name.split('.')[0] in ("MouthLine", "Pout")
        o.scale = (s0[0] * (1 + 0.25 * m), s0[1], s0[2] * (1 + (1.6 if big else 1.3) * m)); kf(o, "scale", f)
def _rot(o, f, dx=0.0, dy=0.0, dz=0.0):
    r0 = SNAP_REST[o.name][1]; o.rotation_euler = (r0[0] + dx, r0[1] + dy, r0[2] + dz); kf(o, "rotation_euler", f)
def _root(f, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
    ROOT.location = loc; ROOT.rotation_euler = rot; ROOT.scale = scale
    kf(ROOT, "location", f); kf(ROOT, "rotation_euler", f); kf(ROOT, "scale", f)
def sea_eat(h):
    kind = SKIND[NAME]; flo = NAME in SFLOAT
    L = 0.3 if flo else 0.2; P = rad(dict(penguin=26, seahorse=12, jelly=10).get(kind, 7 if flo else 4))
    if kind == 'penguin':
        D = [(1, 0), (5, 1), (8, 0.2), (11, 1), (15, 0), (25, 0)]; M = [(1, 0), (25, 0)]
    else:
        D = [(1, 0), (3, -0.25), (6, 1), (9, 0.3), (12, 0), (25, 0)]
        M = [(1, 0), (4, 1), (6, 1), (7.5, 0), (10, 0), (12, 0.55), (14, 0), (16, 0.55), (18, 0), (20, 0.4), (22, 0), (25, 0)]
    for f in range(1, N + 2):
        t = (f - 1) / N; d = crv(f, D); m = crv(f, M); ch = m if f > 10 else 0.0
        _root(f, (0, -L * d, L * 0.45 * max(d, 0)), (P * d + rad(2.5) * ch, 0, 0), (1 + 0.03 * ch, 1 + 0.05 * max(d, 0) - 0.02 * ch, 1 - 0.035 * ch))
        _mouth(m, f)
        if h.get("jaw"): _rot(h["jaw"], f, dx=rad(24) * m)
        if h.get("head"): _rot(h["head"], f, dx=rad(14) * max(d, 0))
        for i, c in enumerate(h.get("claws", [])): _rot(c, f, dz=rad(16) * (1 if i % 2 == 0 else -1) * -max(d, 0) + rad(6) * ch * (1 if i % 2 == 0 else -1))
        for i, fn in enumerate(h.get("fins", [])): _rot(fn, f, dy=rad(14) * (-1 if i % 2 == 0 else 1) * math.sin(TAU * 2 * t))
        for i, wg in enumerate(h.get("wings", [])): _rot(wg, f, dy=rad(12) * (-1 if i % 2 == 0 else 1) * math.sin(TAU * t))
        for i, tt in enumerate(h.get("tentacles", [])): _rot(tt, f, dx=rad(8) * math.sin(TAU * t + i * 0.8))
        if "tail" in h:
            ax = h.get("tailaxis", 2); a = rad(h.get("tailamp", 25) * 0.6) * math.sin(TAU * 2 * t)
            _rot(h["tail"], f, **{("dx", "dy", "dz")[ax]: a})
def sea_sleep(h):
    kind = SKIND[NAME]; flo = NAME in SFLOAT
    set_eyes(False)
    for f in range(1, N + 2):
        t = (f - 1) / N; b = (1 - math.cos(TAU * t)) / 2; sw = math.sin(TAU * t)
        if flo: _root(f, (0, 0, 0.12 * b), (rad(1.5) * sw, rad(3.5) * sw, 0), (1 + 0.02 * b,) * 3)
        else: _root(f, (0, 0, 0), (0, 0, 0), (1 + 0.025 * b, 1 + 0.025 * b, 1 - 0.06 * b))
        for i, fn in enumerate(h.get("fins", [])): _rot(fn, f, dy=(rad(12) + rad(4) * sw) * (-1 if i % 2 == 0 else 1))
        for i, wg in enumerate(h.get("wings", [])): _rot(wg, f, dy=(rad(8) + rad(5) * sw) * (-1 if i % 2 == 0 else 1))
        for i, tt in enumerate(h.get("tentacles", [])): _rot(tt, f, dx=rad(5) * math.sin(TAU * t + i * 0.8))
        for i, c in enumerate(h.get("claws", [])): _rot(c, f, dz=rad(4) * sw * (1 if i % 2 == 0 else -1))
        if h.get("head"): _rot(h["head"], f, dx=rad(14) + rad(2) * b)
        if "tail" in h:
            ax = h.get("tailaxis", 2); _rot(h["tail"], f, **{("dx", "dy", "dz")[ax]: rad(6) * sw})
def sea_run(h):
    kind = SKIND[NAME]
    for f in range(1, N + 2):
        t = (f - 1) / N; w3 = TAU * 3 * t; w4 = TAU * 4 * t; w2 = TAU * 2 * t; s1 = (-1, 1)
        if kind == 'fish':
            ax = h.get("tailaxis", 2); amp = min(52, h.get("tailamp", 25) * 1.9)
            _rot(h["tail"], f, **{("dx", "dy", "dz")[ax]: rad(amp) * math.sin(w4)})
            if ax == 2: _root(f, (0, 0, 0.05 * math.sin(w2)), (rad(5), 0, rad(9) * math.sin(w4 + math.pi)))
            else: _root(f, (0, 0, 0.07 * math.sin(w4 + 1.0)), (rad(4) + rad(7) * math.sin(w4 + math.pi), 0, 0))
            for i, fn in enumerate(h.get("fins", [])): _rot(fn, f, dy=rad(38) * s1[i % 2] * math.sin(w4 + math.pi / 2))
        elif kind == 'seahorse':
            _root(f, (0, 0, 0.09 * (1 - math.cos(w3)) / 2), (rad(13), rad(12) * math.sin(w3), 0))
            for fn in h.get("fins", []): _rot(fn, f, dy=rad(45) * math.sin(TAU * 6 * t))
        elif kind == 'jelly':
            p = (1 - math.cos(w3)) / 2; k = 1.0 if NAME == 'jellyfish' else 0.75
            _root(f, (0, 0, 0.1 * k * p), (rad(11 if NAME == 'jellyfish' else 4), 0, 0), (1 - 0.16 * k * p, 1 - 0.16 * k * p, 1 + 0.18 * k * p))
            for i, tt in enumerate(h.get("tentacles", [])): _rot(tt, f, dx=rad(24) * math.sin(w3 - 1.0 + i * 0.25))
        elif kind == 'star':
            th = TAU * t; zc = 1.0
            _root(f, (-zc * math.sin(th), 0, zc - zc * math.cos(th) + 0.07 * (1 - math.cos(5 * th))), (0, th, 0))
        elif kind == 'crab':
            _root(f, (0.07 * math.sin(w3), 0, 0.05 * (1 - math.cos(2 * w3)) / 2 + 0.06), (0, rad(7) + rad(4) * math.sin(w3), 0))
            for i, l in enumerate(h.get("legs", [])): _rot(l, f, dy=rad(30) * math.sin(TAU * 6 * t + math.pi * (i % 2) + (i // 3) * 1.0))
            for i, c in enumerate(h.get("claws", [])): _rot(c, f, dx=rad(-20), dz=rad(14) * math.sin(w3 + math.pi * i))
        elif kind == 'turtle':
            _root(f, (0, 0, 0.1 * (1 - math.cos(w3)) / 2), (rad(5) + rad(5) * math.sin(w3 + 1.0), 0, 0))
            for i, fn in enumerate(h.get("fins", [])): _rot(fn, f, dy=rad(44) * s1[i % 2] * math.sin(w3 + math.pi * (i // 2) * 0.5))
            if h.get("head"): _rot(h["head"], f, dx=rad(-8) + rad(5) * math.sin(w3))
            if h.get("jaw"): _rot(h["jaw"], f, dx=rad(12))
        elif kind == 'seal':
            _root(f, (0, 0, 0.14 * (1 - math.cos(w3)) / 2), (rad(9) * math.sin(w3 - 0.6), rad(5) * math.sin(w3), 0))
            for i, fn in enumerate(h.get("fins", [])): _rot(fn, f, dy=rad(40) * s1[i % 2] * math.sin(w3 + math.pi / 2))
        elif kind == 'penguin':
            _root(f, (0, 0, 0.1 * (1 - math.cos(2 * w3)) / 2), (rad(9), rad(13) * math.sin(w3), 0))
            for i, fn in enumerate(h.get("fins", [])): _rot(fn, f, dy=(rad(25) + rad(30) * math.sin(2 * w3)) * -s1[i % 2])
        elif kind == 'manta':
            _root(f, (0, 0, 0.14 * math.sin(w2 + 1.2)), (rad(4) + rad(6) * math.sin(w2 + math.pi), 0, 0))
            for i, wg in enumerate(h.get("wings", [])): _rot(wg, f, dy=rad(44) * s1[i % 2] * math.sin(w2))
if IS_DINO: ACTS["eat"] = dino_eat; ACTS["sleep"] = dino_sleep; ACTS["run"] = dino_run
else: ACTS["eat"] = sea_eat; ACTS["sleep"] = sea_sleep; ACTS["run"] = sea_run
