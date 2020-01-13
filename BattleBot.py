import asyncio
import pickle
import sys
import traceback
import asyncpg

import discord
from discord.ext import commands

"""
async def run():
    description = "A bot written in Python that uses asyncpg to connect to a postgreSQL database."

    # NOTE: 127.0.0.1 is the loopback address. If your db is running on the same machine as the code, this address will work
    credentials = {"user": "BattleBot", "password": "Flaming_Feet7", "database": "BattleBot", "host": "127.0.0.1"}
    db = await asyncpg.create_pool(**credentials)

    # Example create table code, you'll probably change it to suit you
    await db.execute("CREATE TABLE IF NOT EXISTS users(id bigint PRIMARY KEY, data text);")

    bot = Bot(db=db)
    try:
        await bot.start(config.token)
    except KeyboardInterrupt:
        # Make sure to do these steps if you use a command to exit the bot
        await db.close()
        await bot.logout()
"""
class BattleBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=self._get_prefix,
            description="A bot for Battle Legion."
        )
        self.owner_ids = [
            270190067354435584, # Green
            224958921993879552, # Flaming
            ]
        self.initial_extensions = ["cogs.owner",
                                   "cogs.links",
                                   "cogs.info",
                                   "cogs.error_handler",
                                   'cogs.options',
                                   'cogs.modlog',
                                   'cogs.joinleave',
                                   'cogs.misc',
                                   'cogs.profiles',
                                   'cogs.clans']
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

#@bot.check
#async def block_banned_users(ctx):
#    banned_users = pickle.load(open('data/bannedUsers.data', 'rb'))
#    if ctx.author.id in banned_users:
#        return False

if __name__ == "__main__":
    if "win" in sys.platform:
        asyncio.set_event_loop(asyncio.ProactorEventLoop())

    BattleBot().run()
