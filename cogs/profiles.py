import discord
from discord.ext import commands
import time
import random
import datetime
import asyncio
import json


class Profiles(commands.Cog):

    # Initialises the variables and sets the bot.
    def __init__(self, bot):
        self.bot = bot
        self.rp_mult = 1

    # Our base level command. Due to invoke_without_command=True it means that this command is only run when no
    # sub-command is run. Makes it a command group with a name.
    @commands.group(name='profile', invoke_without_command = True, aliases = ['p'])
    # Defines it as a function.
    async def profile(self, ctx, *, userName:str = None):
        """
        Check your profile or that of another member.
        You no longer need to mention the user to check their profile!
        """
        if userName is None:
            userName = ctx.author.name
        user = discord.utils.find(lambda u: u.name.startswith(userName), self.bot.users)
        profiles = json.load(open('data/profiles.json'))
        try:
            player = profiles[str(user.id)]
        except KeyError:
            await ctx.send("That person doesn't have a profile yet. Get them to send a message and I'll make one!")
            return
        except AttributeError:
            await ctx.send("I don't know that Discord User.")
            return

        clans = json.load(open('data/clans.json'))
        # Base Info
        page1 = discord.Embed(title = f"{user.display_name}'s profile",
                              colour = int(player['Settings']['colours'][player['Settings']['colour']], 16),
                              description = f"{user.name}#{user.discriminator}")
        page1.set_thumbnail(url = user.avatar_url_as(static_format = 'png'))
        page1.set_footer(text = f"Requested by {ctx.author.display_name}",
                         icon_url = ctx.author.avatar_url_as(static_format='png'))

        page1.add_field(name = "Base Info",
                        value = f"Account Name: {player['Base']['username']} \nClan: {clans[player['Base']['clanID']]['Base']['name']} \nCountry: {player['Base']['country']}",
                        inline = False)
        page1.add_field(name = "Level Info",
                        value = f"Rank: {player['Level']['rank']} \nTotal Rank Points: {player['Level']['rp']}",
                        inline = False)

        message = await ctx.send(embed=page1)
        await message.add_reaction("⏪")
        await message.add_reaction("◀")
        await message.add_reaction("⏺️")
        await message.add_reaction("▶")
        await message.add_reaction("⏩")

        member = discord.utils.find(lambda g: g.get_member(user.id), self.bot.guilds).get_member(user.id)

        # Add Page 2
        page2 = discord.Embed(title = f"{user.display_name}'s profile",
                              colour = int(player['Settings']['colours'][player['Settings']['colour']], 16),
                              description = f"{user.name}#{user.discriminator}")
        page2.set_thumbnail(url = user.avatar_url_as(static_format = 'png'))
        page2.set_footer(text = f"Requested by {ctx.author.display_name}",
                         icon_url = ctx.author.avatar_url_as(static_format='png'))

        page2.add_field(name = "Achievements",
                        value = f"Amount of Lord titles: {player['Achievements']['lords']} \nAmount of Squire titles: {player['Achievements']['squires']} \nBest :trophy: rating: {player['Achievements']['rating']}",
                        inline=False)
        page2.add_field(name = "Fun Favourites",
                        value=f"Favourite unit: {player['Favourites']['unit']} \nFavourite Tactic: {player['Favourites']['tactic']} \nFavourite Tome: {player['Favourites']['tome']} \nFavourite Skin: {player['Favourites']['skin']}",
                        inline=False)

        # Add Page 3
        page3 = discord.Embed(title = f"{user.display_name}'s profile",
                              colour = int(player['Settings']['colours'][player['Settings']['colour']], 16),
                              description = f"{user.name}#{user.discriminator}")
        page3.set_thumbnail(url = user.avatar_url_as(static_format = 'png'))
        page3.set_footer(text = f"Requested by {ctx.author.display_name}",
                         icon_url = ctx.author.avatar_url_as(static_format='png'))

        days = int(int(time.time() - (member.created_at - datetime.datetime.utcfromtimestamp(0)).total_seconds())/86400)
        discord_date = f"{member.created_at.ctime()} ({days} days ago)"

        page3.add_field(name = "Discord Info",
                        value = f"Joined Discord on: {discord_date} \nStatus: {member.status} \nid: `{member.id}` \nAvatar Link: {member.avatar_url_as(format='png')}")

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
                print(profiles)
                playerID = random.choice(list(profiles))
                while playerID == user.id:
                    playerID = random.choice(list(profiles))
                user = await self.bot.fetch_user(playerID)
                player = profiles[playerID]
                while True:
                    try:
                        member = discord.utils.find(lambda g: g.get_member(user.id), self.bot.guilds).get_member(user.id)
                        break
                    except AttributeError:
                        pass
                page1 = discord.Embed(title = f"{user.display_name}'s profile",
                                      colour = player.colour,
                                      description = f"{user.name}#{user.discriminator}")
                page1.set_thumbnail(url = user.avatar_url_as(static_format = 'png'))
                page1.set_footer(text = f"Requested by {ctx.author.display_name}",
                                 icon_url = ctx.author.avatar_url_as(static_format='png'))

                page1.add_field(name = "Base Info",
                                value = f"Account Name: {player.accountName} \nClan: {player.clan} \nCountry: {player.country}",
                                inline = False)
                page1.add_field(name = "Level Info",
                                value = f"Rank: {player.rank} \nTotal Rank Points: {player.rp}",
                                inline = False)
                # Add Page 2
                page2 = discord.Embed(title = f"{user.display_name}'s profile",
                                      colour = player.colour,
                                      description = f"{user.name}#{user.discriminator}")
                page2.set_thumbnail(url = user.avatar_url_as(static_format = 'png'))
                page2.set_footer(text = f"Requested by {ctx.author.display_name}",
                                 icon_url = ctx.author.avatar_url_as(static_format='png'))

                page2.add_field(name = "Achievements",
                                value = f"Amount of Lord titles: {player.lords} \nAmount of Squire titles: {player.squires} \nBest :trophy: rating: {player.rating}",
                                inline=False)
                page2.add_field(name = "Fun Favourites",
                                value=f"Favourite unit: {player.favourites['unit']} \nFavourite Tactic: {player.favourites['tactic']} \nFavourite Tome: {player.favourites['tome']} \nFavourite Skin: {player.favourites['skin']}",
                                inline=False)

                # Add Page 3
                page3 = discord.Embed(title = f"{user.display_name}'s profile",
                                      colour = player.colour,
                                      description = f"{user.name}#{user.discriminator}")
                page3.set_thumbnail(url = user.avatar_url_as(static_format = 'png'))
                page3.set_footer(text = f"Requested by {ctx.author.display_name}",
                                 icon_url = ctx.author.avatar_url_as(static_format='png'))

                days = int(int(time.time() - (member.created_at - datetime.datetime.utcfromtimestamp(0)).total_seconds())/86400)
                discord_date = f"{member.created_at.ctime()} ({days} days ago)"

                page3.add_field(name = "Discord Info",
                                value = f"Joined Discord on: {discord_date} \nStatus: {member.status} \nid: `{member.id}` \nAvatar Link: {member.avatar_url_as(format='png')}")

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

    @profile.command(name="set")
    async def setProfile(self, ctx, attribute, *, value):
        try:
            """
            Change values on your profile. You can change:
            `name`, `country`, `lords`, `squires`, `rating`, `unit`, `tactic`, `tome`, `skin`.
            """
            profiles = pickle.load(open('data/profiles.data', 'rb'))
            player = profiles[ctx.author.id]
            attribute = attribute.lower()

            if attribute in ["lords", "lord"]:
                if str(value)[0] == "+":
                    player.lords += int(value)
                else:
                    player.lords = int(value)
            elif attribute in ["squires", "squire"]:
                if str(value)[0] == "+":
                    player.squires += int(value) 
                else:
                    player.squires = int(value)
            elif attribute in ["rating"]:
                player.rating = int(value)
            elif attribute in ["unit", "units", "troop"]:
                player.favourites['unit'] = value
            elif attribute in ["tactic", "strategy", "layout"]:
                player.favourites['tactic'] = value
            elif attribute in ["tome", "masteryskill", "book"]:
                player.favourites['tome'] = value
            elif attribute in ["skin", "look"]:
                player.favourites['skin'] = value
            elif attribute in ["country", "location"]:
                player.country = value
            elif attribute in ["name", "accountname", "account"]:
                player.accountName = value
            else:
                await ctx.send("This is not a valid setting. Check your profile for valid settings.")
                return
        except ValueError:
            await ctx.send("Invalid Value. Please choose a number.")
        except:
            await ctx.send("An Error occured. Please report this on the support server.")
        else: 
            await ctx.send("Profile updated.")
            pickle.dump(profiles, open('data/profiles.data', 'wb'))


    @profile.command(name='colour', aliases = ['color'])
    async def changeProfileColour(self, ctx, colour:int = None):
        """
        Allows you to change the colour of all your profile based information!
        """
        profiles = pickle.load(open('data/profiles.data', 'rb'))
        try:
            player = profiles[ctx.author.id]
        except:
            await ctx.send("An error occured. Please try again.")
            return
        colourList = list(player.colours)

        if colour is None or colour >= len(player.colours) or colour < 0:
            description = "Unlocked Colours:"
            for colourIndex in range(len(colourList)):
                description = description + f"\n{colourIndex}. {colourList[colourIndex]}"
            embed = discord.Embed(title = "Please select a valid colour.",
                                  colour = player.colour,
                                  description = description)
            embed.set_footer(text = f"Requested by {ctx.author.display_name}",
                             icon_url = ctx.author.avatar_url_as(static_format='png'))
            await ctx.send(embed=embed)
            return

        player.colour = player.colours[colourList[colour]]

        profiles[ctx.author.id] = player
        pickle.dump(profiles, open('data/profiles.data', 'wb'))
        await ctx.send("Updated your colour.")

