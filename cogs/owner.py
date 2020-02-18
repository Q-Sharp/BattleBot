import asyncio
from asyncio.subprocess import PIPE, STDOUT

import discord
from discord.ext import commands
from data.data_handler import data_handler

class Owner(commands.Cog):
    """
    Owner only commands
    """
    def __init__(self, bot):
        self.bot = bot
        
    # Defines this as a command.
    # Marked as hidden so it doesn't appear on the help command.
    @commands.command(hidden=True)
    # Checks the author is an owner
    @commands.is_owner()
    async def load(self, ctx, ext):
        """
        Loads an extention.
        """
        try:
            self.bot.load_extension(ext)
        except Exception as e:
            await ctx.send(f"Error:\n```fix\n{type(e).__name__}: {e}\n```")
        else:
            await ctx.send("\N{WHITE HEAVY CHECK MARK}")

    # Defines this as a command.
    # Marked as hidden so it doesn't appear on the help command.
    @commands.command(hidden=True)
    # Checks the author is an owner
    @commands.is_owner()
    async def unload(self, ctx, ext):
        """
        Unloads an extention.
        """
        try:
            self.bot.unload_extension(ext)
        except Exception as e:
            await ctx.send(f"Error:\n```fix\n{type(e).__name__}: {e}\n```")
        else:
            await ctx.send("\N{WHITE HEAVY CHECK MARK}")

    # Defines this as a command.
    # Marked as hidden so it doesn't appear on the help command.
    @commands.command(aliases=["rl"],hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, ext):
        """
        Reloads an extention.
        """
        try:
            self.bot.reload_extension(ext)
        except Exception as e:
            await ctx.send(f"Error:\n```fix\n{type(e).__name__}: {e}\n```")
        else:
            await ctx.send("\N{WHITE HEAVY CHECK MARK}")

    @commands.command(aliases=["die"],hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        """
        Shuts the bot down.
        """
        # give shutdown command via cmd
        # temp via file
        open("shutdown", "a").close()
        await ctx.send("Bye")
        await self.bot.close()

    @commands.command(aliases=['pull'],hidden=True)
    @commands.is_owner()
    async def update(self, ctx):
        """
        Pulls files from github.
        """
        async with ctx.typing():
            p = await asyncio.create_subprocess_shell(
                "git pull",
                stdin=PIPE,
                stdout=PIPE,
                stderr=STDOUT
            )
            stdout, stderr = await p.communicate()
            code = p.returncode

            if stdout:
                stdout = stdout.decode("utf-8")
            if stderr:
                stderr = stderr.decode("utf-8")

            if stderr:
                out = f"stdout:\n{stdout}\nstderr:\n{stderr}\n\nReturn code: {code}"
            else:
                out = stdout
                if not code:
                    out = f"stdout:\n{stdout}\nstderr:\n{stderr}\n\nReturn code: {code}"

            await ctx.send(out)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def restart(self, ctx):
        """
        Restarts the bot and pulls from github.
        """
        await ctx.send("Restarting...")
        await self.bot.close()

    @commands.command(aliases=["status"],hidden=True)
    @commands.is_owner()
    async def ChangingPresence(self,ctx,activityType,*,activityName):
        """
        Changes the bot presence
        """
        await ctx.message.delete()
        # Check docs for help on this command
        await self.bot.change_presence(activity=discord.Activity(name=activityName,
                                                        type=activityType))

    @commands.command('spacer',hidden=True)
    @commands.is_owner()
    async def Test(self,ctx):
        """
        Prints a spacer/line into the console to help with debugging.
        """
        print("--------------------------------------------------")

    @commands.command('users',hidden=True)
    @commands.is_owner()
    async def Users(self,ctx):
        "Lists the amount of users the bot can see."
        await ctx.send(len(self.bot.users))

    @commands.command('profiles',hidden=True)
    @commands.is_owner()
    async def LenProfiles(self,ctx):
        "Lists the amount of people who have a profile. aka the people who have spoken when the bot can see their messages."
        await ctx.send(len(data_handler.load("profiles")))

def setup(bot):
    bot.add_cog(Owner(bot))
