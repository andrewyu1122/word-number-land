# character recipes; all face -Y, stand on z=0. Each returns a handles dict for the action curves.
def quad(body_c, belly_c, head_c=None, size=1.0, ear="round", ear_c=None, snout=None, tail="short", spots=None, horns=None, legs_c=None, foot=None, head_r=0.38):
    hc = head_c or body_c; ear_c = ear_c or body_c; legs_c = legs_c or body_c
    S(0.42*size, (0,0.05,0.55*size), (1,1.3,0.9), body_c)
    S(0.3*size, (0,-0.1,0.45*size), (0.9,1.1,0.7), belly_c)
    head = S(head_r*size, (0,-0.45,1.0*size), (1,1,0.9), hc)
    if ear == "round":
        for sx in (-1,1): S(0.13*size, (sx*0.28*size,-0.4,1.3*size), (1,0.6,1), ear_c); S(0.07*size, (sx*0.28*size,-0.46,1.3*size), (1,0.5,1), "pink")
    elif ear == "point":
        for sx in (-1,1): Co(0.14*size,0.32*size,(sx*0.25*size,-0.4,1.36*size),ear_c,(rad(-10),rad(sx*15),0)); Co(0.08*size,0.2*size,(sx*0.24*size,-0.45,1.34*size),"pink",(rad(-10),rad(sx*15),0))
    elif ear == "floppy":
        for sx in (-1,1): S(0.12*size, (sx*0.36*size,-0.4,1.05*size), (0.5,0.8,1.3), ear_c)
    if snout: S(snout[0]*size, (0,-0.75*size,0.9*size), (1.1,0.9,0.8), snout[1]); S(0.07*size, (0,-0.95*size,0.98*size), (1.2,0.8,0.7), snout[2] if len(snout)>2 else "black")
    if tail == "short": S(0.1*size,(0,0.6*size,0.85*size),(1,1,1),body_c)
    elif tail == "long": Cy(0.05*size,0.7*size,(0.2,0.55,0.75*size),body_c,(rad(-60),0,rad(-20))); S(0.07*size,(0.3,0.75,1.05*size),(1,1,1),body_c)
    elif tail == "bushy": S(0.18*size,(0.15,0.7*size,0.8*size),(0.8,1.6,0.8),body_c,rot=(rad(-40),0,0)); S(0.1*size,(0.2,0.95*size,1.05*size),(1,1,1),belly_c)
    if spots:
        for (x,y,z) in [(-0.25,0.1,0.85),(0.3,0.25,0.75),(0.1,-0.15,0.9),(-0.2,0.45,0.6)]: S(0.14*size,(x,y,z*size),(1,1,0.5),spots)
    if horns:
        for sx in (-1,1): Co(0.06*size,0.3*size,(sx*0.25*size,-0.35,1.4*size),horns,(rad(-20),rad(sx*25),0))
    legs4(legs_c, 0, 0.3*size, 0.09*size, 0.22*size, 0.28*size, foot=foot)
    face(1.08*size, -0.78*size, 0.16*size, 0.1*size, mouth_dz=(0.26 if snout else 0.17)*size, mr=0.09*size)
    return {"head": head}
def b_cat():
    h = quad("grey","lgrey",ear="point",tail="long",snout=None); S(0.06,(0,-0.8,0.93),(1.2,0.8,0.7),"pink")
    for sx in (-1,1):
        for k in (-1,0,1): Cy(0.008,0.4,(sx*0.3,-0.78,0.9+0.04*k),"white",(0,R90,rad(k*8)))
    return h
def b_pig():
    h = quad("pink","peach",ear="floppy",tail="short"); Cy(0.14,0.1,(0,-0.85,0.95),"hotpink",(R90,0,0))
    for sx in (-1,1): S(0.03,(sx*0.05,-0.91,0.95),(1,1,1.3),"mouth")
    To(0.07,0.025,(0,0.62,0.9),"pink",(0,R90,0)); return h
def b_cow():
    h = quad("white","cream",ear="round",tail="long",spots="black",horns="cream",snout=(0.2,"pink","pink"),foot="dkgrey")
    S(0.14,(0,0.15,0.3),(1,1,0.8),"pink"); return h
def b_hen():
    S(0.42,(0,0.05,0.6),(0.85,1.1,0.95),"brown"); S(0.3,(0,-0.45,1.1),(1,1,1),"brown")
    for k in range(3): S(0.07,(0,-0.4-k*0.1,1.42-abs(k-1)*0.03),(1,1,1.3),"red")
    S(0.08,(0,-0.72,0.93),(1,1,1.5),"red"); Co(0.07,0.2,(0,-0.8,1.05),"orange",(R90,0,0))
    for sx in (-1,1): S(0.18,(sx*0.36,0.05,0.65),(0.4,1,0.7),"chocolate")
    for k in range(3): S(0.12,(0.12*(k-1),0.5,0.85+0.1*(1-abs(k-1))),(0.5,1,1.6),"chocolate",rot=(rad(-35),0,rad(k*15-15)))
    legs2("orange",0,0.3,0.035,0.14,foot="orange"); eyes(1.15,-0.72,0.12,0.07); return {}
def b_fox():
    h = quad("orange","cream",ear="point",tail="bushy",foot="dkbrown"); Co(0.13,0.35,(0,-0.85,0.92),"cream",(R90,0,0)); S(0.06,(0,-1.02,0.93),(1,1,0.8),"black"); return h
def b_toy():  # toy robot
    body = B((0,0,0.75),(0.8,0.6,0.8),"blue",bevel=0.08); B((0,0,1.5),(0.6,0.55,0.5),"yellow",bevel=0.06)
    Cy(0.02,0.25,(0,0,1.85),"grey"); S(0.06,(0,0,1.98),(1,1,1),"red")
    for sx in (-1,1): Cy(0.07,0.5,(sx*0.5,0,0.9),"grey",(0,0,0)); S(0.1,(sx*0.5,0,0.62),(1,1,1),"red"); Cy(0.1,0.3,(sx*0.22,0,0.2),"grey"); B((sx*0.22,-0.05,0.05),(0.3,0.4,0.1),"dkgrey")
    for k in range(3): S(0.05,(0.2*(k-1),-0.31,0.85),(1,0.5,1),["red","yellow","green"][k])
    face(1.55,-0.29,0.15,0.09,mouth_dz=0.15,mr=0.1); return {}
