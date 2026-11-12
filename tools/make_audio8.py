# Voice batch 8: sight words + the readers' picture vocabulary. Run from repo root: python tools/make_audio8.py
import asyncio, os, edge_tts
VOICE="en-US-AnaNeural"; RATE="-5%"; OUT="assets/audio"
SIGHT=["a", "i", "am", "the", "we", "had", "she", "has", "like", "have", "look", "at", "my", "play", "with", "see", "some", "he", "are", "can", "you", "go", "in", "mom", "is", "this", "big", "little", "likes", "me", "here", "that", "goes", "up", "there", "dad", "wants", "to", "they", "all", "get", "will", "do", "it", "be", "and", "down", "said", "went", "eat"]
WORDS=["dad", "gym", "mat", "mom", "ox", "sky", "toe", "band", "bank", "bean", "bush", "chef", "clam", "dime", "dirt", "dish", "doll", "gate", "horn", "lake", "mall", "newt", "park", "pool", "ramp", "room", "rope", "sail", "sand", "tire", "town", "vest", "wind", "beach", "beetle", "berry", "bunny", "camera", "canoe", "celery", "chair", "cheese", "chick", "circle", "coach", "crayon", "desert", "doctor", "dollar", "eraser", "family", "farmer", "field", "finger", "forest", "fruit", "glove", "goose", "heron", "hotdog", "igloo", "iguana", "insect", "jaguar", "juice", "kitten", "marker", "museum", "nickel", "nurse", "olive", "otter", "penny", "pepper", "pilot", "puppy", "quail", "queen", "quilt", "raisin", "river", "sandal", "school", "shell", "shirt", "slide", "soccer", "square", "steps", "street", "stripe", "tennis", "violet", "wagon", "walrus", "zipper", "alligator", "apartment", "aquarium", "baseball", "brother", "caterpillar", "classroom", "cracker", "cucumber", "diamond", "eggplant", "envelope", "feather", "firefighter", "fountain", "grasshopper", "houseboat", "invitation", "janitor", "library", "lightning", "nectarine", "pelican", "playground", "pretzel", "quarter", "raccoon", "racecar", "rectangle", "restaurant", "sailboat", "salamander", "starfish", "sunglasses", "sweater", "teacher", "television", "triangle", "underwear", "vegetable", "vulture", "waterfall", "watermelon"]
def spell(w): return f"{w.capitalize()}! " + ", ".join(c.upper() for c in w) + f". {w.capitalize()}!"
jobs=[]
for w in SIGHT:
    say = "I" if w=="i" else ("A" if w=="a" else w)
    jobs.append((f"w_{w}", say + "."))          # existing w_* files are skipped automatically
    if len(w)>=2: jobs.append((f"s_{w}", spell(w)))
for w in WORDS:
    jobs.append((f"w_{w}", w + "."))
    jobs.append((f"s_{w}", spell(w)))
jobs.append(("p_findword","Find the word"))
for v in ['run','jump','swim','sit','read','kick','catch','hug']:
    jobs.append((f"w_{v}", v + "."))
jobs.append(("p_medal","You won a medal!"))
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
