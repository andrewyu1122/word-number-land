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

## Words, mascot, letters, medals (added later)

```
# one picture word (idle + action + sleep) -> ./incoming/words/<name>/ ; runw.sh runs 4 Blender processes in parallel
tools/blender/runw.sh full ./incoming/words dad:hop gym:wiggle            # or: preview <dir> ...  (256px idle + sleep only)
python tools/blender/sheet_words.py <preview dir> out.png dad,gym       # contact sheet of previews
# mascot action loops (run jump swim eat look play go sit read kick catch hug) with the camera of the existing idle
"$BL" -b --python tools/blender/render_mascot.py -- full ./incoming/mascot [action,action]
# lowercase letter "no" (frown + head shake, 12 f, FRONT camera like the idle tile); needs the original letter .blend
"$BL" -b <game-assets>/letters/a/a.blend --python tools/blender/letters_no.py -- ./incoming/letters
# medals: idle + spin with a sparkle flash
"$BL" -b --python tools/blender/render_word.py -- medal_words50 spin full ./incoming/objects builders_medals.py nosleep,fixed=3.2
# library scene (same script as the night scenes): library bg / fg
"$BL" -b --python tools/blender/render_scene.py -- library bg ./incoming/scenes
```

- `builders_words3.py` — the 139 reader words (shared `person()` for people, mini-scene helpers for places, `coin()` with 1¢/5¢/10¢/25¢).
- `builders_mascot3.py` — mascot props + the 12 action verbs. `builders_medals.py` — the 10 medals.
- `tools/slim_reconvert.py <png roots>` re-converts every character whose original PNGs still reproduce the committed WebP
  (used after changing HEIGHT / quality in `convert_assets.py`); anything without matching PNGs is left untouched.
