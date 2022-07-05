# syntax=docker/dockerfile:1

FROM python:latest
WORKDIR /app
COPY ./mysite/ .
RUN apt update
RUN apt upgrade -y
RUN apt install gcc -y
RUN pip install pandas --no-cache-dir
RUN pip install -r requirements.txt