import datetime
import db
from send_survey import send_survey
from structs import OptionStruct
from interactions.client.enums import ButtonStyle


async def agree_scale_command_receiver(ctx, question: str) -> None:
    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
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

    survey = db.create_survey(
        "0",
        "",
        author,
        question,
        options,
        vote_limit,
        expires
    )

    await send_survey(ctx, survey)
