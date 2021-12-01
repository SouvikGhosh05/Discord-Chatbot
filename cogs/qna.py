import discord
from aiohttp import ClientSession
from json import loads
from random import shuffle
from html import unescape
from discord.ext import commands
from discord_components import (
    DiscordComponents,
    Button,
    Select,
    SelectOption,
    ButtonStyle,
)
from asyncio import gather, TimeoutError


json_data = """
{
    "General Knowledge"     : "9",
    "Books"                 : "10",
    "Movies"                : "11",
    "Music"                 : "12",
    "Television"            : "14",
    "Musicals & Theatres"   : "13",
    "Comics"                : "29",
    "Japanese Anime"        : "31",
    "Cartoons"              : "32",
    "Video Games"           : "15",
    "Board Games"           : "16",
    "Science & Nature"      : "17",
    "Computers & Internet"  : "18",
    "Gadgets"               : "30",
    "Mathematics"           : "19",
    "Mythology"             : "20",
    "Sports"                : "21",
    "Geography"             : "22",
    "History"               : "23",
    "Politics"              : "24",
    "Art"                   : "25",
    "Celebrities"           : "26",
    "Animals"               : "27",
    "Vehicles"              : "28"
}
"""


json_dict = loads(json_data)


class QuesAns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mcq")
    async def multiple_choice(self, ctx, *, category: str = None):
        try:
            category_dict = {
                index + 1: categories
                for index, categories in enumerate(json_dict.keys())
            }
            button_embed = discord.Embed(
                title="Multiple Choice",
                description="Each questions will be Multiple Choice questions. For each correct answers you will receive 5 points. Each questions will have 15 seconds timeout.",
                color=discord.Color.dark_magenta(),
            )
            button_embed.add_field(
                name="Question categories",
                value="\n".join(
                    f"{key}\t\t\t{value}" for key, value in category_dict.items()
                ),
            )
            button_embed.set_footer(
                text="*Put any index from these category listed above and press the green button to start!*",
                icon_url="https://cdn0.iconfinder.com/data/icons/online-education-butterscotch-vol-2/512/Online_Tests-512.png",
            )
            m = await ctx.send(
                embed=button_embed,
                components=[
                    Button(
                        style=ButtonStyle.green,
                        label="Start Quiz 😃",
                        disabled=(
                            is_notcategory := (not category)
                            if (
                                iscondition := (
                                    category
                                    and (
                                        in_dict := (
                                            (stripped := int(category.strip()))
                                            in category_dict
                                        )
                                    )
                                )
                            )
                            else True
                        ),
                    ),
                    Button(
                        style=ButtonStyle.red,
                        label="Cancel ☹️",
                        disabled=is_notcategory if iscondition else True,
                    ),
                ],
            )
            await ctx.send(
                "Invalid category entered, select any category from this list above!"
            ) if not in_dict else None

            res = await self.bot.wait_for("button_click", timeout=10)
            if ctx.author == res.user and res.channel == ctx.channel:

                if res.component.label.startswith("Cancel"):
                    await m.edit(
                        "Already responded!",
                        components=[
                            Button(
                                style=ButtonStyle.red,
                                label="Test canceled!",
                                disabled=True,
                            )
                        ],
                    )
                    await res.respond(
                        content=f"Sorry, you have cancelled the test {ctx.author.mention}"
                    )
                    return
                await m.edit(
                    "Already responded!",
                    components=[
                        Button(
                            style=ButtonStyle.green, label="Good Luck!", disabled=True
                        )
                    ],
                )

                async def fetch_api():
                    url = "https://opentdb.com/api.php"
                    querystring = {
                        "amount": "10",
                        "category": json_dict[category_dict[stripped]],
                        "type": "multiple",
                    }
                    async with ClientSession() as session:
                        async with session.get(url, params=querystring) as resp:
                            data = await resp.json()
                    return data

                response, _, _, _ = await gather(
                    fetch_api(),
                    m.add_reaction(emoji="\U00002705"),
                    m.add_reaction(emoji="\U0001F3AF"),
                    res.respond(
                        content=f"Check DM for your quiz! {ctx.author.mention}"
                    ),
                )
                score, no_of_correct_questions_answered = 0, 0
                for i in response["results"]:
                    answers = [*i["incorrect_answers"], i["correct_answer"]]
                    shuffle(answers)
                    try:
                        await res.user.send(
                            unescape(i["question"]),
                            components=[
                                Select(
                                    placeholder="Select your answer!",
                                    max_values=1,
                                    options=[
                                        SelectOption(
                                            label=str(answers[0]), value=str(answers[0])
                                        ),
                                        SelectOption(
                                            label=str(answers[1]), value=str(answers[1])
                                        ),
                                        SelectOption(
                                            label=str(answers[2]), value=str(answers[2])
                                        ),
                                        SelectOption(
                                            label=str(answers[3]), value=str(answers[3])
                                        ),
                                    ],
                                )
                            ],
                        )

                        interaction = await self.bot.wait_for(
                            "select_option", timeout=15
                        )
                        await interaction.respond(
                            content=f"{interaction.component[0].label} selected!"
                        )
                        score += (
                            5
                            if (
                                is_correct := (
                                    interaction.component[0].value
                                    == i["correct_answer"]
                                )
                            )
                            else 0
                        )
                        no_of_correct_questions_answered += 1 if is_correct else 0
                    except TimeoutError:
                        await res.user.send("Timed out!")
                        await res.user.send(
                            content=f"For each correct answers, you get 5.\nYou scored `5*{no_of_correct_questions_answered}= {score}`! 😄\nThanks for playing with bot!...."
                        ) if score > 0 else await res.user.send(
                            "You scored 0. Better luck next time! 🙂"
                        )
                        break
                else:
                    await res.user.send(
                        content=f"For each correct answers, you get 5.\nYou scored `5*{no_of_correct_questions_answered}= {score}`! 😄\nThanks for playing with bot!...."
                    ) if score > 0 else await res.user.send(
                        "You scored 0. Better luck next time! 🙂"
                    )
            else:
                await m.edit(
                    "Wrong user responded!",
                    components=[
                        Button(style=ButtonStyle.red, label="Try again!", disabled=True)
                    ],
                )
                await res.respond(
                    content=f"Type {self.bot.command_prefix}mcq for your turn!"
                )
        except TimeoutError:
            await m.edit(
                "Prompt timed out!",
                components=[
                    Button(style=ButtonStyle.red, label="Timed out!", disabled=True)
                ],
            )
        except ValueError:
            await ctx.send(
                f"Invalid category entered! Type `{self.bot.command_prefix}mcq` again for the category list."
            )


def setup(bot):
    DiscordComponents(bot)
    bot.add_cog(QuesAns(bot))
