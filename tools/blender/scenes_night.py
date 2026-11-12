import bpy, math, random
from mathutils import Vector
SC = "__SCENE__"; OUT = "__OUT__"
NIGHT = SC.endswith("_night"); XMAS = False; BASE = SC.replace("_night", ""); LEVEL = 1
if BASE.startswith("island_"): LEVEL = int(BASE.split("_")[1]); BASE = "island"
import os; os.makedirs(OUT, exist_ok=True)
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras, bpy.data.curves, bpy.data.worlds):
    for d in list(coll):
        if d.users == 0: coll.remove(d)
scene = bpy.context.scene; rad = math.radians; TAU = math.tau; random.seed(7)
def mat(rgb, rough=0.8, emit=0.0):
    m = bpy.data.materials.new("m"); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    for k in ("Specular IOR Level", "Specular"):
        if k in b.inputs: b.inputs[k].default_value = 0.1
    if emit: b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = emit
    return m
def grad_mat(c_bottom, c_top, z0, z1):
    m = bpy.data.materials.new("sky"); m.use_nodes = True; nt = m.node_tree; nodes = nt.nodes; links = nt.links
    for n in list(nodes): nodes.remove(n)
    out = nodes.new("ShaderNodeOutputMaterial"); em = nodes.new("ShaderNodeEmission"); ramp = nodes.new("ShaderNodeValToRGB")
    geo = nodes.new("ShaderNodeNewGeometry"); sep = nodes.new("ShaderNodeSeparateXYZ"); mr = nodes.new("ShaderNodeMapRange")
    links.new(geo.outputs["Position"], sep.inputs[0]); links.new(sep.outputs["Z"], mr.inputs[0]); mr.inputs[1].default_value = z0; mr.inputs[2].default_value = z1
    links.new(mr.outputs[0], ramp.inputs[0]); ramp.color_ramp.elements[0].color = (*c_bottom, 1); ramp.color_ramp.elements[1].color = (*c_top, 1)
    links.new(ramp.outputs[0], em.inputs[0]); em.inputs[1].default_value = 1.0; links.new(em.outputs[0], out.inputs[0]); return m
def smooth(o):
    for p in o.data.polygons: p.use_smooth = True
def S(r, loc, scale=(1,1,1), m=None, rot=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=14, radius=r, location=loc); o = bpy.context.active_object; o.scale = scale
    if rot: o.rotation_euler = rot
    o.data.materials.append(m); smooth(o); return o
