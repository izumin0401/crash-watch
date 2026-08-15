#!/usr/bin/env python3
"""Daily BTC crash check.

Takes the current price and change-from-previous-close percentage
(fetched by the caller, e.g. via WebSearch — this sandbox's outbound
network is locked to a small allowlist and can't reach finance APIs
directly) and logs a row to history.csv, exiting non-zero if it looks
like a crash.
"""
import argparse
import csv
import os
import sys
from datetime import datetime, timezone

SYMBOL = "BTC-USD"
THRESHOLD_PCT = -10.0  # change from previous close <= this value is treated as a crash
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.csv")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--price", type=float, required=True, help="Current BTC-USD price")
    parser.add_argument("--change-pct", type=float, required=True, help="Change from previous close, percent, e.g. -12.3")
    args = parser.parse_args()

    is_crash = args.change_pct <= THRESHOLD_PCT
    now = datetime.now(timezone.utc).isoformat()

    is_new = not os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp_utc", "symbol", "price", "change_pct_24h", "alert"])
        writer.writerow([now, SYMBOL, args.price, args.change_pct, is_crash])

    status = "CRASH DETECTED" if is_crash else "normal"
    print(f"[{now}] {SYMBOL} price={args.price} change={args.change_pct}% status={status}")

    if is_crash:
        sys.exit(1)


if __name__ == "__main__":
    main()
