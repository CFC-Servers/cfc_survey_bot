import datetime
from loguru import logger
from typing import Optional
from peewee import fn, JOIN
from models import Survey, Option, Vote


def create_survey(
        message_id: str,
        message_url: str,
        author: str,
        question: str,
        options: list,
        expires: Optional[datetime.datetime],
        vote_limit: Optional[int] = None
        ) -> Survey:

    survey = Survey.create(
            message_id=message_id,
            message_url=message_url,
            author=author,
            question=question,
            vote_limit=vote_limit,
            expires=expires
            )

    for i, option in enumerate(options):
        Option.create(
                survey=survey,
                idx=i,
                text=option.text,
                text_emoji_name=option.text_emoji_name,
                button_text=option.button_text,
                button_emoji_name=option.button_emoji_name,
                button_emoji_id=option.button_emoji_id,
                color=option.color
                )

    return survey


def get_option_by_index(survey: Survey, option_idx: int) -> Option:
    return Option.select().where(
        Option.survey == survey,
        Option.idx == option_idx
    )


def cast_vote(
        voter_id: str,
        survey: Survey,
        option_idx: int
        ) -> None:

    # If vote limit is 1
    #     If they casted a vote for a different option
    #         Remove the existing vote
    #         Cast the new vote
    #     If they casted a vote for the same option
    #         Remove the existing vote
    # If the vote limit is > 1
    #     If they have cast a vote for the same option
    #         Remove the existing vote
    #     If they cast a vote for a different option
    #         If their vote count is below the vote_limit
    #             Cast the new vote

    Vote.delete().where(
            Vote.voter == voter_id,
            Vote.survey == survey
            ).execute()

    Vote.create(
        voter=voter_id,
        survey=survey,
        option=get_option_by_index(survey, option_idx),
        option_idx=option_idx
    )


def get_survey_by_message_id(message_id: str) -> Survey:
    logger.info(f"Retrieving message with id: {message_id}")
    return Survey.select().where(Survey.message_id == message_id).first()


def get_option_counts_for_survey(survey: Survey):
    options = (Option
               .select(Option.idx, fn.COUNT(Vote.id).alias('count'))
               .join(Vote, JOIN.LEFT_OUTER)
               .where(Option.survey == survey)
               .group_by(Option.idx))

    option_counts = {}
    total = 0
    for o in options:
        option_counts[o.idx] = o.count
        total = total + o.count

    return option_counts, total


def update_survey_message_info(
        survey: Survey,
        message_id: str,
        message_url: str):

    res = (Survey
           .update(message_id=message_id, message_url=message_url)
           .where(Survey.id == survey.id)
           .execute())

    logger.info(res)

    return res