def B(loc, scale, m, rot=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.active_object; o.scale = scale
    if rot: o.rotation_euler = rot
    o.data.materials.append(m); return o
def Cy(r, d, loc, m, rot=(0,0,0), verts=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=loc, rotation=rot); o = bpy.context.active_object; o.data.materials.append(m); smooth(o); return o
def Co(r, d, loc, m, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=r, depth=d, location=loc, rotation=rot); o = bpy.context.active_object; o.data.materials.append(m); smooth(o); return o
def To(R, r, loc, m, rot=(0,0,0), scale=(1,1,1)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot, major_segments=40, minor_segments=12); o = bpy.context.active_object; o.scale = scale; o.data.materials.append(m); smooth(o); return o
def plane(loc, sx, sy, m, rot=(0,0,0)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot); o = bpy.context.active_object; o.scale = (sx, sy, 1); o.data.materials.append(m); return o
def cloud(x, y, z, s=1.0, m=None):
    for (dx, dz, r) in [(0,0,0.9),(-1.0,-0.1,0.65),(1.0,-0.1,0.7),(0.4,0.5,0.6),(-0.5,0.4,0.55)]: S(r*s, (x+dx*s, y, z+dz*s), (1, 0.6, 1), m)
def tree(x, y, s=1.0, leaf=(0.35,0.7,0.3), trunk=(0.5,0.32,0.15)):
    Cy(0.18*s, 1.4*s, (x, y, 0.7*s), mat(trunk)); S(0.9*s, (x, y, 1.9*s), (1,1,0.9), mat(leaf)); S(0.6*s, (x-0.6*s, y, 1.5*s), (1,1,1), mat(leaf)); S(0.6*s, (x+0.6*s, y, 1.6*s), (1,1,1), mat(leaf))
def star_dots(n, zmin, zmax, y=60, spread=40, r=0.12, col=(1,1,0.9)):
    m = mat(col, 0.5, 4.0)
    for k in range(n): S(r*random.uniform(0.6,1.4), (random.uniform(-spread, spread), y - random.uniform(0, 5), random.uniform(zmin, zmax)), (1,1,1), m, None)
# ---------- camera / common ----------
scene.render.resolution_x, scene.render.resolution_y = 1200, 750; scene.render.resolution_percentage = 100
cd = bpy.data.cameras.new("C"); cd.lens = 35; cd.sensor_width = 36
cam = bpy.data.objects.new("Cam", cd); scene.collection.objects.link(cam); cam.location = (0, -9, 2.4); cam.rotation_euler = (rad(99), 0, 0); scene.camera = cam
world = bpy.data.worlds.new("W"); scene.world = world; world.use_nodes = True
sun = bpy.data.lights.new("Sun", 'SUN'); sun.energy = 3.0; sun.angle = rad(10); so = bpy.data.objects.new("Sun", sun); scene.collection.objects.link(so); so.rotation_euler = (rad(50), rad(15), rad(-30))
def sky(c_bottom, c_top, ambient=(0.7,0.75,0.85), strength=0.6):
    plane((0, 90, 25), 400, 110, grad_mat(c_bottom, c_top, -20, 70), (rad(90), 0, 0))
    bg = world.node_tree.nodes.get("Background"); bg.inputs[0].default_value = (*ambient, 1); bg.inputs[1].default_value = strength
def ground(col, depth=100):
    plane((0, depth/2 - 2, 0), 400, depth, mat(col))
if BASE == "meadow":
    sky((0.75, 0.9, 1.0), (0.4, 0.7, 1.0)); ground((0.5, 0.8, 0.35))
    for (x, y, r) in [(-14, 40, 9), (12, 45, 11), (-2, 55, 10), (22, 38, 8)]: S(r, (x, y, -r*0.55), (1, 0.7, 1), mat((0.45, 0.75, 0.35)))
    tree(-7, 12, 1.6); tree(7.5, 14, 1.4); tree(-12, 20, 2.0); tree(13, 22, 1.8)
    for k in range(24):
        x = random.choice([-1, 1]) * random.uniform(2.5, 9); y = random.uniform(2, 12); c = random.choice([(1,0.4,0.5),(1,0.85,0.2),(1,1,1),(0.7,0.5,1)])
        Cy(0.03, 0.3, (x, y, 0.15), mat((0.3,0.6,0.25))); S(0.12, (x, y, 0.33), (1,1,0.6), mat(c))
    cm = mat((1,1,1), 0.9); cloud(-9, 50, 14, 1.6, cm); cloud(10, 55, 17, 1.9, cm); cloud(2, 60, 20, 1.4, cm)
    S(1.6, (-13, 70, 24), (1,1,1), mat((1, 0.95, 0.6), 0.5, 3.0))
elif BASE == "sea":   # underwater
    sky((0.25, 0.65, 0.85), (0.1, 0.35, 0.7), (0.3, 0.6, 0.8), 0.9); ground((0.9, 0.82, 0.6))
    sun.energy = 2.0
    for (x, y, h, c) in [(-8, 8, 3.5, (0.2,0.6,0.3)), (-6.5, 12, 4.5, (0.3,0.7,0.35)), (9, 9, 4, (0.2,0.6,0.3)), (11, 14, 5, (0.3,0.7,0.35)), (-12, 20, 6, (0.25,0.65,0.3)), (14, 22, 6, (0.25,0.65,0.3))]:
        for k in range(5): S(0.35, (x + 0.35*math.sin(k*1.2), y, 0.4 + k*h/5), (1, 0.4, 1.3), mat(c), (0, rad(10*math.sin(k*1.2)), 0))
    for (x, y, r) in [(-9, 6, 1.2), (8, 5, 1.0), (-14, 15, 2.2), (15, 16, 2.4), (-13, 30, 3), (14, 34, 3)]: S(r, (x, y, r*0.35), (1.2, 1, 0.7), mat((0.6, 0.6, 0.65)))
    bm = mat((0.85, 0.95, 1.0), 0.2, 0.5)
    for k in range(30): S(random.uniform(0.08, 0.25), (random.uniform(-16, 16), random.uniform(5, 40), random.uniform(2, 12)), (1,1,1), bm)
    for k in range(6): S(0.5, (random.uniform(-16, 16), random.uniform(25, 45), random.uniform(4, 10)), (1.6, 0.5, 0.9), mat(random.choice([(1,0.6,0.2),(1,0.9,0.3),(0.9,0.4,0.6)])))
    for (x, y) in [(-11, 10), (12, 12)]:
        for k in range(5): a = k*0.6-1.2; Cy(0.12, 2.5, (x + 1.2*math.sin(a), y, 1.2), mat((1, 0.5, 0.55)), (0, a, 0))
elif BASE == "sky":
    sky((0.8, 0.92, 1.0), (0.35, 0.65, 1.0)); ground((0.95, 0.97, 1.0))
    cm = mat((1, 1, 1), 0.9)
    for (x, y, s) in [(-9, 4, 2.0), (-3, 6, 1.8), (4, 5, 2.2), (10, 6, 1.9), (-14, 10, 2.6), (15, 11, 2.4), (0, 14, 2.5), (-7, 18, 3), (8, 20, 3)]: cloud(x, y, 0.3*s, s, cm)
    cloud(-10, 45, 13, 1.6, cm); cloud(11, 50, 16, 2.0, cm); cloud(0, 60, 22, 1.5, cm); cloud(-16, 55, 20, 1.8, cm)
    S(1.8, (13, 70, 26), (1,1,1), mat((1, 0.95, 0.6), 0.5, 3.0))
    for (x, z) in [(-12, 18), (-10.5, 18.6), (-9, 18.2), (14, 21), (15.5, 21.5)]:
        for sx in (-1, 1): B((x + sx*0.35, 50, z + 0.15), (0.7, 0.05, 0.08), mat((0.2,0.2,0.3)), (0, rad(sx*-25), 0))
elif BASE == "road":
    sky((0.8, 0.9, 1.0), (0.45, 0.7, 1.0)); ground((0.5, 0.78, 0.35))
    plane((0, 48, 0.02), 9, 100, mat((0.42, 0.43, 0.48)))
    for k in range(25): B((0, 1 + k*4, 0.04), (0.3, 1.6, 0.02), mat((1, 0.9, 0.3)))
    for sx in (-1, 1):
        plane((sx*4.8, 48, 0.03), 0.6, 100, mat((0.85, 0.85, 0.85)))
        for k, (y, h, c) in enumerate([(10, 3, (1, 0.6, 0.5)), (16, 4.5, (0.6, 0.8, 1)), (24, 3.5, (1, 0.85, 0.5)), (34, 5, (0.8, 0.7, 1))]):
            x = sx * (8 + (k % 2)*2); B((x, y, h/2), (3.5, 3.5, h), mat(c)); Co(2.6, 1.6, (x, y, h + 0.8), mat((0.8, 0.3, 0.25)))
            for wz in range(int(h) - 1): B((x - sx*1.8, y, 1.2 + wz), (0.08, 0.8, 0.8), mat((0.95, 0.95, 0.7), 0.3, 0.3))
        tree(sx*7, 5, 1.3); tree(sx*12, 29, 1.6)
    cm = mat((1,1,1), 0.9); cloud(-8, 55, 16, 1.7, cm); cloud(9, 60, 19, 1.5, cm)
elif BASE == "space":
    sky((0.15, 0.1, 0.35), (0.03, 0.02, 0.1), (0.2, 0.15, 0.35), 0.5); ground((0.55, 0.55, 0.62))
    sun.energy = 2.5; so.rotation_euler = (rad(55), rad(-20), rad(30))
    star_dots(160, 6, 60)
    for (x, y, r) in [(-7, 6, 1.0), (6, 9, 1.3), (-13, 14, 1.8), (12, 18, 1.5), (-3, 25, 2)]: To(r, 0.25, (x, y, 0.0), mat((0.45, 0.45, 0.52)), scale=(1, 1, 0.6))
    S(3.5, (-13, 55, 20), (1,1,1), mat((1.0, 0.6, 0.3), 0.7)); To(5.5, 0.5, (-13, 55, 20), mat((1.0, 0.85, 0.6)), (rad(70), 0, rad(20)), (1,1,0.3))
    S(2.2, (13, 50, 14), (1,1,1), mat((0.4, 0.8, 1.0), 0.7)); S(1.2, (16, 45, 24), (1,1,1), mat((0.8, 0.8, 0.85), 0.8))
    for k in range(6): a = k; S(0.4, (13 + 2.6*math.cos(a), 50, 14 + 1.0*math.sin(a)), (1,1,1), mat((0.3, 0.6, 0.9), 0.7))
elif BASE == "island":
    sky((0.85, 0.95, 1.0), (0.3, 0.65, 1.0)); ground((0.98, 0.9, 0.62), 30)
    sun.energy = 3.4
    # sea beyond the beach, with a lighter shallow band and foam
    plane((0, 75, -0.02), 400, 95, mat((0.15, 0.55, 0.9), 0.3)); plane((0, 30.5, -0.01), 400, 5, mat((0.4, 0.8, 0.95), 0.3))
    for k in range(10): S(random.uniform(0.6, 1.2), (random.uniform(-30, 30), 28 + random.uniform(-0.6, 0.6), 0.0), (1, 0.35, 0.12), mat((1, 1, 1), 0.9))
    for k in range(14): B((random.uniform(-40, 40), random.uniform(36, 70), 0.0), (random.uniform(1.5, 3.5), 0.12, 0.05), mat((0.7, 0.9, 1.0), 0.3))
    # distant islet with volcano + smoke
    S(9, (14, 48, -4.5), (1, 0.7, 1), mat((0.3, 0.6, 0.3))); Co(6.5, 9.0, (14, 48, 4.4), mat((0.45, 0.35, 0.3))); Co(1.6, 1.0, (14, 48, 8.9), mat((0.95, 0.4, 0.15), 0.5, 1.5))
    for k in range(4): S(1.0 + 0.4*k, (14 + 0.6*k, 47 - 0.5*k, 10 + 1.5*k), (1, 0.8, 0.8), mat((0.85, 0.85, 0.9), 0.9))
    S(7, (-20, 50, -4), (1, 0.7, 1), mat((0.32, 0.62, 0.32)))
    # palms
    def palm(x, y, s=1.0, lean=0.0):
        for k in range(7): Cy(0.17*s*(1 - 0.05*k), 0.8*s, (x + lean*k*0.12*s, y, 0.3*s + k*0.62*s), mat((0.6, 0.42, 0.22)), (0, rad(-lean*8), 0))
        top = (x + lean*0.8*s, y, 4.5*s)
        for k in range(7):
            a = k*TAU/7; o = S(1.1*s, (top[0] + 1.3*s*math.cos(a), top[1] + 1.3*s*math.sin(a), top[2] - 0.35*s), (1.0, 0.32, 0.12), mat((0.25, 0.65, 0.3)), (0, rad(-22), a))
        for k in range(3): S(0.22*s, (top[0] + 0.25*s*math.cos(k*2.1), top[1] + 0.25*s*math.sin(k*2.1), top[2] - 0.2*s), (1,1,1), mat((0.5, 0.32, 0.15)))
    palm(-8.5, 9, 1.5, 0.6); palm(9.5, 11, 1.3, -0.5); palm(-13, 17, 1.7, 0.3); palm(14, 19, 1.5, -0.3)
    # rocks, shells, starfish, bushes kept at the sides
    for (x, y, r) in [(-10, 5, 0.9), (-11.5, 6.2, 0.6), (11, 6, 0.8)]: S(r, (x, y, r*0.35), (1, 0.8, 0.6), mat((0.6, 0.6, 0.62)))
    for (x, y) in [(-6.5, 3.2), (7.5, 2.8), (12.5, 4.5)]: S(0.25, (x, y, 0.1), (1, 0.8, 0.45), mat((1.0, 0.8, 0.85)))
    for k in range(5): a = k*TAU/5; S(0.14, (-9 + 0.3*math.cos(a), 2.2 + 0.3*math.sin(a), 0.06), (1.6, 0.7, 0.4), mat((1.0, 0.55, 0.3)), (0, 0, a))
    for (x, y, s) in [(-15, 12, 1.4), (16, 13, 1.2), (-12, 24, 1.5), (13, 25, 1.3)]: S(s, (x, y, s*0.5), (1, 0.8, 0.7), mat((0.3, 0.7, 0.3))); S(s*0.7, (x + s*0.8, y + 0.3, s*0.45), (1, 0.8, 0.7), mat((0.35, 0.75, 0.3)))
    if LEVEL >= 2:   # waterfall on the left hill + ferns
        S(4.5, (-7, 27, -1.0), (1, 0.8, 1.1), mat((0.3, 0.62, 0.3))); B((-6.5, 25, 2.0), (1.6, 1.0, 4.0), mat((0.5, 0.5, 0.55)))
        wm = mat((0.85, 0.95, 1.0), 0.3, 0.3); B((-6.5, 24.3, 2.4), (1.1, 0.25, 4.6), wm); S(0.9, (-6.5, 24.0, 0.25), (1.4, 1.0, 0.35), wm)
        for k in range(8): S(random.uniform(0.2, 0.4), (-6.5 + random.uniform(-0.9, 0.9), 23.6, random.uniform(0.2, 0.7)), (1, 0.7, 0.6), mat((1, 1, 1), 0.9))
        plane((-6.5, 22.5, 0.03), 5, 3, mat((0.4, 0.75, 0.95), 0.3))
        def fern(x, y, s=1.0):
            for k in range(7):
                a = k*TAU/7; S(0.9*s, (x + 0.8*s*math.cos(a), y + 0.8*s*math.sin(a), 0.5*s), (1.0, 0.28, 0.1), mat((0.25, 0.6, 0.25)), (0, rad(-35), a))
        fern(-9.5, 14, 1.2); fern(10.5, 15, 1.1); fern(-15, 10.5, 1.0); fern(15.5, 9.5, 1.3); fern(-3.2, 22, 1.2); fern(4.5, 24, 1.3)
    if LEVEL >= 3:   # second volcano, rainbow, flowers
        S(6, (-18, 46, -3), (1, 0.7, 1), mat((0.3, 0.6, 0.3))); Co(4.5, 6.5, (-18, 46, 3.2), mat((0.42, 0.33, 0.3))); Co(1.1, 0.8, (-18, 46, 6.5), mat((0.95, 0.4, 0.15), 0.5, 1.5))
        for k in range(3): S(0.8 + 0.3*k, (-18 - 0.5*k, 45.5, 7.4 + 1.2*k), (1, 0.8, 0.8), mat((0.85, 0.85, 0.9), 0.9))
        for i, c in enumerate([(1, 0.3, 0.3), (1, 0.6, 0.2), (1, 0.9, 0.3), (0.4, 0.8, 0.4), (0.4, 0.6, 1.0), (0.6, 0.4, 0.9)]):
            To(13 - i*0.55, 0.28, (0, 62, 2), mat(c, 0.8, 0.6), (rad(90), 0, 0))
        for k in range(26):
            x = random.choice([-1, 1]) * random.uniform(3, 14); y = random.uniform(4, 16); c = random.choice([(1,0.4,0.5),(1,0.85,0.2),(1,1,1),(0.7,0.5,1),(1,0.5,0.2)])
            Cy(0.03, 0.3, (x, y, 0.15), mat((0.3,0.6,0.25))); S(0.13, (x, y, 0.33), (1,1,0.6), mat(c))
        for (x, y, s) in [(-7, 24, 1.6), (8, 23, 1.5), (-17, 20, 1.3), (17, 22, 1.4)]: S(s, (x, y, s*0.5), (1, 0.8, 0.7), mat((0.3, 0.72, 0.3)))
        palm(-3, 24, 1.2, 0.4); palm(3.5, 25, 1.1, -0.4)
    cm = mat((1,1,1), 0.9); cloud(-11, 52, 15, 1.7, cm); cloud(6, 58, 19, 1.5, cm); cloud(20, 55, 17, 1.2, cm)
    S(1.7, (-16, 70, 26), (1,1,1), mat((1, 0.95, 0.6), 0.5, 3.0))
elif BASE == "reef":   # coral reef sea floor
    sky((0.3, 0.7, 0.9), (0.08, 0.3, 0.65), (0.3, 0.6, 0.8), 0.9); ground((0.92, 0.85, 0.62))
    sun.energy = 2.2
    def coral(x, y, s, c):
        for k in range(6):
            a = k*TAU/6 + 0.3; Cy(0.14*s, 1.4*s, (x + 0.3*s*math.cos(a), y + 0.3*s*math.sin(a), 0.7*s), mat(c), (rad(22*math.cos(a)), rad(22*math.sin(a)), 0))
            S(0.2*s, (x + 0.75*s*math.cos(a), y + 0.75*s*math.sin(a), 1.35*s), (1, 1, 1), mat(c)); Cy(0.1*s, 0.8*s, (x + 0.75*s*math.cos(a), y + 0.75*s*math.sin(a), 1.7*s), mat(c), (rad(-15*math.cos(a)), rad(-15*math.sin(a)), 0))
        Cy(0.3*s, 1.0*s, (x, y, 0.5*s), mat(c)); S(0.35*s, (x, y, 1.1*s), (1, 1, 1), mat(c))
    def brain(x, y, s, c):
        S(s, (x, y, s*0.5), (1, 1, 0.7), mat(c))
        for k in range(8): To(s*(0.3 + 0.08*k), s*0.05, (x, y, s*0.5 + 0.1*s*k*(1-k/9)), mat(tuple(v*0.8 for v in c)), scale=(1, 1, 1))
    def anemone(x, y, s, c):
        for k in range(14): a = k*TAU/14; Cy(0.07*s, 1.2*s, (x + 0.35*s*math.cos(a), y + 0.35*s*math.sin(a), 0.6*s), mat(c), (rad(18*math.cos(a+1)), rad(18*math.sin(a+1)), 0)); S(0.1*s, (x + 0.45*s*math.cos(a), y + 0.45*s*math.sin(a), 1.2*s), (1, 1, 1), mat((1, 0.6, 0.7)))
    def weed(x, y, h, c):
        for k in range(6): S(0.3, (x + 0.3*math.sin(k*1.1), y, 0.4 + k*h/6), (1, 0.4, 1.2), mat(c), (0, rad(12*math.sin(k*1.1)), 0))
    coral(-8.5, 14, 1.3, (1.0, 0.45, 0.4)); coral(9.5, 15, 1.2, (1.0, 0.6, 0.2)); coral(-13.5, 22, 1.6, (0.95, 0.35, 0.6)); coral(14, 24, 1.5, (0.6, 0.4, 0.9)); coral(0, 26, 1.4, (1.0, 0.5, 0.7))
    brain(-5, 17, 1.5, (0.95, 0.5, 0.3)); brain(6, 18, 1.3, (0.9, 0.7, 0.3)); brain(-11, 30, 2.2, (1.0, 0.45, 0.5)); brain(12, 32, 2.0, (0.5, 0.75, 0.9))
    anemone(-11, 12, 1.2, (0.9, 0.3, 0.6)); anemone(12, 12, 1.0, (0.3, 0.7, 0.6)); anemone(-2.5, 22, 1.5, (0.95, 0.55, 0.2)); anemone(3.5, 23, 1.4, (0.5, 0.4, 0.9))
    weed(-7.5, 16, 4, (0.2, 0.6, 0.35)); weed(8, 17, 4.5, (0.25, 0.65, 0.3)); weed(-16, 15, 5, (0.2, 0.55, 0.3)); weed(17, 16, 5, (0.25, 0.6, 0.35)); weed(-3, 34, 6, (0.2, 0.6, 0.35)); weed(4, 36, 6, (0.2, 0.6, 0.35))
    for (x, y, r) in [(-15, 36, 4), (14, 40, 5), (0, 48, 6), (-6, 42, 3)]: S(r, (x, y, r*0.3), (1.3, 1, 0.6), mat((0.4, 0.5, 0.65)))
    bm = mat((0.85, 0.95, 1.0), 0.2, 0.5)
    for k in range(32): S(random.uniform(0.08, 0.25), (random.uniform(-16, 16), random.uniform(5, 40), random.uniform(2, 13)), (1,1,1), bm)
    for k in range(8): S(0.5, (random.uniform(-16, 16), random.uniform(25, 45), random.uniform(4, 10)), (1.6, 0.5, 0.9), mat(random.choice([(1,0.6,0.2),(1,0.9,0.3),(0.9,0.4,0.6)])))
elif BASE == "room":
    sky((0.8, 0.74, 0.62), (0.8, 0.74, 0.62), (0.7, 0.65, 0.6), 0.5); ground((0.8, 0.6, 0.4))
    plane((0, 22, 10), 60, 22, mat((0.9, 0.8, 0.66)), (rad(90), 0, 0)); sun.energy = 1.8
    for k in range(-12, 13): B((k*1.6, 11, 0.01), (0.06, 24, 0.02), mat((0.6, 0.42, 0.25)))
    B((0, 21.8, 0.4), (60, 0.3, 0.8), mat((1, 1, 1)))
    B((8.5, 21.6, 7.5), (6, 0.3, 6), mat((1, 1, 1))); B((8.5, 21.4, 7.5), (5.4, 0.2, 5.4), mat((0.6, 0.85, 1.0), 0.3, 0.25)); B((8.5, 21.3, 7.5), (0.25, 0.1, 5.4), mat((1,1,1))); B((8.5, 21.3, 7.5), (5.4, 0.1, 0.25), mat((1,1,1)))
    B((11.8, 21.2, 7.5), (1.0, 0.1, 6.6), mat((1, 0.6, 0.6))); B((5.2, 21.2, 7.5), (1.0, 0.1, 6.6), mat((1, 0.6, 0.6)))
    B((-9, 20.5, 4), (5, 1.6, 8), mat((0.75, 0.55, 0.35)))
    for sz in range(4):
        for k in range(6): B((-11 + k*0.75, 20.3, 1.2 + sz*2), (0.55, 1.2, 1.3), mat(random.choice([(0.9,0.3,0.3),(0.3,0.5,0.9),(0.3,0.7,0.4),(0.95,0.75,0.2),(0.7,0.4,0.8)])))
    B((-3.5, 20.6, 1.4), (1.5, 1.0, 2.8), mat((0.9, 0.9, 0.95))); S(0.45, (-3.5, 20.6, 3.0), (1,1,1), mat((0.4, 0.8, 0.4)))
    Cy(0.12, 6, (13, 19, 3), mat((0.3, 0.3, 0.35))); Co(1.6, 1.6, (13, 19, 6.8), mat((1, 0.85, 0.5), 0.8, 0.6))
elif BASE == "night":
    sky((0.12, 0.15, 0.4), (0.03, 0.03, 0.15), (0.15, 0.15, 0.35), 0.5); ground((0.12, 0.3, 0.2))
    sun.energy = 1.2; sun.color = (0.7, 0.8, 1.0)
    star_dots(120, 8, 60)
    S(2.2, (12, 60, 24), (1,1,1), mat((1.0, 0.98, 0.8), 0.6, 2.5))
    for (x, y, s) in [(-7, 12, 1.5), (-12, 18, 2.0), (8, 14, 1.6), (13, 20, 2.1), (-16, 26, 2.4), (17, 28, 2.3)]: tree(x, y, s, (0.1, 0.3, 0.2), (0.2, 0.15, 0.1))
    for (x, y, r) in [(-10, 40, 9), (9, 44, 10), (0, 52, 11)]: S(r, (x, y, -r*0.6), (1, 0.7, 1), mat((0.1, 0.25, 0.2)))
    fm = mat((1, 0.95, 0.4), 0.3, 6.0)
    for k in range(18): S(0.09, (random.uniform(-12, 12), random.uniform(3, 20), random.uniform(0.5, 3.5)), (1,1,1), fm)

if XMAS:
    sun.energy = max(sun.energy, 2.8)
    snow = mat((0.97, 0.98, 1.0), 0.9)
    if BASE not in ("sea",): plane((0, 8, 0.012), 400, 20, snow)                       # snowy ground near the front
    for ob in [o for o in list(bpy.data.objects) if o.type == 'MESH' and o.scale.z > 0.3 and o.location.y < 40 and o.location.z > 0.8 and o.dimensions.z > 1.0]:
        d = ob.dimensions; S(max(d.x, d.y)*0.3, (ob.location.x, ob.location.y, ob.location.z + d.z*0.45), (1, 1, 0.3), snow)   # snow caps
    def snowman(x, y, s=1.0):
        S(0.9*s, (x, y, 0.8*s), (1, 1, 1), snow); S(0.65*s, (x, y, 2.0*s), (1, 1, 1), snow); S(0.45*s, (x, y, 2.9*s), (1, 1, 1), snow)
        Co(0.1*s, 0.5*s, (x, y - 0.6*s, 2.9*s), mat((1, 0.5, 0.1)), (rad(-90), 0, 0))
        for k in range(3): S(0.07*s, (x, y - 0.6*s, 1.6*s + k*0.35*s), (1, 1, 1), mat((0.1, 0.1, 0.1)))
        for sx in (-1, 1): S(0.07*s, (x + sx*0.17*s, y - 0.4*s, 3.05*s), (1, 1, 1), mat((0.1, 0.1, 0.1)))
        Cy(0.5*s, 0.1*s, (x, y, 3.3*s), mat((0.15, 0.15, 0.18))); Cy(0.35*s, 0.5*s, (x, y, 3.55*s), mat((0.15, 0.15, 0.18))); To(0.46*s, 0.08*s, (x, y, 2.45*s), mat((0.9, 0.2, 0.2)))
    snowman(-7.6, 7.8, 0.72); 
    def gift(x, y, s, c, rc):
        B((x, y, 0.5*s), (s, s, s), mat(c)); B((x, y, 0.5*s), (s*1.04, s*0.22, s*1.04), mat(rc)); B((x, y, 0.5*s), (s*0.22, s*1.04, s*1.04), mat(rc)); S(0.18*s, (x, y, 1.05*s), (1.4, 1.4, 0.6), mat(rc))
    gift(5.6, 6.4, 0.9, (0.9, 0.2, 0.25), (1, 0.85, 0.2)); gift(7.0, 7.6, 0.7, (0.3, 0.6, 1.0), (1, 1, 1)); gift(-9.8, 9.0, 0.75, (0.3, 0.75, 0.4), (0.95, 0.3, 0.3))
    cols = [(1, 0.1, 0.1), (0.1, 0.8, 0.2), (1, 0.75, 0.05), (0.15, 0.4, 1), (1, 0.2, 0.8)]
    for k in range(40):       # string lights across the scene
        x = -16 + 32*k/39; z = 6.5 + 1.2*math.cos(k*0.5); S(0.16, (x, 12, z), (1, 1, 1), mat(cols[k % 5], 0.4, 1.0))
    for k in range(39): Cy(0.015, 32/39*1.05, (-16 + 32*(k+0.5)/39, 12, 6.5 + 1.2*math.cos((k+0.5)*0.5)), mat((0.2, 0.3, 0.2)), (0, rad(90 + 12*math.sin((k+0.5)*0.5)), 0))
    fm = mat((1, 1, 1), 0.9, 0.3)
    for k in range(45): S(random.uniform(0.08, 0.16), (random.uniform(-18, 18), random.uniform(3, 30), random.uniform(0.5, 12)), (1, 1, 1), fm)
    tree(-6.5, 10, 1.4, (0.15, 0.5, 0.25)); 
    for k in range(12): a = k*1.7; S(0.16, (-6.5 + 1.1*math.cos(a), 10 - 0.6*abs(math.sin(a)), 2.0 + 0.9*math.sin(a*0.7)), (1,1,1), mat(cols[k % 5], 0.4, 0.8))
    Fp = None
    bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.45, depth=0.1, location=(-6.5, 10, 3.75), rotation=(rad(90), 0, 0)); st = bpy.context.active_object; st.data.materials.append(mat((1, 0.8, 0.1), 0.4, 1.0))

