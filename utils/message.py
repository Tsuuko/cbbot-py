import discord
from discord.ext import commands
from utils.constants import EmbedColor


class Embed:
    @staticmethod
    async def send_info(ctx: commands.Context, title: str, description: str, author_name: str):
        embed = discord.Embed(title=title, description=description, color=EmbedColor.INFO)
        embed.set_author(name=author_name)
        await Embed._send(ctx, embed)

    @staticmethod
    async def send_success(ctx: commands.Context, title: str, description: str, author_name: str):
        embed = discord.Embed(title=title, description=description, color=EmbedColor.SUCCESS)
        embed.set_author(name=author_name)
        await Embed._send(ctx, embed)

    @staticmethod
    async def send_warn(ctx: commands.Context, title: str, description: str, author_name: str):
        embed = discord.Embed(title=title, description=description, color=EmbedColor.WARN)
        embed.set_author(name=author_name)
        await Embed._send(ctx, embed)

    @staticmethod
    async def send_error(ctx: commands.Context, title: str, description: str, author_name: str):
        embed = discord.Embed(title=title, description=description, color=EmbedColor.ERROR)
        embed.set_author(name=author_name)
        await Embed._send(ctx, embed)

    @staticmethod
    async def _send(ctx: commands.Context, embed: discord.Embed):
        await ctx.send(embed=embed)
