FROM python:3.11-alpine

WORKDIR /app

COPY . /app

RUN apk update && apk upgrade

RUN apk add socat && rm -rf /var/lib/apt/lists/*

EXPOSE 9999

ENTRYPOINT socat TCP-LISTEN:9999,fork EXEC:'python3 chall.py'
