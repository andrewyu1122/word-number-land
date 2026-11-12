exec(open(PIPE + "/builders_words.py", encoding="utf-8").read())
# ================= mascot =================
def b_mascot():
    B((0,0,0.95),(1.0,0.9,1.0),"mint",bevel=0.2); Fp(starpts(0.2,0.09),(0,-0.47,0.72),0.03,"gold")
    Cy(0.025,0.35,(0,0,1.6),"gold"); Fp(starpts(0.17,0.075),(0,0,1.9),0.06,"gold")
    wings=[]
    for sx in (-1,1):
        p=E((sx*0.42,0.35,1.15)); S(0.26,(sx*0.68,0.38,1.2),(1,0.25,0.6),"glass",p,rot=(0,rad(sx*-15),0)); wings.append(p)
    arms=[]
    for sx in (-1,1):
        p=E((sx*0.5,0,1.1)); Cy(0.06,0.42,(sx*0.5,0,0.88),"mint",parent=p); S(0.1,(sx*0.5,0,0.65),(1,1,1),"peach",p); arms.append(p)
    for sx in (-1,1): Cy(0.07,0.3,(sx*0.25,0,0.3),"mint"); S(0.13,(sx*0.25,-0.04,0.08),(1,1.3,0.6),"blue")
    for sx in (-1,1): S(0.08,(sx*0.36,-0.45,1.0),(1,0.4,0.7),"pink")
    face(1.2,-0.46,0.22,0.12,mouth_dz=0.3,mr=0.13); return {"arms":arms,"wings":wings}
def act_happy(h):
    act_hop(h); l,r=h["arms"]
    keys(l,"rotation_euler",[(1,(0,rad(35),0)),(6,(0,rad(60),0)),(12,(0,rad(130),0)),(19,(0,rad(40),0)),(24,(0,rad(35),0))])
    sine(r,"rotation_euler",1,rad(28),3,base=rad(-150))
    for i,w in enumerate(h["wings"]): sine(w,"rotation_euler",1,rad(25)*(1 if i==0 else -1),4)
def act_cheer(h):
    sine(ROOT,"rotation_euler",0,rad(-9),2,base=rad(-5))
    for f in range(1,NFRAMES+2):
        t=(f-1)/NFRAMES; s=1+0.03*math.sin(TAU*2*t); ROOT.scale=(s,s,2-s); kf(ROOT,"scale",f)
    l,r=h["arms"]; sine(l,"rotation_euler",1,rad(30),2,base=rad(75)); sine(r,"rotation_euler",1,rad(-30),2,base=rad(-75))
    for i,w in enumerate(h["wings"]): sine(w,"rotation_euler",1,rad(20)*(1 if i==0 else -1),4)
ACTS["happy"]=act_happy; ACTS["cheer"]=act_cheer
# ================= objects (maths) =================
def b_apple():
    S(0.6,(0,0,0.6),(1,1,0.9),"red"); Cy(0.04,0.3,(0,0,1.2),"dkbrown",(rad(10),0,0)); S(0.16,(0.18,0,1.25),(1,0.35,0.6),"green",rot=(0,rad(-30),0))
    face(0.75,-0.55,0.18,0.1,mouth_dz=0.25,mr=0.1); return {}
def b_strawberry():
    Co(0.55,1.1,(0,0,0.55),"red",(rad(180),0,0),r2=0.15); S(0.5,(0,0,0.95),(1.1,1.1,0.5),"red")
    for k in range(14): a=k*2.4; S(0.035,(0.45*math.cos(a)*(1-k*0.05),0.45*math.sin(a)*(1-k*0.05),0.2+k*0.06),(1,1,1.4),"yellow")
    for k in range(6): a=k*TAU/6; S(0.16,(0.3*math.cos(a),0.3*math.sin(a),1.2),(1.4,0.5,0.3),"green",rot=(0,0,a))
    Cy(0.03,0.2,(0,0,1.3),"green"); face(0.8,-0.46,0.15,0.09,mouth_dz=0.22,mr=0.09); return {}
def b_chick():
    S(0.45,(0,0,0.5),(1,1,0.95),"yellow"); S(0.35,(0,-0.1,1.05),(1,1,1),"yellow"); Co(0.07,0.18,(0,-0.44,1.0),"orange",(R90,0,0))
    for sx in (-1,1): S(0.16,(sx*0.42,0.05,0.5),(0.4,1,0.7),"gold")
    S(0.06,(0,0.05,1.4),(1,1,1.6),"yellow"); legs2("orange",0,0.12,0.025,0.14,foot="orange")
    eyes(1.12,-0.4,0.12,0.07); return {}
