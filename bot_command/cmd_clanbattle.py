###########################
# クランバトル関係のコマンド #
###########################

from discord.ext import commands, tasks
from datetime import datetime
import discord
import clanbattle_manager
import load_settings
import traceback
from channel_manager import *

CB_NOTIFICATION_CHANNEL_ID = load_settings.CB_NOTIFICATION_CHANNEL_ID
BOT_COMMAND_CHANNEL = load_settings.BOT_COMMAND_CHANNEL
BOT_MANAGER_ROLE = load_settings.BOT_MANAGER_ROLE


class clanbattle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.sheet = clanbattle_manager.spreadsheet()
        self.cbstatus = clanbattle_manager.fetch_status()
        self.cb_is_open = False
        self.cb_remaining_days = -1
        self.now_cbday = -1
        self.check_cbstatus.start()
        self.set_cbstatus.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == BOT_COMMAND_CHANNEL:

            # 凸登録用絵文字が押された場合に凸登録＆ロール付け替え
            # 1凸 :attack1:
            # 2凸 :attack2:
            # 3凸 :attack3:
            # 絵文字での凸登録削除はできない
            if message.content.startswith(
                    "<:attack3:") or message.content.startswith(
                        "<:attack2:") or message.content.startswith(
                            "<:attack1:"):
                if self.cb_is_open is True:
                    username = message.author.display_name
                    self.sheet = clanbattle_manager.spreadsheet()

                    # 3凸報告
                    if message.content.startswith("<:attack3:"):
                        self.sheet.set_attack(message.author.display_name, 3,
                                              self.now_cbday)
                        embed = discord.Embed(
                            title="✅ 登録完了",
                            description=f"[ **{username}** さんを3凸登録しました。 ]",
                            color=0x00ff00)
                        await send_success_message(self.bot,
                                                   embed,
                                                   message=message)

                    # 2凸報告
                    elif message.content.startswith("<:attack2:"):
                        self.sheet.set_attack(message.author.display_name, 2,
                                              self.now_cbday)
                        embed = discord.Embed(
                            title="✅ 登録完了",
                            description=f"[ **{username}** さんを2凸登録しました。 ]",
                            color=0x00ff00)
                        await send_success_message(self.bot,
                                                   embed,
                                                   message=message)

                    # 1凸報告
                    elif message.content.startswith("<:attack1:"):
                        self.sheet.set_attack(message.author.display_name, 1,
                                              self.now_cbday)
                        embed = discord.Embed(
                            title="✅ 登録完了",
                            description=f"[ **{username}** さんを1凸登録しました。 ]",
                            color=0x00ff00)
                        await send_success_message(self.bot,
                                                   embed,
                                                   message=message)

                    # ロール付け替え
                    await set_role(self.bot, "凸報告済", message=message)
                    await unset_role(self.bot, "凸未報告", message=message)

                else:
                    msg = f"""
                        クランバトル開催期間ではありません。
                        開催期間は`{self.bot.command_prefix}status`で確認できます。
                        """
                    await send_error_message(self.bot, msg, message=message)


