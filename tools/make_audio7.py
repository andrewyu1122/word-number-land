# Voice batch 7: praise lines played after a perfect word (p_praise1..8). Same voice as every other batch.
# (make_audio6.py was already taken by the phonics re-do, so this batch is 7.)
# Run from repo root: python tools/make_audio7.py   (skips files that exist)
import asyncio, os, edge_tts
VOICE="en-US-AnaNeural"; RATE="-5%"; OUT="assets/audio"
PRAISE=["Great!","Awesome!","You did it!","Super!","Fantastic!","Wonderful!","Yes!","Brilliant!"]
jobs=[(f"p_praise{i+1}",t) for i,t in enumerate(PRAISE)]
async def one(name,text,sem):
    path=f"{OUT}/{name}.mp3"
    if os.path.exists(path) and os.path.getsize(path)>500: return
    async with sem:
        for _ in range(3):
            try: await edge_tts.Communicate(text,VOICE,rate=RATE).save(path); return
            except Exception: await asyncio.sleep(2)
        print("FAILED",name)
async def main():
    os.makedirs(OUT,exist_ok=True); sem=asyncio.Semaphore(6); await asyncio.gather(*(one(n,t,sem) for n,t in jobs)); print("done",len(jobs))
asyncio.run(main())
