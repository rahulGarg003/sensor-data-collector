import os
from pymongo import MongoClient
import json

from logger import logging

class MongoDB(object):

    def __init__(self, host, userName, password, dbName):
        MONGO_URI = f'mongodb://{userName}:{password}@{host}'
        try:
            mongo_client = MongoClient(MONGO_URI)
            self.db = mongo_client[dbName]
        except Exception as e:
            logging.exception(e)

    def insert_data_to_collection(self, collectionName: str, message):
        try:
            data = json.loads(message)
            _id = data['timestamp'][:10].replace('-', '')
            collection = self.db[collectionName.replace('/','_')]
            # collection.insert_one(data)
            if(collection.find_one({"_id": _id})):
                collection.update_one(
                    filter = {"_id" : _id},
                    update = {'$push' : {"values": data}}
                )
            else:
                collection.insert_one(
                    {
                        "_id": _id,
                        "values": [data]
                    }
                )
        except Exception as e:
            logging.exception(e)

