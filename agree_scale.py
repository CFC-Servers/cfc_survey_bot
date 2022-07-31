import data
from structs import OptionStruct
from interactions.client.enums import ButtonStyle


async def agree_scale_command_receiver(bot, ctx, question: str, expires) -> None:
    author = str(ctx.user.id)
    vote_limit = 1

    options = [
        OptionStruct(
            text="Strongly Agree",
            text_emoji_name="🔹",
            button_emoji_name="stronglyagree",
            button_emoji_id="745805882549469354",
            color=ButtonStyle.SECONDARY
        ),
        OptionStruct(
            text="Agree",
            text_emoji_name="🔹",
            button_emoji_name="agree",
            button_emoji_id="745805882599932005",
            color=ButtonStyle.SECONDARY
        ),
        OptionStruct(
            text="Undecided",
            text_emoji_name="🔹",
            button_emoji_name="unsure",
            button_emoji_id="745805882763509780",
            color=ButtonStyle.SECONDARY
        ),
        OptionStruct(
            text="Disagree",
            text_emoji_name="🔹",
            button_emoji_name="disagree",
            button_emoji_id="745805882469646387",
            color=ButtonStyle.SECONDARY
        ),
        OptionStruct(
            text="Strongly Disagree",
            text_emoji_name="🔹",
            button_emoji_name="stronglydisagree",
            button_emoji_id="745805882507526165",
            color=ButtonStyle.SECONDARY
        ),
    ]

    survey = data.create_survey(
        message_id="0",
        message_url="",
        author=author,
        question=question,
        options=options,
        vote_limit=vote_limit,
        expires=expires
    )

    await bot.send_survey(ctx, survey)
