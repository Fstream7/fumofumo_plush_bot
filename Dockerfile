FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk update && apk add --no-cache \
    build-base \
    libpq-dev \
    python3-dev

RUN pip3 install -r requirements.txt

COPY app/ .

CMD [ "python3", "main.py"]
