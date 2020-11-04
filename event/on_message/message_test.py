import discord
from discord.ext import commands
from utils import logger


class MessageTest(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logger.getLogger()

    @commands.Cog.listener("on_message")
    async def message_test(self, message: discord.Message) -> None:
        self.logger.info(f"message recieved: {message.content}")