##    @commands.Cog.listener()
##    async def on_message(self, ctx):
##        """
##        Gives you rank points per message on a one minute cooldown.
##        """
##        if ctx.author.bot:
##            return
##        profiles = json.load(open('data/profiles.json', 'rb'))
##        try:
##            player = profiles[ctx.author.id]
##        except KeyError:
##            profiles[ctx.author.id] = PlayerPY.Player(ctx.author.display_name)
##            player = profiles[ctx.author.id]
##
##        cooldown, rankedUp, rank = player.gainedRP()
##        if cooldown:
##            return
##
##        if rankedUp and player.rankUpMessage in ['any','dm']:
##            if player.rankUpMessage == "any":
##                destination = ctx.channel
##            elif player.rankUpMessage == "dm":
##                destination = ctx.author
##            await destination.send(f"Congrats {ctx.author.mention}! You've earned enough rank points to rank up to rank {rank}!")
##            if rank == 1:
##                await destination.send("You've also unlocked a new colour: Rank 1!")
##                player.addColour("Rank 1", 0xfefefe)
##            elif rank == 5:
##                await destination.send("You've also unlocked a new colour: Rank 5!")
##                player.addColour("Rank 5", 0x7af8d3)
##            elif rank == 10:
##                await destination.send("You've also unlocked a new colour: Level 10!")
##                player.addColour("Rank 10", 0x327c31)
##
##        pickle.dump(profiles, open('data/profiles.data', 'wb'))

