FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app
COPY . /app

RUN pip3 install -r requirements.txt

CMD ./run.sh
