# blender -b --python render_word.py -- <name> <action> <preview|full> <outdir> [builders] [opts]
# words: idle + {action}_001..024 + sleep, fixed set-wide scale 4.5 (same as the earlier word batches)
# opts (comma separated): nosleep, fixed=<ortho scale>   e.g. medals: builders_medals.py nosleep,fixed=3.2
import sys, os
argv = sys.argv[sys.argv.index('--') + 1:]
name, group, mode, outdir = argv[:4]; builders = argv[4] if len(argv) > 4 else 'builders_words3.py'
opts = argv[5].split(',') if len(argv) > 5 else []
fixed = '4.5'
for o_ in opts:
    if o_.startswith('fixed='): fixed = o_[6:]
P = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/')
prev = mode == 'preview'
src = open(P + '/wb.py', encoding='utf-8').read()
src = (src.replace('__NAME__', name).replace('__GROUP__', group).replace('__OUTDIR__', outdir.replace(os.sep, '/'))
          .replace('__IDLE__', 'True').replace('__ANIM__', str(not prev)).replace('__FIXED__', fixed).replace('__MEAS__', 'False')
          .replace('__NFRAMES__', '24').replace('__BUILDERS__', builders).replace('__RES__', '256' if prev else '512'))
if 'nosleep' in opts: src = src.replace('H = BUILD[NAME]() or {}', 'H = BUILD[NAME]() or {}' + chr(10) + 'SLEEP=None')
tail = open(P + '/tail_word.py', encoding='utf-8').read()
if prev: tail = tail.replace('taa_render_samples=64', 'taa_render_samples=16').replace('bpy.ops.wm.save_as_mainfile', 'pass #')
exec(compile('PIPE = r"' + P + '"' + chr(10) + src + tail, 'word_' + name, 'exec'), {'__name__': '__main__'})
