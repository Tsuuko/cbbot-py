from discord.ext import commands
from datetime import datetime
import requests


class clanbattle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
def fetch_status():
    """
    解析サイト<https://redive.estertion.win> からクラバト情報を取ってくる
    return {
        "cb_start": datetime,
        "cb_end": datetime,
        "cb_days": int
    }
    """
    # クラバト開催情報取得
    r = requests.get(
        "https://redive.estertion.win/ver_log_redive/?page=1&filter=clan_battle"
    ).json()

    # クラバト開始日取得
    cb_start = r["data"][0]["clan_battle"][0]["start"]
    cb_start = datetime.strptime(cb_start, "%Y/%m/%d %H:%M:%S")

    # クラバト終了日取得
    cb_end = r["data"][0]["clan_battle"][0]["end"]
    cb_end = datetime.strptime(cb_end, "%Y/%m/%d %H:%M:%S")

    # クラバト開催日数
    cb_days = (cb_end - cb_start).days + 1

    return {"cb_start": cb_start, "cb_end": cb_end, "cb_days": cb_days}

