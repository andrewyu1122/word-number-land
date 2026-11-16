# blender -b --python render_barn.py -- <outdir (absolute)>
# Horse Ranch "egg": barn_s0..s3.png (door closed -> nearly open) + barn_hatch_001..024.png, all with ONE camera.
import sys, os
out = sys.argv[sys.argv.index('--') + 1]
P = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/')
src = open(P + '/wb.py', encoding='utf-8').read()
src = (src.replace('__NAME__', 'barn').replace('__GROUP__', 'hatch').replace('__OUTDIR__', out.replace(os.sep, '/'))
          .replace('__IDLE__', 'False').replace('__ANIM__', 'True').replace('__FIXED__', 'None').replace('__MEAS__', 'False')
          .replace('__NFRAMES__', '24').replace('__BUILDERS__', 'builders_horse.py').replace('__RES__', '512'))
src = src.replace('H = BUILD[NAME]() or {}', 'H = BUILD[NAME]() or {}' + chr(10) + 'SLEEP=None')
tail = open(P + '/tail_word.py', encoding='utf-8').read()
stills = '''
for _o in bpy.data.objects:
    if _o.animation_data: _o.animation_data_clear()
for _m in bpy.data.materials:
    if _m.node_tree and _m.node_tree.animation_data: _m.node_tree.animation_data_clear()
scene.frame_set(1); ROOT.location = (0, 0, 0)
for _nm, _fn in EXTRA_STILLS:
    _fn(); bpy.context.view_layer.update()
    scene.render.filepath = f"{OUTDIR}/{_nm}.png"; bpy.ops.render.render(write_still=True)
print("DONE stills", flush=True)
'''
exec(compile('PIPE = r"' + P + '"' + chr(10) + src + tail + stills, 'barn', 'exec'), {'__name__': '__main__'})
