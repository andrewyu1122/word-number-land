# Sea collection: 16 sea creatures (idle / swim / happy) in the dino style. Face -Y.
exec(open(PIPE + "/builders_dino.py", encoding="utf-8").read().rsplit(chr(10) + "BUILD = {k[2:]", 1)[0])
PAL.update(dict(seagrey=(0.55,0.62,0.72), dkblue=(0.15,0.35,0.7), pearl=(0.9,0.95,1.0), jelly=(1.0,0.6,0.8), lobster=(0.85,0.2,0.12)))
def RC(r, d, loc, c, rot=(0,0,0), parent=None, lv=2):
    o = Cy(r*1.12, d*1.08, loc, c, rot, parent, 12); m = o.modifiers.new("Sub", "SUBSURF"); m.levels = lv; m.render_levels = lv; smooth(o); return o
def fin(loc, size, c, parent=None, rot=None, name="Fin"):
    o = S(size, loc, (1, 0.25, 0.6), c, parent, rot=rot, name=name); return o
def tailfin(piv_loc, c, L=0.5, up=0.5, horizontal=False):
    p = E(piv_loc, name="TailPiv")
    x, y, z = piv_loc
    if horizontal:
        for sx in (-1, 1): S(L*0.5, (x+sx*L*0.5, y+L*0.5, z), (1.0, 0.6, 0.18), c, p, rot=(0, 0, rad(sx*25)), name="Fluke")
    else:
        for sz in (-1, 1): S(L*0.5, (x, y+L*0.5, z+sz*up*0.45), (0.18, 0.7, 1.0), c, p, rot=(rad(sz*-30), 0, 0), name="Fluke")
    return p
def surf_y(x, z, fallback):
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    hit, loc, nrm, idx, ob, mw = scene.ray_cast(dg, Vector((x, -8.0, z)), Vector((0, 1, 0)))
    return loc.y if hit else fallback
def fish_eyes(z, y, spread=0.2, r=0.13, parent=None):
    f = Vector((0, -1, 0))
    for sx in (-1, 1):
        yy = surf_y(sx*spread, z, y) + r*0.45; p = Vector((sx*spread, yy, z))
        EYES.extend([S(r, p, (1, 0.5, 1), "white", parent, name="Eye"), S(r*0.55, p+f*(r*0.6), (1, 0.5, 1), "black", parent, name="Pupil", seg=16, ring=10),
                     S(r*0.18, p+f*(r*0.95)+Vector((-r*0.25, 0, r*0.35)), (1, 1, 1), "white", parent, name="Shine", seg=10, ring=6)])
        LIDS.append((p+f*(r*0.4), parent, r))
_smile0 = smile
def smile(z, y, r=0.14, parent=None, x=0.0, tongue=True, rot=None):
    yy = surf_y(x, z, y) - 0.015
    _smile0(z, yy, r, parent, x, tongue, rot)
def sea_swim(h):
    sine(ROOT, "location", 2, 0.08, 1); sine(ROOT, "rotation_euler", 1, rad(3), 1, phase=math.pi/2)
    if "tail" in h: sine(h["tail"], "rotation_euler", h.get("tailaxis", 2), rad(h.get("tailamp", 25)), 2)
    for i, f in enumerate(h.get("fins", [])): sine(f, "rotation_euler", 1, rad(h.get("finamp", 25))*(-1 if i % 2 == 0 else 1), 2, phase=math.pi/2)
    for i, w in enumerate(h.get("wings", [])): sine(w, "rotation_euler", 1, rad(h.get("flap", 30))*(-1 if i % 2 == 0 else 1), 1)
    for i, t in enumerate(h.get("tentacles", [])): sine(t, "rotation_euler", 0, rad(14), 1, phase=i*0.8)
    for i, l in enumerate(h.get("legs", [])): sine(l, "rotation_euler", 0, rad(20), 2, phase=math.pi*(i % 2))
    for i, c in enumerate(h.get("claws", [])): sine(c, "rotation_euler", 2, rad(15), 2, phase=math.pi*i)
    if h.get("wiggle"): sine(ROOT, "rotation_euler", 1, rad(10), 2)
