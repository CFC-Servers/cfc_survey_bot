# Database Models, Connection, and Setup

import datetime
from loguru import logger
from peewee import Check
from peewee import SqliteDatabase, Model
from peewee import BooleanField, IntegerField
from peewee import TextField, DateTimeField, ForeignKeyField
from playhouse.migrate import *

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
    author = TextField(null=False)
    question = TextField(null=False)
    active = BooleanField(default=True)
    realm = TextField(default="unknown")
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

# Migrations
migrator = SqliteMigrator(db)

def add_realm_to_survey():
    logger.info("Running add_realm_to_survey migration")

    fields = db.get_columns("survey")
    logger.info(fields)
    fields = [f.name for f in fields if f.table == "survey"]

    if "realm" in fields:
        logger.info("Realms already exists, not performing migration")
        return

    realm_field = TextField(default="unknown")
    migrate(
        migrator.add_column("survey", "realm", realm_field),
    )

add_realm_to_survey()
