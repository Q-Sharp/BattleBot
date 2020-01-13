# Used in calculating time based stuff
import time
# Used to store and load binary data.
import pickle

class Clan:
    # What happens when we create a new instance of the class
    # Takes the clan's name and their ID as inputs.
    def __init__(self, name:str, clanID:str, ownerID:int):
        self.name = name # Sets the clan name
        self.clanID = clanID # The clan's in-game id.
        self.leaderID = ownerID # Who is the current owner of the clan
        self.coLeaderIDs = [] # A list of all the co-leaders
        self.elderIDs = [] # A list of all the elders
        self.memberIDs = [] # A list of all the normal members
        self.commanderIDs = [ownerID] # A list of all the ids in the clan
        self.description = "None set" # The description for the clan
        self.discord = "https://discordapp.com" # A link to their discord. (Need to choose an appropriate default)
        self.advertise = f"Come join {name}! It's awesome!" # Their advertisement message
        self.creationTime = time.time() # The time there clan was created in seconds from time.time() = 0
        self.icon = "https://cdn.discordapp.com/embed/avatars/4.png" # This icon for their clan. This is a default discord avatar
        self.xp = 0 # Sets the clan xp. Will be used if challenges to level them up to gain rewards
        self.level = 0 # The current level of the clan. Uses clanXP to set it.
        self.rankRequirement = 0 # The minimum BB user rank a person must be to join
        self.joinType = "Open" # Defines how players can join the clan. Settings will be the same as bl
        self.ratingRequirement = 0 # Mimum top rating requirement to join. Both rank requirement and rating requirement can be set.
        self.mascot = "None" # A unit that is the clan's mascot.
        self.colour = 0x000000 # The clan colour (used when displaying the embed)

    # Allows us to update the clan classes without having to delete the data or input manually
    def setValues(self, clan):
        self.name = clan.name
        self.clanID = clan.clanID
        self.leaderID = clan.leaderID
        self.coLeaderIDs = clan.coLeaderIDs
        self.elderIDs = clan.elderIDs
        self.memberIDs = clan.memberIDs
        self.commanderIDs = clan.commanderIDs
        self.description = clan.description
        self.discord = clan.discord
        self.advertise = clan.advertise
        self.creationTime = clan.creationTime
        self.icon = clan.icon
        self.xp = clan.xp
        self.level = clan.level
        self.rankRequirement = clan.rankRequirement
        self.joinType = clan.joinType
        self.ratingRequirement = clan.ratingRequirement
        self.mascot = clan.mascot
        self.colour = clan.colour
        
        
    # Called when a member wishes to join the server.
    # Further checks need to be added for requirements
    def addMember(self, memberID):
        # Checks the clan isn't full
        if len(self.memberIDs) >= 50:
            raise AttributeError
        # Adds them to the clan.
        # Could probably also set their clan on profile too.
        self.memberIDs.append(memberID)

    # Obtains the total rp of all the members in the clan
    def totalRP(self):
        # Defines the total variable
        totalRP = 0
        # Loads the profiles
        profiles = pickle.load(open('data/profiles.data', 'rb')) # `pickle.load(open('<filepath>', '<mode>'))` Mode is either read binary (rb) or write binary (wb) for pickling
        # Goes through each member and obtains their rp
        # It then adds the rp to the total variable.
        for memberID in self.memberIDs:
            totalRP += profiles[memberID].rp
        # Returns our total variable
        return totalRP
