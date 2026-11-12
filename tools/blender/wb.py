import bpy, math, os
from mathutils import Vector
NAME = "__NAME__"; GROUP = "__GROUP__"
OUTDIR = "__OUTDIR__"; PREFIX = NAME; ACTION = GROUP
DO_IDLE=__IDLE__; DO_ANIM=__ANIM__; FIXED=__FIXED__; MEASURE_ONLY=__MEAS__
NFRAMES = __NFRAMES__
RES = __RES__
GROUND="auto"
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras, bpy.data.curves):
    for d in list(coll):
        if d.users == 0: coll.remove(d)
scene = bpy.context.scene; scene.frame_start, scene.frame_end = 1, NFRAMES; scene.render.fps = 24
TAU = math.tau; R90 = math.radians(90); rad = math.radians
PAL = dict(white=(1,1,1), black=(0.02,0.02,0.02), ink=(0.08,0.07,0.1), grey=(0.6,0.6,0.65), dkgrey=(0.3,0.3,0.34), red=(0.9,0.1,0.1),
           orange=(1.0,0.5,0.05), yellow=(1.0,0.82,0.1), green=(0.3,0.7,0.2), dkgreen=(0.15,0.45,0.15), blue=(0.2,0.5,0.95), sky=(0.55,0.8,1.0),
           navy=(0.12,0.2,0.5), purple=(0.55,0.25,0.8), pink=(1.0,0.5,0.7), hotpink=(0.95,0.25,0.55), brown=(0.55,0.33,0.15), dkbrown=(0.3,0.17,0.07),
           tan=(0.85,0.65,0.4), cream=(1.0,0.93,0.75), lime=(0.6,0.85,0.2), teal=(0.15,0.65,0.65), gold=(1.0,0.75,0.1), mouth=(0.3,0.04,0.08),
           tongue=(1.0,0.3,0.35), lgrey=(0.82,0.82,0.86), beige=(0.95,0.85,0.65), peach=(1.0,0.75,0.6), lavender=(0.75,0.65,1.0), silver=(0.8,0.82,0.88),
           wood=(0.7,0.45,0.2), glass=(0.6,0.85,1.0), mint=(0.6,0.9,0.75), chocolate=(0.35,0.18,0.08), straw=(0.95,0.8,0.45))
_MC = {}
def mat(c, rough=0.6, emit=0.0):
    key = (c, rough, emit)
    if key in _MC: return _MC[key]
    rgb = PAL[c] if isinstance(c, str) else c
    m = bpy.data.materials.new(str(c)); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    for k in ("Specular IOR Level", "Specular"):
        if k in b.inputs: b.inputs[k].default_value = 0.25
    if emit:
        b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = emit
    _MC[key] = m; return m
def par(o, p):
    if p is not ROOT: bpy.context.view_layer.update()
    o.parent = p; o.matrix_parent_inverse = p.matrix_world.inverted()
def smooth(o):
    for p in o.data.polygons: p.use_smooth = True
def _fin(o, c, parent, rot, name, sm=True):
    o.name = name; o.data.materials.append(mat(c))
    if rot: o.rotation_euler = rot
    if sm: smooth(o)
    par(o, parent or ROOT); return o
def E(loc, parent=None, name="E"):
    o = bpy.data.objects.new(name, None); o.location = loc; o.empty_display_size = 0.2; scene.collection.objects.link(o)
    if parent or ROOT: par(o, parent or ROOT)
    return o
def S(r, loc, scale=(1,1,1), c="white", parent=None, rot=None, name="o", seg=24, ring=14):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=ring, radius=r, location=loc)
    o = bpy.context.active_object; o.scale = scale; return _fin(o, c, parent, rot, name)
def B(loc, scale, c="white", parent=None, rot=None, bevel=0.0, name="o"):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.active_object; o.scale = scale
    if bevel > 0:
        bm = o.modifiers.new("Bevel", 'BEVEL'); bm.width = bevel; bm.segments = 4; bm.use_clamp_overlap = True
        try: bm.harden_normals = True
        except Exception: pass
    return _fin(o, c, parent, rot, name, sm=bevel > 0)
def Cy(r, d, loc, c="white", rot=(0,0,0), parent=None, verts=24, name="o"):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=loc, rotation=rot)
    return _fin(bpy.context.active_object, c, parent, None, name)
