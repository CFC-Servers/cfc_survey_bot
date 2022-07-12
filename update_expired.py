import asyncio
import datetime
import interactions
from models import Survey


class ExpirationUpdater(interactions.Extension):
    def __init__(self, bot):
        self.bot = bot
        self.have_expired = {}
        bot._loop.create_task(self.update_expired())

    async def update_expired(self):
        while True:
            await asyncio.sleep(0.5)

            now = datetime.datetime.utcnow()
            expired_surveys = (Survey
                               .select()
                               .where(Survey.expires <= now, Survey.active == True))

            for expired in expired_surveys:
                message_url = expired.message_url

                if self.have_expired.get(message_url, None) is not None:
                    continue

                Survey.update(active=False).where(Survey.id == expired.id).execute()

                if message_url == "":
                    continue

                self.have_expired[message_url] = True
                expired.active = False
                await self.bot.send_survey(expired, expired.message_url)

                break


def setup(bot):
    ExpirationUpdater(bot)
