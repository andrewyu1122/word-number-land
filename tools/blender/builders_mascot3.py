# Mascot action verbs for Read mode: run jump swim eat look play go sit read kick catch hug (24 f loops, same model).
exec(open(PIPE + "/builders_mascot2.py", encoding="utf-8").read().rsplit(chr(10) + "BUILD = {k[2:]", 1)[0])
IDLE_L = (0, rad(22), 0); IDLE_R = (0, rad(-22), 0); HIDE = (0.001, 0.001, 0.001)
def crv(f, pts):
    if f <= pts[0][0]: return pts[0][1]
    for (f0, v0), (f1, v1) in zip(pts, pts[1:]):
        if f <= f1:
            u = (f - f0) / (f1 - f0); u = (1 - math.cos(math.pi * u)) / 2
            if isinstance(v0, tuple): return tuple(a + (b - a) * u for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * u
    return pts[-1][1]
def D(*a): return tuple(rad(x) for x in a)
def setk(o, prop, v, f): setattr(o, prop, v); kf(o, prop, f)
def anim(o, prop, pts):
    for f in range(1, NFRAMES + 2): setk(o, prop, crv(f, pts), f)
def flutter(h, amp=22, cyc=4):
    for i, w in enumerate(h["wings"]): sine(w, "rotation_euler", 1, rad(amp) * (1 if i == 0 else -1), cyc)
def show(p, pts=None):
    """props are 'hidden' by scale; pts = [(frame, scale)]"""
    anim(p, "scale", [(f, (v, v, v)) for f, v in (pts or [(1, 1.0), (25, 1.0)])])
_b_mascot2 = b_mascot
def b_mascot():
    h = _b_mascot2(); legs = []
    for sx in (-1, 1):                                  # leg pivots at the hips (legs were static before)
        p = E((sx*0.25, 0, 0.45), name="LegPiv"); legs.append(p)
        for o in [o for o in ROOT.children if o.type == 'MESH' and abs(o.location.x - sx*0.25) < 0.02 and o.location.z < 0.35 and abs(o.location.y) < 0.06]: par(o, p)
    h["legs"] = legs
    P = {}
    e = E((0, 0, 0), name="Apple"); S(0.24, (0, 0, 0), (1, 1, 0.92), "red", e); Cy(0.025, 0.14, (0, 0, 0.26), "dkbrown", parent=e); S(0.09, (0.09, 0, 0.3), (1.4, 0.5, 0.5), "green", e); P["apple"] = e
    e.location = (0.5, -0.2, 0.6); par(e, h["arms"][1])                 # the apple lives in the right hand
    e = E((0, 0, 0), name="Ball"); S(0.27, (0, 0, 0), (1, 1, 1), "red", e); S(0.272, (0, 0, 0), (1, 1, 0.3), "yellow", e); S(0.274, (0, 0, 0), (0.3, 1, 1), "blue", e); P["ball"] = e
    e = E((0, 0, 0), name="Soccer"); S(0.28, (0, 0, 0), (1, 1, 1), "white", e, seg=32, ring=16)
    for d in [Vector((0, 0, 1)), Vector((0, 0, -1))] + [Vector((math.cos(k*TAU/5), math.sin(k*TAU/5), 0.45)).normalized() for k in range(5)] + [Vector((math.cos(k*TAU/5 + 0.63), math.sin(k*TAU/5 + 0.63), -0.45)).normalized() for k in range(5)]:
        Co(0.1, 0.03, tuple(d*0.272), "black", tuple(d.to_track_quat('Z', 'Y').to_euler()), e, r2=0.09, verts=5)
    P["soccer"] = e
    e = E((0, 0, 0), name="Book")                       # open book, spine along x
    for sx, c in ((-1, "blue"), (1, "blue")):
        q = E((0, 0, 0), e, name="Cover"); B((sx*0.27, 0, 0.0), (0.52, 0.04, 0.7), c, q, bevel=0.02); B((sx*0.26, -0.03, 0.0), (0.46, 0.03, 0.62), "white", q)
        for k in range(4): B((sx*0.26, -0.047, -0.2 + 0.13*k), (0.34, 0.005, 0.03), "lgrey", q)
        q.rotation_euler = (0, 0, rad(sx*-18))
    pg = E((0, -0.05, 0), e, name="Page"); B((0.24, 0, 0), (0.46, 0.012, 0.62), "cream", pg); P["book"] = e; P["page"] = pg
    e = E((0, 0, 0), name="Heart")
    for sx in (-1, 1): S(0.26, (sx*0.2, 0, 0.14), (1, 0.6, 1), "red", e)
    Co(0.44, 0.5, (0, 0, -0.16), "red", (math.pi, 0, 0), e, verts=24).scale = (1, 0.6, 1); S(0.07, (-0.24, -0.15, 0.24), (1, 0.5, 1.4), "white", e); P["heart"] = e
    e = E((0, 0.05, 0), name="Stool"); B((0, 0.05, 0.3), (0.8, 0.7, 0.08), "wood", e, bevel=0.03)
    for sx in (-1, 1):
        for sy in (-1, 1): B((sx*0.3, 0.05 + sy*0.25, 0.14), (0.09, 0.09, 0.28), "brown", e, bevel=0.02)
    P["stool"] = e
    for k in ("apple", "ball", "soccer", "book", "heart", "stool"): P[k].scale = HIDE
    h["props"] = P; return h
def body(f, z=0.0, rx=0.0, ry=0.0, rz=0.0, sq=1.0):
    setk(ROOT, "location", (0, 0, z), f); setk(ROOT, "rotation_euler", (rx, ry, rz), f); setk(ROOT, "scale", (2 - sq if sq < 1 else 1/ sq**0.5, 2 - sq if sq < 1 else 1/sq**0.5, sq), f)
def act_run(h):
    l, r = h["arms"]; ll, lr = h["legs"]
    for f in range(1, NFRAMES + 2):
        t = (f - 1)/NFRAMES; w = TAU*3*t
        body(f, z=0.09*(1 - math.cos(2*w))/2, rx=rad(9) + rad(2)*math.sin(2*w), rz=rad(5)*math.sin(w))
        setk(ll, "rotation_euler", (rad(48)*math.sin(w), 0, 0), f); setk(lr, "rotation_euler", (rad(-48)*math.sin(w), 0, 0), f)
        setk(l, "rotation_euler", (rad(-60)*math.sin(w) - rad(15), rad(18), 0), f); setk(r, "rotation_euler", (rad(60)*math.sin(w) - rad(15), rad(-18), 0), f)
    flutter(h, 26, 6)
def act_jump(h):
    l, r = h["arms"]; ll, lr = h["legs"]
    Z = [(1, 0), (6, 0), (12, 0.72), (18, 0), (25, 0)]; SQ = [(1, 1), (5, 0.86), (7, 1.12), (12, 1.02), (17, 1.08), (19, 0.85), (22, 1.04), (25, 1)]
    for f in range(1, NFRAMES + 2): body(f, z=crv(f, Z), sq=crv(f, SQ))
    anim(l, "rotation_euler", [(1, IDLE_L), (5, D(20, 35, 0)), (11, D(0, 155, 0)), (17, D(0, 120, 0)), (21, D(0, 40, 0)), (25, IDLE_L)])
    anim(r, "rotation_euler", [(1, IDLE_R), (5, D(20, -35, 0)), (11, D(0, -155, 0)), (17, D(0, -120, 0)), (21, D(0, -40, 0)), (25, IDLE_R)])
    for lg, sx in ((ll, -1), (lr, 1)): anim(lg, "rotation_euler", [(1, D(0, 0, 0)), (6, D(0, 0, 0)), (12, D(-25, sx*12, 0)), (18, D(0, 0, 0)), (25, D(0, 0, 0))])
    flutter(h, 30, 6)
def act_swim(h):
    l, r = h["arms"]; ll, lr = h["legs"]
    for f in range(1, NFRAMES + 2):
        t = (f - 1)/NFRAMES; w = TAU*2*t
        body(f, z=0.22 + 0.05*math.sin(w), rx=rad(38) + rad(4)*math.sin(w + 1), rz=rad(7)*math.sin(w))
        setk(l, "rotation_euler", (-w - rad(40), rad(12), 0), f); setk(r, "rotation_euler", (-w - rad(40) - math.pi, rad(-12), 0), f)
        setk(ll, "rotation_euler", (rad(28)*math.sin(2*w) + rad(25), 0, 0), f); setk(lr, "rotation_euler", (rad(-28)*math.sin(2*w) + rad(25), 0, 0), f)
    flutter(h, 16, 4)
def act_eat(h):
    l, r = h["arms"]; ap = h["props"]["apple"]
    show(ap)
    UP_ = D(-72, 0, -48); MID = D(-55, 0, -30)
    anim(r, "rotation_euler", [(1, D(-25, -10, 0)), (5, UP_), (7, UP_), (9, MID), (12, UP_), (14, UP_), (17, D(-45, 0, -20)), (25, D(-25, -10, 0))])
    anim(l, "rotation_euler", [(1, IDLE_L), (25, IDLE_L)])
    SQ = [(1, 1), (5, 1), (6, 0.95), (7, 1.03), (12, 1), (13, 0.95), (14, 1.03), (16, 1), (17.5, 0.95), (19, 1.03), (20.5, 0.95), (22, 1.03), (23.5, 0.97), (25, 1)]
    for f in range(1, NFRAMES + 2): body(f, rx=rad(-4)*crv(f, [(1, 0), (5, 1), (14, 1), (17, 0), (25, 0)]), sq=crv(f, SQ))
    flutter(h, 14, 4)
def act_look(h):
    l, r = h["arms"]
    anim(l, "rotation_euler", [(1, IDLE_L), (4, D(-128, 58, 0)), (21, D(-128, 58, 0)), (25, IDLE_L)]); anim(r, "rotation_euler", [(1, IDLE_R), (5, D(15, -40, 0)), (21, D(15, -40, 0)), (25, IDLE_R)])
    RZ = [(1, 0), (4, 0), (8, 34), (11, 34), (16, -34), (19, -34), (25, 0)]
    for f in range(1, NFRAMES + 2): body(f, rz=rad(crv(f, RZ)), rx=rad(5)*crv(f, [(1, 0), (5, 1), (20, 1), (25, 0)]))
    flutter(h, 14, 4)
def act_play(h):
    l, r = h["arms"]; b = h["props"]["ball"]; show(b)
    LO = (0, -0.62, 0.72); HI = (0, -0.6, 1.05)
    anim(b, "location", [(1, LO), (4, (0, -0.62, 0.66)), (7, HI), (13, (0, -0.55, 2.2)), (19, HI), (21, (0, -0.62, 0.64)), (25, LO)])
    anim(b, "rotation_euler", [(1, D(0, 0, 0)), (7, D(0, 0, 0)), (19, D(360, 0, 120)), (25, D(360, 0, 120))])
    for a, sx in ((l, 1), (r, -1)):
        anim(a, "rotation_euler", [(1, D(-62, sx*38, 0)), (4, D(-52, sx*38, 0)), (7, D(-125, sx*40, 0)), (11, D(-150, sx*25, 0)), (17, D(-140, sx*30, 0)), (19, D(-125, sx*40, 0)), (21, D(-50, sx*38, 0)), (25, D(-62, sx*38, 0))])
    for f in range(1, NFRAMES + 2): body(f, sq=crv(f, [(1, 1), (4, 0.93), (7, 1.06), (12, 1), (19, 1), (21, 0.93), (25, 1)]), rx=rad(-6)*crv(f, [(1, 0), (7, 0), (12, 1), (17, 1), (21, 0), (25, 0)]))
    flutter(h, 18, 4)
def act_go(h):
    l, r = h["arms"]; ll, lr = h["legs"]
    for f in range(1, NFRAMES + 2):
        t = (f - 1)/NFRAMES; w = TAU*2*t
        body(f, z=0.05*(1 - math.cos(2*w))/2, ry=rad(4)*math.sin(w))
        setk(ll, "rotation_euler", (rad(30)*math.sin(w), 0, 0), f); setk(lr, "rotation_euler", (rad(-30)*math.sin(w), 0, 0), f)
        setk(l, "rotation_euler", (rad(-32)*math.sin(w), rad(18), 0), f); setk(r, "rotation_euler", (0, rad(-150) + rad(30)*math.sin(2*w), 0), f)
    flutter(h, 20, 4)
def act_sit(h):
    l, r = h["arms"]; ll, lr = h["legs"]; st = h["props"]["stool"]
    par(st, None) if False else None
    show(st, [(1, 0.001), (2, 0.001), (5, 1), (21, 1), (24, 0.001), (25, 0.001)])
    DN = [(1, 0), (6, 1), (20, 1), (25, 0)]
    for f in range(1, NFRAMES + 2):
        d = crv(f, DN); t = (f - 1)/NFRAMES; sw = math.sin(TAU*3*t)*(1 if 6 <= f <= 20 else 0)
        body(f, z=-0.1*d, rx=rad(-5)*d, sq=crv(f, [(1, 1), (6, 0.93), (8, 1), (25, 1)]))
        setk(ll, "rotation_euler", (rad(-62)*d + rad(20)*sw*d, 0, 0), f); setk(lr, "rotation_euler", (rad(-62)*d - rad(20)*sw*d, 0, 0), f)
        setk(l, "rotation_euler", (rad(25)*d, rad(22) + rad(10)*d, 0), f); setk(r, "rotation_euler", (rad(25)*d, rad(-22) - rad(10)*d, 0), f)
    flutter(h, 12, 4)
def act_read(h):
    l, r = h["arms"]; bk = h["props"]["book"]; pg = h["props"]["page"]; show(bk)
    bk.rotation_euler = D(-25, 0, 0)
    anim(bk, "location", [(1, (0, -0.62, 0.78)), (5, (0, -0.64, 0.98)), (21, (0, -0.64, 0.98)), (25, (0, -0.62, 0.78))])
    anim(pg, "rotation_euler", [(1, D(0, 0, -16)), (11, D(0, 0, -16)), (16, D(0, 0, -164)), (17, D(0, 0, -16)), (25, D(0, 0, -16))])
    for a, sx in ((l, 1), (r, -1)):
        anim(a, "rotation_euler", [(1, D(-58, sx*30, 0)), (5, D(-84, sx*30, 0)), (21, D(-84, sx*30, 0)), (25, D(-58, sx*30, 0))])
    anim(r, "rotation_euler", [(1, D(-58, -30, 0)), (5, D(-84, -30, 0)), (11, D(-84, -30, 0)), (13.5, D(-100, -8, 0)), (16, D(-84, -30, 0)), (21, D(-84, -30, 0)), (25, D(-58, -30, 0))])
    for f in range(1, NFRAMES + 2):
        t = (f - 1)/NFRAMES; body(f, rx=rad(7)*crv(f, [(1, 0), (5, 1), (21, 1), (25, 0)]), rz=rad(5)*math.sin(TAU*t)*crv(f, [(1, 0), (5, 1), (21, 1), (25, 0)]))
    flutter(h, 12, 4)
def act_kick(h):
    l, r = h["arms"]; ll, lr = h["legs"]; b = h["props"]["soccer"]; show(b)
    P0 = (0.32, -0.42, 0.28)
    anim(b, "location", [(1, P0), (7, P0), (10, (0.65, -0.5, 0.75)), (13, (0.9, -0.45, 0.5)), (15, (1.0, -0.4, 0.28)), (17, (0.97, -0.4, 0.28)), (23, P0), (25, P0)])
    anim(b, "rotation_euler", [(1, D(0, 0, 0)), (7, D(0, 0, 0)), (15, D(0, 400, 0)), (23, D(0, 0, 0)), (25, D(0, 0, 0))])
    anim(lr, "rotation_euler", [(1, D(0, 0, 0)), (5, D(42, 0, 0)), (7.5, D(-72, 0, 0)), (11, D(-40, 0, 0)), (16, D(0, 0, 0)), (25, D(0, 0, 0))])
    anim(l, "rotation_euler", [(1, IDLE_L), (5, D(-40, 30, 0)), (8, D(35, 60, 0)), (16, IDLE_L), (25, IDLE_L)]); anim(r, "rotation_euler", [(1, IDLE_R), (5, D(30, -40, 0)), (8, D(-30, -70, 0)), (16, IDLE_R), (25, IDLE_R)])
    for f in range(1, NFRAMES + 2): body(f, rx=rad(crv(f, [(1, 0), (5, 6), (8, -9), (14, 0), (25, 0)])), ry=rad(crv(f, [(1, 0), (5, -5), (8, -8), (14, 0), (25, 0)])), z=crv(f, [(1, 0), (7, 0), (9, 0.06), (12, 0), (25, 0)]))
    flutter(h, 22, 4)
def act_catch(h):
    l, r = h["arms"]; b = h["props"]["ball"]
    show(b, [(1, 0.001), (2, 0.001), (4, 1), (20, 1), (23, 0.001), (25, 0.001)])
    HOLD = (0, -0.62, 1.02)
    anim(b, "location", [(1, (0.9, -0.5, 1.75)), (3, (0.9, -0.5, 1.75)), (9, HOLD), (11, (0, -0.6, 0.9)), (14, HOLD), (17, HOLD), (22, (0.9, -0.5, 1.75)), (25, (0.9, -0.5, 1.75))])
    anim(b, "rotation_euler", [(1, D(0, 0, 0)), (9, D(0, -300, 0)), (17, D(0, -300, 0)), (25, D(0, 0, 0))])
    for a, sx in ((l, 1), (r, -1)):
        anim(a, "rotation_euler", [(1, IDLE_L if sx == 1 else IDLE_R), (6, D(-135, sx*5, 0)), (9, D(-118, sx*40, 0)), (11, D(-100, sx*40, 0)), (14, D(-118, sx*40, 0)), (17, D(-125, sx*40, 0)), (20, D(-150, sx*10, 0)), (25, IDLE_L if sx == 1 else IDLE_R)])
    for f in range(1, NFRAMES + 2): body(f, sq=crv(f, [(1, 1), (9, 1), (11, 0.92), (14, 1.05), (17, 1), (25, 1)]), ry=rad(crv(f, [(1, 0), (5, 8), (10, 0), (18, 0), (21, 6), (25, 0)])))
    flutter(h, 20, 4)
def act_hug(h):
    l, r = h["arms"]; ht = h["props"]["heart"]
    show(ht, [(1, 0.001), (3, 0.001), (8, 1.15), (10, 1.0), (13, 0.9), (16, 1.0), (19, 1.0), (23, 0.001), (25, 0.001)])
    anim(ht, "location", [(1, (0, -0.72, 0.9)), (25, (0, -0.72, 0.9))])
    for a, sx in ((l, 1), (r, -1)):
        anim(a, "rotation_euler", [(1, IDLE_L if sx == 1 else IDLE_R), (6, D(-20, sx*95, 0)), (9, D(-20, sx*95, 0)), (12, D(-78, sx*46, 0)), (19, D(-78, sx*46, 0)), (22, D(-30, sx*60, 0)), (25, IDLE_L if sx == 1 else IDLE_R)])
    for f in range(1, NFRAMES + 2):
        t = (f - 1)/NFRAMES; k = crv(f, [(1, 0), (11, 0), (13, 1), (19, 1), (21, 0), (25, 0)])
        body(f, ry=rad(9)*math.sin(TAU*2*t)*k, sq=1 - 0.05*k)
    flutter(h, 24, 6)
ACTS.update(run=act_run, jump=act_jump, swim=act_swim, eat=act_eat, look=act_look, play=act_play, go=act_go, sit=act_sit, read=act_read, kick=act_kick, catch=act_catch, hug=act_hug)
NEW_ACTIONS = ["run", "jump", "swim", "eat", "look", "play", "go", "sit", "read", "kick", "catch", "hug"]
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}
