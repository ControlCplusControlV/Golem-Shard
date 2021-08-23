FROM mongo:latest

RUN apt update
RUN apt install -y pip
RUN apt-get install -y python3
RUN pip install Pymongo
ADD PyDriver.py .
