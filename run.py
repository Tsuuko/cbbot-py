import discord
from discord.ext import commands
import requests
from bot_command import *
#import db_manager
import load_settings
import s3_manager

# ローカルデバッグ用
# heroku以外で実行する場合shellでこれを実行
# win) set dev=True
# linux) export dev=True

# アクセストークン
TOKEN = load_settings.DISCORD_BOT_TOKEN

## DBを使用する場合
## DBに接続してprefixをとってくる（再起動時にもデータを保持するため）
#db_manager.init_data()
#prefix=db_manager.get_prefix()
##

## cloudcubeを使用する場合
# cloudcubeからprefixをとってくる（再起動時にもデータを保持するため）

try:
    prefix = s3_manager.load_text("prefix")
except:
    print("cloudcubeからのprefixの取得に失敗しました。")
    prefix = "!"
##

bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    print(f"Current prefix is '{prefix}'")


bot.add_cog(channel(bot))

# Botの起動とDiscordサーバーへの接続
bot.run(TOKEN)
