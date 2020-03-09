import asyncio
import pickle
import sys
import traceback
import asyncpg

import discord
from discord.ext import commands

class BattleBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=self._get_prefix,
            description="A bot for Battle Legion."
        )
        # Replace with your own ID if you're testing.
        self.owner_ids = [
            270190067354435584, # Green
            224958921993879552, # Flaming
            301764235887902727 # QoO
            ]
        self.initial_extensions = ["cogs.clans",
                                   "cogs.error_handler",
                                   "cogs.info",
                                   "cogs.joinleave",
                                   "cogs.links",
                                   "cogs.misc",
                                   "cogs.modlog",
                                   "cogs.options",
                                   "cogs.owner",
                                   "cogs.profiles",
                                   "cogs.servers",
                                   "cogs.subscriptions"]
            
        self.load_exts()

    def _get_prefix(self, bot, message):
        if not message.guild:
            return []
        else:
            prefix = ['b!','B!']

        return commands.when_mentioned_or(*prefix)(bot, message)

    def load_exts(self):
        for extension in self.initial_extensions:
            try:
                self.load_extension(extension)
                print(f"Successfully loaded extension - {extension}")
            except Exception:
                print(
                    f"Failed to load extension - {extension}", file=sys.stderr)
                traceback.print_exc()

    async def is_owner(self, user):
        return user.id in self.owner_ids

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(name="with my setup", type=discord.ActivityType.playing))

        print(f"\n\nLogged in as: {self.user.name} - {self.user.id}")
        print(f"Version: {discord.__version__}\n")

    def run(self):
        print("Connecting to discordapp")
        with open("tooken.data", "rb") as f:
            tooken = pickle.load(f)
        super().run(tooken, bot=True, reconnect=True)

if __name__ == "__main__":
    if "win" in sys.platform:
        asyncio.set_event_loop(asyncio.ProactorEventLoop())

    BattleBot().run()
