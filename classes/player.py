# Allows us to use random numbers and pick a choice
import random
# Allows us to play with time
import time

# The formula for ranks.
ranksRP = [int(5 * (i ** 1.5) + 50 * i + 100) for i in range(50)]

# Function to get a user's rank and remaining rp to next rank.
# Takes current rp as parameter
def get_rank_from(rp):
    # Sets the starting value to be our remaining rp
    rem_rp = int(rp)
    # Starts the rank at 0
    rank = 0
    # Loops throught the ranks and checks if the user had enough rp to rank up
    # If so, take that rp away from rem_rp and add one to their rank
    while rem_rp >= ranksRP[rank]:
        rem_rp -= ranksRP[rank]
        rank += 1
    # Returns the final values for rank and rem_rp.
    return rem_rp, rank

# Our Player class.
class Player:
    # Called when we create a new player. Takes in the player's name
    def __init__(self, name):
        self.accountName = name # Player's in-game name
        self.clanTag = None # The player's current clan's tag. This is used when displaying the profile, we place it in [] and in front of the name.
        self.clan = None # The user's current clan. We'll use this in checks to see if the user is in a clan and when obtaining the user's clan. Also used in profile display
        self.rank = 0 # The user's current rank.
        self.rp = 0 # The user's current rp
        self.minRP = 1 # The minimum rp a user can get for a message
        self.maxRP = 10 # The maximum rp a user can get for a message
        self.lords = 0 # Amount of lords titles achieved
        self.squires = 0 # Amount of squire titles achieved
        self.rating = 0 # Top trophy rating achieved
        self.favourites = {'unit':"None",'tactic':"None",'tome':"None",'skin':"None"} # User's personal favourites. Stores in a disctionary so it's easy to add new ones and view a current one.
        self.rankUpMessage = "any" # Where to send rank up messages
        self.country = "Earth" # The country of the user. This is here so people can know native language and timezone as well as if the player can access the game
        self.timeCanEarn = 0 # The time at which a player can next earn rp for speaking
        self.colour = 'Default' # The user's colour. Used when displaying the user's profile. The colour can then be obtained from the colours dictionary
        self.colours = {'Default':0x000000} # The colours a user has. Can be updated to allow more colours or the editing of colours.
        self.permissions = [] # The default permissions a user has. Can be used when adding commands and having checks.

    # Allows us to update all the profiles easily
    def setValues(self, player):
        # Go through each of the attributes of the new player class and set them the values of the old player class
        self.accountName = player.accountName
        self.clanTag = None
        self.clan = player.clan
        self.rank = player.rank
        self.rp = player.rp
        self.minRP = player.minRP
        self.maxRP = player.maxRP
        self.lords = player.lords
        self.squires = player.squires
        self.rating = player.rating
        self.favourites = player.favourites
        self.rankUpMessage = player.rankUpMessage
        self.country = player.country
        self.timeCanEarn = player.timeCanEarn
        self.colour = "Default"
        self.colours = player.colours
        self.permissions = player.permissions

    # Called when a user speaks
    def spoke(self):
        # Checks if the user's message cooldown has ended.
        if self.timeCanEarn > time.time():
            # We have to return three variables (see below)
            return True, False, None
        else:
            # Set the time they can next earn rp to be in 60 seconds time.
            self.timeCanEarn = time.time() + 60
        # Adds a random integer between their minimum rp and maximum rp gain.
        self.rp += random.randint(self.minRP, self.maxRP)
        # calls the get_rank_from function and set's rem_rp to be rem_rp and rank to be rank.
        rem_rp, rank = get_rank_from(self.rp)
        # Defines our rankedUp variable
        rankedUp = False
        # Checks if we ranked up
        if self.rank < rank:
            # Ranks the user up
            rankedUp = True
            self.rank = rank
        # Returns all the results so we can do stuff with it.
        # returns: cooldown, hasRankedUp, currentRank
        return False, rankedUp, self.rank

    # Get's the player's rank card.
    def getRankCard(self):
        # Gets rank and rem_rp
        remRP, rank = get_rank_from(self.rp)
        # returns: TotalRP, rPProgressToNextRank, currentRank
        return self.rp, remRP, rank

    # Adds a colour to the user
    # Takes in the name of the colour and the hex value of the colour
    def addColour(self, name = None, colour = None):
        # Checks are variables are valid
        if name is None or colour is None:
            print("Name or Colour NONE. Check the code you've just written dumb dumb!")
            raise NameError
        # Checks if we have the colour added already
        try:
            colour = self.colours[name]
            print("Colour name already in use!")
            raise NameError
        # Otherwise adds the colour to the colours dictionary!
        except KeyError:
            self.colours[name] = colour

    # Adds a permission
    # Takes in a permission name
    def addPermission(self, permission:str = None):
        # Checks the permission os valid
        if permission is None:
            print("Permission is NONE. Check the code you've just written dumb dumb!")
            raise NameError
        # Checks if we already have the permission
        if permission in self.permissions:
            print("Permission already added")
            raise KeyError
        # Otherwise add the permission to the permissions list!
        else:
            self.permissions.append(permission)
        
