# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /home/vladimir/home-dev/Smith-84

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo
RUN apk add --no-cache python3-dev openssl-dev libffi-dev gcc
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# copy project
COPY . .