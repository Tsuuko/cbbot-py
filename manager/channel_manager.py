import discord
from discord.ext import commands, tasks
import load_settings
BOT_MANAGER_ROLE = load_settings.BOT_MANAGER_ROLE


def is_have_botmanager_role(author):
    """
    BOT_MANAGER_ROLEを持っているか確認する

    params
    ----
    ```
    author:discord.Message.author # ctx.authorとかmessage.authorとか
    ```

    return
    ----
    - 持っている場合：`True`
    - 持っていない場合：`False`
    """
    if BOT_MANAGER_ROLE in [r.id for r in author.roles]:
        return True
    else:
        False


async def send_embed_message(bot, embed,plain_text=None, ctx=None, message=None, channel=None):
    """
    成功メッセージを送信する。

    params
    ----
    ```
    bot:discord.ext.commands.Bot # このプログラムの場合は大体self.bot
    embed:discord.Embed # タイトル、本文、色を設定したembed
    # ex
    embed = discord.Embed(
        title="✅ 登録完了",
        description="メッセージ内容",
        color=0x00ff00)
    ```
    ### Option
    ```
    plain_text:str # embedの前に追加するテキスト（author.mentionを渡すとメンションできる）
    ```

    ### Select (どれか1つ)
    ```
    ctx:discord.ext.commands.Context
    message:discord.Message
    channel:discord.TextChannel # channelの場合はコマンドの表示なし
    ```

    return
    ----
    ```
    None
    ```
    """
    if [ctx,message,channel].count(None)<2:
        print([ctx,message,channel].count(None))
        raise Exception("パラメータが複数指定されています。")

    elif ctx is not None:
        embed.set_footer(text=bot.user.display_name,
                         icon_url=bot.user.avatar_url)
        embed.set_author(name=ctx.message.content)
        if plain_text is not None:
            await ctx.send(plain_text,embed=embed)
        else:
            await ctx.send(embed=embed)

    elif message is not None:
        embed.set_footer(text=bot.user.display_name,
                         icon_url=bot.user.avatar_url)
        embed.set_author(name=message.content)
        if plain_text is not None:
            await message.channel.send(plain_text,embed=embed)
        else:
            await message.channel.send(embed=embed)

    elif channel is not None:
        embed.set_footer(text=bot.user.display_name,
                         icon_url=bot.user.avatar_url)
        if plain_text is not None:
            await channel.send(plain_text,embed=embed)
        else:
            await channel.send(embed=embed)
    else:
        raise Exception("パラメータが指定されていません。")


async def send_error_message(bot, text,plain_text=None, ctx=None, message=None):
    """
    エラーメッセージを送信する。

    params
    ----
    ```
    bot:discord.ext.commands.Bot # このプログラムの場合は大体self.bot

    ```
    ### Option
    ```
    plain_text:str # embedの前に追加するテキスト（author.mentionを渡すとメンションできる）
    ```

    ### Select (どれか1つ)
    ```
    ctx:discord.ext.commands.Context
    message:discord.Message
    ```

    return
    ----
    ```
    None
    ```
    """

    if (ctx is not None) and (message is not None):
        raise Exception("ctxとmessageが両方指定されています。")
    else:
        embed = discord.Embed(title="⚠ エラー", description=text, color=0xff0000)
        embed.set_footer(text=bot.user.display_name,
                         icon_url=bot.user.avatar_url)
        if ctx is not None:
            embed.set_author(name=ctx.message.content)
            if plain_text is not None:
                await ctx.send(plain_text,embed=embed)
            else:
                await ctx.send(embed=embed)
        elif message is not None:
            embed.set_author(name=message.content)
            if plain_text is not None:
                await message.channel.send(plain_text,embed=embed)
            else:
                await message.channel.send(embed=embed)
        else:
            raise Exception("ctxとmessageがどちらも指定されていません。")


async def send_botmanager_role_error(bot,plain_text=None, ctx=None, message=None):
    """
    BOT_MANAGER_ROLEエラーメッセージを送信する。

    params
    ----
    ```
    bot:discord.ext.commands.Bot # このプログラムの場合は大体self.bot

    ```
    ### Option
    ```
    plain_text:str # embedの前に追加するテキスト（author.mentionを渡すとメンションできる）
    ```

    ### Select (どれか1つ)
    ```
    ctx:discord.ext.commands.Context
    message:discord.Message
    ```

    return
    ----
    ```
    None
    ```
    """
    if (ctx is not None) and (message is not None):
        raise Exception("ctxとmessageが両方指定されています。")
    elif ctx is not None:
        msg=f"`{discord.utils.get(ctx.message.guild.roles, id=BOT_MANAGER_ROLE).name}`ロールを持つメンバー以外はこのコマンドは使用できません。"
        if plain_text is not None:
            await send_error_message(bot,msg,plain_text=plain_text,ctx=ctx)
        else:
            await send_error_message(bot,msg,ctx=ctx)


    elif message is not None:
        msg=f"`{discord.utils.get(message.guild.roles, id=BOT_MANAGER_ROLE).name}`ロールを持つメンバー以外はこのコマンドは使用できません。"

        if plain_text is not None:
            await send_error_message(bot,msg,plain_text=plain_text,message=message)
        else:
            await send_error_message(bot,msg,message=message)

    else:
        raise Exception("ctxとmessageがどちらも指定されていません。")


