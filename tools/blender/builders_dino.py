# Dino Island builders — metaball body + subsurf, separate head/jaw/legs for animation
exec(open(PIPE + "/builders_meta.py", encoding="utf-8").read().split("BUILD = {k[2:]")[0])
PAL.update(dict(sky=(0.3,0.6,1.0), mint=(0.2,0.75,0.55), blue=(0.15,0.4,0.95), teal=(0.1,0.7,0.75), lavender=(0.8,0.7,1.0), lgreen=(0.55,0.85,0.35), coral=(1.0,0.45,0.35), violet=(0.45,0.3,0.85), aqua=(0.3,0.8,0.85), sand=(0.95,0.88,0.6), rust=(0.8,0.35,0.15), plum=(0.6,0.2,0.5), ivory=(0.98,0.95,0.85)))

def body_blob(c, belly, elems, extra_mats=(), extra_region=None, bz=1.0, res=0.085, chest=True):
    def region(cc, n):
        if extra_region:
            r = extra_region(cc, n)
            if r: return r
        if n.z < -0.25 and cc.z < bz + 0.05 and abs(cc.x) < 0.55 and -0.9 < cc.y < 0.9: return 1
        if chest and n.y < -0.45 and cc.z < bz + 0.35 and cc.y < -0.25 and abs(cc.x) < 0.42 and cc.z > 0.3: return 1
        return 0
    return metachar(elems, [], [c, belly] + list(extra_mats), region, res=0.065)

def head_unit(piv_loc, c, r=0.42, snout=(0.42, 0.25), hs=(1.0, 1.05, 0.95), eye=(0.17, 0.24), jaw=True, teeth=0, belly=None, top=()):
    """returns (headpiv, jawpiv). head blob in world coords around piv_loc"""
    px, py, pz = piv_loc
    piv = E(piv_loc, name="HeadPiv")
    EL = [((px, py-0.08, pz+0.08), r, hs), ((px, py-snout[0], pz-0.04), snout[1], (1.0, 1.1, 0.8))] + list(top)
    def region(cc, n): return 1 if (belly and n.z < -0.3 and cc.z < pz) else 0
    head = metachar(EL, [], [c, belly or c], region, res=0.06)
    par(head, piv)
    jp = None
    if jaw:
        jz = pz - r*0.55; jy = py - snout[0]*0.35
        jp = E((px, py+0.05, jz), piv, name="JawPiv")
        S(snout[1]*1.1, (px, jy, jz-0.02), (1.0, 1.5, 0.45), c, jp, name="Jaw")
        S(snout[1]*0.95, (px, jy-0.02, jz+0.06), (0.95, 1.4, 0.3), "mouth", jp, name="MouthIn")
        S(snout[1]*0.5, (px, jy-0.1, jz+0.1), (1, 1.3, 0.4), "tongue", jp, name="Tongue")
        S(snout[1]*0.9, (px, jy-0.02, jz+0.2), (0.95, 1.4, 0.35), "mouth", piv, name="MouthRoof")
        for k in range(teeth):
            for sx in (-1, 1):
                Co(0.03, 0.09, (px+sx*(0.08+0.07*k), jy-snout[1]*0.95+0.12*k, jz+0.08), "white", (math.pi, 0, 0), jp, verts=8, name="Tooth")
        # smile line at the lip
        halfdisc((px, jy-snout[1]*1.05, jz+0.1), snout[1]*0.6, 0.04, "mouth", jp)
    ex, ey = eye
    eyes(pz+0.18, py-0.12-r*0.55, ex, ey*0.6, piv)
    return piv, jp

def biped_legs(c, hip=(0.34, 0.3, 0.8), foot_c=None, claws=True, thick=0.26, big=False):
    out = []
    dx, hy, hz = hip
    for sx in (-1, 1):
        p = E((sx*dx, hy, hz), name="LegPiv"); out.append(p)
        S(thick*1.15, (sx*dx*0.9, hy, hz+0.12), (1, 1.1, 0.95), c, name="Hip")          # joint ball, fixed to the body
        S(thick, (sx*dx, hy, hz-0.12), (1, 1.1, 1.3), c, p, name="Thigh")
        Cy(thick*0.45, hz*0.6, (sx*dx, hy-0.02, hz*0.35), c, parent=p)
        S(thick*0.7, (sx*dx, hy-0.14, 0.11), (1.1, 1.7, 0.55), foot_c or c, p, name="Foot")
        if claws:
            for k in (-1, 0, 1): Co(0.045, 0.14, (sx*dx+k*0.1, hy-0.14-thick*0.95, 0.07), "ivory", (R90, 0, 0), p, verts=8, name="Claw")
    return out

