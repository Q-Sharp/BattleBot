"""
This file saves all the global configs for the bot.
"""

"""
Base values for Rrank point earn
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
rp_ranks = [int(5 * (i ** 1.5) + 50 * i + 100) for i in range(50)]
# The ranks (default):
# [100, 155, 214, 275, 340, 405, 473, 542, 613, 685, 758, 832, 907,
# 984, 1061, 1140, 1220, 1300, 1381, 1464, 1547, 1631, 1715, 1801,
# 1887, 1975, 2062, 2151, 2240, 2330, 2421, 2513, 2605, 2697, 2791,
# 2885, 2980, 3075, 3171, 3267, 3364, 3462, 3560, 3659, 3759, 3859, 
# 3959, 4061, 4162, 4265]
rp_showHistoricProfiles = False
