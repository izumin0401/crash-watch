# crash-watch

BTC(BTC-USD)の暴落検知bot。毎日1回、現在価格と前日終値比の騰落率を取得し、
下落率が -10% 以下なら「暴落」と判定してログに記録する。

## 仕組み

- クラウドの実行環境はBashからの外部API直接呼び出し(egress)が制限されており、
  かつユーザー側で許可ドメインを追加する設定もないため、価格取得は
  `WebSearch` ツール(検索エンジン経由)で行う
- `check_btc.py` は取得済みの `--price` / `--change-pct` を受け取り、`history.csv` に1行追記するだけ
- 暴落判定時はスクリプトが非ゼロ終了する(exit code 1)

## 実行方法

```bash
python3 check_btc.py --price 62977.49 --change-pct -0.5
```

依存ライブラリなし(標準ライブラリのみ)。Python 3.7+ で動作。

## 自動実行

Claude Codeの Scheduled Cloud Agent (routine) から毎日実行され、
WebSearchでBTC-USDの価格・騰落率を取得 → `check_btc.py` 実行 →
`history.csv` の更新を自動でこのリポジトリにcommit・pushする。

## しきい値

- 監視対象: BTC-USD
- 暴落しきい値: 前日終値比 -10% 以下
- `check_btc.py` 内の `THRESHOLD_PCT` を変更すれば調整可能

## 既知の制約

- WebSearchのスニペットから数値を読み取る方式のため、直接APIを叩くより精度・安定性は落ちる
