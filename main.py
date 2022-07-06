import interactions
from loguru import logger
from custom_survey import custom_modal_receiver, make_custom_modal
import os


bot = interactions.Client(
    token=os.getenv("DISCORD_BOT_TOKEN")
)


@bot.command(
    name="survey",
    description="Create a new Survey",
    scope=[840097260095275028],
    options=[
        interactions.Option(
            name="custom",
            description="A custom survey",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="option_count",
                    description="How many options your survey will have",
                    type=interactions.OptionType.INTEGER,
                    required=True,
                    min_value=1,
                    max_value=4
                )
            ]
        ),
        interactions.Option(
            name="yes_no",
            description="A simple yes-no Survey",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="question",
                    description="Your Survey Question",
                    type=interactions.OptionType.STRING,
                    required=True,
                    min_length=1,
                    max_length=75
                )
            ]
        ),
        interactions.Option(
            name="agree-scale",
            description="A 1-5 opinion Survey",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="question",
                    description="Your Survey Question",
                    type=interactions.OptionType.STRING,
                    required=True,
                    min_length=1,
                    max_length=75
                )
            ]
        )
    ]
)
async def survey(ctx, sub_command, question=None, option_count=None):
    if sub_command == "custom":
        await ctx.popup(make_custom_modal(option_count))
    elif sub_command == "yes_no":
        await ctx.send("Not implemented")
    elif sub_command == "agree_scale":
        await ctx.send("Not implemented")


@bot.modal("custom-survey-modal")
async def modal_receiver(ctx, question, option1=None, option2=None, option3=None, option4=None):
    logger.info("received the callback")
    await custom_modal_receiver(ctx, question, option1, option2, option3, option4)


bot.start()
