import discord
from discord.ext import commands
from utils import logger, settings


class LeaveMessage(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logger.getLogger()

    @commands.Cog.listener("on_member_remove")
    async def leave_message(self, member: discord.Member) -> None:
        if not settings.MEMBER_NOTIFICATION_CHANNEL_ID:
            self.logger.error("環境変数 `MEMBER_NOTIFICATION_CHANNEL_ID`が設定されていません。")
            return

        channel = self.bot.get_channel(settings.MEMBER_NOTIFICATION_CHANNEL_ID)

        if not settings.MEMBER_NOTIFICATION_CHANNEL_ID:
            await self.logger.error(
                "MEMBER_NOTIFICATION_CHANNEL_IDで指定したChannelが見つかりません。"
            )
            return

        self.logger.info(f"[メンバー脱退] {member} - {member.id}")
        await channel.send(
            settings.MessageText.LEAVE_MESSAGE.format(display_name=member.display_name)
        )
