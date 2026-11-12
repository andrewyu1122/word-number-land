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

# ---------- foreground layer: props on the ground between y=-5.2 and -3.4 (bottom ~20% of the frame), transparent ----------
bg = world.node_tree.nodes.get("Background"); bg.inputs[0].default_value = (0.75, 0.8, 0.9, 1); bg.inputs[1].default_value = 0.7
random.seed(11)
def tuft(x, y, s=1.0, c=(0.3, 0.68, 0.28)):
    m = mat(c)
    for k in range(5): a = -0.6 + 0.3*k; Co(0.05*s, 0.55*s, (x + 0.12*s*math.sin(a*2), y + 0.05*k, 0.26*s), m, (rad(-12*math.cos(a*3)), rad(28*a), 0))
def flowerfg(x, y, c, s=1.0):
    Cy(0.025*s, 0.3*s, (x, y, 0.15*s), mat((0.3, 0.6, 0.25))); S(0.09*s, (x, y, 0.33*s), (1, 1, 0.6), mat(c)); S(0.045*s, (x, y - 0.06*s, 0.36*s), (1, 0.6, 1), mat((1, 0.9, 0.3)))
def rock(x, y, s=1.0, c=(0.6, 0.6, 0.65)):
    S(0.3*s, (x, y, 0.16*s), (1.3, 1, 0.65), mat(c), (0, 0, random.uniform(0, 3)))
xs = [-2.6, -1.9, -1.1, -0.4, 0.5, 1.3, 2.0, 2.7]
if BASE == "meadow":
    for x in xs: tuft(x + random.uniform(-0.2, 0.2), random.uniform(-4.9, -3.8), random.uniform(0.8, 1.2))
    for x, c in [(-2.2, (1, 0.4, 0.5)), (-0.8, (1, 0.85, 0.2)), (0.9, (1, 1, 1)), (2.3, (0.7, 0.5, 1))]: flowerfg(x, -4.3, c)
    rock(1.7, -4.6, 0.8)
elif BASE == "sea":
    sm = mat((0.95, 0.88, 0.65))
    for x in xs: S(0.35, (x, -4.3 + random.uniform(-0.3, 0.3), -0.05), (1.4, 1, 0.35), sm)
    for k in range(7): a = k*TAU/5; S(0.07, (-1.6 + 0.26*math.cos(a), -4.4 + 0.26*math.sin(a), 0.05), (1.4, 0.6, 0.5), mat((1, 0.5, 0.35)), (0, 0, a))   # starfish
    for x, c in [(0.8, (1, 0.75, 0.75)), (2.2, (0.95, 0.95, 0.9))]: S(0.16, (x, -4.5, 0.08), (1, 0.8, 0.6), mat(c))
    for k in range(5): Cy(0.03, 0.5, (-0.4 + 0.08*k, -4.2, 0.25), mat((0.2, 0.6, 0.3)), (rad(random.uniform(-25, 25)), rad(random.uniform(-15, 15)), 0))   # seaweed
elif BASE == "sky":
    cm = mat((1, 1, 1), 0.9)
    for x, s in [(-2.4, 0.5), (-0.9, 0.62), (0.7, 0.55), (2.3, 0.6)]: cloud(x, -4.4, -0.15, s, cm)
elif BASE == "road":
    km = mat((0.75, 0.75, 0.72))
    for x in xs: B((x, -4.4, 0.1), (0.75, 0.3, 0.2), km)
    Co(0.16, 0.5, (1.9, -4.1, 0.25), mat((1, 0.45, 0.1))); To(0.11, 0.02, (1.9, -4.1, 0.3), mat((1, 1, 1)), (0, 0, 0), (1, 1, 1)); B((1.9, -4.1, 0.02), (0.4, 0.4, 0.04), mat((1, 0.45, 0.1)))
    for x in (-2.3, -1.2, 0.3): tuft(x, -4.8, 0.8, (0.35, 0.65, 0.3))
elif BASE == "space":
    gm = mat((0.55, 0.55, 0.62))
    for x in xs: rock(x + random.uniform(-0.2, 0.2), random.uniform(-4.8, -3.9), random.uniform(0.7, 1.3), (0.5, 0.5, 0.58))
    for x, c in [(-1.5, (0.5, 0.9, 1.0)), (1.2, (0.9, 0.5, 1.0))]:
        for k in range(3): Co(0.06, 0.4, (x + 0.1*k, -4.4, 0.2), mat(c, 0.3, 1.5), (rad(random.uniform(-20, 20)), rad(random.uniform(-20, 20)), 0))