def b_frog():
    S(0.6,(0,0,0.45),(1.1,1,0.75),"green"); S(0.42,(0,-0.15,0.35),(1,1,0.65),"cream")
    for sx in (-1,1):
        S(0.16,(sx*0.3,-0.3,0.85),(1,1,1),"green")
        p=E((sx*0.45,-0.25,0.2)); S(0.14,(sx*0.55,-0.35,0.15),(1.4,1.6,0.6),"green",p); S(0.12,(sx*0.45,0.35,0.15),(1.3,1.4,0.6),"green")
    eyes(0.9,-0.4,0.3,0.12); smile(0.5,-0.58,0.3,tongue=False); return {}
def b_ball():
    S(0.65,(0,0,0.65),(1,1,1),"red"); To(0.66,0.09,(0,0,0.65),"white",(R90,0,0),scale=(1,1,0.5)); To(0.66,0.09,(0,0,0.65),"yellow",(0,R90,0),scale=(1,1,0.5)); S(0.14,(0,0,1.3),(1,1,0.35),"blue")
    face(0.85,-0.6,0.2,0.11,mouth_dz=0.3,mr=0.14); return {}
def b_lion():
    h = quad("tan","cream",ear="round",tail="long",snout=(0.2,"cream"),foot="brown")
    To(0.45,0.2,(0,-0.3,1.0),"brown",(R90,0,0)); S(0.08,(0.35,0.95,1.2),(1,1,1.4),"brown"); return h
def b_bear():
    return quad("brown","tan",ear="round",tail="short",snout=(0.2,"tan"),foot="dkbrown")
def b_wolf():
    h = quad("grey","lgrey",ear="point",tail="bushy",foot="dkgrey"); Co(0.13,0.35,(0,-0.85,0.92),"lgrey",(R90,0,0)); S(0.06,(0,-1.02,0.93),(1,1,0.8),"black"); S(0.35,(0,0.1,0.8),(0.9,1.3,0.5),"dkgrey"); return h
def b_deer():
    h = quad("tan","cream",ear="floppy",tail="short",spots="cream",size=1.0,snout=(0.16,"tan","black"))
    for sx in (-1,1):
        Cy(0.03,0.5,(sx*0.2,-0.3,1.55),"dkbrown",(0,rad(sx*15),0))
        for k,(dz,ang) in enumerate([(0.05,-50),(0.2,-40)]): Cy(0.025,0.25,(sx*(0.3+0.08*k),-0.3,1.6+dz),"dkbrown",(0,rad(sx*ang),0))
    return h
def b_goat():
    h = quad("white","lgrey",ear="floppy",tail="short",horns="grey",snout=(0.17,"lgrey","pink"),foot="dkgrey"); Co(0.07,0.25,(0,-0.85,0.7),"lgrey",(rad(170),0,0)); return h
# ---------------- drive ----------------
def b_bus():
    body=E((0,0,0)); B((0,0,0.9),(1.4,3.0,1.1),"yellow",body,bevel=0.08); B((0,0,1.5),(1.3,2.9,0.2),"orange",body,bevel=0.04)
    for sy in (-1.2,-0.5,0.2,0.9):
        for sx in (-1,1): B((sx*0.71,sy+0.15,1.05),(0.03,0.5,0.45),"glass",body)
    B((0,-1.51,1.05),(1.1,0.03,0.5),"glass",body); B((0,-1.52,0.4),(1.3,0.08,0.14),"grey",body)
    for sx in (-1,1): S(0.1,(sx*0.5,-1.52,0.6),(1,0.5,1),"cream",body)
    wheels=[]
    for sx in (-1,1):
        for sy in (-0.9,0.9):
            w=E((sx*0.7,sy,0.33)); Cy(0.33,0.25,(sx*0.7,sy,0.33),"black",(0,R90,0),w); Cy(0.17,0.27,(sx*0.7,sy,0.33),"lgrey",(0,R90,0),w,12)
            for k in range(3): B((sx*0.7+sx*0.14,sy+0.1*math.cos(k*2.1),0.33+0.1*math.sin(k*2.1)),(0.02,0.05,0.05),"dkgrey",w,(k*2.1,0,0))
            wheels.append(w)
    face(1.1,-1.53,0.3,0.1,parent=body,mouth_dz=0.45,mr=0.12); return {"body":body,"wheels":wheels}
def b_ant():
    body=E((0,0,0.0)); S(0.22,(0,-0.5,0.5),(1,1,1),"dkbrown",body); S(0.2,(0,-0.05,0.5),(1,1.1,0.9),"brown",body); S(0.3,(0,0.5,0.5),(1,1.3,0.9),"dkbrown",body)
    for sx in (-1,1): Cy(0.015,0.35,(sx*0.1,-0.65,0.75),"black",(rad(-30),rad(sx*20),0),body); S(0.04,(sx*0.17,-0.72,0.9),(1,1,1),"black",body)
    legs=[]
    for i,y in enumerate((-0.25,0.0,0.25)):
        for sx in (-1,1):
            p=E((sx*0.15,y,0.45),body); Cy(0.02,0.5,(sx*0.32,y,0.3),"black",(0,rad(-sx*50),0),p); Cy(0.02,0.25,(sx*0.5,y,0.1),"black",(0,rad(-sx*5),0),p); legs.append(p)
    face(0.58,-0.68,0.1,0.07,parent=body,mouth_dz=0.13,mr=0.07,tongue=False); return {"body":body,"legs":legs}