def _bsdf(m): return m.node_tree.nodes.get("Principled BSDF") if m and m.node_tree else None
def _sat(c): return (max(c) - min(c)) / max(max(c), 1e-6)
def _glow(ob, k):
    for m in ob.data.materials:
        b = _bsdf(m)
        if not b or b.inputs["Emission Strength"].default_value > 0: continue
        c = tuple(b.inputs["Base Color"].default_value[:3])
        if _sat(c) > 0.45: b.inputs["Emission Color"].default_value = (*c, 1); b.inputs["Emission Strength"].default_value = k

if NIGHT:
    rng = random.Random(21)
    reef = BASE == "reef"
    for m in bpy.data.materials:                       # sky gradient -> deep blue
        if m.name.startswith("sky") and m.node_tree:
            for n in m.node_tree.nodes:
                if n.bl_idname == "ShaderNodeValToRGB":
                    n.color_ramp.elements[0].color = ((0.05, 0.2, 0.42, 1) if reef else (0.12, 0.2, 0.5, 1))
                    n.color_ramp.elements[1].color = ((0.01, 0.05, 0.22, 1) if reef else (0.015, 0.03, 0.17, 1))
    bg = world.node_tree.nodes.get("Background"); bg.inputs[0].default_value = ((0.2, 0.36, 0.7, 1) if reef else (0.3, 0.4, 0.78, 1)); bg.inputs[1].default_value = AMB
    sun.energy = SUNE; sun.color = (0.6, 0.74, 1.0)
    if reef:
        for ob in bpy.data.objects:
            if ob.type == 'MESH' and not (ob.location.z > 3.5 and abs(ob.scale.x - 1.6) < 1e-3): _glow(ob, 0.32)
        pm = [mat((0.2, 1.0, 0.6), 0.3, 2.6), mat((0.2, 0.85, 1.0), 0.3, 2.6), mat((0.75, 1.0, 0.25), 0.3, 2.4)]
        for k in range(16): S(rng.uniform(0.09, 0.15), (rng.uniform(-11, 11), rng.uniform(4, 24), rng.uniform(1.2, 8.5)), (1, 1, 1), pm[k % 3])
    else:
        for ob in list(bpy.data.objects):
            if ob.type != 'MESH': continue
            b = _bsdf(ob.data.materials[0]) if ob.data.materials else None
            if not b: continue
            c = tuple(b.inputs["Base Color"].default_value[:3]); e = b.inputs["Emission Strength"].default_value
            if e >= 2.5 and ob.location.z > 20:        # the sun -> a pale moon
                b.inputs["Base Color"].default_value = (0.95, 0.97, 1.0, 1); b.inputs["Emission Color"].default_value = (0.92, 0.95, 1.0, 1); b.inputs["Emission Strength"].default_value = 2.6
                S(0.3, (ob.location.x - 0.5, ob.location.y - 1.7, ob.location.z + 0.4), (1, 0.3, 1), mat((0.8, 0.84, 0.95), 0.6, 1.9)); S(0.2, (ob.location.x + 0.6, ob.location.y - 1.7, ob.location.z - 0.5), (1, 0.3, 1), mat((0.8, 0.84, 0.95), 0.6, 1.9))
            elif abs(e - 1.5) < 1e-3 and c[0] > 0.9 and c[1] < 0.5:   # volcano crater: soft orange glow
                b.inputs["Emission Strength"].default_value = 2.0; b.inputs["Emission Color"].default_value = (1.0, 0.38, 0.08, 1)
                ld = bpy.data.lights.new("Lava", 'POINT'); ld.energy = 30000 * (ob.dimensions.x / 3.2) ** 2; ld.color = (1.0, 0.45, 0.12); ld.shadow_soft_size = 1.0
                lo = bpy.data.objects.new("Lava", ld); scene.collection.objects.link(lo); lo.location = (ob.location.x, ob.location.y - 0.5, ob.location.z + 1.3)
            elif abs(e - 0.6) < 1e-3 and ob.location.y > 60: b.inputs["Emission Strength"].default_value = 0.14      # rainbow: dim
        sm = [mat((1, 1, 0.9), 0.5, 5.0), mat((0.8, 0.9, 1.0), 0.5, 4.0)]
        for k in range(110): S(0.13 * rng.uniform(0.5, 1.5), (rng.uniform(-44, 44), 80 - rng.uniform(0, 4), rng.uniform(9, 46)), (1, 1, 1), sm[k % 2])
scene.render.engine = 'BLENDER_EEVEE'; scene.render.film_transparent = False
scene.render.image_settings.file_format = 'PNG'; scene.render.image_settings.color_mode = 'RGB'; scene.render.image_settings.color_depth = '8'
scene.view_settings.view_transform = 'Standard'; scene.eevee.taa_render_samples = 64; scene.eevee.use_shadows = True
scene.render.filepath = f"{OUT}/{SC}.png"; bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=f"{OUT}/{SC}.blend"); print("DONE scene", SC)
