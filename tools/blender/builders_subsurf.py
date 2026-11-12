# Fallback recipes: rounded via Subdivision Surface (no raw block look). All face -Y, stand on z=0.
def sub(o, lv=2):
    m = o.modifiers.new("Sub", 'SUBSURF'); m.levels = lv; m.render_levels = lv; smooth(o); return o
def RB(loc, scale, c, parent=None, rot=None, lv=2, name="o"):   # rounded box (pre-scaled: subsurf shrinks a cube ~25%)
    f = 1.0 if lv == 0 else 1.32
    return sub(B(loc, tuple(v*f for v in scale), c, parent, rot, 0.0, name), lv)
def RC(r, d, loc, c, rot=(0,0,0), parent=None, lv=2):            # rounded cylinder (capsule-ish)
    return sub(Cy(r*1.12, d*1.08, loc, c, rot, parent, 12), lv)
def RK(r1, d, loc, c, rot=(0,0,0), parent=None, lv=2, r2=0.0):   # rounded cone (teardrop)
    return sub(Co(r1*1.15, d*1.1, loc, c, rot, parent, r2, 12), lv)
def quad_s(body_c, belly_c, head_c=None, ear="round", ear_c=None, snout=None, tail="short", spots=None, legs_c=None, size=1.0, leg_h=0.4, head_r=0.42):
    hc = head_c or body_c; ear_c = ear_c or body_c; legs_c = legs_c or body_c; s = size
    RB((0,0.05,0.75*s), (1.0*s,1.5*s,0.9*s), body_c)                       # rounded body
    RB((0,-0.15,0.6*s), (0.7*s,1.1*s,0.6*s), belly_c)
    head = RB((0,-0.55*s,1.3*s), (0.9*s,0.85*s,0.8*s), hc)
    if ear == "round":
        for sx in (-1,1): RB((sx*0.32*s,-0.5*s,1.72*s),(0.28*s,0.18*s,0.28*s),ear_c); RB((sx*0.32*s,-0.56*s,1.72*s),(0.16*s,0.08*s,0.16*s),"pink")
    elif ear == "point":
        for sx in (-1,1): RK(0.16*s,0.4*s,(sx*0.3*s,-0.45*s,1.8*s),ear_c,(rad(-10),rad(sx*15),0)); RK(0.09*s,0.26*s,(sx*0.3*s,-0.5*s,1.78*s),"pink",(rad(-10),rad(sx*15),0))
    elif ear == "floppy":
        for sx in (-1,1): RB((sx*0.45*s,-0.5*s,1.45*s),(0.2*s,0.3*s,0.45*s),ear_c)
    if snout: RB((0,-0.98*s,1.15*s),(0.5*s,0.35*s,0.38*s),snout[0]); RB((0,-1.17*s,1.25*s),(0.16*s,0.1*s,0.11*s),snout[1] if len(snout)>1 else "black")
    if tail == "short": RB((0,0.82*s,1.0*s),(0.22*s,0.22*s,0.22*s),body_c)
    elif tail == "long": t=RC(0.06*s,0.8*s,(0.25*s,0.75*s,1.05*s),body_c,(rad(-55),0,rad(-25))); RB((0.42*s,1.0*s,1.4*s),(0.18*s,0.18*s,0.18*s),belly_c)
    elif tail == "bushy": RB((0.15*s,0.9*s,1.05*s),(0.35*s,0.7*s,0.35*s),body_c,rot=(rad(-35),0,0)); RB((0.22*s,1.15*s,1.3*s),(0.22*s,0.25*s,0.22*s),belly_c)
    if spots:
        for (x,y,z) in [(-0.3,0.1,1.05),(0.35,0.3,0.95),(0.1,-0.1,1.15),(-0.25,0.5,0.8),(0.3,-0.25,1.0)]: RB((x*s,y*s,z*s),(0.14*s,0.14*s,0.07*s),spots,lv=1)
    for (x,y) in [(-0.3,-0.4),(0.3,-0.4),(-0.3,0.45),(0.3,0.45)]: RB((x*s,y*s,leg_h*s/2),(0.26*s,0.26*s,leg_h*s),legs_c); RB((x*s,y*s-0.03,0.12*s),(0.3*s,0.36*s,0.18*s),legs_c)
    face(1.4*s,-1.0*s,0.18*s,0.1*s,mouth_dz=(0.3 if snout else 0.2)*s,mr=0.09*s)
    return {"head":head}
def b_lion():
    h = quad_s("tan","cream",ear="round",tail="long",snout=("cream","dkbrown"),legs_c="tan")
    sub(To(0.52,0.26,(0,-0.3,1.3),"brown",(R90,0,0)),1)
    for k in range(12): a=k*TAU/12; RB((0.6*math.cos(a),-0.25,1.3+0.6*math.sin(a)),(0.3,0.25,0.3),"brown",rot=(0,-a,0),lv=1)
    RB((0.45,1.05,1.45),(0.22,0.22,0.22),"brown"); return h
