# A collection of interaction Options

import interactions


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
