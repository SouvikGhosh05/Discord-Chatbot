import discord
from discord.ext import commands
from aiohttp import ClientSession
import random
import os


class GIF(commands.Cog):

    Rapid_A = os.getenv("RAPID_API2")
    Giphy_A = os.getenv("GIPHY_API")

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gif", aliases=["g"])
    async def send_gifs(self, ctx, *, q=None):

        async with ctx.typing():
            headers = {
                "x-rapidapi-key": GIF.Rapid_A,
                "x-rapidapi-host": "giphy.p.rapidapi.com",
            }
            if q:
                url = "https://giphy.p.rapidapi.com/v1/gifs/search"
                querystring = {
                    "api_key": GIF.Giphy_A,
                    "q": q,
                    "limit": "50",
                    "rating": "g",
                }
                async with ClientSession() as session:
                    async with session.get(
                        url, headers=headers, params=querystring
                    ) as resp:
                        response = await resp.json()

                gif_id1 = response["data"][random.randrange(49)]["id"]
                url_em1 = f"https://media.giphy.com/media/{gif_id1}/giphy.gif"
                title = q.title()
                em = discord.Embed(title=title, color=discord.Color.random())
                em.set_image(url=url_em1)
            else:
                url = "https://giphy.p.rapidapi.com/v1/gifs/random"
                querystring = {"api_key": GIF.Giphy_A, "rating": "g"}
                async with ClientSession() as session:
                    async with session.get(
                        url, headers=headers, params=querystring
                    ) as resp:
                        response = await resp.json()

                gif_id2 = response["data"]["id"]
                url_em2 = f"https://media.giphy.com/media/{gif_id2}/giphy.gif"
                title = "Random"
                em = discord.Embed(title=title, color=discord.Color.random())
                em.set_image(url=url_em2)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(GIF(bot))
