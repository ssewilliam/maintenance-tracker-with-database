FROM python:3.7

LABEL MAINTAINER="William Sserubiri <william.sserubiri@andela.com>"
LABEL APPLICATION="maintenance-tracker-with-database"

WORKDIR /usr/tracker-app

COPY ./requirements.txt /usr/tracker-app

RUN pip install -r requirements.txt

COPY . /usr/tracker-app

EXPOSE 5000

CMD python run.py