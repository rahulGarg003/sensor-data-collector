from fastapi import FastAPI
from models import MQQTTopicName, TopicEnum
from datetime import date

from utils import get_latest_ten_readings_from_redis, get_data_from_mongodb

api_route = FastAPI()

@api_route.get('/sensor/{reading_type}/top$10')
def get_latest_10_readings(reading_type: TopicEnum):
    return get_latest_ten_readings_from_redis(MQQTTopicName[reading_type].value)

@api_route.get('/sensor/{reading_type}/')
def get_sensor_readings(reading_type: TopicEnum, strdt: date, enddt: date):
    return get_data_from_mongodb(
        collectionName=MQQTTopicName[reading_type].value,
        strdt=strdt,
        enddt=enddt
    )