def quad_legs(c, dx=0.42, dy=0.5, z=0.7, r=0.16, foot_c=None, nails=True):
    out = []
    for (x, y) in [(-dx, -dy), (dx, -dy), (-dx, dy), (dx, dy)]:
        p = E((x, y, z), name="LegPiv"); out.append(p)
        S(r*1.7, (x*0.85, y*0.9, z+0.08), (1, 1, 0.9), c, name="Hip")                   # joint ball, fixed to the body
        S(r*1.25, (x, y, z*0.6), (1, 1, z*0.55/(r*1.25)), c, p, name="Leg")
        S(r*1.35, (x, y-0.04, 0.12), (1, 1.15, 0.6), foot_c or c, p, name="Foot")
        if nails:
            for k in (-1, 0, 1): S(0.045, (x+k*r*0.7, y-r*1.35, 0.07), (1, 1.2, 0.8), "ivory", p, name="Nail")
    return out

def arms(c, sh=(0.36, -0.3, 1.05), L=0.3):
    for sx in (-1, 1):
        Cy(0.055, L, (sx*sh[0], sh[1]-0.08, sh[2]-L*0.4), c, (rad(-35), 0, 0), name="Arm")
        S(0.075, (sx*sh[0], sh[1]-0.2, sh[2]-L*0.85), (1, 1.2, 0.8), c, name="Hand")

def tail_elems(start=(0, 0.75, 0.9), n=4, r0=0.3, up=0.08, step=0.32):
    out = []; m = n*2
    for k in range(m):
        t = k/(m-1); out.append(((start[0], start[1]+step*(n-1)*t, start[2]+up*(n-1)**2*t*t*0.5), r0*(1-0.42*t), None))
    return out
def chain(p0, p1, r0, r1, n=6):
    a = Vector(p0); b = Vector(p1)
    return [((a+(b-a)*(k/(n-1))).to_tuple(), r0+(r1-r0)*k/(n-1), None) for k in range(n)]

def back_plates(c, ys, z=1.55, size=0.3, shape="plate"):
    for i, y in enumerate(ys):
        s = size*(1-0.35*abs(i-(len(ys)-1)/2)/max(1, (len(ys)-1)/2))
        if shape == "plate": Fp([(-s*0.8, 0), (s*0.8, 0), (s*0.55, s*1.3), (0, s*1.7), (-s*0.55, s*1.3)], (0, y, z-0.15), 0.08, c, rot=(0, 0, R90))
        else: Co(s*0.5, s*1.3, (0, y, z+s*0.4), c, verts=10)