def Co(r1, d, loc, c="white", rot=(0,0,0), parent=None, r2=0.0, verts=24, name="o"):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=d, location=loc, rotation=rot)
    return _fin(bpy.context.active_object, c, parent, None, name)
def To(R, r, loc, c="white", rot=(0,0,0), parent=None, name="o", scale=(1,1,1)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot, major_segments=32, minor_segments=12)
    o = bpy.context.active_object; o.scale = scale; return _fin(o, c, parent, None, name)
def Fp(pts, loc, thick, c, parent=None, rot=None, name="o"):
    vs = []; n = len(pts)
    for layer in (0, 1):
        y = -thick/2 + layer*thick
        for (x, z) in pts: vs.append((x, y, z))
    faces = [list(range(n)), list(range(n, 2*n))[::-1]] + [[i, (i+1) % n, (i+1) % n + n, i+n] for i in range(n)]
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], faces); me.update()
    o = bpy.data.objects.new(name, me); scene.collection.objects.link(o); o.location = loc
    return _fin(o, c, parent, rot, name, sm=False)
def halfdisc(loc, r, thick, c, parent=None, flip=False, segs=16, rot=None):
    pts = [(0,0)] + [(r*math.cos(math.pi+math.pi*i/segs), (-1 if flip else 1)*r*math.sin(math.pi+math.pi*i/segs)) for i in range(segs+1)]
    return Fp(pts, loc, thick, c, parent, rot)
def starpts(ro, ri, n=5): return [((ro if i % 2 == 0 else ri)*math.cos(math.pi/2+i*math.pi/n), (ro if i % 2 == 0 else ri)*math.sin(math.pi/2+i*math.pi/n)) for i in range(2*n)]
EYES = []; LIDS = []
def eyes(z, y, spread=0.2, r=0.12, parent=None, x=0.0, fwd=(0,-1,0), dz=0.0, rim=None):
    f = Vector(fwd).normalized()
    for sx in (-1, 1):
        p = Vector((x+sx*spread, y, z))
        if rim: S(r*1.35, p+f*(-0.02), (1,0.4,1), rim, parent, name="EyeRim")
        EYES.extend([S(r, p, (1,0.5,1), "white", parent, name="Eye"),
                 S(r*0.55, p+f*(r*0.6), (1,0.5,1), "black", parent, name="Pupil", seg=16, ring=10),
                 S(r*0.18, p+f*(r*0.95)+Vector((-r*0.25,0,r*0.35)), (1,1,1), "white", parent, name="Shine", seg=10, ring=6)])
        LIDS.append((p+f*(r*0.4), parent, r))
def smile(z, y, r=0.14, parent=None, x=0.0, tongue=True, rot=None):
    halfdisc((x, y, z), r, 0.05, "mouth", parent, rot=rot)
    if tongue: halfdisc((x, y-0.02, z-r*0.35), r*0.45, 0.05, "tongue", parent, rot=rot)
def face(z, y, spread=0.2, r=0.12, parent=None, x=0.0, mouth_dz=None, mr=None, fwd=(0,-1,0), tongue=True):
    eyes(z, y, spread, r, parent, x, fwd)
    smile(z-(mouth_dz if mouth_dz is not None else r*1.9), y, mr if mr else r*1.1, parent, x, tongue)
def legs4(c, z=0.0, h=0.35, r=0.1, dx=0.25, dy=0.3, parent=None, foot=None):
    out = []
    for (x, y) in [(-dx,-dy),(dx,-dy),(-dx,dy),(dx,dy)]:
        p = E((x, y, z+h), parent); Cy(r, h, (x, y, z+h/2), c, parent=p)
        if foot: S(r*1.3, (x, y-0.03, z+r*0.6), (1,1.2,0.6), foot, p)
        out.append(p)
    return out
def legs2(c, z=0.0, h=0.3, r=0.06, dx=0.18, parent=None, foot=None):
    out = []
    for x in (-dx, dx):
        p = E((x, 0, z+h), parent); Cy(r, h, (x, 0, z+h/2), c, parent=p)
        if foot: S(r*1.8, (x, -0.04, z+r*0.8), (1,1.6,0.5), foot, p)
        out.append(p)
    return out
