FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache tzdata

RUN pip3 install --no-cache-dir -r requirements.txt

COPY app/ .

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
