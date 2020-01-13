import traceback
import sys
from discord.ext import commands
import discord
from discord.ext.commands.cooldowns import BucketType
import cogs.checks as chec
import pickle

"""
If you are not using this inside a cog, add the event decorator e.g:
@bot.event
async def on_command_error(ctx, error)

For examples of cogs see:
Rewrite:
https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
Async:
https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5

This example uses @rewrite version of the lib. For the async version of the lib, simply swap the places of ctx, and error.
e.g: on_command_error(self, error, ctx)

For a list of exceptions:
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#errors
"""


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        # This prevents any commands with local handlers being handled here in on_command_error.
        #if hasattr(ctx.command, 'on_error'):
        #    return

        ignored = (commands.CommandNotFound)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            await ctx.send(f"`{error}`")
            return

        elif isinstance(error, commands.UserInputError):
            return await ctx.send(f"```fix\nERROR:\n{error}\n```")

        #Checks if it's disabled
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'`{ctx.prefix}{ctx.command}` has been disabled.')

        #Private messages check
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f"`{ctx.prefix}{ctx.command}` can't be used in Private Messages.")
            except:
                pass

        #Cooldown check
        elif isinstance(error, commands.errors.CommandOnCooldown):
            seconds = error.retry_after
            seconds = round(seconds, 2)
            hours, remainder = divmod(int(seconds), 3600)
            minutes, seconds = divmod(remainder, 60)
            return await ctx.send(
                f'**`{ctx.prefix}{ctx.command}` is on Cooldown:**\n'
                f'{minutes}m and {seconds}s remaining',
                delete_after=15)

        #Checks if server specific and in that server
        elif isinstance(error, chec.NotInServer):
            return await ctx.send(error.message)

        elif isinstance(error, chec.UserNoPermission):
            try:
                return await ctx.send(f"You don't have the required permission to run that command! Join the support server to learn more about permissions!")
            except:
                pass

        elif isinstance(error, chec.UserNotHighEnoughLevel):
            try:
                return await ctx.send(f"You aren't a high enough level to use that command! You need to be at least level {error.level}. You can gain more xp points by chatting!")
            except:
                pass

        elif isinstance(error, chec.ClanNotHighEnoughRank):
            try:
                return await ctx.send(f"Your clan doesn't have the required rank points to use that command! You can gain rank points by completing challenges and participating in events.")
            except:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                return await ctx.send('I could not find that member. Please try again.')

        elif isinstance(error, commands.CheckFailure):
            try:
                return await ctx.send(f"{ctx.author.mention}, you can't do that.")
            except:
                pass

        elif isinstance(error, commands.MissingPermissions):
            try:
                return await ctx.send("You do not have the required permissions to do that.")
            except:
                pass

        # All other Errors not returned come here... And we can just print the default TraceBack.
        #try:
        await ctx.send(content='> Ignoring exception in command {}:'.format(ctx.command))
        etraceback = traceback.format_exception(type(error), error, error.__traceback__)
        await ctx.send(f"```{etraceback}```")
        #except:
        await ctx.send("Failed to send error")
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    """Below is an example of a Local Error Handler for our command do_repeat"""
    @commands.command(name='repeat', aliases=['mimic', 'copy'],hidden=True)
    @commands.cooldown(1,120.0,BucketType.user)
    async def do_repeat(self, ctx, *, inp: str):
        """A simple command which repeats your input!
        inp  : The input to be repeated"""

        await ctx.send(inp)

    @do_repeat.error
    @commands.Cog.listener()
    async def do_repeat_handler(self, ctx, error):
        """A local Error Handler for our command do_repeat.
        This will only listen for errors in do_repeat.

        The global on_command_error will still be invoked after."""

        # Check if our required argument inp is missing.
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'inp':
                await ctx.send("You forgot to give me input to repeat!")

    @commands.is_owner()
    @commands.command(name='error')
    async def causeError(self,ctx):
        await ctx.send(anError)

    @commands.is_owner()
    @commands.command(name="bot-ban")
    async def botBan(self, ctx, member:discord.Member=None):
        if member is None:
            await ctx.send("Please specify a member")
            return
        banned_users = pickle.load(open('data/bannedUsers.data', 'rb'))
        banned_users.append(member.id)
        pickle.dump(banned_users, open('data/bannedusers.data', 'wb'))

    @commands.is_owner()
    @commands.command(name="bot-pardon")
    async def botPardon(self, ctx, member:discord.Member=None):
        if member is None:
            await ctx.send("Please specify a member")
            return
        banned_users = pickle.load(open('data/bannedUsers.data', 'rb'))
        banned_users.remove(member.id)
        pickle.dump(banned_users, open('data/bannedusers.data', 'wb'))

    @commands.is_owner()
    @commands.command(name="reset-bans")
    async def resetBotBans(self, ctx):
        banned_users = []
        pickle.dump(banned_users, open('data/bannedusers.data', 'wb'))

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
