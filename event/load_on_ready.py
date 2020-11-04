from discord.ext import commands

from .on_ready.login_message import LoginMessage


class OnReady(LoginMessage):
    pass


def setup(bot: commands.Bot) -> None:
    return bot.add_cog(OnReady(bot))
