FROM python:slim

RUN pip3 install pyftpdlib

COPY . /app
WORKDIR /app

CMD ["python3", "app.py"]
