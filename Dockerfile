FROM python:3
MAINTAINER kevin<kevin@idempotent.ca>
ADD . /app
WORKDIR /app
RUN pip install -r requirements/base.txt
RUN pip install .
ADD configurations /usr/local/lib/python3.5/site-packages/configurations