########################################
# BOTコマンドが送信されたときに実行される #
########################################

    @commands.command(name='regist')
    async def cmd_regist(self, ctx, *args):
        """
        スプレッドシートにユーザーを登録する。

        Commands
        ----------
        - ユーザー指定なし: `{prefix}regist`
        - ユーザー指定: `{prefix}regist -u {username}`
        """

        self.sheet = clanbattle_manager.spreadsheet()

        if len(args) == 0:
            try:
                result = self.sheet.add_user(ctx.author.display_name)
                embed = discord.Embed(
                    title="✅ 登録完了",
                    description=
                    f"[ **{ctx.author.display_name}** さんを{result}行目に登録しました。 ]",
                    color=0x00ff00)
                await send_success_message(self.bot, embed, ctx=ctx)
            except Exception as e:
                msg = str(e)
                await send_error_message(self.bot, msg, ctx=ctx)

        elif len(args) == 2 and args[0] == "-u":
            try:
                result = self.sheet.add_user(args[1])
                embed = discord.Embed(
                    title="✅ 登録完了",
                    description=f"[ **{args[1]}** さんを{result}行目に登録しました。 ]",
                    color=0x00ff00)
                await send_success_message(self.bot, embed, ctx=ctx)

            except Exception as e:
                msg = str(e)
                await send_error_message(self.bot, msg, ctx=ctx)

        else:
            msg = "コマンドの引数が正しくありません。"
            await send_error_message(self.bot, msg, ctx=ctx)

    @commands.command(name='delete')
    async def cmd_delete(self, ctx, *args):
        """
        スプレッドシートからユーザーを削除する。

        Commands
        ----------
        - ユーザー指定なし(自分): `{prefix}delete me`
        - ユーザー指定: `{prefix}delete -u {username}`
        """

        self.sheet = clanbattle_manager.spreadsheet()

        if len(args) == 1 and args[0] == "me":
            try:
                self.sheet.delete_user(ctx.author.display_name)
                embed = discord.Embed(
                    title="✅ 削除完了",
                    description=f"[ **{ctx.author.display_name}** さんを削除しました。 ]",
                    color=0x00ff00)
                await send_success_message(self.bot, embed, ctx=ctx)
            except Exception as e:
                msg = str(e)
                await send_error_message(self.bot, msg, ctx=ctx)

        elif len(args) == 2 and args[0] == "-u":
            try:
                self.sheet.delete_user(args[1])
                embed = discord.Embed(
                    title="✅ 削除完了",
                    description=f"[ **{args[1]}** さんを削除しました。 ]",
                    color=0x00ff00)
                await send_success_message(self.bot, embed, ctx=ctx)

            except Exception as e:
                msg = str(e)
                await send_error_message(self.bot, msg, ctx=ctx)

        else:
            msg = "コマンドの引数が正しくありません。"
            await send_error_message(self.bot, msg, ctx=ctx)

    @commands.command(name='attack')
    async def cmd_attack(self, ctx, *args):
        """
        凸登録をする。

        Commands
        ----------
        - ユーザー指定なし(自分): `{prefix}attack {凸回数}`
        - ユーザー指定: `{prefix}attack -u {username} {凸回数}`

        回数=0-3の数字
        """
        if ctx.message.channel.id == BOT_COMMAND_CHANNEL:
            self.sheet = clanbattle_manager.spreadsheet()
            try:
                if self.cb_is_open is True:
                    if len(args) == 1 and args[0].isdecimal():
                        username = ctx.message.author.display_name
                        attack_count = int(args[0])
                        text = ["0凸", "1凸", "2凸", "3凸"]
                        if (attack_count <= 3) and (attack_count >= 0):
                            self.sheet.set_attack(username, attack_count,
                                                  self.now_cbday)

                            # ロール付け替え
                            if attack_count > 0:
                                await set_role(self.bot, "凸報告済", ctx=ctx)
                                await unset_role(self.bot, "凸未報告", ctx=ctx)
                            else:
                                await set_role(self.bot, "凸未報告", ctx=ctx)
                                await unset_role(self.bot, "凸報告済", ctx=ctx)

                            embed = discord.Embed(
                                title="✅ 登録完了",
                                description=
                                f"[ **{username}** さんを{text[attack_count]}登録しました。 ]",
                                color=0x00ff00)
                            await send_success_message(self.bot,
                                                       embed,
                                                       ctx=ctx)
                        else:
                            msg = """
                                凸回数が正しくありません。
                                0以上3以下で入力してください。
                                （0を入力で凸登録をキャンセルします。）
                                """
                            await send_error_message(self.bot, msg, ctx=ctx)

                    elif len(args) == 3:
                        if is_have_botmanager_role(ctx):
                            if args[0] == "-u" and args[2].isdecimal():
                                username = args[1]
                                attack_count = int(args[2])
                                text = ["0凸", "1凸", "2凸", "3凸"]

                                if (attack_count <= 3) and (attack_count >= 0):
                                    self.sheet.set_attack(
                                        username, attack_count, self.now_cbday)
                                    embed = discord.Embed(
                                        title="✅ 登録完了",
                                        description=
                                        f"[ **{username}** さんを{text[attack_count]}登録しました。 ]",
                                        color=0x00ff00)
                                    await send_success_message(self.bot,
                                                               embed,
                                                               ctx=ctx)

                                else:
                                    msg = """
                                        凸回数が正しくありません。
                                        0以上3以下で入力してください。
                                        （0を入力で凸登録をキャンセルします。）
                                        """
                                    await send_error_message(self.bot,
                                                             msg,
                                                             ctx=ctx)

                            else:
                                msg = f"""
                                    コマンドの引数が正しくありません。
                                    ・自分の凸登録:`{self.bot.command_prefix}attack 回数`
                                    ・他人の凸登録:`{self.bot.command_prefix}attack -u ニックネーム 回数`
                                    　※ニックネームは正確に入力する必要があります。
                                    """
                                await send_error_message(self.bot,
                                                         msg,
                                                         ctx=ctx)

                        else:
                            await send_botmanager_role_error(self.bot, ctx=ctx)

                else:
                    msg = f"""
                        クランバトル開催期間ではありません。
                        開催期間は`{self.bot.command_prefix}status`で確認できます。
                        """
                    await send_error_message(self.bot, msg, ctx=ctx)
            except:
                msg = traceback.format_exc()
                await send_error_message(self.bot, msg, ctx=ctx)

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
        embed.add_field(
            name="🕔開始日時",
            value=self.cbstatus["cb_start"].strftime('%Y/%m/%d %H:%M'),
            inline=False)
        embed.add_field(
            name="🕛終了日時",
            value=self.cbstatus["cb_end"].strftime('%Y/%m/%d %H:%M'),
            inline=False)
        embed.add_field(name="🗓開催期間",
                        value=f"{self.cbstatus['cb_days']} 日間",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='reset_attackrole')
    async def cmd_reset_attackrole(self, ctx):
        """
        全員の凸登録ロールをリセットする。

        Commands
        ----------
        - `{prefix}reset_attackrole`
        """
        attacked_role = discord.utils.find(lambda r: r.name == "凸報告済",
                                           ctx.guild.roles)
        no_attack_role = discord.utils.find(lambda r: r.name == "凸未報告",
                                            ctx.guild.roles)
        if attacked_role is None:
            await ctx.send("`凸報告済`という名前のロールを作成してください。")
        if no_attack_role is None:
            await ctx.send("`凸未報告`という名前のロールを作成してください。")

        for member in ctx.guild.members:
            if not member.bot:
                await member.add_roles(no_attack_role)
                await member.remove_roles(attacked_role)
        await ctx.send("メンバー全員の凸報告済の削除、凸未報告のロール付与が完了しました。")

    @commands.command(name='attacked')
    async def cmd_set_attackrole(self, ctx):
        """
        実行した人に凸報告済みロールをつけて凸未報告ロールを外す。

        Commands
        ----------
        - `{prefix}attacked`
        """
        member = ctx.guild.get_member(ctx.author.id)

        attacked_role = discord.utils.find(lambda r: r.name == "凸報告済",
                                           ctx.guild.roles)
        no_attack_role = discord.utils.find(lambda r: r.name == "凸未報告",
                                            ctx.guild.roles)
        if attacked_role is None:
            await ctx.send("`凸報告済`という名前のロールを作成してください。")
        if no_attack_role is None:
            await ctx.send("`凸未報告`という名前のロールを作成してください。")

        await member.add_roles(attacked_role)
        await member.remove_roles(no_attack_role)
        await ctx.send(
            f"{ctx.message.author.mention} 凸未報告の削除、凸報告済のロール付与が完了しました。")

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
    async def set_cbstatus(self):
        """
        10秒毎にクランバトル開催情報を設定する。
        """
        # BOT動作中か確認（起動前にchannel.sendすると動作が止まってしまう）
        if not self.bot.is_ready():
            print("定期実行: set_cbstatus(): BOTログイン前")
        else:
            cb_is_open, cb_remaining_days, now_cbday = clanbattle_manager.set_cbstatus(
                self.status)
            # 現在の開催状況と取得した開催情報が同じ
            if (self.cb_is_open == cb_is_open):
                if self.cb_remaining_days > cb_remaining_days:
                    self.cb_is_open = cb_is_open
                    self.cb_remaining_days = cb_remaining_days
                    self.now_cbday = now_cbday
                    channel = self.bot.get_channel(CB_NOTIFICATION_CHANNEL_ID)
                    await channel.send(
                        f"クラバト{self.status['cb_days']-cb_remaining_days}日目です！！"
                    )
                    print(
                        f"定期実行: set_cbstatus: self.cb_is_open={self.cb_is_open}, self.cb_remaining_days={self.cb_remaining_days}, now_cbday={self.now_cbday}"
                    )
            # 現在の開催状況と取得した開催情報が異なる（非開催中->開催中 or 開催中->非開催中）
            elif self.cb_is_open != cb_is_open:
                # 非開催中->開催中
                if (self.cb_is_open == False) and (cb_is_open == True):
                    self.cb_is_open = cb_is_open
                    self.cb_remaining_days = cb_remaining_days
                    self.now_cbday = now_cbday
                    channel = self.bot.get_channel(CB_NOTIFICATION_CHANNEL_ID)
                    await channel.send("クラバトが開始しました！！")
                # 開催中->非開催中
                elif (self.cb_is_open == True) and (cb_is_open == False):
                    self.cb_is_open = cb_is_open
                    self.cb_remaining_days = cb_remaining_days
                    self.now_cbday = now_cbday
                    channel = self.bot.get_channel(CB_NOTIFICATION_CHANNEL_ID)
                    await channel.send("クラバトが終了しました！！")
                print(
                    f"定期実行: set_cbstatus: self.cb_is_open={self.cb_is_open}, self.cb_remaining_days={self.cb_remaining_days}, now_cbday={self.now_cbday}"
                )
