import data
import interactions
from structs import OptionStruct
from interactions.client.enums import ButtonStyle


async def yes_no_command_receiver(
        bot,
        ctx: interactions.CommandContext,
        question: str,
        expires) -> None:
    author = str(ctx.user.id)
    vote_limit = 1

    options = [
        OptionStruct(
            text="Yes",
            text_emoji_name="",
            button_emoji_name="👍",
            color=ButtonStyle.SUCCESS
        ),
        OptionStruct(
            text="No",
            text_emoji_name="",
            button_emoji_name="👎",
            color=ButtonStyle.DANGER
        )
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
