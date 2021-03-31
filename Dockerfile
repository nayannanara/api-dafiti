FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN python -m pip install --upgrade pip
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt
# RUN apt-get -y install cron

COPY . .