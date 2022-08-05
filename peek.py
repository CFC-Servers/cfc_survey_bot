import interactions
import data
from loguru import logger
from send_survey import build_embed


class Peek(interactions.Extension):
    def __init__(self, bot):
        self.bot = bot
        self.peekers = [840098226145329162, 226970872169234432]

    def can_peek(self, roles):
        return not set(roles).isdisjoint(self.peekers)

    @interactions.extension_command(
        name="See Survey Results",
        type=interactions.ApplicationCommandType.MESSAGE,
        #scope=840097260095275028,
        scope=225975453138026497,
    )
    async def manual_lock(self, ctx):

        if not self.can_peek(ctx.member.roles):
            logger.info(f"User tried to peek at the survey but doesn't have permission: {ctx.member.id}")

            err_embed = interactions.Embed(
                title="Error",
                description="***❌ You do not have permission to use this command***",
                color=0xD83C3E
            )
            await ctx.send("", embeds=[err_embed], ephemeral=True)
            return

        survey = data.get_survey_by_message_id(ctx.target.id)
        if data.get_survey_by_message_id(ctx.target.id) is None:
            logger.info("User tried to peek at a not-survey")

            err_embed = interactions.Embed(
                title="Error",
                description="***❌ Message was not a survey***",
                color=0xD83C3E
            )
            await ctx.send("", embeds=[err_embed], ephemeral=True)
            return

        logger.info(f"Result peek for {ctx.target.id}")

        survey.votes_hidden = False
        embed, components = build_embed(survey, self.bot, False)
        await ctx.send("", embeds=[embed], components=components, ephemeral=True)


def setup(bot):
    Peek(bot)
