import discord
import asyncio
from os import getenv
from random import choice
from aiohttp import ClientSession, BasicAuth
from discord.ext import commands

AUTH_KEY = None
subreddits = [
    "memes",
    "meme",
    "wholesomememes",
    "dankmemes",
    "raimimemes",
    "historymemes",
    "okbuddyretard",
    "comedyheaven",
    "PrequelMemes",
    "AdviceAnimals",
    "terriblefacebookmemes",
    "ProgrammerHumor",
    "programmingmemes",
    "IndianDankMemes",
    "HistoryMemes",
    "codinghumor",
]


async def get_auth_key():

    global AUTH_KEY
    CLIENT_ID = getenv("R_CLIENT_ID")
    CLIENT_SECRET = getenv("R_CLIENT_SECRET")
    PASSWORD = getenv("R_PASSWORD")
    USERNAME = getenv("R_USERNAME")

    client_auth = BasicAuth(CLIENT_ID, CLIENT_SECRET)
    headers = {"User-Agent": "Discord_Bot"}
    url = "https://www.reddit.com/api/v1/access_token"
    post_data = {"grant_type": "password", "username": USERNAME, "password": PASSWORD}
    async with ClientSession(auth=client_auth) as session:
        async with session.post(url, data=post_data, headers=headers) as response:
            AUTH_KEY = await response.json()
    AUTH_KEY = AUTH_KEY["access_token"]


async def call():
    while True:
        asyncio.create_task(get_auth_key())
        print("Running")
        await asyncio.sleep(60 * 30)  # task runs every 30 minutes


async def reddit_query(query=None):

    headers = {"Authorization": f"bearer {AUTH_KEY}", "User-Agent": "Discord_Bot"}
    if not query:
        querystring = {"limit": "100"}
        async with ClientSession() as session:
            async with session.get(
                f"https://oauth.reddit.com/r/{choice(subreddits)}/top",
                headers=headers,
                params=querystring,
            ) as response:
                response = await response.json()
    else:
        querystring = {
            "limit": "100",
            "q": query,
            "sort": choice(["best", "top"]),
            "over_18": "false",
        }
        async with ClientSession() as session:
            async with session.get(
                f"https://oauth.reddit.com/r/{choice(subreddits)}/search",
                headers=headers,
                params=querystring,
            ) as response:
                response = await response.json()

    response = response["data"]["children"]
    title, url = choice(
        list(
            zip(
                [
                    x["data"]["title"]
                    for x in response
                    if x["data"]["url"].startswith("https://i.redd.it")
                ],
                [
                    x["data"]["url"]
                    for x in response
                    if x["data"]["url"].startswith("https://i.redd.it")
                ],
            )
        )
    )
    return title, url


class RedditApi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(call())

    @commands.command(name="meme")
    async def reddit_search(self, ctx, *, query=None):
        async with ctx.typing():
            title, url = (
                await reddit_query() if not query else await reddit_query(query.lower())
            )
            if title and url:
                embed = discord.Embed(title=title, color=discord.Color.random())
                embed.set_image(url=url)
            else:
                embed = discord.Embed(
                    title="Error",
                    description="Sorry, meme not found, try again!",
                    color=discord.Color.red(),
                )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(RedditApi(bot))
