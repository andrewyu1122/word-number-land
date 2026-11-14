# Word & Number Land — project guide for Claude (Code)

A spelling + counting web game for two kids (Jaron ~4, Jaden ~2½), published on GitHub Pages:
https://andrewyu1122.github.io/word-number-land/  (repo: andrewyu1122/word-number-land, branch `main`).
Everything is one static page: `index.html` + `sw.js` + `manifest.webmanifest` + `assets/`. No build step.

## What the game is
- **Spell**: picture is asleep (grey + 💤). Kid taps letter characters in order; correct letter flies into its slot and
  jumps; wrong one shakes. When the word is complete the picture wakes up (flash + colour + its animation + particles)
  and the recorded voice spells it ("Dog! D, O, G. Dog!"). 4 levels: 3-letter / 4-letter / big / super words.
- **Count**: number characters stand on a scene (`a op b = ?`). Big numeral labels float above each character.
  Correct answer makes the "?" character pop into the answer and everyone dances. Levels: ≤10, ≤20, ≤100 (keypad), ×.
- **Adventure map**: 14 stations through 7 scene worlds (meadow→road→sky→sea→room→night→space), alternating
  spell/math, difficulty rising. 2★ needed to unlock the next station.
- **Daily quest** (5 spell + 5 count → a treasure object), **Star garden** (grows with stars, plants have 3 stages,
  animals wander), **Sticker album**, **profiles** (per-kid progress), **PWA** (offline, installable).
- Adaptive: spaced repetition per word (`store.sr`), math skill per level from last 12 results (`store.mr`).

## Files
- `index.html` — all HTML/CSS/JS. Key constants near the top of the script: `WORDS` (levels→[word, emoji, anim]),
  `ART` (word→animation type for words that have 3D art), `OBJECTS`, `PLANTS/WALKERS/FLYERS`, `AVATARS`.
  State lives in `root` (localStorage key `wnl_v3`): `root.profiles[]`, `root.current`, `root.settings`.
  `store` = the active profile.
- `sw.js` — service worker. **Bump `VERSION` on every deploy** (v1, v2, …) or users keep old files.
  `CORE` is the pre-cached list (letters, numbers, scenes, mascot, garden, objects, small audio); words & big audio
  are cached on first use.
- `assets/` — all WebP art and MP3 voice. `assets/credits*.json` = Sketchfab attributions.
- `tools/convert_assets.py` — PNG renders → WebP (see below).

## Asset conventions (Blender renders)
- Transparent PNG, 512×512, same camera/lights for everything (3/4 view, feet on the ground ~20% from bottom).
- Stills: `{name}_idle.png`, `{name}_sleep.png` (words only, eyes closed).
- Animations: `{name}_{action}_001.png … _024.png` (24 fps, loops). Objects/garden animals use 12 frames.
- Word actions: hop, drive, fly, swim, wiggle, spin, float, grow, flash, ring. drive/swim/fly animate **in place**;
  the game moves them across the stage with CSS.
- Numbers `n0…n10, nq` (`nq` = the "?" character). Letters: lowercase `a…z`, uppercase `A…Z` (`assets/letters_upper/`).
- Mascot states: idle, sleep, happy, cheer, wave, think.
- Garden: plants `{name}_s1/s2/s3.png` (3 growth stages), animals `{name}_idle.png` + `{name}_fly|walk_###.png`.
- Dino Island (`assets/dino/`): 16 dinos `{name}_idle.png`, `{name}_walk_###`, `{name}_roar_###`; egg `egg_s0..s3.png`, `egg_hatch_###`; scene `island`.
  Names are in `DINOS` in index.html. Until a dino's files exist the game shows an emoji (`DINO_MISSING` fallback).
- Operators (`assets/num/op_plus|op_minus|op_times|op_equals`): `_idle.webp` + `_bounce.webp` (12 frames). Treasure chest
  (`assets/objects/chest_closed.webp`, `chest_open.webp`, `chest_open_anim.webp`): when a still and a sequence share a state
  name the converter writes the sequence as `{state}_anim`.
- Sea collection (also in `assets/dino/`): 16 sea creatures `{name}_idle/_swim_###/_happy_###` (clownfish seahorse jellyfish starfish turtle octopus crab dolphin whale shark pufferfish lobster seal penguin narwhal manta), egg `seaegg_s0..s3` + `seaegg_hatch_###`, scene `reef`.
  Toddler mode (`assets/objects/`): shapes circle square triangle star heart and colours red blue yellow green orange purple pink black white, `_idle` + `_jump` (12f).
  Island levels `island_2/3`, Christmas `{scene}_xmas`, `mascot_xmas_idle/_wave`, `objects/hat_santa.png`.
