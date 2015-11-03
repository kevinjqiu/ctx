FROM python:3
MAINTAINER kevin<kevin@idempotent.ca>
ADD . /app
WORKDIR /app
RUN pip install -r requirements/base.txt
