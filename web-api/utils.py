import os
from pymongo import MongoClient
import json
import redis
from typing import List, Union
from datetime import date, timedelta

from logger import logging
from models import ReadingModel


MONGO_DB_USERNAME = os.environ['MONGO_DB_USERNAME']
MONGO_DB_PASSWORD = os.environ['MONGO_DB_PASSWORD']
MONGO_DB_HOSTNAME = os.environ['MONGO_DB_HOSTNAME']
MONGO_DB_NAME = os.environ['MONGO_DB_NAME']
REDIS_DB_HOSTNAME = os.environ['REDIS_DB_HOSTNAME']

# def insert_data_to_mongodb_collection(collectionName: str, message):
#     try:
#         MONGO_URI = f'mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOSTNAME}'
#         mongo_client = MongoClient(MONGO_URI)
#         db = mongo_client[MONGO_DB_NAME]
#         data = json.loads(message)
#         _id = data['timestamp'][:10].replace('-', '')
#         collection = db[collectionName.replace('/','_')]
#         # collection.insert_one(data)
#         if(collection.find_one({"_id": _id})):
#             collection.update_one(
#                 filter = {"_id" : _id},
#                 update = {'$push' : {"values": data}}
#             )
#         else:
#             collection.insert_one(
#                 {
#                     "_id": _id,
#                     "values": [data]
#                 }
#             )
#     except Exception as e:
#         logging.exception(e)

# def cache_last_ten_readings_to_redis(keyName, message):
#     try:
#         number_of_readings_to_cached = 10
#         key = keyName.replace("/","_")
#         data = message
#         redis_conn = redis.StrictRedis(host = REDIS_DB_HOSTNAME)
#         if redis_conn.exists(key) != 0 and redis_conn.llen(key) >= number_of_readings_to_cached: # type: ignore
#             redis_conn.lpop(key)
#         redis_conn.rpush(key, data)
#         logging.info(f"data cached to redis with key: {key} and data: {data}")
#     except Exception as e:
#         logging.exception(e)

def get_data_from_mongodb(collectionName: str, strdt: date, enddt: date):
    try:
        MONGO_URI = f'mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOSTNAME}'
        mongo_client = MongoClient(MONGO_URI)
        db = mongo_client[MONGO_DB_NAME]
        date_list = [(strdt+timedelta(days=x)).isoformat().replace('-', '') for x in range((enddt-strdt).days + 1)]
        collection = db[collectionName.replace('/','_')]
        data = []
        for _date in date_list:
            if(collection.find_one({"_id": _date})):
                data.append(collection.find_one({"_id": _date}))
        return data
    except Exception as e:
        logging.exception(e)


def get_latest_ten_readings_from_redis(keyName: str) -> Union[List[ReadingModel], int]:
    try:
        key = f'last_ten_{keyName.replace("/","_")}'
        redis_conn = redis.StrictRedis(host = REDIS_DB_HOSTNAME)
        if redis_conn.exists(key) != 0:
            readings: List[bytes] = redis_conn.lrange(name=key, start=0, end=-1) # type: ignore
        else:
            return -1
        return [convert_data_to_reading_model(json.loads(reading)) for reading in readings]
    except Exception as e:
        logging.exception(e)
        return -1
    

def convert_data_to_reading_model(json_data: dict) -> ReadingModel:
    return ReadingModel(**json_data)