def b_balloon():
    S(0.6,(0,0,1.4),(1,1,1.2),"red"); Co(0.08,0.12,(0,0,0.66),"red",(rad(180),0,0)); Cy(0.008,0.6,(0,0,0.3),"dkgrey"); S(0.12,(-0.25,-0.3,1.85),(1,0.5,1.4),"pink")
    face(1.5,-0.55,0.18,0.1,mouth_dz=0.26,mr=0.1); return {}
def b_cookie():
    Cy(0.75,0.25,(0,0,0.13),"tan",verts=32)
    for (x,y) in [(-0.35,-0.2),(0.3,-0.4),(0.1,0.4),(-0.4,0.35),(0.45,0.1),(0,-0.05)]: S(0.1,(x,y,0.27),(1,1,0.6),"chocolate")
    face(0.28,-0.65,0.22,0.1,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.26,-0.45,0.1,tongue=False); return {}
def b_car():
    body=E((0,0,0)); B((0,0,0.55),(1.5,2.5,0.62),"red",body,bevel=0.14); B((0,0.2,1.02),(1.2,1.35,0.6),"red",body,bevel=0.18)
    B((0,-0.5,1.03),(1.0,0.08,0.42),"glass",body,bevel=0.03); B((0,0.9,1.03),(1.0,0.08,0.4),"glass",body,bevel=0.03)
    for sx in (-1,1): B((sx*0.6,0.2,1.03),(0.06,1.0,0.38),"glass",body,bevel=0.03); S(0.15,(sx*0.5,-1.26,0.62),(1,0.5,1),"cream",body)
    B((0,-1.27,0.3),(1.4,0.14,0.16),"grey",body,bevel=0.04)
    for sx in (-1,1):
        for sy in (-1,1): Cy(0.34,0.28,(sx*0.78,sy*0.82,0.34),"black",(0,R90,0)); Cy(0.18,0.3,(sx*0.78,sy*0.82,0.34),"lgrey",(0,R90,0),verts=16)
    face(1.08,-0.53,0.26,0.14,parent=body,mouth_dz=0.52,mr=0.2); return {}
def b_fish():
    S(0.6,(0,0.1,0.8),(0.55,1.0,0.7),"orange"); S(0.45,(0,0.0,0.7),(0.45,0.9,0.5),"cream")
    for y in (-0.15,0.2): To(0.61,0.03,(0,y,0.8),"red",(R90,0,0),scale=(0.55,1,0.7))
    for sz in (-1,1): S(0.4,(0,0.85,0.85+sz*0.2),(0.12,1,0.45),"gold",rot=(sz*rad(-35),0,0))
    S(0.35,(0,0.1,1.3),(0.12,0.8,0.7),"gold"); S(0.1,(0,-0.55,0.72),(1,0.6,0.8),"pink")
    for sx in (-1,1): S(0.25,(sx*0.3,0.0,0.6),(0.15,0.6,0.9),"gold",rot=(0,rad(sx*30),0))
    face(0.95,-0.42,0.17,0.1,mouth_dz=0.28,mr=0.0,tongue=False); return {}
def b_flower():
    Cy(0.05,1.0,(0,0,0.5),"green"); S(0.2,(0.2,0,0.5),(1.4,0.3,0.7),"green",rot=(0,rad(30),0)); S(0.3,(0,0,1.3),(1,0.5,1),"yellow")
    for k in range(6): a=k*TAU/6; S(0.22,(0.42*math.cos(a),0,1.3+0.42*math.sin(a)),(1,0.4,1),"hotpink")
    face(1.36,-0.15,0.11,0.07,mouth_dz=0.16,mr=0.07); return {}
def b_cupcake():
    Co(0.5,0.6,(0,0,0.3),"pink",r2=0.4,verts=16); Cy(0.45,0.1,(0,0,0.62),"tan",verts=24)
    for i,(r,z) in enumerate([(0.42,0.75),(0.34,0.95),(0.24,1.12),(0.12,1.25)]): S(r,(0,0,z),(1,1,0.6),"lavender")
    S(0.1,(0,0,1.38),(1,1,1),"red");
    for k in range(8): S(0.03,(0.3*math.cos(k*1.4),0.3*math.sin(k*1.4),0.85+0.08*(k%3)),(1,1,1.5),["yellow","sky","hotpink"][k%3])
    face(0.42,-0.47,0.17,0.09,mouth_dz=0.22,mr=0.09); return {}
# ================= garden =================
def b_sprout():
    Cy(0.04,0.6,(0,0,0.3),"green"); S(0.18,(0,0,0.65),(1,0.8,1),"lime")
    for sx in (-1,1): S(0.22,(sx*0.3,0,0.5),(1.2,0.35,0.6),"green",rot=(0,rad(sx*-35),0))
    face(0.7,-0.14,0.09,0.06,mouth_dz=0.12,mr=0.06,tongue=False); return {}
