FROM python:3
MAINTAINER kevin
RUN apt-get update -y
VOLUME /app
EXPOSE 8080
CMD /bin/bash
