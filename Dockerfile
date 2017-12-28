FROM ubuntu:16.04

RUN apt-get -y upgrade && apt-get -y update && apt-get -y install -y python3-pip python3-dev \
    && apt-get -y install apt-utils\
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python && pip3 install --upgrade pip\
    && apt-get -y install libcurl4-openssl-dev libssl-dev
ENV PYTHONUNBUFFERED 1
RUN mkdir /project
WORKDIR /project
ADD requirements.txt /project/
RUN pip3 install -r requirements.txt
ADD . /project/