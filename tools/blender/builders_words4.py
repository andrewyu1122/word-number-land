# Silhouette-test remakes (Nov 2026): every model must be recognisable as a pure black silhouette of its idle frame.
# Helpers: tube() sweeps a smooth tapered tube along a path, spline() smooths a few control points,
# finish() turns the model towards the camera, scales it to a standard height and keeps the sleep lids on the eyes.
exec(open(PIPE + "/builders_words3.py", encoding="utf-8").read().rsplit(chr(10) + "BUILD = {k[2:]", 1)[0])
for _k in [k for k in list(globals()) if k.startswith("b_")]: del globals()[_k]      # only this file's words
import bmesh
from mathutils import Matrix, Euler
PAL.update(dict(crust=(0.72, 0.43, 0.17), crumb=(1.0, 0.9, 0.66), croc=(0.13, 0.46, 0.18), crocd=(0.07, 0.3, 0.1), crocb=(0.8, 0.88, 0.5), lava=(1.0, 0.32, 0.03),
                rock=(0.58, 0.38, 0.22), rockd=(0.45, 0.28, 0.16), stonel=(0.93, 0.86, 0.7), stoned=(0.78, 0.7, 0.55), tig=(1.0, 0.52, 0.08), raisin=(0.34, 0.14, 0.25),
                acorn=(0.95, 0.74, 0.4), capb=(0.5, 0.3, 0.13), capl=(0.68, 0.45, 0.22), eaglb=(0.36, 0.21, 0.1), eagld=(0.26, 0.14, 0.06), bullb=(0.44, 0.25, 0.14),
                kang=(0.85, 0.55, 0.28), squi=(0.9, 0.45, 0.12), gir=(1.0, 0.8, 0.25), girs=(0.6, 0.33, 0.1), mtn=(0.5, 0.56, 0.8), mtnd=(0.4, 0.45, 0.7)))
def flat(o):
    for p in o.data.polygons: p.use_smooth = False
    return o
def spline(pts, n=24):
    P = [Vector(p) for p in pts]; P = [P[0]*2 - P[1]] + P + [P[-1]*2 - P[-2]]; out = []; m = len(P) - 3
    for k in range(n + 1):
        u = k/n*m; i = min(int(u), m - 1); t = u - i; p0, p1, p2, p3 = P[i:i + 4]
        out.append(0.5*((2*p1) + (-p0 + p2)*t + (2*p0 - 5*p1 + 4*p2 - p3)*t*t + (-p0 + 3*p1 - 3*p2 + p3)*t*t*t))
    return out
def lerpr(r0, r1, n): return [r0 + (r1 - r0)*k/n for k in range(n + 1)]
def tube(path, radii, c, seg=16, ref=(0, 1, 0), parent=None, mats=None, cfun=None, cap=True, sm=True, name="tube"):
    """sweep a ring along path; radii = r or (rx along ref, ry); cfun(ring, segment) -> material index into mats"""
    P = [Vector(p) for p in path]; n = len(P); vs = []
    for i in range(n):
        T = (P[min(i + 1, n - 1)] - P[max(i - 1, 0)]).normalized(); U = Vector(ref); U = U - T*U.dot(T)
        if U.length < 1e-4: U = Vector((1, 0, 0)) - T*T.x
        U.normalize(); V = T.cross(U); r = radii[i]; rx, ry = r if isinstance(r, (tuple, list)) else (r, r)
        for j in range(seg): a = TAU*j/seg; vs.append((P[i] + U*(rx*math.cos(a)) + V*(ry*math.sin(a))).to_tuple())
    faces = []; fi = []
    for i in range(n - 1):
        for j in range(seg): faces.append([i*seg + j, i*seg + (j + 1) % seg, (i + 1)*seg + (j + 1) % seg, (i + 1)*seg + j]); fi.append((i, j))
    if cap:
        faces.append(list(range(seg))[::-1]); fi.append((0, 0)); faces.append([(n - 1)*seg + j for j in range(seg)]); fi.append((n - 2, 0))
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], faces); me.update()
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); scene.collection.objects.link(o)
    for m in (mats or [c]): me.materials.append(mat(m))
    if cfun:
        for k, p in enumerate(me.polygons): p.material_index = cfun(*fi[k])
    if sm: smooth(o)
    par(o, parent or ROOT); return o
def swing(e, rot):
    """rotate a sub-assembly and keep the sleep lids of any face inside it in place"""
    bpy.context.view_layer.update(); b = e.matrix_world.copy(); e.rotation_euler = rot; bpy.context.view_layer.update()
    D = e.matrix_world @ b.inverted()
    for i, (p, parent, r) in enumerate(LIDS):
        q = parent
        while q is not None and q is not e: q = q.parent
        if q is e: LIDS[i] = (D @ Vector(p), parent, r)
def finish(h=2.2, maxw=2.7, turn=0.0, tilt=0.0, roll=0.0, H=None):
    """turn (deg about Z; -45 = front faces the camera), scale to the standard height, fix the lids for the sleep still"""
    H = H if H is not None else {}
    tr = E((0, 0, 0), ROOT, "Turn")
    for ob in list(ROOT.children):
        if ob is not tr: par(ob, tr)
    eu = Euler((rad(tilt), rad(roll), rad(turn))); tr.rotation_euler = eu; bpy.context.view_layer.update()
    k = normalize_height(h, maxw); R = eu.to_matrix().to_4x4(); M = Matrix.Scale(k, 4) @ R
    for i, (p, parent, r) in enumerate(LIDS): LIDS[i] = (M @ Vector(p), parent, r*k)
    def _sl():
        bpy.context.view_layer.update(); Rw = ROOT.matrix_world.copy()
        for ob in bpy.data.objects:
            if ob.name.startswith("Lid"):
                mw = ob.matrix_world.copy(); ob.matrix_world = Rw @ Matrix.Translation(mw.translation) @ R @ Matrix.Diagonal(mw.to_scale()).to_4x4()
    H["sleep"] = _sl; return H
# ================================================================ batch 1
def b_banana():
    n = 20; body = spline([(0.3, 0, 0.0), (0.08, 0, 0.5), (0.0, 0, 1.0), (0.1, 0, 1.5)], n)
    tube(body, [0.09 + 0.26*min(1.0, k/5.0)**0.7 for k in range(n + 1)], "yellow", seg=24, mats=["yellow", "dkbrown"], cfun=lambda i, j: 1 if i < 1 else 0)
    flesh = spline([(0.1, 0, 1.45), (0.24, 0, 1.95), (0.5, 0, 2.4)], 14)
    tube(flesh, [0.27*(1 - (k/14.0)**3)**0.5 + 0.02 for k in range(15)], "cream", seg=24, mats=["cream", "dkbrown"], cfun=lambda i, j: 1 if i > 12 else 0)
    c = Vector((0.1, 0, 1.5))
    for a in (0, 180, 90):
        d = Vector((math.cos(rad(a)), math.sin(rad(a)), 0)); s = c + d*0.26; up = Vector((0, 0, 1))
        pts = spline([s - up*0.1, s + d*0.3 + up*0.16, s + d*0.68 - up*0.1, s + d*0.86 - up*0.55, s + d*0.82 - up*0.98], 16)
        tube(pts, [(0.3 - 0.2*(k/16.0)**2, 0.05) for k in range(17)], "yellow", seg=12, ref=(-d.y, d.x, 0), mats=["yellow", "dkbrown"], cfun=lambda i, j: 1 if i > 14 else 0)
    sface(0.95, 0.14, 0.095, x=0.01, mouth_dz=0.25, mr=0.08)
    return finish(2.4, 2.4, turn=-30)
def b_river():
    BX((0, 0, 0.1), (2.9, 2.9, 0.2), "grass", bevel=0.09)
    fx = lambda y: 0.5*math.sin(y*1.9); ys = [1.45 - 2.9*k/28 for k in range(29)]
    tube([(fx(y), y, 0.19) for y in ys], [(0.78, 0.03)]*29, "sand", seg=12, ref=(1, 0, 0))
    tube([(fx(y), y, 0.2) for y in ys], [(0.66, 0.04)]*29, "water", seg=12, ref=(1, 0, 0))
    for (y, dx) in [(-1.1, 0.2), (-0.55, -0.3), (0.35, 0.25), (0.95, -0.2), (-0.05, 0.3)]:
        S(0.09, (fx(y) + dx, y, 0.245), (0.5, 1.9, 0.12), "white", rot=(0, 0, -math.atan(0.95*math.cos(y*1.9))))
    for (x, y, r) in [(1.05, -1.0, 0.2), (-1.1, 0.1, 0.15), (1.1, 0.7, 0.17), (-0.35, 0.6, 0.13), (-1.0, -1.15, 0.12)]: S(r, (x, y, 0.2 + r*0.5), (1.2, 1, 0.75), "stone")
    for (x, y) in [(-1.15, -0.7), (1.2, 0.15), (-1.1, 1.15), (1.15, -0.45)]:
        for k in range(3): Co(0.045, 0.38, (x + 0.08*k, y + 0.05*(k % 2), 0.38), "dkgreen", (0, rad(12*(k - 1)), 0))
    S(0.34, (0.1, -0.1, 1.25), (1.6, 0.6, 1.0), "orange", rot=(0, rad(-40), 0)); Fp([(0, 0), (-0.42, 0.32), (-0.42, -0.32)], (-0.27, -0.1, 0.94), 0.06, "red", rot=(0, rad(-40), 0))
    Fp([(0, 0), (-0.26, 0.26), (-0.32, 0.0)], (0.1, -0.1, 1.54), 0.05, "red", rot=(0, rad(-40), 0))
    eyes(1.46, -0.29, 0.0, 0.095, x=0.36)
    To(0.26, 0.045, (-0.2, -0.1, 0.25), "white", scale=(1, 1, 0.6))
    for (x, z) in [(-0.5, 0.6), (-0.38, 0.42), (-0.12, 0.55), (0.05, 0.4), (-0.3, 0.78)]: S(0.06, (x, -0.1, z), (1, 1, 1.3), "sky")
    return finish(2.0, 3.0, turn=-35, tilt=24)