def b_wolf():
    h = quad_s((0.45,0.55,0.68),"white",ear="point",tail="bushy",snout=((0.45,0.55,0.68),"black"),legs_c=(0.35,0.42,0.55))
    RB((0,-1.1,1.2),(0.4,0.3,0.3),"white"); return h
def b_deer():
    h = quad_s((0.7,0.45,0.2),"cream",ear="floppy",tail="short",spots="cream",snout=((0.7,0.45,0.2),"black"),leg_h=0.5,size=0.95)
    for sx in (-1,1):
        RC(0.035,0.55,(sx*0.22,-0.45,1.95),"dkbrown",(0,rad(sx*12),0),lv=1)
        RC(0.03,0.28,(sx*0.3,-0.45,2.0),"dkbrown",(0,rad(sx*-50),0),lv=1); RC(0.03,0.25,(sx*0.36,-0.45,2.18),"dkbrown",(0,rad(sx*-40),0),lv=1)
    return h
def b_bear():
    return quad_s("brown","tan",ear="round",tail="short",snout=("beige","black"),legs_c="brown")
def b_pig():
    h = quad_s("pink","peach",ear="floppy",tail="short")
    RC(0.2,0.12,(0,-1.1,1.25),"hotpink",(R90,0,0),lv=1)
    for sx in (-1,1): RB((sx*0.07,-1.17,1.25),(0.05,0.03,0.07),"mouth",lv=1)
    sub(To(0.1,0.03,(0,0.85,1.1),"pink",(0,R90,0)),1); return h
def b_swan():
    RB((0,0.15,0.55),(0.9,1.6,0.7),"white")
    for sx in (-1,1): RB((sx*0.42,0.2,0.75),(0.3,1.1,0.45),"white",rot=(0,0,rad(sx*-10)))
    RB((0,0.9,0.85),(0.3,0.5,0.4),"white",rot=(rad(-35),0,0))
    for (y,z,sz) in [(-0.45,0.7,0.36),(-0.62,0.95,0.34),(-0.72,1.22,0.32),(-0.72,1.5,0.3),(-0.64,1.75,0.3)]: RB((0,y,z),(sz,sz,sz*1.25),"white")
    RB((0,-0.6,2.0),(0.46,0.55,0.42),"white"); RK(0.1,0.4,(0,-1.0,1.92),"orange",(R90,0,0),lv=1); RB((0,-0.82,1.95),(0.3,0.12,0.2),"black",lv=1)
    face(2.05,-0.84,0.1,0.065,mouth_dz=0.5,mr=0.0,tongue=False); return {"sway":3,"yawaxis":1}
def b_book():
    for sx in (-1,1):
        RB((sx*0.62,0,0.25),(1.2,1.6,0.08),"navy",rot=(0,rad(sx*-12),0),lv=1); RB((sx*0.6,0,0.33),(1.1,1.5,0.1),"cream",rot=(0,rad(sx*-12),0),lv=1)
        for k in range(5): RB((sx*0.6,-0.5+k*0.25,0.41+0.0),(0.8,0.04,0.015),"grey",rot=(0,rad(sx*-12),0),lv=0)
    RB((0,0,0.22),(0.3,1.62,0.14),"navy",lv=1)
    face(0.45,-0.82,0.2,0.1,x=0.0,mouth_dz=0.22,mr=0.1); return {}
def b_cup():
    RC(0.5,1.0,(0,0,0.5),"sky",lv=2); Cy(0.44,0.08,(0,0,0.96),"chocolate",verts=32); sub(To(0.28,0.07,(0.55,0,0.55),"sky",(R90,0,0)),1)
    for k in range(3): RB((-0.2+k*0.2,0,1.3+0.1*k),(0.06,0.06,0.35),"white",rot=(0,rad(15-15*k),0),lv=2)
    face(0.65,-0.48,0.2,0.1,mouth_dz=0.28,mr=0.1); return {}
def b_web():
    for k in range(8): sub(Cy(0.045,2.0,(0,0,1.05),"silver",(0,k*math.pi/8,0),verts=10),1)
    for r in (0.32,0.6,0.88): sub(To(r,0.04,(0,0,1.05),"silver",(R90,0,0)),1)
    for r in (0.46,0.74):
        for k in range(16): a=k*TAU/16; sub(Cy(0.025,0.34,(r*math.cos(a),0,1.05+r*math.sin(a)),"silver",(0,a+R90,0),verts=8),1)
    RB((0,-0.03,1.05),(0.3,0.2,0.3),"dkgrey"); 
    for sx in (-1,1):
        for k in range(4): RC(0.025,0.32,(sx*0.22,-0.02,1.0+0.05*k),"dkgrey",(0,rad(sx*(35+k*25)),0),lv=1)
    face(1.12,-0.16,0.08,0.055,mouth_dz=0.1,mr=0.05,tongue=False); return {}
