
# ====================== camera fit + render tail (idle + old actions + eat/sleep/run, ONE camera) ======================
import json as _json
from mathutils import Vector as _V
os.makedirs(OUTDIR, exist_ok=True)
def _aim(o,t): o.rotation_euler=(_V(t)-o.location).to_track_quat('-Z','Y').to_euler()
_cd=bpy.data.cameras.new("C34"); _cd.type='ORTHO'; _cd.ortho_scale=4.0
cam=bpy.data.objects.new("Camera34",_cd); scene.collection.objects.link(cam); cam.location=(-9,-9,6.8); _aim(cam,(0,0,1.2))
def _area(name,loc,e,size,col=(1,1,1),target=(0,0,1.0)):
    ld=bpy.data.lights.new(name,'AREA'); ld.energy=e; ld.size=size; ld.color=col
    lo=bpy.data.objects.new(name,ld); scene.collection.objects.link(lo); lo.location=loc; _aim(lo,target)
def setup_lights(h):
    k=max(1.0,h/2.5)
    _area("Key",(-4*k,-5*k,7*k),900*k,4*k,(1,0.98,0.95),(0,0,h/2)); _area("Fill",(6*k,-4*k,3*k),380*k,5*k,(0.95,0.97,1),(0,0,h/2)); _area("Rim",(1,6*k,5*k),300*k,3*k,(1,1,1),(0,0,h/2))
def measure(frames):
    scene.frame_set(1); bpy.context.view_layer.update()
    inv=cam.matrix_world.inverted(); xs=[]; ys=[]
    for f in frames:
        scene.frame_set(f); dg=bpy.context.evaluated_depsgraph_get()
        for ob in scene.objects:
            if ob.type not in ('MESH','FONT','CURVE') or ob.hide_render: continue
            ev=ob.evaluated_get(dg)
            for c in ev.bound_box:
                p=inv @ (ev.matrix_world @ _V(c)); xs.append(p.x); ys.append(p.y)
    scene.frame_set(1)
    dg=bpy.context.evaluated_depsgraph_get(); mz=1e9
    for ob in scene.objects:
        if ob.type in ('MESH','FONT','CURVE') and not ob.hide_render:
            ev=ob.evaluated_get(dg); mz=min([mz]+[(ev.matrix_world @ _V(c)).z for c in ev.bound_box])
    globals()['GP']=(0,0,mz)
    g=inv @ _V(GP)
    return min(xs),max(xs),min(ys),max(ys),g.x,g.y
def fit_camera(bounds, feet=0.2, top_margin=0.05, side_margin=0.04):
    xmin,xmax,ymin,ymax,gx,gy=bounds
    S=max((ymax-gy)/(1-feet-top_margin), (gy-ymin)/max(feet-0.03,0.01), (xmax-xmin)/(1-2*side_margin))
    cam.data.ortho_scale=S
    cam.data.shift_y = 0.5 + gy/S - feet
    cam.data.shift_x = ((xmin+xmax)/2)/S
    from bpy_extras.object_utils import world_to_camera_view as w2c
    scene.frame_set(1); v=w2c(scene,cam,_V(GP))
    if abs(v.y-feet)>0.01:
        cam.data.shift_y=-cam.data.shift_y; cam.data.shift_x=-cam.data.shift_x
        v=w2c(scene,cam,_V(GP))
    return S, v.y

OLD = ["walk", "roar"] if IS_DINO else ["swim", "happy"]; NEW = ["eat", "sleep", "run"]
FR = range(1, NFRAMES+1)
SNAP_REST = {o.name: (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale)) for o in bpy.data.objects}
def restore():
    for o in bpy.data.objects:
        if o.animation_data: o.animation_data_clear()
        if o.name in SNAP_REST: o.location, o.rotation_euler, o.scale = SNAP_REST[o.name]
    if NECKARM:
        for pb in NECKARM.pose.bones: pb.rotation_euler = (0, 0, 0)
    set_eyes(True); scene.frame_set(1)
def lift_fix():
    """raise ROOT on any frame where something would dip below the idle foot line (screen space)"""
    mx = 0.0
    for f in range(1, NFRAMES+2):
        scene.frame_set(f); d = FOOT - sbox(vis_meshes())[2]
        if d > 0.002:
            ROOT.location.z += d / UP[2] + 0.002; ROOT.keyframe_insert("location", frame=f); mx = max(mx, d)
    return mx
def const_fix():
    """shift the whole action up if it dips below the idle foot line"""
    d = 0.0
    for f in range(1, NFRAMES+1):
        scene.frame_set(f); d = max(d, FOOT - sbox(vis_meshes())[2])
    if d > 0.02:
        for f in range(1, NFRAMES+2):
            scene.frame_set(f); ROOT.location.z += d / UP[2]; ROOT.keyframe_insert("location", frame=f)
        return d
    return 0.0
