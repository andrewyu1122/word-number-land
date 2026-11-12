
# ====================== shared camera fit + render tail ======================
# expects: scene, root(s) built, OUTDIR, PREFIX, ACTION, DO_IDLE, DO_ANIM, FIXED (float|None), MEASURE_ONLY (bool), SLEEP (callable|None)
import json as _json
from mathutils import Vector as _V
os.makedirs(OUTDIR, exist_ok=True)
GROUND=globals().get('GROUND',(0,0,0))
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
    if GROUND=='auto':
        dg=bpy.context.evaluated_depsgraph_get(); mz=1e9
        for ob in scene.objects:
            if ob.type in ('MESH','FONT','CURVE') and not ob.hide_render:
                ev=ob.evaluated_get(dg); mz=min([mz]+[(ev.matrix_world @ _V(c)).z for c in ev.bound_box])
        GP=(0,0,mz)
    else: GP=GROUND
    globals()['GP']=GP
    g=inv @ _V(GP)
    return min(xs),max(xs),min(ys),max(ys),g.x,g.y
def fit_camera(frames, feet=0.2, top_margin=0.05, side_margin=0.04, fixed=None):
    xmin,xmax,ymin,ymax,gx,gy=measure(frames)
    S=max((ymax-gy)/(1-feet-top_margin), (gy-ymin)/max(feet-0.03,0.01), (xmax-xmin)/(1-2*side_margin))
    if fixed: S=max(fixed,S)   # never crop, even with a fixed set-wide scale
    cam.data.ortho_scale=S
    cam.data.shift_y = 0.5 + gy/S - feet
    cam.data.shift_x = ((xmin+xmax)/2)/S
    # verify sign convention with Blender's own projection, flip if needed
    from bpy_extras.object_utils import world_to_camera_view as w2c
    scene.frame_set(1); v=w2c(scene,cam,_V(GP))
    if abs(v.y-feet)>0.01:
        cam.data.shift_y=-cam.data.shift_y; cam.data.shift_x=-cam.data.shift_x
        v=w2c(scene,cam,_V(GP))
    return S, v.y
scene.render.resolution_x=scene.render.resolution_y=globals().get('RES',512); scene.render.resolution_percentage=100; scene.camera=cam
setup_lights(globals().get('H_LIGHT', 2.2))
for _l in bpy.data.lights: _l.energy *= globals().get('LIGHT_SCALE', 0.22)
S_used, feet_y = fit_camera(range(1,25), fixed=FIXED)
if MEASURE_ONLY:
    print("MEASURE", _json.dumps({"S":S_used}))
else:
    world=bpy.data.worlds.get("World") or bpy.data.worlds.new("World"); scene.world=world; world.use_nodes=True
    bg=world.node_tree.nodes.get("Background"); bg.inputs[0].default_value=(0.8,0.8,0.85,1); bg.inputs[1].default_value=0.5
    scene.render.engine='BLENDER_EEVEE'; scene.render.resolution_x=scene.render.resolution_y=globals().get('RES',512); scene.render.resolution_percentage=100
    scene.render.film_transparent=True; ims=scene.render.image_settings; ims.file_format='PNG'; ims.color_mode='RGBA'; ims.color_depth='8'
    scene.view_settings.view_transform='Standard'; scene.eevee.use_shadows=True; scene.eevee.taa_render_samples=64
    for kk,v in (("shadow_ray_count",2),("shadow_step_count",4)):
        if hasattr(scene.eevee,kk): setattr(scene.eevee,kk,v)
    scene.camera=cam; scene.frame_set(1)
    if DO_IDLE:
        scene.render.filepath=f"{OUTDIR}/{PREFIX}_idle.png"; bpy.ops.render.render(write_still=True)
    if DO_ANIM:
        scene.render.filepath=f"{OUTDIR}/{PREFIX}_{ACTION}_###"; bpy.ops.render.render(animation=True)
    if SLEEP is not None:
        scene.frame_set(1); SLEEP()
        scene.render.filepath=f"{OUTDIR}/{PREFIX}_sleep.png"; bpy.ops.render.render(write_still=True)
    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=f"{OUTDIR}/{PREFIX}.blend")
    print("DONE", PREFIX, "S=%.2f feet_y=%.3f"%(S_used,feet_y))
