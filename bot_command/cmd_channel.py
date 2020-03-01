from discord.ext import commands
#import db_manager
import s3_manager
import load_settings

MEMBER_NOTIFICATION_CHANNEL_ID=load_settings.MEMBER_NOTIFICATION_CHANNEL_ID


class channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#######################################
# メッセージが送信されたときに実行される #
#######################################
    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(MEMBER_NOTIFICATION_CHANNEL_ID)
        await channel.send(f"ようこそ！**{member.display_name}** さん")

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        channel = self.bot.get_channel(MEMBER_NOTIFICATION_CHANNEL_ID)
        await channel.send(f"さようなら、**{member.display_name}** さん")

    @commands.Cog.listener()
    async def on_member_ban(self,guild,member):
        channel = self.bot.get_channel(MEMBER_NOTIFICATION_CHANNEL_ID)
        await channel.send(f"**{member.display_name}** がBANされたよ！")


#######################################
# メッセージが送信されたときに実行される #
#######################################
    @commands.Cog.listener()
    async def on_message(self, message):
        #--------------------
        # 現在のprefixを確認する。
        # コマンドは`!prefix`固定（現在のprefixの影響を受けない）
        #--------------------
        if message.content == "!prefix":
            await message.channel.send(f"現在のプレフィックスは`{self.bot.command_prefix}`です。")




########################################
# BOTコマンドが送信されたときに実行される #
########################################

    @commands.command(name='aprefix')
    async def __prefix(self, ctx):
        """
        on_messageで定義しているためprefixコマンドを捨てる
        """

    @commands.command(name='set_prefix')
    async def cmd_set_prefix(self, ctx, *args):
        """
        prefixを変更する。
        コマンドは`!set_prefix "prefix"`のように入力する。
        ""を入力しないとスペースで切られてしまう。
        """
        if len(args) != 1:
            msg = "プレフィックスは\"\"で囲んで設定してください。"

        ## cloudcubeを使用する場合
        else:
            s3_manager.save_text(args[0], "prefix")
            self.bot.command_prefix = args[0]
            msg = f"Current prefix: `{self.bot.command_prefix}`"
        ##

        ## dbを使用する場合
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
