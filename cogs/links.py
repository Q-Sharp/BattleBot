import discord
from discord.ext import commands
import asyncio

class WikiLinks(commands.Cog):
    """
    Anything relating to the Battle Legion wiki.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wiki",invoke_without_command=True)
    async def wiki(self,ctx,page:str=None):
        """
        Links a specifed page of the wiki.
        """
        await ctx.send(f"https://battlelegion.wiki/{page}")
        
def setup(bot):
    bot.add_cog(WikiLinks(bot))
