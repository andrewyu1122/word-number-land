# Blender pipeline (Dino Island + Coral Reef characters, night scenes)

Headless, needs Blender 5.x. Run from the repo root (`BL` = path to blender.exe):

```
# one character: idle + walk/roar (or swim/happy) + eat/sleep/run, all with ONE camera -> 512x512 PNGs
"$BL" -b --python tools/blender/render_char.py -- trex dino full ./incoming/dino
"$BL" -b --python tools/blender/render_char.py -- clownfish sea full ./incoming/sea
#   modes: check (metrics only) | preview (8 frames per new action, 256px) | full
# night scenes (island_night, island_2_night, island_3_night, reef_night): background and foreground layer
"$BL" -b --python tools/blender/render_scene.py -- island_night bg ./incoming/scenes
"$BL" -b --python tools/blender/render_scene.py -- island_night fg ./incoming/scenes
python tools/blender/sheet.py <preview dir> out.png trex,triceratops     # contact sheet of previews
```

- `wb.py` shared primitives + base actions; `builders_dino.py` / `builders_sea.py` (on top of `builders_meta.py`) build the models.
- `actions.py` eat / sleep / run (neck rig for the long-necked dinos, closed-eye lids, screen-space foot-line checks).
- `tail2.py` camera fit over the union of all actions, then render. The `REPORT` line shows how far each new action
  leaves the old idle/walk/roar box (`grow_h` must stay 1.0 or the sprite changes size in the game).
- Then convert as usual: `python tools/convert_assets.py dino ./incoming/dino` (also for `./incoming/sea`), `... scenes ./incoming/scenes`.
