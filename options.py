# A collection of interaction Options

import interactions
from loguru import logger
from structs import realm_translation


def Expires():
    return interactions.Option(
        name="expires",
        description="When does your Survey expire",
        type=interactions.OptionType.STRING,
        required=False,
        min_length=1,
        max_length=75
    )


def Question(required: bool = False):
    return interactions.Option(
        name="question",
        description="Your Survey Question",
        type=interactions.OptionType.STRING,
        required=required
    )


def Realm():
    choices = [interactions.Choice(name=long, value=short) for short, long in realm_translation.items()]
    return interactions.Option(
        name="realm",
        description="What realm is this for?",
        type=interactions.OptionType.STRING,
        choices=choices,
        #choices=[
        #    interactions.Choice(name="CFC Build/Kill", value="cfc"),
        #    interactions.Choice(name="CFC TTT", value="cfcttt"),
        #    interactions.Choice(name="Discord", value="discord"),
        #    interactions.Choice(name="Meta", value="meta")
        #],
        required=False
    )


def VotesHidden():
    return interactions.Option(
        name="votes_hidden",
        description="Should votes be hidden until the vote expires?",
        type=interactions.OptionType.BOOLEAN,
        value=False,
        required=False
    )
