# YouTubeLiveScheduler
YouTubeの配信予定を自動的にGoogleカレンダーに同期するツール。

## 概要
YouTubeのライブ配信予定を自動的にGoogleカレンダーに登録するツールです。  
特定のYouTubeチャンネルを監視し、配信予定がある場合はGoogleカレンダーにイベントを追加します。  


## ▶️ 実行方法
### ローカル実行
```bash
python main.py
```
### GitHub Actions（自動実行）

- 自動実行: 毎日午前9時（JST）
- 手動実行: リポジトリの「Actions」タブから「Run workflow」

#### 実行頻度の変更
```
.github/workflows/sync-youtube-calendar.yml の cron を編集：
'0 */6 * * *' : 6時間ごと
'0 8,20 * * *' : 毎日8時と20時
'*/30 * * * *' : 30分ごと
```