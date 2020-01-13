import discord
from discord.ext import commands
import pickle
import asyncio

class Ranking(commands.Cog):
    """
    Check plays top recorded rating! How high have you really climbed?
    """
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(name='rank',invoke_without_command=True)
    async def Rank(self,ctx,member:discord.Member=None):
        """
        Base rank command.
        Displays the top ratching achieved by yourself or another member. They need to set it first though.
        """
        member = member or ctx.author
        profiles = pickle.load(open('data/profiles.data','rb'))
        try:
            await ctx.send(f"{member.name}#{member.discriminator} has {profiles[member.id]['rating']} as their highest trophy count.")
        except KeyError:
            await ctx.send(f"{member.name}#{member.discriminator} hasn't set a top trophy count yet.")
        

    @Rank.command(name="set")
    async def RankSet(self,ctx,value:int=0):
        """
        Sets your rank. Leaving it blank will reset it to 0.
        """
        profiles = pickle.load(open('data/profiles.data','rb'))
        try:
            profiles[ctx.author.id]['rating'] = value
        except KeyError:
            print(profiles)
            return
        pickle.dump(profiles,(open('data/profiles.data','wb')))
        await ctx.send(f"Set your best ranking to {value}.")

    @Rank.command(name="leaderboard",aliases=["lb"])
    async def RankLB(self,ctx,page:int=1):
        """
        Check where people are relative to each other! Not specifing a page will select the first page.
        """
        if page < 1:
            page = 1
        #Sort the dictionary into a list.
        profiles = pickle.load(open('data/profiles.data','rb'))
        rankings = []
        for profile in profiles:
            try:
                rankings.append({'id':profile,'rating':profiles[profile]['rating']})
            except KeyError:
                pass
        def getKey(item):
            return item['rating']
        rankings = sorted(rankings,reverse=True,key=getKey)
        #Make sure it doesn't exceed maximum page.
        if page-1 > (len(rankings)//5):
            page = len(rankings)//5
            
        # Create the embed
        embed = discord.Embed(title="Top players",
                              colour=discord.Colour(0x20d4c0),
                              description="Check out the top players!",
                              inline=True)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}",
                         icon_url=ctx.author.avatar_url_as(static_format="png"))
        if (page*5) >= len(rankings):
            end = len(rankings)
        else:
            end = (page*5)
        for i in range(((page*5)-5),end):
            member = ctx.bot.get_user(rankings[i]['id'])
            embed.add_field(name=f"{i+1}. {member.name}#{member.discriminator}",
                            value=f"**{rankings[i]['rating']}** :trophy:(s).")
        await ctx.send(content="Here you go!",embed=embed)
        
def setup(bot):
    bot.add_cog(Ranking(bot))
