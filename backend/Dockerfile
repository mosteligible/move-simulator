FROM python:3.10-bullseye

WORKDIR /app

COPY . /app
COPY requirements.txt /tmp

RUN apt-get update && apt-get -y upgrade && \
    pip install -r /tmp/requirements.txt --no-cache-dir

EXPOSE 5000

CMD [ "gunicorn", "--workers=4", "--bind='$(HOST):$(PORT)'", "entrypoint:app" ]
