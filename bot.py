import datetime
import os
from pathlib import Path
import traceback

from discord.ext import commands, tasks

INITIAL_EXTZENSIONS = ["cogs.timer"]
ICON = "clock_{hour:02}{minute:02}.png"
# TODO: 時間帯でアイコン画像の変更


class Bot(commands.Bot):
    def __init__(self, command_prefix):
        super(Bot, self).__init__(command_prefix=command_prefix)

        for cog in INITIAL_EXTZENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    # FIXME: 開始時刻によっては変更が遅れてしまう
    @tasks.loop(minutes=30)
    async def change_icon(self):
        JST = datetime.timezone(datetime.timedelta(hours=+9), "JST")
        now = datetime.datetime.now(JST)
        hour = 12 if now.hour > 12 else 0
        minute = now.minute - (30 if now.minute > 30 else 0)
        now += datetime.timedelta(hours=-hour, minutes=-minute)

        icon_name = ICON.format(hour=now.hour, minute=now.minute)
        icon_path = Path(__file__).parent / "images" / icon_name
        self.set_image_icon(icon_path)

    async def set_image_icon(self, path):
        with path.open("rb") as f:
            await self.user.edit(avatar=f.read())


if __name__ == "__main__":
    bot = Bot(command_prefix="/")
    api_token = os.environ["DISCORD_API_TOKEN"]
    bot.run(api_token)
