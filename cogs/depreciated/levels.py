import discord
from discord.ext import commands
import pickle
import time
import random

# The points required for each rank to reach the next. The final range create 50 levels.
ranksRP = [int(5 * (i ** 1.5) + 50 * i + 100) for i in range(50)]


# Locates the rank and remaining rp to the next rank of a user given their total rp.
def get_rank_from(rp):
    rem_rp = int(rp)
    rank = 0
    while rem_rp >= ranksRP[rank]:
        rem_rp -= ranksRP[rank]
        rank += 1
    return rem_rp, rank


# Our Cog.
# The """ comment gives the cog info in the help section
class Levels(commands.Cog):
    """
    A global xp system with a Battle Legion twist.
    """

    # Initialises the variables and sets the bot.
    def __init__(self, bot):
        self.bot = bot
        self.rp_mult = 1

    # Our base level command. Due to invoke_without_command=True it means that this command is only run when no
    # sub-command is run. Makes it a command group with a name.
    @commands.group(name='level', invoke_without_command=True)
    # Defines it as a function.
    async def level(self, ctx, member: discord.Member = None):
        """
        Base level command.
        You can also use it to display the rank card of you or another member.
        """
        member = member or ctx.author
        profiles = pickle.load(open('data/profiles.data', 'rb'))
        try:
            theRP = profiles[member.id]['rp']
            remRP, theRank = get_rank_from(theRP)
        except KeyError:
            theRP = 0
            theRank = 0
            remRP = 0
        embed = discord.Embed(title=f"{member.display_name}'s rank card",
                              colour=member.colour,
                              description=f"{member.name}#{member.discriminator}")

        embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
        embed.set_footer(text=f"Requested by {ctx.author.display_name}",
                         icon_url=ctx.author.avatar_url_as(static_format='png'))

        embed.add_field(name=f"Rank: {theRank}",
                        value=f"Current RP: {remRP} \nRP to next rank: {ranksRP[theRank] - remRP} \nTotal RP: {theRP}")

        await ctx.send(content="", embed=embed)

    @level.group(name="leaderboard", aliases=["lb"], invoke_without_command=True)
    async def levelLB(self, ctx, member: discord.Member = None):
        """
        Check where people are relative to each other! Not specifying a page will select the first page.
        """
        # Sort the dictionary into a list.
        member = member or ctx.author
        profiles = pickle.load(open('data/profiles.data', 'rb'))
        rankings = []
        description = ""
        for profile in profiles:
            try:
                rankings.append({'id': profile, 'rp': profiles[profile]['rp']})
            except KeyError:
                pass

        def getKey(item):
            return item['rp']

        rankings = sorted(rankings, reverse=True, key=getKey)

        # Add the top 5
        end = 5
        if len(rankings) < 5:
            end = len(rankings)
        for i in range(end):
            user = await ctx.bot.fetch_user(rankings[i]['id'])
            description += f"**{i + 1}.** {user.name}#{user.discriminator} - {rankings[i]['rp']} rank points.\n"

        # Add member
        index = -1
        for i in range(len(rankings)):
            if rankings[i]['id'] == member.id:
                index = i
        if index <= 4:
            embed = discord.Embed(title="Global rank point leaderboard",
                                  colour=discord.Colour(0xa72693),
                                  description=description,
                                  inline=True)
            embed.set_footer(text=f"Requested by {ctx.author.display_name}",
                             icon_url=ctx.author.avatar_url_as(static_format="png"))
            await ctx.send(content="Here you go!", embed=embed)
            return
        description += "--==ME==--"
        for i in [index - 1, index, index + 1]:
            if i != len(rankings):
                user = await ctx.bot.fetch_user(rankings[i]['id'])
                description += f"\n**{i + 1}.** {user.name}#{user.discriminator} - {rankings[i]['rp']} rank points."

        embed = discord.Embed(title="Rank leaderboard",
                              colour=discord.Colour(0xa72693),
                              description=description,
                              inline=True)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}",
                         icon_url=ctx.author.avatar_url_as(static_format="png"))
        # Send embed
        await ctx.send(content="Here you go!", embed=embed)

    @levelLB.command(name="here")
    async def levelLBHere(self, ctx, member: discord.Member = None):
        """
        Check where people are relative to each other! Not specifing a page will select the first page.
        """
        # Sort the dictionary into a list.
        member = member or ctx.author
        clans = pickle.load(open('data/clans.data', 'rb'))
        rankings = []
        description = ""
        for profile in clans[ctx.guild.id]['members']:
            try:
                rankings.append({'id': profile, 'rp': clans[ctx.guild.id]['members'][profile]['rp']})
            except KeyError:
                pass

        def getKey(item):
            return item['rp']

        rankings = sorted(rankings, reverse=True, key=getKey)

        # Add the top 5
        end = 5
        if len(rankings) < 5:
            end = len(rankings)
        for i in range(end):
            user = ctx.bot.get_user(rankings[i]['id'])
            description += f"**{i + 1}.** {user.name}#{user.discriminator} - {rankings[i]['rp']} rank points.\n"

        # Add member
        index = -1
        for i in range(len(rankings)):
            if rankings[i]['id'] == member.id:
                index = i
        if index <= 4:
            embed = discord.Embed(title=f"{ctx.guild.name} rank point leaderboard",
                                  colour=discord.Colour(0x009975),
                                  description=description,
                                  inline=True)
            embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format='png'))
            embed.set_footer(text=f"Requested by {ctx.author.display_name}",
                             icon_url=ctx.author.avatar_url_as(static_format="png"))
            await ctx.send(content="Here you go!", embed=embed)
            return
        description += "--==ME==--"
        for i in [index - 1, index, index + 1]:
            if i != len(rankings):
                user = ctx.bot.get_user(rankings[i]['id'])
                description += f"\n**{i + 1}.** {user.name}#{user.discriminator} - {rankings[i]['rp']} rank points."

        embed = discord.Embed(title="Rank leaderboard",
                              colour=discord.Colour(0x009975),
                              description=description,
                              inline=True)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}",
                         icon_url=ctx.author.avatar_url_as(static_format="png"))
        # Send embed
        await ctx.send(content="Here you go!", embed=embed)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        """
        Gives you rank points per message on a one minute cooldown.
        """
        if ctx.author.bot:
            return
        gainedRP = int(random.randint(1, 10) * self.rp_mult)
        profiles = pickle.load(open('data/profiles.data', 'rb'))
        try:
            if profiles[ctx.author.id]['timeOfNextEarn'] <= time.time():
                profiles[ctx.author.id]['rp'] += gainedRP
                profiles[ctx.author.id]['timeOfNextEarn'] = time.time() + 60
                remxp, rank = get_rank_from(profiles[ctx.author.id]['rp'])
                if profiles[ctx.author.id]['rank'] < rank:
                    profiles[ctx.author.id]['rank'] = rank

                    # Message Settings
                    # clanSetting
                    clans = pickle.load(open('data/clans.data', 'rb'))
                    # Sets channel id
                    try:
                        clanChannel = ctx.guild.get_channel(clans[ctx.guild.id]['options']['levels']['channel']).id
                        clanChannel = ctx.guild.get_channel(clans[ctx.guild.id]['options']['levels']['channel'])
                        clansSetting = "channel"
                    # They haven't set an option
                    except KeyError:
                        clanSetting = "any"
                    # They haven't set channel as their option
                    except TypeError:
                        clanSetting = clans[ctx.guild.id]['options']['levels']
                    # Channel doesn't exist
                    except AttributeError:
                        clanSetting = "disabled"

                    # userSetting
                    # Set's their option
                    try:
                        userSetting = profiles[ctx.author.id]['options']['levels']
                    # They haven't set an option
                    except KeyError:
                        userSetting = "any"

                    # Sends the correct message based on their settings
                    # Clan Setting is channel
                    if clanSetting == "channel":
                        if userSetting == "any":
                            # Attempts to send it via the channel
                            try:
                                await clanChannel.send(
                                    f"Congrats {ctx.author.mention}! You've earned enough rank points to rank up to rank {rank}!")
                            # If it can't find the channel or can't post there,
                            # It attempts to DM the user
                            except AttributeError or discord.errors.Forbidden:
                                try:
                                    await ctx.author.send(
                                        f"Congrats {ctx.author.mention}! You've earned enough rank points to rank up to rank {rank}!")
                                # If it can't do that, it just doesn't do anything
                                except discord.errors.Forbidden:
                                    pass
                        elif userSetting == "dm":
                            # Skips channel and tries to send it via dm
                            try:
                                await ctx.author.send(
                                    f"Congrats {ctx.author.mention}! You've earned enough rank points to rank up to rank {rank}!")
                            except discord.errors.Forbidden:
                                pass

                    # Clan Setting is Any
                    elif clanSetting == "any":
                        if userSetting == "any":
                            # Attempts to send it in the current channel
                            try:
                                await ctx.channel.send(
                                    f"Congrats {ctx.author.mention}! You've earned enough rank points to rank up to rank {rank}!")
                            # If that fails it attmpts a DM
                            except discord.errors.Forbidden:
                                try:
                                    await ctx.author.send(
                                        f"Congrats {ctx.author.mention}! You've earned enough rank points to rank up to rank {rank}!")
                                # Otherwise it passes
                                except discord.errors.Forbidden:
                                    pass
                        # Just DMs the user
                        elif userSetting == "dm":
                            try:
                                await ctx.author.send(
                                    f"Congrats {ctx.author.mention}! You've earned enough rank points to rank up to rank {rank}!")
                            except discord.errors.Forbidden:
                                pass

                    # Clan Setting is DM
                    elif clanSetting == "dm":
                        # Checks the user hasn't disabled it.
                        if userSetting in ["any", "dm"]:
                            # Tries to DM the user
                            try:
                                await ctx.author.send(
                                    f"Congrats {ctx.author.mention}! You've earned enough rank points to rank up to rank {rank}!")
                            except discord.errors.Forbidden:
                                pass

        # The user hasn't earnt any rp
        except KeyError:
            profiles[ctx.author.id] = {'rp': gainedRP, 'timeOfNextEarn': time.time() + 60, 'rank': 0}
        # Saves the user's rp
        pickle.dump(profiles, open('data/profiles.data', 'wb'))

    @commands.is_owner()
    @level.command(name='reset', hidden=True)
    async def resetLevel(self, ctx):
        """
        Resets All rp. Used when testing rate of earn
        """
        profiles = pickle.load(open('data/profiles.data', 'rb'))
        for profile in profiles:
            profiles[profile]['rp'] = 0
            profiles[profile]['timeOfNextEarn'] = 0
            profiles[profile]['rank'] = 0
        pickle.dump(profiles, open('data/profiles.data', 'wb'))
        await ctx.send("Reset all rp.")


def setup(bot):
    bot.add_cog(Levels(bot))
