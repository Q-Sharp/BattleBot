import discord
from discord.ext import commands
import asyncio
import pickle
import cogs.checks as check
import random
import requests
import urllib

class Elements(commands.Cog):
    """
    Elements....
    """
    def __init__(self,bot):
        self.bot = bot
        self.channels = [615897971560546304,626165035043127307]
        self.isQuiz = False
        self.correct = {}
        self.answered = []
        self.correctGuild = []
        self.options = ['A','B','C','D']

    @check.test_command()
    @commands.group(name='element',aliases=['E','e'],invoke_without_command=True)
    async def element(self,ctx):
        """
        Check your element card to get an element!
        """
        elements = pickle.load(open('data/elements.data','rb'))
        try:
            user = elements['users'][ctx.author.id]
        except KeyError:
            await ctx.send("You haven't got an element yet!")

    @commands.is_owner()
    @commands.command(name='quiz',hidden=True)
    async def QuizQuestion(self,ctx):
        """
        A random quiz question"
        """
        self.correct = {}
        self.answered = []
        self.correctGuild = []
        self.isQuiz = True

        #for channelID in self.channels:
        #    channel = await self.bot.fetch_channel(channelID)
        #    await channel.send("Quiz is starting in 1 min...")
        #await asyncio.sleep(60)

        url = "https://opentdb.com/api.php?amount=1&type=multiple&encode=url3986"

        response = requests.request("GET", url)
        response = response.json()['results'][0]

        for index in response:
            try:
                response[index] = urllib.parse.unquote(response[index])
            except AttributeError:
                for jdex in range(len(response[index])):
                    response[index][jdex] = urllib.parse.unquote(response[index][jdex])

        answers = ""
        corI = random.randint(0,3)
        for i in range(4):
            answers += f"{self.options[i]}) "
            if i == corI:
                answers += response['correct_answer']
            else:
                answers += response['incorrect_answers'].pop(0)
            if i != 3:
                answers += "\n"

        embed = discord.Embed(title=response['category'],
                              colour=discord.Colour(0xffffff),
                              description=response['question'])

        embed.add_field(name="Correct Answer:",value=f"||{response['correct_answer']}||")

        embed.set_author(name=f"Difficulty: {response['difficulty']}")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url_as(static_format='png'))

        embed.add_field(name="Answers",
                        value=f"{answers}")

        for channelID in self.channels:
            channel = await self.bot.fetch_channel(channelID)
            await channel.send(embed=embed)

        def checkIfABlitz(m):
            if m.channel.id in self.channels:
                if m.author.id != self.bot.user.id:
                    if m.author.id not in self.answered:
                        self.answered.append(m.author.id)
                        if self.options[corI].lower() == m.content.lower():
                            try:
                                self.correct[m.guild.id].append(m.author.id)
                            except KeyError:
                                self.correct[m.guild.id] = [m.author.id]
                                self.correctGuild += [m.guild.id]
            return False

        try:
            guess = await self.bot.wait_for('message',check = checkIfABlitz, timeout=30.0)
        except asyncio.TimeoutError:
            for channelID in self.channels:
                channel = await self.bot.fetch_channel(channelID)
                if channel.guild.id not in self.correctGuild:
                    await channel.send(content=f"Nobody got it. The correct answer was: `{self.options[corI]}) {response['correct_answer']}`.")
                else:
                    msg = ""
                    for memberI in range(len(self.correct[channel.guild.id])):
                        theMember = channel.guild.get_member(self.correct[memberI])
                        msg += f"{theMember.mention}, "
                    msg += "have got the question correct!"
                    await channel.send(msg)
                    await ctx.send("<Add element points here>")
        self.isQuiz = False

    @commands.is_owner()
    @element.group(name='admin',aliases=['a'],invoke_without_command=True)
    async def eAdmin(self,ctx):
        await ctx.send("Admin only commands. Please check admin channel before use.")

    @commands.is_owner()
    @eAdmin.command(name='channel')
    async def addChannel(self,ctx):
        self.channels.append(ctx.channel.id)
        await ctx.send("Added chanel.")

    @commands.is_owner()
    @eAdmin.command(name='fix')
    async def FixElementData(self,ctx):
        await ctx.send("No fixing set.")

    @commands.is_owner()
    @eAdmin.command(name='reset')
    async def elementsReset(self,ctx):
        elements = {
            'elements':
            {'air':{},
             'earth':{},
             'fire':{},
             'water':{}},
            'users':{}}
        pickle.dump(elements,open('data/elements.data','wb'))
        await ctx.send("Element data reset.")

def setup(bot):
    bot.add_cog(Elements(bot))