elif BASE == "room":
    for x, c in [(-2.4, (1, 0.35, 0.35)), (-2.0, (0.3, 0.6, 1)), (-2.2, (1, 0.85, 0.2))]: pass
    B((-2.3, -4.4, 0.18), (0.36, 0.36, 0.36), mat((1, 0.35, 0.35))); B((-1.9, -4.5, 0.18), (0.36, 0.36, 0.36), mat((0.3, 0.6, 1))); B((-2.1, -4.45, 0.54), (0.36, 0.36, 0.36), mat((1, 0.85, 0.2)))
    S(0.3, (1.9, -4.4, 0.3), (1, 1, 1), mat((1, 0.5, 0.2))); To(0.3, 0.03, (1.9, -4.4, 0.3), mat((1, 1, 1)), (rad(90), 0, rad(20)))
    B((0.3, -4.5, 0.06), (0.9, 0.6, 0.12), mat((0.3, 0.5, 0.9))); B((0.3, -4.5, 0.13), (0.86, 0.56, 0.02), mat((1, 1, 1)))
    S(0.12, (-0.7, -4.3, 0.12), (1, 1, 1), mat((0.9, 0.3, 0.6))); S(0.12, (-0.4, -4.6, 0.12), (1, 1, 1), mat((0.3, 0.8, 0.5)))
elif BASE == "night":
    for x in xs: tuft(x + random.uniform(-0.2, 0.2), random.uniform(-4.9, -3.8), random.uniform(0.8, 1.2), (0.12, 0.25, 0.3))
    fm = mat((1, 1, 0.5), 0.3, 6.0)
    for k in range(6): S(0.03, (random.uniform(-2.5, 2.5), random.uniform(-4.8, -3.6), random.uniform(0.2, 0.55)), (1, 1, 1), fm)
elif BASE == "island":
    for x in (-2.5, -1.0, 0.6, 2.2):
        for k in range(5): a = -0.8 + 0.4*k; Co(0.08, 0.8, (x + 0.35*math.sin(a), -4.3, 0.3), mat((0.25, 0.6, 0.25)), (rad(-30), rad(45*a), 0))   # fern fronds
    rock(-1.8, -4.6, 0.9, (0.55, 0.5, 0.45)); rock(1.4, -4.7, 0.7, (0.5, 0.45, 0.4))
    for x in (-0.3, 0.1): S(0.09, (x, -4.5, 0.05), (1, 0.8, 0.6), mat((0.95, 0.95, 0.85)))   # egg shell bits
elif BASE == "reef":
    for x in xs: S(0.35, (x, -4.3 + random.uniform(-0.3, 0.3), -0.05), (1.4, 1, 0.35), mat((0.95, 0.88, 0.65)))
    for x, c in [(-2.2, (1, 0.45, 0.5)), (0.2, (1, 0.7, 0.2)), (2.4, (0.8, 0.4, 1))]:
        for k in range(5): a = k*TAU/5; Cy(0.05, 0.45, (x + 0.1*math.cos(a), -4.4 + 0.1*math.sin(a), 0.22), mat(c), (rad(20*math.cos(a)), rad(20*math.sin(a)), 0)); S(0.07, (x + 0.18*math.cos(a), -4.4 + 0.18*math.sin(a), 0.44), (1, 1, 1), mat(c))
    for x in (-1.1, 1.3):
        for k in range(4): Cy(0.03, 0.55, (x + 0.08*k, -4.2, 0.27), mat((0.2, 0.65, 0.35)), (rad(random.uniform(-25, 25)), rad(random.uniform(-15, 15)), 0))
# move the props from the design band (y~-4.3) into the camera's real near band (y~8) and scale them up
K = 3.2
for o in list(bpy.data.objects):
    if o.type == 'MESH':
        o.location = (o.location.x*K, (o.location.y+4.3)*K+8.0, o.location.z*K); o.scale = (o.scale[0]*K, o.scale[1]*K, o.scale[2]*K)

def _bsdf(m): return m.node_tree.nodes.get("Principled BSDF") if m and m.node_tree else None
def _sat(c): return (max(c) - min(c)) / max(max(c), 1e-6)
def _glow(ob, k):
    for m in ob.data.materials:
        b = _bsdf(m)
        if not b or b.inputs["Emission Strength"].default_value > 0: continue
        c = tuple(b.inputs["Base Color"].default_value[:3])
        if _sat(c) > 0.45: b.inputs["Emission Color"].default_value = (*c, 1); b.inputs["Emission Strength"].default_value = k

if NIGHT:
    bg = world.node_tree.nodes.get("Background"); bg.inputs[0].default_value = ((0.2, 0.36, 0.7, 1) if BASE == "reef" else (0.3, 0.4, 0.78, 1)); bg.inputs[1].default_value = AMB
    sun.energy = SUNE * 3.0 / (2.2 if BASE == "reef" else 3.4); sun.color = (0.6, 0.74, 1.0)
    if BASE == "reef":
        for ob in bpy.data.objects:
            if ob.type == 'MESH': _glow(ob, 0.32)
scene.render.engine = 'BLENDER_EEVEE'; scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'; scene.render.image_settings.color_mode = 'RGBA'; scene.render.image_settings.color_depth = '8'
scene.view_settings.view_transform = 'Standard'; scene.eevee.taa_render_samples = 64; scene.eevee.use_shadows = True
scene.render.filepath = f"{OUT}/{SC}_fg.png"; bpy.ops.render.render(write_still=True)
