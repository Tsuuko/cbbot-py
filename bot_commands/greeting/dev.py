from utils.message import Embed
from discord.ext import commands


class Dev(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="dev")
    async def dev(self, ctx: commands.Context) -> None:
        await Embed.send_info(ctx, "テストタイトル", "本文", "なまえ")
