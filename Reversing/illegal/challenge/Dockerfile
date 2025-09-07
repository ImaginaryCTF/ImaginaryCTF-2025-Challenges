FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update; apt-get -y install python3 python3-pip socat

RUN mkdir /app
RUN mkdir /app/tmp
COPY challenge.py /app
COPY checker /app
RUN chmod +x /app/*
WORKDIR /app

COPY flag.txt /app/

VOLUME /app/tmp

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/app/challenge.py"]
