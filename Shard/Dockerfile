FROM ubuntu:focal
VOLUME /shard/db
RUN apt update
RUN apt-get install libcurl4 openssl liblzma5 curl -y
RUN curl https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2004-5.0.3.tgz -o mongo.tgz
RUN tar -zxvf mongo.tgz
RUN cp mongodb-linux-x86_64-ubuntu2004-5.0.3/bin/* /bin
RUN curl https://downloads.mongodb.com/compass/mongosh-1.1.1-linux-x64.tgz -o mongosh.tgz
RUN tar -zxvf mongosh.tgz
RUN chmod +x mongosh-1.1.1-linux-x64/bin/mongosh
RUN chmod +x mongosh-1.1.1-linux-x64/bin/mongocryptd-mongosh
RUN cp mongosh-1.1.1-linux-x64/bin/mongosh /bin/
RUN cp mongosh-1.1.1-linux-x64/bin/mongocryptd-mongosh /bin/
RUN mkdir -p /var/log/mongodb
RUN mkdir -p /var/lib/mongo
RUN apt install -y pip
RUN apt-get install -y python3
RUN pip install pymongo
RUN pip install argparse
ADD PyDriver.py .
ADD mongod.conf.orig /etc/
ADD mongoScript.js .

# mongod --dbpath /shard/db --logpath /var/log/mongodb/mongod.log --fork
