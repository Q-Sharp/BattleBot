import discord
from discord.ext import commands
import asyncio
from data.data_handler import data_handler

class Servers(commands.Cog):

    # Initialises the variables and sets the bot.
    def __init__(self, bot):
        self.bot = bot
        self.Selection = {}
        self.temp = {}

    # Our base level command. Due to invoke_without_command=True it means that this command is only run when no
    # sub-command is run. Makes it a command group with a name.
    @commands.group(name='server', aliases = ['s'])
    # Defines it as a function.
    async def server(self, ctx):
        """
        Check information on a server!
        """

        servers = data_handler.load("servers")
        try:
            server = servers[str(ctx.guild.id)]
        except KeyError:
            servers[str(ctx.guild.id)] = {
                "Base": {
                    "Type": "Clan",
                    "clanID": "#bb1"
                    },
                    "Messages": {
                        "joinChannel": None,
                        "joinMessages": {},
                        "leaveChannel": {},
                        "leaveMessages": {},
                        "temp": "ExampleJoin",
                        "rankUpMessages": "any",
                        "rankUpChannel": None
                    },
                    "Modlog": {
                        "channel": None
                    }
                }
            data_handler.dump(servers, "servers")
            servers = servers[str(ctx.guild.id)]
        
        if ctx.invoked_subcommand is not None:
            return

        embed = discord.Embed(title = ctx.guild.name,
        description = f"Type: {server['Base']['Type']}",
        colour = ctx.guild.owner.colour)

        embed.set_thumbnail(url = ctx.guild.icon_url_as(static_format="png"))

        if server['Base']['Type'] == "clan":
            embed.add_field(name="Clan",value="WIP")

        Channel = server["Messages"]["joinChannel"] or "`none`"
        embed.add_field(name="`JoinMessages`",
        value=f"Channel: {ctx.guild.get_channel(Channel).mention}\nMessage amount: {len(server['Messages']['joinMessages'])}")

        Channel = server["Messages"]["leaveChannel"] or "`none`"
        embed.add_field(name="`LeaveMessages`",
        value=f"Channel: {ctx.guild.get_channel(Channel).mention}\nMessage amount: {len(server['Messages']['leaveMessages'])}")

        if server["Modlog"]["channel"] is not None:
            embed.add_field(name = "`Modlog`",
            value = f"Status: `Enabled`\nChannel: {ctx.guild.get_channel(server['Modlog']['channel']).mention}",
            inline = False)
        else:
            embed.add_field(name = "Modlog",
            value = "Status: `Disabled`",
            inline = False)

        if server['Messages']["rankUpMessages"] == "channel":
            embed.add_field(name = "`RankUpMessages`",
            value = f"Type: `channel`\nChannel: {ctx.guild.get_channel(server['Messages']['rankUpChannel']).mention}",
            inline = False)
        else:
            embed.add_field(name = "`RankUpMessages`",
            value = f"Type: {server['Messages']['rankUpMessages']}",
            inline = False)

        await ctx.send(content="",embed=embed)

    
    @commands.has_permissions(manage_channels=True)
    @server.command(name = 'modlod', aliases = ['ml'])
    async def modlogMessages(self, ctx, value:str = None, channel = None):
        """
        Enabled/disables the modlog and specifies which channel to send it to.

        Valid values:
        `[y/yes/enable/on]` - Enables the modlog.
        `[n/no/disable/off]` - Disables the modlog.

        Please mention the channel to select it. You will have to specify a channel when re-enabling.
        """

        if value not in ['y','yes','enable','on','n','no','disable','off']:
            await ctx.send(""" That's not a valid setting. Please use one of the following:
`[y/yes/enable/on]` - Enables the modlog.
`[n/no/disable/off]` - Disables the modlog.""")

        servers = data_handler.load("server")
        if value in ['n','no','disable','off']:
            servers[str(ctx.guild.id)]['Modlog']['channel'] = None
        elif value in ['y','yes','enable','on']:
            try:
                servers[str(ctx.guild.id)]['Modlog']['channel'] = await commands.TextChannelConverter().convert(ctx,channel)
                servers[str(ctx.guild.id)]['Modlog']['channel'] = servers[str(ctx.guild.id)]['Modlog']['channel'].id
            except:
                await ctx.send("Please select a vaid channel.")
                return

        data_handler.dump(servers, "servers")
        await ctx.send("Modlog updated.")


    @commands.has_permissions(manage_channels=True)
    @server.command(name = 'rankupmessages', aliases = ['rum', 'rm', 'rankUpMessages', 'rums', 'RankUpMessages', 'rankupmessage'])
    async def rankUpMessages(self, ctx, value:str = None, channel = None):
        """
        Changes where rank up messages go.

        Valid settings:
        `any` - Sends them anywhere. Generally depends on the user's setting.
        `channel` - Sends them to a specific channel (please mention the channel)
        `none` - Doesn't send any rankup messages to the server. If enabled it can DM the user though.
        """

        if value not in ['any', 'channel', 'none']:
            await ctx.send("""That's not a valid setting. Please use one of the following:
`any` - Sends them anywhere. Generally depends on the user's setting.
`channel` - Sends them to a specific channel (please mention the channel)
`none` - Doesn't send any rankup messages to the server. If enabled it can DM the user though.""")
            return
        servers = data_handler.load("servers")
        if value in ['any', 'none']:
            servers[str(ctx.guild.id)]['Messages']['rankUpMessages'] = value
        elif value == 'channel':
            try:
                servers[str(ctx.guild.id)]['Messages']['rankUpChannel'] = await commands.TextChannelConverter().convert(ctx,channel)
                servers[str(ctx.guild.id)]['Messages']['rankUpChannel'] = servers[str(ctx.guild.id)]['Messages']['rankUpChannel'].id
                servers[str(ctx.guild.id)]['Messages']['rankUpMessages'] = "channel"
            except:
                await ctx.send("Please select a vaid channel.")
                return

        data_handler.dump(servers, "servers")
        await ctx.send("Setting updated.")

    @commands.has_permissions(manage_channels=True)
    @server.command(name = 'join', aliases = ['j','joinmessages','joinMessages','JoinMessages','jm', 'messagesjoin'])
    async def joinMessages(self, ctx):
        """
        Enters the message editor for join messages.

        Please note this command generates a lot of spam.
        """
        # Checks they aren't already in the editor.
        try:
            self.Selection[ctx.author.id]
            await ctx.send("You are already in an editor")
            return
        except:
            pass
        self.Selection[ctx.author.id] = None

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
        servers = data_handler.load("servers")
        server = servers[str(ctx.guild.id)]['Messages']
        
        # Breaks when they wish to exit. This exits the editor
        while willExit == False:
            self.Selection[ctx.author.id] = None
            # Breaks when they have a valid selection on the menu
            while self.Selection[ctx.author.id] == None:
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
                            self.Selection[ctx.author.id] = m.content.lower()
                            return True
                        # Invalid option
                        else:
                            raise KeyError
                    # Incorrect channel.
                    return False
                try:
                    # Begins the wait_for
                    await self.bot.wait_for('message',check=isOption)
                # Invalid option
                except KeyError:
                    await ctx.send("That is not a valid option!")
                    await asyncio.sleep(0.5)
            # If they chose to exit
            if self.Selection[ctx.author.id] == "exit":
                del self.Selection[ctx.author.id]
                willExit = True

            # The choose to create a message
            elif self.Selection[ctx.author.id] == "create":
                # Checks they don't exceed 15 messages.
                async def MessageLimitCheck():
                    try:
                        if len(server['joinMessages']) >= 15:
                            await ctx.send("You already have 15 messages. Please delete one to add another.")
                            return True
                    except KeyError:
                        pass
                    return False
                hasHitMessageLimit = await MessageLimitCheck()
                if not hasHitMessageLimit:
                    # Choose the name
                    def theMessageName(m):
                        if m.author.id != ctx.author.id:
                            return False
                        if nameMessage.channel.id != m.channel.id:
                            return False
                        # Store the name in a temp variable
                        # Avoids KeyErrors if they haven't set a message before
                        server["temp"] = m.content
                        return True
                            
                    nameMessage = await ctx.send("What shall be the name of your message?")
                    await self.bot.wait_for('message',check=theMessageName)
                    
                    # Set the message
                    def theMessageContent(m):
                        if m.author.id != ctx.author.id or messageMessage.channel.id != m.channel.id:
                            return False
                        server['joinMessages'][str(server['temp'])] = m.content
                        return True
                    
                    # Asks them to send the messages and mentions placeholders
                    messageMessage = await ctx.send("""What message would you like me to send?
>>> **__Placeholders:__**

`{member_name}` - References the member  that joined by name and discriminator.
`{member_mention}` - Mentions the member that joined.
`{created}` - Tells you when the user created a discord account.
`{position}` - The position the user joined at.
Mentioning channels and users will also work but they won't change for each message.""")
                    await self.bot.wait_for('message',check=theMessageContent)

                    # Ends the create option
                    await ctx.send("Message added. Returning you to the main menu.")
                    await asyncio.sleep(1)

            # Sets the channel
            elif self.Selection[ctx.author.id] == "channel":
                def theChannel(m):
                    return m.author.id == ctx.author.id and aChannel.channel.id == m.channel.id

                # Asks them to specify the channel
                aChannel = await ctx.send("""Which channel would you like to send welcome messages to?""")
                setChannel = await self.bot.wait_for('message',check=theChannel)

                # Sets the channel and makes sure it's a channel.
                try:
                    server['joinChannel'] = await commands.TextChannelConverter().convert(ctx,setChannel.content)
                    server['joinChannel'] = server['joinChannel'].id
                    await ctx.send("Channel set. Returning you to the main menu.")
                except KeyError:
                    await ctx.send("Please create a message first. Returning you to the main menu.")

                # Ends the channel option
                await asyncio.sleep(1)

            # Allows the user to delete a message
            elif self.Selection[ctx.author.id] == "delete":
                def theMessageToDelete(m):
                    return m.author.id == ctx.author.id and aMessage.channel.id == m.channel.id

                aMessage = await ctx.send("Which message would you like to delete? Please use the message name, not content.\n\nTo cancel, please choose an invalid name (anything but the name of a message).")
                messageToDelete = await self.bot.wait_for('message',check=theMessageToDelete)

                try:
                    del server['joinMessages'][messageToDelete.content]
                    await ctx.send(f"Deleted message called `{messageToDelete.content}`")
                except KeyError:
                    await ctx.send("I can't find a message by that name. Returning you to the main menu.")

                await asyncio.sleep(1)
            elif self.Selection[ctx.author.id] == "list":
                try:
                    msg = ">>> **__Message Names__**\n"
                    for name in server['joinMessages']:
                        msg += f"\n• `{name}`"
                    await ctx.send(msg)
                    await asyncio.sleep(5)
                except KeyError:
                    await ctx.send("Please create some messages first. Returning you to the main menu")

                await asyncio.sleep(1)
            elif self.Selection[ctx.author.id] == "view":
                def theMessageToView(m):
                    return m.author.id == ctx.author.id and aMessage.channel.id == m.channel.id

                aMessage = await ctx.send("Which message would you like to view? Please use the message name, not content.\n\nTo cancel, please choose an invalid name (anything but the name of a message).")
                messageToView = await self.bot.wait_for('message',check=theMessageToView)

                try:
                    await ctx.send(f"`{server['joinMessages'][messageToView.content]}`")
                    asyncio.sleep(3)
                except KeyError:
                    await ctx.send("That message doesn't exist. Returning to main menu")

                await asyncio.sleep(1)
                
            # If I haven't set that up yet
            else:
                await ctx.send("Option not created.")
                await asyncio.sleep(0.5)

        await ctx.send("You have now left the editor.")
        servers[str(ctx.guild.id)]['Messages'] = server
        data_handler.dump(servers, "servers")

    @commands.has_permissions(manage_channels=True)
    @server.command(name = 'leave', aliases = ['l','leavemessages','leaveMessages','LeaveMessages','lm', 'messagesleave'])
    async def leaveMessages(self, ctx):
        """
        Enters the message editor for leave messages.

        Please note this command generates a lot of spam.
        """
        # Checks they aren't already in the editor.
        try:
            self.Selection[ctx.author.id]
            await ctx.send("You are already in an editor")
            return
        except:
            pass
        self.Selection[ctx.author.id] = None

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
                              colour=discord.Colour(0x45B858), #0xca1b1b
                              description=description)

        embed.set_author(name="Battle Bot Leave Messages",url=self.bot.user.avatar_url_as(static_format='png'))
        embed.set_footer(text=f"Requested by: {ctx.author.display_name}",icon_url=ctx.author.avatar_url_as(static_format='png'))

        willExit = False
        servers = data_handler.load("servers")
        server = servers[str(ctx.guild.id)]['Messages']
        
        # Breaks when they wish to exit. This exits the editor
        while willExit == False:
            self.Selection[ctx.author.id] = None
            # Breaks when they have a valid selection on the menu
            while self.Selection[ctx.author.id] == None:
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
                            self.Selection[ctx.author.id] = m.content.lower()
                            return True
                        # Invalid option
                        else:
                            raise KeyError
                    # Incorrect channel.
                    return False
                try:
                    # Begins the wait_for
                    await self.bot.wait_for('message',check=isOption)
                # Invalid option
                except KeyError:
                    await ctx.send("That is not a valid option!")
                    await asyncio.sleep(0.5)
            # If they chose to exit
            if self.Selection[ctx.author.id] == "exit":
                del self.Selection[ctx.author.id]
                willExit = True

            # The choose to create a message
            elif self.Selection[ctx.author.id] == "create":
                # Checks they don't exceed 15 messages.
                async def MessageLimitCheck():
                    try:
                        if len(server['leaveMessages']) >= 15:
                            await ctx.send("You already have 15 messages. Please delete one to add another.")
                            return True
                    except KeyError:
                        pass
                    return False
                hasHitMessageLimit = await MessageLimitCheck()
                if not hasHitMessageLimit:
                    # Choose the name
                    def theMessageName(m):
                        if m.author.id != ctx.author.id:
                            return False
                        if nameMessage.channel.id != m.channel.id:
                            return False
                        # Store the name in a temp variable
                        # Avoids KeyErrors if they haven't set a message before
                        server["temp"] = m.content
                        return True
                            
                    nameMessage = await ctx.send("What shall be the name of your message?")
                    await self.bot.wait_for('message',check=theMessageName)
                    
                    # Set the message
                    def theMessageContent(m):
                        if m.author.id != ctx.author.id or messageMessage.channel.id != m.channel.id:
                            return False
                        server['leaveMessages'][str(server['temp'])] = m.content
                        return True
                    
                    # Asks them to send the messages and mentions placeholders
                    messageMessage = await ctx.send("""What message would you like me to send?
>>> **__Placeholders:__**

`{member_name}` - References the member  that left by name and discriminator.
`{created}` - Tells you when the user created a discord account.
`{position}` - The position the user joined at.
`{join_date}` - The date the user originally joined the server.
Mentioning channels and users will also work but they won't change for each message.""")
                    await self.bot.wait_for('message',check=theMessageContent)

                    # Ends the create option
                    await ctx.send("Message added. Returning you to the main menu.")
                    await asyncio.sleep(1)

            # Sets the channel
            elif self.Selection[ctx.author.id] == "channel":
                def theChannel(m):
                    return m.author.id == ctx.author.id and aChannel.channel.id == m.channel.id

                # Asks them to specify the channel
                aChannel = await ctx.send("""Which channel would you like to send leave messages to?""")
                setChannel = await self.bot.wait_for('message',check=theChannel)

                # Sets the channel and makes sure it's a channel.
                try:
                    server['leaveChannel'] = await commands.TextChannelConverter().convert(ctx,setChannel.content)
                    server['leaveChannel'] = server['leaveChannel'].id
                    await ctx.send("Channel set. Returning you to the main menu.")
                except KeyError:
                    await ctx.send("Please create a message first. Returning you to the main menu.")

                # Ends the channel option
                await asyncio.sleep(1)

            # Allows the user to delete a message
            elif self.Selection[ctx.author.id] == "delete":
                def theMessageToDelete(m):
                    return m.author.id == ctx.author.id and aMessage.channel.id == m.channel.id

                aMessage = await ctx.send("Which message would you like to delete? Please use the message name, not content.\n\nTo cancel, please choose an invalid name (anything but the name of a message).")
                messageToDelete = await self.bot.wait_for('message',check=theMessageToDelete)

                try:
                    del server['leaveMessages'][messageToDelete.content]
                    await ctx.send(f"Deleted message called `{messageToDelete.content}`")
                except KeyError:
                    await ctx.send("I can't find a message by that name. Returning you to the main menu.")

                await asyncio.sleep(1)
            elif self.Selection[ctx.author.id] == "list":
                try:
                    msg = ">>> **__Message Names__**\n"
                    for name in server['leaveMessages']:
                        msg += f"\n• `{name}`"
                    await ctx.send(msg)
                    await asyncio.sleep(5)
                except KeyError:
                    await ctx.send("Please create some messages first. Returning you to the main menu")

                await asyncio.sleep(1)
            elif self.Selection[ctx.author.id] == "view":
                def theMessageToView(m):
                    return m.author.id == ctx.author.id and aMessage.channel.id == m.channel.id

                aMessage = await ctx.send("Which message would you like to view? Please use the message name, not content.\n\nTo cancel, please choose an invalid name (anything but the name of a message).")
                messageToView = await self.bot.wait_for('message',check=theMessageToView)

                try:
                    await ctx.send(f"`{server['leaveMessages'][messageToView.content]}`")
                    asyncio.sleep(3)
                except KeyError:
                    await ctx.send("That message doesn't exist. Returning to main menu")

                await asyncio.sleep(1)
                
            # If I haven't set that up yet
            else:
                await ctx.send("Option not created.")
                await asyncio.sleep(0.5)

        await ctx.send("You have now left the editor.")
        servers[str(ctx.guild.id)]['Messages'] = server
        data_handler.dump(servers, "servers")

def setup(bot):
    bot.add_cog(Servers(bot))
    