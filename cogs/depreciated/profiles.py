import discord
from discord.ext import commands
import asyncio
import pickle
import time
import datetime
import asyncio

ranksRP = [int(5*(i**1.5)+50*i+100) for i in range(50)]

def get_rank_from(rp):
    remRP = int(rp)
    rank = 0
    while remRP >= ranksRP[rank]:
        remRP -= ranksRP[rank]
        rank += 1
    return remRP, rank

class Profiles(commands.Cog):
    """
    Info about yourself or other users. Will use Battle Legion API to check stats when added.
    """
    def __init__(self, bot):
        self.bot = bot
        self.valid_elements = ['unit', 'rating', 'account', 'clan', 'tactic', 'lord', 'squire']

    @commands.group(name='profile',invoke_without_command=True)
    async def profile(self,ctx,member:discord.Member=None):
        """
        Base profile command
        Check your profile or that of another member's. Leave the member argument blank to select yourself.
        """
        member = member or ctx.author
        profiles = pickle.load(open('data/profiles.data','rb'))
        embed = discord.Embed(title=f"{member.display_name}'s profile",
                              colour=member.colour,
                              description=f"{member.name}#{member.discriminator}")

        embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
        embed.set_footer(text=f"Requested by {ctx.author.display_name}",
                         icon_url=ctx.author.avatar_url_as(static_format='png'))

        try:
            account = profiles[member.id]['account']
        except KeyError:
            account = "`N/A`"
        try:
            clan = profiles[member.id]['clan']
        except KeyError:
            clan = "`N/A`"
        embed.add_field(name="Base info:",
                        value=f"Primary account: {account} \nClan: {clan}")
        
        try:
            remRP, Rank = get_rank_from(profiles[member.id]['rp'])
            embed.add_field(name="Level Info:",
                            value=f"Rank: {Rank}\nTotal RP: {profiles[member.id]['rp']}")
        except KeyError:
            embed.add_field(name='Level Info:',value="Rank: 0\nTotal RP: 0")

        try:
            squire = profiles[member.id]['squire']
        except KeyError:
            squire = "`N/A`"
        try:
            lord = profiles[member.id]['lord']
        except KeyError:
            lord = "`N/A`"
        try:
            rating = profiles[member.id]['rating']
        except KeyError:
            rating = "`N/A`"
        try:
            days = int(int(time.time() - (member.joined_at - datetime.datetime.utcfromtimestamp(0)).total_seconds())/86400)
            server_date = f"{member.joined_at.ctime()} ({days} days ago)"
        except KeyError:
            print("How tf did I get this!?")
        try:
            days = int(int(time.time() - (member.created_at - datetime.datetime.utcfromtimestamp(0)).total_seconds())/86400)
            discord_date = f"{member.created_at.ctime()} ({days} days ago)"
        except KeyError:
            print("wft?")
        embed.add_field(name="Some Stats:",
                        value=f"Amount of Lord titles: {lord} \nAmount of Squire titles: {squire} \nBest :trophy: rating: {rating} \nJoined Discord on: {discord_date} \nJoined server on: {server_date}")

        try:
            unit = profiles[member.id]['unit']
        except KeyError:
            unit = "`N/A`"
        try:
            tactic = profiles[member.id]['tactic']
        except KeyError:
            tactic = "`N/A`"
        embed.add_field(name='Fun Favourites:',
                        value=f"Favourite unit: {unit} \nFavourite Tactic: {tactic}")

        await ctx.send(content="",embed=embed)

    @profile.command(name="set")
    async def profileSet(self,ctx,element:str=None,*,value:str=None):
        """
        Modifies elements of your profile. Leave the element argument blank to see possible arguments.
        """
        if element not in self.valid_elements:
            await ctx.send("Please select a valid element. Valid elements are: \n`unit` - favourite unit, \n`rating` - top rating achieved (also set with `b!rank set`), \n`account` - Name of account,\n`clan` - Name of you current clan, \n`tactic` - Favourite tactic type, \n`lord` - amount of lord titles. \n`squire` - amount of squire titles.")
            return
        value = value or "`N/A`"
        profiles = pickle.load(open('data/profiles.data','rb'))
        if element in ["rating",'lord']:
            value = int(value)
        profiles[ctx.author.id][element] = value
        pickle.dump(profiles,open('data/profiles.data','wb'))
        await ctx.send(f"`{element}` has been set to `{value}`.")

    @commands.is_owner()
    @profile.command(name="reset",hidden=True)
    async def profileReset(self,ctx):
        """
        Resets all profiles. Do not use unless needed.
        """
        profiles = {}
        pickle.dump(profiles,(open('data/profiles.data','wb')))
        await ctx.send("Deleted all profiles.")

    @commands.is_owner()
    @profile.command(name="fix",hidden=True)
    async def profileFix(self,ctx):
        """
        Must be rewritten each time. Fixes a bug with data.
        """
        profiles = pickle.load(open('data/profiles.data','rb'))
        for profile in profiles:
            try:
                profiles[profile]['rating'] = int(profiles[profile]['rating'])
            except KeyError:
                pass
            except ValueError:
                profiles[profile]['rating'] = 0
        pickle.dump(profiles,(open('data/profiles.data','wb')))
        await ctx.send("Deleted all accounts. They will now have to re input their data.")
        time.sleep(30)
        await ctx.send("Fixed the bug. Accounts restored.")

def setup(bot):
    bot.add_cog(Profiles(bot))