def b_rat():
    body=E((0,0,0)); S(0.4,(0,0.1,0.42),(0.9,1.3,0.85),"grey",body); Co(0.3,0.6,(0,-0.55,0.4),"grey",(R90,0,0),body); S(0.06,(0,-0.86,0.4),(1,1,1),"pink",body)
    for sx in (-1,1): S(0.16,(sx*0.25,-0.2,0.75),(1,0.4,1),"grey",body); S(0.1,(sx*0.25,-0.23,0.75),(1,0.4,1),"pink",body)
    Cy(0.03,0.9,(0.1,0.85,0.2),"pink",(rad(-75),0,rad(-15)),body)
    legs=[]
    for (x,y) in [(-0.22,-0.25),(0.22,-0.25),(-0.25,0.3),(0.25,0.3)]:
        p=E((x,y,0.25),body); Cy(0.05,0.25,(x,y,0.12),"pink",parent=p); legs.append(p)
    face(0.55,-0.6,0.13,0.08,parent=body,mouth_dz=0.1,mr=0.06,tongue=False); return {"body":body,"legs":legs}
def b_taxi():
    body=E((0,0,0)); B((0,0,0.55),(1.5,2.5,0.62),"yellow",body,bevel=0.14); B((0,0.2,1.02),(1.2,1.35,0.6),"yellow",body,bevel=0.18)
    B((0,-0.5,1.03),(1.0,0.08,0.42),"glass",body,bevel=0.03); B((0,0.9,1.03),(1.0,0.08,0.4),"glass",body,bevel=0.03)
    for sx in (-1,1): B((sx*0.6,0.2,1.03),(0.06,1.0,0.38),"glass",body,bevel=0.03); S(0.15,(sx*0.5,-1.26,0.62),(1,0.5,1),"cream",body)
    B((0,-1.27,0.3),(1.4,0.14,0.16),"grey",body,bevel=0.04); B((0,0.2,1.4),(0.6,0.3,0.16),"white",body,bevel=0.03)
    for k in range(6): B((-0.5+k*0.2,-1.27,0.55),(0.1,0.03,0.1),"black" if k%2==0 else "white",body)
    wheels=[]
    for sx in (-1,1):
        for sy in (-1,1):
            w=E((sx*0.78,sy*0.82,0.34)); Cy(0.34,0.28,(sx*0.78,sy*0.82,0.34),"black",(0,R90,0),w); Cy(0.18,0.3,(sx*0.78,sy*0.82,0.34),"lgrey",(0,R90,0),w,16)
            for k in range(4): B((sx*0.78+sx*0.155,sy*0.82+0.11*math.cos(k*0.8),0.34+0.11*math.sin(k*0.8)),(0.02,0.05,0.05),"grey",w,(k*0.8,0,0))
            wheels.append(w)
    face(1.08,-0.53,0.26,0.14,parent=body,mouth_dz=0.52,mr=0.2); return {"body":body,"wheels":wheels}
def b_bike():
    body=E((0,0,0)); wheels=[]
    for y in (-0.75,0.75):
        w=E((0,y,0.42)); To(0.36,0.06,(0,y,0.42),"black",(0,R90,0),w); To(0.2,0.015,(0,y,0.42),"grey",(0,R90,0),w)
        for k in range(6): Cy(0.012,0.66,(0,y,0.42),"grey",(k*math.pi/6,0,0),w)
        wheels.append(w)
    for (a,b_) in [((0,-0.75,0.42),(0,-0.2,1.0)),((0,-0.2,1.0),(0,0.3,0.5)),((0,0.3,0.5),(0,0.75,0.42)),((0,-0.2,1.0),(0,0.35,1.0)),((0,0.35,1.0),(0,0.75,0.42)),((0,0.3,0.5),(0,0.35,1.0))]:
        va,vb=Vector(a),Vector(b_); d=vb-va; Cy(0.03,d.length,tuple((va+vb)/2),"red",d.to_track_quat('Z','Y').to_euler(),body)
    B((0,0.35,1.05),(0.16,0.3,0.06),"dkgrey",body,bevel=0.02); Cy(0.025,0.6,(0,-0.2,1.1),"grey",(0,R90,0),body)
    for sx in (-1,1): Cy(0.03,0.12,(sx*0.33,-0.2,1.1),"black",(0,R90,0),body); Cy(0.03,0.16,(sx*0.08,0.3,0.5),"grey",(0,R90,0),body); B((sx*0.16,0.3,0.5),(0.08,0.14,0.03),"dkgrey",body)
    S(0.1,(0,-0.3,0.95),(1,0.6,1),"cream",body); face(1.15,-0.28,0.1,0.07,parent=body,mouth_dz=0.1,mr=0.06,tongue=False); return {"body":body,"wheels":wheels}
# ---------------- fly ----------------
def wingpair(y, z, c, length=0.6, shape="tri", x0=0.2, parent=None):
    out=[]
    for sx in (-1,1):
        p=E((sx*x0,y,z),parent)
        if shape=="tri": Fp([(0,0.15),(sx*length,0.3),(sx*length*1.1,-0.15),(sx*length*0.5,-0.3),(0,-0.15)],(sx*x0,y,z),0.03,c,p)
        else: S(length/2,(sx*(x0+length/2),y,z),(1,0.5,0.25),c,p)
        out.append(p)
    return out
def b_bat():
    S(0.3,(0,0,1.0),(1,0.9,1.1),"purple"); S(0.26,(0,-0.1,1.4),(1,1,1),"purple")
    for sx in (-1,1): Co(0.1,0.3,(sx*0.18,-0.05,1.7),"purple",(0,rad(sx*15),0)); B((sx*0.05,-0.33,1.3),(0.04,0.02,0.08),"white")
    face(1.45,-0.33,0.11,0.07,mouth_dz=0.12,mr=0.08); return {"wings":wingpair(0.05,1.05,"purple",0.8,"tri",0.12),"flap":30}