def b_fire():
    g=[mat("red",0.6,1.2), mat("orange",0.6,1.8), mat("yellow",0.6,2.6)]
    for k in range(3): a=k*TAU/3+0.4; RC(0.17,1.5,(0.22*math.cos(a),0.22*math.sin(a),0.17),"brown",(R90*0.96,0,a),lv=1)
    for i,(r,hh,x,y,z) in enumerate([(0.52,1.5,0,0.08,0.98),(0.38,1.1,0,-0.2,0.8),(0.22,0.75,0,-0.4,0.62)]):
        o=RK(r,hh,(x,y,z),"red",lv=2); o.data.materials[0]=g[i]
    for (x,y,z,r,hh,gi) in [(-0.42,0.0,0.7,0.2,0.7,0),(0.45,0.05,0.75,0.22,0.8,0),(-0.25,-0.3,0.55,0.13,0.45,1),(0.28,-0.32,0.5,0.12,0.42,1),(0.1,0.3,0.9,0.14,0.6,1)]:
        o=RK(r,hh,(x,y,z),"orange",lv=2); o.data.materials[0]=g[gi]
    for k in range(5): o=RB((0.4*math.cos(k*1.3),0.4*math.sin(k*1.3)-0.1,1.5+0.2*k),(0.08,0.08,0.11),"orange",lv=1); o.data.materials[0]=g[2]
    face(1.0,-0.5,0.14,0.08,mouth_dz=0.22,mr=0.08); return {"glow":g}
def b_ice():
    m=mat((0.55,0.8,1.0),0.1); m.blend_method='BLEND'
    try: m.surface_render_method='BLENDED'
    except Exception: pass
    b=m.node_tree.nodes["Principled BSDF"]; b.inputs["Alpha"].default_value=0.62
    if "Transmission Weight" in b.inputs: b.inputs["Transmission Weight"].default_value=0.3
    o=B((0,0,0.75),(1.5,1.5,1.5),"sky",bevel=0.3); o.modifiers["Bevel"].segments=8; o.data.materials[0]=m
    for (x,z) in [(-0.45,1.2),(0.5,0.4),(0.1,1.35)]: Fp(starpts(0.12,0.04,4),(x,-0.78,z),0.02,"white")
    face(0.95,-0.76,0.25,0.12,mouth_dz=0.32,mr=0.13); return {}
def b_egg():
    o=S(0.72,(0,0,0.8),(0.88,0.88,1.12),"cream"); m=o.modifiers.new("Sub",'SUBSURF'); m.levels=2
    for (x,y,z,c) in [(-0.3,-0.55,1.15,"sky"),(0.35,-0.5,0.7,"pink"),(0.05,-0.6,1.4,"lime"),(-0.4,-0.4,0.55,"lavender"),(0.45,-0.35,1.2,"gold")]: S(0.09,(x,y,z),(1,0.5,1),c)
    face(1.0,-0.62,0.26,0.15,mouth_dz=0.36,mr=0.15); return {}
def b_map():
    RB((0,0,1.0),(1.9,0.08,1.4),"beige",lv=1)
    for sx in (-1,1): RC(0.14,1.7,(sx*0.98,0,1.0),"straw",lv=1); S(0.16,(sx*0.98,0,1.88),(1,1,0.6),"wood"); S(0.16,(sx*0.98,0,0.12),(1,1,0.6),"wood")
    RB((-0.35,-0.06,0.8),(0.6,0.02,0.4),"green",lv=1); RB((0.35,-0.06,1.3),(0.5,0.02,0.3),"sky",lv=1); RB((0.0,-0.06,0.55),(0.7,0.02,0.18),"sky",lv=1)
    for k in range(7): B((-0.55+k*0.16,-0.07,1.05+0.08*math.sin(k*1.1)),(0.07,0.02,0.04),"dkgrey",rot=(0,rad(20*math.cos(k)),0))
    B((0.55,-0.08,1.0),(0.05,0.02,0.3),"red",rot=(0,rad(45),0)); B((0.55,-0.08,1.0),(0.05,0.02,0.3),"red",rot=(0,rad(-45),0))
    face(1.45,-0.07,0.25,0.11,x=-0.1,mouth_dz=0.0,mr=0.0,tongue=False); smile(1.2,-0.08,0.1,x=-0.1,tongue=False); return {}
def b_boat():
    RB((0,0,0.42),(1.1,2.2,0.6),"red",lv=2); RB((0,0,0.62),(0.9,1.9,0.12),"cream",lv=1)
    RC(0.05,2.0,(0,0.1,1.6),"wood",lv=1); RC(0.04,1.1,(0,-0.1,2.5),"wood",(R90,0,0),lv=1)
    sail=Fp([(0,0),(0,1.55),(-1.0,0.1)],(0.06,0.1,0.75),0.04,"white"); m=sail.modifiers.new("Sub",'SUBSURF'); m.levels=1
    s2=Fp([(0,0),(0,0.9),(0.65,0.05)],(-0.06,0.1,0.75),0.04,"sky"); m=s2.modifiers.new("Sub",'SUBSURF'); m.levels=1
    Fp([(0,0),(0.4,0.12),(0,0.25)],(0,0.1,2.55),0.03,"red")
    face(0.45,-1.05,0.2,0.1,mouth_dz=0.25,mr=0.1); return {"sway":6,"yawaxis":1}
