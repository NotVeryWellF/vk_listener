from kafka import KafkaProducer
from fastapi import FastAPI
import logging
import time
import json


def connect_to_kafka(app: FastAPI):
    """Creates connection to kafka"""
    while True:
        time.sleep(1)
        try:
            producer = KafkaProducer(bootstrap_servers=['kafka:9093'], value_serializer=json_serializer)
            app.state.producer = producer
            break
        except Exception as e:
            logging.warning("--Kafka Connection Error--")
            logging.warning(e)


def close_kafka_connection(app: FastAPI) -> None:
    """Close connection with kafka"""
    try:
        app.state.producer.close()
    except Exception as e:
        logging.warning("--Kafka Disconnection Error--")
        logging.warning(e)


def produce_to_topic(topic: str, app: FastAPI, data):
    """Sends data to kafka topic: posts"""
    app.state.producer.send(topic, data)


def json_serializer(data):
    """Serializer for data"""
    return json.dumps(data).encode("utf-8")