def b_raisin():
    o = S(0.62, (-0.3, 0, 0.62), (1.15, 0.95, 1.0), "raisin", seg=64, ring=40)
    for v in o.data.vertices:
        p = v.co; th = math.atan2(p.y, p.x); ph = math.acos(max(-1.0, min(1.0, p.z/0.62)))
        f = 1 - 0.17*(1 - abs(math.sin(4*th + 1.6*math.sin(4*ph)))**0.7) - 0.07*(1 - abs(math.sin(5*ph + 2*th))) + 0.07*math.sin(2*th + 1)*math.sin(2*ph)
        v.co = p*f
    RC(0.035, 0.16, (-0.3, 0, 1.2), "brown", lv=1)
    g = E((0.78, 0.25, 0))
    BX((0.78, 0.25, 0.62), (0.72, 0.42, 1.24), "red", g, bevel=0.03); BX((0.78, -0.06, 1.33), (0.72, 0.04, 0.36), "red", g, rot=(rad(-55), 0, 0), bevel=0.02)
    Cy(0.24, 0.03, (0.78, 0.035, 0.82), "yellow", (R90, 0, 0), g)
    for (x, z) in [(-0.07, 0.9), (0.07, 0.9), (0.0, 0.79), (-0.07, 0.75), (0.07, 0.72), (0.0, 0.65)]: S(0.07, (0.78 + x, 0.0, z), (1, 0.5, 1), "purple", g)
    BX((0.78, 0.03, 0.3), (0.5, 0.02, 0.12), "white", g, bevel=0.01)
    swing(g, (0, 0, rad(-14)))
    for (x, y) in [(0.45, -0.55), (0.72, -0.42)]: S(0.1, (x, y, 0.09), (1.2, 0.9, 0.8), "raisin")
    sface(0.72, 0.2, 0.11, x=-0.3, mouth_dz=0.27, mr=0.1)
    return finish(2.0, 2.7, turn=-10)
def b_crocodile():
    G, D, Bc = "croc", "crocd", "crocb"; tail = E((0, 1.05, 0.5))
    S(0.5, (0, 0.2, 0.52), (0.95, 2.0, 0.78), G); S(0.46, (0, 0.2, 0.42), (0.9, 1.9, 0.62), Bc)
    S(0.42, (0, -0.95, 0.6), (0.95, 1.15, 0.82), G)
    RB((0, -1.7, 0.66), (0.5, 1.25, 0.22), G, lv=2); RB((0, -1.62, 0.36), (0.44, 1.1, 0.15), Bc, rot=(rad(9), 0, 0), lv=2); BX((0, -1.5, 0.5), (0.34, 0.9, 0.1), "mouth", bevel=0.02)
    for sx in (-1, 1):
        for k in range(6): Co(0.05, 0.15, (sx*0.21, -1.25 - 0.17*k, 0.52), "white", (math.pi, 0, 0), verts=8)
        for k in range(4): Co(0.045, 0.13, (sx*0.19, -1.35 - 0.2*k, 0.47 + 0.02*k), "white", verts=8)
        S(0.065, (sx*0.1, -2.22, 0.78), (1, 1, 0.8), D); S(0.19, (sx*0.22, -0.98, 0.98), (1, 1, 1), G)
        for (y, s) in ((-0.45, 1.0), (0.85, 1.1)):
            S(0.2*s, (sx*0.5, y, 0.22), (1.0, 1.2, 1.0), G); S(0.17*s, (sx*0.68, y - 0.12, 0.1), (1.3, 1.5, 0.55), G)
            for k in range(3): Co(0.035, 0.12, (sx*0.68 + 0.08*(k - 1), y - 0.38, 0.06), "white", (R90, 0, 0), verts=8)
    eyes(1.02, -1.13, 0.22, 0.115)
    for k in range(7): Co(0.12, 0.26, (0, -0.55 + 0.24*k, 0.94 - 0.012*k*k/2), D, verts=4)
    pts = spline([(0, 1.0, 0.5), (0.1, 1.75, 0.44), (0.42, 2.4, 0.38), (0.95, 2.8, 0.34)], 20)
    tube(pts, [(0.36 - 0.33*(k/20.0), 0.36 - 0.31*(k/20.0)) for k in range(21)], G, seg=16, ref=(1, 0, 0), parent=tail)
    for k in range(2, 18, 2): p = pts[k]; Co(0.1 - 0.004*k, 0.24 - 0.008*k, (p.x, p.y, p.z + 0.36 - 0.31*k/20.0 + 0.06), D, parent=tail, verts=4)
    return finish(1.5, 3.3, turn=22, H={"tail": tail, "tailamp": 22, "sway": 6})
def b_ball():
    o = S(0.95, (0, 0, 0.95), (1, 1, 1), "white", seg=48, ring=24); cols = ["red", "yellow", "blue", "white"]
    for c in cols[:3]: o.data.materials.append(mat(c))     # slot 0 = white
    for p in o.data.polygons:
        c = p.center; k = int((math.atan2(c.y, c.x) + math.pi)/TAU*8) % 8
        p.material_index = 0 if abs(c.z) > 0.95*0.93 else [1, 2, 3, 0][k % 4]
    o.rotation_euler = (rad(38), rad(-22), 0)
    sface(0.85, 0.22, 0.12, mouth_dz=0.3, mr=0.11)
    return finish(2.0, 2.6)
def _slice(): return [(-0.5, 0), (0.5, 0), (0.5, 0.72)] + [(0.6*math.cos(rad(a)), 0.86 + 0.4*math.sin(rad(a))) for a in range(-20, 201, 20)] + [(-0.5, 0.72)]
def _sc(pts, s, c=(0, 0)): return [(c[0] + (x - c[0])*s, c[1] + (z - c[1])*s) for x, z in pts]
def b_bread():
    P = _sc(_slice(), 1.3); Q = _sc(P, 0.88, (0, 0.82))
    Fp(P, (0, 0.6, 0), 1.5, "crust"); Fp(Q, (0, -0.155, 0), 0.02, "crumb")
    for k in range(3): BX((0, 0.25 + 0.4*k, 1.63), (0.7, 0.05, 0.04), "capb", bevel=0.01)
    for (y, ang, x) in [(-0.5, -8, 0.1), (-1.0, -24, 0.28)]:
        g = E((x, y, 0)); Fp(P, (x, y, 0), 0.17, "crust", g); Fp(Q, (x, y, 0), 0.19, "crumb", g); swing(g, (rad(ang), 0, 0))
    sface(0.9, 0.22, 0.11, x=0.28, mouth_dz=0.3, mr=0.1)
    return finish(2.0, 2.7, turn=-22)
def b_nut():
    n = 24; tube([(0, 0, -0.3 + 1.6*k/n) for k in range(n + 1)], [0.02 + 0.6*math.sin(math.pi/2*(k/n)**0.62) for k in range(n + 1)], "acorn", seg=32)
    S(0.74, (0, 0, 1.3), (1, 1, 0.7), "capb", seg=32, ring=20)
    for i in range(5):
        ph = 0.2 + 0.3*i; m = max(1, int(3 + 5.2*i))
        for k in range(m):
            a = TAU*(k + 0.5*(i % 2))/m; S(0.1, (0.74*math.sin(ph)*math.cos(a), 0.74*math.sin(ph)*math.sin(a), 1.3 + 0.74*0.7*math.cos(ph)), (1, 1, 0.75), "capl", seg=12, ring=8)
    tube(spline([(0, 0, 1.75), (0.03, 0, 1.98), (0.16, 0, 2.15)], 8), lerpr(0.08, 0.065, 8), "capb", seg=12)
    sface(0.62, 0.2, 0.11, mouth_dz=0.27, mr=0.1)
    return finish(2.25, 2.6, roll=-8)
