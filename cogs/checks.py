import discord
from discord.ext import commands
import asyncio
from data.data_handler import data_handler

# Command can't be used in this server.
class NotInServer(commands.CheckFailure):
    def __init__(self, message):
        self.message = message
    pass

# User isn't high enough rank.
class UserNotHighEnoughLevel(commands.CheckFailure):
    def __init__(self, rank):
        self.rank = rank
    pass

# Clan isn't high enough rank.
class ClanNotHighEnoughRank(commands.CheckFailure):
    def __init__(self, rank):
        self.rank = rank
    pass

# User doesn't have permission.
class UserNoPermission(commands.CheckFailure):
    def __init__(self, permission):
        self.permission = permission
    pass

# Checks user has the requied minimum rank.
def user_rank_requirement(rank):
    # Useful to create an async command to run this
    async def predicate(ctx):
        profiles = data_handler.load("profiles")
        # Checks the user has an account
        try:
            # Checks if they aren't high enough level
            if profiles[ctx.author.id].rank < rank:
                raise UserNotHighEnoughLevel(rank)
            else:
                # Returns trus if user has an account and it's high enough level
                return True
        except KeyError:
            pass
        raise UserNotHighEnoughLevel(rank)
    return commands.check(predicate)

# Checks the clan has the required minimum rank.
def clan_rank_requirement(rank):
    async def predicate(ctx):
        clans = data_handler.load("clans")
        try:
            if clans[ctx.guild.id]['rank'] < rank:
                raise ClanNotHighEnoughRank(rank)
            else:
                return True
        except KeyError:
            pass
        raise ClanNotHighEnoughRank(rank)
    return commands.check(predicate)

# Checks user has the requied minimum rank.
def user_permission_requirement(permission):
    async def predicate(ctx):
        profiles = data_handler.load("profiles")
        try:
            if permission in profiles[ctx.author.id].permissions:
                raise UserNoPermission(permission)
            else:
                return True
        except KeyError:
            pass
        raise UserNoPermission(permission)
    return commands.check(predicate)


