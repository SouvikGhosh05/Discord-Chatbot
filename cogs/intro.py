import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ext.commands.errors import BotMissingPermissions
from asyncio import gather
from async_lru import alru_cache
from zoneinfo import ZoneInfo


class Main_BOT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tz = ZoneInfo("Asia/Kolkata")

    @commands.Cog.listener()
    async def on_member_join(self, member):

        mem = member.id
        user = self.bot.get_user(mem)

        channel = member.guild.text_channels[0].id
        welcome_emby = discord.Embed(
            title="New Member!!!",
            description=f"{member.mention} has joined the server! \
                🎉\nThe current number of members are {member.guild.member_count} 🥳",
            color=discord.Color.gold(),
        )
        await self.bot.get_channel(int(channel)).send(embed=welcome_emby)
        if not member.bot:
            github_url = "https://github.com/SouvikGhosh05"
            await user.send(
                f"SouvikBot welcomes you to {member.guild.name}! \
                ❤️\nThis bot is developed by Souvik, check out him on Github. \
                Link is given below:- \n{github_url}"
            )

    @commands.command(name="intro")
    async def on_intro(self, ctx):
        appinfo = await self.bot.application_info()
        github_url = "https://github.com/SouvikGhosh05"
        await ctx.send(
            f"I'm SouvikBot, thankfully created by ***{appinfo.owner}*** ❤️🥰 !\nHis Github url:- {github_url}"
        )

    @commands.command(name="sum", aliases=["s"])
    async def sum_method(self, ctx, *float_numbers):
        if float_numbers:
            try:
                flt_numbers = [float(i) for i in float_numbers]
            except Exception:
                await ctx.send("Input must be numbers, not string!")
            else:
                sum_embed = discord.Embed(
                    title=f"The sum is {sum(flt_numbers)}", color=discord.Color.green()
                )
                sum_embed.set_thumbnail(
                    url="https://img.icons8.com/color/48/000000/calculator--v2.png"
                )
                await ctx.send(embed=sum_embed)
        else:
            await ctx.send("Sorry, no numbers were entered!")

    @commands.command(name="fib")
    async def fibonacci_method(self, ctx, *int_numbers):
        if int_numbers:
            async with ctx.typing():
                try:
                    integers = [int(i) for i in int_numbers]
                except Exception:
                    fibonacci_embed = discord.Embed(
                        title="Error!",
                        description="Input must be integers, not decimal or string!",
                        color=discord.Color.red(),
                    )
                else:

                    @alru_cache(maxsize=256)
                    async def fib(n):
                        if n < 0:
                            return "Number must be a positive integer!"
                        elif n == 0:
                            return 0
                        elif n == 1:
                            return 1
                        else:
                            return await fib(n - 1) + await fib(n - 2)

                    retured_fibs = await gather(*(fib(x) for x in integers))
                    fibonacci_embed = discord.Embed(
                        title="The nth fibonacci number is:-",
                        description="\n\n".join(
                            f"{int_th}th: {fibo}"
                            for int_th, fibo in zip(integers, retured_fibs)
                        ),
                        color=discord.Color.blurple(),
                    )
                    fibonacci_embed.set_thumbnail(
                        url="https://images-platform.99static.com//5SVBLaS5OIyGp6GsUWz7clXTZ8w=/141x1329:\
                        1354x2539/fit-in/500x500/99designs-contests-attachments/118/118791/attachment_118791273"
                    )
                    fibonacci_embed.set_footer(
                        text="The fibonacci number is generated using the recursive function fib(n) = fib(n-1) + fib(n-2)"
                    )
            await ctx.send(embed=fibonacci_embed)
        else:
            await ctx.send("Please input any positive integer.")

    @commands.command(name="invite")
    @commands.has_permissions(create_instant_invite=True)
    async def invite_method(self, ctx, *, reason=None):
        user = self.bot.get_user(ctx.author.id)
        invitation = await ctx.channel.create_invite(
            reason=reason, max_age=60 * 60 * 24 * 7, max_uses=20
        )
        invitation_time = (
            invitation.created_at.replace(tzinfo=ZoneInfo("UTC"))
            .astimezone(tz=self.tz)
            .strftime("%d/%m/%Y %H:%M:%S")
        )
        invite_embed = discord.Embed(
            title="Invite created!",
            description=f"The invite link is: {invitation.url}\nInvite is created by ***{invitation.inviter.name}***",
            color=discord.Color.green(),
        )
        invite_embed.set_footer(
            text=f"Invite link was created at {invitation_time}, will be active for 7 days from when it was created"
        )
        await ctx.message.delete(delay=2)
        await ctx.send("Check DM for the invite link.", delete_after=3)
        await user.send(embed=invite_embed)

    @invite_method.error
    async def invite_method_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.message.delete(delay=2)
            await ctx.send(
                "**:x: | Sorry, you're not allowed to invite anyone in this server.**",
                delete_after=3,
            )

    @commands.command(name="changenick", aliases=["chnick"])
    @commands.has_guild_permissions(change_nickname=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    async def nickname(self, ctx, *, name=None):
        if name:
            await ctx.author.edit(nick=name)
            await ctx.send("Nickname changed!")
        else:
            await ctx.send("Please provide a nickname!")

    @nickname.error
    async def nickname_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.message.delete(delay=2)
            await ctx.send(
                "**:x: | You don't have permission to change nickname in this server.**",
                delete_after=3,
            )
        elif isinstance(error, BotMissingPermissions):
            await ctx.message.delete(delay=2)
            await ctx.send(
                "**Sorry! Bot has no permission to change nickname in this server ☹️.**",
                delete_after=3,
            )

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason=None):

        if member == ctx.author:
            await ctx.send("**You can't kick yourself!**")
        else:
            await ctx.guild.kick(member, reason=reason)
            await ctx.send(
                f"**{member.mention} has been kicked from {ctx.guild.name}!**"
            )

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.message.delete(delay=2)
            await ctx.send(
                "**:x: | You do not have permission to use this command!**",
                delete_after=3,
            )
        elif isinstance(error, BotMissingPermissions):
            await ctx.message.delete(delay=2)
            await ctx.send(
                "**Sorry! Bot has no permission to kick in this server ☹️.**",
                delete_after=3,
            )

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):

        if member == ctx.author:
            await ctx.send("**You can't ban yourself!**")
        else:
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(
                f"**{member.mention} has been banned from {ctx.guild.name}!**"
            )

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.message.delete(delay=2)
            await ctx.send(
                "**:x: | You do not have permission to use this command!**",
                delete_after=3,
            )
        elif isinstance(error, BotMissingPermissions):
            await ctx.message.delete(delay=2)
            await ctx.send(
                "**Sorry! Bot has no permission to ban in this server ☹️.**",
                delete_after=3,
            )

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member, *, reason=None):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user, reason=reason)
                await ctx.send(
                    f"{user.mention} has been unbanned and able to join again!"
                )
                return

        await ctx.send(f"**{member} was not banned previously!**")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.message.delete(delay=2)
            await ctx.send(
                "**:x: | You do not have permission to use this command!**",
                delete_after=3,
            )
        elif isinstance(error, BotMissingPermissions):
            await ctx.message.delete(delay=2)
            await ctx.send(
                "**Sorry! Bot has no permission to unban in this server ☹️.**",
                delete_after=3,
            )


def setup(bot):
    bot.add_cog(Main_BOT(bot))