def b_leaf():
    o=S(0.9,(0,0,1.0),(0.7,0.18,1.0),"green"); m=o.modifiers.new("Sub",'SUBSURF'); m.levels=2
    RC(0.04,2.1,(0,-0.17,1.0),"dkgreen",lv=1); RC(0.05,0.5,(0,0,0.1),"dkgreen",lv=1)
    for k in range(4):
        for sx in (-1,1): RC(0.022,0.55,(sx*0.2,-0.18,1.45-k*0.32),"dkgreen",(0,rad(sx*55),0),lv=1)
    face(1.25,-0.22,0.17,0.1,mouth_dz=0.24,mr=0.1); return {}
def b_snow():
    g=mat((0.85,0.95,1.0),0.4,0.35)
    for k in range(3):
        o=RC(0.07,2.2,(0,0,1.1),"white",(0,k*math.pi/3,0),lv=1); o.data.materials[0]=g
    for k in range(6):
        a=k*math.pi/3
        for d in (0.5,0.85):
            for sgn in (-1,1):
                o=RC(0.045,0.42,(d*math.cos(a),0,1.1+d*math.sin(a)),"white",(0,-a+sgn*rad(55),0),lv=1); o.data.materials[0]=g
        o=S(0.09,(1.1*math.cos(a),0,1.1+1.1*math.sin(a)),(1,1,1),"white"); o.data.materials[0]=g
    o=S(0.28,(0,0,1.1),(1,0.5,1),"sky"); m=o.modifiers.new("Sub",'SUBSURF'); m.levels=1
    face(1.16,-0.14,0.1,0.07,mouth_dz=0.15,mr=0.07,tongue=False); return {}
def b_ring():
    o=To(0.7,0.16,(0,0,0.85),"gold",(R90,0,0)); m=o.modifiers.new("Sub",'SUBSURF'); m.levels=1
    Co(0.3,0.26,(0,0,1.85),"glass",(0,0,0),None,0.0,8); Co(0.3,0.3,(0,0,1.55),"glass",(math.radians(180),0,0),None,0.0,8); Cy(0.3,0.04,(0,0,1.7),"glass",verts=8)
    for k in range(4): a=k*math.pi/2+math.pi/4; RC(0.03,0.4,(0.26*math.cos(a),0.26*math.sin(a),1.7),"gold",(rad(20)*math.sin(a),rad(-20)*math.cos(a),0),lv=1)
    RB((0,0,1.5),(0.5,0.5,0.2),"gold",lv=1)
    face(0.3,-0.17,0.14,0.08,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.1,-0.17,0.08,tongue=False); return {}
def b_athlete():
    RB((0,0,1.0),(0.7,0.45,0.8),"red"); RB((0,0,0.55),(0.65,0.42,0.35),"navy"); S(0.36,(0,0,1.7),(1,0.95,1),"peach"); S(0.38,(0,0.08,1.85),(1,1,0.7),"dkbrown")
    RB((0,-0.05,1.85),(0.8,0.75,0.1),"red",lv=1)
    for sx in (-1,1): RC(0.09,0.5,(sx*0.42,0,0.95),"peach",(0,rad(sx*-25),0)); S(0.1,(sx*0.55,0,0.7),(1,1,1),"peach"); RC(0.11,0.4,(sx*0.18,0,0.18),"peach"); RB((sx*0.18,-0.06,0.07),(0.26,0.4,0.14),"white",lv=1)
    face(1.72,-0.35,0.13,0.08,mouth_dz=0.22,mr=0.08); return {}
def b_banana():
    for k in range(9):
        a=-0.9+k*0.225; RB((1.1*math.sin(a),0,1.0-1.1*math.cos(a)+1.05),(0.32,0.3,0.3),"yellow",rot=(0,-a,0))
    RB((1.1*math.sin(-1.05),0,1.0-1.1*math.cos(-1.05)+1.05),(0.2,0.18,0.3),"dkbrown",rot=(0,1.05,0),lv=1); RB((1.1*math.sin(1.05),0,1.0-1.1*math.cos(1.05)+1.05),(0.2,0.18,0.3),"dkbrown",rot=(0,-1.05,0),lv=1)
    face(1.05,-0.17,0.15,0.09,mouth_dz=0.22,mr=0.09); return {}
