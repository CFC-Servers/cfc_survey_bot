import datetime
import db
from send_survey import send_survey
from structs import OptionStruct
from interactions.client.enums import ButtonStyle


async def yes_no_command_receiver(ctx, question: str) -> None:
    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    author = str(ctx.user.id)
    vote_limit = 1

    options = [
        OptionStruct(
            text="Yes",
            button_text="Yes",
            text_emoji="",
            button_emoji="👍",
            color=ButtonStyle.SUCCESS
        ),
        OptionStruct(
            text="No",
            button_text="No",
            text_emoji="",
            button_emoji="👎",
            color=ButtonStyle.DANGER
        )
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
