import discord
import time
import random
import datetime
import asyncio
import json
import config

from discord.ext import commands
from data.data_handler import data_handler
from itertools import chain
from collections import OrderedDict

def gainedRP(player, gained_rp):
    if player['Level']['timeOfNextEarn'] > time.time():
        return True, False, player['Level']['rank']
    
    rank = get_rank_from(player['Level']['rp'] + gained_rp)

    if rank > player['Level']['rank']:
        return False, True, rank

    return False, False, rank

# Function to get a user's rank and remaining rp to next rank.
# Takes current rp as parameter
def get_rank_from(rp):
    # Sets the starting value to be our remaining rp
    rem_rp = int(rp)
    # Starts the rank at 0
    rank = 0
    # Loops throught the ranks and checks if the user had enough rp to rank up
    # If so, take that rp away from rem_rp and add one to their rank
    while rem_rp >= config.rp_ranks[rank]:
        rem_rp -= config.rp_ranks[rank]
        rank += 1
    # Returns the final values for rank and rem_rp.
    return rank


# Function to get profile pages (1 - 3)
async def get_page(self, ctx, number, userid):
    clans = data_handler.load("clans")
    profiles = data_handler.load("profiles")

    user = await self.bot.fetch_user(userid)
    player = profiles[str(userid)]

    page = discord.Embed(title = f"{user.display_name}'s profile",
                          colour = int(player['Settings']['colours'][player['Settings']['colour']], 16),
                          description = f"{user.name}#{user.discriminator}")

    page.set_thumbnail(url = user.avatar_url_as(static_format = 'png'))
    page.set_footer(text = f"Requested by {ctx.author.display_name}",
                   icon_url = ctx.author.avatar_url_as(static_format='png'))

    if number == 1:
        # Page 1
        try:
            clan = clans[player['Base']['clanID']]['Base']['name']
        except:
            clan = "None"

        page.add_field(name = "Base Info",
                        value = f"Account Name: {player['Base']['username']} \nClan: {clan} \nCountry: {player['Base']['country']}",
                        inline = False)
        page.add_field(name = "Level Info",
                        value = f"Rank: {player['Level']['rank']} \nTotal Rank Points: {player['Level']['rp']}",
                        inline = False)

    if number == 2:
        # Page 2
        page.add_field(name = "Achievements",
                        value = f"Amount of Lord titles: {player['Achievements']['lords']} \nAmount of Squire titles: {player['Achievements']['squires']} \nBest :trophy: rating: {player['Achievements']['rating']}",
                        inline = False)
        page.add_field(name = "Fun Favourites",
                        value = f"Favourite unit: {player['Favourites']['unit']} \nFavourite Tactic: {player['Favourites']['tactic']} \nFavourite Tome: {player['Favourites']['tome']} \nFavourite Skin: {player['Favourites']['skin']}",
                        inline = False)
    
    if number == 3 and userid is not None:
        # Page 3
        member = discord.utils.find(lambda g: g.get_member(userid), self.bot.guilds)
        if member is not None:
            member = member.get_member(userid)
            days = int(int(time.time() - (member.created_at - datetime.datetime.utcfromtimestamp(0)).total_seconds())/ 86400)
            discord_date = f"{member.created_at.ctime()} ({days} days ago)"
        
            page.add_field(name = "Discord Info",
                       value = f"Joined Discord on: {discord_date} \nStatus: {member.status} \nid: `{member.id}` \nAvatar Link: {member.avatar_url_as(format='png')}")

    return page

# get reaction with number + vice versa
def get_reaction(number, reaction = None):
    reactions = {
        1: "1\u20e3",
        2: "2\u20e3",
        3: "3\u20e3",
        4: "4\u20e3",
        5: "5\u20e3",
        6: "6\u20e3",
        7: "7\u20e3",
        8: "8\u20e3",
        9: "9\u20e3",
        10: "10\u20e3"
    }

    if reaction is None:
        return reactions.get(number, 0)
    else:
        return list(reactions.keys())[list(reactions.values()).index(reaction)]