def b_cherry():
    for sx in (-1,1):
        o=S(0.42,(sx*0.42,0,0.45),(1,1,0.95),"red"); m=o.modifiers.new("Sub",'SUBSURF'); m.levels=1
        RC(0.03,1.2,(sx*0.2,0,1.3),"dkgreen",(0,rad(sx*-20),0),lv=1)
    S(0.3,(0.1,0,1.95),(1.3,0.3,0.55),"green",rot=(0,rad(35),0))
    face(0.6,-0.4,0.12,0.08,x=-0.42,mouth_dz=0.2,mr=0.07,tongue=False); face(0.6,-0.4,0.12,0.08,x=0.42,mouth_dz=0.2,mr=0.07,tongue=False); return {}
def b_spider():
    o=S(0.45,(0,0.15,0.75),(1,1.1,0.85),"purple"); m=o.modifiers.new("Sub",'SUBSURF'); m.levels=1; S(0.3,(0,-0.45,0.75),(1,1,1),"purple")
    for sx in (-1,1):
        for k in range(4):
            y=-0.3+k*0.25; p=E((sx*0.2,y,0.75)); RC(0.04,0.7,(sx*0.5,y,0.85),"purple",(0,rad(-sx*65),0),p,lv=1); RC(0.035,0.6,(sx*0.85,y,0.4),"purple",(0,rad(sx*15),0),p,lv=1)
    face(0.85,-0.72,0.12,0.08,mouth_dz=0.2,mr=0.08); eyes(1.0,-0.68,0.26,0.05); return {}
def b_mountain():
    RK(1.2,2.0,(0,0,1.0),"grey",lv=2); RK(0.9,1.3,(-0.9,0.3,0.65),"grey",lv=2); RK(0.8,1.1,(0.95,0.2,0.55),"grey",lv=2)
    RK(0.42,0.6,(0,0,1.75),"white",lv=2); RK(0.3,0.42,(-0.9,0.3,1.12),"white",lv=2)
    for (x,y) in [(-0.5,-0.9),(0.6,-0.8),(1.3,-0.4)]: RC(0.05,0.3,(x,y,0.15),"brown",lv=1); RK(0.18,0.45,(x,y,0.45),"dkgreen",lv=1)
    face(1.1,-0.65,0.17,0.09,mouth_dz=0.24,mr=0.09); return {}
def b_pirate():
    RB((0,0,1.0),(0.75,0.5,0.8),"red"); RB((0,0,0.52),(0.7,0.45,0.35),"navy"); S(0.36,(0,0,1.7),(1,0.95,1),"peach")
    RB((0,0,2.0),(1.0,0.95,0.14),"black",lv=1); RB((0,0,2.18),(0.7,0.65,0.3),"black",lv=1); Fp(starpts(0.1,0.04,5),(0,-0.34,2.2),0.02,"white")
    RB((0.14,-0.33,1.76),(0.24,0.04,0.2),"black",lv=1); B((0,-0.3,1.86),(0.75,0.03,0.04),"black",rot=(0,rad(-12),0))
    for k in range(3): B((0,-0.26,1.05-k*0.25),(0.75,0.02,0.08),"white")
    for sx in (-1,1): RC(0.09,0.5,(sx*0.45,0,0.95),"peach",(0,rad(sx*-20),0)); S(0.1,(sx*0.55,0,0.7),(1,1,1),"peach"); RC(0.11,0.4,(sx*0.18,0,0.18),"navy"); RB((sx*0.18,-0.06,0.07),(0.26,0.4,0.14),"dkbrown",lv=1)
    eyes(1.74,-0.35,0.13,0.08); smile(1.5,-0.36,0.09); return {}
def b_flamingo():
    RB((0,0.1,1.35),(0.75,1.0,0.6),"hotpink"); RB((0,0.5,1.5),(0.35,0.5,0.35),"hotpink",rot=(rad(-30),0,0))
    for (y,z,sz) in [(-0.4,1.45,0.22),(-0.5,1.75,0.2),(-0.5,2.05,0.2),(-0.42,2.3,0.2)]: RB((0,y,z),(sz,sz,sz*1.2),"hotpink")
    RB((0,-0.5,2.5),(0.38,0.42,0.34),"hotpink"); bk=Co(0.08,0.4,(0,-0.82,2.42),"black",(rad(110),0,0),None,0.03,12); m=bk.modifiers.new("Sub",'SUBSURF'); m.levels=1; S(0.11,(0,-0.7,2.45),(1,0.8,0.8),"pink")
    for sx in (-1,1): RC(0.035,1.2,(sx*0.12,0,0.6),"pink",lv=1); RB((sx*0.12,-0.1,0.05),(0.22,0.3,0.08),"pink",lv=1)
    eyes(2.56,-0.78,0.1,0.06); return {}
