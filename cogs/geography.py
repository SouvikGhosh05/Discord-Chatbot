import discord
from decimal import Decimal
from asyncio import gather
from discord.ext import commands
from geopy import distance
from geopy.adapters import AioHTTPAdapter
from geopy.extra.rate_limiter import AsyncRateLimiter
from geopy.geocoders import Nominatim


class GeoSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="geo")
    async def global_location(self, ctx, *, location: str = None):

        if location:
            if (
                length_splitted_location := (len(splitted_location := location.split()))
            ) >= 2:
                async with ctx.typing():
                    try:
                        async with Nominatim(
                            user_agent="DiscordApp", adapter_factory=AioHTTPAdapter
                        ) as geolocator:
                            geocode = AsyncRateLimiter(
                                geolocator.geocode, min_delay_seconds=1 / 20
                            )
                            locator = await gather(
                                *(
                                    geocode(s, language="en", timeout=None)
                                    for s in splitted_location
                                )
                            )
                        position = (
                            (location.latitude, location.longitude)
                            for location in locator
                        )
                        total_distance = round(
                            Decimal(distance.distance(*position).km), 3
                        )
                        title = (
                            f"Distance among {', '.join(splitted_location[:-1]).title()} and {splitted_location[-1].title()}"
                            if length_splitted_location > 2
                            else f"Distance between {splitted_location[0].title()} and {splitted_location[1].title()}"
                        )
                        embed = discord.Embed(
                            title=title,
                            description=f"{total_distance} kilometers",
                            color=discord.Color.blue(),
                        )
                        embed.set_footer(
                            text="Kindly note: put '-' among multiple words for each locations.",
                            icon_url="https://cdn2.iconfinder.com/data/icons/solar_system_png/512/Earth.png",
                        )
                    except Exception:
                        await ctx.send("**Sorry, invalid location was entered!**")
                await ctx.send(embed=embed)
            else:
                await ctx.send("Please enter at least two locations.")
        else:
            await ctx.send("Sorry no locations were entered!")


def setup(bot):
    bot.add_cog(GeoSearch(bot))
