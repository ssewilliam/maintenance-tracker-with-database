FROM python:3.7

LABEL MAINTAINER="William Sserubiri <deriwilliams2008@gmail.com>"
LABEL APPLICATION="maintenance-tracker-with-database"

WORKDIR /usr/tracker-app

COPY requirements.txt /usr/tracker-app

RUN pip install -r requirements.txt
RUN pip install python-coveralls
RUN pip install coverage
RUN pip install nose

COPY . /usr/tracker-app

EXPOSE 5000

RUN chmod +x /usr/tracker-app/docker/test/entrypoint.sh

ENTRYPOINT ["/bin/bash","/usr/tracker-app/docker/test/entrypoint.sh"]
