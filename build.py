#!/usr/bin/env python3
"""Build the Creator Examples static site from data/*.json into site/.
Plain HTML, no CSS. Run: python3 build.py   (set BASE_URL env to override config.json)."""
import json, os, re, shutil, html
from pathlib import Path

ROOT = Path(__file__).parent
SITE = ROOT / "site"
CFG = json.load(open(ROOT / "config.json"))
BASE = os.environ.get("BASE_URL", CFG["base_url"]).rstrip("/")

CREATORS = [  # order on the Intros page
    ("theo", "Theo", "data/theo.json"),
    ("riley-brown", "Riley Brown", "data/riley-brown.json"),
    ("greg-isenberg", "Greg Isenberg", "data/greg-isenberg.json"),
    ("alex-hormozi", "Alex Hormozi", "data/alex-hormozi.json"),
    ("kallaway", "Kallaway", "data/kallaway.json"),
]

SHORT_FORM = [  # order on the Short Form page
    ("kallaway", "Kallaway", "data/short-form/kallaway.json"),
    ("dylan-page", "Dylan Page", "data/short-form/dylan-page.json"),
    ("roberto-nickson", "Roberto Nickson (RPN)", "data/short-form/roberto-nickson.json"),
    ("cleo-abram", "Cleo Abram", "data/short-form/cleo-abram.json"),
    ("nick-saraev", "Nick Saraev", "data/short-form/nick-saraev.json"),
    ("natalie-fratto", "Natalie Fratto", "data/short-form/natalie-fratto.json"),
]

def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:70].rstrip("-")

def page(title, body, path):
    doc = f"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<title>{html.escape(title)}</title>\n</head>\n<body>\n{body}\n</body>\n</html>\n"
    p = SITE / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(doc)

def esc(s): return html.escape(str(s))

if SITE.exists(): shutil.rmtree(SITE)
SITE.mkdir()
urls = ["/", "/intros/", "/short-form/"]
llms = ["# Creator Examples", "",
        "> A plain-text database of creator content examples (YouTube intros, short-form video scripts, and more), kept by Riley Brown. Every page is unstyled HTML. Machine-readable JSON lives under /data/.", "",
        f"- Home: {BASE}/", f"- Intros index: {BASE}/intros/", f"- Short Form index: {BASE}/short-form/", f"- Data index: {BASE}/data/index.json", f"- Skill for agents: {BASE}/skill/SKILL.md", ""]

# home
page("Creator Examples",
     "<h1>Creator Examples</h1>\n<p>Plain-text examples of creator content, organized by type and creator.</p>\n<ul>\n<li><a href=\"/intros/\">Intros</a></li>\n<li><a href=\"/short-form/\">Short Form</a></li>\n</ul>\n<p><a href=\"/llms.txt\">llms.txt</a> | <a href=\"/data/index.json\">data/index.json</a></p>",
     "index.html")

# intros index
items = "\n".join(f"<li><a href=\"/intros/{cslug}/\">{esc(name)}</a></li>" for cslug, name, _ in CREATORS)
page("Intros", f"<h1>Intros</h1>\n<p>Up: <a href=\"/\">Creator Examples</a></p>\n<ul>\n{items}\n</ul>", "intros/index.html")

