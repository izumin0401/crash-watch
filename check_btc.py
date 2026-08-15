#!/usr/bin/env python3
"""Daily BTC crash check. Fetches 24h stats from Binance and logs to history.csv."""
import csv
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

SYMBOL = "BTCUSDT"
THRESHOLD_PCT = -10.0  # 24h change <= this value is treated as a crash
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.csv")


def fetch_ticker(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    req = urllib.request.Request(url, headers={"User-Agent": "crash-watch-bot"})
    with urllib.request.urlopen(req, timeout=10) as res:
        return json.loads(res.read().decode())


def main():
    data = fetch_ticker(SYMBOL)
    price = float(data["lastPrice"])
    change_pct = float(data["priceChangePercent"])
    is_crash = change_pct <= THRESHOLD_PCT
    now = datetime.now(timezone.utc).isoformat()

    is_new = not os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp_utc", "symbol", "price", "change_pct_24h", "alert"])
        writer.writerow([now, SYMBOL, price, change_pct, is_crash])

    status = "CRASH DETECTED" if is_crash else "normal"
    print(f"[{now}] {SYMBOL} price={price} change_24h={change_pct}% status={status}")

    if is_crash:
        sys.exit(1)


if __name__ == "__main__":
    main()
