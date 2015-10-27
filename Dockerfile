FROM python:3
MAINTAINER kevin
RUN apt-get update -y
RUN apt-get install postgresql-client -y
VOLUME /app
EXPOSE 8080
CMD /bin/bash
