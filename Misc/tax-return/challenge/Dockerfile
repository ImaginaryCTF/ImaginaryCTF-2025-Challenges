FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update
RUN apt-get -y install python3 python3-pip wget

RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip3 install -r ./requirements.txt --break-system-packages

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--log-level", "debug"]
