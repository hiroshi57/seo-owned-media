"""
Google Sheets 更新スクリプト
Phase 1完了: KW戦略タブ・記事作成ログタブを更新する
初回実行時はブラウザでGoogle認証が必要
"""
import os
import json
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# スコープ
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# .envから読み込み
from dotenv import load_dotenv
load_dotenv()
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

def get_credentials():
    creds = None
    token_path = 'sheets-token.json'
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return creds

def update_sheets():
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    today = datetime.now().strftime('%Y-%m-%d')

    # KW戦略タブ更新
    kw_values = [[
        today,
        'ChatGPT 業務効率化 具体例',
        '200〜500',
        '15〜25',
        'Commercial',
        '中小企業経営者向け・具体的使い方訴求',
        '未着手'
    ]]
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='KW戦略!A1',
        valueInputOption='RAW',
        body={'values': kw_values}
    ).execute()
    print('[OK] KW戦略タブ 更新完了')

    # 記事作成ログタブ更新
    log_values = [[
        '1',
        today,
        'ChatGPT 業務効率化 具体例',
        '',
        '',
        'KW選定完了',
        '',
        '',
        ''
    ]]
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='記事作成ログ!A1',
        valueInputOption='RAW',
        body={'values': log_values}
    ).execute()
    print('[OK] 記事作成ログタブ 更新完了')
    print('\nPhase 1 完了！スプレッドシートを確認してください。')

if __name__ == '__main__':
    update_sheets()
