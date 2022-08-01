import interactions
import data
from loguru import logger
from send_survey import build_embed


class ManualLock(interactions.Extension):
    def __init__(self, bot):
        self.bot = bot
        self.lockers = [840098226145329162, 226970872169234432]

    def can_lock(self, roles):
        return not set(roles).isdisjoint(self.lockers)

    @interactions.extension_command(
        name="Lock Survey",
        type=interactions.ApplicationCommandType.MESSAGE,
        #scope=840097260095275028,
        scope=225975453138026497,
    )
    async def manual_lock(self, ctx):

        if not self.can_lock(ctx.member.roles):
            logger.info(f"User tried to lock survey but doesn't have permission: {ctx.member.id}")

            err_embed = interactions.Embed(
                title="Error",
                description="***❌ You do not have permission to use this command***",
                color=0xD83C3E
            )
            await ctx.send("", embeds=[err_embed], ephemeral=True)
            return

        survey = data.get_survey_by_message_id(ctx.target.id)
        if data.get_survey_by_message_id(ctx.target.id) is None:
            logger.info("User tried to lock a not-survey")

            err_embed = interactions.Embed(
                title="Error",
                description="***❌ Message was not a survey***",
                color=0xD83C3E
            )
            await ctx.send("", embeds=[err_embed], ephemeral=True)
            return

        logger.info(f"Manual lock for {ctx.target.id}")

        await ctx.defer(ephemeral=True)
        data.expire_survey(survey, ctx.member.id)

        success_embed = interactions.Embed(
            title="Success",
            description=f"***👍 Survey has been locked***",
            color=0x2D7D46
        )
        await ctx.send("", embeds=[success_embed], ephemeral=True)


def setup(bot):
    ManualLock(bot)