data_index = {"creators": []}
for cslug, name, dfile in CREATORS:
    d = json.load(open(ROOT / dfile))
    intros = d["intros"]
    llms.append(f"## Intros: {name}")
    llms.append(f"- Creator page: {BASE}/intros/{cslug}/")
    llms.append(f"- JSON: {BASE}/data/{cslug}.json")
    llms.append(f"- Method: {d['method']}")
    lis = []
    for k, it in enumerate(intros):
        s = f"{it['rank']:02d}-{slug(it['title'])}"
        it["_slug"] = s
        lis.append(f"<li><a href=\"/intros/{cslug}/{s}/\">{esc(it['title'])}</a> ({it['views']:,} views)</li>")
        llms.append(f"- {BASE}/intros/{cslug}/{s}/ : {it['title']} ({it['views']:,} views)")
        urls.append(f"/intros/{cslug}/{s}/")
    llms.append("")
    urls.append(f"/intros/{cslug}/")
    body = (f"<h1>{esc(name)}</h1>\n<p>Up: <a href=\"/intros/\">Intros</a></p>\n"
            f"<p>Channel: <a href=\"{esc(d['channel_url'])}\">{esc(d['handle'])}</a></p>\n"
            f"<p>{esc(d['method'])}</p>\n<p>Snapshot: {esc(d['snapshot_date'])}. Data: <a href=\"/data/{cslug}.json\">{cslug}.json</a></p>\n"
            f"<ol>\n" + "\n".join(lis) + "\n</ol>")
    page(f"{name} intros", body, f"intros/{cslug}/index.html")
    for k, it in enumerate(intros):
        nxt = intros[k + 1] if k + 1 < len(intros) else None
        prv = intros[k - 1] if k > 0 else None
        meta = [f"Creator: <a href=\"/intros/{cslug}/\">{esc(name)}</a>",
                f"Source video: <a href=\"{esc(it['url'])}\">{esc(it['url'])}</a>",
                f"Published: {esc(it['published'])}", f"Views: {it['views']:,}", f"Duration: {esc(it['duration'])}"]
        if it.get("outlier_multiplier"): meta.append(f"Outlier multiplier vs channel median: {it['outlier_multiplier']}x")
        if it.get("intro_ends_at"): meta.append(f"Intro ends at: {esc(it['intro_ends_at'])} ({esc(it.get('intro_ends_reason',''))})")
        elif it.get("intro_ends_reason"): meta.append(f"Intro ends: {esc(it['intro_ends_reason'])}")
        nav = [f"<a href=\"/intros/{cslug}/\">Up: {esc(name)}</a>"]
        if prv: nav.append(f"<a href=\"/intros/{cslug}/{prv['_slug']}/\">Previous</a>")
        if nxt: nav.append(f"<a href=\"/intros/{cslug}/{nxt['_slug']}/\">Next</a>")
        body = (f"<h1>{esc(it['title'])}</h1>\n<p>{' | '.join(nav)}</p>\n<ul>\n" + "\n".join(f"<li>{m}</li>" for m in meta) + "\n</ul>\n"
                f"<h2>Intro</h2>\n" + "\n".join(f"<p>{esc(para)}</p>" for para in it['intro'].split("\n") if para.strip()) + "\n")
        if it.get("rest_of_video"):
            body += "<h2>Rest of video</h2>\n<ul>\n" + "\n".join(f"<li>{esc(b)}</li>" for b in it["rest_of_video"]) + "\n</ul>\n"
        body += f"<p>{' | '.join(nav)}</p>"
        page(f"{it['title']} - {name} intro", body, f"intros/{cslug}/{it['_slug']}/index.html")
    clean = {k: v for k, v in d.items()}
    clean["intros"] = [{k: v for k, v in it.items() if not k.startswith("_")} | {"page": f"{BASE}/intros/{cslug}/{it['_slug']}/"} for it in intros]
    (SITE / "data").mkdir(exist_ok=True)
    json.dump(clean, open(SITE / "data" / f"{cslug}.json", "w"), indent=1)
    data_index["creators"].append({"name": name, "slug": cslug, "type": "intros", "page": f"{BASE}/intros/{cslug}/", "json": f"{BASE}/data/{cslug}.json", "count": len(intros)})

