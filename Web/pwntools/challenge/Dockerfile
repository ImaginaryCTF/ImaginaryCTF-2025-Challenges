FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update; apt-get -y install python3 python3-pip wget
RUN pip3 install pwntools eventlet>=0.30 selenium>=4.0 webdriver_manager --break-system-packages

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get -y install ./google-chrome-stable_current_amd64.deb

RUN mkdir /app
COPY . /app
WORKDIR /app

CMD ["python3", "app.py"]
