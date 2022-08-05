import interactions
import data
import math
from typing import List
from loguru import logger
from structs import realm_translation
from interactions.ext.persistence.parse import PersistentCustomID


class Emojis:
    white_box = "◽"
    black_box = "◾"
    orange_diamond = "🔸"
    crown = "👑"
    chart = "<:chartsmaller:1003500706851999785>"
    lock = "<:locksmaller:1003500694000648202>"


class Colors:
    active = 0x00a5d7
    expired = 0xf38c01


letters: List[str] = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬"]


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


def make_count_line(count, total, is_active=True, votes_hidden=False, is_winner=False):
    out = ""

    percent = None
    should_hide = is_active and votes_hidden
    is_winner = (not is_active) and is_winner

    if total == 0 or should_hide:
        percent = 0
    else:
        percent = math.floor((count / total) * 10)

    for i in range(10):
        x = i + 1

        if x <= percent:
            out = out + (Emojis.orange_diamond if is_winner else Emojis.white_box)
        else:
            out = out + Emojis.black_box

        if x < 10:
            out = out + " "

    if should_hide:
        out = out + " `? votes`"
    else:
        plural = "votes" if count != 1 else "vote"
        out = out + f" `{count} {plural}`"

    if is_winner:
        out = out + f" {Emojis.crown}"

    return out


def make_expires_line(survey):
    expires = round(survey.expires.timestamp())

    votes_hidden = survey.votes_hidden
    active = survey.active
    word = "Expires" if active else "Expired"

    locked_by = survey.locked_by
    expiration = f"<t:{expires}:R>"

    if active:
        if locked_by:
            expiration = f"Locked early by <@{locked_by}>"
        elif votes_hidden:
            expiration = f"Votes revealed {expiration}"

    return {
        "name": f"**{word}**",
        "value": expiration,
        "inline": False
    }


def make_totals_line(total):
    plural = "Votes" if total > 1 else "Vote"

    return {
        "name": "**Total Votes**",
        "value": f"`{total} {plural}`",
        "inline": False
    }


def make_option_block(option, emoji, count, total, is_active, votes_hidden, is_winner):
    return {
        "name": f"{emoji} **{option}**",
        "value": make_count_line(count, total, is_active, votes_hidden, is_winner),
        "inline": False
    }


def make_survey_body(survey):
    options = survey.options
    out = []

    counts, total = data.get_option_counts_for_survey(survey)

    # 0 = first
    # FIXME: This doesn't handle ties or no-vote surveys
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
            survey.active,
            survey.votes_hidden,
            rankings[option_idx] == 0
        )

        out.append(option_block)

    total_line = make_totals_line(total)
    out.append(total_line)

    expires_line = make_expires_line(survey)
    if expires_line:
        out.append(expires_line)

    return out


def make_buttons(survey, bot):
    options = survey.options
    buttons = []

    for option in options:
        option_idx = option.idx
        logger.info(f"Option idx {option_idx}")

        emoji = None
        if option.button_emoji_name:
            emoji = interactions.Emoji(
                name=option.button_emoji_name,
                id=option.button_emoji_id
            )
        else:
            emoji = interactions.Emoji(name=letters[option_idx])

        buttons.append(interactions.Button(
            style=option.color,
            emoji=emoji,
            label=option.button_text,
            custom_id=str(PersistentCustomID(bot, "receive_vote", option_idx))
        ))

    return buttons


def build_embed(survey, bot, interactable=True):
    question = survey.question
    is_active = not survey.is_expired()

    title_prefix = Emojis.chart if is_active else Emojis.lock
    color = Colors.active if is_active else Colors.expired

    embed = interactions.api.models.message.Embed(
        title=f"{title_prefix} **{question}**",
        color=color
    )

    realm = survey.realm
    if realm and realm != "unknown":
        translated = realm_translation.get(realm, realm)
        embed.set_footer(text=f"Subject: {translated}")

    for field in make_survey_body(survey):
        embed.add_field(
            name=field["name"],
            value=field["value"],
            inline=field["inline"]
        )

    components = []

    if is_active and interactable:
        components.append(make_buttons(survey, bot))

    return embed, components


async def send_survey(bot, ctx, survey, message_url=None):
    embed, components = build_embed(survey, bot)

    if message_url:
        # ctx is the bot here because I'm retarded and impatient
        # if message_url is provided, this is an update
        # if it's not, then this is an initial send
        message = await get_discord_message(message_url, ctx._http)
        await message.edit("", embeds=[embed], components=components)
    else:
        message = await ctx.send("", embeds=[embed], components=components)

        message_url = message.url
        message_id = str(message.id)
        logger.info(f"Created message id: {message_id}")
        logger.info(f"Created message url: {message_url}")

        message_cache[message_url] = message

        data.update_survey_message_info(survey, message_id, message_url)