def b_camel():
    RB((0,0.1,1.0),(0.95,1.5,0.8),"tan"); RB((0,-0.05,1.45),(0.55,0.5,0.45),"tan"); RB((0,0.45,1.45),(0.5,0.45,0.42),"tan")
    for (y,z,sz) in [(-0.7,1.3,0.3),(-0.82,1.65,0.28)]: RB((0,y,z),(sz,sz,sz*1.3),"tan")
    RB((0,-0.85,2.05),(0.55,0.75,0.45),"tan"); RB((0,-1.15,1.95),(0.3,0.25,0.25),"beige")
    for sx in (-1,1): RB((sx*0.26,-0.75,2.35),(0.14,0.12,0.2),"tan"); RB((sx*0.3,-0.45,0.4),(0.26,0.26,0.8),"brown"); RB((sx*0.3,0.5,0.4),(0.26,0.26,0.8),"brown")
    RB((0,0.95,1.1),(0.1,0.3,0.1),"brown"); S(0.07,(0,-1.3,2.0),(1.2,0.8,0.7),"black")
    face(2.12,-1.12,0.16,0.09,mouth_dz=0.3,mr=0.08); return {}
def b_planet():
    o=S(0.75,(0,0,1.0),(1,1,1),"sky"); m=o.modifiers.new("Sub",'SUBSURF'); m.levels=1
    for (x,y,z,r) in [(-0.3,-0.55,1.3,0.25),(0.4,-0.5,0.8,0.2),(0.1,-0.7,1.05,0.15),(-0.5,-0.3,0.7,0.18)]: S(r,(x,y,z),(1,0.5,1),"green")
    t=To(1.15,0.08,(0,0,1.0),"gold",(rad(20),rad(10),0)); m=t.modifiers.new("Sub",'SUBSURF'); m.levels=1
    face(1.15,-0.62,0.2,0.1,mouth_dz=0.28,mr=0.1); return {}
def b_eagle():
    RB((0,0.05,1.0),(0.8,1.1,0.9),"brown"); RB((0,-0.35,1.6),(0.6,0.6,0.55),"white"); bk=Co(0.1,0.35,(0,-0.72,1.52),"gold",(rad(100),0,0),None,0.03,12); mm=bk.modifiers.new("Sub",'SUBSURF'); mm.levels=1
    wings=[]
    for sx in (-1,1):
        p=E((sx*0.35,0.05,1.15)); wings.append(p)
        for (dx,dz,sc) in [(0.5,0.1,(1.0,0.5,0.22)),(1.1,0.2,(0.9,0.45,0.18))]: RB((sx*(0.35+dx),0.05,1.15+dz),sc,"brown",p,rot=(0,rad(sx*-8),0))
    for k in range(3): RB((0.15*(k-1),0.65,0.85),(0.18,0.5,0.1),"white",rot=(0,0,rad((k-1)*15)))
    for sx in (-1,1): RC(0.04,0.4,(sx*0.18,-0.1,0.25),"gold",lv=1); RB((sx*0.18,-0.2,0.05),(0.2,0.3,0.08),"gold",lv=1)
    face(1.68,-0.6,0.13,0.08,mouth_dz=0.0,mr=0.0,tongue=False); return {"wings":wings,"flap":30}
def b_dolphin():
    RB((0,0,1.0),(0.7,2.0,0.75),"sky"); RB((0,-0.1,0.85),(0.5,1.6,0.45),"white"); RB((0,-1.15,0.95),(0.3,0.5,0.28),"sky")
    RB((0,0.1,1.45),(0.1,0.5,0.4),"sky",rot=(rad(-25),0,0))
    for sx in (-1,1): RB((sx*0.4,-0.2,0.75),(0.45,0.3,0.08),"sky",rot=(0,rad(sx*25),0))
    for sx in (-1,1): RB((sx*0.25,1.15,1.05),(0.5,0.3,0.08),"sky",rot=(0,0,rad(sx*30)))
    face(1.15,-0.95,0.14,0.08,mouth_dz=0.25,mr=0.0,tongue=False); smile(0.8,-1.38,0.12,tongue=False); return {"sway":5,"yawaxis":1}
def b_house():
    RB((0,0,0.8),(1.6,1.4,1.6),"cream",lv=1); Fp([(-1.0,0),(1.0,0),(0,0.9)],(0,0,1.55),1.7,"red"); RB((0.5,0.3,2.3),(0.25,0.25,0.5),"brown",lv=1)
    RB((0,-0.72,0.45),(0.4,0.06,0.8),"brown",lv=1); S(0.04,(0.12,-0.76,0.45),(1,1,1),"gold")
    for sx in (-1,1): RB((sx*0.5,-0.72,1.15),(0.4,0.06,0.4),"sky",lv=1); B((sx*0.5,-0.76,1.15),(0.42,0.02,0.04),"white"); B((sx*0.5,-0.76,1.15),(0.04,0.02,0.42),"white")
    face(1.95,-0.5,0.16,0.09,mouth_dz=0.0,mr=0.0,tongue=False); smile(1.72,-0.53,0.09,tongue=False); return {}
