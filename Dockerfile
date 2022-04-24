FROM ubuntu:latest

RUN apt-get update
RUN apt install -y python3-dev default-libmysqlclient-dev build-essential
RUN apt install -y pip
WORKDIR /root/
RUN mkdir imageClassification
WORKDIR /root/imageClassification
COPY algorithm /root/imageClassification/algorithm
COPY jsonapi /root/imageClassification/jsonapi
COPY requirements.txt /root/imageClassification
COPY app.py /root/imageClassification
COPY Procfile /root/imageClassification
RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "app:app"]