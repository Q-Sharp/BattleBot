import discord
from discord.ext import commands
import asyncio
from data.data_handler import data_handler

class Subscriptions(commands.Cog):

    # Initialises the variables and sets the bot so we can reference it later.
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='subscriptions', aliases = ['subs', 'subscription'])
    async def subsciptions(self, ctx, channel = None):
        """
        Displays the subscriptions the channel has that are active.

        If a channel is not specified, it uses the channel the command was sent in.
        """

        # Sets up the channel based on a parameter, or lack of user input for one.
        if channel is None:
            channel = ctx.channel
        else:
            channel = await commands.TextChannelConverter().convert(ctx,channel)

        # Loads our data
        subs = data_handler.load("subscriptions")

        # Defines the message
        message = "This channel is subscribed to:"

        # Goes through each of the valid suscriptions
        for subscription in subs["Subscribers"].values():
            # Checks if the subscriber is subscribed
            if channel.id in subscription["Channels"]:
                # Adds the correct subscriptions to the message
                message += f"\n• `{subscription['name']}`"

        # Outputs a different message if they haven't subscribed
        if message == "This channel is subscribed to:":
            await ctx.send("This channel isn't subscribed to anything!")
        # Otherwise just send the message we made
        else:
            await ctx.send(message)

    @commands.command(name="subscribed", aliases = ['subscribers'])
    async def subscribers(self, ctx, subscription = None):
        """
        View the amount of subscribers a subscription has.
        """
        # Collects the data
        subs = data_handler.load("subscriptions")

        # Outputs all valid subscriptions when the user doesn't specify one.
        # It lists the subscription name, channel and server.
        if subscription is None:
            message = "Please select a valid subscription.\n\nValid subscriptions:"
            # Cycles through each of the valid descriptions and formats the output
            # It turns dictionary into a 2d list to do so.
            for key, value in subs["Subscriptions"].items():
                message += f"\n• `{key}` - {self.bot.get_channel(value).mention} in **{self.bot.get_channel(value).guild.name}**"
            await ctx.send(message)
            return


        # Checks the subscription is valid, so there is actually a subscription with that name.
        if subscription not in subs["Subscriptions"].keys():
            message = "Please select a valid subscription.\n\nValid subscriptions:"
            # Cycles through each of the valid descriptions and formats the output
            # It turns dictionary into a 2d list to do so.
            for key, value in subs["Subscriptions"].items():
                message += f"\n• `{key}` - {self.bot.get_channel(value).mention} in **{self.bot.get_channel(value).guild.name}**"
            await ctx.send(message)
            return

        # Gets the number of subscribers
        subscribers = len(subs["Subscribers"][str(subs["Subscriptions"][subscription])]["Channels"])
        # Output a suitable error message.
        await ctx.send(f"`{subscription}` has {subscribers} subscribers.")

    @commands.command(name = "subscribe", aliases = ["sub"])
    async def subscribe(self, ctx, subscription = None, channel = None):
        """
        Subscribes to a channel.

        Don't specify a subscription to view all valid subsciptions.
        """

        # Collects the data
        subs = data_handler.load("subscriptions")

        # Outputs all valid subscriptions when the user doesn't specify one.
        # It lists the subscription name, channel and server.
        if subscription is None:
            message = "Please select a valid subscription.\n\nValid subscriptions:"
            # Cycles through each of the valid descriptions and formats the output
            # It turns dictionary into a 2d list to do so.
            for key, value in subs["Subscriptions"].items():
                message += f"\n• `{key}` - {self.bot.get_channel(value).mention} in **{self.bot.get_channel(value).guild.name}**"
            await ctx.send(message)
            return

        # Checks the subscription is valid, so there is actually a subscription with that name.
        elif subscription not in subs["Subscriptions"].keys():
            message = "Please select a valid subscription.\n\nValid subscriptions:"
            # Cycles through each of the valid descriptions and formats the output
            # It turns dictionary into a 2d list to do so.
            for key, value in subs["Subscriptions"].items():
                message += f"\n• `{key}` - {self.bot.get_channel(value).mention} in **{self.bot.get_channel(value).guild.name}**"
            await ctx.send(message)
            return

        # Converts the channel to a TextChannel object.
        # If no channel is specified, use the current channel.
        if channel is None:
            channel = ctx.channel
        else:
            channel = await commands.TextChannelConverter().convert(ctx,channel)

        # Checks if that channel is already subscibed.
        if channel.id in subs["Subscribers"][str(subs["Subscriptions"][subscription])]["Channels"]:
            await ctx.send(f"You're already subscribed to {subscription}!")
            return
        
        # Gets the permissions for the channel
        permissions = channel.permissions_for(channel.guild.get_member(self.bot.user.id))

        # Checks we have permissions to send messages, send embeds and send attachments (so we can correctly forward messages)
        if not permissions.send_messages or not permissions.embed_links or not permissions.attach_files:
            await ctx.send("I don't have enough permissions there! I need to be able to send messages, embed links and attach files or else not all the messages may go through.")
            return
        
        # Add the channel to the subscription!
        subs["Subscribers"][str(subs["Subscriptions"][subscription])]["Channels"].append(channel.id)

        # Save the data
        data_handler.dump(subs, "subscriptions")

        # Send a message letting the channel know that it's subscribed.
        value = subs["Subscriptions"][subscription]
        await channel.send(f"This channel is now subscibed to {self.bot.get_channel(value).mention} in **{self.bot.get_channel(value).guild.name}**.")

    @commands.command(name = "unsubscribe", aliases = ["unsub"])
    async def unsubscribe(self, ctx, subscription = None, channel = None):
        """
        Unsubscribes to a channel.

        To view current subscriptions. Use `b!sub [channel]`
        """

        # Collects the data
        subs = data_handler.load("subscriptions")

        # Outputs all valid subscriptions when the user doesn't specify one.
        # It lists the subscription name, channel and server.
        if subscription is None:
            message = "Please select a valid subscription.\n\nValid subscriptions:"
            # Cycles through each of the valid descriptions and formats the output
            # It turns dictionary into a 2d list to do so.
            for key, value in subs["Subscriptions"].items():
                message += f"\n• `{key}` - {self.bot.get_channel(value).mention} in **{self.bot.get_channel(value).guild.name}**"
            await ctx.send(message)
            return
        # Checks the subscription is valid, so there is actually a subscription with that name.
        elif subscription not in subs["Subscriptions"].keys():
            message = "Please select a valid subscription.\n\nValid subscriptions:"
            # Cycles through each of the valid descriptions and formats the output
            # It turns dictionary into a 2d list to do so.
            for key, value in subs["Subscriptions"].items():
                message += f"\n• `{key}` - {self.bot.get_channel(value).mention} in **{self.bot.get_channel(value).guild.name}**"
            await ctx.send(message)
            return

        # Converts the channel to a TextChannel object.
        # If no channel is specified, use the current channel.
        if channel is None:
            channel = ctx.channel
        else:
            channel = await commands.TextChannelConverter().convert(ctx,channel)

        # Checks if that channel is already subscibed.
        if channel.id not in subs["Subscribers"][str(subs["Subscriptions"][subscription])]["Channels"]:
            await ctx.send(f"You aren't subscribed to {subscription}!")
            return
        
        # Add the channel to the subscription!
        subs["Subscribers"][str(subs["Subscriptions"][subscription])]["Channels"].remove(channel.id)

        # Save the data
        data_handler.dump(subs, "subscriptions")

        # Send a message letting the channel know that it's subscribed.
        value = subs["Subscriptions"][subscription]
        await channel.send(f"This channel is no longer subscibed to {self.bot.get_channel(value).mention} in **{self.bot.get_channel(value).guild.name}**.")

    # A listener for any messages sent in any valid subscription channels.
    # If it's a valid subscripion, send that message to all the other servers.
    @commands.Cog.listener()
    async def on_message(self, ctx):
        # Obtains the relebent data.
        subs = data_handler.load("subscriptions")

        # Creates a list of ids of valid subscriptions
        channels = list(subs["Subscriptions"].values())
        # Check if the channel is in that list of valid subscriptions we just made
        if ctx.channel.id in channels:

            # Cycle through the subscibed channels of the subscription
            for channelID in subs["Subscribers"][str(ctx.channel.id)]["Channels"]:

                # Get the TextChannel object from the id
                channel = self.bot.get_channel(channelID)

                # Convert the message so we can output it all correctly.
                # Checks if it's a system message, if so, output it nicely.
                if ctx.is_system():
                    message = f">>> {ctx.system_content}"
                # Checks if the content is empty, if no, just add the author's name.
                elif ctx.content == "":
                    message = f"**{ctx.author.name}#{ctx.author.discriminator}:**\n"
                # If the content isn't empty, add the user's name and quote them.
                else:
                    message = f"**{ctx.author.name}#{ctx.author.discriminator}:**\n>>> {ctx.content}"
                
                # Check if the message has any embeds.
                if len(ctx.embeds) == 0:
                    embed = None
                # If it has, add them to the message!
                else:
                    embed = ctx.embeds[0]

                # Turn any attachments into files and add them to the message.
                files = []
                for file in ctx.attachments:
                    theFile = await file.to_file()
                    files.append(theFile)
                if files == []:
                    files = None

                # Escapes mentions so we don't mention everyone if we don't need to.
                message = discord.utils.escape_mentions(message)

                # Try sending the now formatted message.
                try:
                    await channel.send(message, embed=embed, files = files)
                # If the bot doesn't have permissions, just ignore it.
                except discord.Forbidden:
                    pass

# Setup the cog correctly when called to do so.
def setup(bot):
    bot.add_cog(Subscriptions(bot))