def b_tulip():
    Cy(0.04,1.0,(0,0,0.5),"green"); S(0.3,(0.1,0,0.4),(0.35,0.3,1.6),"green",rot=(0,rad(-15),0)); S(0.3,(0,0,1.3),(1,1,1.2),"hotpink")
    for k in range(3): a=k*TAU/3; Co(0.22,0.5,(0.2*math.cos(a),0.2*math.sin(a),1.5),"hotpink",(rad(-15)*math.sin(a),rad(15)*math.cos(a),0))
    face(1.28,-0.28,0.11,0.07,mouth_dz=0.16,mr=0.07,tongue=False); return {}
def b_sunflower():
    Cy(0.06,1.4,(0,0,0.7),"green"); S(0.3,(0.25,0,0.6),(1.4,0.3,0.7),"green",rot=(0,rad(35),0)); Cy(0.4,0.12,(0,0,1.5),"chocolate",(R90,0,0),verts=32)
    for k in range(14): a=k*TAU/14; S(0.2,(0.55*math.cos(a),0,1.5+0.55*math.sin(a)),(1,0.3,1),"yellow",rot=(0,-a,0))
    face(1.58,-0.08,0.13,0.08,mouth_dz=0.2,mr=0.09); return {}
def b_mushroom():
    Cy(0.22,0.7,(0,0,0.35),"cream"); S(0.65,(0,0,0.75),(1,1,0.6),"red")
    for (x,y,z) in [(-0.3,-0.4,0.95),(0.35,-0.3,1.0),(0,0.1,1.12),(-0.15,0.45,0.95),(0.4,0.35,0.9)]: S(0.1,(x,y,z),(1,1,0.6),"white")
    face(0.5,-0.2,0.1,0.07,mouth_dz=0.14,mr=0.07,tongue=False); return {}
def b_blossom():
    Cy(0.05,0.9,(0.2,0,0.45),"dkbrown",(0,rad(-15),0)); Cy(0.04,0.4,(0.45,0,0.5),"dkbrown",(0,rad(50),0))
    for k in range(5): a=k*TAU/5+R90; S(0.2,(0.35*math.cos(a),0,1.0+0.35*math.sin(a)),(1,0.4,1),"pink")
    S(0.14,(0,0,1.0),(1,0.5,1),"yellow"); S(0.1,(0.7,0,0.55),(1,0.5,1),"pink")
    face(1.03,-0.08,0.07,0.05,mouth_dz=0.1,mr=0.05,tongue=False); return {}
def b_snail():
    S(0.35,(0,0.3,0.45),(1,1,1),"gold"); To(0.22,0.08,(0,0.3,0.45),"orange",(0,R90,0)); S(0.25,(0,-0.3,0.25),(0.8,1.6,0.6),"mint"); S(0.2,(0,-0.75,0.4),(1,1,1),"mint")
    for sx in (-1,1): Cy(0.025,0.3,(sx*0.1,-0.8,0.65),"mint",(rad(-15),rad(sx*15),0))
    eyes(0.82,-0.84,0.13,0.07); smile(0.3,-0.9,0.07,tongue=False); return {}
def b_daisy():
    Cy(0.04,1.0,(0,0,0.5),"green"); S(0.22,(0,0,1.15),(1,0.5,1),"yellow")
    for k in range(10): a=k*TAU/10; S(0.14,(0.36*math.cos(a),0,1.15+0.36*math.sin(a)),(1.3,0.3,0.7),"white",rot=(0,-a,0))
    face(1.19,-0.12,0.08,0.05,mouth_dz=0.11,mr=0.05,tongue=False); return {}
def b_ladybug(): return b_bug()
def b_cactus():
    Co(0.4,0.5,(0,0,0.25),"orange",r2=0.32,verts=24); Cy(0.42,0.1,(0,0,0.52),"orange",verts=24); Cy(0.25,1.1,(0,0,1.0),"green"); S(0.25,(0,0,1.55),(1,1,0.8),"green")
    for sx in (-1,1): Cy(0.12,0.4,(sx*0.4,0,0.95),"green",(0,R90,0)); Cy(0.12,0.45,(sx*0.5,0,1.15),"green"); S(0.12,(sx*0.5,0,1.38),(1,1,1),"green")
    S(0.12,(0,0,1.75),(1,1,0.8),"hotpink"); face(1.25,-0.24,0.11,0.07,mouth_dz=0.16,mr=0.07,tongue=False); return {}