def sea_happy(h):
    if "spout" in h:
        sp = h["spout"]; keys(sp, "scale", [(1,(0.01,0.01,0.01)),(5,(0.01,0.01,0.01)),(9,(1.1,1.1,1.0)),(14,(1,1,1.2)),(19,(0.8,0.8,0.5)),(22,(0.01,0.01,0.01)),(24,(0.01,0.01,0.01))])
        keys(ROOT, "location", [(1,(0,0,0)),(5,(0,0,0.3)),(9,(0,0,0)),(14,(0,0,0.15)),(19,(0,0,0)),(24,(0,0,0))])
        keys(ROOT, "rotation_euler", [(1,(0,0,0)),(5,(rad(-10),0,0)),(9,(rad(4),0,0)),(14,(0,0,0)),(24,(0,0,0))])
        if "tail" in h: sine(h["tail"], "rotation_euler", h.get("tailaxis", 2), rad(h.get("tailamp", 25)), 3)
        return
    zc = h.get("zc", 1.0)                      # barrel roll about the body centre (0,0,zc), with a hop
    for f in range(1, NFRAMES+2):
        t = min(1.0, max(0.0, (f-4)/14.0)); th = TAU*t; hop = 0.6*math.sin(math.pi*t) if 0 < t < 1 else 0.0
        ROOT.rotation_euler = (0, th, 0); ROOT.location = (-zc*math.sin(th), 0, zc - zc*math.cos(th) + hop)
        kf(ROOT, "rotation_euler", f); kf(ROOT, "location", f)
    keys(ROOT, "scale", [(1,(1,1,1)),(4,(1.1,1.1,0.9)),(8,(0.95,0.95,1.08)),(18,(1,1,1)),(20,(1.06,1.06,0.94)),(24,(1,1,1))])
    for i, f in enumerate(h.get("fins", [])): sine(f, "rotation_euler", 1, rad(35)*(-1 if i % 2 == 0 else 1), 3)
    for i, w in enumerate(h.get("wings", [])): sine(w, "rotation_euler", 1, rad(40)*(-1 if i % 2 == 0 else 1), 2)
    if "tail" in h: sine(h["tail"], "rotation_euler", h.get("tailaxis", 2), rad(30), 3)
ACTS["swim"] = sea_swim; ACTS["happy"] = sea_happy
def fish_body(c, belly, elems, bz, extra_mats=(), region=None, chest=False):
    return body_blob(c, belly, elems, extra_mats=extra_mats, extra_region=region, bz=bz, chest=chest)
# ------------------------------------------------------------------ creatures
def b_clownfish():
    def stripes(cc, n):
        if abs(cc.y+0.45) < 0.1 or abs(cc.y+0.0) < 0.1 or abs(cc.y-0.5) < 0.08: return 2
        return 0
    fish_body("orange", "orange", [((0, 0, 1.0), 0.55, (0.8, 1.4, 1.0)), ((0, -0.6, 1.0), 0.3, None)], 1.0, extra_mats=["white"], region=stripes)
    t = tailfin((0, 0.7, 1.0), "orange", 0.5, 0.5); fin((0, -0.1, 1.62), 0.3, "orange", rot=(0, 0, 0), name="Dorsal")
    fins = []
    for sx in (-1, 1): p = E((sx*0.35, -0.2, 0.9), name="FinPiv"); fin((sx*0.55, -0.2, 0.85), 0.22, "orange", p, rot=(0, rad(sx*60), 0)); fins.append(p)
    fish_eyes(1.15, -0.78, 0.2, 0.13); smile(0.78, -0.92, 0.1, tongue=False); return {"tail": t, "fins": fins}
