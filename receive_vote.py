import asyncio
import data
from loguru import logger
from send_survey import build_embed
from interactions.ext.persistence import PersistenceExtension, extension_persistent_component


class ReceiveVote(PersistenceExtension):
    def __init__(self, bot):
        self.bot = bot
        self.updates = {}
        #bot._loop.create_task(self.render_votes())

    @extension_persistent_component("receive_vote")
    async def receive_vote(self, ctx, idx: int):
        user_id = str(ctx.user.id)
        message_id = str(ctx.message.id)
        logger.info(f"received a vote: {user_id}")

        survey = data.get_survey_by_message_id(message_id)

        if survey.is_expired():
            await ctx.send("That Survey is expired", ephemeral=True)
            return

        message_url = survey.message_url
        if message_url == "":
            await ctx.send("What even is that")
            return

        data.cast_vote(user_id, survey, idx)
        self.updates[message_url] = survey

        await ctx.defer(edit_origin=True)

        embed, components = build_embed(survey, self.bot)
        await ctx.edit("", embeds=[embed], components=components)

    async def render_votes(self):
        while True:
            await asyncio.sleep(0.5)

            for message_url, update in self.updates.items():
                logger.info(f"Updating: {message_url}")
                await self.bot.send_survey(self.bot, update, message_url)
                del self.updates[message_url]
                break


def setup(bot):
    ReceiveVote(bot)
