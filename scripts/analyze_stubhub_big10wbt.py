#!/usr/bin/env python3
"""Parse StubHub Session 3 event page and append one history row per run."""

import argparse
import csv
import json
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Snapshot date in YYYYMMDD")
    parser.add_argument(
        "--timestamp",
        required=True,
        help="Run timestamp (example: 2026-02-22 20:30:00 EST)",
    )
    parser.add_argument("--stubhub-html", required=True, type=Path)
    parser.add_argument("--history-csv", required=True, type=Path)
    return parser.parse_args()

def extract_json_script_blocks(html: str) -> list[dict]:
    blocks: list[dict] = []
    pattern = re.compile(
        r"<script[^>]*>\s*(.*?)\s*</script>",
        flags=re.DOTALL,
    )
    for match in pattern.finditer(html):
        raw = match.group(1).strip()
        try:
            blocks.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return blocks


def pick_event_payload(blocks: list[dict]) -> dict:
    for block in blocks:
        if isinstance(block, dict) and block.get("appName") == "viagogo-event":
            return block
    return {}


def weighted_median_from_histogram(histogram: dict) -> float | None:
    buckets = histogram.get("buckets", [])
    total = sum(int(bucket.get("frequency", 0)) for bucket in buckets)
    if total <= 0:
        return None

    target = (total + 1) / 2
    cumulative = 0
    for bucket in buckets:
        frequency = int(bucket.get("frequency", 0))
        if frequency <= 0:
            continue
        cumulative += frequency
        if cumulative >= target:
            start = float(bucket.get("startPrice", 0))
            end = float(bucket.get("endPrice", start))
            return (start + end) / 2
    return None


def parse_event_payload(payload: dict, snapshot_date: str, snapshot_timestamp: str) -> dict:
    grid = payload.get("grid", {})
    low = grid.get("minPrice")
    high = grid.get("maxPrice")
    histogram = payload.get("histogram", {})
    median = weighted_median_from_histogram(histogram)

    # Currency is not always a top-level field, so fall back to first listing.
    grid_items = grid.get("items", [])
    if grid_items:
        currency = grid_items[0].get("buyerCurrencyCode", "USD")
    else:
        currency = "USD"

    return {
        "snapshot date": snapshot_date,
        "snapshot timestamp": snapshot_timestamp,
        "event id": str(payload.get("eventId", "")),
        "event name": payload.get("eventName", ""),
        "event datetime": payload.get("formattedLocalEventDateTime", ""),
        "venue": payload.get("venueName", ""),
        "listings counted": str(payload.get("totalListings", payload.get("totalFilteredListings", ""))),
        "low price": f"{float(low):.2f}" if low is not None else "",
        "median price": f"{median:.2f}" if median is not None else "",
        "high price": f"{float(high):.2f}" if high is not None else "",
        "currency": currency,
        "stubhub url": payload.get("eventUrl", ""),
        "median method": "histogram-weighted-midpoint",
    }


def append_history_csv(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "snapshot date",
        "snapshot timestamp",
        "event id",
        "event name",
        "event datetime",
        "venue",
        "listings counted",
        "low price",
        "median price",
        "high price",
        "currency",
        "stubhub url",
        "median method",
    ]
    file_exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    args = parse_args()
    html = args.stubhub_html.read_text(encoding="utf-8")
    blocks = extract_json_script_blocks(html)
    payload = pick_event_payload(blocks)
    if not payload:
        raise SystemExit("Could not find viagogo-event payload in StubHub HTML.")
    row = parse_event_payload(payload, args.date, args.timestamp)
    append_history_csv(args.history_csv, row)


if __name__ == "__main__":
    main()
