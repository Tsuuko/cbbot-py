from discord.ext import commands
from utils import logger


class LoginMessage(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.logger = logger.getLogger()
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def login_message(self) -> None:
        self.logger.info("ログインしました")
