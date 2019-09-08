FROM python:3.7-alpine3.7

LABEL MAINTAINER="William Sserubiri <william.sserubiri@andela.com>"
LABEL APPLICATION="maintenance-tracker-with-database"

WORKDIR /usr/tracker-app

COPY ./requirements.txt /usr/tracker-app

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

COPY . /usr/tracker-app

CMD gunicorn run:app --bind 0.0.0.0:${PORT}