def b_egg():
    o = S(0.56, (0, 0, 1.52), (1, 1, 1.3), (1.0, 0.98, 0.93), seg=40, ring=24)
    for v in o.data.vertices: f = 1 - 0.2*v.co.z/0.56; v.co.x *= f; v.co.y *= f
    Co(0.3, 0.64, (0, 0, 0.95), "blue", r2=0.66, verts=40); To(0.66, 0.055, (0, 0, 1.27), "blue"); Cy(0.15, 0.4, (0, 0, 0.48), "blue")
    Co(0.56, 0.24, (0, 0, 0.16), "blue", r2=0.16, verts=40); Cy(0.56, 0.06, (0, 0, 0.03), "blue", verts=40)
    for a in (-75, -45, -15, 15, 45, 75):
        zz = 1.0 + 0.1*((a // 30) % 2); rr = 0.3 + 0.36*(zz - 0.63)/0.64; S(0.075, (rr*math.sin(rad(a)), -rr*math.cos(rad(a)), zz), (1, 1, 1), "white")
    sface(1.75, 0.19, 0.1, mouth_dz=0.25, mr=0.09)
    return finish(2.25, 2.6)
def b_coat():
    C = "red"; N = "navy"; yb = lambda z, x=0.0: -0.5*math.sqrt(max(0.0, (0.6 + 0.35*(2.0 - z)/2.375)**2 - x*x))
    o = Co(0.95, 1.9, (0, 0, 1.05), C, r2=0.6, verts=40); o.scale = (1, 0.5, 1.25); o.location.z = 0.8125
    S(0.62, (0, 0, 1.97), (1.12, 0.5, 0.36), C)
    for sx in (-1, 1):
        tube([(sx*0.58, 0, 1.95), (sx*0.8, 0, 1.4), (sx*1.04, 0, 0.75)], [0.24, 0.22, 0.21], C, seg=16)
        tube([(sx*1.02, 0, 0.8), (sx*1.08, 0, 0.62)], [0.235, 0.235], N, seg=16)
        Fp([(0, -0.5), (sx*0.44, 0.22), (sx*0.1, 0.3)], (0, -0.36, 1.78), 0.07, N)
        BX((sx*0.47, yb(0.62, 0.47) - 0.01, 0.62), (0.38, 0.06, 0.32), (0.72, 0.04, 0.06), rot=(0, 0, rad(sx*22)), bevel=0.025)
        BX((sx*0.47, yb(0.8, 0.47) - 0.03, 0.8), (0.42, 0.06, 0.12), N, rot=(0, 0, rad(sx*22)), bevel=0.025)
    To(0.3, 0.1, (0, 0, 2.1), N, scale=(1.25, 0.7, 1)); Cy(0.03, 0.2, (0, 0, 2.28), "silver"); To(0.13, 0.03, (0.0, 0, 2.48), "silver", (R90, 0, 0))
    BX((0, yb(0.4) - 0.005, 0.4), (0.03, 0.02, 1.5), (0.6, 0.03, 0.05), bevel=0.0)
    for z in (0.95, 0.6, 0.25, -0.1): S(0.11, (0, yb(z) - 0.01, z), (1, 0.4, 1), "gold")
    face(1.5, yb(1.5) - 0.0, 0.2, 0.1, mouth_dz=0.27, mr=0.09)
    return finish(2.35, 2.7, turn=-35)
def b_door():
    W = "white"; D = "red"; Dd = (0.7, 0.04, 0.05)
    for sx in (-1, 1): BX((sx*0.66, 0, 1.2), (0.18, 0.32, 2.3), W, bevel=0.03)
    BX((0, 0, 2.42), (1.66, 0.38, 0.22), W, bevel=0.03); BX((0, -0.12, 0.05), (1.8, 0.8, 0.1), "lgrey", bevel=0.03); BX((0, 0.1, 1.2), (1.2, 0.04, 2.2), "navy", bevel=0.0)
    hg = E((-0.56, -0.02, 0.1))
    BX((0, -0.02, 1.2), (1.12, 0.1, 2.18), D, hg, bevel=0.02)
    for sx in (-1, 1):
        BX((sx*0.26, -0.075, 1.75), (0.38, 0.03, 0.72), Dd, hg, bevel=0.012); BX((sx*0.26, -0.075, 0.68), (0.38, 0.03, 0.9), Dd, hg, bevel=0.012)
    S(0.1, (0.42, -0.14, 1.2), (1, 1, 1), "gold", hg); Cy(0.045, 0.1, (0.42, -0.09, 1.2), "gold", (R90, 0, 0), hg)
    face(1.78, -0.09, 0.26, 0.11, parent=hg, mouth_dz=0.48, mr=0.1)
    swing(hg, (0, 0, rad(-34)))
    return finish(2.45, 2.7, turn=-28)
# ================================================================ batch 2
def b_net():
    u = Vector((0.535, 0, 0.845)); e = Vector((0.2, 0, 1.55)); C = e + u*0.62
    tube([(-0.75, 0, 0.05), e.to_tuple()], [0.055, 0.05], "wood", seg=12); tube([(-0.75, 0, 0.05), (-0.48, 0, 0.47)], [0.075, 0.075], "red", seg=12)
    up = Vector((0, 0, 1)); yv = Vector((0, 1, 0))
    path = spline([C, C + yv*0.3 - up*0.08, C + yv*0.55 - up*0.6, C + yv*0.6 - up*1.25], 16)
    rr = [0.6, 0.6, 0.59, 0.58, 0.56, 0.54, 0.51, 0.48, 0.45, 0.42, 0.39, 0.35, 0.31, 0.26, 0.21, 0.16, 0.1]
    sface(C.z - 0.72, 0.15, 0.09, x=C.x, mouth_dz=0.22, mr=0.08) if False else None
    tube(path, rr, "white", seg=20, ref=(1, 0, 0), mats=["white", (0.62, 0.85, 1.0)], cfun=lambda i, j: (i + j) % 2, cap=False)
    S(0.1, tuple(path[-1]), (1, 1, 1), "white")
    To(0.6, 0.05, C.to_tuple(), "red", (R90, 0, 0))
    sface(C.z - 0.74, 0.15, 0.09, x=C.x, mouth_dz=0.22, mr=0.08, fb=0.3)
    bx, bz = -0.42, 1.95
    S(0.04, (bx, 0, bz), (1, 1, 2.6), "ink")
    for sx in (-1, 1): S(0.15, (bx + sx*0.15, 0, bz + 0.07), (1, 0.15, 1.1), "orange", rot=(0, rad(sx*-20), 0)); S(0.11, (bx + sx*0.11, 0, bz - 0.1), (1, 0.15, 1), "hotpink")
    return finish(2.5, 2.7, turn=-30)
def b_nose():
    SK = (1.0, 0.82, 0.68); NS = (1.0, 0.56, 0.5)
    S(0.95, (0, 0.25, 1.05), (1, 0.95, 1.05), SK)
    for sx in (-1, 1): S(0.24, (sx*0.93, 0.3, 1.05), (0.6, 0.8, 1.1), SK)
    tube(spline([(0, -0.55, 1.5), (0, -0.95, 1.2), (0, -1.3, 0.85)], 10), lerpr(0.2, 0.36, 10), NS, seg=16, ref=(1, 0, 0))
    S(0.4, (0, -1.32, 0.82), (1, 1, 0.95), NS)
    for sx in (-1, 1):
        S(0.25, (sx*0.3, -1.05, 0.72), (1, 1.1, 0.9), NS); S(0.09, (sx*0.2, -1.42, 0.5), (1, 0.8, 0.7), (0.55, 0.2, 0.18))
        To(0.3, 0.05, (sx*0.42, -0.78, 1.5), "ink", (R90, 0, 0)); Cy(0.29, 0.02, (sx*0.42, -0.77, 1.5), (0.85, 0.95, 1.0), (R90, 0, 0), verts=32)
        Cy(0.035, 0.85, (sx*0.76, -0.35, 1.5), "ink", (R90, 0, 0), verts=8)
    Cy(0.04, 0.26, (0, -0.78, 1.58), "ink", (0, R90, 0), verts=8)
    eyes(1.5, -0.785, 0.42, 0.13); smile(0.42, surf_y(0, 0.42, -0.5) - 0.015, 0.13)
    return finish(2.1, 2.6)
def b_football():
    G = E((0, 0, 0.78)); n = 32; R = lambda t: max(0.012, 0.72*math.sin(math.pi*t)**0.7); BR = (0.58, 0.28, 0.1)
    tube([(-1.25 + 2.5*k/n, 0, 0.78) for k in range(n + 1)], [R(k/n) for k in range(n + 1)], BR, seg=32, ref=(0, 0, 1), parent=G, mats=[BR, "white"], cfun=lambda i, j: 1 if i in (4, 5, 26, 27) else 0)
    sface(0.74, 0.2, 0.11, mouth_dz=0.26, mr=0.09, parent=G)
    L = E((0, 0, 0.78), G)
    for k in range(6): x = -0.35 + 0.14*k; BX((x, 0, 0.78 + R((x + 1.25)/2.5) + 0.01), (0.05, 0.3, 0.045), "white", L, bevel=0.012)
    BX((0, 0, 0.78 + 0.725), (0.82, 0.05, 0.04), "white", L, bevel=0.012)
    swing(L, (rad(58), 0, 0)); swing(G, (0, rad(-18), 0))
    return finish(1.8, 2.7, turn=-15)
def _restripe(o, body=0, stripe=3, paws=4):
    for p in o.data.polygons:
        c = p.center; n = p.normal; m = p.material_index
        if c.z < 0.26: p.material_index = paws; continue
        if m not in (body, stripe): continue
        if c.y > 0.85 and c.z > 1.0: k = ((c.z + 3.0)*4.2) % 1 < 0.45                      # tail rings
        elif c.z < 0.62: k = ((c.z + 3.0)*5.5) % 1 < 0.45 and abs(c.x) > 0.12              # leg bands
        elif c.y < -0.2: k = c.z > 1.62 and ((c.y + 3.0)*5.2) % 1 < 0.42                   # head top
        else: k = n.z > -0.25 and ((c.y + 3.0)*3.3) % 1 < 0.42                              # body
        p.material_index = stripe if k else body
def b_tiger():
    quad_meta("tig", "white", "white", "ink", ear="round", tail="long", stripes=True)
    o = [ob for ob in bpy.data.objects if ob.name.startswith("Body")][-1]; o.data.materials.append(mat("tig")); _restripe(o)
    S(0.06, (0, -1.41, 1.3), (1.3, 0.6, 0.8), "pink")
    for sx in (-1, 1): S(0.09, (sx*0.36, -0.68, 1.86), (1, 0.5, 1), "white")
    return finish(2.3, 2.9, turn=8)
def b_spider():
    P = "purple"; L = (0.2, 0.08, 0.32)
    S(0.66, (0, 0.5, 1.0), (1, 1.1, 0.95), P); S(0.47, (0, -0.42, 0.92), (1, 1, 0.95), (0.65, 0.35, 0.9))
    for (x, y, z, r) in [(0, 0.5, 1.6, 0.16), (-0.3, 0.75, 1.48, 0.12), (0.3, 0.75, 1.48, 0.12), (0, 1.0, 1.4, 0.1)]: S(r, (x, y, z), (1, 1, 0.4), "lavender")
    sface(1.03, 0.2, 0.17, mouth_dz=0.3, mr=0.1)
    for sx in (-1, 1):
        for i, ang in enumerate((-58, -22, 14, 50)):
            a = rad(ang); d = Vector((sx*math.cos(a), math.sin(a), 0)); r0 = Vector((sx*0.3, -0.12 + 0.12*i, 0.85)); up = Vector((0, 0, 1))
            pts = spline([r0, r0 + d*0.72 + up*0.9, r0 + d*1.3 + up*0.35, r0 + d*1.5 - up*0.8], 16)
            tube(pts, lerpr(0.09, 0.055, 16), L, seg=10); S(0.07, tuple(pts[-1]), (1, 1, 0.7), L)
    return finish(2.0, 3.0)
def b_swan():
    W = "white"
    S(0.6, (0, 0.25, 0.6), (0.85, 1.45, 0.8), W); S(0.3, (0, 1.2, 0.95), (0.55, 1.3, 0.45), W, rot=(rad(-38), 0, 0))
    for sx in (-1, 1):
        S(0.5, (sx*0.45, 0.35, 0.88), (0.26, 1.35, 0.78), W, rot=(rad(-16), 0, rad(sx*-9)))
        for k in range(3): S(0.2, (sx*(0.48 - 0.06*k), 0.85 + 0.2*k, 1.12 + 0.13*k), (0.3, 1.5, 0.6), W, rot=(rad(-28 - 9*k), 0, rad(sx*-9)))
    nk = spline([(0, -0.45, 0.72), (0, -1.0, 1.05), (0, -0.92, 1.6), (0, -0.5, 2.0), (0, -0.52, 2.38), (0, -0.82, 2.5)], 28)
    tube(nk, lerpr(0.23, 0.14, 28), W, seg=16, ref=(1, 0, 0)); S(0.21, (0, -0.86, 2.5), (0.95, 1.2, 0.95), W)
    Co(0.11, 0.42, (0, -1.24, 2.42), "orange", (rad(98), 0, 0)); S(0.08, (0, -1.06, 2.55), (1, 1, 1), "ink")
    eyes(2.56, -0.98, 0.14, 0.07)
    return finish(2.45, 3.0, turn=24)
def b_bull():
    quad_meta((0.37, 0.2, 0.11), (0.46, 0.27, 0.15), (0.9, 0.7, 0.55), (0.18, 0.1, 0.05), ear="floppy", tail="long", snout_len=0.1,
              extra_elems=[((0, -0.15, 1.42), 0.52, None), ((0, 0.25, 1.2), 0.45, None)])
    for sx in (-1, 1):
        tube(spline([(sx*0.3, -0.62, 1.74), (sx*0.78, -0.66, 1.8), (sx*1.06, -0.72, 2.08), (sx*1.02, -0.8, 2.45)], 14), lerpr(0.15, 0.03, 14), "ivory", seg=12)
    To(0.14, 0.035, (0, -1.44, 1.08), "gold", (R90, 0, 0)); S(0.2, (0.5, 1.3, 1.7), (1, 1, 1.2), (0.18, 0.1, 0.05))
    for k in range(3): S(0.13, (-0.14 + 0.14*k, -0.7, 1.86), (1, 1, 1.3), (0.18, 0.1, 0.05))
    return finish(2.35, 3.0, turn=8)
def b_eagle():
    Bn = "eaglb"; Bd = "eagld"; wings = []
    S(0.5, (0, 0.05, 1.0), (0.92, 0.85, 1.25), Bn); S(0.4, (0, -0.02, 1.58), (1, 0.9, 0.7), "white"); S(0.36, (0, -0.1, 1.88), (1, 1, 1), "white")
    tube(spline([(0, -0.38, 1.88), (0, -0.66, 1.87), (0, -0.82, 1.72), (0, -0.8, 1.56)], 12), [0.14, 0.14, 0.135, 0.13, 0.125, 0.12, 0.11, 0.1, 0.085, 0.07, 0.05, 0.03, 0.01], "yellow", seg=12, ref=(1, 0, 0))
    eyes(1.98, -0.4, 0.16, 0.085)
    for sx in (-1, 1): B((sx*0.16, -0.46, 2.08), (0.2, 0.05, 0.05), "white", rot=(0, rad(sx*18), 0))
    for k in range(5): S(0.16, (0.17*(k - 2), 0.32, 0.36), (0.6, 0.35, 1.5), "white", rot=(rad(-25), rad(-10*(k - 2)), 0))
    for sx in (-1, 1): S(0.2, (sx*0.2, 0.0, 0.45), (1, 1, 1.2), Bd)
    legs2("yellow", 0, 0.3, 0.06, 0.2, foot="yellow")
    for sx in (1, -1):
        Wg = E((sx*0.35, 0.1, 1.5)); G = E((sx*0.35, 0.1, 1.5), Wg)
        S(0.5, (sx*1.15, 0.12, 1.52), (1.75, 0.22, 0.6), Bn, G)
        for k in range(5): S(0.18, (sx*(0.55 + 0.27*k), 0.15, 1.2 - 0.02*k), (0.7, 0.25, 1.7), Bd if k % 2 else Bn, G)
        for k in range(5):
            a = rad(-68 + 27*k); S(0.13, (sx*(1.85 + 0.42*math.cos(a)), 0.14, 1.5 + 0.42*math.sin(a)), (2.7, 0.25, 0.75), Bd, G, rot=(0, -sx*a, 0))
        G.rotation_euler = (0, rad(-sx*20), 0); wings.append(Wg)
    return finish(2.3, 3.5, turn=-33, H={"wings": wings, "flap": 26})
def b_boot():
    Yc = "yellow"; Rc = "red"
    tube([(-0.3, 0, 0.3), (-0.3, 0, 1.2), (-0.3, 0, 2.1)], [0.42, 0.43, 0.48], Yc, seg=32, ref=(0, 1, 0), cap=False)
    To(0.48, 0.06, (-0.3, 0, 2.1), Rc); Cy(0.44, 0.02, (-0.3, 0, 2.06), (0.5, 0.36, 0.02), verts=32)
    S(0.46, (0.25, 0, 0.47), (1.75, 0.95, 0.86), Yc)
    RB((0.22, 0, 0.13), (1.8, 0.98, 0.26), Rc, lv=2); RB((-0.38, 0, 0.1), (0.62, 0.92, 0.2), Rc, lv=2)
    To(0.43, 0.035, (-0.3, 0, 0.78), Rc)
    S(0.07, (0.72, -0.3, 0.72), (2.2, 0.5, 0.8), "white", rot=(0, rad(18), rad(18)))
    sface(1.45, 0.17, 0.1, x=-0.3, mouth_dz=0.26, mr=0.09)
    return finish(2.35, 2.7, turn=-20)
def b_pencil():
    r = 0.36
    Co(r, 0.66, (0, 0, 0.33), (0.95, 0.75, 0.5), (math.pi, 0, 0), verts=6); Co(0.115, 0.21, (0, 0, 0.105), "ink", (math.pi, 0, 0), verts=12)
    flat(Cy(r, 1.34, (0, 0, 1.33), "yellow", verts=6))
    Cy(r*0.98, 0.26, (0, 0, 2.13), "silver", verts=24)
    for z in (2.06, 2.2): To(r*0.98, 0.02, (0, 0, z), "grey")
    RC(r*0.9, 0.36, (0, 0, 2.42), "pink", lv=2)
    face(1.5, -r*0.866, 0.13, 0.085, mouth_dz=0.24, mr=0.075)
    return finish(2.5, 2.6, turn=-20, roll=14)
# ================================================================ batch 3 / 4 (brighter, bigger)
def em(o, g): o.data.materials[0] = g; return o
def b_castle():
    St = "stonel"; Sd = "stoned"
    BX((0, 0.05, 0.08), (3.0, 2.4, 0.16), "grass", bevel=0.07)
    BX((0, 0.1, 0.85), (1.9, 1.2, 1.4), St, bevel=0.03)
    for k in range(5): BX((-0.72 + 0.36*k, -0.42, 1.66), (0.22, 0.22, 0.24), St, bevel=0.02)
    BX((0, 0.3, 1.8), (0.9, 0.75, 1.6), St, bevel=0.03)
    for k in range(3):
        for y in (-0.02, 0.62): BX((-0.3 + 0.3*k, y, 2.7), (0.2, 0.2, 0.22), St, bevel=0.02)
    Cy(0.03, 0.7, (0, 0.3, 3.0), "wood", verts=8); Fp([(0, 0), (0.5, 0.14), (0, 0.28)], (0.02, 0.3, 3.05), 0.04, "yellow")
    BX((0, -0.09, 2.15), (0.2, 0.04, 0.36), "navy", bevel=0.015)
    for sx in (-1, 1):
        Cy(0.4, 2.0, (sx*1.0, -0.4, 1.15), St, verts=24); Cy(0.45, 0.16, (sx*1.0, -0.4, 2.12), Sd, verts=24); Co(0.52, 0.85, (sx*1.0, -0.4, 2.62), "red")
        BX((sx*1.0, -0.79, 1.5), (0.14, 0.04, 0.32), "navy", bevel=0.015)
        Cy(0.36, 2.3, (sx*1.0, 0.75, 1.3), St, verts=24); Co(0.46, 0.8, (sx*1.0, 0.75, 2.85), "blue")
        S(0.06, (sx*1.0, -0.4, 3.07), (1, 1, 1), "gold")
    BX((0, -0.5, 0.5), (0.56, 0.06, 0.66), "wood", bevel=0.01); Cy(0.28, 0.06, (0, -0.5, 0.83), "wood", (R90, 0, 0))
    BX((0, -0.54, 0.6), (0.03, 0.02, 0.9), "dkbrown")
    eyes(1.3, -0.5, 0.3, 0.12)
    return finish(2.45, 3.0, turn=-18)
def b_computer():
    Wc = "white"; Sv = "silver"
    BX((0, 0.25, 1.5), (2.1, 0.12, 1.3), Wc, bevel=0.04); BX((0, 0.185, 1.53), (1.94, 0.02, 1.1), (0.3, 0.68, 1.0), bevel=0.0)
    BX((0, 0.34, 0.6), (0.24, 0.1, 0.66), Sv, bevel=0.03); BX((0, 0.3, 0.06), (1.0, 0.6, 0.1), Sv, bevel=0.04)
    for (x, z) in [(-0.72, 1.9), (-0.52, 1.9)]: S(0.06, (x, 0.17, z), (1, 0.3, 1), "yellow")
    BX((-0.15, -0.75, 0.07), (1.8, 0.66, 0.12), Wc, bevel=0.04)
    kc = ["lgrey"]*9 + ["red", "yellow", "green", "blue"]
    for i in range(10):
        for j in range(4):
            if j == 0 and 2 <= i <= 6: continue
            BX((-0.9 + 0.167*i, -0.98 + 0.15*j, 0.145), (0.13, 0.115, 0.04), kc[(i*7 + j*3) % 13], bevel=0.012)
    BX((-0.232, -0.98, 0.145), (0.8, 0.115, 0.04), "lgrey", bevel=0.012)
    S(0.16, (1.1, -0.75, 0.09), (0.8, 1.25, 0.6), Wc); Cy(0.02, 0.1, (1.1, -0.85, 0.17), "red", (R90, 0, 0), verts=8)
    face(1.68, 0.175, 0.42, 0.16, mouth_dz=0.42, mr=0.17)
    return finish(2.1, 2.9, turn=-25)
def b_telephone():
    Rd = "red"; Rk = (0.65, 0.03, 0.05)
    o = Fp([(-0.85, 0), (0.75, 0), (0.75, 0.7), (0.3, 0.98), (-0.15, 0.98), (-0.85, 0.32)], (0, 0, 0), 1.8, Rd, rot=(0, 0, R90))
    bm = o.modifiers.new("Bevel", "BEVEL"); bm.width = 0.07; bm.segments = 4
    nrm = Vector((0, -0.73, 0.68)).normalized(); upv = Vector((0, 0.68, 0.73)).normalized(); c = Vector((0, -0.5, 0.65)) + nrm*0.02; th = math.degrees(math.atan2(0.73, 0.68))
    Cy(0.36, 0.07, tuple(c + nrm*0.03), "white", (rad(th), 0, 0), verts=32); Cy(0.13, 0.09, tuple(c + nrm*0.04), Rd, (rad(th), 0, 0), verts=24)
    for k in range(9):
        a = rad(-60 + 33.75*k); p = c + nrm*0.07 + (Vector((1, 0, 0))*math.cos(a) + upv*math.sin(a))*0.25; S(0.05, tuple(p), (1, 1, 1), Rk, seg=12, ring=8)
    eyes(c.z, c.y - 0.02, 0.63, 0.12, fwd=tuple(nrm))
    for sx in (-1, 1): BX((sx*0.55, 0.08, 1.05), (0.34, 0.55, 0.3), Rd, bevel=0.06)
    pv = E((0, 0.08, 1.28))
    tube(spline([(-1.0, 0.08, 1.38), (-0.5, 0.08, 1.55), (0.5, 0.08, 1.55), (1.0, 0.08, 1.38)], 16), [0.15]*17, Rd, seg=16, parent=pv)
    for sx in (-1, 1): S(0.33, (sx*1.05, 0.08, 1.3), (1, 1.05, 0.8), Rd, pv); Cy(0.25, 0.08, (sx*1.05, 0.08, 1.07), Rk, parent=pv)
    n = 60; tube([(-1.15 - 0.09*math.cos(k*1.3) - 0.25*math.sin(math.pi*k/n), -0.2 + 0.09*math.sin(k*1.3) - 0.5*k/n, 1.05 - 0.95*k/n) for k in range(n + 1)], [0.035]*(n + 1), Rk, seg=8)
    return finish(1.95, 2.9, turn=-22, H={"pivot": pv})
def b_scissors():
    Hc = (1.0, 0.3, 0.05)
    for sg, y in ((1, 0.0), (-1, 0.07)):
        g = E((0, y, 1.15))
        Fp([(-0.12, -0.2), (0.12, -0.2), (0.13, 0.55), (0.02, 1.3), (-0.12, 0.95)] if sg > 0 else [(0.12, -0.2), (-0.12, -0.2), (-0.13, 0.55), (-0.02, 1.3), (0.12, 0.95)], (0, y, 1.15), 0.06, "silver", g)
        tube([(0, y, 1.0), (0, y, 0.72)], [(0.11, 0.05), (0.09, 0.05)], Hc, seg=12, ref=(1, 0, 0), parent=g)
        To(0.3, 0.09, (sg*0.14, y, 0.36), Hc, (R90, 0, 0), g, scale=(0.82, 1.3, 1))
        swing(g, (0, rad(sg*21), 0))
    Cy(0.075, 0.22, (0, 0.03, 1.15), "gold", (R90, 0, 0), verts=16)
    eyes(1.5, -0.045, 0.15, 0.1)
    return finish(2.5, 2.7, turn=-38)
def b_sandwich():
    Br = (0.92, 0.66, 0.32)
    RB((0, 0, 0.2), (2.0, 2.0, 0.34), Br, lv=2)
    for k in range(16): a = TAU*k/16; S(0.3, (1.0*math.cos(a), 1.0*math.sin(a), 0.44 + 0.04*(k % 2)), (1, 1, 0.3), "lime" if k % 2 else "green", rot=(0, 0, a))
    S(1.0, (0, 0, 0.42), (1, 1, 0.08), "green")
    for (x, y) in [(0.6, -0.62), (-0.55, -0.66), (0.72, 0.35), (-0.7, 0.4)]: Cy(0.42, 0.12, (x, y, 0.58), "red", verts=24); Cy(0.3, 0.125, (x, y, 0.58), (1.0, 0.35, 0.25), verts=24)
    BX((0, 0, 0.72), (2.05, 2.05, 0.07), "yellow", rot=(0, 0, rad(45)), bevel=0.02)
    for k in range(12): a = TAU*k/12; S(0.36, (0.82*math.cos(a), 0.82*math.sin(a), 0.86), (1, 1, 0.2), "pink")
    S(0.9, (0, 0, 0.86), (1, 1, 0.08), "pink")
    RB((0, 0, 1.15), (2.0, 2.0, 0.42), Br, lv=2); S(0.9, (0, 0, 1.28), (1, 1, 0.16), Br)
    Cy(0.03, 0.8, (0, 0, 1.75), "wood", verts=8); S(0.17, (0, 0, 2.05), (1, 1, 0.9), (0.5, 0.62, 0.12)); S(0.07, (0, -0.13, 2.07), (1, 0.6, 1), "red")
    sface(1.2, 0.24, 0.1, mouth_dz=0.2, mr=0.09)
    return finish(1.95, 2.9, turn=-8)
def b_volcano():
    g = mat("lava", 0.5, 1.6); n = 22; R = lambda t: 0.48 + 1.1*(1 - t)**1.7
    Cy(1.8, 0.12, (0, 0, 0.06), "grass", verts=40)
    o = tube([(0, 0, 0.1 + 1.85*k/n) for k in range(n + 1)], [R(k/n) for k in range(n + 1)], "rock", seg=32, cap=False)
    for v in o.data.vertices:
        th = math.atan2(v.co.y, v.co.x); f = 1 + 0.06*math.sin(5*th + 2.5*v.co.z) + 0.035*math.sin(9*th - 4*v.co.z); v.co.x *= f; v.co.y *= f
    To(0.5, 0.09, (0, 0, 1.95), "rockd"); em(S(0.5, (0, 0, 1.9), (1, 1, 0.3), "lava"), g)
    sface(0.72, 0.25, 0.12, mouth_dz=0.3, mr=0.11)
    for (a0, t1) in [(-35, 0.3), (-150, 0.4), (25, 0.5), (170, 0.35), (-95, 0.72)]:
        pts = []
        for k in range(13):
            t = 1.0 - (1.0 - t1)*k/12; a = rad(a0 + 9*math.sin(k*0.9)); rr = R(t)*1.04 + 0.03; pts.append((rr*math.cos(a), rr*math.sin(a), 0.1 + 1.85*t))
        a = rad(a0); em(tube(pts, [(0.14 - 0.004*k, 0.06) for k in range(13)], "lava", seg=10, ref=(-math.sin(a), math.cos(a), 0)), g); em(S(0.15, pts[-1], (1, 1, 1), "lava"), g)
    em(tube([(0, 0, 1.9), (0.03, 0, 2.3), (0.0, 0, 2.6)], [0.2, 0.14, 0.05], "lava", seg=12), g)
    for (x, y, z, r) in [(-0.35, 0, 2.45, 0.1), (0.4, 0.1, 2.35, 0.09), (0.2, -0.2, 2.75, 0.08), (-0.2, 0.2, 2.8, 0.07), (0.62, -0.1, 2.0, 0.07), (-0.6, 0.1, 2.1, 0.08)]: em(S(r, (x, y, z), (1, 1, 1.3), "lava"), g)
    return finish(2.3, 3.0, H={"glow": [g]})
def b_elf():
    G = "green"; Sk = "peach"
    RB((0, 0, 0.72), (0.98, 0.78, 0.78), G, lv=2); RB((0, 0, 0.42), (1.02, 0.8, 0.15), "red", lv=1); S(0.08, (0, -0.42, 0.42), (1, 0.5, 1), "gold")
    for k in range(6): a = TAU*k/6; Co(0.14, 0.26, (0.36*math.cos(a), 0.3*math.sin(a), 1.0), "red", (math.pi, 0, 0), verts=4)
    S(0.56, (0, 0, 1.52), (1, 1, 0.98), Sk)
    for sx in (-1, 1):
        RK(0.19, 0.8, (sx*0.78, 0.0, 1.68), Sk, (0, rad(sx*66), 0), lv=1); S(0.09, (sx*0.3, -0.48, 1.38), (1, 0.4, 0.7), "pink")
        RC(0.1, 0.52, (sx*0.56, -0.05, 0.75), G, (0, rad(sx*18), 0), lv=1); S(0.13, (sx*0.64, -0.08, 0.46), (1, 1, 1), Sk)
        S(0.17, (sx*0.24, -0.1, 0.1), (1, 1.7, 0.6), "red"); Co(0.09, 0.3, (sx*0.24, -0.42, 0.22), "red", (rad(40), 0, 0)); S(0.05, (sx*0.24, -0.5, 0.36), (1, 1, 1), "gold")
        Cy(0.1, 0.3, (sx*0.24, 0, 0.25), G)
    RC(0.6, 0.16, (0, 0, 1.92), "red", lv=1)
    tube(spline([(0, 0.02, 1.95), (0, 0.06, 2.45), (0.1, 0.12, 2.85), (0.38, 0.14, 3.0)], 14), lerpr(0.52, 0.05, 14), G, seg=20)
    S(0.15, (0.44, 0.14, 2.98), (1, 1, 1), "white")
    face(1.55, -0.53, 0.2, 0.115, mouth_dz=0.3, mr=0.1)
    return finish(2.5, 2.7)
def b_emu():
    Bn = (0.52, 0.34, 0.18); Bd = (0.36, 0.22, 0.1); Nk = (0.45, 0.62, 0.8); Lg = (0.45, 0.4, 0.35)
    S(0.75, (0, 0.2, 1.35), (0.95, 1.25, 0.88), Bn)
    for k in range(14):
        a = rad(-70 + 20*k); S(0.2, (0.62*math.sin(a), 0.35 + 0.72*math.cos(a)*0.9, 1.05 + 0.1*(k % 3)), (0.8, 0.8, 1.9), Bd if k % 2 else Bn, rot=(rad(25)*math.cos(a), 0, 0))
    for k in range(4): S(0.22, (0.15*(k - 1.5), 1.05, 1.15 - 0.05*abs(k - 1.5)), (0.8, 1.2, 1.8), Bd, rot=(rad(35), 0, 0))
    nk = spline([(0, -0.5, 1.55), (0, -0.85, 1.95), (0, -0.7, 2.45), (0, -0.78, 2.85)], 16); tube(nk, lerpr(0.24, 0.14, 16), Nk, seg=16, ref=(1, 0, 0))
    S(0.27, (0, -0.86, 2.95), (0.95, 1.2, 0.95), Bd); Co(0.13, 0.36, (0, -1.25, 2.9), (0.25, 0.22, 0.2), (R90, 0, 0), verts=12)
    for k in range(3): S(0.06, (0.06*(k - 1), -0.75, 3.22), (1, 1, 2.2), Bd)
    eyes(3.02, -1.07, 0.16, 0.085)
    for sx in (-1, 1):
        Cy(0.09, 0.85, (sx*0.26, 0.15, 0.45), Lg); S(0.2, (sx*0.26, 0.15, 0.8), (1, 1, 1.3), Bn)
        for da in (-28, 0, 28): tube([(sx*0.26, 0.15, 0.06), (sx*0.26 + 0.42*math.sin(rad(da)), 0.15 - 0.42*math.cos(rad(da)), 0.05)], [0.07, 0.045], Lg, seg=8)
    return finish(2.55, 2.8, turn=16)
def b_kangaroo():
    K = "kang"; C = "cream"; Kd = (0.68, 0.4, 0.18)
    S(0.56, (0, 0.2, 1.0), (0.9, 1.0, 1.3), K, rot=(rad(-16), 0, 0)); S(0.44, (0, -0.1, 0.98), (0.8, 0.8, 1.15), C, rot=(rad(-16), 0, 0))
    S(0.3, (0, -0.38, 0.72), (1.05, 0.7, 0.75), C); S(0.19, (0, -0.52, 0.98), (1, 1, 1), K)
    for sx in (-1, 1): S(0.06, (sx*0.1, -0.5, 1.22), (0.7, 0.4, 1.9), K); S(0.035, (sx*0.07, -0.69, 1.02), (1, 0.5, 1), "ink")
    S(0.03, (0, -0.72, 0.95), (1.2, 0.6, 0.8), "ink")
    tube([(0, -0.1, 1.5), (0, -0.3, 1.8)], [0.3, 0.24], K, seg=16, ref=(1, 0, 0))
    S(0.35, (0, -0.42, 2.0), (0.92, 1.1, 0.95), K); S(0.22, (0, -0.76, 1.92), (0.9, 1.25, 0.8), K); S(0.07, (0, -1.02, 1.97), (1.2, 0.8, 0.8), "ink")
    for sx in (-1, 1):
        S(0.14, (sx*0.2, -0.26, 2.5), (0.75, 0.45, 2.3), K, rot=(rad(-8), rad(sx*14), 0)); S(0.08, (sx*0.2, -0.31, 2.5), (0.7, 0.4, 2.2), "pink", rot=(rad(-8), rad(sx*14), 0))
        tube(spline([(sx*0.4, -0.2, 1.45), (sx*0.42, -0.55, 1.25), (sx*0.3, -0.72, 1.3)], 8), lerpr(0.1, 0.07, 8), K, seg=10); S(0.09, (sx*0.3, -0.74, 1.3), (1, 1, 1), Kd)
        S(0.4, (sx*0.42, 0.3, 0.55), (0.7, 1.25, 1.15), K, rot=(rad(-20), 0, 0)); S(0.2, (sx*0.44, -0.35, 0.13), (0.85, 3.2, 0.62), K)
    tube(spline([(0, 0.55, 0.7), (0, 1.15, 0.38), (0, 1.75, 0.2), (0, 2.3, 0.22)], 16), lerpr(0.33, 0.09, 16), K, seg=16, ref=(1, 0, 0))
    eyes(2.1, -0.72, 0.19, 0.095); smile(1.8, -0.93, 0.08)
    return finish(2.5, 3.0, turn=28)
def b_squirrel():
    Q = "squi"; C = "cream"; Qd = (0.7, 0.3, 0.06)
    S(0.52, (0, 0.1, 0.78), (0.95, 1.0, 1.25), Q); S(0.4, (0, -0.2, 0.75), (0.8, 0.7, 1.15), C)
    S(0.45, (0, -0.2, 1.72), (1.05, 1.0, 0.95), Q); S(0.24, (0, -0.56, 1.62), (1.3, 0.8, 0.8), C); S(0.065, (0, -0.76, 1.68), (1.2, 0.8, 0.8), "ink")
    for sx in (-1, 1):
        Co(0.15, 0.42, (sx*0.27, -0.12, 2.2), Q, (0, rad(sx*12), 0), verts=16); Co(0.08, 0.26, (sx*0.27, -0.2, 2.16), "pink", (0, rad(sx*12), 0), verts=12)
        tube(spline([(sx*0.42, -0.1, 1.2), (sx*0.42, -0.5, 1.05), (sx*0.16, -0.66, 1.08)], 8), lerpr(0.11, 0.08, 8), Q, seg=10)
        S(0.2, (sx*0.3, -0.42, 0.12), (0.9, 1.7, 0.6), Q); S(0.33, (sx*0.42, 0.1, 0.45), (0.7, 1.1, 1.1), Q)
        B((sx*0.04, -0.75, 1.5), (0.07, 0.03, 0.1), "white")
    S(0.2, (0, -0.72, 1.0), (1, 1, 1.2), "acorn"); S(0.22, (0, -0.72, 1.14), (1, 1, 0.6), "capb"); Cy(0.03, 0.12, (0, -0.72, 1.3), "capb", verts=8)
    tp = spline([(0, 0.5, 0.35), (0, 1.15, 0.7), (0, 1.35, 1.5), (0, 1.1, 2.3), (0, 0.6, 2.62), (0, 0.3, 2.35)], 28)
    tube(tp, [0.2 + 0.36*math.sin(math.pi*min(1.0, (k/28.0)*1.15))**0.6 if k < 26 else 0.2 for k in range(29)], Q, seg=20, ref=(1, 0, 0))
    for k in range(6, 27, 4): S(0.2, (0, tp[k].y + 0.3*(1 if k < 16 else 0.3), tp[k].z + (0.1 if k < 16 else 0.38)), (1.0, 1.0, 1.0), Qd)
    eyes(1.84, -0.6, 0.2, 0.105); smile(1.5, -0.74, 0.07, tongue=False)
    return finish(2.5, 3.0, turn=26)
def b_giraffe():
    Gy = "gir"; Sp = "girs"; C = "cream"
    S(0.56, (0, 0.3, 1.3), (0.85, 1.3, 0.85), Gy)
    for sx in (-1, 1):
        for y in (-0.22, 0.85): Cy(0.125, 1.0, (sx*0.28, y, 0.5), Gy); Cy(0.14, 0.16, (sx*0.28, y, 0.08), Sp)
    nk = spline([(0, -0.3, 1.45), (0, -0.62, 2.1), (0, -0.82, 2.8)], 14); tube(nk, lerpr(0.3, 0.2, 14), Gy, seg=16, ref=(1, 0, 0))
    S(0.31, (0, -0.95, 2.98), (0.9, 1.25, 0.92), Gy); S(0.24, (0, -1.28, 2.88), (1, 1.1, 0.85), C)
    for sx in (-1, 1):
        Cy(0.045, 0.3, (sx*0.13, -0.86, 3.32), Gy, verts=10); S(0.08, (sx*0.13, -0.86, 3.5), (1, 1, 1), Sp); S(0.13, (sx*0.36, -0.82, 3.1), (1.5, 0.5, 0.75), Gy, rot=(0, rad(sx*-20), 0))
        S(0.03, (sx*0.08, -1.5, 2.92), (1, 0.6, 1.2), Sp)
    for k in range(2, 13): p = nk[k]; S(0.09, (0, p.y + 0.22 + 0.1*(1 - k/14.0), p.z + 0.06), (0.6, 1, 1.4), Sp)
    for i, k in enumerate(range(2, 14, 2)):
        p = nk[k]; r = 0.3 - 0.1*k/14.0
        for sx in (-1, 1): S(0.11, (sx*r*0.86, p.y + (0.06 if i % 2 else -0.08), p.z), (0.5, 1, 1), Sp)
        S(0.1, (0.0, p.y - r*0.83, p.z - 0.1), (1, 0.5, 1), Sp)
    for (th, ph) in [(0, 60), (0, 100), (50, 75), (-50, 80), (100, 60), (-100, 65), (140, 90), (-140, 95), (180, 60), (90, 105), (-90, 100), (30, 30), (-150, 35), (130, 30), (-30, 125), (20, 140)]:
        t = rad(th); f = rad(ph); S(0.15, (0.56*0.85*0.9*math.sin(f)*math.sin(t), 0.3 - 0.56*1.3*0.9*math.sin(f)*math.cos(t), 1.3 + 0.56*0.85*0.9*math.cos(f)), (1, 1, 1), Sp)
    tube(spline([(0, 0.98, 1.4), (0, 1.22, 1.1), (0, 1.26, 0.75)], 8), [0.05]*9, Gy, seg=8); S(0.1, (0, 1.26, 0.68), (1, 1, 1.5), Sp)
    eyes(3.1, -1.22, 0.17, 0.095); smile(2.78, -1.5, 0.07, tongue=False)
    return finish(2.65, 2.8, turn=18)
def b_mountain():
    BX((0, 0, 0.07), (3.9, 2.6, 0.14), "grass", bevel=0.07)
    flat(Co(1.5, 2.6, (0.1, 0.2, 1.4), "mtn", verts=9)); flat(Co(1.0, 1.7, (-1.1, 0.35, 0.95), "mtnd", verts=7)); flat(Co(0.85, 1.3, (1.25, 0.3, 0.75), "mtnd", verts=7))
    flat(Co(0.6, 1.04, (0.1, 0.2, 2.2), "white", verts=9))
    for k in range(9): a = TAU*(k + 0.5)/9; flat(Co(0.2, 0.45, (0.1 + 0.52*math.cos(a), 0.2 + 0.52*math.sin(a), 1.6 - 0.1*(k % 2)), "white", (math.pi, 0, 0), verts=4))
    flat(Co(0.36, 0.6, (-1.1, 0.35, 1.52), "white", verts=7)); flat(Co(0.3, 0.46, (1.25, 0.3, 1.19), "white", verts=7))
    for (x, y, s) in [(-1.55, -0.75, 1.0), (-1.1, -0.95, 0.8), (1.5, -0.8, 0.95), (1.05, -1.0, 0.75)]:
        Cy(0.06*s, 0.2*s, (x, y, 0.14 + 0.1*s), "brown", verts=8); Co(0.26*s, 0.5*s, (x, y, 0.14 + 0.42*s), "dkgreen", verts=10); Co(0.19*s, 0.4*s, (x, y, 0.14 + 0.7*s), "green", verts=10)
    sface(0.95, 0.27, 0.14, x=0.1, mouth_dz=0.33, mr=0.12)
    return finish(2.6, 3.3)
# ================================================================ batch 5
def checker(o, fn):
    """two-material pattern on a primitive: fn(center) -> 0/1 (slot 1 must already be appended)"""
    for p in o.data.polygons: p.material_index = fn(p.center)
    return o
def b_crab():
    R = "red"; claws = []
    S(0.85, (0, 0, 0.75), (1.3, 0.95, 0.62), R); S(0.7, (0, -0.1, 0.62), (1.25, 0.9, 0.5), (1.0, 0.55, 0.4))
    for sx in (-1, 1): Cy(0.07, 0.5, (sx*0.32, -0.42, 1.4), R); S(0.18, (sx*0.32, -0.4, 1.74), (1, 1, 1), R)
    eyes(1.74, -0.5, 0.32, 0.19); smile(0.78, -0.8, 0.2, tongue=False)
    for sx in (-1, 1):
        for k in range(3):
            y = -0.1 + 0.32*k; tube(spline([(sx*0.9, y, 0.62), (sx*1.42, y + 0.03, 0.78), (sx*1.62, y + 0.08, 0.02)], 10), lerpr(0.15, 0.07, 10), R, seg=10)
        c = E((sx*0.95, -0.35, 0.9))
        tube(spline([(sx*0.95, -0.35, 0.9), (sx*1.5, -0.5, 1.25), (sx*1.32, -0.55, 1.8)], 10), lerpr(0.16, 0.14, 10), R, seg=12, parent=c)
        S(0.38, (sx*1.3, -0.55, 2.02), (0.95, 0.6, 1.1), R, c)
        tube(spline([(sx*1.44, -0.55, 2.15), (sx*1.54, -0.55, 2.55), (sx*1.3, -0.55, 2.9)], 10), [0.21, 0.21, 0.2, 0.19, 0.18, 0.16, 0.14, 0.12, 0.09, 0.06, 0.03], R, seg=12, parent=c)
        tube(spline([(sx*1.1, -0.55, 2.2), (sx*0.98, -0.55, 2.5), (sx*1.1, -0.55, 2.74)], 8), [0.16, 0.15, 0.14, 0.13, 0.11, 0.09, 0.07, 0.05, 0.03], R, seg=12, parent=c); claws.append(c)
    return finish(2.3, 3.1, turn=-25, H={"claws": claws, "sway": 4, "yawaxis": 1})
def b_ham():
    Pk = (1.0, 0.55, 0.6); Gl = (0.85, 0.42, 0.2); n = 30; z0 = 0.9
    Rf = lambda x: 0.72 + 0.14*math.sin(math.pi*min(1.0, (x + 1.0)/1.3)) if x < 0.3 else 0.72 - 0.52*((x - 0.3)/0.9)**0.8
    xs = [-1.0 + 2.2*k/n for k in range(n + 1)]
    tube([(x, 0, z0) for x in xs], [Rf(x) for x in xs], Pk, seg=32, ref=(0, 0, 1), mats=[Pk, Gl], cfun=lambda i, j: 1 if math.cos(TAU*(j + 0.5)/32) > -0.2 else 0)
    Cy(0.725, 0.03, (-1.0, 0, z0), "cream", (0, R90, 0), verts=32); Cy(0.62, 0.04, (-1.0, 0, z0), (1.0, 0.62, 0.66), (0, R90, 0), verts=32); Cy(0.12, 0.06, (-1.0, 0, z0), "white", (0, R90, 0), verts=16)
    Cy(0.12, 0.75, (1.5, 0, z0), "white", (0, R90, 0), verts=16)
    for dy in (-0.11, 0.11): S(0.17, (1.9, dy, z0), (1, 1, 1), "white")
    sp = lambda x, a: (x, -(Rf(x) + 0.012)*math.sin(a), z0 + (Rf(x) + 0.012)*math.cos(a))
    d = rad(36); c = rad(55)
    for s in (-1, 1):
        for m in range(-6, 12):
            seg = []
            for k in range(41):
                x = -0.95 + 1.9*k/40; a = m*d + s*c*x
                if -rad(62) < a < rad(100): seg.append(sp(x, a))
                elif len(seg) > 1: tube(seg, [0.022]*len(seg), "dkbrown", seg=6); seg = []
                else: seg = []
            if len(seg) > 1: tube(seg, [0.022]*len(seg), "dkbrown", seg=6)
    for m in range(-6, 12):
        for q in range(-6, 12):
            a = (m + q)*d/2; x = (m - q)*d/(2*c)
            if -0.9 < x < 0.85 and -rad(55) < a < rad(95): S(0.055, sp(x, a), (1, 1, 1), "dkbrown", seg=10, ring=8)
    sface(0.62, 0.2, 0.11, x=-0.25, mouth_dz=0.24, mr=0.09)
    return finish(1.9, 2.9, turn=-18, roll=-14)
def b_jam():
    J = (0.85, 0.06, 0.12); Gs = (0.82, 0.93, 1.0); zs = [0.0, 0.04, 0.12, 0.25, 0.4, 0.55, 0.7, 0.85, 1.0, 1.15, 1.3, 1.42, 1.5, 1.58, 1.66, 1.74, 1.8]
    rr = [0.5, 0.62, 0.69, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.71, 0.66, 0.57, 0.52, 0.52]
    def cf(i, j):
        if 3 <= i <= 6 and 11 <= j <= 20: return 1
        return 2 if i >= 11 else 0
    tube([(0, 0, z) for z in zs], rr, J, seg=32, mats=[J, "white", Gs], cfun=cf)
    S(0.06, (-0.5, -0.52, 1.1), (0.6, 0.6, 3.2), "white", rot=(0, 0, rad(-44)))
    S(0.17, (0, -0.74, 0.6), (1.0, 0.45, 1.2), "red", rot=(math.pi, 0, 0));
    for sx in (-1, 0, 1): S(0.07, (sx*0.09, -0.76, 0.78), (1.3, 0.4, 0.7), "green", rot=(0, rad(sx*35), 0))
    for (x, z) in [(-0.06, 0.62), (0.06, 0.6), (0.0, 0.52), (-0.05, 0.7), (0.07, 0.69)]: S(0.018, (x, -0.815, z), (1, 1, 1), "yellow", seg=8, ring=6)
    sface(1.22, 0.2, 0.11, mouth_dz=0.22, mr=0.09)
    Bl = "blue"; ck = lambda c: (int((math.atan2(c.y, c.x) + math.pi)/TAU*16) + int(c.z*9)) % 2
    o = S(0.56, (0, 0, 1.86), (1, 1, 0.5), "white", seg=32, ring=16); o.data.materials.append(mat(Bl)); checker(o, ck)
    o = tube([(0, 0, 1.9), (0, 0, 1.78), (0, 0, 1.66), (0, 0, 1.54), (0, 0, 1.44)], [0.56, 0.535, 0.62, 0.74, 0.84], "white", seg=32, mats=["white", Bl], cfun=lambda i, j: (i + j//2) % 2, cap=False)
    for v in o.data.vertices:
        if v.co.z < 1.75: th = math.atan2(v.co.y, v.co.x); f = 1 + 0.1*math.sin(9*th)*(1.75 - v.co.z)/0.3; v.co.x *= f; v.co.y *= f
    To(0.54, 0.035, (0, 0, 1.77), "straw")
    for sx in (-1, 1): To(0.1, 0.03, (sx*0.11, -0.57, 1.76), "straw", (R90, 0, rad(sx*20)), scale=(1.2, 0.8, 1)); tube([(0, -0.56, 1.76), (sx*0.1, -0.62, 1.55)], [0.03, 0.03], "straw", seg=6)
    return finish(2.2, 2.6)
def b_pony():
    Bn = (0.62, 0.36, 0.17); Gd = (1.0, 0.8, 0.3); Mz = (0.9, 0.7, 0.5)
    body = E((0, 0, 0)); head = E((0, -0.45, 1.25), body); tail = E((0, 0.95, 1.25), body)
    S(0.62, (0, 0.1, 1.05), (0.92, 1.4, 0.9), Bn, body)
    lg = legs4(Bn, 0, 0.55, 0.15, 0.3, 0.55, parent=body, foot="dkbrown")
    tube([(0, -0.45, 1.2), (0, -0.88, 1.8)], [0.34, 0.27], Bn, seg=16, ref=(1, 0, 0), parent=head)
    S(0.37, (0, -0.98, 1.95), (0.92, 1.2, 1.0), Bn, head); S(0.27, (0, -1.34, 1.8), (0.95, 1.1, 0.85), Mz, head)
    for sx in (-1, 1):
        Co(0.11, 0.3, (sx*0.2, -0.85, 2.35), Bn, (0, rad(sx*12), 0), head, verts=12); S(0.03, (sx*0.09, -1.6, 1.84), (1, 0.6, 1.3), "dkbrown", head)
    for k in range(9):
        t = k/8.0; S(0.24 - 0.03*abs(k - 3)/3, (0.06*math.sin(k*2.1), -1.12 + 0.95*t, 2.32 - 0.1*t - 0.75*t*t), (1.15, 1, 1), Gd, head, name="Mane")
    for k in range(3): S(0.17, (0.1*(k - 1), -1.22, 2.2 - 0.03*abs(k - 1)), (1, 1, 1.2), Gd, head, name="Mane")
    for k in range(6): t = k/5.0; S(0.2 + 0.06*math.sin(math.pi*t), (0.04*math.sin(k*2), 1.0 + 0.3*math.sin(math.pi*t*0.7), 1.25 - 0.85*t), (1, 1, 1.15), Gd, tail, name="Tail")
    eyes(2.02, -1.26, 0.2, 0.1, parent=head); smile(1.68, -1.6, 0.07, parent=head, tongue=False)
    return finish(2.35, 2.9, turn=18, H={"body": body, "legs": lg, "head": head, "tail": tail, "legamp": 30})
def b_lemon():
    Y = (1.0, 0.86, 0.05); n = 28; g = E((0, 0, 0.72))
    tube([(-1.05 + 2.1*k/n, 0, 0.72) for k in range(n + 1)], [0.07 + 0.6*math.sin(math.pi*k/n)**0.6 for k in range(n + 1)], Y, seg=32, ref=(0, 0, 1), parent=g)
    for sx in (-1, 1): S(0.09, (sx*1.06, 0, 0.72), (1.2, 1, 1), Y, g)
    S(0.2, (-1.2, 0.05, 0.92), (1.6, 0.6, 0.25), "green", g, rot=(0, rad(35), 0)); Cy(0.03, 0.14, (-1.12, 0, 0.78), "brown", (0, rad(60), 0), g, verts=8)
    sface(0.78, 0.2, 0.11, mouth_dz=0.26, mr=0.09, parent=g); swing(g, (0, rad(-13), 0))
    h = E((0.75, -1.0, 0.5)); c = Vector((0.75, -1.0, 0.5)); m = 12
    tube([(c.x, c.y + 0.6*k/m, c.z) for k in range(m + 1)], [0.52*math.sqrt(max(0.0, 1 - (k/m)**2)) + 0.07*(1 - k/m)**0 * (1 if k < m else 0) + (0.05 if k == m else 0) for k in range(m + 1)], Y, seg=32, ref=(1, 0, 0), parent=h)
    Cy(0.56, 0.03, (c.x, c.y, c.z), "white", (R90, 0, 0), h, verts=32); Cy(0.48, 0.04, (c.x, c.y, c.z), (1.0, 0.95, 0.45), (R90, 0, 0), h, verts=32)
    for k in range(4): B((c.x, c.y - 0.022, c.z), (0.94, 0.012, 0.035), "white", h, (0, rad(45*k), 0))
    S(0.06, (c.x, c.y - 0.02, c.z), (1, 0.3, 1), "white", h)
    swing(h, (rad(-28), 0, rad(22)))
    return finish(1.8, 2.9, turn=-18)
def b_toad():
    T = (0.52, 0.47, 0.2); Td = (0.36, 0.31, 0.1); C = (0.95, 0.88, 0.6)
    S(0.85, (0, 0.2, 0.78), (1.15, 1.2, 0.88), T); S(0.72, (0, -0.42, 1.05), (1.2, 1.0, 0.75), T); S(0.66, (0, -0.4, 0.62), (1.15, 1.0, 0.72), C)
    for sx in (-1, 1):
        S(0.27, (sx*0.44, -0.6, 1.52), (1, 1, 0.95), T); S(0.03, (sx*0.12, -1.1, 1.22), (1, 0.6, 1), Td)
        tube([(sx*0.62, -0.6, 0.6), (sx*0.74, -0.95, 0.12)], [0.19, 0.15], T, seg=12); S(0.2, (sx*0.76, -1.05, 0.08), (1.25, 1.3, 0.4), T)
        S(0.48, (sx*0.9, 0.35, 0.45), (0.8, 1.35, 0.92), T); S(0.26, (sx*1.02, -0.3, 0.09), (0.95, 1.9, 0.38), T)
    eyes(1.57, -0.8, 0.44, 0.17)
    tube(spline([(-0.82, -0.6, 1.08), (-0.45, -0.98, 0.93), (0, -1.11, 0.88), (0.45, -0.98, 0.93), (0.82, -0.6, 1.08)], 20), [0.04]*21, "mouth", seg=8)
    import random; random.seed(7)
    for k in range(34):
        th = random.uniform(0, TAU); ph = random.uniform(0.15, 1.35); r = random.uniform(0.07, 0.13)
        if k % 3: p = (0.85*1.15*math.sin(ph)*math.cos(th), 0.2 + 0.85*1.2*math.sin(ph)*math.sin(th), 0.78 + 0.85*0.88*math.cos(ph))
        else: p = (0.72*1.2*math.sin(ph)*math.cos(th), -0.42 + 0.72*math.sin(ph)*math.sin(th)*(0.5 if math.sin(th) < 0 else 1), 1.05 + 0.72*0.75*math.cos(ph))
        if abs(p[0]) < 0.75 and p[1] < -0.3 and p[2] > 1.3: continue
        S(r, p, (1, 1, 0.75), Td, seg=12, ring=8)
    return finish(1.9, 3.0, turn=6)
def b_candy():
    Rc = "hotpink"; g = E((0, 0, 0.85))
    o = S(0.62, (0, 0, 0.85), (1.2, 1, 1), "white", g, seg=40, ring=24); o.data.materials.append(mat(Rc))
    checker(o, lambda c: int((c.x*1.3 + math.atan2(c.z, c.y)/TAU*2 + 10)*2) % 2)
    for sx in (-1, 1):
        n = 12; o = tube([(sx*(0.6 + 0.9*k/n), 0, 0.85) for k in range(n + 1)], [(0.3 - 0.17*math.sin(math.pi*min(1.0, k/3.0)/1.0)*(1 if k < 3 else 1) + 0.52*max(0.0, (k - 2)/10.0)**0.8, 0.26 - 0.13*min(1.0, k/3.0) + 0.14*max(0.0, (k - 2)/10.0)) for k in range(n + 1)],
                        "white", seg=24, ref=(0, 0, 1), parent=g, mats=["white", Rc], cfun=lambda i, j: (j//2) % 2, cap=False)
        for v in o.data.vertices:
            w = max(0.0, (abs(v.co.x) - 1.0)/0.5)
            if w > 0: a = math.atan2(v.co.z - 0.85, v.co.y); f = 1 + 0.12*w*math.sin(8*a); v.co.y *= f; v.co.z = 0.85 + (v.co.z - 0.85)*f
        To(0.14, 0.035, (sx*0.82, 0, 0.85), "gold", (0, R90, 0), g)
    sface(0.9, 0.2, 0.11, mouth_dz=0.26, mr=0.09, parent=g); swing(g, (0, rad(-16), 0))
    return finish(1.7, 2.9, turn=-15)
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}