def kf(o, prop, f): o.keyframe_insert(prop, frame=f)
def sine(o, prop, axis, amp, cycles, base=0.0, phase=0.0, n=None):
    n = n or NFRAMES
    for f in range(1, n+2):
        t = (f-1)/n; v = list(getattr(o, prop)); v[axis] = base + amp*math.sin(TAU*cycles*t + phase); setattr(o, prop, v); kf(o, prop, f)
def keys(o, prop, lst):
    for f, v in lst: setattr(o, prop, v); kf(o, prop, f)
# ---------------- action curves (shared per group) ----------------
def act_hop(h):
    n = NFRAMES; sc = n/24.0
    K = [(1,0,(1,1,1)),(4,0,(1.14,1.14,0.74)),(6,0.35,(0.9,0.9,1.24)),(12,1.2,(1,1,1.02)),(17,0.45,(0.93,0.93,1.12)),(19,0,(1.25,1.25,0.7)),(22,0,(0.96,0.96,1.06)),(24,0,(1,1,1))]
    for f, z, s in K:
        ff = max(1, min(n, int((f-1)*sc+0.5)+1)) if n != 24 else f
        ROOT.location = (0,0,z); ROOT.scale = s; kf(ROOT,"location",ff); kf(ROOT,"scale",ff)
def act_drive(h):
    body = h.get("body", ROOT); legs = h.get("legs", [])
    if legs:   # animals: real four-leg trot (diagonal pairs), body bounces twice per stride
        n = len(legs)
        for i, l in enumerate(legs):
            ph = math.pi * ((i + (1 if (n >= 4 and i >= n/2) else 0)) % 2)      # 4 legs: diagonal pairs; 2 legs: alternate
            sine(l, "rotation_euler", 0, rad(h.get("legamp", 38)), 2, phase=ph)
        for i, a in enumerate(h.get("arms", [])): sine(a, "rotation_euler", 0, rad(40), 2, phase=math.pi*((i+1) % 2))
        sine(body, "location", 2, 0.09, 4, base=body.location.z, phase=-math.pi/2)
        sine(body, "rotation_euler", 0, rad(5), 2, phase=1.0)
        if "head" in h: sine(h["head"], "rotation_euler", 0, rad(8), 4, phase=math.pi/2)
        if "tail" in h: sine(h["tail"], "rotation_euler", 2, rad(18), 2)
    else:      # vehicles: 12 cm bounce + pitch +-6 deg, wheels spin twice per loop
        sine(body, "location", 2, 0.12, 2, base=body.location.z)
        sine(body, "rotation_euler", 0, rad(6), 2, phase=1.0)
    for w in h.get("wheels", []):
        for f in range(1, NFRAMES+2): w.rotation_euler = (2*TAU*(f-1)/NFRAMES, 0, 0); kf(w, "rotation_euler", f)
def act_fly(h):
    for key in ("rotor", "tailrotor"):
        if key in h:
            ax = 2 if key == "rotor" else 0
            for f in range(1, NFRAMES+2):
                v = [0, 0, 0]; v[ax] = TAU*3*(f-1)/NFRAMES; h[key].rotation_euler = v; kf(h[key], "rotation_euler", f)
    for i, w in enumerate(h.get("wings", [])):
        sx = -1 if i % 2 == 0 else 1
        sine(w, "rotation_euler", 1, rad(h.get("flap", 45))*sx, 3)
    sine(ROOT, "location", 2, 0.26, 1)
    sine(ROOT, "rotation_euler", 1, rad(7), 1, phase=math.pi/2)
    sine(ROOT, "rotation_euler", 0, rad(4), 1, phase=0)
def act_swim(h):
    if "tail" in h: sine(h["tail"], "rotation_euler", 2, rad(h.get("tailamp", 35)), 2)
    for i, c in enumerate(h.get("claws", [])): sine(c, "rotation_euler", 2, rad(28), 2, phase=math.pi*i)
    for i, f_ in enumerate(h.get("fins", [])): sine(f_, "rotation_euler", 1, rad(25)*(-1 if i % 2 else 1), 2)
    sine(ROOT, "rotation_euler", 2 if h.get("yawaxis", 2) == 2 else 1, rad(h.get("sway", 10)), 2, phase=math.pi)
    sine(ROOT, "location", 2, 0.14, 1)
    sine(ROOT, "rotation_euler", 0, rad(4), 1, phase=math.pi/2)
