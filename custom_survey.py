import interactions
import datetime
import db
from send_survey import send_survey
from structs import OptionStruct
from typing import Optional


async def custom_modal_receiver(
        ctx,
        question: str,
        option1: Optional[str] = None,
        option2: Optional[str] = None,
        option3: Optional[str] = None,
        option4: Optional[str] = None):

    options = [o for o in [option1, option2, option3, option4] if o]
    options = [OptionStruct(text=o) for o in options]

    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    author = str(ctx.user.id)
    vote_limit = 1

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


def make_custom_modal(option_count):
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

    modal = interactions.Modal(
        title="Create a Survey",
        custom_id="custom-survey-modal",
        components=modal_components
    )

    return modal
