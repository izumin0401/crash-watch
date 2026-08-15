# crash-watch

BTC(BTC/USDT)の暴落検知bot。毎日1回、Binanceの24時間統計を取得し、
24時間の下落率が -10% 以下なら「暴落」と判定してログに記録する。

## 仕組み

- `check_btc.py` が Binance Public API (`/api/v3/ticker/24hr`) を叩き、価格と24h騰落率を取得
- 結果を `history.csv` に追記
- 暴落判定時はスクリプトが非ゼロ終了する(exit code 1)

## 実行方法

```bash
python3 check_btc.py
```

依存ライブラリなし(標準ライブラリのみ)。Python 3.7+ で動作。

## 自動実行

Claude Codeの Scheduled Cloud Agent (routine) から毎日実行され、
`history.csv` の更新が自動でこのリポジトリにcommit・pushされる。

## しきい値

- 監視対象: BTC/USDT
- 暴落しきい値: 24時間で -10% 以下
- `check_btc.py` 内の `THRESHOLD_PCT` / `SYMBOL` を変更すれば調整可能
