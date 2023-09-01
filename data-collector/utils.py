import os
from pymongo import MongoClient
import json
import redis

from logger import logging


MONGO_DB_USERNAME = os.environ.get('MONGO_DB_USERNAME')
MONGO_DB_PASSWORD = os.environ.get('MONGO_DB_PASSWORD')
MONGO_DB_HOSTNAME = os.environ.get('MONGO_DB_HOSTNAME')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME')
REDIS_DB_HOSTNAME = os.environ.get('REDIS_DB_HOSTNAME')

def insert_data_to_mongodb_collection(collectionName: str, message):
    try:
        MONGO_URI = f'mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOSTNAME}'
        mongo_client = MongoClient(MONGO_URI)
        db = mongo_client[MONGO_DB_NAME]
        data = json.loads(message)
        _id = data['timestamp'][:10].replace('-', '')
        collection = db[collectionName.replace('/','_')]
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

def cache_last_ten_readings_to_redis(keyName, message):
    try:
        number_of_readings_to_cached = 10
        key = keyName.replace("/","_")
        data = message
        redis_conn = redis.StrictRedis(host = REDIS_DB_HOSTNAME)
        if redis_conn.exists(key) != 0 and redis_conn.llen(key) >= number_of_readings_to_cached:
            redis_conn.lpop(key)
        redis_conn.rpush(key, data)
        logging.info(f"data cached to redis with key: {key} and data: {data}")
    except Exception as e:
        logging.exception(e)

