import discord
from discord.ext import commands
import asyncio
import cogs.checks as check
from data.data_handler import data_handler

class ModLog(commands.Cog):
    """
    Allow per-server customisation of the bot!
    """
    def __init__(self,bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        servers = data_handler.Load("servers")
        try:
            if servers[str(message.guild.id)]['Modlog']['channel'] == None:
                return
        except KeyError:
            return
        embed = discord.Embed(description="Message Deleted.",
                              colour=discord.Color(0xef4b4b))

        embed.set_author(name=f"{message.author.name}#{message.author.discriminator}",icon_url=message.author.avatar_url_as(static_format='png'))
        
        embed.add_field(name="User",
                        value=f"{message.author.mention} ({message.author.id})")
        embed.add_field(name="Message ID",
                        value=message.id)
        embed.add_field(name="Channel",
                        value=f"{message.channel.mention} ({message.channel.id})")
        if message.content == "":
            message.content="`None`"
        elif len(message.content) > 1024:
            message.content = message.content[:1020] + "..."
        embed.add_field(name="Content",
                        value=message.content)
        channel = message.guild.get_channel(servers[str(message.guild.id)]['Modlog']['channel'])
        await channel.send(content="",embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self,before,after):
        #Checks modlogs are enabled.
        servers = data_handler.Load("servers")
        try:
            if servers[str(after.guild.id)]['Modlog']['channel'] == None:
                return
        except KeyError:
            return

        #Content Edited
        if before.content != after.content:
            embed = discord.Embed(description="Message Edited.",
                                  colour=discord.Color(0xffdd67))

            embed.set_author(name=f"{after.author.name}#{after.author.discriminator}",icon_url=after.author.avatar_url_as(static_format='png'))
            
            embed.add_field(name="User",
                            value=f"{after.author.mention} ({after.author.id})")
            embed.add_field(name="Message ID",
                            value=after.id)
            embed.add_field(name="Channel",
                            value=f"{after.channel.mention} ({after.channel.id})")
            if before.content == "":
                before.content="`None`"
            elif len(before.content) > 1024:
                before.content = before.content[:1020] + "..."
            embed.add_field(name="Before",
                            value=before.content)
            if after.content == "":
                after.content="`None`"
            elif len(after.content) > 1024:
                after.content = after.content[:1020] + "..."
            embed.add_field(name="After",
                            value=after.content)
            embed.add_field(name="Jump",
                            value=after.jump_url)
            channel = after.guild.get_channel(servers[str(after.guild.id)]['Modlog']['channel'])
            await channel.send(content="",embed=embed)

        #Message Pinned
        elif before.pinned != after.pinned:
            embed = discord.Embed(description="Message (Un)Pinned.",
                                  colour=discord.Color(0x7986c7))

            embed.set_author(name=f"{after.author.name}#{after.author.discriminator}",icon_url=after.author.avatar_url_as(static_format='png'))
            
            embed.add_field(name="User",
                            value=f"{after.author.mention} ({after.author.id})")
            embed.add_field(name="Message ID",
                            value=after.id)
            embed.add_field(name="Channel",
                            value=f"{after.channel.mention} ({after.channel.id})")
            if after.content == "":
                after.content="`None`"
            elif len(after.content) > 1024:
                after.content = after.content[:1020] + "..."
            embed.add_field(name="Content",
                            value=after.content)
            embed.add_field(name="Pinned",
                            value=after.pinned)
            channel = after.guild.get_channel(servers[str(after.guild.id)]['Modlog']['channel'])
            await channel.send(content="",embed=embed)

def setup(bot):
    bot.add_cog(ModLog(bot))
