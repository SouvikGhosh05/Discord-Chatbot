import discord
from random import sample
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = self.bot.command_prefix

    @commands.group(invoke_without_command=True, aliases=["h"])
    async def help(self, ctx):
        ext_two_cogs = (
            *(i.name for i in self.bot.get_cog("GeoSearch").get_commands()),
            *(i.name for i in self.bot.get_cog("Ext_Info").get_commands()),
        )
        fun_cogs = (
            *(i.name for i in self.bot.get_cog("GIF").get_commands()),
            *(i.name for i in self.bot.get_cog("Jokes").get_commands()),
            *(i.name for i in self.bot.get_cog("RedditApi").get_commands()),
        )
        intro_commands = [i.name for i in self.bot.get_cog("Main_BOT").get_commands()]
        info_commands = [i.name for i in self.bot.get_cog("Info").get_commands()]
        general_commands = [*intro_commands[:-4], *info_commands]

        help_Embed = discord.Embed(
            title="Help shows all commands",
            description=f"Use {self.prefix}help <command> for extended help for that command",
            color=discord.Color.random(),
        )
        help_Embed.add_field(
            name="External Information",
            value="\n".join(f"`{key}`" for key in ext_two_cogs),
        )
        help_Embed.add_field(
            name="Fun",
            value="\n".join(f"`{key}`" for key in (sample(fun_cogs, k=len(fun_cogs)))),
        )
        help_Embed.add_field(
            name="Wikipedia",
            value="\n".join(
                f"```{key}```"
                for key in (i.name for i in self.bot.get_cog("Wiki").get_commands())
            ),
            inline=False,
        )
        help_Embed.add_field(
            name="MCQ Based Quiz",
            value="\n".join(
                f"```{key}```"
                for key in (i.name for i in self.bot.get_cog("QuesAns").get_commands())
            ),
        )
        help_Embed.add_field(
            name="Image",
            value="\n".join(
                f"`{key}`"
                for key in (
                    i.name for i in self.bot.get_cog("Imageprocessing").walk_commands()
                )
            ),
            inline=False,
        )
        help_Embed.add_field(
            name="General",
            value="\n".join(f"`{key}`" for key in general_commands),
            inline=True,
        )
        help_Embed.add_field(
            name="Mod commands",
            value="\n".join(f"`{key}`" for key in intro_commands[5:]),
            inline=True,
        )
        help_Embed.set_footer(
            text="Thanks for using me, have fun! 💖",
            icon_url="https://cdn.discordapp.com/emojis/846481130981949450.gif?v=1%22",
        )
        await ctx.send(embed=help_Embed)

    @help.command()
    async def intro(self, ctx):

        em = discord.Embed(
            title=f"{self.prefix}intro",
            description="Gives introduction of the bot",
            color=ctx.author.color,
        )
        await ctx.send(embed=em)

    @help.command(aliases=["s"])
    async def sum(self, ctx):

        em = discord.Embed(
            title="Summation",
            description="Returns sum of numbers",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"{self.prefix}sum | {self.prefix}s",
            value=f"{self.prefix}sum <numbers>",
        )
        await ctx.send(embed=em)

    @help.command()
    async def fib(self, ctx):

        em = discord.Embed(
            title="Fibonacci",
            description="Returns fibonacci series of nth index",
            color=ctx.author.color,
        )
        em.add_field(name=f"{self.prefix}fib", value=f"{self.prefix}fib <integer>")
        await ctx.send(embed=em)

    @help.command()
    async def invite(self, ctx):

        em = discord.Embed(
            title="Invite",
            description="Gives you an invite link to join in this server",
            color=ctx.author.color,
        )
        em.add_field(name=f"{self.prefix}invite", value=f"{self.prefix}invite")
        await ctx.send(embed=em)

    @help.command(aliases=["chnick"])
    async def changenick(self, ctx):

        em = discord.Embed(title="Changes your nickname", color=ctx.author.color)
        em.add_field(
            name=f"{self.prefix}changenick | {self.prefix}chnick",
            value=f"{self.prefix}changenick <nickname>",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["setwlcm"])
    async def setwelcome(self, ctx):
        em = discord.Embed(
            title="Sets welcome message to a specific channel", color=ctx.author.color
        )
        em.add_field(
            name=f"{self.prefix}setwelcome | {self.prefix}setwlcm", value=("\u200b")
        )
        await ctx.send(embed=em)

    @help.command()
    async def kick(self, ctx):

        em = discord.Embed(
            title="Kick",
            description="Kicks member from the server",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"{self.prefix}kick",
            value=f"{self.prefix}kick <mention member> <reason>",
        )
        await ctx.send(embed=em)

    @help.command()
    async def ban(self, ctx):

        em = discord.Embed(
            title="Ban",
            description="Bans member from the server",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"{self.prefix}ban",
            value=f"{self.prefix}ban <mention member> <reason>",
        )
        await ctx.send(embed=em)

    @help.command()
    async def unban(self, ctx):

        em = discord.Embed(
            title="Unban",
            description="Unbans member from the server",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"{self.prefix}unban",
            value=f"{self.prefix}unban <username#discriminator> <reason>",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["ui"])
    async def userinfo(self, ctx):

        em = discord.Embed(
            title="User Info",
            description="Gives user information",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"{self.prefix}userinfo | {self.prefix}ui",
            value=f"{self.prefix}ui <mention member>(Optional)",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["si"])
    async def serverinfo(self, ctx):

        em = discord.Embed(
            title="Server Info",
            description="Gives server information",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"{self.prefix}serverinfo | {self.prefix}si",
            value=("\u200b"),
            inline=True,
        )
        await ctx.send(embed=em)

    @help.command(aliases=["i"])
    async def inspire(self, ctx):
        em = discord.Embed(
            title="Inspirational quotes",
            description="Sends inspirational quotes",
            color=ctx.author.color,
        )
        em.add_field(name=f"{self.prefix}inspire | {self.prefix}i", value=("\u200b"))
        await ctx.send(embed=em)

    @help.command(aliases=["j"])
    async def joke(self, ctx):
        em = discord.Embed(
            title="Funny jokes",
            description="Serves random jokes to your plate",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"{self.prefix}joke | {self.prefix}j",
            value=f"{self.prefix}joke <`spooky`,`dark` ,`pun`,`christmas`, `misc`>*(optional)*",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["cinfo"])
    async def cityinfo(self, ctx):
        em = discord.Embed(
            title="City information",
            description="Gives weather and global position of a city",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"{self.prefix}cityinfo | {self.prefix}cinfo",
            value=f"{self.prefix}cityinfo <name of the city, *country(optional)*>",
        )
        await ctx.send(embed=em)

    @help.command()
    async def covidinfo(self, ctx):
        em = discord.Embed(
            title="Covid infomation",
            description=f"Gives current covid data of a state, \
                type {self.prefix}covidliststates \
                for the list all states available",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"{self.prefix}covidinfo",
            value=f"{self.prefix}covidinfo <name of any Indian state>",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["covidlst"])
    async def covidliststates(self, ctx):
        em = discord.Embed(
            title="Covid info available for these states",
            description="Gives a list of all states available for the covid data",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"{self.prefix}covidliststates | {self.prefix}covidlst",
            value=("\u200b"),
        )
        await ctx.send(embed=em)

    @help.command(aliases=["g"])
    async def gif(self, ctx):
        em = discord.Embed(
            title="Funny gifs", description="Sends gif images", color=ctx.author.color
        )
        em.add_field(
            name=f"{self.prefix}gif | {self.prefix}g",
            value=f"{self.prefix}gif *<search query>(optional)*",
        )
        await ctx.send(embed=em)

    @help.command()
    async def wiki(self, ctx):
        em = discord.Embed(
            title="Wikipedia",
            description="Searches wikipedia for a query",
            color=ctx.author.color,
        )
        em.add_field(name=f"{self.prefix}wiki", value=f"{self.prefix}wiki <query>")
        await ctx.send(embed=em)

    @help.command()
    async def mcq(self, ctx):
        em = discord.Embed(
            title="MCQ",
            description="Sends multiple choice questions",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"{self.prefix}mcq", value=f"{self.prefix}mcq <category_index>"
        )
        await ctx.send(embed=em)

    @help.command()
    async def meme(self, ctx):
        em = discord.Embed(
            title="Meme", description="Sends memes", color=ctx.author.color
        )
        em.add_field(
            name=f"{self.prefix}meme",
            value=f"{self.prefix}meme *<search query>(optional)*",
        )
        await ctx.send(embed=em)

    @help.command()
    async def geo(self, ctx):
        em = discord.Embed(
            title="Geo",
            description="Gives you distance among the locations",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"{self.prefix}geo",
            value=f"{self.prefix}geo <location1> <location2> *<location3>(optional)*",
        )
        await ctx.send(embed=em)

    @help.command()
    async def img(self, ctx):
        em = discord.Embed(
            title="Image",
            description="It sends an image after image processing",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"{self.prefix}img",
            value=f"{self.prefix}img <img subcommands>.\nType {self.prefix}img for more info",
        )
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Help(bot))
