from pydantic import BaseModel
from datetime import datetime
from enum import Enum
import os

class ReadingModel(BaseModel):
    sensor_id: str
    value: float
    timestamp: datetime

class TopicEnum(str, Enum):
    temperature = 'temperature'
    humidity = 'humidity'

class MQQTTopicName(Enum):
    temperature = os.environ.get('MQQT_TOPIC_TEMPERATURE','sensor/temperature')
    humidity = os.environ.get('MQQT_TOPIC_HUMIDITY', 'sensor/humidity')
