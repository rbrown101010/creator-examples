import sys, json, re
slug = sys.argv[1]; SECS = int(sys.argv[2]) if len(sys.argv) > 2 else 150
R = json.load(open(f"work/{slug}.ranked.json"))
for i, r in enumerate(R["top"], 1):
    try: T = json.load(open(f"source/{slug}-transcripts/{r['id']}.json"))
    except FileNotFoundError: print(f"\n##### {i}. {r['title']} -- NO TRANSCRIPT"); continue
    print(f"\n##### {i}. {r['title']}  [{r['id']}] {r['duration_str']}")
    line = ""; last = -1
    for s in T["segments"]:
        if s["startMs"] > SECS * 1000: break
        sec = s["startMs"] // 1000
        if sec // 15 != last:  # timestamp marker every 15s
            line += f" ⟨{sec//60}:{sec%60:02d}⟩ "; last = sec // 15
        line += s["text"].strip() + " "
    print(re.sub(r"\s+", " ", line).strip())