def act_wiggle(h):
    sine(ROOT, "rotation_euler", 1, rad(22), 2)
    for f in range(1, NFRAMES+2):
        t = (f-1)/NFRAMES; s = 1+0.10*math.sin(TAU*2*t+math.pi/2); ROOT.scale = (s, s, 2-s); kf(ROOT, "scale", f)
def act_spin(h):
    for f in range(1, NFRAMES+2): ROOT.rotation_euler = (0, 0, TAU*(f-1)/NFRAMES); kf(ROOT, "rotation_euler", f)
    keys(ROOT, "scale", [(1,(1,1,1)),(7,(0.9,0.9,1.12)),(13,(1.1,1.1,0.92)),(19,(0.9,0.9,1.12)),(25,(1,1,1))])
    sine(ROOT, "location", 2, 0.12, 1, phase=-math.pi/2); 
def act_float(h):
    sine(ROOT, "location", 2, 0.3, 1); sine(ROOT, "rotation_euler", 1, rad(9), 1, phase=math.pi/2); sine(ROOT, "location", 0, 0.1, 1, phase=math.pi/2)
def act_grow(h):
    keys(ROOT, "scale", [(1,(1,1,1)),(6,(0.78,0.78,0.7)),(14,(1.28,1.28,1.32)),(20,(0.94,0.94,0.92)),(25,(1,1,1))])
    sine(ROOT, "rotation_euler", 1, rad(6), 1, phase=math.pi/2)
def act_flash(h):
    keys(ROOT, "location", [(1,(0,0,0)),(5,(0,0,0.45)),(9,(0,0,0)),(13,(0,0,0.45)),(17,(0,0,0)),(21,(0,0,0.38)),(25,(0,0,0))])
    keys(ROOT, "scale", [(1,(1,1,1)),(5,(0.88,0.88,1.22)),(9,(1.16,1.16,0.86)),(13,(0.88,0.88,1.22)),(17,(1.16,1.16,0.86)),(25,(1,1,1))])
    for m in h.get("glow", []):
        inp = m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
        for f in range(1, NFRAMES+2): inp.default_value = 1.2+1.3*math.sin(TAU*3*(f-1)/NFRAMES); inp.keyframe_insert("default_value", frame=f)
def act_ring(h):
    sine(h["pivot"], "rotation_euler", 1, rad(38), 2)
    sine(ROOT, "location", 2, 0.08, 4, phase=-math.pi/2)
def normalize_height(target=2.1, maxw=3.3):
    """scale everything under ROOT so the standing height is `target` (capped by width)"""
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); pts = []
    for ob in scene.objects:
        if ob.type in ('MESH','FONT','CURVE') and not ob.hide_render:
            ev = ob.evaluated_get(dg); pts += [ev.matrix_world @ Vector(c) for c in ev.bound_box]
    hgt = max(p.z for p in pts) - min(p.z for p in pts); wid = max(max(p.x for p in pts) - min(p.x for p in pts), max(p.y for p in pts) - min(p.y for p in pts))
    k = min(target/hgt, maxw/wid); sc = E((0, 0, 0), ROOT, "Scale")
    for ob in list(ROOT.children):
        if ob is not sc: par(ob, sc)
    sc.scale = (k, k, k); bpy.context.view_layer.update(); return k
ACTS = dict(hop=act_hop, drive=act_drive, fly=act_fly, swim=act_swim, wiggle=act_wiggle, spin=act_spin, float=act_float, grow=act_grow, flash=act_flash, ring=act_ring, jump=act_hop)
def SLEEP():
    for ob in bpy.data.objects:
        if ob.animation_data: ob.animation_data_clear()
    for m in bpy.data.materials:
        if m.node_tree and m.node_tree.animation_data: m.node_tree.animation_data_clear()
    scene.frame_set(1)
    for e in EYES: e.hide_render = True
    for (p, parent, r) in LIDS: B(tuple(p), (r*1.7, 0.03, 0.04), "ink", parent, name="Lid")
    if "sleep" in H and callable(H["sleep"]): H["sleep"]()
    ROOT.location = (0, 0, 0); ROOT.rotation_euler = (rad(-6), 0, 0); ROOT.scale = (0.93, 0.93, 0.9)
# =====================================================================
ROOT = None
ROOT = E((0, 0, 0), None, "Root")
H = {}
exec(open(PIPE + "/__BUILDERS__", encoding="utf-8").read())
H = BUILD[NAME]() or {}
ACTS[GROUP](H)
scene.frame_set(1)
