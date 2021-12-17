FROM ubuntu:20.04
MAINTAINER Anastasiia Blyzniuk 'blyzniuk.anastasiia@gmail.com'
#my base image
#FROM python:3.8
RUN apt-get update
RUN apt-get upgrade -y && \
    apt-get install -y python3-pip python3-dev
COPY . /flask_app
WORKDIR /flask_app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ['python', 'flask_app.py']