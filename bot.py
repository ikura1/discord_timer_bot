import asyncio
import os


import discord
from discord.ext import commands
import emoji


bot = commands.Bot(command_prefix="/")


@bot.command(
    brief="This is the brief description", description="This is the full description"
)
async def ping(ctx, time: str):
    await asyncio.sleep(int(time))
    # TODO: 発言者ヘのメンションにする
    # TODO: メッセージをいいかんじにする
    user = ctx.message.author
    message = await ctx.send(f"{user.mention} {time}秒が経過しました")
    check = emoji.emojize(":check_mark:", use_aliases=True)
    x = emoji.emojize(":x:", use_aliases=True)
    await message.add_reaction(check)
    await message.add_reaction(x)
    # TODO: 再実行したい気持ち
    # TODO: リアクションを選択された場合、別々の動作
    # TODO: checkは再実行
    # TODO: xはリアクションの削除


api_token = os.environ["DISCORD_API_TOKEN"]
bot.run(api_token)
