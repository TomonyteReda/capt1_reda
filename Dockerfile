# syntax=docker/dockerfile:1

FROM python:slim-buster
WORKDIR /app
COPY ./mysite/ .
RUN pip install -r requirements.txt