# pull official base image
FROM python:3.8
# set environment variables
ENV PYTHONUNBUFFERED 1
# set work directory
WORKDIR /docker_server
# copy project
COPY . /docker_server
RUN pip install --upgrade pip
# install dependencies
RUN pip install -r requirements.txt﻿
