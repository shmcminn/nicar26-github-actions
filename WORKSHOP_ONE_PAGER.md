# NICAR 2026 GitHub Actions: One-Page Handout

This workshop shows how to automate routine data updates with GitHub Actions, then keep a history in your repo.

## 1) Standard Cron Workflow Pattern (YAML -> Actions -> Bash -> Commit)

Use this mental model for most newsroom automation:

1. **YAML trigger** starts the workflow on a schedule (`cron`) or manually (`workflow_dispatch`).
1. **Actions** set up the repository and dependencies (such as Python)
1. **Bash step** where you do the meat of your work, possibly including running a **Python** file.
1. **Commit step** uses bot identity + `git add` + `git commit` + `git push` so the repo stores the new snapshot.

## 2) Run `workflow_dispatch` + Check Logs (Step by Step)

1. Open your repo on GitHub.com.
2. Click the **Actions** tab.
3. Select a workflow in the left panel.
4. Click **Run workflow** (top right), choose branch (`main`), click **Run workflow** again.
5. Open the new run at the top of the list. (may need to refresh)
6. Click the job name.
7. Open each step and read logs in order:
   - checkout/setup
   - fetch raw data
   - parse/build CSV
   - commit/push
8. Confirm output files changed in the repo (for example, in `data/` or another output folder you track).

## 3) What To Watch For (Quotas and Limits)

Track two buckets:

1. **GitHub Actions usage**
   - Runner minutes (private repos), artifact storage, and cache storage.
   - Check: **Repo/Org Settings -> Billing and plans -> Usage**.
   - [GitHub Pricing](https://github.com/pricing)

2. **Data/API provider quotas**
   - API credits/requests (often the first limit you hit).
   - Monitor your provider's usage dashboard and minimize unnecessary request volume.

Good safeguards:
- Keep workflows short.
- Use only needed API requests/fields.
- Set schedules intentionally (avoid unnecessary frequency).

## 4) Newsroom Tasks That Fit GitHub Actions

- Daily/Hourly public data pulls (crime, housing, permits, elections, weather, sports).
- Monitoring a fixed event/listing and tracking price or count changes. (ticket prices)
- Running QA checks on incoming data, such as schema, null checks, row-count checks. (messy government data)
- Refreshing publish-ready outputs before newsroom meetings. (generating charts)
- Triggering alerts or follow-up jobs when thresholds are crossed. (sending newsroom Slack when new campaign finance filing is published)

Use Actions when the work is repetitive, timestamped, and benefits from a visible audit trail in Git.

# Further resources

* [Go big with GitHub Actions](https://palewi.re/docs/go-big-with-github-actions/)
* [Official GitHub Quickstart for Actions](https://docs.github.com/en/actions/get-started/quickstart)

## Real world examples

- [TeamTrace/butler_p_immigration_shootings](https://github.com/TeamTrace/butler_p_immigration_shootings): This repo is a scheduler wrapper for a Redivis notebook that updates The Trace's immigration shootings workflow. Its `dataset-butler.yml` action runs on `workflow_dispatch` and a cron schedule (`*/13 * * * *`), sets up Python, and runs `app.py`, which calls Redivis notebook `TheTrace.immigration_shootings:k6j5.updater:5n3r` via API using a secret token. It powers this:  https://datahub.thetrace.org/dataset/federal-immigration-agent-shootings/

- [palewire/old-la-photos](https://github.com/palewire/old-la-photos): This repo is a bot that posts a random Los Angeles Public Library photo to Mastodon. The `mastodon.yaml` workflow runs every three hours, sets up Python and pipenv, runs `make toot`, and uses Mastodon secrets to publish the post. After posting, it writes a timestamp and commits updates back to the repo so each run leaves a visible history. It powers this: https://mastodon.palewi.re/@OldLAPhotos

- [chrislkeller/nm-quantified](https://github.com/chrislkeller/nm-quantified): This repo contains many scheduled newsroom data jobs for New Mexico (for example building permits, drought maps, and crop reports). Each workflow checks out the repo, installs Python/pipenv dependencies, runs one or more acquisition scripts, then calls a local composite `commit` action that does `git add`, `git commit`, and `git push` with credentials from repository secrets. 
