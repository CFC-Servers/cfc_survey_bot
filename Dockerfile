FROM python:3.10.5-slim-bullseye

RUN mkdir -p /cfc-survey-bot
WORKDIR /cfc-survey-bot

RUN apt update && apt upgrade -y && apt install -y git && pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install --upgrade -r ./requirements.txt

USER 1000
COPY entrypoint.sh .
COPY *.py /cfc-survey-bot/
ENTRYPOINT ["/cfc-survey-bot/entrypoint.sh"]
