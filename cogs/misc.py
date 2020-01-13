# Allows us to use d.py
import discord
from discord.ext import commands
import asyncio
# Allows us to get http data.
import requests
# Allows us to use random numbers and choices
import random

class Misc(commands.Cog):
    """
    The most random things.
    """
    def __init__(self,bot):
        self.bot = bot
        # Defines all avaliable units and their powers
        self.units = {'Archers':1,
                      'Shieldbearers':1,
                      'War Hounds':1,
                      'Hammer Throwers':1,
                      'Brute':2,
                      'Assassins':2,
                      'Thornguards':2,
                      'Bombot':1,
                      'Fortification':1,
                      'Freeze Trap':1,
                      'Battle Drummer':2,
                      'Plague Throwers':2,
                      'Catapult':3,
                      'Battle Wagon':3,
                      'Entangled Roots':1,
                      'Mindshrooms':1,
                      'Spider Nest':2,
                      'Earth Elemental':2,
                      'Untamed Beast':3,
                      'Stormcaller':3,
                      'Arcane Archer':1,
                      'Spire':1,
                      'Arcane Blades':1,
                      'Barrier Monk':2,
                      'Frost Wizard':2,
                      'Paladin':3,
                      'Death Knight':3,
                      'Wraiths':1,
                      'Plaguebearers':1,
                      'Faceless Knights':2,
                      'Emberfiend':2,
                      'Mind Corruptor':3}

    # Defines it as a command
    @commands.command(name="chuck")
    # Creates the function.
    # Multiline string below this is the command description and is used in the help command
    async def CheckNorris(self,ctx):
        """
        Chuck Norris doesn't need a description.
        """
        # The requests url
        url = "https://matchilling-chuck-norris-jokes-v1.p.rapidapi.com/jokes/random"

        # The header for the data we send
        headers = {
            'x-rapidapi-host': "matchilling-chuck-norris-jokes-v1.p.rapidapi.com",
            'x-rapidapi-key': "9c3cda4346mshd16877fb07c8b54p124221jsn9e522d232d5c",
            'accept': "application/json"
            }

        # Sends the request and get's the response
        response = requests.request("GET", url, headers=headers)

        # Display the response in a pretty embed.
        embed = discord.Embed(title="Chuck Norris!",
                              colour=discord.Colour(0xe77c10),
                              url=response.json()['url'],
                              description=f"{response.json()['value']}")

        embed.set_thumbnail(url=response.json()['icon_url'])
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url_as(static_format='png'))

        # Send the embed with no message
        await ctx.send(content="",embed=embed)

    @commands.command(name="army")
    async def createArmy(self,ctx):
        """
        Gives you 16 power worth of army. Randomly.
        """
        power = 0
        theArmy = []
        while power != 16:
            unit, cost = random.choice(list(self.units.items()))
            power += cost
            if power > 16:
                power -= cost
            else:
                theArmy.append(unit)

        msg = "> The Army:"
        for unit in theArmy:
            msg += f"\n{unit}"

        msg += f"\n> Total Power: {power}"
        await ctx.send(msg)

    @commands.command(name='tactic')
    async def displayTactic(self,ctx):
        """
        Shows and old tactic for you to try to make anew!
        """
        tacticId = random.randint(1,72)
        theFile = discord.File(fp=f"data/tactics/Screenshot_{tacticId}.jpg", filename="Tactic.jpg")
        await ctx.send(content="",file=theFile)

def setup(bot):
    bot.add_cog(Misc(bot))
