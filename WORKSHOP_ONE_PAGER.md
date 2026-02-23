# NICAR 2026 GitHub Actions: One-Page Handout

This workshop shows how to automate routine data updates with GitHub Actions, then keep a history in your repo.

## 1) Standard Cron Workflow Pattern (YAML -> Bash -> Python -> Commit)

Use this mental model for most newsroom automation:

1. **YAML trigger** starts the workflow on a schedule (`cron`) or manually (`workflow_dispatch`).
2. **Bash step** downloads raw data (`curl`) and writes it to `data/raw/`.
3. **Python step** parses/cleans raw data and appends rows to a CSV in `data/`.
4. **Commit step** uses bot identity + `git add` + `git commit` + `git push` so the repo stores the new snapshot.

## 2) Run `workflow_dispatch` + Check Logs (Step by Step)

1. Open your repo on GitHub.com.
2. Click the **Actions** tab.
3. Select a workflow in the left panel.
4. Click **Run workflow** (top right), choose branch (`main`), click **Run workflow** again.
5. Open the new run at the top of the list.
6. Click the job name.
7. Open each step and read logs in order:
   - checkout/setup
   - fetch raw data
   - parse/build CSV
   - commit/push
8. Confirm output files changed in the repo (for example, in `data/` or another output folder you track).

Quick triage:
- `exit code 3` from `curl`: malformed URL or bad secret formatting.
- `401/403`: bad API key or permissions.
- `ModuleNotFoundError`: missing dependency/import issue.
- `git push` rejected: branch protection, token permissions, or secret scanning block.

## 3) What To Watch For (Quotas and Limits)

Track two buckets:

1. **GitHub Actions usage**
   - Runner minutes (private repos), artifact storage, and cache storage.
   - Check: **Repo/Org Settings -> Billing and plans -> Usage**.
   - Your every-2-hour job is usually fine on standard Ubuntu runners, but monitor if jobs get longer.

2. **Data/API provider quotas**
   - API credits/requests (often the first limit you hit).
   - Monitor your provider's usage dashboard and minimize unnecessary request volume.

Good safeguards:
- Keep workflows short.
- Use only needed markets/fields.
- Set schedules intentionally (avoid unnecessary frequency).
- Add clear failure messages when secrets are missing.

## 4) Newsroom Tasks That Fit GitHub Actions

- Daily/Hourly public data pulls (crime, housing, permits, elections, weather, sports).
- Appending trend snapshots to a CSV over time.
- Monitoring a fixed event/listing and tracking price or count changes.
- Running QA checks on incoming data (schema, null checks, row-count checks).
- Refreshing publish-ready outputs before newsroom meetings.
- Triggering alerts or follow-up jobs when thresholds are crossed.

Use Actions when the work is repetitive, timestamped, and benefits from a visible audit trail in Git.
