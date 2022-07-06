FROM python:3.10.5-slim-bullseye

RUN mkdir -p /var/lib/cfc_survey_bot
WORKDIR /cfc-survey-bot

RUN apt update && apt upgrade -y && pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install --upgrade -r ./requirements.txt

COPY entrypoint.sh .
COPY *.py /cfc-survey-bot/
ENTRYPOINT ["/cfc-survey-bot/entrypoint.sh"]
