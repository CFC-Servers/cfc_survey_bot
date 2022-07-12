import interactions
import os
import dateparser
import datetime
import types
from custom_survey import make_custom_modal
from yes_no import yes_no_command_receiver
from agree_scale import agree_scale_command_receiver
from send_survey import send_survey


bot = interactions.Client(
    token=os.getenv("DISCORD_BOT_TOKEN", "")
)

bot.send_survey = types.MethodType(send_survey, bot)


@bot.command(
    name="survey",
    description="Create a new Survey",
    scope=[840097260095275028],
    options=[
        interactions.Option(
            name="custom_survey",
            description="A custom survey",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="option_count",
                    description="How many options your Survey will have",
                    type=interactions.OptionType.INTEGER,
                    required=True,
                    min_value=1,
                    max_value=4
                ),
                interactions.Option(
                    name="expires",
                    description="When does your survey expire",
                    type=interactions.OptionType.STRING,
                    required=False,
                    min_length=1,
                    max_length=75
                ),
            ]
        ),
        interactions.Option(
            name="yes_no_survey",
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
                ),
                interactions.Option(
                    name="expires",
                    description="When does your survey expire",
                    type=interactions.OptionType.STRING,
                    required=False,
                    min_length=1,
                    max_length=75
                ),
            ]
        ),
        interactions.Option(
            name="agree_scale_survey",
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
                ),
                interactions.Option(
                    name="expires",
                    description="When does your survey expire",
                    type=interactions.OptionType.STRING,
                    required=False,
                    min_length=1,
                    max_length=75
                ),
            ]
        )
    ]
)
async def survey(ctx, sub_command, question=None, option_count=None, expires=None):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)

    if expires is not None:
        expiration = dateparser.parse(expires, settings={"TIMEZONE": "UTC"})

    if sub_command == "custom_survey":
        await ctx.popup(make_custom_modal(bot, option_count, expires))

    elif sub_command == "yes_no_survey":
        await yes_no_command_receiver(
            bot,
            ctx,
            question=question,
            expires=expiration
        )
    elif sub_command == "agree_scale_survey":
        await agree_scale_command_receiver(
            bot,
            ctx,
            question=question,
            expires=expiration
        )


bot.load(
    "interactions.ext.persistence",
    cipher_key=interactions.ext.persistence.cipher.generate_key()
)

bot.load("update_expired")
bot.load("custom_survey")
bot.load("receive_vote")

bot.start()
