import discord
from discord.ext import commands
import asyncio
from data.data_handler import data_handler

class Subscriptions(commands.Cog):

    # Initialises the variables and sets the bot.
    def __init__(self, bot):
        self.bot = bot

    # Our base level command. Due to invoke_without_command=True it means that this command is only run when no
    # sub-command is run. Makes it a command group with a name.
    @commands.group(name='subscription', aliases = ['sub'])
    # Defines it as a function.
    async def subsciptions(self, ctx):
        await ctx.send("Lol")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        subs = data_handler.load("subscriptions")
        channels = list(subs["Subscriptions"].values())
        if ctx.channel.id in channels:
            for channelID in list(subs["Subscribers"][str(ctx.channel.id)]):
                channel = self.bot.get_channel(channelID)
                # Format better to include all content (embeds and images)
                if ctx.is_system():
                    message = f">>> {ctx.system_content}"
                elif ctx.content == "":
                    message = f"**{ctx.author.name}#{ctx.author.discriminator}:**\n"
                else:
                    message = f"**{ctx.author.name}#{ctx.author.discriminator}:**\n>>> {ctx.content}"
                if len(ctx.embeds) == 0:
                    embed = None
                else:
                    embed = ctx.embeds[0]
                files = []
                for file in ctx.attachments:
                    theFile = await file.to_file()
                    files.append(theFile)
                if files == []:
                    files = None
                
                await channel.send(message, embed=embed, files = files)

def setup(bot):
    bot.add_cog(Subscriptions(bot))