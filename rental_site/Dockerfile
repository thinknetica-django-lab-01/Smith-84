FROM python:3.8.3-alpine

WORKDIR /rental_site

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add make \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    libxml2-dev \
    libxslt-dev \
    libgcc curl \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev

# https://stackoverflow.com/questions/52894632/cannot-install-pycosat-on-alpine-during-dockerizing
RUN echo "#include <unistd.h>" > /usr/include/sys/unistd.h
RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .