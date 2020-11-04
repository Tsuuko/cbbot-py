from discord.ext import commands


class Hello(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx: commands.Context) -> None:
        await ctx.send("hello!")
