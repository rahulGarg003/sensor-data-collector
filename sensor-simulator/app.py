import os
import paho.mqtt.client as mqtt
from datetime import datetime
import time
from logger import logging
from random import randint

sensor_id = os.environ.get('SENSOR-ID', 1)
mqtt_broker_host = os.environ.get("MQQT-HOSTNAME", 'localhost')
mqtt_broker_port = int(os.environ.get("MQQT-PORT", 1883))
# mqtt_broker_username = 'mqtt-admin'
# mqtt_broker_password = 'mqtt-admin'
mqtt_topic_temprature = os.environ.get('MQQT-TOPIC-TEMPRATURE','sensor/temprature')
mqtt_topic_humidity = os.environ.get('MQQT-TOPIC-HUMIDITY', 'sensor/humidity')


# Establish connection with MQTT Broker Server
def create_mqtt_client() -> mqtt.Client:
    logging.info(f'trying to create mqqt client with HostName -> {mqtt_broker_host} and Port -> {mqtt_broker_port}')
    client = mqtt.Client(client_id=sensor_id)
    # client.username_pw_set(username=mqtt_broker_username, password=mqtt_broker_password)
    # client.on_connect = on_connect
    # client.on_message = on_message
    client.connect(host=mqtt_broker_host, port=mqtt_broker_port)
    logging.info('Connection to mqtt broker Successfully established')

    return client


# def on_connect(client, userdata, flags, rc):
#     logging.error('-------------Connect Call-------------------')
#     print(client)
#     print(userdata)
#     print(flags)
#     print(rc)

# def on_message(client, userdata, msg):
#     logging.error("--------------Message Call------------------")
#     print(client)
#     print(userdata)
#     print(msg)
#     print(f"{msg.topic} {str(msg.payload)}")



client = create_mqtt_client()
client.loop_start()
while True:
    # Reading for Temprature
    message_payload = {
        "sensor_id": F'{sensor_id}-{mqtt_topic_temprature}', 
        "value": randint(5, 50), 
        "timestamp": datetime.now().isoformat()
    }
    logging.info(str(message_payload))
    msginfo = client.publish(
        topic = mqtt_topic_temprature, 
        payload = str(message_payload)
    )
    time.sleep(2)

    # Reading for Humidity
    message_payload = {
        "sensor_id": F'{sensor_id}-{mqtt_topic_humidity}', 
        "value": randint(40, 100), 
        "timestamp": datetime.now().isoformat()
    }
    logging.info(str(message_payload))
    msginfo = client.publish(
        topic = mqtt_topic_humidity, 
        payload = str(message_payload)
    )
    time.sleep(5)

# client.loop_forever()

