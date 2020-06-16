import discord
from discord.ext import commands
import asyncio

class Responses(commands.Cog):
    def __init__(self,bot):
        # Allows us to reference the bot
        self.bot = bot

    @commands.group(name="response", aliases=["r"], invoke_without_command=True)
    async def responseBase(self, ctx):
        "Select from a plethora of responses so you don't have to keep typing the same thing over and over again!"
        await ctx.send("Please select a valid reponse.", delete_after=10)

    @responseBase.command(name="tactic", aliases=["army"])
    async def tacticHelp(self, ctx):
        """
        If someone hasn't given enough information when asking for tactic help, send them this.
        """
        await ctx.send("""You haven't given us enough to work with. If you want help with your armies, people will help you. The first thing we'll need is a picture of your army. We can't improve it if we don't know what it is. After that, there's a few things that can help you receive support:
• Your rank/rating
• Unit levels (shown in the screenshot is best)
• What you're struggling against.
You will likely not get support if you do the following:
• Ask what the best army is in x rank (there is none).
• Ask for tips with no context.
• Telling us your stuck, but not actually giving us any info to help you with.
• Ask us to make you an army.
We can't help you, if you can't help us.""")

    @responseBase.command(name="support")
    async def getSupport(self, ctx):
        """
        Useful when someone needs to contact support via a ticket.
        """
        await ctx.send("""This looks like an issue that would be best to contact support in-game.
"Settings" => "Support" => Use the browser window that opens to submit a ticket.

Common reasons to use a ticket:
• Devs can get game/device information
• You're crashing or freezing
• It's something the team are looking into.
• The bug is specific to your device.
• It's a personal issue (personal details cannot be share on Discord, Traplight policy)""")

    @responseBase.command(name="notabug", aliases=["nab"])
    async def NotABug(self, ctx):
        "Lists the most common issues that aren't bugs."
        await ctx.send("""The following are not bugs or Traplight is already aware of the issue:
• "Units from Mind Corrupted units are on the wrong side."
All spawned units from a unit, spawn allied to the side the spawner is on. If the spawner swaps sides, so does the spawned units (DK+skeletons, Golem+Golemites etc.)
• "A player is using units from a higher rank!"
This is because the ranking system was changed. Traplight are currently trying to fix the issue.""")

    @responseBase.command(name="requested", aliases=["fr"])
    async def FrequentlyRequested(self, ctx):
        "For frequently requested features."
        await ctx.send("""The following are highly requested features:
• Name changes. Traplight would like to do this, not currently working on it.
• Fight a friend. Friendly battles in a clan/against friends are highly requested, and Traplight would like to work on it.
• Friends. Traplight would like to work on this, not currently in development though.
• When can you release to x country? Android has global release, iOS is being worked on.
• Clan Wars. Already planned.
• Use of spells/influence a battle. Unlikely to happen as the defender (your opponent) isn't watching and it would give attacker's an advantage.""")

    @responseBase.command(name="deathknight", aliases=["dk"])
    async def DeathKnightOP(self, ctx):
        "If someone's complaining about Death Knight being OP, send them this."
        await ctx.send("""Death Knight is powerful, but only because it brings forth a whole different style of play that people aren't expecting, or knowledgeable about. Here's some things you can do to help win:
• Use a drummer. The #1 piece of advice. Swarms (those that use DK) rely on melee damage to win. If you use a drummer, you heavily reduce the melee damage they deal.
• AoE units. Units like Earth Elemental, Faceless Knights, Brute are all great counters as they deal AoE damage to the swarm.
• Hammer Throwers > Archers. Their projectile is far superior and will miss much less than archers. (May not be true against other squads though)
• Spires and bombs also work. Spires can target multiple units and bombs deal massive AoE damage in one go.
• Thornguards (+ drummer) will destroy most of an incoming swarm.
Hopefully these counters help you win. If you're still struggling, ask for help, people like to help others.""")

    @responseBase.command(name="pinned", aliases=["pins", "pin"])
    async def ReadThePins(self, ctx):
        "If someone hasn't read the pinned messages, try sending them this."
        await ctx.send("https://i.imgur.com/YrnVuCd.jpg")


# Sets up the cog. Called when loading the file
def setup(bot):
    bot.add_cog(Responses(bot))
    
