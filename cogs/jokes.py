import discord
from discord.ext import commands
from requests import get
from aiohttp import ClientSession
import os


class Jokes(commands.Cog):

    rapid = os.getenv("RAPID_API1")
    Joke_KEY = os.getenv("RANDOM_JOKES")

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="inspire", aliases=["i"])
    async def get_quotes(self, ctx):
        i_res = get("https://zenquotes.io/api/random").json()
        quote = f"{i_res[0]['q']} -{i_res[0]['a']}"
        await ctx.send(quote)

    @commands.command(name="joke", aliases=["j"])
    async def funny_jokes(self, ctx, *, typed: str = None):

        typed = typed or "any" or "misc"
        if typed.lower() in ["any", "spooky", "dark", "pun", "christmas", "misc"]:
            async with ctx.typing():

                url = "https://random-stuff-api.p.rapidapi.com/joke"

                querystring = {"type": typed.lower()}
                headers = {
                    "authorization": Jokes.Joke_KEY,
                    "x-rapidapi-key": Jokes.rapid,
                    "x-rapidapi-host": "random-stuff-api.p.rapidapi.com",
                }
                async with ClientSession() as session:
                    async with session.get(
                        url, headers=headers, params=querystring
                    ) as resp:
                        response = await resp.json()

                async def choose_joke(x):
                    return (
                        {"question": x["setup"], "answer": x["delivery"]}
                        if "setup" in x.keys()
                        else x["joke"]
                    )

                get_joke = await choose_joke(response)
                joke_embed = discord.Embed(
                    title="Random jokes", color=discord.Color.random()
                )

                if isinstance(get_joke, dict):
                    joke_embed.add_field(
                        name=f"Q: {get_joke['question']}",
                        value=f"A: {get_joke['answer']} 🤣",
                    )
                else:
                    joke_embed.add_field(name="Joke:", value=get_joke)
            await ctx.send(embed=joke_embed)
        else:
            await ctx.send(
                "Please choose a joke type: `spooky`,`dark` ,`pun`,`christmas`, `misc`"
            )


def setup(bot):
    bot.add_cog(Jokes(bot))
