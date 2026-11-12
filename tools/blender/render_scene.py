# blender -b --python render_scene.py -- <scene> <bg|fg> <outdir> [amb] [sun]
import sys, os
argv = sys.argv[sys.argv.index('--') + 1:]
sc, layer, out = argv[:3]; amb = float(argv[3]) if len(argv) > 3 else 0.8; sune = float(argv[4]) if len(argv) > 4 else 1.5
P = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/')
src = open(P + ('/scenes_night.py' if layer == 'bg' else '/scenes_fg_night.py'), encoding='utf-8').read().replace('__SCENE__', sc).replace('__OUT__', out.replace(os.sep, '/'))
exec(compile("AMB = %r; SUNE = %r\n" % (amb, sune) + src, 'scene_' + sc, 'exec'), {'__name__': '__main__'})
