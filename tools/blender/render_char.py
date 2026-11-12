# blender -b --python render_char.py -- <name> <dino|sea> <check|preview|idlecheck|full> <outdir>
import sys, os
argv = sys.argv[sys.argv.index('--') + 1:]
name, kind, mode, outdir = argv[:4]
P = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
WB = open(P + '/wb.py', encoding='utf-8').read()
src = (WB.replace('__NAME__', name).replace('__GROUP__', 'dino').replace('__OUTDIR__', outdir.replace('\\', '/'))
         .replace('__IDLE__', 'True').replace('__ANIM__', 'True').replace('__FIXED__', 'None').replace('__MEAS__', 'False')
         .replace('__NFRAMES__', '24').replace('__BUILDERS__', 'builders_dino.py' if kind == 'dino' else 'builders_sea.py').replace('__RES__', '512'))
src = 'PIPE = r"' + P + '"' + chr(10) + src
PRE = f'KIND = "{kind}"; MODE = "{mode}"\nexec(open(r"{P}/actions.py", encoding="utf-8").read())\n'
assert 'H = BUILD[NAME]() or {}' in src
src = src.replace('H = BUILD[NAME]() or {}', PRE + 'H = BUILD[NAME]() or {}\nsetup_rig(H)')
src += open(P + '/tail2.py', encoding='utf-8').read()
exec(compile(src, 'pipeline_' + name, 'exec'), {'__name__': '__main__'})
