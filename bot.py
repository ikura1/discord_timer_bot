import os
import traceback

from discord.ext import commands

INITIAL_EXTZENSIONS = ["cogs.timer"]

# TODO: 時間帯でアイコン画像の変更


class Bot(commands.Bot):
    def __init__(self, command_prefix):
        super(Bot, self).__init__(command_prefix=command_prefix)

        for cog in INITIAL_EXTZENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()


if __name__ == "__main__":
    bot = Bot(command_prefix="/")
    api_token = os.environ["DISCORD_API_TOKEN"]
    bot.run(api_token)