def b_bee():
    S(0.4,(0,0,1.0),(1,1.3,0.95),"yellow")
    for y in (-0.15,0.15,0.4): To(0.41,0.06,(0,y,1.0),"black",(R90,0,0),scale=(1,1,0.9))
    Co(0.06,0.25,(0,0.62,0.95),"black",(rad(-90),0,0)); S(0.28,(0,-0.45,1.08),(1,1,1),"yellow")
    for sx in (-1,1): Cy(0.015,0.3,(sx*0.1,-0.55,1.45),"black",(rad(-20),rad(sx*25),0)); S(0.04,(sx*0.17,-0.6,1.58),(1,1,1),"black")
    face(1.15,-0.7,0.12,0.08,mouth_dz=0.14,mr=0.08); return {"wings":wingpair(0.0,1.35,"glass",0.5,"oval",0.1),"flap":40}
def b_owl():
    S(0.45,(0,0,0.95),(0.9,0.85,1.25),"brown"); S(0.3,(0,-0.2,0.8),(0.8,0.6,0.9),"tan")
    for sx in (-1,1): Co(0.1,0.25,(sx*0.25,0,1.55),"brown",(0,rad(sx*20),0)); S(0.17,(sx*0.18,-0.38,1.25),(1,0.5,1),"cream")
    Co(0.06,0.14,(0,-0.45,1.08),"orange",(R90,0,0)); legs2("orange",0,0.12,0.03,0.15,foot="orange")
    eyes(1.25,-0.4,0.18,0.1); return {"wings":wingpair(0.05,1.0,"brown",0.5,"oval",0.35),"flap":25}
def b_jet():
    body=E((0,0,0)); Cy(0.25,2.0,(0,0,1.0),"white",(R90,0,0),body); Co(0.25,0.6,(0,-1.3,1.0),"white",(rad(-90),0,0),body); S(0.18,(0,-0.5,1.15),(1,1.3,0.7),"glass",body)
    for sx in (-1,1): B((sx*0.6,0.1,0.95),(1.0,0.5,0.05),"sky",body,rot=(0,0,rad(sx*-20))); B((sx*0.3,0.95,1.05),(0.45,0.25,0.04),"sky",body)
    B((0,0.95,1.3),(0.04,0.3,0.45),"sky",body); B((0,0.9,1.0),(0.04,0.6,0.1),"red",body)
    face(1.05,-1.45,0.1,0.07,parent=body,mouth_dz=0.12,mr=0.07,tongue=False); return {"wings":[]}
def b_kite():
    Fp([(0,0.9),(0.6,0.0),(0,-0.9),(-0.6,0.0)],(0,0,1.5),0.04,"red"); Fp([(0,0.88),(0.58,0.0),(0,0.0)],(0,-0.025,1.5),0.02,"yellow"); Fp([(0,-0.88),(-0.58,0.0),(0,0.0)],(0,-0.025,1.5),0.02,"blue")
    Cy(0.01,1.6,(0,0.03,1.5),"dkgrey"); Cy(0.01,1.1,(0,0.03,1.5),"dkgrey",(0,R90,0))
    for k in range(4): B((0.1*(k%2*2-1),0,0.55-k*0.17),(0.2,0.03,0.08),["red","yellow","blue","green"][k],rot=(0,rad(30),0))
    Cy(0.008,0.6,(0,0,0.3),"dkgrey"); face(1.75,-0.03,0.14,0.09,mouth_dz=0.3,mr=0.12); return {"wings":[]}
def b_bird():
    S(0.35,(0,0,1.0),(0.9,1.2,0.85),"blue"); S(0.25,(0,-0.1,0.9),(0.7,0.9,0.6),"sky"); S(0.26,(0,-0.4,1.3),(1,1,1),"blue")
    Co(0.07,0.2,(0,-0.7,1.26),"orange",(R90,0,0)); S(0.06,(0,-0.35,1.6),(1,1,1.6),"blue")
    for k in range(3): S(0.1,(0.08*(k-1),0.45,0.95),(0.4,1,1.4),"navy",rot=(rad(-40),0,rad(k*12-12)))
    legs2("orange",0,0.5,0.025,0.1,foot="orange"); face(1.36,-0.62,0.11,0.07,mouth_dz=0.3,mr=0.0,tongue=False)
    return {"wings":wingpair(0.0,1.1,"navy",0.5,"oval",0.3),"flap":35}
# ---------------- swim ----------------
def b_crab():
    S(0.55,(0,0,0.45),(1.3,0.9,0.6),"red"); claws=[]
    for sx in (-1,1):
        Cy(0.025,0.35,(sx*0.3,-0.3,0.85),"red",(0,rad(sx*10),0))
        p=E((sx*0.55,-0.25,0.5)); Cy(0.05,0.4,(sx*0.68,-0.35,0.55),"red",(0,rad(-sx*70),0),p); S(0.17,(sx*0.82,-0.45,0.6),(1,1.3,0.8),"red",p); S(0.1,(sx*0.82,-0.65,0.65),(1,1,0.6),"red",p); claws.append(p)
        for k in range(3): Cy(0.03,0.45,(sx*0.65,0.1+k*0.15,0.25),"red",(0,rad(-sx*55),0))
    eyes(1.03,-0.3,0.33,0.09); smile(0.45,-0.52,0.14,tongue=False); return {"claws":claws,"sway":4,"yawaxis":1}
def b_duck():
    S(0.45,(0,0.05,0.5),(0.9,1.3,0.75),"yellow"); S(0.3,(0,-0.5,0.95),(1,1,1),"yellow"); Co(0.1,0.3,(0,-0.8,0.9),"orange",(R90,0,0),r2=0.08)
    tail=E((0,0.5,0.5)); S(0.14,(0,0.7,0.65),(0.5,1,1.3),"yellow",tail,rot=(rad(-40),0,0)); S(0.15,(0.3,0,0.5),(0.3,1,0.6),"gold"); S(0.15,(-0.3,0,0.5),(0.3,1,0.6),"gold")
    face(1.02,-0.72,0.11,0.08,mouth_dz=0.5,mr=0.0,tongue=False); return {"tail":tail,"tailamp":20,"sway":3,"yawaxis":1}
