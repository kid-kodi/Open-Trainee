FROM python:3.6-alpine

RUN adduser -D trainee

WORKDIR /home/trainee

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

RUN apk update && apk upgrade

RUN apk add --no-cache curl python pkgconfig python-dev openssl-dev libffi-dev musl-dev make gcc

RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY run.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP run.py

RUN chown -R trainee:trainee ./
USER trainee

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
