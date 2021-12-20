#FROM ubuntu:20.04
#MAINTAINER Anastasiia Blyzniuk 'blyzniuk.anastasiia@gmail.com'
#my base image
FROM python:3.8-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITTEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP flask_app.py
ENV DATABASE_URL 'postgresql://flaskappdb:flaskappdb@localhost/flask_app'


RUN apt-get update && pip install --upgrade pip && \
    apt-get -y install libpq-dev gcc && \
    pip install psycopg2

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 5000
EXPOSE 5432

CMD [ "python3", "flask_app.py"]
#CMD psql --host=192.168.0.106 --port=5433 --username=flaskappdb -c "SELECT 'SUCCESS !!!';"