def dino_walk(h):
    sine(ROOT, "location", 2, 0.13, 4, phase=-math.pi/2)                      # body rises and falls twice per stride
    sine(ROOT, "rotation_euler", 2, rad(7), 2, phase=0)                        # yaw sway: the tail swings left/right
    sine(ROOT, "rotation_euler", 0, rad(3), 4, phase=0)                        # slight pitch
    ph = h.get("legphase", None)
    for i, l in enumerate(h.get("legs", [])):
        sine(l, "rotation_euler", 0, rad(h.get("legamp", 24)*1.4), 2, phase=(ph[i] if ph else math.pi*(i % 2)))
    if "head" in h: sine(h["head"], "rotation_euler", 0, rad(12), 4, phase=math.pi/2); sine(h["head"], "rotation_euler", 2, rad(5), 2, phase=math.pi)
    for i, w in enumerate(h.get("wings", [])):
        sx = -1 if i % 2 == 0 else 1
        sine(w, "rotation_euler", 1, rad(h.get("flap", 30))*sx, 3)
    if h.get("hover"): sine(ROOT, "location", 2, 0.16, 1)
    for i, f in enumerate(h.get("flippers", [])):
        sine(f, "rotation_euler", 1, rad(28)*(-1 if i % 2 == 0 else 1), 2, phase=math.pi*(i // 2))
def dino_roar(h):
    keys(ROOT, "location", [(1,(0,0,0)),(4,(0,0,0)),(7,(0,0,0.42)),(10,(0,0,0.18)),(12,(0,0,0)),(14,(0,0,0)),(16,(0,0,0.26)),(19,(0,0,0)),(24,(0,0,0))])
    keys(ROOT, "scale", [(1,(1,1,1)),(4,(1.08,1.08,0.9)),(7,(0.95,0.95,1.08)),(12,(1,1,1)),(14,(1.05,1.05,0.95)),(17,(0.97,0.97,1.04)),(21,(1,1,1))])
    if "head" in h: keys(h["head"], "rotation_euler", [(1,(0,0,0)),(5,(rad(-26),0,0)),(9,(rad(-22),0,0)),(12,(rad(-28),0,0)),(15,(rad(-23),0,0)),(18,(rad(-27),0,0)),(22,(0,0,0))])
    if h.get("jaw"): keys(h["jaw"], "rotation_euler", [(1,(0,0,0)),(5,(rad(34),0,0)),(8,(rad(26),0,0)),(11,(rad(36),0,0)),(14,(rad(28),0,0)),(18,(rad(32),0,0)),(22,(0,0,0))])
    for i, w in enumerate(h.get("wings", [])):
        sx = -1 if i % 2 == 0 else 1
        keys(w, "rotation_euler", [(1,(0,0,0)),(5,(0,rad(-45)*sx,0)),(12,(0,rad(-50)*sx,0)),(18,(0,rad(-40)*sx,0)),(22,(0,0,0))])
ACTS["walk"] = dino_walk; ACTS["roar"] = dino_roar; ACTS["dino"] = lambda h: None

# ------------------------------------------------------------------ the 16 dinos
def b_trex():
    body_blob("green", "lgreen", [((0, 0.1, 1.05), 0.52, (1.0, 1.3, 0.95)), ((0, -0.45, 1.4), 0.3, None)] + tail_elems((0, 0.7, 0.95), 4, 0.3, 0.1), bz=1.05)
    hp, jp = head_unit((0, -0.62, 1.85), "green", r=0.44, snout=(0.5, 0.27), teeth=3)
    for sx in (-1, 1): S(0.09, (sx*0.2, -0.85, 2.12), (1.3, 1, 0.6), "dkgreen", hp, name="Brow")
    legs = biped_legs("green", hip=(0.36, 0.3, 0.8), thick=0.27); arms("green", sh=(0.4, -0.3, 1.1), L=0.25)
    return {"head": hp, "jaw": jp, "legs": legs}
def b_triceratops():
    body_blob("orange", "sand", [((0, 0.15, 0.95), 0.6, (1.05, 1.4, 0.9))] + tail_elems((0, 0.95, 0.85), 3, 0.26, 0.05), bz=0.95)
    hp, jp = head_unit((0, -0.9, 1.25), "orange", r=0.42, snout=(0.5, 0.26), hs=(1.05, 1.0, 0.95), teeth=0)
    Co(0.07, 0.4, (0, -1.5, 1.2), "ivory", (rad(-100), 0, 0), hp, verts=10, name="NoseHorn")
    for sx in (-1, 1): Co(0.07, 0.55, (sx*0.26, -0.95, 1.62), "ivory", (rad(-30), rad(sx*12), 0), hp, verts=10, name="Horn")
    fr = halfdisc((0, -0.55, 1.3), 0.72, 0.1, "rust", hp, flip=True, segs=20); fr.scale = (1.0, 1, 0.95)
    for k in range(7):
        a = math.pi*(k+0.5)/7; S(0.08, (0.7*math.cos(a), -0.55, 1.3+0.68*math.sin(a)), (1, 1, 1), "gold", hp, name="FrillDot")
    legs = quad_legs("orange", dx=0.45, dy=0.5, z=0.65, r=0.17)
    return {"head": hp, "jaw": jp, "legs": legs, "legphase": [0, math.pi, math.pi, 0]}
def b_stegosaurus():
    body_blob("purple", "lavender", [((0, 0.1, 1.0), 0.62, (0.95, 1.45, 0.95))] + tail_elems((0, 1.0, 0.9), 4, 0.28, 0.1), bz=1.0)
    hp, jp = head_unit((0, -1.0, 1.05), "purple", r=0.34, snout=(0.36, 0.22), hs=(0.95, 1.0, 0.85))
    back_plates("orange", [-0.45, -0.1, 0.25, 0.6, 0.95, 1.3], z=1.55, size=0.32)
    for k in range(4): Co(0.05, 0.3, (0.14*(1 if k % 2 else -1), 1.55+0.12*k, 1.3), "gold", (rad(-30), 0, rad(30*(1 if k % 2 else -1))), verts=8, name="Spike")
    legs = quad_legs("purple", dx=0.42, dy=0.55, z=0.6, r=0.17)
    return {"head": hp, "jaw": jp, "legs": legs, "legphase": [0, math.pi, math.pi, 0]}
def b_brachiosaurus():
    EL = [((0, 0.2, 1.05), 0.6, (0.95, 1.35, 0.95))] + chain((0, -0.5, 1.35), (0, -0.82, 2.95), 0.34, 0.24, 8) + tail_elems((0, 1.05, 0.95), 4, 0.3, 0.06)
    body_blob("sky", "cream", EL, bz=1.05, chest=False)
    hp, jp = head_unit((0, -0.82, 3.15), "sky", r=0.3, snout=(0.3, 0.2), hs=(0.95, 1.0, 0.9), belly="cream")
    legs = quad_legs("sky", dx=0.42, dy=0.5, z=0.68, r=0.18)
    return {"head": hp, "jaw": jp, "legs": legs, "legphase": [0, math.pi, math.pi, 0]}
def b_pterodactyl():
    body_blob("teal", "cream", [((0, 0.0, 1.2), 0.42, (0.9, 1.4, 0.85)), ((0, -0.5, 1.45), 0.26, None)] + tail_elems((0, 0.55, 1.15), 3, 0.2, 0.0), bz=1.2)
    hp, jp = head_unit((0, -0.7, 1.75), "teal", r=0.32, snout=(0.62, 0.17), hs=(0.9, 1.0, 0.85), teeth=0)
    Co(0.12, 0.6, (0, -0.4, 2.05), "orange", (rad(-115), 0, 0), hp, verts=12, name="Crest")
    wings = []
    for sx in (-1, 1):
        p = E((sx*0.3, 0.0, 1.35), name="WingPiv"); wings.append(p)
        w = S(0.5, (sx*1.25, 0.1, 1.4), (2.1, 1.0, 0.14), "orange", p, name="Wing"); w.rotation_euler = (0, rad(sx*-6), rad(sx*-8))
        Cy(0.06, 1.9, (sx*1.2, -0.28, 1.5), "teal", (0, rad(sx*82), 0), p, name="WingBone"); S(0.09, (sx*2.15, -0.35, 1.58), (1, 1, 1), "teal", p, name="WingTip")
    legs = biped_legs("teal", hip=(0.2, 0.25, 0.75), thick=0.15, claws=True)
    return {"head": hp, "jaw": jp, "wings": wings, "flap": 28, "hover": True, "legs": []}
def b_velociraptor():
    def stripes(cc, n):
        if n.z > 0.2 and cc.z > 0.9 and -0.4 < cc.y < 1.4 and int((cc.y+2.0)*4.5) % 2 == 0: return 2
        return 0
    body_blob("coral", "cream", [((0, 0.1, 0.95), 0.42, (0.95, 1.5, 0.9)), ((0, -0.45, 1.25), 0.25, None)] + tail_elems((0, 0.7, 0.9), 5, 0.22, 0.03, 0.3), extra_mats=["rust"], extra_region=stripes, bz=0.95)
    hp, jp = head_unit((0, -0.6, 1.65), "coral", r=0.34, snout=(0.5, 0.2), teeth=3)
    for k in range(4): S(0.1, (0, -0.45+0.1*k, 2.0-0.05*k), (0.6, 1, 1.2), "rust", hp, name="Feather")
    legs = biped_legs("coral", hip=(0.3, 0.3, 0.72), thick=0.2)
    for i, p in enumerate(legs):
        sx = -1 if i == 0 else 1; Co(0.05, 0.22, (sx*0.3-sx*0.1, 0.02, 0.2), "ivory", (rad(-120), 0, 0), p, verts=8, name="Sickle")
    arms("coral", sh=(0.32, -0.3, 1.0), L=0.28)
    return {"head": hp, "jaw": jp, "legs": legs}
def b_ankylosaurus():
    def plates(cc, n):
        if n.z > 0.35 and cc.z > 0.95 and -0.55 < cc.y < 0.9: return 2
        return 0
    body_blob("brown", "tan", [((0, 0.15, 0.85), 0.62, (1.2, 1.45, 0.78))] + tail_elems((0, 1.0, 0.75), 4, 0.3, 0.0, 0.28), extra_mats=["rust"], extra_region=plates, bz=0.85)
    S(0.3, (0, 2.0, 0.8), (1.3, 1.0, 0.9), "rust", name="Club")
    for (x, y) in [(-0.45, -0.3), (0.45, -0.3), (-0.5, 0.2), (0.5, 0.2), (-0.4, 0.7), (0.4, 0.7), (0, -0.05), (0, 0.45)]:
        Co(0.11, 0.3, (x, y, 1.3-abs(x)*0.25), "gold", (rad(x*35), 0, 0), verts=10, name="Spike")
    for sx in (-1, 1):
        for y in (-0.2, 0.3, 0.8): Co(0.08, 0.3, (sx*0.78, y, 0.9), "gold", (0, rad(sx*80), 0), verts=8, name="SideSpike")
    hp, jp = head_unit((0, -0.95, 1.05), "brown", r=0.3, snout=(0.3, 0.22), hs=(1.15, 1.0, 0.8))
    for sx in (-1, 1): Co(0.06, 0.2, (sx*0.3, -0.85, 1.3), "gold", (0, rad(sx*40), 0), hp, verts=8, name="HeadHorn")
    legs = quad_legs("brown", dx=0.5, dy=0.5, z=0.5, r=0.16)
    return {"head": hp, "jaw": jp, "legs": legs, "legphase": [0, math.pi, math.pi, 0], "legamp": 18}
def b_parasaurolophus():
    body_blob("yellow", "cream", [((0, 0.15, 1.05), 0.5, (0.95, 1.35, 0.95)), ((0, -0.5, 1.45), 0.3, None)] + tail_elems((0, 0.75, 0.95), 4, 0.28, 0.06), bz=1.05)
    hp, jp = head_unit((0, -0.7, 1.9), "yellow", r=0.36, snout=(0.5, 0.24), hs=(0.95, 1.05, 0.9))
    Cy(0.11, 0.9, (0, -0.35, 2.45), "orange", (rad(-55), 0, 0), hp, name="Crest"); S(0.12, (0, -0.05, 2.78), (1, 1, 1), "orange", hp, name="CrestTip")
    legs = biped_legs("yellow", hip=(0.35, 0.3, 0.8), thick=0.26, claws=False); arms("yellow", sh=(0.38, -0.3, 1.15), L=0.3)
    return {"head": hp, "jaw": jp, "legs": legs}
def b_spinosaurus():
    body_blob("navy", "sky", [((0, 0.1, 1.05), 0.5, (1.0, 1.4, 0.95)), ((0, -0.5, 1.4), 0.3, None)] + tail_elems((0, 0.75, 0.95), 5, 0.3, 0.05, 0.3), bz=1.05)
    Fp([(-0.75, 0), (0.75, 0), (0.6, 0.6), (0.3, 0.95), (0, 1.05), (-0.3, 0.95), (-0.6, 0.6)], (0, 0.1, 1.45), 0.1, "red", rot=(0, 0, R90), name="Sail")
    hp, jp = head_unit((0, -0.7, 1.85), "navy", r=0.36, snout=(0.75, 0.2), hs=(0.9, 1.1, 0.9), teeth=4)
    legs = biped_legs("navy", hip=(0.36, 0.3, 0.8), thick=0.26); arms("navy", sh=(0.4, -0.3, 1.1), L=0.3)
    return {"head": hp, "jaw": jp, "legs": legs}
def b_diplodocus():
    EL = [((0, 0.3, 1.0), 0.55, (0.95, 1.5, 0.9))] + chain((0, -0.55, 1.15), (0, -2.0, 1.85), 0.32, 0.23, 8)
    EL += chain((0, 1.0, 0.95), (0, 2.7, 1.25), 0.3, 0.17, 9)
    body_blob("mint", "cream", EL, bz=1.0, chest=False)
    hp, jp = head_unit((0, -2.1, 2.05), "mint", r=0.27, snout=(0.3, 0.18), hs=(0.95, 1.05, 0.85), belly="cream")
    legs = quad_legs("mint", dx=0.4, dy=0.55, z=0.65, r=0.17)
    return {"head": hp, "jaw": jp, "legs": legs, "legphase": [0, math.pi, math.pi, 0]}
def b_pachycephalosaurus():
    body_blob("pink", "cream", [((0, 0.1, 1.0), 0.48, (1.0, 1.35, 0.95)), ((0, -0.45, 1.35), 0.28, None)] + tail_elems((0, 0.7, 0.9), 4, 0.26, 0.08), bz=1.0)
    hp, jp = head_unit((0, -0.6, 1.75), "pink", r=0.38, snout=(0.45, 0.22), hs=(1.0, 1.0, 1.05))
    S(0.3, (0, -0.62, 2.12), (1.05, 1.1, 0.75), "hotpink", hp, name="Dome")
    for k in range(8):
        a = k*TAU/8; Co(0.04, 0.14, (0.36*math.cos(a), -0.62+0.36*math.sin(a), 2.0), "ivory", (rad(-30*math.sin(a)), rad(30*math.cos(a)), 0), hp, verts=8, name="Knob")
    legs = biped_legs("pink", hip=(0.33, 0.3, 0.78), thick=0.25); arms("pink", sh=(0.38, -0.3, 1.08), L=0.26)
    return {"head": hp, "jaw": jp, "legs": legs}
def b_plesiosaurus():
    EL = [((0, 0.2, 0.85), 0.55, (1.1, 1.4, 0.75))] + chain((0, -0.6, 0.95), (0, -1.45, 2.25), 0.3, 0.22, 8) + tail_elems((0, 0.95, 0.8), 3, 0.24, 0.0)
    body_blob("blue", "white", EL, bz=0.85, chest=False)
    hp, jp = head_unit((0, -1.5, 2.45), "blue", r=0.28, snout=(0.32, 0.18), hs=(0.95, 1.05, 0.85), teeth=2, belly="white")
    flippers = []
    for (x, y) in [(-0.5, -0.3), (0.5, -0.3), (-0.5, 0.45), (0.5, 0.45)]:
        sx = -1 if x < 0 else 1
        p = E((x, y, 0.55), name="FlipPiv"); flippers.append(p)
        f = S(0.4, (x+sx*0.4, y, 0.4), (1.2, 0.55, 0.22), "blue", p, name="Flipper"); f.rotation_euler = (0, rad(sx*-18), rad(sx*-15))
    S(0.6, (0, 0.2, 0.3), (1.0, 1.3, 0.3), "blue", name="Belly")
    return {"head": hp, "jaw": jp, "flippers": flippers, "legs": []}
def b_iguanodon():
    body_blob("lime", "cream", [((0, 0.1, 1.0), 0.5, (1.0, 1.4, 0.95)), ((0, -0.5, 1.4), 0.3, None)] + tail_elems((0, 0.75, 0.9), 5, 0.3, 0.04, 0.3), bz=1.0)
    hp, jp = head_unit((0, -0.7, 1.85), "lime", r=0.36, snout=(0.5, 0.25), hs=(0.95, 1.05, 0.9))
    Co(0.11, 0.1, (0, -1.3, 1.65), "dkgreen", (rad(-90), 0, 0), hp, verts=12, name="Beak")
    legs = biped_legs("lime", hip=(0.35, 0.3, 0.8), thick=0.26, claws=False); arms("lime", sh=(0.4, -0.3, 1.1), L=0.32)
    for sx in (-1, 1): Co(0.04, 0.18, (sx*0.46, -0.52, 0.95), "ivory", (0, rad(sx*70), 0), verts=8, name="ThumbSpike")
    return {"head": hp, "jaw": jp, "legs": legs}
def b_allosaurus():
    body_blob("rust", "sand", [((0, 0.1, 1.05), 0.52, (1.0, 1.35, 0.95)), ((0, -0.45, 1.4), 0.3, None)] + tail_elems((0, 0.7, 0.95), 5, 0.3, 0.06, 0.3), bz=1.05)
    hp, jp = head_unit((0, -0.62, 1.85), "rust", r=0.42, snout=(0.55, 0.26), teeth=4)
    for sx in (-1, 1): Co(0.1, 0.22, (sx*0.24, -0.78, 2.22), "red", (rad(-20), 0, 0), hp, verts=10, name="BrowHorn")
    legs = biped_legs("rust", hip=(0.36, 0.3, 0.8), thick=0.27); arms("rust", sh=(0.4, -0.3, 1.1), L=0.28)
    return {"head": hp, "jaw": jp, "legs": legs}
def b_dilophosaurus():
    body_blob("violet", "aqua", [((0, 0.1, 1.0), 0.46, (0.95, 1.4, 0.95)), ((0, -0.45, 1.35), 0.28, None)] + tail_elems((0, 0.7, 0.9), 5, 0.27, 0.05, 0.3), bz=1.0)
    hp, jp = head_unit((0, -0.62, 1.8), "violet", r=0.37, snout=(0.55, 0.22), teeth=3)
    for sx in (-1, 1):
        c = halfdisc((sx*0.12, -0.75, 1.95), 0.36, 0.06, "hotpink", hp, flip=True, segs=14); c.rotation_euler = (0, rad(sx*-12), rad(sx*-25))
    legs = biped_legs("violet", hip=(0.33, 0.3, 0.78), thick=0.24); arms("violet", sh=(0.36, -0.3, 1.05), L=0.28)
    return {"head": hp, "jaw": jp, "legs": legs}
def b_archaeopteryx():
    body_blob("gold", "cream", [((0, 0.05, 1.0), 0.38, (0.95, 1.3, 0.95)), ((0, -0.4, 1.25), 0.22, None)] + tail_elems((0, 0.55, 0.95), 3, 0.17, 0.02, 0.28), bz=1.0)
    hp, jp = head_unit((0, -0.52, 1.6), "gold", r=0.3, snout=(0.42, 0.16), hs=(0.95, 1.0, 0.95), teeth=2)
    S(0.1, (0, -0.4, 1.95), (0.6, 1, 1.3), "blue", hp, name="Crest")
    wings = []
    for sx in (-1, 1):
        p = E((sx*0.25, -0.05, 1.15), name="WingPiv"); wings.append(p)
        for k in range(4):
            f = S(0.3, (sx*(0.45+0.26*k), -0.02+0.05*k, 1.18-0.06*k), (1.0, 0.6, 0.16), "blue" if k % 2 else "sky", p, name="Feather"); f.rotation_euler = (0, rad(sx*-12), rad(sx*(10-8*k)))
        w = S(0.4, (sx*0.6, -0.1, 1.25), (1.4, 0.7, 0.18), "gold", p, name="WingTop"); w.rotation_euler = (0, rad(sx*-10), 0)
    for k in range(5): f = S(0.3, (0.12*(k-2), 1.3, 1.0), (0.32, 1.0, 0.15), "blue" if k % 2 else "gold", rot=(0, 0, rad((k-2)*-14)), name="TailFeather")
    legs = biped_legs("orange", hip=(0.2, 0.2, 0.7), thick=0.12, claws=True)
    return {"head": hp, "jaw": jp, "legs": legs, "wings": wings, "flap": 22}

# ------------------------------------------------------------------ egg
def b_egg():
    import bmesh, random
    random.seed(11); R=0.75; Z=0.85; SZ=1.25; CUT=0.95
    EC = globals().get("EGG_C", "ivory"); ESP = globals().get("EGG_SPOTS", ["sky", "pink", "lime", "orange", "lavender", "coral"]); EY = globals().get("EGG_YOLK", "sand")
    def shell_sphere(name, c=EC):
        o = S(R, (0, 0, Z), (1, 1, SZ), c, name=name); m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = 2; return o
    top = shell_sphere("Top")
    cup = shell_sphere("Cup"); bm = bmesh.new(); bm.from_mesh(cup.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z*SZ + Z > CUT], context='VERTS'); bm.to_mesh(cup.data); bm.free()
    for v in cup.data.vertices:   # jagged rim
        if v.co.z*SZ + Z > CUT-0.3: v.co.z += random.uniform(-0.08, 0.08)/SZ
    sm = cup.modifiers.new("Solid", 'SOLIDIFY'); sm.thickness = 0.06; sm.offset = -1
    cup.modifiers.move(1, 0)
    inner = S(R*0.82, (0, 0, 0.62), (1, 1, 0.45), EY, cup, name="Yolk")
    spots_top, spots_cup = [], []
    for k in range(16):
        a = random.uniform(0, TAU); z = random.uniform(0.25, 1.6); r = R*math.sqrt(max(0, 1-((z-Z)/(R*SZ))**2))
        if r < 0.2: continue
        o = S(random.uniform(0.08, 0.13), (r*math.cos(a), r*math.sin(a), z), (1, 1, 1.2), ESP[k % len(ESP)], name="Spot")
        (spots_cup if z < CUT-0.1 else spots_top).append(o)
    # cracks (3 stages) — zigzag dark lines on the front; stage 3 glows
    CR = [[(0.0, -0.75, 1.05), (0.1, -0.73, 0.9), (-0.02, -0.75, 0.75), (0.12, -0.72, 0.62)],
          [(-0.32, -0.67, 1.2), (-0.22, -0.7, 1.02), (-0.36, -0.65, 0.88)],
          [(0.36, -0.64, 1.0), (0.46, -0.58, 0.84), (0.38, -0.62, 0.68)],
          [(0.0, -0.74, 1.05), (-0.14, -0.72, 1.18), (-0.06, -0.7, 1.32), (0.1, -0.68, 1.42)],
          [(0.2, -0.7, 1.28), (0.34, -0.63, 1.2), (0.3, -0.6, 1.38)]]
    cracks = [[], [], []]; glows = []
    for i, seg in enumerate(CR):
        stage = 0 if i == 0 else (1 if i < 3 else 2)
        for a, b in zip(seg, seg[1:]):
            a = Vector(a); b = Vector(b); d = b-a; mid = (a+b)/2
            o = Cy(0.02, d.length+0.02, tuple(mid), "ink", verts=6, name="Crack"); o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler(); cracks[stage].append(o)
            g = Cy(0.045, d.length+0.03, tuple(mid), (1.0, 0.9, 0.45), verts=6, name="Glow"); g.rotation_euler = o.rotation_euler
            g.data.materials[0] = mat((1.0, 0.85, 0.3), 0.4, 1.6); glows.append(g)
    rays = []
    for k in range(6):
        a = rad(-60+k*24); o = Co(0.008, 0.5, (0.45*math.sin(a), -0.95, 1.0+0.3*math.cos(a)), (1.0, 0.9, 0.4), (rad(-80), 0, a), r2=0.03, verts=8, name="Ray")
        o.data.materials[0] = mat((1.0, 0.8, 0.25), 0.4, 1.0); rays.append(o)
    # fragments for the hatch burst
    frags = []
    for k in range(10):
        a = k*TAU/10 + 0.3; z0 = random.uniform(1.0, 1.55); r0 = R*math.sqrt(max(0.05, 1-((z0-Z)/(R*SZ))**2))
        f = S(random.uniform(0.16, 0.26), (r0*math.cos(a), r0*math.sin(a), z0), (1, 1, 0.3), EC, name="Frag"); f.rotation_euler = (0, rad(60*math.cos(a)), a)
        if k % 3 == 0: S(0.07, (r0*math.cos(a), r0*math.sin(a), z0+0.05), (1, 1, 0.6), ESP[k % 3], f, name="FragSpot")
        frags.append((f, a, z0))
    burst = S(0.3, (0, 0, 1.0), (1, 1, 1), (1.0, 0.95, 0.5), name="Burst"); burst.data.materials[0] = mat((1.0, 0.95, 0.5), 0.3, 4.0)
    stars = []
    for k in range(8):
        a = k*TAU/8; st = Fp(starpts(0.12, 0.05), (0, 0, 1.0), 0.03, "gold", name="Star"); st.data.materials[0] = mat("gold", 0.3, 3.0); stars.append((st, a))
    def show(ob, on):
        ob.hide_render = not on; ob.hide_viewport = not on
    def state(stage):
        show(top, True); show(cup, False); show(inner, False)
        for o in spots_top: show(o, True)
        for o in spots_cup: show(o, True)
        for i in range(3):
            for o in cracks[i]: show(o, stage > i)
        for g in glows: show(g, stage >= 3)
        for o in rays: show(o, stage >= 3)
        for f, a, z0 in frags: show(f, False)
        show(burst, False)
        for st, a in stars: show(st, False)
    globals()['EXTRA_STILLS'] = [(f"{PREFIX}_s{k}", (lambda k=k: state(k))) for k in range(4)]
    state(0)
    return {"top": top, "cup": cup, "inner": inner, "spots_top": spots_top, "cracks": cracks, "glows": glows, "rays": rays, "frags": frags, "burst": burst, "stars": stars, "state": state, "show": show}
def egg_hatch(h):
    show = h["show"]; st = h["state"]
    def vis(ob, on, f): show(ob, on); ob.keyframe_insert("hide_render", frame=f); ob.keyframe_insert("hide_viewport", frame=f)
    st(0)
    # wobble + cracks appearing
    keys(ROOT, "rotation_euler", [(1,(0,0,0)),(2,(0,rad(10),0)),(4,(0,rad(-12),0)),(6,(0,rad(12),0)),(7,(0,rad(-8),0)),(8,(0,0,0)),(24,(0,0,0))])
    keys(ROOT, "scale", [(1,(1,1,1)),(5,(1.05,1.05,0.95)),(7,(0.95,0.95,1.1)),(8,(1,1,1))])
    for i in range(3):
        for o in h["cracks"][i]:
            vis(o, False, 1); vis(o, True, 2+2*i); vis(o, False, 8)
    for g in h["glows"]: vis(g, False, 1); vis(g, True, 7); vis(g, False, 8)
    for o in h["rays"]: vis(o, False, 1); vis(o, True, 7); vis(o, False, 8)
    vis(h["top"], True, 1); vis(h["top"], False, 8)
    for o in h["spots_top"]: vis(o, True, 1); vis(o, False, 8)
    vis(h["cup"], False, 1); vis(h["cup"], True, 8); vis(h["inner"], False, 1); vis(h["inner"], True, 8)
    for f, a, z0 in h["frags"]:
        vis(f, False, 1); vis(f, True, 8)
        p0 = Vector(f.location); d = Vector((math.cos(a), math.sin(a), 0))
        f.location = p0; kf(f, "location", 8)
        f.location = p0 + d*0.45 + Vector((0, 0, 0.6)); kf(f, "location", 13)
        f.location = p0 + d*0.85 + Vector((0, 0, 0.15)); kf(f, "location", 18)
        f.location = Vector((p0.x, p0.y, 0)) + d*1.0 + Vector((0, 0, 0.06)); kf(f, "location", 22); kf(f, "location", 24)
        r0 = tuple(f.rotation_euler); f.rotation_euler = r0; kf(f, "rotation_euler", 8)
        f.rotation_euler = (r0[0]+rad(240), r0[1]+rad(180), r0[2]); kf(f, "rotation_euler", 18)
        f.rotation_euler = (rad(90), 0, r0[2]); kf(f, "rotation_euler", 22); kf(f, "rotation_euler", 24)
    b = h["burst"]; vis(b, False, 1); vis(b, True, 8); vis(b, False, 17)
    keys(b, "scale", [(8,(0.3,0.3,0.3)),(11,(1.3,1.3,1.3)),(16,(1.7,1.7,1.7))])
    inp = b.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    for f, v in [(8, 4.0), (12, 2.0), (16, 0.0)]: inp.default_value = v; inp.keyframe_insert("default_value", frame=f)
    for st_, a in h["stars"]:
        vis(st_, False, 1); vis(st_, True, 9); vis(st_, False, 20)
        d = Vector((math.cos(a)*0.7, -0.6, 1.0+math.sin(a)*0.7))
        st_.location = (0, -0.5, 1.0); kf(st_, "location", 9); st_.location = d + Vector((math.cos(a)*0.5, 0, math.sin(a)*0.5)); kf(st_, "location", 19)
        st_.scale = (0.3,0.3,0.3); kf(st_, "scale", 9); st_.scale = (1.3,1.3,1.3); kf(st_, "scale", 14); st_.scale = (0.2,0.2,0.2); kf(st_, "scale", 19)
ACTS["hatch"] = egg_hatch
def b_seaegg():
    globals().update(EGG_C=(0.55, 0.85, 0.85), EGG_SPOTS=["white", (0.8, 0.95, 1.0), "mint", "sky"], EGG_YOLK=(0.7, 0.9, 0.95)); return b_egg()
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}
