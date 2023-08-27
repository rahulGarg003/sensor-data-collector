# sourcery skip: use-fstring-for-formatting
import os
import time
import json
import paho.mqtt.client as mqtt

from logger import logging
from utils import MongoDB

time.sleep(10)

MQQT_HOSTNAME = os.environ.get("MQQT_HOSTNAME", 'localhost')
MQQT_PORT = int(os.environ.get("MQQT_PORT", 1883))
MQQT_TOPIC = os.environ.get('MQQT_TOPIC','sensor/#')
MONGO_DB_USERNAME = os.environ.get('MONGO_DB_USERNAME')
MONGO_DB_PASSWORD = os.environ.get('MONGO_DB_PASSWORD')
MONGO_DB_HOSTNAME = os.environ.get('MONGO_DB_HOSTNAME')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME')

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQQT_TOPIC)

def on_message(client, userdata, msg):
    logging.info(f"Received message: {msg.topic} - {str(msg.payload)}")
    mongodb = MongoDB(
        host=MONGO_DB_HOSTNAME, 
        userName=MONGO_DB_USERNAME, 
        password=MONGO_DB_PASSWORD,
        dbName=MONGO_DB_NAME    
    )
    mongodb.insert_data_to_collection(
        collectionName=msg.topic,
        message=msg.payload
    )

# Create MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

while True:
    try:
        mqtt_client.connect(host=MQQT_HOSTNAME, port=MQQT_PORT)
        mqtt_client.loop_start()
        while True:
            pass
    except KeyboardInterrupt:
        mqtt_client.loop_stop()
        break
    except Exception as e:
        logging.error(e)
        time.sleep(2)
        

