# Allows us to use d.py
import discord
from discord.ext import commands
import asyncio
# Allows us to randomise things
import random
# Allows us to manipulate time
import time
# Used when calculating times from discord
import datetime
from data.data_handler import data_handler

# Our cog for joining and leaving
class JoinLeaveMessages(commands.Cog):
    def __init__(self,bot):
        # Allows us to reference the bot
        self.bot = bot

    # Marks this function as a listener
    @commands.Cog.listener()
    # Creates the listener function.
    # Parameters as per d.py
    async def on_member_join(self,member):
        # Gets the clan data
        servers = data_handler.Load("clans")
        
        # Find the channel id
        try:
            channel = servers[str(member.guild.id)]['Messages']['joinChannel']
        # If it can't find a channel, don't do anything
        except KeyError:
            return

        # Makes sure the server has at least one message
        if len(servers[str(member.guild.id)]['Messages']['joinMessages']) <= 0:
            return
        # Selects a random join message
        joinName, joinMessage = random.choice(list(servers[str(member.guild.id)]['Messages']['joinMessages'].items()))

        # Formats the joinMessage with the placeholders
        joinMessage = joinMessage.replace("{join.name}",f"{member.name}#{member.discriminator}")
        try:
            joinMessage = joinMessage.replace("{join.mention}",f"{member.mention}")
        except KeyError:
            pass
        try:
            joinMessage = joinMessage.replace("{join.creationDate}",f"{member.created_at.ctime()} ({int(int(time.time() - (member.created_at - datetime.datetime.utcfromtimestamp(0)).total_seconds())/86400)} days ago)") # Turns datetime to time to make it easier to deal with.
        except KeyError:
            pass
        # Creates a join position
        try:
            # Creates a list for the guild member's join dates
            join_dates = []
            # Goes through the guild's members and get's their join date
            for user in member.guild.members:
                join_dates.append(user.joined_at)
            # Sorts the join dates
            def get_key(item):
                return item
            join_dates = sorted(join_dates,reverse=False,key=get_key)
            # Set's the join message (by finding the index of the user's join date from the sorted list)
            joinMessage = joinMessage.replace("{join.position}",f"{join_dates.index(member.joined_at)+1}")
        except KeyError:
            pass

        # Attempts to send the message
        try:
            await member.guild.get_channel(channel).send(joinMessage)
        except AttributeError:
            return
        # Can't send the messages (lacks permission/slowmode)
        except discord.Forbidden:
            return

    # Marks the function as a listener
    @commands.Cog.listener()
    # Defines the listener
    # Parameters as per d.py
    async def on_member_leave(self,member):
        # Gets the clan data
        servers = data_handler.Load("clans")
        
        # Find the channel id
        try:
            channel = servers[str(member.guild.id)]['Messages']['leaveChannel']
        except KeyError:
            return
        
        # Selects a random leave message
        if len(servers[str(member.guild.id)]['Messages']['leaveMessages']) <= 0:
            return
        leaveName, leaveMessage = random.choice(list(servers[str(member.guild.id)]['Messages']['leaveMessages'].items()))

        # Formats the leaveMessage with the placeholders
        try:
            leaveMessage = leaveMessage.replace("{leave.name}", f"{member.name}#{member.discriminator}")
        except KeyError:
            pass
        try:
            leaveMessage = leaveMessage.replace("{leave.creationDate}", f"{member.created_at.ctime()} ({int(int(time.time() - (member.created_at - datetime.datetime.utcfromtimestamp(0)).total_seconds())/86400)} days ago)")
        except KeyError:
            pass
        try:
            leaveMessage = leaveMessage.replace("{leave.joinDate}", f"{member.joined_at.ctime()} ({int(int(time.time() - (member.joined_at - datetime.datetime.utcfromtimestamp(0)).total_seconds())/86400)} days ago)")
        except KeyError:
            pass
        # Creates a join position
        try:
            join_dates = []
            for user in member.guild.members:
                join_dates.append(user.joined_at)
            def get_key(item):
                return item
            join_dates = sorted(join_dates,reverse=False,key=get_key)
            leaveMessage = leaveMessage.replace("{leave.position}", f"{join_dates.index(member.joined_at)+1}")
        except KeyError:
            pass

        # Attempts to send the message
        await member.guild.get_channel(channel).send(leaveMessage)

# Sets up the cog. Called when loading the file
def setup(bot):
    bot.add_cog(JoinLeaveMessages(bot))
