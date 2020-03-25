from discord.ext import commands, tasks
from datetime import datetime
import discord
import clanbattle_manager
import load_settings

CB_NOTIFICATION_CHANNEL_ID = load_settings.CB_NOTIFICATION_CHANNEL_ID


class clanbattle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheet = clanbattle_manager.spreadsheet()
        self.cbstatus = clanbattle_manager.fetch_status()
        self.cb_is_open = False
        self.cb_remaining_days = -1
        self.check_cbstatus.start()
        self.set_cbstatus.start()

    @commands.command(name='regist')
    async def cmd_regist(self, ctx, *args):
        """
        スプレッドシートにユーザーを登録する。

        Commands
        ----------
        - ユーザー指定なし: `{prefix}regist`
        - ユーザー指定: `{prefix}regist -u {username}`
        """
        if len(args) == 0:
            try:
                result = self.sheet.add_user(ctx.author.display_name)
                embed = discord.Embed(
                    title="✅ 登録完了",
                    description=
                    f"[ **{ctx.author.display_name}** さんを{result}行目に登録しました。 ]",
                    color=0x00ff00)

            except Exception as e:
                embed = discord.Embed(title="❎ エラー",
                                      description=(str(e)),
                                      color=0xff0000)

        elif len(args) == 2 and args[0] == "-u":
            try:
                result = self.sheet.add_user(args[1])
                embed = discord.Embed(
                    title="✅ 登録完了",
                    description=f"[ **{args[1]}** さんを{result}行目に登録しました。 ]",
                    color=0x00ff00)

            except Exception as e:
                embed = discord.Embed(title="❎ エラー",
                                      description=str(e),
                                      color=0xff0000)

        else:
            embed = discord.Embed(title="❎ エラー",
                                  description="コマンドの引数が正しくありません。",
                                  color=0xff0000)

        embed.set_footer(text=self.bot.user.display_name,
                         icon_url=self.bot.user.avatar_url)
        embed.set_author(name=ctx.message.content)
        await ctx.send(embed=embed)

    @commands.command(name='delete')
    async def cmd_delete(self, ctx, *args):
        """
        スプレッドシートからユーザーを削除する。

        Commands
        ----------
        - ユーザー指定なし(自分): `{prefix}delete me`
        - ユーザー指定: `{prefix}delete -u {username}`
        """
        if len(args) == 1 and args[0] == "me":
            try:
                result = self.sheet.delete_user(ctx.author.display_name)
                embed = discord.Embed(
                    title="✅ 削除完了",
                    description=f"[ **{ctx.author.display_name}** さんを削除しました。 ]",
                    color=0x00ff00)

            except Exception as e:
                embed = discord.Embed(title="❎ エラー",
                                      description=str(e),
                                      color=0xff0000)

        elif len(args) == 2 and args[0] == "-u":
            try:
                result = self.sheet.delete_user(args[1])
                embed = discord.Embed(
                    title="✅ 削除完了",
                    description=f"[ **{args[1]}** さんを削除しました。 ]",
                    color=0x00ff00)

            except Exception as e:
                embed = discord.Embed(title="❎ エラー",
                                      description=str(e),
                                      color=0xff0000)

        else:
            embed = discord.Embed(title="❎ エラー",
                                  description="コマンドの引数が正しくありません。",
                                  color=0xff0000)

        embed.set_footer(text=self.bot.user.display_name,
                         icon_url=self.bot.user.avatar_url)
        embed.set_author(name=ctx.message.content)
        await ctx.send(embed=embed)

    @commands.command(name='status')
    async def cmd_getstatus(self, ctx):
        """
        クランバトル開催情報を表示する。

        Commands
        ----------
        - `{prefix}status`
        """
        self.cbstatus = clanbattle_manager.fetch_status()
        embed = discord.Embed(title="⚔クランバトル開催情報⚔", color=0x00ffff)
        embed.add_field(name="🕔開始日時",
                        value=status["cb_start"].strftime('%Y/%m/%d %H:%M'),
                        inline=False)
        embed.add_field(name="🕛終了日時",
                        value=status["cb_end"].strftime('%Y/%m/%d %H:%M'),
                        inline=False)
        embed.add_field(name="🗓開催期間",
                        value=f"{status['cb_days']} 日間",
                        inline=False)
        await ctx.send(embed=embed)

    ####################
    # 定期的に実行される #
    ####################

    @tasks.loop(seconds=3600.0)
    async def check_cbstatus(self):
        """
        1時間（3600秒）ごとにクラバト開催情報を取ってくる。
        """
        self.status = clanbattle_manager.fetch_status()

    @tasks.loop(seconds=10.0)
    #@commands.command(name='chk')
    async def set_cbstatus(self):
        """
        10秒毎にクランバトル開催情報を設定する。
        """
        # BOT動作中か確認（起動前にchannel.sendすると動作が止まってしまう）
        if not self.bot.is_ready():
            print("定期実行: set_cbstatus(): BOTログイン前")
        else:
            cb_is_open, cb_remaining_days = clanbattle_manager.set_cbstatus(
                self.status)
            # 現在の開催状況と取得した開催情報が同じ
            if (self.cb_is_open == cb_is_open):
                if self.cb_remaining_days > cb_remaining_days:
                    channel = self.bot.get_channel(CB_NOTIFICATION_CHANNEL_ID)
                    await channel.send(
                        f"クラバト{self.status['cb_days']-cb_remaining_days}日目です！！"
                    )
                    print(
                        f"定期実行: set_cbstatus: self.cb_is_open={self.cb_is_open}, self.cb_remaining_days={self.cb_remaining_days}"
                    )
            # 現在の開催状況と取得した開催情報が異なる（非開催中->開催中 or 開催中->非開催中）
            elif self.cb_is_open != cb_is_open:
                # 非開催中->開催中
                if (self.cb_is_open == False) and (cb_is_open == True):
                    channel = self.bot.get_channel(CB_NOTIFICATION_CHANNEL_ID)
                    await channel.send("クラバトが開始しました！！")
                # 開催中->非開催中
                elif (self.cb_is_open == True) and (cb_is_open == False):
                    channel = self.bot.get_channel(CB_NOTIFICATION_CHANNEL_ID)
                    await channel.send("クラバトが終了しました！！")
                print(
                    f"定期実行: set_cbstatus: self.cb_is_open={self.cb_is_open}, self.cb_remaining_days={self.cb_remaining_days}"
                )

            self.cb_is_open = cb_is_open
            self.cb_remaining_days = cb_remaining_days

    @commands.command(name='setstatus')
    async def cmd_setstatus(self, ctx):
        pass