def b_seahorse():
    EL = chain((0, 0.1, 0.5), (0, -0.1, 1.5), 0.26, 0.3, 6) + chain((0, -0.1, 1.5), (0, -0.35, 2.0), 0.28, 0.24, 4) + [((0, -0.6, 2.05), 0.22, None), ((0, -0.95, 1.95), 0.12, (1, 1.4, 0.8))]
    EL += [((0.15, 0.3, 0.3), 0.18, None), ((0.3, 0.45, 0.2), 0.14, None), ((0.3, 0.3, 0.1), 0.12, None), ((0.15, 0.15, 0.1), 0.1, None)]
    fish_body("yellow", "cream", EL, 1.0)
    for k in range(6): S(0.08, (0, 0.2-0.02*k, 0.6+0.2*k), (0.6, 1, 1.5), "orange", name="Spine")
    t = E((0, 0.2, 1.1), name="FinPiv"); fin((0, 0.42, 1.1), 0.3, "orange", t, rot=(0, R90, 0), name="DorsalFin")
    fish_eyes(2.15, -0.72, 0.17, 0.11); smile(1.86, -1.05, 0.05, tongue=False); return {"fins": [t], "finamp": 30, "wiggle": True}
def b_jellyfish():
    o = S(0.8, (0, 0, 1.6), (1, 1, 0.75), "jelly"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2; o.data.materials[0] = mat("jelly", 0.3)
    S(0.75, (0, 0, 1.45), (1, 1, 0.25), "pink"); tent = []
    for k in range(8):
        a = k*TAU/8; p = E((0.5*math.cos(a), 0.5*math.sin(a), 1.35), name="TentPiv"); tent.append(p)
        for j in range(5): S(0.09-0.01*j, (0.5*math.cos(a)+0.06*j*math.cos(a), 0.5*math.sin(a)+0.06*j*math.sin(a), 1.2-0.26*j), (1, 1, 1.6), "hotpink" if k % 2 else "pink", p, name="Tent")
    for k in range(5): S(0.1, (0.3*math.cos(k*1.3), 0.3*math.sin(k*1.3), 1.9+0.1*math.cos(k)), (1, 1, 0.6), "white", name="Dot")
    fish_eyes(1.65, -0.62, 0.22, 0.13); smile(1.3, -0.72, 0.12, tongue=False); return {"tentacles": tent, "wiggle": False}
def b_starfish():
    EL = [((0, 0, 1.0), 0.4, (1, 0.6, 1))]
    for k in range(5):
        a = R90 + k*TAU/5; EL += chain((0.3*math.cos(a), 0, 1.0+0.3*math.sin(a)), (0.95*math.cos(a), 0, 1.0+0.95*math.sin(a)), 0.3, 0.16, 4)
    def region(cc, n): return 0
    metachar(EL, [], ["orange", "coral"], region, res=0.06)
    for k in range(5):
        a = R90 + k*TAU/5
        for j in range(3): S(0.06, (0.35*math.cos(a)*(1+j*0.6), -0.32, 1.0+0.35*math.sin(a)*(1+j*0.6)), (1, 0.6, 1), "coral", name="Bump")
    fish_eyes(1.08, -0.4, 0.17, 0.11); smile(0.78, -0.42, 0.1, tongue=False); return {"wiggle": True}
def b_turtle():
    o = S(0.8, (0, 0.1, 0.75), (1.0, 1.15, 0.6), "green"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2
    for k in range(7): a = k*0.9; S(0.2, (0.42*math.cos(a)*(1-0.3*(k % 2)), 0.1+0.5*math.sin(a)*(1-0.3*(k % 2)), 1.1+0.1*(k % 2)), (1, 1, 0.45), "dkgreen", name="Scute")
    S(0.72, (0, 0.1, 0.55), (1.05, 1.2, 0.4), "lime"); hp, jp = head_unit((0, -0.95, 0.85), "lime", r=0.3, snout=(0.28, 0.2), hs=(0.95, 1.0, 0.85), jaw=True)
    fins = []
    for (x, y) in [(-0.75, -0.3), (0.75, -0.3), (-0.65, 0.6), (0.65, 0.6)]:
        sx = -1 if x < 0 else 1; p = E((x*0.8, y, 0.55), name="FinPiv"); fins.append(p)
        f = S(0.32, (x+sx*0.3, y-0.1, 0.5), (1.3, 0.55, 0.2), "lime", p, name="Flipper"); f.rotation_euler = (0, 0, rad(sx*-20 if y < 0 else sx*20))
    S(0.12, (0, 0.95, 0.55), (0.8, 1, 0.6), "lime", name="Tail")
    return {"head": hp, "jaw": jp, "fins": fins, "finamp": 22}
def b_octopus():
    o = S(0.7, (0, 0, 1.5), (1, 1, 1.15), "purple"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2
    S(0.55, (0, -0.1, 1.1), (1.1, 1.0, 0.7), "purple"); tent = []
    for k in range(8):
        a = k*TAU/8 + 0.2; p = E((0.4*math.cos(a), 0.4*math.sin(a), 0.9), name="TentPiv"); tent.append(p)
        for j in range(6): S(0.15-0.015*j, (0.4*math.cos(a)*(1+0.5*j)+0.02*j*j*math.cos(a), 0.4*math.sin(a)*(1+0.5*j), max(0.1, 0.8-0.14*j)), (1, 1, 0.9), "purple", p, name="Tent")
        for j in range(3): S(0.045, (0.4*math.cos(a)*(1.6+0.5*j), 0.4*math.sin(a)*(1.6+0.5*j)-0.1, max(0.12, 0.55-0.14*j)), (1, 1, 0.6), "pink", p, name="Sucker")
    for k in range(5): S(0.08, (0.35*math.cos(k*1.3), 0.35*math.sin(k*1.3)-0.1, 1.9+0.15*math.cos(k*2)), (1, 1, 0.6), "lavender", name="Spot")
    fish_eyes(1.55, -0.6, 0.26, 0.15); smile(1.15, -0.66, 0.1, tongue=False)
    for sx in (-1, 1): S(0.08, (sx*0.45, -0.58, 1.3), (1, 0.4, 0.7), "pink", name="Cheek")
    return {"tentacles": tent}
def b_crab():
    o = S(0.75, (0, 0, 0.7), (1.35, 0.95, 0.6), "red"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2; claws = []; legs = []
    for sx in (-1, 1):
        RC(0.05, 0.5, (sx*0.35, -0.45, 1.2), "red", (0, rad(sx*10), 0), lv=1)
        p = E((sx*0.85, -0.3, 0.7), name="ClawPiv"); claws.append(p)
        RC(0.11, 0.6, (sx*1.1, -0.55, 0.8), "red", (0, rad(-sx*55), 0), p, lv=1); S(0.32, (sx*1.4, -0.85, 0.95), (1.0, 1.2, 0.8), "red", p, name="Claw"); S(0.18, (sx*1.4, -1.15, 1.1), (1, 1.2, 0.6), "red", p, name="ClawTip")
        for k in range(3):
            lp = E((sx*0.8, 0.1+k*0.25, 0.5), name="LegPiv"); legs.append(lp)
            RC(0.07, 0.75, (sx*1.05, 0.1+k*0.25, 0.4), "red", (0, rad(-sx*60), 0), lp, lv=1); S(0.08, (sx*1.35, 0.1+k*0.25, 0.1), (1, 1, 0.6), "red", lp, name="Foot")
    eyes(1.45, -0.45, 0.35, 0.15); smile(0.65, -0.8, 0.2, tongue=False); return {"claws": claws, "legs": legs, "wiggle": True}
def b_dolphin():
    EL = [((0, 0.0, 1.1), 0.5, (0.75, 1.6, 0.85)), ((0, -0.7, 1.1), 0.32, None), ((0, -1.05, 1.0), 0.17, (1, 1.5, 0.8))] + chain((0, 0.6, 1.1), (0, 1.4, 1.2), 0.3, 0.15, 5)
    fish_body("seagrey", "white", EL, 1.1)
    t = tailfin((0, 1.45, 1.2), "seagrey", 0.5, 0.5, horizontal=True); fin((0, 0.0, 1.65), 0.3, "seagrey", rot=(rad(-25), 0, 0), name="Dorsal")
    fins = []
    for sx in (-1, 1): p = E((sx*0.3, -0.3, 0.85), name="FinPiv"); fin((sx*0.55, -0.3, 0.75), 0.25, "seagrey", p, rot=(0, rad(sx*55), 0)); fins.append(p)
    fish_eyes(1.3, -0.78, 0.2, 0.12); smile(0.9, -1.2, 0.08, tongue=False); return {"tail": t, "tailaxis": 0, "tailamp": 20, "fins": fins}
def b_whale():
    EL = [((0, 0.1, 1.1), 0.7, (0.9, 1.5, 0.9)), ((0, -0.8, 1.05), 0.45, (1, 1, 0.85))] + chain((0, 0.9, 1.1), (0, 1.7, 1.25), 0.4, 0.18, 5)
    fish_body("blue", "white", EL, 1.1)
    t = tailfin((0, 1.75, 1.25), "blue", 0.6, 0.6, horizontal=True)
    fins = []
    for sx in (-1, 1): p = E((sx*0.4, -0.4, 0.8), name="FinPiv"); fin((sx*0.75, -0.4, 0.7), 0.3, "blue", p, rot=(0, rad(sx*55), 0)); fins.append(p)
    sp = E((0, -0.3, 1.85), name="SpoutPiv"); Cy(0.08, 0.9, (0, -0.3, 2.3), "pearl", (0, 0, 0), sp, name="Spout")
    for k in range(5): S(0.16, (0.25*math.cos(k*1.25), -0.3+0.25*math.sin(k*1.25), 2.75), (1, 1, 0.7), "pearl", sp, name="SpoutTop")
    sp.scale = (0.01, 0.01, 0.01)
    fish_eyes(1.3, -1.05, 0.3, 0.13); smile(0.85, -1.25, 0.2, tongue=False); return {"tail": t, "tailaxis": 0, "tailamp": 15, "fins": fins, "spout": sp}
def b_shark():
    EL = [((0, 0.0, 1.1), 0.55, (0.8, 1.7, 0.95)), ((0, -0.85, 1.05), 0.3, (1, 1.2, 0.8))] + chain((0, 0.7, 1.1), (0, 1.5, 1.2), 0.3, 0.16, 5)
    fish_body("seagrey", "white", EL, 1.1)
    t = tailfin((0, 1.55, 1.2), "seagrey", 0.55, 0.7); fin((0, -0.05, 1.75), 0.38, "seagrey", rot=(rad(-30), 0, 0), name="Dorsal")
    fins = []
    for sx in (-1, 1): p = E((sx*0.3, -0.35, 0.8), name="FinPiv"); fin((sx*0.6, -0.35, 0.7), 0.28, "seagrey", p, rot=(0, rad(sx*60), 0)); fins.append(p)
    for k in range(5): Co(0.035, 0.1, (-0.2+0.1*k, -1.12, 0.78), "white", (0, 0, 0), verts=6, name="Tooth")
    S(0.3, (0, -1.08, 0.82), (1.1, 0.4, 0.25), "mouth", name="MouthLine")
    fish_eyes(1.3, -0.95, 0.24, 0.12); return {"tail": t, "tailamp": 25, "fins": fins}
def b_pufferfish():
    o = S(0.75, (0, 0, 1.1), (1, 1, 0.95), "yellow"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2
    S(0.6, (0, -0.1, 0.9), (1.05, 1.0, 0.75), "cream")
    for k in range(22):
        a = k*2.4; b = 0.5+ (k % 5)*0.45; p = (0.72*math.cos(a)*math.sin(b), 0.72*math.sin(a)*math.sin(b), 1.1+0.72*math.cos(b))
        if p[1] < -0.35 and abs(p[0]) < 0.5 and 0.7 < p[2] < 1.5: continue
        Co(0.06, 0.3, p, "orange", (math.atan2(math.hypot(p[0], p[1]), p[2]-1.1)*0 + math.acos(min(1, max(-1, (p[2]-1.1)/0.72))), 0, math.atan2(p[1], p[0])+R90), verts=8, name="Spike")
    t = tailfin((0, 0.7, 1.1), "orange", 0.35, 0.4)
    fins = []
    for sx in (-1, 1): p = E((sx*0.5, -0.2, 1.0), name="FinPiv"); fin((sx*0.75, -0.2, 0.95), 0.2, "orange", p, rot=(0, rad(sx*60), 0)); fins.append(p)
    fish_eyes(1.3, -0.68, 0.26, 0.16); S(0.1, (0, -0.76, 0.9), (1, 0.6, 0.8), "mouth", name="Pout"); return {"tail": t, "fins": fins}
def b_lobster():
    EL = [((0, -0.2, 0.7), 0.4, (1, 1.3, 0.8))] + chain((0, 0.3, 0.7), (0, 1.4, 0.6), 0.32, 0.2, 6)
    fish_body("lobster", "coral", EL, 0.7)
    for sx in (-1, 1): S(0.2, (sx*0.18, 1.6, 0.55), (1.2, 1.4, 0.25), "lobster", rot=(0, 0, rad(sx*25)), name="TailFan")
    claws = []; legs = []
    for sx in (-1, 1):
        p = E((sx*0.4, -0.55, 0.7), name="ClawPiv"); claws.append(p)
        RC(0.09, 0.5, (sx*0.6, -0.85, 0.7), "lobster", (R90, 0, rad(-sx*25)), p, lv=1); S(0.28, (sx*0.7, -1.3, 0.72), (0.9, 1.3, 0.7), "lobster", p, name="Claw"); S(0.15, (sx*0.6, -1.65, 0.8), (0.8, 1.2, 0.5), "lobster", p, name="ClawTip")
        for k in range(3):
            lp = E((sx*0.35, -0.3+k*0.3, 0.55), name="LegPiv"); legs.append(lp); RC(0.045, 0.6, (sx*0.6, -0.3+k*0.3, 0.35), "lobster", (0, rad(-sx*50), 0), lp, lv=1)
        Cy(0.02, 1.2, (sx*0.15, -1.2, 1.2), "lobster", (rad(-60), 0, rad(sx*-10)), name="Antenna")
    fish_eyes(0.98, -0.6, 0.2, 0.11); smile(0.62, -0.62, 0.1, tongue=False); return {"claws": claws, "legs": legs, "wiggle": True}
def b_seal():
    EL = [((0, 0.1, 0.75), 0.6, (1.0, 1.5, 0.85)), ((0, -0.75, 1.0), 0.42, None), ((0, -1.1, 0.95), 0.2, (1, 1.2, 0.8))] + chain((0, 0.8, 0.6), (0, 1.5, 0.5), 0.35, 0.18, 4)
    fish_body((0.6, 0.65, 0.72), (0.85, 0.87, 0.9), EL, 0.75, chest=True)
    for sx in (-1, 1): S(0.22, (sx*0.25, 1.65, 0.4), (1.3, 1.2, 0.25), (0.6, 0.65, 0.72), rot=(0, 0, rad(sx*30)), name="TailFin")
    fins = []
    for sx in (-1, 1): p = E((sx*0.45, -0.3, 0.45), name="FinPiv"); f = S(0.3, (sx*0.7, -0.4, 0.3), (1.2, 0.7, 0.2), (0.6, 0.65, 0.72), p, rot=(0, rad(sx*-15), rad(sx*-30)), name="Flipper"); fins.append(p)
    S(0.09, (0, -1.32, 1.02), (1.2, 0.8, 0.8), "black", name="Nose")
    for sx in (-1, 1):
        for k in range(3): Cy(0.008, 0.4, (sx*0.3, -1.22, 0.9+0.05*k), "white", (0, rad(sx*80+k*8), 0), name="Whisker")
    fish_eyes(1.2, -1.05, 0.22, 0.13); smile(0.85, -1.25, 0.08, tongue=False); return {"fins": fins, "finamp": 20, "wiggle": True}
def b_penguin():
    o = S(0.62, (0, 0, 0.95), (1, 0.95, 1.35), "charcoal" if "charcoal" in PAL else "black"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2
    S(0.5, (0, -0.15, 0.85), (0.85, 0.7, 1.15), "white"); S(0.42, (0, -0.05, 1.85), (1, 1, 1), "charcoal" if "charcoal" in PAL else "black")
    S(0.3, (0, -0.25, 1.78), (1.0, 0.6, 0.85), "white"); Co(0.1, 0.3, (0, -0.5, 1.75), "orange", (R90, 0, 0), verts=12, name="Beak")
    fins = []
    for sx in (-1, 1): p = E((sx*0.5, 0.0, 1.3), name="FinPiv"); f = S(0.32, (sx*0.68, 0.0, 1.0), (0.35, 0.6, 1.0), "charcoal" if "charcoal" in PAL else "black", p, rot=(0, rad(sx*15), 0), name="Flipper"); fins.append(p)
    for sx in (-1, 1): S(0.16, (sx*0.25, -0.15, 0.08), (1, 1.5, 0.5), "orange", name="Foot")
    fish_eyes(1.95, -0.38, 0.18, 0.11); return {"fins": fins, "finamp": 30, "wiggle": True}
def b_narwhal():
    def spots(cc, n):
        if n.z > 0.3 and cc.z > 1.1 and int((cc.x+3)*4) % 2 == 0 and int((cc.y+3)*4) % 2 == 0: return 2
        return 0
    EL = [((0, 0.1, 1.1), 0.58, (0.85, 1.5, 0.9)), ((0, -0.75, 1.05), 0.38, (1, 1, 0.85))] + chain((0, 0.9, 1.1), (0, 1.65, 1.25), 0.35, 0.17, 5)
    fish_body((0.75, 0.8, 0.9), "white", EL, 1.1, extra_mats=[(0.5, 0.55, 0.7)], region=spots)
    t = tailfin((0, 1.7, 1.25), (0.75, 0.8, 0.9), 0.55, 0.55, horizontal=True)
    Co(0.07, 1.6, (0, -1.9, 1.2), "pearl", (R90, 0, 0), verts=10, name="Tusk")
    for k in range(6): To(0.065, 0.015, (0, -1.25-0.22*k, 1.2), "lgrey", (R90, 0, 0))
    fins = []
    for sx in (-1, 1): p = E((sx*0.35, -0.35, 0.8), name="FinPiv"); fin((sx*0.62, -0.35, 0.7), 0.26, (0.75, 0.8, 0.9), p, rot=(0, rad(sx*55), 0)); fins.append(p)
    fish_eyes(1.28, -0.98, 0.25, 0.12); smile(0.88, -1.15, 0.12, tongue=False); return {"tail": t, "tailaxis": 0, "tailamp": 15, "fins": fins}
def b_manta():
    o = S(0.8, (0, 0.1, 1.1), (0.9, 1.3, 0.45), "dkblue"); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2
    S(0.68, (0, 0.0, 0.98), (0.9, 1.2, 0.3), "white"); wings = []
    for sx in (-1, 1):
        p = E((sx*0.5, 0.0, 1.1), name="WingPiv"); wings.append(p)
        w = S(0.95, (sx*1.45, 0.1, 1.1), (1.6, 1.0, 0.12), "dkblue", p, rot=(0, rad(sx*-8), rad(sx*10)), name="Wing"); S(0.14, (sx*2.55, -0.25, 1.15), (1.4, 1, 0.5), "dkblue", p, name="WingTip")
    Cy(0.04, 1.7, (0, 1.7, 1.1), "dkblue", (R90, 0, 0), name="Tail")
    for sx in (-1, 1): S(0.14, (sx*0.45, -1.0, 1.1), (0.6, 1.2, 0.5), "dkblue", name="Lobe")
    fish_eyes(1.22, -0.9, 0.36, 0.15); smile(0.9, -0.95, 0.15, tongue=False); return {"wings": wings, "flap": 28, "zc": 1.1}
ACTS["dino"] = lambda h: None
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}
