###########################
# クランバトル関係のコマンド #
###########################

import traceback

import discord
from discord.ext import commands, tasks

import load_settings
from manager import clanbattle_manager
from manager.channel_manager import (
    clear_attackrole,
    is_have_botmanager_role,
    reset_attackrole,
    send_botmanager_role_error,
    send_embed_message,
    send_error_message,
    set_role,
    unset_role,
)

CB_NOTIFICATION_CHANNEL_ID = load_settings.CB_NOTIFICATION_CHANNEL_ID
BOT_COMMAND_CHANNEL = load_settings.BOT_COMMAND_CHANNEL
BOT_MANAGER_ROLE = load_settings.BOT_MANAGER_ROLE


class clanbattle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheet = clanbattle_manager.spreadsheet()
        self.cbstatus = clanbattle_manager.fetch_status()
        self.cb_is_open = False
        self.cb_remaining_days = -1
        self.now_cbday = None
        self.check_cbstatus.start()
        self.set_cbstatus.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        # チャンネルがBOTコマンドチャンネルの場合
        if message.channel.id == BOT_COMMAND_CHANNEL:
            # 凸登録用絵文字が押された場合に凸登録＆ロール付け替え
            # 1凸 :attack1:
            # 2凸 :attack2:
            # 3凸 :attack3:
            # 絵文字での凸登録削除はできない
            if (
                message.content.startswith("<:attack3:")
                or message.content.startswith("<:attack2:")
                or message.content.startswith("<:attack1:")
            ):
                if self.cb_is_open is True:
                    username = message.author.display_name

                    # 3凸報告
                    if message.content.startswith("<:attack3:"):
                        try:
                            self.sheet.set_attack(
                                message.author.display_name, 3, self.now_cbday
                            )
                            embed = discord.Embed(
                                title="✅ 登録完了",
                                description=f"**{username}** さんを3凸登録しました。",
                                color=0x00FF00,
                            )
                            await send_embed_message(
                                self.bot,
                                embed,
                                plain_text=message.author.mention,
                                message=message,
                            )
                        except Exception as e:
                            msg = str(e)
                            await send_error_message(self.bot, msg, message=message)

                    # 2凸報告
                    elif message.content.startswith("<:attack2:"):
                        try:
                            self.sheet.set_attack(
                                message.author.display_name, 2, self.now_cbday
                            )
                            embed = discord.Embed(
                                title="✅ 登録完了",
                                description=f"**{username}** さんを2凸登録しました。",
                                color=0x00FF00,
                            )
                            await send_embed_message(
                                self.bot,
                                embed,
                                plain_text=message.author.mention,
                                message=message,
                            )
                        except Exception as e:
                            msg = str(e)
                            await send_error_message(self.bot, msg, message=message)

                    # 1凸報告
                    elif message.content.startswith("<:attack1:"):
                        try:
                            self.sheet.set_attack(
                                message.author.display_name, 1, self.now_cbday
                            )
                            embed = discord.Embed(
                                title="✅ 登録完了",
                                description=f"**{username}** さんを1凸登録しました。",
                                color=0x00FF00,
                            )
                            await send_embed_message(
                                self.bot,
                                embed,
                                plain_text=message.author.mention,
                                message=message,
                            )
                        except Exception as e:
                            msg = str(e)
                            await send_error_message(
                                self.bot,
                                msg,
                                plain_text=message.author.mention,
                                message=message,
                            )

                    # ロール付け替え
                    await set_role(self.bot, "凸報告済", message=message)
                    await unset_role(self.bot, "凸未報告", message=message)

                else:
                    msg = f"クランバトル開催期間ではありません。\n開催期間は`{self.bot.command_prefix}status`で確認できます。"
                    await send_error_message(self.bot, msg, message=message)

    ########################################
    # BOTコマンドが送信されたときに実行される #
    ########################################

    @commands.command(name="regist")
    async def cmd_regist(self, ctx, *args):
        """
        スプレッドシートにユーザーを登録する。 ★ユーザー指定はBOT_MANAGER_ROLE限定

        Commands
        ----------
        - ユーザー指定なし: `{prefix}regist`
        - ユーザー指定: `{prefix}regist -u {username}`
        """
        # チャンネルがBOTコマンドチャンネルの場合
        if ctx.message.channel.id == BOT_COMMAND_CHANNEL:
            if len(args) == 0:
                try:
                    self.sheet.add_user(ctx.author.display_name)
                    embed = discord.Embed(
                        title="✅ 登録完了",
                        description=f"**{ctx.author.display_name}** さんを登録しました。",
                        color=0x00FF00,
                    )
                    await send_embed_message(
                        self.bot, embed, plain_text=ctx.author.mention, ctx=ctx
                    )
                except Exception as e:
                    msg = str(e)
                    await send_error_message(self.bot, msg, ctx=ctx)

            elif len(args) == 2 and args[0] == "-u":
                # BOT_MANAGER_ROLEチェック
                if is_have_botmanager_role(ctx.author):
                    try:
                        self.sheet.add_user(args[1])
                        embed = discord.Embed(
                            title="✅ 登録完了",
                            description=f"**{args[1]}** さんを登録しました。",
                            color=0x00FF00,
                        )
                        await send_embed_message(
                            self.bot, embed, plain_text=ctx.author.mention, ctx=ctx
                        )

                    except Exception as e:
                        msg = str(e)
                        await send_error_message(
                            self.bot, msg, plain_text=ctx.author.mention, ctx=ctx
                        )
                # BOT_MANAGER_ROLEを持っていない場合
                else:
                    await send_botmanager_role_error(
                        self.bot, plain_text=ctx.author.mention, ctx=ctx
                    )
            else:
                msg = "コマンドの引数が正しくありません。"
                await send_error_message(
                    self.bot, msg, plain_text=ctx.author.mention, ctx=ctx
                )

    @commands.command(name="delete")
    async def cmd_delete(self, ctx, *args):
        """
        スプレッドシートからユーザーを削除する。 ★ユーザー指定はBOT_MANAGER_ROLE限定

        Commands
        ----------
        - ユーザー指定なし(自分): `{prefix}delete me`
        - ユーザー指定: `{prefix}delete -u {username}`
        """
        # チャンネルがBOTコマンドチャンネルの場合
        if ctx.message.channel.id == BOT_COMMAND_CHANNEL:
            if len(args) == 1 and args[0] == "me":
                try:
                    self.sheet.delete_user(ctx.author.display_name)
                    embed = discord.Embed(
                        title="✅ 削除完了",
                        description=f"**{ctx.author.display_name}** さんを削除しました。",
                        color=0x00FF00,
                    )
                    await send_embed_message(
                        self.bot, embed, plain_text=ctx.author.mention, ctx=ctx
                    )
                except Exception as e:
                    msg = str(e)
                    await send_error_message(
                        self.bot, msg, plain_text=ctx.author.mention, ctx=ctx
                    )

            elif len(args) == 2 and args[0] == "-u":
                # BOT_MANAGER_ROLEチェック
                if is_have_botmanager_role(ctx.author):
                    try:
                        self.sheet.delete_user(args[1])
                        embed = discord.Embed(
                            title="✅ 削除完了",
                            description=f"**{args[1]}** さんを削除しました。",
                            color=0x00FF00,
                        )
                        await send_embed_message(
                            self.bot, embed, plain_text=ctx.author.mention, ctx=ctx
                        )

                    except Exception as e:
                        msg = str(e)
                        await send_error_message(
                            self.bot, msg, plain_text=ctx.author.mention, ctx=ctx
                        )
                # BOT_MANAGER_ROLEを持っていない場合
                else:
                    await send_botmanager_role_error(
                        self.bot, plain_text=ctx.author.mention, ctx=ctx
                    )

            else:
                msg = "コマンドの引数が正しくありません。"
                await send_error_message(
                    self.bot, msg, plain_text=ctx.author.mention, ctx=ctx
                )

    @commands.command(name="attack")
    async def cmd_attack(self, ctx, *args):
        """
        凸登録をする。 ★ユーザー指定はBOT_MANAGER_ROLE限定

        Commands
        ----------
        - ユーザー指定なし(自分): `{prefix}attack {凸回数}`
        - ユーザー指定: `{prefix}attack -u {username} {凸回数}`

        回数=0-3の数字
        """
        if ctx.message.channel.id == BOT_COMMAND_CHANNEL:
            try:
                if self.cb_is_open is True:
                    if len(args) == 1 and args[0].isdecimal():
                        username = ctx.message.author.display_name
                        attack_count = int(args[0])
                        text = ["0凸", "1凸", "2凸", "3凸"]
                        if (attack_count <= 3) and (attack_count >= 0):
                            try:
                                self.sheet.set_attack(
                                    username, attack_count, self.now_cbday
                                )
                            except Exception as e:
                                msg = str(e)
                                await send_error_message(
                                    self.bot,
                                    msg,
                                    plain_text=ctx.author.mention,
                                    ctx=ctx,
                                )

                            # ロール付け替え
                            if attack_count > 0:
                                await set_role(self.bot, "凸報告済", ctx=ctx)
                                await unset_role(self.bot, "凸未報告", ctx=ctx)
                            else:
                                await set_role(self.bot, "凸未報告", ctx=ctx)
                                await unset_role(self.bot, "凸報告済", ctx=ctx)

                            embed = discord.Embed(
                                title="✅ 登録完了",
                                description=f"**{username}** さんを{text[attack_count]}登録しました。",
                                color=0x00FF00,
                            )
                            await send_embed_message(
                                self.bot, embed, plain_text=ctx.author.mention, ctx=ctx
                            )
                        else:
                            msg = """
凸回数が正しくありません。
0以上3以下で入力してください。
（0を入力で凸登録をキャンセルします。）
                                """
                            await send_error_message(
                                self.bot, msg, plain_text=ctx.author.mention, ctx=ctx
                            )

                    elif len(args) == 3:
                        # BOT_MANAGER_ROLEチェック
                        if is_have_botmanager_role(ctx.author):
                            if args[0] == "-u" and args[2].isdecimal():
                                username = args[1]
                                attack_count = int(args[2])
                                text = ["0凸", "1凸", "2凸", "3凸"]

                                if (attack_count <= 3) and (attack_count >= 0):
                                    self.sheet.set_attack(
                                        username, attack_count, self.now_cbday
                                    )
                                    embed = discord.Embed(
                                        title="✅ 登録完了",
                                        description=f"**{username}** さんを{text[attack_count]}登録しました。",
                                        color=0x00FF00,
                                    )
                                    await send_embed_message(
                                        self.bot,
                                        embed,
                                        plain_text=ctx.author.mention,
                                        ctx=ctx,
                                    )

                                else:
                                    msg = """
凸回数が正しくありません。
0以上3以下で入力してください。
（0を入力で凸登録をキャンセルします。）
                                        """
                                    await send_error_message(
                                        self.bot,
                                        msg,
                                        plain_text=ctx.author.mention,
                                        ctx=ctx,
                                    )

                            else:
                                msg = f"""
コマンドの引数が正しくありません。
・自分の凸登録:`{self.bot.command_prefix}attack 回数`
・他人の凸登録:`{self.bot.command_prefix}attack -u ニックネーム 回数`
　※ニックネームは正確に入力する必要があります。
                                    """
                                await send_error_message(
                                    self.bot,
                                    msg,
                                    plain_text=ctx.author.mention,
                                    ctx=ctx,
                                )
                        # BOT_MANAGER_ROLEを持っていない場合
                        else:
                            await send_botmanager_role_error(
                                self.bot, plain_text=ctx.author.mention, ctx=ctx
                            )
                    else:
                        msg = f"""
コマンドの引数が正しくありません。
・自分の凸登録:`{self.bot.command_prefix}attack 回数`
・他人の凸登録:`{self.bot.command_prefix}attack -u ニックネーム 回数`
　※ニックネームは正確に入力する必要があります。
                            """
                        await send_error_message(
                            self.bot, msg, plain_text=ctx.author.mention, ctx=ctx
                        )

                else:
                    msg = f"クランバトル開催期間ではありません。\n開催期間は`{self.bot.command_prefix}status`で確認できます。"
                    await send_error_message(
                        self.bot, msg, plain_text=ctx.author.mention, ctx=ctx
                    )
            except:  # noqa: E722
                msg = traceback.format_exc()
                await send_error_message(
                    self.bot, msg, plain_text=ctx.author.mention, ctx=ctx
                )

    @commands.command(name="status")
    async def cmd_getstatus(self, ctx):
        """
        クランバトル開催情報を表示する。

        Commands
        ----------
        - `{prefix}status`
        """
        self.cbstatus = clanbattle_manager.fetch_status()
        embed = discord.Embed(title="⚔ クランバトル開催情報 ⚔", color=0x00FFFF)
        embed.add_field(
            name="🕔 開始日時",
            value=self.cbstatus["cb_start"].strftime("%Y/%m/%d %H:%M"),
            inline=False,
        )
        embed.add_field(
            name="🕛 終了日時",
            value=self.cbstatus["cb_end"].strftime("%Y/%m/%d %H:%M"),
            inline=False,
        )
        embed.add_field(
            name="🗓 開催期間", value=f"{self.cbstatus['cb_days']} 日間", inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(name="reset_attackrole")
    async def cmd_reset_attackrole(self, ctx):
        """
        全員の凸登録ロールをリセットする。 ★BOT_MANAGER_ROLE限定

        Commands
        ----------
        - `{prefix}reset_attackrole`
        """
        # BOT_MANAGER_ROLEチェック
        if is_have_botmanager_role(ctx.author):
            try:
                await reset_attackrole(ctx.guild)
                embed = discord.Embed(
                    title="✅ 実行完了", description="全員の凸登録ロールをリセットしました。", color=0x00FF00
                )
                await send_embed_message(
                    self.bot, embed, plain_text=ctx.author.mention, ctx=ctx
                )
            except Exception as e:
                await send_error_message(
                    self.bot, str(e), plain_text=ctx.author.mention, ctx=ctx
                )
        # BOT_MANAGER_ROLEを持っていない場合
        else:
            await send_botmanager_role_error(
                self.bot, plain_text=ctx.author.mention, ctx=ctx
            )

    @commands.command(name="clear_attackrole")
    async def cmd_clear_attackrole(self, ctx):
        """
        全員の凸登録ロールをクリアする。 ★BOT_MANAGER_ROLE限定

        Commands
        ----------
        - `{prefix}clear_attackrole`
        """
        # BOT_MANAGER_ROLEチェック
        if is_have_botmanager_role(ctx.author):
            try:
                await clear_attackrole(ctx.guild)
                embed = discord.Embed(
                    title="✅ 実行完了", description="全員の凸登録ロールを削除しました。", color=0x00FF00
                )
                await send_embed_message(
                    self.bot, embed, plain_text=ctx.author.mention, ctx=ctx
                )
            except Exception as e:
                await send_error_message(
                    self.bot, str(e), plain_text=ctx.author.mention, ctx=ctx
                )
        # BOT_MANAGER_ROLEを持っていない場合
        else:
            await send_botmanager_role_error(
                self.bot, plain_text=ctx.author.mention, ctx=ctx
            )

    # @commands.command(name='attacked')
    # async def cmd_set_attackrole(self, ctx):
    #    """
    #    実行した人に凸報告済みロールをつけて凸未報告ロールを外す。
    #
    #    Commands
    #    ----------
    #    - `{prefix}attacked`
    #    """
    #    member = ctx.guild.get_member(ctx.author.id)
    #
    #    attacked_role = discord.utils.find(lambda r: r.name == "凸報告済",
    #                                       ctx.guild.roles)
    #    no_attack_role = discord.utils.find(lambda r: r.name == "凸未報告",
    #                                        ctx.guild.roles)
    #    if attacked_role is None:
    #        await ctx.send("`凸報告済`という名前のロールを作成してください。")
    #    if no_attack_role is None:
    #        await ctx.send("`凸未報告`という名前のロールを作成してください。")
    #
    #    await member.add_roles(attacked_role)
    #    await member.remove_roles(no_attack_role)
    #    await ctx.send(
    #        f"{ctx.message.author.mention} 凸未報告の削除、凸報告済のロール付与が完了しました。")

    @commands.command(name="clear_sheet")
    async def clear_sheet(self, ctx):
        """
        凸管理シートをクリアする。 ★BOT_MANAGER_ROLE限定

        Commands
        ----------
        - `{prefix}clear_sheet`
        """
        # BOT_MANAGER_ROLEチェック
        if is_have_botmanager_role(ctx.author):
            try:
                self.sheet.clear_all_attack()
                embed = discord.Embed(
                    title="✅ 実行完了", description="凸管理シートをクリアしました。", color=0x00FF00
                )
                await send_embed_message(
                    self.bot, embed, plain_text=ctx.author.mention, ctx=ctx
                )

            except Exception as e:
                await send_error_message(
                    self.bot, str(e), plain_text=ctx.author.mention, ctx=ctx
                )
        # BOT_MANAGER_ROLEを持っていない場合
        else:
            await send_botmanager_role_error(
                self.bot, plain_text=ctx.author.mention, ctx=ctx
            )

    @commands.command(name="capture")
    async def capture(self, ctx):
        """
        凸管理シートキャプチャ画像送信
        PDFでダウンロードして画像に変換し、送信する。

        Commands
        ----------
        - `{prefix}capture`
        """
        f = clanbattle_manager.shot_capture()
        await ctx.send(file=discord.File(f, filename="capture.png"))

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
    async def set_cbstatus(self):  # noqa: C901
        """
        10秒毎にクランバトル開催情報を設定する。
        """
        # BOT動作中か確認（起動前にchannel.sendすると動作が止まってしまう）
        if not self.bot.is_ready():
            print("定期実行: set_cbstatus(): BOTログイン前")
        else:
            cb_is_open, cb_remaining_days, now_cbday = clanbattle_manager.set_cbstatus(
                self.status
            )
            # メッセージセクション
            msg_list = list()
            # infoメッセージセクション
            info_msg_list = list()
            # errorメッセージセクション
            error_msg_list = list()

            # embed
            embed = None

            # debug
            # info_msg_list.append(f"**Debug_Data**")
            # info_msg_list.append(f"cb_is_open:{cb_is_open}")
            # info_msg_list.append(f"self.cb_is_open:{self.cb_is_open}")
            # info_msg_list.append(f"cb_remaining_days:{cb_remaining_days}")
            # info_msg_list.append(f"self.cb_remaining_days:{self.cb_remaining_days}")
            # info_msg_list.append(f"now_cbday:{now_cbday}")
            # info_msg_list.append(f"self.now_cbday:{self.now_cbday}")
            ####

            # 現在の開催状況と取得した開催情報が同じ
            if self.cb_is_open == cb_is_open:
                # クラバト開催中の場合
                if cb_is_open:
                    # 日付が進んだ場合
                    if self.cb_remaining_days > cb_remaining_days:
                        self.cb_is_open = cb_is_open
                        self.cb_remaining_days = cb_remaining_days
                        self.now_cbday = now_cbday
                        channel = self.bot.get_channel(CB_NOTIFICATION_CHANNEL_ID)

                        # 開始メッセージのembed作成
                        embed = discord.Embed(title="🗓 日付が変わりました 🗓", color=0x00FF00)

                        # メッセージ追加
                        msg_list.append(f"クランバトル{self.now_cbday}日目です！\n今日も頑張りましょう💪")

                        # ロールを付け替えInfoを追加
                        try:
                            await reset_attackrole(channel.guild)
                            info_msg_list.append("メンバー全員の凸報告ロールをリセットしました。")

                        # ロール付け替えに失敗した場合はエラー文を追加
                        except Exception as e:
                            error_msg_list.append(str(e))

                        print(
                            f"定期実行: set_cbstatus: 日付進行: is_open={self.cb_is_open}, remaining_days={self.cb_remaining_days}, now_cbday={self.now_cbday}"
                        )
                    # ステータス変更なし
                    else:
                        pass
                # 非開催中
                else:
                    pass

            # 現在の開催状況と取得した開催情報が異なる（非開催中->開催中 or 開催中->非開催中）
            elif self.cb_is_open != cb_is_open:
                channel = self.bot.get_channel(CB_NOTIFICATION_CHANNEL_ID)

                # 非開催中->開催中
                if (self.cb_is_open is False) and (cb_is_open is True):
                    self.cb_is_open = cb_is_open
                    self.cb_remaining_days = cb_remaining_days

                    # 開催中メッセージのembed作成
                    embed = discord.Embed(title="⚔ クランバトル開催中です ⚔", color=0x00FF00)

                    # BOT起動時にクラバトが開催中の場合
                    if self.now_cbday is None:
                        self.now_cbday = now_cbday

                        # クラバト最終日以外
                        if self.cb_remaining_days == 0:
                            msg_list.append(
                                "クランバトル最終日です！\n本日23時59分までの開催のため、深夜勢はお気をつけください！"
                            )
                            print(
                                f"定期実行: set_cbstatus: 初回起動_クラバト最終日以外: is_open={self.cb_is_open}, remaining_days={self.cb_remaining_days}, now_cbday={self.now_cbday}"
                            )

                        else:
                            msg_list.append(
                                f"クランバトル{self.now_cbday}日目が開催中です！\nみなさん頑張りましょう💪"
                            )
                            print(
                                f"定期実行: set_cbstatus: 初回起動_クラバト最終日: is_open={self.cb_is_open}, remaining_days={self.cb_remaining_days}, now_cbday={self.now_cbday}"
                            )

                    # BOT起動中に日付が変わって開催中になった場合
                    else:
                        self.now_cbday = now_cbday

                        # メッセージ追加
                        msg_list.append("みなさん頑張りましょう💪")

                        # ロールを付け替えInfoを追加
                        try:
                            await reset_attackrole(channel.guild)
                            info_msg_list.append("メンバー全員の凸報告ロールをリセットしました。")

                        # ロール付け替えに失敗した場合はエラー文を追加
                        except Exception as e:
                            error_msg_list.append(str(e))
                        print(
                            f"定期実行: set_cbstatus: クラバト日付進行: is_open={self.cb_is_open}, remaining_days={self.cb_remaining_days}, now_cbday={self.now_cbday}"
                        )

                # 開催中->非開催中
                elif (self.cb_is_open is True) and (cb_is_open is False):
                    self.cb_is_open = cb_is_open
                    self.cb_remaining_days = cb_remaining_days
                    self.now_cbday = now_cbday

                    # 終了メッセージのembed作成
                    embed = discord.Embed(title="🎉 クランバトルが終了しました 🎉", color=0x00FF00)

                    # メッセージ追加
                    msg_list.append("みなさんお疲れ様でした🍵")

                    # ロールを削除しInfoを追加
                    try:
                        await clear_attackrole(channel.guild)
                        info_msg_list.append("メンバー全員の凸報告ロールをリセットしました。")

                    # ロール付け替えに失敗した場合はエラー文を追加
                    except Exception as e:
                        error_msg_list.append(str(e))

                    # 凸管理シートリセット
                    try:
                        self.sheet.clear_all_attack()
                        info_msg_list.append("凸管理シートをリセットしました。")
                    # リセットに失敗した場合はエラー文を追加
                    except Exception as e:
                        error_msg_list.append(str(e))
                    print(
                        f"定期実行: set_cbstatus: クラバト終了: is_open={self.cb_is_open}, remaining_days={self.cb_remaining_days}, now_cbday={self.now_cbday}"
                    )

            # embedを設定してある場合は送信
            if embed is not None:
                # 各セクションセット
                if len(msg_list) > 0:
                    embed.add_field(
                        name="📝 メッセージ", value="\n".join(msg_list), inline=False
                    )
                if len(info_msg_list) > 0:
                    embed.add_field(
                        name="ℹ Info", value="\n".join(info_msg_list), inline=False
                    )
                if len(error_msg_list) > 0:
                    embed.add_field(
                        name="⚠ Error", value="\n".join(error_msg_list), inline=False
                    )

                await send_embed_message(self.bot, embed, channel=channel)
