from discord.ext import commands
from datetime import datetime
import discord
import clanbattle_manager


class clanbattle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheet = clanbattle_manager.spreadsheet()

    @commands.command(name='regist')
    async def cmd_regist(self, ctx, *args):
        if len(args) == 0:
            try:
                result = self.sheet.add_user(ctx.author.display_name)
                embed = discord.Embed(
                    title="✅ 登録完了",
                    description=
                    f"[ **{ctx.author.display_name}** さんを{result}行目に登録しました。 ]",
                    color=0x00ff00)
                embed.set_footer(text=self.bot.user.display_name,
                                 icon_url=self.bot.user.avatar_url)

            except Exception as e:
                embed = discord.Embed(title="❎ エラー",
                                      description=(str(e)),
                                      color=0xff0000)
                embed.set_footer(text=self.bot.user.display_name,
                                 icon_url=self.bot.user.avatar_url)

        elif len(args) == 2 and args[0] == "-u":
            try:
                result = self.sheet.add_user(args[1])
                embed = discord.Embed(
                    title="✅ 登録完了",
                    description=
                    f"[ **{args[1]}** さんを{result}行目に登録しました。 ]",
                    color=0x00ff00)
                embed.set_footer(text=self.bot.user.display_name,
                                 icon_url=self.bot.user.avatar_url)
            except Exception as e:
                embed = discord.Embed(title="❎ エラー",
                                      description=str(e),
                                      color=0xff0000)
                embed.set_footer(text=self.bot.user.display_name,
                                 icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name='status')
    async def cmd_getstatus(self, ctx):
        status = clanbattle_manager.fetch_status()
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

    @commands.command(name='setstatus')
    async def cmd_setstatus(self, ctx):
        pass
