import asyncio
import db
from loguru import logger
from interactions.ext.persistence import PersistenceExtension, extension_persistent_component


class ReceiveVote(PersistenceExtension):
    def __init__(self, bot):
        self.bot = bot
        self.updates = {}
        self.bot._loop.create_task(self.render_votes())

    @extension_persistent_component("receive_vote")
    async def receive_vote(self, ctx, idx):
        user_id = str(ctx.user.id)
        message_id = str(ctx.message.id)
        logger.info(f"received a vote: {user_id}")

        survey = db.get_survey_by_message_id(message_id)

        if survey.is_expired():
            await ctx.send("That Survey is expired")
            return

        message_url = survey.message_url
        if message_url == "":
            await ctx.send("What even is that")
            return

        db.cast_vote(user_id, survey, idx)
        self.updates[message_url] = survey
        await ctx.send()

    async def render_votes(self):
        while True:
            await asyncio.sleep(0.5)

            for message_url, update in self.updates.items():
                await self.bot.send_survey(update, message_url)
                del self.updates[message_url]
                break


def setup(bot):
    ReceiveVote(bot)