##    @profile.group(name="leaderboard", aliases=["lb"], invoke_without_command = True)
##    async def levelLB(self, ctx, member: discord.Member = None):
##        """
##        Check where people are relative to each other! Not specifying a page will select the first page.
##        """
##        # Sort the dictionary into a list.
##        member = member or ctx.author
##        profiles = pickle.load(open('data/profiles.data', 'rb'))
##        rankings = []
##        description = ""
##        for profile in profiles:
##            try:
##                rankings.append({'id': profile, 'rp': profiles[profile]['rp']})
##            except KeyError:
##                pass
##
##        def getKey(item):
##            return item['rp']
##
##        rankings = sorted(rankings, reverse = True, key = getKey)
##
##        # Add the top 5
##        end = 5
##        if len(rankings) < 5:
##            end = len(rankings)
##        for i in range(end):
##            user = await ctx.bot.fetch_user(rankings[i]['id'])
##            description += f"**{i + 1}.** {user.name}#{user.discriminator} - {rankings[i]['rp']} rank points.\n"
##
##        # Add member
##        index = -1
##        for i in range(len(rankings)):
##            if rankings[i]['id'] == member.id:
##                index = i
##        if index <= 4:
##            embed = discord.Embed(title="Global rank point leaderboard",
##                                  colour=discord.Colour(0xa72693),
##                                  description=description,
##                                  inline=True)
##            embed.set_footer(text=f"Requested by {ctx.author.display_name}",
##                             icon_url=ctx.author.avatar_url_as(static_format="png"))
##            await ctx.send(content="Here you go!", embed=embed)
##            return
##        description += "--==ME==--"
##        for i in [index - 1, index, index + 1]:
##            if i != len(rankings):
##                user = await ctx.bot.fetch_user(rankings[i]['id'])
##                description += f"\n**{i + 1}.** {user.name}#{user.discriminator} - {rankings[i]['rp']} rank points."
##
##        embed = discord.Embed(title="Rank leaderboard",
##                              colour=discord.Colour(0xa72693),
##                              description=description,
##                              inline=True)
##        embed.set_footer(text=f"Requested by {ctx.author.display_name}",
##                         icon_url=ctx.author.avatar_url_as(static_format="png"))
##        # Send embed
##        await ctx.send(content="Here you go!", embed=embed)
##
##    @levelLB.command(name="here")
##    async def levelLBHere(self, ctx, member: discord.Member = None):
##        """
##        Check where people are relative to each other! Not specifing a page will select the first page.
##        """
##        # Sort the dictionary into a list.
##        member = member or ctx.author
##        clans = pickle.load(open('data/clans.data', 'rb'))
##        rankings = []
##        description = ""
##        for profile in clans[ctx.guild.id]['members']:
##            try:
##                rankings.append({'id': profile, 'rp': clans[ctx.guild.id]['members'][profile]['rp']})
##            except KeyError:
##                pass
##
##        def getKey(item):
##            return item['rp']
##
##        rankings = sorted(rankings, reverse = True, key = getKey)
##
##        # Add the top 5
##        end = 5
##        if len(rankings) < 5:
##            end = len(rankings)
##        for i in range(end):
##            user = ctx.bot.get_user(rankings[i]['id'])
##            description += f"**{i + 1}.** {user.name}#{user.discriminator} - {rankings[i]['rp']} rank points.\n"
##
##        # Add member
##        index = -1
##        for i in range(len(rankings)):
##            if rankings[i]['id'] == member.id:
##                index = i
##        if index <= 4:
##            embed = discord.Embed(title=f"{ctx.guild.name} rank point leaderboard",
##                                  colour=discord.Colour(0x009975),
##                                  description=description,
##                                  inline=True)
##            embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format='png'))
##            embed.set_footer(text=f"Requested by {ctx.author.display_name}",
##                             icon_url=ctx.author.avatar_url_as(static_format="png"))
##            await ctx.send(content="Here you go!", embed=embed)
##            return
##        description += "--==ME==--"
##        for i in [index - 1, index, index + 1]:
##            if i != len(rankings):
##                user = ctx.bot.get_user(rankings[i]['id'])
##                description += f"\n**{i + 1}.** {user.name}#{user.discriminator} - {rankings[i]['rp']} rank points."
##
##        embed = discord.Embed(title="Rank leaderboard",
##                              colour=discord.Colour(0x009975),
##                              description=description,
##                              inline=True)
##        embed.set_footer(text=f"Requested by {ctx.author.display_name}",
##                         icon_url=ctx.author.avatar_url_as(static_format="png"))
##        # Send embed
##        await ctx.send(content="Here you go!", embed = embed)

    @commands.is_owner()
    @profile.command(name = 'reset', hidden = True)
    async def resetLevel(self, ctx):
        """
        Resets All rp. Used when testing rate of earn
        """
        profiles = {}
        profiles[270190067354435584] = PlayerPY.Player("Greenfoot5")
        pickle.dump(profiles, open('data/profiles.data', 'wb'))
        await ctx.send("Reset all profiles.")

    @commands.is_owner()
    @profile.command(name = 'fix', hidden = True)
    async def fixData(self, ctx):
        """
        Custom command to repair or fix the data.
        """
        profiles = pickle.load(open('data/profiles.data', 'rb'))
        for profileID in profiles:
            if 'Rank 1' in profiles[profileID].colours:
                profiles[profileID].colours['Rank 1'] = 0xfefefe
        print(profiles)
        pickle.dump(profiles, open('data/profiles.data', 'wb'))
        await ctx.send("Fixed Data.")

    
        

def setup(bot):
    bot.add_cog(Profiles(bot))
