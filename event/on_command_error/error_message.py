from discord.ext import commands
from utils import logger


class ErrorMessage(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logger.getLogger()

    @commands.Cog.listener("on_command_error")
    async def error_message(self, ctx: commands.Context, exception: Exception) -> None:
        msg = f"コマンドが正しくありません。{exception}"
        self.logger.warn(msg)
        await ctx.send(msg)