def b_ship():
    B((0,0,0.35),(1.0,2.4,0.5),"navy",bevel=0.1); B((0,0,0.6),(1.0,2.4,0.08),"wood",bevel=0.02); B((0,0.1,0.95),(0.7,1.1,0.6),"white",bevel=0.05); B((0,0.1,1.4),(0.5,0.7,0.3),"white",bevel=0.04)
    Cy(0.12,0.5,(0,0.6,1.5),"red"); Cy(0.13,0.1,(0,0.6,1.75),"black"); Co(0.3,0.4,(0,-1.3,0.4),"navy",(rad(-90),0,0),r2=0.0)
    for k in range(3): S(0.07,(-0.36,-0.3+k*0.4,1.0),(0.3,1,1),"glass"); S(0.07,(0.36,-0.3+k*0.4,1.0),(0.3,1,1),"glass")
    face(1.05,-0.46,0.14,0.09,mouth_dz=0.2,mr=0.09); return {"sway":6,"yawaxis":1}
def b_boat():
    B((0,0,0.3),(0.9,2.0,0.4),"wood",bevel=0.1); B((0,0,0.5),(0.75,1.9,0.03),"tan"); Cy(0.04,1.6,(0,0.1,1.25),"dkbrown")
    Fp([(0,0),(0.0,1.3),(-0.9,0.0)],(0.05,0.1,0.55),0.02,"white"); Fp([(0,0),(0.0,0.7),(0.5,0.0)],(-0.02,0.1,0.55),0.02,"red")
    face(0.45,-1.0,0.14,0.08,mouth_dz=0.15,mr=0.08); return {"sway":7,"yawaxis":1}
def b_swan():
    S(0.45,(0,0.1,0.5),(0.9,1.4,0.7),"white"); S(0.2,(0,0.7,0.75),(0.6,1,1.3),"white",rot=(rad(-30),0,0))
    for k,(y,z) in enumerate([(-0.5,0.75),(-0.7,1.05),(-0.75,1.4)]): S(0.12,(0,y,z),(1,1,1.2),"white")
    S(0.2,(0,-0.65,1.65),(1,1.1,0.9),"white"); Co(0.07,0.3,(0,-0.95,1.6),"orange",(R90,0,0)); S(0.06,(0,-0.8,1.6),(1,1,1),"black")
    tail=E((0,0.5,0.6)); S(0.14,(0,0.8,0.7),(0.6,1,1.0),"white",tail)
    face(1.7,-0.82,0.1,0.07,mouth_dz=0.5,mr=0.0,tongue=False); return {"tail":tail,"tailamp":15,"sway":3,"yawaxis":1}
def b_seal():
    S(0.45,(0,-0.1,0.45),(0.9,1.4,0.75),"grey"); S(0.3,(0,-0.6,0.7),(1,1,0.9),"grey"); S(0.2,(0,-0.3,0.3),(0.8,1.2,0.5),"lgrey")
    S(0.07,(0,-0.9,0.68),(1.1,0.8,0.7),"black"); tail=E((0,0.5,0.35))
    for sx in (-1,1): S(0.15,(sx*0.2,0.75,0.25),(0.7,1,0.3),"grey",tail,rot=(0,0,rad(sx*25))); S(0.15,(sx*0.45,-0.2,0.2),(0.6,1,0.3),"grey",rot=(0,0,rad(sx*-30)))
    for sx in (-1,1):
        for k in (-1,1): Cy(0.006,0.3,(sx*0.2,-0.9,0.66+0.03*k),"white",(0,R90,rad(k*8)))
    face(0.85,-0.82,0.12,0.08,mouth_dz=0.22,mr=0.07); return {"tail":tail,"tailamp":25,"sway":4,"yawaxis":1}
# ---------------- wiggle ----------------
def b_box():
    B((0,0,0.6),(1.2,1.0,1.2),"tan",bevel=0.03); B((0,0,1.22),(1.26,1.06,0.08),"wood"); B((0,0,1.0),(1.22,0.12,0.5),"brown")
    face(0.85,-0.51,0.25,0.12,mouth_dz=0.3,mr=0.14); return {}
def b_hat():
    Cy(0.95,0.08,(0,0,0.04),"dkgrey"); Cy(0.55,0.9,(0,0,0.53),"dkgrey"); Cy(0.57,0.14,(0,0,0.25),"red"); face(0.7,-0.56,0.2,0.1,mouth_dz=0.25,mr=0.11); return {}
def b_egg():
    S(0.6,(0,0,0.75),(0.85,0.85,1.1),"cream")
    for (x,y,z) in [(-0.3,-0.35,1.1),(0.3,-0.4,0.6),(0.1,0.5,0.9),(-0.4,0.3,0.5)]: S(0.1,(x,y,z),(1,1,0.6),"sky")
    face(0.95,-0.47,0.17,0.1,mouth_dz=0.25,mr=0.1); return {}
def b_pen():
    Cy(0.14,1.6,(0,0,0.95),"blue"); Co(0.14,0.35,(0,0,0.17),"cream",(rad(180),0,0),r2=0.03); Co(0.03,0.08,(0,0,0.03),"dkgrey",(rad(180),0,0)); Cy(0.15,0.2,(0,0,1.7),"silver"); B((0.17,0,1.3),(0.05,0.08,0.7),"silver")
    face(1.2,-0.13,0.08,0.06,mouth_dz=0.12,mr=0.06,tongue=False); return {}
def b_bag():
    B((0,0,0.55),(1.2,0.6,1.0),"hotpink",bevel=0.08); To(0.35,0.05,(0,0,1.1),"hotpink",(R90,0,0),scale=(1,1,0.8)); B((0,-0.31,0.5),(0.9,0.04,0.5),"pink",bevel=0.03); S(0.07,(0,-0.33,0.9),(1,0.5,1),"gold")
    face(0.75,-0.34,0.22,0.1,mouth_dz=0.25,mr=0.1); return {}
