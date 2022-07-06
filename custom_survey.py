import interactions
from loguru import logger
from send_survey import send_survey
from time import time
import storage


async def custom_modal_receiver(ctx, question, option1=None, option2=None, option3=None, option4=None):
    options = [o for o in [option1, option2, option3, option4] if o]
    expires = time() + 100
    author = ctx.user.id
    vote_limit = 1

    survey_id = storage.create_survey(0, expires, author, question, vote_limit, options)
    survey = storage.get_survey_by_id(survey_id)

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
