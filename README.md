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

### 現在の監視対象
- [日向海フェニカさん（UCygtb6wTyiSxXYHPAHs3UKA）](https://www.youtube.com/@hinamiphoenica)
- [天晴ほかるさん（UC6bD0BolIyRtVCXL0SKn8Yw）](https://www.youtube.com/@amanoharehokaru)
- [歩音ティナさん（UCkd3H8yZEXxZSGSOmxeHxrg）](https://www.youtube.com/@arunetina)
- [栃宮るりはさん（UC8xsCroRQKmQt0rXKuYQQyw）](https://www.youtube.com/@tochimiyaruriha)
- [山奈しずくさん（UCJSglVBagnVoCD82MsBlmDA）](https://www.youtube.com/@yamanashizuku)
- [木乃華サクヤさん（UCSWkUurjlKM39CnS1hnfE_Q）](https://www.youtube.com/@-konohanasakuya-3940)
- [ユニバースプロダクション公式チャンネル（UCgtiP3tTIO7-Yn0y_W1s4Cw）](https://www.youtube.com/@unibirth_production)