- **Asset refresh (Nov 2026)**: `wb.py` action curves were enlarged (drive 12 cm bounce ±6°, wiggle ±22° + 10% pulse, fly/swim/float bigger; animals with `legs` handles trot). `mascot_idle.webp` is now a 48-frame breathing loop (blink once per loop); mascot_wave uses both arms.
  Scene foreground layers `assets/scenes/{scene}_fg.webp` (RGBA, props in the bottom ~20%) exist for the 7 worlds + island/island_2/island_3/reef; draw them above the characters.
  Numbers: `python tools/align_num.py <png folders> [--out assets/num]` re-crops every n0–n100/nq with one rule (5% pad under the idle feet, 35% headroom) so sizes and feet rows match; re-run it whenever a number is re-rendered.
  `tools/review_sheets.py` builds contact sheets + metrics into `tools/review/`.
- Scenes: 1200×750 opaque, bottom quarter is ground, nothing busy in the centre: meadow sea sky road space room night.

## Converting & publishing new art
```
python tools/convert_assets.py words   ./incoming/words --update-art   # also refreshes ART in index.html
python tools/convert_assets.py letters ./incoming/letters              # etc: upper num objects garden mascot bosses scenes
```
The converter crops every state of a character with ONE shared box (so idle/jump line up), scales to a fixed height,
and writes animated WebP. Then:
1. edit `sw.js`: bump `VERSION`; if you added a new asset folder, add its files to `CORE` (small folders only).
2. `git add -A && git commit -m "..." && git push` — GitHub Pages updates in ~1 min; the app shows a green
   "New version ready" bar.

## Read mode & reader vocabulary
- **Read** (home tile): sight words (`SIGHT`, 50 words) — L1 hear & find the word, L2 spell it (reuses the spelling screen with `sight:true`), L3/L4 build a sentence from word tiles (`SENT_EASY` / `SENT_HARD` templates + a picture noun). Progress in `store.sw`, levels in `store.lvl.read1..4`.
- `EXTRA_WORDS` in index.html lists ~140 picture words from the kids' readers. A word joins the game only when it appears in `ART` (after its 3D art is converted with `--update-art`). Voice: `tools/make_audio8.py`.

## Medals
`MEDALS` + `medalEarned()` in index.html; art `assets/objects/medal_{name}_{idle,spin}.webp`; earned medals in `store.medals`; shown in the album and awarded by `checkMedals()` after a round or a hatch.
Read-mode action sentences use `assets/mascot/mascot_{verb}.webp` (`VERBS`).

## Parent report, limits, hints
- `store.log[date]={secs,stars,words[]}` feeds Settings → Parent report (7-day minutes, learned / tricky words, math skill) and the Monday weekly recap.
- `store.limit` (minutes/day) shows the bedtime overlay; a grown-up holds the button for 5 more minutes.
- First-time hand hints: `root.tut.{home,spell,math,hunt}`; `pointAt(el)` / `tutDone(k)`.
- `readyGo()` plays a "Ready? Go!" before each round. `celebrate(level)` picks one of four celebration effects.

## Sound effects & music
`assets/sfx/*.mp3` and `assets/music/{home,map,play}.mp3` — see the README in each folder for the exact list and specs.
Loaded by `loadSfx()` / `setTrack()`; every sound has a synthesized fallback, so missing files never break anything.
Praise lines `p_praise1..8` are played after a perfect word.

## Family sync
Firebase Firestore project `word-land-121a6` (config in index.html `FB_CFG`, anonymous auth). Data: `families/{CODE}/profiles/{profileId}`.
A 6-letter family code typed into Settings on each device shares all profiles. Merge is field-wise max/union (`mergeProfile`);
`resetAt` lets a reset win over older data. The Firebase SDK (compat, gstatic CDN) is loaded only when a code is set.

