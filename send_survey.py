import interactions
import storage
import math
from loguru import logger
from time import time

white_box = "◽"
black_box = "◾"


def make_count_line(count, total):
    out = ""

    percent = math.floor(count / total)
    for i in range(10):
        x = i + 1

        if x <= percent:
            out = out + white_box
        else:
            out = out + black_box

        if x < 10:
            out = out + " "

    plural = "votes" if count > 1 else "vote"
    out = out + f" `{count} {plural}`"

    return out


def make_expires_line(survey):
    expires = survey["expires"]
    now = time()

    word = "Expires" if expires > now else "Expired"

    return f"{word}: <t:{expires}:R>"


def make_option_block(option, emoji, count, total):
    return "\n".join([
        f"> {emoji} **{option}**",
        make_count_line(count, total)
    ])


def make_survey_body(survey):
    storage.get_option_counts_for_survey(survey["survey_id"])

    return ""


def make_buttons(survey):
    logger.info(storage.get_options_for_survey(survey["survey_id"]))


async def send_survey(ctx, survey):
    question = survey["question"]

    embed = interactions.api.models.message.Embed(
        title=f"**📊 {question}**",
        color=0x00a5d7,
        description=make_survey_body(survey)
    )

    buttons = make_buttons(survey)

    result = await ctx.send("", embeds=[embed], components=[buttons])
    logger.info(result)
