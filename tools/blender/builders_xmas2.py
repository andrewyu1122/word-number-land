# mascot with a santa hat (mascot_xmas) + standalone hat (hat_santa)
exec(open(PIPE + "/builders_mascot2.py", encoding="utf-8").read().rsplit(chr(10)+"BUILD = {k[2:]", 1)[0])
def santa_hat(x, y, z, s=1.0, tilt=12):
    """brim at height z, cone leaning to the right; returns nothing"""
    piv = E((x, y, z), name="HatPiv"); piv.rotation_euler = (0, rad(tilt), 0)
    o = To(0.5*s, 0.13*s, (x, y, z), "white", parent=piv); bpy.context.view_layer.update()
    c = Co(0.52*s, 0.95*s, (x, y, z+0.45*s), "red", (0, 0, 0), piv, verts=32); m = c.modifiers.new("Sub", 'SUBSURF'); m.levels = 1
    S(0.3*s, (x, y, z+0.1*s), (1.75, 1.75, 0.5), "red", piv, name="HatBase")
    tip = Co(0.2*s, 0.5*s, (x+0.22*s, y, z+1.05*s), "red", (0, rad(50), 0), piv, verts=24)
    S(0.17*s, (x+0.45*s, y, z+1.15*s), (1, 1, 1), "white", piv, name="Pom")
    return piv
def b_mascot_xmas():
    h = b_mascot()
    for ob in list(bpy.data.objects):                      # drop the antenna so the hat sits cleanly
        if ob.location.z > 1.55 and ob.type in ('MESH',) and abs(ob.location.x) < 0.05 and abs(ob.location.y) < 0.05: bpy.data.objects.remove(ob, do_unlink=True)
    santa_hat(0, 0, 1.42, 0.95, 10)
    # scarf
    To(0.5, 0.12, (0, 0, 0.5), "red", (0, 0, 0)); B((0.32, -0.42, 0.25), (0.22, 0.1, 0.5), "red", bevel=0.04); B((0.32, -0.42, 0.02), (0.26, 0.12, 0.08), "white", bevel=0.02)
    return h
def b_hat_santa():
    santa_hat(0, 0, 0.3, 1.0, 0); return {}
BUILD = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("b_")}
