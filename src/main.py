import discord
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound

# from dotenv import load_dotenv
import asyncio
import os

# load_dotenv(".env")
Token = os.getenv("DISCORD_TOKEN")
intents = discord.Intents().all()
bot = commands.Bot(
    command_prefix="~", help_command=None, intents=intents, case_insensitive=True
)


@bot.event
async def on_ready():
    change_status.start()
    print("Bot has logged in")


@tasks.loop(seconds=30)
async def change_status():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="~help 😃")
    )
    await asyncio.sleep(15)
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name="BOT! 🤖")
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("**Invalid command! Type <~h> for more info**")


with os.scandir("./cogs") as cog_dir:
    for cog in cog_dir:
        if cog.is_file() and cog.name.endswith(".py"):
            bot.load_extension(f"cogs.{cog.name[:-3]}")

if __name__ == "__main__":
    bot.run(Token)