def b_butterfly():
    Cy(0.08,0.7,(0,0,1.0),"dkgrey"); S(0.12,(0,0,1.4),(1,1,1),"dkgrey")
    for sx in (-1,1):
        S(0.35,(sx*0.4,0,1.2),(1,0.15,0.9),"purple",rot=(0,rad(sx*-10),0)); S(0.25,(sx*0.32,0,0.72),(1,0.15,0.8),"hotpink",rot=(0,rad(sx*10),0))
        S(0.1,(sx*0.45,-0.05,1.25),(1,0.3,1),"yellow"); Cy(0.012,0.3,(sx*0.08,0,1.6),"dkgrey",(0,rad(sx*-25),0)); S(0.03,(sx*0.15,0,1.75),(1,1,1),"dkgrey")
    face(1.42,-0.1,0.06,0.045,mouth_dz=0.09,mr=0.04,tongue=False); return {}
def b_palm():
    for k in range(6): S(0.16,(0.06*k,0,0.15+k*0.28),(1,1,0.7),"brown" if k%2 else "dkbrown")
    for k in range(7): a=k*TAU/7; S(0.5,(0.3+0.45*math.cos(a),0.45*math.sin(a),1.75),(1,0.3,0.12),"green",rot=(0,rad(20),a))
    for k in range(3): S(0.09,(0.3+0.1*math.cos(k*2),0.1*math.sin(k*2),1.6),(1,1,1),"dkbrown")
    face(0.9,-0.14,0.07,0.05,x=0.1,mouth_dz=0.1,mr=0.05,tongue=False); return {}
def b_rainbow():
    cols=["red","orange","yellow","green","blue","purple"]
    for i,c in enumerate(cols):
        ro=1.3-i*0.13; ri=ro-0.13; segs=24
        pts=[(ro*math.cos(math.pi*k/segs),ro*math.sin(math.pi*k/segs)) for k in range(segs+1)]+[(ri*math.cos(math.pi*k/segs),ri*math.sin(math.pi*k/segs)) for k in range(segs,-1,-1)]
        Fp(pts,(0,0,0.0),0.4,c)
    for sx in (-1,1):
        for (dx,dz,r) in [(0,0.1,0.3),(0.3,0.05,0.25),(-0.3,0.05,0.25),(0,0.3,0.25)]: S(r,(sx*1.05+dx,0,0.15+dz),(1,0.8,1),"white")
    face(0.3,-0.3,0.08,0.06,x=-1.05,mouth_dz=0.12,mr=0.06,tongue=False); return {}
def b_hedgehog():
    S(0.45,(0,0.05,0.45),(1,1.2,0.85),"brown"); S(0.3,(0,-0.5,0.4),(0.9,1.1,0.8),"tan"); S(0.07,(0,-0.85,0.42),(1,1,0.9),"black")
    for k in range(26): a=k*2.4; r=0.35; Co(0.05,0.3,(r*math.cos(a)*0.9,0.05+r*math.sin(a)*0.5,0.55+0.3*abs(math.sin(a*0.7))),"dkbrown",(rad(-30)*math.sin(a),rad(30)*math.cos(a),0))
    for (x,y) in [(-0.2,-0.3),(0.2,-0.3),(-0.22,0.3),(0.22,0.3)]: S(0.09,(x,y,0.1),(1,1.2,0.7),"dkbrown")
    face(0.55,-0.72,0.12,0.07,mouth_dz=0.0,mr=0.0,tongue=False); return {}
def b_clover():
    Cy(0.03,0.7,(0,0,0.35),"green")
    for k in range(4): a=k*TAU/4+R90/2; S(0.2,(0.22*math.cos(a),0,0.85+0.22*math.sin(a)),(1,0.4,1),"green")
    S(0.1,(0,-0.02,0.85),(1,0.4,1),"lime"); face(0.88,-0.1,0.07,0.05,mouth_dz=0.1,mr=0.05,tongue=False); return {}
def b_bunny():
    S(0.4,(0,0.05,0.45),(1,1.1,0.9),"white"); S(0.34,(0,-0.3,1.0),(1,1,0.95),"white"); S(0.12,(0,0.45,0.5),(1,1,1),"lgrey")
    for sx in (-1,1): S(0.1,(sx*0.18,-0.25,1.6),(1,0.6,3.2),"white"); S(0.05,(sx*0.18,-0.31,1.6),(1,0.5,2.6),"pink"); S(0.12,(sx*0.22,-0.35,0.12),(1,1.4,0.6),"white")
    S(0.06,(0,-0.62,0.95),(1.2,0.8,0.7),"pink"); face(1.08,-0.6,0.13,0.08,mouth_dz=0.24,mr=0.07); return {}
def b_parrot():
    S(0.35,(0,0,0.9),(0.85,1.0,1.2),"red"); S(0.28,(0,-0.15,1.45),(1,1,1),"red"); Co(0.1,0.28,(0,-0.42,1.4),"gold",(rad(110),0,0))
    for sx in (-1,1): S(0.3,(sx*0.3,0.1,0.95),(0.3,0.8,1),"blue"); S(0.12,(sx*0.3,0.05,0.65),(0.25,0.6,0.8),"green")
    for k in range(3): S(0.1,(0.08*(k-1),0.3,0.3),(0.4,0.5,1.8),["blue","green","yellow"][k])
    S(0.08,(0,-0.05,1.75),(1,1,1.5),"yellow"); legs2("grey",0,0.3,0.03,0.12,foot="grey"); eyes(1.52,-0.38,0.11,0.07); return {}