def b_tornado():
    for k in range(8):
        r=0.15+k*0.12; z=0.15+k*0.26
        o=To(r,0.1+k*0.015,(0.08*math.sin(k*0.9),0.08*math.cos(k*0.9),z),"lgrey",scale=(1,1,1)); mm=o.modifiers.new("Sub",'SUBSURF'); mm.levels=1
    for k in range(6): S(0.06,(1.1*math.cos(k*1.1),0.3*math.sin(k*1.1),0.6+k*0.3),(1,1,1),"grey")
    face(1.5,-0.95,0.17,0.09,mouth_dz=0.25,mr=0.09); return {}
def b_lemon():
    o=S(0.62,(0,0,0.75),(1.0,0.75,0.78),(1.0,0.92,0.12)); m=o.modifiers.new("Sub",'SUBSURF'); m.levels=2
    RK(0.14,0.3,(-0.68,0,0.75),"yellow",(0,rad(-90),0),lv=1); RK(0.14,0.3,(0.68,0,0.75),"yellow",(0,rad(90),0),lv=1)
    RC(0.03,0.25,(0.55,0,1.15),"dkgreen",(0,rad(30),0),lv=1); S(0.22,(0.75,0,1.3),(1.3,0.3,0.6),"green",rot=(0,rad(-30),0))
    face(0.9,-0.52,0.2,0.11,mouth_dz=0.3,mr=0.11); return {}
def b_grape():
    pos=[(0,0,1.9),(-0.3,-0.2,1.7),(0.3,-0.2,1.7),(0,0.3,1.65),(-0.45,0.1,1.4),(0.45,0.1,1.4),(0,-0.35,1.4),(-0.15,0.35,1.3),(-0.3,-0.25,1.1),(0.3,-0.25,1.1),(0,0.2,1.05),(-0.15,-0.1,0.8),(0.15,-0.1,0.8),(0,0.15,0.55),(0,-0.1,0.32)]
    for i,(x,y,z) in enumerate(pos):
        o=S(0.27,(x,y,z),(1,1,1),"purple" if i%3 else (0.62,0.3,0.85)); m=o.modifiers.new("Sub",'SUBSURF'); m.levels=1
    RC(0.04,0.45,(0,0,2.25),"brown",lv=1); S(0.3,(0.35,0,2.3),(1.4,0.3,0.7),"green",rot=(0,rad(-25),0))
    face(1.72,-0.45,0.2,0.11,mouth_dz=0.3,mr=0.1); return {}
def b_train():
    body=E((0,0,0)); wheels=[]
    RC(0.5,1.6,(0,-0.1,0.95),"red",(R90,0,0),body,lv=2); RB((0,0.9,1.15),(1.0,0.9,1.3),"blue",body,lv=1); RB((0,0.9,1.85),(1.15,1.05,0.12),"red",body,lv=1)
    RC(0.18,0.6,(0,-0.55,1.7),"navy",parent=body,lv=1); RC(0.26,0.12,(0,-0.55,2.0),"gold",parent=body,lv=1); RB((0,0.1,1.5),(0.3,0.3,0.2),"gold",body,lv=1)
    RB((0,-0.1,0.45),(1.3,1.9,0.3),"navy",body,lv=1); Fp([(-0.7,0),(0.7,0),(0,0.45)],(0,-1.15,0.1),0.5,"red",body)
    for sx in (-1,1): RB((sx*0.52,0.95,1.3),(0.04,0.4,0.4),"sky",body,lv=1)
    RB((0,0.38,1.3),(0.6,0.04,0.4),"sky",body,lv=1); RC(0.44,0.06,(0,-0.92,0.95),"gold",(R90,0,0),body,lv=1); S(0.14,(0,-0.98,1.3),(1,0.5,1),"gold",parent=body)
    for sx in (-1,1):
        for (y,r) in ((-0.6,0.28),(0.1,0.28),(0.8,0.34)):
            w=E((sx*0.6,y,r)); Cy(r,0.14,(sx*0.6,y,r),"gold",(0,R90,0),w,verts=24); Cy(r*0.6,0.16,(sx*0.6,y,r),"red",(0,R90,0),w,verts=12)
            for k in range(3): B((sx*0.6+sx*0.09,y+r*0.5*math.cos(k*2.1),r+r*0.5*math.sin(k*2.1)),(0.02,0.06,0.06),"dkgrey",w,(k*2.1,0,0))
            wheels.append(w)
    face(1.1,-0.96,0.22,0.12,parent=body,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.75,-0.98,0.12,parent=body)
    return {"body":body,"wheels":wheels}
