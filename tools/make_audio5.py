# Voice batch 5: sea creature names (s_{name} keys clash with spelled words? no: words use s_{word} too — so we use sea_ prefix)
import asyncio, os, edge_tts
VOICE="en-US-AnaNeural"; RATE="-5%"; OUT="assets/audio"
SEA={"clownfish":"Clownfish!","seahorse":"Seahorse!","jellyfish":"Jellyfish!","starfish":"Starfish!","turtle":"Sea turtle!","octopus":"Octopus!","crab":"Crab!","dolphin":"Dolphin!","whale":"Whale!","shark":"Shark!","pufferfish":"Pufferfish!","lobster":"Lobster!","seal":"Seal!","penguin":"Penguin!","narwhal":"Narwhal!","manta":"Manta ray!"}
jobs=[(f"sea_{k}",v) for k,v in SEA.items()]+[("p_newworld","You found them all! A new world is open!")]
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
