FROM python:3
MAINTAINER kevin<kevin@idempotent.ca>
RUN apt-get update -y
VOLUME /app
EXPOSE 8080
CMD /bin/bash
