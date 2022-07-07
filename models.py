import datetime
from loguru import logger
from peewee import Check
from peewee import SqliteDatabase, Model
from peewee import IntegerField, TextField, DateTimeField, ForeignKeyField

db = SqliteDatabase("surveys.db")


class BaseModel(Model):
    class Meta:
        database = db


class Survey(BaseModel):
    message_id = TextField()
    message_url = TextField()
    posted = DateTimeField(default=datetime.datetime.utcnow)
    expires = DateTimeField(default=-1)
    author = TextField(null=False)
    question = TextField(null=False)
    vote_limit = IntegerField(
        constraints=[Check('vote_limit > 0')]
    )

    def is_expired(self):
        logger.info(f"self.expires: {self.expires}")
        return self.expires < datetime.datetime.utcnow()


class Option(BaseModel):
    survey = ForeignKeyField(Survey, backref="options")
    idx = IntegerField(null=False)
    text = TextField(null=False)
    color = IntegerField(default=1)
    text_emoji = TextField(null=True)
    button_emoji = TextField(null=True)
    button_text = TextField(null=True)


class Vote(BaseModel):
    # TODO: Figure out how to deal with the option vs. option_idx situation
    voter = TextField(null=False)
    option_idx = IntegerField()
    option = ForeignKeyField(Option, backref="votes")
    survey = ForeignKeyField(Survey, backref="votes")


db.connect()
db.create_tables([Survey, Option, Vote])
