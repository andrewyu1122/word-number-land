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
