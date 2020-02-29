from discord.ext import commands
#import db_manager
import s3_manager


class channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "!prefix":
            """
            現在のprefixを確認する。
            コマンドは`!prefix`固定（現在のprefixの影響を受けない）
            """
            await message.channel.send(
                f"現在のプレフィックスは`{self.bot.command_prefix}`です。")

    @commands.command(name='set_prefix')
    async def cmd_set_prefix(self, ctx, *args):
        """
        prefixを変更する。
        コマンドは`!set_prefix "prefix"`のように入力する。
        ""を入力しないとスペースで切られてしまう。
        """
        if len(args) != 1:
            msg = "プレフィックスは\"\"で囲んで設定してください。"

        ## cloudcubeを使用する場合の設定
        else:
            s3_manager.save_text(args[0], "prefix")
            self.bot.command_prefix = args[0]
            msg = f"Current prefix: `{self.bot.command_prefix}`"
        ##

        ## dbを使用する場合の設定
        #elif db_manager.set_prefix(args[0]):
        #    self.bot.command_prefix=args[0]
        #    msg=f"Current prefix: `{self.bot.command_prefix}`"
        ##

        await ctx.send(msg)

    @commands.command(name='test')
    async def test(self, ctx):
        """
        コマンドテスト用。
        """
        #await ctx.send("テスト")
        await ctx.send("!test")

    @commands.command(name='hello')
    async def hello(self, ctx):
        """
        リプライテスト用。
        """
        await ctx.send(f"{ctx.author.mention} Hello!")
