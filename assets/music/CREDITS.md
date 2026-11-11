# Music credits

All three loops are original compositions, written as note lists in `tools/make_sfx.py` (`SONGS`) and synthesized with
numpy (marimba / soft bell / glockenspiel / plucked strings / soft bass). No third-party audio, no vocals. Released as CC0.

Why not downloaded: Pixabay Music is under the Pixabay Content License (not CC0), so the synthesis route was used.

| file | key / chords | tempo | length | instruments |
|---|---|---|---|---|
| home.mp3 | C major, C–Am–F–G | 88 bpm | 24 bars, 65.5 s | marimba melody, plucked arpeggio, soft bass |
| map.mp3 | C major, C–G–Am–F | 116 bpm | 32 bars, 66.2 s | marimba + glockenspiel melody, off-beat strums, bouncy bass, quiet shaker |
| play.mp3 | C major, C–F–Am–G | 96 bpm | 24 bars, 60.0 s | soft bell melody (long notes), steady marimba pattern, soft bass |

Seamless loop: each track is exactly a whole number of bars and the note tails / echo of the last bar are wrapped round
into the first bar, so the end flows into the start.

Re-create: `python tools/make_sfx.py music`.