def b_watermelon():
    halfdisc((0,0,0.0),1.0,0.5,"red",flip=True); halfdisc((0,0,0.0),1.0,0.52,"red",flip=True)
    segs=20; pts=[(1.0*math.cos(math.pi*k/segs),1.0*math.sin(math.pi*k/segs)) for k in range(segs+1)]+[(0.88*math.cos(math.pi*k/segs),0.88*math.sin(math.pi*k/segs)) for k in range(segs,-1,-1)]
    Fp(pts,(0,0,0.0),0.54,"green"); pts2=[(0.88*math.cos(math.pi*k/segs),0.88*math.sin(math.pi*k/segs)) for k in range(segs+1)]+[(0.8*math.cos(math.pi*k/segs),0.8*math.sin(math.pi*k/segs)) for k in range(segs,-1,-1)]
    Fp(pts2,(0,0,0.0),0.53,"cream")
    for k in range(7): a=0.4+k*0.38; S(0.05,(0.55*math.cos(a),-0.27,0.55*math.sin(a)),(1,0.5,1.5),"black")
    face(0.35,-0.28,0.15,0.08,mouth_dz=0.2,mr=0.08,tongue=False); return {}
def b_peacock():
    halfdisc((0,0.3,0.4),1.3,0.15,"teal",flip=False)
    for k in range(7): a=math.pi*(k+0.5)/7; S(0.13,(1.0*math.cos(a),0.2,0.4+1.0*math.sin(a)),(1,0.4,1),"blue"); S(0.06,(1.0*math.cos(a),0.15,0.4+1.0*math.sin(a)),(1,0.4,1),"gold")
    S(0.35,(0,-0.1,0.6),(0.8,1,1.1),"blue"); S(0.22,(0,-0.2,1.25),(1,1,1),"blue"); Co(0.06,0.2,(0,-0.4,1.2),"gold",(R90,0,0))
    for k in range(3): Cy(0.012,0.3,(0.1*(k-1),-0.2,1.55),"blue",(0,rad((k-1)*20),0)); S(0.04,(0.15*(k-1),-0.2,1.7),(1,1,1),"gold")
    legs2("gold",0,0.2,0.025,0.12,foot="gold"); eyes(1.3,-0.4,0.1,0.06); return {}
def b_hibiscus():
    Cy(0.04,0.8,(0,0,0.4),"green"); S(0.25,(0.2,0,0.4),(1.3,0.3,0.6),"green",rot=(0,rad(30),0))
    for k in range(5): a=k*TAU/5+R90; S(0.32,(0.4*math.cos(a),0,1.1+0.4*math.sin(a)),(1,0.3,1),"hotpink",rot=(0,-a,0))
    Cy(0.04,0.5,(0,-0.2,1.1),"yellow",(R90,0,0)); S(0.08,(0,-0.45,1.1),(1,1,1),"gold"); S(0.2,(0,0.02,1.1),(1,0.3,1),"red")
    face(1.2,-0.1,0.1,0.06,mouth_dz=0.0,mr=0.0,tongue=False); return {}
def b_turtle():
    S(0.65,(0,0,0.5),(1,1.15,0.6),"dkgreen"); S(0.5,(0,0,0.55),(1,1.1,0.5),"green")
    for (x,y) in [(0,0),(-0.3,-0.25),(0.3,-0.25),(-0.3,0.3),(0.3,0.3),(0,0.45),(0,-0.45)]: S(0.14,(x,y,0.83-0.1*abs(x)-0.08*abs(y)),(1,1,0.5),"lime")
    S(0.28,(0,-0.75,0.45),(1,1,0.9),"lime"); S(0.12,(0,0.8,0.3),(1,1.4,0.8),"lime")
    for (x,y) in [(-0.5,-0.45),(0.5,-0.45),(-0.5,0.45),(0.5,0.45)]: S(0.14,(x,y,0.18),(1,1.3,0.6),"lime")
    face(0.55,-0.98,0.12,0.07,mouth_dz=0.18,mr=0.07,tongue=False); return {}

def act_wave(h):
    l,r=h["arms"]; sine(r,"rotation_euler",1,rad(30),3,base=rad(-150))
    keys(l,"rotation_euler",[(1,(0,rad(30),0)),(12,(0,rad(40),0)),(24,(0,rad(30),0))])
    for f in range(1,NFRAMES+2):
        t=(f-1)/NFRAMES; s=1+0.02*math.sin(TAU*2*t); ROOT.scale=(s,s,2-s); kf(ROOT,"scale",f)
    for i,w in enumerate(h["wings"]): sine(w,"rotation_euler",1,rad(22)*(1 if i==0 else -1),4)
