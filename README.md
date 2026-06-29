# schedule-APP

乃木坂46・櫻坂46・=LOVE の「本日のスケジュール」を毎朝6:00(JST)にスマホへプッシュ通知するアプリです。
GitHub Actionsの定期実行（cron）と [ntfy.sh](https://ntfy.sh/) を使うので、PCの電源に関係なく送信されます。

## 仕組み

- `scripts/scrape_schedule.py` が各グループの公式サイトから今日の予定を取得します
- `scripts/send_schedule_notify.py` がそれをntfy.sh経由でプッシュ通知として送信します
- `.github/workflows/daily-schedule.yml` がGitHub Actions上で毎日21:00 UTC(=朝6:00 JST)に上記スクリプトを実行します

## セットアップ手順

### 1. スマホにntfyアプリを入れる

- iOS: App Storeで「ntfy」を検索してインストール
- Android: Google Playで「ntfy」を検索してインストール

### 2. 自分専用のトピック名を決める

ntfyは「トピック名」というキーワードを購読することで通知を受け取ります。誰にも知られていない、推測されにくい文字列を決めてください（例: `nogi-sakura-equal-love-a8f3k2`）。

アプリを開いて「Subscribe to topic」からそのトピック名を入力して購読してください。

### 3. GitHubリポジトリにSecretを登録する

リポジトリの `Settings > Secrets and variables > Actions > New repository secret` から以下を登録します。

| Secret名 | 値 |
|---|---|
| `NTFY_TOPIC` | 決めたトピック名 |

### 4. 動作確認

Secret登録後、GitHubの `Actions` タブ → `Daily Idol Schedule Notify` → `Run workflow` で手動実行できます。
正常に動けばスマホに即座に通知が届きます。

以降は毎日朝6:00(JST)に自動実行されます。
