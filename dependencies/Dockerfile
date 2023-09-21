FROM python:3.10-bullseye

WORKDIR /tmp

COPY requirements.txt /tmp

RUN apt-get update && apt-get -y upgrade && \
    pip install -r /tmp/requirements.txt --no-cache-dir
