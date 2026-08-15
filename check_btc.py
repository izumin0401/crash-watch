#!/usr/bin/env python3
"""Daily BTC crash check.

Fetches BTC-USD from Yahoo Finance's chart API and logs a row to
history.csv, exiting non-zero if the drop from the previous close looks
like a crash. Yahoo Finance covers stocks/indices/forex/crypto under the
same domain and JSON shape, so this same approach extends to other
asset classes later without needing a new API/domain.
"""
import csv
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

SYMBOL = "BTC-USD"
THRESHOLD_PCT = -10.0  # change from previous close <= this value is treated as a crash
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.csv")


def fetch_quote(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as res:
        data = json.loads(res.read().decode())
    meta = data["chart"]["result"][0]["meta"]
    return meta["regularMarketPrice"], meta["previousClose"]


def main():
    price, prev_close = fetch_quote(SYMBOL)
    change_pct = (price - prev_close) / prev_close * 100
    is_crash = change_pct <= THRESHOLD_PCT
    now = datetime.now(timezone.utc).isoformat()

    is_new = not os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp_utc", "symbol", "price", "change_pct_24h", "alert"])
        writer.writerow([now, SYMBOL, price, round(change_pct, 3), is_crash])

    status = "CRASH DETECTED" if is_crash else "normal"
    print(f"[{now}] {SYMBOL} price={price} change={change_pct:.3f}% status={status}")

    if is_crash:
        sys.exit(1)


if __name__ == "__main__":
    main()
