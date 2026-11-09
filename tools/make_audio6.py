# Phonics re-do (task 6): vowels and c g q x y with "sound, sound, word" spelling so the letter sound is unambiguous.
# Run from repo root: python tools/make_audio6.py   (overwrites the ten f_*.mp3 files)
import asyncio, os, edge_tts
VOICE="en-US-AnaNeural"; RATE="-5%"; OUT="assets/audio"
PH = {"a":"ah, ah, apple", "e":"eh, eh, elephant", "i":"ih, ih, igloo", "o":"aw, aw, octopus", "u":"uh, uh, umbrella",
      "c":"kuh, kuh, cat", "g":"guh, guh, goat", "q":"kwuh, kwuh, queen", "x":"ks, ks, fox", "y":"yuh, yuh, yellow"}
async def one(name, text, sem):
    async with sem:
        for _ in range(3):
            try: await edge_tts.Communicate(text, VOICE, rate=RATE).save(f"{OUT}/{name}.mp3"); return
            except Exception: await asyncio.sleep(2)
        print("FAILED", name)
async def main():
    sem = asyncio.Semaphore(6); await asyncio.gather(*(one(f"f_{l}", t, sem) for l, t in PH.items())); print("done", len(PH))
asyncio.run(main())
