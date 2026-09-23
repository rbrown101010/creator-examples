# Creator Examples

A plain-text website that acts as a database of creator content examples. No CSS, no JavaScript, just HTML pages with links, so people and AI agents can read it the same way.

Live site: see `config.json` (`base_url`). Agent entry point: `/llms.txt`. Data: `/data/index.json`.

## Layout

- `data/<creator>.json` : source of truth for each creator's examples
- `build.py` : turns `data/` into `site/` (run `python3 build.py`)
- `site/` : generated static site, committed so it can be browsed on GitHub and served by Vercel as-is
- `skill/SKILL.md` : the agent skill that explains how to read and extend this database (also mirrored as a hosted skill on Composio)
- `source/` : raw inputs (OutlierKit transcripts, ranked channel listing, intro outlines)

## Adding examples

1. Edit or add `data/<creator>.json`. Required per intro: `rank`, `title`, `video_id`, `url`, `channel`, `views`, `published`, `duration`, `intro`.
2. New creator: add `(slug, name, data file)` to `CREATORS` in `build.py`.
3. `python3 build.py`, commit `data/` and `site/`, push to `main`. Vercel redeploys.

## Sections

- `/intros/theo/` : Theo (t3.gg) top 10 outlier videos, past 12 months, intros cut at the sponsor handoff
- `/intros/riley-brown/` : Riley Brown top 10 by views, intros cut at the transition into the body
- `/intros/greg-isenberg/` : Greg Isenberg top 10 outliers, intros run through the cold open and guest setup to the handoff line
- `/intros/alex-hormozi/` : Alex Hormozi top 10 outliers, intros cut where the first point or breakdown starts
- `/intros/kallaway/` : Kallaway top 10 outliers, intros cut at the credibility line before section one
- `/short-form/` : full transcripts of the 10 most-viewed Instagram reels for Kallaway (sponsored posts left out), Dylan Page, Roberto Nickson (RPN), Cleo Abram and Nick Saraev. Data in `data/short-form/<creator>.json`, listed in `SHORT_FORM` in `build.py`.

Ranking for the outlier sets: views divided by the channel's median views over its past-year long-form uploads. Video lists via yt-dlp, transcripts via YouTube captions (Theo's via OutlierKit).
