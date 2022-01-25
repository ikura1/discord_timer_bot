import datetime
import os
from pathlib import Path
import traceback

import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand

INITIAL_EXTZENSIONS = ["cogs.timer"]
ICON = "clock_{hour:02}{minute:02}.png"


guilds = [450975581174235136]


class Bot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super(Bot, self).__init__(
            command_prefix=command_prefix, case_insensitive=True, intents=intents
        )
        slash = SlashCommand(self, sync_commands=True)
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
    intents = discord.Intents.all()
    intents.typing = False
    intents.members = False
    intents.presences = False

    bot = Bot(command_prefix="/", intents=intents)
    # slash = SlashCommand(bot, override_type=True)
    api_token = os.environ["DISCORD_API_TOKEN"]
    bot.run(api_token)
