# Task 4: mascot with a breathing idle loop (48 f = 2 s, one blink), two-arm wave with body sway, bigger think
_SP = PIPE + "/"
exec(open(_SP + "builders_misc.py", encoding="utf-8").read().split("BUILD = {k[2:]")[0])
def act_idle(h):
    n = NFRAMES
    for f in range(1, n+2):
        t = (f-1)/n; s = 1+0.035*math.sin(TAU*2*t); ROOT.scale = (1+0.012*math.sin(TAU*2*t), 1+0.012*math.sin(TAU*2*t), s); kf(ROOT, "scale", f)
    sine(ROOT, "location", 2, 0.03, 2, phase=-math.pi/2)
    l, r = h["arms"]; sine(l, "rotation_euler", 1, rad(6), 2, base=rad(22)); sine(r, "rotation_euler", 1, rad(-6), 2, base=rad(-22))
    for i, w in enumerate(h["wings"]): sine(w, "rotation_euler", 1, rad(14)*(1 if i == 0 else -1), 4)
    star = h.get("star")
    if star is not None:
        for f in range(1, n+2):
            t = (f-1)/n; k = 1+0.25*max(0.0, math.sin(TAU*2*t))**3; star.scale = (k, k, k); kf(star, "scale", f)
        m = star.data.materials[0]; inp = m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
        for f in range(1, n+2): inp.default_value = 0.6+1.6*max(0.0, math.sin(TAU*2*(f-1)/n))**3; inp.keyframe_insert("default_value", frame=f)
    # blink: pupils+eyes squash flat around frame 0.62*n for 3 frames
    bf = int(0.62*n)
    for e in EYES:
        for f, sz in ((bf-2, 1.0), (bf, 0.08), (bf+2, 1.0)):
            e.scale = (e.scale[0], e.scale[1], e.scale[2]*sz if f == bf else e.scale[2]); kf(e, "scale", f)
    for lid in [o for o in bpy.data.objects if o.name.startswith("BlinkLid")]:
        for f, v in ((bf-2, True), (bf-1, False), (bf+1, False), (bf+2, True)): lid.hide_render = v; lid.keyframe_insert("hide_render", frame=f)
def act_wave(h):
    l, r = h["arms"]
    sine(r, "rotation_euler", 1, rad(38), 3, base=rad(-150)); sine(l, "rotation_euler", 1, rad(-34), 3, base=rad(150), phase=math.pi)
    sine(ROOT, "rotation_euler", 1, rad(9), 1.5 if False else 1, phase=0); sine(ROOT, "rotation_euler", 1, rad(5), 3, phase=0.5)
    for f in range(1, NFRAMES+2):
        t = (f-1)/NFRAMES; s = 1+0.05*math.sin(TAU*3*t); ROOT.scale = (s, s, 2-s); kf(ROOT, "scale", f)
    for i, w in enumerate(h["wings"]): sine(w, "rotation_euler", 1, rad(26)*(1 if i == 0 else -1), 4)
def act_think(h):
    l, r = h["arms"]
    keys(ROOT, "rotation_euler", [(1, (0, 0, 0)), (8, (rad(-7), rad(20), 0)), (16, (rad(-7), rad(20), 0)), (24, (0, 0, 0))])
    keys(l, "rotation_euler", [(1, (0, rad(30), 0)), (8, (rad(-100), rad(40), 0)), (16, (rad(-100), rad(40), 0)), (24, (0, rad(30), 0))])
    keys(r, "rotation_euler", [(1, (0, rad(-30), 0)), (12, (0, rad(-45), 0)), (24, (0, rad(-30), 0))])
    for i, w in enumerate(h["wings"]): sine(w, "rotation_euler", 1, rad(22)*(1 if i == 0 else -1), 4)
def act_hop(h):   # mascot-only: lower jump so the shared crop box stays tight (mascot renders bigger)
    n = NFRAMES; K = [(1,0,(1,1,1)),(4,0,(1.14,1.14,0.74)),(6,0.25,(0.9,0.9,1.24)),(12,0.72,(1,1,1.02)),(17,0.3,(0.93,0.93,1.12)),(19,0,(1.25,1.25,0.7)),(22,0,(0.96,0.96,1.06)),(24,0,(1,1,1))]
    for f, z, s in K: ROOT.location = (0, 0, z); ROOT.scale = s; kf(ROOT, "location", f); kf(ROOT, "scale", f)
def act_happy(h):
    act_hop(h); l, r = h["arms"]
    keys(l, "rotation_euler", [(1, (0, rad(35), 0)), (6, (0, rad(60), 0)), (12, (0, rad(140), 0)), (19, (0, rad(40), 0)), (24, (0, rad(35), 0))])
    sine(r, "rotation_euler", 1, rad(32), 3, base=rad(-150))
    for i, w in enumerate(h["wings"]): sine(w, "rotation_euler", 1, rad(28)*(1 if i == 0 else -1), 4)
ACTS.update(idle=act_idle, wave=act_wave, think=act_think, happy=act_happy, hop=act_hop)
_prev_b_mascot = b_mascot
def b_mascot():
    h = _prev_b_mascot()
    star = next((o for o in bpy.data.objects if o.type == 'MESH' and abs(o.location.z-1.9) < 0.01 and abs(o.location.x) < 0.01), None)
    if star is not None:
        m = mat("gold", 0.4, 0.6); star.data.materials[0] = m; h["star"] = star
    # eyelids used only by the blink (hidden otherwise)
    for (p, parent, r) in LIDS: o = B(tuple(p), (r*1.7, 0.03, 0.05), "ink", parent, name="BlinkLid"); o.hide_render = True
    return h
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}
