import dateparser
import datetime
import interactions
from loguru import logger
from interactions import Option, OptionType
from options import Expires, Question, Realm, VotesHidden

from custom_survey import make_custom_modal
from yes_no import yes_no_command_receiver
from agree_scale import agree_scale_command_receiver


class SurveyCommand(interactions.Extension):
    def __init__(self, client):
        self.client = client

    @interactions.extension_command(
        name="survey",
        description="Create a new Survey",
        #scope=[840097260095275028],
        scope=[225975453138026497],
        options=[
            Option(
                name="custom",
                description="A custom Survey",
                type=OptionType.SUB_COMMAND,
                options=[
                    Question(),
                    Realm(),
                    Expires(),
                    VotesHidden(),
                ]
            ),
            Option(
                name="yes_no",
                description="A simple yes-or-no Survey",
                type=OptionType.SUB_COMMAND,
                options=[
                    Question(),
                    Realm(),
                    Expires(),
                    VotesHidden(),
                ]
            ),
            Option(
                name="agree_scale",
                description="A 1-5 opinion Survey",
                type=OptionType.SUB_COMMAND,
                options=[
                    Question(),
                    Realm(),
                    Expires(),
                    VotesHidden(),
                ]
            )
        ]
    )
    async def survey(
            self,
            ctx: interactions.CommandContext,
            sub_command: str,
            question: str,
            realm: str = "unknown",
            expires: str = None,
            votes_hidden: bool = False):
        logger.info(f"Received a survey request: {sub_command}")

        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)

        if expires != "":
            expiration = dateparser.parse(expires, settings={"TIMEZONE": "UTC"})

        if sub_command == "custom":
            await ctx.popup(make_custom_modal(self.client, question, expires, realm, votes_hidden))

        elif sub_command == "yes_no":
            await yes_no_command_receiver(
                self.client,
                ctx,
                question=question,
                expires=expiration,
                realm=realm,
                votes_hidden=votes_hidden
            )
        elif sub_command == "agree_scale":
            await agree_scale_command_receiver(
                self.client,
                ctx,
                question=question,
                expires=expiration,
                realm=realm,
                votes_hidden=votes_hidden
            )


def setup(bot):
    SurveyCommand(bot)
