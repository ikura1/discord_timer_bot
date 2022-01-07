import asyncio

from discord.ext import commands
import emoji


class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        brief="This is the brief description",
        description="This is the full description",
    )
    async def timer(self, ctx, time: str = None):
        await asyncio.sleep(int(time))
        # TODO: 経過時間の表示したいなー
        user = ctx.message.author
        # TODO: ボイスチャットにユーザーがいるなら音声で通知したい
        message = await ctx.send(f"{user.mention} {time}秒が経過しました")
        check = emoji.emojize(":check_mark:", use_aliases=True)
        x = emoji.emojize(":x:", use_aliases=True)
        await message.add_reaction(check)
        await message.add_reaction(x)
        # TODO: 再実行したい気持ち
        # TODO: リアクションを選択された場合、別々の動作
        # TODO: checkは再実行
        # TODO: xはリアクションの削除


def setup(bot):
    bot.add_cog(Timer(bot))
