FROM python:3.8.7-slim-buster

RUN apt update && apt install -y git && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 bashbot
RUN useradd -u 1000 -g bashbot -s /bin/sh -m bashbot

RUN git clone https://github.com/Adikso/BashBot.git
WORKDIR BashBot
RUN pip install --no-cache-dir -r requirements.txt
RUN chown -R bashbot:bashbot .

USER bashbot
CMD [ "python", "./bashbot.py" ]
