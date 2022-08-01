import asyncio
import data
from loguru import logger
from send_survey import build_embed
from interactions.ext.persistence import PersistenceExtension, extension_persistent_component


class ReceiveVote(PersistenceExtension):
    def __init__(self, bot):
        self.bot = bot

    @extension_persistent_component("receive_vote")
    async def receive_vote(self, ctx, idx: int):
        user_id = str(ctx.user.id)
        message_id = str(ctx.message.id)
        logger.info(f"received a vote: {user_id} voted for: {idx}")

        survey = data.get_survey_by_message_id(message_id)

        if survey.is_expired():
            await ctx.send("That Survey is expired", ephemeral=True)
            return

        message_url = survey.message_url
        if message_url == "":
            await ctx.send("What even is that")
            return

        await ctx.defer(edit_origin=True)
        data.cast_vote(user_id, survey, idx)

        embed, components = build_embed(survey, self.bot)
        await ctx.edit("", embeds=[embed], components=components)

def setup(bot):
    ReceiveVote(bot)