# short form: full transcripts of top short-form videos
items = "\n".join(f"<li><a href=\"/short-form/{cslug}/\">{esc(name)}</a></li>" for cslug, name, _ in SHORT_FORM)
page("Short Form", f"<h1>Short Form</h1>\n<p>Up: <a href=\"/\">Creator Examples</a></p>\n<p>Full transcripts of each creator's most-viewed short-form videos.</p>\n<ul>\n{items}\n</ul>", "short-form/index.html")
(SITE / "data" / "short-form").mkdir(parents=True, exist_ok=True)
for cslug, name, dfile in SHORT_FORM:
    d = json.load(open(ROOT / dfile))
    vids = d["videos"]
    llms.append(f"## Short Form: {name}")
    llms.append(f"- Creator page: {BASE}/short-form/{cslug}/")
    llms.append(f"- JSON: {BASE}/data/short-form/{cslug}.json")
    llms.append(f"- Method: {d['method']}")
    lis = []
    for it in vids:
        s = f"{it['rank']:02d}-{slug(it['title'])}"
        it["_slug"] = s
        tag = " [sponsored]" if it.get("sponsored") else ""
        lis.append(f"<li><a href=\"/short-form/{cslug}/{s}/\">{esc(it['title'])}</a> ({it['views']:,} views){tag}</li>")
        llms.append(f"- {BASE}/short-form/{cslug}/{s}/ : {it['title']} ({it['views']:,} views){tag}")
        urls.append(f"/short-form/{cslug}/{s}/")
    llms.append("")
    urls.append(f"/short-form/{cslug}/")
    body = (f"<h1>{esc(name)}</h1>\n<p>Up: <a href=\"/short-form/\">Short Form</a></p>\n"
            f"<p>Profile: <a href=\"{esc(d['profile_url'])}\">{esc(d['handle'])}</a> ({esc(d['platform'])})</p>\n"
            f"<p>{esc(d['method'])}</p>\n<p>Snapshot: {esc(d['snapshot_date'])}. Data: <a href=\"/data/short-form/{cslug}.json\">short-form/{cslug}.json</a></p>\n"
            f"<ol>\n" + "\n".join(lis) + "\n</ol>")
    page(f"{name} short form", body, f"short-form/{cslug}/index.html")
    for k, it in enumerate(vids):
        nxt = vids[k + 1] if k + 1 < len(vids) else None
        prv = vids[k - 1] if k > 0 else None
        meta = [f"Creator: <a href=\"/short-form/{cslug}/\">{esc(name)}</a>",
                f"Source video: <a href=\"{esc(it['url'])}\">{esc(it['url'])}</a>",
                f"Published: {esc(it['published'])}", f"Views: {it['views']:,}"]
        if it.get("likes") is not None: meta.append(f"Likes: {it['likes']:,}")
        if it.get("comments") is not None: meta.append(f"Comments: {it['comments']:,}")
        meta.append(f"Duration: {esc(it['duration'])}")
        if it.get("sponsored"): meta.append("Sponsored: yes (paid partnership or partner tag on Instagram)")
        nav = [f"<a href=\"/short-form/{cslug}/\">Up: {esc(name)}</a>"]
        if prv: nav.append(f"<a href=\"/short-form/{cslug}/{prv['_slug']}/\">Previous</a>")
        if nxt: nav.append(f"<a href=\"/short-form/{cslug}/{nxt['_slug']}/\">Next</a>")
        body = (f"<h1>{esc(it['title'])}</h1>\n<p>{' | '.join(nav)}</p>\n<ul>\n" + "\n".join(f"<li>{m}</li>" for m in meta) + "\n</ul>\n"
                f"<h2>Transcript</h2>\n" + "\n".join(f"<p>{esc(para)}</p>" for para in it['transcript'].split("\n") if para.strip()) + "\n")
        if it.get("caption"):
            body += "<h2>Caption</h2>\n" + "\n".join(f"<p>{esc(para)}</p>" for para in it['caption'].split("\n") if para.strip()) + "\n"
        body += f"<p>{' | '.join(nav)}</p>"
        page(f"{it['title']} - {name} short form", body, f"short-form/{cslug}/{it['_slug']}/index.html")
    clean = {k: v for k, v in d.items()}
    clean["videos"] = [{k: v for k, v in it.items() if not k.startswith("_")} | {"page": f"{BASE}/short-form/{cslug}/{it['_slug']}/"} for it in vids]
    json.dump(clean, open(SITE / "data" / "short-form" / f"{cslug}.json", "w"), indent=1)
    data_index["creators"].append({"name": name, "slug": cslug, "type": "short-form", "page": f"{BASE}/short-form/{cslug}/", "json": f"{BASE}/data/short-form/{cslug}.json", "count": len(vids)})

json.dump(data_index, open(SITE / "data" / "index.json", "w"), indent=1)
(SITE / "llms.txt").write_text("\n".join(llms) + "\n")
(SITE / "sitemap.xml").write_text("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + "\n".join(f"<url><loc>{BASE}{u}</loc></url>" for u in urls) + "\n</urlset>\n")
(SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
shutil.copytree(ROOT / "skill", SITE / "skill")
print(f"built {sum(1 for _ in SITE.rglob('*.html'))} html pages into site/ with base {BASE}")
