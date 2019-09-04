FROM python:3.7

LABEL MAINTAINER="William Sserubiri <william.sserubiri@andela.com>"
LABEL APPLICATION="maintenance-tracker-with-database"

WORKDIR /usr/tracker-app

COPY ./requirements.txt /usr/tracker-app

RUN pip install -r requirements.txt

COPY . /usr/tracker-app

CMD gunicorn run:app --bind 0.0.0.0:${PORT}
