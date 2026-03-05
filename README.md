# NICAR 2026: GitHub Actions for Data Automation

### 1) Understand what GitHub Actions are

Use this basic model:

- A workflow file (`.yml`) defines automation.
- Triggers like `schedule` and `workflow_dispatch` decide when it runs.
- Jobs and steps run scripts, API calls, and git commits on a hosted runner.

### 2) Review a real newsroom example (The Trace)

Use this repo as your first concrete example:

- Repo: [TeamTrace/butler_p_immigration_shootings](https://github.com/TeamTrace/butler_p_immigration_shootings)
- Workflow: `/.github/workflows/dataset-butler.yml`

Focus on:

- `workflow_dispatch` for manual runs.
- `schedule` for recurring runs.
- Python step that calls a Redivis notebook updater via API.

### 3) Fork and clone this repo

1. Fork this repository to your own GitHub account.
2. Clone your fork to your own computer.
3. Open your fork on GitHub and confirm the `Actions` tab is available.

### 4) Inspect the first YAML file: ticket prices

Open:

- `.github/workflows/daily-ncaaw-ticket-prices.yml`

Check what this workflow does:

- Pulls StubHub event HTML.
- Runs `scripts/analyze_stubhub_big10wbt.py`.
- Appends a timestamped row to `data/stubhub_big10wbt_session7_history.csv`.
- Commits sanitized classroom-safe HTML to `data/raw_public/`. (removing API keys from the html file)

### 5) Run `workflow_dispatch` for ticket prices

Steps:

1. Go to `Actions`.
2. Select `daily-ncaaw-ticket-prices`.
3. Click `Run workflow`.
4. Open logs and review each step.
5. Confirm output files changed in the repo.

### 6) Inspect the second YAML file: sports odds

Open:

- `.github/workflows/daily-wncaab-odds.yml`

Check what this workflow does:

- Calls The Odds API for WNCAAB moneyline odds.
- Runs `scripts/fetch_wncaab_odds.py`.
- Writes raw JSON snapshots and appends CSV rows.
- Make a change to the frequency of how often it runs.

### 7) Set up API key for sports odds

1. Get a key from [the-odds-api.com](https://the-odds-api.com/).
2. In the forked repo, go to `Settings` -> `Secrets and variables` -> `Actions`.
3. Add a new repository secret named `THE_ODDS_API_KEY`.
4. Paste only the key value.

### 8) Run `workflow_dispatch` for sports odds

1. Go to `Actions`.
2. Select `daily-wncaab-odds`.
3. Click `Run workflow`.
4. Check logs and confirm new files in `data/`.

### 9) Review the one-pager

Use [WORKSHOP_ONE_PAGER.md](./WORKSHOP_ONE_PAGER.md):

- limitations of GitHub Actions
- use cases that fit Actions
- more real-world examples
