##############################
# チャンネル管理関係のコマンド #
##############################

from discord.ext import commands
#import db_manager
import s3_manager
import load_settings

MEMBER_NOTIFICATION_CHANNEL_ID = load_settings.MEMBER_NOTIFICATION_CHANNEL_ID


class channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#######################################
# 各種イベントが発生したときに実行される #
#######################################

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        メンバーがサーバーに参加したときにメッセージを送信する。
        """
        channel = self.bot.get_channel(MEMBER_NOTIFICATION_CHANNEL_ID)
        await channel.send(f"ようこそ！**{member.display_name}** さん")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        メンバーがサーバーから退出したときにメッセージを送信する。
        """
        channel = self.bot.get_channel(MEMBER_NOTIFICATION_CHANNEL_ID)
        await channel.send(f"さようなら、**{member.display_name}** さん")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        """
        メンバーがBANされたときにメッセージを送信する。
        """
        channel = self.bot.get_channel(MEMBER_NOTIFICATION_CHANNEL_ID)
        await channel.send(f"**{member.display_name}** がBANされたよ！")

#######################################
# メッセージが送信されたときに実行される #
#######################################

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        現在のprefixを確認する。

        現在のprefixの影響を受けない。

        Commands
        ----------
        - `!prefix`
        """
        if message.content == "!prefix":
            await message.channel.send(
                f"現在のプレフィックスは`{self.bot.command_prefix}`です。")


########################################
# BOTコマンドが送信されたときに実行される #
########################################

    @commands.command(name='prefix')
    async def __prefix(self, ctx):
        """
        on_messageで定義しているためprefixコマンドを捨てる
        """
        pass

    @commands.command(name='set_prefix')
    async def cmd_set_prefix(self, ctx, *args):
        """
        prefixを変更する。

        スペースを含む場合は""で囲む

        Commands
        ----------
        - `{prefix}set_prefix {Prefix_to_set}`

        Example
        ----------
        - `{prefix}set_prefix !`
        - `{prefix}set_prefix hoge`
        - `{prefix}set_prefix "hoge hoge"`
        - `{prefix}set_prefix "hoge "`
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

        Commands
        ----------
        - `{prefix}test`
        """
        #await ctx.send("テスト")
        await ctx.send("!test")

    @commands.command(name='hello')
    async def hello(self, ctx):
        """
        リプライテスト用。

        Commands
        ----------
        - `{prefix}hello`
        """
        await ctx.send(f"{ctx.author.mention} Hello!")
