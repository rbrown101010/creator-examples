import sys, json, statistics, re
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi
handle, slug = sys.argv[1], sys.argv[2]; CUT = "20250921"; TOP = 10
chan = json.load(open(f"work/{handle}.channel.json"))
rows = [json.loads(l) for l in open(f"work/{handle}.meta.jsonl") if l.strip()]
ok = [r for r in rows if not r.get("error") and r.get("view_count") is not None and (r.get("upload_date") or "") >= CUT and (r.get("duration") or 0) >= 120 and not r.get("is_live")]
med = statistics.median(r["view_count"] for r in ok)
for r in ok: r["outlier"] = round(r["view_count"] / med, 2)
ok.sort(key=lambda r: -r["view_count"])
print(f"{chan['channel']} ({chan['channel_id']}): {len(rows)} fetched, {len(ok)} past-year long-form, median {med:,.0f}")
top = ok[:TOP]
Path(f"source/{slug}-transcripts").mkdir(parents=True, exist_ok=True)
api = YouTubeTranscriptApi()
for i, r in enumerate(top, 1):
    d = r["upload_date"]; r["published"] = f"{d[:4]}-{d[4:6]}-{d[6:]}"
    m, s = divmod(int(r["duration"]), 60); h, m = divmod(m, 60); r["duration_str"] = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
    try:
        t = api.fetch(r["id"], languages=["en", "en-US", "en-GB"])
        segs = [{"startMs": int(x.start * 1000), "endMs": int((x.start + x.duration) * 1000), "text": x.text.replace("\n", " ")} for x in t]
        json.dump({"videoId": r["id"], "language": t.language_code, "generated": t.is_generated, "segments": segs, "fullText": " ".join(x["text"] for x in segs)}, open(f"source/{slug}-transcripts/{r['id']}.json", "w"))
        r["transcript"] = "ok"
    except Exception as e:
        r["transcript"] = f"FAIL {type(e).__name__}"
    print(f"{i:2}. {r['outlier']:5.2f}x {r['view_count']:>10,} {r['published']} {r['duration_str']:>8} {r['id']} {r['transcript']:<8} {r['title'][:70]}")
json.dump({"channel": chan, "median": med, "count_past_year": len(ok), "top": top}, open(f"work/{slug}.ranked.json", "w"), indent=1)
