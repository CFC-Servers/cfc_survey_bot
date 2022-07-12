import asyncio
import db


updates = {}


async def receive_vote(ctx, idx):
    user_id = str(ctx.user.id)
    message_id = str(ctx.message.id)

    survey = db.get_survey_by_message_id(message_id)

    if survey.is_expired():
        await ctx.send("That Survey is expired")
        return

    message_url = survey.message_url
    if message_url == "":
        await ctx.send("What even is that")
        return

    db.cast_vote(user_id, survey, idx)
    updates[message_url] = survey
    await ctx.send()


def setup(bot):
    async def render_votes():
        while True:
            await asyncio.sleep(0.5)

            for message_url, update in updates.items():
                await bot.send_survey(update, message_url)
                del updates[message_url]
                break

    bot._loop.create_task(render_votes())
    bot.component("receive_vote")(receive_vote)
