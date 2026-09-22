---
name: creator-examples
description: Look up Riley Brown's Creator Examples database, a plain-text website of creator content examples (currently YouTube video intros from Theo t3.gg and Riley Brown). Use whenever Riley or an agent needs reference intros, hooks, or outlier-video examples to study, imitate, compare against, or cite; when asked "what does a good intro look like", "show me Theo's intros", "pull my best intros"; or when adding new creators or examples to the database.
---

# Creator Examples

A static, unstyled website that acts as a database of creator content examples. Owned by Riley Brown. Every page is plain HTML with links, so any agent can read it with a simple fetch. Machine-readable JSON sits next to the pages.

## Where it lives

- Site: https://creator-examples.vercel.app
- Index for agents: https://creator-examples.vercel.app/llms.txt (lists every page and data file)
- Data index: https://creator-examples.vercel.app/data/index.json
- Repo: https://github.com/rbrown101010/creator-examples
- Hosting: Vercel, project creator-examples. Pushes to main redeploy.

## Structure

- / : Creator Examples home. Links to content types.
- /intros/ : Intros. Links to one page per creator.
- /intros/theo/ : Theo (t3.gg) top 10 outlier videos of the past year, each intro cut at the sponsor handoff.
- /intros/riley-brown/ : Riley Brown top 10 videos by views, each intro cut at the transition into the body, plus a bullet outline of the rest of the video.
- /intros/<creator>/<NN-slug>/ : one page per example with title, source video link, views, duration, where the intro ends, and the intro text.
- /data/<creator>.json : the same data as JSON. Each intro has title, url, views, duration, intro text, and its page URL.

## How to read it

1. Fetch https://creator-examples.vercel.app/llms.txt to see everything available.
2. For analysis across many examples, fetch https://creator-examples.vercel.app/data/<creator>.json instead of crawling pages.
3. Cite the source video URL when quoting an intro. The intros are short excerpts of other creators' videos gathered for study; link back to the original.

## How to add examples

The repo is the source of truth. Data lives in data/<creator>.json; build.py turns it into site/.

1. Clone https://github.com/rbrown101010/creator-examples
2. Add or edit data/<creator>.json. Required fields per intro: rank, title, video_id, url, channel, views (int), published, duration, intro. Optional: outlier_multiplier, intro_ends_at, intro_ends_reason, rest_of_video (list of strings).
3. New creator: add a tuple to CREATORS in build.py (slug, display name, data file).
4. Run `python3 build.py`, commit both data/ and site/, push to main. Vercel redeploys.

## Conventions

- Intro = the spoken opening up to the first clear transition (sponsor handoff, "let's dive in", first demo).
- Keep pages unstyled. No CSS, no JavaScript.
- Keep the plain-text feel: headings, paragraphs, lists, links only.
