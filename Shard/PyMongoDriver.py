# Slow Python Database Driver

import datetime
import json
from pymongo import MongoClient
import argparse


client = MongoClient('mongodb://tmp/mongodb-27017.sock')
db = client["MyDatabase"]
col = db["MyCollection"]

def create(document : dict):
    post_id = col.insert(document)

def read(documentParams : dict):
    col.find_one(documentParams)


def update(document : dict, newDoc : dict):
    col.update(document, newDoc, multi=True)

def remove(paramterDict : dict):
    col.remove(paramterDict)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--create", type=json.loads)
    parser.add_argument("-r", "--read", type=json.loads)
    parser.add_argument("-u", "--update", type=json.loads)
    parser.add_argument("-d", "--delete", type=json.loads)

    args = parser.parse_args()

    if len(args.create) >= 1:
        create(args.create)
    if len(args.read) >= 1:
        create(args.read)
    if len(args.update) >= 1:
        create(args.update)
    if len(args.delete) >= 1:
        create(args.delete)
