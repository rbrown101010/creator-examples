import sys, json, subprocess, time
from yt_dlp import YoutubeDL
handle = sys.argv[1]; cutoff = "20250921"
flat = json.loads(subprocess.run(["python3","-m","yt_dlp","--flat-playlist","-J","--playlist-end","600",f"https://www.youtube.com/@{handle}/videos"],capture_output=True,text=True).stdout)
entries = flat["entries"]; chan = {"channel": flat.get("channel"), "channel_id": flat.get("channel_id"), "subs": flat.get("channel_follower_count"), "handle": handle, "listed": len(entries)}
json.dump(chan, open(f"work/{handle}.channel.json","w"))
out = open(f"work/{handle}.meta.jsonl","w"); older = 0; n = 0
ydl = YoutubeDL({"quiet": True, "no_warnings": True, "skip_download": True, "extractor_args": {"youtube": {"player_skip": ["js"]}}})
for e in entries:
    try:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={e['id']}", download=False)
    except Exception as ex:
        out.write(json.dumps({"id": e["id"], "error": str(ex)[:120]})+"\n"); continue
    row = {k: info.get(k) for k in ("id","title","view_count","upload_date","duration","like_count","is_live","was_live")}
    out.write(json.dumps(row)+"\n"); out.flush(); n += 1
    if (row["upload_date"] or "99999999") < cutoff:
        older += 1
        if older >= 6: break
    else: older = 0
open(f"work/{handle}.done","w").write(f"{n} videos\n")
