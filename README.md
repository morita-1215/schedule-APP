# schedule-APP

乃木坂46・櫻坂46・=LOVE の「本日のスケジュール」を毎朝6:00(JST)にメールで送るアプリです。
GitHub Actionsの定期実行（cron）を使うので、PCの電源に関係なく送信されます。

## 仕組み

- `scripts/scrape_schedule.py` が各グループの公式サイトから今日の予定を取得します
- `scripts/send_schedule_mail.py` がそれをメール本文にしてSMTP経由で送信します
- `.github/workflows/daily-schedule.yml` がGitHub Actions上で毎日21:00 UTC(=朝6:00 JST)に上記スクリプトを実行します

## セットアップ手順

### 1. このリポジトリにpushする

ローカルで作成済みのコードをこのリポジトリにpushしてください（pushはこちらで実行可能です。お知らせください）。

### 2. au.comメールのSMTP設定値を確認する

以下のauサポートページにログインして、自分のメールアドレス用のSMTP設定（サーバー名・ポート番号）を確認してください。
https://www.au.com/support/service/internet/guide/mail/mail-server/

一般的には下記のいずれかになります（要・本人確認）。
- ポート587（SSTARTTLS）または465（SSL）
- SMTP認証ID・パスワードが必要

### 3. GitHubリポジトリにSecretsを登録する

リポジトリの `Settings > Secrets and variables > Actions > New repository secret` から以下を登録します。

| Secret名 | 値 |
|---|---|
| `SMTP_HOST` | au.comサポートページで確認したSMTPサーバー名 |
| `SMTP_PORT` | `587` または `465`（確認した値） |
| `SMTP_USER` | SMTP認証ID（多くの場合メールアドレス） |
| `SMTP_PASS` | メールのパスワード（認証パスワード） |
| `MAIL_FROM` | 送信元アドレス（`shushu34@au.com`） |
| `MAIL_TO` | 送信先アドレス（`shushu34@au.com`） |

### 4. 動作確認

Secrets登録後、GitHubの `Actions` タブ → `Daily Idol Schedule Mail` → `Run workflow` で手動実行できます。
正常に動けば即座にメールが届きます。届かない場合はActionsのログでエラーを確認してください（SMTP認証エラーが最も多いです）。

以降は毎日朝6:00(JST)に自動実行されます。
