# Sound effect credits

All 12 files in this folder are original, synthesized by `tools/make_sfx.py` (numpy additive synthesis, encoded with ffmpeg).
No third-party recordings or samples are used, so there is nothing to attribute. Released as CC0 along with the script.

Why not downloaded: Pixabay sound effects are under the Pixabay Content License (not CC0), and freesound.org downloads
need a logged-in account, so synthesis (the fallback route in the brief) was used for every file.

| file | how it is made |
|---|---|
| pop.mp3 | marimba note at C5: fundamental + fast-decaying 4th and 10th partials (candidate "a" of 3) |
| wrong.mp3 | soft "boing": low sine falling 240 → 150 Hz with a little wobble |
| win.mp3 | glockenspiel arpeggio C5 E5 G5 C6 (inharmonic bell partials) |
| whoosh.mp3 | band-passed white noise with a rising-then-falling filter sweep |
| combo.mp3 | marimba + glockenspiel run C5 → E6, bell (G6 + C7) at the end |
| crack.mp3 | four short shell ticks: band-limited noise burst + 950 Hz knock |
| hatch.mp3 | five shell ticks, soft pop, then pentatonic glockenspiel sparkle and a C major bell chord |
| chest.mp3 | creak (stick-slip pulses on wood resonances), lid thunk, rising shimmer |
| star.mp3 | single twinkle: two bell notes E6 + B6 |
| tap.mp3 | tiny 1.1 kHz click, 80 ms |
| roar.mp3 | friendly "rawr": voiced harmonics through vowel formants, pitch 270 → 440 → 230 Hz, light growl |
| splash.mp3 | filtered noise burst with a falling sweep + five little bubble chirps |

Re-create: `python tools/make_sfx.py sfx` (deterministic, fixed random seed).
