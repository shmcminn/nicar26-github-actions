# NICAR 2026: GitHub Actions for Data Automation

This repository is a teaching scaffold for a 1-hour NICAR session focused on GitHub Actions automation, not scraper-writing.

## Workshop Goal

Automate routine data pulls so updates happen while you sleep, with practical newsroom patterns:

- `schedule` runs on a cron
- `workflow_dispatch` for manual "Run workflow"
- append-only history files for trend tracking

## What Is Included

### 1) Main Class Example: StubHub Session 3 Price Workflow

File:
- `.github/workflows/daily-ncaaw-ticket-prices.yml`

What it does:
- Runs on schedule (Nov-Apr) and manual dispatch
- Downloads raw StubHub Session 3 event HTML from https://www.stubhub.com/big-ten-women-s-basketball-tournament-indianapolis-tickets-3-5-2026/event/157634620/
- Runs a Python script to extract low/median/high from embedded event payload
- Appends one timestamped row to a single history CSV on each run

Script:
- `scripts/analyze_stubhub_big10wbt.py`

Outputs:
- `data/raw_public/stubhub_session3_event_YYYYMMDD.html` (sanitized, student-visible snapshot)
- `data/stubhub_big10wbt_session3_history.csv`

Note:
- The workflow downloads raw HTML during the run into `data/raw/` (ignored), then commits a sanitized copy to `data/raw_public/`.

### 2) API Key Example: WNCAAB Odds Workflow

File:
- `.github/workflows/daily-wncaab-odds.yml`

What it does:
- Runs every 2 hours (Nov-Apr) and manual dispatch
- Calls The Odds API in YAML with `markets=h2h` only
- Writes daily raw JSON snapshot
- Appends timestamped rows into date-partitioned CSV (`data/wncaab_odds_YYYYMMDD.csv`)

Script:
- `scripts/fetch_wncaab_odds.py` (analysis-only; reads raw JSON and appends CSV rows)

Outputs:
- `data/raw/wncaab_odds_YYYYMMDD_HHMMSS.json`
- `data/wncaab_odds_YYYYMMDD.csv`

## GitHub.com Setup (One Time)

1. In your repository, go to `Settings` -> `Actions` -> `General`.
2. Under `Actions permissions`, allow actions to run (either all actions, or at minimum `actions/checkout` and `actions/setup-python`).
3. Under `Workflow permissions`, choose `Read and write permissions`.
4. Save.

## The Odds API Secret Setup (GitHub)

1. Sign up for an API key at [the-odds-api.com](https://the-odds-api.com/).
2. In your GitHub repository, go to `Settings` -> `Secrets and variables` -> `Actions`.
3. Click `New repository secret`.
4. Set `Name` to `THE_ODDS_API_KEY`.
5. Paste only the raw key as the secret value and save.
6. Do not include `THE_ODDS_API_KEY=` in the value field.

Current Odds API request in this repo:
- `sport=basketball_wncaab`
- `regions=us`
- `markets=h2h`
- `oddsFormat=american`
- `dateFormat=iso`

## Repository Layout

- `.github/workflows/` GitHub Actions workflow files
- `scripts/` small utility scripts used by Actions
- `data/raw/` raw API/page snapshots
- `data/raw_public/` sanitized HTML snapshots committed for classroom inspection
- `data/` append-only or day-partitioned CSV outputs

## Teaching Notes

- Keep Python scripts as utilities; teach the workflow YAML and logs.
- Show `workflow_dispatch` first for fast feedback.
- Use append-only rows + timestamps to teach trend tracking.
- Emphasize secret management via GitHub Secrets for key-based APIs.
