from pymongo import MongoClient
CONNECTION = MongoClient('mongodb://tmp/mongodb-27017.sock')
print(CONNECTION)