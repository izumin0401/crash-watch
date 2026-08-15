# crash-watch

BTC(BTC-USD)の暴落検知bot。毎日1回、Yahoo Financeの現在値・前日終値を取得し、
前日終値からの下落率が -10% 以下なら「暴落」と判定してログに記録する。

## 仕組み

- `check_btc.py` が Yahoo Finance の chart API (`query1.finance.yahoo.com/v8/finance/chart/{symbol}`) を叩き、価格と前日終値比の騰落率を取得
- 結果を `history.csv` に追記
- 暴落判定時はスクリプトが非ゼロ終了する(exit code 1)
- このAPIは株・指数・為替・仮想通貨を同じドメイン・同じJSON構造で扱えるため、将来他の銘柄を追加してもドメイン許可の追加申請が不要

## 実行方法

```bash
python3 check_btc.py
```

依存ライブラリなし(標準ライブラリのみ)。Python 3.7+ で動作。

## 自動実行

Claude Codeの Scheduled Cloud Agent (routine) から毎日実行され、
`history.csv` の更新が自動でこのリポジトリにcommit・pushされる。
クラウド環境側で `query1.finance.yahoo.com` へのegressを許可しておく必要がある。

## しきい値

- 監視対象: BTC-USD
- 暴落しきい値: 前日終値比 -10% 以下
- `check_btc.py` 内の `THRESHOLD_PCT` / `SYMBOL` を変更すれば調整可能
