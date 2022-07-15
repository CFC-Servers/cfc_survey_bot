import dateparser
import datetime
import interactions
import db
from loguru import logger
from structs import OptionStruct
from typing import Optional
from interactions.ext.persistence.parse import PersistentCustomID
from interactions.ext.persistence import PersistenceExtension, extension_persistent_modal


class ReceiveCustom(PersistenceExtension):
    def __init__(self, bot):
        self.bot = bot

    @extension_persistent_modal("custom_modal")
    async def custom_modal_receiver(
            self,
            ctx,
            expires,
            question: str,
            option1: Optional[str] = None,
            option2: Optional[str] = None,
            option3: Optional[str] = None,
            option4: Optional[str] = None):
        logger.info("Received custom modal receiver")

        options = [o for o in [option1, option2, option3, option4] if o]
        options = [OptionStruct(text=o) for o in options]

        author = str(ctx.user.id)
        vote_limit = 1

        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)

        if expires is not None:
            expiration = dateparser.parse(expires, settings={"TIMEZONE": "UTC"})

        survey = db.create_survey(
            message_id="0",
            message_url="",
            author=author,
            question=question,
            options=options,
            vote_limit=vote_limit,
            expires=expiration
        )

        await self.bot.send_survey(ctx, survey)


def make_custom_modal(bot, option_count, expires):
    modal_components = [
        interactions.TextInput(
            style=interactions.TextStyleType.SHORT,
            custom_id="question-input",
            label="Your Survey Question",
            required=True,
            min_lenth=1,
            max_length=45
        )
    ]

    for i in range(option_count):
        modal_components.append(interactions.TextInput(
            style=interactions.TextStyleType.SHORT,
            custom_id=f"question-option-{i+1}",
            label=f"Option {i+1}",
            required=True,
            min_length=1,
            max_length=25
        ))

    modal_id = PersistentCustomID(bot, "custom_modal", expires)
    modal = interactions.Modal(
        title="Create a Survey",
        custom_id=str(modal_id),
        components=modal_components
    )

    return modal


def setup(bot):
    ReceiveCustom(bot)