# async handling of user reactions
async def handle_reactions(self, ctx, userid, pages, page1, message):
    profiles = data_handler.load("profiles")
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
           playerid = int(random.choice(list(profiles)))
           while playerid == userid:
               playerid = int(random.choice(list(profiles)))

           page1 = await get_page(self, ctx, 1, playerid)
           page2 = await get_page(self, ctx, 2, playerid)
           page3 = await get_page(self, ctx, 3, playerid)
           pages = [page1, page2, page3]

           await message.edit(embed=pages[0])
           await handle_reactions(self, ctx, playerid, pages, page1, message)
           return

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
    

class Profiles(commands.Cog):
    # Initialises the variables and sets the bot.
    def __init__(self, bot):
        self.bot = bot

    # Our base level command. Due to invoke_without_command=True it means that this command is only run when no
    # sub-command is run. Makes it a command group with a name.
    @commands.group(name='profile', invoke_without_command = True, aliases = ['p'])
    # Defines it as a function.
    async def profile(self, ctx, *, userName:str = None):
        """
        Check your profile or that of another member.
        You no longer need to mention the user to check their profile!
        """
        profiles = data_handler.load("profiles")
        userids = list()

        if userName is None:
            # if user wants to display his own profile, display only his own.
            userid = ctx.message.author.id
        else:
            for user in list(filter(lambda u: userName in u.name, self.bot.users)):
                userids.append(user.id)

            for guild in self.bot.guilds:
                for member in list(filter(lambda m: userName in m.display_name, guild.members)):
                    userids.append(member.id)

            for profil in profiles:
                if userName in profiles[profil]['Base']['username']:
                  userids.append(int(profil))

            # distinct result list
            userids = list(OrderedDict.fromkeys(userids))

            # filter out userids without existing user profile
            tempUserids = list()
            for userid in userids:
                try:
                    player = profiles[str(userid)]
                    if config.rp_showHistoricProfiles == False:
                        member = discord.utils.find(lambda g: g.get_member(userid), self.bot.guilds).get_member(userid)
                    tempUserids.append(userid)
                except:
                    continue

            userids = tempUserids

            if len(userids) <= 0:
                await ctx.send("I don't know that Discord User/profile")
                return

            if len(userids) > 10:
                await ctx.send("I found more than 10 matching profiles. Please be more specific.")
                return

            if len(userids) > 1:
                # more then 1 possilbe profile found, let the user decide which should be shown
                selectionpage = discord.Embed(title = "I found more than one matching profile. Please select the correct one:", description = "")
                selectionpage.set_footer(text = f"Requested by {ctx.author.display_name}", icon_url = ctx.author.avatar_url_as(static_format='png'))

                selection = await ctx.send(embed=selectionpage)
                foundUser = list()
                i = 1

                for userid in userids:
                    player = profiles[str(userid)]
                    user = await self.bot.fetch_user(userid)
                    reactionString = str(get_reaction(i))

                    selectionpage.add_field(name = f"{reactionString}", value = f"{user.name}#{user.discriminator} - Account Name: {player['Base']['username']}", inline = False)
                    foundUser.append(userid)
                    await selection.add_reaction(reactionString)
                    i += 1

                await selection.edit(embed=selectionpage)
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=lambda r, u: u.id == ctx.author.id and u.bot == False)
                except asyncio.TimeoutError:
                    return

                # show the profile of this id:
                userid = foundUser[int(get_reaction(0, str(reaction))) - 1]
            else:
                userid = userids[0]

            
        # display profile of found user
        page1 = await get_page(self, ctx, 1, userid)
        page2 = await get_page(self, ctx, 2, userid)
        page3 = await get_page(self, ctx, 3, userid)
        pages = [page1, page2, page3]

        message = await ctx.send(embed=page1)
        await message.add_reaction("⏪")
        await message.add_reaction("◀")
        await message.add_reaction("⏺️")
        await message.add_reaction("▶")
        await message.add_reaction("⏩")
        
        await handle_reactions(self, ctx, userid, pages, page1, message)


    @profile.command(name="set")
    async def setProfile(self, ctx, attribute, *, value):
        try:
            """
            Change values on your profile. You can change:
            `username`, `clan`, `country`, `lords`, `squires`, `rating`, `unit`, `tactic`, `tome`, `skin`, `colour`.
            """
            profiles = data_handler.load("profiles")
            player = profiles[str(ctx.author.id)]
            attribute = attribute.lower()

            if attribute in ['colour', 'color', 'colours', 'colors']:
                await self.changeProfileColour(ctx, int(value))
                return

            if attribute in ["lords", "lord"]:
                if str(value)[0] == "+":
                    player['Achievements']['lords'] += int(value)
                else:
                    player['Achievements']['lords'] = int(value)
            elif attribute in ["clans" "clan"]:
                player["Base"]["clan"] = value
            elif attribute in ["squires", "squire"]:
                if str(value)[0] == "+":
                    player['Achievements']['squires'] += int(value) 
                else:
                    player['Achievements']['squires'] = int(value)
            elif attribute in ["rating"]:
                player['Achievements']['rating'] = int(value)
            elif attribute in ["unit", "units", "troop"]:
                player['Favourites']['unit'] = value
            elif attribute in ["tactic", "strategy", "layout"]:
                player['Favourites']['tactic'] = value
            elif attribute in ["tome", "masteryskill", "book"]:
                player['Favourites']['tome'] = value
            elif attribute in ["skin", "look"]:
                player['Favourites']['skin'] = value
            elif attribute in ["country", "location"]:
                player['Base']['country'] = value
            elif attribute in ["name", "accountname", "account", "username"]:
                player['Base']['username'] = value
            else:
                await ctx.send("This is not a valid setting.  You can change: " +
                               "`username`, `clan`, `country`, `lords`, `squires`, `rating`, `unit`, `tactic`, `tome`, `skin`, `colour`.")
                return
        except ValueError:
            await ctx.send("Invalid Value. Please choose a number.")
        else: 
            await ctx.send("Profile updated.")
            data_handler.dump(profiles, "profiles")


    @profile.command(name='colour', aliases = ['color', 'colours', 'colors'])
    async def changeProfileColour(self, ctx, colour:int = None):
        """
        Allows you to change the colour of all your profile based information!
        """
        profiles = data_handler.load("profiles")
        try:
            player = profiles[str(ctx.author.id)]
        except:
            await ctx.send("An error occured. Please try again.")
            return
        colourList = list(player['Settings']['colours'])

        if colour is None or colour >= len(colourList) or colour < 0:
            description = "Unlocked Colours:"
            for colourIndex in range(len(colourList)):
                description = description + f"\n{colourIndex}. {colourList[colourIndex]} - `#{player['Settings']['colours'][colourList[colourIndex]]}`" 
            embed = discord.Embed(title = "Please select a valid colour.",
                                  colour = int(player['Settings']['colours'][player['Settings']['colour']], 16),
                                  description = description)

            Color = str(colourList.index(player['Settings']['colour'])) + ". " + player['Settings']['colour'] + " - `#" + player['Settings']['colours'][f"{player['Settings']['colour']}"] + "`"
            embed.add_field(name = "Current Colour:",
                            value = Color)

            embed.set_footer(text = f"Requested by {ctx.author.display_name}",
                             icon_url = ctx.author.avatar_url_as(static_format='png'))
            await ctx.send(embed=embed)
            return

        player['Settings']['colour'] = colourList[colour]

        profiles[ctx.author.id] = player
        data_handler.dump(profiles, "profiles")
        await ctx.send("Updated your colour.")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        """
        Gives you rank points per message on a one minute cooldown.
        """

        if ctx.author.bot:
            return
        profiles = data_handler.load("profiles")

        try:
            player = profiles[str(ctx.author.id)]
        except KeyError:
            profiles[f"{ctx.author.id}"] = {
                "Base": {
                    "username": f"{ctx.author.display_name}", "clanID": "None", "country": "Earth"},
                "Level": {
                    "rp": 0, "rank": 0, "timeOfNextEarn": 0},
                "Achievements": {
                    "lords": 0, "squires": 0, "rating": 1000},
                "Favourites": {
                    "unit": "None", "tactic": "None", "tome": "None", "skin": "None"},
                "Settings": {
                    "rankUpMessage": "chat", "colour": "Default", "colours": {"Default": "000000"},"permissions": []}}

            player = profiles[str(ctx.author.id)]

        gained_rp = int(random.randint(config.rp_min, config.rp_max) * config.rp_mult)

        cooldown, rankedUp, rank = gainedRP(player, gained_rp)
        if cooldown:
            return

        player['Level']['rank'] = rank
        player['Level']['timeOfNextEarn'] = time.time() + config.rp_cooldown
        player['Level']['rp'] += gained_rp

        pRUM = player['Settings']['rankUpMessage']

        if rankedUp and pRUM in ['any','dm','chat']:
            servers = data_handler.load("servers")
            try:
                sRUM = servers[str(ctx.guild.id)]['Messages']['rankUpMessages']
            except KeyError:
                sRUM = "any"

            if sRUM == "channel":
                destination = ctx.guild.get_channel(servers[str(ctx.guild.id)]['Messages']['rankUpChannel'])
            elif sRUM == "any" and pRUM in ["chat", "any"]:
                destination = ctx.channel
            elif pRUM in ["dm", "any"]:
                destination = ctx.author

            try:
                await destination.send(f"Congrats {ctx.author.mention}! You've earned enough rank points to rank up to Rank {rank}!")
            except discord.Forbidden:
                if pRUM == "any":
                    destination = ctx.author
                    await destination.send(f"Congrats {ctx.author.mention}! You've earned enough rank points to rank up to Rank {rank}!")

            if rank == 1:
                await destination.send("You've also unlocked a new colour: Rank 1!")
                player['Settings']['colours']['Rank 1'] = "fefefe"
            elif rank == 5:
                await destination.send("You've also unlocked a new colour: Rank 5!")
                player['Settings']['colours']['Rank 5'] = "7af8d3"
            elif rank == 10:
                await destination.send("You've also unlocked a new colour: Level 10!")
                player['Settings']['colours']['Rank 10'] = "327c31"

        data_handler.dump(profiles, "profiles")

    @profile.group(name="leaderboard", aliases=["lb"], invoke_without_command = True)
    async def levelLB(self, ctx, member: discord.Member = None):
        """
        Check where people are relative to each other! Not specifying a page will select the first page.
        """
        # Sort the dictionary into a list.
        member = member or ctx.author
        profiles = data_handler.load("profiles")
        rankings = []
        description = ""
        for player in profiles:
            try:
                rankings.append({'id': player, 'rp': profiles[player]['Level']['rp']})
            except KeyError:
                pass

        def getKey(item):
           return item['rp']

        rankings = sorted(rankings, reverse = True, key = getKey)

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
                description += f"\n**{i + 1}.** {user.name}#{user.discriminator} - {rankings[i]['Level']['rp']} rank points."

        embed = discord.Embed(title="Rank leaderboard",
                              colour=discord.Colour(0xa72693),
                              description=description,
                              inline=True)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}",
                         icon_url=ctx.author.avatar_url_as(static_format="png"))
        # Send embed
        await ctx.send(content="Here you go!", embed=embed)

    @profile.group(name = 'options', aliases = ['option', 'o'])
    async def pOptions(self, ctx, option:str = None, value:str = None):
        """
        Checks or change profile options.

        To check options, don't specify an option or values.
        To change an option, specify the option and it's new value.
        Leave the value blank to see possible settings.
        """
        profiles = data_handler.load("profiles")
        try:
            player = profiles[str(ctx.author.id)]
        except KeyError:
            await ctx.send("An error occured. Please try again.")
        
        if option is None:
            embed = discord.Embed(title = "Personal Settings",
            description = "To change an option, specify the option and it's new value.\nLeave the value blank to see possible settings.",
            colour = int(player["Settings"]["colours"][player["Settings"]["colour"]], 16))

            # rankUpMessage setting
            if player["Settings"]["rankUpMessage"] == "any":
                embed.add_field(name = "`RankUpMessage` **:** `any`",
                value = "This means the bot will try to tell you in chat when you level up, or in the server's level up channel. If it can't do either, it will DM you.")
            elif player["Settings"]["rankUpMessage"] == "chat":
                embed.add_field(name = "`RankUpMessage` **:** `chat`",
                value = "This means the bot will try to tell you in chat when you level up, or in the server's level up channel. If it can't do either, it will **not** DM you.")
            elif player["Settings"]["rankUpMessage"] == "dm":
                embed.add_field(name = "`RankUpMessage` **:** `dm`",
                value = "This means the bot shall try to DM you with the rank up message. If that's not possible, you won't be informed.")
            elif player["Settings"]["rankUpMessage"] == "none":
                embed.add_field(name = "`RankUpMessage` **:** `none`",
                value = "This means you will not be told when you rank up.")

            # Not sure if I want to use this feature...
            # permissions = "None"
            # if "*" in player["Settings"]["permissions"]:
            #     permissions = "*"
            
            # embed.add_field(name = "Permissions",
            # value = permissions)

            embed.set_footer(text = f"Requested by {ctx.author.display_name}",
            icon_url = ctx.author.avatar_url_as(static_format='png'))
            embed.set_thumbnail(url = ctx.author.avatar_url_as(static_format = 'png'))

            await ctx.send(content = "", embed=embed)

        elif option.lower() in ["rum", "rankupmessage", "rankup"]:
            if value is None:
                embed = discord.Embed(title = "Rank Up Message",
                description = "Specify where rank up messages should be allowed.",
                colour = int(player["Settings"]["colours"][player["Settings"]["colour"]], 16))

                embed.add_field(name = "`any`",
                value = "This means the bot will try to tell you in chat when you level up, or in the server's level up channel. If it can't do either, it will DM you.")
                embed.add_field(name = "`chat`",
                value = "This means the bot will try to tell you in chat when you level up, or in the server's level up channel. If it can't do either, it will **not** DM you.")
                embed.add_field(name = "`dm`",
                value = "This means the bot shall try to DM you with the rank up message. If that's not possible, you won't be informed.")
                embed.add_field(name = "`none`",
                value = "This means you will not be told when you rank up.")

                embed.set_footer(text = f"Requested by {ctx.author.display_name}",
                icon_url = ctx.author.avatar_url_as(static_format='png'))

                await ctx.send(content = "", embed=embed)

            elif value.lower() == "any":
                player["Settings"]["rankUpMessage"] = "any"
                await ctx.send(f"{option} updated.")

            elif value.lower() == "chat":
                player["Settings"]["rankUpMessage"] = "chat"
                await ctx.send(f"{option} updated.")

            elif value.lower() == "dm":
                player["Settings"]["rankUpMessage"] = "dm"
                await ctx.send(f"{option} updated.")

            elif value.lower() == "none":
                player["Settings"]["rankUpMessage"] = "none"
                await ctx.send(f"{option} updated.")
        
        profiles[str(ctx.author.id)] = player
        data_handler.dump(profiles, "profiles")
            

    @commands.is_owner()
    @profile.command(name = 'reset', hidden = True)
    async def resetLevel(self, ctx):
        """
        Resets All rp. Used when testing rate of earn
        """
        profiles = {}
        data_handler.dump(profiles, "profiles")
        await ctx.send("Reset all profiles.")

def setup(bot):
    bot.add_cog(Profiles(bot))
