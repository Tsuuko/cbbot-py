from discord.ext import commands

from .greeting.hello import Hello


class Greeting(Hello):
    pass


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Greeting(bot))
