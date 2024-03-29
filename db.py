# Database Models, Connection, and Setup

import datetime
from loguru import logger
from peewee import Check
from peewee import SqliteDatabase, Model
from peewee import BooleanField, IntegerField
from peewee import TextField, DateTimeField, ForeignKeyField

# db = SqliteDatabase("surveys.db")
db = SqliteDatabase("surveys.db", pragmas={
    "journal_mode": "wal",
    "cache_size": -1 * 64000,  # 64MB
    "foreign_keys": 1,
    "ignore_check_constraints": 0,
    "synchronous": 0})


class BaseModel(Model):
    class Meta:
        database = db


class Survey(BaseModel):
    message_id = TextField()
    message_url = TextField()
    posted = DateTimeField(default=datetime.datetime.utcnow)
    expires = DateTimeField(default=-1)
    author = TextField()
    question = TextField()
    active = BooleanField(default=True)
    realm = TextField(null=True)
    locked_by = TextField(null=True)
    votes_hidden = BooleanField(default=False)
    vote_limit = IntegerField(
        constraints=[Check('vote_limit > 0')]
    )

    def is_expired(self):
        logger.info(f"self.expires: {self.expires}")
        return self.expires <= datetime.datetime.utcnow()


class Option(BaseModel):
    survey = ForeignKeyField(Survey, backref="options")
    idx = IntegerField(null=False)
    text = TextField(null=False)
    color = IntegerField(default=1)
    text_emoji_name = TextField(null=True)
    button_emoji_name = TextField(null=True)
    button_emoji_id = TextField(null=True)
    button_text = TextField(null=True)


class Vote(BaseModel):
    # TODO: Figure out how to deal with the option vs. option_idx situation
    voter = TextField(null=False)
    option_idx = IntegerField()
    option = ForeignKeyField(Option, backref="votes")
    survey = ForeignKeyField(Survey, backref="votes")


db.connect()
db.create_tables([Survey, Option, Vote])
