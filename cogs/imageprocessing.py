import discord
from asyncio import to_thread
from io import BytesIO
from typing import IO, Any
from discord.ext import commands
from PIL import Image, ImageFilter


def contour_image(fp: IO[Any]):
    with Image.open(fp) as img:
        img = img.convert("RGBA")
        im1 = img.filter(ImageFilter.CONTOUR)

        with BytesIO() as byte_s:
            im1.save(byte_s, format="PNG")
            byte_s.seek(0)
            binary_byte, is_readable = byte_s.getvalue(), byte_s.readable()
    return binary_byte, is_readable


def emboss_image(fp: IO[Any]):
    with Image.open(fp) as img:
        img = img.convert("RGBA")
        im1 = img.filter(ImageFilter.EMBOSS)

        with BytesIO() as byte_s:
            im1.save(byte_s, format="PNG")
            byte_s.seek(0)
            binary_byte, is_readable = byte_s.getvalue(), byte_s.readable()
    return binary_byte, is_readable


class Imageprocessing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="img", invoke_without_command=True)
    async def image(self, ctx):
        cogname = self.bot.get_cog(ctx.command.cog_name)
        walking = [i.name for i in cogname.walk_commands()]
        img_em = discord.Embed(
            title=f"`{self.bot.command_prefix}{ctx.command.name}`",
            description="\n".join(walking[1:]),
            colour=discord.Colour.random(),
        )
        img_em.set_author(name="Image Commands", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=img_em)

    @image.command(name="contour")
    async def image_contour(self, ctx, user: commands.MemberConverter = None):

        async with ctx.typing():
            user = user or ctx.author
            asset = user.avatar_url_as()
            binary, condition = await to_thread(
                contour_image, fp=BytesIO(await asset.read())
            )
            (
                await ctx.send(
                    file=discord.File(fp=BytesIO(binary), filename=f"{user.name}.png")
                )
                if condition
                else await ctx.send("Image processing failed!")
            )

    @image.command(name="emboss")
    async def image_emboss(self, ctx, user: commands.MemberConverter = None):

        async with ctx.typing():
            user = user or ctx.author
            asset = user.avatar_url_as()
            binary, condition = await to_thread(
                emboss_image, fp=BytesIO(await asset.read())
            )
            (
                await ctx.send(
                    file=discord.File(fp=BytesIO(binary), filename=f"{user.name}.png")
                )
                if condition
                else await ctx.send("Image processing failed!")
            )


def setup(bot):
    bot.add_cog(Imageprocessing(bot))
