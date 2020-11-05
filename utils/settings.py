# ---------------------------------------------------------------------------- #
#                           環境変数から設定を読み込む                           #
# ---------------------------------------------------------------------------- #

import os
from typing import Final, List, Union

from utils import extension

# ----------------------------- ローカルデバッグ用 ----------------------------- #
# heroku以外で実行する場合は.envファイルから環境変数を読み取る
if os.environ.get("DYNO") is None:
    from os.path import dirname, join

    from dotenv import load_dotenv

    dotenv_path: str = join(dirname(__file__), ".env.dev")
    load_dotenv(dotenv_path, encoding="utf8")
# ----------------------------------------------------------------------------- #


# ----------------------------------- 共通 ------------------------------------ #

# エクステンション <https://discordpy.readthedocs.io/ja/latest/ext/commands/extensions.html>
EXTENSIONS: Final[List[str]] = extension.get_extension_path_list()

# DiscordBOTのトークン
DISCORD_BOT_TOKEN: Final[Union[str, None]] = os.environ.get("DISCORD_BOT_TOKEN")

# 〇〇をプレイ中の文字列
ACTIVITY_NAME: Final[Union[str, None]] = os.getenv("ACTIVITY_NAME")

# メンバーのサーバー入退室通知を送信するチャンネル
MEMBER_NOTIFICATION_CHANNEL_ID: Final[Union[int, None]] = (
    lambda x: int(x) if x.isalnum() else None
)(os.getenv("MEMBER_NOTIFICATION_CHANNEL_ID"))
# ----------------------------------------------------------------------------- #