## Modes added later
- **Little mode** (profile flag `little`, Jaden default): 6 activities (Colors, Shapes, Count, ABC, Words, Match) × 5 levels each, `store.ll[kind]`; a round of 6 with ≤1 miss levels up, ≥6 misses levels down. See `renderLittle()`.
- **Christmas** (`root.settings.xmas` auto/on/off; auto = Dec 1–Jan 6): `sceneArt()`/`mascotArt()` pick `_xmas` variants, `body.xmas` adds Santa hats via CSS and snow.
- **Collections**: `SETS` in index.html — Dino Island (16) then Coral Reef (16, `assets/dino/{sea name}_*`, egg `seaegg`, scene `reef`). State in `store.dino` / `store.sea`. Add a set = push to `SETS` + art + voice (`tools/make_audio5.py` pattern).
- **Horse Ranch** (`SET_HORSE`, 16 horses in `HORSES`): a third collection. Each profile has `theme` ('dino' | 'horse', chosen in Edit player; Jaden = horse) which decides which collection comes first in `SETS`. Art lives in `assets/dino/` like the others: `{id}_idle/walk/happy/eat/sleep/run`, the "egg" is a barn door `barn_s0..s3` + `barn_hatch`, scenes `ranch`, `ranch_2`, `ranch_3` (+ `_night`, `_fg`). Voice `horse_{id}` + `p_hatched_horse` (`tools/make_audio9.py`), sound `assets/sfx/neigh.mp3`.
- **Island life** (`startIslandLife`): creatures wander/idle/chat, `eat` when food is dropped (tap ground), `run` when playing chase, `sleep` at night (20:00–06:00 or the ☀️/🌙 toggle; scenes `*_night` + `*_night_fg`). Poking a sleeper wakes it briefly.
- **Island stages**: island / island_2 / island_3 by hatched count (6, 12).

## Voice
To add voice lines run `python tools/make_audio3.py` (needs `pip install edge-tts`, internet) — it writes into `assets/audio/` and skips files that exist.
Pre-recorded with Edge TTS voice `en-US-AnaNeural` (scripts in the chat history: `make_audio.py`, `make_audio2.py`).
Keys: `w_{word}` (word), `s_{word}` (spelled celebration), `l_{letter}` (name), `f_{letter}` (phonics sound),
`n_{0-100}`, `x_{0-100}` (excited), `q_{a}p{b}` / `a_{a}p{b}` (whole addition question/answer ≤20; `m` for minus),
`p_*` phrases, `p_combo3/5/8`. `say(keys, fallbackText, altKeys)` in index.html plays a sequence; missing files fall
back to `altKeys`, then to the browser's speechSynthesis.

## Design rules (please keep)
- Kid-first: huge tap targets, no text he must read, every success has sound + motion + confetti.
- Home shows only: Adventure hero, Spell, Count, Today's quest, Stickers, garden. Parent stuff lives behind ⚙️.
- No counting objects / clutter in the math stage — the number characters ARE the visual.
- Audio must be unlocked by the ▶ start button (mobile autoplay rules). Never autoplay before it.
- Keep `index.html` self-contained; relative asset paths (`assets/...`) because the site lives under `/word-number-land/`.
- Test at 420×900 (phone), 1180×820 (iPad landscape), 1280×900 (desktop) before pushing.

## Ideas not yet built
Parent dashboard (per-word accuracy, time limits, custom words), toddler mode for Jaden, listening-only spelling,
find-the-wrong-letter, number-merge animation (3 + 4 walk together → 7), scene "bosses" at the end of each world,
treasure-chest opening animation, 11–20 as single characters, animated operator symbols, hats/accessories shop.

## Blender pipeline (in the repo since Nov 2026)
`tools/blender/` holds the headless scripts for the two collections and the night scenes (see its README): `render_char.py`
renders idle + walk/roar (swim/happy) + **eat / sleep / run** for one character with a single camera; `render_scene.py` renders
`island_night`, `island_2_night`, `island_3_night`, `reef_night` and their `_fg` layers. Every dino / sea creature now has
`{name}_eat|sleep|run.webp` in `assets/dino/`. Sleep is a lying-down breathing loop (frame 1 is not idle — cross-fade in/out).
- Asset sizes (Nov 2026 slimming): `convert_assets.py` now uses words/dino height 320, bosses 420, animated WebP quality 74.
  `python tools/slim_reconvert.py ./incoming <other png roots>` re-converts only characters whose source PNGs match what is committed.
- Added art: mascot verbs `mascot_{run,jump,swim,eat,look,play,go,sit,read,kick,catch,hug}.webp`, scene `library` + `library_fg`,
  lowercase `{letter}_no.webp` (head shake), medals `assets/objects/medal_{words50,words100,words200,math,hunt,read,dino,sea,streak7,map}_{idle,spin}.webp`.