async def set_role(bot, rolename, ctx=None, message=None):
    """
    ロールをセットする。

    params
    ----
    ```
    bot:discord.ext.commands.Bot # このプログラムの場合は大体self.bot
    rolename:str # セットするロール名
    ```
    ### Select (どれか1つ)
    ```
    ctx:discord.ext.commands.Context
    message:discord.Message
    ```

    return
    ----
    ```
    None
    ```
    """
    if (ctx is not None) and (message is not None):
        raise Exception("ctxとmessageが両方指定されています。")
    elif ctx is not None:
        member = ctx.guild.get_member(ctx.author.id)
        role = discord.utils.find(lambda r: r.name == rolename,
                                  ctx.guild.roles)
        if role is None:
            msg = f"`{rolename}`というロールが見つかりません。"
            await send_error_message(bot, msg, ctx=ctx)
        else:
            await member.add_roles(role)

    elif message is not None:
        member = message.guild.get_member(message.author.id)
        role = discord.utils.find(lambda r: r.name == rolename,
                                  message.guild.roles)
        print(role)
        if role is None:
            msg = f"`{rolename}`というロールが見つかりません。"
            await send_error_message(bot, msg, message=message)
        else:
            await member.add_roles(role)
    else:
        raise Exception("ctxとmessageがどちらも指定されていません。")

async def unset_role(bot, rolename, ctx=None, message=None):
    """
    ロールを外す。

    params
    ----
    ```
    bot:discord.ext.commands.Bot # このプログラムの場合は大体self.bot
    rolename:str # 外すロール名
    ```
    ### Select (どれか1つ)
    ```
    ctx:discord.ext.commands.Context
    message:discord.Message
    ```

    return
    ----
    ```
    None
    ```
    """
    if (ctx is not None) and (message is not None):
        raise Exception("ctxとmessageが両方指定されています。")
    elif ctx is not None:
        member = ctx.guild.get_member(ctx.author.id)
        role = discord.utils.find(lambda r: r.name == rolename,
                                  ctx.guild.roles)
        if role is None:
            msg = f"`{rolename}`というロールが見つかりません。"
            await send_error_message(bot, msg, ctx=ctx)
        else:
            await member.remove_roles(role)

    elif message is not None:
        member = message.guild.get_member(message.author.id)
        role = discord.utils.find(lambda r: r.name == rolename,
                                  message.guild.roles)
        if role is None:
            msg = f"`{rolename}`というロールが見つかりません。"
            await send_error_message(bot, msg, message=message)
        else:
            await member.remove_roles(role)
    else:
        raise Exception("ctxとmessageがどちらも指定されていません。")

async def reset_attackrole(guild):
    """
    全員の凸登録ロールをリセットする。

    params
    ----
    ```
    guild:discord.Guild # ctx.guildやmessage.guildなど
    ```

    return
    ----
    ```
    None
    ```
    """
    attacked_role = discord.utils.find(lambda r: r.name == "凸報告済",
                                       guild.roles)
    no_attack_role = discord.utils.find(lambda r: r.name == "凸未報告",
                                        guild.roles)
    msg = ""
    if (attacked_role is None) or (no_attack_role is None):
        if attacked_role is None:
            msg += "`凸報告済`という名前のロールが見つかりません。"
        if no_attack_role is None:
            if len(msg) > 0:
                msg += "\n"
            msg += "`凸未報告`という名前のロールが見つかりません。"
        raise Exception(msg)
    else:
        for member in guild.members:
            if not member.bot:
                await member.add_roles(no_attack_role)
                await member.remove_roles(attacked_role)

async def clear_attackrole(guild):
    """
    全員の凸登録ロールを削除する。

    params
    ----
    ```
    guild:discord.Guild # ctx.guildやmessage.guildなど
    ```

    return
    ----
    ```
    None
    ```
    """
    attacked_role = discord.utils.find(lambda r: r.name == "凸報告済",
                                       guild.roles)
    no_attack_role = discord.utils.find(lambda r: r.name == "凸未報告",
                                        guild.roles)
    msg = ""
    if (attacked_role is None) or (no_attack_role is None):
        if attacked_role is None:
            msg += "`凸報告済`という名前のロールが見つかりません。"
        if no_attack_role is None:
            if len(msg) > 0:
                msg += "\n"
            msg += "`凸未報告`という名前のロールが見つかりません。"
        raise Exception(msg)
    else:
        for member in guild.members:
            if not member.bot:
                await member.remove_roles(no_attack_role)
                await member.remove_roles(attacked_role)
