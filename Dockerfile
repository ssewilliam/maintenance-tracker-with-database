FROM python:3.7

LABEL MAINTAINER="William Sserubiri <william.sserubiri@andela.com>"
LABEL APPLICATION="maintenance-tracker-with-database"

WORKDIR /usr

COPY . /usr

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python run.py