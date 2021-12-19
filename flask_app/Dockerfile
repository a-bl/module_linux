#FROM ubuntu:20.04
#MAINTAINER Anastasiia Blyzniuk 'blyzniuk.anastasiia@gmail.com'
#my base image
FROM python:3.8

WORKDIR /app

ENV FLASK_APP flask_app.py
ENV DATABASE_URL 'postgresql://admin:admin@localhost/flask_app'

COPY requirements.txt /app/requirements.txt
COPY . /app/

RUN apt-get update && pip install --upgrade pip && \
    apt-get -y install libpq-dev gcc && \
    pip install psycopg2 && pip install -r requirements.txt

EXPOSE 5000
#EXPOSE 5432

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]]