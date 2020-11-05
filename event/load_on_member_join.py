from discord.ext import commands

from .on_member_join.welcome_message import WelcomeMessage


class OnMemberJoin(WelcomeMessage):
    pass


def setup(bot: commands.Bot) -> None:
    return bot.add_cog(OnMemberJoin(bot))