def apply(a):
    restore(); fx = 0.0
    if a:
        ACTS[a](H)
        if a == "sleep" or (a == "eat" and not IS_DINO): fx = lift_fix()
        else: fx = const_fix()
    scene.frame_set(1); return fx
def abox(a):
    bx = None
    for f in (FR if a else [1]):
        scene.frame_set(f); b = sbox(vis_meshes())
        bx = b if bx is None else (min(bx[0], b[0]), max(bx[1], b[1]), min(bx[2], b[2]), max(bx[3], b[3]))
    scene.frame_set(1); return bx
def uni(bs):
    bs = list(bs); return (min(b[0] for b in bs), max(b[1] for b in bs), min(b[2] for b in bs), max(b[3] for b in bs))
scene.render.resolution_x = scene.render.resolution_y = 512; scene.render.resolution_percentage = 100; scene.render.pixel_aspect_x = scene.render.pixel_aspect_y = 1.0
scene.camera = cam
setup_lights(globals().get('H_LIGHT', 2.2))
for _l in bpy.data.lights: _l.energy *= globals().get('LIGHT_SCALE', 0.22)
ACTIONS = OLD if MODE == "idlecheck" else OLD + NEW
BB = {}; AB = {}; FX = {}
for a in ACTIONS + [None]:
    FX[a] = apply(a); BB[a] = measure(FR if a else [1]); AB[a] = abox(a)
Bu = (min(b[0] for b in BB.values()), max(b[1] for b in BB.values()), min(b[2] for b in BB.values()), max(b[3] for b in BB.values()), BB[None][4], BB[None][5])
S_used, feet_y = fit_camera(Bu)
old = uni(AB[a] for a in OLD + [None]); allb = uni(AB.values()); ho = old[3] - old[2]; wo = old[1] - old[0]
rep = dict(name=NAME, S=round(S_used, 3), grow_h=round((allb[3] - allb[2]) / ho, 3), grow_w=round((allb[1] - allb[0]) / wo, 3))
for a in ACTIONS:
    if a in NEW:
        b = AB[a]; rep[a] = dict(bottom=round((old[2] - b[2]) / ho, 3), top=round((b[3] - old[3]) / ho, 3), left=round((old[0] - b[0]) / wo, 3), right=round((b[1] - old[1]) / wo, 3),
                                 below_foot=round(FOOT - b[2], 3), fix=round(FX[a], 3))
print("REPORT", _json.dumps(rep), flush=True)
if MODE != "check":
    PREV = MODE == "preview"
    world=bpy.data.worlds.get("World") or bpy.data.worlds.new("World"); scene.world=world; world.use_nodes=True
    bg=world.node_tree.nodes.get("Background"); bg.inputs[0].default_value=(0.8,0.8,0.85,1); bg.inputs[1].default_value=0.5
    scene.render.engine='BLENDER_EEVEE'; scene.render.resolution_x=scene.render.resolution_y=(256 if PREV else 512); scene.render.resolution_percentage=100
    scene.render.film_transparent=True; ims=scene.render.image_settings; ims.file_format='PNG'; ims.color_mode='RGBA'; ims.color_depth='8'
    scene.view_settings.view_transform='Standard'; scene.eevee.use_shadows=True; scene.eevee.taa_render_samples=(16 if PREV else 64)
    for kk,v in (("shadow_ray_count",2),("shadow_step_count",4)):
        if hasattr(scene.eevee,kk): setattr(scene.eevee,kk,v)
    scene.camera=cam
    if PREV:
        for a in NEW:
            apply(a)
            for f in (1, 4, 7, 10, 13, 16, 19, 22):
                scene.frame_set(f); scene.render.filepath=f"{OUTDIR}/{PREFIX}_{a}_{f:03d}.png"; bpy.ops.render.render(write_still=True)
    else:
        apply(None)
        scene.render.filepath=f"{OUTDIR}/{PREFIX}_idle.png"; bpy.ops.render.render(write_still=True)
        if MODE == "full":
            for a in ACTIONS:
                apply(a); scene.frame_start, scene.frame_end = 1, NFRAMES
                scene.render.filepath=f"{OUTDIR}/{PREFIX}_{a}_###"; bpy.ops.render.render(animation=True)
            apply(None)
            bpy.ops.wm.save_as_mainfile(filepath=f"{OUTDIR}/{PREFIX}.blend")
    print("DONE", PREFIX, MODE, "S=%.2f feet_y=%.3f"%(S_used,feet_y), flush=True)