def b_cap():
    S(0.6,(0,0.05,0.35),(1,1,0.75),"red"); B((0,-0.65,0.1),(0.9,0.6,0.06),"red",bevel=0.03); S(0.07,(0,0,0.8),(1,1,1),"white")
    for k in range(3): B((0,0.05,0.4),(0.02,1.15,0.55),"white",rot=(0,0,k*math.pi/3))
    face(0.5,-0.57,0.17,0.09,mouth_dz=0.25,mr=0.0,tongue=False); smile(0.08,-0.95,0.1,tongue=False); return {}
def b_ice():
    Co(0.35,0.9,(0,0,0.45),"tan",(rad(180),0,0)); S(0.4,(0,0,1.1),(1,1,0.9),"pink"); S(0.33,(0,0,1.55),(1,1,0.9),"mint"); S(0.06,(0,0,1.9),(1,1,1),"red")
    for k in range(5): S(0.03,(0.25*math.cos(k*1.3),-0.25*abs(math.sin(k*1.3)),1.2+0.1*k),(1,1,1),["red","yellow","blue","green","purple"][k])
    face(1.15,-0.37,0.16,0.09,mouth_dz=0.22,mr=0.09); return {}
def b_pie():
    Cy(0.75,0.3,(0,0,0.15),"tan",verts=32); Cy(0.68,0.12,(0,0,0.33),"orange",verts=32); To(0.72,0.07,(0,0,0.33),"wood")
    for k in range(3): B((0,0,0.38),(0.08,1.3,0.03),"tan",rot=(0,0,k*math.pi/3))
    face(0.3,-0.72,0.2,0.1,mouth_dz=0.0,mr=0.1,tongue=False); return {}
def b_cup():
    Cy(0.42,0.9,(0,0,0.45),"sky",verts=32); Cy(0.36,0.06,(0,0,0.9),"brown",verts=32); To(0.3,0.05,(0.45,0,0.5),"sky",(R90,0,0)); To(0.42,0.04,(0,0,0.9),"sky")
    face(0.6,-0.4,0.17,0.09,mouth_dz=0.25,mr=0.1); return {}
def b_map():
    B((0,0,0.6),(1.4,0.06,1.0),"beige",bevel=0.02); Cy(0.08,1.1,(-0.72,0,0.6),"straw"); Cy(0.08,1.1,(0.72,0,0.6),"straw")
    B((-0.2,-0.04,0.45),(0.5,0.02,0.3),"green",bevel=0.05); B((0.3,-0.04,0.75),(0.4,0.02,0.25),"sky",bevel=0.05); B((0.25,-0.05,0.35),(0.03,0.02,0.4),"red",rot=(0,rad(40),0)); S(0.05,(0.35,-0.05,0.9),(1,1,1),"red")
    face(0.85,-0.05,0.2,0.09,mouth_dz=0.1,mr=0.0,tongue=False); smile(0.65,-0.05,0.09,tongue=False); return {}
def b_fan():
    Cy(0.4,0.08,(0,0,0.04),"dkgrey"); Cy(0.05,0.8,(0,0,0.45),"grey"); To(0.55,0.05,(0,0,1.2),"sky",(R90,0,0)); Cy(0.1,0.1,(0,0,1.2),"grey",(R90,0,0))
    for k in range(4): B((0,0,1.2),(0.9,0.02,0.22),"glass",rot=(0,k*math.pi/4,0))
    face(1.38,-0.06,0.15,0.08,mouth_dz=0.0,mr=0.0,tongue=False); smile(1.05,-0.06,0.09,tongue=False); return {}
def b_bug():
    S(0.5,(0,0,0.4),(1,1.2,0.7),"red"); S(0.26,(0,-0.5,0.4),(1,1,0.8),"black"); B((0,0.1,0.75),(0.03,1.0,0.1),"black")
    for (x,y) in [(-0.25,-0.1),(0.25,-0.1),(-0.3,0.3),(0.3,0.3),(0,0.45)]: S(0.09,(x,y,0.72),(1,1,0.4),"black")
    for sx in (-1,1): Cy(0.012,0.3,(sx*0.1,-0.7,0.6),"black",(rad(-40),rad(sx*20),0)); S(0.03,(sx*0.17,-0.78,0.72),(1,1,1),"black")
    for sx in (-1,1):
        for k in range(3): Cy(0.02,0.3,(sx*0.45,-0.1+k*0.2,0.15),"black",(0,rad(-sx*50),0))
    face(0.5,-0.72,0.11,0.07,mouth_dz=0.14,mr=0.07,tongue=False); return {}
def b_milk():
    B((0,0,0.65),(0.8,0.8,1.3),"white",bevel=0.02); Fp([(-0.4,0),(0.4,0),(0,0.35)],(0,0,1.3),0.8,"white"); B((0,0,1.38),(0.05,0.82,0.15),"sky")
    B((0,-0.41,0.65),(0.6,0.02,0.35),"sky",bevel=0.05); S(0.1,(0,-0.43,0.3),(1,0.4,1),"sky")
    face(0.95,-0.41,0.2,0.1,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.72,-0.43,0.1); return {}
def b_cake():
    Cy(0.7,0.45,(0,0,0.22),"tan",verts=32); Cy(0.7,0.08,(0,0,0.48),"hotpink",verts=32); Cy(0.5,0.4,(0,0,0.72),"tan",verts=32); Cy(0.5,0.08,(0,0,0.95),"hotpink",verts=32)
    Cy(0.04,0.4,(0,0,1.2),"sky"); S(0.07,(0,0,1.45),(1,1,1.3),"orange"); S(0.08,(0,-0.45,1.0),(1,1,1),"red")
    for k in range(8): S(0.07,(0.7*math.cos(k*0.785),0.7*math.sin(k*0.785),0.48),(1,1,0.8),"white")
    face(0.3,-0.68,0.2,0.1,mouth_dz=0.12,mr=0.1); return {}
