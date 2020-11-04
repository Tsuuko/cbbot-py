from discord.ext import commands

from .on_command_error.error_message import ErrorMessage


class OnCommandError(ErrorMessage):
    pass


def setup(bot: commands.Bot) -> None:
    bot.add_cog(OnCommandError(bot))
