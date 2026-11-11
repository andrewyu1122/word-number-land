# Voice batch 7: prompts for Little mode. Run from repo root: python tools/make_audio7.py
import asyncio, os, edge_tts
VOICE="en-US-AnaNeural"; RATE="-5%"; OUT="assets/audio"
jobs=[("p_whatis","What is"),("p_different","Which one is different?"),("p_howmany","How many?"),("p_more","Which has more?"),
      ("p_findletter","Find the letter"),("p_whereis","Where is the"),("p_shadow","Find my shadow!"),("p_pairs","Find the pairs!"),("p_levelup","Level up!")]
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
