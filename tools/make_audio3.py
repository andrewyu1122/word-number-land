# Voice lines batch 3: dinosaur names, hunt prompts, hatch phrase. Run from repo root: python tools/make_audio3.py
import asyncio, os, edge_tts
VOICE="en-US-AnaNeural"; RATE="-5%"; OUT="assets/audio"
DINOS=["trex","triceratops","stegosaurus","brachiosaurus","pterodactyl","velociraptor","ankylosaurus","parasaurolophus","spinosaurus","diplodocus","pachycephalosaurus","plesiosaurus","iguanodon","allosaurus","dilophosaurus","archaeopteryx"]
SAY={"trex":"T. Rex!"}
jobs=[(f"d_{d}", SAY.get(d, d.capitalize()+"!")) for d in DINOS]
jobs+=[("p_hatched","A new dinosaur hatched!"),("p_which","Which ones start with"),("p_whichlike","Which ones start like"),("p_letsplay","Let\u2019s play!")]
async def one(name,text,sem):
    path=f"{OUT}/{name}.mp3"
    if os.path.exists(path) and os.path.getsize(path)>500: return
    async with sem:
        for _ in range(3):
            try: await edge_tts.Communicate(text,VOICE,rate=RATE).save(path); return
            except Exception: await asyncio.sleep(2)
        print("FAILED",name)
async def main():
    os.makedirs(OUT,exist_ok=True); sem=asyncio.Semaphore(6)
    await asyncio.gather(*(one(n,t,sem) for n,t in jobs)); print("done",len(jobs))
asyncio.run(main())
