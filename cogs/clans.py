import discord
from discord.ext import commands
import asyncio
import time
import random
import cogs.checks as check
from data.data_handler import data_handler

#ranksRP = formula = [int(50*(i**1.5)+100*i+300) for i in range(50)]


class Clans(commands.Cog):
    """
    A server based XP system. Gives clans a way to compete plus allows them to check activity for their server.
    """
    def __init__(self, bot):
        self.bot = bot
        self.rp_mult = 1
        self.editingClan = []

    @commands.group(name = 'clan', invoke_without_command = True, aliases = ['c','C'])
    async def clan(self, ctx, *, clanID:str = None):
        """
        Displays info based on your clan stats.
        """
        profiles = data_handler.load("profiles")
        
        if clanID is None:
            try:
                clanID = profiles[str(ctx.author.id)]["Base"]["clanID"]
                if clanID is None:
                    await ctx.send("You aren't in a clan!")
                    return
            except KeyError:
                await ctx.send("An error occured. Please try again")

        clans = data_handler.load("clans")
        try:
            clan = clans[clanID]
        except KeyError:
            await ctx.send("That clan doesn't exist yet! Maybe you'll be it's High Constable?")
            return
        # Base Info
        page1 = discord.Embed(title = f"{clan['Base']['name']}",
                              colour = int(clan['Base']['colours'][clan['Base']['colour']], 16),
                              description = f"ID: `{clanID}`\nHigh Constable: {self.bot.get_user(clan['Members']['leaderID']).name}#{self.bot.get_user(clan['Members']['leaderID']).discriminator}")
        page1.set_thumbnail(url = clan["Base"]["icon"])
        page1.set_footer(text = f"Requested by {ctx.author.display_name}",
                         icon_url = ctx.author.avatar_url_as(static_format='png'))

        page1.add_field(name = "Description",
                        value = clan["Info"]["description"],
                        inline = False)
        page1.add_field(name = "Members",
                        value = f"{len(clan['Members']['commanderIDs'])}/50",
                        inline = False)
        page1.add_field(name = "Location",
                        value = clan["Info"]['location'],
                        inline = False)
        page1.add_field(name = "Capacity",
                        value = f"{len(clan['Members']['commanderIDs'])}/50",
                        inline = False)
        page1.add_field(name = "Days since creation",
                        value = f"{int((time.time() - clan['Info']['creationTime']) / (60 * 60 * 24))} days",
                        inline = False)

        message = await ctx.send(embed=page1)
        await message.add_reaction("⏪")
        await message.add_reaction("◀")
        await message.add_reaction("⏺️")
        await message.add_reaction("▶")
        await message.add_reaction("⏩")

        # Add Page 2
        page2 = discord.Embed(title = f"{clan['Base']['name']}",
                              colour = int(clan['Base']['colours'][clan['Base']['colour']], 16),
                              description = f"High Constable: {self.bot.get_user(clan['Members']['leaderID']).name}#{self.bot.get_user(clan['Members']['leaderID']).discriminator}")
        page2.set_thumbnail(url = clan["Base"]["icon"])
        page2.set_footer(text = f"Requested by {ctx.author.display_name}",
                         icon_url = ctx.author.avatar_url_as(static_format='png'))

        leaders = f"{profiles[str(clan['Members']['leaderID'])]['Base']['username']} - {profiles[str(clan['Members']['leaderID'])]['Achievements']['rating']}"
        for pID in clan['Members']['coLeaderIDs']:
            leaders += f"\n{profiles[str(clan['Members']['coLeaderIDs'][pID])]['Base']['Username']} - {profiles[str(clan['Members']['coLeaderIDs'])]['Achievements']['rating']}"
        page2.add_field(name = "Constables:",
                        value = constables,
                        inline = False)

        elders = ""
        for pID in clan['Members']['elderIDs']:
            elders += f"\n{profiles[str(clan['Members']['elderIDs'][pID])]['Base']['Username']} - {profiles[str(clan['Members']['elderIDs'])]['Achievements']['rating']}"
        page2.add_field(name = "Captains",
                        value = eldes,
                        inline = False)

        members = ""
        for pID in clan['Members']['memberIDs']:
            members += f"\n{profiles[str(clan['Members']['memberIDs'][pID])]['Base']['Username']} - {profiles[str(clan['Members']['memberIDs'])]['Achievements']['rating']}"
        page2.add_field(name = "Commanders",
                        value = members,
                        inline = False)

        # Add Page 3
        page3 = discord.Embed(title = f"{clan.name}",
                              colour = clan.colour,
                              description = f"High Constable: {self.bot.get_user(clan.highConstable).name}#{self.bot.get_user(clan.highConstable).discriminator}")
        page3.set_thumbnail(url = clan.icon)
        page3.set_footer(text = f"Requested by {ctx.author.display_name}",
                         icon_url = ctx.author.avatar_url_as(static_format='png'))

        page3.add_field(name = "Join Type",
                        value = f"{clan.joinType}",
                        inline = False)
        page3.add_field(name = "Rank Requirement",
                        value = f"{clan.rankRequirement}",
                        inline = False)
        page3.add_field(name = "Rating Requirement",
                        value = f"{clan.ratingRequirement}",
                        inline = False)

        pages = [page1, page2, page3]
        page = 0

        while True:
            def check(reaction, user):
                if user.bot == True:
                    return False
                if reaction.message.id != message.id:
                    return False
                reactions = ['⏪', '◀', '⏺️', '▶', '⏩']
                return user.id == ctx.author.id and str(reaction) in reactions
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                break
            reaction = str(reaction)
            if reaction == '⏺️':
                while True:
                    newclanID = random.choice(list(clans))
                    if newclanID != clanID:
                        clanID = newclanID
                        break
                clan = clans[clanID]
                page1 = discord.Embed(title = f"{clan.name}",
                                      colour = clan.colour,
                                      description = f"High Constable: {self.bot.get_user(clan.highConstable).name}#{self.bot.get_user(clan.highConstable).discriminator}")
                page1.set_thumbnail(url = clan.icon)
                page1.set_footer(text = f"Requested by {ctx.author.display_name}",
                                 icon_url = ctx.author.avatar_url_as(static_format='png'))

                page1.add_field(name = "Description",
                                value = clan.description,
                                inline = False)
                page1.add_field(name = "Total RP",
                                value = f"{clan.totalRP()}",
                                inline = False)
                page1.add_field(name = "Level",
                                value = f"{clan.level}",
                                inline = False)
                page1.add_field(name = "Mascot",
                                value = clan.mascot,
                                inline = False)
                page1.add_field(name = "Days since creation",
                                value = f"{int((time.time() - clan.creationTime) / (60 * 60 * 24))} days",
                                inline = False)
                # Add Page 2
                page2 = discord.Embed(title = f"{clan.name}",
                                      colour = clan.colour,
                                      description = f"High Constable: {self.bot.get_user(clan.highConstable).name}#{self.bot.get_user(clan.highConstable).discriminator}")
                page2.set_thumbnail(url = clan.icon)
                page2.set_footer(text = f"Requested by {ctx.author.display_name}",
                                 icon_url = ctx.author.avatar_url_as(static_format='png'))
                # Format constables better
                page2.add_field(name = "Constables:",
                                value = f"{clan.constableIDs}",
                                inline = False)
                # Format Captains better
                page2.add_field(name = "Captains",
                                value = f"{clan.captainIDs}",
                                inline = False)
                page2.add_field(name = "Commanders",
                                value = f"{clan.commanderIDs}",
                                inline = False)

                # Add Page 3
                page3 = discord.Embed(title = f"{clan.name}",
                                      colour = clan.colour,
                                      description = f"High Constable: {self.bot.get_user(clan.highConstable).name}#{self.bot.get_user(clan.highConstable).discriminator}")
                page3.set_thumbnail(url = clan.icon)
                page3.set_footer(text = f"Requested by {ctx.author.display_name}",
                                 icon_url = ctx.author.avatar_url_as(static_format='png'))

                page3.add_field(name = "Join Type",
                                value = f"{clan.joinType}",
                                inline = False)
                page3.add_field(name = "Rank Requirement",
                                value = f"{clan.rankRequirement}",
                                inline = False)
                page3.add_field(name = "Rating Requirement",
                                value = f"{clan.ratingRequirement}",
                                inline = False)

                pages = [page1, page2, page3]
                page = 0
            elif reaction == '⏪':
                page = 0
            elif reaction == '◀':
                page -= 1
                if page < 0:
                    page = 0
            elif reaction == '▶':
                page += 1
                if page >= 3:
                    page = 2
            elif reaction == '⏩':
                page = 2

            await message.edit(embed=pages[page])

    @commands.is_owner()
    @clan.command(name='create')
    async def createClan(self, ctx, *, name:str = None):
        # TODO - Allow to edit clan straight away?
        if name is None:
            await ctx.send("Please specify a clan name.")
            return
        clans = data_handler.load("clans")
        profiles = data_handler.load("profiles")
        try:
            clan = clans[name]
            await ctx.send("A clan already exists with that name! Pick something else.")
            return
        except KeyError:
            if profiles[ctx.author.id].clan is not None:
                await ctx.send("You're already in a clan! Leave that first!")
                return
            profiles[str(ctx.author.id)].clan = name
        
        await ctx.send("Clan created. Congratulations on becoming a High Constable! Use `b!clan edit` to setup your clan!")

        data_handler.dump(clans, "clans")
        data_handler.dump(profiles, "profiles")

    @clan.command(name='join')
    async def joinClan(self, ctx, *, clanName:str = None):
        # TODO - Check against invites
        # TODO - Ask for password using wait_for
        clans = data_handler.load("clans")
        profiles = data_handler.load("profiles")
        try:
            clan = clans[clanName]
        except KeyError:
            await ctx.send("That clan doesn't exist!")
            return
        if clan.joinType == "closed":
            await ctx.send("That clan is currently closed to new members.")
            return
        if profiles[ctx.author.id].clan is not None:
            await ctx.send("You are already in a clan! Please leave that one first!")
            return
        try:
            clan.addMember(ctx.author.id)
            profiles[ctx.author.id] = clanName
        except AttributeError:
            await ctx.send("That clan has too many members! You can't join them.")
            return
        
        await ctx.send(f"You have joined {clanName}.")
        data_handler.dump(clans, "clans")
        data_handler.dump(profiles, "profiles")

    @clan.command(name='edit')
    async def editClan(self, ctx):
        # Checks if they are editing thier clan.
        if ctx.author.id in self.editingClan:
            await ctx.send("You are already editing your clan!")
            return

        # Sets the description. Placed seperate for easy editing.
        description = """`description` - Change the clan description.
`discord` - Add a discord invite.
`icon` - Change the clan icon.
`advertise` - Set a new advertisement message.
`colour` - Set the clan colour.
`type` - Change the join type
`requirements` - Change the join requirements
`mascot` - Change the clan mascot.
"""

    @commands.is_owner()
    @clan.command(name='reset', hidden = True)
    async def resetClans(self, ctx):
        """
        Resets all clan RP.
        """
        clans = {}
        data_handler.dump(clans, "clans")
        await ctx.send("Clans reset.")

    @commands.is_owner()
    @clan.command(name='fix', hidden = True)
    async def fixClans(self, ctx):
        clans = data_handler.load("clans")
        clans = {}
        data_handler.dump(clans, "clans")
        
    @commands.is_owner()
    @commands.command(name='servers', hidden = True)
    async def clans(self, ctx):
        await ctx.send(f"I am in {len(self.bot.guilds)} servers.")
        print(self.bot.guilds)

def setup(bot):
    bot.add_cog(Clans(bot))
