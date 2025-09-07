FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update; apt-get -y install python3 python3-pip wget

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get -y install ./google-chrome-stable_current_amd64.deb

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip3 install -r ./requirements.txt --break-system-packages

RUN echo ictf{common_os_path_join_L_b19d35ca} > /flag.txt
ENV FLAG_2 ictf{}

VOLUME /app/profiles/
VOLUME /root
VOLUME /tmp

CMD ["flask", "run", "-h", "0.0.0.0"]
