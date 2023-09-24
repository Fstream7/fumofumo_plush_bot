FROM python:3.11

WORKDIR /app

RUN apt-get -y update

RUN apt-get -y install git gcc python3-dev

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY app/ .

CMD [ "python3", "main.py"]