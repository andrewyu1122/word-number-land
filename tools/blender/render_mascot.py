# blender -b --python render_mascot.py -- <check|preview|full> <outdir> [action,action,...]
# Renders the mascot's Read-mode action loops with EXACTLY the camera the existing mascot_idle was rendered with
# (set-wide scale measured on "happy", framing from the idle loop), so new states line up with idle/happy/wave/...
import sys, os
argv = sys.argv[sys.argv.index('--') + 1:]
mode, outdir = argv[:2]; only = argv[2].split(',') if len(argv) > 2 else None
P = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/')
src = open(P + '/wb.py', encoding='utf-8').read()
src = (src.replace('__NAME__', 'mascot').replace('__GROUP__', 'none').replace('__OUTDIR__', outdir.replace(os.sep, '/'))
          .replace('__IDLE__', 'True').replace('__ANIM__', 'True').replace('__FIXED__', 'None').replace('__MEAS__', 'False')
          .replace('__NFRAMES__', '24').replace('__BUILDERS__', 'builders_mascot3.py').replace('__RES__', '512'))
src = src.replace('ACTS[GROUP](H)', 'ACTS["none"] = lambda h: None\nACTS[GROUP](H)')
TAIL = r'''
import json as _json
from mathutils import Vector as _V
from bpy_extras.object_utils import world_to_camera_view as w2c
MODE = "__MODE__"; ONLY = __ONLY__
os.makedirs(OUTDIR, exist_ok=True)
def _aim(o,t): o.rotation_euler=(_V(t)-o.location).to_track_quat('-Z','Y').to_euler()
_cd=bpy.data.cameras.new("C34"); _cd.type='ORTHO'; _cd.ortho_scale=4.0
cam=bpy.data.objects.new("Camera34",_cd); scene.collection.objects.link(cam); cam.location=(-9,-9,6.8); _aim(cam,(0,0,1.2))
def _area(name,loc,e,size,col=(1,1,1),target=(0,0,1.0)):
    ld=bpy.data.lights.new(name,'AREA'); ld.energy=e; ld.size=size; ld.color=col
    lo=bpy.data.objects.new(name,ld); scene.collection.objects.link(lo); lo.location=loc; _aim(lo,target)
h_=2.2; k=max(1.0,h_/2.5)
_area("Key",(-4*k,-5*k,7*k),900*k,4*k,(1,0.98,0.95),(0,0,h_/2)); _area("Fill",(6*k,-4*k,3*k),380*k,5*k,(0.95,0.97,1),(0,0,h_/2)); _area("Rim",(1,6*k,5*k),300*k,3*k,(1,1,1),(0,0,h_/2))
for _l in bpy.data.lights: _l.energy *= 0.22
scene.render.resolution_x=scene.render.resolution_y=512; scene.render.resolution_percentage=100; scene.camera=cam
SNAP = {o.name: (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale), o.parent, o.matrix_parent_inverse.copy()) for o in bpy.data.objects}
def restore():
    for o in bpy.data.objects:
        if o.animation_data: o.animation_data_clear()
        if o.name in SNAP: o.parent = SNAP[o.name][3]; o.matrix_parent_inverse = SNAP[o.name][4]; o.location, o.rotation_euler, o.scale = SNAP[o.name][:3]
        if o.name.startswith("BlinkLid"): o.hide_render = True
    for m in bpy.data.materials:
        if m.node_tree and m.node_tree.animation_data: m.node_tree.animation_data_clear()
    scene.frame_set(1)
def measure(frames):
    inv=cam.matrix_world.inverted(); xs=[]; ys=[]
    for f in frames:
        scene.frame_set(f); dg=bpy.context.evaluated_depsgraph_get()
        for ob in scene.objects:
            if ob.type not in ('MESH','FONT','CURVE') or ob.hide_render: continue
            ev=ob.evaluated_get(dg)
            if max(ev.matrix_world.to_scale()) < 0.01: continue        # hidden props
            for c in ev.bound_box:
                p=inv @ (ev.matrix_world @ _V(c)); xs.append(p.x); ys.append(p.y)
    scene.frame_set(1); g=inv @ _V((0,0,0))
    return min(xs),max(xs),min(ys),max(ys),g.x,g.y
def need_S(b, feet=0.2, top_margin=0.05, side_margin=0.04):
    xmin,xmax,ymin,ymax,gx,gy=b
    return max((ymax-gy)/(1-feet-top_margin), (gy-ymin)/max(feet-0.03,0.01), (xmax-xmin)/(1-2*side_margin))
def run_act(a, n=24):
    globals()['NFRAMES'] = n; restore(); ACTS[a](H); scene.frame_set(1)
# 1) the set-wide scale: measured on "happy" (as the earlier mascot renders did)
run_act("happy"); S_fix = need_S(measure(range(1, 25)))
# 2) framing of the existing idle loop (48 f loop, fitted on frames 1-24)
run_act("idle", 48); bi = measure(range(1, 25)); S = max(S_fix, need_S(bi))
scene.frame_set(1); dg=bpy.context.evaluated_depsgraph_get(); gz=1e9      # "auto" ground of the old pipeline: lowest point at frame 1 of the idle loop
for ob in scene.objects:
    if ob.type in ('MESH','FONT','CURVE') and not ob.hide_render:
        ev=ob.evaluated_get(dg)
        if max(ev.matrix_world.to_scale()) >= 0.01: gz=min([gz]+[(ev.matrix_world @ _V(c)).z for c in ev.bound_box])
GPI=_V((0,0,gz)); gyi=(cam.matrix_world.inverted() @ GPI).y
cam.data.ortho_scale = S; cam.data.shift_y = 0.5 + gyi/S - 0.2; cam.data.shift_x = ((bi[0]+bi[1])/2)/S
scene.frame_set(1); v = w2c(scene, cam, GPI)
if abs(v.y-0.2) > 0.01: cam.data.shift_y = -cam.data.shift_y; cam.data.shift_x = -cam.data.shift_x; v = w2c(scene, cam, GPI)
print("CAMERA S=%.3f feet=%.3f" % (S, v.y), flush=True)
def frame_box(frames):
    b = measure(frames)                     # camera-space box -> frame fractions 0..1
    cx = cam.data.shift_x*S; cy = cam.data.shift_y*S
    return [round((b[0]-cx)/S+0.5, 3), round((b[1]-cx)/S+0.5, 3), round((b[2]-cy)/S+0.5, 3), round((b[3]-cy)/S+0.5, 3)]
old = None
for a in ("idle", "happy", "cheer", "wave", "think"):
    run_act(a, 48 if a == "idle" else 24); b = frame_box(range(1, 25)); old = b if old is None else [min(old[0], b[0]), max(old[1], b[1]), min(old[2], b[2]), max(old[3], b[3])]
print("OLDBOX", old, flush=True)
world=bpy.data.worlds.get("World") or bpy.data.worlds.new("World"); scene.world=world; world.use_nodes=True
bg=world.node_tree.nodes.get("Background"); bg.inputs[0].default_value=(0.8,0.8,0.85,1); bg.inputs[1].default_value=0.5
scene.render.engine='BLENDER_EEVEE'; scene.render.film_transparent=True; ims=scene.render.image_settings; ims.file_format='PNG'; ims.color_mode='RGBA'; ims.color_depth='8'
scene.view_settings.view_transform='Standard'; scene.eevee.use_shadows=True; scene.eevee.taa_render_samples=(16 if MODE=="preview" else 64)
for kk,v_ in (("shadow_ray_count",2),("shadow_step_count",4)):
    if hasattr(scene.eevee,kk): setattr(scene.eevee,kk,v_)
if MODE == "preview": scene.render.resolution_x=scene.render.resolution_y=256
if MODE == "idlecheck":
    run_act("idle", 48); scene.frame_set(1); scene.render.filepath=f"{OUTDIR}/mascot_idlecheck.png"; bpy.ops.render.render(write_still=True)
for a in (ONLY or NEW_ACTIONS):
    if MODE == "idlecheck": break
    run_act(a); b = frame_box(range(1, 25))
    print("ACT", a, b, "outside_frame" if (b[0] < 0 or b[1] > 1 or b[2] < 0 or b[3] > 1) else "", "exceeds_old", [round(old[0]-b[0], 3), round(b[1]-old[1], 3), round(old[2]-b[2], 3), round(b[3]-old[3], 3)], flush=True)
    if MODE == "check": continue
    if MODE == "preview":
        for f in (1, 4, 7, 10, 13, 16, 19, 22):
            scene.frame_set(f); scene.render.filepath=f"{OUTDIR}/mascot_{a}_{f:03d}.png"; bpy.ops.render.render(write_still=True)
    else:
        scene.frame_start, scene.frame_end = 1, 24; scene.render.filepath=f"{OUTDIR}/mascot_{a}_###"; bpy.ops.render.render(animation=True)
restore()
if MODE == "full": bpy.ops.wm.save_as_mainfile(filepath=f"{OUTDIR}/mascot_actions.blend")
print("DONE mascot", MODE, flush=True)
'''.replace('__MODE__', mode).replace('__ONLY__', repr(only))
exec(compile('PIPE = r"' + P + '"' + chr(10) + src + TAIL, 'mascot', 'exec'), {'__name__': '__main__'})
