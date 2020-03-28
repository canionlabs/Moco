FROM python:3.6-stretch

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

RUN apt update && apt upgrade -y

COPY ./requirements.txt /opt/app/requirements.txt
RUN pip install --quiet -r /opt/app/requirements.txt

COPY . /opt/app/
WORKDIR /opt/app/

EXPOSE 8001
