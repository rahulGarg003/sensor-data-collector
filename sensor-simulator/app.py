import os
import paho.mqtt.client as mqtt
from datetime import datetime
import time
import sqlite3

from logger import logging
from utils import get_temprature_data, get_humidity_data, insert_unpublished_data_to_db

time.sleep(10)

SENSOR_ID = os.environ.get('SENSOR_ID', 1)
MQQT_HOSTNAME = os.environ.get("MQQT_HOSTNAME", 'localhost')
MQQT_PORT = int(os.environ.get("MQQT_PORT", 1883))
# mqtt_broker_username = 'mqtt-admin'
# mqtt_broker_password = 'mqtt-admin'
MQQT_TOPIC_TEMPRATURE = os.environ.get('MQQT_TOPIC_TEMPRATURE','sensor/temprature')
MQQT_TOPIC_HUMIDITY = os.environ.get('MQQT_TOPIC_HUMIDITY', 'sensor/humidity')

def on_connect(client, userdata, flags, rc):
    data_temprature = get_temprature_data(sensor_id=f'{SENSOR_ID}-{MQQT_TOPIC_TEMPRATURE}')
    logging.info(data_temprature)
    try:
        client.publish(
            topic = MQQT_TOPIC_TEMPRATURE, 
            payload = data_temprature
        )
    except Exception as e:
        logging.exception(e)
        insert_unpublished_data_to_db(MQQT_TOPIC_TEMPRATURE, data_temprature)

    data_humidity = get_humidity_data(sensor_id=f'{SENSOR_ID}-{MQQT_TOPIC_HUMIDITY}')
    logging.info(data_humidity)
    try:
        client.publish(
            topic = MQQT_TOPIC_HUMIDITY, 
            payload = data_humidity
        )
    except Exception as e:
        logging.error("Not able to publish message to MQTT Broker, saving data to local db")
        insert_unpublished_data_to_db(MQQT_TOPIC_HUMIDITY, data_humidity)

    time.sleep(5)

def on_connect_fail():
    data_temprature = get_temprature_data(sensor_id=f'{SENSOR_ID}-{MQQT_TOPIC_TEMPRATURE}')
    logging.info(data_temprature)
    insert_unpublished_data_to_db(MQQT_TOPIC_TEMPRATURE, data_temprature)
    
    data_humidity = get_humidity_data(sensor_id=f'{SENSOR_ID}-{MQQT_TOPIC_HUMIDITY}')
    logging.info(data_humidity)
    insert_unpublished_data_to_db(MQQT_TOPIC_HUMIDITY, data_humidity)


client = mqtt.Client(client_id=SENSOR_ID)
# client.username_pw_set(username=mqtt_broker_username, password=mqtt_broker_password)
client.on_connect = on_connect

while True:
    try:
        client.connect(host=MQQT_HOSTNAME, port=MQQT_PORT)
        client.loop_start()
    except KeyboardInterrupt:
        client.loop_stop()
        break
    except Exception as e:
        logging.error("Failed to connect to MQTT Broker, saving data to local db")
        on_connect_fail()
        time.sleep(5)
    finally:
        client.loop_stop()
        client.disconnect()


