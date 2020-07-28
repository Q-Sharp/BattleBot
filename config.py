from range_key_dict import RangeKeyDict

"""
This file saves all the global configs for the bot.
"""

"""
Base values for rank point earn
"""

# A multiplier for all rank points earnt. Good if you wanted to decrease the amount people earnt or increase it for an event.
rp_mult = 1
# The minimum amount of rank points a person can earn per message.
rp_min = 15
# The maximum amount of rank points a person can earn per message.
rp_max = 25
# The amount of time the bot waits between message before awarding rank points. In secconds
rp_cooldown = 60

# The formula for ranks. The default ranks are listed below.
# By default there are 50 ranks to play with, however, you can increase that about by changing the number inside the range() bracket.
rp_ranks = [int(5 * (i ** 1.5) + 50 * i + 100) for i in range(70)]
# The ranks (default):
# [100, 155, 214, 275, 340, 405, 473, 542, 613, 685, 758, 832, 907,
# 984, 1061, 1140, 1220, 1300, 1381, 1464, 1547, 1631, 1715, 1801,
# 1887, 1975, 2062, 2151, 2240, 2330, 2421, 2513, 2605, 2697, 2791,
# 2885, 2980, 3075, 3171, 3267, 3364, 3462, 3560, 3659, 3759, 3859, 
# 3959, 4061, 4162, 4265, 4367, 4471, 4574, 4679, 4784, 4889, 4995, 
# 5101, 5208, 5315, 5423, 5532, 5640, 5750, 5860, 5970, 6080, 6192, 
# 6303, 6415]

# ranking range
rp_ranktitles = RangeKeyDict({
        (0, 5): "Village",
        (5, 10): "Battlegrounds",
        (10, 15): "Bandit Town",
        (15, 20): "Iron Ramparts",
        (20, 25): "Soldiers' Encampment",
        (25, 30): "Royal Encampment",
        (30, 35): "Uncharted Jungle",
        (35, 40): "Sky Temple",
        (40, 45): "Arcane Desert",
        (45, 50): "Ancient Tomb",
        (50, 55): "Eldricht Mountains",
        (55, 60): "Divine Sanctuary",
        (60, 65): "Whispering Ruins",
        (65, 70): "Druidic Forest",
        (70, 75): "Valley of Giants"
    })


# show old profiles
rp_showHistoricProfiles = False
