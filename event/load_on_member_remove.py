from discord.ext import commands

from .on_member_remove.leave_message import LeaveMessage


class OnMemberRemove(LeaveMessage):
    pass


def setup(bot: commands.Bot) -> None:
    return bot.add_cog(OnMemberRemove(bot))
