import discord
from discord.ext import commands
import asyncio
import pickle
import cogs.checks as check
import random
import time
import datetime
from data.data_handler import data_handler

# Error on option select
class NotAnOption(commands.CheckFailure):
    pass

class Options(commands.Cog):
    """
    Allow per-server customisation of the bot!
    """
    def __init__(self,bot):
        self.bot = bot
        self.joinSelection = {}
        self.leaveSelection = {}
        self.temp = {}

    async def __error(self,ctx,error):
        if isinstance(error, NotAnOption):
            await ctx.send(error)
        else:
            pass
        
    @commands.group(name='options',invoke_without_command=True)
    async def options(self,ctx,option:str=None):
        """
        Use to check the current setting of any option.
        """
        clans = data_handler.Load("clans")
        profiles = data_handler.Load("profiles")
        if option == 'modlog':
            await ctx.send("Gotta work on some UI and check so there won't be any errors. Bear with me.")
        else:
            await ctx.send("No option selected. Valid options: \n`modlog` - moderation log settings.")

    @options.group(name='set',invoke_without_command=True)
    async def setOptions(self,ctx):
        """
        Use this to set the options of the server! Requires user rank 1 minimum.\nAn option may have certain requirements and be either be user or clan settings.
        """
        await ctx.send("You haven't specified a setting! Current settings avaliable: \n`modlog` - Specifies a channel to add a modlog to. Leave blank to turn off the modlog.")

    @commands.has_permissions(manage_channels=True)
    @setOptions.group(name='modlog',invoke_without_command=True)
    async def setModLog(self,ctx):
        """
        Settings for moderation logs. Requires manage channels permissions and a clan rank of one minimum.
        """
        await ctx.send("Please specify a setting. You can find the types in `b!help options set modlog.`")

    @commands.has_permissions(manage_channels=True)
    @setModLog.command(name='channel')
    async def setModLogChannel(self,ctx,channel:discord.TextChannel=None):
        """
        Sets the modlog to a certain channel or disables it. User must have manage channels permissions.
        """
        clans = data_handler.Load("clans")
        if channel != None:
            try:
                options = clans[ctx.guild.id]['options']
                try:
                    clans[ctx.guild.id]['options']['modlog']['channel'] = channel.id
                except KeyError:
                    clans[ctx.guild.id]['options']['modlog'] = {'channel':channel.id}
            except KeyError:
                clans[ctx.guild.id]['options'] = {'modlog':{'channel':channel.id}}
        else:
            try:
                clans[ctx.guild.id]['options']['modlog']['channel'] = None
            except KeyError:
                await ctx.send("You haven't enabled the moderation logs yet. No need to disable them!")
        pickle.dump(clans,open('data/clans.data','wb'))
        if channel != None:
            await ctx.send(f"Moderation logs now sent to {channel.mention}.")
            return
        await ctx.send("Moderation logs disabled.")

    @setOptions.group(name='levels',invoke_without_command=True)
    async def setLevels(self,ctx):
        """
        Options for user and clan notifications
        """
        await ctx.send("Please select user or clan")

    @setLevels.command(name='user')
    async def setLevelsUser(self,ctx,setting:str=None):
        """
        Setting for per-user rankup messages. They can also be disabled per server as well.
        """
        profiles = data_handler.Load("profiles")
        settings = ['any','dm','disabled']
        if setting not in settings:
            setting = None
        if setting is None:
            await ctx.send("""Please select a valid setting:
\n`any` - Tries to send it in the channel where you earned that rankup. Otherwise sends it via dm.
\n`dm` - Sends it via DM. Unless a clan channel is set.
\n`disabled` - No rank up messages.
""")
            return
        try:
            options = profiles[ctx.author.id]['options']
        except KeyError:
            profiles[ctx.author.id]['options'] = {'levels':"any"}
        if setting.lower() == "disable" or setting.lower() == "disabled":
            profiles[ctx.author.id]['options']['levels'] = "disabled"
        elif setting.lower() == "any":
            profiles[ctx.author.id]['options']['levels'] = "any"
        elif setting.lower() == "dm" or setting.lower() == "pm":
            profiles[ctx.author.id]['options']['levels'] = "dm"
        await ctx.send("Options updated.")
        pickle.dump(profiles,open('data/profiles.data','wb'))

    @commands.has_permissions(manage_channels=True)
    @setLevels.command(name="clan")
    async def setLevelClan(self,ctx,setting:str=None,channel:discord.TextChannel=None):
        """
        Sets rankup messages for the server.
        Requires the manage_channels permission
        """
        clans = data_handler.Load("clans")
        settings = ['any','channel','disabled','dm']
        if setting not in settings:
            setting = None
        if setting is None:
            await ctx.send("""Please select a valid setting:
\n`any` - Default setting. Enables all messages in the channel they were earnt.
\n`channel <channel>` - Send them to a certain channel. This also sends clan rankup messages here. If you delete the channel it doesn't send a message.
\n`disabled` - Doesn't send messages. Also doesn't DM the user unless they have it set to DM.
\n`dm` - DMs the user unless they have it disabled. Disables clan rankup messages.
""")
            return
        if setting.lower() == "channel" and channel == None:
            await ctx.send("Please specify a channel.")
            return
        try:
            options = clans[ctx.guild.id]['options']
        except KeyError:
            clans[ctx.guild.id]['options'] = {'levels':"any"}
        if setting.lower() == "disable" or setting.lower() == "disabled":
            clans[ctx.guild.id]['options']['levels'] = "disabled"
        elif setting.lower() == "any":
            clans[ctx.clans.id]['options']['levels'] = "any"
        elif setting.lower() == "dm" or setting.lower() == "pm":
            clans[ctx.guild.id]['options']['levels'] = "dm"
        elif setting.lower() == "channel":
            clans[ctx.guild.id]['options']['levels'] = {'channel':chanel.id}
        await ctx.send("Option updated.")
        pickle.dump(clans,open('data/clans.data','wb'))

    @commands.has_permissions(manage_channels=True)
    @setOptions.group(name='messages', invoke_without_command=True)
    async def setMessages(self,ctx):
        """
        Command to change leave and welcome messages
        """
        await ctx.send("Please select either join or leave.")

    @commands.has_permissions(manage_channels=True)
    @setMessages.command(name='join',inkove_without_command=True)
    async def setJoinMessages(self,ctx):
        """
        Enters the message editor for join messages.
        """
        # Checks they aren't already in the editor.
        try:
            myVar = self.joinSelection[ctx.author.id]
            await ctx.send("You are already in an editor")
            return
        except KeyError:
            pass
        try:
            myVar = self.leaveSelection[ctx.author.id]
            await ctx.send("You are already in an editor.")
            return
        except KeyError:
            pass

        # Create the menu
        description = """`create` or edit a message
`list` the message names
`view` a message
`delete` a message
`channel` to set the channel
`exit` the editor
"""
        # List of menu options
        options = ["create",'list','view','delete','exit','channel']
        # Tell them they are in the editor
        await ctx.send("You have now entered the Join Message editor.")
        await asyncio.sleep(1)

        # Display the menu
        embed = discord.Embed(title="Main Menu",
                              colour=discord.Colour(0x45B858), #0xca1b1b
                              description=description)

        embed.set_author(name="Battle Bot Welcome Messages",url=self.bot.user.avatar_url_as(static_format='png'))
        embed.set_footer(text=f"Requested by: {ctx.author.display_name}",icon_url=ctx.author.avatar_url_as(static_format='png'))

        willExit = False
        clans = data_handler.Load("clans")
        
        # Breaks when they wish to exit. This exits the editor
        while willExit == False:
            self.joinSelection[ctx.author.id] = None
            # Breaks when they have a valid selection on the menu
            while self.joinSelection[ctx.author.id] == None:
                # Sends the menu and tells them to make a selection
                mainMessage = await ctx.send(content="Please select an option:",embed=embed)
                # Checks it's a valid option by the author and is in the correct channel
                def isOption(m):
                    # Check correct author
                    if m.author.id != ctx.author.id:
                        return False
                    # Correct channel?
                    if mainMessage.channel.id == m.channel.id:
                        # Valid option?
                        if m.content.lower() in options:
                            # Sets the selection
                            self.joinSelection[ctx.author.id] = m.content.lower()
                            return True
                        # Invalid option
                        else:
                            raise KeyError
                    # Incorrect channel.
                    return False
                try:
                    # Begins the wait_for
                    select = await self.bot.wait_for('message',check=isOption)
                # Invalid option
                except KeyError:
                    await ctx.send("That is not a valid option!")
                    await asyncio.sleep(0.5)
            # If they chose to exit
            if self.joinSelection[ctx.author.id] == "exit":
                del self.joinSelection[ctx.author.id]
                willExit = True

            # The choose to create a message
            elif self.joinSelection[ctx.author.id] == "create":
                # Checks they don't exceed 15 messages.
                async def MessageLimitCheck():
                    try:
                        if len(clans[ctx.guild.id]['options']['messages']['join']) >= 15:
                            await ctx.send("You already have 15 messages. Please delete one to add another.")
                            return False
                    except KeyError:
                        pass
                    return True
                hasHitMessageLimit = await MessageLimitCheck()
                if hasHitMessageLimit:
                    # Choose the name
                    def theMessageName(m):
                        if m.author.id != ctx.author.id:
                            return False
                        if nameMessage.channel.id != m.channel.id:
                            return False
                        # Store the name in a temp variable
                        # Avoids KeyErrors if they haven't set a message before
                        try:
                            options = clans[ctx.guild.id]['options']
                            try:
                                messages = clans[ctx.guild.id]['options']['messages']['temp']
                                clans[ctx.guild.id]['options']['messages']['temp'] = m.content
                            except KeyError:
                                clans[ctx.guild.id]['options']['messages'] = {'join':{},'leave':{},'temp':m.content}
                        except KeyError:
                            clans[ctx.guild.id]['options'] = {'messages':{'join':{},'leave':{},'temp':m.content}}
                        return True
                            
                    nameMessage = await ctx.send("What shall be the name of your message?")
                    createName = await self.bot.wait_for('message',check=theMessageName)
                    
                    # Set the message
                    def theMessageContent(m):
                        if m.author.id != ctx.author.id or messageMessage.channel.id != m.channel.id:
                            return False
                        clans[ctx.guild.id]['options']['messages']['join'][str(clans[ctx.guild.id]['options']['messages']['temp'])] = m.content
                        return True
                    
                    # Asks them to send the messages and mentions placeholders
                    messageMessage = await ctx.send("""What message would you like me to send?
>>> **__Placeholders:__**

`{member_name}` - References the member  that joined by name and discriminator.
`{member_mention}` - Mentions the member that joined.
`{created}` - Tells you when the user created a discord account.
`{position}` - The position the user joined at.
Mentioning channels and users will also work but they won't change for each message.""")
                    createMessage = await self.bot.wait_for('message',check=theMessageContent)

                    # Ends the create option
                    await ctx.send("Message added. Returning you to the main menu.")
                    await asyncio.sleep(1)

            # Sets the channel
            elif self.joinSelection[ctx.author.id] == "channel":
                def theChannel(m):
                    return m.author.id == ctx.author.id and aChannel.channel.id == m.channel.id

                # Asks them to specify the channel
                aChannel = await ctx.send("""Which channel would you like to send welcome messages to?""")
                setChannel = await self.bot.wait_for('message',check=theChannel)

                # Sets the channel and makes sure it's a channel.
                try:
                    clans[ctx.guild.id]['options']['messages']['joinChannel'] = await commands.TextChannelConverter().convert(ctx,setChannel.content)
                    clans[ctx.guild.id]['options']['messages']['joinChannel'] = clans[ctx.guild.id]['options']['messages']['joinChannel'].id
                    await ctx.send("Channel set. Returning you to the main menu.")
                except KeyError:
                    await ctx.send("Please create a message first. Returning you to the main menu.")

                # Ends the channel option
                await asyncio.sleep(1)

            # Allows the user to delete a message
            elif self.joinSelection[ctx.author.id] == "delete":
                def theMessageToDelete(m):
                    return m.author.id == ctx.author.id and aMessage.channel.id == m.channel.id

                aMessage = await ctx.send("Which message would you like to delete? Please use the message name, not content.\n\nTo cancel, please choose an invalid name.")
                messageToDelete = await self.bot.wait_for('message',check=theMessageToDelete)

                try:
                    del clans[ctx.guild.id]['options']['messages']['join'][messageToDelete.content]
                    await ctx.send(f"Deleted message called `{messageToDelete.content}`")
                except KeyError:
                    await ctx.send("I can't find a message by that name. Returning you to the main menu.")

                await asyncio.sleep(1)
            elif self.joinSelection[ctx.author.id] == "list":
                try:
                    msg = ">>> **__Message Names__**\n"
                    for name in clans[ctx.guild.id]['options']['messages']['join']:
                        msg += f"\n• `{name}`"
                        #msg += f"{clans[ctx.guild.id]['options']['messages']['join'][name]}\n"
                    await ctx.send(msg)
                    await asyncio.sleep(5)
                except KeyError:
                    await ctx.send("Please create some messages first. Returning you to the main menu")

                await asyncio.sleep(1)
            elif self.joinSelection[ctx.author.id] == "view":
                def theMessageToView(m):
                    return m.author.id == ctx.author.id and aMessage.channel.id == m.channel.id

                aMessage = await ctx.send("Which message would you like to view? Please use the message name, not content.\n\nTo cancel, please choose an invalid name.")
                messageToView = await self.bot.wait_for('message',check=theMessageToView)

                try:
                    await ctx.send("`{clans[ctx.author.id]['options']['messages']['join']['messageToView.content']}`")
                    asyncio.sleep(3)
                except KeyError:
                    await ctx.send("That message doesn't exist. Returning to main menu")

                await asyncio.sleep(1)
                
            # If I haven't set that up yet
            else:
                await ctx.send("Option not created yet.")
                await asyncio.sleep(0.5)

        await ctx.send("You have now left the editor.")
        pickle.dump(clans,open('data/clans.data','wb'))

    @commands.has_permissions(manage_channels=True)
    @setMessages.command(name='leave',inkove_without_command=True)
    async def setLeaveMessages(self,ctx):
        """
        Enters the message editor for leave messages.
        """
        # Checks they aren't already in the editor.
        try:
            myVar = self.joinSelection[ctx.author.id]
            await ctx.send("You are already in an editor")
            return
        except KeyError:
            pass
        try:
            myVar = self.leaveSelection[ctx.author.id]
            await ctx.send("You are already in an editor.")
            return
        except KeyError:
            pass

        # Create the menu
        description = """`create` or edit a message
`list` the message names
`view` a message
`delete` a message
`channel` to set the channel
`exit` the editor
"""
        # List of menu options
        options = ["create",'list','view','delete','exit','channel']
        # Tell them they are in the editor
        await ctx.send("You have now entered the Leave Message editor.")
        await asyncio.sleep(1)

        # Display the menu
        embed = discord.Embed(title="Main Menu",
                              colour=discord.Colour(0xca1b1b), #0xca1b1b
                              description=description)

        embed.set_author(name="Battle Bot Leave Messages",url=self.bot.user.avatar_url_as(static_format='png'))
        embed.set_footer(text=f"Requested by: {ctx.author.display_name}",icon_url=ctx.author.avatar_url_as(static_format='png'))

        willExit = False
        clans = data_handler.Load("clans")
        
        # Breaks when they wish to exit. This exits the editor
        while willExit == False:
            self.leaveSelection[ctx.author.id] = None
            # Breaks when they have a valid selection on the menu
            while self.leaveSelection[ctx.author.id] == None:
                # Sends the menu and tells them to make a selection
                mainMessage = await ctx.send(content="Please select an option:",embed=embed)
                # Checks it's a valid option by the author and is in the correct channel
                def isOption(m):
                    # Check correct author
                    if m.author.id != ctx.author.id:
                        return False
                    # Correct channel?
                    if mainMessage.channel.id == m.channel.id:
                        # Valid option?
                        if m.content.lower() in options:
                            # Sets the selection
                            self.leaveSelection[ctx.author.id] = m.content.lower()
                            return True
                        # Invalid option
                        else:
                            raise KeyError
                    # Incorrect channel.
                    return False
                try:
                    # Begins the wait_for
                    select = await self.bot.wait_for('message',check=isOption)
                # Invalid option
                except KeyError:
                    await ctx.send("That is not a valid option!")
                    await asyncio.sleep(0.5)
            # If they chose to exit
            if self.leaveSelection[ctx.author.id] == "exit":
                del self.leaveSelection[ctx.author.id]
                willExit = True

            # The choose to create a message
            elif self.leaveSelection[ctx.author.id] == "create":
                # Checks they don't exceed 15 messages.
                async def MessageLimitCheck():
                    try:
                        if len(clans[ctx.guild.id]['options']['messages']['leave']) >= 15:
                            await ctx.send("You already have 15 messages. Please delete one to add another.")
                            return False
                    except KeyError:
                        pass
                    return True
                hasHitMessageLimit = await MessageLimitCheck()
                if hasHitMessageLimit:
                    # Choose the name
                    def theMessageName(m):
                        if m.author.id != ctx.author.id:
                            return False
                        if nameMessage.channel.id != m.channel.id:
                            return False
                        # Store the name in a temp variable
                        # Avoids KeyErrors if they haven't set a message before
                        try:
                            options = clans[ctx.guild.id]['options']
                            try:
                                messages = clans[ctx.guild.id]['options']['messages']['temp']
                                clans[ctx.guild.id]['options']['messages']['temp'] = m.content
                            except KeyError:
                                clans[ctx.guild.id]['options']['messages'] = {'join':{},'leave':{},'temp':m.content}
                        except KeyError:
                            clans[ctx.guild.id]['options'] = {'messages':{'join':{},'leave':{},'temp':m.content}}
                        return True
                            
                    nameMessage = await ctx.send("What shall be the name of your message?")
                    createName = await self.bot.wait_for('message',check=theMessageName)
                    
                    # Set the message
                    def theMessageContent(m):
                        if m.author.id != ctx.author.id or messageMessage.channel.id != m.channel.id:
                            return False
                        clans[ctx.guild.id]['options']['messages']['leave'][str(clans[ctx.guild.id]['options']['messages']['temp'])] = m.content
                        return True
                    
                    # Asks them to send the messages and mentions placeholders
                    messageMessage = await ctx.send("""What message would you like me to send?
>>> **__Placeholders:__**

`{member_name}` - References the member  that left by name and discriminator.
`{created}` - Tells you when the user created a discord account.
`{position}` - The position the user joined at.
Mentioning channels and users will also work but they won't change for each message.""")
                    createMessage = await self.bot.wait_for('message',check=theMessageContent)

                    # Ends the create option
                    await ctx.send("Message added. Returning you to the main menu.")
                    await asyncio.sleep(1)

            # Sets the channel
            elif self.leaveSelection[ctx.author.id] == "channel":
                def theChannel(m):
                    return m.author.id == ctx.author.id and aChannel.channel.id == m.channel.id

                # Asks them to specify the channel
                aChannel = await ctx.send("""Which channel would you like to send welcome messages to?""")
                setChannel = await self.bot.wait_for('message',check=theChannel)

                # Sets the channel and makes sure it's a channel.
                try:
                    clans[ctx.guild.id]['options']['messages']['leaveChannel'] = await commands.TextChannelConverter().convert(ctx,setChannel.content)
                    clans[ctx.guild.id]['options']['messages']['leaveChannel'] = clans[ctx.guild.id]['options']['messages']['leaveChannel'].id
                    await ctx.send("Channel set. Returning you to the main menu.")
                except KeyError:
                    await ctx.send("Please create a message first. Returning you to the main menu.")

                # Ends the channel option
                await asyncio.sleep(1)

            # Allows the user to delete a message
            elif self.leaveSelection[ctx.author.id] == "delete":
                def theMessageToDelete(m):
                    return m.author.id == ctx.author.id and aMessage.channel.id == m.channel.id

                aMessage = await ctx.send("Which message would you like to delete? Please use the message name, not content.\n\nTo cancel, please choose an invalid name.")
                messageToDelete = await self.bot.wait_for('message',check=theMessageToDelete)

                try:
                    del clans[ctx.guild.id]['options']['messages']['leave'][messageToDelete.content]
                    await ctx.send(f"Deleted message called `{messageToDelete.content}`")
                except KeyError:
                    await ctx.send("I can't find a message by that name. Returning you to the main menu.")

                await asyncio.sleep(1)
            elif self.leaveSelection[ctx.author.id] == "list":
                try:
                    msg = ">>> **__Message Names__**\n"
                    for name in clans[ctx.guild.id]['options']['messages']['leave']:
                        msg += f"\n• `{name}`"
                        #msg += f"{clans[ctx.guild.id]['options']['messages']['leave'][name]}\n"
                    await ctx.send(msg)
                    await asyncio.sleep(5)
                except KeyError:
                    await ctx.send("Please create some messages first. Returning you to the main menu")

                await asyncio.sleep(1)
            elif self.leaveSelection[ctx.author.id] == "view":
                def theMessageToView(m):
                    return m.author.id == ctx.author.id and aMessage.channel.id == m.channel.id

                aMessage = await ctx.send("Which message would you like to view? Please use the message name, not content.\n\nTo cancel, please choose an invalid name.")
                messageToView = await self.bot.wait_for('message',check=theMessageToView)

                try:
                    await ctx.send("`{clans[ctx.author.id]['options']['messages']['leave']['messageToView.content']}`")
                    asyncio.sleep(3)
                except KeyError:
                    await ctx.send("That message doesn't exist. Returning to main menu")

                await asyncio.sleep(1)
                
            # If I haven't set that up yet
            else:
                await ctx.send("Option not created yet.")
                await asyncio.sleep(0.5)
                
        await ctx.send("You have now left the editor.")
        pickle.dump(clans,open('data/clans.data','wb'))
            
def setup(bot):
    bot.add_cog(Options(bot))
