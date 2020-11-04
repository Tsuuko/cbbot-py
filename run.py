import discord
from discord.ext import commands

from utils import settings

# 環境変数に設定されている場合はその文字列、されていない場合はなし
activity = discord.Game(name=settings.ACTIVITY_NAME) if settings.ACTIVITY_NAME else None

bot = commands.Bot(
    command_prefix="!",
    activity=activity,
)

# エクステンション読み込み
for ext in settings.EXTENSIONS:
    bot.load_extension(ext)

# bot起動
bot.run(settings.DISCORD_BOT_TOKEN)