def b_crab():
    o=S(0.9,(0,0,0.7),(1.3,0.9,0.65),"red"); m=o.modifiers.new("Sub",'SUBSURF'); m.levels=1; claws=[]
    for sx in (-1,1):
        RC(0.05,0.55,(sx*0.4,-0.45,1.3),"red",(0,rad(sx*10),0),lv=1);
        p=E((sx*0.85,-0.4,0.75)); RC(0.1,0.6,(sx*1.0,-0.6,0.85),"red",(0,rad(-sx*55),0),p,lv=1); RB((sx*1.3,-0.85,1.0),(0.55,0.75,0.45),"red",p); RB((sx*1.28,-1.2,1.1),(0.35,0.4,0.25),"red",p); claws.append(p)
        for k in range(3): RC(0.07,0.8,(sx*1.0,0.1+k*0.25,0.4),"red",(0,rad(-sx*55),0),lv=1)
    eyes(1.6,-0.45,0.4,0.16); smile(0.65,-0.85,0.26,tongue=False); return {"claws":claws,"sway":4,"yawaxis":1}
def b_snow():
    g=mat((0.75,0.9,1.0),0.4,0.5)
    for k in range(3):
        o=RC(0.11,2.3,(0,0,1.15),"white",(0,k*math.pi/3,0),lv=1); o.data.materials[0]=g
    for k in range(6):
        a=k*math.pi/3
        for d in (0.5,0.85):
            for sgn in (-1,1):
                o=RC(0.07,0.5,(d*math.cos(a),0,1.15+d*math.sin(a)),"white",(0,-a+sgn*rad(55),0),lv=1); o.data.materials[0]=g
        o=S(0.14,(1.15*math.cos(a),0,1.15+1.15*math.sin(a)),(1,1,1),"white"); o.data.materials[0]=g
    o=S(0.38,(0,0,1.15),(1,0.6,1),"sky"); m=o.modifiers.new("Sub",'SUBSURF'); m.levels=1
    face(1.22,-0.2,0.14,0.09,mouth_dz=0.2,mr=0.09,tongue=False); return {}
def b_truck():
    body=E((0,0,0)); wheels=[]
    RB((0,-0.95,1.0),(1.5,1.1,1.0),"blue",body,lv=1); RB((0,0.55,1.1),(1.55,2.0,1.3),"orange",body,lv=1); RB((0,-0.2,0.45),(1.6,3.0,0.35),"dkgrey",body,lv=1)
    RB((0,-1.5,1.15),(1.2,0.06,0.5),"glass",body,lv=1)
    for sx in (-1,1): RB((sx*0.76,-0.95,1.15),(0.06,0.6,0.45),"glass",body,lv=1); S(0.14,(sx*0.5,-1.52,0.75),(1,0.5,1),"cream",parent=body)
    RB((0,-1.55,0.5),(1.4,0.12,0.18),"grey",body,lv=1); Fp(starpts(0.25,0.1),(0,-0.46,1.2),0.03,"yellow",body); RB((0.5,0.3,1.2),(0.9,0.04,0.4),"white",body,lv=1)
    for sx in (-1,1):
        for y in (-0.95,0.5,1.2):
            w=E((sx*0.8,y,0.38)); Cy(0.38,0.3,(sx*0.8,y,0.38),"black",(0,R90,0),w); Cy(0.2,0.32,(sx*0.8,y,0.38),"lgrey",(0,R90,0),w,verts=16)
            for k in range(3): B((sx*0.8+sx*0.17,y+0.12*math.cos(k*2.1),0.38+0.12*math.sin(k*2.1)),(0.02,0.06,0.06),"dkgrey",w,(k*2.1,0,0));
            wheels.append(w)
    face(1.2,-1.53,0.3,0.14,parent=body,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.95,-1.56,0.14,parent=body); return {"body":body,"wheels":wheels}
def b_helicopter():
    RB((0,-0.1,1.1),(1.3,2.0,1.1),"red",lv=2); RB((0,-0.95,1.15),(1.0,0.7,0.75),"glass",lv=2); RB((0,1.3,1.25),(0.3,1.6,0.3),"red",lv=2); RB((0,2.1,1.55),(0.08,0.5,0.6),"blue",lv=1)
    for sx in (-1,1): RC(0.05,1.6,(sx*0.45,-0.1,0.25),"grey",(R90,0,0),lv=1); RC(0.04,0.5,(sx*0.45,-0.3,0.5),"grey",(rad(20),0,0),lv=1)
    RC(0.08,0.4,(0,-0.1,1.85),"grey",lv=1); rotor=E((0,-0.1,2.05)); RB((0,-0.1,2.05),(3.0,0.16,0.04),"dkgrey",rotor,lv=0); RB((0,-0.1,2.05),(0.16,3.0,0.04),"dkgrey",rotor,lv=0); S(0.1,(0,-0.1,2.08),(1,1,1),"gold",parent=rotor)
    tr=E((0.12,2.1,1.55)); RB((0.12,2.1,1.55),(0.04,0.5,0.1),"dkgrey",tr,lv=0); RB((0.12,2.1,1.55),(0.04,0.1,0.5),"dkgrey",tr,lv=0)
    face(1.3,-1.3,0.2,0.12,mouth_dz=0.32,mr=0.12); return {"rotor":rotor,"tailrotor":tr,"wings":[]}
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}
