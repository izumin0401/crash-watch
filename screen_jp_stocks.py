#!/usr/bin/env python3
"""Daily Japanese individual stock crash screen.

Unlike check_btc.py (which tracks one fixed symbol), this is a screener:
the caller (e.g. via WebSearch against "本日 値下がり率ランキング" /
"日本株 急落" style queries) finds whatever stocks are crashing *today*,
without any pre-defined watchlist, and passes them in as JSON. This
script just validates, thresholds, and logs them.

Pass hits as a JSON array via --hits, e.g.:

  python3 screen_jp_stocks.py --hits '[
    {"name": "○○ホールディングス", "code": "1234", "price": 980, "change_pct": -18.2, "reason": "下方修正"}
  ]'

Pass an empty array `--hits '[]'` when the screen found nothing.
Exits non-zero if any hit's change_pct is at or below THRESHOLD_PCT.
"""
import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone

THRESHOLD_PCT = -10.0  # day's change <= this value is treated as a crash
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jp_stocks_history.csv")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--hits", required=True, help="JSON array of {name, code, price, change_pct, reason}")
    args = parser.parse_args()

    try:
        hits = json.loads(args.hits)
    except json.JSONDecodeError as e:
        print(f"error: --hits is not valid JSON: {e}", file=sys.stderr)
        sys.exit(2)

    now = datetime.now(timezone.utc).isoformat()
    is_new = not os.path.exists(LOG_PATH)
    crashed = []

    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp_utc", "name", "code", "price", "change_pct", "alert", "reason"])

        if not hits:
            writer.writerow([now, "(no crash found)", "", "", "", False, ""])
        else:
            for hit in hits:
                change_pct = float(hit["change_pct"])
                is_crash = change_pct <= THRESHOLD_PCT
                writer.writerow([
                    now,
                    hit.get("name", ""),
                    hit.get("code", ""),
                    hit.get("price", ""),
                    change_pct,
                    is_crash,
                    hit.get("reason", ""),
                ])
                if is_crash:
                    crashed.append(hit)

    if not hits:
        print(f"[{now}] JP stock screen: no candidates found, status=normal")
    else:
        for hit in hits:
            status = "CRASH DETECTED" if float(hit["change_pct"]) <= THRESHOLD_PCT else "normal"
            print(f"[{now}] {hit.get('name','?')}({hit.get('code','?')}) change={hit['change_pct']}% status={status}")

    if crashed:
        sys.exit(1)


if __name__ == "__main__":
    main()