def act_think(h):
    l,r=h["arms"]
    keys(ROOT,"rotation_euler",[(1,(0,0,0)),(8,(rad(-4),rad(14),0)),(16,(rad(-4),rad(14),0)),(24,(0,0,0))])
    keys(l,"rotation_euler",[(1,(0,rad(30),0)),(8,(rad(-95),rad(35),0)),(16,(rad(-95),rad(35),0)),(24,(0,rad(30),0))])
    keys(r,"rotation_euler",[(1,(0,rad(-30),0)),(12,(0,rad(-38),0)),(24,(0,rad(-30),0))])
    for i,w in enumerate(h["wings"]): sine(w,"rotation_euler",1,rad(18)*(1 if i==0 else -1),4)
ACTS["wave"]=act_wave; ACTS["think"]=act_think
def _mascot_sleep():
    for body,size,loc,rz in (("z z",0.35,(0.55,-0.2,2.1),-20),("Z",0.5,(0.95,-0.2,2.45),-25)):
        fz=bpy.data.curves.new("Zz",'FONT'); fz.body=body; fz.size=size; fz.extrude=0.02
        t=bpy.data.objects.new("Zz",fz); scene.collection.objects.link(t); t.rotation_euler=(rad(90),0,rad(rz)); t.location=loc; t.data.materials.append(mat("navy")); par(t,ROOT)
_old_b_mascot=b_mascot
def b_mascot():
    h=_old_b_mascot(); h["sleep"]=_mascot_sleep; return h
# ---------------- 20 extra daily objects ----------------
def b_pencil(): return b_pen()
def b_crayon():
    Cy(0.18,1.4,(0,0,0.85),"orange"); Co(0.18,0.4,(0,0,1.75),"orange",r2=0.04); B((0,0,0.85),(0.37,0.37,0.5),"cream",bevel=0.02); B((0,-0.19,0.85),(0.3,0.02,0.3),"orange")
    face(1.15,-0.17,0.1,0.07,mouth_dz=0.14,mr=0.07,tongue=False); return {}
def b_teddy():
    S(0.42,(0,0,0.55),(1,0.9,1.0),"brown"); S(0.34,(0,-0.05,1.15),(1,1,0.95),"brown"); S(0.26,(0,-0.12,0.5),(0.8,0.6,0.8),"tan"); S(0.16,(0,-0.3,1.05),(1,0.7,0.8),"tan"); S(0.06,(0,-0.44,1.1),(1.2,0.8,0.8),"black")
    for sx in (-1,1): S(0.13,(sx*0.28,-0.05,1.42),(1,0.6,1),"brown"); S(0.07,(sx*0.28,-0.1,1.42),(1,0.5,1),"tan"); S(0.14,(sx*0.45,-0.1,0.6),(0.7,0.7,1.3),"brown",rot=(0,rad(sx*20),0)); S(0.16,(sx*0.25,-0.15,0.15),(1,1.3,0.7),"brown")
    B((0,-0.28,0.8),(0.5,0.06,0.1),"red",bevel=0.02); S(0.07,(0,-0.33,0.8),(1,0.6,1),"red")
    face(1.22,-0.34,0.13,0.08,mouth_dz=0.3,mr=0.0,tongue=False); return {}
def b_trophy():
    Cy(0.45,0.15,(0,0,0.08),"dkbrown",verts=24); Cy(0.3,0.12,(0,0,0.21),"dkbrown",verts=24); Cy(0.1,0.35,(0,0,0.42),"gold"); Co(0.5,0.9,(0,0,1.05),"gold",(rad(180),0,0),r2=0.18); Cy(0.52,0.06,(0,0,1.5),"gold",verts=32)
    for sx in (-1,1): To(0.22,0.05,(sx*0.6,0,1.1),"gold",(R90,0,0))
    B((0,-0.31,0.21),(0.3,0.02,0.08),"gold"); Fp(starpts(0.12,0.05),(0,-0.48,1.0),0.02,"yellow")
    face(1.25,-0.47,0.17,0.09,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.75,-0.4,0.09,tongue=False); return {}
def b_medal():
    B((0,0,1.55),(0.5,0.06,0.5),"red",bevel=0.02); B((-0.18,-0.01,1.55),(0.12,0.06,0.5),"white"); B((0.18,-0.01,1.55),(0.12,0.06,0.5),"white")
    Cy(0.55,0.12,(0,0,0.75),"gold",(R90,0,0),verts=32); To(0.5,0.04,(0,-0.07,0.75),"orange",(R90,0,0)); Fp(starpts(0.3,0.13),(0,-0.08,0.55),0.03,"orange")
    face(0.9,-0.08,0.2,0.1,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.7,-0.1,0.09,tongue=False); return {}