def b_drum():
    Cy(0.65,0.8,(0,0,0.4),"red",verts=32); Cy(0.66,0.08,(0,0,0.8),"cream",verts=32); Cy(0.66,0.08,(0,0,0.04),"cream",verts=32)
    for k in range(8): Cy(0.03,0.8,(0.66*math.cos(k*0.785),0.66*math.sin(k*0.785),0.4),"gold",(rad(25),0,k*0.785+R90))
    for sx in (-1,1): Cy(0.03,0.7,(sx*0.3,-0.2,1.1),"wood",(0,rad(sx*-30),0)); S(0.08,(sx*0.48,-0.2,1.4),(1,1,1),"cream")
    face(0.5,-0.63,0.2,0.1,mouth_dz=0.22,mr=0.1); return {}
def b_book():
    B((0,0,0.65),(1.0,0.35,1.3),"blue",bevel=0.02); B((0.0,-0.02,0.65),(0.96,0.3,1.24),"cream"); B((0,-0.19,0.65),(1.0,0.03,1.3),"blue"); B((0,-0.21,0.95),(0.6,0.02,0.1),"gold"); B((0,-0.21,0.35),(0.6,0.02,0.05),"gold")
    face(0.75,-0.21,0.2,0.1,mouth_dz=0.25,mr=0.1); return {}
def b_tent():
    Fp([(-0.9,0),(0.9,0),(0,1.3)],(0,0,0),1.6,"orange"); Fp([(-0.3,0),(0.3,0),(0,0.55)],(0,-0.81,0),0.04,"dkgrey"); Cy(0.03,1.4,(0,0,1.32),"dkbrown",(R90,0,0))
    face(0.95,-0.82,0.15,0.08,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.72,-0.82,0.08,tongue=False); return {}
def b_gift():
    B((0,0,0.5),(1.0,1.0,1.0),"red",bevel=0.02); B((0,0,1.03),(1.08,1.08,0.1),"red"); B((0,0,0.55),(0.2,1.1,1.12),"gold"); B((0,0,0.55),(1.1,0.2,1.12),"gold")
    for sx in (-1,1): S(0.15,(sx*0.18,0,1.2),(1.2,0.7,0.6),"gold",rot=(0,rad(sx*30),0))
    face(0.75,-0.52,0.25,0.11,mouth_dz=0.3,mr=0.12); return {}
def b_worm():
    for k in range(6): S(0.2,(0.18*math.sin(k*1.2),0.3*k-0.75,0.2+0.12*abs(math.sin(k*0.9))),(1,1,1),"pink" if k%2 else "hotpink")
    S(0.24,(0,-0.95,0.45),(1,1,1),"pink"); face(0.55,-1.15,0.11,0.08,mouth_dz=0.16,mr=0.08); return {}
# ---------------- spin ----------------
def b_sun():
    S(0.55,(0,0,1.0),(1,0.5,1),"yellow")
    for k in range(10): a=k*TAU/10; Co(0.1,0.35,(0.75*math.cos(a),0,1.0+0.75*math.sin(a)),"orange",(0,-a+R90,0))
    face(1.15,-0.28,0.2,0.1,mouth_dz=0.3,mr=0.14); return {}
def b_key():
    To(0.38,0.1,(0,0,1.45),"gold",(R90,0,0)); Cy(0.1,1.1,(0,0,0.55),"gold"); B((0.15,0,0.15),(0.3,0.1,0.1),"gold"); B((0.15,0,0.4),(0.25,0.1,0.1),"gold")
    face(1.55,-0.1,0.12,0.07,mouth_dz=0.2,mr=0.0,tongue=False); smile(1.25,-0.1,0.08,tongue=False); return {}
def b_nut():
    Cy(0.7,0.4,(0,0,0.65),"silver",(R90,0,0),verts=6); To(0.3,0.08,(0,0,0.65),"grey",(R90,0,0)); face(0.95,-0.22,0.2,0.1,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.35,-0.22,0.1,tongue=False); return {}
def b_web():
    for k in range(8): Cy(0.015,1.8,(0,0,1.0),"lgrey",(0,k*math.pi/8,0))
    for r in (0.3,0.55,0.8): To(r,0.012,(0,0,1.0),"lgrey",(R90,0,0),scale=(1,1,1))
    S(0.2,(0,0,1.0),(1,0.6,1),"dkgrey"); face(1.06,-0.13,0.08,0.06,mouth_dz=0.12,mr=0.05,tongue=False); return {}
def b_star():
    Fp(starpts(0.95,0.42),(0,0,1.0),0.3,"yellow"); face(1.0,-0.17,0.2,0.1,mouth_dz=0.3,mr=0.12); return {}
def b_ring():
    To(0.65,0.12,(0,0,0.9),"gold",(R90,0,0)); Fp([(0,0.2),(0.2,0),(0,-0.2),(-0.2,0)],(0,0,1.75),0.2,"sky"); To(0.2,0.05,(0,0,1.75),"gold",(R90,0,0))
    face(0.98,-0.14,0.11,0.07,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.55,-0.14,0.09,tongue=False); return {}
def b_coin():
    Cy(0.8,0.16,(0,0,0.8),"gold",(R90,0,0),verts=40); To(0.65,0.04,(0,-0.09,0.8),"orange",(R90,0,0)); Fp(starpts(0.3,0.13),(0,-0.1,0.5),0.04,"orange")
    face(0.95,-0.1,0.22,0.11,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.75,-0.12,0.1,tongue=False); return {}
