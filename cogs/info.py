import discord
from discord.ext import commands
from pytz import timezone


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tz = timezone("Asia/Kolkata")

    @commands.command(name="userinfo", aliases=["ui"])
    async def user_info(self, ctx, mem: discord.Member = None):

        mem = mem or ctx.author
        embed = discord.Embed(title="User information", color=mem.color)

        embed.set_thumbnail(url=mem.avatar_url)

        fields = [
            ("Name", str(mem), True),
            ("ID", mem.id, True),
            ("Bot?", mem.bot, True),
            ("Top role", mem.top_role, True),
            ("Status", str(mem.status).title(), True),
            (
                "Activity",
                f"{str(mem.activity.type).split('.')[-1].title() if mem.activity else 'N/A'} {mem.activity.name if mem.activity else ''}",
                True,
            ),
            (
                "Created at",
                mem.created_at.replace(tzinfo=timezone("UTC"))
                .astimezone(tz=self.tz)
                .strftime("%d/%m/%Y %H:%M:%S"),
                True,
            ),
            (
                "Joined at",
                mem.joined_at.replace(tzinfo=timezone("UTC"))
                .astimezone(tz=self.tz)
                .strftime("%d/%m/%Y %H:%M:%S"),
                True,
            ),
            ("Boosted", bool(mem.premium_since), True),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", aliases=["si"])
    async def server_info(self, ctx):

        statuses = [
            len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members))),
        ]

        fields = [
            ("ID", ctx.guild.id, True),
            ("Owner", ctx.guild.owner, True),
            ("Region", ctx.guild.region, True),
            (
                "Created at",
                ctx.guild.created_at.replace(tzinfo=timezone("UTC"))
                .astimezone(tz=self.tz)
                .strftime("%d/%m/%Y %H:%M:%S"),
                True,
            ),
            ("Members", ctx.guild.member_count, True),
            ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
            ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
            (
                "Statuses",
                f"*🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}*",
                True,
            ),
            ("Text channels", len(ctx.guild.text_channels), True),
            ("Voice channels", len(ctx.guild.voice_channels), True),
            ("Categories", len(ctx.guild.categories), True),
            ("Roles", len(ctx.guild.roles), True),
        ]

        embed = discord.Embed(title="Server information", color=ctx.guild.owner.color)
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        embed.set_footer(text="🟢= online 🟠= idle 🔴= dnd ⚪= offline")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
