import dateparser
import datetime
import interactions
import data
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
            persisted,
            option1: Optional[str] = None,
            option2: Optional[str] = None,
            option3: Optional[str] = None,
            option4: Optional[str] = None,
            option5: Optional[str] = None):
        logger.info("Received custom modal receiver")

        question, expires, realm, votes_hidden = persisted

        options = [o for o in [option1, option2, option3, option4, option5] if o]
        options = [OptionStruct(text=o) for o in options]

        author = str(ctx.user.id)
        vote_limit = 1

        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)

        if expires is not None:
            expiration = dateparser.parse(expires, settings={"TIMEZONE": "UTC"})

        survey = data.create_survey(
            message_id="0",
            message_url="",
            author=author,
            question=question,
            options=options,
            vote_limit=vote_limit,
            expires=expiration,
            realm=realm,
            votes_hidden=votes_hidden
        )

        await self.bot.send_survey(ctx, survey)


def make_custom_modal(bot, question, expires=None, realm=None, votes_hidden=False):
    modal_components = []

    for i in range(5):
        is_optional = i > 1

        modal_components.append(interactions.TextInput(
            style=interactions.TextStyleType.SHORT,
            custom_id=f"question-option-{i+1}",
            label=f"Option {i+1}",
            required=not is_optional,
            min_length=1,
            max_length=40
        ))

    modal_id = PersistentCustomID(bot, "custom_modal", [question, expires, realm, votes_hidden])
    modal = interactions.Modal(
        title="Create a Survey",
        custom_id=str(modal_id),
        components=modal_components
    )

    return modal


def setup(bot):
    ReceiveCustom(bot)
