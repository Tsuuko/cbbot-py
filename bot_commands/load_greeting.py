from discord.ext import commands

from .greeting.hello import Hello
from .greeting.dev import Dev


class Greeting(Hello, Dev):
    pass


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Greeting(bot))
