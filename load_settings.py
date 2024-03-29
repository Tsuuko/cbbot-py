#####
# 環境変数から設定を読み込む
#####

import os

# DiscordBOTのトークン読み取り
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

# S3の接続情報読み取り
S3_ENDPOINT = os.environ.get("S3_ENDPOINT")
S3_ACCESS_KEY_ID = os.environ.get("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

# mongoDBの接続情報読み取り
MONGODB_URI = os.environ.get("MONGODB_URI")

# チャンネル設定読み取り
MEMBER_NOTIFICATION_CHANNEL_ID = int(os.environ.get("MEMBER_NOTIFICATION_CHANNEL_ID"))

CB_NOTIFICATION_CHANNEL_ID = int(os.environ.get("CB_NOTIFICATION_CHANNEL_ID"))
BOT_COMMAND_CHANNEL = int(os.environ.get("BOT_COMMAND_CHANNEL"))
BOT_MANAGER_ROLE = int(os.environ.get("BOT_MANAGER_ROLE"))

# google sheets apiのoauth認証情報読み取り
# https://qiita.com/a-r-i/items/bb8b8317840e3a87771a
SHEETS_CREDENTIAL = {
    "type": "service_account",
    "project_id": os.environ["SHEET_PROJECT_ID"],
    "private_key_id": os.environ["SHEET_PRIVATE_KEY_ID"],
    "private_key": os.environ["SHEET_PRIVATE_KEY"],
    "client_email": os.environ["SHEET_CLIENT_EMAIL"],
    "client_id": os.environ["SHEET_CLIENT_ID"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ["SHEET_CLIENT_X509_CERT_URL"],
}
SPREADSHEET_URL = os.environ.get("SPREADSHEET_URL")
