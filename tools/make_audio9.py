# Voice batch 9: Horse Ranch names + arrival line. Run from repo root: python tools/make_audio9.py
import asyncio, os, edge_tts
VOICE="en-US-AnaNeural"; RATE="-5%"; OUT="assets/audio"
H={"chestnut":"Brown horse!","blackhorse":"Black horse!","whitehorse":"White horse!","palomino":"Golden horse!","pinto":"Patchy horse!","appaloosa":"Spotty horse!","dapple":"Grey horse!","clydesdale":"Big horse!","shetland":"Little pony!","foal":"Baby foal!","mustang":"Wild horse!","arabian":"Fast horse!","zebrah":"Zebra!","donkey":"Donkey!","unicornh":"Unicorn!","pegasus":"Pegasus!"}
jobs=[(f"horse_{k}",v) for k,v in H.items()]+[("p_hatched_horse","A new horse is here!")]
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
