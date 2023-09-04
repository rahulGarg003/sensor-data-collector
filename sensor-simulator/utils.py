import os
import json
from random import randint
from datetime import datetime, timedelta, timezone
import sqlite3

from logger import logging

def get_temprature_data(sensor_id):
    data = {
        "sensor_id": sensor_id, 
        "value": randint(5, 50), 
        "timestamp": datetime.now(
                        tz=timezone(
                            offset=timedelta(
                                hours=float(os.environ.get('TIMEZONE_OFFSET_HOURS', 5)),
                                minutes=float(os.environ.get('TIMEZONE_OFFSET_MINUTES', 30))
                            )
                        )
                    ).isoformat()
    }
    return json.dumps(data)

def get_humidity_data(sensor_id):
    data = {
        "sensor_id": sensor_id, 
        "value": randint(40, 100), 
        "timestamp": datetime.now(
                        tz=timezone(
                            offset=timedelta(
                                hours=float(os.environ.get('TIMEZONE_OFFSET_HOURS', 5)),
                                minutes=float(os.environ.get('TIMEZONE_OFFSET_MINUTES', 30))
                            )
                        )
                    ).isoformat()
    }
    return json.dumps(data)

def insert_unpublished_data_to_db(msg_topic, msg_payload):
    SQL_DB_NAME = os.environ.get('SQL_DB_NAME', 'data')
    SQL_DB_TABLE_NAME = os.environ.get('SQL_DB_TABLE_NAME', 'data')

    db_file_path = os.path.join(os.getcwd(), 'data')
    try:
        os.makedirs(db_file_path, exist_ok=True)
        with sqlite3.connect(f'{db_file_path}/{SQL_DB_NAME}.db') as conn:
            cur = conn.cursor()
            query = f"""CREATE TABLE IF NOT EXISTS {SQL_DB_TABLE_NAME} (
                            id INTEGER PRIMARY KEY autoincrement,
                            message_topic TEXT,
                            message_payload TEXT
                        )"""
            cur.execute(query)
            query = f"""INSERT INTO {SQL_DB_TABLE_NAME} 
                        (message_topic, message_payload) 
                        VALUES 
                        ('{msg_topic}', '{msg_payload}')
                    """
            cur.execute(query)
    except Exception as e:
        logging.exception(e)
    
def publish_data_from_local_db(client):
    SQL_DB_NAME = os.environ.get('SQL_DB_NAME', 'data')
    SQL_DB_TABLE_NAME = os.environ.get('SQL_DB_TABLE_NAME', 'data')

    db_file_path = os.path.join(os.getcwd(), 'data')

    try:
        with sqlite3.connect(f'{db_file_path}/{SQL_DB_NAME}.db') as conn:
            cur = conn.cursor()
            query = f"""SELECT * FROM {SQL_DB_TABLE_NAME}"""
            cur.execute(query)

            output = cur.fetchall()
            for row in output:
                try:
                    logging.info(f"publishing from local db: {row}")
                    client.publish(
                        topic = f'{row[1]}_localdb', 
                        payload = row[2],
                    )
                    logging.info("data published to local db")
                    query = f"DELETE FROM {SQL_DB_TABLE_NAME} WHERE id = {row[0]}"
                    cur.execute(query)
                    logging.info(f"record deleted to local db: {row}")
                except Exception as e:
                    logging.exception(e)
                    raise
                

    except Exception as e:
        logging.exception(e)
