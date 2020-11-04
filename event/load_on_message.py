from discord.ext import commands

from .on_message.message_test import MessageTest


class OnMessage(MessageTest):
    pass


def setup(bot: commands.Bot) -> None:
    return bot.add_cog(OnMessage(bot))
