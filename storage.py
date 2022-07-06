import sqlite3
from time import time
from loguru import logger

con = sqlite3.connect('surveys.db')
cur = con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS surveys (
        survey_id   INTEGER PRIMARY KEY,
        message_id  INTEGER NOT NULL,
        message_url TEXT NOT NULL,
        posted      REAL    NOT NULL,
        expires     REAL    NOT NULL,
        author      TEXT    NOT NULL,
        question    TEXT    NOT NULL,
        vote_limit  INTEGER DEFAULT 1 NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS options(
        option_id    INTEGER PRIMARY KEY,
        survey_id    INTEGER NOT NULL,
        option_idx   INTEGER NOT NULL,
        option_text  TEXT NOT NULL,
        option_color INTEGER DEFAULT 1,
        option_emoji TEXT,
        FOREIGN KEY (survey_id)
           REFERENCES surveys (survey_id)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS votes(
        vote_id    INTEGER PRIMARY KEY,
        voter      INTEGER NOT NULL,
        option_idx INTEGER NOT NULL,
        survey_id  INTEGER NOT NULL,
        FOREIGN KEY (survey_id)
          REFERENCES surveys (survey_id)
    )
''')
cur.execute('''
    CREATE UNIQUE INDEX IF NOT EXISTS
        idx_voter_survey_option
    ON
        votes
        (voter, survey_id, option_idx)
''')

con.commit()


def create_survey(message_id, message_url, expires, author, question, vote_limit, options):
    posted = time()

    cur.execute('''
        INSERT INTO
            surveys
            (survey_id, message_id, message_url, posted, expires, author, question, vote_limit)
        VALUES
          (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (None, str(message_id), message_url, posted, expires, str(author), question, vote_limit))

    survey_id = cur.lastrowid

    options_data = []
    for i, option in enumerate(options):
        options_data.append((None, survey_id, i, option, None, None))

    cur.executemany('''
        INSERT INTO
            options
            (option_id, survey_id, option_idx, option_text, option_emoji, option_color)
        VALUES
          (?, ?, ?, ?, ?, ?)
    ''', options_data)

    con.commit()

    return survey_id


def remove_vote(voter_id, survey_id, option_idx):
    cur.execute('''
        DELETE FROM
            votes
        WHERE
            voter = ?
        AND
            survey_id = ?
        AND
            option_idx = ?
    ''', (str(voter_id), str(survey_id), str(option_idx)))

    con.commit()


def remove_all_votes(voter_id, survey_id):
    cur.execute('''
        DELETE FROM
            votes
        WHERE
            voter = ?
        AND
            survey_id = ?
    ''', (str(voter_id), str(survey_id)))

    con.commit()


def cast_vote(voter_id, survey_id, option_idx):
    # TODO: Only do this step if the max votes is 1
    # Otherwise just don't register the vote change unless
    # they un-click an already-clicked option

    remove_all_votes(voter_id, survey_id)

    cur.execute('''
        INSERT INTO
            votes
            (vote_id, voter, survey_id, option_idx)
        VALUES
            (?, ?, ?, ?)
    ''', (None, str(voter_id), str(survey_id), str(option_idx)))

    con.commit()


def _format_response_to_survey(response):
    fields = [
        "survey_id",
        "message_id",
        "message_url",
        "posted",
        "expires",
        "author",
        "question",
        "vote_limit"
    ]

    return dict(zip(fields, response))


def _format_responses_to_survey(responses):
    return [_format_response_to_survey(r) for r in responses]


def get_survey_by_message_id(message_id):
    result = cur.execute('''
        SELECT * FROM
            surveys
        WHERE
            message_id=?
    ''', str(message_id)).fetchall()

    return _format_response_to_survey(result[0])


def get_survey_by_id(survey_id):
    logger.info(type(survey_id))
    result = cur.execute('''
        SELECT * FROM
            surveys
        WHERE
            survey_id=?
    ''', str(survey_id)).fetchall()

    return _format_response_to_survey(result[0])


def get_option_counts_for_survey(survey_id):
    result = cur.execute('''
        SELECT *
        FROM
            surveys s
        INNER JOIN (
            SELECT
                survey_id, v.option_idx, count(v.vote_id)
            FROM
                votes v
            GROUP BY
                survey_id, option_idx
        ) AS
            counts
          ON
            s.survey_id = counts.survey_id
        WHERE
            s.survey_id = ?
    ''', str(survey_id)).fetchall()

    logger.info(result)

    return result


def get_options_for_survey(survey_id):
    result = cur.execute('''
        SELECT
            option_idx, option_text, option_emoji, option_color
        FROM
            options
        WHERE
            survey_id=?
    ''', str(survey_id)).fetchall()

    logger.info(result)
    fields = ["option_idx", "option_text", "option_emoji", "option_color"]
    return [dict(zip(fields, r)) for r in result]


def update_survey_message_info(survey_id, message_id, message_url):
    cur.execute('''
        UPDATE
            surveys
        SET
            message_id=?,
            message_url=?
        WHERE
            survey_id=?
    ''', (str(survey_id), message_url, str(message_id)))

    con.commit()
