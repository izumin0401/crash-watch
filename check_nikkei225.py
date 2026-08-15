#!/usr/bin/env python3
"""Daily Nikkei 225 crash check.

Market-wide signal, as opposed to screen_jp_stocks.py which looks at
individual companies. A single stock dropping double digits on bad
earnings happens on the Tokyo exchange most trading days and isn't
newsworthy; the whole index dropping several percent in a day is rare
and is what actually indicates a market-wide shock.

Takes the current value and change-from-previous-close percentage
(fetched by the caller, e.g. via WebSearch — this sandbox's outbound
network is locked to a small allowlist and can't reach finance APIs
directly) and exits non-zero if it looks like a crash.
"""
import argparse
import sys
from datetime import datetime, timezone

INDEX = "Nikkei225"
THRESHOLD_PCT = -3.0  # change from previous close <= this value is treated as a crash


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--value", type=float, required=True, help="Current Nikkei 225 value")
    parser.add_argument("--change-pct", type=float, required=True, help="Change from previous close, percent, e.g. -4.2")
    args = parser.parse_args()

    is_crash = args.change_pct <= THRESHOLD_PCT
    now = datetime.now(timezone.utc).isoformat()

    status = "CRASH DETECTED" if is_crash else "normal"
    print(f"[{now}] {INDEX} value={args.value} change={args.change_pct}% status={status}")

    if is_crash:
        sys.exit(1)


if __name__ == "__main__":
    main()
