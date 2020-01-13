import discord
from discord.ext import commands


class HelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            "help": "Shows help about the bot, a command, or a category."
        })
        
    def get_opening_note(self):
        command_name = self.invoked_with
        return "Use `{0}{1} [command]` for more info on a command.\n" \
               "You can also use `{0}{1} [Category]` for more info on a category.".format(
                   self.clean_prefix, command_name)

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = '|'.join(command.aliases)
            fmt = f'[{command.name}|{aliases}]'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{alias} {command.signature}'

    def add_command_formatting(self, command):
        if command.description:
            self.paginator.add_line(command.description, empty=True)

        signature = self.get_command_signature(command)
        self.paginator.add_line(signature, empty=True)
        
        if command.help:
            try:
                self.paginator.add_line(command.help, empty=True)
            except RuntimeError:
                for line in command.help.splitlines():
                    self.paginator.add_line(line)
                self.paginator.add_line()

    def add_bot_commands_formatting(self, commands, heading):
        if commands:
            print("XD")
            # U+2022 Bullet
            joined = ' \U00002022 '.join(c.name for c in commands)
            self.paginator.add_line(f'__**{heading}**__')
            self.paginator.add_line(joined)


class Info(commands.Cog):
    # TODO: cog help string
    """
    Shows info about the bot.
    """

    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    @commands.command(aliases=["info"])
    async def about(self, ctx):
        """
        Tells you information about the bot itself.
        """
        embed = discord.Embed(title=f"{self.bot.user.display_name} info",
                              colour=discord.Colour(0xc06c84),
                              description="BattleBot is a Battle Legion based bot. The aim is to create Battle Legion based bot content that is enjoyed by both Traplight and players alike.")

        embed.set_thumbnail(url=self.bot.user.avatar_url_as(static_format='png'))
        embed.set_author(name=f"{self.bot.user.name}#{self.bot.user.discriminator}",
                         icon_url=self.bot.user.avatar_url_as(static_format='png'),
                         url="https://discordapp.com/oauth2/authorize?client_id=612344319323537458&permissions=67501120&scope=bot")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}",icon_url=ctx.author.avatar_url_as(static_format='png'))

        embed.add_field(name="My parents:",
                        value="**Main Dev/Founder** - Greenfoot5#2535 \n**Nit-Picker** - Flaming_Galaxy#7245",
                        inline = False)
        embed.add_field(name="Invite me to your server!",
                        value="https://discordapp.com/oauth2/authorize?client_id=612344319323537458&permissions=67501120&scope=bot")
        embed.add_field(name="Join my support server and test out new commands!",
                        value="https://discord.gg/FkpUHNK")

        await ctx.send(content="",embed=embed)

    @commands.command(name='ping')
    async def ping(self,ctx):
        await ctx.send('Pong! {0}ms'.format(int(round(self.bot.latency,3)*1000)))

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(Info(bot))
