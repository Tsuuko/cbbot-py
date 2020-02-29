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
