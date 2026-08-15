# crash-watch

BTC(BTC-USD)の暴落検知bot。毎日1回、現在価格と前日終値比の騰落率を取得し、
下落率が -10% 以下なら「暴落」と判定して通知する。

## 仕組み

- クラウドの実行環境はBashからの外部API直接呼び出し(egress)が制限されており、
  個人アカウントでは許可ドメインを追加する設定もないため、価格取得は
  `WebSearch` ツール(検索エンジン経由)で行う
- `check_btc.py` は取得済みの `--price` / `--change-pct` を受け取り、暴落判定するだけ
- 暴落判定時はスクリプトが非ゼロ終了する(exit code 1)
- 判定結果はルーティンの実行ログ・通知で確認する(GitHubへの自動commit/pushはしない。
  クラウド実行環境からのgit pushはGitHub連携の書き込み権限の制約で現状動かないため)

## 実行方法

```bash
python3 check_btc.py --price 62977.49 --change-pct -0.5
```

依存ライブラリなし(標準ライブラリのみ)。Python 3.7+ で動作。

## 自動実行

Claude Codeの Scheduled Cloud Agent (routine) から毎日実行され、
WebSearchでBTC-USDの価格・騰落率を取得 → `check_btc.py` 実行 → 結果を報告する。

## しきい値

- 監視対象: BTC-USD
- 暴落しきい値: 前日終値比 -10% 以下
- `check_btc.py` 内の `THRESHOLD_PCT` を変更すれば調整可能

## 既知の制約

- WebSearchのスニペットから数値を読み取る方式のため、直接APIを叩くより精度・安定性は落ちる
- 日々の価格履歴はリポジトリに保存されない(GitHub書き込み権限が使えるようになったら復活予定)
