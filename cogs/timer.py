import asyncio
from pathlib import Path

from discord.ext import commands
from discord.channel import VoiceChannel
from discord import FFmpegPCMAudio
import emoji

DIRECTORY = Path(__file__).parent.parent
FFMPEG = DIRECTORY / "ffmpeg" / "bin" / "ffmpeg.exe"


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
        # TODO: ボイスチャットにユーザーがいるなら音声で通知したい
        user = ctx.message.author
        if user.voice:
            await self.voice_notification(ctx, time)
        await self.text_notification(ctx, time)

    async def voice_notification(self, ctx, time):
        user = ctx.message.author
        # 接続
        voiceChannel = await VoiceChannel.connect(user.voice.channel)
        # 再生
        path = DIRECTORY / "clock.mp3"
        voiceChannel.play(
            FFmpegPCMAudio(str(path), executable=str(FFMPEG)),
        )
        # 切断
        # もっと時間置いて切断でも良い
        while voiceChannel.is_playing():
            await asyncio.sleep(1)
        await voiceChannel.disconnect()

    async def text_notification(self, ctx, time):
        user = ctx.message.author
        message = await ctx.send(f"{user.mention} {time}秒タイマーが終了しました")
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
