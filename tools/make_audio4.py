# Voice lines batch 4: 49 new words (w_/s_), toddler-mode phrases, colours and shapes. Run from repo root: python tools/make_audio4.py
import asyncio, os, edge_tts
VOICE="en-US-AnaNeural"; RATE="-5%"; OUT="assets/audio"
WORDS="van log gem pot pan net tub jar axe bow saw jam ham bun mug pin elf ape emu yak sock lamp door lock nest shoe boot coat hand foot nose wave road bone soap salt rice soup pear kiwi taco crow dove bull lamb pony toad hawk moth".split()
jobs=[]
for w in WORDS:
    jobs.append((f"w_{w}", f"{w}."))
    jobs.append((f"s_{w}", f"{w.capitalize()}! {', '.join(w.upper())}. {w.capitalize()}!"))
jobs+=[("p_whichcolor","Which one is"),("p_tapthe","Tap the"),("p_welldone","Well done!"),("p_wow","Wow!")]
jobs+=[(f"c_{c}", c) for c in "red blue yellow green orange purple pink black white".split()]
jobs+=[(f"sh_{s}", s) for s in "circle square triangle star heart".split()]
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
