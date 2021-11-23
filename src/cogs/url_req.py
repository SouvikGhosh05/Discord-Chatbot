import discord
from discord.ext import commands
from aiohttp import ClientSession
from decimal import Decimal as dc
from json import load
from os import getenv, getcwd

print(getcwd())

with open("./states.json", "r") as json_data:
    json_dict = load(json_data)


class Ext_Info(commands.Cog):

    C_api = getenv("City_API")

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cityinfo", aliases=["cinfo"])
    async def get_cityinfo(self, ctx, *, message=None):

        if message:
            async with ctx.typing():
                fetch_url = f"https://api.openweathermap.org/data/2.5/weather?q={message}&appid={Ext_Info.C_api}"
                async with ClientSession() as session:
                    async with session.get(fetch_url) as resp:
                        c_res = await resp.json()

                if "message" in c_res.keys():
                    await ctx.send("**Incorrect city name, recheck again!**")

                city_info = {
                    "city": c_res["name"],
                    "country": c_res["sys"]["country"],
                    "position": f"lat: {c_res['coord']['lat']}, lon: {c_res['coord']['lon']}",
                    "temperature": round(dc(c_res["main"]["temp"] - 273), 3),
                    "temp_feelslike": round(dc(c_res["main"]["feels_like"] - 273), 3),
                    "humidity": c_res["main"]["humidity"],
                    "description": c_res["weather"][0]["description"],
                    "wind_speed": round(dc(c_res["wind"]["speed"] * 3.6), 2),
                    "wind_deg": f"{c_res['wind']['deg']}°",
                    "icon": c_res["weather"][0]["icon"],
                }

                city_embed = discord.Embed(
                    title="City information", color=discord.Color.random()
                )
                city_embed.set_thumbnail(
                    url=f"https://openweathermap.org/img/w/{city_info['icon']}.png"
                )
                city_embed.add_field(name="City", value=city_info["city"])
                city_embed.add_field(name="Position", value=city_info["position"])
                city_embed.add_field(name="Country", value=city_info["country"])
                city_embed.add_field(
                    name="Temperature",
                    value=f"{city_info['temperature']}°C, *feels like* {city_info['temp_feelslike']}°C, *humidity* {city_info['humidity']}%",
                )
                city_embed.add_field(
                    name="Wind speed",
                    value=f"{city_info['wind_speed']}km/h, *direction* {city_info['wind_deg']}",
                )
                city_embed.add_field(name="Description", value=city_info["description"])
            await ctx.send(embed=city_embed)
        else:
            await ctx.send("**Please provide a city name!**")

    @commands.command(name="covidinfo")
    async def covid_info(self, ctx, *, state: str = None):
        if state:
            async with ctx.typing():
                try:

                    async def get_metadata(y):
                        return {"7days info": y["delta7"], "data_info": y["meta"]}

                    async def get_response(x):
                        url = "https://api.covid19india.org/v4/min/data.min.json"
                        try:
                            async with ClientSession() as session:
                                async with session.get(url) as resp:
                                    data = await resp.json()
                            return await get_metadata(data[x])
                        except KeyError:
                            await ctx.send(
                                "**Sorry, Covid info not found for this state. ☹️**"
                            )

                    state_removewhitespaces = " ".join(state.split())
                    st_info = await get_response(
                        json_dict[state_removewhitespaces.title()]
                    )
                    data = {
                        "population": st_info["data_info"]["population"],
                        "tested_people": st_info["7days info"]["tested"]
                        if "tested" in st_info["7days info"].keys()
                        else 0,
                        "confirmed": st_info["7days info"]["confirmed"]
                        if "confirmed" in st_info["7days info"].keys()
                        else 0,
                        "recovered": st_info["7days info"]["recovered"]
                        if "recovered" in st_info["7days info"].keys()
                        else 0,
                        "deceased": st_info["7days info"]["deceased"]
                        if "deceased" in st_info["7days info"].keys()
                        else 0,
                        "1st_dose": st_info["7days info"]["vaccinated1"]
                        if "vaccinated1" in st_info["7days info"].keys()
                        else 0,
                        "2nd_dose": st_info["7days info"]["vaccinated2"]
                        if "vaccinated2" in st_info["7days info"].keys()
                        else 0,
                        "test_date": st_info["data_info"]["tested"]["date"]
                        if "date" in st_info["data_info"]["tested"].keys()
                        else "*Not Available*",
                        "source": st_info["data_info"]["tested"]["source"]
                        if "source" in st_info["data_info"]["tested"].keys()
                        else "*Not Available*",
                        "last_updated": f"*{st_info['data_info']['last_updated'][:10]} at {st_info['data_info']['last_updated'][11:19]}*",
                    }

                    recovery_rate = (
                        f"{round(dc((data['recovered']*100)/data['confirmed']), 2)}%"
                    )
                    covid_embed = discord.Embed(
                        title=f"Information of {state_removewhitespaces.title()} in past 7 days",
                        color=discord.Color.random(),
                    )
                    covid_embed.set_author(
                        name="Coronavirus Info",
                        icon_url="https://cdn.discordapp.com/attachments/857225424115597334/874307648953147422/7528_coronavirus.png",
                    )
                    covid_embed.add_field(name="Population", value=data["population"])
                    covid_embed.add_field(
                        name="People tested", value=data["tested_people"]
                    )
                    covid_embed.add_field(
                        name="Active cases",
                        value=f"*Confirmed cases: {data['confirmed']}, Recovered: {data['recovered']}, \nRecovery rate: {recovery_rate}, Deceased: {data['deceased']}*",
                    )
                    covid_embed.add_field(
                        name="Results tested on", value=data["test_date"]
                    )
                    covid_embed.add_field(
                        name="People vaccinated",
                        value=f"*1st dose taken by {data['1st_dose']} people, 2nd dose taken by {data['2nd_dose']} people*",
                    )
                    covid_embed.add_field(name="Source of data", value=data["source"])
                    covid_embed.add_field(
                        name="Last updated on", value=data["last_updated"]
                    )
                    covid_embed.set_footer(
                        text=f"Requested by {ctx.author.name}",
                        icon_url=ctx.author.avatar_url,
                    )

                except KeyError:
                    covid_embed = discord.Embed(
                        title="**You mispelled the state name, Reenter again!**",
                        color=discord.Color.red(),
                    )
            await ctx.send(embed=covid_embed)
        else:
            await ctx.send("Please enter a state name!")

    @commands.command(name="covidliststates", aliases=["covidlst"], pass_context=True)
    async def states_list(self, ctx):

        states_dict = {
            select + 1: states for select, states in enumerate(json_dict.keys())
        }

        states_embed = discord.Embed(
            title="List of Indian states",
            description="\n".join(
                f"{key}\t\t{value}" for key, value in states_dict.items()
            ),
            color=discord.Color.random(),
        )
        await ctx.send(embed=states_embed)


def setup(bot):
    bot.add_cog(Ext_Info(bot))
