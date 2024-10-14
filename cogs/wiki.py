import discord
from discord.ext import commands
from aiohttp import ClientSession


class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wiki")
    async def wiki_search(self, ctx, *, search: str = None):
        if search:
            async with ctx.typing():
                url = "https://en.wikipedia.org/w/api.php"
                query_search = {
                    "action": "query",
                    "list": "search",
                    "format": "json",
                    "srsearch": search.lower(),
                    "srlimit": "10",
                }
                async with ClientSession() as session:
                    async with session.get(url, params=query_search) as resp:
                        data_json = await resp.json()

                if data_json["query"]["searchinfo"]["totalhits"] == 0:
                    await ctx.send("Sorry, your search could not be found!")
                else:
                    title = [i["title"] for i in data_json["query"]["search"]]
                    indexed_title = (
                        search.title() if search.title() in title else title[0]
                    )
                    search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{indexed_title}"
                    querystring = {"redirect": "true"}

                    async with ClientSession() as session:
                        async with session.get(search_url, params=querystring) as resp:
                            content_json = await resp.json()

                    if content_json["type"] != "disambiguation":
                        embed = discord.Embed(
                            title=content_json["title"],
                            description=content_json["extract"],
                            url=(
                                content_json["content_urls"]["mobile"]["page"]
                                if ctx.author.is_on_mobile()
                                else content_json["content_urls"]["desktop"]["page"]
                            ),
                            color=discord.Color.random(),
                        )
                        (
                            embed.set_thumbnail(url=content_json["thumbnail"]["source"])
                            if "thumbnail" in content_json
                            else None
                        )
                    else:
                        embed = discord.Embed(
                            title="Disambiguated Page!", color=discord.Color.random()
                        )

                    embed.add_field(name="Related Searches", value="\n".join(title[1:]))
                    embed.set_author(
                        name="Wikipedia",
                        icon_url="https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png",
                    )
                    embed.set_footer(
                        text=f"Requested by {ctx.author.name}",
                        icon_url=ctx.author.avatar_url,
                    )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Please enter a search query...")


def setup(bot):
    bot.add_cog(Wiki(bot))
