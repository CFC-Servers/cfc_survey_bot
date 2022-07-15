# A collection of interaction Options

import interactions


def OptionCount():
    return interactions.Option(
        name="option_count",
        description="How many options your Survey will have",
        type=interactions.OptionType.INTEGER,
        required=True,
        min_value=1,
        max_value=4
    )


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
