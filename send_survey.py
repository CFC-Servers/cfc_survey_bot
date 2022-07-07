import interactions
import db
import math
from loguru import logger

white_box = "◽"
black_box = "◾"
orange_diamond = "🔸"
crown = "👑"
chart = "📊"
lock = "🔒"
letters = ["🇦", "🇧", "🇨", "🇩"]
letters_names = [
    "regional_indicator_a"
    "regional_indicator_b"
    "regional_indicator_c"
    "regional_indicator_d"
]
active_color = 0x00a5d7
expired_color = 0xf38c01

message_cache = {}
msg = interactions.api.models.message.Message


async def get_discord_message(url: str, http):
    cached = message_cache.get(url, None)

    if cached:
        logger.info(f"Returning cached message for: {url}")
        return cached

    message = await msg.get_from_url(url, http)
    message_cache[url] = message

    return message


def make_count_line(count, total, is_winner=False):
    out = ""

    percent = None

    if total == 0:
        percent = 0
    else:
        percent = math.floor((count / total) * 10)

    for i in range(10):
        x = i + 1

        if x <= percent:
            out = out + (orange_diamond if is_winner else white_box)
        else:
            out = out + black_box

        if x < 10:
            out = out + " "

    plural = "votes" if count != 1 else "vote"
    out = out + f" `{count} {plural}`"

    if is_winner:
        out = out + f" {crown}"

    return out


def make_expires_line(survey):
    expires = round(survey.expires.timestamp())
    expired = survey.is_expired()

    word = "Expired" if expired else "Expires"

    return f"**{word}**: <t:{expires}:R>"


def make_option_block(option, emoji, count, total, is_expired, ranking):
    return "\n".join([
        f"> {emoji} **{option}**",
        make_count_line(count, total, is_expired and ranking == 0),
        ""
    ])


def make_survey_body(survey):
    options = survey.options
    is_expired = survey.is_expired()
    out = []

    counts, total = db.get_option_counts_for_survey(survey)

    # 0 = first
    # FIXME: This doesn't handle ties
    rankings = dict(zip(sorted(counts, key=counts.get, reverse=True), range(len(options))))

    for option in options:
        option_idx = option.idx
        option_emoji = option.text_emoji_name

        if option_emoji is None:
            option_emoji = letters[option_idx]

        count = counts[option_idx]

        option_block = make_option_block(
            option.text,
            option_emoji,
            count,
            total,
            is_expired,
            rankings[option_idx]
        )
        out.append(option_block)

    out.append(make_expires_line(survey))

    return "\n".join(out)


def make_buttons(survey):
    options = survey.options
    buttons = []

    for option in options:
        option_idx = option.idx

        buttons.append(interactions.Button(
            style=option.color,
            emoji=interactions.Emoji(
                name=option.button_emoji_name or letters_names[option_idx],
                id=option.button_emoji_id
            ),
            label=option.button_text,
            custom_id=f"receive_vote_{option_idx}"
        ))

    return buttons


async def send_survey(ctx, survey, message_url=None):
    question = survey.question
    is_expired = survey.is_expired()

    title_prefix = lock if is_expired else chart
    color = expired_color if is_expired else active_color

    embed = interactions.api.models.message.Embed(
        title=f"**{title_prefix} {question}**",
        color=color,
        description=make_survey_body(survey)
    )

    components = []

    if not is_expired:
        components.append(make_buttons(survey))

    if message_url:
        # ctx is the bot here because I'm retarded and impatient
        message = await get_discord_message(message_url, ctx._http)
        await message.edit("", embeds=[embed], components=components)
    else:
        message = await ctx.send("", embeds=[embed], components=components)

        message_url = message.url
        message_id = str(message.id)
        logger.info(f"Created message id: {message_id}")
        logger.info(f"Created message url: {message_url}")

        message_cache[message_url] = message

        db.update_survey_message_info(survey, message_id, message_url)