# ---------------- float ----------------
def b_bed():
    B((0,0,0.35),(1.3,2.0,0.3),"wood",bevel=0.03); B((0,0,0.6),(1.25,1.9,0.25),"white",bevel=0.05); B((0,0.2,0.7),(1.25,1.4,0.15),"sky",bevel=0.05); B((0,-0.7,0.78),(1.0,0.5,0.2),"white",bevel=0.08)
    B((0,1.0,0.8),(1.3,0.08,1.0),"wood",bevel=0.02); B((0,-1.0,0.55),(1.3,0.08,0.5),"wood",bevel=0.02)
    face(1.0,-1.05,0.22,0.1,mouth_dz=0.25,mr=0.1); return {}
def b_moon():
    m=S(0.8,(0,0,1.0),(1,0.5,1),"yellow"); cut=S(0.7,(0.45,0,1.1),(1,1.2,1),"yellow"); cut.hide_render=True; cut.hide_viewport=True
    bm=m.modifiers.new("Cut",'BOOLEAN'); bm.operation='DIFFERENCE'; bm.object=cut
    face(1.1,-0.36,0.12,0.08,x=-0.35,mouth_dz=0.22,mr=0.08); return {}
def b_leaf():
    S(0.7,(0,0,1.0),(0.6,0.25,1.0),"green"); Cy(0.03,1.9,(0,-0.1,1.0),"dkgreen"); Cy(0.04,0.5,(0,0,0.0),"dkgreen")
    for k in range(3): Cy(0.015,0.5,(0,-0.18,1.2-k*0.35),"dkgreen",(0,rad(55),0)); Cy(0.015,0.5,(0,-0.18,1.2-k*0.35),"dkgreen",(0,rad(-55),0))
    face(1.3,-0.22,0.13,0.08,mouth_dz=0.2,mr=0.08); return {}
def b_snow():
    for k in range(3): B((0,0,1.0),(1.8,0.08,0.12),"white",rot=(0,k*math.pi/3,0))
    for k in range(6):
        a=k*math.pi/3
        for s in (-1,1): B((0.6*math.cos(a),0,1.0+0.6*math.sin(a)),(0.35,0.06,0.08),"white",rot=(0,-a+s*rad(50),0))
    S(0.3,(0,0,1.0),(1,0.4,1),"sky"); face(1.08,-0.13,0.11,0.07,mouth_dz=0.16,mr=0.07,tongue=False); return {}
def b_rain():
    for (x,z,r) in [(-0.45,1.3,0.35),(0,1.45,0.45),(0.45,1.3,0.35),(-0.2,1.15,0.35),(0.25,1.15,0.35)]: S(r,(x,0,z),(1,0.8,1),"lgrey")
    for k in range(5): S(0.07,(-0.5+k*0.25,0,0.55-0.15*(k%2)),(0.8,0.8,1.4),"sky")
    face(1.4,-0.4,0.18,0.1,mouth_dz=0.25,mr=0.1); return {}
# ---------------- grow / flash / ring ----------------
def b_tree():
    Cy(0.18,0.8,(0,0,0.4),"brown"); S(0.55,(0,0,1.3),(1,1,0.9),"green"); S(0.4,(-0.4,0,1.1),(1,1,1),"green"); S(0.4,(0.4,0,1.1),(1,1,1),"green"); S(0.35,(0,0,1.8),(1,1,1),"green")
    for (x,z) in [(-0.3,1.3),(0.3,1.5),(0.0,1.05)]: S(0.07,(x,-0.5,z),(1,1,1),"red")
    face(1.35,-0.52,0.15,0.09,mouth_dz=0.22,mr=0.09); return {}
def b_corn():
    S(0.35,(0,0,0.9),(1,1,2.2),"yellow")
    for k in range(40): S(0.06,(0.3*math.cos(k*0.9),0.3*math.sin(k*0.9),0.25+k*0.035),(1,1,1),"gold")
    for sx in (-1,1): S(0.3,(sx*0.25,0.1,0.7),(0.5,0.3,1.6),"green",rot=(0,rad(sx*-20),0))
    face(1.3,-0.3,0.13,0.08,mouth_dz=0.2,mr=0.08); return {}
def b_rose():
    Cy(0.04,1.1,(0,0,0.55),"dkgreen"); S(0.2,(0.2,0,0.6),(1.4,0.3,0.7),"green",rot=(0,rad(30),0))
    S(0.3,(0,0,1.3),(1,1,1.1),"red")
    for k in range(6): a=k*1.05; S(0.17,(0.25*math.cos(a),0.25*math.sin(a),1.3),(1,1,1.3),"red")
    face(1.35,-0.38,0.11,0.07,mouth_dz=0.16,mr=0.07,tongue=False); return {}
def b_fire():
    g=[mat("orange",0.6,1.5), mat("yellow",0.6,2.0), mat("red",0.6,1.0)]
    for i,(r,h,z,c) in enumerate([(0.55,1.4,0.7,"red"),(0.4,1.1,0.55,"orange"),(0.22,0.7,0.35,"yellow")]):
        Co(r,h,(0,0,z),c); bpy.context.active_object.data.materials[0]=g[[2,0,1][i]]
    for k in range(4): S(0.08,(0.4*math.cos(k*1.7),0.4*math.sin(k*1.7),1.3+0.2*k),(1,1,1.5),"orange")
    face(0.6,-0.4,0.15,0.09,mouth_dz=0.22,mr=0.09); return {"glow":g}
def b_bell():
    piv=E((0,0,1.9)); Cy(0.03,0.3,(0,0,1.9),"dkbrown",(R90,0,0),piv); To(0.08,0.025,(0,0,1.75),"gold",(0,R90,0),piv)
    S(0.45,(0,0,1.25),(1,1,1.1),"gold",piv); Co(0.62,0.5,(0,0,0.85),"gold",(0,0,0),piv,r2=0.4); To(0.62,0.06,(0,0,0.62),"orange",parent=piv); S(0.12,(0,0,0.55),(1,1,1),"dkgrey",piv)
    face(1.3,-0.42,0.14,0.08,parent=piv,mouth_dz=0.2,mr=0.08); return {"pivot":piv}
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}
