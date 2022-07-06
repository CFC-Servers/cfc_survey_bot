import interactions
import storage
import math
from loguru import logger
from time import time

white_box = "◽"
black_box = "◾"


def make_count_line(count, total):
    out = ""

    percent = None

    if total == 0:
        percent = 0
    else:
        percent = math.floor(count / total) * 10

    for i in range(10):
        x = i + 1

        if x <= percent:
            out = out + white_box
        else:
            out = out + black_box

        if x < 10:
            out = out + " "

    plural = "votes" if count != 1 else "vote"
    out = out + f" `{count} {plural}`"

    return out


def make_expires_line(survey):
    expires = round(survey["expires"])
    now = time()

    word = "Expires" if expires > now else "Expired"

    return f"{word}: <t:{expires}:R>"


def make_option_block(option, emoji, count, total):
    return "\n".join([
        f"> {emoji} **{option}**",
        make_count_line(count, total),
        ""
    ])


def make_survey_body(survey):
    survey_id = survey["survey_id"]
    options = storage.get_options_for_survey(survey_id)
    out = []

    letters = ["🇦", "🇧", "🇨", "🇩"]
    counts = storage.get_option_counts_for_survey(survey_id)
    total = counts["total"]
    logger.info(counts)

    for option in options:
        option_text = option["option_text"]
        option_idx = option["option_idx"]
        option_emoji = option["option_emoji"] or letters[option_idx]

        count = counts.get(option_idx, 0)

        out.append(make_option_block(option_text, option_emoji, count, total))

    out.append(make_expires_line(survey))

    return "\n".join(out)


def make_buttons(survey):
    options = storage.get_options_for_survey(survey["survey_id"])
    buttons = []

    letters = ["🇦", "🇧", "🇨", "🇩"]

    for option in options:
        option_idx = option["option_idx"]

        buttons.append(interactions.Button(
            style=option.get("option_color", 1) or 1,
            label=option["option_emoji"] or letters[option_idx],
            custom_id=f"receive_vote_{option_idx}"
        ))

    return buttons


async def send_survey(ctx, survey, message_url=None):
    question = survey["question"]
    survey_id = survey["survey_id"]

    embed = interactions.api.models.message.Embed(
        title=f"**📊 {question}**",
        color=0x00a5d7,
        description=make_survey_body(survey)
    )

    buttons = make_buttons(survey)

    if message_url:
        # ctx is the bot here because I'm retarded and impatient
        msg = interactions.api.models.message.Message
        message = await msg.get_from_url(message_url, ctx._http)
        await message.edit("", embeds=[embed], components=[buttons])
    else:
        result = await ctx.send("", embeds=[embed], components=[buttons])
        logger.info(result.id)
        logger.info(result.url)
        storage.update_survey_message_info(survey_id, result.id, result.url)

