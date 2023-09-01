# sourcery skip: use-fstring-for-formatting
import os
import time
import json
import paho.mqtt.client as mqtt

from logger import logging
from utils import insert_data_to_mongodb_collection, cache_last_ten_readings_to_redis

time.sleep(10)

MQQT_HOSTNAME = os.environ.get("MQQT_HOSTNAME", 'localhost')
MQQT_PORT = int(os.environ.get("MQQT_PORT", 1883))
MQQT_TOPIC = os.environ.get('MQQT_TOPIC','sensor/#')


def on_connect(client, userdata, flags, rc):
    client.subscribe(MQQT_TOPIC)

def on_message(client, userdata, msg):
    logging.info(f"Received message: {msg.topic} - {str(msg.payload)}")

    insert_data_to_mongodb_collection(
        collectionName=msg.topic.replace('_localdb',''),
        message=msg.payload
    )

    if('_localdb' not in msg.topic):
        cache_last_ten_readings_to_redis(keyName=f'last_ten_{msg.topic}', message=msg.payload)


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
        

