#!/usr/bin/env python3
"""Read raw WNCAAB odds JSON and append tidy rows to a CSV."""

import argparse
import csv
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Snapshot date in YYYYMMDD (ET)")
    parser.add_argument(
        "--timestamp",
        required=True,
        help="Run timestamp (example: 2026-02-23 04:00:00 EST)",
    )
    parser.add_argument(
        "--input-json",
        required=True,
        type=Path,
        help="Path to raw odds JSON",
    )
    parser.add_argument(
        "--csv",
        required=True,
        type=Path,
        help="Output path for flattened odds CSV",
    )
    return parser.parse_args()


def to_rows(events: list[dict], snapshot_date: str, snapshot_timestamp: str) -> list[dict]:
    rows: list[dict] = []
    for event in events:
        event_id = event.get("id", "")
        sport_key = event.get("sport_key", "")
        sport_title = event.get("sport_title", "")
        commence_time = event.get("commence_time", "")
        home_team = event.get("home_team", "")
        away_team = event.get("away_team", "")

        for bookmaker in event.get("bookmakers", []):
            bookmaker_key = bookmaker.get("key", "")
            bookmaker_title = bookmaker.get("title", "")
            last_update = bookmaker.get("last_update", "")
            for market in bookmaker.get("markets", []):
                if market.get("key") != "h2h":
                    continue
                outcomes = {o.get("name", ""): o.get("price") for o in market.get("outcomes", [])}
                rows.append(
                    {
                        "snapshot_date": snapshot_date,
                        "snapshot_timestamp": snapshot_timestamp,
                        "event_id": event_id,
                        "sport_key": sport_key,
                        "sport_title": sport_title,
                        "commence_time": commence_time,
                        "home_team": home_team,
                        "away_team": away_team,
                        "bookmaker_key": bookmaker_key,
                        "bookmaker_title": bookmaker_title,
                        "bookmaker_last_update": last_update,
                        "market_key": market.get("key", ""),
                        "market_last_update": market.get("last_update", ""),
                        "home_price": outcomes.get(home_team),
                        "away_price": outcomes.get(away_team),
                        "draw_price": outcomes.get("Draw"),
                    }
                )
    return rows


def append_rows_to_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = [
        "snapshot_date",
        "snapshot_timestamp",
        "event_id",
        "sport_key",
        "sport_title",
        "commence_time",
        "home_team",
        "away_team",
        "bookmaker_key",
        "bookmaker_title",
        "bookmaker_last_update",
        "market_key",
        "market_last_update",
        "home_price",
        "away_price",
        "draw_price",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    args = parse_args()
    events = json.loads(args.input_json.read_text(encoding="utf-8"))

    rows = to_rows(events, args.date, args.timestamp)
    append_rows_to_csv(args.csv, rows)


if __name__ == "__main__":
    main()
