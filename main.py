import os
import json
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests

class YouTubeCalendarSync:
    def __init__(self):
        # 環境変数から認証情報を取得
        self.youtube_api_key = os.environ.get('YOUTUBE_API_KEY')
        self.service_account_info = json.loads(os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON'))
        self.calendar_id = os.environ.get('GOOGLE_CALENDAR_ID')
        
        # YouTube Data API クライアント
        self.youtube = build('youtube', 'v3', developerKey=self.youtube_api_key)
        
        # Google Calendar API クライアント
        credentials = service_account.Credentials.from_service_account_info(
            self.service_account_info,
            scopes=['https://www.googleapis.com/auth/calendar']
        )
        self.calendar = build('calendar', 'v3', credentials=credentials)
    
    def get_channel_upcoming_streams(self, channel_id):
        """指定されたチャンネルの配信予定を取得"""
        try:
            # チャンネルの配信予定を検索
            request = self.youtube.search().list(
                part='snippet',
                channelId=channel_id,
                eventType='upcoming',
                type='video',
                order='date',
                maxResults=10
            )
            response = request.execute()
            
            streams = []
            for item in response['items']:
                video_id = item['id']['videoId']
                
                # 詳細情報を取得（配信開始時刻など）
                video_request = self.youtube.videos().list(
                    part='snippet,liveStreamingDetails',
                    id=video_id
                )
                video_response = video_request.execute()
                
                if video_response['items']:
                    video_data = video_response['items'][0]
                    live_details = video_data.get('liveStreamingDetails', {})
                    
                    if 'scheduledStartTime' in live_details:
                        stream_info = {
                            'title': video_data['snippet']['title'],
                            'description': video_data['snippet']['description'],
                            'scheduled_start_time': live_details['scheduledStartTime'],
                            'video_id': video_id,
                            'url': f'https://www.youtube.com/watch?v={video_id}',
                            'channel_title': video_data['snippet']['channelTitle']
                        }
                        streams.append(stream_info)
            
            return streams
        
        except Exception as e:
            print(f"YouTube API エラー: {e}")
            return []
    
    def create_calendar_event(self, stream_info):
        """Googleカレンダーにイベントを作成"""
        try:
            # ISO 8601形式の時刻をパース
            start_time = datetime.fromisoformat(stream_info['scheduled_start_time'].replace('Z', '+00:00'))
            end_time = start_time + timedelta(hours=2)  # デフォルト2時間
            
            event = {
                'summary': f"📺 {stream_info['title']}",
                'description': f"{stream_info['description'][:500]}\n\n配信URL: {stream_info['url']}\nチャンネル: {stream_info['channel_title']}",
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Asia/Tokyo',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Asia/Tokyo',
                },
                'source': {
                    'title': 'YouTube Live',
                    'url': stream_info['url']
                }
            }
            
            # イベント作成
            created_event = self.calendar.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()
            
            print(f"イベント作成完了: {stream_info['title']}")
            return created_event
        
        except Exception as e:
            print(f"カレンダーイベント作成エラー: {e}")
            return None
    
    def check_existing_event(self, stream_info):
        """既存のイベントをチェック（重複防止）"""
        try:
            # 配信予定時刻の前後1日で検索
            start_time = datetime.fromisoformat(stream_info['scheduled_start_time'].replace('Z', '+00:00'))
            time_min = (start_time - timedelta(days=1)).isoformat()
            time_max = (start_time + timedelta(days=1)).isoformat()
            
            events_result = self.calendar.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                q=stream_info['title'][:50],  # タイトルの一部で検索
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # URLが含まれているイベントがあるかチェック
            for event in events:
                description = event.get('description', '')
                if stream_info['url'] in description:
                    return event
            
            return None
        
        except Exception as e:
            print(f"既存イベントチェックエラー: {e}")
            return None
    
    def sync_channel(self, channel_id):
        """指定されたチャンネルの配信予定を同期"""
        print(f"チャンネル {channel_id} の配信予定を取得中...")
        
        streams = self.get_channel_upcoming_streams(channel_id)
        print(f"配信予定 {len(streams)} 件を取得")
        
        for stream in streams:
            print(f"\n処理中: {stream['title']}")
            
            # 既存イベントをチェック
            existing_event = self.check_existing_event(stream)
            
            if existing_event:
                print(f"  → 既存のイベントが見つかりました: {existing_event['summary']}")
            else:
                # 新しいイベントを作成
                created_event = self.create_calendar_event(stream)
                if created_event:
                    print(f"  → 新しいイベントを作成しました")
    
    def sync_multiple_channels(self, channel_ids):
        """複数のチャンネルを同期"""
        for channel_id in channel_ids:
            try:
                self.sync_channel(channel_id)
            except Exception as e:
                print(f"チャンネル {channel_id} の同期でエラー: {e}")

def main():
    channel_ids = [
        # ここに監視したいチャンネルのIDを追加
        'UCygtb6wTyiSxXYHPAHs3UKA', # 日向海フェニカ
        'UC6bD0BolIyRtVCXL0SKn8Yw', # 天晴ほかる
        'UCkd3H8yZEXxZSGSOmxeHxrg', # 歩音ティナ
        'UC8xsCroRQKmQt0rXKuYQQyw', # 栃宮るりは
        'UCJSglVBagnVoCD82MsBlmDA', # 山奈しずく
        'UCSWkUurjlKM39CnS1hnfE_Q', # 木乃華サクヤ
        'UCgtiP3tTIO7-Yn0y_W1s4Cw', # ユニバースプロダクション
    ]
    
    # 環境変数チェック
    required_env_vars = ['YOUTUBE_API_KEY', 'GOOGLE_SERVICE_ACCOUNT_JSON', 'GOOGLE_CALENDAR_ID']
    missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"必要な環境変数が設定されていません: {', '.join(missing_vars)}")
        return
    
    if not channel_ids:
        print("監視するチャンネルIDを設定してください")
        return
    
    # 同期実行
    sync = YouTubeCalendarSync()
    sync.sync_multiple_channels(channel_ids)
    print("\n同期処理完了")

if __name__ == '__main__':
    main()