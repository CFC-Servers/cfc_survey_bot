import interactions
import os
import types
from send_survey import send_survey

bot = interactions.Client(token=os.getenv("DISCORD_BOT_TOKEN", ""))
bot.send_survey = types.MethodType(send_survey, bot)

bot.load(
    "interactions.ext.persistence",
    cipher_key=interactions.ext.persistence.cipher.generate_key()
)


bot.load("survey")
bot.load("update_expired")
bot.load("receive_vote")

bot.start()
