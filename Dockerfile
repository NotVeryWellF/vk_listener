FROM python:3.8.0-slim-buster

WORKDIR /vk_listener

RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .
