import discord
from discord.ext import commands, tasks
import load_settings
BOT_MANAGER_ROLE = load_settings.BOT_MANAGER_ROLE


def is_have_botmanager_role(ctx):
    if BOT_MANAGER_ROLE in [r.id for r in ctx.message.author.roles]:
        return True
    else:
        False


#def get_message_channel(bot,message):
#    """
#    メッセージを受信したchannelを返す。
#    ctxと同じように扱える。（多分
#    """
#    return bot.get_channel(message.channel.id)


async def send_success_message(bot, embed, ctx=None, message=None):
    """
    成功メッセージを送信する。

    bot
    ctx(message.channel)

        embed = discord.Embed(
            title="✅ 登録完了",
            description="メッセージ内容",
            color=0x00ff00)
    """
    if (ctx is not None) and (message is not None):
        raise Exception("ctxとmessageが両方指定されています。")

    elif ctx is not None:
        embed.set_footer(text=bot.user.display_name,
                         icon_url=bot.user.avatar_url)
        embed.set_author(name=ctx.message.content)
        await ctx.send(embed=embed)

    elif message is not None:
        embed.set_footer(text=bot.user.display_name,
                         icon_url=bot.user.avatar_url)
        embed.set_author(name=message.content)
        await message.channel.send(embed=embed)

    else:
        raise Exception("ctxとmessageがどちらも指定されていません。")

async def send_error_message(bot, text, ctx=None, message=None):
    if (ctx is not None) and (message is not None):
        raise Exception("ctxとmessageが両方指定されています。")
    elif ctx is not None:
        embed = discord.Embed(title="❎ エラー", description=text, color=0xff0000)
        embed.set_footer(text=bot.user.display_name,
                         icon_url=bot.user.avatar_url)
        embed.set_author(name=ctx.message.content)
        await ctx.send(embed=embed)
    elif message is not None:
        embed = discord.Embed(title="❎ エラー", description=text, color=0xff0000)
        embed.set_footer(text=bot.user.display_name,
                         icon_url=bot.user.avatar_url)
        embed.set_author(name=message.content)
        await message.channel.send(embed=embed)
    else:
        raise Exception("ctxとmessageがどちらも指定されていません。")

async def send_botmanager_role_error(bot, ctx=None, message=None):

    if (ctx is not None) and (message is not None):
        raise Exception("ctxとmessageが両方指定されています。")
    elif ctx is not None:
        await send_error_message(
            bot,
            f"{discord.utils.get(ctx.message.guild.roles, id=BOT_MANAGER_ROLE).name}ロールを持つメンバー以外はこのコマンドは使用できません。",
            ctx=ctx)
    elif message is not None:
        await send_error_message(
            bot,
            f"{discord.utils.get(ctx.message.guild.roles, id=BOT_MANAGER_ROLE).name}ロールを持つメンバー以外はこのコマンドは使用できません。",
            message=message)
    else:
        raise Exception("ctxとmessageがどちらも指定されていません。")


async def set_role(bot,rolename,ctx=None,message=None):
    if (ctx is not None) and (message is not None):
        raise Exception("ctxとmessageが両方指定されています。")
    elif ctx is not None:
        member = ctx.guild.get_member(ctx.author.id)
        role = discord.utils.find(lambda r: r.name == rolename,
                                           ctx.guild.roles)
        if role is None:
            msg=f"`{rolename}`というロールが見つかりません。"
            await send_error_message(bot, msg, ctx=ctx)
        else:
            await member.add_roles(role)

    elif message is not None:
        member = message.guild.get_member(message.author.id)
        role = discord.utils.find(lambda r: r.name == rolename,
                                           message.guild.roles)
        print(role)
        if role is None:
            msg=f"`{rolename}`というロールが見つかりません。"
            await send_error_message(bot, msg, message=message)
        else:
            await member.add_roles(role)
    else:
        raise Exception("ctxとmessageがどちらも指定されていません。")





async def unset_role(bot,rolename,ctx=None,message=None):
    if (ctx is not None) and (message is not None):
        raise Exception("ctxとmessageが両方指定されています。")
    elif ctx is not None:
        member = ctx.guild.get_member(ctx.author.id)
        role = discord.utils.find(lambda r: r.name == rolename,
                                           ctx.guild.roles)
        if role is None:
            msg=f"`{rolename}`というロールが見つかりません。"
            await send_error_message(bot, msg, ctx=ctx)
        else:
            await member.remove_roles(role)

    elif message is not None:
        member = message.guild.get_member(message.author.id)
        role = discord.utils.find(lambda r: r.name == rolename,
                                           message.guild.roles)
        if role is None:
            msg=f"`{rolename}`というロールが見つかりません。"
            await send_error_message(bot, msg, message=message)
        else:
            await member.remove_roles(role)
    else:
        raise Exception("ctxとmessageがどちらも指定されていません。")



