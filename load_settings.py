#####
# 環境変数から設定を読み込む
#####

import os

# ローカルデバッグ用
# heroku以外で実行する場合は.envファイルから環境変数を読み取る
if os.environ.get("DYNO") is None:
    from dotenv import load_dotenv
    from os.path import join, dirname
    #load_dotenv(verbose=True,encoding="utf8")
    dotenv_path = join(dirname(__file__), '.env.development')
    load_dotenv(dotenv_path, encoding="utf8")

# DiscordBOTのトークン読み取り
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

# cloudcubeの接続情報読み取り
CLOUDCUBE_ACCESS_KEY_ID = os.environ.get("CLOUDCUBE_ACCESS_KEY_ID")
CLOUDCUBE_SECRET_ACCESS_KEY = os.environ.get("CLOUDCUBE_SECRET_ACCESS_KEY")
CLOUDCUBE_URL = os.environ.get("CLOUDCUBE_URL")

# mongoDBの接続情報読み取り
MONGODB_URI = os.environ.get("MONGODB_URI")

# チャンネル設定読み取り
MEMBER_NOTIFICATION_CHANNEL_ID=int(os.environ.get("MEMBER_NOTIFICATION_CHANNEL_ID"))


# google sheets apiのoauth認証情報読み取り
# https://qiita.com/a-r-i/items/bb8b8317840e3a87771a
SHEETS_CREDENTIAL = {
                "type": "service_account",
                "project_id": os.environ['SHEET_PROJECT_ID'],
                "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
                "private_key": os.environ['SHEET_PRIVATE_KEY'],
                "client_email": os.environ['SHEET_CLIENT_EMAIL'],
                "client_id": os.environ['SHEET_CLIENT_ID'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url":  os.environ['SHEET_CLIENT_X509_CERT_URL']
}
SPREADSHEET_URL=os.environ.get("SPREADSHEET_URL")
