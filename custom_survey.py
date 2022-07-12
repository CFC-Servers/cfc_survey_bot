import interactions
import db
from structs import OptionStruct
from typing import Optional
from interactions.ext.persistence.parse import PersistentCustomID


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

    modal_id = PersistentCustomID(bot, "custom_survey", expires)
    modal = interactions.Modal(
        title="Create a Survey",
        custom_id=str(modal_id),
        components=modal_components
    )

    return modal


def setup(bot):
    @bot.modal("custom_modal")
    async def custom_modal_receiver(
            ctx,
            expires,
            question: str,
            option1: Optional[str] = None,
            option2: Optional[str] = None,
            option3: Optional[str] = None,
            option4: Optional[str] = None):

        options = [o for o in [option1, option2, option3, option4] if o]
        options = [OptionStruct(text=o) for o in options]

        author = str(ctx.user.id)
        vote_limit = 1

        survey = db.create_survey(
            message_id="0",
            message_url="",
            author=author,
            question=question,
            options=options,
            vote_limit=vote_limit,
            expires=expires
        )

        await bot.send_survey(ctx, survey)
