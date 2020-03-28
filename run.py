import discord
from discord.ext import commands, tasks
import requests
from bot_command import *
import load_settings
#import db_manager       # mmongoDBを使用する場合
import s3_manager  # cloudcubeを使用する場合
import clanbattle_manager
from channel_manager import send_embed_message,send_error_message



# アクセストークン
TOKEN = load_settings.DISCORD_BOT_TOKEN

# メンバーのサーバー入退室通知を送信するチャンネル
MEMBER_NOTIFICATION_CHANNEL_ID = load_settings.MEMBER_NOTIFICATION_CHANNEL_ID

# prefixをとってくる（再起動時にもデータを保持するため）
## mongoDBを使用する場合
#db_manager.init_data()
#prefix=db_manager.get_prefix()
##

## cloudcubeを使用する場合
try:
    prefix = s3_manager.load_text("prefix")
except:
    print("cloudcubeからのprefixの取得に失敗しました。")
    prefix = "!"
##

bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    # リッチプレセンス（～をプレイ中）を設定
    await bot.change_presence(activity=discord.Game("dev"))
    for guild in bot.guilds:
        channel=guild.system_channel
        embed = discord.Embed(
            title="ℹ BOTが起動しました",
            color=0x00ff00)
        await send_embed_message(bot,embed,channel=channel)

    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    print(f"Current prefix is '{prefix}'")


bot.add_cog(channel(bot))
bot.add_cog(clanbattle(bot))
# Botの起動とDiscordサーバーへの接続
bot.run(TOKEN)
