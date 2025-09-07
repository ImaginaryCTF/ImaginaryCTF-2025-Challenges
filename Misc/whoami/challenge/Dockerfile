FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && apt-get -y install python3 python3-pip socat
RUN pip3 install requests --break-system-packages

RUN mkdir /app
COPY . /app
WORKDIR /app

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:'python3 app.py'"]
