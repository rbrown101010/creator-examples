---
name: creator-examples
description: Look up Riley Brown's Creator Examples database, a plain-text website of creator content examples (YouTube video intros from Theo t3.gg, Riley Brown, Greg Isenberg, Alex Hormozi, and Kallaway, plus full short-form scripts from the top Instagram reels of Kallaway, Dylan Page, Roberto Nickson (RPN), Cleo Abram, and Nick Saraev). Use whenever Riley or an agent needs reference intros, hooks, or outlier-video examples to study, imitate, compare against, or cite; when asked "what does a good intro look like", "show me Theo's intros", "pull my best intros", "show me Cleo Abram's short form scripts"; or when adding new creators or examples to the database.
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
- /intros/greg-isenberg/ : Greg Isenberg top 10 outliers, past year. Intro = produced cold open plus the guest setup, ending at "let's get into it" or "Enjoy the episode".
- /intros/alex-hormozi/ : Alex Hormozi top 10 outliers, past year. Intro = hook and promise up to the line that starts the first point or business breakdown.
- /intros/kallaway/ : Kallaway top 10 outliers, past year. Intro = hook, promise, and credibility line up to the sentence that opens section one.
- /short-form/ : Short Form. Full spoken transcripts of each creator's 10 most-viewed Instagram reels (all time, ranked by play count). Creators: kallaway (sponsored posts left out), dylan-page, roberto-nickson, cleo-abram, nick-saraev. Sponsored reels elsewhere are kept and marked.
- /short-form/<creator>/<NN-slug>/ : one page per reel with the spoken hook as title, reel link, views, likes, comments, duration, sponsored flag, the full transcript (one sentence per line) and the original caption.
- /data/short-form/<creator>.json : the same data as JSON.
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
   Short form: add or edit data/short-form/<creator>.json (fields per video: rank, title, shortcode, url, views, published, duration, sponsored, transcript; optional likes, comments, caption) and add a tuple to SHORT_FORM in build.py. Pull reels with ScrapeCreators (SCRAPECREATORS_LIST_INSTAGRAM_USER_POSTS, rank by play_count, is_paid_partnership marks sponsored) and transcripts with SCRAPECREATORS_GET_INSTAGRAM_MEDIA_TRANSCRIPT.
4. Run `python3 build.py`, commit both data/ and site/, push to main. Vercel redeploys.

## Conventions

- Short form = the whole spoken script of the reel, one sentence per line; the title is the spoken hook.
- Intro = the spoken opening up to the first clear transition (sponsor handoff, "let's dive in", first demo).
- Keep pages unstyled. No CSS, no JavaScript.
- Keep the plain-text feel: headings, paragraphs, lists, links only.