def b_crown():
    Cy(0.6,0.5,(0,0,0.3),"gold",verts=10); To(0.6,0.06,(0,0,0.06),"orange")
    for k in range(10):
        a=k*TAU/10; Co(0.14,0.4,(0.6*math.cos(a),0.6*math.sin(a),0.72),"gold",verts=4)
        if k%2==0: S(0.08,(0.6*math.cos(a),0.6*math.sin(a),0.95),(1,1,1),["red","blue","green","purple","sky"][k//2])
        S(0.09,(0.62*math.cos(a+0.3),0.62*math.sin(a+0.3),0.3),(1,1,1),"red" if k%2 else "blue")
    face(0.4,-0.6,0.2,0.1,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.2,-0.62,0.1,tongue=False); return {}
def b_gem():
    Co(0.7,0.5,(0,0,1.0),"hotpink",r2=0.0,verts=8); Co(0.7,0.4,(0,0,1.55),"hotpink",(rad(180),0,0),r2=0.0,verts=8); Cy(0.7,0.1,(0,0,1.3),"hotpink",verts=8)
    for k in range(3): S(0.05,(0.3*math.cos(k*2),-0.35,1.4+0.1*k),(1,1,1),"white")
    face(1.35,-0.62,0.2,0.1,mouth_dz=0.26,mr=0.1); return {}
def b_shell():
    for i in range(6): r=0.55-i*0.08; S(r,(0.12*i,0,0.5+0.1*i),(1,0.7,1),"peach" if i%2 else "cream")
    for k in range(7): a=-0.4+k*0.3; Cy(0.03,0.9,(0.5*math.sin(a),0,0.5+0.5*math.cos(a)),"peach",(0,a,0))
    face(0.8,-0.4,0.17,0.09,mouth_dz=0.24,mr=0.09); return {}
def b_seashell():
    Fp([(0,0)]+[(0.8*math.cos(math.pi*i/12),0.8*math.sin(math.pi*i/12)) for i in range(13)],(0,0,0.2),0.35,"pink")
    for k in range(9): a=math.pi*(k+0.5)/9; Cy(0.05,0.8,(0.4*math.cos(a),-0.18,0.2+0.4*math.sin(a)),"hotpink",(0,-a+R90,0))
    S(0.15,(0,0,0.2),(1,1,0.8),"hotpink"); face(0.6,-0.2,0.17,0.09,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.4,-0.22,0.09,tongue=False); return {}
def b_feather():
    S(0.55,(0,0,1.0),(0.45,0.12,1.0),"sky"); S(0.35,(0,0,1.75),(0.35,0.1,0.5),"sky"); Cy(0.03,2.1,(0,-0.1,1.0),"white"); Cy(0.04,0.6,(0,0,0.0),"white")
    for k in range(5): Cy(0.012,0.5,(0,-0.13,1.5-k*0.25),"white",(0,rad(50),0)); Cy(0.012,0.5,(0,-0.13,1.5-k*0.25),"white",(0,rad(-50),0))
    face(1.25,-0.14,0.1,0.07,mouth_dz=0.15,mr=0.07,tongue=False); return {}
def b_acorn(): return b_nut()
def b_pinecone():
    for i in range(6):
        r=0.45-abs(i-2)*0.07; z=0.3+i*0.26
        for k in range(8): a=k*TAU/8+(i%2)*0.4; S(0.14,(r*math.cos(a),r*math.sin(a),z),(1,1,0.6),"brown",rot=(0,rad(40),a))
    S(0.3,(0,0,1.0),(1,1,2.0),"dkbrown"); S(0.1,(0,0,1.95),(1,1,1),"dkbrown")
    face(1.3,-0.45,0.15,0.09,mouth_dz=0.22,mr=0.09); return {}
def b_donut():
    To(0.6,0.28,(0,0,0.3),"tan"); To(0.6,0.26,(0,0,0.36),"hotpink",scale=(1,1,0.6))
    for k in range(14): a=k*1.9; S(0.03,(0.6*math.cos(a)+0.15*math.sin(k),0.6*math.sin(a)+0.15*math.cos(k),0.62),(1,1,2.5),["yellow","sky","white","lime"][k%4],rot=(0,0,k))
    face(0.4,-0.88,0.17,0.09,mouth_dz=0.0,mr=0.0,tongue=False); smile(0.22,-0.9,0.09,tongue=False); return {}
def b_lollipop():
    Cy(0.04,1.2,(0,0,0.6),"white"); Cy(0.5,0.16,(0,0,1.6),"hotpink",(R90,0,0),verts=32)
    for k in range(3): To(0.14+k*0.15,0.03,(0,-0.09,1.6),"white",(R90,0,0))
    face(1.7,-0.1,0.17,0.09,mouth_dz=0.24,mr=0.09); return {}
def b_icecream():
    Co(0.35,0.9,(0,0,0.45),"tan",(rad(180),0,0)); S(0.4,(0,0,1.1),(1,1,0.9),"pink"); S(0.33,(0,0,1.55),(1,1,0.9),"mint"); S(0.06,(0,0,1.9),(1,1,1),"red")
    for k in range(5): S(0.03,(0.25*math.cos(k*1.3),-0.25*abs(math.sin(k*1.3)),1.2+0.1*k),(1,1,1),["red","yellow","blue","green","purple"][k])
    face(1.15,-0.37,0.16,0.09,mouth_dz=0.22,mr=0.09); return {}
def b_pretzel():
    To(0.5,0.13,(0,0,0.7),"brown",(R90,0,0)); To(0.3,0.12,(-0.25,0,0.9),"brown",(R90,0,0)); To(0.3,0.12,(0.25,0,0.9),"brown",(R90,0,0)); To(0.3,0.12,(0,0,0.45),"brown",(R90,0,0))
    for k in range(12): S(0.035,(0.5*math.cos(k*0.52),-0.12,0.7+0.5*math.sin(k*0.52)),(1,1,1.6),"white",rot=(0,k,0))
    face(0.9,-0.14,0.1,0.065,mouth_dz=0.12,mr=0.06,tongue=False); return {}

ACTS["none"] = lambda h: None
def act_walk(h):
    sine(ROOT, "location", 2, 0.06, 2, phase=0); sine(ROOT, "rotation_euler", 0, rad(-3), 2, phase=1.0); sine(ROOT, "rotation_euler", 1, rad(4), 1)
    for i, l in enumerate(h.get("legs", [])): sine(l, "rotation_euler", 0, rad(25), 2, phase=math.pi * (i % 2))
ACTS["walk"] = act_walk
_old_butterfly = b_butterfly
def b_butterfly():
    Cy(0.08,0.7,(0,0,1.0),"dkgrey"); S(0.12,(0,0,1.4),(1,1,1),"dkgrey"); wings=[]
    for sx in (-1,1):
        p=E((sx*0.06,0,1.1)); wings.append(p)
        S(0.35,(sx*0.4,0,1.2),(1,0.15,0.9),"purple",p,rot=(0,rad(sx*-10),0)); S(0.25,(sx*0.32,0,0.72),(1,0.15,0.8),"hotpink",p,rot=(0,rad(sx*10),0))
        S(0.1,(sx*0.45,-0.05,1.25),(1,0.3,1),"yellow",p)
        Cy(0.012,0.3,(sx*0.08,0,1.6),"dkgrey",(0,rad(sx*-25),0)); S(0.03,(sx*0.15,0,1.75),(1,1,1),"dkgrey")
    face(1.42,-0.1,0.06,0.045,mouth_dz=0.09,mr=0.04,tongue=False); return {"wings":wings,"flap":45}
def b_ladybug():
    S(0.5,(0,0,0.4),(1,1.2,0.7),"red"); S(0.26,(0,-0.5,0.4),(1,1,0.8),"black"); wings=[]
    for sx in (-1,1):
        p=E((sx*0.02,0.1,0.72)); wings.append(p)
        S(0.48,(sx*0.26,0.1,0.45),(0.52,1.15,0.65),"red",p)
        for (x,y) in [(0.25,-0.1),(0.3,0.3),(0.12,0.45)]: S(0.09,(sx*x,y,0.72),(1,1,0.4),"black",p)
        Cy(0.012,0.3,(sx*0.1,-0.7,0.6),"black",(rad(-40),rad(sx*20),0)); S(0.03,(sx*0.17,-0.78,0.72),(1,1,1),"black")
        for k in range(3): Cy(0.02,0.3,(sx*0.45,-0.1+k*0.2,0.15),"black",(0,rad(-sx*50),0))
    B((0,0.1,0.75),(0.03,1.0,0.1),"black"); face(0.5,-0.72,0.11,0.07,mouth_dz=0.14,mr=0.07,tongue=False); return {"wings":wings,"flap":30}
def b_seedling():
    Cy(0.035,0.45,(0,0,0.22),"green"); S(0.12,(0,0,0.5),(1,0.8,1),"lime")
    for sx in (-1,1): S(0.16,(sx*0.2,0,0.4),(1.2,0.35,0.6),"green",rot=(0,rad(sx*-35),0))
    face(0.54,-0.1,0.07,0.045,mouth_dz=0.09,mr=0.045,tongue=False); return {}
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}


