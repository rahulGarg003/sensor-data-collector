
# Sensor Data Collector

Simulate the behaviour of sensors, monitor their readings and APIs to retrieve data based sensor.

# Dependency #

- Python 3.8
    - Please refer below for Aditional Package details
        - [python:3.8-alpine](https://hub.docker.com/_/python) Docker Official Image
        - [Sensor-Simulator](https://github.com/rahulGarg003/sensor-data-collector/blob/main/sensor-simulator/requirements.txt) requirements
        - [Data-Collector](https://github.com/rahulGarg003/sensor-data-collector/blob/main/data-collector/requirements.txt) requirements
        - [Web-API](https://github.com/rahulGarg003/sensor-data-collector/blob/main/web-api/requirements.txt) requirements

- [eclipse-mosquitto:2.0.16](https://hub.docker.com/_/eclipse-mosquitto) Docker Official Image
    - Required to send data from Sensor to the server

- [mongo:7.0.1-rc0-jammy](https://hub.docker.com/_/mongo) Docker Official Image
    - Required to store sensor data

- [redis:7.2.0-alpine3.18](https://hub.docker.com/_/redis)
    - Required to cache data in memory

# How to clone #

To clone the repository, go to the path to download the repository. 
```
# clone the repository 
git clone https://github.com/rahulGarg003/sensor-data-collector.git
```

# How to build #

## Build with Docker

You can use the Docker container to avoid building all the dependencies yourself. 
1. Install Docker on [Linux](https://docs.docker.com/install/).
2. Navigate to the repository. 
    ```
    cd sensor-data-collector
    ```
3. Build and Run Docker Containers
    ```
    docker compose up
    ```

# How to use APIs

Open Any Browser and Please read API docs
```
http://127.0.0.1:5000/api/v1/docs/
or
http://localhost:5000/api/v1/docs/
```

# Design

![Solution Design Diagram](https://github.com/rahulGarg003/sensor-data-collector/blob/main/Solution%20Design.jpg)

# Insights of Services in docker-compose.yml
1. Mosquitto MQQT Broker
    - This is used as a broker between publisher and subscriber

2. Sensor Simulator
    - This is used to simulate the sensor behaviour and send data to MQTT Broker
    - Dependancy
        - Python-3.8
        - paho-mqtt Python library
    - [Dockerfile](https://github.com/rahulGarg003/sensor-data-collector/blob/main/sensor-simulator/Dockerfile)
    - Message Schema
        - { "sensor_id": "unique_sensor_id", "value": "<reading_value>", "timestamp": "ISO8601_formatted_date_time" }

3. Data Collector
    - This is used as subscriber of the MQTT Broker and store data to MongoDB and cache data to Redis
    - Dependancy
        - Python-3.8
        - paho-mqtt==1.6.1
        - pymongo
        - redis
    - [Dockerfile](https://github.com/rahulGarg003/sensor-data-collector/blob/main/data-collector/Dockerfile)

4. MongoDB
    - This is used to store data
    - Data Store Schema
        - [{"_id": "20230101", Value: [Message1, Message2, ...]}, {"_id": "20230102", Value: [Message1, Message2, ...]}, ...]

5. Redis
    - This is used to cache last 10 readings in memory
    - Data Store Schema
        - key1: [message1, message2, ...]
        - key2: [message1, message2, ...]
    

