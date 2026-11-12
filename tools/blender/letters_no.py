# blender -b <game-assets>/abc/<L>.blend --python letters_no.py -- <outroot> [check]
# Adds the "no" clip to a lowercase letter character: frown + shake the head twice (12 frames), rendered with the
# camera / lights saved in the letter's own .blend so it lines up with the existing idle and jump renders.
import bpy, sys, os, math
argv = sys.argv[sys.argv.index('--') + 1:]
outroot = argv[0]; check = len(argv) > 1 and argv[1] == 'check'
L = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
out = f"{outroot}/{L}"; os.makedirs(out, exist_ok=True)
s = bpy.context.scene; rad = math.radians
for o in bpy.data.objects:
    if o.animation_data: o.animation_data_clear()
s.frame_set(1)
root = bpy.data.objects["Root"]; root.location = (0, 0, 0); root.scale = (1, 1, 1); root.rotation_euler = (0, 0, 0)
for o in bpy.data.objects:
    if o.name.startswith("ArmPiv"): o.rotation_euler = (0, rad(20) * (1 if o.location.x < 0 else -1), 0)
# the letter tiles use the FRONT view for idle (the jump frames are 3/4); "no" follows idle, so use the front camera
front = bpy.data.objects.get("CameraFront")
if front: s.camera = front
if check:                                   # reproduce the idle still to prove the saved scene matches the old render
    s.render.filepath = f"{out}/{L}_check.png"; bpy.ops.render.render(write_still=True)
# frown: inner brow ends down, eyebrows lower, smile flipped, tongue hidden
for o in bpy.data.objects:
    n = o.name.split('.')[0]
    if n == "Brow": o.rotation_euler = (0, rad(24) * (1 if o.location.x < 0 else -1), 0); o.location.z -= 0.035
    elif n == "Tongue": o.hide_render = True
    elif n == "Mouth": o.rotation_euler = (o.rotation_euler[0], o.rotation_euler[1] + math.pi, o.rotation_euler[2]); o.location.z -= 0.115; o.scale = (0.85, 1, 0.75)
K = [(1, 0), (2.5, 24), (5, -24), (7.5, 24), (10, -24), (12, -6), (13, 0)]
def val(f):
    for (f0, v0), (f1, v1) in zip(K, K[1:]):
        if f <= f1: u = (f - f0) / (f1 - f0); u = (1 - math.cos(math.pi * u)) / 2; return v0 + (v1 - v0) * u
    return 0
for f in range(1, 14):
    a = val(f); root.rotation_euler = (0, 0, rad(a)); root.keyframe_insert("rotation_euler", frame=f)
    for o in bpy.data.objects:
        if o.name.startswith("ArmPiv"):
            sx = 1 if o.location.x < 0 else -1; o.rotation_euler = (rad(-a * 0.5), rad(20 + abs(a) * 0.35) * sx, 0); o.keyframe_insert("rotation_euler", frame=f)
s.frame_start, s.frame_end = 1, 12
s.render.filepath = f"{out}/{L}_no_###"; bpy.ops.render.render(animation=True)
print("DONE", L, flush=True)
